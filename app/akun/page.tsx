'use client'

import Link from 'next/link'
import { useEffect, useState, type FormEvent } from 'react'
import { ArrowLeft } from 'lucide-react'
import { Notice, PageLoading, WorkspaceHeader } from '../components/atlas'
import { supabase } from '../lib/supabase'
import { provinces } from '../lib/provinces'
import { isStudentAccountEmail } from '../lib/kelas'

type Profile = { nama: string | null; email: string | null; username: string | null; sekolah: string | null; kelas: string | null; provinsi: string | null; nomor_hp: string | null }
type Message = { text: string; error: boolean } | null

export default function AkunPage() {
  const [loading, setLoading] = useState(true)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [form, setForm] = useState({ nama: '', sekolah: '', kelas: '', provinsi: '', nomor_hp: '' })
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState<Message>(null)
  const [password, setPassword] = useState({ baru: '', ulang: '' })
  const [pwSaving, setPwSaving] = useState(false)
  const [pwMessage, setPwMessage] = useState<Message>(null)

  useEffect(() => {
    void (async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) { window.location.href = '/login'; return }
      const { data } = await supabase.from('profiles')
        .select('nama, email, username, sekolah, kelas, provinsi, nomor_hp').eq('id', user.id).single()
      const p = (data ?? null) as Profile | null
      setProfile(p)
      setForm({
        nama: p?.nama && !/^Siswa \d+$/.test(p.nama) ? p.nama : '',
        sekolah: p?.sekolah ?? '', kelas: p?.kelas ?? '', provinsi: p?.provinsi ?? '', nomor_hp: p?.nomor_hp ?? '',
      })
      setLoading(false)
    })()
  }, [])

  const saveProfile = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (saving) return
    setSaving(true); setMessage(null)
    const { error } = await supabase.rpc('update_my_profile', {
      p_nama: form.nama, p_sekolah: form.sekolah, p_kelas: form.kelas, p_provinsi: form.provinsi, p_nomor_hp: form.nomor_hp,
    })
    setSaving(false)
    setMessage(error
      ? { text: /nama/i.test(error.message) ? 'Nama harus 2 sampai 80 karakter.' : 'Data belum tersimpan. Periksa nomor HP dan coba lagi.', error: true }
      : { text: 'Data diri tersimpan.', error: false })
  }

  const savePassword = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (pwSaving) return
    if (password.baru.length < 6) { setPwMessage({ text: 'Kata sandi minimal 6 karakter.', error: true }); return }
    if (password.baru !== password.ulang) { setPwMessage({ text: 'Kedua kata sandi belum sama.', error: true }); return }
    setPwSaving(true); setPwMessage(null)
    const { error } = await supabase.auth.updateUser({ password: password.baru })
    if (!error) await supabase.rpc('clear_my_initial_password')
    setPwSaving(false)
    if (error) setPwMessage({ text: 'Kata sandi belum berubah. Coba kata sandi lain.', error: true })
    else { setPassword({ baru: '', ulang: '' }); setPwMessage({ text: 'Kata sandi baru tersimpan. Gunakan saat masuk berikutnya.', error: false }) }
  }

  if (loading) return <PageLoading>Memuat akun…</PageLoading>
  const studentAccount = isStudentAccountEmail(profile?.email)
  const field = (key: keyof typeof form) => ({ value: form[key], onChange: (e: { target: { value: string } }) => setForm({ ...form, [key]: e.target.value }) })

  return (
    <>
      <WorkspaceHeader title="Akun">
        <Link href="/dashboard" className="atlas-button"><ArrowLeft size={16} aria-hidden="true" /> Dashboard</Link>
      </WorkspaceHeader>
      <main className="atlas-container atlas-work-content">
        <div className="mx-auto grid max-w-2xl gap-6">
          <section className="atlas-card p-5 sm:p-6" aria-labelledby="data-diri">
            <h1 className="atlas-subtitle" id="data-diri">Data diri</h1>
            <p className="mt-1 text-sm text-gray-600">
              {studentAccount
                ? <>Masuk dengan username <strong className="font-mono">{profile?.username}</strong>. Lengkapi namamu agar guru mudah mengenali hasil belajarmu.</>
                : <>Masuk dengan email <strong>{profile?.email}</strong>.</>}
            </p>
            <form className="atlas-auth-form mt-5" onSubmit={saveProfile}>
              <label>Nama lengkap
                <input className="atlas-field" required minLength={2} maxLength={80} autoComplete="name" placeholder="Nama lengkap" {...field('nama')} />
              </label>
              <div className="grid gap-4 sm:grid-cols-2">
                <label>Sekolah
                  <input className="atlas-field" maxLength={120} placeholder="Nama sekolah" {...field('sekolah')} />
                </label>
                <label>Kelas
                  <input className="atlas-field" maxLength={60} placeholder="Misalnya XI IPS 2" {...field('kelas')} />
                </label>
              </div>
              <label>Asal provinsi
                <select className="atlas-field" {...field('provinsi')}>
                  <option value="">Pilih provinsi</option>
                  {provinces.map(p => <option key={p} value={p}>{p}</option>)}
                </select>
              </label>
              <label>Nomor HP <span className="font-normal text-gray-500">(opsional)</span>
                <input className="atlas-field" type="tel" autoComplete="tel" placeholder="0812 3456 7890" {...field('nomor_hp')} />
              </label>
              {message && <Notice error={message.error}>{message.text}</Notice>}
              <button className="atlas-button atlas-button--primary" type="submit" disabled={saving}>{saving ? 'Menyimpan…' : 'Simpan data diri'}</button>
            </form>
          </section>

          <section className="atlas-card p-5 sm:p-6" aria-labelledby="ganti-sandi">
            <h2 className="atlas-subtitle" id="ganti-sandi">Ganti kata sandi</h2>
            {studentAccount && <p className="mt-1 text-sm text-gray-600">Setelah diganti, kata sandi lama dari guru tidak berlaku lagi dan tidak lagi terlihat oleh guru.</p>}
            <form className="atlas-auth-form mt-5" onSubmit={savePassword}>
              <input type="text" name="username" autoComplete="username" value={profile?.username ?? profile?.email ?? ''} readOnly hidden />
              <label>Kata sandi baru
                <input className="atlas-field" type="password" autoComplete="new-password" minLength={6} required
                  value={password.baru} onChange={e => setPassword({ ...password, baru: e.target.value })} />
              </label>
              <label>Ulangi kata sandi baru
                <input className="atlas-field" type="password" autoComplete="new-password" minLength={6} required
                  value={password.ulang} onChange={e => setPassword({ ...password, ulang: e.target.value })} />
              </label>
              {pwMessage && <Notice error={pwMessage.error}>{pwMessage.text}</Notice>}
              <button className="atlas-button atlas-button--primary" type="submit" disabled={pwSaving}>{pwSaving ? 'Menyimpan…' : 'Simpan kata sandi'}</button>
            </form>
          </section>
        </div>
      </main>
    </>
  )
}
