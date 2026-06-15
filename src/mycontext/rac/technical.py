"""Technical requirements generator (the *how*).

Where :func:`mycontext.rac.product` answers *what* the system must do (behavior +
eval contract), this answers *how* it is built: architecture, guardrails, tools,
cost, security, deployment, observability, and failure behavior — plus an opt-in
``frontier`` layer (fine-tune / RL / computer-use).

Two entry paths, same output shape:

- ``technical(product=<product_doc>)`` — the rich path. Every technical control
  carries a ``serves:`` list of the **product requirement IDs** it implements
  (tasks ``T*``, actions ``A*``, safety ``P*``, gates ``G*``), so
  :func:`mycontext.rac.trace` can prove coverage and catch drift.
- ``technical("<natural language>")`` — bootstrap from intent alone; ``serves``
  links are left as ``TODO(OQ-n)`` with a nudge to generate a product spec first.

Offline + deterministic, with the same non-blocking ``open_questions`` philosophy
as the product generator. Anti-goals unchanged: author + score, never enforce.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..version import __version__
from .architect import _QuestionLog, _slug
from .intake import parse_intent

_ARCH_PATTERN = {
    "agent": "tool_augmented_agent (plan -> act -> observe loop)",
    "multi_agent": "supervisor_orchestrator (planner + specialist workers)",
    "rag": "retrieve_then_generate (RAG over a trusted source)",
    "service": "stateless_request_handler",
}

_TECH_NOTE = (
    "Technical requirements authored by mycontext. Each control's `serves` field "
    "links to the product requirement it implements. Authoring + scoring only — "
    "build/enforcement belongs to your stack."
)


@dataclass
class _Signals:
    system_name: str = "agent"
    kind: str = "agent"
    has_product: bool = False
    primary_task_ids: list[str] = field(default_factory=list)
    oos_task_ids: list[str] = field(default_factory=list)
    approve_actions: list[tuple[str, str]] = field(default_factory=list)  # (id, tool)
    forbidden: list[tuple[str, list[str]]] = field(default_factory=list)  # (id, tools)
    money_action_ids: list[str] = field(default_factory=list)
    tool_actions: list[tuple[str, str, bool]] = field(default_factory=list)  # (id, tool, write?)
    safety_ids: list[str] = field(default_factory=list)
    injection_safety_ids: list[str] = field(default_factory=list)
    leak_safety_ids: list[str] = field(default_factory=list)
    gate_ids: list[str] = field(default_factory=list)
    rubric_ids: list[str] = field(default_factory=list)
    pii: bool = False
    hitl: bool = False


def _signals_from_product(doc: dict[str, Any]) -> _Signals:
    s = _Signals(has_product=True)
    meta = doc.get("meta", {}) or {}
    s.system_name = meta.get("system_name", "agent")
    s.kind = meta.get("kind", "agent")

    for tid, t in (doc.get("tasks", {}) or {}).items():
        if t.get("no_draft") or t.get("name") == "out_of_scope":
            s.oos_task_ids.append(tid)
        else:
            s.primary_task_ids.append(tid)

    for a in doc.get("actions", []) or []:
        aid = a.get("id", "A-?")
        policy = a.get("policy")
        tool = a.get("tool")
        tools = a.get("tools") or ([tool] if tool else [])
        if policy == "forbidden":
            s.forbidden.append((aid, [str(t) for t in tools]))
            continue
        write = policy in ("approve", "auto") and not any("read-only" in str(t).lower() for t in tools)
        for t in tools:
            s.tool_actions.append((aid, str(t), write))
        if policy == "approve":
            s.approve_actions.append((aid, str(tool or (tools[0] if tools else aid))))
        if "amount" in str(a).lower() or "refund" in str(a).lower() or "payment" in str(a).lower():
            s.money_action_ids.append(aid)

    for p in doc.get("safety", []) or []:
        pid = p.get("id", "P?")
        s.safety_ids.append(pid)
        blob = f"{p.get('incident', '')} {p.get('requirement', '')}".lower()
        if "inject" in blob or "instruction" in blob:
            s.injection_safety_ids.append(pid)
        if "leak" in blob or "data" in blob or "pii" in blob:
            s.leak_safety_ids.append(pid)
            s.pii = True

    s.rubric_ids = list((doc.get("rubrics", {}) or {}).keys())
    s.gate_ids = [g.get("id") for g in (doc.get("gates", {}) or {}).get("items", []) if g.get("id")]
    s.hitl = bool(s.approve_actions)
    return s


def _signals_from_text(text: str) -> _Signals:
    intake = parse_intent(text)
    s = _Signals(has_product=False)
    s.system_name = _slug(intake.name) if intake.name else "agent"
    s.kind = intake.kind
    s.pii = bool(intake.constraints.get("pii"))
    s.hitl = bool(intake.constraints.get("hitl"))
    if intake.constraints.get("money_actions"):
        s.money_action_ids = ["(money action)"]
    return s


@dataclass
class TechnicalArchitect:
    """Generate a technical-requirements spec from a product spec or intent."""

    provider: str = "openai"
    execute: bool = False
    frontier: bool = False
    model: str | None = None

    def draft(
        self,
        *,
        text: str | None = None,
        product: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if product is not None:
            s = _signals_from_product(product)
        elif text:
            s = _signals_from_text(text)
        else:
            raise ValueError("technical() needs either a product spec or natural-language text.")

        q = _QuestionLog()

        def serves(ids: list[str], hint: str) -> list[str]:
            ids = [i for i in ids if i]
            if ids:
                return ids
            if s.has_product:
                return []
            return [q.add(f"Link this control to product requirement IDs ({hint})", f"{hint}.serves")]

        doc: dict[str, Any] = {}
        doc["meta"] = {
            "system_name": s.system_name,
            "spec_type": "technical_requirements",
            "for_product": s.system_name,
            "kind": s.kind,
            "spec_version": "0.1.0",
            "status": "draft",
            "generated_by": f"mycontext-ai {__version__} technical-architect",
            "source": "product_requirements" if s.has_product else "natural_language",
            "note": _TECH_NOTE,
            "review_checklist": [
                "Pin concrete model IDs, infra, and thresholds (replace TODO markers)",
                "Confirm every `serves` reference resolves to a real product requirement",
                "Run `mycontext rac trace` to verify product/technical coverage",
            ],
        }
        doc["architecture"] = self._architecture(s, q, serves)
        doc["guardrails"] = self._guardrails(s, q, serves)
        doc["tools"] = self._tools(s, q, serves)
        doc["cost"] = self._cost(s, q, serves)
        doc["deployment"] = self._deployment(s, q, serves)
        doc["observability"] = self._observability(s, q, serves)
        doc["security"] = self._security(s, q, serves)
        doc["failure_behavior"] = self._failure(s, q, serves)
        if self.frontier:
            doc["frontier"] = self._frontier(s, q, serves)
        doc["assumptions"] = []
        doc["open_questions"] = q.items

        if self.execute:
            from .fill import complete
            from .patterns import TECHNICAL_KEY_PATTERNS, pattern_brief, provenance

            if product is not None:
                source = (product.get("meta", {}) or {}).get("intent") or s.system_name
            else:
                source = text or s.system_name
            notes, brief = pattern_brief(
                TECHNICAL_KEY_PATTERNS, source, provider=self.provider, model=self.model
            )
            if notes:
                doc["meta"]["informed_by"] = provenance(notes)
            doc = complete(doc, provider=self.provider, model=self.model, extra_context=brief)

        return doc

    def _architecture(self, s, q, serves):
        pattern = _ARCH_PATTERN.get(s.kind, _ARCH_PATTERN["agent"])
        return {
            "pattern": pattern,
            "orchestration": {
                "loop": "plan -> act -> observe",
                "max_steps": q.add("Max reasoning/tool steps per request?", "architecture.orchestration.max_steps", suggested_default=6),
            },
            "state": {
                "short_term": "per-request scratchpad (conversation memory)",
                "long_term": "vector store over the trusted source" if s.kind == "rag" else "none (stateless between requests)",
            },
            "model_routing_ref": "cost.routing",
            "serves": serves(s.primary_task_ids, "architecture"),
        }

    def _guardrails(self, s, q, serves):
        inp = [
            {"control": "Treat all user/tool content as data, never instructions (prompt-injection defense)",
             "serves": serves(s.injection_safety_ids, "guardrails.input")},
            {"control": "Schema + length validation on inbound payloads", "serves": serves(s.primary_task_ids, "guardrails.input")},
        ]
        proc = [
            {"control": "Tool-call allowlist; calls outside the registry are rejected",
             "serves": serves([fid for fid, _ in s.forbidden] + [aid for aid, _ in s.approve_actions], "guardrails.processing")},
            {"control": "Per-request step + token budget enforced", "serves": ["cost"]},
        ]
        out = [
            {"control": "Groundedness check — every claim traceable to source before send",
             "serves": serves(s.rubric_ids[:1], "guardrails.output")},
            {"control": "No claim that an approval-gated action completed before approval",
             "serves": serves([aid for aid, _ in s.approve_actions], "guardrails.output")},
        ]
        for pid in s.leak_safety_ids:
            out.append({"control": "PII / cross-customer data redaction on output", "serves": [pid]})
        if not s.leak_safety_ids and s.pii:
            out.append({"control": "PII redaction on output", "serves": serves([], "guardrails.output")})
        return {"input": inp, "processing": proc, "output": out}

    def _tools(self, s, q, serves):
        registry = []
        if s.has_product:
            for aid, tool, write in s.tool_actions:
                registry.append({
                    "name": tool,
                    "access": "write" if write else "read",
                    "requires_approval": any(aid == a for a, _ in s.approve_actions),
                    "scope": q.add(f"Least-privilege scope for tool '{tool}'?", f"tools.{_slug(tool)[:24]}.scope"),
                    "serves": [aid],
                })
        else:
            registry.append({
                "name": "TODO: enumerate tools",
                "serves": serves([], "tools"),
            })
        forbidden = [{"tools": tools, "policy": "forbidden", "serves": [fid]} for fid, tools in s.forbidden]
        return {
            "registry": registry,
            "forbidden": forbidden,
            "non_human_identity": {
                "principle": "least privilege per tool; short-lived credentials",
                "scopes": q.add("Define the NHI/service-account scopes per tool", "tools.non_human_identity.scopes"),
            },
        }

    def _cost(self, s, q, serves):
        return {
            "budget_per_task_usd": q.add("Max cost per request (USD)?", "cost.budget_per_task_usd", suggested_default=0.40),
            "routing": {
                "draft_model": q.add("Cheap/fast model for the common path?", "cost.routing.draft_model"),
                "escalation_model": q.add("Strong model for high-risk / low-confidence?", "cost.routing.escalation_model"),
                "rule": "use the strong model for high/critical-risk tasks and on low confidence; cheap model otherwise",
                "serves": serves(s.primary_task_ids, "cost.routing"),
            },
            "daily_budget_usd": q.add("Daily spend cap (USD)?", "cost.daily_budget_usd", suggested_default=200),
            "on_exhaustion": "degrade to draft-only / escalate to human; never silently drop work",
        }

    def _deployment(self, s, q, serves):
        return {
            "rollout": {
                "strategy": "shadow -> canary -> full",
                "stages": ["5% shadow", "25% canary", "100%"],
                "gated_by": serves(s.gate_ids, "deployment.rollout"),
            },
            "rollback": "auto-rollback if any hard gate regresses in canary",
            "canary_dimensions": ["task risk tier", "new tool usage", "cost per task"],
        }

    def _observability(self, s, q, serves):
        return {
            "metrics": [
                {"name": "rubric_pass_rate", "serves": serves(s.gate_ids, "observability.metrics")},
                {"name": "hitl_approval_and_rejection_rate", "serves": serves([a for a, _ in s.approve_actions], "observability.metrics")},
                {"name": "cost_per_task", "serves": ["cost"]},
                {"name": "unmapped_task_rate (charter drift)", "serves": serves(s.primary_task_ids, "observability.metrics")},
            ],
            "tracing": "span per plan/act/observe step, each tool call, and each approval decision",
            "audit_log": {
                "what": "all write + approval actions, immutable",
                "serves": serves([a for a, _ in s.approve_actions] + s.money_action_ids, "observability.audit_log"),
            },
        }

    def _security(self, s, q, serves):
        owasp = [
            {"risk": "Excessive Agency", "mitigation": "forbidden-tool list + approval gates on irreversible actions",
             "serves": serves([f for f, _ in s.forbidden] + [a for a, _ in s.approve_actions], "security.owasp")},
            {"risk": "Prompt Injection", "mitigation": "input-as-data guard; risky actions stay HITL regardless",
             "serves": serves(s.injection_safety_ids, "security.owasp")},
            {"risk": "Sensitive Information Disclosure", "mitigation": "output PII/cross-customer redaction",
             "serves": serves(s.leak_safety_ids, "security.owasp")},
        ]
        return {
            "owasp_agentic_top10": owasp,
            "secrets": "no secrets in prompts/logs; pull from a secrets manager at call time",
            "data_handling": "PII minimized + redacted in traces" if s.pii else "no PII expected; reconfirm on review",
        }

    def _failure(self, s, q, serves):
        return {
            "on_tool_error": {"strategy": "retry with backoff then escalate",
                              "max_retries": q.add("Max tool retries before escalating?", "failure_behavior.on_tool_error.max_retries", suggested_default=2)},
            "on_low_confidence": {"strategy": "route to human; never guess",
                                  "serves": serves(s.oos_task_ids + s.safety_ids, "failure_behavior.on_low_confidence")},
            "degraded_mode": "draft-only / read-only when a dependency is down; surface status, don't fail silently",
        }

    def _frontier(self, s, q, serves):
        return {
            "model_layer_advanced": {
                "fine_tune": q.add("Fine-tune candidate? (data volume, task)", "frontier.model_layer_advanced.fine_tune", suggested_default="not yet"),
                "distillation": "consider once a strong-model baseline is stable",
                "self_host": "evaluate only at volume where it beats API cost",
            },
            "agent_rl": {"enabled": False, "note": q.add("Is RL/online-learning in scope?", "frontier.agent_rl.note", suggested_default="out of scope for v1")},
            "frontier_capabilities": {"computer_use": False, "multimodal": q.add("Any image/PDF/voice inputs?", "frontier.frontier_capabilities.multimodal", suggested_default=False), "voice": False, "agent_to_agent": s.kind == "multi_agent"},
            "serves": serves(s.primary_task_ids, "frontier"),
        }


def technical(
    text: str | None = None,
    *,
    product: dict[str, Any] | None = None,
    frontier: bool = False,
    execute: bool = False,
    provider: str = "openai",
    model: str | None = None,
) -> dict[str, Any]:
    """Generate a **technical requirements** spec.

    Pass ``product=<product_doc>`` to derive controls that trace back to concrete
    product requirement IDs, or pass natural-language ``text`` to bootstrap.
    Set ``frontier=True`` to include the fine-tune / RL / computer-use layer.
    ``execute=True`` uses an LLM (your own key) to answer open questions and
    return a *filled* spec.
    """
    return TechnicalArchitect(
        provider=provider, execute=execute, frontier=frontier, model=model
    ).draft(text=text, product=product)
