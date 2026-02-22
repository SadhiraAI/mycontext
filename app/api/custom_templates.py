"""Custom templates API: CRUD + build."""

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import get_current_user
from app.db import get_db
from app.db.models import CustomTemplate, User
from app.services import custom_template_service

router = APIRouter(prefix="/api/templates/custom", tags=["custom-templates"])


class CreateTemplateRequest(BaseModel):
    name: str
    description: str | None = None
    guidance: dict[str, Any]  # {role, rules, style}
    directive_template: str
    input_schema: list[dict[str, Any]]  # [{name, type, default}]
    constraints: dict[str, Any] | None = None
    thinking_strategy: str | None = "direct"
    examples: list[dict[str, str]] | None = None  # [{input, output}]
    output_schema: list[dict[str, str]] | None = None  # [{name, type}]


class UpdateTemplateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    guidance: dict[str, Any] | None = None
    directive_template: str | None = None
    input_schema: list[dict[str, Any]] | None = None
    constraints: dict[str, Any] | None = None
    thinking_strategy: str | None = None
    examples: list[dict[str, str]] | None = None
    output_schema: list[dict[str, str]] | None = None


class BuildCustomRequest(BaseModel):
    params: dict[str, Any]
    output_format: str | None = None  # json, markdown - request LLM to respond in this format


class BuildPreviewRequest(BaseModel):
    """Build from template definition without saving. For demos and example panel."""
    guidance: dict[str, Any]
    directive_template: str
    input_schema: list[dict[str, Any]]
    params: dict[str, Any]
    output_format: str | None = None
    constraints: dict[str, Any] | None = None
    thinking_strategy: str | None = "direct"
    examples: list[dict[str, str]] | None = None
    output_schema: list[dict[str, str]] | None = None  # [{name, type}]


def _to_response(t: CustomTemplate) -> dict:
    return {
        "id": t.id,
        "name": t.name,
        "description": t.description,
        "guidance": json.loads(t.guidance) if t.guidance else {},
        "directive_template": t.directive_template,
        "input_schema": json.loads(t.input_schema) if t.input_schema else [],
        "constraints": json.loads(t.constraints) if t.constraints else None,
        "thinking_strategy": getattr(t, "thinking_strategy", None) or "direct",
        "examples": json.loads(t.examples) if getattr(t, "examples", None) else [],
        "output_schema": json.loads(t.output_schema) if getattr(t, "output_schema", None) else [],
        "created_at": t.created_at.isoformat() if t.created_at else None,
        "updated_at": t.updated_at.isoformat() if t.updated_at else None,
    }


