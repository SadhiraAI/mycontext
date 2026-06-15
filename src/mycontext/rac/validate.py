"""Deterministic best-practice checks for a Requirements Architect spec.

These are *structural* lint rules — no LLM, no enforcement. They encode the
non-negotiables from the eval-first methodology so a half-baked spec is caught
before it is handed to a coding agent:

- every task references a rubric that exists;
- there is at least one mandatory refusal / out-of-scope row;
- irreversible / money / PII actions are never ``auto``;
- every safety entry is a hard gate with a machine-checkable assert;
- safety datasets have no dev split;
- unresolved ``TODO(OQ-n)`` markers are reported (blocking ones as errors).
"""

from __future__ import annotations

import re
from typing import Any

_TODO_RE = re.compile(r"TODO\((OQ-\d+)\)")


def _walk_todos(obj: Any) -> list[str]:
    found: list[str] = []
    if isinstance(obj, str):
        found += _TODO_RE.findall(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            found += _walk_todos(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            found += _walk_todos(v)
    return found


def validate(doc: dict[str, Any]) -> list[str]:
    """Return a list of issues (``[ERROR] ...`` / ``[WARN] ...``). Empty == clean.

    Dispatches on ``meta.spec_type`` so both product and technical specs can be
    checked with the same entry point.
    """
    spec_type = (doc.get("meta", {}) or {}).get("spec_type")
    if spec_type == "technical_requirements":
        return _validate_technical(doc)
    return _validate_product(doc)


def _validate_product(doc: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    def err(msg: str) -> None:
        issues.append(f"[ERROR] {msg}")

    def warn(msg: str) -> None:
        issues.append(f"[WARN] {msg}")

    tasks = doc.get("tasks", {}) or {}
    rubrics = doc.get("rubrics", {}) or {}
    actions = doc.get("actions", []) or []
    safety = doc.get("safety", []) or []
    datasets = doc.get("datasets", {}) or {}
    gates = doc.get("gates", {}) or {}

    if not tasks:
        err("No tasks defined — the spec needs a task taxonomy.")

    # Every task must reference an existing rubric.
    for tid, t in tasks.items():
        rid = t.get("rubric")
        if not rid:
            err(f"Task {tid} has no rubric reference.")
        elif rid not in rubrics:
            err(f"Task {tid} references rubric {rid!r} which is not defined.")

    # At least one mandatory refusal / out-of-scope row.
    if not any(t.get("no_draft") or t.get("name") == "out_of_scope" for t in tasks.values()):
        warn("No out-of-scope / refusal task — add a mandatory 'no_draft' row.")

    # Irreversible / money / PII actions must never be auto.
    for a in actions:
        policy = a.get("policy")
        reversible = a.get("reversible", True)
        money = "amount" in str(a).lower() or "refund" in str(a).lower() or "payment" in str(a).lower()
        if policy == "auto" and (reversible is False or money):
            err(f"Action {a.get('id', '?')} is irreversible/money but policy=auto (must be approve or forbidden).")

    # Safety: hard gate + machine-checkable assert; never auto.
    if not safety:
        warn("No safety / pre-mortem entries — list what must never happen.")
    for p in safety:
        ev = p.get("eval", {}) or {}
        if not ev.get("hard_gate"):
            err(f"Safety {p.get('id', '?')} is not a hard_gate (safety reqs are absolute).")
        if not ev.get("assert"):
            warn(f"Safety {p.get('id', '?')} has no machine-checkable assert yet.")

    # Safety datasets must have no dev split.
    for sl in datasets.get("slices", []) or []:
        if str(sl.get("task", "")).lower().startswith("safety") and sl.get("dev", 0):
            err(f"Safety dataset slice {sl.get('task')} has a dev split (forbidden — contamination risk).")

    # Gates must include an absolute safety gate.
    gate_items = gates.get("items", []) or []
    if not any(g.get("scope") == "safety" and g.get("hard_gate") for g in gate_items):
        warn("No absolute safety release gate found.")

    # Open questions / TODO markers.
    todos = set(_walk_todos(doc))
    oqs = {q.get("id"): q for q in doc.get("open_questions", []) or []}
    blocking = [qid for qid in todos if oqs.get(qid, {}).get("blocking")]
    if blocking:
        err(f"{len(blocking)} blocking open question(s) unresolved: {', '.join(sorted(blocking))}.")
    nonblocking = sorted(todos - set(blocking))
    if nonblocking:
        warn(f"{len(nonblocking)} non-blocking open question(s) to review: {', '.join(nonblocking)}.")

    # Status should not be 'ready' while questions remain.
    status = (doc.get("meta", {}) or {}).get("status")
    if status == "ready" and todos:
        err("meta.status is 'ready' but unresolved TODO(OQ-n) markers remain.")

    return issues


_REQUIRED_TECH_SECTIONS = ("architecture", "guardrails", "tools", "cost", "security")


def _validate_technical(doc: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    def err(msg: str) -> None:
        issues.append(f"[ERROR] {msg}")

    def warn(msg: str) -> None:
        issues.append(f"[WARN] {msg}")

    for section in _REQUIRED_TECH_SECTIONS:
        if not doc.get(section):
            err(f"Technical spec missing required section: {section}.")

    # Every guardrail layer should have at least one control.
    guardrails = doc.get("guardrails", {}) or {}
    for layer in ("input", "processing", "output"):
        if not guardrails.get(layer):
            warn(f"guardrails.{layer} has no controls.")

    # Forbidden tools must be declared somewhere in security/tools.
    tools = doc.get("tools", {}) or {}
    if not tools.get("forbidden"):
        warn("No forbidden tools declared — confirm there are genuinely no off-limits actions.")

    # Open-question / TODO bookkeeping (shared convention).
    todos = set(_walk_todos(doc))
    oqs = {q.get("id"): q for q in doc.get("open_questions", []) or []}
    blocking = [qid for qid in todos if oqs.get(qid, {}).get("blocking")]
    if blocking:
        err(f"{len(blocking)} blocking open question(s) unresolved: {', '.join(sorted(blocking))}.")
    nonblocking = sorted(todos - set(blocking))
    if nonblocking:
        warn(f"{len(nonblocking)} non-blocking open question(s) to review: {', '.join(nonblocking)}.")

    return issues
