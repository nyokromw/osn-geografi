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

export function validQrUrl(value: string, environment: Environment) {
  try {
    const url = new URL(value)
    return url.origin === apiBase(environment) && url.pathname.startsWith('/v2/qris/')
      && !url.username && !url.password
  } catch { return false }
}

export function qrUrl(status: GatewayStatus, environment: Environment) {
  const action = status.actions?.find(item => item.name === 'generate-qr-code-v2')
    ?? status.actions?.find(item => item.name === 'generate-qr-code')
  if (action && validQrUrl(action.url, environment)) return action.url
  // GET Status need not repeat actions. This image endpoint is documented by Midtrans.
  if (/^[a-zA-Z0-9-]{1,100}$/.test(status.transaction_id)) {
    return `${apiBase(environment)}/v2/qris/${status.transaction_id}/qr-code`
  }
  return null
}

export async function validSignature(body: Record<string, unknown>, serverKey: string) {
  const { order_id, status_code, gross_amount, signature_key } = body
  if (typeof order_id !== 'string' || typeof status_code !== 'string'
    || typeof gross_amount !== 'string' || typeof signature_key !== 'string'
    || !/^[a-f0-9]{128}$/i.test(signature_key)) return false
  const digest = await crypto.subtle.digest('SHA-512', new TextEncoder().encode(
    `${order_id}${status_code}${gross_amount}${serverKey}`,
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
    throw new Error('Midtrans request failed')
  }
  return data
}
