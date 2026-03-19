"""Templates API: list 85 patterns, build context."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException  # noqa: F401
from pydantic import BaseModel

from app.auth.deps import get_current_user
from app.db.models import User
from app.services import template_service

router = APIRouter(prefix="/api/templates", tags=["templates"])


class BuildRequest(BaseModel):
    """Build context request."""

    params: dict[str, Any]
    export_format: str | None = "markdown"  # openai, anthropic, json, markdown, yaml
    output_format: str | None = None  # json, markdown - request LLM to respond in this format


class GenericPromptRequest(BaseModel):
    """Request a filled generic prompt for a template."""

    question: str


@router.get("")
async def list_templates(
    user: User = Depends(get_current_user),
) -> list[dict[str, Any]]:
    """List all 85 templates from catalog."""
    return template_service.list_templates()


@router.get("/{name}/params")
async def get_params(
    name: str,
    user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """Get build_context params (primary + defaults) for a template."""
    params = template_service.get_template_params(name)
    if not params:
        raise HTTPException(404, detail="Template not found")
    return params


@router.post("/{name}/generic-prompt")
async def generic_prompt(
    name: str,
    body: GenericPromptRequest,
    user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """Get the filled generic prompt for a template given a question."""
    has_enterprise = getattr(user, "enterprise_license", False)
    prompt = template_service.get_generic_prompt(name, body.question, include_enterprise=has_enterprise)
    if prompt is None:
        raise HTTPException(404, detail="No generic prompt available for this template")
    return {"prompt": prompt, "template": name, "chars": len(prompt)}


@router.post("/{name}/build")
async def build_context(
    name: str,
    body: BuildRequest,
    user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """Build context for a template, optionally export in a format."""
    templates = template_service.list_templates()
    tpl = next((t for t in templates if t["name"] == name), None)
    if tpl and tpl.get("license") == "enterprise":
        has_ent = getattr(user, "enterprise_license", False)
        if not has_ent:
            raise HTTPException(403, detail="Enterprise template. Upgrade to use.")
    ctx = template_service.build_context(name, body.params)
    if not ctx:
        raise HTTPException(404, detail="Template not found or failed to build")

    from mycontext import Context as MxContext

    assembled = ctx.assemble()
    ofmt = (body.output_format or "").lower()
    has_output_section = "## OUTPUT FORMAT" in assembled
    if ofmt in ("json", "markdown") and not has_output_section:
        from mycontext.utils import output_format
        assembled = assembled + "\n\n" + output_format(ofmt)
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
    fmt = (body.export_format or "markdown").lower()
    if fmt not in exports:
        fmt = "markdown"
    return {"assembled": assembled, "exports": exports, "format": fmt}
