'use client'

import { useId, useRef, useState } from 'react'
import { Clock3, ExternalLink, Play, Sparkles, X } from 'lucide-react'
import { accessLabels, requiredAccess } from '../lib/membership'
import { getYouTubeVideoId } from '../lib/youtube'

export type LearningVideo = {
  id: number
  judul: string
  youtube_id: string | null
  kode?: string | null
  deskripsi?: string | null
  urutan?: number | null
  topik_id?: number | null
  akses?: string | null
  is_premium?: boolean | null
  aktif?: boolean | null
  topik_materi?: { nama: string } | null
}

type Topic = { id: number; nama: string; urutan?: number | null }

/** A video row is "coming soon" while it has no valid YouTube link yet. */
export const isComingSoon = (video: LearningVideo) => !getYouTubeVideoId(video.youtube_id)

const isConcept = (video: LearningVideo) => /-V00$/.test(video.kode ?? '') || /^konsep dasar/i.test(video.judul)
const cleanTitle = (judul: string) => judul.replace(/^konsep dasar:\s*/i, '')

function VideoPlayer({ video, id, dialog, titleId, playing, onClose }: {
  video: LearningVideo; id: string; dialog: React.RefObject<HTMLDialogElement | null>; titleId: string; playing: boolean; onClose: () => void
}) {
  return (
    <dialog ref={dialog} aria-labelledby={titleId} onClose={onClose}
      className="fixed inset-0 m-auto max-h-[90dvh] w-[calc(100%_-_1.5rem)] max-w-4xl overflow-y-auto rounded-2xl border-0 bg-forest-800 p-0 text-[#fff7e7] shadow-2xl backdrop:bg-[#0f1f18]/75">
      <div className="flex items-center justify-between gap-3 px-4 py-3">
        <h2 id={titleId} className="text-base font-bold">{video.kode ? video.kode + ' · ' : ''}{video.judul}</h2>
        <form method="dialog">
          <button type="submit" className="atlas-button" aria-label="Tutup pemutar video"><X size={18} aria-hidden="true" /></button>
        </form>
      </div>
      <div className="relative aspect-video min-h-[200px] bg-black">
        {playing && (
          <iframe className="absolute inset-0 size-full border-0"
            src={'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&playsinline=1&rel=0'}
            title={'Video YouTube — ' + video.judul} referrerPolicy="strict-origin-when-cross-origin"
            allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowFullScreen />
        )}
      </div>
      {video.deskripsi && <p className="px-4 pt-3 text-sm text-[#fff7e7]/80">{video.deskripsi}</p>}
      <div className="flex justify-end px-4 py-3">
        <a href={'https://www.youtube.com/watch?v=' + id} target="_blank" rel="noreferrer"
          className="inline-flex items-center gap-1.5 text-sm font-semibold hover:underline">
          Buka di YouTube <ExternalLink size={14} aria-hidden="true" />
        </a>
      </div>
    </dialog>
  )
}

function usePlayer() {
  const dialog = useRef<HTMLDialogElement>(null)
  const titleId = useId()
  const [playing, setPlaying] = useState(false)
  const open = () => {
    if (!dialog.current || dialog.current.open) return
    dialog.current.showModal()
    setPlaying(true)
  }
  return { dialog, titleId, playing, open, close: () => setPlaying(false) }
}

export function LearningVideoCard({ video }: { video: LearningVideo }) {
  const player = usePlayer()
  const id = getYouTubeVideoId(video.youtube_id)
  const access = requiredAccess(video, true)
  const concept = isConcept(video)

  if (!id) {
    return (
      <article className="learn-card video-soon" aria-label={video.judul + ' — segera tayang'}>
        <div className="video-thumb video-soon-thumb" aria-hidden="true">
          <span className="video-soon-code">{video.kode ?? 'Video'}</span>
          <span className="video-soon-badge"><Clock3 size={14} /> Segera tayang</span>
        </div>
        <div className="learn-card-body">
          {concept && <span className="video-kind" data-kind="concept">Konsep Dasar</span>}
          <h3>{cleanTitle(video.judul)}</h3>
          {video.deskripsi && <p className="video-desc">{video.deskripsi}</p>}
          <div className="learn-card-foot">
            <span className="video-soon-note">Sedang diproduksi</span>
          </div>
        </div>
      </article>
    )
  }

  return (
    <article className="learn-card">
      <button type="button" className="video-thumb" aria-label={'Putar ' + video.judul} aria-haspopup="dialog" onClick={player.open}>
        {/* The thumbnail is loaded directly from YouTube. */}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={'https://img.youtube.com/vi/' + id + '/hqdefault.jpg'} alt="" loading="lazy" />
        <span className="video-thumb-play"><Play size={22} fill="currentColor" aria-hidden="true" /></span>
        {video.kode
          ? <span className="video-thumb-topic">{video.kode}</span>
          : video.topik_materi?.nama && <span className="video-thumb-topic">{video.topik_materi.nama}</span>}
      </button>
      <div className="learn-card-body">
        {concept && <span className="video-kind" data-kind="concept">Konsep Dasar</span>}
        <h3>{cleanTitle(video.judul)}</h3>
        {video.deskripsi && <p className="video-desc">{video.deskripsi}</p>}
        <div className="learn-card-foot">
          <span className="access-badge" data-access={access}>{accessLabels[access]}</span>
          <button type="button" aria-haspopup="dialog" onClick={player.open} className="atlas-link inline-flex items-center gap-1 text-sm">
            <Play size={14} aria-hidden="true" /> Tonton
          </button>
        </div>
      </div>
      <VideoPlayer video={video} id={id} dialog={player.dialog} titleId={player.titleId} playing={player.playing} onClose={player.close} />
    </article>
  )
}

