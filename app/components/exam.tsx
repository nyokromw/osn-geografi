'use client'

import Link from 'next/link'
import { useEffect, useRef, useState, type ReactNode } from 'react'
import { ArrowLeft, ArrowRight, Check, Clock3, ListChecks, Maximize2, X } from 'lucide-react'
import { WorkspaceHeader } from './atlas'

const options = ['a', 'b', 'c', 'd', 'e'] as const

export type Question = {
  id: number
  pertanyaan: string
  jawaban_benar: string
  pembahasan?: string | null
  gambar_url?: string | null
} & Partial<Record<`pilihan_${typeof options[number]}`, string | null>>

export type ExamScore = { benar: number; salah: number; kosong: number; totalPoin: number }
type ExamMode = 'Tryout' | 'Latihan'
type Answers = Record<number, string>

function formatTime(seconds: number) {
  return [Math.floor(seconds / 3600), Math.floor(seconds / 60) % 60, seconds % 60]
    .map(value => String(value).padStart(2, '0')).join(':')
}

function ExamDialog({ title, close, children, large = false }: {
  title: string; close: () => void; children: ReactNode; large?: boolean
}) {
  const ref = useRef<HTMLDialogElement>(null)
  useEffect(() => {
    const dialog = ref.current
    if (!dialog) return
    dialog.showModal()
    return () => dialog.close()
  }, [])
  return (
    <dialog ref={ref} className={'atlas-dialog ' + (large ? 'atlas-dialog--large' : '')}
      onCancel={event => { event.preventDefault(); close() }} aria-label={title}>
      <div className="mb-4 flex items-center justify-between gap-4">
        <h2 className="font-semibold">{title}</h2>
        <button type="button" className="atlas-button shrink-0" onClick={close} aria-label="Tutup">
          <X size={18} aria-hidden="true" />
        </button>
      </div>
      {children}
    </dialog>
  )
}

