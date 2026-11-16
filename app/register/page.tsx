'use client'

import Link from 'next/link'
import { useState, type FormEvent } from 'react'
import { AuthShell, Notice } from '../components/atlas'
import { supabase } from '../lib/supabase'

export default function Register() {
  const [nama, setNama] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [pesan, setPesan] = useState('')
  const [sukses, setSukses] = useState(false)

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (loading) return
    setLoading(true)
    setPesan('')
    try {
      const { error } = await supabase.auth.signUp({
        email, password, options: { data: { nama } },
      })
      if (error) setPesan('Gagal mendaftar. ' + error.message)
      else setSukses(true)
    } catch {
      setPesan('Terjadi gangguan koneksi. Coba lagi.')
    } finally {
      setLoading(false)
    }
  }

  if (sukses) return (
    <AuthShell title="Pendaftaran berhasil" description="Akun OSNGEO kamu sudah dibuat.">
      <Link href="/login" className="atlas-button atlas-button--primary mt-6 w-full">Masuk</Link>
    </AuthShell>
  )

  return (
    <AuthShell title="Daftar akun" description="Buat akun untuk mulai latihan OSN Geografi.">
      <form className="atlas-auth-form" onSubmit={submit}>
        <label>
          Nama lengkap
          <input className="atlas-field" type="text" name="name" autoComplete="name" required
            placeholder="Nama lengkap" value={nama} onChange={event => setNama(event.target.value)} />
        </label>
        <label>
          Email
          <input className="atlas-field" type="email" name="email" autoComplete="email" required
            placeholder="nama@contoh.id" value={email} onChange={event => setEmail(event.target.value)} />
        </label>
        <label>
          Kata sandi
          <input className="atlas-field" type="password" name="password" autoComplete="new-password" required
            minLength={6} placeholder="Minimal 6 karakter" value={password} onChange={event => setPassword(event.target.value)} />
        </label>
        {pesan && <Notice error>{pesan}</Notice>}
        <button className="atlas-button atlas-button--primary" type="submit" disabled={loading}>
          {loading ? 'Mendaftarkan akun…' : 'Buat akun'}
        </button>
      </form>
      <p className="mt-5 text-sm text-gray-500">Sudah punya akun? <Link href="/login" className="atlas-link">Masuk</Link></p>
    </AuthShell>
  )
}
