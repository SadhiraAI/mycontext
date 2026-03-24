"""
Prompt Architect — Apply the 9-Section Architecture to any raw prompt.

Translates the prompt-engineering guidebook into a callable SDK tool:
  1. PARSE   — detect which of the 9 sections already exist in a raw string.
  2. SCORE   — run QualityMetrics on the current prompt.
  3. BUILD   — construct a full 9-section Context from a task description alone.
  4. IMPROVE — parse + score + rewrite weak sections + score again + diff.

Research basis for the 9-section ordering (same as core.py research_flow):
  PRIMACY ZONE    → ① Role  ② Goal          (Liu et al. 2023)
  INSTRUCTIONS    → ③ Rules  ④ Style         (OpenAI guide)
  MIDDLE          → ⑤ Reasoning strategies (task-fit; one or many)  ⑥ Examples  (Li et al. 2025)
  LATE            → ⑦ Output Contract  ⑧ Guard Rails  (CO-STAR)
  RECENCY ZONE    → ⑨ Task (ALWAYS LAST)     (Li et al. 2023)
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from typing import Any

from ..core import Context, ProviderHint
from ..foundation import Constraints, Directive, Guidance

logger = logging.getLogger(__name__)

# ── Section identifiers ──────────────────────────────────────────────────────

SECTION_NAMES = [
    "role",
    "goal",
    "rules",
    "style",
    "reasoning",
    "examples",
    "output_contract",
    "guard_rails",
    "task",
]

# Slugs the LLM should prefer in ``reasoning_strategies`` (may combine several).
# Atomic strategies (composable building blocks):
REASONING_STRATEGY_CHOICES = (
    "step_by_step",
    "multiple_angles",
    "verify",
    "explain_simply",
    "creative",
)

# Named archetypes: pre-validated strategy compositions for common task types.
# Use these in reasoning_strategies when the task matches the archetype.
REASONING_ARCHETYPES: dict[str, tuple[str, ...]] = {
    "analytical": ("step_by_step", "verify"),
    "deliberative": ("multiple_angles", "step_by_step", "verify"),
    "explanatory": ("explain_simply", "step_by_step"),
    "creative": ("creative", "multiple_angles"),
    "high_stakes": ("step_by_step", "multiple_angles", "verify"),
}

ALL_STRATEGY_SLUGS = REASONING_STRATEGY_CHOICES + tuple(REASONING_ARCHETYPES.keys())

# ── Linguistic rules distilled from research (THE_PROMPT_GUIDEBOOK.md) ────────
# Embedded into every LLM rewriting call so the generated content follows the
# same word-choice, framing, and specificity standards as hand-built prompts.

_LINGUISTIC_RULES = """\
LINGUISTIC RULES — apply to EVERY field you write:
1. IMPERATIVE framing — goals and tasks as directives, not descriptions.
   BAD: "Analyze the data."  GOOD: "Your mission: Surface every anomaly in Q4 revenue — accomplish this fully."
2. POSITIVE REDIRECT — never bare negation ("Do not hallucinate"). State the positive action + an explicit fallback phrase.
   BAD: "Do not hallucinate."  GOOD: "Every claim must be grounded in the provided source material. If the answer is absent, state: 'Not found in the provided material.'"
3. BINDING MODALS — must / always / never / shall / will. Never use should / try / ideally / consider / might for constraints.
4. SPECIFICITY — every rule must be objectively testable. If a reviewer cannot verify compliance, rewrite.
   BAD: "Be detailed."  GOOD: "Every finding must include ≥3 supporting data points."
