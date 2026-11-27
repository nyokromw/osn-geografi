-- Paket Kelas: one guru + N student accounts with ready-made usernames.
-- Student accounts sign in with a username; their auth email is <username>@siswa.osngeo.id
-- (never mailed). Accounts are created only by the kelas-admin Edge Function (service role).

-- ------------------------------------------------------------------ profiles: identity fields
alter table public.profiles
  add column username text,
  add column sekolah text,
  add column kelas text,
  add constraint profiles_username_check check (username ~ '^[a-z0-9][a-z0-9_-]{2,31}$'),
  add constraint profiles_sekolah_check check (char_length(sekolah) <= 120),
  add constraint profiles_kelas_check check (char_length(kelas) <= 60);

create unique index profiles_username_key on public.profiles (username) where username is not null;

-- ------------------------------------------------------------------ classes
create table public.kelas (
  id uuid primary key default gen_random_uuid(),
  nama text not null check (char_length(btrim(nama)) between 2 and 120),
  guru_id uuid not null references public.profiles (id) on delete restrict,
  akses text not null default 'platinum' check (akses in ('premium', 'platinum')),
  kuota integer not null default 10 check (kuota between 1 and 200),
  kode text not null unique check (kode ~ '^[a-z][a-z0-9]{2,15}$'),
  -- UTC, same convention as profiles.status_expired
  berlaku_sampai timestamp not null,
  dibuat_oleh uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now()
);
create index kelas_guru_id_idx on public.kelas (guru_id);

create table public.kelas_anggota (
  kelas_id uuid not null references public.kelas (id) on delete cascade,
  user_id uuid not null unique references public.profiles (id) on delete cascade,
  username text not null,
  -- The generated password stays visible to the guru until the student sets their own
  -- (or the guru resets it), so the guru can hand out or reprint login cards.
  password_awal text,
  created_at timestamptz not null default now(),
  primary key (kelas_id, user_id)
);

alter table public.kelas enable row level security;
alter table public.kelas_anggota enable row level security;
revoke all on table public.kelas, public.kelas_anggota from public, anon, authenticated;
grant select on table public.kelas, public.kelas_anggota to authenticated;

-- Is the caller the guru of this student? security definer: no recursion through RLS.
create function osngeo_private.is_guru_of(p_user uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.kelas_anggota as anggota
    join public.kelas as kelas on kelas.id = anggota.kelas_id
    where anggota.user_id = p_user and kelas.guru_id = (select auth.uid())
  );
$$;
revoke execute on function osngeo_private.is_guru_of(uuid) from public, anon;
grant execute on function osngeo_private.is_guru_of(uuid) to authenticated;

create policy "Guru baca kelas sendiri" on public.kelas
  for select to authenticated
  using (guru_id = (select auth.uid()) or (select osngeo_private.is_admin()));

create policy "Guru dan siswa baca anggota kelas" on public.kelas_anggota
  for select to authenticated
  using (
    user_id = (select auth.uid())
    or (select osngeo_private.is_admin())
    or (select osngeo_private.is_guru_of(user_id))
  );

-- The guru can read the profile and results of their own students (progress dashboard).
create policy "Guru baca profil siswa kelas" on public.profiles
  for select to authenticated using ((select osngeo_private.is_guru_of(id)));
create policy "Guru baca hasil tryout siswa kelas" on public.hasil_to
  for select to authenticated using ((select osngeo_private.is_guru_of(user_id)));
create policy "Guru baca hasil pendalaman siswa kelas" on public.hasil_pendalaman
  for select to authenticated using ((select osngeo_private.is_guru_of(user_id)));

-- ------------------------------------------------------------------ self-service profile edits
-- profiles UPDATE stays admin-only (its column grants include role/status), so students edit
-- their own identity through these functions, which touch only safe columns.
create function public.update_my_profile(p_nama text, p_sekolah text, p_kelas text, p_provinsi text, p_nomor_hp text)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  uid uuid := (select auth.uid());
  clean_nama text := pg_catalog.btrim(coalesce(p_nama, ''));
  clean_hp text := nullif(pg_catalog.regexp_replace(coalesce(p_nomor_hp, ''), '[[:space:]().-]', '', 'g'), '');
begin
  if uid is null then raise exception 'Silakan masuk terlebih dahulu.'; end if;
  if char_length(clean_nama) < 2 or char_length(clean_nama) > 80 then
    raise exception 'Nama harus 2 sampai 80 karakter.';
  end if;
  update public.profiles
  set nama = clean_nama,
      sekolah = nullif(pg_catalog.btrim(coalesce(p_sekolah, '')), ''),
      kelas = nullif(pg_catalog.btrim(coalesce(p_kelas, '')), ''),
      provinsi = nullif(pg_catalog.btrim(coalesce(p_provinsi, '')), ''),
      nomor_hp = clean_hp
  where id = uid;
end;
$$;
revoke execute on function public.update_my_profile(text, text, text, text, text) from public, anon;
grant execute on function public.update_my_profile(text, text, text, text, text) to authenticated;

