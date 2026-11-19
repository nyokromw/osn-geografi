-- Midtrans orders are server-written. Sandbox payments never change profiles.
create table public.pembayaran_midtrans (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.profiles(id),
  paket_id integer not null references public.paket_membership(id),
  order_id text not null unique,
  environment text not null check (environment in ('sandbox', 'production')),
  nama_paket text not null,
  akses text not null check (akses in ('premium', 'platinum')),
  durasi_hari integer not null check (durasi_hari > 0),
  nominal integer not null check (nominal > 0),
  status text not null default 'created'
    check (status in ('created', 'pending', 'paid', 'expired', 'failed', 'review', 'refunded')),
  midtrans_status text,
  midtrans_transaction_id text unique,
  qr_url text,
  expires_at timestamptz not null default (now() + interval '15 minutes'),
  paid_at timestamptz,
  fulfilled_at timestamptz,
  membership_ends_at timestamptz,
  review_reason text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index pembayaran_midtrans_user_created_idx
  on public.pembayaran_midtrans(user_id, created_at desc);
create index pembayaran_midtrans_paket_idx on public.pembayaran_midtrans(paket_id);

alter table public.pembayaran_midtrans enable row level security;
revoke all on public.pembayaran_midtrans from public, anon, authenticated;
grant select on public.pembayaran_midtrans to authenticated;
grant select, insert, update on public.pembayaran_midtrans to service_role;

create policy "Pengguna baca pembayaran sendiri" on public.pembayaran_midtrans
  for select to authenticated using (user_id = (select auth.uid()));
create policy "Admin baca pembayaran Midtrans" on public.pembayaran_midtrans
  for select to authenticated using ((select osngeo_private.is_admin()));

-- Invoker functions are granted ONLY to the service role used by Edge Functions.
create function public.midtrans_create_order(p_user_id uuid, p_paket_id integer, p_environment text)
returns jsonb language plpgsql security invoker set search_path = '' as $$
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
$$;

-- Called only AFTER server-to-server verification with Midtrans GET Status API.
-- The row locks make notification retries and concurrent different orders safe.
create function public.midtrans_reconcile_order(
  p_order_id text, p_environment text, p_nominal numeric,
  p_transaction_id text, p_payment_type text, p_status text,
  p_status_code text, p_fraud_status text, p_currency text
)
returns public.pembayaran_midtrans
language plpgsql security invoker set search_path = '' as $$
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
      if account.status in ('premium', 'platinum') and
         (account.status_expired is null or account.status_expired > timezone('UTC', now())) and
         (account.status_expired is null or (account.status = 'platinum' and payment.akses = 'premium')) then
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
$$;

revoke execute on function public.midtrans_create_order(uuid, integer, text) from public, anon, authenticated;
grant execute on function public.midtrans_create_order(uuid, integer, text) to service_role;
revoke execute on function public.midtrans_reconcile_order(text, text, numeric, text, text, text, text, text, text)
  from public, anon, authenticated;
grant execute on function public.midtrans_reconcile_order(text, text, numeric, text, text, text, text, text, text)
  to service_role;

notify pgrst, 'reload schema';
