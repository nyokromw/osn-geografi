# Pembayaran QRIS otomatis OSNGEO.id

Integrasi menggunakan QRIS dinamis GoPay melalui Midtrans Core API. Checkout ada di `/pembayaran?paket=<id>`, riwayat siswa di dashboard **Paket dan akses**, dan riwayat admin di **Transaksi**.

## Konfigurasi awal: Sandbox

1. Buka Midtrans Dashboard, pilih **Sandbox**, lalu **Settings → Access Keys**.
2. Buat **Server Key Sandbox** dengan izin **Core API: Write**; produk dan capability lainnya **None**. Salin langsung ke [Supabase Edge Functions Secrets](https://supabase.com/dashboard/project/lhzlcaxlemlmjhfmichz/functions/secrets), dengan nama `MIDTRANS_SANDBOX_SERVER_KEY`. Kunci baru hanya ditampilkan sekali.
3. Tambahkan `MIDTRANS_ENVIRONMENT` dengan nilai `sandbox`. Biarkan `MIDTRANS_PAYMENTS_ENABLED` bernilai `false` atau belum diisi.
4. Di Midtrans Sandbox, isi **Payment Notification URL** pada pengaturan pembayaran/konfigurasi dengan:

   ```text
   https://lhzlcaxlemlmjhfmichz.supabase.co/functions/v1/midtrans-payment
   ```

5. Masuk OSNGEO.id menggunakan akun admin. Buka **Dashboard → Paket dan akses → Uji pembayaran QRIS**. Selesaikan pembayaran menggunakan [simulator Sandbox Midtrans](https://simulator.sandbox.midtrans.com/), bukan transfer uang sungguhan.
6. Pastikan pesanan berubah menjadi **Lunas** dan diberi label **Simulasi**. Profil dan tanggal kedaluwarsa akun harus tetap sama.

Sandbox hanya tersedia untuk akun dengan `profiles.role = 'admin'`. Pelanggan tetap menggunakan alur pemesanan WhatsApp sampai mode Production diaktifkan. Pembayaran Sandbox tidak pernah mengaktifkan keanggotaan sungguhan.

Server Key merupakan rahasia. Jangan masukkan di kode, GitHub, `NEXT_PUBLIC_*`, screenshot, atau percakapan. Tidak diperlukan Client Key untuk alur Core API ini. Kunci Supabase server sudah tersedia otomatis di Edge Functions dan tidak perlu dipasang ke Vercel.

## Membuka pembayaran pelanggan

Sesudah Midtrans menyetujui merchant dan QRIS Production aktif:

1. Tambahkan **Server Key Production** sebagai `MIDTRANS_PRODUCTION_SERVER_KEY` di Supabase Secrets. Pertahankan kunci Sandbox agar pesanan uji lama masih dapat diperiksa.
2. Isi **Payment Notification URL Production** dengan URL yang sama di atas.
3. Ubah `MIDTRANS_ENVIRONMENT` menjadi `production` dan `MIDTRANS_PAYMENTS_ENABLED` menjadi `true`.
4. Muat ulang halaman paket OSNGEO.id. Tombol paket aktif berubah menjadi **Bayar dengan QRIS**.
5. Lakukan satu transaksi nyata melalui akun siswa yang disiapkan untuk pengujian. Pastikan nominal, status **Lunas**, tingkat keanggotaan, masa berlaku, dan akses materi benar. Verifikasi juga saat tab pembayaran ditutup: webhook tetap harus mengaktifkan akun.

Perubahan secrets berlaku tanpa redeploy fungsi. Matikan pembelian baru dengan `MIDTRANS_PAYMENTS_ENABLED=false`; webhook dan pemeriksaan pesanan yang sudah dibuat tetap berjalan. Jangan menghapus kunci Production ketika masih ada pesanan.

Waktu pesanan untuk `custom_expiry` dikirim dalam GMT+7 sesuai format Core API. Jika penerbitan QRIS ditolak, layar menampilkan kode kesalahan tanpa membocorkan respons penyedia: `400`/`408` menunjukkan format data, `401` menunjukkan kunci atau mode, `402` menunjukkan akses metode pembayaran, dan `403` memerlukan pemeriksaan izin kunci serta pengaturan integrasi. Log fungsi hanya menyimpan kode dan status HTTP.

## Aturan keanggotaan

- Harga, tingkat akses, nama, dan durasi disalin dari paket aktif di database saat pesanan dibuat. Perubahan katalog berikutnya tidak mengubah pesanan itu.
- Akses baru dimulai setelah pembayaran diverifikasi oleh server.
- Perpanjangan paket dengan tingkat yang sama menambahkan durasi ke masa aktif yang tersisa.
- Upgrade Premium ke Platinum memulai durasi Platinum yang baru. Sisa Premium tidak dikonversi; informasi ini ditampilkan sebelum checkout.
- Akun dengan Platinum aktif tidak dapat membeli Premium. Akun berbayar tanpa batas waktu diarahkan ke admin.
- Jika akses berubah menjadi lebih tinggi ketika pembayaran masih tertunda, pesanan ditandai **Perlu peninjauan**. Sistem menjaga akses yang sudah lebih tinggi dan tidak menurunkannya.
- Notifikasi berulang tidak menambah durasi dua kali. Notifikasi pending/kedaluwarsa tidak membatalkan pesanan yang sudah lunas.
- Refund/chargeback dicatat dan ditandai untuk peninjauan admin. Penyesuaian akses terkait refund dilakukan admin; jangan menganggap refund otomatis mencabut semua akses, karena akun bisa memiliki perpanjangan atau pemberian akses lain.

## Keamanan dan pemeliharaan

Fungsi `midtrans-payment` memverifikasi login Supabase untuk checkout/pemeriksaan status. Notifikasi Midtrans tidak membutuhkan login pengguna: fungsi selalu mengambil **GET Transaction Status** langsung dari Midtrans dengan otorisasi Server Key, lalu mencocokkan identitas transaksi, nominal, metode pembayaran, dan mata uang dengan pesanan di database. Status/nominal dari notifikasi atau browser tidak dipakai untuk aktivasi. Ini mengikuti metode verifikasi status langsung yang digunakan library resmi Midtrans.

Sejak 28 Oktober 2026, Midtrans memisahkan **Signature Secret Key** dari Server Key. Jika ingin menambahkan pemeriksaan signature sebelum GET Status, simpan rahasia tersebut sebagai `MIDTRANS_SANDBOX_SIGNATURE_SECRET_KEY` dan/atau `MIDTRANS_PRODUCTION_SIGNATURE_SECRET_KEY`. Konfigurasi ini opsional; GET Status yang terautentikasi tetap wajib dijalankan. Jangan menggunakan Server Key baru sebagai pengganti Signature Secret Key. Dokumentasi: [Access Keys](https://docs.midtrans.com/docs/access-keys).

RPC `midtrans_create_order` dan `midtrans_reconcile_order` memakai **SECURITY INVOKER**, dengan izin eksekusi hanya untuk `service_role`. Tabel `pembayaran_midtrans` memakai RLS: siswa hanya membaca pesanan sendiri dan admin dapat membaca semua pesanan. Klien tidak dapat menyisipkan/mengubah pesanan atau memanggil RPC aktivasi.

Aktivasi dan pencatatan pesanan berjalan dalam satu transaksi database. Row lock mencegah pemrosesan ganda, termasuk dua notifikasi yang masuk bersamaan. Pemeriksaan status dari halaman pembayaran menjadi jalur pemulihan jika notifikasi terlambat.

Kode fungsi ada di `supabase/functions/midtrans-payment/index.ts`; pengujian murni di `supabase/functions/_shared/midtrans_test.ts`. Jalankan dengan Deno:

```sh
deno test supabase/functions/_shared/midtrans_test.ts
deno check supabase/functions/midtrans-payment/index.ts
```

Pengujian transaksi database ada di `supabase/tests/midtrans_membership.sql`. Skrip menggunakan fixture sementara dan `ROLLBACK`, sehingga tidak menyimpan akun atau transaksi uji.

Dokumentasi penyedia: [QRIS Core API](https://docs.midtrans.com/reference/qris), [HTTP notifications](https://docs.midtrans.com/docs/https-notification-webhooks), [Get Transaction Status](https://docs.midtrans.com/reference/get-transaction-status).
