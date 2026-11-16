'use client'
import { useEffect, useState, useCallback } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { supabase } from '../../lib/supabase'
import { getUserStatus, bisaAkses } from '../../lib/checkAkses'
import { PageLoading } from '../../components/atlas'
import { ExamResults, ExamScreen, type ExamScore, type Question } from '../../components/exam'

export default function TryoutPage() {
  const params = useParams()
  const router = useRouter()
  const paketId = Number(params.id)

  const [loading, setLoading] = useState(true)
  const [paket, setPaket] = useState<any>(null)
  const [soalList, setSoalList] = useState<Question[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [jawaban, setJawaban] = useState<Record<number, string>>({})
  const [timeLeft, setTimeLeft] = useState(0)
  const [submitted, setSubmitted] = useState(false)
  const [hasil, setHasil] = useState<ExamScore | null>(null)
  const [userId, setUserId] = useState<string | null>(null)
  // Simpan jawaban selama belum submit
useEffect(() => {
  if (!submitted && Object.keys(jawaban).length > 0) {
    localStorage.setItem(`tryout-${paketId}`, JSON.stringify(jawaban))
  }
}, [jawaban, paketId, submitted])
  useEffect(() => {
    const init = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) { router.push('/login'); return }
      setUserId(user.id)

const { data: p } = await supabase.from('paket_to').select('*').eq('id', paketId).single()
      if (!p) { router.push('/dashboard'); return }

      const statusUser = await getUserStatus()
      const aksesKonten = p.akses || (p.is_premium ? 'premium' : 'gratis')
      if (!bisaAkses(statusUser, aksesKonten)) {
        router.push('/dashboard?akses=ditolak')
        return
      }

      setPaket(p)

      // Lanjutkan progress HANYA jika jawaban DAN timer tersimpan
      const savedJawaban = localStorage.getItem(`tryout-${p.id}`)
      const savedTime = localStorage.getItem(`tryout-time-${p.id}`)
      if (savedJawaban && savedTime && Number(savedTime) > 0) {
        setJawaban(JSON.parse(savedJawaban))
        setTimeLeft(Number(savedTime))
      } else {
        localStorage.removeItem(`tryout-${p.id}`)
        localStorage.removeItem(`tryout-time-${p.id}`)
        setTimeLeft((p.durasi_menit || 120) * 60)
      }

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
    localStorage.removeItem(`tryout-${paketId}`)
    localStorage.removeItem(`tryout-time-${paketId}`)
    setHasil({ benar, salah, kosong, totalPoin })
    setSubmitted(true)
  }, [userId, paket, soalList, jawaban, paketId])

  useEffect(() => {
  if (loading || submitted || !soalList.length) return
  if (timeLeft <= 0) { handleSubmit(); return }
  localStorage.setItem(`tryout-time-${paketId}`, String(timeLeft))
  const t = setTimeout(() => setTimeLeft(p => p - 1), 1000)
  return () => clearTimeout(t)
}, [timeLeft, loading, submitted, handleSubmit, paketId, soalList.length])

  if (loading) return <PageLoading>Memuat soal…</PageLoading>

  const title = paket?.nama || 'Tryout'
  if (submitted && hasil) return (
    <ExamResults mode="Tryout" title={title} score={hasil} questions={soalList} answers={jawaban} />
  )

  return (
    <ExamScreen mode="Tryout" title={title} timeLeft={timeLeft} questions={soalList} answers={jawaban}
      index={currentIndex} onNavigate={setCurrentIndex} onFinish={handleSubmit}
      onAnswer={(id, answer) => setJawaban(previous => ({ ...previous, [id]: answer }))} />
  )
}
