"""Custom template service: build Context from CustomTemplate.

Assembles all wizard steps into a single, research-backed prompt structure.

Prompt flow is grounded in peer-reviewed research:

  ┌─────────────────────────────────────────────────────────────────┐
  │  PRIMACY ZONE  (strongest recall — Liu et al. 2023)            │
  │  ① ROLE & IDENTITY  — who the AI is                            │
  │  ② GOAL             — what success looks like                  │
  ├─────────────────────────────────────────────────────────────────┤
  │  EARLY INSTRUCTIONS  (OpenAI: "put instructions at the start") │
  │  ③ RULES            — behavioral constraints (hard → easy)     │
  │  ④ STYLE            — communication tone                       │
  ├─────────────────────────────────────────────────────────────────┤
  │  MIDDLE  (demos stabilise here — Li et al. 2025 +6 pts)       │
  │  ⑤ REASONING        — thinking strategy injection              │
  │  ⑥ EXAMPLES         — few-shot demonstrations                  │
  ├─────────────────────────────────────────────────────────────────┤
  │  LATE  (output spec close to the ask — CO-STAR Response)       │
  │  ⑦ OUTPUT FORMAT    — structured schema                        │
  │  ⑧ GUARD RAILS      — must/must-not/format constraints         │
  ├─────────────────────────────────────────────────────────────────┤
  │  RECENCY ZONE  (up to +9.7 BLEU — Li et al. 2023)             │
  │  ⑨ TASK             — the actual instruction, ALWAYS LAST      │
  └─────────────────────────────────────────────────────────────────┘

References:
  • Liu et al. (2023) "Lost in the Middle" — primacy & recency bias
  • Li et al. (2023) "Instruction Position Matters" — post-instruction +9.7 BLEU
  • Li et al. (2025) "Where to Place Demos" — start placement +6 pts
  • CO-STAR Framework (GovTech Singapore, 2023) — Context→Objective→Style→Tone→Audience→Response
  • OpenAI Prompt Engineering Guide — "put instructions at the beginning, use ### to separate"
  • Anthropic Prompt Engineering Guide — XML-tagged sections for clarity
  • PASTA (ICLR 2024) — emphasis markers improve attention +22%
  • GUIDE (ICLR 2024) — tagged emphasis improves instruction-following 29→60%
  • Zhang et al. (2025) — hard-to-easy constraint ordering
"""

import json
import re
from typing import Any

STRATEGY_INJECTIONS = {
    "step_by_step": "Think through this step by step. Break the problem down into stages, show your reasoning at each stage, then give your final answer.",
    "multiple_angles": "Before answering, brainstorm at least 3 different approaches or perspectives. Briefly evaluate the strengths and weaknesses of each, then choose the best approach and explain why.",
    "verify": "After providing your answer, critically review it. Check for errors, missing information, unsupported claims, or logical gaps. If you find issues, revise your answer.",
    "explain_simply": "Explain your reasoning in simple, everyday language that anyone can understand. Avoid jargon and technical terms. Use analogies where helpful.",
    "creative": "Explore unconventional, surprising, and creative ideas. Don't limit yourself to the obvious answer. Challenge assumptions and consider perspectives that others might miss.",
}

STRATEGY_LABELS = {
    "step_by_step": "Chain of Thought",
    "multiple_angles": "Tree of Thought",
    "verify": "Self-Reflection",
    "explain_simply": "Simplification",
    "creative": "Divergent Thinking",
}

try:
    from mycontext import Context
    from mycontext.foundation import Directive, Guidance
except ImportError:
    Context = None
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


# ── Section builders ─────────────────────────────────────────────


def _section_role(role: str) -> str:
    return f"## ROLE\n\n**You are {role}.**"


def _section_goal(goal: str) -> str:
    if not goal:
        return ""
    return f"## GOAL\n\n**Objective:** {goal}"


def _section_rules(rules: list[str]) -> str:
    if not rules:
        return ""
    items = "\n".join(f"  {i+1}. {r}" for i, r in enumerate(rules))
    return f"## RULES\n\n**You MUST follow these rules at all times:**\n{items}"


def _section_style(style: str) -> str:
    if not style:
        return ""
    return f"## STYLE\n\n**Tone & voice:** {style}"


def _section_reasoning(thinking_strategy: str | None) -> str:
    text = STRATEGY_INJECTIONS.get(thinking_strategy or "", "")
    if not text:
        return ""
    label = STRATEGY_LABELS.get(thinking_strategy, "")
    header = f"## REASONING APPROACH ({label})" if label else "## REASONING APPROACH"
    return f"{header}\n\n**Important — {text}**"


