create table public.video_beranda (
  posisi smallint primary key check (posisi between 1 and 3),
  judul text not null check (char_length(btrim(judul)) between 1 and 90),
  youtube_id text not null check (youtube_id ~ '^[A-Za-z0-9_-]{11}$')
);

alter table public.video_beranda enable row level security;
revoke all on public.video_beranda from public, anon, authenticated;
grant select on public.video_beranda to anon, authenticated;
grant insert, update on public.video_beranda to authenticated;

create policy "Video beranda bisa dibaca semua"
  on public.video_beranda for select to anon, authenticated using (true);
create policy "Admin tambah video beranda"
  on public.video_beranda for insert to authenticated with check ((select osngeo_private.is_admin()));
create policy "Admin edit video beranda"
  on public.video_beranda for update to authenticated
  using ((select osngeo_private.is_admin())) with check ((select osngeo_private.is_admin()));

insert into public.video_beranda (posisi, judul, youtube_id) values
  (1, 'Edukasi Bencana Tanah Longsor', 'UAPce7ywdeI'),
  (2, 'Volcanoes 101', 'VNGUdObDoLk'),
  (3, 'Why Do Rivers Have Deltas?', 'A47ythEcz74');

alter table public.paket_to
  add column kategori text not null default 'latihan'
    check (kategori in ('latihan', 'prediksi'));

update public.paket_to
set kategori = 'prediksi'
where nama ~* '\mpredi(ksi|ktif)\M';

-- Adjust the existing practice series only. Preserve package IDs and result history.
with ranked as (
  select p.id, p.jenis,
    row_number() over (partition by p.jenis order by p.urutan nulls last, p.id) as position
  from public.paket_to p
  where p.kategori = 'latihan' and p.status = 'aktif' and (
    (p.jenis = 'OSNK' and p.id between 1 and 25)
    or (p.jenis = 'OSNP' and p.id between 26 and 35)
  )
), assigned as (
  select ranked.id,
    case when position = 1 then 'gratis'
      when position <= case when jenis = 'OSNK' then 10 else 5 end then 'premium'
      else 'platinum' end as access,
    (jenis <> 'OSNK' or position <= 20 or exists (
      select 1 from public.hasil_to h where h.paket_id = ranked.id
    )) as published
  from ranked
)
update public.paket_to p
set akses = a.access,
    level = a.access,
    is_premium = (a.access <> 'gratis'),
    status = case when a.published then 'aktif' else 'nonaktif' end,
    aktif = a.published
from assigned a
where p.id = a.id;

update public.paket_membership
set fitur = to_jsonb(case id
  when 7 then replace(fitur #>> '{}', '4 tryout OSN-K lengkap dengan pembahasan',
    '1 latihan OSN-K dan 1 latihan OSN-P dengan pembahasan')
  when 8 then replace(replace(fitur #>> '{}', '10 paket OSN-K dan pembahasannya', '10 latihan OSN-K dengan pembahasan'),
    '5 paket OSN Provinsi dan pembahasannya', '5 latihan OSN-P dengan pembahasan')
  when 9 then replace(replace(fitur #>> '{}', '10 paket OSN-K dan pembahasannya', '10 latihan OSN-K dengan pembahasan'),
    '5 paket OSN Provinsi dan pembahasannya', '5 latihan OSN-P dengan pembahasan')
  else replace(replace(fitur #>> '{}', '20 paket OSN-K (termasuk 4 gratis) dan pembahasannya', '20 latihan OSN-K dengan pembahasan'),
    '10 paket OSN Provinsi dan pembahasannya', '10 latihan OSN-P dengan pembahasan')
end)
where id in (7, 8, 9, 10, 11) and jsonb_typeof(fitur) = 'string';

notify pgrst, 'reload schema';
