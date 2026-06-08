export default function Home() {
  return (
    <main className="min-h-screen bg-white text-gray-900 font-sans">

      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-10 py-4 border-b border-gray-100 sticky top-0 z-50 bg-white">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-black text-white text-sm">G</div>
          <span className="font-black text-gray-800">OSN<span className="text-blue-600">Geo</span>.id</span>
        </div>
        <ul className="hidden md:flex gap-8 list-none text-sm text-gray-500">
          <li><a href="#paket-to" className="hover:text-gray-900 transition">Paket TO</a></li>
          <li><a href="#bimbel" className="hover:text-gray-900 transition">Bimbel</a></li>
          <li><a href="#gratis" className="hover:text-gray-900 transition">Gratis</a></li>
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

      {/* HERO */}
      <section className="max-w-4xl mx-auto px-6 pt-20 pb-16 text-center">
        <div className="inline-block text-xs font-semibold text-blue-600 bg-blue-50 border border-blue-100 px-3 py-1 rounded-full mb-6">
          Platform Latihan OSN Geografi
        </div>
        <h1 className="text-4xl md:text-6xl font-black leading-tight mb-5 text-gray-900">
          Persiapan OSN Geografi<br />
          <span className="text-blue-600">Lebih Terstruktur</span>
        </h1>
        <p className="text-gray-500 text-base max-w-lg mx-auto leading-relaxed mb-8">
          Tryout online dengan sistem penilaian resmi OSN, pembahasan mendalam, dan bimbingan dari pembina berpengalaman.
        </p>
        <div className="flex gap-3 justify-center flex-wrap">
          <a href="/register" className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg text-sm font-semibold transition">
            Mulai Gratis
          </a>
          <a href="#paket-to" className="border border-gray-200 hover:border-gray-300 text-gray-600 px-6 py-2.5 rounded-lg text-sm transition">
            Lihat Paket
          </a>
        </div>

        {/* STATS */}
        <div className="flex gap-12 justify-center mt-16 pt-10 border-t border-gray-100">
          <div className="text-center">
            <div className="text-3xl font-black text-gray-800">60+</div>
            <div className="text-xs text-gray-400 mt-1">Paket Tryout</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-black text-gray-800">100</div>
            <div className="text-xs text-gray-400 mt-1">Soal per Paket</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-black text-gray-800">30</div>
            <div className="text-xs text-gray-400 mt-1">Pertemuan Intensif</div>
          </div>
        </div>
      </section>

      {/* PAKET TO */}
      <section id="paket-to" className="max-w-5xl mx-auto px-6 py-16">
        <div className="mb-10">
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-widest mb-2">Paket Tryout</div>
          <h2 className="text-3xl font-black text-gray-800 mb-2">Simulasi Soal OSN</h2>
          <p className="text-gray-500 text-sm max-w-lg">Soal setara OSN Kabupaten hingga Nasional. Sistem penilaian resmi: Benar +4, Salah -1, Kosong 0.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="border border-gray-200 rounded-xl p-6 hover:border-blue-300 hover:shadow-sm transition">
            <div className="text-xs font-semibold text-blue-600 bg-blue-50 px-2.5 py-1 rounded w-fit mb-5">Pendalaman Materi</div>
            <h3 className="font-bold text-base text-gray-800 mb-2">10 Paket Pendalaman</h3>
            <p className="text-gray-500 text-xs leading-relaxed mb-5">Latihan soal per topik — peta, inderaja, SIG, geografi fisik dan manusia.</p>
            <div className="text-2xl font-black text-gray-800 mb-1">Rp 99.000</div>
            <p className="text-gray-400 text-xs mb-5">sekali bayar, akses selamanya</p>
            <a href="https://wa.me/6285157220761?text=Halo,%20saya%20ingin%20info%20Paket%20Pendalaman%20OSNGeo.id" target="_blank"
              className="block text-center w-full bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-lg text-sm font-semibold transition">
              Info & Daftar
            </a>
          </div>

          <div className="border-2 border-blue-500 rounded-xl p-6 relative shadow-sm">
            <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-xs font-black px-3 py-0.5 rounded-full">
              Terpopuler
            </div>
            <div className="text-xs font-semibold text-blue-600 bg-blue-50 px-2.5 py-1 rounded w-fit mb-5 mt-2">TO Provinsi & Nasional</div>
            <h3 className="font-bold text-base text-gray-800 mb-2">50 Paket Tryout OSN</h3>
            <p className="text-gray-500 text-xs leading-relaxed mb-5">Simulasi lengkap tingkat Kabupaten, Provinsi, dan Nasional dengan pembahasan.</p>
            <div className="text-2xl font-black text-gray-800 mb-1">Rp 249.000</div>
            <p className="text-gray-400 text-xs mb-5">sekali bayar, akses selamanya</p>
            <a href="https://wa.me/6285157220761?text=Halo,%20saya%20ingin%20info%20Paket%2050%20TO%20OSNGeo.id" target="_blank"
              className="block text-center w-full bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-lg text-sm font-semibold transition">
              Info & Daftar
            </a>
          </div>

          <div className="border border-gray-200 rounded-xl p-6 hover:border-blue-300 hover:shadow-sm transition">
            <div className="text-xs font-semibold text-green-600 bg-green-50 px-2.5 py-1 rounded w-fit mb-5">Bundling Hemat</div>
            <h3 className="font-bold text-base text-gray-800 mb-2">Paket Lengkap</h3>
            <p className="text-gray-500 text-xs leading-relaxed mb-5">Semua paket TO + pendalaman materi + bonus akses kursus 5 pertemuan.</p>
            <div className="text-2xl font-black text-gray-800 mb-1">Rp 349.000</div>
            <p className="text-gray-400 text-xs mb-5">sekali bayar, akses selamanya</p>
            <a href="https://wa.me/6285157220761?text=Halo,%20saya%20ingin%20info%20Paket%20Lengkap%20OSNGeo.id" target="_blank"
              className="block text-center w-full border border-gray-200 hover:border-blue-300 text-gray-700 hover:text-blue-600 py-2.5 rounded-lg text-sm font-semibold transition">
              Info & Daftar
            </a>
          </div>
        </div>
      </section>

      {/* BIMBEL */}
      <section id="bimbel" className="bg-gray-50 border-y border-gray-100 py-16">
        <div className="max-w-5xl mx-auto px-6">
          <div className="mb-10">
            <div className="text-xs font-semibold text-blue-600 uppercase tracking-widest mb-2">Bimbingan Belajar</div>
            <h2 className="text-3xl font-black text-gray-800 mb-2">Bimbel Online OSN Geografi</h2>
            <p className="text-gray-500 text-sm max-w-lg">Belajar langsung bersama pembina OSN dengan materi terstruktur via video eksklusif.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {[
              { sesi: '5', label: 'Starter', harga: 'Rp 149.000', msg: 'Bimbel%205%20Pertemuan' },
              { sesi: '10', label: 'Reguler', harga: 'Rp 249.000', msg: 'Bimbel%2010%20Pertemuan', featured: true },
              { sesi: '30', label: 'Intensif', harga: 'Rp 599.000', msg: 'Bimbel%20Intensif%2030%20Pertemuan' },
            ].map((p, i) => (
              <div key={i} className={`bg-white rounded-xl p-6 ${p.featured ? 'border-2 border-blue-500 shadow-sm' : 'border border-gray-200'}`}>
                {p.featured && <div className="text-xs font-bold text-blue-600 mb-2">Direkomendasikan</div>}
                <div className="text-4xl font-black text-gray-800 mb-1">{p.sesi}</div>
                <div className="text-xs text-gray-400 mb-4">Pertemuan · {p.label}</div>
                <ul className="text-xs text-gray-500 space-y-1.5 mb-5">
                  <li>— {p.sesi} video materi eksklusif</li>
                  <li>— Akses selamanya</li>
                  <li>— Materi OSN terstruktur</li>
                </ul>
                <div className="text-xl font-black text-gray-800 mb-4">{p.harga}</div>
                <a href={`https://wa.me/6285157220761?text=Halo,%20saya%20ingin%20info%20${p.msg}%20OSNGeo.id`} target="_blank"
                  className={`block text-center w-full py-2.5 rounded-lg text-sm font-semibold transition ${
                    p.featured ? 'bg-blue-600 hover:bg-blue-700 text-white' : 'border border-gray-200 hover:border-blue-300 text-gray-700 hover:text-blue-600'
                  }`}>
                  Info & Daftar
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* GRATIS */}
      <section id="gratis" className="max-w-5xl mx-auto px-6 py-16">
        <div className="mb-8">
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-widest mb-2">Uji Coba Gratis</div>
          <h2 className="text-3xl font-black text-gray-800 mb-2">Coba Dulu, Bayar Nanti</h2>
          <p className="text-gray-500 text-sm max-w-lg">Daftar gratis dan langsung akses konten latihan tanpa kartu kredit.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {[
            { title: '5 Paket Tryout Gratis', desc: 'Simulasi OSN lengkap dengan timer, sistem poin resmi, dan pembahasan otomatis.' },
            { title: '10 Video Pembahasan', desc: 'Pembahasan soal OSN dari berbagai tahun yang bisa ditonton kapan saja.' },
            { title: 'Dashboard & Statistik', desc: 'Pantau perkembangan nilai dan riwayat tryout di dashboard pribadi.' },
          ].map((f, i) => (
            <div key={i} className="border border-gray-200 rounded-xl p-5 hover:border-blue-200 transition">
              <div className="font-bold text-sm text-gray-800 mb-1">{f.title}</div>
              <p className="text-gray-500 text-xs leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
        <div className="flex gap-3 flex-wrap">
          <a href="/register" className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg text-sm font-semibold transition">
            Daftar Gratis Sekarang
          </a>
          <a href="https://wa.me/6285157220761" target="_blank"
            className="border border-gray-200 hover:border-gray-300 text-gray-600 px-6 py-2.5 rounded-lg text-sm transition">
            Hubungi Admin
          </a>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-gray-100 py-8 px-6">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <div className="font-black text-gray-800 mb-1">OSN<span className="text-blue-600">Geo</span>.id</div>
            <p className="text-gray-400 text-xs">Platform latihan OSN Geografi · Sistem penilaian resmi</p>
          </div>
          <div className="flex gap-6 text-xs text-gray-400">
            <a href="#paket-to" className="hover:text-gray-700 transition">Paket TO</a>
            <a href="#bimbel" className="hover:text-gray-700 transition">Bimbel</a>
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