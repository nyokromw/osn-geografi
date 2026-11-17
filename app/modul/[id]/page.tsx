'use client'

import Link from 'next/link'
import { useParams, useRouter } from 'next/navigation'
import { useEffect, useId, useRef, useState } from 'react'
import { ArrowLeft, ChevronLeft, ChevronRight, List, Maximize, Minimize, X, ZoomIn, ZoomOut } from 'lucide-react'
import { Notice, PageLoading, WorkspaceHeader } from '../../components/atlas'
import { supabase } from '../../lib/supabase'

type EntriDaftarIsi = {
  judul: string
  halaman: number
  subbagian: boolean
}

type Modul = {
  id: number
  judul: string
  folder_halaman: string
  jumlah_halaman: number
  daftar_isi: { folder_halaman: string; entri: EntriDaftarIsi[] } | null
}

type ModulResult =
  | { id: string; modul: Modul }
  | { id: string; error: string }

const daftarModul = '/dashboard?tab=modul'
const kelasKonten = 'atlas-container mx-auto max-w-5xl py-6 sm:py-8'
const tombolIkon = 'atlas-button px-2.5! sm:px-3.5! disabled:opacity-40'

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
        .select('id, judul, folder_halaman, jumlah_halaman, daftar_isi')
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
      {modul ? <Pembaca key={modul.id} modul={modul} /> : (
        <>
          <KepalaPembaca />
          <main className={kelasKonten}><Notice error>{error}</Notice></main>
        </>
      )}
    </div>
  )
}

function KepalaPembaca() {
  return (
    <WorkspaceHeader title="Pembaca modul">
      <Link href={daftarModul} className="atlas-button">
        <ArrowLeft size={16} aria-hidden="true" /> Daftar modul
      </Link>
    </WorkspaceHeader>
  )
}

function Pembaca({ modul }: { modul: Modul }) {
  const [halaman, setHalaman] = useState(1)
  const [nomor, setNomor] = useState('1')
  const [zoom, setZoom] = useState(100)
  const [layarPenuh, setLayarPenuh] = useState(false)
  const [percobaan, setPercobaan] = useState(0)
  const [gambar, setGambar] = useState<{ halaman: number; percobaan: number; url: string | null } | null>(null)
  const areaPembaca = useRef<HTMLElement>(null)
  const areaHalaman = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const area = areaPembaca.current
    function sinkronLayarPenuh() {
      setLayarPenuh(document.fullscreenElement === area)
    }
    function tutupSaatEscape(event: KeyboardEvent) {
      if (event.key === 'Escape' && !document.fullscreenElement && !area?.querySelector('dialog[open]')) {
        setLayarPenuh(false)
      }
    }
    document.addEventListener('fullscreenchange', sinkronLayarPenuh)
    document.addEventListener('keydown', tutupSaatEscape)
    return () => {
      document.removeEventListener('fullscreenchange', sinkronLayarPenuh)
      document.removeEventListener('keydown', tutupSaatEscape)
    }
  }, [])

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
    if (next !== halaman) {
      areaHalaman.current?.scrollTo({ top: 0, left: 0, behavior: 'auto' })
      if (!layarPenuh) window.scrollTo({ top: 0, behavior: 'auto' })
    }
  }

  function ubahLayarPenuh() {
    const area = areaPembaca.current
    if (layarPenuh) {
      if (area && document.fullscreenElement === area) {
        void document.exitFullscreen().catch(() => {})
      } else {
        setLayarPenuh(false)
      }
      return
    }

    setLayarPenuh(true)
    if (document.fullscreenEnabled && area?.requestFullscreen) {
      void area.requestFullscreen().catch(() => {
        // Keep the in-page full viewport when the browser declines fullscreen.
      })
    }
  }

  const tampil = gambar?.halaman === halaman && gambar.percobaan === percobaan ? gambar : null
  const daftarIsi = modul.daftar_isi
  const entriDaftarIsi = daftarIsi?.folder_halaman === modul.folder_halaman && Array.isArray(daftarIsi.entri)
    ? daftarIsi.entri.filter(entri => typeof entri?.judul === 'string' && entri.judul.trim() &&
      Number.isInteger(entri.halaman) && entri.halaman >= 1 && entri.halaman <= modul.jumlah_halaman)
    : []
  const labelLayarPenuh = layarPenuh ? 'Keluar layar penuh' : 'Layar penuh'
  const ukuranGambar = layarPenuh ? { maxWidth: zoom + '%', maxHeight: zoom + '%' } : { width: zoom + '%' }

  return (
    <>
      {!layarPenuh && <KepalaPembaca />}
      <main ref={areaPembaca} className={layarPenuh ? 'fixed inset-0 z-40 flex h-dvh flex-col bg-gray-50' : kelasKonten}>
        <h1 className={layarPenuh ? 'sr-only' : 'mb-4 text-xl font-bold text-gray-900 sm:text-2xl'}>{modul.judul}</h1>
        <div className={'atlas-card z-10 flex flex-wrap items-center justify-between gap-2 p-2.5 sm:p-3 ' +
          (layarPenuh ? 'm-2 mt-[max(0.5rem,env(safe-area-inset-top))] shrink-0' : 'sticky top-[4.25rem] mb-4')}>
          <div className="flex items-center gap-1.5">
            <button type="button" className={tombolIkon} aria-label="Halaman sebelumnya"
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
            <button type="button" className={tombolIkon} aria-label="Halaman berikutnya"
              disabled={halaman === modul.jumlah_halaman} onClick={() => bukaHalaman(halaman + 1)}>
              <ChevronRight size={18} aria-hidden="true" />
            </button>
          </div>
          <div className="flex flex-wrap items-center gap-1.5">
            {entriDaftarIsi.length > 0 && (
              <DaftarIsiModul entri={entriDaftarIsi} halaman={halaman} onNavigate={bukaHalaman} />
            )}
            <button type="button" className={tombolIkon} aria-label={labelLayarPenuh} title={labelLayarPenuh}
              onClick={ubahLayarPenuh}>
              {layarPenuh ? <Minimize size={17} aria-hidden="true" /> : <Maximize size={17} aria-hidden="true" />}
              <span className="hidden sm:inline">{labelLayarPenuh}</span>
            </button>
            <div className="flex items-center gap-1.5">
              <button type="button" className={tombolIkon} aria-label="Perkecil"
                disabled={zoom === 100} onClick={() => setZoom(zoom - 25)}>
                <ZoomOut size={17} aria-hidden="true" />
              </button>
              <span className="min-w-9 text-center text-sm tabular-nums text-gray-600">{zoom}%</span>
              <button type="button" className={tombolIkon} aria-label="Perbesar"
                disabled={zoom === 200} onClick={() => setZoom(zoom + 25)}>
                <ZoomIn size={17} aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
        <div ref={areaHalaman} aria-busy={!tampil}
          className={'overflow-auto bg-gray-100 ' + (layarPenuh
            ? 'flex min-h-0 flex-1 flex-col overscroll-contain p-2 sm:p-4'
            : 'rounded-xl p-1 sm:p-3')}>
          {!tampil ? (
            <p className="px-3 py-16 text-center text-sm text-gray-600" role="status">Memuat halaman {halaman}…</p>
          ) : tampil.url ? (
            // The app holds a short-lived blob URL for one authorized page.
            // eslint-disable-next-line @next/next/no-img-element
            <img src={tampil.url} alt={'Halaman ' + halaman + ' — ' + modul.judul}
              className={'mx-auto block h-auto select-none bg-white ' +
                (layarPenuh ? 'my-auto w-auto shrink-0 shadow-md' : 'max-w-none')}
              style={ukuranGambar} draggable={false} onContextMenu={event => event.preventDefault()} />
          ) : (
            <div className="space-y-3 p-4">
              <Notice error>Halaman ini gagal dimuat. Periksa koneksi dan status akun Platinum Anda.</Notice>
              <button type="button" className="atlas-button" onClick={() => setPercobaan(value => value + 1)}>
                Coba lagi
              </button>
            </div>
          )}
        </div>
      </main>
    </>
  )
}

