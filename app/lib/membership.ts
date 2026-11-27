export const adminWhatsApp = 'https://wa.me/6285809937263'

export const accessLabels = { gratis: 'Gratis', premium: 'Premium', platinum: 'Platinum' } as const
export type AccessLevel = keyof typeof accessLabels

const accessRank: Record<AccessLevel, number> = { gratis: 0, premium: 1, platinum: 2 }

export type MembershipPlan = {
  id: number
  nama: string
  harga: number
  durasi_hari: number | null
  deskripsi: string | null
  fitur: unknown
  akses: AccessLevel
  aktif: boolean | null
  jenis?: 'perorangan' | 'kelas' | null
  kuota_siswa?: number | null
}

const rupiahFormatter = new Intl.NumberFormat('id-ID')

export function rupiah(amount: number) {
  return `Rp${rupiahFormatter.format(amount)}`
}

export function membershipFeatures(value: unknown): string[] {
  const features = typeof value === 'string' ? value.split('\n') : value
  return Array.isArray(features) ? features.flatMap(item => (
    typeof item === 'string' && item.trim() ? [item.trim()] : []
  )) : []
}

export function planWhatsAppLink(plan: MembershipPlan) {
  const action = plan.aktif ? 'memesan' : 'menanyakan ketersediaan'
  const message = plan.jenis === 'kelas'
    ? `Halo, saya guru dan ingin ${action} ${plan.nama} (${rupiah(plan.harga)}) di OSNGEO.id.\nNama sekolah/lembaga: \nEmail akun guru di OSNGEO: `
    : `Halo, saya ingin ${action} paket ${plan.nama} (${rupiah(plan.harga)}) di OSNGEO.id.\nEmail akun OSNGEO saya: `
  return `${adminWhatsApp}?text=${encodeURIComponent(message)}`
}

export function membershipExpiry(value: string) {
  // Supabase stores this timestamp in UTC without returning a timezone suffix.
  return Date.parse(/(?:Z|[+-]\d{2}:?\d{2})$/i.test(value) ? value : `${value}Z`)
}

export function activeAccess(profile: { status: string | null; status_expired: string | null } | null): AccessLevel {
  const status = profile?.status
  if (status !== 'premium' && status !== 'platinum') return 'gratis'
  const expiry = profile?.status_expired
  return !expiry || membershipExpiry(expiry) > Date.now() ? status : 'gratis'
}

export function requiredAccess(content: { akses?: string | null; is_premium?: boolean | null }, media = false): AccessLevel {
  if (content.akses === 'platinum') return 'platinum'
  if (content.akses === 'premium' || content.is_premium) return media ? 'platinum' : 'premium'
  return 'gratis'
}

export function bisaAkses(user: AccessLevel, content: AccessLevel) {
  return accessRank[user] >= accessRank[content]
}
