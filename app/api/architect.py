"""Prompt Architect API: parse and improve any raw prompt using the 9-Section Architecture."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.keys import get_decrypted_key_for_user
from app.auth.deps import get_current_user
from app.db import get_db
from app.db.models import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/architect", tags=["architect"])


class ParseRequest(BaseModel):
    prompt: str


class ImproveRequest(BaseModel):
    prompt: str
    provider: str = "openai"
    model: str | None = None


@router.post("/parse")
async def parse_prompt(body: ParseRequest) -> dict[str, Any]:
    """Heuristic parse of a raw prompt — free, no LLM call.

    Detects which of the 9 sections (role, goal, rules, style, reasoning,
    examples, output_contract, guard_rails, task) are present or missing.
    """
    if not body.prompt or not body.prompt.strip():
        raise HTTPException(400, detail="Prompt cannot be empty.")

    try:
        from mycontext.intelligence import PromptArchitect

        arch = PromptArchitect()
        parsed = arch.parse(body.prompt)
        return {
            "present": parsed.present(),
            "missing": parsed.missing(),
            "sections": {
                "role": parsed.role,
                "goal": parsed.goal,
                "rules": parsed.rules,
                "style": parsed.style,
                "reasoning": parsed.reasoning,
                "examples": parsed.examples,
                "output_contract": parsed.output_contract,
                "guard_rails": parsed.guard_rails,
                "task": parsed.task,
            },
        }
    except Exception as e:
        logger.error("Prompt parse failed: %s", e, exc_info=True)
        raise HTTPException(500, detail="Parse failed. Please try again.") from e


@router.post("/improve")
async def improve_prompt(
    body: ImproveRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Improve a raw prompt using the 9-Section Architecture — requires API key.

    Steps: parse → score → LLM rewrites missing/weak sections → score again → diff.
    Returns before/after scores, section diffs, and the improved prompt.
    """
    if not body.prompt or not body.prompt.strip():
        raise HTTPException(400, detail="Prompt cannot be empty.")

    api_key = await get_decrypted_key_for_user(db, str(user.id), body.provider)
    if not api_key:
        raise HTTPException(
            400,
            detail=f"Add an API key for '{body.provider}' in Settings to use Prompt Improvement.",
        )

    try:
        from mycontext.intelligence import PromptArchitect

        model = body.model or "gpt-4o-mini"
        arch = PromptArchitect(provider=body.provider, model=model)
        # Inject the user's API key via litellm kwargs
        result = arch.improve(body.prompt, provider=body.provider, model=model, api_key=api_key)

        return {
            "improved_prompt": result.improved_prompt,
            "before_score": result.before_score,
            "after_score": result.after_score,
            "score_delta": result.score_delta,
            "diffs": [
                {
                    "section": d.section,
                    "action": d.action,
                    "before": d.before,
                    "after": d.after,
                    "rationale": d.rationale,
                }
                for d in result.diffs
            ],
            "before_issues": result.before_issues,
            "after_issues": result.after_issues,
            "resolved_issues": result.resolved_issues,
        }
    except Exception as e:
        logger.error("Prompt improve failed: %s", e, exc_info=True)
        err_msg = str(e).lower()
        if "api_key" in err_msg or "api key" in err_msg or "authentication" in err_msg:
            raise HTTPException(
                400,
                detail="Your API key may be invalid. Update it in Settings.",
            ) from e
        raise HTTPException(500, detail=f"Improvement failed: {e}") from e
