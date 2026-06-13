"""
Map natural-language tasks to LiteLLM/OpenAI-compatible generation kwargs.

Caller-side policy (not model-learned adaptive decoding). Uses optional
:class:`~mycontext.foundation.task_contract.TaskContract` plus lightweight
heuristics on the question text. For OpenAI-style reasoning SKUs that reject
non-default sampling, omits ``temperature`` / ``top_p`` and optionally sets
``reasoning_effort`` instead.
"""

from __future__ import annotations

import re
from typing import Any, Literal

from ..foundation.task_contract import TaskContract

GenerationRouteMode = Literal["internal", "downstream"]

# Intents drive preset tables (not exposed as public enum to keep API small).
_Intent = Literal[
    "structured",
    "factual",
    "balanced",
    "creative",
    "judge",
    "explore",
]

_STRUCTURED_HINT = re.compile(
    r"\b(json|schema|yaml|xml|sql|regex|typescript|protobuf|openapi|"
    r"strictly valid|parseable|machine[- ]readable)\b",
    re.I,
)
_CREATIVE_HINT = re.compile(
    r"\b(brainstorm|ideat|marketing hook|tagline|story|poem|joke|"
    r"divergent|novel|wild ideas|creative writing)\b",
    re.I,
)
_JUDGE_HINT = re.compile(
    r"\b(score|rubric|grade|evaluate|llm[- ]as[- ]a[- ]judge|"
    r"which answer is better|pick the best)\b",
    re.I,
)
_EXPLORE_HINT = re.compile(
    r"\b(several options|multiple drafts|three versions|variants|"
    r"best of|self[- ]consisten|vote between)\b",
    re.I,
)


def model_allows_sampling(model: str) -> bool:
    """Return False when the model family typically rejects custom temperature/top_p.

    Conservative heuristics on model id strings only (no network).
    Chat-flavored GPT-5 ids keep sampling knobs per current OpenAI product lines.
    """
    ml = model.lower().replace(" ", "")
    if ml.startswith(("o1", "o2", "o3", "o4")):
        return False
    if "gpt-5" in ml or "gpt5" in ml.replace("-", ""):
        return "chat" in ml
    return True


def classify_generation_intent(
    question: str,
    task_contract: TaskContract | None = None,
) -> str:
    """Cheap lexical + TaskContract classification (no LLM)."""
    q = (question or "").strip()
    low = q.lower()

    genre = (task_contract.genre or "").lower() if task_contract and task_contract.genre else ""
    metaphor = (
        (task_contract.metaphor or "").lower()
        if task_contract and getattr(task_contract, "metaphor", None)
        else ""
    )

    if _STRUCTURED_HINT.search(q) or "json" in genre or "api" in genre:
        return "structured"
    if _JUDGE_HINT.search(q):
        return "judge"
    if _EXPLORE_HINT.search(q):
        return "explore"
    if _CREATIVE_HINT.search(q) or "brainstorm" in genre or "blog" in genre:
        return "creative"
    if metaphor and "analog" in metaphor:
        return "creative"
    if any(
        tok in low
        for tok in (
            "summarize",
            "summary",
            "rewrite",
            "neutral tone",
            "explain like",
            "tutorial",
        )
    ):
        return "balanced"
    if any(
        tok in low
        for tok in (
            "why did",
            "root cause",
            "prove",
            "theorem",
            "compliance",
            "policy",
            "contract",
            "legal",
        )
    ):
        return "factual"
    return "balanced"


def _reasoning_effort_for_intent(intent: str) -> str:
    if intent in ("structured", "judge"):
        return "low"
    if intent in ("factual", "balanced"):
        return "medium"
    return "high"


def _sampling_preset(intent: str, mode: GenerationRouteMode) -> dict[str, Any]:
    """Return kwargs fragment for chat-style models."""
    if mode == "internal":
        # JSON / section rewrite — stay cold regardless of user creative ask.
        return {"temperature": 0.25, "top_p": 0.9, "n": 1}

    # downstream — honor task diversity
    if intent == "structured":
        return {"temperature": 0.15, "top_p": 0.85, "n": 1}
    if intent == "factual":
        return {"temperature": 0.2, "top_p": 0.9, "n": 1}
    if intent == "judge":
        return {"temperature": 0.1, "top_p": 0.85, "n": 1}
    if intent == "balanced":
        return {"temperature": 0.55, "top_p": 0.92, "n": 1}
    if intent == "creative":
        return {"temperature": 0.9, "top_p": 0.95, "n": 1}
    if intent == "explore":
        return {"temperature": 0.75, "top_p": 0.93, "n": 3}
    return {"temperature": 0.55, "top_p": 0.92, "n": 1}


def resolve_generation_kwargs(
    *,
    question: str,
    provider: str,
    model: str,
    task_contract: TaskContract | None = None,
    mode: GenerationRouteMode,
) -> tuple[dict[str, Any], str]:
    """Return (litellm_extra_kwargs, short_rationale)."""
    intent = classify_generation_intent(question, task_contract)
    prov = (provider or "").lower().strip()

    if not model_allows_sampling(model):
        effort = _reasoning_effort_for_intent(intent)
        if mode == "internal":
            rationale = (
                f"Reasoning-style model id — omit sampling; "
                f"reasoning_effort={effort} for JSON rewriter ({intent})."
            )
            return {"reasoning_effort": effort}, rationale
        rationale = (
            f"Reasoning-style model id — omit sampling; "
            f"reasoning_effort={effort} for downstream ({intent})."
        )
        extra: dict[str, Any] = {"reasoning_effort": effort}
        if intent == "explore":
            extra["n"] = 3
        return extra, rationale

    preset = _sampling_preset(intent, mode)
    rationale = f"Chat-style model — preset for {intent} ({mode})."
    if prov in ("gemini", "google", "vertex", "genai") and preset.get("n", 1) != 1:
        preset = {**preset, "n": 1}
        rationale += " n reset to 1 for Gemini routing."
    return preset, rationale
