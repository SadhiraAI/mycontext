"""
Hypothesis Generator - Generate testable hypotheses systematically.

Creates well-formed hypotheses following the scientific method.
Based on scientific reasoning and experimental design research.

rigor parameter drives a genuinely different directive per level:
  exploratory — 3 sections: observation + hypothesis + next steps
  standard    — 6 sections: + background + predictions + success criteria
  scientific  — all 10 sections (default, full experimental design)
"""

from __future__ import annotations

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern

VALID_RIGOR_LEVELS: frozenset[str] = frozenset({"exploratory", "standard", "scientific"})


def _build_directive(rigor: str) -> str:
    """Assemble the directive at runtime — scaffold never stored as a module-level constant."""

    def _next_steps(n: int) -> str:
        return (
            f"{n}. **NEXT STEPS**\n"
            "   - Immediate: [First action \u2014 data collection, lit review, pilot]\n"
            "   - Short-term: [Early validation test \u2014 cheapest way to get signal]\n"
            "   - Long-term: [Comprehensive study if initial results are promising]\n"
            "   - Resources needed: [Data, tools, expertise, time, budget]"
        )

    sections_map = {
        "observation": (
            "1. **OBSERVATION ANALYSIS**\n"
            "   - Core observation: [What exactly was observed?]\n"
            "   - Pattern: [What relationship or pattern was noticed?]\n"
            "   - Context: [Under what conditions?]\n"
            "   - Significance: [Why is this interesting or worth investigating?]"
        ),
        "background": (
            "2. **BACKGROUND KNOWLEDGE**\n"
            "   - Known theory: [What existing theory applies?]\n"
            "   - Prior evidence: [What is already established?]\n"
            "   - Mechanisms: [What could explain this?]\n"
            "   - Gaps: [What remains unknown?]"
        ),
        "hypotheses": (
            "3. **HYPOTHESIS FORMULATION**\n\n"
            '   **Primary Hypothesis (H1)**: [Clear cause-effect: "If X, then Y because Z"]\n'
            "   - Independent variable: [What is manipulated] | Dependent variable: [What is measured]\n"
            "   - Mechanism: [Why would this happen?]\n\n"
            "   **Null Hypothesis (H0)**: [No effect \u2014 the default assumption to reject]\n\n"
            "   **Alternative Hypotheses**:\n"
            "   - H2: [An alternative explanation]\n"
            "   - H3: [Another possibility \u2014 different mechanism, same outcome]"
        ),
        "predictions": (
            "4. **TESTABLE PREDICTIONS**\n"
            "   If the primary hypothesis is true:\n"
            "   - Prediction 1: [Specific, observable, measurable outcome]\n"
            "   - Prediction 2: [Another testable outcome]\n\n"
            "   If the hypothesis is false:\n"
            "   - What we would observe instead: [The null result]"
        ),
        "variables": (
            "5. **VARIABLES & CONTROLS**\n\n"
            "   Independent Variables: [Variable] \u2014 [How to manipulate]\n"
            "   Dependent Variables: [Variable] \u2014 [How to measure]\n"
            "   Control Variables: [Variable] \u2014 [What to hold constant]\n"
            "   Confounding Variables: [Variable] \u2014 [Mitigation]"
        ),
        "experimental_design": (
            "6. **EXPERIMENTAL DESIGN**\n\n"
            "   Method: [Design type] | Sample size: [Minimum] | Duration: [Time required]\n"
            "   Treatment group: [What they receive] | Control group: [Comparison baseline]\n"
            "   Primary outcome: [Key metric] | Secondary outcomes: [Additional metrics]"
        ),
        "success_criteria": (
            "7. **SUCCESS CRITERIA**\n\n"
            "   Evidence that supports the hypothesis:\n"
            "   - Statistical: [Significance threshold, effect size, confidence interval]\n"
            "   - Practical: [Minimum meaningful difference \u2014 not just statistical]\n\n"
            "   Reject the hypothesis if:\n"
            "   - [Specific statistical conditions] | [Practical conditions]"
        ),
        "limitations": (
            "8. **LIMITATIONS & ASSUMPTIONS**\n\n"
            "   Assumptions: [What must be true for the experiment to be valid]\n"
            "   Limitations: [What this experiment cannot tell us]\n"
            "   Boundary conditions: [When or where this hypothesis may not apply]"
        ),
        "rival_hypotheses": (
            "9. **RIVAL HYPOTHESES**\n"
            "   Rival Hypothesis A: [Alternative explanation] \u2014 Why plausible: [Evidence] "
            "\u2014 How to distinguish: [Finding that tells them apart]\n"
            "   Rival Hypothesis B: [Another alternative] \u2014 How to rule out: [Test]"
        ),
    }

    configs = {
        "exploratory": {
            "keys": ["observation", "hypotheses"],
            "next_steps_n": 3,
            "instruction": (
                "Generate a clear, testable hypothesis from this observation. "
                "Keep it lean \u2014 state what you think is happening, why, and "
                "the most direct way to test it."
            ),
            "total": 3,
        },
        "standard": {
            "keys": ["observation", "background", "hypotheses", "predictions", "success_criteria"],
            "next_steps_n": 6,
            "instruction": (
                "Apply standard scientific hypothesis generation. "
                "Ground the hypothesis in background knowledge, define testable "
                "predictions, set clear success criteria, and outline next steps."
            ),
            "total": 6,
        },
        "scientific": {
            "keys": [
                "observation",
                "background",
                "hypotheses",
                "predictions",
                "variables",
                "experimental_design",
                "success_criteria",
                "limitations",
                "rival_hypotheses",
            ],
            "next_steps_n": 10,
            "instruction": (
                "Apply the full scientific method. Generate a rigorously specified "
                "hypothesis with null and alternative hypotheses, detailed variable "
                "definitions, an experimental design, success criteria, rival "
                "hypotheses to rule out, and a prioritised next-steps plan."
            ),
            "total": 10,
        },
    }
    cfg = configs.get(rigor, configs["scientific"])
    sections_list = [sections_map[k] for k in cfg["keys"]] + [_next_steps(cfg["next_steps_n"])]
    sections_text = "\n\n".join(sections_list)

    return (
        f"Generate testable hypotheses from this observation:\n\n"
        f"**OBSERVATION**: {{observation}}\n\n"
        f"{{context_section}}\n\n"
        f"**DOMAIN**: {{domain}}\n\n"
        f"**RIGOR LEVEL**: {rigor} ({cfg['total']} sections)\n\n"
        f"{cfg['instruction']}\n\n"
        f"All hypotheses must be testable and falsifiable.\n\n"
        f"{sections_text}\n\n"
        f"**OUTPUT FORMAT**: Scientific, rigorous hypothesis with clear testing plan."
    )