5. ONE RULE = ONE SENTENCE — split compound rules into separate items.
6. CRITICAL-FIRST ordering — place the most important rules first; models apply earlier rules more reliably when conflicts arise.
7. SCOPE BOUNDING — after the role, add "Scope: Limit to X. Do not Y." to prevent persona drift.
8. OUTPUT CONTRACT — start with "Return ONLY" to suppress preamble.
9. GUARD RAILS — use "Omit X" + the positive behavior. Add an explicit fallback phrase for uncertainty. Suppress hedging: probably, might, could be, seems to, appears to.
10. TASK LAST — the task/instruction goes in the final position (recency zone) for highest recall at generation start.
11. GROUNDING PROTOCOL — include at least one rule requiring claims to be traceable to provided material. Add a fallback phrase for missing data (e.g. "If absent, state: '[NOT IN PACKET]'"). Without grounding, models invent plausible-sounding facts.
12. ANTI-BOILERPLATE — add a guard rail suppressing generic AI filler: "Omit stock phrases: 'in today's rapidly evolving', 'it's no wonder that', 'delve into', 'tapestry of', 'game-changer'. Write as a domain practitioner, not a generic AI."
13. DISCOURSE COHESION — each section must connect to the next. Use transitional framing: the last sentence of a section should motivate the next. Avoid orphan sections that repeat the introduction.\
"""

# ── Result dataclasses ───────────────────────────────────────────────────────


@dataclass
class ParsedSections:
    """Which of the 9 sections were detected in a raw prompt string."""

    role: str | None = None
    goal: str | None = None
    rules: list[str] = field(default_factory=list)
    style: str | None = None
    reasoning: str | None = None
    examples: list[str] = field(default_factory=list)
    output_contract: str | None = None
    guard_rails: list[str] = field(default_factory=list)
    task: str | None = None

    def present(self) -> list[str]:
        """Return names of sections that have content."""
        out = []
        for name in SECTION_NAMES:
            val = getattr(self, name)
            if val and (not isinstance(val, list) or len(val) > 0):
                out.append(name)
        return out

    def missing(self) -> list[str]:
        return [s for s in SECTION_NAMES if s not in self.present()]


@dataclass
class SectionDiff:
    """Change record for a single section."""

    section: str
    action: str  # "added", "strengthened", "unchanged", "kept"
    before: str
    after: str
    rationale: str


@dataclass
class ArchitectResult:
    """Full result from improve() or build()."""

    improved_context: Context
    improved_prompt: str

    before_score: float
    after_score: float
    score_delta: float

    parsed: ParsedSections
    diffs: list[SectionDiff]

    before_issues: list[str]
    after_issues: list[str]
    resolved_issues: list[str]

    metadata: dict[str, Any] = field(default_factory=dict)

    # ── Rendering helpers ──────────────────────────────────────────────

    def summary(self) -> str:
        """Short human-readable summary of what changed and the score lift."""
        added = [d.section for d in self.diffs if d.action == "added"]
        strengthened = [d.section for d in self.diffs if d.action == "strengthened"]
        lines = [
            f"Score: {self.before_score:.0%} → {self.after_score:.0%}  "
            f"(+{self.score_delta:.0%})",
        ]
        if added:
            lines.append(f"Added sections: {', '.join(added)}")
        if strengthened:
            lines.append(f"Strengthened: {', '.join(strengthened)}")
        if self.resolved_issues:
            lines.append(
                f"Resolved {len(self.resolved_issues)} issue(s): "
                + "; ".join(self.resolved_issues[:3])
            )
        return "\n".join(lines)

    def diff_report(self) -> str:
        """Section-by-section diff with rationale."""
        lines = ["── SECTION DIFF ──────────────────────────────────────────"]
        for d in self.diffs:
            tag = f"[{d.action.upper()}]"
            lines.append(f"\n{tag}  § {d.section.upper().replace('_', ' ')}")
            if d.action in ("added", "strengthened"):
                if d.before:
                    lines.append(f"  BEFORE: {d.before[:200]}")
                lines.append(f"  AFTER:  {d.after[:200]}")
            lines.append(f"  WHY:    {d.rationale}")
        lines.append("\n──────────────────────────────────────────────────────")
        return "\n".join(lines)


# ── Main class ───────────────────────────────────────────────────────────────


class PromptArchitect:
    """
    Apply the 9-Section Prompt Architecture to any raw prompt string.

    Three entry points:

    ``improve(prompt)``
        Parse an existing prompt, identify weak/missing sections,
        rewrite them using 9-section principles, and return the
        improved Context together with before/after scores and a
        section-level diff.

    ``build(task)``
        Given a plain task description, build a complete 9-section
        prompt from scratch using an LLM.

    ``parse(prompt)``
        Inspect a raw string and return which of the 9 sections it
        already contains (heuristic, no LLM call).

    Example::

        from mycontext.intelligence import PromptArchitect

        arch = PromptArchitect()

        # Improve an existing weak prompt
        result = arch.improve("You are an analyst. Summarize this data.")
        print(result.summary())
        print(result.diff_report())
        print(result.improved_prompt)

        # Build from scratch
        result = arch.build("Analyze customer churn and identify at-risk segments")
        print(result.improved_prompt)
    """

    # ── Construction rules used during rewriting ──────────────────────────────

    # ── Per-section construction rules (research-backed, THE_PROMPT_GUIDEBOOK) ─

    _ROLE_UPGRADE_HINTS = [
        "Formula: 'You are' + seniority + domain + optional context/setting.",
        "BAD: 'You are an expert.' GOOD: 'You are a senior data analyst with 10 years of experience in B2B SaaS revenue analysis.'",
        "Immediately after the role add: 'Scope: Limit [analysis/review/work] to [X]. Do not [Y].' — prevents persona drift.",
        "Reject generics: 'Expert Assistant', 'Helpful AI', 'AI helper' activate no domain knowledge.",
    ]

    _GOAL_UPGRADE_HINTS = [
        "Formula: 'Your mission: [specific achievement] — accomplish this fully.'",
        "State the completion criterion — what does success look like? The model must be able to judge its own output.",
        "Use imperative framing (directive, not description). BAD: 'Goal: Analyze data.' GOOD: 'Your mission: Identify every revenue anomaly above 2σ and rank by impact.'",
        "Place immediately after role (primacy zone — highest recall position).",
    ]

    _RULES_UPGRADE_HINTS = [
        "Rules are guarantees, not preferences. BAD: 'Try to be thorough.' GOOD: 'Every finding must include a code location, severity, and remediation step.'",
        "BINDING modals only: must / always / never / shall / will. Never should / try / ideally / consider.",
        "Each rule must be testable — a reviewer can objectively verify compliance.",
        "One rule = one sentence. Split compound rules.",
        "Order critical-first (Zhang et al. — earlier rules win conflicts).",
        "4-6 rules. Fewer than 3 leaves gaps; more than 8 dilutes attention.",
    ]

    _STYLE_UPGRADE_HINTS = [
        "Specify formality (formal/casual/technical), pace (concise/thorough/step-by-step), audience (senior engineer/executive/general public).",
        "Add negative style constraints: 'No hedging language', 'No jargon without definition', 'No preamble or greeting'.",
        "Keep style (voice/tone) separate from format (structure/layout) — do not mix.",
        "Reject generics: 'clear and helpful' is not a style. Name 2-3 specific, measurable tone adjectives.",
        "REGISTER FIT: Match vocabulary and diction to the declared audience and genre. "
        "A technical brief for staff engineers differs from a travel blog for tourists. "
        "Explicitly name the genre (blog / internal brief / tutorial / proposal) so tone is anchored.",
        "Suppress generic AI voice: 'Omit jargon without definition and preamble or greeting' is the minimum; "
        "add 'Write in the voice of a practicing [domain] professional, not a generic AI assistant.'",
    ]

    _REASONING_UPGRADE_HINTS = [
        "Read the user's GOAL and TASK. Choose reasoning strategy slugs that fit the *question*, not a default.",
        "Use ONE strategy when a single mode is enough; use MANY (ordered) when the task blends needs "
        "(e.g. step_by_step + verify for long multi-step work under accountability).",
        "Atomic slugs (combine when appropriate): "
        + ", ".join(REASONING_STRATEGY_CHOICES)
        + ".",
        "  step_by_step — decomposition / CoT; early-step errors propagate.",
        "  multiple_angles — real trade-offs; compare options before choosing.",
        "  verify — self-check, high-stakes or low-review settings.",
        "  explain_simply — non-expert audience; plain language.",
        "  creative — novelty / divergent generation is the goal.",
        "Named archetypes (pre-validated compositions — use when task matches): "
        + ", ".join(f"{k} ({'+'.join(v)})" for k, v in REASONING_ARCHETYPES.items())
        + ".",
        "  analytical — step_by_step + verify: data analysis, root cause, debugging.",
        "  deliberative — multiple_angles + step_by_step + verify: decision making, trade-off analysis.",
        "  explanatory — explain_simply + step_by_step: tutorials, user guides, onboarding.",
        "  creative — creative + multiple_angles: brainstorming, content creation, ideation.",
        "  high_stakes — step_by_step + multiple_angles + verify: compliance, security, medical.",
        "Order matters: put the primary strategy first, then supporting passes (e.g. decompose → verify).",
        "Output them as a JSON array under reasoning_strategies (see schema). Legacy single string "
        "\"reasoning\" is still accepted if exactly one slug applies.",
    ]

    _EXAMPLES_UPGRADE_HINTS = [
        "2-5 representative examples. Fewer than 2 = too much ambiguity; more than 5 = token waste.",
        "Examples must match the exact output format (JSON → JSON, bullets → bullets).",
        "Include at least one edge case or negative example showing what WRONG looks like.",
        "Place after the reasoning-strategy rules (middle zone — calibration position).",
    ]

    _OUTPUT_CONTRACT_UPGRADE_HINTS = [
        "Start with 'Return ONLY' — these two words reliably suppress preamble.",
        "Specify: (1) form (JSON/bullets/table/prose), (2) structure of each item, (3) what to exclude (no preamble, no summary, no markdown if unwanted).",
        "BAD: 'Output a summary.' GOOD: 'Return ONLY a 3-part structure: 1) KEY FINDING (1 sentence), 2) EVIDENCE (2-3 bullets), 3) RECOMMENDED ACTION (1 sentence).'",
    ]

    _GUARD_RAILS_UPGRADE_HINTS = [
        "POSITIVE REDIRECTS only. BAD: 'Do not hallucinate.' GOOD: 'Every claim must be grounded in the source material. If absent, state: \"Not found in the provided material.\"'",
        "Use 'Omit' for exclusions: 'Omit speculation', 'Omit hedging language: probably, might, could be, seems to, appears to.'",
        "For every exclusion, provide the positive alternative: what the model SHOULD do instead.",
        "Include an explicit fallback phrase for uncertainty — exact words to produce instead of guessing.",
        "Add edge-case handling: missing data, ambiguous input, or out-of-scope requests.",
        "GROUNDING: Always include a rail requiring factual claims to trace to provided material. "
        "Without grounding, models invent plausible-sounding statistics, vendors, and studies.",
        "ANTI-BOILERPLATE: Add 'Omit stock AI phrases: \"in today's rapidly evolving\", \"delve into\", \"tapestry of\", \"game-changer\", \"it's no wonder\". "
        "Write as a domain practitioner, not a generic AI assistant.'",
    ]

    _TASK_UPGRADE_HINTS = [
        "Place LAST (recency zone — highest attention when generation begins).",
        "Be specific about the input: refer to exactly what data/material is provided.",
        "The final sentence must be the clearest, most direct imperative in the entire prompt.",
        "For long-context tasks (>1500 chars of data), add a REMINDER after the data restating the core instruction.",
    ]

    _HINTS: dict[str, list[str]] = {
        "role": _ROLE_UPGRADE_HINTS,
        "goal": _GOAL_UPGRADE_HINTS,
        "rules": _RULES_UPGRADE_HINTS,
        "style": _STYLE_UPGRADE_HINTS,
        "reasoning": _REASONING_UPGRADE_HINTS,
        "examples": _EXAMPLES_UPGRADE_HINTS,
        "output_contract": _OUTPUT_CONTRACT_UPGRADE_HINTS,
        "guard_rails": _GUARD_RAILS_UPGRADE_HINTS,
        "task": _TASK_UPGRADE_HINTS,
    }

    _GENRE_FORMAT_HINTS: dict[str, str] = {
        "internal brief": "Return ONLY markdown with ## headings as specified. No JSON wrapper.",
        "blog post": "Return ONLY markdown prose with a title and ## subheadings. No JSON.",
        "tutorial": "Return ONLY markdown with ## step headings and fenced code blocks.",
        "executive summary": "Return ONLY markdown prose — 1-2 pages, ## sections.",
        "api reference": "Return ONLY valid JSON matching the specified schema.",
        "email": "Return ONLY plain text. No markdown formatting.",
        "proposal": "Return ONLY markdown with ## sections. No JSON wrapper.",
    }

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4o-mini",
        *,
        assembly_provider_hint: ProviderHint | None = None,
    ):
        self.provider = provider
        self.model = model
        # How assemble() formats headings/XML (openai / anthropic / gemini).
        # None → inferred from *provider* (the LLM used for improve/build).
        self._assembly_provider_hint = assembly_provider_hint

    def _resolve_assembly_provider_hint(self) -> ProviderHint | None:
        if self._assembly_provider_hint is not None:
            return self._assembly_provider_hint
        p = (self.provider or "").lower().strip()
        direct: dict[str, ProviderHint] = {
            "openai": "openai",
            "anthropic": "anthropic",
            "gemini": "gemini",
        }
        if p in direct:
            return direct[p]
        if p in ("google", "vertex", "genai"):
            return "gemini"
        return None

    # ── Public API ────────────────────────────────────────────────────────────

    def parse(self, prompt: str) -> ParsedSections:
        """
        Heuristically detect which of the 9 sections are present in a raw prompt.

        No LLM call — pure text analysis.

        Args:
            prompt: Any raw prompt string.

        Returns:
            ParsedSections with found content per section.
        """
        return self._heuristic_parse(prompt)

    def build(
        self,
        task: str,
        provider: str | None = None,
        model: str | None = None,
        user_message: str | None = None,
        task_contract: Any | None = None,
        **execute_kwargs: Any,
    ) -> ArchitectResult:
        """
        Build a complete 9-section prompt from a plain task description.

        Args:
            task: Plain-language task description.
            provider: Override default provider.
            model: Override default model.
            user_message: The actual user message/task the model will receive.
            task_contract: Optional TaskContract (L0 metadata).

        Returns:
            ArchitectResult with the built context and scores.
        """
        provider = provider or self.provider
        model = model or self.model

        # Score a trivial context so we have a "before" baseline
        baseline_ctx = Context(
            guidance=Guidance(role="Assistant", rules=[]),
            directive=Directive(content=task),
        )
        from .quality_metrics import QualityMetrics

        qm = QualityMetrics()
        before_score_obj = qm.evaluate(baseline_ctx)
        before_score = before_score_obj.overall

        # LLM build
        built_json = self._llm_build(
            task, provider, model,
            user_message=user_message,
            task_contract=task_contract,
            **execute_kwargs,
        )
        improved_ctx = self._json_to_context(built_json, task, task_contract=task_contract)

        after_score_obj = qm.evaluate(improved_ctx)
        after_score = after_score_obj.overall

        # All sections were added from scratch
        diffs = self._build_diffs_from_json(built_json)

        return ArchitectResult(
            improved_context=improved_ctx,
            improved_prompt=improved_ctx.assemble(),
            before_score=before_score,
            after_score=after_score,
            score_delta=after_score - before_score,
            parsed=ParsedSections(task=task),
            diffs=diffs,
            before_issues=before_score_obj.issues,
            after_issues=after_score_obj.issues,
            resolved_issues=list(set(before_score_obj.issues) - set(after_score_obj.issues)),
            metadata={"mode": "build", "model": model, "provider": provider},
        )

    def improve(
        self,
        prompt: str,
        provider: str | None = None,
        model: str | None = None,
        user_message: str | None = None,
        task_contract: Any | None = None,
        **execute_kwargs: Any,
    ) -> ArchitectResult:
        """
        Parse an existing prompt, identify weak/missing sections, and rewrite them.

        Steps:
          1. Parse: detect existing sections heuristically.
          2. Score: QualityMetrics on the original.
          3. Rewrite: LLM fills missing sections, strengthens weak ones. The model
             chooses ``reasoning_strategies`` (one or many, task-ordered) from the
             goal/task, not a fixed default.
          4. Score: QualityMetrics on the improved version.
          5. Diff: section-by-section change record.

        Args:
            prompt: The raw prompt string to improve.
            provider: Override default provider.
            model: Override default model.
            user_message: The actual user message/task the model will receive.
                When provided, the LLM rewriter can infer output format, grounding
                markers, and domain-specific terms from it.
            task_contract: Optional TaskContract (L0 metadata) — domain, audience,
                genre, grounding. Calibrates every generated section.

        Returns:
            ArchitectResult with improved context, scores, and diffs.
        """
        provider = provider or self.provider
        model = model or self.model

        # Step 1 — Parse
        parsed = self._heuristic_parse(prompt)

        # Step 2 — Score original
        original_ctx = self._parsed_to_context(parsed, prompt)
        from .quality_metrics import QualityMetrics

        qm = QualityMetrics()
        before_score_obj = qm.evaluate(original_ctx)
        before_score = before_score_obj.overall

        # Step 3 — LLM rewrite
        improved_json = self._llm_improve(
            prompt, parsed, provider, model,
            user_message=user_message,
            task_contract=task_contract,
            **execute_kwargs,
        )
        improved_ctx = self._json_to_context(
            improved_json, parsed.task or prompt, task_contract=task_contract,
        )

        # Step 4 — Score improved
        after_score_obj = qm.evaluate(improved_ctx)
        after_score = after_score_obj.overall

        # Step 5 — Diff
        diffs = self._compute_diffs(parsed, improved_json)

        return ArchitectResult(
            improved_context=improved_ctx,
            improved_prompt=improved_ctx.assemble(),
            before_score=before_score,
            after_score=after_score,
            score_delta=after_score - before_score,
            parsed=parsed,
            diffs=diffs,
            before_issues=before_score_obj.issues,
            after_issues=after_score_obj.issues,
            resolved_issues=list(set(before_score_obj.issues) - set(after_score_obj.issues)),
            metadata={"mode": "improve", "model": model, "provider": provider},
        )

    # ── Heuristic parser ──────────────────────────────────────────────────────

    def _heuristic_parse(self, prompt: str) -> ParsedSections:
        """Detect 9-section content in a raw prompt string without an LLM call."""
        lower = prompt.lower()
        lines = [ln.strip() for ln in prompt.split("\n") if ln.strip()]

        # ① Role
        role = self._extract_role(prompt, lower, lines)

        # ② Goal
        goal = self._extract_goal(prompt, lower, lines)

        # ③ Rules
        rules = self._extract_rules(prompt, lower, lines)

        # ④ Style
        style = self._extract_style(lower, lines)

        # ⑤ Reasoning
        reasoning = self._extract_reasoning(lower)

        # ⑥ Examples
        examples = self._extract_examples(prompt, lower)

        # ⑦ Output contract
        output_contract = self._extract_output_contract(lower, lines)

        # ⑧ Guard rails
        guard_rails = self._extract_guard_rails(lower, lines)

        # ⑨ Task — last substantive imperative sentence
        task = self._extract_task(prompt, lower, lines)

        return ParsedSections(
            role=role,
            goal=goal,
            rules=rules,
            style=style,
            reasoning=reasoning,
            examples=examples,
            output_contract=output_contract,
            guard_rails=guard_rails,
            task=task,
        )

    def _extract_role(self, prompt: str, lower: str, lines: list[str]) -> str | None:
        # "You are X" is the canonical pattern
        m = re.search(r"you are ([^\n.!]+)", lower)
        if m:
            # Return original-case segment
            start = m.start(1)
            end = m.end(1)
            return prompt[start:end].strip()
        # "act as X"
        m = re.search(r"act as ([^\n.!]+)", lower)
        if m:
            return prompt[m.start(1):m.end(1)].strip()
        # Role/Persona label
        for ln in lines[:5]:
            if re.match(r"^(role|persona)\s*[:：]", ln.lower()):
                return re.sub(r"^(role|persona)\s*[:：]\s*", "", ln, flags=re.IGNORECASE).strip()
        return None

    def _extract_goal(self, prompt: str, lower: str, lines: list[str]) -> str | None:
        m = re.search(r"(?:goal|objective|mission|your goal|your mission)\s*[:：]\s*([^\n]+)", lower)
        if m:
            start = m.start(1)
            return prompt[start:start + len(m.group(1))].strip()
        # Standalone imperative sentence (capitalize first word is an action verb)
        action_verbs = (
            "identify", "analyze", "produce", "generate", "determine",
            "evaluate", "assess", "summarize", "classify", "detect",
            "find", "recommend", "explain", "describe", "extract",
        )
        for ln in lines[:8]:
            first = ln.split()[0].lower().rstrip(".,") if ln.split() else ""
            if first in action_verbs and len(ln.split()) > 4:
                return ln.strip()
        return None

    def _extract_rules(self, prompt: str, lower: str, lines: list[str]) -> list[str]:
        rules = []
        in_rules = False
        for ln in lines:
            ll = ln.lower()
            if re.match(r"^(rules|guidelines|principles|follow these)\s*[:：]?$", ll):
                in_rules = True
                continue
            if in_rules:
                if re.match(r"^[-*•]\s+.+", ln) or re.match(r"^\d+[.)]\s+.+", ln):
                    rules.append(re.sub(r"^[-*•\d.)\s]+", "", ln).strip())
                elif ln == "" or re.match(r"^#{1,3}\s+", ln):
                    in_rules = False
            # Also grab bullet/numbered items that contain binding modals
            elif re.match(r"^[-*•]\s+.+", ln) or re.match(r"^\d+[.)]\s+.+", ln):
                item = re.sub(r"^[-*•\d.)\s]+", "", ln).strip()
                if any(w in item.lower() for w in ("must", "always", "never", "will ", "shall")):
                    rules.append(item)
        return rules

    def _extract_style(self, lower: str, lines: list[str]) -> str | None:
        m = re.search(r"(?:style|tone|voice|communication style)\s*[:：]\s*([^\n]+)", lower)
        if m:
            return m.group(1).strip()
        return None

    def _extract_reasoning(self, lower: str) -> str | None:
        # Assembled prompts from improve() weave strategies into the first RULE line:
        m = re.search(
            r"reasoning strategies\s*\([^)]*\)\s*:\s*([^\n]+)",
            lower,
        )
        if m:
            return m.group(1).strip()
        m = re.search(r"reasoning\s*strategies\s*:\s*([^\n]+)", lower)
        if m:
            return m.group(1).strip()
        m = re.search(r"reasoning\s*strategy\s*:\s*([^\n]+)", lower)
        if m:
            return m.group(1).strip()
        strategy_patterns = [
            r"step[- ]by[- ]step",
            r"chain[- ]of[- ]thought",
            r"tree[- ]of[- ]thought",
            r"think.*through",
            r"reason.*step",
            r"before.*answer.*consider",
        ]
        for pat in strategy_patterns:
            if re.search(pat, lower):
                return re.search(pat, lower).group(0)
        return None

    def _extract_examples(self, prompt: str, lower: str) -> list[str]:
        examples = []
        # Code fences labeled as examples
        for m in re.finditer(r"```[^\n]*\n(.*?)```", prompt, re.DOTALL):
            if any(kw in lower[max(0, m.start() - 100):m.start()] for kw in ("example", "e.g.", "sample")):
                examples.append(m.group(0)[:300])
        # Inline "Example:" blocks
        for m in re.finditer(r"(?:example|e\.g\.)[^:]*:\s*([^\n]+)", lower):
            examples.append(prompt[m.start(1):m.start(1) + len(m.group(1))].strip()[:200])
        return examples[:3]

    def _extract_output_contract(self, lower: str, lines: list[str]) -> str | None:
        patterns = [
            r"output[_ ](?:format|contract|schema)\s*[:：]?\s*([^\n]+)",
            r"respond (?:with|in)\s*([^\n]+)",
            r"return (?:only|a)\s*([^\n]+)",
            r"format\s*[:：]\s*([^\n]+)",
        ]
        for pat in patterns:
            m = re.search(pat, lower)
            if m:
                return m.group(1).strip()
        return None

    def _extract_guard_rails(self, lower: str, lines: list[str]) -> list[str]:
        rails = []
        for ln in lines:
            ll = ln.lower()
            if any(
                ll.startswith(p)
                for p in ("do not", "don't", "never ", "avoid ", "must not", "exclude ")
            ):
                rails.append(ln.strip())
        return rails[:6]

    def _extract_task(self, prompt: str, lower: str, lines: list[str]) -> str | None:
        # Last non-empty line that is a direct instruction
        for ln in reversed(lines):
            if len(ln.split()) >= 4 and not ln.startswith("#"):
                return ln.strip()
        return None

    # ── Context construction helpers ──────────────────────────────────────────

    def _parsed_to_context(self, parsed: ParsedSections, raw: str) -> Context:
        """Wrap parsed sections into a Context for scoring."""
        role = parsed.role or "Assistant"
        guidance = Guidance(
            role=role,
            goal=parsed.goal,
            rules=parsed.rules or [],
            style=parsed.style,
        )
        task_text = parsed.task or raw
        directive = Directive(content=task_text)
        constraints = None
        if parsed.output_contract or parsed.guard_rails:
            constraints = Constraints(
                output_contract=parsed.output_contract,
                must_not_include=parsed.guard_rails or None,
            )
        return Context(guidance=guidance, directive=directive, constraints=constraints)

    @staticmethod
    @staticmethod
    def _normalize_reasoning_strategies(raw: Any) -> list[str]:
        """Coerce LLM JSON into an ordered, de-duplicated list of strategy slugs.

        Named archetypes (e.g. "analytical") are expanded into their
        component atomic strategies. Atomic slugs pass through unchanged.
        """
        if raw is None:
            return []
        if isinstance(raw, str):
            s = raw.strip()
            if not s or s.lower() in ("null", "none"):
                return []
            raw = [s]
        if isinstance(raw, list):
            out: list[str] = []
            for x in raw:
                if x is None:
                    continue
                t = str(x).strip().lower()
                if not t or t in ("null", "none"):
                    continue
                if t in REASONING_ARCHETYPES:
                    for slug in REASONING_ARCHETYPES[t]:
                        if slug not in out:
                            out.append(slug)
                else:
                    if t not in out:
                        out.append(t)
            return out
        return []

    def _json_to_context(
        self,
        data: dict,
        fallback_task: str,
        task_contract: Any | None = None,
    ) -> Context:
        """Convert LLM-returned JSON dict into a Context object."""
        from ..foundation.task_contract import TaskContract

        role = data.get("role") or "Assistant"
        goal = data.get("goal") or None
        rules = data.get("rules") or []
        style = data.get("style") or None
        output_contract = data.get("output_contract") or None
        guard_rails = data.get("guard_rails") or []
        task = data.get("task") or fallback_task

        raw_rs = data.get("reasoning_strategies")
        if raw_rs is None:
            raw_rs = data.get("reasoning")
        strategies = self._normalize_reasoning_strategies(raw_rs)

        # Genre-format alignment: if a TaskContract specifies a genre, ensure
        # the output_contract doesn't contradict it (e.g. genre="internal brief"
        # but output_contract says "Return ONLY JSON").
        tc = task_contract
        if tc and hasattr(tc, "genre") and tc.genre:
            genre_lower = tc.genre.lower().strip()
            genre_hint = self._GENRE_FORMAT_HINTS.get(genre_lower)
            if genre_hint and output_contract:
                oc_lower = output_contract.lower()
                is_prose_genre = genre_lower in (
                    "internal brief", "blog post", "tutorial",
                    "executive summary", "proposal",
                )
                if is_prose_genre and "json" in oc_lower and "no json" not in oc_lower:
                    logger.info(
                        "Genre-format fix: genre='%s' but output_contract mentions JSON — overriding",
                        tc.genre,
                    )
                    output_contract = genre_hint
            elif genre_hint and not output_contract:
                output_contract = genre_hint

        # Weave task-chosen reasoning into rules (first = highest attention in RULES)
        full_rules = list(rules)
        if len(strategies) == 1:
            full_rules.insert(0, f"Reasoning strategy: {strategies[0]}")
        elif len(strategies) > 1:
            chain = " → ".join(strategies)
            full_rules.insert(
                0,
                "Reasoning strategies (infer fit from goal/task; apply in order): "
                + chain,
            )

        guidance = Guidance(
            role=role,
            goal=goal,
            rules=full_rules,
            style=style,
        )

        # Examples go in the directive as an injected block
        examples_block = ""
        raw_examples = data.get("examples") or []
        if raw_examples:
            ex_lines = "\n".join(
                f"Example {i+1}: {ex}" for i, ex in enumerate(raw_examples)
            )
            examples_block = f"\n\n**EXAMPLES**\n{ex_lines}\n\n"

        directive = Directive(content=f"{examples_block}{task}")

        constraints = None
        if output_contract or guard_rails:
            constraints = Constraints(
                output_contract=output_contract or None,
                must_not_include=guard_rails or None,
            )

        # Resolve TaskContract
        resolved_tc: TaskContract | None = None
        if tc and isinstance(tc, TaskContract):
            resolved_tc = tc
        elif tc and hasattr(tc, "to_dict"):
            resolved_tc = tc

        return Context(
            guidance=guidance,
            directive=directive,
            constraints=constraints,
            task_contract=resolved_tc,
            research_flow=True,
            provider_hint=self._resolve_assembly_provider_hint(),
        )

    # ── LLM calls ─────────────────────────────────────────────────────────────

    def _llm_improve(
        self,
        original: str,
        parsed: ParsedSections,
        provider: str,
        model: str,
        **kwargs: Any,
    ) -> dict:
        """Ask the LLM to fill missing sections and strengthen weak ones."""
        user_message = kwargs.pop("user_message", None)
        task_contract = kwargs.pop("task_contract", None)

        missing = parsed.missing()
        present = parsed.present()

        hints_block = ""
        for section in missing:
            hints = self._HINTS.get(section, [])
            hints_block += f"\nSection '{section}' is MISSING. Rules for writing it:\n"
            hints_block += "\n".join(f"  - {h}" for h in hints)

        weak_sections = self._detect_weak_sections(parsed)
        for section in weak_sections:
            if section not in missing:
                hints = self._HINTS.get(section, [])
                hints_block += f"\nSection '{section}' is WEAK. Improvement rules:\n"
                hints_block += "\n".join(f"  - {h}" for h in hints)

        present_summary = ", ".join(present) if present else "none detected"

        # Build optional context blocks
        user_msg_block = ""
        if user_message:
            user_msg_block = f"""
