'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ArrowRight, Check, Lock, MessageCircle, Sparkles } from 'lucide-react'
import { supabase } from '../lib/supabase'
import { membershipFeatures, planWhatsAppLink, rupiah, type AccessLevel, type MembershipPlan } from '../lib/membership'
import { paymentConfig } from '../lib/payments'

type Offer = { plan: MembershipPlan; lockedTryouts: number; qris: boolean }

/** Shown on the result screen right after an exam: the moment a student most wants the next package. */
export function UpgradeOffer({ access, mode }: { access: AccessLevel; mode: 'Tryout' | 'Latihan' }) {
  const [offer, setOffer] = useState<Offer | null>(null)

  useEffect(() => {
    if (access === 'platinum') return
    let active = true
    const target: AccessLevel = access === 'gratis' ? 'premium' : 'platinum'
    void (async () => {
      const [plans, tryouts, config] = await Promise.all([
        supabase.from('paket_membership').select('*').eq('akses', target).eq('aktif', true).neq('jenis', 'kelas').order('harga'),
        supabase.from('paket_to').select('akses').eq('status', 'aktif'),
        paymentConfig(),
      ])
      const plan = (plans.data as MembershipPlan[] | null)?.[0]
      if (!active || !plan) return
      const rank: Record<string, number> = { gratis: 0, premium: 1, platinum: 2 }
      const lockedTryouts = (tryouts.data ?? []).filter(row => {
        const level = rank[row.akses ?? 'gratis'] ?? 0
        return level > rank[access] && level <= rank[target]
      }).length
      setOffer({ plan, lockedTryouts, qris: config.available })
    })()
    return () => { active = false }
  }, [access])

  if (!offer) return null
  const { plan, lockedTryouts, qris } = offer
  const features = membershipFeatures(plan.fitur).filter(item => !/^seluruh akses/i.test(item)).slice(0, 3)
  const tierName = plan.akses === 'premium' ? 'Premium' : 'Platinum'

  return (
    <aside className="upgrade-offer mt-6" aria-labelledby="upgrade-offer-title">
      <span className="upgrade-offer-eyebrow"><Sparkles size={14} aria-hidden="true" /> {mode === 'Tryout' ? 'Lanjutkan latihanmu' : 'Siap naik level?'}</span>
      <h2 id="upgrade-offer-title" className="upgrade-offer-title">
        {lockedTryouts > 0
          ? <>Masih ada <strong>{lockedTryouts} paket tryout</strong> lain dengan pembahasan di {tierName}.</>
          : <>Buka materi {tierName} untuk persiapan yang lebih lengkap.</>}
      </h2>
      {features.length > 0 && (
        <ul className="upgrade-offer-list">
          {features.map(feature => <li key={feature}><Check size={15} aria-hidden="true" />{feature}</li>)}
        </ul>
      )}
      <div className="upgrade-offer-actions">
        {qris ? (
          <Link href={`/pembayaran?paket=${plan.id}`} className="atlas-button atlas-button--primary">
            Buka {tierName} · {rupiah(plan.harga)} <ArrowRight size={15} aria-hidden="true" />
          </Link>
        ) : (
          <a href={planWhatsAppLink(plan)} target="_blank" rel="noreferrer" className="atlas-button atlas-button--primary">
            <MessageCircle size={15} aria-hidden="true" /> Pesan {tierName} · {rupiah(plan.harga)}
          </a>
        )}
        <Link href="/dashboard?tab=paket" className="atlas-button">
          <Lock size={15} aria-hidden="true" /> Bandingkan paket
        </Link>
      </div>
      <p className="upgrade-offer-note">{plan.nama} · aktif {plan.durasi_hari} hari setelah pembayaran diverifikasi.</p>
    </aside>
  )
}
