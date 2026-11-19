'use client'

import Link from 'next/link'
import { useState, type FormEvent } from 'react'
import { AuthShell, Notice } from '../components/atlas'
import { supabase } from '../lib/supabase'
import { safePaymentReturn } from '../lib/payments'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [forgotEmail, setForgotEmail] = useState('')
  const [showForgot, setShowForgot] = useState(false)
  const [loading, setLoading] = useState(false)
  const [notice, setNotice] = useState<{ message: string; error: boolean } | null>(null)

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (loading) return
    setLoading(true)
    setNotice(null)
    try {
      if (showForgot) {
        const { error } = await supabase.auth.resetPasswordForEmail(forgotEmail, {
          redirectTo: window.location.origin + '/reset-password',
        })
        if (error) {
          setNotice({ message: 'Tautan reset gagal dikirim. Coba lagi.', error: true })
        } else {
          setShowForgot(false)
          setNotice({ message: 'Tautan reset sudah dikirim. Periksa kotak masuk atau folder spam.', error: false })
        }
      } else {
        const { error } = await supabase.auth.signInWithPassword({ email, password })
        if (error) setNotice({ message: 'Email atau kata sandi salah.', error: true })
        else window.location.href = safePaymentReturn(new URLSearchParams(window.location.search).get('next'))
      }
    } catch {
      setNotice({ message: 'Terjadi gangguan koneksi. Coba lagi.', error: true })
    } finally {
      setLoading(false)
    }
  }

  function toggleForgot() {
    if (!showForgot) setForgotEmail(email)
    setShowForgot(!showForgot)
    setNotice(null)
  }

  return (
    <AuthShell title={showForgot ? 'Lupa kata sandi' : 'Masuk'}
      description={showForgot ? 'Masukkan email akun OSNGEO untuk menerima tautan reset.' : 'Lanjutkan persiapan OSN Geografi.'}>
      <form className="atlas-auth-form" onSubmit={submit}>
        <label>
          Email
          <input className="atlas-field" type="email" name="email" autoComplete="email"
            placeholder="nama@contoh.id" required value={showForgot ? forgotEmail : email}
            onChange={event => (showForgot ? setForgotEmail : setEmail)(event.target.value)} />
        </label>
        {!showForgot && (
          <label>
            Kata sandi
            <input className="atlas-field" type="password" name="password" autoComplete="current-password"
              required value={password} onChange={event => setPassword(event.target.value)} />
          </label>
        )}
        {notice && <Notice error={notice.error}>{notice.message}</Notice>}
        <button className="atlas-button atlas-button--primary" type="submit" disabled={loading}>
          {loading ? 'Memproses…' : showForgot ? 'Kirim tautan reset' : 'Masuk'}
        </button>
      </form>
      <div className="mt-5 flex flex-wrap items-center justify-between gap-3 text-sm">
        <button className="atlas-link" type="button" disabled={loading} onClick={toggleForgot}>
          {showForgot ? 'Kembali ke masuk' : 'Lupa kata sandi?'}
        </button>
        {!showForgot && <Link href="/register" className="atlas-link">Daftar akun</Link>}
      </div>
    </AuthShell>
  )
}
