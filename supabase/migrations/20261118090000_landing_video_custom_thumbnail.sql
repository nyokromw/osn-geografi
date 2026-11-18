-- Optional custom thumbnail per homepage carousel slot (falls back to the YouTube thumbnail).
alter table public.video_beranda
  add column thumbnail_url text
    check (thumbnail_url is null or thumbnail_url ~ '^(/[A-Za-z0-9._/-]+|https://\S+)$');

update public.video_beranda set thumbnail_url = '/brand/promo-thumbnail.jpg' where posisi = 1;

notify pgrst, 'reload schema';