function DaftarIsiModul({ entri, halaman, onNavigate }: {
  entri: EntriDaftarIsi[]
  halaman: number
  onNavigate: (halaman: number) => void
}) {
  const dialog = useRef<HTMLDialogElement>(null)
  const judulId = useId()
  const aktif = entri.findIndex(item => item.halaman === halaman)

  return (
    <>
      <button type="button" className="atlas-button whitespace-nowrap" aria-haspopup="dialog"
        onClick={() => dialog.current?.showModal()}>
        <List size={18} aria-hidden="true" /> Daftar isi
      </button>
      <dialog ref={dialog} aria-labelledby={judulId}
        className="atlas-card fixed inset-0 m-auto max-h-[min(84dvh,42rem)] w-[calc(100%_-_1.5rem)] max-w-lg overflow-y-auto p-0 text-gray-900 shadow-xl backdrop:bg-black/45">
        <div className="sticky top-0 z-10 flex items-center justify-between gap-3 border-b border-gray-200 bg-white px-4 py-3">
          <h2 id={judulId} className="text-lg font-bold">Daftar isi</h2>
          <form method="dialog">
            <button type="submit" className="atlas-button" aria-label="Tutup daftar isi">
              <X size={18} aria-hidden="true" />
            </button>
          </form>
        </div>
        <ol className="space-y-0.5 p-2">
          {entri.map((item, index) => (
            <li key={item.halaman + '-' + item.judul}>
              <button type="button" aria-current={index === aktif ? 'page' : undefined}
                className={'flex min-h-11 w-full items-center justify-between gap-3 rounded-md px-3 py-2 text-left text-sm hover:bg-gray-100 focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-forest-700 aria-[current=page]:bg-forest-100 ' +
                  (item.subbagian ? 'pl-6' : 'font-semibold')}
                onClick={() => {
                  dialog.current?.close()
                  onNavigate(item.halaman)
                }}>
                <span>{item.judul}</span>
                <span className="shrink-0 tabular-nums text-gray-600">
                  <span className="sr-only">Halaman </span>{item.halaman}
                </span>
              </button>
            </li>
          ))}
        </ol>
      </dialog>
    </>
  )
}
