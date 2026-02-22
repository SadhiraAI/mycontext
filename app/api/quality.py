"""Quality API: evaluate prompt/context quality."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.keys import get_decrypted_key_for_user
from app.auth.deps import get_current_user
from app.db import get_db
from app.db.models import User
from app.services import quality_service

router = APIRouter(prefix="/api/quality", tags=["quality"])


class EvaluateRequest(BaseModel):
    assembled_content: str
    mode: str = "fast"  # fast (heuristic) | accurate (LLM)
    provider: str = "openai"


@router.post("/evaluate")
async def evaluate(
    body: EvaluateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Evaluate prompt quality. Fast=free heuristic. Accurate=LLM (needs API key)."""
    mode_internal = "heuristic" if body.mode == "fast" else "llm"
    api_key = None
    if mode_internal == "llm":
        api_key = await get_decrypted_key_for_user(db, str(user.id), body.provider)
        if not api_key:
            raise HTTPException(
                400,
                detail=f"Add an API key for {body.provider} in Settings for Accurate mode",
            )

    result = quality_service.evaluate_context(
        assembled_content=body.assembled_content,
        mode=mode_internal,
        provider=body.provider,
        api_key=api_key,
    )
    if not result:
        raise HTTPException(503, detail="Quality evaluation unavailable")
    return result
