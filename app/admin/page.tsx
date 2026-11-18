'use client'
import Link from 'next/link'
import { useEffect, useRef, useState } from 'react'
import { ClipboardList, FileText, Images, LayoutDashboard, Layers3, LogOut, Megaphone, Menu, Receipt, ShieldCheck, Ticket, UserRound, Users, Video, X } from 'lucide-react'
import { Brand, PageLoading } from '../components/atlas'
import { accessLabels, membershipExpiry, membershipFeatures, requiredAccess, rupiah, type MembershipPlan } from '../lib/membership'
import { supabase } from '../lib/supabase'
import { getYouTubeVideoId } from '../lib/youtube'
import { tryoutLevel, tryoutLevelLabels, tryoutLevelOptions, type TryoutLevelFilter } from '../lib/tryout-levels'
import { predictionYear, tryoutCategories, tryoutCategory, tryoutCategoryLabel, tryoutCategoryLabels, type TryoutCategoryFilter } from '../lib/tryout-catalog'
import { LandingVideoSettings } from './landing-videos'
import { loadStudentOverview, type StudentProfile } from './student-data'
import { StudentRoster } from './students'

type View =
  | 'dashboard' | 'siswa'
  | 'paket_tryout' | 'soal_tryout'
  | 'pendalaman' | 'soal_pendalaman'
  | 'video' | 'modul'
  | 'membership' | 'transaksi'
  | 'pengumuman' | 'banner' | 'video_beranda'

const accessOptions = Object.entries(accessLabels).map(([value, label]) => ({ value, label }))
const mediaAccessOptions = accessOptions.filter(({ value }) => value !== 'premium')
const accessBadge = {
  Gratis: 'bg-green-100 text-green-700',
  Premium: 'bg-yellow-100 text-yellow-700',
  Platinum: 'bg-purple-100 text-purple-700',
}