USER MESSAGE (the actual task the model will receive — infer the required output
format, grounding markers, domain terms, and structural requirements from this):
\"\"\"
{user_message[:3000]}
\"\"\"
"""

        tc_block = ""
        if task_contract and hasattr(task_contract, "to_dict"):
            tc_dims = task_contract.to_dict()
            if tc_dims:
                rows = "\n".join(f"  {k}: {v}" for k, v in tc_dims.items())
                tc_block = f"""
TASK CONTRACT (L0 — calibrate EVERY section against these dimensions):
{rows}
CRITICAL: The 'genre' MUST match the output_contract format. If genre is
'internal brief' or 'blog post', output_contract MUST specify markdown, NOT JSON.
"""

        system = (
            "You are a world-class prompt engineer applying the 9-Section "
            "Prompt Architecture.\n\n"
            f"{_LINGUISTIC_RULES}\n\n"
            "You output ONLY valid JSON — no commentary, no markdown wrapper."
        )

        user = f"""ORIGINAL PROMPT:
\"\"\"
{original}
\"\"\"
{user_msg_block}{tc_block}
SECTIONS ALREADY PRESENT: {present_summary}
SECTIONS MISSING OR WEAK: {', '.join(missing + weak_sections) or 'none'}

{hints_block}

Your task: rewrite the prompt by completing ALL 9 sections.
Preserve the intent of the original. Upgrade weak sections. Add missing ones.
Apply every LINGUISTIC RULE from your instructions to every field you write.
{"If a USER MESSAGE is provided above, ensure the output_contract format matches what the user expects (e.g. markdown headings, not JSON, for a brief/blog)." if user_message else ""}

