'use client'

import { useId, useRef, useState } from 'react'
import { ExternalLink, Play, Video, X } from 'lucide-react'
import { accessLabels, requiredAccess } from '../lib/membership'
import { getYouTubeVideoId } from '../lib/youtube'

export type LearningVideo = {
  id: number
  judul: string
  youtube_id: string | null
  akses?: string | null
  is_premium?: boolean | null
  aktif?: boolean | null
  topik_materi?: { nama: string } | null
}

export function LearningVideoCard({ video }: { video: LearningVideo }) {
  const dialog = useRef<HTMLDialogElement>(null)
  const titleId = useId()
  const [playing, setPlaying] = useState(false)
  const id = getYouTubeVideoId(video.youtube_id)
  const access = requiredAccess(video, true)

  function openPlayer() {
    if (!dialog.current || dialog.current.open) return
    dialog.current.showModal()
    setPlaying(true)
  }

  return (
    <article className="learn-card">
      {id ? (
        <button type="button" className="video-thumb"
          aria-label={'Putar ' + video.judul} aria-haspopup="dialog" onClick={openPlayer}>
          {/* The thumbnail is loaded directly from YouTube. */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={'https://img.youtube.com/vi/' + id + '/hqdefault.jpg'} alt="" loading="lazy" />
          <span className="video-thumb-play"><Play size={22} fill="currentColor" aria-hidden="true" /></span>
          {video.topik_materi?.nama && <span className="video-thumb-topic">{video.topik_materi.nama}</span>}
        </button>
      ) : (
        <div className="video-thumb grid place-items-center text-white/70">
          <Video size={28} aria-hidden="true" />
        </div>
      )}
      <div className="learn-card-body">
        <h3>{video.judul}</h3>
        <div className="learn-card-foot">
          <span className="access-badge" data-access={access}>{accessLabels[access]}</span>
          {id ? (
            <button type="button" aria-haspopup="dialog" onClick={openPlayer} className="atlas-link inline-flex items-center gap-1 text-sm">
              <Play size={14} aria-hidden="true" /> Tonton
            </button>
          ) : (
            <span className="text-xs text-gray-600">Tautan video tidak valid</span>
          )}
        </div>
      </div>
      {id && (
        <dialog ref={dialog} aria-labelledby={titleId} onClose={() => setPlaying(false)}
          className="fixed inset-0 m-auto max-h-[90dvh] w-[calc(100%_-_1.5rem)] max-w-4xl overflow-y-auto rounded-2xl border-0 bg-forest-800 p-0 text-[#fff7e7] shadow-2xl backdrop:bg-[#0f1f18]/75">
          <div className="flex items-center justify-between gap-3 px-4 py-3">
            <h2 id={titleId} className="text-base font-bold">{video.judul}</h2>
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
          <div className="flex justify-end px-4 py-3">
            <a href={'https://www.youtube.com/watch?v=' + id} target="_blank" rel="noreferrer"
              className="inline-flex items-center gap-1.5 text-sm font-semibold hover:underline">
              Buka di YouTube <ExternalLink size={14} aria-hidden="true" />
            </a>
          </div>
        </dialog>
      )}
    </article>
  )
}
