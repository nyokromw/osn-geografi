'use client'
import { useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'

type Tab = 'dashboard' | 'tryout' | 'pendalaman' | 'video' | 'modul' | 'pengumuman' | 'paket'

const MAX_POIN = 400

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null)
  const [profile, setProfile] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<Tab>('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(true)

  // Stats
  const [stats, setStats] = useState({ totalTO: 0, rataRata: 0, tertinggi: 0, terendah: 0 })
  const [riwayat, setRiwayat] = useState<any[]>([])

  // Data
  const [paketTO, setPaketTO] = useState<any[]>([])
  const [topikList, setTopikList] = useState<any[]>([])
  const [paketPendalaman, setPaketPendalaman] = useState<any[]>([])
  const [videoList, setVideoList] = useState<any[]>([])
  const [modulList, setModulList] = useState<any[]>([])
  const [pengumumanList, setPengumumanList] = useState<any[]>([])
  const [membershipList, setMembershipList] = useState<any[]>([])

  // Drill-down
  const [selectedTopik, setSelectedTopik] = useState<any>(null)

  useEffect(() => {
    const init = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) { window.location.href = '/login'; return }
      setUser(user)

      const { data: prof } = await supabase.from('profiles').select('*').eq('id', user.id).single()
      setProfile(prof)

      const { data: hasil } = await supabase
        .from('hasil_to')
        .select('*, paket_to(nama)')
        .eq('user_id', user.id)
        .order('created_at', { ascending: true })

      if (hasil && hasil.length > 0) {
        const poinList = hasil.map((h: any) => h.total_poin)
        setStats({
          totalTO: hasil.length,
          rataRata: Math.round(poinList.reduce((a: number, b: number) => a + b, 0) / hasil.length),
          tertinggi: Math.max(...poinList),
          terendah: Math.min(...poinList),
        })
        setRiwayat(hasil)
      }

      const [
        { data: pt }, { data: tp }, { data: pp },
        { data: v }, { data: m }, { data: pg }, { data: mb }
      ] = await Promise.all([
        supabase.from('paket_to').select('*').eq('status', 'aktif').order('urutan'),
        supabase.from('topik_materi').select('*').order('urutan'),
        supabase.from('paket_pendalaman').select('*, topik_materi(nama)').eq('status', 'aktif').order('id'),
        supabase.from('video_pembelajaran').select('*, topik_materi(nama)').order('urutan'),
        supabase.from('modul_materi').select('*, topik_materi(nama)').order('id'),
        supabase.from('pengumuman').select('*').eq('aktif', true).order('created_at', { ascending: false }),
        supabase.from('paket_membership').select('*').order('id'),
      ])

      setPaketTO(pt || [])
      setTopikList(tp || [])
      setPaketPendalaman(pp || [])
      setVideoList(v || [])
      setModulList(m || [])
      setPengumumanList(pg || [])
      setMembershipList(mb || [])

      setLoading(false)
    }
    init()
  }, [])

  if (loading) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <p className="text-gray-400 animate-pulse">Memuat dashboard...</p>
    </div>
  )

  const level =
    stats.rataRata >= 300 ? { label: '🏆 Luar Biasa', color: 'text-green-600', bg: 'bg-green-50', border: 'border-green-200' }
    : stats.rataRata >= 200 ? { label: '⭐ Baik', color: 'text-blue-600', bg: 'bg-blue-50', border: 'border-blue-200' }
    : stats.rataRata >= 100 ? { label: '📈 Berkembang', color: 'text-yellow-600', bg: 'bg-yellow-50', border: 'border-yellow-200' }
    : { label: '📚 Perlu Latihan', color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200' }
    
  const navTo = (tab: Tab) => { setActiveTab(tab); setSelectedTopik(null) }

  const menus = [
    {
      group: 'Utama', items: [
        { label: 'Dashboard', key: 'dashboard', icon: '⊞' },
        { label: 'Pengumuman', key: 'pengumuman', icon: '📢' },
      ]
    },
    {
      group: 'Ujian', items: [
        { label: 'Tryout', key: 'tryout', icon: '📝' },
        { label: 'Pendalaman Materi', key: 'pendalaman', icon: '🧩' },
      ]
    },
    {
      group: 'Materi', items: [
        { label: 'Modul / PDF', key: 'modul', icon: '📄' },
        { label: 'Video Pembelajaran', key: 'video', icon: '▶️' },
      ]
    },
    {
      group: 'Lainnya', items: [
        { label: 'Paket & Upgrade', key: 'paket', icon: '💎' },
      ]
    },
  ]

  const nama = user?.user_metadata?.nama || profile?.nama || 'Siswa'
  const inisial = nama.charAt(0).toUpperCase()

  return (
    <div className="min-h-screen flex" style={{ colorScheme: 'light', background: '#f9fafb' }}>

      {/* SIDEBAR */}
      <aside style={{ width: sidebarOpen ? '256px' : '0' }}
        className="transition-all duration-300 bg-white border-r border-gray-200 flex flex-col shrink-0 fixed h-full z-30 overflow-hidden">

        {/* LOGO */}
        <div className="px-5 py-4 border-b border-gray-100 shrink-0">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-black text-white text-sm">G</div>
            <span className="font-black text-gray-800">OSN<span className="text-blue-600">Geo</span>.id</span>
          </div>
        </div>

        {/* USER INFO */}
        <div className="px-5 py-4 border-b border-gray-100 shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-black text-sm">
              {inisial}
            </div>
            <div className="overflow-hidden">
              <div className="font-bold text-sm text-gray-800 leading-tight truncate">
                {nama.split(' ').slice(0, 2).join(' ')}
              </div>
              <div className="text-xs text-gray-400 truncate">{user?.email}</div>
            </div>
          </div>
          {profile?.role === 'admin' && (
            <a href="/admin"
              className="mt-3 flex items-center justify-center w-full bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 text-xs font-bold py-1.5 rounded-lg transition">
              Panel Admin
            </a>
          )}
        </div>

        {/* MENU */}
        <nav className="flex-1 overflow-y-auto py-3 px-3">
          {menus.map((g, gi) => (
            <div key={gi} className="mb-4">
              <div className="text-xs font-bold text-gray-400 uppercase tracking-widest px-2 mb-1">{g.group}</div>
              {g.items.map((m) => (
                <button key={m.key} onClick={() => navTo(m.key as Tab)}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition mb-0.5 w-full text-left ${
                    activeTab === m.key ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'
                  }`}>
                  <span>{m.icon}</span>
                  <span className="whitespace-nowrap">{m.label}</span>
                </button>
              ))}
            </div>
          ))}
        </nav>

        {/* LOGOUT */}
        <div className="px-3 py-3 border-t border-gray-100 shrink-0">
          <button onClick={async () => { await supabase.auth.signOut(); window.location.href = '/login' }}
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-red-500 hover:bg-red-50 w-full transition">
            <span>🚪</span><span>Log Out</span>
          </button>
        </div>
      </aside>

      {/* MAIN */}
      <div className="flex-1 flex flex-col transition-all duration-300" style={{ marginLeft: sidebarOpen ? '256px' : '0' }}>

        {/* TOPBAR */}
        <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between sticky top-0 z-20">
          <div className="flex items-center gap-3">
            <button onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-gray-500 hover:text-gray-800 p-1.5 rounded-lg hover:bg-gray-100 transition">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <h1 className="font-black text-gray-800 text-sm capitalize">{activeTab === 'dashboard' ? 'Dashboard' : menus.flatMap(g => g.items).find(m => m.key === activeTab)?.label}</h1>
          </div>
          <div className="flex items-center gap-3">
            <a href="https://wa.me/6285157220761" target="_blank"
              className="bg-green-500 hover:bg-green-600 text-white text-xs font-bold px-3 py-1.5 rounded-lg transition">
              WA Support
            </a>
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-black text-sm">
              {inisial}
            </div>
          </div>
        </header>

        {/* KONTEN */}
        <main className="flex-1 p-6">
{/* ── DASHBOARD UTAMA ───────────────────────────────────── */}
          {activeTab === 'dashboard' && (
            <div>
              <div className="mb-6">
                <h1 className="text-2xl font-black text-gray-800">Dashboard</h1>
                <p className="text-gray-500 text-sm mt-0.5">
                  Selamat datang, {nama.split(' ')[0]}! Semangat belajar OSN Geografi.
                </p>
              </div>

              {/* STAT CARDS */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                {[
                  { label: 'TO Dikerjakan', value: stats.totalTO, color: 'bg-blue-600', icon: '📝' },
                  { label: 'Skor Tertinggi', value: stats.totalTO > 0 ? stats.tertinggi : '—', color: 'bg-green-500', icon: '🏆' },
                  { label: 'Rata-rata Poin', value: stats.totalTO > 0 ? stats.rataRata : '—', color: 'bg-yellow-500', icon: '📊' },
                  { label: 'Skor Terendah', value: stats.totalTO > 0 ? stats.terendah : '—', color: 'bg-red-400', icon: '📉' },
                ].map((s, i) => (
                  <div key={i} className={`${s.color} text-white rounded-xl p-4 flex items-center justify-between`}>
                    <div>
                      <div className="text-xs font-semibold opacity-80">{s.label}</div>
                      <div className="text-3xl font-black mt-1">{s.value}</div>
                    </div>
                    <div className="text-3xl opacity-20">{s.icon}</div>
                  </div>
                ))}
              </div>

              {/* LEVEL + AKSES CEPAT */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">

                {/* LEVEL PERFORMA */}
                <div className={`rounded-xl border p-5 ${stats.totalTO > 0 ? `${level.bg} ${level.border}` : 'bg-gray-50 border-gray-200'}`}>
                  <div className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3">Level Performa</div>
                  {stats.totalTO > 0 ? (
                    <div>
                      <div className={`text-4xl font-black ${level.color}`}>{level.label}</div>
                      <div className="text-gray-500 text-sm mt-1">
                        Rata-rata {stats.rataRata} poin dari {MAX_POIN} maksimal
                      </div>
                      <div className="mt-3 h-2 bg-white/60 rounded-full overflow-hidden">
                        <div className="h-full rounded-full transition-all"
                          style={{
                            width: `${Math.min(Math.max((stats.rataRata + 100) / 500 * 100, 0), 100)}%`,
                            background: stats.rataRata >= 240 ? '#22c55e' : stats.rataRata >= 120 ? '#eab308' : stats.rataRata >= 0 ? '#3b82f6' : '#ef4444'
                          }} />
                      </div>
                    </div>
                  ) : (
                    <p className="text-gray-400 text-sm">Kerjakan tryout pertama untuk melihat level performa kamu.</p>
                  )}
                </div>

                {/* AKSES CEPAT */}
                <div className="bg-white border border-gray-200 rounded-xl p-5">
                  <div className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3">Akses Cepat</div>
                  <div className="flex flex-col gap-2">
                    <button onClick={() => setActiveTab('tryout')}
                      className="flex items-center justify-between bg-blue-50 hover:bg-blue-100 border border-blue-200 px-4 py-3 rounded-lg transition">
                      <div className="flex items-center gap-3">
                        <span className="text-xl">📝</span>
                        <div className="text-left">
                          <div className="text-sm font-bold text-blue-700">Tryout</div>
                          <div className="text-xs text-blue-500">{paketTO.length} paket tersedia</div>
                        </div>
                      </div>
                      <span className="text-blue-400 text-sm">→</span>
                    </button>
                    <button onClick={() => setActiveTab('pendalaman')}
                      className="flex items-center justify-between bg-purple-50 hover:bg-purple-100 border border-purple-200 px-4 py-3 rounded-lg transition">
                      <div className="flex items-center gap-3">
                        <span className="text-xl">🧩</span>
                        <div className="text-left">
                          <div className="text-sm font-bold text-purple-700">Pendalaman Materi</div>
                          <div className="text-xs text-purple-500">{topikList.length} topik OSN Geografi</div>
                        </div>
                      </div>
                      <span className="text-purple-400 text-sm">→</span>
                    </button>
                    <button onClick={() => setActiveTab('video')}
                      className="flex items-center justify-between bg-green-50 hover:bg-green-100 border border-green-200 px-4 py-3 rounded-lg transition">
                      <div className="flex items-center gap-3">
                        <span className="text-xl">▶️</span>
                        <div className="text-left">
                          <div className="text-sm font-bold text-green-700">Video Pembelajaran</div>
                          <div className="text-xs text-green-500">{videoList.length} video tersedia</div>
                        </div>
                      </div>
                      <span className="text-green-400 text-sm">→</span>
                    </button>
                  </div>
                </div>
              </div>

              {/* RIWAYAT TO */}
              <div className="bg-white border border-gray-200 rounded-xl mb-6">
                <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
                  <h2 className="font-bold text-gray-800">Riwayat Tryout</h2>
                  <span className="text-xs text-gray-400">{riwayat.length} sesi</span>
                </div>
                {riwayat.length > 0 ? (
                  <div className="divide-y divide-gray-50">
                    {riwayat.slice().reverse().map((h, i) => (
                      <div key={i} className="px-5 py-3.5 flex items-center justify-between hover:bg-gray-50 transition">
                        <div>
                          <div className="font-semibold text-sm text-gray-800">{h.paket_to?.nama || 'Tryout'}</div>
                          <div className="text-xs text-gray-400 mt-0.5 flex flex-wrap gap-2">
                            <span className="text-green-600">✓ {h.poin_benar} benar</span>
                            <span className="text-red-500">✗ {h.poin_salah} salah</span>
                            <span className="text-gray-400">— {h.poin_kosong} kosong</span>
                            <span>{new Date(h.created_at).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
                          </div>
                        </div>
                        <div className={`text-2xl font-black ml-4 ${h.total_poin >= 0 ? 'text-blue-600' : 'text-red-500'}`}>
                          {h.total_poin}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="px-5 py-8 text-center text-gray-400 text-sm">
                    Belum ada riwayat tryout. Mulai dari menu Tryout di sidebar!
                  </div>
                )}
              </div>

              {/* BANNER UPGRADE */}
              <div className="bg-blue-600 text-white rounded-xl p-6 flex flex-col md:flex-row items-center justify-between gap-4">
                <div>
                  <div className="font-black text-lg mb-1">Upgrade ke Paket Lengkap</div>
                  <p className="text-blue-200 text-sm">Akses 60 paket TO + kursus intensif bersama pembina OSN.</p>
                </div>
                <button onClick={() => setActiveTab('paket')}
                  className="bg-yellow-400 hover:bg-yellow-300 text-black px-6 py-2.5 rounded-lg font-black text-sm transition whitespace-nowrap shrink-0">
                  Lihat Paket →
                </button>
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
                        <div key={p.id} className="bg-white border border-gray-200 rounded-xl p-5 hover:border-blue-300 hover:shadow-sm transition">
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
                              className="block w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold py-2 rounded-lg transition text-center">
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
                      className="text-blue-600 hover:underline font-medium">Pendalaman Materi</button>
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
                            className="block w-full bg-purple-600 hover:bg-purple-700 text-white text-sm font-bold py-2 rounded-lg transition text-center">
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
                            className="text-xs text-blue-600 font-bold hover:underline">Tonton →</a>
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
                          className="text-xs text-blue-600 font-bold hover:underline">Unduh →</a>
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
                  <div key={i} className="bg-white border border-gray-200 rounded-xl p-6 hover:border-blue-300 hover:shadow-sm transition">
                    <div className="font-black text-gray-800 text-lg mb-1">{m.nama}</div>
                    <div className="text-3xl font-black text-blue-600 mb-1">
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
                      className="block w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold py-2.5 rounded-lg transition text-center">
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

        <footer className="text-center text-xs text-gray-400 py-4 border-t border-gray-100">
          © 2025 OSNGeo.id
        </footer>
      </div>
    </div>
  )
}