// Paket Kelas accounts. Needs the service role, so it runs here and not in the browser.
//   create          (admin)        make a class: guru gets class access, N student accounts are created
//   reset_password  (guru / admin) give a student a new generated password
import { createClient } from 'npm:@supabase/supabase-js@2.106.2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Cache-Control': 'no-store',
}
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), {
  status, headers: { ...corsHeaders, 'Content-Type': 'application/json' },
})

export const STUDENT_EMAIL_DOMAIN = 'siswa.osngeo.id'
const LEVEL: Record<string, number> = { gratis: 0, premium: 1, platinum: 2 }

// Readable passwords: no 0/O, 1/l/I. 8 chars from 55 symbols ≈ 46 bits.
export function generatePassword(length = 8) {
  const alphabet = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  const bytes = crypto.getRandomValues(new Uint32Array(length))
  return Array.from(bytes, b => alphabet[b % alphabet.length]).join('')
}

export const validCode = (kode: unknown): kode is string => typeof kode === 'string' && /^[a-z][a-z0-9]{2,15}$/.test(kode)

// UTC "YYYY-MM-DD HH:MM:SS" for `timestamp without time zone` columns.
const utc = (date: Date) => date.toISOString().slice(0, 19).replace('T', ' ')

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders })
  if (req.method !== 'POST') return json({ error: 'Metode tidak didukung.' }, 405)
  try {
    const text = await req.text()
    if (text.length > 16384) return json({ error: 'Permintaan terlalu besar.' }, 413)
    let body: Record<string, unknown>
    try {
      body = JSON.parse(text)
      if (!body || typeof body !== 'object' || Array.isArray(body)) throw new Error('Invalid body')
    } catch { return json({ error: 'Format permintaan tidak valid.' }, 400) }

    const projectUrl = Deno.env.get('SUPABASE_URL')!
    const serviceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')
      ?? JSON.parse(Deno.env.get('SUPABASE_SECRET_KEYS') ?? '{}').default
    const db = createClient(projectUrl, serviceKey, { auth: { persistSession: false, autoRefreshToken: false } })

    const authorization = req.headers.get('Authorization') ?? ''
    const token = authorization.startsWith('Bearer ') ? authorization.slice(7) : ''
    const { data: { user } } = token ? await db.auth.getUser(token) : { data: { user: null } }
    if (!user) return json({ error: 'Silakan masuk ke akun OSNGEO.id.' }, 401)
    const { data: caller, error: callerError } = await db.from('profiles').select('role').eq('id', user.id).single()
    if (callerError) throw callerError
    const isAdmin = caller?.role === 'admin'

    // ---------------------------------------------------------------- create a class (admin)
    if (body.action === 'create') {
      if (!isAdmin) return json({ error: 'Hanya admin yang dapat membuat Paket Kelas.' }, 403)
      const nama = typeof body.nama === 'string' ? body.nama.trim() : ''
      const guruEmail = typeof body.guru_email === 'string' ? body.guru_email.trim().toLowerCase() : ''
      const kode = typeof body.kode === 'string' ? body.kode.trim().toLowerCase() : ''
      const kuota = Number(body.kuota ?? 10)
      const durasi = Number(body.durasi_hari ?? 365)
      const akses = body.akses === 'premium' ? 'premium' : 'platinum'
      if (nama.length < 2 || nama.length > 120) return json({ error: 'Nama kelas/sekolah 2–120 karakter.' }, 400)
      if (!validCode(kode)) return json({ error: 'Kode username: huruf kecil/angka, 3–16 karakter, diawali huruf.' }, 400)
      if (!Number.isInteger(kuota) || kuota < 1 || kuota > 50) return json({ error: 'Jumlah siswa 1–50.' }, 400)
      if (!Number.isInteger(durasi) || durasi < 1 || durasi > 730) return json({ error: 'Durasi 1–730 hari.' }, 400)

      const { data: guru, error: guruError } = await db.from('profiles')
        .select('id, nama, role, status, status_expired').ilike('email', guruEmail).maybeSingle()
      if (guruError) throw guruError
      if (!guru) return json({ error: 'Akun guru dengan email itu belum terdaftar. Minta guru mendaftar di osngeo.id dulu.' }, 404)

      const usernames = Array.from({ length: kuota }, (_, i) => kode + String(i + 1).padStart(2, '0'))
      const [{ data: usedCode }, { data: usedNames }] = await Promise.all([
        db.from('kelas').select('id').eq('kode', kode).maybeSingle(),
        db.from('profiles').select('username').in('username', usernames),
      ])
      if (usedCode || (usedNames ?? []).length) return json({ error: 'Kode username sudah dipakai. Pilih kode lain.' }, 409)

      const ends = new Date(Date.now() + durasi * 86400000)
      const { data: kelas, error: kelasError } = await db.from('kelas').insert({
        nama, guru_id: guru.id, akses, kuota, kode, berlaku_sampai: utc(ends), dibuat_oleh: user.id,
      }).select('*').single()
      if (kelasError) throw kelasError

      const created: string[] = []
      const credentials: { username: string; password: string }[] = []
      try {
        for (const [i, username] of usernames.entries()) {
          const password = generatePassword()
          const { data: account, error } = await db.auth.admin.createUser({
            email: `${username}@${STUDENT_EMAIL_DOMAIN}`, password, email_confirm: true,
            user_metadata: { nama: `Siswa ${i + 1}` },
          })
          if (error || !account.user) throw error ?? new Error('createUser failed')
          created.push(account.user.id)
          const { error: profileError } = await db.from('profiles').update({
            username, sekolah: nama, status: akses, status_expired: utc(ends),
          }).eq('id', account.user.id)
          if (profileError) throw profileError
          const { error: memberError } = await db.from('kelas_anggota').insert({
            kelas_id: kelas.id, user_id: account.user.id, username, password_awal: password,
          })
          if (memberError) throw memberError
          credentials.push({ username, password })
        }
      } catch (error) {
        // All-or-nothing: remove what was created so the admin can retry cleanly.
        for (const id of created) await db.auth.admin.deleteUser(id).catch(() => {})
        await db.from('kelas').delete().eq('id', kelas.id)
        throw error
      }

      // The guru gets the same access, never lowered and never shortened.
      if (guru.role !== 'admin') {
        const current = guru.status_expired ? Date.parse(guru.status_expired + 'Z') : 0
        const keepCurrent = (LEVEL[guru.status ?? 'gratis'] ?? 0) > LEVEL[akses] && current > Date.now()
        if (!keepCurrent) {
          const { error } = await db.from('profiles').update({
            status: akses, status_expired: utc(new Date(Math.max(ends.getTime(), (guru.status === akses ? current : 0)))),
          }).eq('id', guru.id)
          if (error) throw error
        }
      }
      return json({ kelas: { id: kelas.id, nama, kode, kuota, akses, berlaku_sampai: kelas.berlaku_sampai }, guru: { nama: guru.nama }, credentials })
    }

    // ---------------------------------------------------------------- reset a student's password (guru / admin)
    if (body.action === 'reset_password') {
      const studentId = typeof body.user_id === 'string' ? body.user_id : ''
      const { data: member, error } = await db.from('kelas_anggota')
        .select('user_id, username, kelas:kelas_id(guru_id)').eq('user_id', studentId).maybeSingle()
      if (error) throw error
      const guruId = (member?.kelas as { guru_id?: string } | null)?.guru_id
      if (!member || (!isAdmin && guruId !== user.id)) return json({ error: 'Siswa tidak ditemukan di kelas Anda.' }, 404)
      const password = generatePassword()
      const { error: authError } = await db.auth.admin.updateUserById(member.user_id, { password })
      if (authError) throw authError
      const { error: saveError } = await db.from('kelas_anggota').update({ password_awal: password }).eq('user_id', member.user_id)
      if (saveError) throw saveError
      return json({ username: member.username, password })
    }

    return json({ error: 'Aksi tidak dikenal.' }, 400)
  } catch (error) {
    console.error('kelas-admin', error instanceof Error ? error.message : 'error')
    return json({ error: 'Terjadi kesalahan. Coba lagi atau hubungi admin.' }, 500)
  }
})
