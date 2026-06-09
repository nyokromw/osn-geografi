'use client'
import { useState } from 'react'
import { supabase } from '../lib/supabase'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [pesan, setPesan] = useState('')
  const [pesanType, setPesanType] = useState<'error' | 'success'>('error')
  const [showForgot, setShowForgot] = useState(false)
  const [forgotEmail, setForgotEmail] = useState('')
  const [forgotLoading, setForgotLoading] = useState(false)

  const handleLogin = async () => {
    setLoading(true)
    setPesan('')
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) {
      setPesan('Email atau password salah.')
      setPesanType('error')
    } else {
      window.location.href = '/dashboard'
    }
    setLoading(false)
  }

  const handleForgotPassword = async () => {
    if (!forgotEmail) { setPesan('Masukkan email dulu.'); setPesanType('error'); return }
    setForgotLoading(true)
    setPesan('')
    const { error } = await supabase.auth.resetPasswordForEmail(forgotEmail, {
      redirectTo: `${window.location.origin}/reset-password`,
    })
    if (error) {
      setPesan('Gagal kirim email. Coba lagi.')
      setPesanType('error')
    } else {
      setPesan('Email reset password sudah dikirim! Cek inbox atau folder spam.')
      setPesanType('success')
      setShowForgot(false)
    }
    setForgotLoading(false)
  }

  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white border border-gray-200 rounded-2xl p-8 w-full max-w-md shadow-sm">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-black text-white text-sm">G</div>
            <span className="font-black text-gray-800">OSN<span className="text-blue-600">Geo</span>.id</span>
          </div>
          <h1 className="text-2xl font-black text-gray-800">{showForgot ? 'Lupa Password' : 'Masuk'}</h1>
          <p className="text-gray-400 text-sm mt-1">
            {showForgot ? 'Masukkan email untuk reset password' : 'Selamat datang kembali!'}
          </p>
        </div>

        {!showForgot ? (
          <div className="flex flex-col gap-4">
            <div>
              <label className="text-gray-700 text-sm font-medium mb-1 block">Email</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}
                placeholder="email@kamu.com"
                className="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800 focus:outline-none focus:border-blue-400 bg-white"/>
            </div>
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-gray-700 text-sm font-medium">Password</label>
                <button onClick={() => { setShowForgot(true); setPesan('') }}
                  className="text-xs text-blue-600 hover:underline">
                  Lupa Password?
                </button>
              </div>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                placeholder="Password kamu"
                onKeyDown={(e) => e.key === 'Enter' && handleLogin()}
                className="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800 focus:outline-none focus:border-blue-400 bg-white"/>
            </div>

            {pesan && (
              <div className={`text-sm px-4 py-2 rounded-lg border ${
                pesanType === 'success'
                  ? 'text-green-600 bg-green-50 border-green-100'
                  : 'text-red-500 bg-red-50 border-red-100'
              }`}>
                {pesan}
              </div>
            )}

            <button onClick={handleLogin} disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-bold text-sm transition mt-1">
              {loading ? 'Memproses...' : 'Masuk'}
            </button>

            <p className="text-center text-gray-400 text-sm">
              Belum punya akun?{' '}
              <a href="/register" className="text-blue-600 hover:underline font-semibold">Daftar di sini</a>
            </p>

            <div className="text-center">
              <a href="/" className="text-gray-400 text-xs hover:text-gray-600 transition">← Kembali ke Beranda</a>
            </div>
          </div>
        ) : (
          <div className="flex flex-col gap-4">
            <div>
              <label className="text-gray-700 text-sm font-medium mb-1 block">Email</label>
              <input type="email" value={forgotEmail} onChange={(e) => setForgotEmail(e.target.value)}
                placeholder="email@kamu.com"
                onKeyDown={(e) => e.key === 'Enter' && handleForgotPassword()}
                className="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800 focus:outline-none focus:border-blue-400 bg-white"/>
            </div>

            {pesan && (
              <div className={`text-sm px-4 py-2 rounded-lg border ${
                pesanType === 'success'
                  ? 'text-green-600 bg-green-50 border-green-100'
                  : 'text-red-500 bg-red-50 border-red-100'
              }`}>
                {pesan}
              </div>
            )}

            <button onClick={handleForgotPassword} disabled={forgotLoading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-bold text-sm transition">
              {forgotLoading ? 'Mengirim...' : 'Kirim Email Reset'}
            </button>

            <button onClick={() => { setShowForgot(false); setPesan('') }}
              className="text-center text-gray-400 text-sm hover:text-gray-600 transition">
              ← Kembali ke Login
            </button>
          </div>
        )}
      </div>
    </main>
  )
}