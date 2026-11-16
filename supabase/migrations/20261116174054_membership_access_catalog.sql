alter table public.paket_membership
  add column akses text not null default 'gratis'
    check (akses in ('gratis', 'premium', 'platinum'));

-- Paid offers can be browsed while their content is being prepared.
with tiers(akses, fitur) as (
  values
    ('gratis', to_jsonb(concat_ws(E'\n',
      '4 tryout OSN-K lengkap dengan pembahasan',
      '3 cuplikan pendalaman dengan pembahasan',
      'Grafik kemajuan belajar'
    ))),
    ('premium', to_jsonb(concat_ws(E'\n',
      'Seluruh akses Gratis',
      '10 paket OSN-K (termasuk 4 gratis)',
      '5 paket OSN Provinsi',
      '1 paket OSN Nasional',
      '1 paket pendalaman per bab atau materi'
    ))),
    ('platinum', to_jsonb(concat_ws(E'\n',
      'Seluruh akses Gratis',
      '20 paket OSN-K (termasuk 4 gratis)',
      '10 paket OSN Provinsi',
      '5 paket OSN Nasional',
      '4 paket pendalaman per bab atau materi',
      'Video pembelajaran dan modul'
    )))
), offers(urutan, nama, harga, durasi_hari, akses, aktif) as (
  values
    (1, 'Gratis', 0, null::integer, 'gratis', true),
    (2, 'Premium 1 bulan', 50000, 30, 'premium', false),
    (3, 'Premium 1 tahun', 200000, 365, 'premium', false),
    (4, 'Platinum 1 bulan', 100000, 30, 'platinum', false),
    (5, 'Platinum 1 tahun', 500000, 365, 'platinum', false)
)
insert into public.paket_membership (nama, harga, durasi_hari, akses, aktif, fitur)
select o.nama, o.harga, o.durasi_hari, o.akses, o.aktif, t.fitur
from offers o join tiers t using (akses)
where not exists (select 1 from public.paket_membership p where p.nama = o.nama)
order by o.urutan;

