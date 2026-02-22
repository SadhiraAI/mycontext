"""
SkillRunner - Load skill, build Context, run QualityMetrics, optionally execute.

Returns SkillRunResult with context, quality_score, and execution_result.
When skill.pattern is set, fuses skill content with the named mycontext Pattern.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..core import Context
from ..intelligence.quality_metrics import QualityMetrics, QualityScore
from .improvement import log_run
from .pattern_registry import get_pattern
from .skill import Skill

# Parameter names that typically receive "task" or skill body when not in params
_PRIMARY_INPUT_KEYS = frozenset({
    "options", "problem", "statement", "decision", "topic", "concept", "situation",
    "input", "observation", "phenomenon", "challenge", "action", "conflict", "risk",
    "system", "project", "process", "objective", "goal", "sources", "text", "message",
    "complex_topic", "technical_text", "data_description",
})


def _fuse_pattern_context(skill: Skill, task: str | None, params: dict[str, Any]) -> Context:
    """
    Build a Context by fusing skill content with the named mycontext Pattern.

    Skill body + task become context/context_section; params and task fill
    pattern-specific inputs (options, problem, etc.).
    """
    pattern = get_pattern(skill.pattern)
    skill_content = (skill.body or "").strip()
    if task:
        skill_content += "\n\nTask: " + task
    instruction = skill.full_instructions(params)
    if instruction and instruction != skill_content:
        skill_content = instruction + ("\n\n" + skill_content if skill_content else "")

    sig = inspect.signature(pattern.build_context)
    kwargs: dict[str, Any] = {}
    for name, param in sig.parameters.items():
        if name in ("self", "kwargs"):
            continue
        if name in params:
            kwargs[name] = params[name]
        elif name in ("context", "context_section"):
            kwargs[name] = params.get(name) or skill_content
        elif name == "options" and name not in params:
            kwargs[name] = params.get("options") or ([task] if task else [])
        elif name in _PRIMARY_INPUT_KEYS and task and name not in params:
            kwargs[name] = task
        elif param.default is not inspect.Parameter.empty:
            kwargs[name] = param.default
        elif name in ("context", "context_section"):
            kwargs[name] = skill_content
        else:
            kwargs[name] = ""
    return pattern.build_context(**kwargs)


@dataclass
class SkillRunResult:
    """Result of running a skill: context, quality score, and optional execution result."""

    context: Context
    quality_score: QualityScore
    execution_result: Any | None = None
    skill: Skill | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    gated: bool = False  # True when execution was skipped due to quality_threshold


class SkillRunner:
    """
    Load a skill, build Context, evaluate quality, and optionally execute.

    - If skill has input_schema: validates and templates body with params.
    - When skill.pattern is set, fuses skill content with that mycontext Pattern.
    """

    def __init__(
        self,
        quality_metrics: QualityMetrics | None = None,
        log_runs: bool = False,
        log_path: Path | None = None,
    ):
        self._quality = quality_metrics or QualityMetrics()
        self._log_runs = log_runs
        self._log_path = log_path

    def load_skill(self, path: Path) -> Skill:
        """Load a skill from a directory or SKILL.md file."""
        return Skill.load(path)

    def build_context(
        self,
        skill: Skill,
        task: str | None = None,
        include_references: bool = True,
        **params: Any,
    ) -> Context:
        """
        Build a Context from the skill.

        If skill.pattern is set, fuses skill body/task/params with that mycontext
        Pattern and returns the Pattern's Context. Otherwise uses skill.to_context().
        """
        if not skill.pattern:
            return skill.to_context(
                task=task,
                include_references=include_references,
                **params,
            )
        skill.validate_params(params)
        ctx = _fuse_pattern_context(skill, task, params)
        if include_references and skill.path:
            ref_dir = skill.path / "references"
            if ref_dir.exists():
                parts = []
                for f in sorted(ref_dir.glob("*.md")):
                    parts.append(f.read_text(encoding="utf-8", errors="replace"))
                if parts:
                    knowledge = "\n\n---\n\n".join(parts)
                    ctx.knowledge = (ctx.knowledge + "\n\n" + knowledge) if ctx.knowledge else knowledge
        ctx.metadata["skill_name"] = skill.name
        ctx.metadata["skill_path"] = str(skill.path) if skill.path else None
        ctx.data["skill"] = skill.name
        ctx.data["task"] = task
        return ctx

    def run(
        self,
        skill_path: Path,
        task: str | None = None,
        execute: bool = False,
        provider: str = "openai",
        include_references: bool = True,
        quality_threshold: float | None = None,
        **params: Any,
    ) -> SkillRunResult:
        """
        Load skill, build Context, run QualityMetrics, optionally execute.

        Args:
            skill_path: Directory containing SKILL.md or path to SKILL.md.
            task: Optional task text (appended to directive).
            execute: If True, call context.execute(provider, **provider_kwargs).
            provider: LLM provider when execute=True.
            include_references: Include skill references folder in knowledge.
            quality_threshold: If set, do not execute when quality_score.overall < threshold.
            **params: Skill parameters (for input_schema) and provider kwargs if execute.

        Returns:
            SkillRunResult with context, quality_score, execution_result (if run), and gated (if skipped).
        """
        skill = self.load_skill(skill_path)
        context = self.build_context(
            skill,
            task=task,
            include_references=include_references,
            **{k: v for k, v in params.items() if k not in _PROVIDER_KWARGS},
        )
        quality_score = self._quality.evaluate(context)
        execution_result = None
        gated = False
        if execute:
            if quality_threshold is not None and quality_score.overall < quality_threshold:
                gated = True
            else:
                provider_kwargs = {k: v for k, v in params.items() if k in _PROVIDER_KWARGS}
                execution_result = context.execute(provider=provider, **provider_kwargs)
        result = SkillRunResult(
            context=context,
            quality_score=quality_score,
            execution_result=execution_result,
            skill=skill,
            metadata={"skill_path": str(skill.path), "task": task},
            gated=gated,
        )
        if self._log_runs:
            log_run(result, self._log_path)
        return result


# Known provider parameter names (for filtering from skill params)
_PROVIDER_KWARGS = {
    "model",
    "temperature",
    "max_tokens",
    "top_p",
    "frequency_penalty",
    "presence_penalty",
    "stop",
    "user",
    "api_key",
    "base_url",
}