Return ONLY this JSON (fill every field — use null only if truly not applicable):
{{
  "role": "'You are' + seniority + domain. Follow with 'Scope: Limit to X. Do not Y.'",
  "goal": "'Your mission: [specific achievement] — accomplish this fully.' (imperative, not declarative)",
  "rules": ["binding-modal rule 1 (testable, one sentence)", "rule 2", "rule 3", "rule 4 — order critical-first"],
  "style": "formality + pace + audience. Add negative style constraints.",
  "reasoning_strategies": ["slug_from_task_1", "optional_second_slug"],
  "examples": ["example matching output format", "edge-case or negative example — optional"],
  "output_contract": "'Return ONLY …' + form + structure + exclusions",
  "guard_rails": ["positive redirect + fallback phrase", "Omit hedging: probably, might, could be"],
  "task": "clearest imperative sentence — placed last (recency zone)"
}}

For reasoning_strategies: read the ORIGINAL PROMPT's goal and task. Pick one or more from:
  Atomic: {", ".join(REASONING_STRATEGY_CHOICES)}
  Archetypes: {", ".join(f"{k} ({'+'.join(v)})" for k, v in REASONING_ARCHETYPES.items())}
Use [] or null only if no cognitive scaffold helps. Order = application order (primary first).
You may use a named archetype slug (e.g. "analytical") which expands to its component strategies.
Legacy single field "reasoning" with one slug is still accepted when exactly one applies."""

        return self._call_llm_for_json(system, user, provider, model, **kwargs)

    def _llm_build(
        self,
        task: str,
        provider: str,
        model: str,
        **kwargs: Any,
    ) -> dict:
        """Build all 9 sections from a plain task description."""
        user_message = kwargs.pop("user_message", None)
        task_contract = kwargs.pop("task_contract", None)

        hints_block = ""
        for section, hints in self._HINTS.items():
            hints_block += f"\n§ {section.upper().replace('_', ' ')}:\n"
            hints_block += "\n".join(f"  - {h}" for h in hints)

        user_msg_block = ""
        if user_message:
            user_msg_block = f"""
