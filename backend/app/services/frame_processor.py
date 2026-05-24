from app.config import get_settings
from app.db.object_events import create_object_events
from app.models.ai_response import VisionAnalysisResult
from app.models.api import UploadFrameResponse
from app.models.object_event import ObjectEventCreate
from app.services.ai_vision import analyze_room_image
from app.services.image_diff import ChangeDecision, classify_change, compute_difference_score
from app.services.storage import upload_frame

# In-memory previous frame per camera session (MVP).
_previous_frames: dict[str, bytes] = {}


async def process_uploaded_frame(
    image_bytes: bytes,
    session_id: str = "default",
    content_type: str = "image/jpeg",
) -> UploadFrameResponse:
    settings = get_settings()
    previous_bytes = _previous_frames.get(session_id)
    score = compute_difference_score(previous_bytes, image_bytes)
    decision = classify_change(
        score,
        settings.diff_ignore_threshold,
        settings.diff_save_only_threshold,
    )

    _previous_frames[session_id] = image_bytes

    if decision == ChangeDecision.IGNORE:
        return UploadFrameResponse(
            status="ignored",
            difference_score=score,
            message="Room has not changed enough to process.",
        )

    image_url = upload_frame(image_bytes, content_type=content_type)
    ai_result: VisionAnalysisResult | None = None
    saved_events = 0

    if decision == ChangeDecision.PROCESS_WITH_AI:
        ai_result = await analyze_room_image(image_bytes)
        events = [
            ObjectEventCreate(
                object_name=event.object_name,
                action=event.action,
                location=event.location,
                confidence=event.confidence,
                image_url=image_url,
                scene_summary=ai_result.scene_summary,
                evidence=event.evidence,
            )
            for event in ai_result.events
        ]
        create_object_events(events)
        saved_events = len(events)

    return UploadFrameResponse(
        status=decision.value,
        difference_score=score,
        image_url=image_url,
        ai_result=ai_result,
        saved_events=saved_events,
        message="Frame processed successfully.",
    )
