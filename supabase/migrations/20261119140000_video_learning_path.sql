-- Learning path metadata for the concept video series (stage, level, prerequisite codes).
alter table public.video_pembelajaran add column if not exists tahap text;
alter table public.video_pembelajaran add column if not exists level text;
alter table public.video_pembelajaran add column if not exists prasyarat text;
