import uuid
from datetime import UTC, datetime

from app.config import get_settings
from app.db.supabase_client import get_supabase_client


def upload_frame(image_bytes: bytes, content_type: str = "image/jpeg") -> str:
    settings = get_settings()
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    filename = f"frames/{timestamp}_{uuid.uuid4().hex[:8]}.jpg"

    client = get_supabase_client()
    client.storage.from_(settings.supabase_storage_bucket).upload(
        path=filename,
        file=image_bytes,
        file_options={"content-type": content_type, "upsert": "false"},
    )

    public_url = client.storage.from_(settings.supabase_storage_bucket).get_public_url(filename)
    return public_url