USER MESSAGE (the actual task the model will receive — infer output format,
grounding markers, and domain terms from this):
\"\"\"
{user_message[:3000]}
\"\"\"
"""

        tc_block = ""
        if task_contract and hasattr(task_contract, "to_dict"):
            tc_dims = task_contract.to_dict()
            if tc_dims:
                rows = "\n".join(f"  {k}: {v}" for k, v in tc_dims.items())
                tc_block = f"""
TASK CONTRACT (L0 — calibrate EVERY section against these dimensions):
{rows}
CRITICAL: The 'genre' MUST match the output_contract format.
"""

        system = (
            "You are a world-class prompt engineer applying the 9-Section "
            "Prompt Architecture.\n\n"
            f"{_LINGUISTIC_RULES}\n\n"
            "You output ONLY valid JSON — no commentary, no markdown wrapper."
        )

        user = f"""TASK DESCRIPTION:
\"{task}\"
{user_msg_block}{tc_block}
Build a complete 9-section prompt for this task.
Apply every LINGUISTIC RULE from your instructions to every field you write.
{"If a USER MESSAGE is provided above, ensure the output_contract format matches what the user expects." if user_message else ""}
{hints_block}

Return ONLY this JSON (fill every field — use null only if truly not applicable):
{{
  "role": "'You are' + seniority + domain. Follow with 'Scope: Limit to X. Do not Y.'",
  "goal": "'Your mission: [specific achievement] — accomplish this fully.' (imperative, not declarative)",
  "rules": ["binding-modal rule 1 (testable, one sentence)", "rule 2", "rule 3", "rule 4 — order critical-first"],
  "style": "formality + pace + audience. Add negative style constraints.",
  "reasoning_strategies": ["slug_from_task_1", "optional_second_slug"],
  "examples": ["example matching output format", "edge-case or negative example — optional"],
  "output_contract": "'Return ONLY …' + form + structure + exclusions",
  "guard_rails": ["positive redirect + fallback phrase", "Omit hedging: probably, might, could be"],
  "task": "clearest imperative sentence — placed last (recency zone)"
}}