# ---------------------------------------------------------------------------
# Template class
# ---------------------------------------------------------------------------


class HypothesisGenerator(Pattern):
    """
    Generate testable hypotheses systematically from observations.

    The **rigor** parameter controls how comprehensive the output is:

    - ``exploratory`` (3 sections): Observation → Hypothesis → Next steps.
      Fast — good for product managers, analysts, and business teams who need
      a well-formed hypothesis to guide a quick experiment.
    - ``standard`` (6 sections): + Background + Predictions + Success criteria.
      Good for most research and data science contexts.
    - ``scientific`` (10 sections, default): Full scientific method including
      variable definitions, experimental design, rival hypotheses, and
      limitations.  Good for academic research and rigorous experimentation.

    Based on: Scientific method and hypothesis formation research.

    Examples:
        >>> generator = HypothesisGenerator()
        >>> # Quick product hypothesis
        >>> result = generator.execute(
        ...     provider="openai",
        ...     observation="Users who complete onboarding in under 5 minutes retain at 2x the rate",
        ...     domain="SaaS product analytics",
        ...     rigor="exploratory",
        ... )
        >>> # Full scientific hypothesis
        >>> result = generator.execute(
        ...     provider="openai",
        ...     observation="Plants in the east-facing room grew 30% taller than west-facing ones",
        ...     domain="botany",
        ...     rigor="scientific",
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "Generate testable hypotheses from the following observation:\n\n"
        "Observation: {observation}\n"
        "Domain: {domain}\n"
        "{context_section}\n\n"
        "Analyse what was observed and in what context, identify relevant background "
        "knowledge, formulate a primary hypothesis (H1), a null hypothesis (H0), and "
        "alternative hypotheses, define testable predictions with variables and controls, "
        "set success criteria, acknowledge limitations, and recommend next steps.\n\n"
        "All hypotheses must be testable and falsifiable."
    )

    def __init__(self):
        super().__init__(
            name="hypothesis_generator",
            description="Generate testable hypotheses systematically",
            guidance=Guidance(
                role="Expert Scientific Researcher and Hypothesis Specialist",
                rules=[
                    "Include at least one hypothesis that contradicts the user's implied expectation.",
                    "Hypotheses must be testable and falsifiable",
                    "State clear cause-effect relationships",
                    "Include null and alternative hypotheses",
                    "Provide measurable predictions",
                    "Consider confounding variables",
                ],
                style="rigorous, scientific, precise",
            ),
            directive_template=_build_directive("scientific"),
            input_schema={
                "observation": str,
                "context_section": str,
                "domain": str,
            },
            constraints=Constraints(
                must_include=[
                    "testable_hypothesis",
                    "null_hypothesis",
                    "predictions",
                ],
                style_guide="Be scientific but accessible, rigorous but practical",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        observation: str = "",
        domain: str = "general",
        context: str | None = None,
        rigor: str = "scientific",
        **kwargs,
    ):
        """
        Build context for hypothesis generation.

        Args:
            observation: The observation to explain
            domain: Domain context (e.g. "e-commerce", "biology", "engineering")
            context: Optional additional context
            rigor: Depth of scientific rigour — ``"exploratory"`` (3 sections)
                | ``"standard"`` (6 sections) | ``"scientific"`` (10, default)
            **kwargs: Additional options
        """
        if rigor not in VALID_RIGOR_LEVELS:
            raise ValueError(f"Invalid rigor {rigor!r}. Choose from: {sorted(VALID_RIGOR_LEVELS)}")
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        context_section = self._render_context_section(context)
        directive_text = _build_directive(rigor)
        directive_content = safe_format_template(
            directive_text,
            observation=observation,
            domain=domain,
            context_section=context_section,
        )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data={"observation": observation, "domain": domain, "context_section": context_section},
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["rigor"] = rigor
        self._apply_default_self_check(
            ctx,
            [
                "Did I include at least one hypothesis that contradicts the user's implied expectation?",
                "Can each hypothesis be tested or falsified with available methods?",
            ],
        )
        if ctx.examples is None:
            ctx.examples = [
                {
                    "input": "Website conversion rate dropped after redesign",
                    "output": (
                        "H1: New layout moves the CTA below the fold on mobile (test: compare scroll-depth heatmaps).\n"
                        "H2: Page load time increased with new assets (test: compare Core Web Vitals before/after).\n"
                        "H3 (null): The drop is within normal weekly variance and unrelated to the redesign "
                        "(test: run A/B with old design for 2 weeks).\n"
                        "H4 (contrarian): The redesign actually improved UX, but a concurrent pricing change "
                        "drove users away (test: segment conversion by new vs returning visitors)."
                    ),
                }
            ]
        return ctx

    def execute(
        self,
        provider: str = "openai",
        observation: str = "",
        domain: str = "general",
        context: str | None = None,
        rigor: str = "scientific",
        **kwargs,
    ):
        """
        Execute hypothesis generation.

        Args:
            provider: LLM provider to use
            observation: The observation to explain
            domain: Domain context
            context: Optional additional context
            rigor: ``"exploratory"`` | ``"standard"`` | ``"scientific"`` (default)
            **kwargs: Provider parameters (model, temperature, max_tokens, etc.)
        """
        provider_params = {
            "model",
            "temperature",
            "max_tokens",
            "top_p",
            "frequency_penalty",
            "presence_penalty",
            "stop",
            "user",
            "api_key",
            "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        ctx = self.build_context(
            observation=observation,
            domain=domain,
            context=context,
            rigor=rigor,
        )
        return ctx.execute(provider=provider, **provider_kwargs)
