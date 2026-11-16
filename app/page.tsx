'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { ArrowRight, ArrowUpRight, BookOpen, ClipboardList, Compass, Layers3, MessageCircle, TrendingUp } from 'lucide-react'
import { AtlasMap, Brand } from './components/atlas'
import { MembershipPlans } from './components/membership-plans'
import { adminWhatsApp, type MembershipPlan } from './lib/membership'
import { supabase } from './lib/supabase'

const sections = [
  ['Keunggulan', '#kenapa'],
  ['Materi', '#topik'],
  ['Paket', '#paket'],
  ['Gratis', '#gratis'],
]

const journeys = [
  { title: 'Tryout', description: 'Simulasi ujian dengan timer.', href: '#gratis', Icon: ClipboardList },
  { title: 'Pendalaman materi', description: 'Latihan soal per topik.', href: '#topik', Icon: Layers3 },
  { title: 'Video dan modul', description: 'Materi untuk belajar mandiri.', href: '#kenapa', Icon: BookOpen },
]

type Topic = { id: number; nama: string }
type Announcement = { id: number; judul: string; isi: string; created_at: string }

export default function Home() {
  const [memberships, setMemberships] = useState<MembershipPlan[]>([])
  const [announcements, setAnnouncements] = useState<Announcement[]>([])
  const [topics, setTopics] = useState<Topic[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let active = true
    const load = async () => {
      try {
        const [plans, news, catalog] = await Promise.all([
          supabase.from('paket_membership').select('id, nama, harga, durasi_hari, deskripsi, fitur, akses, aktif').order('id'),
          supabase.from('pengumuman').select('id, judul, isi, created_at').eq('aktif', true).order('created_at', { ascending: false }).limit(3),
          supabase.from('topik_materi').select('id, nama').order('urutan'),
        ])
        if (!active) return
        setMemberships(plans.data ?? [])
        setAnnouncements(news.data ?? [])
        setTopics(catalog.data ?? [])
      } finally {
        if (active) setLoading(false)
      }
    }
    void load()
    return () => { active = false }
  }, [])

  return (
    <>
      <header className="atlas-topbar">
        <div className="atlas-container atlas-topbar-inner">
          <Brand />
          <nav aria-label="Navigasi utama" className="hidden items-center gap-6 text-sm font-medium text-gray-600 md:flex">
            {sections.map(([name, href]) => (
              <a key={href} className="hover:text-forest-700 hover:underline hover:underline-offset-4" href={href}>{name}</a>
            ))}
          </nav>
          <div className="atlas-top-actions">
            <Link href="/login" className="atlas-button">Masuk</Link>
            <Link href="/register" className="atlas-button atlas-button--primary">Daftar</Link>
          </div>
        </div>
      </header>
      <main>
        <div className="atlas-container">
          <section className="atlas-hero">
            <div className="atlas-hero-copy">
              <h1>Siap untuk <em>OSN Geografi.</em></h1>
              <p className="text-base leading-relaxed lg:text-lg">
                Persiapkan olimpiade lewat tryout, latihan per topik, dan pembahasan geografi.
              </p>
              <div className="flex flex-wrap gap-2.5">
                <Link href="/register" className="atlas-button atlas-button--primary">
                  Mulai gratis <ArrowRight size={17} aria-hidden="true" />
                </Link>
                <a href="#paket" className="atlas-button">Lihat paket</a>
              </div>
            </div>
            <AtlasMap priority />
          </section>
          <nav className="atlas-journeys" aria-label="Pilihan belajar">
            {journeys.map(({ title, description, href, Icon }) => (
              <a key={title} href={href} className="atlas-journey">
                <span className="atlas-icon"><Icon aria-hidden="true" /></span>
                <span>
                  <strong className="block text-sm font-bold">{title}</strong>
                  <small className="block text-xs text-gray-500">{description}</small>
                </span>
                <ArrowUpRight className="atlas-journey-arrow" size={16} aria-hidden="true" />
              </a>
            ))}
          </nav>
          <section id="kenapa" className="atlas-section">
            <h2 className="atlas-subtitle">Belajar dan ukur kemajuanmu</h2>
            <div className="mt-6 grid gap-3 md:grid-cols-3">
              {[
                { Icon: Compass, label: 'Latihan terarah', detail: 'Pilih topik yang perlu kamu perdalam dan pelajari pembahasannya.' },
                { Icon: BookOpen, label: 'Materi mandiri', detail: 'Pelajari konsep dan cara mengerjakan soal lewat video dan modul.' },
                { Icon: TrendingUp, label: 'Grafik kemajuan', detail: 'Lihat perubahan poin dan persentase jawaban benar dari sesi ke sesi.' },
              ].map(({ Icon, label, detail }) => (
                <article key={label} className="atlas-card p-5">
                  <span className="atlas-icon"><Icon aria-hidden="true" /></span>
                  <h3 className="mt-3 text-base font-bold">{label}</h3>
                  <p className="mt-1 text-sm leading-relaxed text-gray-500">{detail}</p>
                </article>
              ))}
            </div>
          </section>
        </div>
        <section id="topik" className="atlas-section border-y border-gray-200 bg-white">
          <div className="atlas-container">
            <h2 className="atlas-subtitle">Topik geografi</h2>
            {topics.length ? (
              <ul className="mt-6 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
                {topics.map(topic => (
                  <li key={topic.id} className="flex items-center gap-3 rounded-lg border border-gray-200 px-4 py-3 text-sm font-semibold">
                    <Compass size={17} className="shrink-0 text-forest-500" aria-hidden="true" /> {topic.nama}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-3 text-sm text-gray-500">{loading ? 'Memuat topik…' : 'Daftar topik belum tersedia.'}</p>
            )}
          </div>
        </section>
        <section id="paket" className="atlas-container atlas-section">
          <h2 className="atlas-subtitle">Paket belajar</h2>
          <p className="mt-2 text-sm text-gray-500">Pilih akses belajar sesuai kebutuhanmu.</p>
          <MembershipPlans plans={memberships} loading={loading} />
        </section>
        <section id="gratis" className="atlas-section border-y border-forest-200 bg-forest-100">
          <div className="atlas-container flex flex-wrap items-center justify-between gap-5">
            <div>
              <h2 className="atlas-subtitle">Coba latihan gratis</h2>
              <p className="mt-2 max-w-prose text-sm text-gray-600">Coba 4 tryout OSN-K dan 3 cuplikan pendalaman gratis. Pantau hasilnya di dashboard.</p>
            </div>
            <Link href="/register" className="atlas-button atlas-button--primary">
              Buat akun gratis <ArrowRight size={17} aria-hidden="true" />
            </Link>
          </div>
        </section>
        {announcements.length > 0 && (
          <section id="pengumuman" className="atlas-container atlas-section">
            <h2 className="atlas-subtitle">Pengumuman</h2>
            <div className="mt-5 grid gap-3 md:grid-cols-3">
              {announcements.map(item => (
                <article key={item.id} className="atlas-card p-5">
                  <h3 className="font-bold">{item.judul}</h3>
                  <p className="mt-2 whitespace-pre-line text-sm text-gray-600">{item.isi}</p>
                  <time className="mt-3 block text-xs text-gray-500" dateTime={item.created_at}>
                    {new Date(item.created_at).toLocaleDateString('id-ID')}
                  </time>
                </article>
              ))}
            </div>
          </section>
        )}
      </main>
      <footer className="border-t border-gray-200 bg-white py-6">
        <div className="atlas-container flex flex-wrap items-center justify-between gap-4">
          <Brand />
          <nav className="flex flex-wrap gap-4 text-sm text-gray-600" aria-label="Tautan footer">
            {sections.map(([name, href]) => <a key={href} className="hover:underline" href={href}>{name}</a>)}
          </nav>
          <a href={adminWhatsApp} target="_blank" rel="noreferrer" className="atlas-button">
            <MessageCircle size={16} aria-hidden="true" /> Hubungi admin
          </a>
        </div>
      </footer>
    </>
  )
}
