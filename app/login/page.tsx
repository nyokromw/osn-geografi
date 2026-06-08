'use client'
import { useState } from 'react'
import { supabase } from '../lib/supabase'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [pesan, setPesan] = useState('')

  const handleLogin = async () => {
    setLoading(true)
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) {
      setPesan('Email atau password salah.')
    } else {
      window.location.href = '/dashboard'
    }
    setLoading(false)
  }

  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white border border-gray-200 rounded-2xl p-8 w-full max-w-md shadow-sm">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-black text-white text-sm">G</div>
            <span className="font-black text-gray-800">OSN<span className="text-blue-600">Geo</span>.id</span>
          </div>
          <h1 className="text-2xl font-black text-gray-800">Masuk</h1>
          <p className="text-gray-400 text-sm mt-1">Selamat datang kembali!</p>
        </div>

        <div className="flex flex-col gap-4">
          <div>
            <label className="text-gray-700 text-sm font-medium mb-1 block">Email</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}
              placeholder="email@kamu.com"
              className="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800 focus:outline-none focus:border-blue-400 bg-white"/>
          </div>
          <div>
            <label className="text-gray-700 text-sm font-medium mb-1 block">Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
              placeholder="Password kamu"
              className="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800 focus:outline-none focus:border-blue-400 bg-white"/>
          </div>

          {pesan && (
            <div className="text-sm text-red-500 bg-red-50 border border-red-100 px-4 py-2 rounded-lg">
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
      </div>
    </main>
  )
}