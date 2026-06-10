'use client'
import { useEffect, useState, useCallback } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { supabase } from '../../lib/supabase'
import { getUserStatus, bisaAkses } from '../../lib/checkAkses'

export default function TryoutPage() {
  const params = useParams()
  const router = useRouter()
  const paketId = Number(params.id)

  const [loading, setLoading] = useState(true)
  const [paket, setPaket] = useState<any>(null)
  const [soalList, setSoalList] = useState<any[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [jawaban, setJawaban] = useState<Record<number, string>>(() => {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem(`tryout-${paketId}`)
    return saved ? JSON.parse(saved) : {}
  }
  return {}
})
  const [timeLeft, setTimeLeft] = useState(0)
  const [submitted, setSubmitted] = useState(false)
  const [hasil, setHasil] = useState<any>(null)
  const [zoomImg, setZoomImg] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const [userId, setUserId] = useState<string | null>(null)
useEffect(() => {
  if (Object.keys(jawaban).length > 0) {
    localStorage.setItem(`tryout-${paketId}`, JSON.stringify(jawaban))
  }
}, [jawaban, paketId])
  useEffect(() => {
    const init = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) { router.push('/login'); return }
      setUserId(user.id)

const { data: p } = await supabase.from('paket_to').select('*').eq('id', paketId).single()
      if (!p) { router.push('/dashboard'); return }

      // Cek akses
      const statusUser = await getUserStatus()
      const aksesKonten = p.akses || (p.is_premium ? 'premium' : 'gratis')
      if (!bisaAkses(statusUser, aksesKonten)) {
        router.push('/dashboard?akses=ditolak')
        return
      }

      setPaket(p)
      setTimeLeft((p.durasi_menit || 120) * 60)

      const { data: soal } = await supabase
        .from('soal')
        .select('*')
        .eq('paket_id', paketId)
        .order('id')
      setSoalList(soal || [])
      setLoading(false)
    }
    init()
  }, [paketId])

  const handleSubmit = useCallback(async () => {
    if (!userId || !paket) return
    let benar = 0, salah = 0, kosong = 0
    soalList.forEach(s => {
      const j = jawaban[s.id]
      if (!j) kosong++
      else if (j === s.jawaban_benar) benar++
      else salah++
    })
    const totalPoin = (benar * 4) + (salah * -1)
    await supabase.from('hasil_to').insert({
      user_id: userId,
      paket_id: paketId,
      total_soal: soalList.length,
      poin_benar: benar,
      poin_salah: salah,
      poin_kosong: kosong,
      skor: benar,
      total_poin: totalPoin,
    })
    setHasil({ benar, salah, kosong, totalPoin })
    localStorage.removeItem(`tryout-${paketId}`)
    setSubmitted(true)
    setShowConfirm(false)
  }, [userId, paket, soalList, jawaban, paketId])

  useEffect(() => {
    if (loading || submitted) return
    if (timeLeft <= 0) { handleSubmit(); return }
    const t = setTimeout(() => setTimeLeft(p => p - 1), 1000)
    return () => clearTimeout(t)
  }, [timeLeft, loading, submitted, handleSubmit])

  if (loading) return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center">
      <p className="text-gray-400 animate-pulse">Memuat soal...</p>
    </div>
  )

  const formatTime = (s: number) => {
    const h = Math.floor(s / 3600)
    const m = Math.floor((s % 3600) / 60)
    const sc = s % 60
    return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(sc).padStart(2,'0')}`
  }

  const soal = soalList[currentIndex]
  const totalSoal = soalList.length
  const dijawab = Object.keys(jawaban).length
  const belum = totalSoal - dijawab
  const timerDanger = timeLeft < 300

  // HASIL SCREEN
  if (submitted && hasil) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
        <div className="bg-white rounded-2xl shadow-lg p-8 max-w-2xl w-full">
          <div className="text-center mb-8">
            <div className="text-5xl mb-3">🎯</div>
            <h1 className="text-2xl font-black text-gray-800 mb-1">Tryout Selesai!</h1>
            <p className="text-gray-500 text-sm">{paket?.nama}</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {[
              { label: 'Total Poin', value: hasil.totalPoin, color: hasil.totalPoin >= 0 ? 'bg-blue-600' : 'bg-red-500' },
              { label: 'Benar (+4)', value: hasil.benar, color: 'bg-green-500' },
              { label: 'Salah (-1)', value: hasil.salah, color: 'bg-red-400' },
              { label: 'Kosong (0)', value: hasil.kosong, color: 'bg-gray-400' },
            ].map((s, i) => (
              <div key={i} className={`${s.color} text-white rounded-xl p-4 text-center`}>
                <div className="text-xs opacity-80 mb-1">{s.label}</div>
                <div className="text-3xl font-black">{s.value}</div>
              </div>
            ))}
          </div>

          <div className="mb-8">
            <h2 className="font-bold text-gray-800 mb-4">Pembahasan</h2>
            <div className="flex flex-col gap-4 max-h-96 overflow-y-auto pr-1">
              {soalList.map((s, i) => {
                const j = jawaban[s.id]
                const benar = j === s.jawaban_benar
                const kosong = !j
                return (
                  <div key={s.id} className={`rounded-xl border p-4 ${
                    kosong ? 'border-gray-200 bg-gray-50'
                    : benar ? 'border-green-200 bg-green-50'
                    : 'border-red-200 bg-red-50'
                  }`}>
                    <div className="flex items-start gap-3 mb-2">
                      <span className={`text-xs font-black px-2 py-0.5 rounded-full shrink-0 ${
                        kosong ? 'bg-gray-200 text-gray-600'
                        : benar ? 'bg-green-200 text-green-700'
                        : 'bg-red-200 text-red-700'
                      }`}>{i + 1}</span>
                      <p className="text-sm text-gray-800 flex-1">{s.pertanyaan}</p>
                    </div>
                    {s.gambar_url && (
                      <img src={s.gambar_url} alt="" className="w-full max-h-40 object-contain rounded-lg mb-2" />
                    )}
                    <div className="flex gap-3 text-xs mt-2 flex-wrap">
                      <span className="text-gray-500">Jawaban kamu: <strong className={kosong ? 'text-gray-500' : benar ? 'text-green-600' : 'text-red-600'}>{j || '—'}</strong></span>
                      <span className="text-gray-500">Jawaban benar: <strong className="text-green-600">{s.jawaban_benar}</strong></span>
                    </div>
                    {s.pembahasan && (
                      <div className="mt-2 pt-2 border-t border-gray-200 text-xs text-gray-600">
                        <span className="font-semibold">Pembahasan: </span>{s.pembahasan}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>

          <button onClick={() => router.push('/dashboard')}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl transition">
            Kembali ke Dashboard
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col" style={{ colorScheme: 'light', background: '#f1f5f9' }}>

      {/* TOPBAR */}
      <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between sticky top-0 z-20">
        <div className="flex items-center gap-3">
          <button onClick={() => router.push('/dashboard')}
            className="text-gray-400 hover:text-gray-700 text-sm transition">← Keluar</button>
          <div className="h-4 w-px bg-gray-200" />
          <span className="font-bold text-gray-800 text-sm truncate max-w-xs">{paket?.nama}</span>
        </div>
        <div className={`font-black text-lg tabular-nums px-4 py-1.5 rounded-lg ${
          timerDanger ? 'bg-red-100 text-red-600 animate-pulse' : 'bg-gray-100 text-gray-700'
        }`}>
          {formatTime(timeLeft)}
        </div>
      </header>

      {/* BODY */}
      <div className="flex flex-1 overflow-hidden">

{/* AREA SOAL */}
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-2xl mx-auto">

            {/* PROGRESS */}
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-bold text-gray-600">Soal {currentIndex + 1} dari {totalSoal}</span>
              <div className="flex items-center gap-2">
                <div className="h-1.5 w-40 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 rounded-full transition-all"
                    style={{ width: `${((currentIndex + 1) / totalSoal) * 100}%` }} />
                </div>
                <span className="text-xs text-gray-400">{Math.round(((currentIndex + 1) / totalSoal) * 100)}%</span>
              </div>
            </div>

            {/* KARTU SOAL */}
            <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-4">

              {/* PERTANYAAN */}
              <p className="text-gray-800 leading-relaxed mb-5 text-[15px]">{soal?.pertanyaan}</p>

              {/* GAMBAR */}
              {soal?.gambar_url && (
                <div className="mb-5">
                  <img
                    src={soal.gambar_url}
                    alt="Gambar soal"
                    onClick={() => setZoomImg(true)}
                    className="max-h-64 w-full object-contain rounded-xl border border-gray-100 cursor-zoom-in hover:opacity-90 transition"
                  />
                  <p className="text-xs text-gray-400 text-center mt-1">Klik gambar untuk perbesar</p>
                </div>
              )}

              {/* PILIHAN */}
              <div className="flex flex-col gap-2.5">
                {['a','b','c','d','e'].map(op => {
                  const val = soal?.[`pilihan_${op}`]
                  if (!val) return null
                  const opUpper = op.toUpperCase()
                  const selected = jawaban[soal?.id] === opUpper
                  return (
                    <button key={op}
                      onClick={() => setJawaban(prev => ({ ...prev, [soal.id]: opUpper }))}
                      className={`flex items-center gap-3 px-4 py-3 rounded-xl border text-left transition ${
                        selected
                          ? 'border-blue-500 bg-blue-50 text-blue-800'
                          : 'border-gray-200 hover:border-blue-300 hover:bg-blue-50/50 text-gray-700'
                      }`}>
                      <span className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-black shrink-0 transition ${
                        selected ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-500'
                      }`}>{opUpper}</span>
                      <span className="text-sm leading-relaxed">{val}</span>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* NAVIGASI PREV / NEXT */}
            <div className="flex items-center justify-between">
              <button
                onClick={() => setCurrentIndex(i => Math.max(0, i - 1))}
                disabled={currentIndex === 0}
                className="px-5 py-2 rounded-lg border border-gray-200 text-sm font-semibold text-gray-600 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition">
                ← Sebelumnya
              </button>
              {jawaban[soal?.id] && (
                <span className="text-xs text-green-600 font-semibold">✓ Terjawab</span>
              )}
              <button
                onClick={() => setCurrentIndex(i => Math.min(totalSoal - 1, i + 1))}
                disabled={currentIndex === totalSoal - 1}
                className="px-5 py-2 rounded-lg border border-gray-200 text-sm font-semibold text-gray-600 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition">
                Selanjutnya →
              </button>
            </div>
          </div>
        </main>

        {/* PANEL NAVIGASI SOAL (kanan) */}
        <aside className="w-56 shrink-0 bg-white border-l border-gray-200 flex flex-col p-4 overflow-y-auto">
          <div className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3">Navigasi Soal</div>

          {/* GRID NOMOR */}
          <div className="grid grid-cols-5 gap-1.5 mb-5">
            {soalList.map((s, i) => {
              const isCurrent = i === currentIndex
              const isDijawab = !!jawaban[s.id]
              return (
                <button key={s.id}
                  onClick={() => setCurrentIndex(i)}
                  className={`w-full aspect-square rounded-lg text-xs font-bold transition ${
                    isCurrent
                      ? 'bg-yellow-400 text-yellow-900'
                      : isDijawab
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                  }`}>
                  {i + 1}
                </button>
              )
            })}
          </div>

          {/* LEGENDA */}
          <div className="flex flex-col gap-1.5 mb-5 text-xs text-gray-500">
            <div className="flex items-center gap-2">
              <span className="w-4 h-4 rounded bg-yellow-400 shrink-0" />Sedang dibuka
            </div>
            <div className="flex items-center gap-2">
              <span className="w-4 h-4 rounded bg-blue-500 shrink-0" />Sudah dijawab
            </div>
            <div className="flex items-center gap-2">
              <span className="w-4 h-4 rounded bg-gray-100 border border-gray-200 shrink-0" />Belum dijawab
            </div>
          </div>

          {/* STATISTIK */}
          <div className="bg-gray-50 rounded-xl p-3 mb-4 text-xs flex flex-col gap-1">
            <div className="flex justify-between">
              <span className="text-gray-500">Dijawab</span>
              <span className="font-bold text-blue-600">{dijawab}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Belum</span>
              <span className="font-bold text-gray-500">{belum}</span>
            </div>
            <div className="flex justify-between border-t border-gray-200 pt-1 mt-1">
              <span className="text-gray-500">Total</span>
              <span className="font-bold text-gray-700">{totalSoal}</span>
            </div>
          </div>

          {/* TOMBOL SUBMIT */}
          <button onClick={() => setShowConfirm(true)}
            className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-2.5 rounded-xl text-sm transition mt-auto">
            Selesai & Submit
          </button>
        </aside>
      </div>

      {/* MODAL ZOOM GAMBAR */}
      {zoomImg && soal?.gambar_url && (
        <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4"
          onClick={() => setZoomImg(false)}>
          <div className="relative max-w-4xl w-full">
            <img src={soal.gambar_url} alt="Zoom" className="w-full max-h-[85vh] object-contain rounded-xl" />
            <button onClick={() => setZoomImg(false)}
              className="absolute top-3 right-3 bg-white/20 hover:bg-white/40 text-white w-8 h-8 rounded-full flex items-center justify-center text-lg transition">
              ✕
            </button>
            <p className="text-center text-white/60 text-xs mt-2">Klik di mana saja untuk menutup</p>
          </div>
        </div>
      )}

      {/* MODAL KONFIRMASI SUBMIT */}
      {showConfirm && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl p-6 max-w-sm w-full shadow-xl">
            <div className="text-center mb-5">
              <div className="text-4xl mb-2">⚠️</div>
              <h3 className="font-black text-gray-800 text-lg mb-1">Submit Tryout?</h3>
              <p className="text-gray-500 text-sm">
                Kamu baru menjawab <strong>{dijawab}</strong> dari <strong>{totalSoal}</strong> soal.
                {belum > 0 && <span className="text-red-500"> {belum} soal belum dijawab.</span>}
              </p>
            </div>
            <div className="flex gap-3">
              <button onClick={() => setShowConfirm(false)}
                className="flex-1 border border-gray-200 text-gray-600 py-2.5 rounded-xl text-sm font-semibold hover:bg-gray-50 transition">
                Lanjut Kerjakan
              </button>
              <button onClick={handleSubmit}
                className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2.5 rounded-xl text-sm font-bold transition">
                Ya, Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}