def _section_examples(examples: list[dict[str, str]] | None) -> str:
    if not examples:
        return ""
    pairs = []
    for i, ex in enumerate(examples, 1):
        inp = ex.get("input", "").strip()
        out = ex.get("output", "").strip()
        if inp and out:
            pairs.append(f"**Example {i}:**\nInput: {inp}\nOutput: {out}")
    if not pairs:
        return ""
    return "## EXAMPLES\n\nLearn from these examples of expected input → output:\n\n" + "\n\n".join(pairs)


def _section_output_format(output_schema: list[dict[str, str]] | None) -> str:
    if not output_schema:
        return ""
    fields = [f for f in output_schema if f.get("name")]
    if not fields:
        return ""
    lines = ["## OUTPUT FORMAT", "", "**Return your response as a JSON object** with these required fields:", ""]
    for f in fields:
        lines.append(f"- **`{f['name']}`** ({f.get('type', 'str')})")
    lines.append("")
    skeleton = ", ".join(f'"{f["name"]}": ...' for f in fields)
    lines.append(f"```json\n{{{skeleton}}}\n```")
    return "\n".join(lines)


def _section_guard_rails(constraints_json: str | dict | None) -> str:
    """Render constraints with emphasis. Hard constraints first (Zhang et al. 2025)."""
    if not constraints_json:
        return ""
    try:
        c = json.loads(constraints_json) if isinstance(constraints_json, str) else constraints_json
    except (json.JSONDecodeError, TypeError):
        return ""
    if not c:
        return ""

    parts = ["## GUARD RAILS"]
    must_not = [i for i in (c.get("must_not_include") or []) if i]
    must = [i for i in (c.get("must_include") or []) if i]
    fmt = [i for i in (c.get("format_rules") or []) if i]

    if not must_not and not must and not fmt:
        return ""

    if must_not:
        items = "\n".join(f"  - {i}" for i in must_not)
        parts.append(f"\n**NEVER include the following:**\n{items}")
    if must:
        items = "\n".join(f"  - {i}" for i in must)
        parts.append(f"\n**ALWAYS include the following:**\n{items}")
    if fmt:
        items = "\n".join(f"  - {i}" for i in fmt)
        parts.append(f"\n**Format rules:**\n{items}")

    return "\n".join(parts)


def _section_task(directive_template: str, params: dict[str, Any]) -> str:
    text = _substitute(directive_template, params).strip()
    if not text:
        return ""
    return f"---\n\n## YOUR TASK\n\n{text}"


# ── Main builder ─────────────────────────────────────────────────


def build_custom_context(
    guidance_json: str,
    directive_template: str,
    params: dict[str, Any],
    constraints_json: str | dict | None = None,
    thinking_strategy: str | None = None,
    examples: list[dict[str, str]] | None = None,
    output_schema: list[dict[str, str]] | None = None,
) -> Any:
    """Build Context from custom template fields.

    Assembles a single, coherent prompt in research-backed order:

      PRIMACY ZONE   → ① Role  ② Goal
      INSTRUCTIONS   → ③ Rules  ④ Style
      MIDDLE         → ⑤ Reasoning  ⑥ Examples
      LATE           → ⑦ Output Format  ⑧ Guard Rails
      RECENCY ZONE   → ⑨ Task (ALWAYS LAST)

    We bypass the SDK's fragmented Guidance.render() / Constraints.render()
    chain and instead build the entire prompt as a single Directive so the
    ordering is guaranteed and the emphasis formatting is consistent.
    """
    if not Context or not Directive:
        return None

    try:
        g = json.loads(guidance_json) if isinstance(guidance_json, str) else guidance_json
        role = g.get("role", "Helpful Assistant")
        rules = g.get("rules", [])
        if isinstance(rules, str):
            rules = [r.strip() for r in rules.split("\n") if r.strip()]
        style = g.get("style") or ""
        goal = g.get("goal") or ""
    except (json.JSONDecodeError, TypeError):
        role, rules, style, goal = "Helpful Assistant", [], "", ""

    sections = [
        _section_role(role),
        _section_goal(goal),
        _section_rules(rules),
        _section_style(style),
        _section_reasoning(thinking_strategy),
        _section_examples(examples),
        _section_output_format(output_schema),
        _section_guard_rails(constraints_json),
        _section_task(directive_template, params),
    ]

    content = "\n\n".join(s for s in sections if s)
    if not content.strip():
        content = directive_template or "Respond helpfully."

    directive = Directive(content=content)
    return Context(directive=directive)
