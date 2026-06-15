"""Cognitive-pattern brief for the requirements generators (``execute=True`` only).

The product/technical generators are deterministic and pattern-free when run
offline. When ``execute=True``, we additionally run a *small, curated* set of
cognitive patterns over the system intent — one cluster per high-leverage
section — and fold their analyses into the LLM fill pass as expert context. The
result: the open-question answers are grounded in real reasoning (a task
decomposition, a rubric design, a pre-mortem, an architecture trade-off study)
rather than the fill model's unaided guess.

This module owns only the *authoring* side (run patterns -> text brief). It does
not enforce anything, and it degrades gracefully: any pattern that errors or
returns nothing is simply skipped, so a missing key or offline provider never
breaks the fill — it just yields an empty brief.
"""

from __future__ import annotations

from typing import Any

# Section -> ordered cognitive patterns that inform it. Curated to the few
# highest-leverage sections of each spec (not every section) to bound cost.
PRODUCT_KEY_PATTERNS: dict[str, list[str]] = {
    "tasks": ["problem_decomposer", "gap_analyzer"],
    "rubrics": ["rubric_designer"],
    "safety": ["scenario_planner", "root_cause_analyzer"],
}

TECHNICAL_KEY_PATTERNS: dict[str, list[str]] = {
    "architecture": ["design_thinker", "decision_framework"],
    "guardrails": ["risk_mitigator"],
    "security": ["ethical_framework_analyzer"],
}

_PER_PATTERN_CHARS = 900


def run_pattern(name: str, text: str, *, provider: str, model: str | None) -> str:
    """Run a single cognitive pattern over ``text`` and return its output text.

    Returns an empty string if the pattern is unknown or the call fails — the
    caller treats an empty brief as "no extra context", never an error. A missing
    provider default is a *config* error, so it is resolved before the try block
    and allowed to propagate.
    """
    from .models import resolve_model

    resolved = resolve_model(provider, model)
    try:
        from ..skills.pattern_registry import get_pattern, get_pattern_build_params

        pattern = get_pattern(name)
        primary, _ = get_pattern_build_params(name)
        context = pattern.build_context(**{primary: text})
        result = context.execute(
            provider=provider,
            model=resolved,
            temperature=0,
            use_cache=True,
        )
        out = result if isinstance(result, str) else getattr(result, "response", str(result))
        return (out or "").strip()
    except Exception:  # pragma: no cover - depends on live provider/key
        return ""


def pattern_brief(
    section_patterns: dict[str, list[str]],
    text: str,
    *,
    provider: str,
    model: str | None,
) -> tuple[dict[str, dict[str, str]], str]:
    """Run the curated patterns for each section and build an expert brief.

    Returns ``(notes, brief_text)`` where ``notes`` is
    ``{section: {pattern_name: output}}`` (for transparency, attached to the
    spec) and ``brief_text`` is a compact, section-headed string suitable for
    injecting into the fill prompt. Empty pattern outputs are dropped.
    """
    notes: dict[str, dict[str, str]] = {}
    blocks: list[str] = []
    for section, names in section_patterns.items():
        section_notes: dict[str, str] = {}
        for name in names:
            out = run_pattern(name, text, provider=provider, model=model)
            if not out:
                continue
            section_notes[name] = out
            blocks.append(f"### {section} — {name}\n{out[:_PER_PATTERN_CHARS]}")
        if section_notes:
            notes[section] = section_notes
    return notes, "\n\n".join(blocks)


def analyze(
    text: str,
    *,
    kind: str = "product",
    provider: str = "openai",
    model: str | None = None,
) -> dict[str, dict[str, str]]:
    """Run the curated cognitive patterns for ``kind`` and return their analyses.

    This is the *grounding* layer behind ``execute=True``, exposed so you can read
    or render it directly: ``{section: {pattern_name: analysis_text}}``. ``kind``
    is ``"product"`` or ``"technical"``. Requires a provider API key (your own).
    Pair it with :func:`format_brief` to render readable markdown.
    """
    if kind == "product":
        section_map = PRODUCT_KEY_PATTERNS
    elif kind == "technical":
        section_map = TECHNICAL_KEY_PATTERNS
    else:
        raise ValueError(f"kind must be 'product' or 'technical', got {kind!r}")
    notes, _ = pattern_brief(section_map, text, provider=provider, model=model)
    return notes


def format_brief(notes: dict[str, dict[str, str]]) -> str:
    """Render the pattern analyses as readable markdown (for display, not specs).

    The spec itself never carries this prose — use this only to *show* what the
    cognitive patterns produced before the fill model distilled them into answers.
    """
    if not notes:
        return "_No pattern analyses (offline run or no API key)._"
    lines: list[str] = []
    for section, patterns in notes.items():
        lines.append(f"## `{section}`")
        for name, analysis in patterns.items():
            lines.append(f"### {name}")
            lines.append(analysis.strip())
            lines.append("")
    return "\n".join(lines).strip()


def provenance(notes: dict[str, dict[str, str]]) -> dict[str, list[str]]:
    """Collapse full pattern analyses to a clean ``{section: [pattern names]}`` map.

    The raw analyses are verbose prose used only to ground the fill model; we keep
    just this lightweight provenance on the spec so the output stays clean and
    still records *which* patterns shaped each section.
    """
    return {section: list(patterns) for section, patterns in notes.items() if patterns}
