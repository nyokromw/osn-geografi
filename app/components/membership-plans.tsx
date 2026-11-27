'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { ArrowRight, Check, MessageCircle } from 'lucide-react'
import { accessLabels, membershipFeatures, planWhatsAppLink, rupiah, type MembershipPlan } from '../lib/membership'
import { paymentConfig } from '../lib/payments'

export function MembershipPlans({ plans, loading, onFree, highlightPlanId }: {
  plans: MembershipPlan[]
  loading?: boolean
  onFree?: () => void
  highlightPlanId?: number | null
}) {
  const [sandboxCheckout, setSandboxCheckout] = useState(false)
  const inDashboard = !!onFree
  useEffect(() => {
    if (!inDashboard) return
    let active = true
    void paymentConfig().then(config => { if (active) setSandboxCheckout(config.test_available) })
    return () => { active = false }
  }, [inDashboard])

  if (!plans.length) {
    return <p className="mt-5 text-sm text-gray-600">{loading ? 'Memuat paket…' : 'Daftar paket belum tersedia.'}</p>
  }

  return (
    <>
      <div className="mt-6 grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        {plans.map(plan => {
          const free = plan.akses === 'gratis' && plan.harga === 0
          // Only compare a yearly individual plan with its monthly sibling (never the class package).
          const monthly = plan.durasi_hari === 365 && plan.jenis !== 'kelas'
            ? plans.find(item => item.akses === plan.akses && item.durasi_hari === 30 && item.jenis !== 'kelas')
            : undefined
          const annualComparison = monthly ? monthly.harga * 12 : 0
          const highlighted = plan.id === highlightPlanId
          return (
            <article key={plan.id} id={highlighted ? `membership-plan-${plan.id}` : undefined}
              tabIndex={highlighted ? -1 : undefined}
              data-access={plan.akses}
              className={`atlas-card plan-card flex flex-col p-4 sm:p-5 ${free ? 'sm:col-span-2 xl:col-span-1' : ''} ${highlighted ? 'scroll-mt-24 ring-2 ring-forest-500' : ''}`}>
              <span className="access-badge mb-3 self-start" data-access={plan.akses}>{accessLabels[plan.akses] ?? plan.akses}</span>
              <h3 className="font-bold text-forest-900">{plan.nama}</h3>
              {plan.aktif === false && (
                <p className="mt-1 text-xs font-semibold text-gray-600">Dalam persiapan</p>
              )}
              <p className="mt-3 text-2xl font-bold tabular-nums text-forest-900">{rupiah(plan.harga)}</p>
              <p className="mt-1 text-xs text-gray-600">{free ? 'Tanpa batas waktu' : `Untuk ${plan.durasi_hari} hari`}</p>
              {annualComparison > plan.harga && (
                <p className="mt-2 text-xs leading-relaxed text-forest-700">
                  <strong>Hemat {rupiah(annualComparison - plan.harga)}</strong> dari 12× harga bulanan ({rupiah(annualComparison)}).
                </p>
              )}
              {plan.deskripsi && <p className="mt-3 text-sm leading-relaxed text-gray-600">{plan.deskripsi}</p>}
              <ul className="my-4 space-y-2 text-sm leading-snug text-gray-700">
                {membershipFeatures(plan.fitur).map((feature, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <Check size={14} aria-hidden="true" className="mt-0.5 shrink-0 text-forest-600" />{feature}
                  </li>
                ))}
              </ul>
              <div className="mt-auto">
                {free ? (
                  onFree ? (
                    <button type="button" onClick={onFree} className="atlas-button atlas-button--primary w-full">
                      Lihat tryout <ArrowRight size={15} aria-hidden="true" />
                    </button>
                  ) : (
                    <Link href="/register" className="atlas-button atlas-button--primary w-full">
                      Mulai gratis <ArrowRight size={15} aria-hidden="true" />
                    </Link>
                  )
                ) : (
                  <a className="atlas-button w-full" href={planWhatsAppLink(plan)} target="_blank" rel="noreferrer"
                    aria-label={`${plan.aktif ? 'Pesan' : 'Tanya'} ${plan.nama} via WhatsApp`}>
                    <MessageCircle size={15} className="shrink-0" aria-hidden="true" />{plan.aktif ? 'Pesan via WhatsApp' : 'Tanya via WhatsApp'}
                  </a>
                )}
                {!free && plan.aktif && plan.jenis !== 'kelas' && sandboxCheckout && <Link href={`/pembayaran?paket=${plan.id}`}
                  className="atlas-link mt-3 block text-center text-sm">Uji QRIS (admin)</Link>}
              </div>
            </article>
          )
        })}
      </div>
      <p className="mt-4 max-w-prose text-sm leading-relaxed text-gray-600">
        Pemesanan paket melalui WhatsApp. Admin mengaktifkan akses setelah pembayaran diverifikasi.
      </p>
    </>
  )
}
