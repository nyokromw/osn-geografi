'use client'

import { useState } from 'react'
import { ArrowLeft, ArrowRight, ExternalLink, Play } from 'lucide-react'
import { getYouTubeVideoId } from '../lib/youtube'
import type { LandingVideo } from '../lib/landing-videos'

export function LandingVideoCarousel({ videos }: { videos: LandingVideo[] }) {
  const [index, setIndex] = useState(0)
  const [playing, setPlaying] = useState(false)
  const video = videos[index] ?? videos[0]
  const id = getYouTubeVideoId(video?.youtube_id)
  if (!video || !id) return null

  function select(position: number) {
    const next = (position + videos.length) % videos.length
    if (next === index) return
    setPlaying(false)
    setIndex(next)
  }

  return (
    <section className="landing-videos" aria-label="Contoh video pembelajaran" aria-roledescription="karusel">
      <div className="landing-video-toolbar">
        <h2>Contoh video pembelajaran</h2>
        {videos.length > 1 && <div role="group" aria-label="Navigasi karusel" className="landing-video-controls">
          <button type="button" onClick={() => select(index - 1)} aria-label="Video sebelumnya"><ArrowLeft size={16} /></button>
          <output aria-live="polite">{index + 1} / {videos.length}</output>
          <button type="button" onClick={() => select(index + 1)} aria-label="Video berikutnya"><ArrowRight size={16} /></button>
        </div>}
      </div>
      <figure className="landing-video-frame">
        <div className="landing-video-cover">
          {playing ? (
            <iframe className="size-full border-0" src={'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&playsinline=1'}
              title={'Video YouTube · ' + video.judul} referrerPolicy="strict-origin-when-cross-origin"
              allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowFullScreen />
          ) : (
            <button type="button" className="landing-video-play" aria-label={'Putar ' + video.judul} onClick={() => setPlaying(true)}>
              {/* The public thumbnail is hosted by YouTube. */}
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={'https://img.youtube.com/vi/' + id + '/hqdefault.jpg'} alt="" fetchPriority={index === 0 ? 'high' : 'auto'} />
              <span><Play size={24} fill="currentColor" aria-hidden="true" /></span>
            </button>
          )}
        </div>
        <figcaption className="landing-video-caption">
          <strong>{video.judul}</strong>
          <a href={'https://www.youtube.com/watch?v=' + id} target="_blank" rel="noreferrer">
            Buka di YouTube <ExternalLink size={13} aria-hidden="true" />
          </a>
        </figcaption>
      </figure>
      {videos.length > 1 && <div className="landing-video-tabs" role="group" aria-label="Pilih video pembelajaran">
        {videos.map((item, position) => (
          <button key={item.posisi} type="button" aria-pressed={index === position} onClick={() => select(position)}>
            {item.judul}
          </button>
        ))}
      </div>}
    </section>
  )
}
