import { supabase } from './supabase'

export type PaymentConfig = { available: boolean; test_available: boolean; environment: 'sandbox' | 'production'; booking_mode?: 'whatsapp' | 'qris' }
export type PaymentOrder = {
  order_id: string
  environment: 'sandbox' | 'production'
  nama_paket: string
  akses: 'pemula' | 'premium' | 'platinum'
  durasi_hari: number
  nominal: number
  status: 'created' | 'pending' | 'paid' | 'expired' | 'failed' | 'review' | 'refunded'
  qr_url: string | null
  expires_at: string
  paid_at: string | null
  fulfilled_at: string | null
  membership_ends_at: string | null
  review_reason: string | null
  created_at: string
}

export const paymentStatusLabels: Record<PaymentOrder['status'], string> = {
  created: 'Menyiapkan pembayaran', pending: 'Menunggu pembayaran', paid: 'Lunas',
  expired: 'Kedaluwarsa', failed: 'Tidak berhasil', review: 'Perlu peninjauan', refunded: 'Dana dikembalikan',
}

export async function paymentRequest<T>(body: Record<string, unknown>): Promise<T> {
  const { data, error } = await supabase.functions.invoke('midtrans-payment', { body })
  if (error) {
    let message = 'Layanan pembayaran belum dapat dihubungi. Coba kembali atau hubungi admin.'
    if (error.context instanceof Response) {
      try { message = (await error.context.json()).error || message } catch { /* No JSON error response. */ }
    }
    throw new Error(message)
  }
  return data as T
}

export async function paymentConfig(): Promise<PaymentConfig> {
  try { return await paymentRequest<PaymentConfig>({ action: 'config' }) }
  catch { return { available: false, test_available: false, environment: 'sandbox' } }
}

export function paymentDate(value: string) {
  return new Intl.DateTimeFormat('id-ID', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'Asia/Jakarta' })
    .format(new Date(value)) + ' WIB'
}

export function safePaymentReturn(value: string | null) {
  if (!value || !value.startsWith('/pembayaran?') || value.includes('\\')) return '/dashboard'
  return value
}
