'use client'

import { useEffect, useId, useRef, useState } from 'react'
import { ArrowRight, ChartNoAxesCombined, ClipboardList, Crosshair, Lightbulb, TrendingDown, TrendingUp, Trophy } from 'lucide-react'
import './progress.css'

export type StudyResult = {
  id: number
  paket_id?: number | null
  created_at: string | null
  total_poin: number | null
  total_soal: number | null
  poin_benar: number | null
  poin_salah: number | null
  poin_kosong: number | null
  paket_to?: { nama: string } | null
  paket_pendalaman?: { nama: string } | null
}

type Mode = 'tryout' | 'latihan'
type Metric = 'points' | 'correct'
type Counts = [benar: number, salah: number, kosong: number]
type Session = {
  id: number
  title: string
  date: string
  points: number | null
  correct: number | null
  counts: Counts | null
}

const SESSION_LIMIT = 12
const dateFormat = new Intl.DateTimeFormat('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })
const numberFormat = new Intl.NumberFormat('id-ID')
const answerLabels = ['Benar', 'Salah', 'Kosong']
const answerColors = ["#396957", "#983f29", "#dcd3c4"]

function countIsValid(value: number | null): value is number {
  return value !== null && Number.isInteger(value) && value >= 0
}

function prepareSessions(results: StudyResult[], mode: Mode): Session[] {
  return results.slice(-SESSION_LIMIT).map(row => {
    const { poin_benar: correct, poin_salah: wrong, poin_kosong: blank } = row
    const counts: Counts | null = countIsValid(correct) && countIsValid(wrong) && countIsValid(blank)
      ? [correct, wrong, blank] : null
    const counted = counts?.reduce((sum, count) => sum + count, 0) ?? 0
    const total = countIsValid(row.total_soal) && row.total_soal > 0 ? row.total_soal : counted
    const date = row.created_at ? new Date(row.created_at) : null

    return {
      id: row.id,
      title: (mode === 'tryout' ? row.paket_to?.nama : row.paket_pendalaman?.nama)
        || (mode === 'tryout' ? 'Tryout' : 'Pendalaman materi'),
      date: date && Number.isFinite(date.getTime()) ? dateFormat.format(date) : 'Tanggal belum tercatat',
      points: typeof row.total_poin === 'number' && Number.isFinite(row.total_poin) ? row.total_poin : null,
      correct: countIsValid(correct) && total > 0 && correct <= total ? Math.round(correct / total * 100) : null,
      counts: counted ? counts : null,
    }
  })
}

function formatMetric(value: number, metric: Metric) {
  return numberFormat.format(value) + (metric === 'correct' ? '%' : ' poin')
}

function TrendPlot({ values, metric, selectedId, select }: {
  values: { session: Session; value: number; index: number }[]
  metric: Metric
  selectedId: number | undefined
  select: (id: number) => void
}) {
  const [width, setWidth] = useState(500)
  const container = useRef<HTMLDivElement>(null)
  const gradient = useId()

  useEffect(() => {
    const element = container.current
    if (!element) return
    const observer = new ResizeObserver(([entry]) => {
      setWidth(Math.max(220, Math.round(entry.contentRect.width)))
    })
    observer.observe(element)
    return () => observer.disconnect()
  }, [])

  const left = width < 350 ? 37 : 44
  const right = width - 15
  const top = 14
  const bottom = 172
  const scores = values.map(point => point.value)
  const minScore = Math.min(0, ...scores)
  const maxScore = Math.max(1, ...scores)
  const step = metric === 'correct' ? 25 : Math.max(1, Math.ceil((maxScore - minScore) / 4))
  const minimum = metric === 'correct' ? 0 : Math.floor(minScore / step) * step
  const maximum = metric === 'correct' ? 100 : Math.ceil(maxScore / step) * step
  const ticks = Array.from({ length: Math.round((maximum - minimum) / step) + 1 }, (_, i) => minimum + i * step)
  const ordinate = (value: number) => bottom - (value - minimum) / (maximum - minimum) * (bottom - top)

  const points = values.map((point, index) => ({
    ...point,
    x: values.length === 1 ? (left + right) / 2 : left + (right - left) * index / (values.length - 1),
    y: ordinate(point.value),
  }))
  const path = points.map(({ x, y }, index) => (index ? 'L ' : 'M ') + x + ' ' + y).join(' ')
  const first = points[0]
  const last = points[points.length - 1]
  const area = points.length > 1 ? path + ' L ' + last.x + ' ' + bottom + ' H ' + first.x + ' Z' : ''
  const mean = scores.reduce((sum, value) => sum + value, 0) / (scores.length || 1)
  const bestValue = Math.max(...scores)

  return (
    <div ref={container} className="progress-plot">
      <svg viewBox={'0 0 ' + width + ' 219'} width="100%" height="219" role="group"
        aria-label={metric === 'correct' ? 'Grafik persentase jawaban benar' : 'Grafik poin per sesi'}>
        <defs>
          <linearGradient id={gradient} x1="0" x2="0" y1="0" y2="1">
            <stop offset="0" stopColor="#396957" stopOpacity=".19" />
            <stop offset="1" stopColor="#396957" stopOpacity=".025" />
          </linearGradient>
        </defs>
        {ticks.map(tick => (
          <g key={tick} aria-hidden="true">
            <line className={tick === 0 ? 'progress-grid progress-grid--base' : 'progress-grid'}
              x1={left} x2={right} y1={ordinate(tick)} y2={ordinate(tick)} />
            <text className="progress-axis" x={left - 8} y={ordinate(tick)} textAnchor="end" dominantBaseline="middle">
              {numberFormat.format(tick)}{metric === 'correct' ? '%' : ''}
            </text>
          </g>
        ))}
        {area && <path d={area} fill={'url(#' + gradient + ')'} aria-hidden="true" />}
        {points.length > 1 && <path d={path} className="progress-line" aria-hidden="true" />}
        {points.length > 1 && (
          <g aria-hidden="true">
            <line className="progress-mean" x1={left} x2={right} y1={ordinate(mean)} y2={ordinate(mean)} />
            <text className="progress-mean-label" x={right} y={ordinate(mean) - 6} textAnchor="end">
              rata-rata {numberFormat.format(Math.round(mean))}{metric === 'correct' ? '%' : ''}
            </text>
          </g>
        )}
        {points.map(({ x, y, session, index, value }, i) => (
          <g key={session.id} className="progress-point" role="button" tabIndex={0}
            aria-label={'Sesi ' + (index + 1) + ', ' + session.title + ', ' + formatMetric(value, metric)}
            aria-pressed={session.id === selectedId}
            onClick={() => select(session.id)} onFocus={() => select(session.id)}
            onPointerEnter={() => select(session.id)}
            onKeyDown={event => {
              if (event.key !== 'Enter' && event.key !== ' ') return
              event.preventDefault()
              select(session.id)
            }}>
            <circle className="progress-point-hit" cx={x} cy={y} r={13} fill="transparent" />
            <circle className="progress-dot" data-best={values.length > 1 && value === bestValue} cx={x} cy={y} r={session.id === selectedId ? 5.5 : 3.8} />
            {(width >= 400 || i % 2 === 0 || i === points.length - 1) && (
              <text className="progress-axis" x={x} y={bottom + 18} textAnchor="middle" aria-hidden="true">{index + 1}</text>
            )}
          </g>
        ))}
        <text className="progress-axis" x={(left + right) / 2} y={211} textAnchor="middle" aria-hidden="true">Urutan sesi</text>
      </svg>
    </div>
  )
}

function AnswerComposition({ session }: { session: Session | undefined }) {
  const counts = session?.counts
  if (!counts) return <p className="progress-empty">Rincian jawaban untuk sesi ini belum tersedia.</p>

  const total = counts.reduce((sum, count) => sum + count, 0)
  const correctStop = counts[0] / total * 100
  const wrongStop = (counts[0] + counts[1]) / total * 100
  const fill = 'conic-gradient(' + answerColors[0] + ' 0 ' + correctStop + '%, ' +
    answerColors[1] + ' ' + correctStop + '% ' + wrongStop + '%, ' + answerColors[2] + ' ' + wrongStop + '% 100%)'

  return (
    <div className="progress-composition">
      <div className="progress-donut" style={{ backgroundImage: fill }} aria-hidden="true">
        <div><strong>{numberFormat.format(total)}</strong><span>soal</span></div>
      </div>
      <dl className="progress-legend">
        {counts.map((count, index) => (
          <div key={answerLabels[index]}>
            <dt><span style={{ backgroundColor: answerColors[index] }} aria-hidden="true" />{answerLabels[index]}</dt>
            <dd>{numberFormat.format(count)} <span>soal</span></dd>
          </div>
        ))}
      </dl>
    </div>
  )
}

function average(values: number[]) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : null
}

