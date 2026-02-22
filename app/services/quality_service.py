"""Quality service: evaluate context/prompt quality."""

from typing import Any

try:
    from mycontext import Context
    from mycontext.foundation import Guidance, Directive, Constraints
    from mycontext.intelligence import QualityMetrics
    from mycontext.intelligence.quality_metrics import QualityDimension, QualityScore
except ImportError:
    Context = None
    Guidance = None
    Directive = None
    Constraints = None
    QualityMetrics = None
    QualityDimension = None
    QualityScore = None

ENV_KEYS = {"openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY", "google": "GOOGLE_API_KEY"}


def _parse_assembled_to_context(text: str):
    """
    Reconstruct a structured Context from assembled text so the evaluator
    can properly detect guidance, directive, and constraints instead of
    treating everything as a flat directive string.
    """
    if not Context or not Guidance or not Directive:
        return Context(directive=text)

    lines = text.split("\n")
    role = None
    rules = []
    style = None
    goal = None
    directive_lines = []
    constraints_must_include = []
    constraints_must_not = []
    constraints_format_rules = []

    section = "preamble"  # preamble | rules | constraints_inc | constraints_not | constraints_fmt | directive

    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()

        # Detect role
        if lower.startswith("you are ") and not role:
            role = stripped[8:].rstrip(".")
            continue

        # Detect goal
        if lower.startswith("## goal") or lower.startswith("goal:"):
            goal_text = stripped.split(":", 1)[1].strip() if ":" in stripped else ""
            if goal_text:
                goal = goal_text
            section = "goal"
            continue
        if section == "goal" and stripped and not stripped.startswith("#"):
            goal = stripped
            section = "preamble"
            continue

        # Detect rules section
        if "follow these rules:" in lower or lower == "follow these rules:":
            section = "rules"
            continue
        if section == "rules":
            if stripped and (stripped[0].isdigit() or stripped.startswith("- ") or stripped.startswith("* ")):
                rule_text = stripped.lstrip("0123456789.-* ").strip()
                if rule_text:
                    rules.append(rule_text)
                continue
            elif stripped == "":
                section = "preamble"
                continue
            else:
                section = "preamble"

        # Detect style
        if lower.startswith("communication style:"):
            style = stripped.split(":", 1)[1].strip()
            continue

        # Detect constraints
        if lower.startswith("constraints:"):
            section = "constraints"
            continue
        if lower.startswith("must include:"):
            section = "constraints_inc"
            continue
        if lower.startswith("must not include:"):
            section = "constraints_not"
            continue
        if lower.startswith("format rules:"):
            section = "constraints_fmt"
            continue

        if section == "constraints_inc":
            if stripped.startswith("- ") or stripped.startswith("* "):
                constraints_must_include.append(stripped.lstrip("- *").strip())
                continue
            elif stripped == "":
                continue
            else:
                section = "directive"
        if section == "constraints_not":
            if stripped.startswith("- ") or stripped.startswith("* "):
                constraints_must_not.append(stripped.lstrip("- *").strip())
                continue
            elif stripped == "":
                continue
            else:
                section = "directive"
        if section == "constraints_fmt":
            if stripped.startswith("- ") or stripped.startswith("* "):
                constraints_format_rules.append(stripped.lstrip("- *").strip())
                continue
            elif stripped == "":
                continue
            else:
                section = "directive"
        if section == "constraints":
            if stripped == "":
                continue
            if stripped.startswith("Must include"):
                section = "constraints_inc"
                continue
            if stripped.startswith("Must NOT"):
                section = "constraints_not"
                continue
            if stripped.startswith("Format rules"):
                section = "constraints_fmt"
                continue
            section = "directive"

        # Everything else is directive content
        directive_lines.append(line)

    # Build structured Context
    guidance = None
    if role:
        guidance = Guidance(
            role=role,
            rules=rules if rules else [],
            style=style,
        )

    directive = None
    dir_text = "\n".join(directive_lines).strip()
    if dir_text:
        directive = Directive(content=dir_text)

    constraints = None
    if constraints_must_include or constraints_must_not or constraints_format_rules:
        kwargs = {}
        if constraints_must_include:
            kwargs["must_include"] = constraints_must_include
        if constraints_must_not:
            kwargs["must_not_include"] = constraints_must_not
        if constraints_format_rules:
            kwargs["format_rules"] = constraints_format_rules
        try:
            constraints = Constraints(**kwargs)
        except Exception:
            pass

    if guidance or constraints:
        return Context(
            guidance=guidance,
            directive=directive or Directive(content=text),
            constraints=constraints,
        )

    # Fallback: couldn't parse, use as flat directive
    return Context(directive=text)


def evaluate_context(
    assembled_content: str,
    mode: str = "heuristic",
    provider: str = "openai",
    api_key: str | None = None,
) -> dict[str, Any] | None:
    """Evaluate quality of assembled context. Returns score dict or None."""
    if not Context or not QualityMetrics:
        return None

    ctx = _parse_assembled_to_context(assembled_content)

    if mode in ("llm", "accurate") and api_key:
        import os

        key = ENV_KEYS.get(provider, "OPENAI_API_KEY")
        old = os.environ.get(key)
        try:
            os.environ[key] = api_key
            metrics = QualityMetrics(mode="llm", llm_provider=provider)
            score = metrics.evaluate(ctx)
        finally:
            if old is not None:
                os.environ[key] = old
            elif key in os.environ:
                os.environ.pop(key)
    else:
        metrics = QualityMetrics(mode="heuristic")
        score = metrics.evaluate(ctx)

    dims = {}
    if hasattr(score, "dimensions"):
        for d, v in score.dimensions.items():
            k = d.value if hasattr(d, "value") else str(d)
            dims[k] = round(float(v), 3)

    return {
        "overall": round(score.overall, 3),
        "dimensions": dims,
        "issues": list(score.issues) if score.issues else [],
        "strengths": list(score.strengths) if score.strengths else [],
        "suggestions": list(score.suggestions) if score.suggestions else [],
        "metadata": getattr(score, "metadata", {}) or {},
    }
