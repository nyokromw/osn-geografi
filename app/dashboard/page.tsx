'use client'

import Link from 'next/link'
import { useEffect, useState, type ReactNode } from 'react'
import type { User } from '@supabase/supabase-js'
import { ArrowRight, BookOpen, CheckCircle2, CircleDashed, ClipboardList, Clock, FileText, LayoutDashboard, Layers3, Lock, LogOut, Megaphone, MessageCircle, ShieldCheck, Ticket, Video } from 'lucide-react'
import { Notice, PageLoading, WorkspaceHeader } from '../components/atlas'
import { MembershipPlans } from '../components/membership-plans'
import { accessLabels, activeAccess, adminWhatsApp, bisaAkses, membershipExpiry, requiredAccess, type AccessLevel, type MembershipPlan } from '../lib/membership'
import { supabase } from '../lib/supabase'
import { tryoutLevel, tryoutLevelLabels, tryoutLevelOptions, type TryoutLevelFilter } from '../lib/tryout-levels'
import { groupTryoutPackages, predictionYear, tryoutCategories, tryoutCategory, tryoutCategoryLabels, type TryoutCategoryFilter } from '../lib/tryout-catalog'
import { LearningProgress, type StudyResult } from './learning-progress'
import { LearningVideoCard, type LearningVideo } from './learning-video'
import { accuracy, activityByDay, ActivityHeatmap, DashboardHero, KpiCard, MeterBar, QuickLink, studyStreak } from './overview'
import './dashboard.css'

const menu = [
  { key: 'dashboard', label: 'Dashboard', Icon: LayoutDashboard },
  { key: 'tryout', label: 'Tryout', Icon: ClipboardList },
  { key: 'pendalaman', label: 'Soal Pendalaman Materi', Icon: Layers3 },
  { key: 'video', label: 'Video', Icon: Video },
  { key: 'modul', label: 'Modul', Icon: FileText },
  { key: 'pengumuman', label: 'Pengumuman', Icon: Megaphone },
  { key: 'paket', label: 'Paket dan akses', Icon: Ticket },
] as const

type Tab = (typeof menu)[number]['key']
type Profile = { nama: string | null; status: string | null; status_expired: string | null; role: string | null }
type TryoutPackage = {
  id: number
  nama: string
  jenis: string
  kategori?: string | null
  tahun: number | null
  durasi_menit: number
  deskripsi: string | null
  akses?: string | null
  is_premium?: boolean | null
}

const questionAccessLabels: Record<AccessLevel, string> = {
  gratis: 'Gratis',
  premium: 'Premium + Platinum',
  platinum: 'Khusus Platinum',
}

function QuestionAccessBadge({ access, label }: { access: AccessLevel; label?: string }) {
  return <span className="access-badge" data-access={access}>{label ?? questionAccessLabels[access]}</span>
}

type PracticeRow = { paket_id: number | null; created_at: string | null; poin_benar: number | null; poin_salah: number | null; poin_kosong: number | null; total_soal: number | null; total_poin: number | null }

function bestAccuracy(rows: PracticeRow[]) {
  const values = rows.flatMap(row => { const value = accuracy(row); return value === null ? [] : [value] })
  return values.length ? Math.max(...values) : null
}

