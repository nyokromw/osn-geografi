import Link from 'next/link'
import { ArrowRight, Check, MessageCircle } from 'lucide-react'
import { membershipFeatures, planWhatsAppLink, rupiah, type MembershipPlan } from '../lib/membership'

export function MembershipPlans({ plans, loading, onFree }: {
  plans: MembershipPlan[]
  loading?: boolean
  onFree?: () => void
}) {
  if (!plans.length) {
    return <p className="mt-5 text-sm text-gray-600">{loading ? 'Memuat paket…' : 'Daftar paket belum tersedia.'}</p>
  }

  return (
    <>
      <div className="mt-6 grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        {plans.map(plan => {
          const free = plan.akses === 'gratis' && plan.harga === 0
          const monthly = plan.durasi_hari === 365
            ? plans.find(item => item.akses === plan.akses && item.durasi_hari === 30)
            : undefined
          const annualComparison = monthly ? monthly.harga * 12 : 0
          return (
            <article key={plan.id} className={`atlas-card flex flex-col p-4 sm:p-5 ${free ? 'sm:col-span-2 xl:col-span-1' : ''}`}>
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
              </div>
            </article>
          )
        })}
      </div>
      <p className="mt-4 max-w-prose text-sm leading-relaxed text-gray-600">
        Hubungi admin lewat WhatsApp untuk mengecek ketersediaan paket. Admin mengaktifkan akses setelah pembayaran diverifikasi.
      </p>
    </>
  )
}
