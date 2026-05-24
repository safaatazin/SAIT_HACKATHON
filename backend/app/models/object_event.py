from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

ObjectAction = Literal["placed", "moved", "removed", "picked_up", "stored", "unknown"]


class ObjectEvent(BaseModel):
    id: str | None = None
    object_name: str
    action: ObjectAction
    location: str
    confidence: float = Field(ge=0.0, le=1.0)
    image_url: str | None = None
    scene_summary: str | None = None
    evidence: str | None = None
    created_at: datetime | None = None


class ObjectEventCreate(BaseModel):
    object_name: str
    action: ObjectAction
    location: str
    confidence: float = Field(ge=0.0, le=1.0)
    image_url: str | None = None
    scene_summary: str | None = None
    evidence: str | None = None
