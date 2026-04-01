"""
Context Amplification Index (CAI) - Measure the lift cognitive templates provide

Compares LLM output quality when using a raw prompt vs. a template-built
context.  CAI > 1.0 means the template amplified output quality.

    CAI = templated_score / raw_score   (per dimension and overall)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..core import Context
from .output_evaluator import OutputDimension, OutputEvaluator, OutputQualityScore


@dataclass
class CAIResult:
    question: str
    template_name: str
    raw_output: str
    templated_output: str
    raw_score: OutputQualityScore
    templated_score: OutputQualityScore
    cai_overall: float
    cai_dimensions: dict[OutputDimension, float]
    verdict: str
    metadata: dict[str, Any] = field(default_factory=dict)


def _verdict(cai: float) -> str:
    if cai >= 1.5:
        return "significant lift"
    if cai >= 1.2:
        return "moderate lift"
    if cai >= 1.05:
        return "slight lift"
    if cai >= 0.95:
        return "neutral"
    return "negative lift"


class ContextAmplificationIndex:
    """
    Measure how much a cognitive template amplifies LLM output quality
    compared to a raw, unstructured prompt.

    Example::

        >>> from mycontext.intelligence.context_amplification import ContextAmplificationIndex
        >>> cai = ContextAmplificationIndex(provider="openai")
        >>> result = cai.measure(
        ...     question="Why are API response times 3x slower after deploy?",
        ...     template_name="diagnostic_root_cause_analyzer",
        ...     api_key="sk-...",
        ... )
        >>> print(f"CAI: {result.cai_overall:.2f}x  ({result.verdict})")
    """

    def __init__(
        self,
        provider: str = "openai",
        eval_mode: str = "heuristic",
        model: str | None = None,
    ):
        self.provider = provider
        self.eval_mode = eval_mode
        self.model = model
        self._evaluator = OutputEvaluator(mode=eval_mode, provider=provider)

    def measure(
        self,
        question: str,
        template_name: str,
        **kwargs: Any,
    ) -> CAIResult:
        """Run the same question raw vs. template-built, compare output quality.

        Always executes the LLM twice: once with the raw question, once with
        the template-assembled context. Then scores both responses.
        eval_mode controls only HOW the scoring is done (heuristic vs LLM).
        """
        api_key = kwargs.pop("api_key", None)
        exec_model = kwargs.pop("model", self.model)

        exec_kwargs: dict[str, Any] = {}
        if api_key:
            exec_kwargs["api_key"] = api_key
        if exec_model:
            exec_kwargs["model"] = exec_model

        raw_output = self._execute_raw(question, **exec_kwargs)
        templated_output = self._execute_template(question, template_name, **exec_kwargs)

        raw_ctx = Context(directive=question)
        templated_ctx = self._build_template_context(question, template_name)

        eval_kw: dict[str, Any] = {}
        if api_key:
            eval_kw["api_key"] = api_key

        raw_score = self._evaluator.evaluate(raw_ctx, raw_output, **eval_kw)
        templated_score = self._evaluator.evaluate(
            templated_ctx or raw_ctx, templated_output, **eval_kw
        )

        cai_dims = {}
        for dim in OutputDimension:
            raw_val = raw_score.dimensions.get(dim, 0.01)
            tmpl_val = templated_score.dimensions.get(dim, 0.0)
            cai_dims[dim] = tmpl_val / max(raw_val, 0.01)

        cai_overall = templated_score.overall / max(raw_score.overall, 0.01)

        return CAIResult(
            question=question,
            template_name=template_name,
            raw_output=raw_output,
            templated_output=templated_output,
            raw_score=raw_score,
            templated_score=templated_score,
            cai_overall=round(cai_overall, 3),
            cai_dimensions={d: round(v, 3) for d, v in cai_dims.items()},
            verdict=_verdict(cai_overall),
            metadata={"provider": self.provider, "eval_mode": self.eval_mode},
        )

    def measure_chain(
        self,
        question: str,
        chain: list[str],
        **kwargs: Any,
    ) -> CAIResult:
        """Compare single best template vs. integrated chain of templates."""
        if not chain:
            raise ValueError("chain must contain at least one template name")

        api_key = kwargs.pop("api_key", None)
        exec_model = kwargs.pop("model", self.model)
        exec_kwargs: dict[str, Any] = {}
        if api_key:
            exec_kwargs["api_key"] = api_key
        if exec_model:
            exec_kwargs["model"] = exec_model

        single_name = chain[0]
        single_output = self._execute_template(question, single_name, **exec_kwargs)
        single_ctx = self._build_template_context(question, single_name) or Context(
            directive=question
        )

        chain_output = self._execute_chain(question, chain, **exec_kwargs)
        chain_ctx = Context(
            guidance="Integrated chain of " + str(len(chain)) + " cognitive templates",
            directive=question,
        )

        eval_kw: dict[str, Any] = {}
        if api_key:
            eval_kw["api_key"] = api_key

        single_score = self._evaluator.evaluate(single_ctx, single_output, **eval_kw)
        chain_score = self._evaluator.evaluate(chain_ctx, chain_output, **eval_kw)

        cai_dims = {}
        for dim in OutputDimension:
            s_val = single_score.dimensions.get(dim, 0.01)
            c_val = chain_score.dimensions.get(dim, 0.0)
            cai_dims[dim] = c_val / max(s_val, 0.01)

        cai_overall = chain_score.overall / max(single_score.overall, 0.01)
        chain_label = "+".join(chain)

        return CAIResult(
            question=question,
            template_name="chain[" + chain_label + "]",
            raw_output=single_output,
            templated_output=chain_output,
            raw_score=single_score,
            templated_score=chain_score,
            cai_overall=round(cai_overall, 3),
            cai_dimensions={d: round(v, 3) for d, v in cai_dims.items()},
            verdict=_verdict(cai_overall),
            metadata={
                "provider": self.provider,
                "eval_mode": self.eval_mode,
                "comparison": "chain_vs_single",
                "chain": chain,
                "single": single_name,
            },
        )

    def _execute_raw(self, question, **kwargs):
        ctx = Context(directive=question)
        try:
            result = ctx.execute(provider=self.provider, **kwargs)
            return result.response if hasattr(result, "response") else str(result)
        except Exception as e:
            return "[execution error: " + str(e) + "]"

    def _execute_template(self, question, template_name, **kwargs):
        ctx = self._build_template_context(question, template_name)
        if not ctx:
            return self._execute_raw(question, **kwargs)
        try:
            result = ctx.execute(provider=self.provider, **kwargs)
            return result.response if hasattr(result, "response") else str(result)
        except Exception as e:
            return "[execution error: " + str(e) + "]"

    def _execute_chain(self, question, chain, **kwargs):
        try:
            from .template_integrator_agent import TemplateIntegratorAgent

            agent = TemplateIntegratorAgent(include_enterprise=True)
            result = agent.integrate(
                question=question,
                template_names=chain,
                provider=self.provider,
                **kwargs,
            )
            return result.integrated_context
        except Exception:
            return self._execute_template(question, chain[0], **kwargs)

    def _build_template_context(self, question, template_name):
        try:
            from .chain_orchestration_agent import PATTERN_BUILD_CONTEXT_REGISTRY
            from .pattern_suggester import get_pattern_class

            klass = get_pattern_class(template_name, include_enterprise=True)
            if not klass:
                return None
            reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(template_name, ("problem", {}))
            primary, defaults = reg
            params = dict(defaults)
            params[primary] = question
            return klass().build_context(**params)
        except Exception:
            return None

    def report(self, result):
        lines = [
            "Context Amplification Index (CAI) Report",
            "=" * 41,
            "",
            "Question: " + result.question[:80] + "...",
            "Template: " + result.template_name,
            "CAI Overall: " + str(round(result.cai_overall, 2)) + "x  (" + result.verdict + ")",
            "",
            "Per-Dimension CAI:",
        ]
        for dim in OutputDimension:
            val = result.cai_dimensions.get(dim, 0)
            label = dim.value.replace("_", " ").title()
            raw = result.raw_score.dimensions.get(dim, 0)
            tmpl = result.templated_score.dimensions.get(dim, 0)
            lines.append(
                "  "
                + label
                + ": "
                + str(round(val, 2))
                + "x  (raw="
                + str(round(raw * 100, 1))
                + "% -> templated="
                + str(round(tmpl * 100, 1))
                + "%)"
            )
        lines.append("")
        lines.append("Raw Overall:      " + str(round(result.raw_score.overall * 100, 1)) + "%")
        lines.append(
            "Templated Overall: " + str(round(result.templated_score.overall * 100, 1)) + "%"
        )
        return "\n".join(lines)
