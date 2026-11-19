'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { rupiah } from '../lib/membership'
import { paymentDate, paymentStatusLabels, type PaymentOrder } from '../lib/payments'
import { supabase } from '../lib/supabase'

export function PaymentHistory() {
  const [orders, setOrders] = useState<PaymentOrder[]>([])
  const [failed, setFailed] = useState(false)
  useEffect(() => {
    let active = true
    async function load() {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) return
      const { data, error } = await supabase.from('pembayaran_midtrans').select('*').eq('user_id', user.id)
        .order('created_at', { ascending: false }).limit(10)
      if (active) { setOrders(data ?? []); setFailed(!!error) }
    }
    void load()
    return () => { active = false }
  }, [])
  if (!orders.length && !failed) return null
  return <section className="atlas-card mt-8 p-5">
    <h3 className="font-bold text-forest-900">Riwayat pembayaran QRIS</h3>
    {failed ? <p className="mt-3 text-sm text-gray-600">Riwayat belum dapat dimuat. Muat ulang halaman untuk mencoba lagi.</p>
      : <ul className="mt-3 divide-y divide-gray-200">{orders.map(order => <li key={order.order_id} className="flex flex-wrap items-center justify-between gap-3 py-4 text-sm">
        <div><strong>{order.nama_paket}</strong>{order.environment === 'sandbox' && <span className="ml-2 text-xs text-gray-500">Simulasi</span>}
          <p className="mt-1 text-gray-600">{rupiah(order.nominal)} · {paymentStatusLabels[order.status]}</p>
          <p className="mt-1 text-xs text-gray-500">{paymentDate(order.created_at)}</p></div>
        <Link href={'/pembayaran?pesanan=' + encodeURIComponent(order.order_id)} className="atlas-link">Lihat pembayaran</Link>
      </li>)}</ul>}
  </section>
}