export function ExamScreen({ mode, title, topic, timeLeft, questions, answers, index, onNavigate, onAnswer, onFinish }: {
  mode: ExamMode
  title: string
  topic?: string
  timeLeft?: number
  questions: Question[]
  answers: Answers
  index: number
  onNavigate: (index: number) => void
  onAnswer: (questionId: number, answer: string) => void
  onFinish: () => Promise<void>
}) {
  const [zoom, setZoom] = useState(false)
  const [confirm, setConfirm] = useState(false)
  const [saving, setSaving] = useState(false)
  const current = questions[index]
  const answered = questions.filter(item => !!answers[item.id]).length
  const remaining = questions.length - answered

  if (!current) return (
    <>
      <WorkspaceHeader title={mode} />
      <main className="atlas-container atlas-work-content">
        <section className="atlas-card max-w-xl p-6">
          <h1 className="atlas-title">Soal belum tersedia</h1>
          <p className="mt-2 text-gray-500">Pilih paket lain untuk melanjutkan latihan.</p>
          <Link href="/dashboard" className="atlas-button atlas-button--primary mt-5">Kembali ke dashboard</Link>
        </section>
      </main>
    </>
  )

  const progress = Math.round((index + 1) / questions.length * 100)
  return (
    <div className="atlas-exam">
      <header className="atlas-topbar">
        <div className="atlas-container atlas-topbar-inner atlas-exam-top">
          <Link href="/dashboard" className="atlas-link inline-flex items-center gap-1.5 whitespace-nowrap text-sm">
            <ArrowLeft size={17} aria-hidden="true" /> Keluar
          </Link>
          <div className="min-w-0 border-l border-gray-200 pl-3">
            <p className="atlas-exam-name">{title}</p>
            {topic && <p className="text-xs text-gray-500">{topic}</p>}
          </div>
          {timeLeft !== undefined ? (
            <span className={'atlas-exam-timer rounded-lg px-2 py-1.5 font-bold sm:px-3 ' +
              (timeLeft < 300 ? 'bg-red-100 text-red-700' : 'bg-forest-100 text-forest-800')}
              role="timer" aria-label="Waktu tersisa">
              <Clock3 size={16} className="shrink-0" aria-hidden="true" /> {formatTime(timeLeft)}
            </span>
          ) : (
            <span className="rounded-md bg-forest-100 px-2 py-1.5 text-xs font-semibold text-forest-800">Latihan</span>
          )}
        </div>
      </header>
      <div className="atlas-container atlas-exam-grid">
        <main className="atlas-exam-question atlas-card p-4 sm:p-6">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-x-3 gap-y-2">
            <p className="text-sm font-semibold text-gray-600">Soal {index + 1} dari {questions.length}</p>
            <div className="flex items-center gap-2">
              <div className="atlas-exam-progress h-1.5 overflow-hidden rounded-full bg-gray-200"
                role="progressbar" aria-label="Posisi soal" aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100}>
                <div className="h-full rounded-full bg-forest-500" style={{ width: progress + '%' }} />
              </div>
              <span className="text-xs tabular-nums text-gray-500">{progress}%</span>
            </div>
          </div>
          <h1 className="mb-4 whitespace-pre-line text-lg leading-relaxed font-semibold sm:text-xl">{current.pertanyaan}</h1>
          {current.gambar_url && (
            <button className="mb-4 block w-full rounded-lg border border-gray-200 p-2 text-sm text-gray-600"
              type="button" onClick={() => setZoom(true)} aria-label="Perbesar gambar soal">
              {/* Images uploaded by the admin can be hosted on external domains. */}
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={current.gambar_url} alt="Gambar soal" className="mx-auto max-h-[28rem] w-full object-contain" />
              <span className="mt-2 flex items-center justify-center gap-2">
                <Maximize2 size={14} aria-hidden="true" /> Perbesar gambar
              </span>
            </button>
          )}
          <div className="grid gap-2" aria-label="Pilihan jawaban" role="group">
            {options.map(option => {
              const value = current['pilihan_' + option as keyof Question]
              const letter = option.toUpperCase()
              const selected = answers[current.id] === letter
              if (!value) return null
              return (
                <button key={letter} type="button" aria-pressed={selected} onClick={() => onAnswer(current.id, letter)}
                  className={'atlas-exam-answer flex items-center gap-3 rounded-lg border px-3 py-2.5 text-left text-sm ' +
                    (selected ? 'border-forest-500 bg-forest-50 text-forest-800' : 'border-gray-200 text-gray-700 hover:border-forest-300 hover:bg-forest-50')}>
                  <span className={'grid size-7 shrink-0 place-items-center rounded-full font-bold ' +
                    (selected ? 'bg-forest-600 text-white' : 'bg-gray-100 text-gray-600')}>{letter}</span>
                  <span className="min-w-0 break-words">{value}</span>
                  {selected && <Check size={16} aria-hidden="true" className="ml-auto shrink-0 text-forest-600" />}
                </button>
              )
            })}
          </div>
          <div className="mt-5 flex flex-wrap items-center justify-between gap-2">
            <button type="button" className="atlas-button" disabled={index === 0} onClick={() => onNavigate(index - 1)}>
              <ArrowLeft size={15} className="hidden sm:block" aria-hidden="true" /> Sebelumnya
            </button>
            <button type="button" className="atlas-button atlas-button--primary" disabled={index + 1 === questions.length}
              onClick={() => onNavigate(index + 1)}>Selanjutnya <ArrowRight size={15} className="hidden sm:block" aria-hidden="true" /></button>
          </div>
          <a className="atlas-link mt-4 block text-sm md:hidden" href="#nomor-soal">Lihat daftar soal</a>
        </main>
        <aside className="atlas-exam-nav atlas-card scroll-mt-20" id="nomor-soal" aria-labelledby="exam-nav-title">
          <h2 id="exam-nav-title" className="flex items-center gap-2 font-bold">
            <ListChecks size={18} className="text-forest-600" aria-hidden="true" /> Daftar soal
          </h2>
          <div className="mt-4 grid grid-cols-5 gap-1.5 max-md:grid-cols-6">
            {questions.map((question, number) => (
              <button key={question.id} type="button" onClick={() => onNavigate(number)}
                aria-current={index === number ? 'step' : undefined} data-current={index === number}
                aria-label={'Soal ' + (number + 1) + (answers[question.id] ? ', sudah dijawab' : ', belum dijawab')}
                className={'atlas-exam-number min-h-9 rounded-md border border-gray-200 text-sm font-semibold tabular-nums ' +
                  (answers[question.id] ? 'bg-forest-100 text-forest-800' : 'bg-white text-gray-600 hover:bg-gray-100')}>
                {number + 1}
              </button>
            ))}
          </div>
          <p className="mt-4 text-sm text-gray-600"><strong className="text-forest-800">{answered}</strong> dari {questions.length} terjawab</p>
          <button className="atlas-button mt-4 w-full" type="button" onClick={() => setConfirm(true)}>
            Selesaikan {mode.toLowerCase()}
          </button>
        </aside>
      </div>
      {zoom && current.gambar_url && (
        <ExamDialog title="Gambar soal" close={() => setZoom(false)} large>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={current.gambar_url} alt="Gambar soal yang diperbesar" className="mx-auto max-h-[75vh] object-contain" />
        </ExamDialog>
      )}
      {confirm && (
        <ExamDialog title={'Selesaikan ' + mode.toLowerCase() + '?'} close={() => { if (!saving) setConfirm(false) }}>
          <p className="text-sm text-gray-600">
            Kamu sudah menjawab {answered} dari {questions.length} soal.
            {remaining > 0 && <strong className="ml-1 text-clay-500">{remaining} soal masih kosong.</strong>}
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            <button className="atlas-button grow" type="button" disabled={saving} onClick={() => setConfirm(false)}>Lanjutkan</button>
            <button className="atlas-button atlas-button--primary grow" type="button" disabled={saving}
              onClick={async () => {
                if (saving) return
                setSaving(true)
                try { await onFinish() } finally { setSaving(false) }
              }}>{saving ? 'Menyimpan…' : 'Kirim jawaban'}</button>
          </div>
        </ExamDialog>
      )}
    </div>
  )
}

