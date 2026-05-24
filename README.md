# FindIt - Supabase Database

FindIt is a hackathon MVP that uses a camera to remember where users put their stuff.

This repo contains the Supabase database design only. It does not include frontend or backend code.

## What's Included

- `scans` table for each camera scan event
- `detected_items` table for objects found in each scan
- One-to-many relationship from scans to detected items
- Indexes for item search and latest scans
- Private Supabase storage bucket named `scan-images`
- Sample insert data
- Example SQL query to find where an item was last seen

## How To Run

1. Open your Supabase project.
2. Go to SQL Editor.
3. Open `supabase/schema.sql`.
4. Paste the full SQL file into Supabase.
5. Click Run.

If the query says `Success. No rows returned`, that is normal for table, index, bucket, and insert commands.

## Verify The Data

Run these in the Supabase SQL Editor:

```sql
select * from public.scans;
select * from public.detected_items;
```

## Find Last Seen Item

Change `'keys'` to the item you want to search for:

```sql
select s.location_label,
       s.image_path,
       s.created_at
from public.detected_items d
join public.scans s on s.id = d.scan_id
where lower(d.item_name) = lower('keys')
order by s.created_at desc
limit 1;
```

## Notes

- Sample rows use `null` for `user_id` so the SQL works before Supabase Auth users exist.
- The `scan-images` bucket is private.
- Row Level Security policies are left as a post-MVP improvement.
