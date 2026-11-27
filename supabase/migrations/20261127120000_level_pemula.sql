-- New access level "pemula" between gratis and premium.
-- Ranks: gratis 0 · pemula 1 · premium 2 · platinum 3. Structural only (no catalogue data changes),
-- so it is safe to apply before the web app that knows about "pemula" is deployed.

create function osngeo_private.access_rank(p_level text)
returns integer
language sql
immutable
set search_path = ''
as $$
  select case p_level when 'platinum' then 3 when 'premium' then 2 when 'pemula' then 1 else 0 end;
$$;
grant execute on function osngeo_private.access_rank(text) to authenticated, anon, service_role;
-- The Midtrans RPCs run as service_role and now call access_rank.
grant usage on schema osngeo_private to service_role;

create or replace function osngeo_private.membership_level()
returns integer
language sql
stable
set search_path = ''
as $$
  select coalesce((
    select osngeo_private.access_rank(status)
    from public.profiles
    where id = (select auth.uid())
      and (status_expired is null or status_expired > timezone('UTC', now()))
  ), 0);
$$;

-- Content rank required by a package (is_premium is the legacy flag for premium).
create function osngeo_private.content_rank(p_akses text, p_is_premium boolean)
returns integer
language sql
immutable
set search_path = ''
as $$
  select greatest(osngeo_private.access_rank(p_akses), case when p_is_premium then 2 else 0 end);
$$;
grant execute on function osngeo_private.content_rank(text, boolean) to authenticated, anon, service_role;

alter table public.paket_membership drop constraint paket_membership_akses_check,
  add constraint paket_membership_akses_check check (akses in ('gratis', 'pemula', 'premium', 'platinum'));
alter table public.pembayaran_midtrans drop constraint pembayaran_midtrans_akses_check,
  add constraint pembayaran_midtrans_akses_check check (akses in ('pemula', 'premium', 'platinum'));

-- Policies that compared against the old ranks (platinum was 2).
drop policy "Soal bisa dibaca semua" on public.soal;
create policy "Soal bisa dibaca semua" on public.soal
  for select to authenticated using (exists (
    select 1 from public.paket_to p
    where p.id = soal.paket_id and p.status = 'aktif'
      and (select osngeo_private.membership_level()) >= osngeo_private.content_rank(p.akses, p.is_premium)
  ));

drop policy "Semua baca soal pendalaman" on public.soal_pendalaman;
create policy "Semua baca soal pendalaman" on public.soal_pendalaman
  for select to authenticated using (exists (
    select 1 from public.paket_pendalaman p
    where p.id = soal_pendalaman.paket_id and p.status = 'aktif'
      and (select osngeo_private.membership_level()) >= osngeo_private.content_rank(p.akses, p.is_premium)
  ));

drop policy "Platinum baca modul" on public.modul_materi;
create policy "Platinum baca modul" on public.modul_materi
  for select to authenticated using (aktif is not false and (select osngeo_private.membership_level()) = 3);

drop policy "Platinum baca video" on public.video_pembelajaran;
create policy "Platinum baca video" on public.video_pembelajaran
  for select to authenticated using (aktif is not false and (select osngeo_private.membership_level()) = 3);

drop policy "Platinum membaca halaman modul" on storage.objects;
create policy "Platinum membaca halaman modul" on storage.objects
  for select to authenticated using (
    bucket_id = 'modul-halaman'
    and (
      storage.allow_only_operation('object.get_authenticated')
      or (
        storage.allow_only_operation('object.get_authenticated_info')
        and current_setting('request.method', true) = 'GET'
        and (
          split_part(current_setting('request.path', true), '?', 1) = '/object/info/modul-halaman/' || name
          or split_part(current_setting('request.path', true), '?', 1) = '/object/info/authenticated/modul-halaman/' || name
        )
      )
    )
    and ((select osngeo_private.membership_level()) = 3 or (select osngeo_private.is_admin()))
    and exists (
      select 1 from public.modul_materi m
      where m.folder_halaman = (storage.foldername(objects.name))[1] and m.aktif is true and m.akses = 'platinum'
    )
  );

-- Checkout: any paid individual level; never sell a lower level over an active higher one.
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
  if not found or plan.aktif is not true or plan.akses not in ('pemula', 'premium', 'platinum')
     or plan.jenis is distinct from 'perorangan'
     or plan.harga <= 0 or plan.durasi_hari is null or plan.durasi_hari <= 0 then
    raise exception 'Paket ini belum tersedia untuk pembayaran.';
  end if;
  if p_environment = 'production' and osngeo_private.access_rank(account.status) > 0
     and (account.status_expired is null or account.status_expired > timezone('UTC', now())) then
    if account.status_expired is null then
      raise exception 'Akses akun tidak memiliki batas waktu. Hubungi admin sebelum membeli paket.';
    end if;
    if osngeo_private.access_rank(account.status) > osngeo_private.access_rank(plan.akses) then
      raise exception 'Akses yang lebih tinggi masih aktif. Pilih paket yang sama atau lebih tinggi.';
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