const resultColumns = 'id, paket_id, created_at, total_poin, total_soal, poin_benar, poin_salah, poin_kosong'
const dateFormat = new Intl.DateTimeFormat('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })

function formatDate(date: string | null) {
  if (!date) return ''
  const value = membershipExpiry(date)
  return Number.isFinite(value) ? dateFormat.format(value) : ''
}

function SectionHead({ eyebrow, title, detail, children }: { eyebrow: string; title: string; detail?: string; children?: ReactNode }) {
  return (
    <header className="dash-section-head">
      <div>
        <span className="dash-eyebrow">{eyebrow}</span>
        <h2>{title}</h2>
        {detail && <p>{detail}</p>}
      </div>
      {children}
    </header>
  )
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<Tab>('dashboard')
  const [tryoutFilter, setTryoutFilter] = useState<TryoutLevelFilter>('semua')
  const [categoryFilter, setCategoryFilter] = useState<TryoutCategoryFilter>('semua')
  const [accessDenied, setAccessDenied] = useState(false)
  const [riwayat, setRiwayat] = useState<StudyResult[]>([])
  const [practiceResults, setPracticeResults] = useState<StudyResult[]>([])
  const [practiceAll, setPracticeAll] = useState<PracticeRow[]>([])
  const [videoTopic, setVideoTopic] = useState('semua')
  const [loadErrors, setLoadErrors] = useState({ tryout: false, latihan: false })

  const [paketTO, setPaketTO] = useState<TryoutPackage[]>([])
  const [topikList, setTopikList] = useState<any[]>([])
  const [paketPendalaman, setPaketPendalaman] = useState<any[]>([])
  const [videoList, setVideoList] = useState<LearningVideo[]>([])
  const [modulList, setModulList] = useState<any[]>([])
  const [pengumumanList, setPengumumanList] = useState<any[]>([])
  const [membershipList, setMembershipList] = useState<MembershipPlan[]>([])
  const [upgradePlanId, setUpgradePlanId] = useState<number | null>(null)
  const [selectedTopik, setSelectedTopik] = useState<any>(null)

  useEffect(() => {
    let active = true
    const init = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!active) return
      if (!user) { window.location.href = '/login'; return }
      setUser(user)

      const params = new URLSearchParams(window.location.search)
      const tab = params.get('tab')
      if (params.get('akses') === 'ditolak') {
        setAccessDenied(true)
        setActiveTab('paket')
        window.history.replaceState({}, '', '/dashboard')
      } else if (tab === 'modul' || tab === 'video' || tab === 'tryout') {
        setActiveTab(tab)
        window.history.replaceState({}, '', '/dashboard')
      }

      const [account, tryouts, practices, pt, tp, pp, v, m, pg, mb, allPractices] = await Promise.all([
        supabase.from('profiles').select('nama, status, status_expired, role').eq('id', user.id).single(),
        supabase.from('hasil_to').select(resultColumns + ', paket_to(nama)')
          .eq('user_id', user.id).order('created_at', { ascending: true, nullsFirst: true }).order('id')
          .overrideTypes<StudyResult[], { merge: false }>(),
        supabase.from('hasil_pendalaman').select(resultColumns + ', paket_pendalaman(nama)')
          .eq('user_id', user.id).order('created_at', { ascending: false, nullsFirst: false }).order('id', { ascending: false })
          .limit(12).overrideTypes<StudyResult[], { merge: false }>(),
        supabase.from('paket_to').select('*').eq('status', 'aktif').order('urutan'),
        supabase.from('topik_materi').select('*').order('urutan'),
        supabase.from('paket_pendalaman').select('*, topik_materi(nama)').eq('status', 'aktif').order('id'),
        supabase.from('video_pembelajaran').select('*, topik_materi(nama)').order('urutan'),
        supabase.from('modul_materi').select('*, topik_materi(nama)').order('id'),
        supabase.from('pengumuman').select('*').eq('aktif', true).order('created_at', { ascending: false }),
        supabase.from('paket_membership').select('*').order('id'),
        supabase.from('hasil_pendalaman').select('paket_id, created_at, poin_benar, poin_salah, poin_kosong, total_soal, total_poin')
          .eq('user_id', user.id).overrideTypes<PracticeRow[], { merge: false }>(),
      ])
      if (!active) return

      setProfile(account.data)
      setRiwayat(tryouts.data ?? [])
      setPracticeResults((practices.data ?? []).slice().reverse())
      setPracticeAll(allPractices.data ?? [])
      setLoadErrors({ tryout: !!tryouts.error, latihan: !!practices.error })
      setPaketTO(pt.data ?? [])
      setTopikList(tp.data ?? [])
      setPaketPendalaman(pp.data ?? [])
      const access = account.data?.role === 'admin' ? 'platinum' : activeAccess(account.data)
      setVideoList((v.data ?? []).filter(item => item.aktif !== false && bisaAkses(access, requiredAccess(item, true))))
      setModulList((m.data ?? []).filter(item => item.aktif !== false && bisaAkses(access, requiredAccess(item, true))))
      setPengumumanList(pg.data ?? [])
      setMembershipList(mb.data ?? [])
      setLoading(false)
    }
    void init()
    return () => { active = false }
  }, [])

  useEffect(() => {
    if (activeTab !== 'paket' || upgradePlanId === null) return
    const plan = document.getElementById(`membership-plan-${upgradePlanId}`)
    plan?.scrollIntoView({ block: 'start' })
    plan?.focus({ preventScroll: true })
  }, [activeTab, upgradePlanId])

  if (loading) return <PageLoading>Memuat dashboard…</PageLoading>

  const nama = user?.user_metadata?.nama || profile?.nama || 'Siswa'
  const namaDepan = String(nama).trim().split(/\s+/)[0] || 'Siswa'
  const statusAkun = activeAccess(profile)
  const learningAccess = profile?.role === 'admin' ? 'platinum' : statusAkun
  const expiry = statusAkun !== 'gratis' && profile?.status_expired ? formatDate(profile.status_expired) : undefined

  const scored = riwayat.filter(item => item.total_poin !== null)
  const points = scored.map(item => item.total_poin as number)
  const accuracies = riwayat.flatMap(item => { const value = accuracy(item); return value === null ? [] : [value] })
  const lastTwo = (values: number[]) => values.length >= 2 ? values[values.length - 1] - values[values.length - 2] : null
  const average = (values: number[]) => values.length ? Math.round(values.reduce((sum, value) => sum + value, 0) / values.length) : null
  const activity = activityByDay([...riwayat, ...practiceAll])
  const streak = studyStreak(activity)
  const totalSessions = riwayat.length + practiceAll.length

  const practiceByPackage = new Map<number, PracticeRow[]>()
  for (const row of practiceAll) {
    if (row.paket_id === null) continue
    practiceByPackage.set(row.paket_id, [...(practiceByPackage.get(row.paket_id) ?? []), row])
  }
  const tryoutByPackage = new Map<number, StudyResult[]>()
  for (const row of riwayat) {
    if (!row.paket_id) continue
    tryoutByPackage.set(row.paket_id, [...(tryoutByPackage.get(row.paket_id) ?? []), row])
  }

  const videoTopics = Array.from(new Set(videoList.map(video => video.topik_materi?.nama).filter((name): name is string => !!name)))
  const shownVideos = videoTopic === 'semua' ? videoList : videoList.filter(video => video.topik_materi?.nama === videoTopic)

  const navTo = (tab: Tab) => {
    setActiveTab(tab)
    setSelectedTopik(null)
    setAccessDenied(false)
    setUpgradePlanId(null)
    window.scrollTo({ top: 0, behavior: 'auto' })
  }

  const openUpgrade = (access: AccessLevel) => {
    const plans = membershipList.filter(plan => plan.akses === access)
    const target = plans.find(plan => plan.aktif) ?? plans[0]
    navTo('paket')
    setUpgradePlanId(target?.id ?? null)
  }

  return (
    <>
      <WorkspaceHeader title="Ruang belajar">
        {profile?.role === 'admin' && (
          <Link href="/admin" className="atlas-button" aria-label="Panel admin" title="Panel admin">
            <ShieldCheck size={16} aria-hidden="true" /><span className="hidden sm:inline">Admin</span>
          </Link>
        )}
        <a href={adminWhatsApp} target="_blank" rel="noreferrer"
          className="atlas-button" aria-label="Bantuan WhatsApp" title="Bantuan WhatsApp">
          <MessageCircle size={16} aria-hidden="true" /><span className="hidden sm:inline">Bantuan</span>
        </a>
        <button type="button" className="atlas-button" aria-label="Keluar akun" title="Keluar akun"
          onClick={async () => { await supabase.auth.signOut(); window.location.href = '/login' }}>
          <LogOut size={16} aria-hidden="true" /><span className="hidden sm:inline">Keluar</span>
        </button>
      </WorkspaceHeader>
      <div className="atlas-tabs-wrap">
        <nav className="atlas-container atlas-tabs" aria-label="Ruang belajar">
          {menu.map(({ key, label, Icon }) => (
            <button key={key} type="button" aria-current={activeTab === key ? 'page' : undefined} onClick={() => navTo(key)}>
              <Icon size={16} aria-hidden="true" /> {label}
            </button>
          ))}
        </nav>
      </div>

      <main className="atlas-container atlas-work-content">
        {accessDenied && (
          <div className="mb-4"><Notice error>Konten ini memerlukan paket berbayar. Pilih tingkat akses yang sesuai.</Notice></div>
        )}

        {/* ── DASHBOARD ─────────────────────────────────────────── */}
        {activeTab === 'dashboard' && (
          <div className="space-y-6">
            <DashboardHero name={namaDepan} access={statusAkun} accessLabel={accessLabels[statusAkun]} expiry={expiry} streak={streak}>
              <button type="button" className="atlas-button atlas-button--primary" onClick={() => navTo('tryout')}>
                Kerjakan tryout <ArrowRight size={16} aria-hidden="true" />
              </button>
              <button type="button" className="atlas-button" onClick={() => navTo('paket')}>
                <Ticket size={16} aria-hidden="true" /> Paket saya
              </button>
            </DashboardHero>

            <dl className="dash-kpis">
              <KpiCard label="Sesi selesai" value={loadErrors.tryout ? null : totalSessions}
                hint={`${riwayat.length} tryout · ${practiceAll.length} soal pendalaman materi`} />
              <KpiCard label="Poin tryout terakhir" value={points.length ? points[points.length - 1] : null} unit="poin"
                delta={lastTwo(points)} />
              <KpiCard label="Akurasi tryout terakhir" value={accuracies.length ? accuracies[accuracies.length - 1] : null} unit="%"
                delta={lastTwo(accuracies)} deltaUnit="%" />
              <KpiCard label="Rata-rata poin" value={average(points)} unit="poin"
                hint={points.length ? `Tertinggi ${Math.max(...points)} · terendah ${Math.min(...points)}` : 'Belum ada tryout'} />
            </dl>

            <LearningProgress tryouts={riwayat} practices={practiceResults} loadErrors={loadErrors}
              openPractice={mode => navTo(mode === 'tryout' ? 'tryout' : 'pendalaman')} />

            <div className="grid items-start gap-4 lg:grid-cols-[minmax(0,1.7fr)_minmax(0,1fr)]">
              <section className="atlas-card overflow-hidden" aria-labelledby="riwayat-title">
                <header className="flex items-center justify-between border-b border-gray-200 px-4 py-4">
                  <h3 id="riwayat-title" className="font-bold">Riwayat tryout</h3>
                  <span className="text-xs text-gray-500">{riwayat.length} sesi</span>
                </header>
                {riwayat.length ? (
                  <ul className="dash-history max-h-[26rem] overflow-y-auto">
                    {riwayat.slice().reverse().map(item => {
                      const acc = accuracy(item)
                      return (
                        <li key={item.id}>
                          <div className="min-w-0">
                            <h4>{item.paket_to?.nama || 'Tryout'}</h4>
                            <div className="dash-history-meta">
                              {item.poin_benar !== null && <span>{item.poin_benar} benar</span>}
                              {item.poin_salah !== null && <span>{item.poin_salah} salah</span>}
                              {item.poin_kosong !== null && <span>{item.poin_kosong} kosong</span>}
                              {item.created_at && <time dateTime={item.created_at}>{formatDate(item.created_at)}</time>}
                            </div>
                          </div>
                          <div className="dash-history-acc">
                            {acc !== null && <><span>Akurasi {acc}%</span><MeterBar value={acc} label={'Akurasi ' + acc + '%'} /></>}
                          </div>
                          <div className="dash-history-score"><strong>{item.total_poin ?? '—'}</strong><span>poin</span></div>
                        </li>
                      )
                    })}
                  </ul>
                ) : (
                  <p className="px-4 py-5 text-sm text-gray-500">{loadErrors.tryout ? 'Riwayat tryout belum dapat dimuat.' : 'Belum ada riwayat tryout.'}</p>
                )}
              </section>
              <div className="grid gap-4">
                <ActivityHeatmap days={activity} />
                <section className="atlas-card dash-panel" aria-labelledby="lanjut-title">
                  <h3 id="lanjut-title" className="font-bold">Lanjut belajar</h3>
                  <div className="mt-3 grid gap-2">
                    <QuickLink icon={<ClipboardList size={18} />} label="Tryout" detail={paketTO.length + ' paket'} onClick={() => navTo('tryout')} />
                    <QuickLink icon={<Layers3 size={18} />} label="Pendalaman materi" detail={topikList.length + ' topik'} onClick={() => navTo('pendalaman')} />
                    <QuickLink icon={<BookOpen size={18} />} label="Video pembelajaran" detail={videoList.length + ' video'} onClick={() => navTo('video')} />
                    <QuickLink icon={<FileText size={18} />} label="Modul" detail={modulList.length + ' modul'} onClick={() => navTo('modul')} />
                  </div>
                </section>
              </div>
            </div>
          </div>
        )}

        {/* ── TRYOUT ───────────────────────────────────────────── */}
        {activeTab === 'tryout' && (
          <div>
            <SectionHead eyebrow="Ujian simulasi" title="Paket tryout" detail="Pilih paket tryout OSN Geografi yang ingin dikerjakan." />

            {paketTO.length > 0 && (
              <div className="mb-2 flex flex-wrap gap-x-6">
                <div role="group" aria-label="Filter jenjang tryout" className="learn-filter">
                  {(['semua', ...tryoutLevelOptions] as TryoutLevelFilter[])
                    .filter(jenjang => jenjang === 'semua' || paketTO.some(paket => tryoutLevel(paket.jenis) === jenjang))
                    .map(jenjang => (
                      <button key={jenjang} type="button" aria-pressed={tryoutFilter === jenjang} onClick={() => setTryoutFilter(jenjang)}>
                        {jenjang === 'semua' ? 'Semua jenjang' : tryoutLevelLabels[jenjang]}
                      </button>
                    ))}
                </div>
                <div role="group" aria-label="Filter kategori tryout" className="learn-filter">
                  {(['semua', ...tryoutCategories] as TryoutCategoryFilter[]).map(category => (
                    <button key={category} type="button" aria-pressed={categoryFilter === category} onClick={() => setCategoryFilter(category)}>
                      {category === 'semua' ? 'Semua kategori' : tryoutCategoryLabels[category]}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {categoryFilter === 'prediksi' && !paketTO.some(p =>
              tryoutCategory(p.kategori) === 'prediksi' && p.tahun === predictionYear &&
              (tryoutFilter === 'semua' || tryoutLevel(p.jenis) === tryoutFilter)
            ) && <p className="atlas-notice mb-6">Prediksi {predictionYear} untuk jenjang ini belum diterbitkan.</p>}

            {tryoutLevelOptions.filter(jenjang => tryoutFilter === 'semua' || tryoutFilter === jenjang).map(jenjang => {
              const list = paketTO.filter(p => tryoutLevel(p.jenis) === jenjang &&
                (categoryFilter === 'semua' || tryoutCategory(p.kategori) === categoryFilter))
              if (list.length === 0) return null
              return (
                <section key={jenjang} aria-label={tryoutLevelLabels[jenjang]} className="mb-9">
                  <div className="mb-4 flex items-center gap-3">
                    <h3 className="text-lg font-bold">{tryoutLevelLabels[jenjang]}</h3>
                    <div className="h-px flex-1 bg-gray-200" />
                    <span className="text-xs text-gray-500">{list.length} paket</span>
                  </div>
                  {groupTryoutPackages(list).map(([category, packages]) => (
                    <div key={category} className="mb-6">
                      <h4 className="mb-3 text-sm font-bold text-clay-600">{category}</h4>
                      <div className="learn-grid">
                        {packages.map(p => {
                          const access = requiredAccess(p)
                          const locked = !bisaAkses(learningAccess, access)
                          const done = tryoutByPackage.get(p.id) ?? []
                          const best = done.length ? Math.max(...done.map(row => row.total_poin ?? -Infinity)) : null
                          return (
                            <article key={p.id} className="learn-card" data-locked={locked}>
                              <div className="learn-card-body">
                                <div className="flex items-start justify-between gap-2">
                                  <QuestionAccessBadge access={access} />
                                  {p.durasi_menit ? <span className="learn-status"><Clock size={13} aria-hidden="true" /> {p.durasi_menit} menit</span> : null}
                                </div>
                                <h5>{p.nama}</h5>
                                {p.tahun && <p className="learn-card-meta">Tahun {p.tahun}</p>}
                                {p.deskripsi && <p className="text-xs leading-relaxed text-gray-600">{p.deskripsi}</p>}
                                <span className="learn-status" data-done={done.length > 0}>
                                  {done.length ? <><CheckCircle2 size={14} aria-hidden="true" /> Dikerjakan {done.length}× · terbaik {Number.isFinite(best) ? best : '—'} poin</>
                                    : <><CircleDashed size={14} aria-hidden="true" /> Belum dikerjakan</>}
                                </span>
                                <div className="learn-card-foot">
                                  {locked ? (
                                    <button type="button" onClick={() => openUpgrade(access)} className="atlas-button w-full">
                                      <Lock size={15} aria-hidden="true" /> Buka dengan {accessLabels[access]}
                                    </button>
                                  ) : (
                                    <Link href={`/tryout/${p.id}`} prefetch={false} className="atlas-button atlas-button--primary w-full">
                                      {done.length ? 'Kerjakan lagi' : 'Mulai tryout'} <ArrowRight size={15} aria-hidden="true" />
                                    </Link>
                                  )}
                                </div>
                              </div>
                            </article>
                          )
                        })}
                      </div>
                    </div>
                  ))}
                </section>
              )
            })}

            {!paketTO.some(p => (tryoutFilter === 'semua' || tryoutLevel(p.jenis) === tryoutFilter) &&
              (categoryFilter === 'semua' || tryoutCategory(p.kategori) === categoryFilter)) && (
              <div className="learn-empty">Belum ada paket tryout tersedia.</div>
            )}
          </div>
        )}

        {/* ── SOAL PENDALAMAN MATERI ─────────────────────────────────── */}
        {activeTab === 'pendalaman' && (
          <div>
            <SectionHead eyebrow="Latihan per topik" title="Soal Pendalaman Materi"
              detail={selectedTopik ? undefined : 'Pilih topik, kerjakan paketnya, dan lihat kemajuanmu per topik.'} />

            {!selectedTopik ? (
              <div className="learn-grid">
                {topikList.map((t, index) => {
                  const paketTopik = paketPendalaman.filter(p => p.topik_id === t.id)
                  const selesai = paketTopik.filter(p => practiceByPackage.has(p.id)).length
                  const persen = paketTopik.length ? Math.round(selesai / paketTopik.length * 100) : 0
                  return (
                    <button key={t.id} type="button" onClick={() => setSelectedTopik(t)}
                      className="learn-card topic-tile" data-done={paketTopik.length > 0 && selesai === paketTopik.length}>
                      <div className="topic-tile-top">
                        <span className="topic-tile-num">{String(index + 1).padStart(2, '0')}</span>
                        <ArrowRight size={18} className="text-gray-400" aria-hidden="true" />
                      </div>
                      <h3>{t.nama}</h3>
                      <div className="topic-tile-progress">
                        <div><span>{selesai}/{paketTopik.length} paket selesai</span><strong>{persen}%</strong></div>
                        <MeterBar value={persen} label={`${persen}% paket selesai`} />
                      </div>
                    </button>
                  )
                })}
                {topikList.length === 0 && <div className="learn-empty col-span-full">Belum ada topik tersedia.</div>}
              </div>
            ) : (
              <div>
                <nav className="learn-crumbs" aria-label="Lokasi">
                  <button type="button" onClick={() => setSelectedTopik(null)}>Semua topik</button>
                  <span className="text-gray-400" aria-hidden="true">›</span>
                  <span className="font-bold text-gray-800">{selectedTopik.nama}</span>
                </nav>

                <div className="learn-grid">
                  {paketPendalaman.filter(p => p.topik_id === selectedTopik.id).map(p => {
                    const access = requiredAccess(p)
                    const locked = !bisaAkses(learningAccess, access)
                    const rows = practiceByPackage.get(p.id) ?? []
                    const best = bestAccuracy(rows)
                    return (
                      <article key={p.id} className="learn-card" data-locked={locked}>
                        <div className="learn-card-body">
                          <div className="flex items-start justify-between gap-2">
                            <QuestionAccessBadge access={access} />
                            {p.durasi_menit ? <span className="learn-status"><Clock size={13} aria-hidden="true" /> {p.durasi_menit} menit</span> : null}
                          </div>
                          <h3>{p.nama}</h3>
                          {p.deskripsi && <p className="text-xs leading-relaxed text-gray-600">{p.deskripsi}</p>}
                          {rows.length > 0 && best !== null ? (
                            <div className="grid gap-1.5 text-xs text-gray-600">
                              <div className="flex justify-between"><span className="learn-status" data-done="true"><CheckCircle2 size={14} aria-hidden="true" /> Selesai {rows.length}×</span><strong>Terbaik {best}%</strong></div>
                              <MeterBar value={best} label={`Akurasi terbaik ${best}%`} />
                            </div>
                          ) : (
                            <span className="learn-status"><CircleDashed size={14} aria-hidden="true" /> Belum dikerjakan</span>
                          )}
                          <div className="learn-card-foot">
                            {locked ? (
                              <button type="button" onClick={() => openUpgrade(access)} className="atlas-button w-full">
                                <Lock size={15} aria-hidden="true" /> Buka dengan {accessLabels[access]}
                              </button>
                            ) : (
                              <a href={`/pendalaman/${p.id}`} className="atlas-button atlas-button--primary w-full">
                                {rows.length ? 'Latihan lagi' : 'Mulai latihan'} <ArrowRight size={15} aria-hidden="true" />
                              </a>
                            )}
                          </div>
                        </div>
                      </article>
                    )
                  })}
                  {paketPendalaman.filter(p => p.topik_id === selectedTopik.id).length === 0 && (
                    <div className="learn-empty col-span-full">Belum ada paket latihan untuk topik ini.</div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ── VIDEO PEMBELAJARAN ────────────────────────────────── */}
        {activeTab === 'video' && (
          <div>
            <SectionHead eyebrow="Belajar konsep" title="Video pembelajaran" detail={videoList.length + ' video tersedia untuk aksesmu.'} />
            {videoTopics.length > 1 && (
              <div role="group" aria-label="Filter topik video" className="learn-filter">
                {['semua', ...videoTopics].map(topic => (
                  <button key={topic} type="button" aria-pressed={videoTopic === topic} onClick={() => setVideoTopic(topic)}>
                    {topic === 'semua' ? 'Semua topik' : topic}
                  </button>
                ))}
              </div>
            )}
            <div className="learn-grid">
              {shownVideos.map(video => <LearningVideoCard key={video.id} video={video} />)}
              {shownVideos.length === 0 && <div className="learn-empty col-span-full">Belum ada video tersedia.</div>}
            </div>
          </div>
        )}

        {/* ── MODUL / PDF ───────────────────────────────────────── */}
        {activeTab === 'modul' && (
          <div>
            <SectionHead eyebrow="Bacaan mendalam" title="Modul belajar" detail={modulList.length + ' modul tersedia untuk aksesmu.'} />
            <div className="learn-grid">
              {modulList.map((m, index) => {
                const access = requiredAccess(m, true)
                return (
                  <article key={m.id} className="learn-card">
                    <div className="modul-cover" data-tone={index % 4}>
                      <div className="modul-cover-top">
                        <span>Modul {String(index + 1).padStart(2, '0')}</span>
                        <span>OSNGEO.id</span>
                      </div>
                      <h3>{m.judul}</h3>
                    </div>
                    <div className="learn-card-body">
                      <p className="learn-card-meta">
                        {[m.topik_materi?.nama, m.jumlah_halaman && m.jumlah_halaman + ' halaman'].filter(Boolean).join(' · ') || 'Modul OSN Geografi'}
                      </p>
                      {m.deskripsi && <p className="text-xs leading-relaxed text-gray-600">{m.deskripsi}</p>}
                      <div className="learn-card-foot">
                        <QuestionAccessBadge access={access} label={accessLabels[access]} />
                        {m.jumlah_halaman ? (
                          <Link href={'/modul/' + m.id} aria-label={'Baca ' + m.judul} className="atlas-button atlas-button--primary">
                            Baca modul <ArrowRight size={15} aria-hidden="true" />
                          </Link>
                        ) : m.file_url && (
                          <a href={m.file_url} target="_blank" rel="noreferrer" className="atlas-button atlas-button--primary">Buka modul <ArrowRight size={15} aria-hidden="true" /></a>
                        )}
                      </div>
                    </div>
                  </article>
                )
              })}
              {modulList.length === 0 && (
                <div className="learn-empty col-span-full">
                  {learningAccess === 'platinum' ? 'Belum ada modul tersedia.' : (
                    <>
                      <FileText size={28} className="text-forest-500" aria-hidden="true" />
                      <p className="text-gray-700">Modul lengkap 13 bab tersedia untuk akun Platinum.</p>
                      <button type="button" className="atlas-button atlas-button--primary" onClick={() => openUpgrade('platinum')}>
                        Lihat paket Platinum
                      </button>
                    </>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* ── PENGUMUMAN ────────────────────────────────────────── */}
        {activeTab === 'pengumuman' && (
          <div>
            <SectionHead eyebrow="Kabar terbaru" title="Pengumuman" detail="Informasi terbaru dari OSNGEO.id." />
            <div className="grid gap-3">
              {pengumumanList.map(p => {
                const date = new Date(p.created_at)
                return (
                  <article key={p.id ?? p.created_at} className="atlas-card news-item">
                    <time className="news-date" dateTime={p.created_at}>
                      <strong>{date.getDate()}</strong>
                      <span>{date.toLocaleDateString('id-ID', { month: 'short' })}</span>
                    </time>
                    <div className="min-w-0">
                      <h3 className="font-bold">{p.judul}</h3>
                      <p className="mt-1 whitespace-pre-line text-sm leading-relaxed text-gray-600">{p.isi}</p>
                      <p className="mt-2 text-xs text-gray-500">{date.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })}</p>
                    </div>
                  </article>
                )
              })}
              {pengumumanList.length === 0 && <div className="learn-empty">Belum ada pengumuman.</div>}
            </div>
          </div>
        )}

        {/* ── PAKET & UPGRADE ───────────────────────────────────── */}
        {activeTab === 'paket' && (
          <div>
            <SectionHead eyebrow="Keanggotaan" title="Paket dan akses"
              detail={`Akses saat ini ${accessLabels[statusAkun]}${expiry ? ` hingga ${expiry}` : ''}.`} />
            <MembershipPlans plans={membershipList} onFree={() => navTo('tryout')} highlightPlanId={upgradePlanId} />
          </div>
        )}
      </main>
    </>
  )
}
