"""
Intelligence Layer — Pydantic schemas for all LLM-structured responses.

Research basis:
  instructor (Peng, 2024 — python.useinstructor.com, 12.2k GitHub stars, 3M
  monthly downloads): Wraps any LLM client to enforce Pydantic schemas on
  responses via function-calling or JSON mode, with automatic retry on
  validation failure.  Benchmark shows 98%+ parse success vs ~70% for fragile
  regex on production LLM output variance.

  Pydantic v2 (2023): Field-level validators provide self-documenting,
  testable constraints on LLM outputs.  Combined with instructor's retry
  logic, malformed responses are corrected automatically rather than silently
  producing wrong data.

Design
------
All three intelligence parsing sites use this module:

  1. pattern_suggester._suggest_with_llm          → PatternSuggestionResponse
  2. template_integrator_agent._parse_result       → IntegrationResponse
  3. context_generator._parse_llm_json             → ContextSpec

Each schema is used in two ways:
  a) With instructor (when litellm + instructor are available): the LLM is
     asked to produce structured output via JSON mode; instructor auto-retries
     on validation failure.
  b) Fallback (always available): parse the raw text with _parse_json_fallback,
     construct the Pydantic model manually, validate, and re-raise on failure.

The fallback path ensures the system degrades gracefully if instructor is not
installed, matching the existing behaviour exactly but with type safety added.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Instructor availability flag
# ---------------------------------------------------------------------------

try:
    import instructor as _instructor
    _INSTRUCTOR_AVAILABLE = True
except ImportError:
    _instructor = None  # type: ignore[assignment]
    _INSTRUCTOR_AVAILABLE = False
    logger.debug(
        "instructor not installed — intelligence parsing will use Pydantic-only "
        "fallback (no auto-retry on malformed LLM responses). "
        "Install with: pip install instructor"
    )


# ---------------------------------------------------------------------------
# Schema 1: Pattern suggestion response
# ---------------------------------------------------------------------------

class PatternSelection(BaseModel):
    """A single pattern selected by the LLM with its justification."""
    name: str = Field(description="Exact snake_case pattern name from the catalog")
    reason: str = Field(description="1-2 sentences explaining why this pattern is needed")

    @field_validator("name", mode="before")
    @classmethod
    def normalise_name(cls, v: str) -> str:
        return str(v).strip().lower().replace("-", "_").replace(" ", "_")


class PatternSuggestionResponse(BaseModel):
    """Structured output for _suggest_with_llm."""
    selections: list[PatternSelection] = Field(
        description="Ordered list of selected patterns (2-4, pipeline order)",
        min_length=1,
        max_length=5,
    )
    integration: str = Field(
        default="",
        description="2-3 sentences on how the selected patterns work together",
    )

    @field_validator("selections", mode="after")
    @classmethod
    def validate_pattern_names(cls, v: list[PatternSelection]) -> list[PatternSelection]:
        from .pattern_catalog import VALID_PATTERN_NAMES
        valid = [s for s in v if s.name in VALID_PATTERN_NAMES]
        if not valid and v:
            # All names unknown — still return them so caller can decide
            logger.warning(
                "PatternSuggestionResponse: none of the suggested pattern names "
                "matched the catalog: %s",
                [s.name for s in v],
            )
        return valid if valid else v


# ---------------------------------------------------------------------------
# Schema 2: Template integration response
# ---------------------------------------------------------------------------

class IntegrationResponse(BaseModel):
    """Structured output for TemplateIntegratorAgent._parse_result."""
    role: str = Field(default="", description="Unified role for the integrated context")
    rules: list[str] = Field(
        default_factory=list,
        description="Merged behavioral rules from all source templates",
    )
    directive: str = Field(
        default="",
        description="The unified analytical directive merging all template methodologies",
    )
    output_requirements: list[str] = Field(
        default_factory=list,
        description="Required elements in the final output",
    )
    integration_rationale: str = Field(
        default="",
        description="How the templates were synthesized and why the combination works",
    )


# ---------------------------------------------------------------------------
# Schema 3: Context generator spec
# ---------------------------------------------------------------------------

class ExamplePair(BaseModel):
    input: str
    output: str


class OutputField(BaseModel):
    name: str
    type: str = "str"


class ContextSpec(BaseModel):
    """Structured output for generate_context (context_generator.py)."""
    rules: list[str] = Field(
        default_factory=list,
        description="3-5 concrete behavioral rules",
        max_length=10,
    )
    style: str = Field(default="", description="Communication tone in ~10 words")
    expertise: list[str] = Field(
        default_factory=list,
        description="3-6 specific domain areas",
        max_length=10,
    )
    thinking_strategy: str = Field(
        default="step_by_step",
        description="Reasoning strategy",
    )
    examples: list[ExamplePair] = Field(
        default_factory=list,
        description="2-3 input→output demonstrations",
        max_length=5,
    )
    output_schema: list[OutputField] = Field(
        default_factory=list,
        description="3-5 structured output fields",
        max_length=10,
    )
    must_include: list[str] = Field(
        default_factory=list,
        description="Elements that must appear in every response",
        max_length=8,
    )
    must_not_include: list[str] = Field(
        default_factory=list,
        description="Things the LLM must never include",
        max_length=6,
    )

    @field_validator("thinking_strategy", mode="before")
    @classmethod
    def validate_strategy(cls, v: str) -> str:
        valid = {"step_by_step", "multiple_angles", "verify", "explain_simply", "creative"}
        s = str(v).strip().lower()
        return s if s in valid else "step_by_step"

    def to_dict(self) -> dict[str, Any]:
        """Convert back to the plain dict format used by _spec_to_context."""
        return {
            "rules": self.rules,
            "style": self.style,
            "expertise": self.expertise,
            "thinking_strategy": self.thinking_strategy,
            "examples": [{"input": e.input, "output": e.output} for e in self.examples],
            "output_schema": [{"name": f.name, "type": f.type} for f in self.output_schema],
            "must_include": self.must_include,
            "must_not_include": self.must_not_include,
        }


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def _extract_json_block(text: str) -> str:
    """Strip markdown fences and extract the outermost JSON object."""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence:
        text = fence.group(1).strip()
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        return text[start: end + 1]
    return text


def parse_with_fallback(schema_cls: type[BaseModel], raw: str) -> BaseModel:
    """Parse *raw* JSON text into *schema_cls*, raising ValueError on failure.

    Does NOT require instructor — always available.
    """
    cleaned = _extract_json_block(raw)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Could not parse LLM response as JSON for {schema_cls.__name__}. "
            f"First 300 chars: {raw[:300]!r}"
        ) from exc
    return schema_cls.model_validate(data)


def get_instructor_client(provider_instance: Any) -> Any | None:
    """Return an instructor-wrapped LiteLLM client, or None if unavailable.

    Args:
        provider_instance: A LiteLLMProvider instance (or any object with
                           a ``._provider`` attribute).  Used only as a hint
                           for logging; the actual client wraps litellm.completion.
    """
    if not _INSTRUCTOR_AVAILABLE:
        return None
    try:
        import litellm
        client = _instructor.from_litellm(litellm.completion)
        return client
    except Exception as exc:
        logger.debug("get_instructor_client: could not build instructor client: %s", exc)
        return None
