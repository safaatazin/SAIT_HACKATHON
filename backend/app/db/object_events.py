from datetime import datetime

from app.db.supabase_client import get_supabase_client
from app.models.object_event import ObjectEvent, ObjectEventCreate


def _row_to_event(row: dict) -> ObjectEvent:
    return ObjectEvent(
        id=row["id"],
        object_name=row["object_name"],
        action=row["action"],
        location=row["location"],
        confidence=row["confidence"],
        image_url=row.get("image_url"),
        scene_summary=row.get("scene_summary"),
        evidence=row.get("evidence"),
        created_at=row.get("created_at"),
    )


def create_object_events(events: list[ObjectEventCreate]) -> list[ObjectEvent]:
    if not events:
        return []

    payload = [event.model_dump(exclude_none=True) for event in events]
    response = get_supabase_client().table("object_events").insert(payload).execute()
    return [_row_to_event(row) for row in response.data]


def get_recent_events(limit: int = 20) -> list[ObjectEvent]:
    response = (
        get_supabase_client()
        .table("object_events")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return [_row_to_event(row) for row in response.data]


def search_object_events(object_name: str, limit: int = 10) -> list[ObjectEvent]:
    response = (
        get_supabase_client()
        .table("object_events")
        .select("*")
        .ilike("object_name", f"%{object_name}%")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return [_row_to_event(row) for row in response.data]
