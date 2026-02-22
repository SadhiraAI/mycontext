"""Evaluation API: output scoring, CAI measurement, benchmarks."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.keys import get_decrypted_key_for_user
from app.auth.deps import get_current_user
from app.db import get_db
from app.services import evaluate_service

router = APIRouter(prefix="/api/evaluate", tags=["evaluate"])


class EvaluateOutputRequest(BaseModel):
    assembled_content: str
    llm_output: str
    mode: str = "fast"
    provider: str = "openai"


class MeasureCAIRequest(BaseModel):
    question: str
    template_name: str
    provider: str = "openai"
    eval_mode: str = "fast"
    model: Optional[str] = None


class RunBenchmarkRequest(BaseModel):
    template_name: str
    provider: str = "openai"
    eval_mode: str = "fast"
    model: Optional[str] = None


@router.post("/output")
async def evaluate_output(
    req: EvaluateOutputRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Score an LLM output against the context that produced it."""
    api_key = await get_decrypted_key_for_user(db, str(user.id), req.provider)
    result = evaluate_service.evaluate_output(
        assembled_content=req.assembled_content,
        llm_output=req.llm_output,
        mode=req.mode,
        provider=req.provider,
        api_key=api_key,
    )
    if result is None:
        raise HTTPException(500, detail="Evaluation service not available")
    return result


@router.post("/cai")
async def measure_cai(
    req: MeasureCAIRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Run Context Amplification Index measurement."""
    api_key = await get_decrypted_key_for_user(db, str(user.id), req.provider)
    if not api_key:
        raise HTTPException(
            400,
            detail="API key required for CAI measurement. Add one in Settings.",
        )

    eval_mode = {"fast": "heuristic", "accurate": "llm"}.get(req.eval_mode, req.eval_mode)
    try:
        result = evaluate_service.measure_cai(
            question=req.question,
            template_name=req.template_name,
            provider=req.provider,
            api_key=api_key,
            eval_mode=eval_mode,
            model=req.model,
        )
    except Exception as e:
        msg = str(e)
        if "api_key" in msg.lower() or "api key" in msg.lower():
            raise HTTPException(400, detail="API key may be invalid: " + msg)
        raise HTTPException(500, detail="CAI measurement failed: " + msg)

    if result is None:
        raise HTTPException(500, detail="CAI service not available")
    return result


@router.post("/benchmark")
async def run_benchmark(
    req: RunBenchmarkRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Run quality benchmark for a template. Requires API key."""
    api_key = await get_decrypted_key_for_user(db, str(user.id), req.provider)
    if not api_key:
        raise HTTPException(
            400, detail="API key required for benchmarks. Add one in Settings."
        )

    eval_mode = {"fast": "heuristic", "accurate": "llm"}.get(req.eval_mode, req.eval_mode)
    try:
        result = evaluate_service.run_benchmark(
            template_name=req.template_name,
            provider=req.provider,
            api_key=api_key,
            eval_mode=eval_mode,
            model=req.model,
        )
    except Exception as e:
        raise HTTPException(500, detail="Benchmark failed: " + str(e))

    if result is None:
        raise HTTPException(500, detail="Benchmark service not available")
    return result