-- Called after a student sets their own password: the guru no longer needs to see it.
create function public.clear_my_initial_password()
returns void
language sql
security definer
set search_path = ''
as $$
  update public.kelas_anggota set password_awal = null where user_id = (select auth.uid());
$$;
revoke execute on function public.clear_my_initial_password() from public, anon;
grant execute on function public.clear_my_initial_password() to authenticated;

-- ------------------------------------------------------------------ catalogue
alter table public.paket_membership
  add column jenis text not null default 'perorangan' check (jenis in ('perorangan', 'kelas')),
  add column kuota_siswa integer check (kuota_siswa is null or kuota_siswa > 0);

insert into public.paket_membership (nama, harga, durasi_hari, deskripsi, fitur, akses, aktif, jenis, kuota_siswa)
values (
  'Paket Kelas', 690000, 365,
  'Untuk sekolah, bimbel, dan kelompok belajar.',
  to_jsonb(
    '1 akun guru + 10 akun siswa siap pakai (username & kata sandi dari sistem)' || chr(10) ||
    'Akses Platinum untuk semua akun selama 1 tahun' || chr(10) ||
    'Semua paket tryout & prediksi, pendalaman materi, dan modul' || chr(10) ||
    'Guru memantau nilai dan kemajuan belajar tiap siswa'
  ),
  'platinum', true, 'kelas', 10
);

-- Class packages are fulfilled by an admin (account creation), never by self-checkout.
create or replace function public.midtrans_create_order(p_user_id uuid, p_paket_id integer, p_environment text)
 returns jsonb
 language plpgsql
 set search_path to ''
as $function$
declare
  account public.profiles%rowtype;
  plan public.paket_membership%rowtype;
  payment public.pembayaran_midtrans%rowtype;
begin
  if p_environment is null or p_environment not in ('sandbox', 'production') then
    raise exception 'Lingkungan pembayaran tidak valid.';
  end if;
  select * into account from public.profiles where id = p_user_id for update;
  if not found then raise exception 'Profil akun tidak ditemukan.'; end if;
  if p_environment = 'sandbox' and account.role is distinct from 'admin' then
    raise exception 'Simulasi pembayaran hanya tersedia untuk admin.';
  end if;
  select * into plan from public.paket_membership where id = p_paket_id;
  if not found or plan.aktif is not true or plan.akses not in ('premium', 'platinum')
     or plan.jenis is distinct from 'perorangan'
     or plan.harga <= 0 or plan.durasi_hari is null or plan.durasi_hari <= 0 then
    raise exception 'Paket ini belum tersedia untuk pembayaran.';
  end if;
  if p_environment = 'production' and account.status in ('premium', 'platinum')
     and (account.status_expired is null or account.status_expired > timezone('UTC', now())) then
    if account.status_expired is null then
      raise exception 'Akses akun tidak memiliki batas waktu. Hubungi admin sebelum membeli paket.';
    end if;
    if account.status = 'platinum' and plan.akses = 'premium' then
      raise exception 'Platinum masih aktif. Pilih perpanjangan Platinum atau tunggu masa aktif berakhir.';
    end if;
  end if;
  select * into payment from public.pembayaran_midtrans
    where user_id = p_user_id and paket_id = p_paket_id and environment = p_environment
      and status in ('created', 'pending') and expires_at > now()
    order by created_at desc limit 1;
  if found then return jsonb_build_object('order', to_jsonb(payment), 'is_new', false); end if;
  if (select count(*) from public.pembayaran_midtrans where user_id = p_user_id
        and created_at > now() - interval '10 minutes') >= 5 then
    raise exception 'Terlalu banyak pesanan baru. Lanjutkan pembayaran yang ada atau coba beberapa menit lagi.';
  end if;
  insert into public.pembayaran_midtrans
    (user_id, paket_id, order_id, environment, nama_paket, akses, durasi_hari, nominal)
  values (p_user_id, plan.id, 'OSNGEO-' || case p_environment when 'sandbox' then 'SB-' else 'PR-' end
    || replace(gen_random_uuid()::text, '-', ''), p_environment, plan.nama,
    plan.akses, plan.durasi_hari, plan.harga)
  returning * into payment;
  return jsonb_build_object('order', to_jsonb(payment), 'is_new', true);
end;
$function$;

-- ------------------------------------------------------------------ learning videos are open to everyone
update public.video_pembelajaran
set akses = 'gratis', is_premium = false
where coalesce(akses, 'gratis') <> 'gratis' or is_premium is true;
alter table public.video_pembelajaran alter column akses set default 'gratis';
update public.paket_membership
set fitur = to_jsonb(pg_catalog.replace(fitur #>> '{}', chr(10) || 'Video pembelajaran animasi yang mudah dipahami (segera terbit)', ''))
where akses = 'platinum' and jenis = 'perorangan' and jsonb_typeof(fitur) = 'string';

notify pgrst, 'reload schema';
