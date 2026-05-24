from pydantic import BaseModel, Field

from app.models.ai_response import VisionAnalysisResult
from app.models.object_event import ObjectEvent


class UploadFrameResponse(BaseModel):
    status: str
    difference_score: float | None = None
    image_url: str | None = None
    ai_result: VisionAnalysisResult | None = None
    saved_events: int = 0
    message: str | None = None


class AskRequest(BaseModel):
    question: str = Field(min_length=1, examples=["Where is my calculator?"])


class AskResponse(BaseModel):
    question: str
    object_name: str | None = None
    answer: str
    location: str | None = None
    confidence: float | None = None
    image_url: str | None = None
    scene_summary: str | None = None
    matched_event: ObjectEvent | None = None


class RecentEventsResponse(BaseModel):
    events: list[ObjectEvent]
    count: int
