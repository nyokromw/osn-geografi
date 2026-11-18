'use client'

import { useState } from 'react'
import { ChevronLeft, ChevronRight, ExternalLink, Play } from 'lucide-react'
import { getYouTubeVideoId } from '../lib/youtube'
import type { LandingVideo } from '../lib/landing-videos'

const thumbnail = (id: string) => 'https://img.youtube.com/vi/' + id + '/hqdefault.jpg'

export function LandingVideoCarousel({ videos }: { videos: LandingVideo[] }) {
  const items = videos.flatMap(video => {
    const id = getYouTubeVideoId(video.youtube_id)
    return id ? [{ ...video, id }] : []
  })
  const [index, setIndex] = useState(0)
  const [playing, setPlaying] = useState(false)
  const video = items[index] ?? items[0]
  if (!video) return null

  function select(position: number) {
    const next = (position + items.length) % items.length
    if (next === index) return
    setPlaying(false)
    setIndex(next)
  }

  return (
    <section className="landing-videos" aria-label="Contoh video pembelajaran" aria-roledescription="karusel">
      <figure className="landing-video-frame">
        <div className="landing-video-cover">
          {playing ? (
            <iframe className="size-full border-0" src={'https://www.youtube-nocookie.com/embed/' + video.id + '?autoplay=1&playsinline=1&rel=0'}
              title={'Video YouTube · ' + video.judul} referrerPolicy="strict-origin-when-cross-origin"
              allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowFullScreen />
          ) : (
            <button type="button" className="landing-video-play" aria-label={'Putar ' + video.judul} onClick={() => setPlaying(true)}>
              {/* The public thumbnail is hosted by YouTube. */}
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={thumbnail(video.id)} alt="" fetchPriority={index === 0 ? 'high' : 'auto'} />
              <span className="landing-video-badge">Contoh video</span>
              <span className="landing-video-play-icon"><Play size={26} fill="currentColor" aria-hidden="true" /></span>
            </button>
          )}
          {items.length > 1 && !playing && <>
            <button type="button" className="landing-video-arrow" data-side="prev" onClick={() => select(index - 1)} aria-label="Video sebelumnya">
              <ChevronLeft size={20} aria-hidden="true" />
            </button>
            <button type="button" className="landing-video-arrow" data-side="next" onClick={() => select(index + 1)} aria-label="Video berikutnya">
              <ChevronRight size={20} aria-hidden="true" />
            </button>
          </>}
        </div>
        <figcaption className="landing-video-caption">
          <div className="min-w-0">
            {items.length > 1 && <output aria-live="polite">Video {index + 1} dari {items.length}</output>}
            <strong>{video.judul}</strong>
          </div>
          <a href={'https://www.youtube.com/watch?v=' + video.id} target="_blank" rel="noreferrer">
            YouTube <ExternalLink size={13} aria-hidden="true" />
          </a>
        </figcaption>
      </figure>
      {items.length > 1 && <div className="landing-video-tabs" role="group" aria-label="Pilih video pembelajaran">
        {items.map((item, position) => (
          <button key={item.posisi} type="button" aria-pressed={index === position} onClick={() => select(position)}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={thumbnail(item.id)} alt="" loading="lazy" />
            <span>{item.judul}</span>
          </button>
        ))}
      </div>}
    </section>
  )
}