function Insights({ sessions, metric }: { sessions: Session[]; metric: Metric }) {
  const values = sessions.flatMap(session => session[metric] === null ? [] : [session[metric] as number])
  const totals = sessions.reduce((sum, session) => {
    if (!session.counts) return sum
    return [sum[0] + session.counts[0], sum[1] + session.counts[1], sum[2] + session.counts[2]]
  }, [0, 0, 0])
  const answered = totals[0] + totals[1]
  const all = answered + totals[2]
  const precision = answered ? Math.round(totals[0] / answered * 100) : null
  const blankRate = all ? Math.round(totals[2] / all * 100) : null

  const recent = values.slice(-3)
  const before = values.slice(-6, -3)
  const trend = recent.length && before.length ? Math.round((average(recent) as number) - (average(before) as number)) : null
  const best = sessions.reduce<Session | null>((top, session) =>
    session[metric] !== null && (top === null || (session[metric] as number) > (top[metric] as number)) ? session : top, null)
  const unit = metric === 'correct' ? '%' : ' poin'

  const cards = [
    {
      Icon: trend !== null && trend < 0 ? TrendingDown : TrendingUp,
      tone: trend === null ? 'neutral' : trend >= 0 ? 'good' : 'warn',
      title: 'Arah kemajuan',
      value: trend === null ? '—' : (trend > 0 ? '+' : '') + numberFormat.format(trend) + unit,
      text: trend === null
        ? 'Selesaikan minimal 4 sesi untuk membandingkan 3 sesi terakhir dengan sebelumnya.'
        : trend > 0 ? 'Rata-rata 3 sesi terakhir lebih tinggi dari 3 sesi sebelumnya. Pertahankan!'
        : trend < 0 ? 'Rata-rata 3 sesi terakhir menurun. Ulangi topik yang sering salah sebelum tryout berikutnya.'
        : 'Hasilmu stabil. Coba paket yang sedikit lebih menantang.',
    },
    {
      Icon: Crosshair,
      tone: precision === null ? 'neutral' : precision >= 70 ? 'good' : precision >= 50 ? 'neutral' : 'warn',
      title: 'Ketepatan menjawab',
      value: precision === null ? '—' : precision + '%',
      text: precision === null ? 'Rincian jawaban belum tersedia.'
        : `Dari ${numberFormat.format(answered)} soal yang kamu jawab, ${precision}% benar.` +
          (precision < 50 ? ' Fokus pada pemahaman konsep sebelum menambah kecepatan.' : ''),
    },
    {
      Icon: Lightbulb,
      tone: blankRate === null ? 'neutral' : blankRate > 25 ? 'warn' : 'good',
      title: 'Soal dikosongkan',
      value: blankRate === null ? '—' : blankRate + '%',
      text: blankRate === null ? 'Rincian jawaban belum tersedia.'
        : blankRate > 25 ? 'Cukup banyak soal kosong. Dengan skor +4/−1, menjawab setelah mengeliminasi opsi yang jelas salah biasanya lebih menguntungkan.'
        : 'Kamu menjawab hampir semua soal. Bagus untuk manajemen waktu.',
    },
    {
      Icon: Trophy,
      tone: 'good',
      title: 'Sesi terbaik',
      value: best ? numberFormat.format(best[metric] as number) + unit : '—',
      text: best ? `${best.title} · ${best.date}` : 'Belum ada sesi dengan nilai tercatat.',
    },
  ]

  return (
    <div className="progress-insights" aria-label="Analisis otomatis">
      {cards.map(({ Icon, tone, title, value, text }) => (
        <article key={title} className="progress-insight" data-tone={tone}>
          <div className="progress-insight-head">
            <span className="progress-insight-icon"><Icon size={16} aria-hidden="true" /></span>
            <h4>{title}</h4>
          </div>
          <strong>{value}</strong>
          <p>{text}</p>
        </article>
      ))}
    </div>
  )
}

