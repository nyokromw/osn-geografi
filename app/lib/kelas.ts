import { supabase } from './supabase'

/** Paket Kelas student accounts sign in with a username; their auth email lives on this (unmailed) domain. */
export const STUDENT_EMAIL_DOMAIN = 'siswa.osngeo.id'

/** "smansa01" → "smansa01@siswa.osngeo.id"; a real email is used as typed. */
export function loginEmail(identifier: string) {
  const value = identifier.trim()
  return value.includes('@') ? value : `${value.toLowerCase()}@${STUDENT_EMAIL_DOMAIN}`
}

export const isStudentAccountEmail = (email: string | null | undefined) =>
  !!email && email.toLowerCase().endsWith('@' + STUDENT_EMAIL_DOMAIN)

export type Kelas = {
  id: string
  nama: string
  guru_id: string
  akses: 'premium' | 'platinum'
  kuota: number
  kode: string
  berlaku_sampai: string
  created_at: string
}

export type KelasAnggota = {
  kelas_id: string
  user_id: string
  username: string
  password_awal: string | null
  created_at: string
}

export type Credential = { username: string; password: string }

export async function kelasRequest<T>(body: Record<string, unknown>): Promise<T> {
  const { data, error } = await supabase.functions.invoke('kelas-admin', { body })
  if (error) {
    let message = 'Layanan kelas belum dapat dihubungi. Coba lagi.'
    if (error.context instanceof Response) {
      try { message = (await error.context.json()).error || message } catch { /* No JSON error body. */ }
    }
    throw new Error(message)
  }
  return data as T
}

/** A printable sheet of login cards, opened in its own window. */
export function printLoginCards(kelasNama: string, rows: { username: string; password: string | null; nama?: string | null }[]) {
  const esc = (value: string) => value.replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]!))
  const cards = rows.map(row => `
    <article>
      <p class="brand">OSNGEO<span>.id</span></p>
      <p class="kelas">${esc(kelasNama)}</p>
      ${row.nama && !/^Siswa \d+$/.test(row.nama) ? `<p class="nama">${esc(row.nama)}</p>` : ''}
      <dl>
        <dt>Username</dt><dd>${esc(row.username)}</dd>
        <dt>Kata sandi</dt><dd>${row.password ? esc(row.password) : '<em>sudah diganti siswa</em>'}</dd>
      </dl>
      <p class="url">Masuk di <strong>osngeo.id/login</strong>, lalu ganti nama & kata sandi di menu Akun.</p>
    </article>`).join('')
  const win = window.open('', '_blank', 'width=900,height=700')
  if (!win) return false
  win.document.write(`<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Kartu login · ${esc(kelasNama)}</title>
<style>
  *{box-sizing:border-box} body{margin:24px;font-family:system-ui,sans-serif;color:#162923}
  h1{font-size:18px;margin:0 0 16px} .grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
  article{border:1.5px dashed #628775;border-radius:12px;padding:14px 16px;break-inside:avoid}
  .brand{margin:0;font-weight:800;font-size:16px}.brand span{color:#983f29}
  .kelas{margin:2px 0 8px;font-size:12px;color:#52655d}.nama{margin:0 0 6px;font-weight:700}
  dl{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;margin:0;font-size:14px}
  dt{color:#52655d}dd{margin:0;font-family:ui-monospace,monospace;font-weight:700;font-size:16px}
  .url{margin:10px 0 0;font-size:11px;color:#52655d}
  @media print{body{margin:10mm}h1{display:none}}
</style></head><body><h1>Kartu login ${esc(kelasNama)} · potong per kartu</h1><div class="grid">${cards}</div>
<script>window.onload=()=>window.print()</script></body></html>`)
  win.document.close()
  return true
}
