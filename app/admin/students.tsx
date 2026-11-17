'use client'

import { useEffect, useState } from 'react'
import { ChevronLeft, ChevronRight, Search } from 'lucide-react'
import { Notice } from '../components/atlas'
import { accessLabels, activeAccess, membershipExpiry } from '../lib/membership'
import { provinces } from '../lib/provinces'
import { defaultStudentFilters, loadStudentPage, studentPageSize, studentSortOptions, type StudentProfile } from './student-data'

const statuses = [
  ['gratis', 'Gratis'],
  ['premium', 'Premium aktif'],
  ['platinum', 'Platinum aktif'],
  ['akanHabis', 'Berakhir dalam 7 hari'],
  ['habis', 'Sudah berakhir'],
]
const colors = {
  gratis: 'bg-gray-100 text-gray-700',
  premium: 'bg-yellow-100 text-yellow-800',
  platinum: 'bg-purple-100 text-purple-800',
}
const dateFormat = new Intl.DateTimeFormat('id-ID', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'Asia/Jakarta' })
const numberFormat = new Intl.NumberFormat('id-ID')

function displayDate(value: string | null) {
  const date = value ? membershipExpiry(value) : NaN
  return Number.isFinite(date) ? dateFormat.format(date) : '—'
}

type PageResult = { key: string; rows: StudentProfile[]; count: number; error: boolean }