For reasoning_strategies: infer from the TASK DESCRIPTION above. Pick one or more from:
  Atomic: {", ".join(REASONING_STRATEGY_CHOICES)}
  Archetypes: {", ".join(f"{k} ({'+'.join(v)})" for k, v in REASONING_ARCHETYPES.items())}
Use [] or null if none apply. Order = application order.
You may use a named archetype slug (e.g. "analytical") which expands to its component strategies.
Legacy single "reasoning" slug is allowed when only one applies."""

        return self._call_llm_for_json(system, user, provider, model, **kwargs)

    def _call_llm_for_json(
        self,
        system: str,
        user: str,
        provider: str,
        model: str,
        **kwargs: Any,
    ) -> dict:
        """Execute an LLM call and parse the JSON response. Falls back to empty dict."""
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
                temperature=kwargs.pop("temperature", 0.3),
                **kwargs,
            )
            raw = result.response.strip()
            # Strip optional markdown fence
            if raw.startswith("```"):
                raw = re.sub(r"^```[a-z]*\n?", "", raw)
                raw = re.sub(r"\n?```$", "", raw).strip()
            return json.loads(raw)
        except Exception as exc:
            logger.warning("PromptArchitect LLM call failed: %s", exc, exc_info=True)
            return {}

    # ── Diff helpers ──────────────────────────────────────────────────────────

    def _compute_diffs(self, parsed: ParsedSections, improved: dict) -> list[SectionDiff]:
        diffs = []
        for section in SECTION_NAMES:
            before_val = getattr(parsed, section)
            if section == "reasoning":
                after_val = improved.get("reasoning_strategies")
                if after_val is None:
                    after_val = improved.get("reasoning")
            else:
                after_val = improved.get(section)

            before_str = self._val_to_str(before_val)
            after_str = self._val_to_str(after_val)

            if not before_str and after_str:
                action = "added"
                rationale = f"Section was absent; added using 9-section principle: {self._HINTS[section][0]}"
            elif before_str and after_str and before_str != after_str:
                action = "strengthened"
                rationale = f"Existing content was weak or incomplete; upgraded per: {self._HINTS[section][0]}"
            elif before_str and not after_str:
                action = "kept"
                rationale = "Section was present and LLM returned no replacement."
            else:
                action = "unchanged"
                rationale = "No change needed."

            diffs.append(
                SectionDiff(
                    section=section,
                    action=action,
                    before=before_str[:300],
                    after=after_str[:300],
                    rationale=rationale,
                )
            )
        return diffs

    def _build_diffs_from_json(self, built: dict) -> list[SectionDiff]:
        diffs = []
        for section in SECTION_NAMES:
            if section == "reasoning":
                after_val = built.get("reasoning_strategies")
                if after_val is None:
                    after_val = built.get("reasoning")
            else:
                after_val = built.get(section)
            after_str = self._val_to_str(after_val)
            diffs.append(
                SectionDiff(
                    section=section,
                    action="added" if after_str else "unchanged",
                    before="",
                    after=after_str[:300],
                    rationale=self._HINTS[section][0] if after_str else "Not applicable.",
                )
            )
        return diffs

    @staticmethod
    def _val_to_str(val: Any) -> str:
        if val is None:
            return ""
        if isinstance(val, list):
            return "; ".join(str(v) for v in val if v)
        return str(val).strip()

    def _detect_weak_sections(self, parsed: ParsedSections) -> list[str]:
        """Flag sections that exist but are low-quality."""
        weak = []
        # Role is weak if it's generic
        if parsed.role:
            generic = {"assistant", "expert assistant", "helpful assistant", "ai assistant"}
            if parsed.role.lower().strip() in generic:
                weak.append("role")
        # Rules are weak if fewer than 3 or use suggestive language
        if parsed.rules:
            if len(parsed.rules) < 3:
                weak.append("rules")
            else:
                suggestive = sum(
                    1 for r in parsed.rules
                    if any(w in r.lower() for w in ("should", "try to", "ideally", "consider"))
                )
                if suggestive > len(parsed.rules) // 2:
                    weak.append("rules")
        # Goal is weak if very short
        if parsed.goal and len(parsed.goal.split()) < 5:
            weak.append("goal")
        return list(dict.fromkeys(weak))  # deduplicate, preserve order
