from fastapi import APIRouter

from app.models.api import AskRequest, AskResponse
from app.services.object_search import answer_question

router = APIRouter(prefix="/ask", tags=["search"])


@router.post("", response_model=AskResponse)
async def ask(payload: AskRequest) -> AskResponse:
    return await answer_question(payload.question)
