"""
Skill improvement - Report, suggested edits, and feedback loop.

Provides improvement_report(), suggested_edits(), log_run(), skill_health_report(),
suggested_edits_from_log(), and improve_skill_with_llm() for skill authors.
No automatic SKILL.md writes; improve_skill_with_llm() returns improved content for you to save.
"""

from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .runner import SkillRunResult

# Max task length stored in log (no PII)
_TASK_PREVIEW_LEN = 200

_DEFAULT_LOG_NAME = "skill_log.jsonl"


def improvement_report(result: SkillRunResult) -> str:
    """
    Format quality score into a short text report for the skill author.

    Includes overall score, issues, strengths, and suggestions.
    """
    q = result.quality_score
    lines = [
        "# Skill quality report",
        "",
        f"**Overall score:** {q.overall:.2f} (0–1)",
        "",
    ]
    if result.skill:
        lines.append(f"**Skill:** {result.skill.name}")
        lines.append("")
    if result.gated:
        lines.append("*Execution was skipped due to quality threshold.*")
        lines.append("")
    if q.issues:
        lines.append("## Issues")
        for i in q.issues:
            lines.append(f"- {i}")
        lines.append("")
    if q.strengths:
        lines.append("## Strengths")
        for s in q.strengths:
            lines.append(f"- {s}")
        lines.append("")
    if q.suggestions:
        lines.append("## Suggestions")
        for s in q.suggestions:
            lines.append(f"- {s}")
        lines.append("")
    if q.dimensions:
        lines.append("## Dimensions")
        for dim, score in q.dimensions.items():
            name = dim.value if hasattr(dim, "value") else str(dim)
            lines.append(f"- {name}: {score:.2f}")
    return "\n".join(lines).strip()


def suggested_edits(result: SkillRunResult) -> list[str]:
    """
    Map QualityScore suggestions to concrete edit suggestions for SKILL.md.

    Returns a list of suggested insertions or changes (e.g. body text to add).
    Author applies manually; no file writes.
    """
    q = result.quality_score
    edits: list[str] = []
    for s in q.suggestions:
        s = s.strip()
        if not s:
            continue
        # Map common suggestion patterns to concrete edits
        lower = s.lower()
        if "output format" in lower or "specify" in lower and "format" in lower:
            edits.append(
                f"Body: Add a line specifying output format, e.g. 'Always specify the output format (e.g. table, list, steps).' (from: {s})"
            )
        elif "step" in lower and ("add" in lower or "include" in lower):
            edits.append(f"Body: Consider adding an explicit step or bullet. Suggestion: {s}")
        elif "vague" in lower or "ambiguous" in lower:
            edits.append(f"Body: Replace vague language with concrete terms. Suggestion: {s}")
        elif "clarity" in lower or "clear" in lower:
            edits.append(f"Body: Improve clarity. Suggestion: {s}")
        elif "constraint" in lower or "boundary" in lower:
            edits.append(f"Body or constraints: Add boundaries or constraints. Suggestion: {s}")
        else:
            edits.append(f"Consider: {s}")
    for i in q.issues:
        i = i.strip()
        if i and i not in q.suggestions:
            edits.append(f"Address issue: {i}")
    return edits


def improve_skill_with_llm(
    result: SkillRunResult,
    skill_path: Path | None = None,
    current_content: str | None = None,
    provider: str = "openai",
    model: str = "gpt-4o-mini",
    temperature: float = 0.3,
    **kwargs,
) -> str | None:
    """
    Use an LLM to improve SKILL.md based on mycontext's recommendations.

    Builds a prompt from the current SKILL.md, the improvement report (issues,
    strengths, suggestions), and suggested_edits(result), then calls the given
    provider and returns the improved file content. Does not write files;
    the caller may save the returned string as SKILL.md.

    Args:
        result: SkillRunResult from SkillRunner.run() (holds quality_score and skill).
        skill_path: Path to SKILL.md or skill directory. Used to read current
            content if current_content is None.
        current_content: Current SKILL.md text. If None, read from skill_path
            (skill_path can be a file or a directory containing SKILL.md).
        provider: LLM provider name (e.g. "openai", "anthropic").
        model: Model name for the provider.
        temperature: Sampling temperature for the LLM.
        **kwargs: Passed to context.execute() (e.g. api_key).

    Returns:
        Improved SKILL.md content (markdown string), or None if the LLM was not
        called (e.g. missing API key or execution error).
    """
    from ..core import Context

    content = current_content
    if content is None and skill_path is not None:
        path = Path(skill_path)
        if path.is_dir():
            path = path / "SKILL.md"
        if path.exists():
            content = path.read_text(encoding="utf-8", errors="replace")
    if not content:
        return None

    report_text = improvement_report(result)
    edits = suggested_edits(result)
    edits_block = "\n".join(f"- {e}" for e in edits) if edits else "(none)"

    user_prompt = f"""Current SKILL.md:
---
{content}
---

Mycontext quality report (issues, strengths, suggestions):
{report_text}

Concrete edit suggestions from mycontext:
{edits_block}

Task: Rewrite the SKILL.md to address the issues and suggestions above. Preserve YAML frontmatter (name, description). Add or adjust sections (e.g. Constraints, Example) as recommended. Output only the new file content, no commentary before or after."""

    editor_context = Context(
        guidance="You are a skill author. You improve SKILL.md files by applying mycontext's quality feedback. Preserve the skill's intent and the Agent Skills format (frontmatter + markdown body).",
        directive="Output only the improved SKILL.md file content. No explanation before or after.",
    )

    if not os.environ.get("OPENAI_API_KEY") and provider == "openai":
        return None
    if provider == "anthropic" and not os.environ.get("ANTHROPIC_API_KEY"):
        return None

    try:
        resp = editor_context.execute(
            provider=provider,
            user=user_prompt,
            model=model,
            temperature=temperature,
            **kwargs,
        )
        improved = (resp.response or "").strip()
        if improved.startswith("```"):
            parts = improved.split("\n", 1)
            if len(parts) == 2:
                improved = parts[1].rsplit("```", 1)[0].strip()
            else:
                improved = improved.strip("`").strip()
        return improved if improved else None
    except Exception:
        return None


