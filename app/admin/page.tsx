'use client'
import { useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'

type View =
  | 'dashboard' | 'siswa'
  | 'paket_tryout' | 'soal_tryout'
  | 'pendalaman' | 'soal_pendalaman'
  | 'video' | 'modul'
  | 'membership' | 'transaksi'
  | 'pengumuman' | 'banner'

export default function AdminPage() {
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState<View>('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(true)

  // Stats
  const [stats, setStats] = useState({ totalSiswa: 0, totalTO: 0, rataRata: 0, totalTransaksi: 0 })

  // Data lists
  const [siswa, setSiswa] = useState<any[]>([])
  const [hasil, setHasil] = useState<any[]>([])
  const [paketTO, setPaketTO] = useState<any[]>([])
  const [soalTO, setSoalTO] = useState<any[]>([])
  const [topikList, setTopikList] = useState<any[]>([])
  const [paketPendalaman, setPaketPendalaman] = useState<any[]>([])
  const [soalPendalaman, setSoalPendalaman] = useState<any[]>([])
  const [videoList, setVideoList] = useState<any[]>([])
  const [modulList, setModulList] = useState<any[]>([])
  const [membershipList, setMembershipList] = useState<any[]>([])
  const [transaksiList, setTransaksiList] = useState<any[]>([])
  const [pengumumanList, setPengumumanList] = useState<any[]>([])
  const [bannerList, setBannerList] = useState<any[]>([])

  // Drill-down state
  const [selectedPaket, setSelectedPaket] = useState<any>(null)
  const [selectedTopik, setSelectedTopik] = useState<any>(null)
  const [selectedPaketPendalaman, setSelectedPaketPendalaman] = useState<any>(null)

  // Form state
const [showForm, setShowForm] = useState(false)
const [editData, setEditData] = useState<any>(null)
const [formData, setFormData] = useState<any>({})
const [showEditSoal, setShowEditSoal] = useState(false)
const [editSoalData, setEditSoalData] = useState<any>(null)
const [editSoalForm, setEditSoalForm] = useState<any>({})
const [showEditUser, setShowEditUser] = useState(false)
const [editUserData, setEditUserData] = useState<any>(null)
const [editUserForm, setEditUserForm] = useState<any>({})

  useEffect(() => {
    const init = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) { window.location.href = '/login'; return }
      const { data: profile } = await supabase.from('profiles').select('role').eq('id', user.id).single()
      if (profile?.role !== 'admin') { window.location.href = '/dashboard'; return }
      await loadAll()
      setLoading(false)
    }
    init()
  }, [])

  const loadAll = async () => {
    const [
      { data: s }, { data: h }, { data: pt }, { data: tp },
      { data: pp }, { data: v }, { data: m }, { data: mb },
      { data: tr }, { data: pg }, { data: bn }
    ] = await Promise.all([
      supabase.from('profiles').select('*').order('created_at', { ascending: false }),
      supabase.from('hasil_to').select('*, profiles(nama), paket_to(nama)').order('created_at', { ascending: false }).limit(50),
      supabase.from('paket_to').select('*').order('urutan'),
      supabase.from('topik_materi').select('*').order('urutan'),
      supabase.from('paket_pendalaman').select('*, topik_materi(nama)').order('id'),
      supabase.from('video_pembelajaran').select('*, topik_materi(nama)').order('urutan'),
      supabase.from('modul_materi').select('*, topik_materi(nama)').order('id'),
      supabase.from('paket_membership').select('*').order('id'),
      supabase.from('transaksi').select('*, profiles(nama), paket_membership(nama)').order('created_at', { ascending: false }),
      supabase.from('pengumuman').select('*').order('created_at', { ascending: false }),
      supabase.from('banner').select('*').order('id'),
    ])
    setSiswa(s || [])
    setHasil(h || [])
    setPaketTO(pt || [])
    setTopikList(tp || [])
    setPaketPendalaman(pp || [])
    setVideoList(v || [])
    setModulList(m || [])
    setMembershipList(mb || [])
    setTransaksiList(tr || [])
    setPengumumanList(pg || [])
    setBannerList(bn || [])
    const totalTO = h?.length || 0
    const rataRata = totalTO > 0 ? Math.round((h || []).reduce((a: number, b: any) => a + b.total_poin, 0) / totalTO) : 0
    setStats({ totalSiswa: s?.length || 0, totalTO, rataRata, totalTransaksi: tr?.length || 0 })
  }

  const loadSoalTO = async (paketId: number) => {
    const { data } = await supabase.from('soal').select('*').eq('paket_id', paketId).order('id')
    setSoalTO(data || [])
  }

  const loadSoalPendalaman = async (paketId: number) => {
    const { data } = await supabase.from('soal_pendalaman').select('*').eq('paket_id', paketId).order('id')
    setSoalPendalaman(data || [])
  }

const handleDelete = async (table: string, id: number, extra?: () => void) => {
  if (!confirm('Yakin hapus?')) return
  const { error, data } = await supabase.from(table).delete().eq('id', id)
  console.log('delete result:', { error, data })
  await loadAll()
  if (extra) extra()
}

  const handleSave = async (table: string, data: any) => {
    if (editData) {
      await supabase.from(table).update(data).eq('id', editData.id)
    } else {
      await supabase.from(table).insert(data)
    }
    await loadAll()
    setShowForm(false)
    setEditData(null)
    setFormData({})
  }

  const resetForm = () => { setShowForm(false); setEditData(null); setFormData({}) }

  const handleSaveSoal = async () => {
  await supabase.from('soal').update({
    pertanyaan: editSoalForm.pertanyaan,
    gambar_url: editSoalForm.gambar_url || null,
    pilihan_a: editSoalForm.pilihan_a,
    pilihan_b: editSoalForm.pilihan_b,
    pilihan_c: editSoalForm.pilihan_c,
    pilihan_d: editSoalForm.pilihan_d,
    pilihan_e: editSoalForm.pilihan_e,
    jawaban_benar: editSoalForm.jawaban_benar,
    pembahasan: editSoalForm.pembahasan,
    is_premium: editSoalForm.is_premium === 'true',
  }).eq('id', editSoalData.id)
  await loadSoalTO(selectedPaket.id)
  setShowEditSoal(false)
  setEditSoalData(null)
  setEditSoalForm({})
}
const handleSaveSoalPendalaman = async () => {
  await supabase.from('soal_pendalaman').update({
    pertanyaan: editSoalForm.pertanyaan,
    gambar_url: editSoalForm.gambar_url || null,
    pilihan_a: editSoalForm.pilihan_a,
    pilihan_b: editSoalForm.pilihan_b,
    pilihan_c: editSoalForm.pilihan_c,
    pilihan_d: editSoalForm.pilihan_d,
    pilihan_e: editSoalForm.pilihan_e,
    jawaban_benar: editSoalForm.jawaban_benar,
    pembahasan: editSoalForm.pembahasan,
  }).eq('id', editSoalData.id)
  await loadSoalPendalaman(selectedPaketPendalaman.id)
  setShowEditSoal(false)
  setEditSoalData(null)
  setEditSoalForm({})
}
const handleSaveUser = async () => {
  const updateData: any = {
    nama: editUserForm.nama,
    role: editUserForm.role,
    status: editUserForm.status,
    status_expired: editUserForm.status === 'gratis' ? null
      : new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString(),
  }
  await supabase.from('profiles').update(updateData).eq('id', editUserData.id)
  await loadAll()
  setShowEditUser(false)
  setEditUserData(null)
  setEditUserForm({})
}

const handleResetPassword = async (email: string) => {
  const { error } = await supabase.auth.resetPasswordForEmail(email, {
    redirectTo: `${window.location.origin}/reset-password`,
  })
  if (error) alert('Gagal kirim email reset.')
  else alert(`Email reset password sudah dikirim ke ${email}`)
}

  const openAdd = () => { setEditData(null); setFormData({}); setShowForm(true) }

  const navTo = (v: View) => { setView(v); resetForm(); setSelectedPaket(null); setSelectedTopik(null); setSelectedPaketPendalaman(null) }

  if (loading) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <p className="text-gray-400 animate-pulse">Memuat panel admin...</p>
    </div>
  )

  const menuGroups = [
    {
      group: 'Manajemen', items: [
        { label: 'Dashboard', key: 'dashboard', icon: '⊞' },
        { label: 'Data Siswa', key: 'siswa', icon: '👥' },
      ]
    },
    {
      group: 'Tryout', items: [
        { label: 'Paket Tryout', key: 'paket_tryout', icon: '📋' },
        { label: 'Pendalaman Materi', key: 'pendalaman', icon: '🧩' },
      ]
    },
    {
      group: 'Materi', items: [
        { label: 'Video Pembelajaran', key: 'video', icon: '▶️' },
        { label: 'Modul / PDF', key: 'modul', icon: '📄' },
      ]
    },
    {
      group: 'Transaksi', items: [
        { label: 'Paket Membership', key: 'membership', icon: '💎' },
        { label: 'Daftar Transaksi', key: 'transaksi', icon: '🧾' },
      ]
    },
    {
      group: 'Lainnya', items: [
        { label: 'Pengumuman', key: 'pengumuman', icon: '📢' },
        { label: 'Banner', key: 'banner', icon: '🖼️' },
      ]
    },
  ]

  const activeKey = ['soal_tryout'].includes(view) ? 'paket_tryout'
    : ['soal_pendalaman'].includes(view) ? 'pendalaman'
    : view

  // Input field helpers
  const inp = (placeholder: string, key: string, type = 'text') => (
    <input type={type} placeholder={placeholder} value={formData[key] || ''}
      onChange={e => setFormData({ ...formData, [key]: type === 'number' ? Number(e.target.value) : e.target.value })}
      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400" />
  )
  const ta = (placeholder: string, key: string, rows = 3) => (
    <textarea placeholder={placeholder} rows={rows} value={formData[key] || ''}
      onChange={e => setFormData({ ...formData, [key]: e.target.value })}
      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400" />
  )
  const sel = (key: string, opts: { value: any, label: string }[], placeholder = 'Pilih...') => (
    <select value={formData[key] ?? ''} onChange={e => setFormData({ ...formData, [key]: e.target.value })}
      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400">
      <option value="">{placeholder}</option>
      {opts.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
    </select>
  )

  const FormBtns = ({ onSave }: { onSave: () => void }) => (
    <div className="flex gap-3 pt-2">
      <button onClick={onSave} className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg text-sm font-semibold transition">Simpan</button>
      <button onClick={resetForm} className="border border-gray-200 text-gray-600 px-4 py-2 rounded-lg text-sm transition">Batal</button>
    </div>
  )

  const Th = ({ children }: { children: any }) => (
    <th className="text-left px-5 py-3 text-gray-500 font-bold text-xs uppercase">{children}</th>
  )
  const ThC = ({ children }: { children: any }) => (
    <th className="text-center px-5 py-3 text-gray-500 font-bold text-xs uppercase">{children}</th>
  )

  const Badge = ({ v, map }: { v: string, map: Record<string, string> }) => {
    const cls = map[v] || 'bg-gray-100 text-gray-600'
    return <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${cls}`}>{v}</span>
  }

  return (
    <div className="min-h-screen flex" style={{ colorScheme: 'light', background: '#f9fafb' }}>

      {/* SIDEBAR */}
      <aside style={{ width: sidebarOpen ? '240px' : '0' }}
        className="transition-all duration-300 bg-white border-r border-gray-200 flex flex-col shrink-0 fixed h-full z-30 overflow-hidden">
        <div className="px-4 py-4 border-b border-gray-100 shrink-0">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-red-600 rounded-lg flex items-center justify-center font-black text-white text-xs">A</div>
            <div>
              <div className="font-black text-gray-800 text-sm">OSN<span className="text-blue-600">Geo</span>.id</div>
              <div className="text-xs text-red-500 font-bold">Super Admin</div>
            </div>
          </div>
        </div>
        <nav className="flex-1 overflow-y-auto py-3 px-2">
          {menuGroups.map((g, gi) => (
            <div key={gi} className="mb-3">
              <div className="text-xs font-bold text-gray-400 uppercase tracking-widest px-2 mb-1">{g.group}</div>
              {g.items.map((m) => (
                <button key={m.key} onClick={() => navTo(m.key as View)}
                  className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition mb-0.5 w-full text-left ${
                    activeKey === m.key ? 'bg-red-600 text-white' : 'text-gray-600 hover:bg-gray-100'
                  }`}>
                  <span>{m.icon}</span><span className="whitespace-nowrap">{m.label}</span>
                </button>
              ))}
            </div>
          ))}
          <div className="mt-2 border-t border-gray-100 pt-3">
            <a href="/dashboard" className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 transition">
              <span>👤</span><span>Dashboard Siswa</span>
            </a>
          </div>
        </nav>
        <div className="px-2 py-3 border-t border-gray-100 shrink-0">
          <button onClick={async () => { await supabase.auth.signOut(); window.location.href = '/login' }}
            className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium text-red-500 hover:bg-red-50 w-full transition">
            <span>🚪</span><span>Log Out</span>
          </button>
        </div>
      </aside>

      {/* MAIN */}
      <div className="flex-1 flex flex-col" style={{ marginLeft: sidebarOpen ? '240px' : '0' }}>
        <header className="bg-white border-b border-gray-200 px-5 py-3 flex items-center justify-between sticky top-0 z-20">
          <div className="flex items-center gap-3">
            <button onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-gray-500 hover:text-gray-800 p-1.5 rounded-lg hover:bg-gray-100 transition">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <h1 className="font-black text-gray-800 text-sm">Panel Admin</h1>
          </div>
          <span className="text-xs bg-red-100 text-red-600 border border-red-200 font-bold px-2 py-1 rounded-full">Super Admin</span>
        </header>

        <main className="flex-1 p-5">
          {/* ── DASHBOARD ─────────────────────────────────────────── */}
          {view === 'dashboard' && (
            <div>
              <div className="mb-5">
                <h2 className="text-xl font-black text-gray-800">Dashboard Admin</h2>
                <p className="text-gray-500 text-sm">Ringkasan aktivitas OSNGeo.id</p>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                {[
                  { label: 'Total Siswa', value: stats.totalSiswa, color: 'bg-blue-600', icon: '👥' },
                  { label: 'TO Dikerjakan', value: stats.totalTO, color: 'bg-green-500', icon: '📝' },
                  { label: 'Rata-rata Poin', value: stats.rataRata, color: 'bg-yellow-500', icon: '📊' },
                  { label: 'Total Transaksi', value: stats.totalTransaksi, color: 'bg-purple-500', icon: '🧾' },
                ].map((s, i) => (
                  <div key={i} className={`${s.color} text-white rounded-xl p-4 flex items-center justify-between`}>
                    <div>
                      <div className="text-xs opacity-80">{s.label}</div>
                      <div className="text-3xl font-black mt-1">{s.value}</div>
                    </div>
                    <div className="text-3xl opacity-20">{s.icon}</div>
                  </div>
                ))}
              </div>
              <div className="bg-white border border-gray-200 rounded-xl">
                <div className="px-5 py-3 border-b border-gray-100">
                  <h3 className="font-bold text-gray-800 text-sm">Hasil TO Terbaru</h3>
                </div>
                <div className="divide-y divide-gray-50">
                  {hasil.slice(0, 10).map((h, i) => (
                    <div key={i} className="px-5 py-3 flex items-center justify-between hover:bg-gray-50">
                      <div>
                        <div className="font-semibold text-sm text-gray-800">{h.profiles?.nama || '—'}</div>
                        <div className="text-xs text-gray-400 flex gap-2 mt-0.5">
                          <span>{h.paket_to?.nama || 'Tryout'}</span>
                          <span className="text-green-600">✓{h.poin_benar}</span>
                          <span className="text-red-500">✗{h.poin_salah}</span>
                          <span>{new Date(h.created_at).toLocaleDateString('id-ID', { day: 'numeric', month: 'short' })}</span>
                        </div>
                      </div>
                      <div className={`text-xl font-black ${h.total_poin >= 0 ? 'text-blue-600' : 'text-red-500'}`}>{h.total_poin}</div>
                    </div>
                  ))}
                  {hasil.length === 0 && <div className="px-5 py-8 text-center text-gray-400 text-sm">Belum ada data.</div>}
                </div>
              </div>
            </div>
          )}

         {/* ── DATA SISWA ────────────────────────────────────────── */}
          {view === 'siswa' && (
            <div>
              <div className="mb-5">
                <h2 className="text-xl font-black text-gray-800">Data Siswa</h2>
                <p className="text-gray-500 text-sm">{siswa.length} akun terdaftar</p>
              </div>
              <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 bg-gray-50">
                      <Th>No</Th><Th>Nama</Th><Th>Role</Th><Th>Status</Th><Th>Expired</Th><Th>Bergabung</Th><ThC>Aksi</ThC>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {siswa.map((s, i) => (
                      <tr key={i} className="hover:bg-gray-50">
                        <td className="px-5 py-3 text-gray-400 text-xs">{i + 1}</td>
                        <td className="px-5 py-3 font-medium text-gray-800">{s.nama || '—'}</td>
                        <td className="px-5 py-3">
                          <Badge v={s.role} map={{ admin: 'bg-red-100 text-red-600', siswa: 'bg-blue-100 text-blue-600' }} />
                        </td>
                        <td className="px-5 py-3">
                          <Badge v={s.status || 'gratis'} map={{
                            gratis: 'bg-gray-100 text-gray-600',
                            premium: 'bg-yellow-100 text-yellow-700',
                            platinum: 'bg-purple-100 text-purple-700',
                          }} />
                        </td>
                        <td className="px-5 py-3 text-gray-400 text-xs">
                          {s.status_expired
                            ? new Date(s.status_expired).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })
                            : '—'}
                        </td>
                        <td className="px-5 py-3 text-gray-400 text-xs">
                          {new Date(s.created_at).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })}
                        </td>
                        <td className="px-5 py-3 text-center">
                          <button onClick={() => {
                            setEditUserData(s)
                            setEditUserForm({
                              nama: s.nama,
                              role: s.role,
                              status: s.status || 'gratis',
                            })
                            setShowEditUser(true)
                          }} className="text-xs text-blue-600 border border-blue-200 px-2 py-1 rounded transition">
                            Edit
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* MODAL EDIT USER */}
              {showEditUser && editUserData && (
                <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
                  <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-xl">
                    <div className="flex items-center justify-between mb-5">
                      <h3 className="font-black text-gray-800">Edit User</h3>
                      <button onClick={() => setShowEditUser(false)}
                        className="text-gray-400 hover:text-gray-700 text-xl">✕</button>
                    </div>
                    <div className="flex flex-col gap-3">
                      <div>
                        <label className="text-xs font-semibold text-gray-500 mb-1 block">Nama</label>
                        <input value={editUserForm.nama || ''} onChange={e => setEditUserForm({...editUserForm, nama: e.target.value})}
                          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400"/>
                      </div>
                      <div>
                        <label className="text-xs font-semibold text-gray-500 mb-1 block">Email</label>
                        <input value={editUserData.email || '—'} disabled
                          className="w-full border border-gray-100 rounded-lg px-3 py-2 text-sm text-gray-400 bg-gray-50"/>
                      </div>
                      <div>
                        <label className="text-xs font-semibold text-gray-500 mb-1 block">Role</label>
                        <select value={editUserForm.role || 'siswa'} onChange={e => setEditUserForm({...editUserForm, role: e.target.value})}
                          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400">
                          <option value="siswa">Siswa</option>
                          <option value="admin">Admin</option>
                        </select>
                      </div>
                      <div>
                        <label className="text-xs font-semibold text-gray-500 mb-1 block">Status Akses</label>
                        <select value={editUserForm.status || 'gratis'} onChange={e => setEditUserForm({...editUserForm, status: e.target.value})}
                          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400">
                          <option value="gratis">Gratis</option>
                          <option value="premium">Premium</option>
                          <option value="platinum">Platinum</option>
                        </select>
                      </div>
                      {editUserForm.status !== 'gratis' && (
                        <div className="text-xs text-gray-400 bg-gray-50 px-3 py-2 rounded-lg">
                          Expired otomatis: <strong>{new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })}</strong>
                        </div>
                      )}
                      <div className="flex gap-3 pt-2">
                        <button onClick={handleSaveUser}
                          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition">
                          Simpan
                        </button>
                        <button onClick={() => handleResetPassword(editUserData.email)}
                          className="flex-1 border border-gray-200 text-gray-600 px-4 py-2 rounded-lg text-sm hover:bg-gray-50 transition">
                          Reset Password
                        </button>
                      </div>
                      <button onClick={() => setShowEditUser(false)}
                        className="text-center text-gray-400 text-xs hover:text-gray-600 transition">
                        Batal
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* ── PAKET TRYOUT (list) ───────────────────────────────── */}
          {view === 'paket_tryout' && (
            <div>
              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-black text-gray-800">Paket Tryout</h2>
                  <p className="text-gray-500 text-sm">{paketTO.length} paket</p>
                </div>
                <button onClick={openAdd} className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">
                  + Tambah Paket
                </button>
              </div>

              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">{editData ? 'Edit Paket' : 'Tambah Paket Baru'}</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {inp('Nama paket (contoh: OSNK Paket 1)', 'nama')}
                    {sel('jenis', [
                      { value: 'OSNK', label: 'OSNK (Kabupaten/Kota)' },
                      { value: 'OSNP', label: 'OSNP (Provinsi)' },
                      { value: 'Nasional', label: 'Nasional' },
                    ], 'Pilih Jenis')}
                    {inp('Tahun (contoh: 2024)', 'tahun', 'number')}
                    {inp('Durasi (menit)', 'durasi_menit', 'number')}
                    {sel('status', [{ value: 'aktif', label: 'Aktif' }, { value: 'nonaktif', label: 'Nonaktif' }], 'Status')}
{sel('akses', [
                      { value: 'gratis', label: 'Gratis' },
                      { value: 'premium', label: 'Premium' },
                      { value: 'platinum', label: 'Platinum' },
                    ], 'Tipe Akses')}
                                        <div className="md:col-span-2">{inp('Deskripsi singkat (opsional)', 'deskripsi')}</div>
                  </div>
                  <div className="mt-3">
                    <FormBtns onSave={() => handleSave('paket_to', {
                      nama: formData.nama,
                      jenis: formData.jenis,
                      tahun: formData.tahun || null,
                      durasi_menit: formData.durasi_menit || 120,
                      status: formData.status || 'aktif',
                      is_premium: formData.is_premium === 'true',
                      deskripsi: formData.deskripsi || null,
                      ...(editData ? {} : { urutan: paketTO.length + 1 }),
                    })} />
                  </div>
                </div>
              )}

              <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 bg-gray-50">
                      <Th>Nama Paket</Th><Th>Jenis</Th><Th>Tahun</Th>
                      <ThC>Durasi</ThC><ThC>Tipe</ThC><ThC>Status</ThC><ThC>Aksi</ThC>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {paketTO.map((p, i) => (
                      <tr key={i} className="hover:bg-gray-50">
                        <td className="px-5 py-3 font-medium text-gray-800">{p.nama}</td>
                        <td className="px-5 py-3 text-gray-500 text-xs">{p.jenis || '—'}</td>
                        <td className="px-5 py-3 text-gray-500 text-xs">{p.tahun || '—'}</td>
                        <td className="px-5 py-3 text-center text-gray-500 text-xs">{p.durasi_menit} mnt</td>
                        <td className="px-5 py-3 text-center">
                          <Badge v={p.is_premium ? 'Premium' : 'Gratis'} map={{ Premium: 'bg-yellow-100 text-yellow-700', Gratis: 'bg-green-100 text-green-700' }} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          <Badge v={p.status || 'aktif'} map={{ aktif: 'bg-blue-100 text-blue-700', nonaktif: 'bg-gray-100 text-gray-500' }} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          <div className="flex items-center justify-center gap-2">
                            <button onClick={async () => {
                              setSelectedPaket(p)
                              await loadSoalTO(p.id)
                              setView('soal_tryout')
                            }} className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded transition">
                              Kelola Soal
                            </button>
                            <button onClick={() => {
                              setEditData(p)
                              setFormData({
                                nama: p.nama,
                                jenis: p.jenis,
                                tahun: p.tahun,
                                durasi_menit: p.durasi_menit,
                                status: p.status,
                                is_premium: p.is_premium ? 'true' : 'false',
                                deskripsi: p.deskripsi,
                              })
                              setShowForm(true)
                            }} className="text-xs text-blue-600 border border-blue-200 px-2 py-1 rounded transition">
                              Edit
                            </button>
                            <button onClick={() => handleDelete('paket_to', p.id)}
                              className="text-xs text-red-500 border border-red-200 px-2 py-1 rounded transition">
                              Hapus
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                    {paketTO.length === 0 && (
                      <tr><td colSpan={7} className="px-5 py-8 text-center text-gray-400 text-sm">Belum ada paket tryout.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* ── SOAL TRYOUT (drill-down dari paket) ──────────────── */}
          {view === 'soal_tryout' && selectedPaket && (
            <div>
              {/* Breadcrumb */}
              <div className="flex items-center gap-2 mb-5 text-sm">
                <button onClick={() => { setView('paket_tryout'); setSelectedPaket(null); resetForm() }}
                  className="text-blue-600 hover:underline font-medium">Paket Tryout</button>
                <span className="text-gray-400">›</span>
                <span className="font-bold text-gray-800">{selectedPaket.nama}</span>
              </div>

              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-black text-gray-800">{selectedPaket.nama}</h2>
                  <p className="text-gray-500 text-sm">{soalTO.length} soal · {selectedPaket.jenis} · {selectedPaket.durasi_menit} menit</p>
                </div>
                <button onClick={openAdd} className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">
                  + Tambah Soal
                </button>
              </div>

              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">{editData ? 'Edit Soal' : 'Tambah Soal Baru'}</h3>
                  <div className="flex flex-col gap-3">
                    {ta('Tulis pertanyaan di sini...', 'pertanyaan', 4)}
   <div>
                      <label className="text-xs font-semibold text-gray-500 mb-1 block">Gambar Soal (opsional)</label>
                      <div className="flex gap-2">
                        <input placeholder="URL gambar atau upload di bawah" value={formData.gambar_url || ''}
                          onChange={e => setFormData({...formData, gambar_url: e.target.value})}
                          className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400"/>
                        <label className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-lg text-sm cursor-pointer transition shrink-0">
                          Upload
                          <input type="file" accept="image/*" className="hidden" onChange={async e => {
                            const file = e.target.files?.[0]
                            if (!file) return
                            const ext = file.name.split('.').pop()
                            const fileName = `${Date.now()}.${ext}`
                            const { data, error } = await supabase.storage
                              .from('soal-images')
                              .upload(fileName, file)
                            if (error) { alert('Gagal upload: ' + error.message); return }
                            const { data: urlData } = supabase.storage
                              .from('soal-images')
                              .getPublicUrl(fileName)
                            setFormData({...formData, gambar_url: urlData.publicUrl})
                          }}/>
                        </label>
                      </div>
                      {formData.gambar_url && (
                        <img src={formData.gambar_url} alt="preview" className="mt-2 max-h-32 rounded-lg object-contain border border-gray-100"/>
                      )}
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
                      {['a', 'b', 'c', 'd', 'e'].map(op => (
                        <div key={op}>
                          <label className="text-xs font-semibold text-gray-500 mb-1 block">Pilihan {op.toUpperCase()}</label>
                          {inp(`Opsi ${op.toUpperCase()}`, `pilihan_${op}`)}
                        </div>
                      ))}
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      {sel('jawaban_benar', ['A','B','C','D','E'].map(x => ({ value: x, label: x })), 'Jawaban Benar')}
                      {sel('is_premium', [{ value: 'false', label: 'Gratis' }, { value: 'true', label: 'Premium' }], 'Tipe')}
                    </div>
                    {ta('Tulis pembahasan jawaban...', 'pembahasan', 2)}
                    <FormBtns onSave={async () => {
                      await handleSave('soal', {
                        paket_id: selectedPaket.id,
                        pertanyaan: formData.pertanyaan,
                        gambar_url: formData.gambar_url || null,
                        pilihan_a: formData.pilihan_a,
                        pilihan_b: formData.pilihan_b,
                        pilihan_c: formData.pilihan_c,
                        pilihan_d: formData.pilihan_d,
                        pilihan_e: formData.pilihan_e,
                        jawaban_benar: formData.jawaban_benar,
                        pembahasan: formData.pembahasan,
                        is_premium: formData.is_premium === 'true',
                      })
                      await loadSoalTO(selectedPaket.id)
                    }} />
                  </div>
                </div>
              )}

              <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 bg-gray-50">
                      <Th>No</Th><Th>Pertanyaan</Th><ThC>Jwb</ThC><ThC>Gambar</ThC><ThC>Tipe</ThC><ThC>Aksi</ThC>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {soalTO.map((s, i) => (
                      <tr key={i} className="hover:bg-gray-50">
                        <td className="px-5 py-3 text-gray-400 text-xs">{i + 1}</td>
                        <td className="px-5 py-3 text-gray-800 max-w-xs"><p className="truncate">{s.pertanyaan}</p></td>
                        <td className="px-5 py-3 text-center">
                          <span className="bg-green-100 text-green-700 text-xs font-bold px-2 py-0.5 rounded">{s.jawaban_benar}</span>
                        </td>
                        <td className="px-5 py-3 text-center">
                          {s.gambar_url ? <span className="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded">Ada</span> : <span className="text-xs text-gray-300">—</span>}
                        </td>
                        <td className="px-5 py-3 text-center">
                          <Badge v={s.is_premium ? 'Premium' : 'Gratis'} map={{ Premium: 'bg-yellow-100 text-yellow-700', Gratis: 'bg-green-100 text-green-700' }} />
                        </td>
                        <td className="px-5 py-3 text-center">
  <div className="flex items-center justify-center gap-2">
    <button onClick={() => {
      setEditSoalData(s)
      setEditSoalForm({
        pertanyaan: s.pertanyaan,
        gambar_url: s.gambar_url || '',
        pilihan_a: s.pilihan_a,
        pilihan_b: s.pilihan_b,
        pilihan_c: s.pilihan_c,
        pilihan_d: s.pilihan_d,
        pilihan_e: s.pilihan_e,
        jawaban_benar: s.jawaban_benar,
        pembahasan: s.pembahasan,
        is_premium: s.is_premium ? 'true' : 'false',
      })
      setShowEditSoal(true)
    }} className="text-xs text-blue-600 border border-blue-200 px-2 py-1 rounded transition">
      Edit
    </button>
    <button onClick={async () => {
      await handleDelete('soal', s.id)
      await loadSoalTO(selectedPaket.id)
    }} className="text-xs text-red-500 border border-red-200 px-2 py-1 rounded transition">
      Hapus
    </button>
  </div>
</td>
                      </tr>
                    ))}
                    {soalTO.length === 0 && (
                      <tr><td colSpan={6} className="px-5 py-8 text-center text-gray-400 text-sm">Belum ada soal. Klik + Tambah Soal untuk mulai.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* MODAL EDIT SOAL TO */}
{showEditSoal && editSoalData && (
  <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
    <div className="bg-white rounded-2xl p-6 max-w-2xl w-full shadow-xl max-h-[90vh] overflow-y-auto">
      <div className="flex items-center justify-between mb-5">
        <h3 className="font-black text-gray-800">Edit Soal #{editSoalData.id}</h3>
        <button onClick={() => setShowEditSoal(false)}
          className="text-gray-400 hover:text-gray-700 text-xl">✕</button>
      </div>
      <div className="flex flex-col gap-3">
        <div>
          <label className="text-xs font-semibold text-gray-500 mb-1 block">Pertanyaan</label>
          <textarea rows={4} value={editSoalForm.pertanyaan || ''} onChange={e => setEditSoalForm({...editSoalForm, pertanyaan: e.target.value})}
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400"/>
        </div>
        <div>
          <label className="text-xs font-semibold text-gray-500 mb-1 block">Gambar Soal (opsional)</label>
          <div className="flex gap-2">
            <input placeholder="URL gambar atau upload" value={editSoalForm.gambar_url || ''}
              onChange={e => setEditSoalForm({...editSoalForm, gambar_url: e.target.value})}
              className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400"/>
            <label className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-lg text-sm cursor-pointer transition shrink-0">
              Upload
              <input type="file" accept="image/*" className="hidden" onChange={async e => {
                const file = e.target.files?.[0]
                if (!file) return
                const ext = file.name.split('.').pop()
                const fileName = `${Date.now()}.${ext}`
                const { data, error } = await supabase.storage
                  .from('soal-images')
                  .upload(fileName, file)
                if (error) { alert('Gagal upload: ' + error.message); return }
                const { data: urlData } = supabase.storage
                  .from('soal-images')
                  .getPublicUrl(fileName)
                setEditSoalForm({...editSoalForm, gambar_url: urlData.publicUrl})
              }}/>
            </label>
          </div>
          {editSoalForm.gambar_url && (
            <img src={editSoalForm.gambar_url} alt="preview" className="mt-2 max-h-32 rounded-lg object-contain border border-gray-100"/>
          )}
        </div>
<div className="flex flex-col gap-3">
            {['a','b','c','d','e'].map(op => (
            <div key={op}>
              <label className="text-xs font-semibold text-gray-500 mb-1 block">Pilihan {op.toUpperCase()}</label>
              <input value={editSoalForm[`pilihan_${op}`] || ''} onChange={e => setEditSoalForm({...editSoalForm, [`pilihan_${op}`]: e.target.value})}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400"/>
            </div>
          ))}
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-xs font-semibold text-gray-500 mb-1 block">Jawaban Benar</label>
            <select value={editSoalForm.jawaban_benar || ''} onChange={e => setEditSoalForm({...editSoalForm, jawaban_benar: e.target.value})}
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400">
              {['A','B','C','D','E'].map(op => <option key={op} value={op}>{op}</option>)}
            </select>
          </div>
          <div>
            <label className="text-xs font-semibold text-gray-500 mb-1 block">Tipe</label>
            <select value={editSoalForm.is_premium} onChange={e => setEditSoalForm({...editSoalForm, is_premium: e.target.value})}
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400">
              <option value="false">Gratis</option>
              <option value="true">Premium</option>
            </select>
          </div>
        </div>
        <div>
          <label className="text-xs font-semibold text-gray-500 mb-1 block">Pembahasan</label>
          <textarea rows={3} value={editSoalForm.pembahasan || ''} onChange={e => setEditSoalForm({...editSoalForm, pembahasan: e.target.value})}
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400"/>
        </div>
        <div className="flex gap-3 pt-2">
          <button onClick={handleSaveSoal}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg text-sm font-semibold transition">
            Simpan Perubahan
          </button>
          <button onClick={() => setShowEditSoal(false)}
            className="border border-gray-200 text-gray-600 px-4 py-2 rounded-lg text-sm transition">
            Batal
          </button>
        </div>
      </div>
    </div>
  </div>
)}

          {/* ── PENDALAMAN MATERI (list topik → paket) ───────────── */}
          {view === 'pendalaman' && !selectedTopik && (
            <div>
              <div className="mb-5">
                <h2 className="text-xl font-black text-gray-800">Pendalaman Materi</h2>
                <p className="text-gray-500 text-sm">Pilih topik untuk kelola paket pendalaman</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {topikList.map((t) => {
                  const jumlahPaket = paketPendalaman.filter(p => p.topik_id === t.id).length
                  return (
                    <button key={t.id} onClick={() => setSelectedTopik(t)}
                      className="bg-white border border-gray-200 rounded-xl p-4 text-left hover:border-blue-400 hover:shadow-sm transition">
                      <div className="font-bold text-gray-800 text-sm mb-1">{t.nama}</div>
                      <div className="text-xs text-gray-400">{jumlahPaket} paket pendalaman</div>
                    </button>
                  )
                })}
              </div>
            </div>
          )}

          {/* ── PENDALAMAN: LIST PAKET PER TOPIK ─────────────────── */}
          {view === 'pendalaman' && selectedTopik && !selectedPaketPendalaman && (
            <div>
              <div className="flex items-center gap-2 mb-5 text-sm">
                <button onClick={() => { setSelectedTopik(null); resetForm() }}
                  className="text-blue-600 hover:underline font-medium">Pendalaman Materi</button>
                <span className="text-gray-400">›</span>
                <span className="font-bold text-gray-800">{selectedTopik.nama}</span>
              </div>

              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-black text-gray-800">{selectedTopik.nama}</h2>
                  <p className="text-gray-500 text-sm">Paket pendalaman untuk topik ini</p>
                </div>
                <button onClick={openAdd} className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">
                  + Tambah Paket
                </button>
              </div>

              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">{editData ? 'Edit Paket Pendalaman' : 'Tambah Paket Pendalaman'}</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {inp('Nama paket (contoh: Latihan Soal Hidrosfer)', 'nama')}
                    {inp('Durasi (menit)', 'durasi_menit', 'number')}
                    {sel('status', [{ value: 'aktif', label: 'Aktif' }, { value: 'nonaktif', label: 'Nonaktif' }], 'Status')}
{sel('akses', [
                      { value: 'gratis', label: 'Gratis' },
                      { value: 'premium', label: 'Premium' },
                      { value: 'platinum', label: 'Platinum' },
                    ], 'Tipe Akses')}
                                        <div className="md:col-span-2">{inp('Deskripsi (opsional)', 'deskripsi')}</div>
                  </div>
                  <div className="mt-3">
                    <FormBtns onSave={() => handleSave('paket_pendalaman', {
                      topik_id: selectedTopik.id,
                      nama: formData.nama,
                      durasi_menit: formData.durasi_menit || 60,
                      status: formData.status || 'aktif',
                      is_premium: formData.is_premium === 'true',
                      deskripsi: formData.deskripsi || null,
                    })} />
                  </div>
                </div>
              )}

              <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 bg-gray-50">
                      <Th>Nama Paket</Th><ThC>Durasi</ThC><ThC>Tipe</ThC><ThC>Status</ThC><ThC>Aksi</ThC>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {paketPendalaman.filter(p => p.topik_id === selectedTopik.id).map((p, i) => (
                      <tr key={i} className="hover:bg-gray-50">
                        <td className="px-5 py-3 font-medium text-gray-800">{p.nama}</td>
                        <td className="px-5 py-3 text-center text-gray-500 text-xs">{p.durasi_menit} mnt</td>
                        <td className="px-5 py-3 text-center">
                          <Badge v={p.is_premium ? 'Premium' : 'Gratis'} map={{ Premium: 'bg-yellow-100 text-yellow-700', Gratis: 'bg-green-100 text-green-700' }} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          <Badge v={p.status || 'aktif'} map={{ aktif: 'bg-blue-100 text-blue-700', nonaktif: 'bg-gray-100 text-gray-500' }} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          <div className="flex items-center justify-center gap-2">
                            <button onClick={async () => {
                              setSelectedPaketPendalaman(p)
                              await loadSoalPendalaman(p.id)
                              resetForm()
                            }} className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded transition">
                              Kelola Soal
                            </button>
                            <button onClick={() => {
                              setEditData(p)
                              setFormData({
                                nama: p.nama,
                                durasi_menit: p.durasi_menit,
                                status: p.status,
                                is_premium: p.is_premium ? 'true' : 'false',
                                deskripsi: p.deskripsi,
                              })
                              setShowForm(true)
                            }} className="text-xs text-blue-600 border border-blue-200 px-2 py-1 rounded transition">
                              Edit
                            </button>
                            <button onClick={() => handleDelete('paket_pendalaman', p.id)}
                              className="text-xs text-red-500 border border-red-200 px-2 py-1 rounded transition">
                              Hapus
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                    {paketPendalaman.filter(p => p.topik_id === selectedTopik.id).length === 0 && (
                      <tr><td colSpan={5} className="px-5 py-8 text-center text-gray-400 text-sm">Belum ada paket untuk topik ini.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* ── SOAL PENDALAMAN ───────────────────────────────────── */}
          {view === 'pendalaman' && selectedTopik && selectedPaketPendalaman && (
            <div>
              <div className="flex items-center gap-2 mb-5 text-sm flex-wrap">
                <button onClick={() => { setSelectedTopik(null); setSelectedPaketPendalaman(null); resetForm() }}
                  className="text-blue-600 hover:underline font-medium">Pendalaman Materi</button>
                <span className="text-gray-400">›</span>
                <button onClick={() => { setSelectedPaketPendalaman(null); resetForm() }}
                  className="text-blue-600 hover:underline font-medium">{selectedTopik.nama}</button>
                <span className="text-gray-400">›</span>
                <span className="font-bold text-gray-800">{selectedPaketPendalaman.nama}</span>
              </div>

              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-black text-gray-800">{selectedPaketPendalaman.nama}</h2>
                  <p className="text-gray-500 text-sm">{soalPendalaman.length} soal · {selectedTopik.nama}</p>
                </div>
                <button onClick={openAdd} className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">
                  + Tambah Soal
                </button>
              </div>

              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">Tambah Soal Pendalaman</h3>
                  <div className="flex flex-col gap-3">
                    {ta('Tulis pertanyaan di sini...', 'pertanyaan', 4)}
                    <div>
                      <label className="text-xs font-semibold text-gray-500 mb-1 block">Gambar Soal (opsional)</label>
                      <div className="flex gap-2">
                        <input placeholder="URL gambar atau upload di bawah" value={formData.gambar_url || ''}
                          onChange={e => setFormData({...formData, gambar_url: e.target.value})}
                          className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400"/>
                        <label className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-lg text-sm cursor-pointer transition shrink-0">
                          Upload
                          <input type="file" accept="image/*" className="hidden" onChange={async e => {
                            const file = e.target.files?.[0]
                            if (!file) return
                            const ext = file.name.split('.').pop()
                            const fileName = `${Date.now()}.${ext}`
                            const { data, error } = await supabase.storage
                              .from('soal-images')
                              .upload(fileName, file)
                            if (error) { alert('Gagal upload: ' + error.message); return }
                            const { data: urlData } = supabase.storage
                              .from('soal-images')
                              .getPublicUrl(fileName)
                            setFormData({...formData, gambar_url: urlData.publicUrl})
                          }}/>
                        </label>
                      </div>
                      {formData.gambar_url && (
                        <img src={formData.gambar_url} alt="preview" className="mt-2 max-h-32 rounded-lg object-contain border border-gray-100"/>
                      )}
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
                      {['a', 'b', 'c', 'd', 'e'].map(op => (
                        <div key={op}>
                          <label className="text-xs font-semibold text-gray-500 mb-1 block">Pilihan {op.toUpperCase()}</label>
                          {inp(`Opsi ${op.toUpperCase()}`, `pilihan_${op}`)}
                        </div>
                      ))}
                    </div>
                    {sel('jawaban_benar', ['A','B','C','D','E'].map(x => ({ value: x, label: x })), 'Jawaban Benar')}
                    {ta('Tulis pembahasan jawaban...', 'pembahasan', 2)}
                    <FormBtns onSave={async () => {
                      await handleSave('soal_pendalaman', {
                        paket_id: selectedPaketPendalaman.id,
                        pertanyaan: formData.pertanyaan,
                        gambar_url: formData.gambar_url || null,
                        pilihan_a: formData.pilihan_a,
                        pilihan_b: formData.pilihan_b,
                        pilihan_c: formData.pilihan_c,
                        pilihan_d: formData.pilihan_d,
                        pilihan_e: formData.pilihan_e,
                        jawaban_benar: formData.jawaban_benar,
                        pembahasan: formData.pembahasan,
                      })
                      await loadSoalPendalaman(selectedPaketPendalaman.id)
                    }} />
                  </div>
                </div>
              )}

              <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 bg-gray-50">
                      <Th>No</Th><Th>Pertanyaan</Th><ThC>Jwb</ThC><ThC>Gambar</ThC><ThC>Aksi</ThC>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {soalPendalaman.map((s, i) => (
                      <tr key={i} className="hover:bg-gray-50">
                        <td className="px-5 py-3 text-gray-400 text-xs">{i + 1}</td>
                        <td className="px-5 py-3 text-gray-800 max-w-xs"><p className="truncate">{s.pertanyaan}</p></td>
                        <td className="px-5 py-3 text-center">
                          <span className="bg-green-100 text-green-700 text-xs font-bold px-2 py-0.5 rounded">{s.jawaban_benar}</span>
                        </td>
                        <td className="px-5 py-3 text-center">
                          {s.gambar_url ? <span className="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded">Ada</span> : <span className="text-xs text-gray-300">—</span>}
                        </td>
                        <td className="px-5 py-3 text-center">
  <div className="flex items-center justify-center gap-2">
    <button onClick={() => {
      setEditSoalData(s)
      setEditSoalForm({
        pertanyaan: s.pertanyaan,
        gambar_url: s.gambar_url || '',
        pilihan_a: s.pilihan_a,
        pilihan_b: s.pilihan_b,
        pilihan_c: s.pilihan_c,
        pilihan_d: s.pilihan_d,
        pilihan_e: s.pilihan_e,
        jawaban_benar: s.jawaban_benar,
        pembahasan: s.pembahasan,
      })
      setShowEditSoal(true)
    }} className="text-xs text-blue-600 border border-blue-200 px-2 py-1 rounded transition">
      Edit
    </button>
    <button onClick={async () => {
      await handleDelete('soal_pendalaman', s.id)
      await loadSoalPendalaman(selectedPaketPendalaman.id)
    }} className="text-xs text-red-500 border border-red-200 px-2 py-1 rounded transition">
      Hapus
    </button>
  </div>
</td>
                      </tr>
                    ))}
                    {soalPendalaman.length === 0 && (
                      <tr><td colSpan={5} className="px-5 py-8 text-center text-gray-400 text-sm">Belum ada soal.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* ── VIDEO PEMBELAJARAN ────────────────────────────────── */}
          {view === 'video' && (
            <div>
              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-black text-gray-800">Video Pembelajaran</h2>
                  <p className="text-gray-500 text-sm">{videoList.length} video</p>
                </div>
                <button onClick={openAdd} className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">+ Tambah Video</button>
              </div>
              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">Tambah Video</h3>
                  <div className="grid grid-cols-2 gap-3 mb-3">
                    {inp('Judul video', 'judul')}
                    {inp('YouTube ID (contoh: dQw4w9WgXcQ)', 'youtube_id')}
                    {sel('topik_id', topikList.map(t => ({ value: t.id, label: t.nama })), 'Pilih Topik')}
                    {sel('is_premium', [{ value: 'false', label: 'Gratis' }, { value: 'true', label: 'Premium' }], 'Tipe')}
                  </div>
                  <FormBtns onSave={() => handleSave('video_pembelajaran', {
                    judul: formData.judul,
                    youtube_id: formData.youtube_id,
                    topik_id: Number(formData.topik_id),
                    is_premium: formData.is_premium === 'true',
                    urutan: videoList.length + 1,
                  })} />
                </div>
              )}
              <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 bg-gray-50">
                      <Th>Judul</Th><Th>Topik</Th><Th>YouTube ID</Th><ThC>Tipe</ThC><ThC>Aksi</ThC>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {videoList.map((v, i) => (
                      <tr key={i} className="hover:bg-gray-50">
                        <td className="px-5 py-3 font-medium text-gray-800">{v.judul}</td>
                        <td className="px-5 py-3 text-gray-500 text-xs">{v.topik_materi?.nama || '—'}</td>
                        <td className="px-5 py-3 text-gray-500 text-xs font-mono">{v.youtube_id}</td>
                        <td className="px-5 py-3 text-center">
                          <Badge v={v.is_premium ? 'Premium' : 'Gratis'} map={{ Premium: 'bg-yellow-100 text-yellow-700', Gratis: 'bg-green-100 text-green-700' }} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          <button onClick={() => handleDelete('video_pembelajaran', v.id)}
                            className="text-xs text-red-500 border border-red-200 px-2 py-1 rounded transition">Hapus</button>
                        </td>
                      </tr>
                    ))}
                    {videoList.length === 0 && <tr><td colSpan={5} className="px-5 py-8 text-center text-gray-400 text-sm">Belum ada video.</td></tr>}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* ── MODUL / PDF ───────────────────────────────────────── */}
          {view === 'modul' && (
            <div>
              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-black text-gray-800">Modul / PDF</h2>
                  <p className="text-gray-500 text-sm">{modulList.length} modul</p>
                </div>
                <button onClick={openAdd} className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">+ Tambah Modul</button>
              </div>
              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">Tambah Modul</h3>
                  <div className="grid grid-cols-2 gap-3 mb-3">
                    {inp('Judul modul', 'judul')}
                    {sel('topik_id', topikList.map(t => ({ value: t.id, label: t.nama })), 'Pilih Topik')}
                    <div className="col-span-2">{inp('URL File (Google Drive / langsung)', 'file_url')}</div>
                    {sel('is_premium', [{ value: 'false', label: 'Gratis' }, { value: 'true', label: 'Premium' }], 'Tipe')}
                    {inp('Deskripsi (opsional)', 'deskripsi')}
                  </div>
                  <FormBtns onSave={() => handleSave('modul_materi', {
                    judul: formData.judul,
                    topik_id: Number(formData.topik_id),
                    file_url: formData.file_url,
                    is_premium: formData.is_premium === 'true',
                    deskripsi: formData.deskripsi || null,
                  })} />
                </div>
              )}
              <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 bg-gray-50">
                      <Th>Judul</Th><Th>Topik</Th><ThC>Tipe</ThC><ThC>File</ThC><ThC>Aksi</ThC>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {modulList.map((m, i) => (
                      <tr key={i} className="hover:bg-gray-50">
                        <td className="px-5 py-3 font-medium text-gray-800">{m.judul}</td>
                        <td className="px-5 py-3 text-gray-500 text-xs">{m.topik_materi?.nama || '—'}</td>
                        <td className="px-5 py-3 text-center">
                          <Badge v={m.is_premium ? 'Premium' : 'Gratis'} map={{ Premium: 'bg-yellow-100 text-yellow-700', Gratis: 'bg-green-100 text-green-700' }} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          {m.file_url ? <a href={m.file_url} target="_blank" rel="noreferrer" className="text-xs text-blue-600 hover:underline">Buka</a> : <span className="text-gray-300 text-xs">—</span>}
                        </td>
                        <td className="px-5 py-3 text-center">
                          <button onClick={() => handleDelete('modul_materi', m.id)}
                            className="text-xs text-red-500 border border-red-200 px-2 py-1 rounded transition">Hapus</button>
                        </td>
                      </tr>
                    ))}
                    {modulList.length === 0 && <tr><td colSpan={5} className="px-5 py-8 text-center text-gray-400 text-sm">Belum ada modul.</td></tr>}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* ── PAKET MEMBERSHIP ──────────────────────────────────── */}
          {view === 'membership' && (
            <div>
              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-black text-gray-800">Paket Membership</h2>
                  <p className="text-gray-500 text-sm">{membershipList.length} paket</p>
                </div>
                <button onClick={openAdd} className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">+ Tambah Paket</button>
              </div>
              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">{editData ? 'Edit Paket Membership' : 'Tambah Paket Membership'}</h3>
                  <div className="grid grid-cols-2 gap-3 mb-3">
                    {inp('Nama paket', 'nama')}
                    {inp('Harga (Rp)', 'harga', 'number')}
                    {inp('Durasi (hari)', 'durasi_hari', 'number')}
                    {inp('Deskripsi singkat', 'deskripsi')}
                    <div className="col-span-2">{ta('Fitur (pisahkan dengan enter)', 'fitur', 3)}</div>
                  </div>
                  <FormBtns onSave={() => handleSave('paket_membership', {
                    nama: formData.nama,
                    harga: formData.harga,
                    durasi_hari: formData.durasi_hari,
                    deskripsi: formData.deskripsi,
                    fitur: formData.fitur,
                  })} />
                </div>
              )}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {membershipList.map((m, i) => (
                  <div key={i} className="bg-white border border-gray-200 rounded-xl p-5">
                    <div className="font-black text-gray-800 mb-1">{m.nama}</div>
                    <div className="text-2xl font-black text-blue-600 mb-1">Rp {m.harga?.toLocaleString('id-ID')}</div>
                    <div className="text-xs text-gray-400 mb-3">{m.durasi_hari} hari · {m.deskripsi}</div>
                    <div className="flex gap-2">
                      <button onClick={() => {
                        setEditData(m)
                        setFormData({
                          nama: m.nama,
                          harga: m.harga,
                          durasi_hari: m.durasi_hari,
                          deskripsi: m.deskripsi,
                          fitur: m.fitur,
                        })
                        setShowForm(true)
                      }} className="text-xs text-blue-600 border border-blue-200 px-3 py-1 rounded transition">Edit</button>
                      <button onClick={() => handleDelete('paket_membership', m.id)}
                        className="text-xs text-red-500 border border-red-200 px-3 py-1 rounded transition">Hapus</button>
                    </div>
                  </div>
                ))}
                {membershipList.length === 0 && (
                  <div className="col-span-3 bg-white border border-gray-200 rounded-xl px-5 py-8 text-center text-gray-400 text-sm">Belum ada paket membership.</div>
                )}
              </div>
            </div>
          )}

          {/* ── TRANSAKSI ─────────────────────────────────────────── */}
          {view === 'transaksi' && (
            <div>
              <div className="mb-5">
                <h2 className="text-xl font-black text-gray-800">Daftar Transaksi</h2>
                <p className="text-gray-500 text-sm">{transaksiList.length} transaksi</p>
              </div>
              <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 bg-gray-50">
                      <Th>Siswa</Th><Th>Paket</Th><ThC>Nominal</ThC><ThC>Status</ThC><ThC>Ubah Status</ThC>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {transaksiList.map((t, i) => (
                      <tr key={i} className="hover:bg-gray-50">
                        <td className="px-5 py-3 font-medium text-gray-800">{t.profiles?.nama || '—'}</td>
                        <td className="px-5 py-3 text-gray-500 text-xs">{t.paket_membership?.nama || '—'}</td>
                        <td className="px-5 py-3 text-center font-semibold text-gray-800">Rp {t.nominal?.toLocaleString('id-ID')}</td>
                        <td className="px-5 py-3 text-center">
                          <Badge v={t.status} map={{
                            selesai: 'bg-green-100 text-green-700',
                            dibayar: 'bg-blue-100 text-blue-700',
                            gagal: 'bg-red-100 text-red-700',
                            pending: 'bg-yellow-100 text-yellow-700',
                          }} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          <select value={t.status} onChange={async e => {
                            await supabase.from('transaksi').update({ status: e.target.value }).eq('id', t.id)
                            await loadAll()
                          }} className="text-xs border border-gray-200 rounded px-2 py-1 text-gray-700 focus:outline-none">
                            {['pending', 'dibayar', 'selesai', 'gagal'].map(s => <option key={s} value={s}>{s}</option>)}
                          </select>
                        </td>
                      </tr>
                    ))}
                    {transaksiList.length === 0 && <tr><td colSpan={5} className="px-5 py-8 text-center text-gray-400 text-sm">Belum ada transaksi.</td></tr>}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* ── PENGUMUMAN ────────────────────────────────────────── */}
          {view === 'pengumuman' && (
            <div>
              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-black text-gray-800">Pengumuman</h2>
                  <p className="text-gray-500 text-sm">{pengumumanList.length} pengumuman</p>
                </div>
                <button onClick={openAdd} className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">+ Tambah</button>
              </div>
              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">Tambah Pengumuman</h3>
                  <div className="flex flex-col gap-3">
                    {inp('Judul pengumuman', 'judul')}
                    {ta('Isi pengumuman...', 'isi', 3)}
                    <FormBtns onSave={() => handleSave('pengumuman', { judul: formData.judul, isi: formData.isi, aktif: true })} />
                  </div>
                </div>
              )}
              <div className="flex flex-col gap-3">
                {pengumumanList.map((p, i) => (
                  <div key={i} className="bg-white border border-gray-200 rounded-xl px-5 py-4 flex items-start justify-between">
                    <div>
                      <div className="font-bold text-sm text-gray-800">{p.judul}</div>
                      <div className="text-gray-500 text-xs mt-1">{p.isi}</div>
                      <div className="text-gray-400 text-xs mt-1">{new Date(p.created_at).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })}</div>
                    </div>
                    <button onClick={() => handleDelete('pengumuman', p.id)}
                      className="text-xs text-red-500 border border-red-200 px-2 py-1 rounded transition ml-4 shrink-0">Hapus</button>
                  </div>
                ))}
                {pengumumanList.length === 0 && (
                  <div className="bg-white border border-gray-200 rounded-xl px-5 py-8 text-center text-gray-400 text-sm">Belum ada pengumuman.</div>
                )}
              </div>
            </div>
          )}

          {/* ── BANNER ───────────────────────────────────────────── */}
          {view === 'banner' && (
            <div>
              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-black text-gray-800">Banner</h2>
                  <p className="text-gray-500 text-sm">{bannerList.length} banner</p>
                </div>
                <button onClick={openAdd} className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">+ Tambah Banner</button>
              </div>
              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">Tambah Banner</h3>
                  <div className="grid grid-cols-2 gap-3 mb-3">
                    {inp('Judul banner', 'judul')}
                    {inp('URL Gambar', 'gambar_url')}
                    <div className="col-span-2">{inp('Link tujuan (opsional)', 'link')}</div>
                  </div>
                  <FormBtns onSave={() => handleSave('banner', {
                    judul: formData.judul,
                    gambar_url: formData.gambar_url,
                    link: formData.link || null,
                    aktif: true,
                  })} />
                </div>
              )}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {bannerList.map((b, i) => (
                  <div key={i} className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                    {b.gambar_url && <img src={b.gambar_url} alt={b.judul} className="w-full h-32 object-cover" />}
                    <div className="p-4 flex items-center justify-between">
                      <div>
                        <div className="font-bold text-sm text-gray-800">{b.judul}</div>
                        {b.link && <a href={b.link} target="_blank" rel="noreferrer" className="text-xs text-blue-500 hover:underline">{b.link}</a>}
                      </div>
                      <button onClick={() => handleDelete('banner', b.id)}
                        className="text-xs text-red-500 border border-red-200 px-2 py-1 rounded transition ml-3 shrink-0">Hapus</button>
                    </div>
                  </div>
                ))}
                {bannerList.length === 0 && (
                  <div className="col-span-2 bg-white border border-gray-200 rounded-xl px-5 py-8 text-center text-gray-400 text-sm">Belum ada banner.</div>
                )}
              </div>
            </div>
          )}

       {/* MODAL EDIT SOAL PENDALAMAN */}
{showEditSoal && editSoalData && !selectedPaket && (
  <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
    <div className="bg-white rounded-2xl p-6 max-w-2xl w-full shadow-xl max-h-[90vh] overflow-y-auto">
      <div className="flex items-center justify-between mb-5">
        <h3 className="font-black text-gray-800">Edit Soal #{editSoalData.id}</h3>
        <button onClick={() => setShowEditSoal(false)}
          className="text-gray-400 hover:text-gray-700 text-xl">✕</button>
      </div>
      <div className="flex flex-col gap-3">
        <div>
          <label className="text-xs font-semibold text-gray-500 mb-1 block">Pertanyaan</label>
          <textarea rows={4} value={editSoalForm.pertanyaan || ''} onChange={e => setEditSoalForm({...editSoalForm, pertanyaan: e.target.value})}
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400"/>
        </div>
        <div>
          <label className="text-xs font-semibold text-gray-500 mb-1 block">Gambar Soal (opsional)</label>
          <div className="flex gap-2">
            <input placeholder="URL gambar atau upload" value={editSoalForm.gambar_url || ''}
              onChange={e => setEditSoalForm({...editSoalForm, gambar_url: e.target.value})}
              className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400"/>
            <label className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-lg text-sm cursor-pointer transition shrink-0">
              Upload
              <input type="file" accept="image/*" className="hidden" onChange={async e => {
                const file = e.target.files?.[0]
                if (!file) return
                const ext = file.name.split('.').pop()
                const fileName = `${Date.now()}.${ext}`
                const { data, error } = await supabase.storage
                  .from('soal-images')
                 .upload(fileName, file)
                if (error) { alert('Gagal upload: ' + error.message); return }
                const { data: urlData } = supabase.storage
                  .from('soal-images')
                  .getPublicUrl(fileName)
                setEditSoalForm({...editSoalForm, gambar_url: urlData.publicUrl})
              }}/>
            </label>
          </div>
          {editSoalForm.gambar_url && (
            <img src={editSoalForm.gambar_url} alt="preview" className="mt-2 max-h-32 rounded-lg object-contain border border-gray-100"/>
          )}
        </div>
        <div className="flex flex-col gap-3">
          {['a','b','c','d','e'].map(op => (
            <div key={op}>
              <label className="text-xs font-semibold text-gray-500 mb-1 block">Pilihan {op.toUpperCase()}</label>
              <input value={editSoalForm[`pilihan_${op}`] || ''} onChange={e => setEditSoalForm({...editSoalForm, [`pilihan_${op}`]: e.target.value})}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400"/>
            </div>
          ))}
        </div>
        <div>
          <label className="text-xs font-semibold text-gray-500 mb-1 block">Jawaban Benar</label>
          <select value={editSoalForm.jawaban_benar || ''} onChange={e => setEditSoalForm({...editSoalForm, jawaban_benar: e.target.value})}
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400">
            {['A','B','C','D','E'].map(op => <option key={op} value={op}>{op}</option>)}
          </select>
        </div>
        <div>
          <label className="text-xs font-semibold text-gray-500 mb-1 block">Pembahasan</label>
          <textarea rows={3} value={editSoalForm.pembahasan || ''} onChange={e => setEditSoalForm({...editSoalForm, pembahasan: e.target.value})}
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-400"/>
        </div>
        <div className="flex gap-3 pt-2">
          <button onClick={handleSaveSoalPendalaman}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg text-sm font-semibold transition">
            Simpan Perubahan
          </button>
          <button onClick={() => setShowEditSoal(false)}
            className="border border-gray-200 text-gray-600 px-4 py-2 rounded-lg text-sm transition">
            Batal
          </button>
        </div>
      </div>
    </div>
  </div>
)}
        </main>

        <footer className="text-center text-xs text-gray-400 py-4 border-t border-gray-100">
          © 2025 OSNGeo.id — Panel Admin
        </footer>
      </div>
    </div>
  )
}