export default function AdminPage() {
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState<View>('dashboard')
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [packageQuery, setPackageQuery] = useState('')
  const [packageLevel, setPackageLevel] = useState<TryoutLevelFilter>('semua')
  const [packageCategory, setPackageCategory] = useState<TryoutCategoryFilter>('semua')

  // Stats
  const [stats, setStats] = useState<Awaited<ReturnType<typeof loadStudentOverview>> & {
    totalTO: number | null; rataRata: number | null; totalTransaksi: number | null
  }>({ total: null, registered: null, premium: null, platinum: null, submissions: null,
    totalTO: null, rataRata: null, totalTransaksi: null })
  const [studentRevision, setStudentRevision] = useState(0)

  // Data lists
  const [hasil, setHasil] = useState<any[]>([])
  const [paketTO, setPaketTO] = useState<any[]>([])
  const [soalTO, setSoalTO] = useState<any[]>([])
  const [soalTryoutError, setSoalTryoutError] = useState('')
  const [topikList, setTopikList] = useState<any[]>([])
  const [paketPendalaman, setPaketPendalaman] = useState<any[]>([])
  const [soalPendalaman, setSoalPendalaman] = useState<any[]>([])
  const [videoList, setVideoList] = useState<any[]>([])
  const [modulList, setModulList] = useState<any[]>([])
  const [membershipList, setMembershipList] = useState<MembershipPlan[]>([])
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
const [editSoalError, setEditSoalError] = useState('')
const [savingSoal, setSavingSoal] = useState(false)
const paketFormRef = useRef<HTMLDivElement>(null)
const [showEditUser, setShowEditUser] = useState(false)
const [editUserData, setEditUserData] = useState<StudentProfile | null>(null)
const [editUserForm, setEditUserForm] = useState({ nama: '', role: 'siswa', planId: '' })
const [savingUser, setSavingUser] = useState(false)

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

  useEffect(() => {
    if (view === 'paket_tryout' && showForm && editData) {
      paketFormRef.current?.scrollIntoView({ block: 'start' })
      paketFormRef.current?.focus({ preventScroll: true })
    }
  }, [view, showForm, editData])

  const loadAll = async () => {
    const [
      studentOverview, { data: h, count: totalTO }, { data: pt }, { data: tp },
      { data: pp }, { data: v }, { data: m }, { data: mb },
      { data: tr, count: totalTransaksi }, { data: pg }, { data: bn }
    ] = await Promise.all([
      loadStudentOverview(),
      supabase.from('hasil_to').select('*, profiles(nama), paket_to(nama)', { count: 'exact' })
        .order('created_at', { ascending: false }).limit(50),
      supabase.from('paket_to').select('*').order('urutan'),
      supabase.from('topik_materi').select('*').order('urutan'),
      supabase.from('paket_pendalaman').select('*, topik_materi(nama)').order('id'),
      supabase.from('video_pembelajaran').select('*, topik_materi(nama)').order('urutan'),
      supabase.from('modul_materi').select('*, topik_materi(nama)').order('id'),
      supabase.from('paket_membership').select('*').order('id'),
      supabase.from('transaksi').select('*, profiles(nama), paket_membership(nama)', { count: 'exact' }).order('created_at', { ascending: false }),
      supabase.from('pengumuman').select('*').order('created_at', { ascending: false }),
      supabase.from('banner').select('*').order('id'),
    ])
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
    const rataRata = h?.length ? Math.round(h.reduce((total, row) => total + row.total_poin, 0) / h.length) : null
    setStats({ ...studentOverview, totalTO, rataRata, totalTransaksi })
  }

  const loadSoalTO = async (paketId: number) => {
    const { data, error } = await supabase.from('soal').select('*').eq('paket_id', paketId).order('id')
    setSoalTO(data ?? [])
    setSoalTryoutError(error ? 'Soal gagal dimuat. Buka kembali paket untuk mencoba lagi.' : '')
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
    const { error } = editData
      ? await supabase.from(table).update(data).eq('id', editData.id)
      : await supabase.from(table).insert(data)
    if (error) {
      alert('Data gagal disimpan. Periksa isian dan coba lagi.')
      return
    }
    await loadAll()
    setShowForm(false)
    setEditData(null)
    setFormData({})
  }

  const resetForm = () => { setShowForm(false); setEditData(null); setFormData({}) }

  const closeSoalEditor = () => {
    setShowEditSoal(false)
    setEditSoalData(null)
    setEditSoalForm({})
    setEditSoalError('')
  }

  const handleSaveSoal = async () => {
    if (!selectedPaket || !editSoalData || savingSoal) return
    setSavingSoal(true)
    setEditSoalError('')
    try {
      const { data, error } = await supabase.from('soal').update({
        pertanyaan: editSoalForm.pertanyaan,
        gambar_url: editSoalForm.gambar_url || null,
        pilihan_a: editSoalForm.pilihan_a,
        pilihan_b: editSoalForm.pilihan_b,
        pilihan_c: editSoalForm.pilihan_c,
        pilihan_d: editSoalForm.pilihan_d,
        pilihan_e: editSoalForm.pilihan_e,
        jawaban_benar: editSoalForm.jawaban_benar,
        pembahasan: editSoalForm.pembahasan,
      }).eq('id', editSoalData.id).eq('paket_id', selectedPaket.id).select('id').maybeSingle()

      if (error || !data) {
        setEditSoalError(error?.message || 'Perubahan belum tersimpan. Buka kembali soal dan coba lagi.')
        return
      }
      await loadSoalTO(selectedPaket.id)
      closeSoalEditor()
    } catch {
      setEditSoalError('Koneksi terganggu saat menyimpan soal. Coba lagi.')
    } finally {
      setSavingSoal(false)
    }
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
  if (!editUserData || savingUser) return
  const updateData: Partial<StudentProfile> = { nama: editUserForm.nama, role: editUserForm.role }
  const planId = editUserForm.planId
  if (planId === 'gratis') {
    updateData.status = 'gratis'
    updateData.status_expired = null
  } else if (planId) {
    const plan = membershipList.find(item => item.id === Number(planId))
    if (!plan || plan.akses === 'gratis' || !plan.durasi_hari || plan.durasi_hari < 1) {
      alert('Pilih paket berbayar dengan durasi yang valid.')
      return
    }
    const now = Date.now()
    const currentExpiry = editUserData.status_expired ? membershipExpiry(editUserData.status_expired) : NaN
    const start = plan.akses === editUserData.status && currentExpiry > now ? currentExpiry : now
    updateData.status = plan.akses
    updateData.status_expired = new Date(start + plan.durasi_hari * 86_400_000).toISOString()
  }

  setSavingUser(true)
  try {
    let update = supabase.from('profiles').update(updateData).eq('id', editUserData.id)
    if (planId) {
      const { status, status_expired: expiry } = editUserData
      update = status === null ? update.is('status', null) : update.eq('status', status)
      update = expiry === null ? update.is('status_expired', null) : update.eq('status_expired', expiry)
    }
    const { data, error } = await update.select('id').maybeSingle()
    if (error || !data) {
      alert('Perubahan data siswa gagal disimpan. Muat ulang data siswa lalu coba lagi.')
      return
    }
    await loadAll()
    setStudentRevision(value => value + 1)
    setShowEditUser(false)
    setEditUserData(null)
  } finally {
    setSavingUser(false)
  }
}

const handleResetPassword = async (email: string) => {
  const { error } = await supabase.auth.resetPasswordForEmail(email, {
    redirectTo: `${window.location.origin}/reset-password`,
  })
  if (error) alert('Gagal kirim email reset.')
  else alert(`Email reset password sudah dikirim ke ${email}`)
}

  const openAdd = () => { setEditData(null); setFormData({}); setShowForm(true) }

  const navTo = (view: View) => {
    setView(view)
    resetForm()
    setSelectedPaket(null)
    setSelectedTopik(null)
    setSelectedPaketPendalaman(null)
    setDrawerOpen(false)
    window.scrollTo({ top: 0, behavior: 'auto' })
  }

  if (loading) return <PageLoading>Memuat panel admin…</PageLoading>

  const menuGroups = [
    { group: 'Manajemen', items: [
      { label: 'Dashboard', key: 'dashboard', Icon: LayoutDashboard },
      { label: 'Data siswa', key: 'siswa', Icon: Users },
    ] },
    { group: 'Ujian', items: [
      { label: 'Paket tryout', key: 'paket_tryout', Icon: ClipboardList },
      { label: 'Pendalaman materi', key: 'pendalaman', Icon: Layers3 },
    ] },
    { group: 'Materi', items: [
      { label: 'Video pembelajaran', key: 'video', Icon: Video },
      { label: 'Modul / PDF', key: 'modul', Icon: FileText },
    ] },
    { group: 'Transaksi', items: [
      { label: 'Paket membership', key: 'membership', Icon: Ticket },
      { label: 'Daftar transaksi', key: 'transaksi', Icon: Receipt },
    ] },
    { group: 'Publikasi', items: [
      { label: 'Video beranda', key: 'video_beranda', Icon: Video },
      { label: 'Pengumuman', key: 'pengumuman', Icon: Megaphone },
      { label: 'Banner', key: 'banner', Icon: Images },
    ] },
  ] as const

  const activeKey = ['soal_tryout'].includes(view) ? 'paket_tryout'
    : ['soal_pendalaman'].includes(view) ? 'pendalaman'
    : view
  const packageSearch = packageQuery.trim().toLowerCase()
  const visiblePackages = paketTO.filter(paket =>
    (packageLevel === 'semua' || tryoutLevel(paket.jenis) === packageLevel) &&
    (packageCategory === 'semua' || tryoutCategory(paket.kategori) === packageCategory) &&
    String(paket.nama).toLowerCase().includes(packageSearch))

  // Input field helpers
  const inp = (placeholder: string, key: string, type = 'text') => (
    <input type={type} placeholder={placeholder} value={formData[key] ?? ''}
      onChange={e => setFormData({ ...formData, [key]: type === 'number' ? Number(e.target.value) : e.target.value })}
      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400" />
  )
  const ta = (placeholder: string, key: string, rows = 3) => (
    <textarea placeholder={placeholder} rows={rows} value={formData[key] || ''}
      onChange={e => setFormData({ ...formData, [key]: e.target.value })}
      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400" />
  )
  const sel = (key: string, opts: { value: any, label: string }[], placeholder = 'Pilih...') => (
    <select value={formData[key] ?? ''} onChange={e => setFormData({ ...formData, [key]: e.target.value })}
      className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400">
      <option value="">{placeholder}</option>
      {opts.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
    </select>
  )

  const FormBtns = ({ onSave }: { onSave: () => void }) => (
    <div className="flex gap-3 pt-2">
      <button onClick={onSave} className="bg-forest-600 hover:bg-forest-700 text-white px-5 py-2 rounded-lg text-sm font-semibold transition">Simpan</button>
      <button onClick={resetForm} className="border border-gray-200 text-gray-600 px-4 py-2 rounded-lg text-sm transition">Batal</button>
    </div>
  )

  const Th = ({ children }: { children: any }) => (
    <th scope="col" className="text-left px-5 py-3 text-gray-500 font-semibold text-xs">{children}</th>
  )
  const ThC = ({ children }: { children: any }) => (
    <th scope="col" className="text-center px-5 py-3 text-gray-500 font-semibold text-xs">{children}</th>
  )

  const Badge = ({ v, map }: { v: string, map: Record<string, string> }) => {
    const cls = map[v] || 'bg-gray-100 text-gray-600'
    return <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${cls}`}>{v}</span>
  }

  return (
    <div className="atlas-admin-shell" data-collapsed={sidebarCollapsed} data-drawer={drawerOpen}
      onKeyDown={event => { if (event.key === 'Escape' && drawerOpen) setDrawerOpen(false) }}>
      {drawerOpen && (
        <button type="button" className="atlas-admin-overlay" onClick={() => setDrawerOpen(false)} aria-label="Tutup menu admin" />
      )}
      <aside className="atlas-admin-sidebar" id="admin-sidebar">
        <div className="flex min-h-[4.25rem] shrink-0 items-center gap-2 border-b border-gray-200 px-4">
          <Brand />
          <button type="button" className="atlas-admin-mobile-toggle ml-auto rounded-md p-2 text-gray-600 hover:bg-gray-100"
            onClick={() => setDrawerOpen(false)} aria-label="Tutup navigasi">
            <X size={18} aria-hidden="true" />
          </button>
        </div>
        <nav className="flex-1 overflow-y-auto px-3 py-4" aria-label="Navigasi admin">
          {menuGroups.map(group => (
            <div key={group.group} className="mb-4">
              <p className="mb-1 px-2 text-xs font-semibold text-gray-500">{group.group}</p>
              {group.items.map(({ key, label, Icon }) => (
                <button key={key} type="button" onClick={() => navTo(key)} aria-current={activeKey === key ? 'page' : undefined}
                  className={'mb-0.5 flex w-full items-center gap-2.5 rounded-lg px-2.5 py-2.5 text-left text-sm font-semibold ' +
                    (activeKey === key ? 'bg-forest-100 text-forest-800' : 'text-gray-600 hover:bg-gray-100')}>
                  <Icon size={17} className="shrink-0" aria-hidden="true" /> {label}
                </button>
              ))}
            </div>
          ))}
          <Link href="/dashboard" className="mt-3 flex items-center gap-2.5 border-t border-gray-200 px-2.5 py-3 text-sm font-semibold text-gray-600">
            <UserRound size={17} aria-hidden="true" /> Dashboard siswa
          </Link>
        </nav>
        <div className="border-t border-gray-200 p-3">
          <button type="button" onClick={async () => { await supabase.auth.signOut(); window.location.href = '/login' }}
            className="atlas-button w-full justify-start">
            <LogOut size={17} aria-hidden="true" /> Keluar akun
          </button>
        </div>
      </aside>

      <div className="min-w-0">
        <header className="atlas-topbar">
          <div className="atlas-topbar-inner atlas-admin-head">
            <div className="flex items-center gap-3">
              <button type="button" className="atlas-button atlas-admin-mobile-toggle"
                aria-label="Buka menu admin" aria-controls="admin-sidebar" aria-expanded={drawerOpen}
                onClick={() => setDrawerOpen(true)}><Menu size={18} aria-hidden="true" /></button>
              <button type="button" className="atlas-button atlas-admin-desktop-toggle"
                aria-label={sidebarCollapsed ? 'Tampilkan menu admin' : 'Sembunyikan menu admin'}
                aria-controls="admin-sidebar" aria-expanded={!sidebarCollapsed}
                onClick={() => setSidebarCollapsed(!sidebarCollapsed)}><Menu size={18} aria-hidden="true" /></button>
              <h1 className="font-bold">Panel admin</h1>
            </div>
            <span className="inline-flex items-center gap-1.5 rounded-full bg-forest-100 px-2.5 py-1.5 text-xs font-semibold text-forest-800">
              <ShieldCheck size={14} aria-hidden="true" /> Administrator
            </span>
          </div>
        </header>

        <main className="atlas-admin-content atlas-work-content">
          {/* ── DASHBOARD ─────────────────────────────────────────── */}
          {view === 'dashboard' && (
            <div>
              <div className="mb-5">
                <h2 className="text-xl font-black text-gray-800">Dashboard Admin</h2>
                <p className="text-gray-500 text-sm">Ringkasan aktivitas OSNGeo.id</p>
              </div>
              {[
                [
                  { label: 'Total siswa', value: stats.total },
                  { label: 'Pendaftar 7 hari', value: stats.registered },
                  { label: 'Premium aktif', value: stats.premium },
                  { label: 'Platinum aktif', value: stats.platinum },
                ],
                [
                  { label: 'Total pengerjaan tryout', value: stats.totalTO },
                  { label: 'Pengerjaan tryout 7 hari', value: stats.submissions },
                  { label: 'Rata-rata poin (50 terakhir)', value: stats.rataRata },
                  { label: 'Total transaksi', value: stats.totalTransaksi },
                ],
              ].map(group => (
                <dl key={group[0].label} className="atlas-stat-strip mb-6">
                  {group.map(({ label, value }) => (
                    <div key={label}><dt>{label}</dt><dd>{value?.toLocaleString('id-ID') ?? '—'}</dd></div>
                  ))}
                </dl>
              ))}
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
                      <div className={`text-xl font-black ${h.total_poin >= 0 ? 'text-forest-600' : 'text-red-500'}`}>{h.total_poin}</div>
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
              <StudentRoster revision={studentRevision} onEdit={student => {
                setEditUserData(student)
                setEditUserForm({ nama: student.nama || '', role: student.role || 'siswa', planId: '' })
                setShowEditUser(true)
              }} />

              {/* MODAL EDIT USER */}
              {showEditUser && editUserData && (
                <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
                  <div className="max-h-[90svh] w-full max-w-md overflow-y-auto rounded-2xl bg-white p-6 shadow-xl">
                    <div className="flex items-center justify-between mb-5">
                      <h3 className="font-black text-gray-800">Edit User</h3>
                      <button disabled={savingUser} aria-label="Tutup edit siswa" onClick={() => setShowEditUser(false)}
                        className="text-gray-400 hover:text-gray-700 text-xl">✕</button>
                    </div>
                    <div className="flex flex-col gap-3">
                      <div>
                        <label className="text-xs font-semibold text-gray-500 mb-1 block">Nama</label>
                        <input value={editUserForm.nama || ''} onChange={e => setEditUserForm({...editUserForm, nama: e.target.value})}
                          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400"/>
                      </div>
                      <dl className="grid gap-3 rounded-lg bg-gray-50 p-3 text-sm sm:grid-cols-2">
                        <div className="sm:col-span-2">
                          <dt className="text-xs font-semibold text-gray-500">Email</dt>
                          <dd className="mt-1 break-all">{editUserData.email || '—'}</dd>
                        </div>
                        <div>
                          <dt className="text-xs font-semibold text-gray-500">Asal provinsi</dt>
                          <dd className="mt-1">{editUserData.provinsi || '—'}</dd>
                        </div>
                        <div>
                          <dt className="text-xs font-semibold text-gray-500">Nomor HP</dt>
                          <dd className="mt-1 tabular-nums">{editUserData.nomor_hp || '—'}</dd>
                        </div>
                      </dl>
                      <div>
                        <label className="text-xs font-semibold text-gray-500 mb-1 block">Role</label>
                        <select value={editUserForm.role || 'siswa'} onChange={e => setEditUserForm({...editUserForm, role: e.target.value})}
                          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400">
                          <option value="siswa">Siswa</option>
                          <option value="admin">Admin</option>
                        </select>
                      </div>
                      <div>
                        <label htmlFor="student-plan" className="text-xs font-semibold text-gray-500 mb-1 block">Paket yang diaktifkan</label>
                        <select id="student-plan" disabled={savingUser} value={editUserForm.planId} onChange={e => setEditUserForm({...editUserForm, planId: e.target.value})}
                          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400">
                          <option value="">Pertahankan akses saat ini</option>
                          <option value="gratis">Gratis</option>
                          {membershipList.filter(plan => plan.akses !== 'gratis' && (plan.durasi_hari ?? 0) > 0).map(plan => (
                            <option key={plan.id} value={plan.id}>{plan.nama} · {plan.durasi_hari} hari</option>
                          ))}
                        </select>
                        <p className="mt-2 text-xs text-gray-600">Pilih paket setelah pembayaran diverifikasi via WhatsApp. Memilih tingkat yang sama akan memperpanjang akses yang masih aktif.</p>
                      </div>
                      <div className="flex gap-3 pt-2">
                        <button disabled={savingUser} onClick={handleSaveUser}
                          className="flex-1 bg-forest-600 hover:bg-forest-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition disabled:opacity-50">
                          {savingUser ? 'Menyimpan…' : 'Simpan'}
                        </button>
                        <button disabled={!editUserData.email} onClick={() => { if (editUserData.email) void handleResetPassword(editUserData.email) }}
                          className="flex-1 border border-gray-200 text-gray-600 px-4 py-2 rounded-lg text-sm hover:bg-gray-50 transition disabled:opacity-50">
                          Reset Password
                        </button>
                      </div>
                      <button disabled={savingUser} onClick={() => setShowEditUser(false)}
                        className="text-center text-gray-400 text-xs hover:text-gray-600 transition">
                        Batal
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {view === 'video_beranda' && <LandingVideoSettings />}

          {/* ── PAKET TRYOUT (list) ───────────────────────────────── */}
          {view === 'paket_tryout' && (
            <div>
              <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
                <div>
                  <h2 className="text-xl font-black text-gray-800">Paket Tryout</h2>
                  <p className="text-gray-500 text-sm" role="status">{visiblePackages.length} dari {paketTO.length} paket</p>
                </div>
                <button onClick={openAdd} className="atlas-button atlas-button--primary">
                  + Tambah Paket
                </button>
              </div>
              <div className="mb-4 grid max-w-3xl gap-3 sm:grid-cols-[2fr_1fr_1fr]">
                <label className="block text-sm font-semibold">
                  Cari paket
                  <input type="search" className="atlas-field mt-1.5 block" value={packageQuery}
                    onChange={event => setPackageQuery(event.target.value)} placeholder="Nama paket tryout" />
                </label>
                <label className="block text-sm font-semibold">
                  Jenjang
                  <select className="atlas-field mt-1.5 block" value={packageLevel}
                    onChange={event => setPackageLevel(event.target.value as TryoutLevelFilter)}>
                    <option value="semua">Semua jenjang</option>
                    {tryoutLevelOptions.map(jenjang => <option key={jenjang} value={jenjang}>{tryoutLevelLabels[jenjang]}</option>)}
                  </select>
                </label>
                <label className="block text-sm font-semibold">
                  Kategori
                  <select className="atlas-field mt-1.5 block" value={packageCategory}
                    onChange={event => setPackageCategory(event.target.value as TryoutCategoryFilter)}>
                    <option value="semua">Semua kategori</option>
                    {tryoutCategories.map(category => <option key={category} value={category}>{tryoutCategoryLabels[category]}</option>)}
                  </select>
                </label>
              </div>

              {showForm && (
                <div ref={paketFormRef} tabIndex={-1} className="mb-5 scroll-mt-24 rounded-xl border border-gray-200 bg-white p-5">
                  <h3 className="mb-4 font-bold text-gray-800">{editData ? 'Edit Paket' : 'Tambah Paket Baru'}</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {inp('Nama paket (contoh: OSN-K Paket 1)', 'nama')}
                    {sel('jenis', [
                      { value: 'OSNK', label: 'OSN-K (Kabupaten/Kota)' },
                      { value: 'OSNP', label: 'OSN-P (Provinsi)' },
                      { value: 'Nasional', label: 'OSN Nasional' },
                    ], 'Pilih Jenis')}
                    <label className="block text-xs font-semibold">Kategori tryout
                      <select className="atlas-field mt-1 block" value={tryoutCategory(formData.kategori)}
                        onChange={event => setFormData({ ...formData, kategori: event.target.value })}>
                        {tryoutCategories.map(category => <option key={category} value={category}>{tryoutCategoryLabels[category]}</option>)}
                      </select>
                    </label>
                    <label className="block text-xs font-semibold">Tahun
                      {inp(`Contoh: ${predictionYear}`, 'tahun', 'number')}
                    </label>
                    {inp('Durasi (menit)', 'durasi_menit', 'number')}
                    {sel('status', [{ value: 'aktif', label: 'Aktif' }, { value: 'nonaktif', label: 'Nonaktif' }], 'Status')}
                    {sel('akses', accessOptions, 'Tipe akses (Gratis)')}
                    <div className="md:col-span-2">{inp('Deskripsi singkat (opsional)', 'deskripsi')}</div>
                  </div>
                  <div className="mt-3">
                    <FormBtns onSave={() => handleSave('paket_to', {
                      nama: formData.nama,
                      jenis: formData.jenis,
                      kategori: tryoutCategory(formData.kategori),
                      tahun: formData.tahun || (formData.kategori === 'prediksi' ? predictionYear : null),
                      durasi_menit: formData.durasi_menit || 120,
                      status: formData.status || 'aktif',
                      aktif: formData.status !== 'nonaktif',
                      akses: formData.akses || 'gratis',
                      is_premium: Boolean(formData.akses && formData.akses !== 'gratis'),
                      deskripsi: formData.deskripsi || null,
                      ...(editData ? {} : { urutan: Math.max(0, ...paketTO.map(p => Number(p.urutan) || 0)) + 1 }),
                    })} />
                  </div>
                </div>
              )}

              <div className="bg-white border border-gray-200 rounded-xl atlas-table-scroll">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 bg-gray-50">
                      <Th>Nama Paket</Th><Th>Jenjang</Th><Th>Kategori</Th><Th>Tahun</Th>
                      <ThC>Durasi</ThC><ThC>Tipe</ThC><ThC>Status</ThC><ThC>Aksi</ThC>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {visiblePackages.map(p => (
                      <tr key={p.id} className="hover:bg-gray-50">
                        <td className="px-5 py-3 font-medium text-gray-800">{p.nama}</td>
                        <td className="px-5 py-3 text-gray-500 text-xs">{tryoutLevelLabels[tryoutLevel(p.jenis)]}</td>
                        <td className="px-5 py-3 text-gray-500 text-xs">{tryoutCategoryLabel(p)}</td>
                        <td className="px-5 py-3 text-gray-500 text-xs">{p.tahun || '—'}</td>
                        <td className="px-5 py-3 text-center text-gray-500 text-xs">{p.durasi_menit} mnt</td>
                        <td className="px-5 py-3 text-center">
                          <Badge v={accessLabels[requiredAccess(p)]} map={accessBadge} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          <Badge v={p.status || 'aktif'} map={{ aktif: 'bg-forest-100 text-forest-700', nonaktif: 'bg-gray-100 text-gray-500' }} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          <div className="flex items-center justify-center gap-2">
                            <button onClick={async () => {
                              await loadSoalTO(p.id)
                              resetForm()
                              closeSoalEditor()
                              setSelectedPaket(p)
                              setView('soal_tryout')
                              window.scrollTo({ top: 0, behavior: 'auto' })
                            }} className="text-xs bg-forest-600 hover:bg-forest-700 text-white px-3 py-1 rounded transition">
                              Kelola Soal
                            </button>
                            <button onClick={() => {
                              setEditData({ ...p })
                              setFormData({
                                nama: p.nama,
                                jenis: p.jenis,
                                kategori: p.kategori,
                                tahun: p.tahun,
                                durasi_menit: p.durasi_menit,
                                status: p.status,
                                akses: requiredAccess(p),
                                deskripsi: p.deskripsi,
                              })
                              setShowForm(true)
                            }} className="text-xs text-forest-600 border border-forest-200 px-2 py-1 rounded transition">
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
                    {visiblePackages.length === 0 && (
                      <tr><td colSpan={8} className="px-5 py-8 text-center text-gray-500 text-sm">
                        {paketTO.length ? 'Tidak ada paket yang cocok dengan filter.' : 'Belum ada paket tryout.'}
                      </td></tr>
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
                  className="text-forest-600 hover:underline font-medium">Paket Tryout</button>
                <span className="text-gray-400">›</span>
                <span className="font-bold text-gray-800">{selectedPaket.nama}</span>
              </div>

              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-black text-gray-800">{selectedPaket.nama}</h2>
                  <p className="text-gray-500 text-sm">{soalTO.length} soal · {selectedPaket.jenis} · {selectedPaket.durasi_menit} menit</p>
                </div>
                <button onClick={openAdd} className="bg-forest-600 hover:bg-forest-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">
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
                          className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400"/>
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
                    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                      {sel('jawaban_benar', ['A','B','C','D','E'].map(x => ({ value: x, label: x })), 'Jawaban Benar')}
                      <p className="self-center text-sm text-gray-600">Akses paket {accessLabels[requiredAccess(selectedPaket)]}</p>
                    </div>
                    {ta('Tulis pembahasan jawaban...', 'pembahasan', 2)}
                    <FormBtns onSave={async () => {
                      const akses = requiredAccess(selectedPaket)
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
                        akses,
                        is_premium: akses !== 'gratis',
                      })
                      await loadSoalTO(selectedPaket.id)
                    }} />
                  </div>
                </div>
              )}

              <div className="bg-white border border-gray-200 rounded-xl atlas-table-scroll">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 bg-gray-50">
                      <Th>No</Th><Th>Pertanyaan</Th><ThC>Jwb</ThC><ThC>Gambar</ThC><ThC>Tipe</ThC><ThC>Aksi</ThC>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {soalTO.map((s, i) => (
                      <tr key={s.id} className="hover:bg-gray-50">
                        <td className="px-5 py-3 text-gray-400 text-xs">{i + 1}</td>
                        <td className="px-5 py-3 text-gray-800 max-w-xs"><p className="truncate">{s.pertanyaan}</p></td>
                        <td className="px-5 py-3 text-center">
                          <span className="bg-green-100 text-green-700 text-xs font-bold px-2 py-0.5 rounded">{s.jawaban_benar}</span>
                        </td>
                        <td className="px-5 py-3 text-center">
                          {s.gambar_url ? <span className="text-xs bg-forest-100 text-forest-600 px-2 py-0.5 rounded">Ada</span> : <span className="text-xs text-gray-300">—</span>}
                        </td>
                        <td className="px-5 py-3 text-center">
                          <Badge v={accessLabels[requiredAccess(selectedPaket)]} map={accessBadge} />
                        </td>
                        <td className="px-5 py-3 text-center">
  <div className="flex items-center justify-center gap-2">
    <button onClick={() => {
      setEditSoalError('')
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
    }} className="text-xs text-forest-600 border border-forest-200 px-2 py-1 rounded transition">
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
                      <tr><td colSpan={6} className="px-5 py-8 text-center text-sm text-gray-600">
                        {soalTryoutError ? <span role="alert" className="text-red-700">{soalTryoutError}</span> : 'Belum ada soal. Klik + Tambah Soal untuk mulai.'}
                      </td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* MODAL EDIT SOAL TO */}
{view === 'soal_tryout' && selectedPaket && showEditSoal && editSoalData && (
  <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
    <div role="dialog" aria-modal="true" aria-labelledby="edit-soal-tryout-title" className="bg-white rounded-2xl p-6 max-w-2xl w-full shadow-xl max-h-[90vh] overflow-y-auto">
      <div className="flex items-center justify-between mb-5">
        <h3 id="edit-soal-tryout-title" className="font-black text-gray-800">Edit Soal #{editSoalData.id}</h3>
        <button onClick={closeSoalEditor} disabled={savingSoal} aria-label="Tutup edit soal"
          className="text-gray-400 hover:text-gray-700 text-xl">✕</button>
      </div>
      <div className="flex flex-col gap-3">
        <div>
          <label htmlFor="edit-soal-tryout-pertanyaan" className="text-xs font-semibold text-gray-500 mb-1 block">Pertanyaan</label>
          <textarea id="edit-soal-tryout-pertanyaan" rows={4} value={editSoalForm.pertanyaan || ''} onChange={e => setEditSoalForm({...editSoalForm, pertanyaan: e.target.value})}
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400"/>
        </div>
        <div>
          <label className="text-xs font-semibold text-gray-500 mb-1 block">Gambar Soal (opsional)</label>
          <div className="flex gap-2">
            <input placeholder="URL gambar atau upload" value={editSoalForm.gambar_url || ''}
              onChange={e => setEditSoalForm({...editSoalForm, gambar_url: e.target.value})}
              className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400"/>
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
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400"/>
            </div>
          ))}
        </div>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div>
            <label className="text-xs font-semibold text-gray-500 mb-1 block">Jawaban Benar</label>
            <select value={editSoalForm.jawaban_benar || ''} onChange={e => setEditSoalForm({...editSoalForm, jawaban_benar: e.target.value})}
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400">
              {['A','B','C','D','E'].map(op => <option key={op} value={op}>{op}</option>)}
            </select>
          </div>
          <p className="self-center text-sm text-gray-600">Akses paket {accessLabels[requiredAccess(selectedPaket)]}</p>
        </div>
        <div>
          <label className="text-xs font-semibold text-gray-500 mb-1 block">Pembahasan</label>
          <textarea rows={3} value={editSoalForm.pembahasan || ''} onChange={e => setEditSoalForm({...editSoalForm, pembahasan: e.target.value})}
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400"/>
        </div>
        {editSoalError && <p role="alert" className="text-sm font-semibold text-red-700">{editSoalError}</p>}
        <div className="flex gap-3 pt-2">
          <button onClick={handleSaveSoal} disabled={savingSoal}
            className="bg-forest-600 hover:bg-forest-700 text-white px-5 py-2 rounded-lg text-sm font-semibold transition disabled:opacity-60">
            {savingSoal ? 'Menyimpan…' : 'Simpan Perubahan'}
          </button>
          <button onClick={closeSoalEditor} disabled={savingSoal}
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
                      className="bg-white border border-gray-200 rounded-xl p-4 text-left hover:border-forest-400 hover:shadow-sm transition">
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
                  className="text-forest-600 hover:underline font-medium">Pendalaman Materi</button>
                <span className="text-gray-400">›</span>
                <span className="font-bold text-gray-800">{selectedTopik.nama}</span>
              </div>

              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-black text-gray-800">{selectedTopik.nama}</h2>
                  <p className="text-gray-500 text-sm">Paket pendalaman untuk topik ini</p>
                </div>
                <button onClick={openAdd} className="bg-forest-600 hover:bg-forest-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">
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
                    {sel('akses', accessOptions, 'Tipe akses (Gratis)')}
                    <div className="md:col-span-2">{inp('Deskripsi (opsional)', 'deskripsi')}</div>
                  </div>
                  <div className="mt-3">
                    <FormBtns onSave={() => handleSave('paket_pendalaman', {
                      topik_id: selectedTopik.id,
                      nama: formData.nama,
                      durasi_menit: formData.durasi_menit || 60,
                      status: formData.status || 'aktif',
                      akses: formData.akses || 'gratis',
                      is_premium: Boolean(formData.akses && formData.akses !== 'gratis'),
                      deskripsi: formData.deskripsi || null,
                    })} />
                  </div>
                </div>
              )}

              <div className="bg-white border border-gray-200 rounded-xl atlas-table-scroll">
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
                          <Badge v={accessLabels[requiredAccess(p)]} map={accessBadge} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          <Badge v={p.status || 'aktif'} map={{ aktif: 'bg-forest-100 text-forest-700', nonaktif: 'bg-gray-100 text-gray-500' }} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          <div className="flex items-center justify-center gap-2">
                            <button onClick={async () => {
                              setSelectedPaketPendalaman(p)
                              await loadSoalPendalaman(p.id)
                              resetForm()
                            }} className="text-xs bg-forest-600 hover:bg-forest-700 text-white px-3 py-1 rounded transition">
                              Kelola Soal
                            </button>
                            <button onClick={() => {
                              setEditData(p)
                              setFormData({
                                nama: p.nama,
                                durasi_menit: p.durasi_menit,
                                status: p.status,
                                akses: requiredAccess(p),
                                deskripsi: p.deskripsi,
                              })
                              setShowForm(true)
                            }} className="text-xs text-forest-600 border border-forest-200 px-2 py-1 rounded transition">
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
                  className="text-forest-600 hover:underline font-medium">Pendalaman Materi</button>
                <span className="text-gray-400">›</span>
                <button onClick={() => { setSelectedPaketPendalaman(null); resetForm() }}
                  className="text-forest-600 hover:underline font-medium">{selectedTopik.nama}</button>
                <span className="text-gray-400">›</span>
                <span className="font-bold text-gray-800">{selectedPaketPendalaman.nama}</span>
              </div>

              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-black text-gray-800">{selectedPaketPendalaman.nama}</h2>
                  <p className="text-gray-500 text-sm">{soalPendalaman.length} soal · {selectedTopik.nama}</p>
                </div>
                <button onClick={openAdd} className="bg-forest-600 hover:bg-forest-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">
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
                          className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400"/>
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

              <div className="bg-white border border-gray-200 rounded-xl atlas-table-scroll">
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
                          {s.gambar_url ? <span className="text-xs bg-forest-100 text-forest-600 px-2 py-0.5 rounded">Ada</span> : <span className="text-xs text-gray-300">—</span>}
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
    }} className="text-xs text-forest-600 border border-forest-200 px-2 py-1 rounded transition">
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
                <button onClick={openAdd} className="bg-forest-600 hover:bg-forest-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">+ Tambah Video</button>
              </div>
              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">Tambah Video</h3>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 mb-3">
                    {inp('Judul video', 'judul')}
                    {inp('Tautan atau ID YouTube', 'youtube_id')}
                    {sel('topik_id', topikList.map(t => ({ value: t.id, label: t.nama })), 'Pilih topik (opsional)')}
                    {sel('akses', mediaAccessOptions, 'Tipe akses (Gratis)')}
                  </div>
                  <FormBtns onSave={() => {
                    const youtubeId = getYouTubeVideoId(formData.youtube_id)
                    const title = typeof formData.judul === 'string' ? formData.judul.trim() : ''
                    if (!title || !youtubeId) {
                      alert('Isi judul dan tempel tautan atau ID video YouTube yang valid.')
                      return
                    }

                    void handleSave('video_pembelajaran', {
                      judul: title,
                      youtube_id: youtubeId,
                      topik_id: formData.topik_id ? Number(formData.topik_id) : null,
                      akses: formData.akses || 'gratis',
                      is_premium: formData.akses === 'platinum',
                      urutan: videoList.length + 1,
                    })
                  }} />
                </div>
              )}
              <div className="bg-white border border-gray-200 rounded-xl atlas-table-scroll">
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
                          <Badge v={accessLabels[requiredAccess(v, true)]} map={accessBadge} />
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
                <button onClick={openAdd} className="bg-forest-600 hover:bg-forest-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">+ Tambah Modul</button>
              </div>
              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">Tambah Modul</h3>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 mb-3">
                    {inp('Judul modul', 'judul')}
                    {sel('topik_id', topikList.map(t => ({ value: t.id, label: t.nama })), 'Pilih Topik')}
                    <div className="col-span-2">{inp('URL File (Google Drive / langsung)', 'file_url')}</div>
                    {sel('akses', mediaAccessOptions, 'Tipe akses (Gratis)')}
                    {inp('Deskripsi (opsional)', 'deskripsi')}
                  </div>
                  <FormBtns onSave={() => handleSave('modul_materi', {
                    judul: formData.judul,
                    topik_id: Number(formData.topik_id),
                    file_url: formData.file_url,
                    akses: formData.akses || 'gratis',
                    is_premium: formData.akses === 'platinum',
                    deskripsi: formData.deskripsi || null,
                  })} />
                </div>
              )}
              <div className="bg-white border border-gray-200 rounded-xl atlas-table-scroll">
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
                          <Badge v={accessLabels[requiredAccess(m, true)]} map={accessBadge} />
                        </td>
                        <td className="px-5 py-3 text-center">
                          {m.jumlah_halaman ? (
                            <Link href={'/modul/' + m.id} target="_blank" rel="noreferrer"
                              className="text-xs text-forest-600 hover:underline">Baca modul</Link>
                          ) : m.file_url ? (
                            <a href={m.file_url} target="_blank" rel="noreferrer" className="text-xs text-forest-600 hover:underline">Buka</a>
                          ) : <span className="text-gray-300 text-xs">—</span>}
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
                <button onClick={openAdd} className="bg-forest-600 hover:bg-forest-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">+ Tambah Paket</button>
              </div>
              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">{editData ? 'Edit Paket Membership' : 'Tambah Paket Membership'}</h3>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 mb-3">
                    {inp('Nama paket', 'nama')}
                    {inp('Harga (Rp)', 'harga', 'number')}
                    {inp('Durasi (hari)', 'durasi_hari', 'number')}
                    {inp('Deskripsi singkat', 'deskripsi')}
                    {sel('akses', accessOptions, 'Tingkat akses (Gratis)')}
                    {sel('aktif', [{ value: 'true', label: 'Siap dipesan' }, { value: 'false', label: 'Dalam persiapan' }], 'Ketersediaan')}
                    <div className="col-span-2">{ta('Fitur (pisahkan dengan enter)', 'fitur', 3)}</div>
                  </div>
                  <FormBtns onSave={() => handleSave('paket_membership', {
                    nama: formData.nama,
                    harga: formData.harga ?? 0,
                    durasi_hari: formData.akses && formData.akses !== 'gratis' ? formData.durasi_hari || 30 : null,
                    deskripsi: formData.deskripsi,
                    fitur: membershipFeatures(formData.fitur).join('\n'),
                    akses: formData.akses || 'gratis',
                    aktif: formData.akses === 'gratis' || !formData.akses || formData.aktif === 'true',
                  })} />
                </div>
              )}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {membershipList.map(m => (
                  <div key={m.id} className="bg-white border border-gray-200 rounded-xl p-5">
                    <div className="font-black text-gray-800 mb-1">{m.nama}</div>
                    <div className="text-2xl font-black text-forest-600 mb-1">{rupiah(m.harga)}</div>
                    <p className="mb-3 text-xs text-gray-600">
                      {m.akses === 'gratis' ? 'Tanpa batas waktu' : `${m.durasi_hari} hari · ${m.aktif ? 'Siap dipesan' : 'Dalam persiapan'}`}
                    </p>
                    <div className="flex gap-2">
                      <button onClick={() => {
                        setEditData(m)
                        setFormData({
                          nama: m.nama,
                          harga: m.harga,
                          durasi_hari: m.durasi_hari,
                          deskripsi: m.deskripsi,
                          fitur: membershipFeatures(m.fitur).join('\n'),
                          akses: m.akses,
                          aktif: String(m.aktif === true),
                        })
                        setShowForm(true)
                      }} className="text-xs text-forest-600 border border-forest-200 px-3 py-1 rounded transition">Edit</button>
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
              <div className="bg-white border border-gray-200 rounded-xl atlas-table-scroll">
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
                            dibayar: 'bg-forest-100 text-forest-700',
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
                <button onClick={openAdd} className="bg-forest-600 hover:bg-forest-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">+ Tambah</button>
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
                <button onClick={openAdd} className="bg-forest-600 hover:bg-forest-700 text-white text-sm px-4 py-2 rounded-lg font-semibold transition">+ Tambah Banner</button>
              </div>
              {showForm && (
                <div className="bg-white border border-gray-200 rounded-xl p-5 mb-5">
                  <h3 className="font-bold text-gray-800 mb-4">Tambah Banner</h3>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 mb-3">
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
                        {b.link && <a href={b.link} target="_blank" rel="noreferrer" className="text-xs text-forest-500 hover:underline">{b.link}</a>}
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
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400"/>
        </div>
        <div>
          <label className="text-xs font-semibold text-gray-500 mb-1 block">Gambar Soal (opsional)</label>
          <div className="flex gap-2">
            <input placeholder="URL gambar atau upload" value={editSoalForm.gambar_url || ''}
              onChange={e => setEditSoalForm({...editSoalForm, gambar_url: e.target.value})}
              className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400"/>
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
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400"/>
            </div>
          ))}
        </div>
        <div>
          <label className="text-xs font-semibold text-gray-500 mb-1 block">Jawaban Benar</label>
          <select value={editSoalForm.jawaban_benar || ''} onChange={e => setEditSoalForm({...editSoalForm, jawaban_benar: e.target.value})}
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400">
            {['A','B','C','D','E'].map(op => <option key={op} value={op}>{op}</option>)}
          </select>
        </div>
        <div>
          <label className="text-xs font-semibold text-gray-500 mb-1 block">Pembahasan</label>
          <textarea rows={3} value={editSoalForm.pembahasan || ''} onChange={e => setEditSoalForm({...editSoalForm, pembahasan: e.target.value})}
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:border-forest-400"/>
        </div>
        <div className="flex gap-3 pt-2">
          <button onClick={handleSaveSoalPendalaman}
            className="bg-forest-600 hover:bg-forest-700 text-white px-5 py-2 rounded-lg text-sm font-semibold transition">
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
