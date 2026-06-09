'use client'
import { useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'

export default function ResetPassword() {
  const [password, setPassword] = useState('')
  const [konfirmasi, setKonfirmasi] = useState('')
  const [loading, setLoading] = useState(false)
  const [pesan, setPesan] = useState('')
  const [pesanType, setPesanType] = useState<'error' | 'success'>('error')
  const [valid, setValid] = useState(false)

  useEffect(() => {
    // Cek apakah user datang dari link reset yang valid
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event) => {
      if (event === 'PASSWORD_RECOVERY') {
        setValid(true)
      }
    })
    return () => subscription.unsubscribe()
  }, [])

  const handleReset = async () => {
    if (!password || !konfirmasi) {
      setPesan('Isi semua field.')
      setPesanType('error')
      return
    }
    if (password !== konfirmasi) {
      setPesan('Password tidak cocok.')
      setPesanType('error')
      return
    }
    if (password.length < 6) {
      setPesan('Password minimal 6 karakter.')
      setPesanType('error')
      return
    }

    setLoading(true)
    const { error } = await supabase.auth.updateUser({ password })
    if (error) {
      setPesan('Gagal reset password. Coba minta link baru.')
      setPesanType('error')
    } else {
      setPesan('Password berhasil diubah! Silakan login.')
      setPesanType('success')
      setTimeout(() => { window.location.href = '/login' }, 2000)
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
          <h1 className="text-2xl font-black text-gray-800">Reset Password</h1>
          <p className="text-gray-400 text-sm mt-1">Masukkan password baru kamu</p>
        </div>

        {!valid ? (
          <div className="text-center">
            <div className="text-gray-400 text-sm mb-4">
              Link reset tidak valid atau sudah kadaluarsa.
            </div>
            <a href="/login" className="text-blue-600 hover:underline text-sm font-semibold">
              Kembali ke Login
            </a>
          </div>
        ) : (
          <div className="flex flex-col gap-4">
            <div>
              <label className="text-gray-700 text-sm font-medium mb-1 block">Password Baru</label>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                placeholder="Minimal 6 karakter"
                className="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800 focus:outline-none focus:border-blue-400 bg-white"/>
            </div>
            <div>
              <label className="text-gray-700 text-sm font-medium mb-1 block">Konfirmasi Password</label>
              <input type="password" value={konfirmasi} onChange={(e) => setKonfirmasi(e.target.value)}
                placeholder="Ulangi password baru"
                onKeyDown={(e) => e.key === 'Enter' && handleReset()}
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

            <button onClick={handleReset} disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-bold text-sm transition">
              {loading ? 'Menyimpan...' : 'Simpan Password Baru'}
            </button>

            <div className="text-center">
              <a href="/login" className="text-gray-400 text-xs hover:text-gray-600 transition">← Kembali ke Login</a>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}