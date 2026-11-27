'use client'

import { useEffect, useState } from 'react'
import { Copy, Eye, EyeOff, KeyRound, Printer, RotateCcw, Users } from 'lucide-react'
import { supabase } from '../lib/supabase'
import { accessLabels } from '../lib/membership'
import { kelasRequest, printLoginCards, type Kelas, type KelasAnggota } from '../lib/kelas'
import { accuracy, KpiCard, MeterBar } from './overview'

type Result = {
  user_id: string
  created_at: string | null
  total_poin: number | null
  total_soal: number | null
  poin_benar: number | null
  poin_salah: number | null
  poin_kosong: number | null
  paket_to?: { nama: string } | null
  paket_pendalaman?: { nama: string; topik_materi?: { nama: string } | null } | null
}
type Student = KelasAnggota & { nama: string | null; kelasSiswa: string | null }
type ClassData = { kelas: Kelas; students: Student[] }

const dateFormat = new Intl.DateTimeFormat('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })
const fmtDate = (value: string | null) => value ? dateFormat.format(new Date(value.endsWith('Z') || value.includes('+') ? value : value + 'Z')) : '—'
const avg = (values: number[]) => values.length ? Math.round(values.reduce((a, b) => a + b, 0) / values.length) : null
const placeholderName = (nama: string | null) => !nama || /^Siswa \d+$/.test(nama)
const DAY = 86400000

function topicStats(rows: Result[]) {
  const byTopic = new Map<string, number[]>()
  for (const row of rows) {
    const topic = row.paket_pendalaman?.topik_materi?.nama
    const acc = accuracy(row)
    if (!topic || acc === null) continue
    byTopic.set(topic, [...(byTopic.get(topic) ?? []), acc])
  }
  return [...byTopic.entries()].map(([topic, values]) => ({ topic, accuracy: avg(values) as number, attempts: values.length }))
    .sort((a, b) => a.accuracy - b.accuracy)
}

async function loadClassroom(userId: string): Promise<{ classes: ClassData[]; tryouts: Result[]; practices: Result[] }> {
  const { data: kelasRows } = await supabase.from('kelas').select('*').eq('guru_id', userId).order('created_at')
  const list = (kelasRows ?? []) as Kelas[]
  if (!list.length) return { classes: [], tryouts: [], practices: [] }
  const { data: memberRows } = await supabase.from('kelas_anggota').select('*').in('kelas_id', list.map(k => k.id)).order('username')
  const members = (memberRows ?? []) as KelasAnggota[]
  const ids = members.map(m => m.user_id)
    const [profiles, to, pd] = await Promise.all([
      supabase.from('profiles').select('id, nama, kelas').in('id', ids),
      supabase.from('hasil_to').select('user_id, created_at, total_poin, total_soal, poin_benar, poin_salah, poin_kosong, paket_to(nama)')
        .in('user_id', ids).order('created_at', { ascending: true }),
      supabase.from('hasil_pendalaman').select('user_id, created_at, total_poin, total_soal, poin_benar, poin_salah, poin_kosong, paket_pendalaman(nama, topik_materi(nama))')
        .in('user_id', ids).order('created_at', { ascending: true }),
    ])
  const names = new Map((profiles.data ?? []).map(p => [p.id as string, p as { nama: string | null; kelas: string | null }]))
  return {
    tryouts: (to.data ?? []) as unknown as Result[],
    practices: (pd.data ?? []) as unknown as Result[],
    classes: list.map(kelas => ({
      kelas,
      students: members.filter(m => m.kelas_id === kelas.id)
        .map(m => ({ ...m, nama: names.get(m.user_id)?.nama ?? null, kelasSiswa: names.get(m.user_id)?.kelas ?? null })),
    })),
  }
}

/** Guru view: the classes this account teaches, their logins, and each student's progress. */
export function ClassroomPanel({ userId }: { userId: string }) {
  const [classes, setClasses] = useState<ClassData[] | null>(null)
  const [tryouts, setTryouts] = useState<Result[]>([])
  const [practices, setPractices] = useState<Result[]>([])
  const [shown, setShown] = useState<Record<string, boolean>>({})
  const [busy, setBusy] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    void loadClassroom(userId).then(data => {
      if (!active) return
      setTryouts(data.tryouts); setPractices(data.practices); setClasses(data.classes)
    })
    return () => { active = false }
  }, [userId])

  const reset = async (student: Student) => {
    if (busy) return
    if (!window.confirm(`Buat kata sandi baru untuk ${student.username}? Kata sandi lama tidak berlaku lagi.`)) return
    setBusy(student.user_id); setNotice(null)
    try {
      const res = await kelasRequest<{ password: string }>({ action: 'reset_password', user_id: student.user_id })
      setClasses(prev => prev?.map(c => ({ ...c, students: c.students.map(s => s.user_id === student.user_id ? { ...s, password_awal: res.password } : s) })) ?? null)
      setShown(prev => ({ ...prev, [student.user_id]: true }))
      setNotice(`Kata sandi baru ${student.username}: ${res.password}`)
    } catch (error) {
      setNotice(error instanceof Error ? error.message : 'Gagal mereset kata sandi.')
    } finally { setBusy(null) }
  }

  if (classes === null) return <p className="text-sm text-gray-500" role="status">Memuat kelas…</p>
  if (!classes.length) return <div className="learn-empty">Belum ada kelas. Kelas muncul di sini setelah Paket Kelas diaktifkan admin.</div>

  return (
    <div className="grid gap-8">
      {notice && <p className="atlas-notice" role="status">{notice}</p>}
      {classes.map(({ kelas, students }) => {
        const ids = new Set(students.map(s => s.user_id))
        const to = tryouts.filter(r => ids.has(r.user_id))
        const pd = practices.filter(r => ids.has(r.user_id))
        const recent = new Set([...to, ...pd].filter(r => r.created_at && Date.now() - Date.parse(r.created_at) < 7 * DAY).map(r => r.user_id))
        const toAcc = to.flatMap(r => { const a = accuracy(r); return a === null ? [] : [a] })
        const weakTopics = topicStats(pd).filter(t => t.attempts >= 1).slice(0, 3)
        const copyText = students.map(s => `${s.username} / ${s.password_awal ?? '(sudah diganti siswa)'}`).join('\n')
        return (
          <section key={kelas.id} className="grid gap-4" aria-labelledby={'kelas-' + kelas.id}>
            <header className="flex flex-wrap items-end justify-between gap-3">
              <div>
                <span className="dash-eyebrow"><Users size={13} aria-hidden="true" className="mr-1 inline" />Paket Kelas · {accessLabels[kelas.akses]}</span>
                <h3 id={'kelas-' + kelas.id} className="text-xl font-bold">{kelas.nama}</h3>
                <p className="text-sm text-gray-600">{students.length} siswa · berlaku sampai {fmtDate(kelas.berlaku_sampai)}</p>
              </div>
              <div className="flex flex-wrap gap-2">
                <button type="button" className="atlas-button" onClick={() => {
                  if (!printLoginCards(kelas.nama, students.map(s => ({ username: s.username, password: s.password_awal, nama: s.nama }))))
                    setNotice('Izinkan pop-up untuk mencetak kartu login.')
                }}><Printer size={16} aria-hidden="true" /> Cetak kartu login</button>
                <button type="button" className="atlas-button" onClick={async () => {
                  try { await navigator.clipboard.writeText(`Login OSNGEO.id · ${kelas.nama}\nosngeo.id/login\n\n${copyText}`); setNotice('Daftar login disalin. Tempel ke grup WhatsApp kelas.') }
                  catch { setNotice('Tidak bisa menyalin otomatis. Gunakan Cetak kartu login.') }
                }}><Copy size={16} aria-hidden="true" /> Salin daftar login</button>
              </div>
            </header>

            <dl className="dash-kpis">
              <KpiCard label="Siswa aktif 7 hari" value={`${recent.size}/${students.length}`} hint="mengerjakan tryout atau latihan" />
              <KpiCard label="Rata-rata akurasi tryout" value={avg(toAcc)} unit="%" hint={to.length + ' sesi tryout'} />
              <KpiCard label="Sesi pendalaman" value={pd.length} hint="latihan per topik" />
              <KpiCard label="Belum mulai" value={students.filter(s => !to.some(r => r.user_id === s.user_id) && !pd.some(r => r.user_id === s.user_id)).length} unit="siswa" />
            </dl>

            <div className="atlas-card dash-panel">
              <h4 className="font-bold">Topik terlemah kelas</h4>
              {weakTopics.length ? (
                <ul className="mt-3 grid gap-3">
                  {weakTopics.map(t => (
                    <li key={t.topic} className="grid gap-1 text-sm">
                      <div className="flex justify-between gap-3"><span>{t.topic}</span><strong>{t.accuracy}%</strong></div>
                      <MeterBar value={t.accuracy} label={`Akurasi ${t.topic} ${t.accuracy}%`} />
                    </li>
                  ))}
                </ul>
              ) : <p className="mt-2 text-sm text-gray-500">Muncul setelah siswa mengerjakan soal pendalaman materi.</p>}
            </div>

            <div className="atlas-card overflow-x-auto">
              <table className="classroom-table">
                <thead>
                  <tr><th>Siswa</th><th>Login</th><th>Tryout</th><th>Pendalaman</th><th>Topik terlemah</th><th>Terakhir aktif</th><th aria-label="Aksi" /></tr>
                </thead>
                <tbody>
                  {students.map(s => {
                    const st = to.filter(r => r.user_id === s.user_id)
                    const sp = pd.filter(r => r.user_id === s.user_id)
                    const last = st[st.length - 1]
                    const lastAcc = last ? accuracy(last) : null
                    const spAcc = avg(sp.flatMap(r => { const a = accuracy(r); return a === null ? [] : [a] }))
                    const weak = topicStats(sp)[0]
                    const lastActive = [...st, ...sp].map(r => r.created_at).filter(Boolean).sort().pop() ?? null
                    return (
                      <tr key={s.user_id}>
                        <td>
                          <strong className={placeholderName(s.nama) ? 'font-normal italic text-gray-500' : ''}>{placeholderName(s.nama) ? 'Belum mengisi nama' : s.nama}</strong>
                          {s.kelasSiswa && <span className="block text-xs text-gray-500">{s.kelasSiswa}</span>}
                        </td>
                        <td>
                          <span className="block font-mono text-sm font-semibold">{s.username}</span>
                          {s.password_awal ? (
                            <button type="button" className="classroom-secret" onClick={() => setShown(p => ({ ...p, [s.user_id]: !p[s.user_id] }))}
                              aria-label={shown[s.user_id] ? 'Sembunyikan kata sandi' : 'Tampilkan kata sandi'}>
                              {shown[s.user_id] ? <EyeOff size={13} aria-hidden="true" /> : <Eye size={13} aria-hidden="true" />}
                              <span className="font-mono">{shown[s.user_id] ? s.password_awal : '••••••••'}</span>
                            </button>
                          ) : <span className="block text-xs text-gray-500"><KeyRound size={12} aria-hidden="true" className="mr-1 inline" />diganti siswa</span>}
                        </td>
                        <td>{st.length ? <>{st.length}× <span className="block text-xs text-gray-500">terakhir {last?.total_poin ?? '—'} poin{lastAcc !== null ? ` · ${lastAcc}%` : ''}</span></> : <span className="text-gray-400">—</span>}</td>
                        <td>{sp.length ? <>{sp.length}× <span className="block text-xs text-gray-500">rata-rata {spAcc ?? '—'}%</span></> : <span className="text-gray-400">—</span>}</td>
                        <td>{weak ? <>{weak.topic} <span className="block text-xs text-gray-500">{weak.accuracy}%</span></> : <span className="text-gray-400">—</span>}</td>
                        <td className="whitespace-nowrap">{fmtDate(lastActive)}</td>
                        <td>
                          <button type="button" className="atlas-button classroom-reset" disabled={busy === s.user_id} onClick={() => reset(s)}>
                            <RotateCcw size={14} aria-hidden="true" /> {busy === s.user_id ? 'Memproses…' : 'Reset sandi'}
                          </button>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </section>
        )
      })}
    </div>
  )
}
