"""
Output Evaluator - Measure LLM output quality against its context

Evaluates the *output* of an LLM (not the prompt), scoring how well the
response leverages the cognitive scaffolding provided by the context.

Seven dimensions (distinct from QualityMetrics' prompt-level dimensions):
  - Instruction Following
  - Reasoning Depth
  - Actionability
  - Structure Compliance
  - Cognitive Scaffolding
  - Groundedness       (v2: does every claim trace to provided material?)
  - Register Fit       (v2: does tone/vocab match audience and genre?)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from ..core import Context


class OutputDimension(Enum):
    INSTRUCTION_FOLLOWING = "instruction_following"
    REASONING_DEPTH = "reasoning_depth"
    ACTIONABILITY = "actionability"
    STRUCTURE_COMPLIANCE = "structure_compliance"
    COGNITIVE_SCAFFOLDING = "cognitive_scaffolding"
    GROUNDEDNESS = "groundedness"
    REGISTER_FIT = "register_fit"


@dataclass
class OutputQualityScore:
    overall: float
    dimensions: dict[OutputDimension, float]
    evidence: dict[OutputDimension, str]
    strengths: list[str]
    weaknesses: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


_DIMENSION_WEIGHTS = {
    OutputDimension.INSTRUCTION_FOLLOWING: 0.20,
    OutputDimension.REASONING_DEPTH: 0.15,
    OutputDimension.ACTIONABILITY: 0.15,
    OutputDimension.STRUCTURE_COMPLIANCE: 0.10,
    OutputDimension.COGNITIVE_SCAFFOLDING: 0.15,
    OutputDimension.GROUNDEDNESS: 0.15,
    OutputDimension.REGISTER_FIT: 0.10,
}


class OutputEvaluator:
    """
    Evaluate LLM output quality relative to the context that produced it.

    Example::

        >>> from mycontext import Context
        >>> from mycontext.intelligence.output_evaluator import OutputEvaluator
        >>> ctx = Context(guidance="Senior analyst", directive="Identify root causes")
        >>> evaluator = OutputEvaluator()
        >>> score = evaluator.evaluate(ctx, llm_output)
        >>> print(f"Overall: {score.overall:.1%}")
    """

    def __init__(
        self,
        mode: str = "heuristic",
        provider: str = "openai",
        model: str = "gpt-4o-mini",
        dimension_weights: dict[str, float] | None = None,
    ):
        self.mode = mode
        self.provider = provider
        self.model = model
        self._custom_weights: dict[OutputDimension, float] | None = None
        if dimension_weights:
            self._custom_weights = {
                OutputDimension(k): v for k, v in dimension_weights.items()
                if k in {d.value for d in OutputDimension}
            }

    def evaluate(
        self,
        context: Context,
        output: str,
        **kwargs: Any,
    ) -> OutputQualityScore:
        if self.mode == "llm":
            return self._evaluate_llm(context, output, **kwargs)
        elif self.mode == "hybrid":
            return self._evaluate_hybrid(context, output, **kwargs)
        return self._evaluate_heuristic(context, output)

    # -- Heuristic evaluation -------------------------------------------------

    def _evaluate_heuristic(
        self, context: Context, output: str
    ) -> OutputQualityScore:
        assembled = context.assemble()
        words = output.split()
        word_count = len(words)

        dims: dict[OutputDimension, float] = {}
        evidence: dict[OutputDimension, str] = {}
        strengths: list[str] = []
        weaknesses: list[str] = []

        if_score, if_ev = self._score_instruction_following(assembled, output)
        dims[OutputDimension.INSTRUCTION_FOLLOWING] = if_score
        evidence[OutputDimension.INSTRUCTION_FOLLOWING] = if_ev

        rd_score, rd_ev = self._score_reasoning_depth(output)
        dims[OutputDimension.REASONING_DEPTH] = rd_score
        evidence[OutputDimension.REASONING_DEPTH] = rd_ev

        ac_score, ac_ev = self._score_actionability(output)
        dims[OutputDimension.ACTIONABILITY] = ac_score
        evidence[OutputDimension.ACTIONABILITY] = ac_ev

        sc_score, sc_ev = self._score_structure_compliance(assembled, output)
        dims[OutputDimension.STRUCTURE_COMPLIANCE] = sc_score
        evidence[OutputDimension.STRUCTURE_COMPLIANCE] = sc_ev

        cs_score, cs_ev = self._score_cognitive_scaffolding(assembled, output)
        dims[OutputDimension.COGNITIVE_SCAFFOLDING] = cs_score
        evidence[OutputDimension.COGNITIVE_SCAFFOLDING] = cs_ev

        gr_score, gr_ev = self._score_groundedness(assembled, output)
        dims[OutputDimension.GROUNDEDNESS] = gr_score
        evidence[OutputDimension.GROUNDEDNESS] = gr_ev

        rf_score, rf_ev = self._score_register_fit(assembled, output)
        dims[OutputDimension.REGISTER_FIT] = rf_score
        evidence[OutputDimension.REGISTER_FIT] = rf_ev

        for dim, score in dims.items():
            label = dim.value.replace("_", " ").title()
            if score >= 0.7:
                strengths.append(f"Strong {label}")
            elif score < 0.4:
                weaknesses.append(f"Weak {label}")

        weights = self._custom_weights or _DIMENSION_WEIGHTS
        overall = sum(s * weights.get(d, 0.0) for d, s in dims.items())
        if word_count < 20:
            overall = min(overall, 0.30)
            weaknesses.append("Output is too short to demonstrate quality")

        overall = max(0.0, min(1.0, overall))

        return OutputQualityScore(
            overall=overall,
            dimensions=dims,
            evidence=evidence,
            strengths=strengths,
            weaknesses=weaknesses,
            metadata={"mode": "heuristic", "output_words": word_count},
        )

    # -- Dimension scorers ----------------------------------------------------

    def _score_instruction_following(
        self, assembled: str, output: str
    ) -> tuple:
        lower_ctx = assembled.lower()
        lower_out = output.lower()

        # Refusal / deflection detection — must check before any other scoring
        _REFUSAL_PATTERNS = [
            r"i (can't|cannot|am unable to|don't have the ability)",
            r"as an? (ai|language model|llm)",
            r"(this (falls|is) )?(outside|beyond) (my )?(capabilities|scope|knowledge)",
            r"i (don't|do not) have access to (real.?time|current|live|up.?to.?date)",
            r"i('d| would) (recommend|suggest) (consulting|speaking with)",
            r"i need to (clarify|note) that i (cannot|can't)",
            r"i('m| am) not able to (provide|help|assist)",
            r"that('s| is) (not something|outside what) i",
        ]
        for pat in _REFUSAL_PATTERNS:
            if re.search(pat, lower_out):
                return 0.05, "Refusal or deflection detected — output did not follow instructions"

        action_verbs = re.findall(
            r"\b(analyze|review|identify|evaluate|summarize|classify|compare|"
            r"diagnose|assess|explain|generate|create|write|extract|recommend|"
            r"suggest|describe|determine|calculate|list|outline|provide|examine|"
            r"investigate|map|prioritize|design|plan|validate)\b",
            lower_ctx,
        )
        action_verbs = list(set(action_verbs))

        if not action_verbs:
            return 0.5, "No explicit action verbs detected in context"

        found = sum(1 for v in action_verbs if v in lower_out)
        ratio = found / len(action_verbs) if action_verbs else 0

        must_include = re.findall(r"must include[:\s]+([^\n]+)", lower_ctx, re.I)
        must_terms: list = []
        for mi in must_include:
            must_terms.extend([t.strip().lower() for t in mi.split(",") if t.strip()])
        must_hit = sum(1 for t in must_terms if t in lower_out) if must_terms else 0
        must_ratio = must_hit / len(must_terms) if must_terms else 1.0

        score = 0.3 + 0.4 * ratio + 0.3 * must_ratio
        ev = f"Matched {found}/{len(action_verbs)} action verbs"
        if must_terms:
            ev += f", {must_hit}/{len(must_terms)} required terms"

        # Numbered instruction coverage — check how many enumerated items are addressed
        numbered_items = re.findall(r"(?:^|\n)\s*\d+[\.\)]\s+(.+)", assembled, re.MULTILINE)
        if len(numbered_items) >= 2:
            covered = sum(
                1 for item in numbered_items
                if any(word in lower_out for word in item.lower().split() if len(word) > 4)
            )
            coverage = covered / len(numbered_items)
            ev += f" | Instruction coverage: {covered}/{len(numbered_items)} items"
            if coverage < 0.5:
                score = max(score - 0.15, 0.0)
            elif coverage >= 0.8:
                score = min(score + 0.10, 1.0)

        return max(0.0, min(1.0, score)), ev

    def _score_reasoning_depth(self, output: str) -> tuple:
        lower = output.lower()
        markers = [
            "because", "therefore", "consequently", "given that",
            "this implies", "as a result", "due to", "which means",
            "leads to", "root cause", "contributing factor", "since",
            "however", "on the other hand", "conversely", "although",
            "furthermore", "moreover", "in contrast", "nevertheless",
        ]
        found = [m for m in markers if m in lower]
        marker_count = len(found)

        numbered = len(re.findall(r"\n\s*\d+[\.\)]\s", output))
        headings = len(re.findall(r"\n#+\s", output))
        nested = len(re.findall(r"\n\s{2,}[-*]\s", output))

        # Quantified claims — specific numbers/metrics are the strongest signal of
        # concrete reasoning ("declined 23% YoY" vs "declined significantly")
        quantified = len(re.findall(
            r"\b\d+(?:\.\d+)?(?:\s*%|x|\s+(?:percent|times|fold|days?|weeks?|months?|years?|hours?))\b"
            r"|\b(?:Q[1-4]|FY|H[12])\s*\d{4}\b"
            r"|\$\s*\d",
            output, re.IGNORECASE,
        ))

        # Evidence citation — explicit "Evidence:" labels in the output signal that
        # findings are backed by data, not asserted. Counts both markdown bold
        # ("**Evidence**:") and plain bullet forms ("- Evidence:").
        evidence_citations = len(re.findall(
            r"(?:^|\n)\s*[-*]?\s*\*{0,2}evidence\*{0,2}\s*:",
            output, re.IGNORECASE | re.MULTILINE,
        ))

        depth_signals = (
            marker_count
            + numbered * 0.5
            + headings * 0.3
            + nested * 0.3
            + quantified * 0.4
            + evidence_citations * 0.5
        )
        score = min(1.0, 0.15 + depth_signals * 0.07)

        ev = f"{marker_count} reasoning markers, {numbered} numbered steps"
        if headings:
            ev += f", {headings} section headings"
        if quantified:
            ev += f", {quantified} quantified claims"
        if evidence_citations:
            ev += f", {evidence_citations} evidence citations"
        return max(0.0, min(1.0, score)), ev

    def _score_actionability(self, output: str) -> tuple:
        lower = output.lower()
        action_phrases = [
            "should", "recommend", "action", "implement", "next step",
            "solution", "mitigat", "address", "resolv", "ensur",
            "consider", "adopt", "integrat", "establish", "deploy",
            "prioritiz", "allocat", "schedul", "assign", "track",
        ]
        found = [p for p in action_phrases if p in lower]

        numbered_actions = len(re.findall(
            r"\n\s*\d+[\.\)]\s.*(?:should|recommend|implement|action)", lower
        ))
        bullet_actions = len(re.findall(
            r"\n\s*[-*]\s.*(?:should|recommend|implement|action)", lower
        ))
        specifics = len(re.findall(
            r"\d+%|\$\d|\d+ (?:days?|weeks?|hours?|months?)", lower
        ))

        score = min(
            1.0,
            0.10 + len(found) * 0.06
            + (numbered_actions + bullet_actions) * 0.08
            + specifics * 0.05,
        )
        ev = f"{len(found)} action phrases, {numbered_actions + bullet_actions} action items"
        if specifics:
            ev += f", {specifics} concrete metrics"

        # Gap-honest statements are assertive analytical conclusions, not hedges.
        # Reward outputs that explicitly flag unanswerable questions rather than
        # speculating — this is a sign of analytical rigour, not vagueness.
        _GAP_HONEST = [
            "cannot be answered", "can't be answered",
            "data is not available", "data is not provided",
            "not available in the data", "not provided in the data",
            "would need", "attribution data", "baseline is not",
            "insufficient data", "data does not include",
        ]
        gap_hits = sum(1 for g in _GAP_HONEST if g in lower)
        if gap_hits >= 1:
            score = min(score + 0.05 * min(gap_hits, 2), 1.0)
            ev += f" | Gap-honest statements: {gap_hits}"

        # Vague/hedge penalty — outputs that never commit to an answer score poorly.
        # Only penalise genuine vagueness, not gap-honest refusals (handled above).
        _OUTPUT_HEDGES = [
            "it depends", "generally speaking", "in most cases", "this varies",
            "it's hard to say", "might be worth",
            "could potentially", "there are many factors",
            "no one-size-fits-all", "varies widely",
        ]
        hedge_hits = sum(1 for h in _OUTPUT_HEDGES if h in lower)
        if hedge_hits >= 3:
            score = max(score - 0.15, 0.0)
            ev += f" | Heavy hedging ({hedge_hits} vague phrases)"
        elif hedge_hits >= 1:
            score = max(score - 0.05, 0.0)

        return max(0.0, min(1.0, score)), ev

    def _score_structure_compliance(
        self, assembled: str, output: str
    ) -> tuple:
        lower_ctx = assembled.lower()

        score = 0.4
        notes: list = []

        wants_json = any(p in lower_ctx for p in ["json", "json schema", '{"'])
        has_json = bool(re.search(r'\{[^{}]*"[a-z_]+"\s*:', output))
        if wants_json:
            score += 0.4 if has_json else -0.2
            notes.append("JSON " + ("found" if has_json else "missing"))

        wants_list = any(p in lower_ctx for p in ["bullet", "numbered list", "list of"])
        has_list = bool(re.findall(r"\n\s*[-*]\s|\n\s*\d+[\.\)]\s", output))
        if wants_list:
            score += 0.3 if has_list else -0.1
            notes.append("List " + ("found" if has_list else "missing"))

        wants_headers = any(p in lower_ctx for p in ["sections", "headings", "## "])
        has_headers = "##" in output or bool(re.findall(r"\n[A-Z][A-Za-z ]+:\n", output))
        if wants_headers:
            score += 0.3 if has_headers else -0.1
            notes.append("Headers " + ("found" if has_headers else "missing"))

        if not wants_json and not wants_list and not wants_headers:
            if has_headers and has_list:
                score += 0.35
                notes.append("Well-structured output")
            elif has_headers or has_list:
                score += 0.20
                notes.append("Some structure present")

        ev = "; ".join(notes) if notes else "Default structure assessment"
        return max(0.0, min(1.0, score)), ev

    def _score_cognitive_scaffolding(
        self, assembled: str, output: str
    ) -> tuple:
        lower_ctx = assembled.lower()
        lower_out = output.lower()

        framework_terms = {
            "root cause": ["root cause", "underlying cause", "primary cause"],
            "decision matrix": ["decision matrix", "weighted criteria", "scoring matrix"],
            "swot": ["strength", "weakness", "opportunity", "threat"],
            "pros and cons": ["advantage", "disadvantage", "pro", "con"],
            "hypothesis": ["hypothesis", "null hypothesis", "test"],
            "stakeholder": ["stakeholder", "impact analysis", "affected party"],
            "causal": ["causal", "cause and effect", "chain of causation"],
            "temporal": ["timeline", "temporal", "sequence of events", "chronolog"],
            "diagnostic": ["symptom", "diagnosis", "differential", "prognosis"],
            "feedback loop": ["feedback loop", "reinforcing", "balancing", "loop"],
            "leverage point": ["leverage point", "intervention", "high-impact"],
            "trade-off": ["trade-off", "tension", "balance between"],
            "risk": ["risk", "mitigation", "probability", "impact"],
            "gap analysis": ["current state", "desired state", "gap", "bridge"],
        }

        ctx_frameworks: list = []
        for name, keywords in framework_terms.items():
            if any(kw in lower_ctx for kw in keywords):
                ctx_frameworks.append(name)

        if not ctx_frameworks:
            words = len(output.split())
            base = 0.5 if words > 100 else 0.3
            return base, "No specific cognitive framework detected in context"

        used = 0
        for fw in ctx_frameworks:
            keywords = framework_terms[fw]
            if any(kw in lower_out for kw in keywords):
                used += 1

        ratio = used / len(ctx_frameworks)
        score = 0.20 + 0.80 * ratio
        ev = f"Output uses {used}/{len(ctx_frameworks)} cognitive frameworks from context"
        return max(0.0, min(1.0, score)), ev

    def _score_groundedness(
        self, assembled: str, output: str
    ) -> tuple:
        """How well does the output stay within the provided context/material?"""
        lower_out = output.lower()
        lower_ctx = assembled.lower()

        score = 0.50
        notes: list[str] = []

        grounding_markers = [
            "according to", "based on the", "the provided", "from the context",
            "the data shows", "the material", "as stated", "per the",
            "source material", "the packet", "[not in packet]",
            "not found in the provided", "not available in the",
        ]
        marker_hits = sum(1 for m in grounding_markers if m in lower_out)
        if marker_hits >= 3:
            score += 0.25
            notes.append(f"{marker_hits} grounding markers")
        elif marker_hits >= 1:
            score += 0.15
            notes.append(f"{marker_hits} grounding markers")

        hedge_inventions = [
            "it is widely known", "experts agree that",
            "studies have shown", "research suggests",
            "it is common knowledge", "as we all know",
            "it goes without saying",
        ]
        ctx_allows = any(p in lower_ctx for p in [
            "widely known", "experts agree", "studies have shown",
            "research suggests", "common knowledge",
        ])
        if not ctx_allows:
            invention_hits = sum(1 for h in hedge_inventions if h in lower_out)
            if invention_hits >= 2:
                score -= 0.20
                notes.append(f"{invention_hits} unsourced authority claims")
            elif invention_hits >= 1:
                score -= 0.10
                notes.append(f"{invention_hits} unsourced authority claim")

        has_grounding_instruction = any(
            p in lower_ctx for p in [
                "only use", "do not invent", "stay within",
                "not in packet", "grounding", "factual",
                "do not fabricate", "source material only",
            ]
        )
        if has_grounding_instruction:
            score += 0.10
            notes.append("Context includes grounding instructions")

        ev = "; ".join(notes) if notes else "Default groundedness assessment"
        return max(0.0, min(1.0, score)), ev

    def _score_register_fit(
        self, assembled: str, output: str
    ) -> tuple:
        """Does the output's register/tone match the context's declared audience and genre?"""
        lower_ctx = assembled.lower()
        lower_out = output.lower()

        score = 0.50
        notes: list[str] = []

        _AI_BOILERPLATE = [
            "in today's rapidly evolving", "in today's fast-paced",
            "let's dive in", "without further ado",
            "game-changer", "game changer", "cutting-edge",
            "leverage the power", "unlock the full potential",
            "embark on a journey", "navigate the complexities",
            "delve into", "in the realm of", "tapestry of",
            "it's no wonder that", "ever-evolving", "ever-changing",
            "paramount importance", "of a lifetime",
        ]
        boilerplate_hits = sum(1 for bp in _AI_BOILERPLATE if bp in lower_out)
        if boilerplate_hits >= 4:
            score -= 0.30
            notes.append(f"{boilerplate_hits} AI boilerplate phrases — heavy generic tone")
        elif boilerplate_hits >= 2:
            score -= 0.15
            notes.append(f"{boilerplate_hits} AI boilerplate phrases")
        elif boilerplate_hits == 0:
            score += 0.15
            notes.append("No AI boilerplate detected")

        is_technical = any(p in lower_ctx for p in [
            "technical", "engineer", "developer", "staff", "senior",
            "internal brief", "incident", "architecture",
        ])
        is_casual = any(p in lower_ctx for p in [
            "blog", "traveler", "tourist", "visitor", "general public",
            "casual", "approachable",
        ])

        if is_technical:
            casual_markers = sum(1 for m in [
                "exciting", "amazing", "wonderful", "fantastic",
                "awesome", "incredible", "stunning",
            ] if m in lower_out)
            if casual_markers >= 3:
                score -= 0.15
                notes.append("Casual superlatives in a technical context")
            else:
                score += 0.10
                notes.append("Tone consistent with technical context")

        if is_casual:
            jargon_markers = sum(1 for m in [
                "pursuant to", "heretofore", "aforementioned",
                "notwithstanding", "whereby", "therein",
            ] if m in lower_out)
            if jargon_markers >= 2:
                score -= 0.15
                notes.append("Formal jargon in a casual context")
            else:
                score += 0.10
                notes.append("Tone consistent with casual/blog context")

        ev = "; ".join(notes) if notes else "Default register assessment"
        return max(0.0, min(1.0, score)), ev

    # -- LLM evaluation -------------------------------------------------------

    def _evaluate_llm(
        self, context: Context, output: str, **kwargs: Any
    ) -> OutputQualityScore:
        import json

        assembled = context.assemble()
        user_task = kwargs.pop("user_task", None) or ""

        prompt = f"""You are an expert evaluator of LLM outputs. Score this output against the context that produced it.

