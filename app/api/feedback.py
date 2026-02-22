"""Feedback API: collect user feedback (bug reports, feature requests, etc.)."""


from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import get_current_user
from app.db import get_db
from app.db.models import Feedback, User

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


class FeedbackRequest(BaseModel):
    feedback_type: str  # "bug" | "feature" | "general"
    message: str
    page_url: str | None = None


class FeedbackResponse(BaseModel):
    success: bool
    message: str


@router.post("", response_model=FeedbackResponse)
async def submit_feedback(
    body: FeedbackRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FeedbackResponse:
    """Store user feedback in the database."""
    fb = Feedback(
        user_id=user.id,
        feedback_type=body.feedback_type,
        message=body.message,
        page_url=body.page_url,
    )
    db.add(fb)
    await db.flush()
    return FeedbackResponse(success=True, message="Thank you for your feedback!")
