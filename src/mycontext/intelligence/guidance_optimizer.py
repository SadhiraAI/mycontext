"""
Guidance Optimizer — Automatically upgrade Guidance objects in SDK templates.

Targets the three most common weaknesses that degrade template quality:
  1. Suggestive modals  — "should/try to/ideally" → "must/always/never"
  2. Vague directives   — "be accurate" (< 5 words, no criterion) → specific and testable
  3. Under-specified    — rules that describe intent rather than behaviour

This is the SDK-template counterpart to PromptOptimizer (which handles raw strings).

Research basis:
  - Binding vs suggestive modals (InstructGPT / Ouyang et al. 2022):
    "must" and "always" increase instruction-following compliance vs "should" / "try to"
  - Measurability criterion: rules that contain a testable condition reduce ambiguity
    (Habernal & Gurevych 2016 — argument quality decomposition)
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from typing import Any

from ..core import Context
from ..foundation import Directive, Guidance

logger = logging.getLogger(__name__)

# ── Weakness detectors ───────────────────────────────────────────────────────

# Suggestive modals — language that makes rules optional
_SUGGESTIVE_MODALS = re.compile(
    r"\b(should|try to|ideally|consider|when possible|if applicable|"
    r"where relevant|you may|you might|it is recommended|generally|"
    r"typically|often|usually|aim to|seek to|attempt to)\b",
    re.IGNORECASE,
)

# Generic filler phrases that add no testable constraint
_VAGUE_PHRASES = re.compile(
    r"\b(be (helpful|accurate|thorough|clear|concise|professional|detailed|"
    r"comprehensive|objective|balanced|neutral|systematic|thoughtful|careful|"
    r"precise|rigorous|complete))\b",
    re.IGNORECASE,
)


# ── Result dataclasses ───────────────────────────────────────────────────────


@dataclass
class RuleAudit:
    """Audit record for a single rule."""

    original: str
    issues: list[str]  # "suggestive_modal", "vague_directive", "too_short"
    rewritten: str | None = None
    action: str = "unchanged"  # "rewritten", "unchanged", "kept"


@dataclass
class GuidanceAuditResult:
    """Full audit of a Guidance object before optimization."""

    role_is_generic: bool
    total_rules: int
    binding_rules: int
    weak_rules: list[RuleAudit]
    rule_strength_score: float  # 0.0–1.0

    def summary(self) -> str:
        weak = len(self.weak_rules)
        return (
            f"Rules: {self.total_rules} total  |  "
            f"{self.binding_rules} binding  |  "
            f"{weak} weak  |  "
            f"Strength: {self.rule_strength_score:.0%}"
        )


@dataclass
class OptimizedGuidance:
    """Result from GuidanceOptimizer.optimize()."""

    original_guidance: Guidance
    optimized_guidance: Guidance

    before_score: float  # rule_strength_score before
    after_score: float   # rule_strength_score after
    score_delta: float

    audit: GuidanceAuditResult
    rule_diffs: list[RuleAudit]

    metadata: dict[str, Any] = field(default_factory=dict)

    def audit_report(self) -> str:
        """Human-readable audit showing every weak rule and its fix."""
        lines = [
            "── GUIDANCE AUDIT ────────────────────────────────────────",
            f"Role:  {self.original_guidance.role}",
            self.audit.summary(),
        ]

        if not self.audit.weak_rules:
            lines.append("\nNo weak rules detected. Guidance is already well-specified.")
        else:
            lines.append("\nWEAK RULES DETECTED:")
            for i, ra in enumerate(self.audit.weak_rules, 1):
                lines.append(f"\n  [{i}] \"{ra.original}\"")
                for issue in ra.issues:
                    lines.append(f"      Issue: {_issue_label(issue)}")
                if ra.rewritten:
                    lines.append(f"      Fix:   \"{ra.rewritten}\"")

        lines.append(
            f"\nRule strength score: {self.before_score:.0%} → {self.after_score:.0%}"
        )
        lines.append("──────────────────────────────────────────────────────────")
        return "\n".join(lines)

    def summary(self) -> str:
        rewritten = sum(1 for r in self.rule_diffs if r.action == "rewritten")
        return (
            f"Rule strength: {self.before_score:.0%} → {self.after_score:.0%}  "
            f"(+{self.score_delta:.0%})  |  "
            f"{rewritten}/{self.audit.total_rules} rules rewritten"
        )


def _issue_label(code: str) -> str:
    return {
        "suggestive_modal": "suggestive modal — replace with must/always/never",
        "vague_directive": "vague directive — add a measurable criterion",
        "too_short": "too short to be a testable constraint (< 5 words)",
    }.get(code, code)


# ── Main class ───────────────────────────────────────────────────────────────


class GuidanceOptimizer:
    """
    Automatically upgrade ``Guidance`` objects to use binding, testable rules.

    Targets three weaknesses:

    1. **Suggestive modals** — "should", "try to", "ideally", "when possible"
       These make rules optional. Replace with "must", "always", "never".

    2. **Vague directives** — "be accurate", "be thorough", "be clear"
       Generic adjective rules have no testable criterion. Replace with
       a specific, verifiable constraint.

    3. **Under-specified rules** — any rule < 5 words without a direct object
       or measurable condition.

    Example::

        from mycontext.intelligence import GuidanceOptimizer
        from mycontext.foundation import Guidance

        guidance = Guidance(
            role="Data analyst",
            rules=[
                "Try to look for patterns",
                "You should mention limitations",
                "Be accurate",
            ],
        )

        opt = GuidanceOptimizer(provider="openai", model="gpt-4o-mini")
        result = opt.optimize(guidance)

        print(result.audit_report())
        print(result.optimized_guidance.rules)
        # [
        #   "Identify and quantify every pattern — report the metric and its value.",
        #   "Must explicitly state each data gap: what is absent and what it prevents.",
        #   "Every claim must cite the specific data point that supports it.",
        # ]
    """

    # Upgrade hints per weakness type — fed to the LLM as rewriting principles
    _REWRITE_HINTS = {
        "suggestive_modal": [
            "Replace the suggestive modal (should/try to/ideally) with must/always/never.",
            "Make the rule binding: the model must be able to violate it to make it testable.",
            "Preserve the intent; change only the commitment level.",
        ],
        "vague_directive": [
            "Replace the generic adjective (accurate/thorough/clear) with a specific, measurable criterion.",
            "A good rule answers: 'How would I know if this was violated?'",
            "Example upgrade: 'Be accurate' → 'Every claim must cite the specific metric that supports it.'",
        ],
        "too_short": [
            "Expand to a complete constraint with a subject, verb, and measurable condition.",
            "A rule of < 5 words cannot be tested — add the criterion.",
            "Example: 'Be helpful' → 'Every response must end with at least one concrete next step.'",
        ],
    }

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4o-mini",
    ):
        self.provider = provider
        self.model = model

    # ── Public API ─────────────────────────────────────────────────────────

    def audit(self, guidance: Guidance) -> GuidanceAuditResult:
        """
        Inspect a Guidance object and report weaknesses — no LLM call.

        Args:
            guidance: The Guidance object to audit.

        Returns:
            GuidanceAuditResult with per-rule weakness records.
        """
        return self._audit(guidance)

    def optimize(
        self,
        guidance: Guidance,
        provider: str | None = None,
        model: str | None = None,
        **execute_kwargs: Any,
    ) -> OptimizedGuidance:
        """
        Audit and rewrite weak rules using an LLM.

        Only rules identified as weak are sent to the LLM — binding rules
        are kept exactly as written.

        Args:
            guidance: The Guidance object to optimize.
            provider: Override default provider.
            model: Override default model.

        Returns:
            OptimizedGuidance with the improved Guidance and full audit trail.
        """
        provider = provider or self.provider
        model = model or self.model

        audit = self._audit(guidance)
        before_score = audit.rule_strength_score

        if not audit.weak_rules:
            # Nothing to do — return as-is with a perfect score
            return OptimizedGuidance(
                original_guidance=guidance,
                optimized_guidance=guidance,
                before_score=before_score,
                after_score=before_score,
                score_delta=0.0,
                audit=audit,
                rule_diffs=[
                    RuleAudit(original=r, issues=[], action="kept")
                    for r in (guidance.rules or [])
                ],
                metadata={"mode": "no_change", "reason": "no weak rules detected"},
            )

        # LLM rewrite for weak rules only
        rewrites = self._llm_rewrite_rules(
            audit.weak_rules, guidance, provider, model, **execute_kwargs
        )

        # Apply rewrites: keep binding rules, replace weak ones
        original_rules = guidance.rules or []
        weak_originals = {ra.original for ra in audit.weak_rules}

        new_rules: list[str] = []
        rule_diffs: list[RuleAudit] = []

        for rule in original_rules:
            if rule in weak_originals and rule in rewrites:
                rewritten = rewrites[rule]
                new_rules.append(rewritten)
                # Find original audit record
                orig_audit = next(ra for ra in audit.weak_rules if ra.original == rule)
                rule_diffs.append(
                    RuleAudit(
                        original=rule,
                        issues=orig_audit.issues,
                        rewritten=rewritten,
                        action="rewritten",
                    )
                )
            else:
                new_rules.append(rule)
                rule_diffs.append(RuleAudit(original=rule, issues=[], action="kept"))

        optimized = Guidance(
            role=guidance.role,
            goal=guidance.goal,
            rules=new_rules,
            style=guidance.style,
            expertise=guidance.expertise,
            persona_scope=guidance.persona_scope,
        )

        after_score = self._compute_strength_score(new_rules)

        return OptimizedGuidance(
            original_guidance=guidance,
            optimized_guidance=optimized,
            before_score=before_score,
            after_score=after_score,
            score_delta=after_score - before_score,
            audit=audit,
            rule_diffs=rule_diffs,
            metadata={"mode": "optimized", "model": model, "provider": provider},
        )

    # ── Heuristic audit ───────────────────────────────────────────────────

    def _audit(self, guidance: Guidance) -> GuidanceAuditResult:
        rules = guidance.rules or []
        weak: list[RuleAudit] = []
        binding_count = 0

        for rule in rules:
            issues = self._detect_issues(rule)
            if issues:
                weak.append(RuleAudit(original=rule, issues=issues, action="pending"))
            else:
                binding_count += 1

        generic_roles = {
            "assistant", "expert assistant", "helpful assistant",
            "ai assistant", "analyst", "expert",
        }
        role_is_generic = guidance.role.lower().strip() in generic_roles

        strength = self._compute_strength_score(rules)

        return GuidanceAuditResult(
            role_is_generic=role_is_generic,
            total_rules=len(rules),
            binding_rules=binding_count,
            weak_rules=weak,
            rule_strength_score=strength,
        )

    def _detect_issues(self, rule: str) -> list[str]:
        """Return a list of issue codes for a single rule string."""
        issues = []
        lower = rule.lower().strip()

        if _SUGGESTIVE_MODALS.search(lower):
            issues.append("suggestive_modal")

        if _VAGUE_PHRASES.search(lower):
            issues.append("vague_directive")

        word_count = len(rule.split())
        if word_count < 5 and not issues:
            issues.append("too_short")

        return issues

    @staticmethod
    def _compute_strength_score(rules: list[str]) -> float:
        """Score 0.0–1.0: fraction of rules that are binding and specific."""
        if not rules:
            return 0.0
        binding = re.compile(
            r"\b(must|always|never|will |shall |required to|do not|don't)\b",
            re.IGNORECASE,
        )
        specific = re.compile(
            r"\b(cite|quantify|identify|state|include|list|provide|calculate|"
            r"reference|trace|report|specify|name|define|document)\b",
            re.IGNORECASE,
        )
        score = 0.0
        for rule in rules:
            has_binding = bool(binding.search(rule))
            has_specific = bool(specific.search(rule))
            word_count = len(rule.split())
            if has_binding and has_specific and word_count >= 8:
                score += 1.0
            elif has_binding or (has_specific and word_count >= 8):
                score += 0.6
            elif word_count >= 8:
                score += 0.3
            else:
                score += 0.0
        return min(1.0, score / len(rules))

    # ── LLM rewrite ───────────────────────────────────────────────────────

    def _llm_rewrite_rules(
        self,
        weak_rules: list[RuleAudit],
        guidance: Guidance,
        provider: str,
        model: str,
        **kwargs: Any,
    ) -> dict[str, str]:
        """
        Ask the LLM to rewrite only the weak rules.
        Returns a dict mapping original rule → rewritten rule.
        """
        # Build per-rule context block
        rules_block = ""
        for i, ra in enumerate(weak_rules, 1):
            hints = []
            for issue in ra.issues:
                hints.extend(self._REWRITE_HINTS.get(issue, []))
            hint_text = "\n".join(f"  - {h}" for h in hints)
            rules_block += (
                f'\nRule {i}: "{ra.original}"\n'
                f"Issues: {', '.join(ra.issues)}\n"
                f"Rewriting principles:\n{hint_text}\n"
            )

        system = (
            "You are an expert prompt engineer specializing in binding instruction design. "
            "You rewrite weak rules into specific, testable, binding constraints. "
            "You output ONLY valid JSON. No commentary."
        )

        user = f"""CONTEXT (the template role):
\"{guidance.role}\"

WEAK RULES TO REWRITE:
{rules_block}

For each rule, produce a rewritten version that:
- Uses binding language (must/always/never/will)
- Contains a specific, testable criterion
- Preserves the original intent
- Is 10–25 words long

Return ONLY this JSON — keys are the original rules, values are the rewritten versions:
{{
{chr(10).join(f'  "{ra.original}": "<rewritten rule>"' for ra in weak_rules)}
}}"""

        ctx = Context(
            guidance=Guidance(
                role=system,
                rules=["Output ONLY valid JSON. No prose. No markdown fences."],
            ),
            directive=Directive(content=user),
        )

        try:
            result = ctx.execute(
                provider=provider,
                model=model,
                temperature=kwargs.pop("temperature", 0.2),
                **kwargs,
            )
            raw = result.response.strip()
            if raw.startswith("```"):
                raw = re.sub(r"^```[a-z]*\n?", "", raw)
                raw = re.sub(r"\n?```$", "", raw).strip()
            return json.loads(raw)
        except Exception as exc:
            logger.warning(
                "GuidanceOptimizer LLM rewrite failed: %s — returning originals", exc,
                exc_info=True,
            )
            return {}
