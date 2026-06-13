"""
Route Suggester — Multi-angle analysis route planning.

Given a user question, decomposes it into distinct analytical dimensions
and proposes multiple differentiated template chains (routes). Each route
maps directly to agents in a multi-agent system: developers use the output
to decide how many agents to build and what each one does.

Subsumes the LLM paths of suggest_patterns() and build_workflow_chain()
while providing richer, multi-route output.
"""

from __future__ import annotations

import logging
from typing import Any

from .pattern_catalog import ENRICHED_CATALOG_TEXT, VALID_PATTERN_NAMES
from .schemas import AnalysisRoute, RouteAnalysis, RouteStep

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# LLM prompt
# ---------------------------------------------------------------------------

_ROUTE_SYSTEM_MSG = (
    "You are an expert cognitive-pattern architect specializing in multi-agent "
    "system design. You analyze questions to identify every meaningful "
    "analytical dimension, then design differentiated template pipelines for "
    "each dimension. You select templates with surgical precision from a "
    "catalog of 88 cognitive reasoning frameworks.\n\n"
    "CRITICAL RULES:\n"
    "- Each route MUST target a genuinely different analytical dimension "
    "(diagnostic, predictive, strategic, risk, communication, evaluation, "
    "creative, ethical). No two routes may share the same terminal template.\n"
    "- Each step in a route is an AGENT. Specify exactly what it receives "
    "and what it produces — these map to agent inputs and outputs.\n"
    "- Use ONLY exact snake_case template names from the catalog.\n"
    "- 2-4 steps per route. 2-6 routes total.\n"
    "- Respond with JSON matching the RouteAnalysis schema."
)


def _build_route_prompt(question: str, max_routes: int) -> str:
    return f"""USER QUESTION: "{question}"

TEMPLATE CATALOG (88 cognitive reasoning frameworks, with what each produces):
{ENRICHED_CATALOG_TEXT}

TASK: Analyze this question and design {max_routes} differentiated analysis routes.

STEP 1 — DECOMPOSE THE QUESTION:
Identify ALL meaningful analytical dimensions. Think about:
- What different stakeholders would want from this question (CFO vs PM vs engineer)
- What different analytical lenses apply (diagnostic, predictive, strategic, risk, trend, ethical)
- What different deliverable types are possible (root cause report vs forecast vs action plan)

STEP 2 — DESIGN ROUTES:
For each dimension, design a template pipeline where:
- Each template is an AGENT with a clear role
- Data flows from one agent to the next (specify receives/produces)
- The terminal template determines the route's unique analytical angle
- No two routes share the same terminal template

STEP 3 — RECOMMEND:
Which route should the user start with, and why?

Respond with ONLY valid JSON matching this schema:
{{
  "question_decomposition": "Analysis of dimensions, stakeholders, and scope...",
  "routes": [
    {{
      "label": "Human-readable route name",
      "dimension": "diagnostic|predictive|strategic|risk|communication|evaluation|creative|ethical",
      "rationale": "Why this angle matters for this specific question",
      "steps": [
        {{
          "template": "exact_template_name",
          "agent_role": "Plain-English role description",
          "receives": "user_input OR output from previous_template_name",
          "produces": "What this agent outputs",
          "params": {{"key": "value"}}
        }}
      ],
      "final_output": "What the complete route delivers"
    }}
  ],
  "recommendation": "Which route to start with and why"
}}"""


# ---------------------------------------------------------------------------
# Post-processing
# ---------------------------------------------------------------------------


def _deduplicate_terminal_templates(routes: list[AnalysisRoute]) -> list[AnalysisRoute]:
    """Drop routes that share a terminal template, keeping the first."""
    seen_terminals: set[str] = set()
    unique: list[AnalysisRoute] = []
    for route in routes:
        if not route.steps:
            continue
        terminal = route.steps[-1].template
        if terminal not in seen_terminals:
            seen_terminals.add(terminal)
            unique.append(route)
        else:
            logger.debug(
                "suggest_routes: dropping duplicate terminal-template route %r "
                "(terminal=%s already used)",
                route.label,
                terminal,
            )
    return unique


