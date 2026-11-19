-- Video series: allow "segera tayang" rows without a YouTube link, add a series code,
-- and let everyone list coming-soon rows (they carry no link, so nothing is exposed).
alter table public.video_pembelajaran alter column youtube_id drop not null;
alter table public.video_pembelajaran add column if not exists kode text;

do $$
begin
  if not exists (
    select 1 from pg_policies
    where schemaname = 'public' and tablename = 'video_pembelajaran' and policyname = 'Semua lihat video segera tayang'
  ) then
    create policy "Semua lihat video segera tayang" on public.video_pembelajaran
      for select to anon, authenticated using (youtube_id is null);
  end if;
end $$;
