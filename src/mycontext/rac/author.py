"""Author and score Requirements-as-Code artifacts from cognitive patterns.

The mapping below is the heart of the bridge: each ``requirements.yaml`` section
is drafted by the cognitive pattern(s) best suited to it.

    task_taxonomy      -> question_analyzer, intent_recognizer, stakeholder_mapper
    rubrics            -> code_reviewer, comparative_analyzer, socratic_questioner
    action_risk_matrix -> risk_assessor, impact_assessor
    pre_mortem         -> future_scenario_planner, conflict_resolver

Authoring is offline by default (it emits the per-section prompts you can run
anywhere). With ``execute=True`` and a provider, each section is filled with LLM
output using your own API key.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import yaml

from ..version import __version__

# Section -> ordered list of cognitive patterns that draft it.
SECTION_TEMPLATES: dict[str, list[str]] = {
    "task_taxonomy": ["question_analyzer", "intent_recognizer", "stakeholder_mapper"],
    "rubrics": ["code_reviewer", "comparative_analyzer", "socratic_questioner"],
    "action_risk_matrix": ["risk_assessor", "impact_assessor"],
    "pre_mortem": ["future_scenario_planner", "conflict_resolver"],
}

_ANTI_GOAL_NOTE = (
    "Authored and scored by mycontext (authoring + scoring only). Enforcement — "
    "spec compilation, CI gates, human-in-the-loop approval, and budget/policy "
    "checks — is the responsibility of your own stack."
)


@dataclass
class RequirementsAuthor:
    """Draft and score Requirements-as-Code sections from cognitive patterns.

    Args:
        provider: LLM provider used only when ``execute=True``.
        execute: If True, run each section's pattern with your own API key to
            fill in drafted content. If False (default), emit the prompts only.
    """

    provider: str = "openai"
    execute: bool = False
    sections: dict[str, list[str]] = field(default_factory=lambda: dict(SECTION_TEMPLATES))

    def _draft_section(self, templates: list[str], task: str, **kwargs: Any) -> dict:
        from ..skills.pattern_registry import get_pattern, get_pattern_build_params

        entries = []
        for name in templates:
            try:
                pattern = get_pattern(name)
            except KeyError:
                continue
            primary, _ = get_pattern_build_params(name)
            context = pattern.build_context(**{primary: task})
            prompt = context.assemble()
            entry: dict[str, Any] = {"template": name, "prompt": prompt}
            if self.execute:
                try:
                    result = context.execute(provider=self.provider, **kwargs)
                    entry["draft"] = (
                        result if isinstance(result, str)
                        else getattr(result, "response", str(result))
                    )
                except Exception as exc:  # pragma: no cover - depends on live key
                    entry["error"] = str(exc)
            entries.append(entry)
        return {"templates": templates, "drafts": entries}

    def draft(self, task: str, **kwargs: Any) -> dict:
        """Draft a full requirements.yaml structure for ``task``."""
        doc: dict[str, Any] = {
            "version": 1,
            "task": task,
            "metadata": {
                "generated_by": f"mycontext-ai {__version__}",
                "mode": "authoring",
                "note": _ANTI_GOAL_NOTE,
            },
        }
        for section, templates in self.sections.items():
            doc[section] = self._draft_section(templates, task, **kwargs)
        return doc


def draft_requirements(
    task: str, provider: str = "openai", execute: bool = False, **kwargs: Any
) -> dict:
    """Convenience wrapper that drafts a requirements.yaml structure for ``task``."""
    return RequirementsAuthor(provider=provider, execute=execute).draft(task, **kwargs)


def to_yaml(requirements: dict) -> str:
    """Serialize a drafted requirements structure to YAML."""
    return yaml.safe_dump(requirements, sort_keys=False, allow_unicode=True, width=100)


def score_output(context_prompt: str, output: str, mode: str = "heuristic") -> dict:
    """Score a candidate ``output`` against the ``context_prompt`` that produced it.

    Offline by default (``mode='heuristic'``). Use this to score candidate rubric
    answers or agent outputs before handing the requirements to your own gates.
    """
    from ..core import Context
    from ..intelligence.output_evaluator import OutputEvaluator

    ctx = Context(directive=context_prompt)
    score = OutputEvaluator(mode=mode).evaluate(ctx, output)
    return {
        "overall": round(score.overall, 4),
        "dimensions": {d.value: round(v, 4) for d, v in score.dimensions.items()},
        "strengths": score.strengths,
        "weaknesses": score.weaknesses,
    }