-- Each free preview has three original questions and a worked explanation.
with previews(topik, nama) as (
  values
    ('Iklim dan Perubahan Iklim', 'Cuplikan Gratis · Iklim'),
    ('Geologi, Geomorfologi, dan Penggunaan Lahan', 'Cuplikan Gratis · Geomorfologi'),
    ('Perpetaan dan Interpretasi Informasi Geospasial', 'Cuplikan Gratis · Perpetaan')
), inserted as (
  insert into public.paket_pendalaman (topik_id, nama, deskripsi, akses, is_premium, status, durasi_menit)
  select t.id, p.nama, 'Coba tiga soal dan pelajari pembahasannya.', 'gratis', false, 'aktif', 10
  from previews p join public.topik_materi t on t.nama = p.topik
  where not exists (
    select 1 from public.paket_pendalaman existing where existing.topik_id = t.id and existing.nama = p.nama
  )
  returning id, nama
), questions(paket, urutan, pertanyaan, a, b, c, d, e, kunci, pembahasan) as (
  values
    ('Cuplikan Gratis · Iklim', 1,
      'Angin lembap dari laut melewati pegunungan. Pada elevasi yang sama, lereng yang menghadap arah datang angin menerima lebih banyak hujan. Proses utama yang menjelaskan pola itu adalah …',
      'Udara turun dan menghangat di lereng tersebut',
      'Udara dipaksa naik, mendingin, lalu uap air mengembun',
      'Udara bergerak mendatar sehingga suhunya tetap',
      'Tekanan yang meningkat di puncak membuat udara mengembun',
      'Angin dari laut membawa udara yang lebih kering daripada angin darat',
      'B', 'Lereng yang menghadap datangnya angin memaksa udara lembap terangkat. Udara mengembang dan mendingin saat naik, sehingga pengembunan dan hujan orografis lebih mungkin terjadi.'),
    ('Cuplikan Gratis · Iklim', 2,
      'Pada malam cerah dengan angin lemah, pusat kota masih lebih hangat daripada kawasan bervegetasi di sekitarnya. Mekanisme utama yang mempertahankan perbedaan itu adalah …',
      'Aspal dan bangunan melepaskan panas yang tersimpan sejak siang',
      'Permukaan kota menyerap lebih banyak sinar Matahari setelah gelap',
      'Pusat kota kehilangan panas lebih cepat karena permukaannya kedap air',
      'Angin lemah mempercepat pencampuran udara pusat kota dan pinggiran',
      'Daerah perkotaan memiliki kandungan ozon stratosfer yang lebih rendah',
      'A', 'Material seperti aspal dan beton menyerap dan menyimpan panas pada siang hari, lalu melepaskannya pada malam hari. Angin lemah membantu mempertahankan perbedaan suhu setempat.'),
    ('Cuplikan Gratis · Iklim', 3,
      'Suhu udara di suatu stasiun naik dari 20 °C menjadi 30 °C. Tekanan udara dan kandungan uap airnya hampir tetap. Apa yang terjadi pada kelembapan relatif?',
      'Naik karena tekanan uap jenuh turun',
      'Tetap karena kandungan uap air tetap',
      'Mencapai 100 persen karena udara memuai',
      'Turun karena tekanan uap jenuh meningkat',
      'Turun karena semua uap air mengembun',
      'D', 'Kelembapan relatif adalah perbandingan tekanan uap aktual dengan tekanan uap jenuh. Saat suhu naik, tekanan uap jenuh meningkat. Jika tekanan uap aktual hampir tetap, perbandingannya turun.'),
    ('Cuplikan Gratis · Geomorfologi', 1,
      'Pada tikungan sungai yang berkelok, tebing di sisi luar terus mundur dan endapan pasir tumbuh di sisi dalam. Pasangan proses dominan pada kedua sisi itu adalah …',
      'Pengendapan di luar dan pengendapan di dalam',
      'Erosi di luar dan erosi di dalam',
      'Erosi di luar dan pengendapan di dalam',
      'Pengendapan di luar dan erosi di dalam',
      'Pelapukan kimia di luar dan abrasi di dalam',
      'C', 'Arus utama cenderung lebih cepat di sisi luar tikungan sehingga mengikis tebing. Di sisi dalam, aliran yang lebih lambat memungkinkan sedimen mengendap dan membentuk gosong.'),
    ('Cuplikan Gratis · Geomorfologi', 2,
      'Air hujan meresap melalui tanah yang kaya CO₂, lalu masuk ke rekahan batu gamping. Proses yang paling langsung memperlebar rekahan tersebut adalah …',
      'Kristalisasi kuarsa di dalam rekahan',
      'Pengendapan besi saat air menguap',
      'Peleburan batu gamping akibat panas dari tanah',
      'Pembekuan air di rekahan sepanjang tahun',
      'Pelarutan kalsium karbonat oleh air yang mengandung asam karbonat',
      'E', 'CO₂ terlarut membentuk asam karbonat lemah yang membantu melarutkan kalsium karbonat. Pelarutan yang berulang dapat memperbesar rekahan dan membentuk lorong karst.'),
    ('Cuplikan Gratis · Geomorfologi', 3,
      'Sebagian besar lahan bervegetasi di DAS kecil berubah menjadi jalan dan atap. Dengan hujan serupa serta tanpa kolam retensi, perubahan hidrograf yang paling mungkin adalah …',
      'Debit puncak lebih tinggi dan tercapai lebih cepat',
      'Debit puncak lebih rendah dan tercapai lebih lambat',
      'Debit puncak tetap dan waktu puncak lebih lambat',
      'Debit puncak lebih tinggi dan tercapai lebih lambat',
      'Debit puncak lebih rendah dan tercapai lebih cepat',
      'A', 'Permukaan kedap mengurangi infiltrasi, sehingga lebih banyak hujan menjadi limpasan. Air mencapai saluran lebih cepat dan debit puncak biasanya meningkat.'),
    ('Cuplikan Gratis · Perpetaan', 1,
      'Pada peta skala 1 banding 50.000, jarak lurus dua titik adalah 3 cm dan beda ketinggiannya 150 m. Berapa kemiringan rata-rata antara kedua titik?',
      '5 persen', '10 persen', '15 persen', '20 persen', '25 persen',
      'B', 'Jarak mendatar di lapangan adalah 3 × 50.000 cm atau 1.500 m. Kemiringan persen adalah beda tinggi dibagi jarak mendatar dikali 100, sehingga 150 ÷ 1.500 × 100 = 10 persen.'),
    ('Cuplikan Gratis · Perpetaan', 2,
      'Tiga garis kontur tertutup dan bersarang memiliki elevasi 450 m, 425 m, dan 400 m dari luar ke dalam. Bentuk muka bumi yang ditunjukkan adalah …',
      'Puncak bukit', 'Punggungan memanjang', 'Pelana di antara dua bukit', 'Cekungan tertutup', 'Dataran pada elevasi seragam',
      'D', 'Elevasi kontur yang makin rendah ke pusat menunjukkan cekungan. Kontur tertutup pada bukit menunjukkan urutan elevasi yang naik ke pusat.'),
    ('Cuplikan Gratis · Perpetaan', 3,
      'Dalam raster terproyeksi beresolusi 30 m × 30 m, tepat 20 piksel diklasifikasikan sebagai mangrove. Berapa luas kelas mangrove yang dihitung dari raster tersebut?',
      '0,06 hektare', '0,6 hektare', '1,8 hektare', '18 hektare', '180 hektare',
      'C', 'Luas satu piksel adalah 900 m². Dua puluh piksel mencakup 18.000 m², setara 1,8 hektare karena satu hektare sama dengan 10.000 m².')
)
insert into public.soal_pendalaman (paket_id, pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d, pilihan_e, jawaban_benar, pembahasan)
select p.id, q.pertanyaan, q.a, q.b, q.c, q.d, q.e, q.kunci, q.pembahasan
from inserted p join questions q on q.paket = p.nama
order by p.id, q.urutan;