export function LearningProgress({ tryouts, practices, loadErrors, openPractice }: {
  tryouts: StudyResult[]
  practices: StudyResult[]
  loadErrors: { tryout: boolean; latihan: boolean }
  openPractice: (mode: Mode) => void
}) {
  const [mode, setMode] = useState<Mode>(tryouts.length || !practices.length ? 'tryout' : 'latihan')
  const [metric, setMetric] = useState<Metric>('points')
  const [selectedId, setSelectedId] = useState<number>()
  const sessions = prepareSessions(mode === 'tryout' ? tryouts : practices, mode)
  const values = sessions.flatMap((session, index) => {
    const value = session[metric]
    return value === null ? [] : [{ session, index, value }]
  })
  const selected = sessions.find(session => session.id === selectedId) ?? sessions[sessions.length - 1]
  const selectedValue = selected?.[metric]

  return (
    <section aria-labelledby="learning-progress-title">
      <header className="mb-4 flex flex-wrap items-end justify-between gap-3">
        <div>
          <span className="dash-eyebrow">Analisis belajar</span>
          <h2 className="atlas-subtitle" id="learning-progress-title">Kemajuan belajar</h2>
          <p className="mt-1 text-sm text-gray-500">Dihitung dari {SESSION_LIMIT} hasil terakhir. Klik titik grafik untuk melihat detail sesi.</p>
        </div>
        <div className="progress-toggle" role="group" aria-label="Jenis hasil">
          <button type="button" aria-pressed={mode === 'tryout'} onClick={() => { setMode('tryout'); setSelectedId(undefined) }}>Tryout</button>
          <button type="button" aria-pressed={mode === 'latihan'} onClick={() => { setMode('latihan'); setSelectedId(undefined) }}>Pendalaman</button>
        </div>
      </header>

      {sessions.length ? (
        <div className="progress-grid-layout">
          <article className="atlas-card progress-panel">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h3 className="flex items-center gap-2 font-bold">
                <ChartNoAxesCombined size={18} className="text-forest-600" aria-hidden="true" /> Tren hasil
              </h3>
              <div className="progress-toggle" role="group" aria-label="Ukuran grafik">
                <button type="button" aria-pressed={metric === 'points'} onClick={() => setMetric('points')}>Poin</button>
                <button type="button" aria-pressed={metric === 'correct'} onClick={() => setMetric('correct')}>% Benar</button>
              </div>
            </div>
            {values.length ? (
              <TrendPlot values={values} selectedId={selected?.id} metric={metric} select={setSelectedId} />
            ) : (
              <p className="progress-empty">Ukuran ini belum tercatat pada hasil yang tersedia.</p>
            )}
            {selected && (
              <div className="progress-selection">
                <div><strong>{selected.title}</strong><span>{selected.date}</span></div>
                <strong>{selectedValue === null || selectedValue === undefined ? '—' : formatMetric(selectedValue, metric)}</strong>
              </div>
            )}
          </article>
          <article className="atlas-card progress-panel">
            <h3 className="flex items-center gap-2 font-bold">
              <ClipboardList size={18} className="text-forest-600" aria-hidden="true" /> Komposisi jawaban
            </h3>
            <p className="mt-1 text-sm text-gray-500">{selected?.title}</p>
            <AnswerComposition session={selected} />
          </article>
          <Insights sessions={sessions} metric={metric} />
        </div>
      ) : (
        <div className="atlas-card flex flex-wrap items-center justify-between gap-4 p-5">
          <div>
            <h3 className="font-bold">{loadErrors[mode] ? 'Riwayat belum dapat dimuat' : 'Belum ada hasil'}</h3>
            <p className="mt-1 text-sm text-gray-500">
              {loadErrors[mode] ? 'Muat ulang halaman untuk mencoba lagi.' : 'Selesaikan satu sesi untuk melihat grafik kemajuanmu.'}
            </p>
          </div>
          {!loadErrors[mode] && (
            <button type="button" className="atlas-button atlas-button--primary" onClick={() => openPractice(mode)}>
              {mode === 'tryout' ? 'Lihat tryout' : 'Lihat latihan'} <ArrowRight size={17} aria-hidden="true" />
            </button>
          )}
        </div>
      )}
    </section>
  )
}
