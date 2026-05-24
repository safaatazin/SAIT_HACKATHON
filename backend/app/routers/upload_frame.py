from fastapi import APIRouter, File, Form, UploadFile

from app.models.api import UploadFrameResponse
from app.services.frame_processor import process_uploaded_frame

router = APIRouter(prefix="/upload-frame", tags=["camera"])


@router.post("", response_model=UploadFrameResponse)
async def upload_frame(
    file: UploadFile = File(...),
    session_id: str = Form(default="default"),
) -> UploadFrameResponse:
    image_bytes = await file.read()
    content_type = file.content_type or "image/jpeg"
    return await process_uploaded_frame(image_bytes, session_id=session_id, content_type=content_type)
