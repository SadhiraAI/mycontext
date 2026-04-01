"""
Fragments — reusable quality-enhancing building blocks for Blueprint composition.

Each fragment returns partial Constraints and/or Guidance rules that can be
merged into any Context to enhance output quality. Fragments are the composable
atoms that Blueprint orchestrates.

Usage::

    from mycontext.fragments import anti_fluff, answer_first, self_check_analysis

    # Apply to a Context
    ctx = some_template.build_context(...)
    anti_fluff.apply(ctx)
    answer_first.apply(ctx)

    # Or get the raw Constraints for manual use
    constraints = anti_fluff.constraints()
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core import Context

from ..foundation import Constraints, Guidance


@dataclass(frozen=True)
class Fragment:
    """A reusable quality-enhancing snippet that can be applied to any Context."""

    name: str
    description: str
    _constraints_kwargs: dict = field(default_factory=dict)
    _guidance_rules: list[str] = field(default_factory=list)

    def constraints(self) -> Constraints | None:
        if not self._constraints_kwargs:
            return None
        return Constraints(**self._constraints_kwargs)

    def guidance_rules(self) -> list[str]:
        return list(self._guidance_rules)

    def apply(self, ctx: Context) -> None:
        """Merge this fragment's quality settings into a Context in-place.

        - Constraints fields are set only if not already present on the Context.
        - Guidance rules are appended (no duplicates).
        """
        if self._constraints_kwargs:
            if ctx.constraints is None:
                ctx.constraints = Constraints(**self._constraints_kwargs)
            else:
                updates = {}
                for k, v in self._constraints_kwargs.items():
                    if getattr(ctx.constraints, k, None) is None:
                        updates[k] = v
                    elif isinstance(v, list) and isinstance(getattr(ctx.constraints, k), list):
                        existing = set(getattr(ctx.constraints, k))
                        merged = list(getattr(ctx.constraints, k)) + [
                            item for item in v if item not in existing
                        ]
                        updates[k] = merged
                if updates:
                    ctx.constraints = ctx.constraints.model_copy(update=updates)

        if self._guidance_rules and ctx.guidance:
            existing_rules = set(ctx.guidance.rules or [])
            new_rules = [r for r in self._guidance_rules if r not in existing_rules]
            if new_rules:
                updated = list(ctx.guidance.rules or []) + new_rules
                ctx.guidance = ctx.guidance.model_copy(update={"rules": updated})


# ── Output style fragments ────────────────────────────────────────────────────

anti_fluff = Fragment(
    name="anti_fluff",
    description="Ban stock AI filler and set a direct communication posture.",
    _constraints_kwargs={
        "communication_posture": "direct",
        "forbidden_phrases": [
            "in today's rapidly evolving",
            "it's worth noting that",
            "delve into",
            "game-changer",
            "tapestry of",
        ],
    },
)

answer_first_fragment = Fragment(
    name="answer_first",
    description="Lead with the conclusion, then supporting reasoning.",
    _constraints_kwargs={"answer_first": True},
)

show_reasoning = Fragment(
    name="show_reasoning",
    description="Explain the reasoning journey; do not skip to the answer.",
    _constraints_kwargs={
        "answer_first": False,
        "communication_posture": "educational",
    },
)

minimal_output = Fragment(
    name="minimal_output",
    description="Be concise — minimal verbosity.",
    _constraints_kwargs={"verbosity": "minimal"},
)

detailed_output = Fragment(
    name="detailed_output",
    description="Provide thorough, detailed analysis.",
    _constraints_kwargs={"verbosity": "detailed"},
)

# ── Objectivity fragments ─────────────────────────────────────────────────────

objectivity = Fragment(
    name="objectivity",
    description="Prioritize accuracy over agreeability. Push back on sycophancy.",
    _guidance_rules=[
        "Prioritize accuracy over validating the user's beliefs. Respectful correction is more valuable than false agreement.",
        "If the question's framing contains an unexamined assumption, name it before answering.",
    ],
)

# ── Self-check fragments ──────────────────────────────────────────────────────

self_check_analysis = Fragment(
    name="self_check_analysis",
    description="Analytical domain self-verification checks.",
    _constraints_kwargs={
        "self_check": [
            "Did I distinguish correlation from causation?",
            "Are my conclusions supported by the data, or am I extrapolating?",
            "Did I consider alternative explanations?",
        ],
    },
)

self_check_creative = Fragment(
    name="self_check_creative",
    description="Creative domain self-verification checks.",
    _constraints_kwargs={
        "self_check": [
            "Are at least 30% of ideas genuinely unconventional?",
            "Do any ideas essentially duplicate each other?",
            "Would a domain expert find at least one idea they had not considered?",
        ],
    },
)

self_check_communication = Fragment(
    name="self_check_communication",
    description="Communication domain self-verification checks.",
    _constraints_kwargs={
        "self_check": [
            "Would the target audience understand every sentence?",
            "Did I preserve the core message's accuracy while adapting?",
        ],
    },
)

# ── Output format fragments ───────────────────────────────────────────────────

structured_json = Fragment(
    name="structured_json",
    description="Enforce JSON output contract.",
    _constraints_kwargs={
        "output_contract": "Return ONLY a valid JSON object. No prose, no markdown wrapper.",
        "format_rules": ["Valid JSON only", "No trailing commas"],
    },
)

structured_markdown = Fragment(
    name="structured_markdown",
    description="Enforce markdown output contract.",
    _constraints_kwargs={
        "output_contract": "Return ONLY markdown with ## headings. No JSON wrapper.",
    },
)

# ── Grounding fragment ────────────────────────────────────────────────────────

grounding_strict = Fragment(
    name="grounding_strict",
    description="Strict source grounding — cite evidence, flag unsupported claims.",
    _constraints_kwargs={
        "must_include": ["source citations for every factual claim"],
    },
    _guidance_rules=[
        "Every factual claim must be traceable to provided material. If absent, state: '[NOT IN PACKET]'.",
        "Do not invent plausible-sounding facts to fill gaps.",
    ],
)


# ── Registry for programmatic access ──────────────────────────────────────────

ALL_FRAGMENTS: dict[str, Fragment] = {
    f.name: f
    for f in [
        anti_fluff,
        answer_first_fragment,
        show_reasoning,
        minimal_output,
        detailed_output,
        objectivity,
        self_check_analysis,
        self_check_creative,
        self_check_communication,
        structured_json,
        structured_markdown,
        grounding_strict,
    ]
}


def get_fragment(name: str) -> Fragment | None:
    """Look up a fragment by name."""
    return ALL_FRAGMENTS.get(name)
