"""
Template Integrator Agent - The Best of All Worlds

Intelligently merges multiple cognitive templates into a single unified
context, combining the strongest methodologies from each into one cohesive
reasoning framework tailored to a specific question.

Research Foundation:
- DSPy: Compiling Declarative LM Calls (arxiv 2310.03714)
- Agentic Context Engineering (arxiv 2510.04618)
"""

from dataclasses import dataclass, field

from ..intelligence.pattern_catalog import NAME_TO_DESCRIPTION
from ..intelligence.pattern_suggester import (
    ENTERPRISE_LICENSE_NOTE,
    NAME_TO_CATEGORY,
    VALID_PATTERN_NAMES,
)


@dataclass
class IntegrationResult:
    """Result of template integration."""

    question: str
    source_templates: list[str]
    integrated_context: str
    role: str = ""
    rules: list[str] = field(default_factory=list)
    directive: str = ""
    output_requirements: list[str] = field(default_factory=list)
    raw_llm_response: str = ""

    def to_context(self):
        """Convert to a mycontext Context object for direct execution."""
        from ..core import Context
        from ..foundation import Constraints, Directive, Guidance

        gkw = {}
        if self.role:
            gkw["role"] = self.role
        if self.rules:
            gkw["rules"] = self.rules

        return Context(
            guidance=Guidance(**gkw) if gkw else None,
            directive=Directive(
                content=self.directive or self.integrated_context
            ),
            constraints=Constraints(
                must_include=self.output_requirements
            ) if self.output_requirements else None,
            data={
                "integration_metadata": {
                    "source_templates": self.source_templates,
                    "question": self.question,
                    "agent": "TemplateIntegratorAgent",
                }
            },
        )


INTEGRATION_PROMPT_TEMPLATE = (
    'You are the Template Integrator Agent.\n\n'
    'USER QUESTION: "{question}"\n\n'
    'SELECTED TEMPLATES AND THEIR CAPABILITIES:\n{summaries}\n\n'
    'YOUR PRIMARY GOAL: Create a context that will produce a COMPLETE, '
    'HIGH-QUALITY answer to the user\'s question.\n\n'
    'IMPORTANT CONSTRAINTS:\n'
    '- Draw the BEST techniques from each template. You do NOT need to '
    'include every section from every template.\n'
    '- The output framework MUST be completable in a single LLM response. '
    'Aim for 5-7 output sections maximum, not 10+.\n'
    '- Every output section must directly address an aspect of the user\'s '
    'question. Remove any section that doesn\'t serve the answer.\n'
    '- Prioritize ANSWERING THE QUESTION over methodological completeness.\n\n'
    'Respond in this EXACT format:\n\n'
    'ROLE: [A combined expert role relevant to the user\'s question]\n\n'
    'RULES:\n'
    '- [Key analytical rule, max 6 rules]\n\n'
    'DIRECTIVE:\n'
    '[Step-by-step instructions that guide the LLM to answer the user\'s '
    'question thoroughly. Incorporate the best techniques from the selected '
    'templates but stay focused on the question.]\n\n'
    'OUTPUT MUST INCLUDE:\n'
    '- [Section that addresses aspect 1 of the question]\n'
    '- [Section that addresses aspect 2 of the question]\n'
    '- [5-7 sections max, each tied to a question aspect]\n'
    '- ALWAYS end with a concrete Recommendations / Next Steps section\n\n'
    'CONCISENESS: The final LLM output should be 3,500-4,500 characters. '
    'Be thorough but concise — depth over breadth.'
)


