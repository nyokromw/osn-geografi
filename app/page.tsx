'use client'
import { useEffect, useState } from 'react'
import { supabase } from './lib/supabase'

export default function Home() {
  const [paketMembership, setPaketMembership] = useState<any[]>([])
  const [pengumuman, setPengumuman] = useState<any[]>([])
  const [jumlahPaketGratis, setJumlahPaketGratis] = useState(0)
  const [jumlahVideo, setJumlahVideo] = useState(0)
  const [jumlahSoal, setJumlahSoal] = useState(0)
  const [jumlahPaket, setJumlahPaket] = useState(0)
  const [topikList, setTopikList] = useState<any[]>([])

  useEffect(() => {
    const load = async () => {
      const [
        { data: mb }, { data: pg }, { data: pt }, { data: v },
        { data: sq }, { data: tp }
      ] = await Promise.all([
        supabase.from('paket_membership').select('*').order('id'),
        supabase.from('pengumuman').select('*').eq('aktif', true).order('created_at', { ascending: false }).limit(3),
        supabase.from('paket_to').select('id').eq('status', 'aktif'),
        supabase.from('video_pembelajaran').select('id').eq('is_premium', false),
        supabase.from('soal').select('id'),
        supabase.from('topik_materi').select('*').order('urutan'),
      ])
      setPaketMembership(mb || [])
      setPengumuman(pg || [])
      setJumlahPaketGratis(pt?.filter((p: any) => !p.is_premium)?.length || 0)
      setJumlahVideo(v?.length || 0)
      setJumlahSoal(sq?.length || 0)
      setJumlahPaket(pt?.length || 0)
      setTopikList(tp || [])
    }
    load()
  }, [])

  const iconTopik: Record<string, string> = {
    'Geomorfologi': '🏔️',
    'Klimatologi': '🌦️',
    'Hidrologi': '💧',
    'Oseanografi': '🌊',
    'Kependudukan': '👥',
    'Geografi Ekonomi': '📈',
    'Penginderaan Jauh': '🛰️',
    'SIG': '🗺️',
    'Mitigasi Bencana': '🚨',
    'Geografi Regional': '🌏',
    'Kartografi': '📍',
    'Biogeografi': '🌿',
    'Geografi Budaya': '🏛️',
  }

  return (
    <main className="min-h-screen bg-white text-gray-900 font-sans">

      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-10 py-4 border-b border-gray-100 sticky top-0 z-50 bg-white">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-black text-white text-sm">G</div>
          <span className="font-black text-gray-800">OSN<span className="text-blue-600">Geo</span>.id</span>
        </div>
        <ul className="hidden md:flex gap-8 list-none text-sm text-gray-500">
          <li><a href="#kenapa" className="hover:text-gray-900 transition">Keunggulan</a></li>
          <li><a href="#topik" className="hover:text-gray-900 transition">Materi</a></li>
          <li><a href="#paket" className="hover:text-gray-900 transition">Paket</a></li>
          <li><a href="#gratis" className="hover:text-gray-900 transition">Gratis</a></li>
          {pengumuman.length > 0 && <li><a href="#pengumuman" className="hover:text-gray-900 transition">Pengumuman</a></li>}
        </ul>
        <div className="flex items-center gap-2">
          <a href="/login" className="text-sm text-gray-600 hover:text-gray-900 px-4 py-2 rounded-lg border border-gray-200 hover:border-gray-300 transition">
            Masuk
          </a>
          <a href="/register" className="text-sm bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition">
            Daftar
          </a>
        </div>
      </nav>

      {/* PENGUMUMAN TICKER */}
      {pengumuman.length > 0 && (
        <div className="bg-blue-600 text-white text-xs py-2 px-6 flex items-center gap-3">
          <span className="font-bold shrink-0 bg-white/20 px-2 py-0.5 rounded">📢 Info</span>
          <span className="truncate">{pengumuman[0].judul} — {pengumuman[0].isi}</span>
        </div>
      )}

      {/* HERO */}
      <section className="max-w-4xl mx-auto px-6 pt-20 pb-16 text-center">
        <div className="inline-block text-xs font-semibold text-blue-600 bg-blue-50 border border-blue-100 px-3 py-1 rounded-full mb-6">
          Platform Persiapan OSN Geografi Terlengkap di Indonesia
        </div>
        <h1 className="text-4xl md:text-6xl font-black leading-tight mb-5 text-gray-900">
          Juara OSN Geografi<br />
          <span className="text-blue-600">Dimulai dari Sini</span>
        </h1>
        <p className="text-gray-500 text-base max-w-xl mx-auto leading-relaxed mb-8">
          Latihan soal, tryout online, video pembahasan, dan bimbingan intensif untuk membantu siswa meraih prestasi terbaik di Olimpiade Sains Nasional Geografi.
        </p>
        <div className="flex gap-3 justify-center flex-wrap mb-6">
          <a href="/register" className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg text-sm font-semibold transition">
            Mulai Gratis
          </a>
          <a href="#paket" className="border border-gray-200 hover:border-gray-300 text-gray-600 px-6 py-2.5 rounded-lg text-sm transition">
            Lihat Paket
          </a>
        </div>

        {/* CHECKLIST */}
        <div className="flex flex-wrap justify-center gap-3 text-xs text-gray-500 mb-12">
          {[
            `${jumlahPaket > 0 ? jumlahPaket + '+' : '60+'} Paket Tryout`,
            `${jumlahSoal > 0 ? jumlahSoal.toLocaleString('id-ID') + '+' : '6.000+'} Soal Geografi`,
            'Sistem Penilaian Setara OSN',
            'Dashboard Kemajuan Belajar',
          ].map((t, i) => (
            <span key={i} className="flex items-center gap-1.5 bg-gray-50 border border-gray-100 px-3 py-1.5 rounded-full">
              <span className="text-green-500">✓</span>{t}
            </span>
          ))}
        </div>

        {/* STATS */}
        <div className="flex gap-8 md:gap-16 justify-center pt-10 border-t border-gray-100 flex-wrap">
          {[
            { value: jumlahPaket > 0 ? `${jumlahPaket}+` : '60+', label: 'Paket Tryout' },
            { value: jumlahSoal > 0 ? `${jumlahSoal.toLocaleString('id-ID')}+` : '6.000+', label: 'Soal OSN' },
            { value: topikList.length > 0 ? `${topikList.length}` : '13', label: 'Topik Materi' },
            { value: jumlahVideo > 0 ? `${jumlahVideo}+` : '10+', label: 'Video Gratis' },
          ].map((s, i) => (
            <div key={i} className="text-center">
              <div className="text-3xl font-black text-gray-800">{s.value}</div>
              <div className="text-xs text-gray-400 mt-1">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* KENAPA OSNGEO.ID */}
      <section id="kenapa" className="bg-gray-50 border-y border-gray-100 py-16">
        <div className="max-w-5xl mx-auto px-6">
          <div className="mb-10 text-center">
            <div className="text-xs font-semibold text-blue-600 uppercase tracking-widest mb-2">Keunggulan</div>
            <h2 className="text-3xl font-black text-gray-800 mb-2">Mengapa OSNGeo.id?</h2>
            <p className="text-gray-500 text-sm max-w-lg mx-auto">Dirancang khusus untuk membantu siswa meraih hasil terbaik di OSN Geografi.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {[
              { icon: '📍', title: 'Soal Sesuai Kisi-kisi OSN', desc: 'Soal disusun berdasarkan kisi-kisi OSN terbaru, dari tingkat kabupaten hingga nasional.' },
              { icon: '🎯', title: 'Sistem Penilaian Resmi', desc: 'Benar +4, Salah -1, Kosong 0 — persis seperti sistem penilaian OSN asli.' },
              { icon: '📊', title: 'Dashboard Kemajuan', desc: 'Pantau perkembangan nilai, riwayat tryout, dan level performa secara real-time.' },
              { icon: '💡', title: 'Pembahasan Mendalam', desc: 'Setiap soal dilengkapi pembahasan detail yang mudah dipahami.' },
              { icon: '🛰️', title: 'Materi Lengkap', desc: 'Mencakup seluruh topik OSN Geografi dari geomorfologi hingga penginderaan jauh.' },
              { icon: '📱', title: 'Akses Kapan Saja', desc: 'Belajar dari mana saja dan kapan saja melalui browser di HP atau laptop.' },
            ].map((f, i) => (
              <div key={i} className="bg-white rounded-xl p-5 border border-gray-200 hover:border-blue-200 hover:shadow-sm transition">
                <div className="text-2xl mb-3">{f.icon}</div>
                <div className="font-bold text-sm text-gray-800 mb-1">{f.title}</div>
                <p className="text-gray-500 text-xs leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* COCOK UNTUK */}
      <section className="max-w-5xl mx-auto px-6 py-16">
        <div className="mb-10 text-center">
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-widest mb-2">Target Pengguna</div>
          <h2 className="text-3xl font-black text-gray-800 mb-2">Cocok Untuk Siapa?</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[
            { icon: '🎓', title: 'Siswa SMA', desc: 'Peserta OSN Geografi tingkat kabupaten hingga nasional.' },
            { icon: '👨‍🏫', title: 'Guru Pembina', desc: 'Pembina OSN yang ingin menyiapkan siswanya dengan tryout berkualitas.' },
            { icon: '🏫', title: 'Sekolah', desc: 'Sekolah yang ingin melakukan simulasi seleksi OSN internal.' },
            { icon: '🏆', title: 'Peserta KSN', desc: 'Peserta Kompetisi Sains Nasional tingkat sekolah hingga nasional.' },
          ].map((t, i) => (
            <div key={i} className="border border-gray-200 rounded-xl p-5 text-center hover:border-blue-200 hover:shadow-sm transition">
              <div className="text-3xl mb-3">{t.icon}</div>
              <div className="font-bold text-sm text-gray-800 mb-1">{t.title}</div>
              <p className="text-gray-500 text-xs leading-relaxed">{t.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* TOPIK MATERI */}
      {topikList.length > 0 && (
        <section id="topik" className="bg-gray-50 border-y border-gray-100 py-16">
          <div className="max-w-5xl mx-auto px-6">
            <div className="mb-10 text-center">
              <div className="text-xs font-semibold text-blue-600 uppercase tracking-widest mb-2">Materi</div>
              <h2 className="text-3xl font-black text-gray-800 mb-2">Topik yang Dipelajari</h2>
              <p className="text-gray-500 text-sm max-w-lg mx-auto">Mencakup seluruh {topikList.length} topik OSN Geografi secara komprehensif.</p>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
              {topikList.map((t, i) => (
                <div key={i} className="bg-white border border-gray-200 rounded-xl px-4 py-3 flex items-center gap-3 hover:border-blue-200 transition">
                  <span className="text-xl shrink-0">{iconTopik[t.nama] || '📚'}</span>
                  <span className="text-sm font-medium text-gray-700">{t.nama}</span>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* PAKET MEMBERSHIP */}
      <section id="paket" className="max-w-5xl mx-auto px-6 py-16">
        <div className="mb-10 text-center">
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-widest mb-2">Paket Membership</div>
          <h2 className="text-3xl font-black text-gray-800 mb-2">Pilih Paket yang Tepat</h2>
          <p className="text-gray-500 text-sm max-w-lg mx-auto">Akses penuh ke semua konten tryout, pendalaman materi, dan video pembelajaran.</p>
        </div>

        {paketMembership.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {paketMembership.map((p, i) => {
              const featured = i === Math.floor(paketMembership.length / 2)
              const fiturList = p.fitur ? String(p.fitur).split('\n').filter(Boolean) : []
              return (
                <div key={p.id} className={`rounded-xl p-6 relative transition ${
                  featured ? 'border-2 border-blue-500 shadow-sm' : 'border border-gray-200 hover:border-blue-300 hover:shadow-sm'
                }`}>
                  {featured && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-xs font-black px-3 py-0.5 rounded-full">
                      Terpopuler
                    </div>
                  )}
                  <div className="text-xs font-semibold text-blue-600 bg-blue-50 px-2.5 py-1 rounded w-fit mb-4 mt-2">{p.nama}</div>
                  <div className="text-2xl font-black text-gray-800 mb-1">Rp {p.harga?.toLocaleString('id-ID')}</div>
                  <div className="text-xs text-gray-400 mb-4">{p.durasi_hari} hari · {p.deskripsi}</div>
                  {fiturList.length > 0 && (
                    <ul className="text-xs text-gray-500 space-y-1.5 mb-5">
                      {fiturList.map((f: string, fi: number) => (
                        <li key={fi} className="flex items-start gap-1.5">
                          <span className="text-green-500 shrink-0">✓</span>{f}
                        </li>
                      ))}
                    </ul>
                  )}
                  <a href={`https://wa.me/6285157220761?text=Halo,%20saya%20ingin%20info%20${encodeURIComponent(p.nama)}%20OSNGeo.id`}
                    target="_blank"
                    className={`block text-center w-full py-2.5 rounded-lg text-sm font-semibold transition ${
                      featured ? 'bg-blue-600 hover:bg-blue-700 text-white' : 'border border-gray-200 hover:border-blue-300 text-gray-700 hover:text-blue-600'
                    }`}>
                    Info & Daftar
                  </a>
                </div>
              )
            })}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-400 text-sm">Paket segera tersedia.</div>
        )}
      </section>

      {/* GRATIS */}
      <section id="gratis" className="bg-blue-600 py-16">
        <div className="max-w-5xl mx-auto px-6">
          <div className="mb-8 text-center">
            <div className="text-xs font-semibold text-blue-200 uppercase tracking-widest mb-2">Uji Coba Gratis</div>
            <h2 className="text-3xl font-black text-white mb-2">Coba Dulu, Bayar Nanti</h2>
            <p className="text-blue-200 text-sm max-w-lg mx-auto">Daftar gratis dan langsung akses konten latihan tanpa kartu kredit.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            {[
              { icon: '📝', title: `${jumlahPaketGratis > 0 ? jumlahPaketGratis : 5} Paket Tryout Gratis`, desc: 'Simulasi OSN lengkap dengan timer, sistem poin resmi, dan pembahasan otomatis.' },
              { icon: '▶️', title: `${jumlahVideo > 0 ? jumlahVideo : 10} Video Pembahasan`, desc: 'Pembahasan soal OSN dari berbagai tahun yang bisa ditonton kapan saja.' },
              { icon: '📊', title: 'Dashboard & Statistik', desc: 'Pantau perkembangan nilai dan riwayat tryout di dashboard pribadi.' },
            ].map((f, i) => (
              <div key={i} className="bg-white/10 border border-white/20 rounded-xl p-5 hover:bg-white/20 transition">
                <div className="text-2xl mb-2">{f.icon}</div>
                <div className="font-bold text-sm text-white mb-1">{f.title}</div>
                <p className="text-blue-200 text-xs leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
          <div className="flex gap-3 flex-wrap justify-center">
            <a href="/register" className="bg-white hover:bg-gray-100 text-blue-600 px-6 py-2.5 rounded-lg text-sm font-bold transition">
              Daftar Gratis Sekarang
            </a>
            <a href="https://wa.me/6285157220761" target="_blank"
              className="border border-white/40 hover:border-white text-white px-6 py-2.5 rounded-lg text-sm transition">
              Hubungi Admin
            </a>
          </div>
        </div>
      </section>

      {/* PENGUMUMAN */}
      {pengumuman.length > 0 && (
        <section id="pengumuman" className="max-w-5xl mx-auto px-6 py-16">
          <div className="mb-6">
            <div className="text-xs font-semibold text-blue-600 uppercase tracking-widest mb-2">Pengumuman</div>
            <h2 className="text-2xl font-black text-gray-800">Info Terbaru</h2>
          </div>
          <div className="flex flex-col gap-3">
            {pengumuman.map((p, i) => (
              <div key={i} className="bg-blue-50 rounded-xl px-5 py-4 border border-blue-100">
                <div className="font-bold text-sm text-gray-800 mb-1">{p.judul}</div>
                <div className="text-gray-500 text-xs">{p.isi}</div>
                <div className="text-gray-400 text-xs mt-1">
                  {new Date(p.created_at).toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* FOOTER */}
      <footer className="border-t border-gray-100 py-8 px-6">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <div className="font-black text-gray-800 mb-1">OSN<span className="text-blue-600">Geo</span>.id</div>
            <p className="text-gray-400 text-xs">Platform Persiapan OSN Geografi Terlengkap di Indonesia</p>
          </div>
          <div className="flex gap-6 text-xs text-gray-400">
            <a href="#kenapa" className="hover:text-gray-700 transition">Keunggulan</a>
            <a href="#topik" className="hover:text-gray-700 transition">Materi</a>
            <a href="#paket" className="hover:text-gray-700 transition">Paket</a>
            <a href="#gratis" className="hover:text-gray-700 transition">Gratis</a>
            <a href="/login" className="hover:text-gray-700 transition">Masuk</a>
          </div>
          <a href="https://wa.me/6285157220761" target="_blank"
            className="text-xs bg-green-50 hover:bg-green-100 text-green-700 border border-green-200 px-4 py-2 rounded-lg transition">
            WA: 0851-5722-0761
          </a>
        </div>
        <div className="text-center text-gray-300 text-xs mt-6">© 2025 OSNGeo.id</div>
      </footer>

      {/* WA FLOATING */}
      <a href="https://wa.me/6285157220761?text=Halo,%20saya%20ingin%20tanya%20tentang%20OSNGeo.id"
        target="_blank"
        className="fixed bottom-6 right-6 z-50 bg-green-500 hover:bg-green-600 text-white px-4 py-3 rounded-xl text-sm font-semibold shadow-lg transition">
        Hubungi Admin
      </a>
    </main>
  )
}