export function ExamResults({ mode, title, score, questions, answers, offer }: {
  mode: ExamMode; title: string; score: ExamScore; questions: Question[]; answers: Answers; offer?: ReactNode
}) {
  // The exam screen is usually scrolled to the question list when it is submitted; start the result at the score.
  useEffect(() => { window.scrollTo({ top: 0, behavior: 'auto' }) }, [])
  return (
    <>
      <WorkspaceHeader title={'Hasil ' + mode.toLowerCase()} />
      <main className="atlas-container atlas-work-content">
        <section className="atlas-exam-result mx-auto">
          <h1 className="atlas-title">{mode} selesai</h1>
          <p className="mt-2 text-gray-500">{title}</p>
          <dl className="atlas-stat-strip mt-5">
            {[
              ['Total poin', score.totalPoin],
              ['Benar (+4)', score.benar],
              ['Salah (−1)', score.salah],
              ['Kosong (0)', score.kosong],
            ].map(([name, value]) => <div key={name}><dt>{name}</dt><dd>{value}</dd></div>)}
          </dl>
          {offer}
          <section className="mt-6" aria-labelledby="review-title">
            <h2 className="atlas-subtitle mb-3" id="review-title">Pembahasan</h2>
            <ol className="grid gap-2">
              {questions.map((question, index) => {
                const answer = answers[question.id]
                const color = !answer ? 'text-gray-600 bg-gray-100'
                  : answer === question.jawaban_benar ? 'text-forest-800 bg-forest-100' : 'text-red-700 bg-red-100'
                return (
                  <li key={question.id} className="atlas-card p-4">
                    <div className="flex gap-3">
                      <span className={'grid size-7 shrink-0 place-items-center rounded-full text-xs font-semibold ' + color}>{index + 1}</span>
                      <p className="whitespace-pre-line text-sm font-semibold">{question.pertanyaan}</p>
                    </div>
                    {question.gambar_url && (
                      /* eslint-disable-next-line @next/next/no-img-element */
                      <img src={question.gambar_url} alt="Gambar soal" className="mx-auto mt-3 max-h-80 w-full object-contain" loading="lazy" />
                    )}
                    <div className="mt-3 flex flex-wrap gap-3 text-sm text-gray-600">
                      <span>Jawaban kamu <strong>{answer || 'Kosong'}</strong></span>
                      <span>Jawaban benar <strong className="text-forest-700">{question.jawaban_benar}</strong></span>
                    </div>
                    {question.pembahasan && <p className="mt-3 whitespace-pre-line border-t border-gray-200 pt-3 text-sm text-gray-600">{question.pembahasan}</p>}
                  </li>
                )
              })}
            </ol>
          </section>
          <Link href="/dashboard" className="atlas-button atlas-button--primary mt-6">
            <ArrowLeft size={17} aria-hidden="true" /> Kembali ke dashboard
          </Link>
        </section>
      </main>
    </>
  )
}
