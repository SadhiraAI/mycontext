"""Intake — turn a natural-language intent into a structured intent.

This is *Step 0* of the Requirements Architect: a free-text description (a
sentence or a paragraph) is parsed into the small set of fields the generator
needs (name, kind, what must never happen, volume, constraints). It mines the
implicit hard constraints (HITL, budget, PII) the way a good BA reads product
intent between the lines.

It is deliberately heuristic and fully offline — no LLM call. Whatever it cannot
infer is **not** guessed: it is recorded as an open question (see
``Intake.gaps``) so the architect can still emit a complete framework and let the
user answer later.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

# Capitalized tokens that are common English words, never an agent name.
_NAME_STOPWORDS = {
    "The", "We", "Win", "It", "I", "A", "An", "Our", "They", "This", "That",
    "Build", "Building", "Want", "Wants", "When", "While", "If", "For", "And",
    "Or", "But", "So", "Each", "Every", "All", "Success", "Goal", "Win",
    "Customer", "User", "Users", "AI", "LLM", "Agent",
}

_MONEY_WORDS = ("refund", "payment", "charge", "credit", "invoice", "transfer", "money", "purchase")
_DESTRUCTIVE_WORDS = ("delete", "drop", "erase", "wipe", "purge", "overwrite", "destroy")
_PII_WORDS = ("pii", "personal data", "customer data", "privacy", "gdpr", "sensitive data", "ccpa")
_HITL_WORDS = ("approval", "approve", "human review", "human-in-the-loop", "human in the loop", "sign off", "sign-off")
_RAG_WORDS = ("rag", "retrieval", "knowledge base", "knowledge-base", "policy wiki", "documentation", "documents")
_MULTI_WORDS = ("multi-agent", "multi agent", "subagent", "sub-agent", "orchestrat", "team of agents", "supervisor")


@dataclass
class Gap:
    """A piece of missing/ambiguous input, surfaced as a question for later."""

    question: str
    affects: str
    suggested_default: Any | None = None
    blocking: bool = False


@dataclass
class Intake:
    """Structured intent derived from natural language, plus the gaps found."""

    name: str | None
    kind: str
    intent: str
    must_never: list[str] = field(default_factory=list)
    volume: str | None = None
    constraints: dict[str, Any] = field(default_factory=dict)
    tier: int = 1
    gaps: list[Gap] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "kind": self.kind,
            "intent": self.intent,
            "must_never": self.must_never,
            "volume": self.volume,
            "constraints": self.constraints,
            "tier": self.tier,
        }


def _slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return s or "agent"


def _detect_name(text: str) -> str | None:
    # Quoted names win: "Aurora", 'PolicyPal'.
    m = re.search(r"""["']([A-Z][a-zA-Z0-9 \-]{1,30})["']""", text)
    if m:
        return m.group(1).strip()
    # "wants/build/introduce X" / "called X" / "named X".
    m = re.search(
        r"\b(?:wants?|build|building|introduce|introducing|call(?:ed)?|named)\s+(?:an?\s+)?([A-Z][a-zA-Z0-9]+)",
        text,
    )
    if m and m.group(1) not in _NAME_STOPWORDS:
        return m.group(1)
    # "Name:" — a capitalized token immediately followed by a colon.
    m = re.search(r"\b([A-Z][a-zA-Z0-9]+)\s*:", text)
    if m and m.group(1) not in _NAME_STOPWORDS:
        return m.group(1)
    # First capitalized non-stopword token.
    for tok in re.findall(r"\b[A-Z][a-zA-Z0-9]+\b", text):
        if tok not in _NAME_STOPWORDS and len(tok) > 2 and not tok.isupper():
            return tok
    return None


def _detect_kind(low: str) -> str:
    if any(w in low for w in _MULTI_WORDS):
        return "multi_agent"
    if any(w in low for w in _RAG_WORDS):
        return "rag"
    if "agent" in low:
        return "agent"
    return "service"


def _detect_must_never(text: str, low: str) -> list[str]:
    found: list[str] = []

    def _split(clause: str) -> list[str]:
        parts = re.split(r",|\bor\b|\band\b", clause)
        return [p.strip(" .;") for p in parts if p.strip(" .;")]

    for m in re.finditer(r"without\s+(.+?)(?:\.|$)", text, flags=re.IGNORECASE):
        found.extend(_split(m.group(1)))
    for m in re.finditer(r"(?:never|must not|must never|should never|no)\s+(.+?)(?:\.|,|$)", text, flags=re.IGNORECASE):
        cand = m.group(1).strip(" .;")
        if 2 < len(cand) < 80:
            found.append(cand)

    # Dedupe, keep order, lowercase first char.
    seen: set[str] = set()
    out: list[str] = []
    for item in found:
        norm = item[0].lower() + item[1:] if item else item
        key = norm.lower()
        if key and key not in seen:
            seen.add(key)
            out.append(norm)
    return out


def _detect_volume(text: str) -> str | None:
    m = re.search(
        r"(~?\s*[\d][\d,\.]*\s*(?:k|thousand|million|mn|m)?)\s*([a-zA-Z\-]+)?\s*(?:/|per|a|each)\s*(day|month|week|hour|minute)",
        text,
        flags=re.IGNORECASE,
    )
    if m:
        return re.sub(r"\s+", " ", m.group(0)).strip()
    return None


def parse_intent(text: str, *, tier: int = 1) -> Intake:
    """Parse free-text intent into a structured :class:`Intake` (offline)."""
    text = (text or "").strip()
    low = text.lower()
    gaps: list[Gap] = []

    name = _detect_name(text)
    if not name:
        gaps.append(Gap("What is the system/agent name?", "meta.system_name", blocking=False))

    kind = _detect_kind(low)
    must_never = _detect_must_never(text, low)
    if not must_never:
        gaps.append(
            Gap("What must this system NEVER do? (the hard safety lines)", "safety", blocking=True)
        )

    volume = _detect_volume(text)
    if not volume:
        gaps.append(Gap("What is the expected volume/cadence? (drives dataset sizing)", "datasets", blocking=False))

    constraints: dict[str, Any] = {}
    if any(w in low for w in _PII_WORDS):
        constraints["pii"] = True
    if any(w in low for w in _HITL_WORDS):
        constraints["hitl"] = True
    money = any(w in low for w in _MONEY_WORDS)
    if money:
        constraints["money_actions"] = True

    budget_m = re.search(r"\$\s?([\d]+(?:\.[\d]+)?)", text)
    if budget_m:
        constraints["budget_per_task_usd"] = float(budget_m.group(1))
    else:
        gaps.append(
            Gap(
                "What is the cost budget per task (USD)?",
                "budgets.per_task.max_cost_usd",
                suggested_default=0.40,
                blocking=False,
            )
        )

    return Intake(
        name=name,
        kind=kind,
        intent=text,
        must_never=must_never,
        volume=volume,
        constraints=constraints,
        tier=tier,
        gaps=gaps,
    )
