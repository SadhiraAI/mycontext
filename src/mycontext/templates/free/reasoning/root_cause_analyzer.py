"""
Root Cause Analysis Pattern - Identify underlying causes of problems.

Systematic investigation to find true root causes, not just symptoms.
Based on systems thinking and quality management methodologies (5 Whys, Ishikawa).

Depth parameter now drives a genuinely different directive per level:
  quick    — 3 sections: problem definition + 5-whys + root cause statement
  standard — 6 sections: + symptom/cause separation + contributing factors + prevention
  thorough — all 10 sections (default, full Ishikawa + verification + systemic analysis)
"""

from __future__ import annotations

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern

VALID_DEPTHS: frozenset[str] = frozenset({"quick", "standard", "thorough"})


def _build_directive(depth: str) -> str:
    """Assemble the directive at runtime — scaffold never stored as a module-level constant."""

    def _five_whys(n: int) -> str:
        return (
            f"{n}. **FIVE WHYS ANALYSIS**\n"
            "   Iterative questioning to reach the root:\n\n"
            "   Problem: {problem}\n\n"
            "   Why? \u2192 [Answer 1]\n"
            "   Why [Answer 1]? \u2192 [Answer 2]\n"
            "   Why [Answer 2]? \u2192 [Answer 3]\n"
            "   Why [Answer 3]? \u2192 [Answer 4]\n"
            "   Why [Answer 4]? \u2192 [ROOT CAUSE]"
        )

    def _contributing(n: int) -> str:
        return (
            f"{n}. **CONTRIBUTING FACTORS**\n"
            "   Primary Root Cause: [Main underlying cause]\n"
            "   - Evidence: [What supports this?] | Mechanism: [How it causes the problem] | Confidence: [H/M/L]\n\n"
            "   Secondary Factors: [What they contribute and how they amplify]\n"
            "   Interactions: [How factors combine]"
        )

    def _root_cause_statement(n: int) -> str:
        return (
            f"{n}. **ROOT CAUSE STATEMENT**\n"
            "   **Primary Root Cause**: [Clear, specific statement]\n\n"
            "   **How It Causes the Problem**: [Detailed causal mechanism]\n\n"
            "   **Why It Was Not Obvious**: [What obscured the root cause]\n\n"
            "   **Verification Method**: [How to confirm this is really the root]"
        )

    def _prevention(n: int) -> str:
        return (
            f"{n}. **PREVENTION STRATEGY**\n"
            "   - Short-term fix: [Address symptoms immediately]\n"
            "   - Root cause fix: [Address underlying cause]\n"
            "   - Preventive measures: [Stop it happening again]\n"
            "   - Monitoring: [Early warning systems]"
        )

    problem_def = (
        "1. **PROBLEM DEFINITION**\n"
        "   - Problem statement: [Clear, specific description]\n"
        "   - Observable symptoms: [What we can see/measure]\n"
        "   - Impact: [Severity and scope] | When started: [Timeline] | Who affected: [Stakeholders]"
    )
    symptom_cause = (
        "2. **SYMPTOM VS. CAUSE**\n"
        "   Symptoms (observable effects):\n"
        "   - Symptom 1: [What we observe] | Symptom 2: [Another observable]\n\n"
        "   Immediate causes (surface-level triggers):\n"
        "   - Cause A: [Direct trigger] | Cause B: [Another trigger]\n\n"
        "   We need to go deeper..."
    )
    ishikawa = (
        "4. **ISHIKAWA (FISHBONE) ANALYSIS**\n"
        "   - **People**: [Human factors, skills, knowledge, behaviour]\n"
        "   - **Process**: [Procedural issues, workflow problems]\n"
        "   - **Technology**: [Technical failures, system issues]\n"
        "   - **Environment**: [External factors, contextual issues]\n"
        "   - **Materials/Data**: [Input quality, resource issues]\n"
        "   - **Management/Organisation**: [Structural issues, decision-making]"
    )
    verification = (
        "6. **CAUSE VERIFICATION**\n"
        "   For each suspected root cause:\n"
        "   - Hypothesis: [If this is the cause, then...] | Test: [How to verify] "
        "| Evidence: [Data supports/refutes?] | Confidence: [H/M/L]"
    )
    systemic = (
        "7. **SYSTEMIC ANALYSIS**\n"
        "   - System design flaws: [Structural issues]\n"
        "   - Feedback loops: [Reinforcing problems]\n"
        "   - Emergent issues: [From system complexity]\n"
        "   - Hidden dependencies: [Unexpected connections]"
    )
    lessons = (
        "10. **LESSONS LEARNED**\n"
        "   **Key Insights**: [What we learned about the system and diagnosis process]\n"
        "   **Similar Problems**: [Other areas with same root cause? Broader implications?]"
    )

    configs = {
        "quick": {
            "sections": [problem_def, _five_whys(2), _root_cause_statement(3)],
            "instruction": (
                "Provide a rapid root cause investigation. "
                "Define the problem, drill down with Five Whys, and state the root cause clearly."
            ),
            "total": 3,
        },
        "standard": {
            "sections": [
                problem_def,
                symptom_cause,
                _five_whys(3),
                _contributing(4),
                _root_cause_statement(5),
                _prevention(6),
            ],
            "instruction": (
                "Conduct a thorough investigation. "
                "Separate symptoms from causes, apply Five Whys, identify contributing "
                "factors, state the root cause, and recommend prevention."
            ),
            "total": 6,
        },
        "thorough": {
            "sections": [
                problem_def,
                symptom_cause,
                _five_whys(3),
                ishikawa,
                _contributing(5),
                verification,
                systemic,
                _root_cause_statement(8),
                _prevention(9),
                lessons,
            ],
            "instruction": (
                "Conduct a comprehensive root cause investigation using all frameworks: "
                "Five Whys, Ishikawa fishbone, cause verification, systemic analysis, "
                "and lessons learned."
            ),
            "total": 10,
        },
    }
    cfg = configs.get(depth, configs["thorough"])
    sections_text = "\n\n".join(cfg["sections"])

    return (
        f"Conduct systematic root cause analysis:\n\n"
        f"**PROBLEM**: {{problem}}\n\n"
        f"{{context_section}}\n\n"
        f"**ANALYSIS DEPTH**: {depth} ({cfg['total']} sections)\n\n"
        f"{cfg['instruction']}\n\n"
        f"{sections_text}\n\n"
        f"**OUTPUT FORMAT**: Systematic investigation with clear root cause identification."
    )


