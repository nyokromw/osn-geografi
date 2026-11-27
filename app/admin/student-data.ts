import { supabase } from '../lib/supabase'

export type StudentProfile = {
  id: string
  nama: string | null
  email: string | null
  provinsi: string | null
  nomor_hp: string | null
  role: string | null
  status: string | null
  status_expired: string | null
  created_at: string | null
}

const columns = 'id, nama, email, provinsi, nomor_hp, role, status, status_expired, created_at'
const studentRoles = 'role.neq.admin,role.is.null'
const paidPlans = ['pemula', 'premium', 'platinum']
const week = 7 * 86_400_000
export const studentPageSize = 25

export const studentSortOptions = {
  terbaru: { label: 'Terbaru bergabung', column: 'created_at', ascending: false },
  terlama: { label: 'Terlama bergabung', column: 'created_at', ascending: true },
  namaAZ: { label: 'Nama A–Z', column: 'nama', ascending: true },
  namaZA: { label: 'Nama Z–A', column: 'nama', ascending: false },
  provinsi: { label: 'Provinsi A–Z', column: 'provinsi', ascending: true },
  berakhir: { label: 'Tanggal berakhir paling awal', column: 'status_expired', ascending: true },
} as const

export const defaultStudentFilters = {
  search: '',
  province: '',
  role: '',
  status: '',
  sort: 'terbaru' as keyof typeof studentSortOptions,
}

function activeExpiry(now: string) {
  return 'status_expired.is.null,status_expired.gt.' + now
}

export async function loadStudentOverview() {
  const now = new Date()
  const since = new Date(now.getTime() - week).toISOString()
  const countStudents = () => supabase.from('profiles').select('id', { count: 'exact', head: true }).or(studentRoles)
  const [total, registered, pemula, premium, platinum, submissions] = await Promise.all([
    countStudents(),
    countStudents().gte('created_at', since),
    countStudents().eq('status', 'pemula').or(activeExpiry(now.toISOString())),
    countStudents().eq('status', 'premium').or(activeExpiry(now.toISOString())),
    countStudents().eq('status', 'platinum').or(activeExpiry(now.toISOString())),
    supabase.from('hasil_to').select('id', { count: 'exact', head: true }).gte('created_at', since),
  ])
  return {
    total: total.count,
    registered: registered.count,
    pemula: pemula.count,
    premium: premium.count,
    platinum: platinum.count,
    submissions: submissions.count,
  }
}

export function loadStudentPage(filters: typeof defaultStudentFilters, page: number, signal: AbortSignal) {
  const now = new Date()
  const cutoff = now.toISOString()
  const query = supabase.from('profiles').select(columns, { count: 'exact' })

  const search = filters.search.trim()
  if (search) {
    // Quote the PostgREST value and escape regex operators for a literal, case-insensitive search.
    const literal = JSON.stringify(search.replace(/[\\^$.*+?()[\]{}|]/g, '\\$&'))
    query.or(['nama', 'email', 'nomor_hp'].map(column => column + '.imatch.' + literal).join(','))
  }
  if (filters.province === 'kosong') query.is('provinsi', null)
  else if (filters.province) query.eq('provinsi', filters.province)

  if (filters.role === 'siswa') query.or(studentRoles)
  else if (filters.role === 'admin') query.eq('role', 'admin')

  switch (filters.status) {
    case 'gratis':
      query.or('status.is.null,status.not.in.(pemula,premium,platinum),and(status.in.(pemula,premium,platinum),status_expired.lte.' + cutoff + ')')
      break
    case 'pemula':
    case 'premium':
    case 'platinum':
      query.eq('status', filters.status).or(activeExpiry(cutoff))
      break
    case 'akanHabis':
      query.in('status', paidPlans).gt('status_expired', cutoff)
        .lte('status_expired', new Date(now.getTime() + week).toISOString())
      break
    case 'habis':
      query.in('status', paidPlans).lte('status_expired', cutoff)
  }

  const { column, ascending } = studentSortOptions[filters.sort]
  const start = page * studentPageSize
  return query.order(column, { ascending, nullsFirst: false })
    .order('id').range(start, start + studentPageSize - 1).abortSignal(signal)
}
