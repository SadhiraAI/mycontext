"""Trace — keep product and technical requirements in sync.

``trace(product, technical, diff=None)`` answers three questions, deterministically
and offline:

1. **Coverage** — does every risk-bearing product requirement (tasks, safety,
   approval/forbidden actions, gates) have at least one technical control whose
   ``serves`` field references it?
2. **Orphans** — does any technical ``serves`` reference an ID that doesn't exist
   in the product spec (drift / typo / stale link)?
3. **Diff impact** — if a code diff is supplied, which requirement IDs does the
   change touch, and does it *violate* anything (e.g. introduces a forbidden tool)?

This is scoring/alignment, not enforcement — it reports; your CI decides.
"""

from __future__ import annotations

import re
from typing import Any

from .diffparse import parse_diff

_STOP = {"the", "and", "for", "with", "without", "system", "must", "never", "data",
         "reply", "replies", "each", "that", "this", "into", "from", "defense", "depth"}


def _collect_serves(obj: Any, path: str = "") -> list[tuple[str, str]]:
    """Return (served_id, location) pairs found in any ``serves`` lists."""
    out: list[tuple[str, str]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            loc = f"{path}.{k}" if path else k
            if k == "serves" and isinstance(v, list):
                for sid in v:
                    if isinstance(sid, str):
                        out.append((sid, path or "technical"))
            else:
                out += _collect_serves(v, loc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += _collect_serves(v, f"{path}[{i}]")
    return out


def _product_ids(product: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Map every product requirement ID -> {kind, label, requires_coverage}."""
    ids: dict[str, dict[str, Any]] = {}
    for tid, t in (product.get("tasks", {}) or {}).items():
        ids[tid] = {"kind": "task", "label": t.get("name", tid), "requires_coverage": True}
    for rid in (product.get("rubrics", {}) or {}):
        ids[rid] = {"kind": "rubric", "label": rid, "requires_coverage": False}
    for a in product.get("actions", []) or []:
        aid = a.get("id")
        if not aid:
            continue
        policy = a.get("policy")
        ids[aid] = {"kind": "action", "label": a.get("tool") or a.get("tools") or aid,
                    "requires_coverage": policy in ("approve", "forbidden")}
    for p in product.get("safety", []) or []:
        pid = p.get("id")
        if pid:
            ids[pid] = {"kind": "safety", "label": p.get("requirement", pid), "requires_coverage": True}
    for g in (product.get("gates", {}) or {}).get("items", []) or []:
        gid = g.get("id")
        if gid:
            ids[gid] = {"kind": "gate", "label": g.get("scope", gid), "requires_coverage": True}
    return ids


def _keyword_index(product: dict[str, Any]) -> tuple[dict[str, str], set[str]]:
    """Map keyword -> product ID for diff matching, plus the set of forbidden tools."""
    index: dict[str, str] = {}
    forbidden_tools: set[str] = set()

    def add_tool(tool: str, aid: str) -> None:
        tool = str(tool).lower()
        for tok in re.findall(r"[a-z_][a-z0-9_]{3,}", tool):
            if tok not in _STOP:
                index.setdefault(tok, aid)

    for a in product.get("actions", []) or []:
        aid = a.get("id", "")
        tools = a.get("tools") or ([a.get("tool")] if a.get("tool") else [])
        for t in tools:
            add_tool(t, aid)
            if a.get("policy") == "forbidden":
                for tok in re.findall(r"[a-z_][a-z0-9_]{3,}", str(t).lower()):
                    forbidden_tools.add(tok)
    for p in product.get("safety", []) or []:
        pid = p.get("id", "")
        blob = f"{p.get('incident', '')} {p.get('requirement', '')}".lower()
        for tok in re.findall(r"[a-z][a-z]{4,}", blob):
            if tok not in _STOP:
                index.setdefault(tok, pid)
    return index, forbidden_tools


def trace(product: dict[str, Any], technical: dict[str, Any], diff: str | None = None) -> dict[str, Any]:
    """Compare a product spec to a technical spec (and an optional code diff)."""
    findings: list[str] = []
    pids = _product_ids(product)
    served_pairs = _collect_serves(technical)
    served_ids = {sid for sid, _ in served_pairs}

    # 1. Coverage.
    covered, uncovered = [], []
    for pid, info in pids.items():
        if not info["requires_coverage"]:
            continue
        if pid in served_ids:
            covered.append(pid)
        else:
            uncovered.append({"id": pid, "kind": info["kind"], "label": info["label"]})
            findings.append(f"[ERROR] Uncovered {info['kind']} {pid} ({info['label']}) — no technical control serves it.")

    # 2. Orphans (serves references that don't resolve, ignoring TODO markers).
    orphans = []
    for sid, loc in served_pairs:
        if sid.startswith("TODO(") or sid in ("cost",):
            continue
        if sid not in pids:
            orphans.append({"served_id": sid, "location": loc})
            findings.append(f"[WARN] Orphan reference {sid!r} in technical.{loc} — no such product requirement.")

    # 3. Diff impact.
    diff_impact: list[dict[str, Any]] = []
    if diff:
        index, forbidden_tools = _keyword_index(product)
        for fd in parse_diff(diff):
            touched: set[str] = set()
            violations: list[str] = []
            for line in fd.added:
                low = line.lower()
                for tok in re.findall(r"[a-z_][a-z0-9_]{3,}", low):
                    if tok in index:
                        touched.add(index[tok])
                    if tok in forbidden_tools:
                        violations.append(tok)
            for line in fd.removed:
                for tok in re.findall(r"[a-z_][a-z0-9_]{3,}", line.lower()):
                    if tok in index:
                        touched.add(index[tok])
            if touched or violations:
                diff_impact.append({"file": fd.path, "touches": sorted(touched), "forbidden_used": sorted(set(violations))})
            for tok in sorted(set(violations)):
                findings.append(f"[ERROR] {fd.path}: introduces forbidden tool/action '{tok}' (policy=forbidden in product spec).")
        if not diff_impact:
            findings.append("[WARN] Diff did not match any known requirement IDs — confirm the change is in scope.")

    has_error = any(f.startswith("[ERROR]") for f in findings)
    status = "drift_detected" if has_error else ("review" if findings else "in_sync")
    if status == "in_sync":
        findings.append("[OK] Product and technical requirements are in sync.")

    return {
        "status": status,
        "coverage": {"covered": sorted(covered), "uncovered": uncovered,
                     "ratio": round(len(covered) / max(1, len(covered) + len(uncovered)), 3)},
        "orphans": orphans,
        "diff_impact": diff_impact,
        "findings": findings,
    }


def format_report(report: dict[str, Any]) -> str:
    """Render a :func:`trace` report as readable markdown."""
    cov = report["coverage"]
    lines = [
        f"# Requirements trace — {report['status'].upper()}",
        "",
        f"Coverage: {len(cov['covered'])}/{len(cov['covered']) + len(cov['uncovered'])} "
        f"risk-bearing requirements served ({int(cov['ratio'] * 100)}%).",
        "",
        "## Findings",
        "",
    ]
    lines += [f"- {f}" for f in report["findings"]]
    if report["diff_impact"]:
        lines += ["", "## Diff impact", ""]
        for d in report["diff_impact"]:
            extra = f" — FORBIDDEN: {', '.join(d['forbidden_used'])}" if d.get("forbidden_used") else ""
            lines.append(f"- `{d['file']}` touches {', '.join(d['touches']) or '(none)'}{extra}")
    lines.append("")
    return "\n".join(lines)