-- Fulfilment: same level extends, a higher level starts a new period, a lower level goes to review.
create or replace function public.midtrans_reconcile_order(p_order_id text, p_environment text, p_nominal numeric, p_transaction_id text, p_payment_type text, p_status text, p_status_code text, p_fraud_status text, p_currency text)
 returns public.pembayaran_midtrans
 language plpgsql
 set search_path to ''
as $function$
declare
  payment public.pembayaran_midtrans%rowtype;
  account public.profiles%rowtype;
  expiry timestamptz;
begin
  select * into payment from public.pembayaran_midtrans where order_id = p_order_id for update;
  if not found then raise exception 'Pesanan tidak ditemukan.'; end if;
  if p_environment is distinct from payment.environment or p_nominal is distinct from payment.nominal::numeric
     or p_payment_type is distinct from 'qris' or p_currency is distinct from 'IDR'
     or nullif(p_transaction_id, '') is null then
    raise exception 'Data pembayaran tidak cocok dengan pesanan.';
  end if;
  if payment.midtrans_transaction_id is not null
     and payment.midtrans_transaction_id <> p_transaction_id then
    raise exception 'Identitas transaksi tidak cocok.';
  end if;
  -- A late pending/expired event must never overwrite an already paid order.
  if payment.status in ('paid', 'review', 'refunded')
     and p_status not in ('refund', 'partial_refund', 'chargeback', 'partial_chargeback') then
    return payment;
  end if;
  update public.pembayaran_midtrans set midtrans_transaction_id = p_transaction_id,
    midtrans_status = p_status, updated_at = now() where id = payment.id;
  if p_status in ('refund', 'partial_refund', 'chargeback', 'partial_chargeback') then
    update public.pembayaran_midtrans set status = 'refunded',
      review_reason = 'Pengembalian dana: admin perlu meninjau akses dan masa aktif akun.'
      where id = payment.id returning * into payment;
    return payment;
  end if;
  if p_status = 'settlement' and p_status_code = '200'
     and (p_fraud_status is null or lower(p_fraud_status) = 'accept') then
    if payment.environment = 'production' then
      select * into account from public.profiles where id = payment.user_id for update;
      if not found then raise exception 'Profil akun tidak ditemukan.'; end if;
      if osngeo_private.access_rank(account.status) > 0 and
         (account.status_expired is null or account.status_expired > timezone('UTC', now())) and
         (account.status_expired is null
          or osngeo_private.access_rank(account.status) > osngeo_private.access_rank(payment.akses)) then
        update public.pembayaran_midtrans set status = 'review', paid_at = coalesce(paid_at, now()),
          review_reason = 'Pembayaran diterima; akses akun sudah lebih tinggi atau tanpa batas waktu. Hubungi admin.'
          where id = payment.id returning * into payment;
        return payment;
      end if;
      expiry := now() + make_interval(days => payment.durasi_hari);
      if account.status = payment.akses and account.status_expired > timezone('UTC', now()) then
        expiry := (account.status_expired at time zone 'UTC') + make_interval(days => payment.durasi_hari);
      end if;
      update public.profiles set status = payment.akses, status_expired = timezone('UTC', expiry)
        where id = account.id;
      update public.pembayaran_midtrans set fulfilled_at = now(), membership_ends_at = expiry
        where id = payment.id;
    end if;
    update public.pembayaran_midtrans set status = 'paid', paid_at = coalesce(paid_at, now())
      where id = payment.id;
  elsif p_status = 'pending' then
    update public.pembayaran_midtrans set status = 'pending' where id = payment.id;
  elsif p_status = 'expire' then
    update public.pembayaran_midtrans set status = 'expired' where id = payment.id;
  elsif p_status in ('deny', 'cancel', 'failure') then
    update public.pembayaran_midtrans set status = 'failed' where id = payment.id;
  else
    update public.pembayaran_midtrans set status = 'review',
      review_reason = 'Status pembayaran memerlukan verifikasi admin.' where id = payment.id;
  end if;
  select * into payment from public.pembayaran_midtrans where id = payment.id;
  return payment;
end;
$function$;

notify pgrst, 'reload schema';
