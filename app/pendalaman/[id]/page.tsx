'use client'
import { useEffect, useState, useCallback } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { supabase } from '../../lib/supabase'
import { getUserStatus } from '../../lib/checkAkses'
import { bisaAkses, requiredAccess } from '../../lib/membership'
import { PageLoading } from '../../components/atlas'
import { ExamResults, ExamScreen, type ExamScore, type Question } from '../../components/exam'
import { UpgradeOffer } from '../../components/upgrade-offer'
import type { AccessLevel } from '../../lib/membership'

export default function PendalamanPage() {
  const params = useParams()
  const router = useRouter()
  const paketId = Number(params.id)

  const [loading, setLoading] = useState(true)
  const [paket, setPaket] = useState<any>(null)
  const [soalList, setSoalList] = useState<Question[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
const [jawaban, setJawaban] = useState<Record<number, string>>(() => {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem(`pendalaman-${paketId}`)
    return saved ? JSON.parse(saved) : {}
  }
  return {}
})
  const [submitted, setSubmitted] = useState(false)
  const [hasil, setHasil] = useState<ExamScore | null>(null)
  useEffect(() => {
  if (Object.keys(jawaban).length > 0) {
    localStorage.setItem(`pendalaman-${paketId}`, JSON.stringify(jawaban))
  }
}, [jawaban, paketId])
  const [userId, setUserId] = useState<string | null>(null)
  const [access, setAccess] = useState<AccessLevel>('gratis')

  useEffect(() => {
    const init = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) { router.push('/login'); return }
      setUserId(user.id)

      const { data: p } = await supabase
        .from('paket_pendalaman')
        .select('*, topik_materi(nama)')
        .eq('id', paketId)
        .single()
      if (!p || p.status !== 'aktif') { router.push('/dashboard'); return }

      // Cek akses
      const statusUser = await getUserStatus(user.id)
      if (!bisaAkses(statusUser, requiredAccess(p))) {
        router.push('/dashboard?akses=ditolak')
        return
      }

      setAccess(statusUser)
      setPaket(p)
      
      const { data: soal } = await supabase
        .from('soal_pendalaman')
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
    await supabase.from('hasil_pendalaman').insert({
      user_id: userId,
      paket_id: paketId,
      total_soal: soalList.length,
      poin_benar: benar,
      poin_salah: salah,
      poin_kosong: kosong,
      total_poin: totalPoin,
    })
    setHasil({ benar, salah, kosong, totalPoin })
    localStorage.removeItem(`pendalaman-${paketId}`)
    setSubmitted(true)
  }, [userId, paket, soalList, jawaban, paketId])

  if (loading) return <PageLoading>Memuat soal…</PageLoading>

  const title = paket?.nama || 'Latihan'
  if (submitted && hasil) return (
    <ExamResults mode="Latihan" title={title} score={hasil} questions={soalList} answers={jawaban}
      offer={<UpgradeOffer access={access} mode="Latihan" />} />
  )

  return (
    <ExamScreen mode="Latihan" title={title} topic={paket?.topik_materi?.nama} questions={soalList} answers={jawaban}
      index={currentIndex} onNavigate={setCurrentIndex} onFinish={handleSubmit}
      onAnswer={(id, answer) => setJawaban(previous => ({ ...previous, [id]: answer }))} />
  )
}