@router.get("")
async def list_custom(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """List user's custom templates."""
    result = await db.execute(select(CustomTemplate).where(CustomTemplate.user_id == user.id))
    items = result.scalars().all()
    return [_to_response(t) for t in items]


@router.post("")
async def create_custom(
    body: CreateTemplateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Create a custom template."""
    result = await db.execute(
        select(CustomTemplate).where(CustomTemplate.user_id == user.id, CustomTemplate.name == body.name)
    )
    if result.scalar_one_or_none():
        raise HTTPException(400, detail="Template with this name already exists")
    t = CustomTemplate(
        user_id=user.id,
        name=body.name,
        description=body.description,
        guidance=json.dumps(body.guidance),
        directive_template=body.directive_template,
        input_schema=json.dumps(body.input_schema),
        constraints=json.dumps(body.constraints) if body.constraints else None,
        thinking_strategy=body.thinking_strategy or "direct",
        examples=json.dumps(body.examples) if body.examples else None,
        output_schema=json.dumps(body.output_schema) if body.output_schema else None,
    )
    db.add(t)
    await db.commit()
    await db.refresh(t)
    return _to_response(t)


@router.post("/build-preview")
async def build_preview(
    body: BuildPreviewRequest,
    user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """Build from template definition without saving. For example panel demos."""
    ctx = custom_template_service.build_custom_context(
        json.dumps(body.guidance),
        body.directive_template,
        body.params,
        json.dumps(body.constraints) if body.constraints else None,
        thinking_strategy=body.thinking_strategy,
        examples=body.examples,
        output_schema=body.output_schema,
    )
    if not ctx:
        raise HTTPException(500, detail="Failed to build context")
    assembled = ctx.assemble()
    ofmt = (body.output_format or "").lower()
    if ofmt in ("json", "markdown"):
        from mycontext.utils import output_format
        assembled = assembled + "\n\n" + output_format(ofmt)
    from mycontext import Context as MxContext
    ctx_export = MxContext(directive=assembled)
    exports = {
        "markdown": assembled,
        "json": ctx_export.to_json(),
        "yaml": ctx_export.to_yaml(),
        "openai": ctx_export.to_openai(),
        "anthropic": ctx_export.to_anthropic(),
        "google": ctx_export.to_google(),
        "langchain": ctx_export.to_langchain(),
        "llamaindex": ctx_export.to_llamaindex(),
    }
    return {"assembled": assembled, "exports": exports}


@router.get("/{id}")
async def get_custom(
    id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get one custom template."""
    result = await db.execute(
        select(CustomTemplate).where(CustomTemplate.id == id, CustomTemplate.user_id == user.id)
    )
    t = result.scalar_one_or_none()
    if not t:
        raise HTTPException(404, detail="Template not found")
    return _to_response(t)


@router.put("/{id}")
async def update_custom(
    id: str,
    body: UpdateTemplateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Update a custom template."""
    result = await db.execute(
        select(CustomTemplate).where(CustomTemplate.id == id, CustomTemplate.user_id == user.id)
    )
    t = result.scalar_one_or_none()
    if not t:
        raise HTTPException(404, detail="Template not found")
    if body.name is not None:
        t.name = body.name
    if body.description is not None:
        t.description = body.description
    if body.guidance is not None:
        t.guidance = json.dumps(body.guidance)
    if body.directive_template is not None:
        t.directive_template = body.directive_template
    if body.input_schema is not None:
        t.input_schema = json.dumps(body.input_schema)
    if body.constraints is not None:
        t.constraints = json.dumps(body.constraints)
    if body.thinking_strategy is not None:
        t.thinking_strategy = body.thinking_strategy
    if body.examples is not None:
        t.examples = json.dumps(body.examples) if body.examples else None
    if body.output_schema is not None:
        t.output_schema = json.dumps(body.output_schema) if body.output_schema else None
    await db.commit()
    await db.refresh(t)
    return _to_response(t)


@router.delete("/{id}")
async def delete_custom(
    id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Delete a custom template."""
    result = await db.execute(
        select(CustomTemplate).where(CustomTemplate.id == id, CustomTemplate.user_id == user.id)
    )
    t = result.scalar_one_or_none()
    if not t:
        raise HTTPException(404, detail="Template not found")
    await db.delete(t)
    await db.commit()
    return {"status": "deleted", "id": id}


@router.post("/{id}/build")
async def build_custom(
    id: str,
    body: BuildCustomRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Build context from custom template. Returns assembled + exports."""
    result = await db.execute(
        select(CustomTemplate).where(CustomTemplate.id == id, CustomTemplate.user_id == user.id)
    )
    t = result.scalar_one_or_none()
    if not t:
        raise HTTPException(404, detail="Template not found")
    saved_examples = json.loads(t.examples) if getattr(t, "examples", None) else None
    saved_output_schema = json.loads(t.output_schema) if getattr(t, "output_schema", None) else None
    ctx = custom_template_service.build_custom_context(
        t.guidance, t.directive_template, body.params, t.constraints,
        thinking_strategy=getattr(t, "thinking_strategy", None),
        examples=saved_examples,
        output_schema=saved_output_schema,
    )
    if not ctx:
        raise HTTPException(500, detail="Failed to build context")
    assembled = ctx.assemble()
    ofmt = (body.output_format or "").lower()
    if ofmt in ("json", "markdown"):
        from mycontext.utils import output_format
        assembled = assembled + "\n\n" + output_format(ofmt)
    from mycontext import Context as MxContext
    ctx_export = MxContext(directive=assembled)
    exports = {
        "markdown": assembled,
        "json": ctx_export.to_json(),
        "yaml": ctx_export.to_yaml(),
        "openai": ctx_export.to_openai(),
        "anthropic": ctx_export.to_anthropic(),
        "google": ctx_export.to_google(),
        "langchain": ctx_export.to_langchain(),
        "llamaindex": ctx_export.to_llamaindex(),
    }
    return {"assembled": assembled, "exports": exports}