-- The caller only reads their own persisted membership through profiles RLS.
create function osngeo_private.membership_level()
returns integer
language sql stable security invoker
set search_path = ''
as $$
  select coalesce((
    select case status when 'platinum' then 2 when 'premium' then 1 else 0 end
    from public.profiles
    where id = (select auth.uid())
      and (status_expired is null or status_expired > timezone('UTC', now()))
  ), 0);
$$;

revoke execute on function osngeo_private.membership_level() from public, anon;
grant execute on function osngeo_private.membership_level() to authenticated;

create index if not exists soal_paket_id_idx on public.soal (paket_id);
create index if not exists soal_pendalaman_paket_id_idx on public.soal_pendalaman (paket_id);

alter table public.paket_membership enable row level security;
alter table public.paket_to enable row level security;
alter table public.paket_pendalaman enable row level security;
alter table public.soal enable row level security;
alter table public.soal_pendalaman enable row level security;
alter table public.video_pembelajaran enable row level security;
alter table public.modul_materi enable row level security;

revoke all on public.paket_membership, public.paket_to, public.paket_pendalaman,
  public.soal, public.soal_pendalaman, public.video_pembelajaran, public.modul_materi
  from public, anon, authenticated;

grant select on public.paket_membership, public.paket_to, public.paket_pendalaman,
  public.video_pembelajaran, public.modul_materi to anon, authenticated;
grant select on public.soal, public.soal_pendalaman to authenticated;
grant insert, update, delete on public.paket_membership, public.paket_to, public.paket_pendalaman,
  public.soal, public.soal_pendalaman, public.video_pembelajaran, public.modul_materi to authenticated;
grant usage on sequence public.paket_membership_id_seq, public.paket_to_id_seq,
  public.paket_pendalaman_id_seq, public.soal_id_seq, public.soal_pendalaman_id_seq,
  public.video_pembelajaran_id_seq, public.modul_materi_id_seq to authenticated;

-- Package metadata stays readable, including the titles used by past results.
alter policy "Semua baca paket" on public.paket_membership to anon, authenticated;
alter policy "Paket bisa dibaca semua" on public.paket_to to anon, authenticated;
alter policy "Semua baca paket pendalaman" on public.paket_pendalaman to anon, authenticated;

alter policy "Soal bisa dibaca semua" on public.soal to authenticated
  using (exists (
    select 1 from public.paket_to p
    where p.id = soal.paket_id and p.status = 'aktif'
      and (select osngeo_private.membership_level()) >= case
        when p.akses = 'platinum' then 2
        when p.akses = 'premium' or p.is_premium is true then 1
        else 0
      end
  ));

alter policy "Semua baca soal pendalaman" on public.soal_pendalaman to authenticated
  using (exists (
    select 1 from public.paket_pendalaman p
    where p.id = soal_pendalaman.paket_id and p.status = 'aktif'
      and (select osngeo_private.membership_level()) >= case
        when p.akses = 'platinum' then 2
        when p.akses = 'premium' or p.is_premium is true then 1
        else 0
      end
  ));

alter policy "Semua baca video" on public.video_pembelajaran to anon, authenticated
  using (aktif is not false and coalesce(akses, 'gratis') = 'gratis' and is_premium is not true);
alter policy "Semua baca modul" on public.modul_materi to anon, authenticated
  using (aktif is not false and coalesce(akses, 'gratis') = 'gratis' and is_premium is not true);

create policy "Platinum baca video" on public.video_pembelajaran
  for select to authenticated using (aktif is not false and (select osngeo_private.membership_level()) = 2);
create policy "Platinum baca modul" on public.modul_materi
  for select to authenticated using (aktif is not false and (select osngeo_private.membership_level()) = 2);

alter policy "Admin kelola paket" on public.paket_membership to authenticated
  using ((select osngeo_private.is_admin())) with check ((select osngeo_private.is_admin()));
create policy "Admin kelola paket tryout" on public.paket_to for all to authenticated
  using ((select osngeo_private.is_admin())) with check ((select osngeo_private.is_admin()));
alter policy "Admin kelola paket pendalaman" on public.paket_pendalaman to authenticated
  using ((select osngeo_private.is_admin())) with check ((select osngeo_private.is_admin()));
create policy "Admin kelola soal tryout" on public.soal for all to authenticated
  using ((select osngeo_private.is_admin())) with check ((select osngeo_private.is_admin()));
alter policy "Admin kelola soal pendalaman" on public.soal_pendalaman to authenticated
  using ((select osngeo_private.is_admin())) with check ((select osngeo_private.is_admin()));
alter policy "Admin kelola video" on public.video_pembelajaran to authenticated
  using ((select osngeo_private.is_admin())) with check ((select osngeo_private.is_admin()));
alter policy "Admin kelola modul" on public.modul_materi to authenticated
  using ((select osngeo_private.is_admin())) with check ((select osngeo_private.is_admin()));

notify pgrst, 'reload schema';
