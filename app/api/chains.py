"""Chain API: suggest workflow chain, run orchestrator."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

from app.api.keys import get_decrypted_key_for_user
from app.auth.deps import get_current_user
from app.db import get_db
from app.db.models import User
from app.services import chain_service

router = APIRouter(prefix="/api/chains", tags=["chains"])


class SuggestRequest(BaseModel):
    """Suggest chain request."""

    question: str
    mode: str = "smart"  # quick (no key), smart (full LLM), best (hybrid)
    provider: str = "openai"
    use_question_analyzer: bool = True
    max_patterns: int | None = None
    include_enterprise: bool = True


class SuggestResponse(BaseModel):
    """Suggest chain response."""

    chain: list[str]
    chain_params: dict[str, dict[str, Any]]
    reasoning: str
    selection_reasoning: dict[str, str] = {}
    pattern_categories: dict[str, str] = {}
    question_analysis: dict[str, Any] | None = None
    template_decomposition: str | None = None


@router.post("/suggest", response_model=SuggestResponse)
async def suggest_chain(
    body: SuggestRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SuggestResponse:
    """Suggest workflow chain. Quick=no key, Smart/Best=needs key."""
    mode = (body.mode or "smart").lower()
    has_enterprise = getattr(user, "enterprise_license", False)
    include_ent = body.include_enterprise and has_enterprise
    if mode == "quick":
        result = chain_service.suggest_patterns_chain(
            body.question,
            mode="quick",
            include_enterprise=include_ent,
            max_patterns=body.max_patterns or 5,
        )
        if not result:
            raise HTTPException(503, detail="Chain suggestion service unavailable")
        selection = result.get("selection_reasoning") or {}
        cats = {p["name"]: p["category"] for p in result.get("suggested_patterns", [])}
        return SuggestResponse(
            chain=result["chain"],
            chain_params=result["chain_params"],
            reasoning=result.get("reasoning", ""),
            selection_reasoning=selection,
            pattern_categories=cats,
        )

    api_key = await get_decrypted_key_for_user(db, str(user.id), body.provider)
    if not api_key or not str(api_key).strip():
        raise HTTPException(
            400,
            detail=f"Add an API key for provider '{body.provider}' in Settings for Smart/Best modes",
        )

    if mode == "best":
        logger.info("Hybrid chain suggest: provider=%s", body.provider)
        try:
            result = chain_service.suggest_patterns_chain(
                body.question,
                mode="best",
                include_enterprise=include_ent,
                max_patterns=body.max_patterns or 5,
                llm_provider=body.provider,
                api_key=api_key,
            )
        except Exception as e:
            logger.error("Hybrid chain suggest exception: %s", e, exc_info=True)
            err_msg = str(e).lower()
            if "api_key" in err_msg or "api key" in err_msg:
                raise HTTPException(
                    400,
                    detail="Your API key may be invalid or not set correctly. Update it in Account > Settings.",
                ) from e
            raise
        if not result:
            raise HTTPException(503, detail="Chain suggestion service unavailable")
        logger.info("Hybrid chain result: chain=%s, reasoning_preview=%s", result.get("chain"), str(result.get("reasoning", ""))[:200])
        best_cats = {p["name"]: p["category"] for p in result.get("suggested_patterns", [])}
        return SuggestResponse(
            chain=result["chain"],
            chain_params=result["chain_params"],
            reasoning=result.get("reasoning", ""),
            selection_reasoning=result.get("selection_reasoning") or {},
            pattern_categories=best_cats,
        )

    logger.info("Smart chain suggest: provider=%s, mode=%s", body.provider, mode)
    try:
        result = chain_service.suggest_chain(
            body.question,
            provider=body.provider,
            use_question_analyzer=body.use_question_analyzer,
            max_patterns=body.max_patterns,
            include_enterprise=include_ent,
            api_key=api_key,
        )
    except Exception as e:
        logger.error("Smart chain suggest exception: %s", e, exc_info=True)
        err_msg = str(e).lower()
        if "api_key" in err_msg or "api key" in err_msg:
            raise HTTPException(
                400,
                detail="Your API key may be invalid or not set correctly. Update it in Account > Settings and ensure it has no extra spaces.",
            ) from e
        raise
    if not result:
        raise HTTPException(503, detail="Chain suggestion service unavailable")

    logger.info(
        "Smart chain result: chain=%s, reasoning_preview=%s",
        result.chain,
        (result.reasoning or "")[:200],
    )
    smart_cats = getattr(result, "pattern_categories", None) or chain_service.categories_for_chain(result.chain)

    return SuggestResponse(
        chain=result.chain,
        chain_params=result.chain_params,
        reasoning=result.reasoning,
        selection_reasoning=getattr(result, "selection_reasoning", {}) or {},
        pattern_categories=smart_cats,
        question_analysis=getattr(result, "question_analysis", None),
        template_decomposition=getattr(result, "template_decomposition", None),
    )


class IntegrateRequest(BaseModel):
    """Request to generate an integrated template from selected patterns."""

    question: str
    selected_templates: list[str]
    selection_reasoning: dict[str, str] = {}
    provider: str = "openai"


@router.post("/integrate")
async def integrate_templates(
    body: IntegrateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """LLM merges selected templates into one integrated context. Enterprise gated."""
    has_enterprise = getattr(user, "enterprise_license", False)

    cats = chain_service.categories_for_chain(body.selected_templates)
    enterprise_templates = [t for t, c in cats.items() if c == "enterprise"]
    if enterprise_templates and not has_enterprise:
        raise HTTPException(
            403,
            detail=f"Enterprise license required to integrate enterprise templates: {', '.join(enterprise_templates)}. "
                   "Remove them or upgrade your license.",
        )

    api_key = await get_decrypted_key_for_user(db, str(user.id), body.provider)
    if not api_key:
        raise HTTPException(400, detail=f"Add an API key for '{body.provider}' in Settings to use integration.")

    result = chain_service.generate_integrated_template(
        question=body.question,
        selected_templates=body.selected_templates,
        selection_reasoning=body.selection_reasoning,
        provider=body.provider,
        api_key=api_key,
        include_enterprise=has_enterprise,
    )
    if not result:
        raise HTTPException(503, detail="Integration service unavailable")
    if "error" in result:
        raise HTTPException(500, detail=result["error"])
    return result


class CompilePromptRequest(BaseModel):
    """Compile templates into a reusable prompt (LLM-refined)."""

    question: str
    template_names: list[str]
    provider: str = "openai"
    refine: bool = True


class CompileGenericRequest(BaseModel):
    """Compile generic prompts statically — zero LLM calls."""

    question: str
    template_names: list[str]


@router.post("/compile-prompt")
async def compile_prompt(
    body: CompilePromptRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Compile templates into a single prompt (dynamic, LLM-refined)."""
    has_enterprise = getattr(user, "enterprise_license", False)
    api_key = await get_decrypted_key_for_user(db, str(user.id), body.provider)
    if not api_key:
        raise HTTPException(400, detail=f"Add an API key for '{body.provider}' to compile prompts.")
    result = chain_service.compile_prompt(
        question=body.question,
        template_names=body.template_names,
        provider=body.provider,
        api_key=api_key,
        include_enterprise=has_enterprise,
        refine=body.refine,
    )
    if not result:
        raise HTTPException(503, detail="Compile service unavailable")
    if "error" in result:
        raise HTTPException(500, detail=result["error"])
    return result


