import { createClient } from 'npm:@supabase/supabase-js@2.106.2'
import { configuredEnvironment, gatewayRequest, qrUrl, validOrderId, validSignature, validateGatewayStatus,
  type Environment, type GatewayStatus } from '../_shared/midtrans.ts'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Cache-Control': 'no-store',
}

const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), {
  status, headers: { ...corsHeaders, 'Content-Type': 'application/json' },
})

function serverKey(environment: Environment) {
  return Deno.env.get(environment === 'production' ? 'MIDTRANS_PRODUCTION_SERVER_KEY' : 'MIDTRANS_SANDBOX_SERVER_KEY') ?? ''
}

function publicOrder(order: Record<string, unknown>) {
  // No customer information or provider payload is returned to the browser.
  const keys = ['order_id', 'environment', 'nama_paket', 'akses', 'durasi_hari', 'nominal', 'status',
    'qr_url', 'expires_at', 'paid_at', 'fulfilled_at', 'membership_ends_at', 'review_reason', 'created_at']
  return Object.fromEntries(keys.map(key => [key, order[key]]))
}

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders })
  if (req.method !== 'POST') return json({ error: 'Metode tidak didukung.' }, 405)
  try {
    if (Number(req.headers.get('content-length') ?? 0) > 65536) return json({ error: 'Permintaan terlalu besar.' }, 413)
    const text = await req.text()
    if (text.length > 65536) return json({ error: 'Permintaan terlalu besar.' }, 413)
    let body: Record<string, unknown>
    try {
      body = JSON.parse(text)
      if (!body || typeof body !== 'object' || Array.isArray(body)) throw new Error('Invalid body')
    } catch { return json({ error: 'Format permintaan tidak valid.' }, 400) }

    const projectUrl = Deno.env.get('SUPABASE_URL')!
    const serviceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')
      ?? JSON.parse(Deno.env.get('SUPABASE_SECRET_KEYS') ?? '{}').default
    const db = createClient(projectUrl, serviceKey, { auth: { persistSession: false, autoRefreshToken: false } })

    async function findOrder(orderId: unknown, userId?: string) {
      if (!validOrderId(orderId)) return null
      let query = db.from('pembayaran_midtrans').select('*').eq('order_id', orderId)
      if (userId) query = query.eq('user_id', userId)
      const { data, error } = await query.maybeSingle()
      if (error) throw error
      return data
    }

    async function reconcile(order: NonNullable<Awaited<ReturnType<typeof findOrder>>>, data: GatewayStatus) {
      const verified = validateGatewayStatus(data, order)
      const { data: payment, error } = await db.rpc('midtrans_reconcile_order', {
        p_order_id: order.order_id, p_environment: order.environment,
        p_nominal: Number(verified.gross_amount), p_transaction_id: verified.transaction_id,
        p_payment_type: verified.payment_type, p_status: verified.transaction_status,
        p_status_code: verified.status_code, p_fraud_status: verified.fraud_status ?? null,
        p_currency: verified.currency,
      })
      if (error) throw error
      if (payment.status === 'pending' && !payment.qr_url) {
        const image = qrUrl(verified, order.environment)
        if (image) {
          const { error: imageError } = await db.from('pembayaran_midtrans').update({ qr_url: image })
            .eq('id', order.id).in('status', ['created', 'pending'])
          if (imageError) throw imageError
          payment.qr_url = image
        }
      }
      return payment
    }

    // Midtrans notifications do not contain an action or Supabase user token.
    if (body.action === undefined) {
      const order = await findOrder(body.order_id)
      // Acknowledge other orders on the same merchant account without touching them.
      if (!order) return json({ received: true })
      const key = serverKey(order.environment)
      if (!key) return json({ error: 'Konfigurasi pembayaran belum lengkap.' }, 503)
      // Since 28 Oct 2026, notification signatures use a separate Signature Secret Key.
      // It is optional here: authenticated GET Status is always the source of truth,
      // matching the verification method used by the official Midtrans libraries.
      const signatureSecret = Deno.env.get(order.environment === 'production'
        ? 'MIDTRANS_PRODUCTION_SIGNATURE_SECRET_KEY' : 'MIDTRANS_SANDBOX_SIGNATURE_SECRET_KEY')
      if (signatureSecret && !await validSignature(body, signatureSecret)) {
        return json({ error: 'Notifikasi tidak valid.' }, 401)
      }
      // Never use a status or amount supplied by the caller to grant access.
      const status = await gatewayRequest(order.environment, key, `/v2/${encodeURIComponent(order.order_id)}/status`)
      if (!status) return json({ error: 'Status transaksi belum tersedia.' }, 503)
      await reconcile(order, status)
      return json({ received: true })
    }

    const environment = configuredEnvironment(Deno.env.get('MIDTRANS_ENVIRONMENT'))
    const live = environment === 'production' && Deno.env.get('MIDTRANS_PAYMENTS_ENABLED') === 'true'
      && !!serverKey('production')
    const authorization = req.headers.get('Authorization') ?? ''
    const token = authorization.startsWith('Bearer ') ? authorization.slice(7) : ''
    const { data: { user } } = token ? await db.auth.getUser(token) : { data: { user: null } }
    let isAdmin = false
    if (user) {
      const { data: profile, error } = await db.from('profiles').select('role').eq('id', user.id).single()
      if (error) throw error
      isAdmin = profile?.role === 'admin'
    }
    if (body.action === 'config') return json({ available: live,
      test_available: isAdmin && environment === 'sandbox' && !!serverKey('sandbox'), environment })
    if (!user) return json({ error: 'Silakan masuk ke akun OSNGEO.id.' }, 401)

    if (body.action === 'create') {
      if (!Number.isSafeInteger(body.paket_id) || Number(body.paket_id) <= 0) return json({ error: 'Paket tidak valid.' }, 400)
      if (!live && !(isAdmin && environment === 'sandbox' && serverKey('sandbox'))) {
        return json({ error: 'Pembayaran QRIS sedang disiapkan. Hubungi admin untuk membeli paket.' }, 503)
      }
      const { data: created, error } = await db.rpc('midtrans_create_order', {
        p_user_id: user.id, p_paket_id: body.paket_id, p_environment: environment,
      })
      if (error) return json({ error: error.message }, 400)
      const order = created.order
      if (order.qr_url) return json({ order: publicOrder(order) })
      const key = serverKey(environment)
      if (!created.is_new) {
        const current = await gatewayRequest(environment, key, `/v2/${encodeURIComponent(order.order_id)}/status`)
        if (current) return json({ order: publicOrder(await reconcile(order, current)) })
        // A concurrent checkout owns a newly-created order. Avoid duplicate charge requests.
        if (Date.now() - Date.parse(order.created_at) < 30000) return json({ order: publicOrder(order) })
      }
      const { data: customer, error: customerError } = await db.from('profiles').select('nama, nomor_hp')
        .eq('id', user.id).single()
      if (customerError) throw customerError
      const status = await gatewayRequest(environment, key, '/v2/charge', {
        payment_type: 'qris', qris: { acquirer: 'gopay' },
        transaction_details: { order_id: order.order_id, gross_amount: order.nominal },
        item_details: [{ id: String(order.paket_id), price: order.nominal, quantity: 1, name: order.nama_paket }],
        customer_details: { first_name: customer?.nama?.slice(0, 100) || 'Peserta OSNGEO',
          email: user.email, ...(customer?.nomor_hp ? { phone: customer.nomor_hp } : {}) },
        custom_expiry: { order_time: new Date(order.created_at).toISOString().replace('T', ' ').slice(0, 19) + ' +0000',
          expiry_duration: 15, unit: 'minute' },
      })
      if (!status) throw new Error('Charge unavailable')
      return json({ order: publicOrder(await reconcile(order, status)) })
    }
    if (body.action === 'status') {
      const order = await findOrder(body.order_id, user.id)
      if (!order) return json({ error: 'Pesanan tidak ditemukan.' }, 404)
      if (order.environment === 'sandbox' && !isAdmin) return json({ error: 'Pesanan tidak ditemukan.' }, 404)
      const key = serverKey(order.environment)
      if (!key) return json({ error: 'Konfigurasi pembayaran belum lengkap. Hubungi admin.' }, 503)
      // Also fetch status for already paid orders when requested: refunds remain visible.
      const status = await gatewayRequest(order.environment, key, `/v2/${encodeURIComponent(order.order_id)}/status`)
      if (!status && order.status === 'created' && Date.parse(order.expires_at) <= Date.now()) {
        const { data: expired, error } = await db.from('pembayaran_midtrans').update({ status: 'expired' })
          .eq('id', order.id).eq('status', 'created').select('*').maybeSingle()
        if (error) throw error
        return json({ order: publicOrder(expired ?? order) })
      }
      return json({ order: publicOrder(status ? await reconcile(order, status) : order) })
    }
    return json({ error: 'Permintaan tidak dikenal.' }, 400)
  } catch (error) {
    // Never log provider bodies, auth headers, server keys, or customer details.
    console.error('Midtrans operation failed:', error instanceof Error ? error.name : 'UnknownError')
    return json({ error: 'Pembayaran belum dapat diproses. Coba cek status kembali atau hubungi admin.' }, 503)
  }
})
