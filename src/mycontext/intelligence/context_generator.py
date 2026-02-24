"""
Context Generator — Build a fully-populated Context from minimal inputs.

Provide a role and goal. An LLM fills in everything else: behavioral rules,
communication style, reasoning strategy, few-shot examples, output schema,
and guard rails. The result is a Context(research_flow=True) ready to
assemble and execute.

Example::

    from mycontext.intelligence import generate_context

    ctx = generate_context(
        role="Senior fraud analyst",
        goal="Detect suspicious transaction patterns in real-time",
        task="Analyze this batch of transactions for fraud signals",
        provider="openai",
    )
    print(ctx.assemble())
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from ..core import THINKING_STRATEGIES, Context
from ..foundation import Constraints, Directive, Guidance
from ..providers import get_provider

# ── Meta-prompt sent to the LLM ──────────────────────────────────────────────

_SYSTEM = (
    "You are an expert prompt engineer specialising in context engineering. "
    "Given a role and goal, you generate a complete, production-ready context "
    "specification as a JSON object. Every field must be specific and useful — "
    "not generic boilerplate."
)

_USER_TEMPLATE = """\
Generate a complete context specification for the following:

ROLE: {role}
GOAL: {goal}{task_block}

Return a JSON object with EXACTLY these fields:

{{
  "rules": [
    // 3-5 specific behavioral rules the LLM must follow.
    // Each rule should be concrete and verifiable, not vague.
  ],
  "style": "...",            // Communication tone and style in ~10 words
  "expertise": [             // 3-6 specific domain areas relevant to the role
    "...", "..."
  ],
  "thinking_strategy": "...", // Exactly one of: step_by_step | multiple_angles | verify | explain_simply | creative
                               // Choose the one that best fits the goal
  "examples": [              // 2-3 input→output demonstrations calibrated to the goal
    {{"input": "...", "output": "..."}},
    {{"input": "...", "output": "..."}}
  ],
  "output_schema": [         // 3-5 structured output fields
    {{"name": "...", "type": "str"}},
    {{"name": "...", "type": "str"}}
  ],
  "must_include": [          // 2-4 elements that MUST appear in every response
    "...", "..."
  ],
  "must_not_include": [      // 1-3 things the LLM must never include
    "...", "..."
  ]
}}

Rules for the rules field:
- Write rules the way you would write acceptance criteria — concrete, not preferences
- Each rule must directly serve the stated goal
- Bad: "Be thorough"  Good: "Every risk must include a probability score (Low/Medium/High)"

