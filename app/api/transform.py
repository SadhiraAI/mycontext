"""Transform API: one-shot transform, explain selection."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth.deps import get_current_user
from app.db.models import User
from app.services import transform_service

router = APIRouter(prefix="/api/transform", tags=["transform"])


class TransformRequest(BaseModel):
    """Transform request."""

    question: str


@router.post("")
async def transform_question(
    body: TransformRequest,
    user: User = Depends(get_current_user),
):
    """Transform question into context. No API key needed. Returns assembled, patterns, explanation, exports."""
    if not body.question.strip():
        raise HTTPException(400, detail="Question is required")
    include_ent = getattr(user, "enterprise_license", False)
    result = transform_service.transform_question(body.question.strip(), include_enterprise=include_ent)
    if not result:
        raise HTTPException(503, detail="Transform service unavailable")
    return result
