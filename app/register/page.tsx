'use client'

import Link from 'next/link'
import { useState, type FormEvent } from 'react'
import { AuthShell, Notice } from '../components/atlas'
import { supabase } from '../lib/supabase'

const provinces: readonly string[] = [
  'Aceh', 'Bali', 'Banten', 'Bengkulu', 'DI Yogyakarta', 'DKI Jakarta',
  'Gorontalo', 'Jambi', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur',
  'Kalimantan Barat', 'Kalimantan Selatan', 'Kalimantan Tengah', 'Kalimantan Timur', 'Kalimantan Utara',
  'Kepulauan Bangka Belitung', 'Kepulauan Riau', 'Lampung', 'Maluku', 'Maluku Utara',
  'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Papua', 'Papua Barat', 'Papua Barat Daya',
  'Papua Pegunungan', 'Papua Selatan', 'Papua Tengah', 'Riau',
  'Sulawesi Barat', 'Sulawesi Selatan', 'Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Utara',
  'Sumatera Barat', 'Sumatera Selatan', 'Sumatera Utara',
]

function normalizePhone(value: string) {
  const digits = value.trim().replace(/[\s().-]/g, '')
  return /^\+?[0-9]{8,15}$/.test(digits) ? digits : null
}

export default function Register() {
  const [nama, setNama] = useState('')
  const [email, setEmail] = useState('')
  const [provinsi, setProvinsi] = useState('')
  const [nomorHp, setNomorHp] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [pesan, setPesan] = useState('')
  const [sukses, setSukses] = useState(false)

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (loading) return
    const fullName = nama.trim()
    const phone = normalizePhone(nomorHp)
    if (!fullName) { setPesan('Masukkan nama lengkap.'); return }
    if (!provinces.includes(provinsi)) { setPesan('Pilih provinsi asal.'); return }
    if (!phone) { setPesan('Masukkan nomor HP yang valid, misalnya 0812 3456 7890.'); return }
    setLoading(true)
    setPesan('')
    try {
      const { error } = await supabase.auth.signUp({
        email: email.trim(),
        password,
        options: { data: { nama: fullName, provinsi, nomor_hp: phone } },
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
          Asal provinsi
          <select className="atlas-field" name="provinsi" autoComplete="address-level1" required
            value={provinsi} onChange={event => setProvinsi(event.target.value)}>
            <option value="" disabled>Pilih provinsi asal</option>
            {provinces.map(province => <option key={province} value={province}>{province}</option>)}
          </select>
        </label>
        <label>
          Nomor HP
          <input className="atlas-field" type="tel" name="nomor_hp" autoComplete="tel" required
            placeholder="0812 3456 7890" value={nomorHp} onChange={event => setNomorHp(event.target.value)} />
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
