'use client'

import { useEffect, useState, type FormEvent } from 'react'
import { Copy, Printer } from 'lucide-react'
import { Notice } from '../components/atlas'
import { accessLabels } from '../lib/membership'
import { kelasRequest, printLoginCards, type Credential, type Kelas } from '../lib/kelas'
import { supabase } from '../lib/supabase'

type KelasRow = Kelas & { guru: { nama: string | null; email: string | null } | null; kelas_anggota: { count: number }[] }
type Created = { kelas: { nama: string; kode: string; berlaku_sampai: string }; guru: { nama: string | null }; credentials: Credential[] }

const fmt = (value: string) => new Intl.DateTimeFormat('id-ID', { dateStyle: 'medium' }).format(new Date(value.endsWith('Z') ? value : value + 'Z'))
const suggestCode = (nama: string) => nama.toLowerCase().normalize('NFD').replace(/[^a-z0-9]/g, '').replace(/^[0-9]+/, '').slice(0, 10)

/** Admin: create a Paket Kelas after payment and hand the logins to the guru. */
export function ClassAdmin() {
  const [rows, setRows] = useState<KelasRow[]>([])
  const [form, setForm] = useState({ nama: '', guru_email: '', kode: '', kuota: 10, durasi_hari: 365, akses: 'platinum' })
  const [codeTouched, setCodeTouched] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [created, setCreated] = useState<Created | null>(null)

  const [revision, setRevision] = useState(0)
  useEffect(() => {
    let active = true
    void supabase.from('kelas')
      .select('*, guru:profiles!kelas_guru_id_fkey(nama, email), kelas_anggota(count)')
      .order('created_at', { ascending: false })
      .then(({ data }) => { if (active) setRows((data ?? []) as unknown as KelasRow[]) })
    return () => { active = false }
  }, [revision])

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (saving) return
    if (!window.confirm(`Buat Paket Kelas "${form.nama}" dengan ${form.kuota} akun siswa (${form.kode}01–${form.kode}${String(form.kuota).padStart(2, '0')})?`)) return
    setSaving(true); setError(''); setCreated(null)
    try {
      const result = await kelasRequest<Created>({ action: 'create', ...form })
      setCreated(result)
      setForm({ nama: '', guru_email: '', kode: '', kuota: 10, durasi_hari: 365, akses: 'platinum' }); setCodeTouched(false)
      setRevision(r => r + 1)
    } catch (e) { setError(e instanceof Error ? e.message : 'Gagal membuat kelas.') }
    finally { setSaving(false) }
  }

  const credentialText = created
    ? `Login OSNGEO.id · ${created.kelas.nama}\nosngeo.id/login\n\n` + created.credentials.map(c => `${c.username} / ${c.password}`).join('\n')
    : ''
  const field = 'w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400'

  return (
    <div className="grid gap-6">
      <div>
        <h2 className="text-xl font-black text-gray-800">Paket Kelas</h2>
        <p className="text-sm text-gray-500">Setelah guru membayar, buat kelasnya di sini. Guru harus sudah punya akun OSNGEO (daftar dengan email).
          Akun siswa dibuat otomatis; guru melihat username & kata sandi di dashboard tab <strong>Kelas saya</strong>.</p>
      </div>

      <form onSubmit={submit} className="grid gap-3 rounded-xl border border-gray-200 bg-white p-4 sm:grid-cols-2">
        <label className="grid gap-1 text-sm font-semibold text-gray-700">Nama sekolah / kelas
          <input className={field} required minLength={2} maxLength={120} placeholder="SMAN 1 Bandar Lampung" value={form.nama}
            onChange={e => setForm({ ...form, nama: e.target.value, kode: codeTouched ? form.kode : suggestCode(e.target.value) })} />
        </label>
        <label className="grid gap-1 text-sm font-semibold text-gray-700">Email akun guru
          <input className={field} type="email" required placeholder="guru@sekolah.sch.id" value={form.guru_email}
            onChange={e => setForm({ ...form, guru_email: e.target.value })} />
        </label>
        <label className="grid gap-1 text-sm font-semibold text-gray-700">Kode username
          <input className={field + ' font-mono'} required pattern="[a-z][a-z0-9]{2,15}" title="Huruf kecil/angka, 3–16 karakter, diawali huruf"
            value={form.kode} onChange={e => { setCodeTouched(true); setForm({ ...form, kode: e.target.value.toLowerCase().replace(/[^a-z0-9]/g, '') }) }} />
          <span className="text-xs font-normal text-gray-500">Username siswa: {form.kode || 'kode'}01, {form.kode || 'kode'}02, …</span>
        </label>
        <div className="grid grid-cols-3 gap-2">
          <label className="grid gap-1 text-sm font-semibold text-gray-700">Siswa
            <input className={field} type="number" min={1} max={50} value={form.kuota} onChange={e => setForm({ ...form, kuota: Number(e.target.value) })} />
          </label>
          <label className="grid gap-1 text-sm font-semibold text-gray-700">Hari
            <input className={field} type="number" min={1} max={730} value={form.durasi_hari} onChange={e => setForm({ ...form, durasi_hari: Number(e.target.value) })} />
          </label>
          <label className="grid gap-1 text-sm font-semibold text-gray-700">Akses
            <select className={field} value={form.akses} onChange={e => setForm({ ...form, akses: e.target.value })}>
              <option value="platinum">Platinum</option><option value="premium">Premium</option>
            </select>
          </label>
        </div>
        {error && <div className="sm:col-span-2"><Notice error>{error}</Notice></div>}
        <div className="sm:col-span-2">
          <button className="atlas-button atlas-button--primary" type="submit" disabled={saving}>{saving ? 'Membuat akun…' : 'Buat kelas & akun siswa'}</button>
        </div>
      </form>

      {created && (
        <section className="rounded-xl border-2 border-forest-400 bg-forest-50 p-4">
          <h3 className="font-bold">Kelas {created.kelas.nama} dibuat · berlaku sampai {fmt(created.kelas.berlaku_sampai)}</h3>
          <p className="mt-1 text-sm text-gray-600">Guru ({created.guru.nama}) juga melihat daftar ini di tab Kelas saya. Kirimkan atau cetak sekarang.</p>
          <div className="mt-3 flex flex-wrap gap-2">
            <button type="button" className="atlas-button" onClick={() => navigator.clipboard.writeText(credentialText)}><Copy size={15} aria-hidden="true" /> Salin</button>
            <button type="button" className="atlas-button" onClick={() => printLoginCards(created.kelas.nama, created.credentials)}><Printer size={15} aria-hidden="true" /> Cetak kartu</button>
          </div>
          <pre className="mt-3 overflow-x-auto rounded-lg bg-white p-3 text-sm">{credentialText}</pre>
        </section>
      )}

      <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
        <table className="classroom-table">
          <thead><tr><th>Kelas</th><th>Guru</th><th>Kode</th><th>Siswa</th><th>Akses</th><th>Berlaku sampai</th></tr></thead>
          <tbody>
            {rows.map(row => (
              <tr key={row.id}>
                <td><strong>{row.nama}</strong></td>
                <td>{row.guru?.nama}<span className="block text-xs text-gray-500">{row.guru?.email}</span></td>
                <td className="font-mono">{row.kode}</td>
                <td>{row.kelas_anggota?.[0]?.count ?? 0}/{row.kuota}</td>
                <td>{accessLabels[row.akses]}</td>
                <td>{fmt(row.berlaku_sampai)}</td>
              </tr>
            ))}
            {!rows.length && <tr><td colSpan={6} className="text-gray-500">Belum ada Paket Kelas.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}
