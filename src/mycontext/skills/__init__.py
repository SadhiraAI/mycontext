"""
Agent Skills integration for mycontext.

- Skill: parse SKILL.md with optional input_schema and pattern
- SkillRunner: load → build Context → QualityMetrics → optional execute
- SkillRunResult: context, quality_score, execution_result, gated
- improvement_report, suggested_edits: quality report and edit suggestions for skill authors
- improve_skill_with_llm: use an LLM to improve SKILL.md from mycontext recommendations
"""

from .improvement import (
    improve_skill_with_llm,
    improvement_report,
    log_run,
    skill_health_report,
    suggested_edits,
    suggested_edits_from_log,
)
from .runner import SkillRunner, SkillRunResult
from .skill import Skill

__all__ = [
    "Skill",
    "SkillRunner",
    "SkillRunResult",
    "improvement_report",
    "suggested_edits",
    "improve_skill_with_llm",
    "log_run",
    "skill_health_report",
    "suggested_edits_from_log",
]
