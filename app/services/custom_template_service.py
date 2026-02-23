"""Custom template service: build Context from CustomTemplate.

Now delegates to the SDK's ``Context(research_flow=True)`` which implements
the same research-backed 9-section ordering.  See ``mycontext.core`` and
``docs/PROMPT_FLOW_RESEARCH.md`` for the full reference list.
"""

import json
import re
from typing import Any

try:
    from mycontext import Context
    from mycontext.foundation import Constraints, Directive, Guidance
except ImportError:
    Context = None
    Constraints = None
    Directive = None
    Guidance = None


def _substitute(template: str, params: dict[str, Any]) -> str:
    """Replace {{ name }} with params. Fallback to empty string."""
    result = template
    for key, val in params.items():
        placeholder = "{{ " + key + " }}"
        result = result.replace(placeholder, str(val) if val is not None else "")
    result = re.sub(r"\{\{\s*[\w_]+\s*\}\}", "", result)
    return result


def build_custom_context(
    guidance_json: str,
    directive_template: str,
    params: dict[str, Any],
    constraints_json: str | dict | None = None,
    thinking_strategy: str | None = None,
    examples: list[dict[str, str]] | None = None,
    output_schema: list[dict[str, str]] | None = None,
) -> Any:
    """Build a research-flow Context from custom template wizard fields.

    This is the bridge between the web-app's JSON fields and the SDK's
    ``Context(research_flow=True)`` engine.  All the heavy lifting
    (section ordering, emphasis formatting, guard-rail rendering) is
    now handled by the SDK core.
    """
    if not Context or not Directive:
        return None

    # ── Parse guidance JSON ──────────────────────────────────
    try:
        g = json.loads(guidance_json) if isinstance(guidance_json, str) else guidance_json
        role = g.get("role", "Helpful Assistant")
        rules = g.get("rules", [])
        if isinstance(rules, str):
            rules = [r.strip() for r in rules.split("\n") if r.strip()]
        style = g.get("style") or None
        goal = g.get("goal") or None
    except (json.JSONDecodeError, TypeError):
        role, rules, style, goal = "Helpful Assistant", [], None, None

    # ── Parse constraints JSON ───────────────────────────────
    c_must_include = None
    c_must_not_include = None
    c_format_rules = None
    if constraints_json:
        try:
            c = json.loads(constraints_json) if isinstance(constraints_json, str) else constraints_json
            c_must_include = [i for i in (c.get("must_include") or []) if i] or None
            c_must_not_include = [i for i in (c.get("must_not_include") or []) if i] or None
            c_format_rules = [i for i in (c.get("format_rules") or []) if i] or None
        except (json.JSONDecodeError, TypeError):
            pass

    # ── Build directive with variable substitution ───────────
    directive_content = _substitute(directive_template, params).strip()
    if not directive_content:
        directive_content = "Respond helpfully."

    # ── Assemble via SDK ─────────────────────────────────────
    constraints_obj = None
    if c_must_include or c_must_not_include or c_format_rules or output_schema:
        constraints_obj = Constraints(
            must_include=c_must_include,
            must_not_include=c_must_not_include,
            format_rules=c_format_rules,
            output_schema=output_schema,
        )

    return Context(
        guidance=Guidance(
            role=role,
            goal=goal,
            rules=rules,
            style=style,
        ),
        directive=Directive(content=directive_content),
        constraints=constraints_obj,
        thinking_strategy=thinking_strategy,
        examples=examples,
        research_flow=True,
    )
