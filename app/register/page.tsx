'use client'
import { useState } from 'react'
import { supabase } from '../lib/supabase'

export default function Register() {
  const [nama, setNama] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [pesan, setPesan] = useState('')
  const [sukses, setSukses] = useState(false)

  const handleRegister = async () => {
    if (!nama || !email || !password) {
      setPesan('Semua field harus diisi.')
      return
    }
    if (password.length < 6) {
      setPesan('Password minimal 6 karakter.')
      return
    }
    setLoading(true)
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: { data: { nama } }
    })
    if (error) {
      setPesan('Gagal daftar: ' + error.message)
    } else {
      setSukses(true)
    }
    setLoading(false)
  }

  if (sukses) return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white border border-gray-200 rounded-2xl p-8 w-full max-w-md shadow-sm text-center">
        <div className="text-5xl mb-4">✅</div>
        <h2 className="text-2xl font-black text-gray-800 mb-2">Pendaftaran Berhasil!</h2>
        <p className="text-gray-500 text-sm mb-6">Akun kamu sudah dibuat. Silakan login sekarang.</p>
        <a href="/login" className="block w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-bold text-sm transition">
          Login Sekarang
        </a>
      </div>
    </main>
  )

  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white border border-gray-200 rounded-2xl p-8 w-full max-w-md shadow-sm">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-black text-white text-sm">G</div>
            <span className="font-black text-gray-800">OSN<span className="text-blue-600">Geo</span>.id</span>
          </div>
          <h1 className="text-2xl font-black text-gray-800">Daftar Akun</h1>
          <p className="text-gray-400 text-sm mt-1">Gratis, tanpa kartu kredit</p>
        </div>

        <div className="flex flex-col gap-4">
          <div>
            <label className="text-gray-700 text-sm font-medium mb-1 block">Nama Lengkap</label>
            <input type="text" value={nama} onChange={(e) => setNama(e.target.value)}
              placeholder="Nama lengkap kamu"
              className="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800 focus:outline-none focus:border-blue-400 bg-white"/>
          </div>
          <div>
            <label className="text-gray-700 text-sm font-medium mb-1 block">Email</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}
              placeholder="email@kamu.com"
              className="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800 focus:outline-none focus:border-blue-400 bg-white"/>
          </div>
          <div>
            <label className="text-gray-700 text-sm font-medium mb-1 block">Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
              placeholder="Minimal 6 karakter"
              className="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800 focus:outline-none focus:border-blue-400 bg-white"/>
          </div>

          {pesan && (
            <div className="text-sm text-red-500 bg-red-50 border border-red-100 px-4 py-2 rounded-lg">
              {pesan}
            </div>
          )}

          <button onClick={handleRegister} disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-bold text-sm transition mt-1">
            {loading ? 'Memproses...' : 'Daftar Sekarang'}
          </button>

          <p className="text-center text-gray-400 text-sm">
            Sudah punya akun?{' '}
            <a href="/login" className="text-blue-600 hover:underline font-semibold">Masuk di sini</a>
          </p>

          <div className="text-center">
            <a href="/" className="text-gray-400 text-xs hover:text-gray-600 transition">← Kembali ke Beranda</a>
          </div>
        </div>
      </div>
    </main>
  )
}