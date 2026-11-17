alter table public.modul_materi
  add column daftar_isi jsonb,
  add constraint modul_materi_daftar_isi_privat_check
    check (
      daftar_isi is null
      or (
        folder_halaman is not null
        and jsonb_typeof(daftar_isi) = 'object'
      )
    );
