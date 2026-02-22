"""Execute API: run assembled context through LLM."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.keys import get_decrypted_key_for_user
from app.auth.deps import get_current_user
from app.db import get_db
from app.db.models import User
from app.services import execute_service

router = APIRouter(prefix="/api/execute", tags=["execute"])


class ExecuteRequest(BaseModel):
    """Execute request."""

    assembled_content: str
    provider: str = "openai"
    user_message: str = ""
    output_format: str | None = None  # json, markdown - append structured-output instructions


class SmartExecuteRequest(BaseModel):
    """Smart three-tier execution request."""

    question: str
    provider: str = "openai"


@router.post("")
async def execute(
    body: ExecuteRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Run assembled context through LLM with user's API key."""
    api_key = await get_decrypted_key_for_user(db, str(user.id), body.provider)
    if not api_key:
        raise HTTPException(
            400,
            detail=f"Add an API key for provider '{body.provider}' in Settings before executing",
        )

    content = body.assembled_content
    ofmt = (body.output_format or "").lower()
    if ofmt in ("json", "markdown"):
        from mycontext.utils import output_format
        content = content + "\n\n" + output_format(ofmt)

    result = execute_service.execute_context(
        assembled_content=content,
        provider=body.provider,
        api_key=api_key,
        user_message=body.user_message or "",
    )
    if not result:
        raise HTTPException(503, detail="Execute service unavailable")

    if "error" in result:
        raise HTTPException(502, detail=result["error"])

    return result


@router.post("/smart")
async def smart_execute(
    body: SmartExecuteRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Three-tier smart execution: auto-routes via complexity router."""
    api_key = await get_decrypted_key_for_user(db, str(user.id), body.provider)
    if not api_key:
        raise HTTPException(
            400, detail=f"Add an API key for '{body.provider}' in Settings to use Smart Execute",
        )
    has_enterprise = getattr(user, "enterprise_license", False)
    result = execute_service.smart_execute(
        question=body.question,
        provider=body.provider,
        api_key=api_key,
        include_enterprise=has_enterprise,
    )
    if not result:
        raise HTTPException(503, detail="Smart execute service unavailable")
    if "error" in result:
        raise HTTPException(502, detail=result["error"])
    return result
