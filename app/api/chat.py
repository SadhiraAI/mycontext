"""Copilot chat API: guided context building + quality-gated refinement."""

import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.keys import get_decrypted_key_for_user
from app.auth.deps import get_current_user
from app.db import get_db
from app.db.models import User
from app.services import chat_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    mode: str = "guide"
    provider: str = "openai"
    model: str | None = None
    current_context: dict | None = None
    quality_score: dict | None = None
    stream: bool = False


class RefineRequest(BaseModel):
    assembled_content: str
    provider: str = "openai"
    model: str | None = None


@router.post("")
async def chat(
    body: ChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Copilot chat: guided context building or quality-gated refinement."""
    api_key = await get_decrypted_key_for_user(db, str(user.id), body.provider)
    if not api_key:
        raise HTTPException(
            400,
            detail=f"Add an API key for {body.provider} in Account settings to use the Copilot.",
        )

    conversation = [{"role": m.role, "content": m.content} for m in body.messages]
    llm_messages = chat_service.build_messages(
        conversation,
        mode=body.mode,
        current_context=body.current_context,
        quality_score=body.quality_score,
    )

    if body.stream:
        def event_stream():
            try:
                for chunk in chat_service.chat_completion_stream(
                    llm_messages, api_key, body.provider, model=body.model
                ):
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                yield "data: {\"done\": true}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    try:
        response = chat_service.chat_completion(
            llm_messages, api_key, body.provider, model=body.model
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(502, detail=f"LLM error: {e}") from None


@router.post("/refine")
async def refine(
    body: RefineRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Quality-gated refinement: score → suggest fixes → before/after."""
    api_key = await get_decrypted_key_for_user(db, str(user.id), body.provider)
    if not api_key:
        raise HTTPException(
            400,
            detail=f"Add an API key for {body.provider} in Account settings to use refinement.",
        )

    result = chat_service.refine_with_quality_gate(
        body.assembled_content, api_key, body.provider, model=body.model
    )
    if "error" in result:
        raise HTTPException(503, detail=result["error"])
    return result