def _fuzzy_fix_template_names(steps: list[RouteStep]) -> list[RouteStep]:
    """Try to fix close-but-wrong template names via common substitutions."""
    fixed: list[RouteStep] = []
    for step in steps:
        name = step.template
        if name in VALID_PATTERN_NAMES:
            fixed.append(step)
            continue
        # Common LLM mistakes: plurals, missing/extra underscores
        candidates = [
            name.rstrip("s"),
            name + "er",
            name.replace("analyzer", "analyser"),
            name.replace("analyser", "analyzer"),
        ]
        matched = False
        for candidate in candidates:
            if candidate in VALID_PATTERN_NAMES:
                step.template = candidate
                fixed.append(step)
                matched = True
                break
        if not matched:
            logger.warning(
                "suggest_routes: dropping step with unknown template %r",
                name,
            )
    return fixed


# ---------------------------------------------------------------------------
# Main function
# ---------------------------------------------------------------------------


def suggest_routes(
    question: str,
    max_routes: int = 4,
    include_enterprise: bool = True,
    provider: str = "openai",
    temperature: float = 0,
    model: str | None = None,
    **kwargs: Any,
) -> RouteAnalysis:
    """Analyze a question and suggest multiple differentiated analysis routes.

    Each route is a template pipeline that maps directly to agents in a
    multi-agent system. Developers use the output to decide how many agents
    to build, what each one does, and how data flows between them.

    Args:
        question: The user's question or problem description.
        max_routes: Maximum number of routes to generate (2-6).
        include_enterprise: Include enterprise templates in suggestions.
        provider: LLM provider ("openai", "anthropic", "gemini").
        temperature: LLM temperature (default 0 for determinism).
        model: Override model name.
        **kwargs: Extra kwargs passed to the LLM.

    Returns:
        RouteAnalysis with question decomposition, routes, and recommendation.
    """
    from ..core import Context
    from ..foundation import Directive, Guidance
    from .schemas import (
        RouteAnalysis as RouteAnalysisSchema,
        get_instructor_client,
        parse_with_fallback,
    )

    max_routes = max(2, min(6, max_routes))
    prompt = _build_route_prompt(question, max_routes)
    resolved_model = model or "gpt-4o"

    # ── Attempt instructor-structured path ────────────────────────────────
    instructor_client = get_instructor_client(None)
    if instructor_client is not None:
        try:
            create_kw: dict = {
                "model": resolved_model,
                "response_model": RouteAnalysisSchema,
                "messages": [
                    {"role": "system", "content": _ROUTE_SYSTEM_MSG},
                    {"role": "user", "content": prompt},
                ],
                "max_retries": 2,
            }
            for _fwd in ("max_tokens", "top_p"):
                if _fwd in kwargs:
                    create_kw[_fwd] = kwargs[_fwd]
            if temperature != 0:
                create_kw["temperature"] = temperature

            result = instructor_client.chat.completions.create(**create_kw)
            return _postprocess(result, include_enterprise)
        except Exception as exc:
            logger.debug(
                "suggest_routes: instructor path failed (%s), falling back. Error: %s",
                type(exc).__name__,
                exc,
            )

    # ── Fallback: classic LLM call + Pydantic parse ──────────────────────
    ctx = Context(
        guidance=Guidance(
            role=("Expert cognitive-pattern architect specializing in multi-agent system design"),
            rules=[
                "Analyze questions to identify every meaningful analytical dimension.",
                "Design differentiated template pipelines for each dimension.",
                "Use ONLY exact snake_case names from the catalog.",
                "Each route targets a different dimension. No two routes share the same terminal template.",
                "Respond as valid JSON matching the RouteAnalysis schema.",
            ],
        ),
        directive=Directive(content=prompt),
    )
    exec_kw: dict = {"temperature": temperature, **kwargs}
    if model:
        exec_kw["model"] = model
    llm_result = ctx.execute(provider=provider, **exec_kw)
    raw = llm_result.response.strip()

    try:
        parsed = parse_with_fallback(RouteAnalysisSchema, raw)
        return _postprocess(parsed, include_enterprise)
    except (ValueError, Exception) as exc:
        logger.warning(
            "suggest_routes: could not parse LLM response: %s",
            exc,
        )
        return RouteAnalysis(
            question_decomposition=f"Failed to decompose: {question}",
            routes=[],
            recommendation="Parsing failed. Try again or use suggest_patterns() as fallback.",
        )


def _postprocess(result: RouteAnalysis, include_enterprise: bool = True) -> RouteAnalysis:
    """Validate template names, fix fuzzy matches, deduplicate terminals."""
    cleaned_routes: list[AnalysisRoute] = []
    for route in result.routes:
        fixed_steps = _fuzzy_fix_template_names(route.steps)
        if not fixed_steps:
            continue
        route.steps = fixed_steps
        cleaned_routes.append(route)

    result.routes = _deduplicate_terminal_templates(cleaned_routes)
    return result
