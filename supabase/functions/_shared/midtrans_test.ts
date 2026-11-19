import { strict as assert } from 'node:assert'
import { configuredEnvironment, gatewayRequest, midtransOrderTime, MidtransApiError, qrUrl, validOrderId, validQrUrl, validSignature, validateGatewayStatus } from './midtrans.ts'

const order = { order_id: 'OSNGEO-SB-' + 'a'.repeat(32), nominal: 50000 }
const status = {
  order_id: order.order_id, transaction_id: '00000000-0000-0000-0000-000000000001',
  gross_amount: '50000.00', transaction_status: 'settlement', status_code: '200',
  payment_type: 'qris', currency: 'IDR',
}

Deno.test('optional signature verification uses the separate signature secret', async () => {
  const body = { order_id: order.order_id, status_code: '200', gross_amount: '50000.00', signature_key: '' }
  const digest = await crypto.subtle.digest('SHA-512', new TextEncoder().encode(body.order_id + body.status_code + body.gross_amount + 'test-key'))
  body.signature_key = [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('')
  assert.equal(await validSignature(body, 'test-key'), true)
  assert.equal(await validSignature({ ...body, gross_amount: '1.00' }, 'test-key'), false)
  assert.equal(await validSignature(body, 'wrong-key'), false)
  assert.equal(await validSignature({ ...body, signature_key: 'bad' }, 'test-key'), false)
  assert.equal(await validSignature(body, 'new-server-api-key'), false)
})

Deno.test('verification rejects mismatched amount, order, currency, and payment method', () => {
  assert.equal(validateGatewayStatus(status, order).transaction_status, 'settlement')
  for (const changes of [{ gross_amount: '1.00' }, { gross_amount: '5e4' }, { order_id: 'other' },
    { currency: 'USD' }, { payment_type: 'gopay' }, { transaction_id: '' }]) {
    assert.throws(() => validateGatewayStatus({ ...status, ...changes }, order))
  }
})

Deno.test('a notification signature alone does not authenticate the payment status', async () => {
  // The integration must always GET the status, even with a correct signature.
  const body = { order_id: order.order_id, status_code: '200', gross_amount: '50000.00', signature_key: '' }
  const digest = await crypto.subtle.digest('SHA-512', new TextEncoder().encode(body.order_id + body.status_code + body.gross_amount + 'test-key'))
  body.signature_key = [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('')
  assert.equal(await validSignature({ ...body, transaction_status: 'settlement' }, 'test-key'), true)
  assert.equal(await validSignature({ ...body, transaction_status: 'pending' }, 'test-key'), true)
})

Deno.test('sandbox is default; a malformed environment cannot turn on production', () => {
  assert.equal(configuredEnvironment(undefined), 'sandbox')
  assert.equal(configuredEnvironment('production'), 'production')
  assert.throws(() => configuredEnvironment('prod'))
  assert.equal(validOrderId(order.order_id), true)
  assert.equal(validOrderId('../../status'), false)
})

Deno.test('custom expiry uses GMT+7 without changing the order instant', () => {
  assert.equal(midtransOrderTime('2026-11-19T03:42:20.369666+00:00'), '2026-11-19 10:42:20 +0700')
  assert.equal(midtransOrderTime('2026-11-19T20:00:00Z'), '2026-11-20 03:00:00 +0700')
  assert.equal(midtransOrderTime('2026-11-19T10:42:20+07:00'), '2026-11-19 10:42:20 +0700')
})

Deno.test('provider errors expose only a safe code and explanation, never provider payloads', async () => {
  const originalFetch = globalThis.fetch
  globalThis.fetch = (() => Promise.resolve(new Response(JSON.stringify({
    status_code: '402', status_message: 'sensitive-provider-payload',
    error_messages: ['sensitive-provider-payload'],
  }), { status: 402 }))) as typeof fetch
  try {
    await assert.rejects(() => gatewayRequest('sandbox', 'test-key', '/v2/charge', {}), error => {
      assert.ok(error instanceof MidtransApiError)
      assert.equal(error.gatewayCode, '402')
      assert.equal(error.httpStatus, 402)
      assert.ok(error.message.includes('QRIS belum tersedia'))
      assert.ok(!error.message.includes('sensitive-provider-payload'))
      return true
    })
  } finally { globalThis.fetch = originalFetch }
})

Deno.test('QR images are restricted to the matching Midtrans API environment', () => {
  assert.equal(validQrUrl('https://api.midtrans.com/v2/qris/tx/qr-code', 'production'), true)
  assert.equal(validQrUrl('https://api.midtrans.com/v4/qris/tx/qr-code', 'production'), true)
  assert.equal(validQrUrl('https://api.midtrans.com/v40/qris/tx/qr-code', 'production'), false)
  assert.equal(validQrUrl('https://api.sandbox.midtrans.com/v2/qris/tx/qr-code', 'production'), false)
  assert.equal(validQrUrl('https://evil.example/v2/qris/tx/qr-code', 'sandbox'), false)
  assert.equal(validQrUrl('https://user:pass@api.midtrans.com/v2/qris/tx/qr-code', 'production'), false)
  assert.equal(qrUrl({ ...status, actions: [
    { name: 'generate-qr-code', url: 'https://api.sandbox.midtrans.com/v2/qris/tx/qr-code' },
    { name: 'generate-qr-code-v2', url: 'https://api.sandbox.midtrans.com/v4/qris/tx/qr-code' },
  ] }, 'sandbox'), 'https://api.sandbox.midtrans.com/v4/qris/tx/qr-code')
})

Deno.test('gateway requests retrieve authoritative status and never send keys to a different host', async () => {
  const originalFetch = globalThis.fetch
  let calls = 0
  globalThis.fetch = ((url: string | URL | Request, init?: RequestInit) => {
    calls++
    assert.equal(String(url), `https://api.sandbox.midtrans.com/v2/${order.order_id}/status`)
    assert.equal(init?.method, 'GET')
    assert.equal((init?.headers as Record<string, string>).Authorization, 'Basic ' + btoa('test-key:'))
    return Promise.resolve(new Response(JSON.stringify(status), { status: 200 }))
  }) as typeof fetch
  try {
    assert.equal((await gatewayRequest('sandbox', 'test-key', `/v2/${order.order_id}/status`)).transaction_status, 'settlement')
    assert.equal(calls, 1)
  } finally { globalThis.fetch = originalFetch }
})
