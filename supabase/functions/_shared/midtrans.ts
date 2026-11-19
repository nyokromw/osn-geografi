export type Environment = 'sandbox' | 'production'

export type GatewayStatus = {
  order_id: string
  transaction_id: string
  gross_amount: string
  transaction_status: string
  status_code: string
  payment_type: string
  currency: string
  fraud_status?: string
  actions?: { name: string; url: string }[]
}

export function apiBase(environment: Environment) {
  return environment === 'production' ? 'https://api.midtrans.com' : 'https://api.sandbox.midtrans.com'
}

export function validOrderId(value: unknown): value is string {
  return typeof value === 'string' && /^OSNGEO-(SB|PR)-[a-f0-9]{32}$/.test(value)
}

export function configuredEnvironment(value: string | undefined): Environment {
  // Fail closed: a typo must not silently select live payments.
  if (value && value !== 'sandbox' && value !== 'production') throw new Error('Invalid Midtrans environment')
  return value === 'production' ? 'production' : 'sandbox'
}

export function midtransOrderTime(value: string) {
  // Core API requires the custom-expiry timestamp in GMT+7.
  const localTime = new Date(Date.parse(value) + 7 * 60 * 60 * 1000)
  return localTime.toISOString().replace('T', ' ').slice(0, 19) + ' +0700'
}

export class MidtransApiError extends Error {
  readonly gatewayCode: string
  readonly httpStatus: number
  constructor(httpStatus: number, code: unknown) {
    const safeCode = /^\d{3}$/.test(String(code)) ? String(code) : String(httpStatus)
    const explanations: Record<string, string> = {
      '400': 'Midtrans menolak format data pembayaran. Hubungi admin untuk memeriksa integrasi.',
      '401': 'Midtrans menolak Server Key. Pastikan kunci sesuai dengan mode Sandbox atau Production.',
      '402': 'QRIS belum tersedia untuk akun Midtrans ini. Periksa aktivasi metode pembayaran QRIS.',
      '403': 'Permintaan ditolak Midtrans. Periksa izin Core API Write pada Server Key dan pengaturan integrasi.',
      '406': 'Nomor pesanan sudah terdaftar. Cek status pembayaran sebelum membuat pesanan baru.',
      '408': 'Midtrans menolak tipe data pembayaran. Hubungi admin untuk memeriksa integrasi.',
      '429': 'Batas permintaan Midtrans tercapai. Tunggu sebentar lalu coba kembali.',
    }
    super(`${explanations[safeCode] ?? 'Midtrans belum dapat memproses pembayaran. Coba kembali atau hubungi admin.'} (kode ${safeCode})`)
    this.name = 'MidtransApiError'
    this.gatewayCode = safeCode
    this.httpStatus = httpStatus
  }
}

export function validQrUrl(value: string, environment: Environment) {
  try {
    const url = new URL(value)
    return url.origin === apiBase(environment) && /^\/v(?:2|4)\/qris\//.test(url.pathname)
      && !url.username && !url.password
  } catch { return false }
}

export function qrUrl(status: GatewayStatus, environment: Environment) {
  for (const name of ['generate-qr-code-v2', 'generate-qr-code']) {
    const action = status.actions?.find(item => item.name === name && validQrUrl(item.url, environment))
    if (action) return action.url
  }
  // GET Status need not repeat actions. This image endpoint is documented by Midtrans.
  if (/^[a-zA-Z0-9-]{1,100}$/.test(status.transaction_id)) {
    return `${apiBase(environment)}/v2/qris/${status.transaction_id}/qr-code`
  }
  return null
}

export async function validSignature(body: Record<string, unknown>, signatureSecretKey: string) {
  const { order_id, status_code, gross_amount, signature_key } = body
  if (typeof order_id !== 'string' || typeof status_code !== 'string'
    || typeof gross_amount !== 'string' || typeof signature_key !== 'string'
    || !/^[a-f0-9]{128}$/i.test(signature_key)) return false
  const digest = await crypto.subtle.digest('SHA-512', new TextEncoder().encode(
    `${order_id}${status_code}${gross_amount}${signatureSecretKey}`,
  ))
  const expected = [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('')
  let mismatch = 0
  const actual = signature_key.toLowerCase()
  for (let i = 0; i < expected.length; i++) mismatch |= expected.charCodeAt(i) ^ actual.charCodeAt(i)
  return mismatch === 0
}

export function validateGatewayStatus(value: unknown, order: { order_id: string; nominal: number }): GatewayStatus {
  if (!value || typeof value !== 'object') throw new Error('Invalid gateway response')
  const data = value as GatewayStatus
  if (data.order_id !== order.order_id || typeof data.transaction_id !== 'string' || !data.transaction_id
    || !/^\d+(?:\.0{1,2})?$/.test(String(data.gross_amount))
    || Number(data.gross_amount) !== order.nominal || data.payment_type !== 'qris'
    || data.currency !== 'IDR' || typeof data.transaction_status !== 'string'
    || typeof data.status_code !== 'string') throw new Error('Payment does not match order')
  return data
}

export async function gatewayRequest(environment: Environment, serverKey: string, path: string, body?: unknown) {
  const response = await fetch(`${apiBase(environment)}${path}`, {
    method: body ? 'POST' : 'GET',
    headers: {
      Authorization: `Basic ${btoa(`${serverKey}:`)}`,
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
    signal: AbortSignal.timeout(12000),
  })
  const data = await response.json()
  // Midtrans can return a business error in a JSON response; check both layers.
  if (response.status === 404 || data.status_code === '404') return null
  if (!response.ok || !['200', '201', '202', '407'].includes(data.status_code)) {
    throw new MidtransApiError(response.status, data.status_code)
  }
  return data
}
