-- =====================================================================
-- FindIt - Supabase Schema (Hackathon MVP)
-- =====================================================================
-- Paste this whole file into the Supabase SQL editor and run it once.
-- Order: extensions -> tables -> indexes -> storage bucket -> sample
-- data -> example "last seen" query.
-- =====================================================================


-- ---------------------------------------------------------------------
-- 0. Extensions
-- ---------------------------------------------------------------------
-- gen_random_uuid() lives in pgcrypto on Supabase.
create extension if not exists "pgcrypto";


-- ---------------------------------------------------------------------
-- 1. scans table
--    One row per camera capture event.
-- ---------------------------------------------------------------------
create table if not exists public.scans (
    id              uuid        primary key default gen_random_uuid(),
    user_id         uuid        references auth.users(id) on delete cascade,
    image_path      text        not null,                   -- object key inside the scan-images bucket
    location_label  text,                                   -- e.g. "kitchen counter", "bedroom drawer"
    created_at      timestamptz not null default now()
);


-- ---------------------------------------------------------------------
-- 2. detected_items table
--    One row per object detected in a scan.
-- 3. Relationship: scans (1) --- (many) detected_items
--    FK with ON DELETE CASCADE so deleting a scan removes its items.
-- ---------------------------------------------------------------------
create table if not exists public.detected_items (
    id           uuid        primary key default gen_random_uuid(),
    scan_id      uuid        not null references public.scans(id) on delete cascade,
    item_name    text        not null,                      -- e.g. "keys", "wallet"
    confidence   real,                                      -- optional detection score in [0, 1]
    created_at   timestamptz not null default now()
);


-- ---------------------------------------------------------------------
-- 4. Indexes
--    - case-insensitive search on item_name
--    - fast FK joins
--    - "latest scans" feeds (global + per user)
-- ---------------------------------------------------------------------
create index if not exists idx_detected_items_item_name_lower
    on public.detected_items (lower(item_name));

create index if not exists idx_detected_items_scan_id
    on public.detected_items (scan_id);

create index if not exists idx_scans_created_at_desc
    on public.scans (created_at desc);

create index if not exists idx_scans_user_created
    on public.scans (user_id, created_at desc);


-- ---------------------------------------------------------------------
-- 5. Storage bucket: scan-images (private)
-- ---------------------------------------------------------------------
insert into storage.buckets (id, name, public)
values ('scan-images', 'scan-images', false)
on conflict (id) do nothing;

-- TODO (post-MVP): enable RLS and add policies, e.g.
--   alter table public.scans enable row level security;
--   alter table public.detected_items enable row level security;
--   create policy "users read own scans" on public.scans
--     for select using (auth.uid() = user_id);
--   -- plus matching storage.objects policies for the scan-images bucket.


-- ---------------------------------------------------------------------
-- 6. Sample data
--    Uses NULL for user_id so this works before Supabase Auth is set up.
-- ---------------------------------------------------------------------
-- Fixed scan ids keep the inserts deterministic and easy to query.
with
  demo as (
    select
      null::uuid as user_id,
      '11111111-1111-1111-1111-111111111111'::uuid as kitchen_scan_id,
      '22222222-2222-2222-2222-222222222222'::uuid as bedroom_scan_id
  ),
  ins_scans as (
    insert into public.scans (id, user_id, image_path, location_label, created_at)
    select kitchen_scan_id, user_id, 'demo/kitchen.jpg', 'kitchen counter', now() - interval '2 hours' from demo
    union all
    select bedroom_scan_id, user_id, 'demo/bedroom.jpg', 'bedroom drawer',  now() - interval '10 minutes' from demo
    on conflict (id) do nothing
    returning id
  )
insert into public.detected_items (scan_id, item_name, confidence)
select '11111111-1111-1111-1111-111111111111'::uuid, 'keys',    0.95
union all
select '11111111-1111-1111-1111-111111111111'::uuid, 'wallet',  0.88
union all
select '22222222-2222-2222-2222-222222222222'::uuid, 'phone',   0.91
union all
select '22222222-2222-2222-2222-222222222222'::uuid, 'glasses', 0.82;


-- ---------------------------------------------------------------------
-- 7. Useful query: last seen location of an item
--    Swap 'keys' for any item name. Case-insensitive thanks to the
--    lower(item_name) index above.
-- ---------------------------------------------------------------------
-- select s.location_label,
--        s.image_path,
--        s.created_at
-- from public.detected_items d
-- join public.scans s on s.id = d.scan_id
-- where lower(d.item_name) = lower('keys')
-- order by s.created_at desc
-- limit 1;
