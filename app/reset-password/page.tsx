'use client'

import Link from 'next/link'
import { useEffect, useState, type FormEvent } from 'react'
import { AuthShell, Notice } from '../components/atlas'
import { supabase } from '../lib/supabase'

export default function ResetPassword() {
  const [password, setPassword] = useState('')
  const [konfirmasi, setKonfirmasi] = useState('')
  const [loading, setLoading] = useState(false)
  const [notice, setNotice] = useState<{ message: string; error: boolean } | null>(null)
  const [valid, setValid] = useState(false)
  const [sukses, setSukses] = useState(false)

  useEffect(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event) => {
      if (event === 'PASSWORD_RECOVERY') setValid(true)
    })
    return () => subscription.unsubscribe()
  }, [])

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!valid || loading) return
    if (password !== konfirmasi) {
      setNotice({ message: 'Kedua kata sandi harus sama.', error: true })
      return
    }

    setLoading(true)
    setNotice(null)
    try {
      const { error } = await supabase.auth.updateUser({ password })
      if (error) setNotice({ message: 'Kata sandi gagal diubah. Coba minta tautan baru.', error: true })
      else setSukses(true)
    } catch {
      setNotice({ message: 'Terjadi gangguan koneksi. Coba lagi.', error: true })
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthShell title="Atur ulang kata sandi" description="Buat kata sandi baru untuk akun OSNGEO.">
      {sukses ? (
        <div className="mt-5 space-y-4">
          <Notice>Kata sandi berhasil diubah.</Notice>
          <Link href="/login" className="atlas-button atlas-button--primary w-full">Masuk</Link>
        </div>
      ) : valid ? (
        <form className="atlas-auth-form" onSubmit={submit}>
          <label>
            Kata sandi baru
            <input type="password" className="atlas-field" autoComplete="new-password" minLength={6} required
              value={password} onChange={event => setPassword(event.target.value)} placeholder="Minimal 6 karakter" />
          </label>
          <label>
            Konfirmasi kata sandi
            <input type="password" className="atlas-field" autoComplete="new-password" minLength={6} required
              value={konfirmasi} onChange={event => setKonfirmasi(event.target.value)} />
          </label>
          {notice && <Notice error={notice.error}>{notice.message}</Notice>}
          <button type="submit" className="atlas-button atlas-button--primary" disabled={loading}>
            {loading ? 'Menyimpan…' : 'Simpan kata sandi'}
          </button>
        </form>
      ) : (
        <div className="mt-5 space-y-4">
          <Notice>Buka halaman ini lewat tautan yang dikirim ke emailmu.</Notice>
          <Link href="/login" className="atlas-link text-sm">Kembali ke masuk</Link>
        </div>
      )}
    </AuthShell>
  )
}
