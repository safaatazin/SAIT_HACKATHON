import base64
import json
import re
from pathlib import Path

import httpx

from app.config import Settings, get_settings
from app.models.ai_response import VisionAnalysisResult

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "vision_analysis.txt"


def _load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def _extract_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


async def _analyze_with_openai(image_bytes: bytes, settings: Settings) -> VisionAnalysisResult:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    encoded = base64.b64encode(image_bytes).decode("utf-8")
    payload = {
        "model": settings.openai_vision_model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": _load_prompt()},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}},
                ],
            }
        ],
        "response_format": {"type": "json_object"},
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json=payload,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

    return VisionAnalysisResult.model_validate(_extract_json(content))


async def _analyze_with_gemini(image_bytes: bytes, settings: Settings) -> VisionAnalysisResult:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    encoded = base64.b64encode(image_bytes).decode("utf-8")
    model = settings.gemini_vision_model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": _load_prompt()},
                    {"inline_data": {"mime_type": "image/jpeg", "data": encoded}},
                ]
            }
        ],
        "generationConfig": {"responseMimeType": "application/json"},
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, params={"key": settings.gemini_api_key}, json=payload)
        response.raise_for_status()
        content = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    return VisionAnalysisResult.model_validate(_extract_json(content))


async def _analyze_with_anthropic(image_bytes: bytes, settings: Settings) -> VisionAnalysisResult:
    if not settings.anthropic_api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not configured")

    encoded = base64.b64encode(image_bytes).decode("utf-8")
    payload = {
        "model": settings.anthropic_vision_model,
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": _load_prompt()},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": encoded,
                        },
                    },
                ],
            }
        ],
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.anthropic_api_key,
                "anthropic-version": "2023-06-01",
            },
            json=payload,
        )
        response.raise_for_status()
        content = response.json()["content"][0]["text"]

    return VisionAnalysisResult.model_validate(_extract_json(content))


async def analyze_room_image(image_bytes: bytes) -> VisionAnalysisResult:
    settings = get_settings()
    provider = settings.ai_provider.lower()

    if provider == "openai":
        return await _analyze_with_openai(image_bytes, settings)
    if provider == "gemini":
        return await _analyze_with_gemini(image_bytes, settings)
    if provider == "anthropic":
        return await _analyze_with_anthropic(image_bytes, settings)

    raise RuntimeError(f"Unsupported AI provider: {settings.ai_provider}")