def log_run(result: SkillRunResult, log_path: Path | None = None) -> None:
    """
    Append one run to the skill log (JSONL). No PII; task is truncated.

    Args:
        result: SkillRunResult from runner.run().
        log_path: Path to JSONL file. If None, uses cwd/skill_log.jsonl.
    """
    from datetime import datetime

    p = Path(log_path) if log_path is not None else Path.cwd() / _DEFAULT_LOG_NAME
    skill_id = result.skill.name if result.skill else result.metadata.get("skill_path") or "unknown"
    task_preview = ""
    if result.metadata.get("task"):
        t = str(result.metadata["task"])[:_TASK_PREVIEW_LEN]
        task_preview = t + (
            "..." if len(str(result.metadata.get("task", ""))) > _TASK_PREVIEW_LEN else ""
        )
    record = {
        "skill_id": skill_id,
        "task_preview": task_preview,
        "overall": result.quality_score.overall,
        "issues": list(result.quality_score.issues),
        "suggestions": list(result.quality_score.suggestions),
        "gated": result.gated,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def skill_health_report(
    skill_id: str | None = None,
    log_path: Path | None = None,
) -> str:
    """
    Aggregate log entries and produce a short health report per skill.

    Args:
        skill_id: If set, report only this skill; else all skills in the log.
        log_path: Path to JSONL log. If None, uses cwd/skill_log.jsonl.

    Returns:
        Markdown report: avg score, common issues, suggestions.
    """
    p = Path(log_path) if log_path is not None else Path.cwd() / _DEFAULT_LOG_NAME
    if not p.exists():
        return "# Skill health report\n\nNo log found."
    by_skill: dict = defaultdict(lambda: {"scores": [], "issues": [], "suggestions": []})
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                sid = rec.get("skill_id", "unknown")
                by_skill[sid]["scores"].append(rec.get("overall", 0.0))
                by_skill[sid]["issues"].extend(rec.get("issues") or [])
                by_skill[sid]["suggestions"].extend(rec.get("suggestions") or [])
            except (json.JSONDecodeError, TypeError):
                continue
    if skill_id is not None:
        by_skill = {k: v for k, v in by_skill.items() if k == skill_id}
    lines = ["# Skill health report", ""]
    for sid, data in sorted(by_skill.items()):
        scores = data["scores"]
        avg = sum(scores) / len(scores) if scores else 0.0
        n = len(scores)
        lines.append(f"## {sid}")
        lines.append(f"- Runs: {n}")
        lines.append(f"- Average score: {avg:.2f}")
        issues = data["issues"]
        if issues:
            common = Counter(issues).most_common(5)
            lines.append("- Frequent issues:")
            for issue, count in common:
                lines.append(f"  - [{count}x] {issue}")
        suggestions = data["suggestions"]
        if suggestions:
            common_s = Counter(suggestions).most_common(3)
            lines.append("- Common suggestions:")
            for s, count in common_s:
                lines.append(f"  - [{count}x] {s}")
        lines.append("")
    return "\n".join(lines).strip()


def suggested_edits_from_log(
    skill_id: str,
    log_path: Path | None = None,
    min_count: int = 2,
) -> list[str]:
    """
    Suggest edits from frequent QualityScore.suggestions for this skill in the log.

    Args:
        skill_id: Skill name or path to filter.
        log_path: Path to JSONL log. If None, uses cwd/skill_log.jsonl.
        min_count: Minimum times a suggestion must appear to be included.

    Returns:
        List of suggested edits (same style as suggested_edits()).
    """
    p = Path(log_path) if log_path is not None else Path.cwd() / _DEFAULT_LOG_NAME
    if not p.exists():
        return []
    all_suggestions: list[str] = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                if rec.get("skill_id") != skill_id:
                    continue
                all_suggestions.extend(rec.get("suggestions") or [])
            except (json.JSONDecodeError, TypeError):
                continue
    freq = Counter(all_suggestions)
    edits = []
    for s, count in freq.most_common():
        if count < min_count:
            break
        s = s.strip()
        if s:
            edits.append(f"[{count}x] Consider: {s}")
    return edits