# ---------------------------------------------------------------------------
# Template class
# ---------------------------------------------------------------------------


class RootCauseAnalyzer(Pattern):
    """
    Systematic root cause analysis for problem investigation.

    Uses multiple techniques grounded in quality management and systems
    thinking: 5 Whys, Ishikawa (fishbone), cause verification, systemic
    analysis, and lessons learned.

    The **depth** parameter drives a genuinely different directive per level:

    - ``quick`` (3 sections): Problem definition → Five Whys → Root cause statement.
      Fast — good for ops incidents where the fix is urgent.
    - ``standard`` (6 sections): + Symptom/cause separation + Contributing factors
      + Prevention strategy.  Good for most engineering and process investigations.
    - ``thorough`` (10 sections, default): Full Ishikawa + cause verification
      + systemic analysis + lessons learned.  Good for post-mortems and
      recurring problems.

    Examples:
        >>> analyzer = RootCauseAnalyzer()
        >>> # Fast ops investigation
        >>> result = analyzer.execute(
        ...     provider="openai",
        ...     problem="API latency spiked 5x after deployment",
        ...     context="Deployment at 14:32 UTC, rollback at 15:10",
        ...     depth="quick",
        ... )
        >>> # Full post-mortem
        >>> result = analyzer.execute(
        ...     provider="openai",
        ...     problem="Checkout failure rate rose from 0.1% to 8%",
        ...     depth="thorough",
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "Investigate the following problem to identify its true root cause:\n\n"
        "Problem: {problem}\n"
        "{context_section}\n"
        "Analysis depth: {depth}\n\n"
        "Separate symptoms from underlying causes, apply Five Whys iteratively, "
        "examine causes across people/process/technology/environment/management, "
        "identify contributing factors and systemic issues, verify candidate causes, "
        "state the root cause clearly with the causal chain, and recommend prevention.\n\n"
        "Be systematic and evidence-driven throughout."
    )

    def __init__(self):
        super().__init__(
            name="root_cause_analyzer",
            description="Systematic root cause investigation",
            guidance=Guidance(
                role="Expert Root Cause Analysis Specialist and Systems Thinker",
                rules=[
                    "Distinguish symptoms from causes",
                    "Dig deep with systematic questioning",
                    "Consider multiple contributing factors",
                    "Use evidence, not speculation",
                    "Verify root causes with tests",
                    "Consider systemic and organisational factors",
                ],
                style="investigative, thorough, evidence-based",
            ),
            directive_template=_build_directive("thorough"),
            input_schema={
                "problem": str,
                "context_section": str,
                "depth": str,
            },
            constraints=Constraints(
                must_include=[
                    "five_whys",
                    "root_cause_statement",
                    "verification_method",
                ],
                style_guide="Be thorough but focused, investigative but not speculative",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        problem: str = "",
        context: str | None = None,
        depth: str = "thorough",
        output_format: str = "structured",
        **kwargs,
    ):
        """
        Build context for root cause analysis.

        Args:
            problem: The problem to investigate
            context: Optional additional context (timeline, recent changes, etc.)
            depth: Analysis depth — ``"quick"`` | ``"standard"``
                | ``"thorough"`` (default)
            output_format: Presentation style — ``"structured"`` (default),
                ``"narrative"``, ``"brief"``, ``"actionable"``, ``"slides"``,
                ``"email"``, ``"qa"``, ``"checklist"``, ``"json"``, ``"table"``
            **kwargs: Additional options (ignored)

        Returns:
            Context object ready for export/use
        """
        if depth not in VALID_DEPTHS:
            raise ValueError(f"Invalid depth {depth!r}. Choose from: {sorted(VALID_DEPTHS)}")
        from mycontext.core import Context
        from mycontext.utils.format_directives import VALID_OUTPUT_FORMATS, get_format_directive
        from mycontext.utils.template_safety import safe_format_template

        if output_format not in VALID_OUTPUT_FORMATS:
            raise ValueError(
                f"Invalid output_format {output_format!r}. "
                f"Choose from: {sorted(VALID_OUTPUT_FORMATS)}"
            )

        context_section = self._render_context_section(context)
        directive_text = _build_directive(depth)
        directive_content = safe_format_template(
            directive_text, problem=problem, context_section=context_section, depth=depth
        )
        fmt = get_format_directive(output_format)
        if fmt:
            directive_content += fmt

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data={"problem": problem, "context_section": context_section, "depth": depth},
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["depth"] = depth
        ctx.metadata["output_format"] = output_format
        self._apply_default_self_check(
            ctx,
            [
                "Am I stopping at symptoms or reaching actual root causes?",
                "Did I consider systemic/structural causes, not just proximate ones?",
            ],
        )
        if ctx.examples is None:
            ctx.examples = [
                {
                    "input": "Customer support tickets doubled last month",
                    "output": (
                        "SYMPTOM: 2x support volume.\n"
                        "PROXIMATE CAUSE: New onboarding flow confuses users at step 3 (68% of tickets reference it).\n"
                        "STRUCTURAL CAUSE: No usability testing was done before the flow shipped — "
                        "the team's release process skips user validation for 'minor' changes.\n"
                        "ROOT: The definition of 'minor change' is subjective and has no checklist criteria, "
                        "so UX review is routinely skipped for changes that affect user-facing flows."
                    ),
                }
            ]
        return ctx

    def execute(
        self,
        provider: str = "openai",
        problem: str = "",
        context: str | None = None,
        depth: str = "thorough",
        output_format: str = "structured",
        **kwargs,
    ):
        """
        Execute root cause analysis.

        Args:
            provider: LLM provider to use
            problem: The problem to investigate
            context: Optional additional context
            depth: Analysis depth — ``"quick"`` | ``"standard"``
                | ``"thorough"`` (default)
            output_format: Presentation style (structured, brief, json, etc.)
            **kwargs: Provider parameters (model, temperature, max_tokens, etc.)

        Returns:
            ProviderResponse with the analysis
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
        from mycontext.utils.format_directives import is_machine_format

        if is_machine_format(output_format) and "temperature" not in provider_kwargs:
            provider_kwargs["temperature"] = 0.0
        ctx = self.build_context(
            problem=problem,
            context=context,
            depth=depth,
            output_format=output_format,
        )
        return ctx.execute(provider=provider, **provider_kwargs)
