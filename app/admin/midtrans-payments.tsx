'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { Notice } from '../components/atlas'
import { rupiah } from '../lib/membership'
import { paymentConfig, paymentDate, paymentStatusLabels, type PaymentConfig, type PaymentOrder } from '../lib/payments'
import { supabase } from '../lib/supabase'

type AdminOrder = PaymentOrder & { profiles: { nama: string | null } | null }

export function MidtransPayments() {
  const [config, setConfig] = useState<PaymentConfig | null>(null)
  const [orders, setOrders] = useState<AdminOrder[]>([])
  const [environment, setEnvironment] = useState('production')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [revision, setRevision] = useState(0)
  useEffect(() => {
    let active = true
    async function load() {
      setLoading(true)
      const [settings, result] = await Promise.all([
        paymentConfig(),
        supabase.from('pembayaran_midtrans').select('*, profiles(nama)').eq('environment', environment)
          .order('created_at', { ascending: false }).limit(50).overrideTypes<AdminOrder[], { merge: false }>(),
      ])
      if (active) {
        setConfig(settings); setOrders(result.data ?? [])
        setError(result.error ? 'Riwayat pembayaran QRIS gagal dimuat.' : ''); setLoading(false)
      }
    }
    void load()
    return () => { active = false }
  }, [environment, revision])

  return <section className="mb-8 rounded-xl border border-gray-200 bg-white p-5">
    <div className="flex flex-wrap items-center justify-between gap-3">
      <h2 className="text-xl font-bold text-forest-900">Pembayaran QRIS Midtrans</h2>
      <button type="button" className="atlas-button text-sm" disabled={loading} onClick={() => setRevision(value => value + 1)}>Muat ulang</button>
    </div>
    {config && !config.available && <div className="my-4 rounded-lg bg-gray-50 p-4 text-sm leading-relaxed">
      <p className="font-semibold">{config.test_available ? 'Mode uji admin aktif' : 'Pembayaran otomatis belum diaktifkan'}</p>
      <p className="mt-2">Pelanggan tetap dapat memesan melalui WhatsApp. Simulasi tidak mengubah keanggotaan akun.</p>
      {!config.test_available && <p className="mt-2">Untuk mulai menguji, tambahkan <code>MIDTRANS_SANDBOX_SERVER_KEY</code> di pengaturan rahasia Edge Functions dan gunakan <code>MIDTRANS_ENVIRONMENT=sandbox</code>.</p>}
      <div className="mt-3 flex flex-wrap gap-4">
        <a className="atlas-link" href="https://supabase.com/dashboard/project/lhzlcaxlemlmjhfmichz/functions/secrets" target="_blank" rel="noreferrer">Pengaturan kunci pembayaran</a>
        <a className="atlas-link" href="https://github.com/nyokromw/osn-geografi/blob/main/docs/midtrans-qris.md" target="_blank" rel="noreferrer">Panduan aktivasi</a>
        {config.test_available && <Link className="atlas-link" href="/dashboard?tab=paket">Uji pembelian paket</Link>}
      </div>
    </div>}
    {config?.available && <p className="my-3 text-sm text-forest-700">Pembayaran pelanggan aktif. Akses akun diproses otomatis setelah pembayaran terverifikasi.</p>}
    <label className="mt-4 block text-sm">Jenis transaksi
      <select className="atlas-field mt-1 max-w-xs" value={environment} onChange={event => setEnvironment(event.target.value)}>
        <option value="production">Pembayaran pelanggan</option><option value="sandbox">Simulasi admin</option>
      </select>
    </label>
    {error && <div className="mt-4"><Notice error>{error}</Notice></div>}
    <div className="atlas-table-scroll mt-4"><table className="w-full text-left text-sm">
      <thead><tr className="border-b border-gray-200"><th className="p-3">Siswa dan pesanan</th><th className="p-3">Paket</th><th className="p-3">Nominal</th><th className="p-3">Status</th><th className="p-3">Masa aktif</th></tr></thead>
      <tbody>{orders.map(order => <tr key={order.order_id} className="border-b border-gray-100 align-top">
        <td className="p-3"><strong>{order.profiles?.nama ?? 'Peserta'}</strong><p className="mt-1 max-w-64 break-all text-xs text-gray-500">{order.order_id}</p><p className="mt-1 text-xs text-gray-500">{paymentDate(order.created_at)}</p></td>
        <td className="p-3">{order.nama_paket}</td><td className="whitespace-nowrap p-3">{rupiah(order.nominal)}</td>
        <td className="p-3"><strong>{paymentStatusLabels[order.status]}</strong>{order.review_reason && <p className="mt-2 max-w-xs text-red-700">{order.review_reason}</p>}</td>
        <td className="p-3">{order.membership_ends_at ? paymentDate(order.membership_ends_at) : order.environment === 'sandbox' ? 'Simulasi' : '—'}</td>
      </tr>)}</tbody>
    </table></div>
    {!orders.length && !error && <p className="py-5 text-sm text-gray-600">{loading ? 'Memuat transaksi…' : 'Belum ada transaksi untuk jenis ini.'}</p>}
    <p className="mt-3 text-sm text-gray-500">Menampilkan 50 transaksi terbaru. Status QRIS diperbarui melalui notifikasi Midtrans. Pengembalian dana dan status peninjauan perlu ditangani admin.</p>
  </section>
}