export function StudentRoster({ revision, onEdit }: { revision: number; onEdit: (profile: StudentProfile) => void }) {
  const [filters, setFilters] = useState(defaultStudentFilters)
  const [page, setPage] = useState(0)
  const [retry, setRetry] = useState(0)
  const [result, setResult] = useState<PageResult | null>(null)
  const queryKey = JSON.stringify([filters, page, revision, retry])
  const current = result?.key === queryKey ? result : null

  useEffect(() => {
    const controller = new AbortController()
    const load = async () => {
      const { data, error, count } = await loadStudentPage(filters, page, controller.signal)
      if (controller.signal.aborted) return
      if (error?.code === 'PGRST103' && page > 0) {
        setPage(0)
        return
      }
      if (!error && count !== null && page > 0 && page * studentPageSize >= count) {
        setPage(Math.max(0, Math.ceil(count / studentPageSize) - 1))
        return
      }
      setResult({ key: queryKey, rows: data ?? [], count: count ?? 0, error: !!error || count === null })
    }
    const timer = window.setTimeout(() => {
      void load().catch(() => {
        if (!controller.signal.aborted) setResult({ key: queryKey, rows: [], count: 0, error: true })
      })
    }, filters.search ? 250 : 0)

    return () => {
      window.clearTimeout(timer)
      controller.abort()
    }
  }, [filters, page, queryKey])

  function change<K extends keyof typeof filters>(name: K, value: (typeof filters)[K]) {
    setFilters(previous => ({ ...previous, [name]: value }))
    setPage(0)
  }

  const pageCount = Math.max(1, Math.ceil((current?.count ?? 0) / studentPageSize))
  const start = page * studentPageSize
  const showReset = Object.keys(defaultStudentFilters).some(key =>
    filters[key as keyof typeof filters] !== defaultStudentFilters[key as keyof typeof filters])

  return (
    <section aria-label="Daftar siswa">
      <div className="mb-5">
        <h2 className="text-xl font-black text-gray-800">Data Siswa</h2>
      </div>
      <div className="atlas-card mb-4 grid gap-3 p-4 sm:grid-cols-2 lg:grid-cols-4">
        <label className="block text-sm font-semibold text-gray-700 sm:col-span-2 lg:col-span-4">
          Cari siswa
          <span className="relative mt-1 block max-w-xl">
            <Search aria-hidden="true" size={17} className="pointer-events-none absolute left-3 top-3.5 text-gray-500" />
            <input type="search" maxLength={120} placeholder="Nama, email, atau nomor HP"
              value={filters.search} onChange={event => change('search', event.target.value)}
              className="atlas-field pl-9!" />
          </span>
        </label>
        <label className="block min-w-0 text-sm font-semibold text-gray-700">
          Provinsi
          <select className="atlas-field mt-1" value={filters.province} onChange={event => change('province', event.target.value)}>
            <option value="">Semua provinsi</option>
            <option value="kosong">Provinsi belum diisi</option>
            {provinces.map(province => <option key={province}>{province}</option>)}
          </select>
        </label>
        <label className="block min-w-0 text-sm font-semibold text-gray-700">
          Status paket
          <select className="atlas-field mt-1" value={filters.status} onChange={event => change('status', event.target.value)}>
            <option value="">Semua status</option>
            {statuses.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
          </select>
        </label>
        <label className="block min-w-0 text-sm font-semibold text-gray-700">
          Peran
          <select className="atlas-field mt-1" value={filters.role} onChange={event => change('role', event.target.value)}>
            <option value="">Semua peran</option>
            <option value="siswa">Siswa</option>
            <option value="admin">Admin</option>
          </select>
        </label>
        <label className="block min-w-0 text-sm font-semibold text-gray-700">
          Urutkan
          <select className="atlas-field mt-1" value={filters.sort}
            onChange={event => change('sort', event.target.value as keyof typeof studentSortOptions)}>
            {Object.entries(studentSortOptions).map(([value, { label }]) => <option key={value} value={value}>{label}</option>)}
          </select>
        </label>
      </div>
      <div className="mb-3 flex min-h-10 flex-wrap items-center justify-between gap-2">
        <p className="text-sm text-gray-600" role="status">
          {current?.error ? 'Data siswa gagal dimuat.' : current
            ? numberFormat.format(current.count) + ' akun ditemukan' : 'Memuat data siswa…'}
        </p>
        {showReset && (
          <button type="button" className="atlas-button" onClick={() => {
            setFilters(defaultStudentFilters)
            setPage(0)
          }}>Reset filter</button>
        )}
      </div>
      {current?.error && (
        <Notice error>
          <button type="button" className="atlas-link" onClick={() => setRetry(value => value + 1)}>Coba lagi</button>
        </Notice>
      )}
      {!current?.error && (
        <div className="atlas-card atlas-table-scroll" role="region" aria-label="Tabel data siswa" tabIndex={0} aria-busy={!current}>
          <table className="w-full min-w-[61rem] text-sm">
            <thead>
              <tr className="border-b border-gray-100 bg-gray-50">
                {['No', 'Nama dan email', 'Provinsi', 'Nomor HP', 'Peran', 'Status paket', 'Berakhir', 'Bergabung', 'Aksi'].map(label => (
                  <th key={label} scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-600">{label}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {current?.rows.map((student, index) => {
                const status = activeAccess(student)
                const recordedPlan = student.status
                const expired = status === 'gratis' && (recordedPlan === 'premium' || recordedPlan === 'platinum')
                return (
                  <tr key={student.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-xs tabular-nums text-gray-500">{start + index + 1}</td>
                    <td className="px-4 py-3">
                      <span className="block font-semibold text-gray-800">{student.nama || '—'}</span>
                      <span className="block break-all text-xs text-gray-600">{student.email || '—'}</span>
                    </td>
                    <td className="px-4 py-3">{student.provinsi || 'Belum diisi'}</td>
                    <td className="whitespace-nowrap px-4 py-3 tabular-nums">{student.nomor_hp || '—'}</td>
                    <td className="px-4 py-3">{student.role === 'admin' ? 'Admin' : 'Siswa'}</td>
                    <td className="px-4 py-3">
                      <span className={'rounded-full px-2 py-0.5 text-xs font-semibold ' + colors[status]}>{accessLabels[status]}</span>
                      {expired && <span className="mt-1 block text-xs text-gray-600">{accessLabels[recordedPlan]} berakhir</span>}
                    </td>
                    <td className="whitespace-nowrap px-4 py-3 text-xs text-gray-600">{displayDate(student.status_expired)}</td>
                    <td className="whitespace-nowrap px-4 py-3 text-xs text-gray-600">{displayDate(student.created_at)}</td>
                    <td className="px-4 py-3">
                      <button type="button" onClick={() => onEdit(student)}
                        className="rounded border border-forest-200 px-2 py-1 text-xs text-forest-700">Edit</button>
                    </td>
                  </tr>
                )
              })}
              {current?.count === 0 && (
                <tr><td colSpan={9} className="px-4 py-10 text-center text-gray-600">Tidak ada akun yang cocok dengan filter.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      )}
      {current && !current.error && current.count > studentPageSize && (
        <nav aria-label="Halaman data siswa" className="mt-4 flex flex-wrap items-center justify-between gap-2">
          <p className="text-sm tabular-nums text-gray-600">
            {numberFormat.format(start + 1)}–{numberFormat.format(Math.min(start + studentPageSize, current.count))}
            {' dari '}{numberFormat.format(current.count)} akun
          </p>
          <div className="flex items-center gap-2">
            <button type="button" className="atlas-button" disabled={page === 0}
              onClick={() => setPage(page - 1)} aria-label="Halaman siswa sebelumnya"><ChevronLeft size={17} /></button>
            <span className="px-1 text-sm tabular-nums text-gray-600">Halaman {page + 1} / {pageCount}</span>
            <button type="button" className="atlas-button" disabled={page + 1 >= pageCount}
              onClick={() => setPage(page + 1)} aria-label="Halaman siswa berikutnya"><ChevronRight size={17} /></button>
          </div>
        </nav>
      )}
    </section>
  )
}