@router.post("/compile-generic")
async def compile_generic(
    body: CompileGenericRequest,
    user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """Compile generic prompts statically — zero LLM calls."""
    has_enterprise = getattr(user, "enterprise_license", False)
    result = chain_service.compile_generic(
        question=body.question,
        template_names=body.template_names,
        include_enterprise=has_enterprise,
    )
    if not result:
        raise HTTPException(503, detail="Generic compile service unavailable")
    if "error" in result:
        raise HTTPException(500, detail=result["error"])
    return result


class ExecuteChainRequest(BaseModel):
    """Execute chain request."""

    chain: list[str]
    chain_params: dict[str, dict[str, Any]]
    initial_input: str
    topic: str = "Task"
    max_chars_per_step: int = 4000


@router.post("/execute")
async def execute_chain(
    body: ExecuteChainRequest,
    user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """Run the chain orchestrator (template-only, no LLM). Returns assembled output + exports."""
    output = chain_service.run_orchestrator(
        chain=body.chain,
        chain_params=body.chain_params,
        initial_input=body.initial_input,
        topic=body.topic,
        max_chars_per_step=body.max_chars_per_step,
    )
    if output is None:
        raise HTTPException(503, detail="Chain execution service unavailable")
    exports = chain_service.export_context(output)
    return {"output": output, "exports": exports}
