'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import type { User } from '@supabase/supabase-js'
import { ArrowRight, BookOpen, ClipboardList, FileText, LayoutDashboard, Layers3, LogOut, Megaphone, MessageCircle, ShieldCheck, Ticket, Video } from 'lucide-react'
import { Notice, PageLoading, WorkspaceHeader } from '../components/atlas'
import { supabase } from '../lib/supabase'
import { LearningProgress, type StudyResult } from './learning-progress'

const menu = [
  { key: 'dashboard', label: 'Dashboard', Icon: LayoutDashboard },
  { key: 'tryout', label: 'Tryout', Icon: ClipboardList },
  { key: 'pendalaman', label: 'Pendalaman', Icon: Layers3 },
  { key: 'video', label: 'Video', Icon: Video },
  { key: 'modul', label: 'Modul', Icon: FileText },
  { key: 'pengumuman', label: 'Pengumuman', Icon: Megaphone },
  { key: 'paket', label: 'Paket dan akses', Icon: Ticket },
] as const

type Tab = (typeof menu)[number]['key']
type Profile = { nama: string | null; status: string | null; status_expired: string | null; role: string | null }

const resultColumns = 'id, created_at, total_poin, total_soal, poin_benar, poin_salah, poin_kosong'
const dateFormat = new Intl.DateTimeFormat('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })

function formatDate(date: string | null) {
  if (!date) return ''
  const value = new Date(date)
  return Number.isFinite(value.getTime()) ? dateFormat.format(value) : ''
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<Tab>('dashboard')
  const [accessDenied, setAccessDenied] = useState(false)
  const [riwayat, setRiwayat] = useState<StudyResult[]>([])
  const [practiceResults, setPracticeResults] = useState<StudyResult[]>([])
  const [loadErrors, setLoadErrors] = useState({ tryout: false, latihan: false })

  const [paketTO, setPaketTO] = useState<any[]>([])
  const [topikList, setTopikList] = useState<any[]>([])
  const [paketPendalaman, setPaketPendalaman] = useState<any[]>([])
  const [videoList, setVideoList] = useState<any[]>([])
  const [modulList, setModulList] = useState<any[]>([])
  const [pengumumanList, setPengumumanList] = useState<any[]>([])
  const [membershipList, setMembershipList] = useState<any[]>([])
  const [selectedTopik, setSelectedTopik] = useState<any>(null)

  useEffect(() => {
    let active = true
    const init = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!active) return
      if (!user) { window.location.href = '/login'; return }
      setUser(user)

      const params = new URLSearchParams(window.location.search)
      if (params.get('akses') === 'ditolak') {
        setAccessDenied(true)
        window.history.replaceState({}, '', '/dashboard')
      }

      const [account, tryouts, practices, pt, tp, pp, v, m, pg, mb] = await Promise.all([
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
      ])
      if (!active) return

      setProfile(account.data)
      setRiwayat(tryouts.data ?? [])
      setPracticeResults((practices.data ?? []).slice().reverse())
      setLoadErrors({ tryout: !!tryouts.error, latihan: !!practices.error })
      setPaketTO(pt.data ?? [])
      setTopikList(tp.data ?? [])
      setPaketPendalaman(pp.data ?? [])
      setVideoList(v.data ?? [])
      setModulList(m.data ?? [])
      setPengumumanList(pg.data ?? [])
      setMembershipList(mb.data ?? [])
      setLoading(false)
    }
    void init()
    return () => { active = false }
  }, [])

  if (loading) return <PageLoading>Memuat dashboard…</PageLoading>

  const points = riwayat.flatMap(item => item.total_poin === null ? [] : [item.total_poin])
  const stats = [
    ['Tryout selesai', loadErrors.tryout ? '—' : riwayat.length],
    ['Poin tertinggi', points.length ? Math.max(...points) : '—'],
    ['Rata-rata poin', points.length ? Math.round(points.reduce((total, value) => total + value, 0) / points.length) : '—'],
    ['Poin terendah', points.length ? Math.min(...points) : '—'],
  ]
  const nama = user?.user_metadata?.nama || profile?.nama || 'Siswa'
  const namaDepan = String(nama).trim().split(/\s+/)[0] || 'Siswa'
  const statusAkun = profile?.status || 'gratis'
  const activeMembership = statusAkun !== 'gratis' && (!profile?.status_expired || new Date(profile.status_expired) >= new Date())
  const membershipName = activeMembership ? statusAkun.charAt(0).toUpperCase() + statusAkun.slice(1) : 'Gratis'

  const navTo = (tab: Tab) => {
    setActiveTab(tab)
    setSelectedTopik(null)
    window.scrollTo({ top: 0, behavior: 'auto' })
  }

  return (
    <>
      <WorkspaceHeader title="Ruang belajar">
        {profile?.role === 'admin' && (
          <Link href="/admin" className="atlas-button" aria-label="Panel admin" title="Panel admin">
            <ShieldCheck size={16} aria-hidden="true" /><span className="hidden sm:inline">Admin</span>
          </Link>
        )}
        <a href="https://wa.me/6285157220761" target="_blank" rel="noreferrer"
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
          <div className="mb-4"><Notice error>Konten ini memerlukan akses premium. Pilih Paket dan akses untuk melihat opsi yang tersedia.</Notice></div>
        )}
        {activeTab === 'dashboard' && (
          <div className="space-y-7">
            <header className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <h1 className="atlas-title">Halo, {namaDepan}.</h1>
                <p className="mt-2 text-sm text-gray-500">{user?.email || 'Pantau hasil belajar dan pilih latihan berikutnya.'}</p>
              </div>
              <button type="button" className="atlas-button" onClick={() => navTo('paket')}>
                <Ticket size={16} aria-hidden="true" /> Akses {membershipName}
                {activeMembership && profile?.status_expired && (
                  <span className="text-xs text-gray-500">· s.d. {formatDate(profile.status_expired)}</span>
                )}
              </button>
            </header>

            <dl className="atlas-stat-strip">
              {stats.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}
            </dl>

            <LearningProgress tryouts={riwayat} practices={practiceResults} loadErrors={loadErrors}
              openPractice={mode => navTo(mode === 'tryout' ? 'tryout' : 'pendalaman')} />

            <div className="grid items-start gap-4 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
              <section className="atlas-card">
                <header className="flex items-center justify-between border-b border-gray-200 px-4 py-4">
                  <h2 className="font-bold">Riwayat tryout</h2>
                  <span className="text-xs text-gray-500">{riwayat.length} sesi</span>
                </header>
                {riwayat.length ? (
                  <ul className="divide-y divide-gray-100">
                    {riwayat.slice().reverse().map(item => (
                      <li key={item.id} className="flex items-center justify-between gap-4 px-4 py-3.5">
                        <div className="min-w-0">
                          <h3 className="break-words text-sm font-semibold">{item.paket_to?.nama || 'Tryout'}</h3>
                          <div className="mt-1 flex flex-wrap gap-x-2 gap-y-1 text-xs text-gray-500">
                            {item.poin_benar !== null && <span>{item.poin_benar} benar</span>}
                            {item.poin_salah !== null && <span>{item.poin_salah} salah</span>}
                            {item.poin_kosong !== null && <span>{item.poin_kosong} kosong</span>}
                            {item.created_at && <time dateTime={item.created_at}>{formatDate(item.created_at)}</time>}
                          </div>
                        </div>
                        <div className="shrink-0 text-right"><strong className="block text-xl tabular-nums">{item.total_poin ?? '—'}</strong><span className="text-xs text-gray-500">poin</span></div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="px-4 py-5 text-sm text-gray-500">{loadErrors.tryout ? 'Riwayat tryout belum dapat dimuat.' : 'Belum ada riwayat tryout.'}</p>
                )}
              </section>
              <section className="atlas-card bg-forest-50 p-4">
                <h2 className="font-bold">Lanjut belajar</h2>
                <div className="mt-3 grid gap-2">
                  {[
                    { tab: 'tryout', Icon: ClipboardList, label: 'Tryout', detail: paketTO.length + ' paket' },
                    { tab: 'pendalaman', Icon: Layers3, label: 'Pendalaman materi', detail: topikList.length + ' topik' },
                    { tab: 'video', Icon: BookOpen, label: 'Video pembelajaran', detail: videoList.length + ' video' },
                  ].map(({ tab, Icon, label, detail }) => (
                    <button key={tab} type="button" className="atlas-button justify-start text-left" onClick={() => navTo(tab as Tab)}>
                      <Icon size={17} aria-hidden="true" />
                      <span className="grow">{label}<small className="block font-normal text-gray-500">{detail}</small></span>
                      <ArrowRight size={16} aria-hidden="true" />
                    </button>
                  ))}
                </div>
              </section>
            </div>
          </div>
        )}

          {/* ── TRYOUT ───────────────────────────────────────────── */}
          {activeTab === 'tryout' && (
            <div>
              <div className="mb-6">
                <h2 className="text-xl font-black text-gray-800">Paket Tryout</h2>
                <p className="text-gray-500 text-sm">Pilih paket tryout OSN Geografi yang ingin dikerjakan</p>
              </div>

              {/* Filter jenis */}
              {['OSNK', 'OSNP', 'Nasional'].map(jenis => {
                const list = paketTO.filter(p => p.jenis === jenis)
                if (list.length === 0) return null
                return (
                  <div key={jenis} className="mb-8">
                    <div className="flex items-center gap-3 mb-3">
                      <h3 className="font-black text-gray-700">{jenis}</h3>
                      <div className="h-px flex-1 bg-gray-200" />
                      <span className="text-xs text-gray-400">{list.length} paket</span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {list.map((p) => (
                        <div key={p.id} className="bg-white border border-gray-200 rounded-xl p-5 hover:border-forest-300 hover:shadow-sm transition">
                          <div className="flex items-start justify-between mb-3">
                            <div>
                              <div className="font-bold text-gray-800 text-sm">{p.nama}</div>
                              <div className="text-xs text-gray-400 mt-0.5">{p.tahun || ''} · {p.durasi_menit} menit</div>
                            </div>
                            <span className={`text-xs font-bold px-2 py-0.5 rounded-full shrink-0 ml-2 ${
                              p.is_premium ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'
                            }`}>
                              {p.is_premium ? 'Premium' : 'Gratis'}
                            </span>
                          </div>
                          {p.deskripsi && <p className="text-xs text-gray-400 mb-3">{p.deskripsi}</p>}
                          {p.is_premium ? (
                            <button onClick={() => setActiveTab('paket')}
                              className="w-full bg-yellow-400 hover:bg-yellow-300 text-black text-sm font-bold py-2 rounded-lg transition">
                              Upgrade untuk Akses
                            </button>
                          ) : (
                            <a href={`/tryout/${p.id}`}
                              className="block w-full bg-forest-600 hover:bg-forest-700 text-white text-sm font-bold py-2 rounded-lg transition text-center">
                              Mulai Tryout →
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )
              })}

              {paketTO.length === 0 && (
                <div className="bg-white border border-gray-200 rounded-xl px-5 py-12 text-center text-gray-400 text-sm">
                  Belum ada paket tryout tersedia.
                </div>
              )}
            </div>
          )}
          {/* ── PENDALAMAN MATERI ─────────────────────────────────── */}
          {activeTab === 'pendalaman' && (
            <div>
              <div className="mb-6">
                <h2 className="text-xl font-black text-gray-800">Pendalaman Materi</h2>
                <p className="text-gray-500 text-sm">Latihan soal per topik OSN Geografi</p>
              </div>

              {!selectedTopik ? (
                /* LIST TOPIK */
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {topikList.map((t) => {
                    const paketTopik = paketPendalaman.filter(p => p.topik_id === t.id)
                    return (
                      <button key={t.id} onClick={() => setSelectedTopik(t)}
                        className="bg-white border border-gray-200 rounded-xl p-5 text-left hover:border-purple-400 hover:shadow-sm transition">
                        <div className="text-2xl mb-2">🧩</div>
                        <div className="font-bold text-gray-800 text-sm mb-1">{t.nama}</div>
                        <div className="text-xs text-gray-400">{paketTopik.length} paket latihan</div>
                      </button>
                    )
                  })}
                  {topikList.length === 0 && (
                    <div className="col-span-3 bg-white border border-gray-200 rounded-xl px-5 py-12 text-center text-gray-400 text-sm">
                      Belum ada topik tersedia.
                    </div>
                  )}
                </div>
              ) : (
                /* LIST PAKET PER TOPIK */
                <div>
                  <div className="flex items-center gap-2 mb-5 text-sm">
                    <button onClick={() => setSelectedTopik(null)}
                      className="text-forest-600 hover:underline font-medium">Pendalaman Materi</button>
                    <span className="text-gray-400">›</span>
                    <span className="font-bold text-gray-800">{selectedTopik.nama}</span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {paketPendalaman.filter(p => p.topik_id === selectedTopik.id).map((p) => (
                      <div key={p.id} className="bg-white border border-gray-200 rounded-xl p-5 hover:border-purple-300 hover:shadow-sm transition">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <div className="font-bold text-gray-800 text-sm">{p.nama}</div>
                            <div className="text-xs text-gray-400 mt-0.5">{p.durasi_menit} menit</div>
                          </div>
                          <span className={`text-xs font-bold px-2 py-0.5 rounded-full shrink-0 ml-2 ${
                            p.is_premium ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'
                          }`}>
                            {p.is_premium ? 'Premium' : 'Gratis'}
                          </span>
                        </div>
                        {p.deskripsi && <p className="text-xs text-gray-400 mb-3">{p.deskripsi}</p>}
                        {p.is_premium ? (
                          <button onClick={() => setActiveTab('paket')}
                            className="w-full bg-yellow-400 hover:bg-yellow-300 text-black text-sm font-bold py-2 rounded-lg transition">
                            Upgrade untuk Akses
                          </button>
                        ) : (
                          <a href={`/pendalaman/${p.id}`}
                            className="block w-full bg-forest-600 hover:bg-forest-700 text-white text-sm font-bold py-2 rounded-lg transition text-center">
                            Mulai Latihan →
                          </a>
                        )}
                      </div>
                    ))}
                    {paketPendalaman.filter(p => p.topik_id === selectedTopik.id).length === 0 && (
                      <div className="col-span-3 bg-white border border-gray-200 rounded-xl px-5 py-12 text-center text-gray-400 text-sm">
                        Belum ada paket latihan untuk topik ini.
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* ── VIDEO PEMBELAJARAN ────────────────────────────────── */}
          {activeTab === 'video' && (
            <div>
              <div className="mb-6">
                <h2 className="text-xl font-black text-gray-800">Video Pembelajaran</h2>
                <p className="text-gray-500 text-sm">{videoList.length} video tersedia</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {videoList.map((v, i) => (
                  <div key={i} className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-sm transition">
                    <a href={`https://youtube.com/watch?v=${v.youtube_id}`} target="_blank" rel="noreferrer">
                      <img
                        src={`https://img.youtube.com/vi/${v.youtube_id}/mqdefault.jpg`}
                        alt={v.judul}
                        className="w-full h-40 object-cover"
                      />
                    </a>
                    <div className="p-4">
                      <div className="font-bold text-sm text-gray-800 mb-1">{v.judul}</div>
                      <div className="text-xs text-gray-400 mb-3">{v.topik_materi?.nama || '—'}</div>
                      <div className="flex items-center justify-between">
                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                          v.is_premium ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'
                        }`}>
                          {v.is_premium ? 'Premium' : 'Gratis'}
                        </span>
                        {v.is_premium ? (
                          <button onClick={() => setActiveTab('paket')}
                            className="text-xs text-yellow-600 font-bold hover:underline">Upgrade →</button>
                        ) : (
                          <a href={`https://youtube.com/watch?v=${v.youtube_id}`} target="_blank" rel="noreferrer"
                            className="text-xs text-forest-600 font-bold hover:underline">Tonton →</a>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                {videoList.length === 0 && (
                  <div className="col-span-3 bg-white border border-gray-200 rounded-xl px-5 py-12 text-center text-gray-400 text-sm">
                    Belum ada video tersedia.
                  </div>
                )}
              </div>
            </div>
          )}

          {/* ── MODUL / PDF ───────────────────────────────────────── */}
          {activeTab === 'modul' && (
            <div>
              <div className="mb-6">
                <h2 className="text-xl font-black text-gray-800">Modul / PDF</h2>
                <p className="text-gray-500 text-sm">{modulList.length} modul tersedia</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {modulList.map((m, i) => (
                  <div key={i} className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-sm transition">
                    <div className="text-3xl mb-3">📄</div>
                    <div className="font-bold text-sm text-gray-800 mb-1">{m.judul}</div>
                    <div className="text-xs text-gray-400 mb-1">{m.topik_materi?.nama || '—'}</div>
                    {m.deskripsi && <p className="text-xs text-gray-400 mb-3">{m.deskripsi}</p>}
                    <div className="flex items-center justify-between mt-3">
                      <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                        m.is_premium ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'
                      }`}>
                        {m.is_premium ? 'Premium' : 'Gratis'}
                      </span>
                      {m.is_premium ? (
                        <button onClick={() => setActiveTab('paket')}
                          className="text-xs text-yellow-600 font-bold hover:underline">Upgrade →</button>
                      ) : (
                        <a href={m.file_url} target="_blank" rel="noreferrer"
                          className="text-xs text-forest-600 font-bold hover:underline">Unduh →</a>
                      )}
                    </div>
                  </div>
                ))}
                {modulList.length === 0 && (
                  <div className="col-span-3 bg-white border border-gray-200 rounded-xl px-5 py-12 text-center text-gray-400 text-sm">
                    Belum ada modul tersedia.
                  </div>
                )}
              </div>
            </div>
          )}

          {/* ── PENGUMUMAN ────────────────────────────────────────── */}
          {activeTab === 'pengumuman' && (
            <div>
              <div className="mb-6">
                <h2 className="text-xl font-black text-gray-800">Pengumuman</h2>
                <p className="text-gray-500 text-sm">Informasi terbaru dari OSNGeo.id</p>
              </div>
              <div className="flex flex-col gap-4">
                {pengumumanList.map((p, i) => (
                  <div key={i} className="bg-white border border-gray-200 rounded-xl px-5 py-4">
                    <div className="font-bold text-gray-800 mb-1">{p.judul}</div>
                    <div className="text-gray-600 text-sm mb-2">{p.isi}</div>
                    <div className="text-xs text-gray-400">
                      {new Date(p.created_at).toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })}
                    </div>
                  </div>
                ))}
                {pengumumanList.length === 0 && (
                  <div className="bg-white border border-gray-200 rounded-xl px-5 py-12 text-center text-gray-400 text-sm">
                    Belum ada pengumuman.
                  </div>
                )}
              </div>
            </div>
          )}

          {/* ── PAKET & UPGRADE ───────────────────────────────────── */}
          {activeTab === 'paket' && (
            <div>
              <div className="mb-6">
                <h2 className="text-xl font-black text-gray-800">Paket & Upgrade</h2>
                <p className="text-gray-500 text-sm">Pilih paket untuk akses konten premium</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                {membershipList.map((m, i) => (
                  <div key={i} className="bg-white border border-gray-200 rounded-xl p-6 hover:border-forest-300 hover:shadow-sm transition">
                    <div className="font-black text-gray-800 text-lg mb-1">{m.nama}</div>
                    <div className="text-3xl font-black text-forest-600 mb-1">
                      Rp {m.harga?.toLocaleString('id-ID')}
                    </div>
                    <div className="text-xs text-gray-400 mb-4">{m.durasi_hari} hari · {m.deskripsi}</div>
                    {m.fitur && (
                      <div className="mb-4 flex flex-col gap-1">
                        {String(m.fitur).split('\n').filter(Boolean).map((f: string, fi: number) => (
                          <div key={fi} className="flex items-start gap-2 text-sm text-gray-600">
                            <span className="text-green-500 mt-0.5 shrink-0">✓</span>
                            <span>{f}</span>
                          </div>
                        ))}
                      </div>
                    )}
                    <a href={`https://wa.me/6285157220761?text=Halo,%20saya%20ingin%20berlangganan%20${encodeURIComponent(m.nama)}%20di%20OSNGeo.id`}
                      target="_blank" rel="noreferrer"
                      className="block w-full bg-forest-600 hover:bg-forest-700 text-white text-sm font-bold py-2.5 rounded-lg transition text-center">
                      Hubungi Admin →
                    </a>
                  </div>
                ))}
                {membershipList.length === 0 && (
                  <div className="col-span-3 bg-white border border-gray-200 rounded-xl px-5 py-12 text-center text-gray-400 text-sm">
                    Belum ada paket tersedia.
                  </div>
                )}
              </div>
            </div>
          )}

      </main>
    </>
  )
}
