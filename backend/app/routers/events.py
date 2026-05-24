from fastapi import APIRouter, Query

from app.db.object_events import get_recent_events
from app.models.api import RecentEventsResponse

router = APIRouter(prefix="/recent-events", tags=["debug"])


@router.get("", response_model=RecentEventsResponse)
async def recent_events(limit: int = Query(default=20, ge=1, le=100)) -> RecentEventsResponse:
    events = get_recent_events(limit=limit)
    return RecentEventsResponse(events=events, count=len(events))
