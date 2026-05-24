from pydantic import BaseModel, Field

from app.models.object_event import ObjectAction


class VisionEvent(BaseModel):
    object_name: str
    action: ObjectAction
    location: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: str


class VisionAnalysisResult(BaseModel):
    events: list[VisionEvent]
    scene_summary: str
