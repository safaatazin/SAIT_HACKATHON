import re

from app.db.object_events import search_object_events
from app.models.api import AskResponse
from app.models.object_event import ObjectEvent


def extract_object_name(question: str) -> str | None:
    normalized = question.strip().lower()
    patterns = [
        r"where (?:is|did i put|are) (?:my|the|a|an)?\s*(.+?)\??$",
        r"find (?:my|the|a|an)?\s*(.+?)\??$",
        r"looking for (?:my|the|a|an)?\s*(.+?)\??$",
    ]

    for pattern in patterns:
        match = re.search(pattern, normalized)
        if match:
            return match.group(1).strip(" .?!")

    return normalized if normalized else None


def _format_answer(event: ObjectEvent) -> str:
    return (
        f"I last saw your {event.object_name} {event.action.replace('_', ' ')} "
        f"at {event.location}."
    )


async def answer_question(question: str) -> AskResponse:
    object_name = extract_object_name(question)

    if not object_name:
        return AskResponse(
            question=question,
            answer="Please ask something like: Where is my calculator?",
        )

    matches = search_object_events(object_name, limit=5)
    if not matches:
        return AskResponse(
            question=question,
            object_name=object_name,
            answer=f"I couldn't find any recent records for '{object_name}'.",
        )

    best_match = max(matches, key=lambda event: event.confidence)
    return AskResponse(
        question=question,
        object_name=best_match.object_name,
        answer=_format_answer(best_match),
        location=best_match.location,
        confidence=best_match.confidence,
        image_url=best_match.image_url,
        scene_summary=best_match.scene_summary,
        matched_event=best_match,
    )
