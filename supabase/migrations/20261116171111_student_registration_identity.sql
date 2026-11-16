-- Extend the existing OSNGEO profiles and signup trigger.
alter table public.profiles
  add column provinsi text,
  add column nomor_hp text,
  add constraint profiles_provinsi_check check (
    provinsi in (
      'Aceh', 'Bali', 'Banten', 'Bengkulu', 'DI Yogyakarta', 'DKI Jakarta',
      'Gorontalo', 'Jambi', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur',
      'Kalimantan Barat', 'Kalimantan Selatan', 'Kalimantan Tengah', 'Kalimantan Timur', 'Kalimantan Utara',
      'Kepulauan Bangka Belitung', 'Kepulauan Riau', 'Lampung', 'Maluku', 'Maluku Utara',
      'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Papua', 'Papua Barat', 'Papua Barat Daya',
      'Papua Pegunungan', 'Papua Selatan', 'Papua Tengah', 'Riau',
      'Sulawesi Barat', 'Sulawesi Selatan', 'Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Utara',
      'Sumatera Barat', 'Sumatera Selatan', 'Sumatera Utara'
    )
  ),
  add constraint profiles_nomor_hp_check check (nomor_hp ~ '^[+]?[0-9]{8,15}$');

create schema osngeo_private;
revoke all on schema osngeo_private from public;
grant usage on schema osngeo_private to authenticated, supabase_auth_admin;

-- Read the caller's persisted role without recursing through profiles RLS.
create function osngeo_private.is_admin()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.profiles
    where id = (select auth.uid()) and role = 'admin'
  );
$$;

revoke execute on function osngeo_private.is_admin() from public, anon;
grant execute on function osngeo_private.is_admin() to authenticated;

drop policy "Admin baca semua" on public.profiles;
drop policy "Allow insert profiles" on public.profiles;
drop policy "Baca profil sendiri" on public.profiles;

alter table public.profiles enable row level security;
revoke all on table public.profiles from public, anon, authenticated;

-- Existing public catalog policies reference these columns to check admin access.
-- An anonymous caller has no profiles SELECT policy and sees zero rows.
grant select (id, role) on public.profiles to anon;
grant select on public.profiles to authenticated;
grant update (nama, role, status, status_expired) on public.profiles to authenticated;

create policy "Pengguna baca profil sendiri" on public.profiles
  for select to authenticated using (id = (select auth.uid()));

create policy "Admin baca semua profil" on public.profiles
  for select to authenticated using ((select osngeo_private.is_admin()));

create policy "Admin edit profil siswa" on public.profiles
  for update to authenticated
  using ((select osngeo_private.is_admin()))
  with check ((select osngeo_private.is_admin()));

-- Moving the existing function keeps its trigger binding on auth.users.
alter function public.handle_new_user() set schema osngeo_private;

create or replace function osngeo_private.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.profiles (id, nama, email, provinsi, nomor_hp, role, status, created_at)
  values (
    new.id,
    coalesce(nullif(pg_catalog.btrim(new.raw_user_meta_data ->> 'nama'), ''), new.email),
    new.email,
    nullif(pg_catalog.btrim(new.raw_user_meta_data ->> 'provinsi'), ''),
    nullif(pg_catalog.btrim(new.raw_user_meta_data ->> 'nomor_hp'), ''),
    'siswa',
    'gratis',
    pg_catalog.now()
  );
  return new;
end;
$$;

revoke execute on function osngeo_private.handle_new_user() from public, anon, authenticated;
grant execute on function osngeo_private.handle_new_user() to supabase_auth_admin;

update public.profiles as profile
set email = account.email
from auth.users as account
where profile.id = account.id
  and nullif(pg_catalog.btrim(profile.email), '') is null
  and nullif(pg_catalog.btrim(account.email), '') is not null;

notify pgrst, 'reload schema';