CALIBRATION — be strict and differentiate:
  0.0–0.2  Broken / off-topic / refusal
  0.2–0.4  Superficial or mostly misses the ask
  0.4–0.6  Adequate but generic; a competent baseline would do this
  0.6–0.8  Good — follows instructions, adds depth, concrete details
  0.8–0.9  Very good — tight, specific, well-grounded, uses frameworks
  0.9–1.0  Exceptional — publishable quality, no wasted words

IMPORTANT: Outputs that are structurally similar but differ in depth, specificity, or grounding MUST receive DIFFERENT scores. Identical scores across arms indicate a failed evaluation.

<system_context>
{assembled[:6000]}
</system_context>

{f"<user_task>{chr(10)}{user_task[:2000]}{chr(10)}</user_task>" if user_task else ""}

<output>
{output[:10000]}
</output>

Rate on 7 dimensions (0.0–1.0):

1. **instruction_following** — Did it follow every directive, rule, and constraint from the system context? Count missed instructions.
   - 0.3 = ignores most instructions; 0.6 = follows major ones, misses details; 0.9 = follows all

2. **reasoning_depth** — Multi-step analysis, not surface-level summaries? Uses causal language, quantified claims, explicit tradeoffs?
   - 0.3 = surface restatement; 0.6 = some analysis with "because/therefore"; 0.9 = deep chains with evidence

