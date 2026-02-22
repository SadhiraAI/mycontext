"""
Output Evaluator - Measure LLM output quality against its context

Evaluates the *output* of an LLM (not the prompt), scoring how well the
response leverages the cognitive scaffolding provided by the context.

Five dimensions (distinct from QualityMetrics' prompt-level dimensions):
  - Instruction Following
  - Reasoning Depth
  - Actionability
  - Structure Compliance
  - Cognitive Scaffolding
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


@dataclass
class OutputQualityScore:
    overall: float
    dimensions: dict[OutputDimension, float]
    evidence: dict[OutputDimension, str]
    strengths: list[str]
    weaknesses: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


_DIMENSION_WEIGHTS = {
    OutputDimension.INSTRUCTION_FOLLOWING: 0.25,
    OutputDimension.REASONING_DEPTH: 0.20,
    OutputDimension.ACTIONABILITY: 0.20,
    OutputDimension.STRUCTURE_COMPLIANCE: 0.15,
    OutputDimension.COGNITIVE_SCAFFOLDING: 0.20,
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
    ):
        self.mode = mode
        self.provider = provider
        self.model = model

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

        for dim, score in dims.items():
            label = dim.value.replace("_", " ").title()
            if score >= 0.7:
                strengths.append(f"Strong {label}")
            elif score < 0.4:
                weaknesses.append(f"Weak {label}")

        overall = sum(s * _DIMENSION_WEIGHTS[d] for d, s in dims.items())
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

        depth_signals = marker_count + numbered * 0.5 + headings * 0.3 + nested * 0.3
        score = min(1.0, 0.15 + depth_signals * 0.07)

        ev = f"{marker_count} reasoning markers, {numbered} numbered steps"
        if headings:
            ev += f", {headings} section headings"
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

    # -- LLM evaluation -------------------------------------------------------

    def _evaluate_llm(
        self, context: Context, output: str, **kwargs: Any
    ) -> OutputQualityScore:
        import json

        assembled = context.assemble()
        prompt = (
            "You are an expert evaluator of LLM outputs. Score this output "
            "against the context that produced it.\n\n"
            "Be STRICT. Most outputs score 0.4-0.7. Only exceptional outputs "
            "score above 0.85.\n\n"
            f"<context>\n{assembled[:4000]}\n</context>\n\n"
            f"<output>\n{output[:8000]}\n</output>\n\n"
            "Rate on 5 dimensions (0.0-1.0):\n"
            "1. **instruction_following** -- Did it follow directive/rules/constraints?\n"
            "2. **reasoning_depth** -- Multi-step reasoning, not surface answers?\n"
            "3. **actionability** -- Concrete, implementable recommendations?\n"
            "4. **structure_compliance** -- Matches requested format?\n"
            "5. **cognitive_scaffolding** -- Uses the cognitive framework from the template?\n\n"
            "Output ONLY valid JSON:\n"
            '{"instruction_following": 0.0, "reasoning_depth": 0.0, '
            '"actionability": 0.0, "structure_compliance": 0.0, '
            '"cognitive_scaffolding": 0.0, '
            '"evidence": {"instruction_following": "...", "reasoning_depth": "...", '
            '"actionability": "...", "structure_compliance": "...", '
            '"cognitive_scaffolding": "..."}, '
            '"strengths": ["..."], "weaknesses": ["..."]}'
        )

        try:
            api_key = kwargs.pop("api_key", None)
            eval_ctx = Context(
                guidance="You are a strict, honest output quality evaluator. Output ONLY valid JSON.",
                directive=prompt,
            )
            response = eval_ctx.execute(
                provider=self.provider,
                model=self.model,
                temperature=0.2,
                api_key=api_key,
            )
            text = response.response.strip()
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
            }
            ev_data = data.get("evidence", {})
            evidence = {
                OutputDimension.INSTRUCTION_FOLLOWING: ev_data.get("instruction_following", ""),
                OutputDimension.REASONING_DEPTH: ev_data.get("reasoning_depth", ""),
                OutputDimension.ACTIONABILITY: ev_data.get("actionability", ""),
                OutputDimension.STRUCTURE_COMPLIANCE: ev_data.get("structure_compliance", ""),
                OutputDimension.COGNITIVE_SCAFFOLDING: ev_data.get("cognitive_scaffolding", ""),
            }
            overall = sum(s * _DIMENSION_WEIGHTS[d] for d, s in dims.items())
            return OutputQualityScore(
                overall=max(0.0, min(1.0, overall)),
                dimensions=dims,
                evidence=evidence,
                strengths=data.get("strengths", []),
                weaknesses=data.get("weaknesses", []),
                metadata={"mode": "llm", "model": self.model, "provider": self.provider},
            )
        except Exception as e:
            result = self._evaluate_heuristic(context, output)
            result.metadata["llm_error"] = str(e)
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
