-- Run this in the Supabase SQL editor.

create table if not exists object_events (
  id uuid primary key default gen_random_uuid(),
  object_name text not null,
  action text not null check (
    action in ('placed', 'moved', 'removed', 'picked_up', 'stored', 'unknown')
  ),
  location text not null,
  confidence double precision not null check (confidence >= 0 and confidence <= 1),
  image_url text,
  scene_summary text,
  evidence text,
  created_at timestamptz not null default now()
);

create index if not exists object_events_object_name_idx
  on object_events (lower(object_name));

create index if not exists object_events_created_at_idx
  on object_events (created_at desc);