3. **actionability** — Concrete, implementable next steps with owners/timelines/metrics, not vague advice?
   - 0.3 = "consider improving"; 0.6 = some specific actions; 0.9 = every recommendation has who/what/when

4. **structure_compliance** — Matches requested format (sections, headings, JSON, lists) exactly?
   - 0.3 = ignores format; 0.6 = roughly right; 0.9 = exact match

5. **cognitive_scaffolding** — Uses the analytical framework from the context (root cause, SWOT, decision matrix, etc.)?
   - 0.3 = ignores framework; 0.6 = mentions it; 0.9 = framework drives the analysis

6. **groundedness** — Every factual claim traced to provided context? No invented statistics, vendors, or studies?
   - 0.3 = invents freely; 0.6 = mostly grounded with a few unsourced claims; 0.9 = every claim traceable

7. **register_fit** — Tone, vocabulary, and diction match the declared audience/genre? Free of AI boilerplate?
   - 0.3 = generic AI tone, boilerplate-heavy; 0.6 = mostly appropriate; 0.9 = reads like a domain expert wrote it

Output ONLY valid JSON:
{{"instruction_following": 0.0, "reasoning_depth": 0.0, "actionability": 0.0, "structure_compliance": 0.0, "cognitive_scaffolding": 0.0, "groundedness": 0.0, "register_fit": 0.0, "evidence": {{"instruction_following": "...", "reasoning_depth": "...", "actionability": "...", "structure_compliance": "...", "cognitive_scaffolding": "...", "groundedness": "...", "register_fit": "..."}}, "strengths": ["..."], "weaknesses": ["..."]}}"""

        api_key = kwargs.pop("api_key", None)
        eval_ctx = Context(
            guidance=(
                "You are a strict, honest output quality evaluator. "
                "Differentiate between outputs — never give identical scores to different texts. "
                "Output ONLY valid JSON."
            ),
            directive=prompt,
        )

        def _parse_llm_response(text: str) -> OutputQualityScore:
            if text.startswith("```"):
                lines = text.split("\n")
                text = "\n".join(lines[1:-1]) if len(lines) > 2 else text
                text = text.replace("```json", "").replace("```", "").strip()
            data = json.loads(text)
            dims = {
                OutputDimension.INSTRUCTION_FOLLOWING: float(data["instruction_following"]),
                OutputDimension.REASONING_DEPTH: float(data["reasoning_depth"]),
                OutputDimension.ACTIONABILITY: float(data["actionability"]),
                OutputDimension.STRUCTURE_COMPLIANCE: float(data["structure_compliance"]),
                OutputDimension.COGNITIVE_SCAFFOLDING: float(data["cognitive_scaffolding"]),
                OutputDimension.GROUNDEDNESS: float(data.get("groundedness", 0.5)),
                OutputDimension.REGISTER_FIT: float(data.get("register_fit", 0.5)),
            }
            ev_data = data.get("evidence", {})
            evidence = {d: ev_data.get(d.value, "") for d in OutputDimension}
            weights = self._custom_weights or _DIMENSION_WEIGHTS
            overall = sum(s * weights.get(d, 0.0) for d, s in dims.items())
            return OutputQualityScore(
                overall=max(0.0, min(1.0, overall)),
                dimensions=dims,
                evidence=evidence,
                strengths=data.get("strengths", []),
                weaknesses=data.get("weaknesses", []),
            )

        def _call_judge() -> str:
            resp = eval_ctx.execute(
                provider=self.provider,
                model=self.model,
                temperature=0.2,
                api_key=api_key,
            )
            return resp.response.strip()

        try:
            score = _parse_llm_response(_call_judge())
            score.metadata = {"mode": "llm", "model": self.model, "provider": self.provider}
            return score
        except Exception as first_err:
            import time as _time

            _time.sleep(2)
            try:
                score = _parse_llm_response(_call_judge())
                score.metadata = {
                    "mode": "llm_retry",
                    "model": self.model,
                    "provider": self.provider,
                    "first_error": str(first_err),
                }
                return score
            except Exception as retry_err:
                result = self._evaluate_heuristic(context, output)
                result.metadata["llm_error"] = str(retry_err)
                result.metadata["llm_first_error"] = str(first_err)
                result.metadata["mode"] = "heuristic_fallback"
                return result

    def _evaluate_hybrid(
        self, context: Context, output: str, **kwargs: Any
    ) -> OutputQualityScore:
        heuristic = self._evaluate_heuristic(context, output)
        if heuristic.overall > 0.75 or heuristic.overall < 0.35:
            heuristic.metadata["mode"] = "hybrid_fast"
            return heuristic
        llm_result = self._evaluate_llm(context, output, **kwargs)
        llm_result.metadata["mode"] = "hybrid_llm"
        llm_result.metadata["heuristic_overall"] = heuristic.overall
        return llm_result

    # -- Report ---------------------------------------------------------------

    def report(self, score: OutputQualityScore) -> str:
        lines = [
            "Output Quality Report",
            "=" * 21,
            "",
            f"Overall: {score.overall:.1%}",
            "",
            "Dimensions:",
        ]
        for dim in OutputDimension:
            s = score.dimensions.get(dim, 0)
            icon = "+" if s >= 0.7 else "~" if s >= 0.4 else "-"
            label = dim.value.replace("_", " ").title()
            ev = score.evidence.get(dim, "")
            lines.append(f"  [{icon}] {label}: {s:.1%}  ({ev})")
        if score.strengths:
            lines.append("")
            lines.append("Strengths:")
            for s in score.strengths:
                lines.append(f"  + {s}")
        if score.weaknesses:
            lines.append("")
            lines.append("Weaknesses:")
            for w in score.weaknesses:
                lines.append(f"  - {w}")
        return "\n".join(lines)
