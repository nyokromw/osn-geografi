-- Price restructure for the 2026/2027 season: one payment, valid 1 year.
--   Gratis Rp0 · Pemula Rp10.000 · Premium Rp49.000 · Platinum Rp149.000 · Paket Kelas Rp990.000
-- Apply together with the web release that knows the "pemula" level (20261127120000_level_pemula.sql).

-- ------------------------------------------------------------------ Pemula content: 5 packages move down from Premium
update public.paket_to
set akses = 'pemula', is_premium = false
where status = 'aktif' and nama in (
  'Soal Latihan OSN-K Geografi Paket 3',
  'Soal Latihan OSN-K Geografi Paket 4',
  'Soal Latihan OSN-K Geografi Paket 5',
  'Soal Latihan OSN-P Geografi Paket 3',
  'Soal Prediksi OSN-Geografi 2027 Paket 2'
);

-- ------------------------------------------------------------------ catalogue
update public.paket_membership set fitur = to_jsonb(
  '5 paket tryout dengan pembahasan (2 OSN-K, 2 OSN-P, 1 Prediksi 2027)' || chr(10) ||
  '13 paket pendalaman materi, masing-masing 10 soal dengan pembahasan' || chr(10) ||
  'Semua video pembelajaran' || chr(10) ||
  'Grafik kemajuan belajar'
) where jenis = 'perorangan' and akses = 'gratis';

insert into public.paket_membership (nama, harga, durasi_hari, deskripsi, fitur, akses, aktif, jenis)
select 'Pemula', 10000, 365, 'Mulai serius dengan harga jajan.', to_jsonb(
  '10 paket tryout dengan pembahasan (5 OSN-K, 3 OSN-P, 2 Prediksi 2027)' || chr(10) ||
  '13 paket pendalaman materi' || chr(10) ||
  'Semua video pembelajaran' || chr(10) ||
  'Berlaku 1 tahun, sekali bayar'
), 'pemula', true, 'perorangan'
where not exists (select 1 from public.paket_membership where akses = 'pemula' and jenis = 'perorangan');

-- Yearly plans become the one Premium / Platinum offer; monthly plans are retired.
update public.paket_membership set nama = 'Premium', harga = 49000, deskripsi = 'Paket paling pas untuk persiapan OSN-K.', fitur = to_jsonb(
  '24 paket tryout dengan pembahasan (12 OSN-K, 10 OSN-P, 2 Prediksi 2027)' || chr(10) ||
  '26 paket pendalaman materi (2 per bab)' || chr(10) ||
  'Semua video pembelajaran' || chr(10) ||
  'Berlaku 1 tahun, sekali bayar'
) where jenis = 'perorangan' and akses = 'premium' and durasi_hari = 365;

update public.paket_membership set nama = 'Platinum', harga = 149000, deskripsi = 'Semua soal dan materi OSNGEO.id.', fitur = to_jsonb(
  'Semua 35 paket tryout dengan pembahasan (20 OSN-K, 10 OSN-P, 5 Prediksi 2027)' || chr(10) ||
  'Semua 78 paket pendalaman materi' || chr(10) ||
  '13 modul belajar lengkap' || chr(10) ||
  'Semua video pembelajaran' || chr(10) ||
  'Berlaku 1 tahun, sekali bayar'
) where jenis = 'perorangan' and akses = 'platinum' and durasi_hari = 365;

update public.paket_membership set aktif = false
where jenis = 'perorangan' and akses in ('premium', 'platinum') and durasi_hari = 30;

update public.paket_membership set harga = 990000, fitur = to_jsonb(
  '1 akun guru + 10 akun siswa siap pakai (username & kata sandi dari sistem)' || chr(10) ||
  'Akses Platinum untuk semua akun selama 1 tahun' || chr(10) ||
  'Semua 35 paket tryout & prediksi, 78 pendalaman materi, dan 13 modul' || chr(10) ||
  'Guru memantau nilai dan kemajuan belajar tiap siswa'
) where jenis = 'kelas';
