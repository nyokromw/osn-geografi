'use client'

import type { ReactNode } from 'react'
import { ArrowDownRight, ArrowRight, ArrowUpRight, Flame, Minus } from 'lucide-react'

export type ActivityRow = { created_at: string | null }
export type ScoreRow = {
  total_poin: number | null
  total_soal: number | null
  poin_benar: number | null
  poin_salah: number | null
  poin_kosong: number | null
}

const numberFormat = new Intl.NumberFormat('id-ID')
const dayFormat = new Intl.DateTimeFormat('id-ID', { weekday: 'long', day: 'numeric', month: 'long' })
const monthFormat = new Intl.DateTimeFormat('id-ID', { month: 'short' })

export function accuracy(row: ScoreRow): number | null {
  const total = row.total_soal && row.total_soal > 0 ? row.total_soal
    : (row.poin_benar ?? 0) + (row.poin_salah ?? 0) + (row.poin_kosong ?? 0)
  if (row.poin_benar === null || !total) return null
  return Math.round(row.poin_benar / total * 100)
}

function dayKey(date: Date) {
  return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()
}

function startOfDay(date: Date) {
  const copy = new Date(date)
  copy.setHours(0, 0, 0, 0)
  return copy
}

export function activityByDay(rows: ActivityRow[]) {
  const days = new Map<string, number>()
  for (const row of rows) {
    if (!row.created_at) continue
    const date = new Date(row.created_at)
    if (!Number.isFinite(date.getTime())) continue
    const key = dayKey(date)
    days.set(key, (days.get(key) ?? 0) + 1)
  }
  return days
}

export function studyStreak(days: Map<string, number>) {
  const cursor = startOfDay(new Date())
  if (!days.has(dayKey(cursor))) cursor.setDate(cursor.getDate() - 1)
  let streak = 0
  while (days.has(dayKey(cursor))) {
    streak++
    cursor.setDate(cursor.getDate() - 1)
  }
  return streak
}

export function DashboardHero({ name, access, accessLabel, expiry, streak, children }: {
  name: string
  access: 'gratis' | 'premium' | 'platinum'
  accessLabel: string
  expiry?: string
  streak: number
  children?: ReactNode
}) {
  return (
    <section className="dash-hero" aria-labelledby="dash-hero-title">
      <div className="dash-hero-copy">
        <p className="dash-hero-date">{dayFormat.format(new Date())}</p>
        <h1 id="dash-hero-title">Halo, {name}!</h1>
        <p className="dash-hero-lead">
          {streak > 1
            ? `Kamu sudah belajar ${streak} hari berturut-turut. Pertahankan ritmenya!`
            : streak === 1 ? 'Ritme belajarmu sudah dimulai. Tambah satu sesi lagi besok untuk membangun kebiasaan.'
            : 'Yuk mulai sesi hari ini. Satu latihan kecil tetap membawa kemajuan.'}
        </p>
        <div className="dash-hero-meta">
          <span className="access-badge dash-hero-access" data-access={access}>Akses {accessLabel}</span>
          {expiry && <span className="dash-chip dash-chip--light">Aktif s.d. {expiry}</span>}
          {streak > 0 && <span className="dash-chip dash-chip--clay"><Flame size={14} aria-hidden="true" /> {streak} hari beruntun</span>}
        </div>
      </div>
      {children && <div className="dash-hero-actions">{children}</div>}
    </section>
  )
}

export function Delta({ value, unit = '' }: { value: number | null; unit?: string }) {
  if (value === null) return <span className="dash-delta" data-tone="flat">Belum ada pembanding</span>
  const tone = value > 0 ? 'up' : value < 0 ? 'down' : 'flat'
  const Icon = value > 0 ? ArrowUpRight : value < 0 ? ArrowDownRight : Minus
  return (
    <span className="dash-delta" data-tone={tone}>
      <Icon size={14} aria-hidden="true" />
      {(value > 0 ? '+' : '') + numberFormat.format(value) + unit} <span>dari sesi sebelumnya</span>
    </span>
  )
}

