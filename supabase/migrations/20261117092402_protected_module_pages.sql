alter table public.modul_materi
  add column folder_halaman text,
  add column jumlah_halaman integer,
  add constraint modul_materi_halaman_privat_check check (
    (folder_halaman is null and jumlah_halaman is null)
    or (
      folder_halaman is not null
      and folder_halaman ~ '^[a-z0-9][a-z0-9-]{1,79}$'
      and jumlah_halaman is not null and jumlah_halaman between 1 and 9999
      and file_url is null and akses is not distinct from 'platinum' and is_premium is true
    )
  );

create unique index modul_materi_folder_halaman_key
  on public.modul_materi (folder_halaman)
  where folder_halaman is not null;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('modul-halaman', 'modul-halaman', false, 2097152, array['image/webp']);

create policy "Platinum membaca halaman modul"
  on storage.objects for select to authenticated
  using (
    bucket_id = 'modul-halaman'
    and storage.allow_only_operation('object.get_authenticated')
    and (
      (select osngeo_private.membership_level()) = 2
      or (select osngeo_private.is_admin())
    )
    and exists (
      select 1
      from public.modul_materi m
      where m.folder_halaman = (storage.foldername(name))[1]
        and m.aktif is true and m.akses = 'platinum'
    )
  );