class TemplateIntegratorAgent:
    """
    The Best of All Worlds - merges multiple cognitive templates into one.

    Given a user question and a set of template names, the agent:
    1. Gathers what each template brings (methodology, structure, focus)
    2. Asks the LLM to fuse them into a single integrated context
    3. Returns a structured IntegrationResult that can be used directly

    Enterprise gating: non-enterprise users cannot integrate enterprise
    templates unless include_enterprise=True.

    Usage (SDK):
        >>> agent = TemplateIntegratorAgent()
        >>> result = agent.integrate(
        ...     question="Should we migrate to microservices?",
        ...     template_names=["decision_framework", "risk_assessor"],
        ...     provider="openai",
        ... )
        >>> ctx = result.to_context()
        >>> ctx.execute(provider="openai")

    All-in-one (suggest + integrate):
        >>> result = agent.suggest_and_integrate(
        ...     question="Why did churn spike?",
        ...     provider="openai",
        ... )
    """

    TAGLINE = "The Best of All Worlds"

    def __init__(self, include_enterprise=True):
        self.include_enterprise = include_enterprise

    # ------------------------------------------------------------------ #
    #  Public API                                                         #
    # ------------------------------------------------------------------ #

    def integrate(
        self,
        question,
        template_names,
        provider="openai",
        selection_reasoning=None,
        temperature=0.2,
        model=None,
        **kwargs,
    ):
        """Merge multiple templates into one unified context."""
        self._validate(template_names)
        selection_reasoning = selection_reasoning or {}
        summaries = self._build_summaries(template_names, selection_reasoning)
        prompt = INTEGRATION_PROMPT_TEMPLATE.format(
            question=question, summaries=summaries
        )
        raw = self._call_llm(prompt, provider, temperature, model, **kwargs)
        return self._parse_result(question, template_names, raw)

    def suggest_and_integrate(
        self,
        question,
        provider="openai",
        max_patterns=3,
        mode="hybrid",
        integration_mode="focused",
        **kwargs,
    ):
        """All-in-one: suggest the best templates AND integrate them.

        Args:
            question: User's question
            provider: LLM provider
            max_patterns: Max templates to integrate (default 3, was 5)
            mode: Suggestion mode ("keyword", "llm", "hybrid")
            integration_mode: "focused" (2-3 templates, surgical) or
                              "full" (up to max_patterns, comprehensive)
            **kwargs: Extra kwargs passed to LLM
        """
        from .pattern_suggester import suggest_patterns

        effective_max = min(max_patterns, 2) if integration_mode == "focused" else max_patterns

        result = suggest_patterns(
            question,
            include_enterprise=self.include_enterprise,
            suggest_chain=True,
            max_patterns=effective_max,
            mode=mode,
            llm_provider=provider,
            **kwargs,
        )
        names = (
            result.suggested_chain
            or [s.name for s in result.suggested_patterns]
        )
        reasoning = {s.name: s.reason for s in result.suggested_patterns}
        return self.integrate(
            question=question,
            template_names=names,
            provider=provider,
            selection_reasoning=reasoning,
            **kwargs,
        )

    def suggest_and_compile(
        self,
        question,
        provider="openai",
        max_patterns=3,
        mode="hybrid",
        refine=True,
        **kwargs,
    ):
        """All-in-one: suggest templates and compile them into a composed prompt.

        Instead of integrating template frameworks into a single context
        (which competes for output tokens), this method generates a compact
        prompt from each template and composes them into one comprehensive
        prompt via :class:`PromptComposer`.

        Args:
            question: User's question
            provider: LLM provider
            max_patterns: Max templates to compose (default 3)
            mode: Suggestion mode ("keyword", "llm", "hybrid")
            refine: Whether to LLM-refine individual prompts
            **kwargs: Extra kwargs passed to LLM

        Returns:
            ComposedPrompt that can be executed or exported as a string.
        """
        from .pattern_suggester import suggest_patterns
        from .prompt_composer import PromptComposer

        result = suggest_patterns(
            question,
            include_enterprise=self.include_enterprise,
            suggest_chain=True,
            max_patterns=max_patterns,
            mode=mode,
            llm_provider=provider,
            **kwargs,
        )
        names = (
            result.suggested_chain
            or [s.name for s in result.suggested_patterns]
        )

        composer = PromptComposer(
            include_enterprise=self.include_enterprise,
            provider=provider,
        )
        return composer.compose_from_templates(
            question=question,
            template_names=names,
            refine=refine,
            provider=provider,
            **kwargs,
        )

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                   #
    # ------------------------------------------------------------------ #

    def _validate(self, template_names):
        invalid = [t for t in template_names if t not in VALID_PATTERN_NAMES]
        if invalid:
            raise ValueError("Unknown template(s): " + str(invalid))

        if not self.include_enterprise:
            ent = [
                t for t in template_names
                if NAME_TO_CATEGORY.get(t) == "enterprise"
            ]
            if ent:
                raise ValueError(
                    "Enterprise license required for: " + str(ent)
                    + ". " + ENTERPRISE_LICENSE_NOTE.strip()
                )

    def _build_summaries(self, names, reasoning):
        from .pattern_catalog import ENRICHED_CATALOG
        lines = []
        for name in names:
            cat = NAME_TO_CATEGORY.get(name, "free")
            desc = NAME_TO_DESCRIPTION.get(name, name)
            why = reasoning.get(name, "")
            enrichment = ENRICHED_CATALOG.get(name, {})

            line = f"### {name} [{cat}]: {desc}"
            if why:
                line += f"\n  Why chosen: {why}"

            # Extract actual template content so the integrator knows what each template does
            template_detail = self._get_template_detail(name)
            if template_detail:
                line += f"\n  {template_detail}"

            wtu = enrichment.get("when_to_use", "")
            if wtu:
                line += f"\n  Best for: {wtu}"

            lines.append(line)
        return "\n\n".join(lines)

    @staticmethod
    def _get_template_detail(name):
        """Extract role, key rules, and directive structure from an actual template."""
        try:
            from .chain_orchestration_agent import PATTERN_BUILD_CONTEXT_REGISTRY
            from .pattern_suggester import get_pattern_class
            klass = get_pattern_class(name, include_enterprise=True)
            if not klass:
                return ""
            reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(name, ("input", {}))
            primary_key, defaults = reg
            params = dict(defaults)
            params[primary_key] = "PLACEHOLDER"
            ctx = klass().build_context(**params)
            parts = []
            if hasattr(ctx, 'guidance') and ctx.guidance:
                g = ctx.guidance
                if hasattr(g, 'role') and g.role:
                    parts.append(f"Role: {g.role[:120]}")
                if hasattr(g, 'rules') and g.rules:
                    top_rules = g.rules[:3]
                    parts.append("Key rules: " + "; ".join(
                        r[:80] for r in top_rules
                    ))
            if hasattr(ctx, 'directive') and ctx.directive:
                d = ctx.directive
                content = d.content if hasattr(d, 'content') else str(d)
                sections = [
                    line.strip() for line in content.split('\n')
                    if line.strip().startswith(('#', '##', '1.', '2.', '3.', '- **'))
                ][:5]
                if sections:
                    parts.append("Directive sections: " + " | ".join(
                        s.lstrip('#- *').strip()[:60] for s in sections
                    ))
            return " | ".join(parts)[:500] if parts else ""
        except Exception:
            return ""

    def _call_llm(self, prompt, provider, temperature, model, **kwargs):
        from ..core import Context
        from ..foundation import Directive, Guidance

        ctx = Context(
            guidance=Guidance(
                role=(
                    "Template Integrator Agent -- expert at fusing "
                    "multiple cognitive reasoning frameworks into one "
                    "unified, powerful context"
                ),
                rules=[
                    "Merge methodologies, do not just concatenate them.",
                    "Every element must be specific to the user question.",
                    "The result must be directly usable as an LLM prompt.",
                ],
            ),
            directive=Directive(content=prompt),
        )
        exec_kw = {"temperature": temperature}
        exec_kw.update(kwargs)
        if model:
            exec_kw["model"] = model
        result = ctx.execute(provider=provider, **exec_kw)
        return result.response.strip()

    def _parse_result(self, question, names, raw):
        import re

        role = ""
        rules = []
        directive = ""
        output_reqs = []

        role_m = re.search(r"ROLE:\s*(.+)", raw)
        if role_m:
            role = role_m.group(1).strip()

        rules_m = re.search(r"RULES:\s*\n((?:- .+\n?)+)", raw)
        if rules_m:
            rules = [
                line.lstrip("- ").strip()
                for line in rules_m.group(1).strip().split("\n")
                if line.strip().startswith("-")
            ]

        dir_m = re.search(
            r"DIRECTIVE:\s*\n([\s\S]+?)"
            r"(?=\nOUTPUT MUST INCLUDE:|\nINTEGRATION RATIONALE:|$)",
            raw,
        )
        if dir_m:
            directive = dir_m.group(1).strip()

        out_m = re.search(
            r"OUTPUT MUST INCLUDE:\s*\n((?:- .+\n?)+)", raw
        )
        if out_m:
            output_reqs = [
                line.lstrip("- ").strip()
                for line in out_m.group(1).strip().split("\n")
                if line.strip().startswith("-")
            ]

        return IntegrationResult(
            question=question,
            source_templates=names,
            integrated_context=raw,
            role=role,
            rules=rules,
            directive=directive,
            output_requirements=output_reqs,
            raw_llm_response=raw,
        )
