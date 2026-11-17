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
    <article className="atlas-card overflow-hidden">
      {id ? (
        <button type="button" className="group relative block aspect-video w-full overflow-hidden bg-gray-100"
          aria-label={'Putar ' + video.judul} aria-haspopup="dialog" onClick={openPlayer}>
          {/* The thumbnail is loaded directly from YouTube. */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={'https://img.youtube.com/vi/' + id + '/mqdefault.jpg'} alt="" loading="lazy"
            className="absolute inset-0 size-full object-cover" />
          <span className="absolute inset-0 grid place-items-center bg-black/15">
            <span className="grid size-12 place-items-center rounded-full bg-black/65 text-white group-hover:bg-forest-700">
              <Play size={23} fill="currentColor" aria-hidden="true" />
            </span>
          </span>
        </button>
      ) : (
        <div className="grid aspect-video place-items-center bg-gray-100 text-gray-500">
          <Video size={28} aria-hidden="true" />
        </div>
      )}
      <div className="space-y-2 p-4">
        <h3 className="text-sm font-bold text-gray-900">{video.judul}</h3>
        {video.topik_materi?.nama && <p className="text-xs text-gray-600">{video.topik_materi.nama}</p>}
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span className={'rounded-full px-2 py-0.5 text-xs font-bold ' +
            (access === 'gratis' ? 'bg-green-100 text-green-700' : 'bg-forest-100 text-forest-800')}>
            {accessLabels[access]}
          </span>
          {id ? (
            <button type="button" aria-haspopup="dialog" onClick={openPlayer} className="atlas-link text-sm">Putar video</button>
          ) : (
            <span className="text-xs text-gray-600">Tautan video tidak valid</span>
          )}
        </div>
      </div>
      {id && (
        <dialog ref={dialog} aria-labelledby={titleId} onClose={() => setPlaying(false)}
          className="atlas-card fixed inset-0 m-auto max-h-[90dvh] w-[calc(100%_-_1.5rem)] max-w-4xl overflow-y-auto p-0 shadow-xl backdrop:bg-black/55">
          <div className="flex items-center justify-between gap-3 px-4 py-3">
            <h2 id={titleId} className="text-base font-bold text-gray-900">{video.judul}</h2>
            <form method="dialog">
              <button type="submit" className="atlas-button" aria-label="Tutup pemutar video"><X size={18} aria-hidden="true" /></button>
            </form>
          </div>
          <div className="relative aspect-video min-h-[200px] bg-black">
            {playing && (
              <iframe className="absolute inset-0 size-full border-0"
                src={'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&playsinline=1'}
                title={'Video YouTube — ' + video.judul} referrerPolicy="strict-origin-when-cross-origin"
                allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowFullScreen />
            )}
          </div>
          <div className="flex justify-end px-4 py-3">
            <a href={'https://www.youtube.com/watch?v=' + id} target="_blank" rel="noreferrer"
              className="atlas-link inline-flex items-center gap-1.5 text-sm">
              Buka di YouTube <ExternalLink size={14} aria-hidden="true" />
            </a>
          </div>
        </dialog>
      )}
    </article>
  )
}
