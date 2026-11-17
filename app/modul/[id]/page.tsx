'use client'

import Link from 'next/link'
import { useParams, useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { ArrowLeft, ChevronLeft, ChevronRight, ZoomIn, ZoomOut } from 'lucide-react'
import { Notice, PageLoading, WorkspaceHeader } from '../../components/atlas'
import { supabase } from '../../lib/supabase'

type Modul = {
  id: number
  judul: string
  folder_halaman: string
  jumlah_halaman: number
}

type ModulResult =
  | { id: string; modul: Modul }
  | { id: string; error: string }

const daftarModul = '/dashboard?tab=modul'

export default function ModulPage() {
  const { id } = useParams<{ id: string }>()
  const router = useRouter()
  const [result, setResult] = useState<ModulResult | null>(null)
  const validId = /^[1-9]\d{0,9}$/.test(id) && Number(id) <= 2147483647

  useEffect(() => {
    if (!validId) return
    const request = new AbortController()

    async function loadModul() {
      const { data: { user } } = await supabase.auth.getUser()
      if (request.signal.aborted) return
      if (!user) {
        router.replace('/login')
        return
      }
      const { data, error } = await supabase.from('modul_materi')
        .select('id, judul, folder_halaman, jumlah_halaman')
        .eq('id', Number(id))
        .eq('aktif', true)
        .eq('akses', 'platinum')
        .abortSignal(request.signal)
        .maybeSingle()
      if (request.signal.aborted) return
      if (error) {
        setResult({ id, error: 'Modul gagal dimuat. Muat ulang halaman untuk mencoba lagi.' })
      } else if (!data?.folder_halaman || !data.jumlah_halaman) {
        setResult({ id, error: 'Modul ini tersedia untuk akun Platinum yang aktif.' })
      } else {
        setResult({ id, modul: data })
      }
    }

    void loadModul().catch(() => {
      if (!request.signal.aborted) {
        setResult({ id, error: 'Modul gagal dimuat. Muat ulang halaman untuk mencoba lagi.' })
      }
    })
    return () => request.abort()
  }, [id, validId, router])

  if (validId && result?.id !== id) return <PageLoading>Memuat modul…</PageLoading>
  const modul = validId && result && 'modul' in result ? result.modul : null
  const error = result && 'error' in result ? result.error : 'Modul tidak ditemukan.'

  return (
    <div className="print:hidden">
      <WorkspaceHeader title="Pembaca modul">
        <Link href={daftarModul} className="atlas-button">
          <ArrowLeft size={16} aria-hidden="true" /> Daftar modul
        </Link>
      </WorkspaceHeader>
      <main className="atlas-container mx-auto max-w-5xl py-6 sm:py-8">
        {modul ? <Pembaca key={modul.id} modul={modul} /> : <Notice error>{error}</Notice>}
      </main>
    </div>
  )
}

function Pembaca({ modul }: { modul: Modul }) {
  const [halaman, setHalaman] = useState(1)
  const [nomor, setNomor] = useState('1')
  const [zoom, setZoom] = useState(100)
  const [percobaan, setPercobaan] = useState(0)
  const [gambar, setGambar] = useState<{ halaman: number; percobaan: number; url: string | null } | null>(null)

  useEffect(() => {
    const request = new AbortController()
    let url: string | null = null

    async function loadHalaman() {
      const name = String(halaman).padStart(4, '0') + '.webp'
      const { data, error } = await supabase.storage.from('modul-halaman')
        .download(modul.folder_halaman + '/' + name, {}, { signal: request.signal, cache: 'no-store' })
      if (request.signal.aborted) return
      if (!error && data) url = URL.createObjectURL(data)
      setGambar({ halaman, percobaan, url })
    }

    void loadHalaman().catch(() => {
      if (!request.signal.aborted) setGambar({ halaman, percobaan, url: null })
    })
    return () => {
      request.abort()
      if (url) URL.revokeObjectURL(url)
    }
  }, [modul.folder_halaman, halaman, percobaan])

  function bukaHalaman(next: number) {
    if (!Number.isInteger(next) || next < 1 || next > modul.jumlah_halaman) {
      setNomor(String(halaman))
      return
    }
    setHalaman(next)
    setNomor(String(next))
    if (next !== halaman) window.scrollTo({ top: 0, behavior: 'auto' })
  }

  const tampil = gambar?.halaman === halaman && gambar.percobaan === percobaan ? gambar : null

  return (
    <>
      <h1 className="mb-4 text-xl font-bold text-gray-900 sm:text-2xl">{modul.judul}</h1>
      <div className="atlas-card sticky top-[4.25rem] z-10 mb-4 flex flex-wrap items-center justify-between gap-2 p-2.5 sm:p-3">
        <div className="flex items-center gap-1.5">
          <button type="button" className="atlas-button disabled:opacity-40" aria-label="Halaman sebelumnya"
            disabled={halaman === 1} onClick={() => bukaHalaman(halaman - 1)}>
            <ChevronLeft size={18} aria-hidden="true" />
          </button>
          <form className="flex items-center gap-1.5" onSubmit={event => {
            event.preventDefault()
            bukaHalaman(Number(nomor))
          }}>
            <input type="number" inputMode="numeric" min={1} max={modul.jumlah_halaman}
              aria-label="Nomor halaman" value={nomor} onChange={event => setNomor(event.target.value)}
              className="w-14 rounded-md border border-gray-300 px-1.5 py-2 text-center text-sm" />
            <span className="text-sm tabular-nums text-gray-600">/ {modul.jumlah_halaman}</span>
            <button type="submit" className="atlas-button text-sm">Buka</button>
          </form>
          <button type="button" className="atlas-button disabled:opacity-40" aria-label="Halaman berikutnya"
            disabled={halaman === modul.jumlah_halaman} onClick={() => bukaHalaman(halaman + 1)}>
            <ChevronRight size={18} aria-hidden="true" />
          </button>
        </div>
        <div className="flex items-center gap-1.5">
          <button type="button" className="atlas-button disabled:opacity-40" aria-label="Perkecil"
            disabled={zoom === 100} onClick={() => setZoom(zoom - 25)}>
            <ZoomOut size={17} aria-hidden="true" />
          </button>
          <span className="min-w-10 text-center text-sm tabular-nums text-gray-600">{zoom}%</span>
          <button type="button" className="atlas-button disabled:opacity-40" aria-label="Perbesar"
            disabled={zoom === 200} onClick={() => setZoom(zoom + 25)}>
            <ZoomIn size={17} aria-hidden="true" />
          </button>
        </div>
      </div>
      <div className="overflow-auto rounded-xl bg-gray-100 p-1 sm:p-3" aria-busy={!tampil}>
        {!tampil ? (
          <p className="px-3 py-16 text-center text-sm text-gray-600" role="status">Memuat halaman {halaman}…</p>
        ) : tampil.url ? (
          // The app holds a short-lived blob URL for one authorized page.
          // eslint-disable-next-line @next/next/no-img-element
          <img src={tampil.url} alt={'Halaman ' + halaman + ' — ' + modul.judul}
            className="mx-auto block h-auto max-w-none select-none bg-white"
            style={{ width: zoom + '%' }} draggable={false} onContextMenu={event => event.preventDefault()} />
        ) : (
          <div className="space-y-3 p-4">
            <Notice error>Halaman ini gagal dimuat. Periksa koneksi dan status akun Platinum Anda.</Notice>
            <button type="button" className="atlas-button" onClick={() => setPercobaan(value => value + 1)}>
              Coba lagi
            </button>
          </div>
        )}
      </div>
    </>
  )
}
