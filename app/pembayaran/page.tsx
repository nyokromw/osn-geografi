'use client'

import Link from 'next/link'
import { useCallback, useEffect, useRef, useState } from 'react'
import { CheckCircle2, QrCode, RefreshCw } from 'lucide-react'
import { Notice, PageLoading, WorkspaceHeader } from '../components/atlas'
import { accessLabels, activeAccess, adminWhatsApp, membershipExpiry, planWhatsAppLink, rupiah, type MembershipPlan } from '../lib/membership'
import { paymentConfig, paymentDate, paymentRequest, paymentStatusLabels, type PaymentConfig, type PaymentOrder } from '../lib/payments'
import { supabase } from '../lib/supabase'

export default function PaymentPage() {
  const [loading, setLoading] = useState(true)
  const [plan, setPlan] = useState<MembershipPlan | null>(null)
  const [config, setConfig] = useState<PaymentConfig | null>(null)
  const [order, setOrder] = useState<PaymentOrder | null>(null)
  const [profile, setProfile] = useState<{ status: string | null; status_expired: string | null } | null>(null)
  const [busy, setBusy] = useState(false)
  const [notice, setNotice] = useState('')
  const polling = useRef(false)
  const [remaining, setRemaining] = useState<number | null>(null)

  useEffect(() => {
    let active = true
    async function init() {
      try {
        const { data: { user } } = await supabase.auth.getUser()
        if (!user) {
          window.location.replace('/login?next=' + encodeURIComponent(window.location.pathname + window.location.search))
          return
        }
        const params = new URLSearchParams(window.location.search)
        const orderId = params.get('pesanan')
        const planId = Number(params.get('paket'))
        const settings = await paymentConfig()
        if (!active) return
        setConfig(settings)
        if (orderId) {
          const result = await paymentRequest<{ order: PaymentOrder }>({ action: 'status', order_id: orderId })
          if (active) setOrder(result.order)
        } else if (Number.isSafeInteger(planId) && planId > 0) {
          const [selection, account] = await Promise.all([
            supabase.from('paket_membership').select('*').eq('id', planId).eq('aktif', true).single(),
            supabase.from('profiles').select('status, status_expired').eq('id', user.id).single(),
          ])
          if (!selection.data || selection.data.harga <= 0 || selection.data.akses === 'gratis') {
            throw new Error('Paket tidak tersedia. Pilih kembali paket di dashboard.')
          }
          if (account.error) throw new Error('Profil akun gagal dimuat. Muat ulang halaman untuk mencoba lagi.')
          if (active) { setPlan(selection.data); setProfile(account.data) }
        } else throw new Error('Pilih paket melalui halaman Paket dan akses.')
      } catch (error) {
        if (active) setNotice(error instanceof Error ? error.message : 'Pembayaran gagal dimuat.')
      } finally { if (active) setLoading(false) }
    }
    void init()
    return () => { active = false }
  }, [])

  const checkStatus = useCallback(async (orderId: string, manual = false) => {
    if (polling.current) return
    polling.current = true
    if (manual) { setBusy(true); setNotice('') }
    try {
      const result = await paymentRequest<{ order: PaymentOrder }>({ action: 'status', order_id: orderId })
      setOrder(result.order)
      if (manual && ['created', 'pending'].includes(result.order.status)) {
        setNotice('Pembayaran belum terkonfirmasi. Jika sudah membayar, tunggu sebentar lalu cek kembali.')
      }
    } catch (error) {
      if (manual) setNotice(error instanceof Error ? error.message : 'Status belum dapat diperiksa.')
    } finally { polling.current = false; if (manual) setBusy(false) }
  }, [])

  const pending = order && ['created', 'pending'].includes(order.status)
  useEffect(() => {
    if (!order || !pending) return
    const orderId = order.order_id
    const interval = window.setInterval(() => {
      if (document.visibilityState === 'visible') void checkStatus(orderId)
    }, 10000)
    const focus = () => { void checkStatus(orderId) }
    window.addEventListener('focus', focus)
    return () => { window.clearInterval(interval); window.removeEventListener('focus', focus) }
  }, [order?.order_id, pending, checkStatus]) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!order || !pending) return
    const expiresAt = Date.parse(order.expires_at)
    const update = () => setRemaining(Math.max(0, Math.ceil((expiresAt - Date.now()) / 1000)))
    update()
    const timer = window.setInterval(update, 1000)
    return () => window.clearInterval(timer)
  }, [order?.expires_at, pending]) // eslint-disable-line react-hooks/exhaustive-deps

  async function createPayment() {
    if (!plan || busy) return
    setBusy(true); setNotice('')
    try {
      const result = await paymentRequest<{ order: PaymentOrder }>({ action: 'create', paket_id: plan.id })
      setOrder(result.order)
      window.history.replaceState({}, '', '/pembayaran?pesanan=' + encodeURIComponent(result.order.order_id))
    } catch (error) {
      setNotice(error instanceof Error ? error.message : 'Pembayaran belum dapat dibuat.')
    } finally { setBusy(false) }
  }

  if (loading) return <PageLoading>Memuat pembayaran…</PageLoading>
  const canPay = config?.available || config?.test_available
  const currentAccess = activeAccess(profile)
  const renewing = !!plan && currentAccess === plan.akses && !!profile?.status_expired
  const upgraded = !!plan && currentAccess === 'premium' && plan.akses === 'platinum'
  const paid = order?.status === 'paid'
  const sandbox = order?.environment === 'sandbox' || (!order && config?.test_available)
  const imageAllowed = order?.qr_url && (() => {
    try {
      const url = new URL(order.qr_url)
      return url.origin === (order.environment === 'production' ? 'https://api.midtrans.com' : 'https://api.sandbox.midtrans.com')
        && /^\/v(?:2|4)\/qris\//.test(url.pathname) && !url.username && !url.password
    } catch { return false }
  })()

  return (
    <>
      <WorkspaceHeader title="Pembayaran">
        <Link className="atlas-link text-sm" href="/dashboard?tab=paket">Paket dan akses</Link>
      </WorkspaceHeader>
      <main className="atlas-container py-10 sm:py-16">
        <section className="atlas-card mx-auto max-w-xl p-5 sm:p-8" aria-labelledby="payment-title">
          <span className="access-badge mb-4" data-access={order?.akses ?? plan?.akses ?? 'gratis'}>
            {order ? accessLabels[order.akses] : plan ? accessLabels[plan.akses] : 'OSNGEO.id'}
          </span>
          <h1 id="payment-title" className="text-2xl font-bold text-forest-900">
            {paid ? 'Pembayaran berhasil' : order ? paymentStatusLabels[order.status] : 'Pembayaran paket'}
          </h1>
          {sandbox && <div className="mt-4"><Notice>Mode uji admin. Gunakan simulator Midtrans; pembayaran simulasi tidak mengubah akses akun.</Notice></div>}
          {(order || plan) && <div className="my-6 space-y-2 border-y border-gray-200 py-5 text-sm">
            <div className="flex justify-between gap-4"><span>Paket</span><strong>{order?.nama_paket ?? plan?.nama}</strong></div>
            <div className="flex justify-between gap-4"><span>Masa aktif</span><strong>{order?.durasi_hari ?? plan?.durasi_hari} hari</strong></div>
            <div className="flex justify-between gap-4 text-lg"><span>Total pembayaran</span><strong>{rupiah(order?.nominal ?? plan?.harga ?? 0)}</strong></div>
          </div>}
          {notice && <div className="my-4"><Notice error>{notice}</Notice></div>}
          {!order && plan && <>
            <p className="mb-5 text-sm leading-relaxed text-gray-600">
              {renewing ? `Masa aktif akan ditambahkan setelah ${paymentDate(new Date(membershipExpiry(profile!.status_expired!)).toISOString())}.`
                : 'Masa aktif dimulai setelah pembayaran berhasil diverifikasi.'}
              {upgraded && ' Upgrade memulai masa aktif Platinum yang baru. Sisa masa aktif Premium tidak dikonversi.'}
            </p>
            {canPay ? <button type="button" disabled={busy} onClick={createPayment}
              className="atlas-button atlas-button--primary w-full">
              <QrCode size={18} aria-hidden="true" />{busy ? 'Menyiapkan pembayaran…' : sandbox ? 'Buat QRIS uji' : 'Bayar dengan QRIS'}
            </button> : <>
              <Notice>Pembayaran QRIS sedang disiapkan. Pemesanan paket tetap tersedia melalui admin.</Notice>
              <a className="atlas-button atlas-button--primary mt-4 w-full" href={planWhatsAppLink(plan)} target="_blank" rel="noreferrer">Hubungi admin</a>
            </>}
          </>}
          {order && <>
            <p className="break-all text-xs text-gray-500">Nomor pesanan: {order.order_id}</p>
            {pending && <>
              {imageAllowed && (remaining === null || remaining > 0) ? <div className="my-5 text-center">
                {/* eslint-disable-next-line @next/next/no-img-element -- QRIS image is rendered by the payment provider. */}
                <img src={order.qr_url!} width={340} height={400} className="mx-auto h-auto max-w-full" alt="Kode QRIS pembayaran pesanan OSNGEO.id" />
                <p className="mt-3 text-sm text-gray-600">Pindai melalui aplikasi bank atau dompet digital yang mendukung QRIS.</p>
                <a href={order.qr_url!} target="_blank" rel="noreferrer" className="atlas-link mt-3 inline-block text-sm">Buka gambar QRIS untuk disimpan</a>
              </div> : <p className="my-5 text-sm text-gray-600">{remaining === 0 ? 'Waktu pembayaran telah habis. Periksa status sebelum membuat pesanan baru.' : 'Kode pembayaran sedang disiapkan. Periksa status kembali dalam beberapa saat.'}</p>}
              {remaining !== null && remaining > 0 && <p className="my-4 text-center text-sm tabular-nums">Sisa waktu {Math.floor(remaining / 60)}:{String(remaining % 60).padStart(2, '0')}</p>}
              <button className="atlas-button atlas-button--primary mt-4 w-full" type="button" disabled={busy}
                onClick={() => void checkStatus(order.order_id, true)}><RefreshCw size={16} aria-hidden="true" />{busy ? 'Memeriksa…' : 'Cek status pembayaran'}</button>
              <p className="mt-3 text-sm text-gray-600">Status diperiksa otomatis selama halaman ini terbuka. Anda juga bisa melanjutkan dari riwayat pembayaran.</p>
            </>}
            {paid && <div className="my-5 space-y-3 text-sm leading-relaxed">
              <CheckCircle2 className="text-forest-600" size={32} aria-hidden="true" />
              <p>{sandbox ? 'Simulasi pembayaran berhasil. Akses akun tidak berubah.' : `Paket ${accessLabels[order.akses]} sudah aktif.`}</p>
              {order.membership_ends_at && <p>Berlaku hingga <strong>{paymentDate(order.membership_ends_at)}</strong>.</p>}
              <Link className="atlas-button atlas-button--primary w-full" href="/dashboard?tab=paket">Buka dashboard</Link>
            </div>}
            {order.review_reason && <div className="my-5"><Notice>{order.review_reason}</Notice>
              <a className="atlas-button mt-4" href={`${adminWhatsApp}?text=${encodeURIComponent('Halo, mohon bantu tinjau pesanan OSNGEO.id ' + order.order_id)}`} target="_blank" rel="noreferrer">Hubungi admin</a></div>}
            {['expired', 'failed'].includes(order.status) && <Link className="atlas-button mt-5 w-full" href="/dashboard?tab=paket">Pilih paket kembali</Link>}
          </>}
          {!plan && !order && <Link className="atlas-button mt-5 w-full" href="/dashboard?tab=paket">Lihat paket</Link>}
        </section>
      </main>
    </>
  )
}
