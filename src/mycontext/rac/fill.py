"""LLM completion pass — turn a draft spec into a *complete* one.

The product/technical generators always emit a complete framework offline, with
gaps marked as ``open_questions`` + inline ``TODO(OQ-n)`` markers. This module
asks an LLM (via LiteLLM, your own key) to **answer those open questions** with
concrete, production-grade values, then substitutes the answers back into the
spec — so ``execute=True`` yields a filled requirements doc instead of a skeleton.

We deliberately only fill the *gaps* (a clean, parseable id → value mapping). The
deterministic structure, typed IDs, and traceability stay intact; the LLM never
rewrites the skeleton, it only resolves the questions the skeleton raised.
"""

from __future__ import annotations

import json
import re
from typing import Any

from .author import to_yaml

_MARKER_RE = re.compile(r"TODO\((OQ-\d+)\)")

_SYSTEM = """You are a senior staff engineer and AI evaluation lead. You are \
completing a machine-generated {spec_type} for the system described below. \
Answer EVERY open question with a concrete, realistic, production-grade value \
that is consistent with the system intent and the rest of the spec.

Rules:
- Return ONLY a JSON object mapping each question id (e.g. "OQ-01") to its answer.
- The answer must be directly usable as the value of the field named in "affects":
  numbers as JSON numbers, lists as JSON arrays, booleans as booleans, short
  strings otherwise. Do not wrap values in extra prose.
- Prefer the suggested_default when it is reasonable; otherwise choose a sensible,
  defensible value. Never answer with "TODO", "N/A", or a question.
"""


def _collect_questions(doc: dict[str, Any]) -> list[dict[str, Any]]:
    return [q for q in doc.get("open_questions", []) or [] if q.get("id")]


def _ask_llm(
    doc: dict[str, Any],
    questions: list[dict[str, Any]],
    provider: str,
    model: str | None,
    extra_context: str | None = None,
) -> dict[str, Any]:
    from ..core import Context
    from .models import resolve_model

    meta = doc.get("meta", {}) or {}
    spec_type = meta.get("spec_type", "requirements")
    intent = meta.get("intent") or meta.get("system_name", "the system")

    payload: dict[str, Any] = {
        "system_intent": intent,
        "spec_excerpt": to_yaml(
            {k: v for k, v in doc.items() if k != "open_questions"}
        )[:6000],
        "open_questions": [
            {k: q.get(k) for k in ("id", "question", "affects", "suggested_default") if k in q}
            for q in questions
        ],
    }
    # Expert analyses from cognitive patterns (when execute=True) ground the
    # answers in real reasoning rather than the fill model's unaided guess.
    if extra_context:
        payload["expert_analysis"] = extra_context[:8000]

    ctx = Context(guidance=_SYSTEM.format(spec_type=spec_type))
    result = ctx.execute(
        provider=provider,
        model=resolve_model(provider, model),
        user="Answer the open_questions for this spec. Ground each answer in the "
        "expert_analysis when relevant. Respond with JSON only.\n\n"
        + json.dumps(payload, ensure_ascii=False),
        temperature=0,
        use_cache=False,
        response_format={"type": "json_object"},
    )
    text = result if isinstance(result, str) else getattr(result, "response", str(result))
    return _parse_answers(text)


def _parse_answers(text: str) -> dict[str, Any]:
    text = (text or "").strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not m:
            return {}
        try:
            data = json.loads(m.group(0))
        except json.JSONDecodeError:
            return {}
    # Allow an optional {"answers": {...}} envelope.
    if isinstance(data, dict) and "answers" in data and isinstance(data["answers"], dict):
        data = data["answers"]
    return {str(k).strip(): v for k, v in data.items()} if isinstance(data, dict) else {}


def _apply_answers(obj: Any, answers: dict[str, Any]) -> Any:
    if isinstance(obj, dict):
        return {k: _apply_answers(v, answers) for k, v in obj.items()}
    if isinstance(obj, list):
        out: list[Any] = []
        for item in obj:
            # A list element that is exactly a marker may expand into a list answer.
            if isinstance(item, str):
                exact = _MARKER_RE.fullmatch(item.strip())
                if exact and exact.group(1) in answers:
                    ans = answers[exact.group(1)]
                    if isinstance(ans, list):
                        out.extend(ans)
                        continue
                    out.append(ans)
                    continue
            out.append(_apply_answers(item, answers))
        return out
    if isinstance(obj, str):
        exact = _MARKER_RE.fullmatch(obj.strip())
        if exact and exact.group(1) in answers:
            return answers[exact.group(1)]
        # Inline marker(s) inside a larger string -> stringify the answer.
        def _sub(match: re.Match) -> str:
            qid = match.group(1)
            return str(answers[qid]) if qid in answers else match.group(0)

        return _MARKER_RE.sub(_sub, obj)
    return obj


def complete(
    doc: dict[str, Any],
    *,
    provider: str = "openai",
    model: str | None = None,
    extra_context: str | None = None,
) -> dict[str, Any]:
    """Fill a draft spec's open questions with LLM answers and substitute them in.

    Returns a *new* doc (the input is not mutated). Questions that the LLM
    answers are marked ``status: answered`` with the chosen value recorded; any
    left unanswered keep their ``TODO(OQ-n)`` marker. ``meta.status`` becomes
    ``filled`` when no markers remain. ``extra_context`` (a cognitive-pattern
    brief) is passed to the model as expert grounding for the answers.
    """
    questions = _collect_questions(doc)
    if not questions:
        return doc

    answers = _ask_llm(doc, questions, provider, model, extra_context)
    filled = _apply_answers(doc, answers)

    remaining = set(_MARKER_RE.findall(to_yaml(filled)))
    new_oqs = []
    for q in filled.get("open_questions", []) or []:
        qid = q.get("id")
        if qid in answers:
            q = {**q, "status": "answered", "answer": answers[qid]}
        new_oqs.append(q)
    filled["open_questions"] = new_oqs

    from .models import resolve_model

    meta = dict(filled.get("meta", {}) or {})
    meta["filled_by"] = f"{provider}:{resolve_model(provider, model)}"
    if not remaining:
        meta["status"] = "filled"
        meta["note"] = (meta.get("note", "") + " | LLM-completed: review the filled values before ratifying.").strip(" |")
    filled["meta"] = meta
    return filled