function Spotlight({ video }: { video: LearningVideo }) {
  const player = usePlayer()
  const id = getYouTubeVideoId(video.youtube_id)
  if (!id) return null
  return (
    <section className="video-spotlight" aria-label="Video terbaru">
      <button type="button" className="video-spotlight-thumb" onClick={player.open} aria-haspopup="dialog" aria-label={'Putar ' + video.judul}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={'https://img.youtube.com/vi/' + id + '/hqdefault.jpg'} alt="" />
        <span className="video-thumb-play"><Play size={26} fill="currentColor" aria-hidden="true" /></span>
      </button>
      <div className="video-spotlight-body">
        <span className="video-spotlight-eyebrow"><Sparkles size={14} aria-hidden="true" /> Baru tayang{video.kode ? ' · ' + video.kode : ''}</span>
        <h3>{video.judul}</h3>
        {video.deskripsi && <p>{video.deskripsi}</p>}
        <button type="button" onClick={player.open} aria-haspopup="dialog" className="atlas-button atlas-button--primary video-spotlight-cta">
          <Play size={16} fill="currentColor" aria-hidden="true" /> Tonton sekarang
        </button>
      </div>
      <VideoPlayer video={video} id={id} dialog={player.dialog} titleId={player.titleId} playing={player.playing} onClose={player.close} />
    </section>
  )
}

/** Student video library: grouped per chapter, live videos first-class, the rest shown as "segera tayang". */
export function VideoLibrary({ videos, topics }: { videos: LearningVideo[]; topics: Topic[] }) {
  const [bab, setBab] = useState<number | 'semua'>('semua')
  const [liveOnly, setLiveOnly] = useState(false)

  const order = new Map(topics.map((t, i) => [t.id, t.urutan ?? i + 1]))
  const groups = new Map<number, LearningVideo[]>()
  for (const v of videos) {
    const key = v.topik_id ?? 0
    groups.set(key, [...(groups.get(key) ?? []), v])
  }
  const chapterIds = [...groups.keys()].sort((a, b) => (order.get(a) ?? 999) - (order.get(b) ?? 999))
  const topicName = (id: number) => topics.find(t => t.id === id)?.nama ?? groups.get(id)?.[0]?.topik_materi?.nama ?? 'Lainnya'
  const live = videos.filter(v => !isComingSoon(v))
  const newest = [...live].sort((a, b) => b.id - a.id)[0]
  const shownIds = bab === 'semua' ? chapterIds : chapterIds.filter(id => id === bab)

  return (
    <div className="video-library">
      <div className="video-series">
        <div>
          <span className="dash-eyebrow">Seri Video Konsep OSN Geografi</span>
          <p className="video-series-stat"><strong>{live.length}</strong> dari {videos.length} video sudah tayang</p>
        </div>
        <div className="video-series-bar" role="img" aria-label={`${live.length} dari ${videos.length} video sudah tayang`}>
          <span style={{ width: `${videos.length ? Math.max(2, (live.length / videos.length) * 100) : 0}%` }} />
        </div>
      </div>

      {newest && bab === 'semua' && <Spotlight video={newest} />}

      <div className="video-toolbar">
        <div role="group" aria-label="Filter bab" className="learn-filter">
          <button type="button" aria-pressed={bab === 'semua'} onClick={() => setBab('semua')}>Semua bab</button>
          {chapterIds.map(id => (
            <button key={id} type="button" aria-pressed={bab === id} onClick={() => setBab(id)} title={topicName(id)}>
              {order.has(id) ? 'Bab ' + order.get(id) : topicName(id)}
            </button>
          ))}
        </div>
        <label className="video-live-toggle">
          <input type="checkbox" checked={liveOnly} onChange={e => setLiveOnly(e.target.checked)} /> Sudah tayang saja
        </label>
      </div>

      {shownIds.map(id => {
        const all = (groups.get(id) ?? []).slice().sort((a, b) => (a.urutan ?? 0) - (b.urutan ?? 0))
        const items = liveOnly ? all.filter(v => !isComingSoon(v)) : all
        const done = all.filter(v => !isComingSoon(v)).length
        if (!items.length) return null
        return (
          <section key={id} className="video-chapter" aria-labelledby={'bab-' + id}>
            <header className="video-chapter-head">
              <div>
                {order.has(id) && <span className="video-chapter-num">Bab {order.get(id)}</span>}
                <h3 id={'bab-' + id}>{topicName(id)}</h3>
              </div>
              <span className="video-chapter-progress" data-done={done === all.length}>
                {done}/{all.length} tayang
              </span>
            </header>
            <div className="learn-grid">
              {items.map(v => <LearningVideoCard key={v.id} video={v} />)}
            </div>
          </section>
        )
      })}
      {shownIds.every(id => !(groups.get(id) ?? []).some(v => !liveOnly || !isComingSoon(v))) && (
        <div className="learn-empty">{liveOnly ? 'Belum ada video yang tayang di bab ini.' : 'Belum ada video tersedia.'}</div>
      )}
    </div>
  )
}