export function KpiCard({ label, value, unit, delta, deltaUnit, hint }: {
  label: string
  value: number | string | null
  unit?: string
  delta?: number | null
  deltaUnit?: string
  hint?: string
}) {
  return (
    <div className="dash-kpi">
      <dt>{label}</dt>
      <dd>
        <strong>{value === null ? '—' : typeof value === 'number' ? numberFormat.format(value) : value}</strong>
        {value !== null && unit && <span>{unit}</span>}
      </dd>
      {delta !== undefined ? <Delta value={delta} unit={deltaUnit} /> : hint && <p className="dash-kpi-hint">{hint}</p>}
    </div>
  )
}

const WEEKS = 15

export function ActivityHeatmap({ days }: { days: Map<string, number> }) {
  const today = startOfDay(new Date())
  const start = new Date(today)
  start.setDate(start.getDate() - ((today.getDay() + 6) % 7) - (WEEKS - 1) * 7)
  const columns = Array.from({ length: WEEKS }, (_, week) => Array.from({ length: 7 }, (_, weekday) => {
    const date = new Date(start)
    date.setDate(start.getDate() + week * 7 + weekday)
    return { date, count: date > today ? -1 : days.get(dayKey(date)) ?? 0 }
  }))
  const recent = columns.flat().filter(cell => cell.count > 0 && today.getTime() - cell.date.getTime() < 30 * 864e5)
  const total30 = recent.reduce((sum, cell) => sum + cell.count, 0)
  const activeDays = recent.length

  return (
    <article className="atlas-card dash-panel">
      <header className="dash-panel-head">
        <div>
          <h3>Aktivitas belajar</h3>
          <p>{total30} sesi di {activeDays} hari dalam 30 hari terakhir</p>
        </div>
      </header>
      <div className="dash-heatmap" role="img"
        aria-label={`Peta aktivitas ${WEEKS} minggu terakhir. ${total30} sesi dalam 30 hari terakhir.`}>
        <div className="dash-heatmap-days" aria-hidden="true"><span>Sen</span><span /><span>Rab</span><span /><span>Jum</span><span /><span>Min</span></div>
        <div className="dash-heatmap-grid">
          {columns.map((column, index) => (
            <div key={index} className="dash-heatmap-col">
              <span className="dash-heatmap-month" aria-hidden="true">
                {column[0].date.getDate() <= 7 ? monthFormat.format(column[0].date) : ''}
              </span>
              {column.map(({ date, count }) => (
                <span key={date.getTime()} className="dash-heatmap-cell"
                  data-level={count < 0 ? 'future' : Math.min(count, 4)}
                  title={count >= 0 ? `${date.toLocaleDateString('id-ID')}: ${count} sesi` : undefined} />
              ))}
            </div>
          ))}
        </div>
      </div>
      <div className="dash-heatmap-legend" aria-hidden="true">
        Sedikit {[0, 1, 2, 3, 4].map(level => <span key={level} className="dash-heatmap-cell" data-level={level} />)} Banyak
      </div>
    </article>
  )
}

export function QuickLink({ icon, label, detail, onClick }: { icon: ReactNode; label: string; detail: string; onClick: () => void }) {
  return (
    <button type="button" className="dash-quick" onClick={onClick}>
      <span className="dash-quick-icon">{icon}</span>
      <span className="grow"><strong>{label}</strong><small>{detail}</small></span>
      <ArrowRight size={16} aria-hidden="true" />
    </button>
  )
}

export function MeterBar({ value, label }: { value: number; label?: string }) {
  const clamped = Math.max(0, Math.min(100, value))
  return (
    <span className="dash-meter" role="img" aria-label={label ?? clamped + '%'}>
      <span style={{ width: clamped + '%' }} />
    </span>
  )
}