Return ONLY the JSON. No explanation. No markdown fences.
"""


@dataclass
class GeneratedContext:
    """
    Result of generate_context().

    Attributes:
        context: The fully-populated Context(research_flow=True) ready to use.
        generation_meta: Raw dict of what the LLM generated (useful for inspection/debugging).
    """

    context: Context
    generation_meta: dict[str, Any] = field(default_factory=dict)

    def assemble(self) -> str:
        """Convenience pass-through — assemble the underlying context."""
        return self.context.assemble()

    def execute(self, provider: str = "openai", **kwargs: Any) -> Any:
        """Convenience pass-through — execute the underlying context."""
        return self.context.execute(provider=provider, **kwargs)

    def to_context(self) -> Context:
        """Return the underlying Context object."""
        return self.context


def _parse_llm_json(text: str) -> dict[str, Any]:
    """
    Extract and parse the JSON object from LLM output into a validated ContextSpec.

    Uses the Pydantic ContextSpec schema for validation and type-safety.
    Falls back to raw JSON parse if schema validation fails (backward compatible).

    Handles:
    - Bare JSON responses
    - JSON wrapped in ```json ... ``` fences
    - Responses with leading/trailing prose
    """
    from .schemas import ContextSpec, parse_with_fallback

    # ── Pydantic-validated path ───────────────────────────────────────────────
    try:
        spec = parse_with_fallback(ContextSpec, text)
        return spec.to_dict()
    except (ValueError, Exception):
        pass

    # ── Legacy fallback: raw json.loads (keeps backward compatibility) ────────
    cleaned = text.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", cleaned)
    if fence_match:
        cleaned = fence_match.group(1).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(cleaned[start: end + 1])
        except json.JSONDecodeError:
            pass

    raise ValueError(
        f"Could not extract valid JSON from LLM response. "
        f"First 200 chars: {text[:200]!r}"
    )


def _spec_to_context(
    role: str,
    goal: str,
    task: str | None,
    spec: dict[str, Any],
) -> Context:
    """Build a Context(research_flow=True) from a validated spec dict."""

    # ── Validate thinking_strategy ────────────────────────────────────────────
    raw_strategy = str(spec.get("thinking_strategy", "")).strip().lower()
    thinking_strategy: str | None = raw_strategy if raw_strategy in THINKING_STRATEGIES else None

    # ── Guidance ──────────────────────────────────────────────────────────────
    guidance = Guidance(
        role=role,
        goal=goal,
        rules=[str(r) for r in spec.get("rules", []) if r],
        style=str(spec.get("style", "")).strip() or None,
        expertise=[str(e) for e in spec.get("expertise", []) if e] or None,
    )

    # ── Directive ─────────────────────────────────────────────────────────────
    directive = Directive(content=task) if task else None

    # ── Examples ─────────────────────────────────────────────────────────────
    raw_examples = spec.get("examples", [])
    examples: list[dict[str, str]] | None = None
    if isinstance(raw_examples, list) and raw_examples:
        cleaned = [
            {"input": str(ex.get("input", "")), "output": str(ex.get("output", ""))}
            for ex in raw_examples
            if isinstance(ex, dict) and ex.get("input") and ex.get("output")
        ]
        examples = cleaned if cleaned else None

    # ── Constraints ───────────────────────────────────────────────────────────
    raw_schema = spec.get("output_schema", [])
    output_schema: list[dict[str, str]] | None = None
    if isinstance(raw_schema, list) and raw_schema:
        cleaned_schema = [
            {"name": str(f.get("name", "")), "type": str(f.get("type", "str"))}
            for f in raw_schema
            if isinstance(f, dict) and f.get("name")
        ]
        output_schema = cleaned_schema if cleaned_schema else None

    must_include = [str(i) for i in spec.get("must_include", []) if i] or None
    must_not_include = [str(i) for i in spec.get("must_not_include", []) if i] or None

    constraints: Constraints | None = None
    if any(x is not None for x in [must_include, must_not_include, output_schema]):
        constraints = Constraints(
            must_include=must_include,
            must_not_include=must_not_include,
            output_schema=output_schema,
        )

    return Context(
        guidance=guidance,
        directive=directive,
        constraints=constraints,
        examples=examples,
        thinking_strategy=thinking_strategy,
        research_flow=True,
    )


def generate_context(
    role: str,
    goal: str,
    task: str | None = None,
    provider: str = "openai",
    model: str = "gpt-4o-mini",
    **kwargs: Any,
) -> GeneratedContext:
    """
    Build a fully-populated Context from a role and goal.

    An LLM generates the behavioral rules, communication style, expertise areas,
    reasoning strategy, few-shot examples, output schema, and guard rails.
    The result is a ``Context(research_flow=True)`` ready to assemble and execute.

    Args:
        role:     Who the AI should be. Be specific — seniority, domain, context.
                  Example: "Senior fraud analyst at a tier-1 investment bank"
        goal:     What success looks like for this interaction.
                  Example: "Detect suspicious transaction patterns with low false-positive rate"
        task:     Optional — the specific task to embed in the directive.
                  If omitted, the Context has no directive and you can set one later.
        provider: LLM provider for generation (default: "openai").
        model:    Model to use (default: "gpt-4o-mini" — fast and sufficient for generation).
        **kwargs: Additional kwargs passed to the LLM (e.g. temperature, api_key).

    Returns:
        GeneratedContext with:
          - .context      — the fully-populated Context(research_flow=True)
          - .generation_meta — the raw spec the LLM produced (for inspection)

    Raises:
        ValueError: If the LLM response cannot be parsed as valid JSON.
        RuntimeError: If the LLM call fails.

    Example::

        from mycontext.intelligence import generate_context

        result = generate_context(
            role="Senior fraud analyst",
            goal="Detect suspicious transaction patterns in real-time",
            task="Analyze this batch of 50 transactions for fraud signals",
            provider="openai",
        )

        # Inspect what was generated
        print(result.generation_meta)

        # Assemble the prompt
        print(result.assemble())

        # Execute directly
        response = result.execute(provider="openai")
        print(response.response)
    """
    if not role or not role.strip():
        raise ValueError("role must be a non-empty string")
    if not goal or not goal.strip():
        raise ValueError("goal must be a non-empty string")

    role = role.strip()
    goal = goal.strip()
    task_block = f"\nTASK: {task.strip()}" if task and task.strip() else ""

    user_prompt = _USER_TEMPLATE.format(
        role=role,
        goal=goal,
        task_block=task_block,
    )

    api_key = kwargs.pop("api_key", None)
    temperature = kwargs.pop("temperature", 0.4)

    # ── Attempt instructor-structured path ────────────────────────────────────
    from .schemas import ContextSpec, get_instructor_client
    instructor_client = get_instructor_client(None)

    if instructor_client is not None:
        try:
            response = instructor_client.chat.completions.create(
                model=model,
                response_model=ContextSpec,
                messages=[
                    {"role": "system", "content": _SYSTEM},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_retries=2,
            )
            spec = response.to_dict()
            context = _spec_to_context(role=role, goal=goal, task=task, spec=spec)
            return GeneratedContext(context=context, generation_meta=spec)
        except Exception as exc:
            import logging as _logging
            _logging.getLogger(__name__).debug(
                "generate_context: instructor path failed (%s), falling back. Error: %s",
                type(exc).__name__, exc,
            )

    # ── Fallback: classic LLM call + Pydantic/JSON parse ─────────────────────
    gen_ctx = Context(
        guidance=Guidance(role="Expert prompt engineer"),
        directive=Directive(content=user_prompt),
    )

    try:
        provider_instance = get_provider(provider, api_key=api_key)
        result = provider_instance.generate(
            gen_ctx,
            model=model,
            temperature=temperature,
            **kwargs,
        )
        raw_text = result.response
    except Exception as exc:
        raise RuntimeError(
            f"generate_context: LLM call failed ({provider}/{model}). "
            f"Check your API key and provider. Original error: {exc}"
        ) from exc

    # ── Parse ─────────────────────────────────────────────────────────────────
    try:
        spec = _parse_llm_json(raw_text)
    except ValueError as exc:
        raise ValueError(
            f"generate_context: Could not parse LLM response as JSON. "
            f"Try again — the model occasionally produces malformed output. "
            f"Details: {exc}"
        ) from exc

    # ── Build Context ─────────────────────────────────────────────────────────
    context = _spec_to_context(role=role, goal=goal, task=task, spec=spec)

    return GeneratedContext(context=context, generation_meta=spec)
