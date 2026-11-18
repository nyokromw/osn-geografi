'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { ArrowRight, BookOpen, Compass, MessageCircle, TrendingUp } from 'lucide-react'
import Image from 'next/image'
import { AtlasMap, Brand } from './components/atlas'
import { LandingVideoCarousel } from './components/landing-video-carousel'
import { MembershipPlans } from './components/membership-plans'
import { TryoutComparison } from './components/tryout-comparison'
import type { LandingVideo } from './lib/landing-videos'
import { adminWhatsApp, type MembershipPlan } from './lib/membership'
import { supabase } from './lib/supabase'
import { predictionYear, type TryoutCatalogEntry } from './lib/tryout-catalog'

const sections = [
  ['Materi', '#topik'],
  ['Tryout', '#tryout'],
  ['Paket', '#paket'],
  ['Gratis', '#gratis'],
]

const highlights = [
  ['Tryout OSN', 'Latihan dan prediksi dengan pembahasan'],
  ['13 bab', 'Modul OSN Geografi'],
  ['Video konsep', 'Contoh pembelajaran siap tonton'],
  ['Rp0', 'Untuk mulai berlatih'],
]

type Topic = { id: number; nama: string }
type Announcement = { id: number; judul: string; isi: string; created_at: string }

export default function Home() {
  const [memberships, setMemberships] = useState<MembershipPlan[]>([])
  const [announcements, setAnnouncements] = useState<Announcement[]>([])
  const [topics, setTopics] = useState<Topic[]>([])
  const [videos, setVideos] = useState<LandingVideo[]>([])
  const [tryouts, setTryouts] = useState<TryoutCatalogEntry[] | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let active = true
    const load = async () => {
      try {
        const [plans, news, catalog, featured, packages] = await Promise.all([
          supabase.from('paket_membership').select('id, nama, harga, durasi_hari, deskripsi, fitur, akses, aktif').order('id'),
          supabase.from('pengumuman').select('id, judul, isi, created_at').eq('aktif', true).order('created_at', { ascending: false }).limit(3),
          supabase.from('topik_materi').select('id, nama').order('urutan'),
          supabase.from('video_beranda').select('posisi, judul, youtube_id').order('posisi'),
          supabase.from('paket_to').select('jenis, kategori, tahun, akses, is_premium').eq('status', 'aktif'),
        ])
        if (!active) return
        setMemberships(plans.data ?? [])
        setAnnouncements(news.data ?? [])
        setTopics(catalog.data ?? [])
        setVideos(featured.data ?? [])
        setTryouts(packages.data)
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
            <Link href="/register" className="atlas-button atlas-button--primary">Mulai Gratis</Link>
          </div>
        </div>
      </header>
      <main className="landing-home">
        <div className="landing-hero-background">
          <section className="atlas-container landing-hero">
            <div className="atlas-hero-copy">
              <p className="landing-hero-eyebrow">
                <Image src="/brand/logo-mark.svg" width={22} height={22} alt="" unoptimized /> Olimpiade Sains Nasional · Geografi
              </p>
              <h1>Persiapan Lebih Matang dengan <span>OSNGEO.id</span></h1>
              <p className="text-base leading-relaxed lg:text-lg">
                Pelajari modul, video, latihan soal, dan try out dalam satu aplikasi OSNGEO.id
              </p>
              <div className="flex flex-wrap gap-2.5">
                <Link href="/register" className="atlas-button atlas-button--primary">
                  Mulai Gratis <ArrowRight size={17} aria-hidden="true" />
                </Link>
                <a href="#topik" className="atlas-button">Jelajahi Materi</a>
              </div>
              <p className="landing-free-note">Mulai dengan tryout dan latihan per topik lengkap dengan pembahasan.</p>
            </div>
            {videos.length ? <LandingVideoCarousel videos={videos} />
              : loading ? <div className="landing-hero-placeholder" role="status" aria-label="Memuat contoh video" />
              : <AtlasMap priority />}
          </section>
          <div className="landing-highlights">
            <ul className="atlas-container">
              {highlights.map(([title, description]) => <li key={title}><strong>{title}</strong><span>{description}</span></li>)}
            </ul>
          </div>
        </div>
        <div className="atlas-container">
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
        <section id="tryout" className="atlas-container atlas-section">
          <h2 className="atlas-subtitle">Latihan dan Prediksi {predictionYear}</h2>
          <p className="mt-2 mb-5 max-w-prose text-sm text-gray-600">Platinum mencakup seluruh akses Premium. Keterangan tersedia menunjukkan jumlah paket yang sudah bisa dikerjakan jika berbeda dari alokasi.</p>
          <TryoutComparison catalog={tryouts} />
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
              <p className="mt-2 max-w-prose text-sm text-gray-600">Coba tryout OSN-K dan OSN-P serta latihan pendalaman gratis per topik. Pantau hasilnya di dashboard.</p>
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
      <footer className="landing-footer">
        <div className="atlas-container landing-footer-inner">
          <div>
            <Brand />
            <p>Persiapan OSN Geografi · © {new Date().getFullYear()} OSNGEO.id</p>
          </div>
          <nav aria-label="Tautan footer">
            {sections.map(([name, href]) => <a key={href} className="hover:text-forest-700 hover:underline" href={href}>{name}</a>)}
          </nav>
          <a href={adminWhatsApp} target="_blank" rel="noreferrer" className="atlas-button justify-self-start">
            <MessageCircle size={16} aria-hidden="true" /> Hubungi admin
          </a>
        </div>
      </footer>
    </>
  )
}
