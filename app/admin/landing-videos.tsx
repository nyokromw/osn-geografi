'use client'

import { useEffect, useState, type FormEvent } from 'react'
import { supabase } from '../lib/supabase'
import { getYouTubeVideoId } from '../lib/youtube'
import { landingVideoSlots, type LandingVideo } from '../lib/landing-videos'

const blank = landingVideoSlots.map(posisi => ({ posisi, judul: '', youtube_id: '' }))

export function LandingVideoSettings() {
  const [slots, setSlots] = useState<LandingVideo[]>(blank)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [loadError, setLoadError] = useState(false)
  const [message, setMessage] = useState<{ error: boolean; text: string } | null>(null)

  useEffect(() => {
    let mounted = true
    void supabase.from('video_beranda').select('posisi, judul, youtube_id').order('posisi').then(({ data, error }) => {
      if (!mounted) return
      if (error) setLoadError(true)
      else setSlots(blank.map(slot => data?.find(item => item.posisi === slot.posisi) ?? slot))
      setLoading(false)
    })
    return () => { mounted = false }
  }, [])

  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const updated = slots.map(slot => ({
      posisi: slot.posisi,
      judul: slot.judul.trim(),
      youtube_id: getYouTubeVideoId(slot.youtube_id),
    }))
    const invalid = updated.find(slot => !slot.judul || !slot.youtube_id)
    if (invalid) {
      setMessage({ error: true, text: 'Periksa judul dan tautan YouTube pada Video ' + invalid.posisi + '.' })
      return
    }
    setSaving(true)
    setMessage(null)
    try {
      const { error } = await supabase.from('video_beranda').upsert(updated, { onConflict: 'posisi' })
      setMessage(error
        ? { error: true, text: 'Video beranda gagal disimpan. Coba lagi.' }
        : { error: false, text: 'Video beranda sudah diperbarui.' })
    } finally {
      setSaving(false)
    }
  }

  function change(position: number, field: 'judul' | 'youtube_id', value: string) {
    setSlots(current => current.map(slot => slot.posisi === position ? { ...slot, [field]: value } : slot))
  }

  return (
    <section className="max-w-2xl">
      <h2 className="text-xl font-black">Video beranda</h2>
      <p className="mt-1 text-sm text-gray-600">Pilih tiga video YouTube untuk karusel di halaman publik. Urutan mengikuti nomor slot.</p>
      {loading ? <p className="mt-4 text-sm text-gray-600">Memuat pengaturan…</p> : loadError ? (
        <p className="atlas-notice mt-4" data-error="true" role="alert">Pengaturan belum dapat dimuat. Muat ulang halaman untuk mencoba lagi.</p>
      ) : (
        <form className="mt-5 grid gap-4" onSubmit={save}>
          {slots.map(slot => (
            <fieldset key={slot.posisi} className="atlas-card grid gap-3 px-4 pb-4">
              <legend className="px-1 text-sm font-bold">Video {slot.posisi}</legend>
              <label className="grid gap-1 text-sm font-semibold">Judul video
                <input className="atlas-field" value={slot.judul} maxLength={90} required disabled={saving}
                  onChange={event => change(slot.posisi, 'judul', event.target.value)} />
              </label>
              <label className="grid gap-1 text-sm font-semibold">Tautan atau ID YouTube
                <input className="atlas-field" value={slot.youtube_id} required disabled={saving}
                  onChange={event => change(slot.posisi, 'youtube_id', event.target.value)} />
              </label>
            </fieldset>
          ))}
          {message && <p className="atlas-notice" data-error={message.error} role={message.error ? 'alert' : 'status'}>{message.text}</p>}
          <button className="atlas-button atlas-button--primary justify-self-start" type="submit" disabled={saving}>
            {saving ? 'Menyimpan…' : 'Simpan Video Beranda'}
          </button>
        </form>
      )}
    </section>
  )
}
