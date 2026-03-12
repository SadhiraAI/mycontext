"""
Scenario Planner - Plan for multiple possible futures.

Develops comprehensive scenario plans to navigate uncertainty.
Based on strategic foresight and scenario planning methodologies.

mode parameter controls the planning approach:
  strategic    — full 10-section strategic foresight analysis (default)
  operational  — 3 sections: signposts + actions + quick preparedness plan
"""

from __future__ import annotations

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern

VALID_MODES: frozenset[str] = frozenset({"strategic", "operational"})


def _build_directive(mode: str) -> str:
    """Assemble the directive at runtime — scaffold never stored as a module-level constant."""

    def _signposts(n: int) -> str:
        return (
            f"{n}. **SIGNPOSTS & TRIGGERS**\n\n"
            "   Concrete checkpoints and go/no-go triggers:\n\n"
            "   Decision triggers:\n"
            "   - If [Signal] reaches [Threshold] by [Date] \u2192 Execute [Action]\n"
            "   - If [Signal] drops below [Threshold] \u2192 Escalate / pivot to [Plan B]\n"
            "   - Review checkpoint: [Date] \u2014 reassess scenario probabilities\n\n"
            "   Monitoring responsibilities:\n"
            "   - [Person/team] monitors [Metric] weekly\n"
            "   - [Person/team] monitors [Metric] monthly"
        )

    def _preparedness(n: int) -> str:
        return (
            f"{n}. **PREPAREDNESS PLAN**\n\n"
            "   Immediate actions (next 30 days, regardless of scenario):\n"
            "   - [ ] [Action 1 \u2014 builds optionality]\n"
            "   - [ ] [Action 2 \u2014 reduces exposure]\n"
            "   - [ ] [Action 3 \u2014 gathers information]\n\n"
            "   Capabilities to build:\n"
            "   - [Capability A] \u2014 enables response to scenarios [1, 2]\n"
            "   - [Capability B] \u2014 critical hedge for scenario 3\n\n"
            "   Decision points and timeline:\n"
            "   - [Date 1]: [Decision to make] \u2014 inputs needed: [Data/analysis]\n"
            "   - [Date 2]: [Next decision point]"
        )

    robust_strategies = (
        "5. **ROBUST STRATEGIES**\n\n"
        "   Options that work well across multiple scenarios:\n"
        "   - Strategy A: [Action] \u2014 Works because: [Rationale] \u2014 Scenarios served: [1, 2]\n"
        "   - Strategy B: [Action] \u2014 Works because: [Rationale] \u2014 Scenarios served: [1, 2, 3]\n"
        "   - Strategy C: [Action] \u2014 Works because: [Rationale] \u2014 Scenarios served: [2, 3]\n\n"
        "   Scenario-specific hedges:\n"
        "   - If Scenario 1: [Action to take early]\n"
        "   - If Scenario 3: [Defensive action to take]"
    )

    if mode == "operational":
        sections_list = [_signposts(1), robust_strategies, _preparedness(3)]
        instruction = (
            "Provide an operational scenario response kit: signposts and triggers "
            "to monitor, robust strategies that work across scenarios, and a "
            "concrete 30-day preparedness plan. Skip the full foresight analysis \u2014 "
            "deliver what a team needs to act now."
        )
        total = "3 sections"
    else:
        sections_list = [
            (
                "1. **SITUATION ANALYSIS**\n"
                "   - Decision context: {situation}\n"
                "   - Key uncertainties: [List the main unknown variables]\n"
                "   - Time horizon: [Short / medium / long term]\n"
                "   - Stakes: [What is at risk or could be gained?]"
            ),
            (
                "2. **DRIVING FORCES**\n\n"
                "   Critical Uncertainties (high impact, high uncertainty):\n"
                "   - Force 1: [What could swing this either way?]\n"
                "   - Force 2: [Another major uncertain driver]\n\n"
                "   Predetermined Elements (near-certain regardless of scenario):\n"
                "   - [Factor that will happen regardless]\n"
                "   - [Another near-certain element]"
            ),
            (
                "3. **SCENARIO DEVELOPMENT**\n\n"
                "   **Scenario 1 \u2014 [Best Case Name]**:\n"
                "   - What happens: [Description] | Probability: [Low/Medium/High] | Impact: [Implications]\n\n"
                "   **Scenario 2 \u2014 [Base Case Name]**:\n"
                "   - What happens: [Most likely trajectory] | Probability: [Low/Medium/High] | Impact: [Implications]\n\n"
                "   **Scenario 3 \u2014 [Worst Case Name]**:\n"
                "   - What happens: [Adverse scenario] | Probability: [Low/Medium/High] | Impact: [Implications]\n\n"
                "   **Scenario 4 \u2014 [Wild Card / Black Swan]**:\n"
                "   - What happens: [Low probability, high impact] | Why plausible: [Case] | Impact: [Magnitude]"
            ),
            (
                "4. **IMPLICATIONS BY SCENARIO**\n\n"
                "   | Dimension | Scenario 1 | Scenario 2 | Scenario 3 |\n"
                "   |-----------|------------|------------|------------|\n"
                "   | Strategy | [Impact] | [Impact] | [Impact] |\n"
                "   | Resources | [Impact] | [Impact] | [Impact] |\n"
                "   | Timeline | [Impact] | [Impact] | [Impact] |\n"
                "   | Risk | [Impact] | [Impact] | [Impact] |"
            ),
            robust_strategies,
            (
                "6. **EARLY WARNING INDICATORS**\n\n"
                "   | Signal | Points to Scenario | Threshold | How to Monitor |\n"
                "   |--------|-------------------|-----------|----------------|\n"
                "   | [Signal 1] | [Scenario] | [Value/Date] | [Source] |\n"
                "   | [Signal 2] | [Scenario] | [Value/Date] | [Source] |"
            ),
            _signposts(7),
            (
                "8. **CONTINGENCY PLANNING**\n\n"
                "   Scenario 1 Response Plan:\n"
                "   - Trigger: [Event or signal] | Immediate actions (48h): [Steps] | Resources: [What to pre-position]\n\n"
                "   Scenario 3 Response Plan:\n"
                "   - Trigger: [What signals this] | Emergency actions: [Stabilisation] | Recovery: [Path to scenario 2]"
            ),
            _preparedness(9),
            (
                "10. **MONITORING FRAMEWORK**\n\n"
                "   Review cadence:\n"
                "   - Weekly: [Fast-moving signals] | Monthly: [Trend review] | Quarterly: [Scenario reassessment]\n\n"
                "   Dashboard metrics:\n"
                "   - [Metric 1]: [Target range] | [Metric 2]: [Alert threshold] | [Metric 3]: [Leading indicator]"
            ),
        ]
        instruction = (
            "Apply rigorous strategic foresight methodology. Develop 4 distinct scenarios "
            "(best case, base case, worst case, wild card), map implications for each, "
            "identify robust strategies that work across multiple scenarios, define early "
            "warning indicators, and build a comprehensive contingency and preparedness plan."
        )
        total = "10 sections"

    sections_text = "\n\n".join(sections_list)
    return (
        f"Develop a scenario plan for:\n\n"
        f"**SITUATION**: {{situation}}\n\n"
        f"{{context_section}}\n\n"
        f"**TIME HORIZON**: {{time_horizon}}\n\n"
        f"**FOCUS AREAS**:\n{{focus_areas_section}}\n\n"
        f"**MODE**: {mode} ({total})\n\n"
        f"{instruction}\n\n"
        f"{sections_text}\n\n"
        f"**OUTPUT FORMAT**: Actionable planning document with specific, concrete signals and steps."
    )


# ---------------------------------------------------------------------------
# Template class
# ---------------------------------------------------------------------------

class ScenarioPlanner(Pattern):
    """
    Plan for multiple possible futures using scenario planning methodology.

    The **mode** parameter controls planning scope:

    - ``strategic`` (10 sections, default): Full strategic foresight analysis —
      situation analysis, driving forces, 4 distinct scenarios (best/base/worst/
      wild card), cross-scenario implications table, robust strategies, early
      warning indicators, signposts, contingency plans, preparedness plan, and
      monitoring framework.
    - ``operational`` (3 sections): Signposts + triggers → robust strategies →
      30-day preparedness plan.  Use when you already have a scenario framework
      and just need the response playbook.  ~70% fewer sections.

    Examples:
        >>> planner = ScenarioPlanner()
        >>> # Full strategic analysis
        >>> result = planner.execute(
        ...     provider="openai",
        ...     situation="We are deciding whether to expand into the EU market in 2026",
        ...     time_horizon="18 months",
        ...     mode="strategic",
        ... )
        >>> # Operational response kit
        >>> result = planner.execute(
        ...     provider="openai",
        ...     situation="Interest rates may rise sharply in Q3 2026",
        ...     time_horizon="6 months",
        ...     mode="operational",
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "Develop comprehensive scenario plans for the following situation:\n\n"
        "Situation: {situation}\n"
        "Time horizon: {time_horizon}\n"
        "{context_section}\n"
        "Focus areas: {focus_areas}\n\n"
        "Identify driving forces and critical uncertainties, develop 3-4 distinct "
        "plausible scenarios, map implications for each, identify robust strategies "
        "that work across scenarios, and create contingency plans with early warning "
        "indicators.\n\n"
        "Focus on actionable insights and practical decision support."
    )

    def __init__(self):
        super().__init__(
            name="scenario_planner",
            description="Plan for multiple possible futures",
            guidance=Guidance(
                role="Expert Strategic Planner and Scenario Planning Specialist",
                rules=[
                    "Create genuinely different scenarios — not just better/worse versions",
                    "Focus on high-uncertainty, high-impact drivers",
                    "Identify robust strategies that work across multiple scenarios",
                    "Provide concrete, specific signals and indicators",
                    "Make action plans specific and time-bound",
                ],
                style="strategic, rigorous, practical",
            ),
            directive_template=_build_directive("strategic"),
            input_schema={
                "situation": str,
                "context_section": str,
                "time_horizon": str,
                "focus_areas_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "multiple_scenarios",
                    "robust_strategies",
                    "early_warning_indicators",
                ],
                style_guide="Be specific with signals, thresholds, and actions",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def _render_focus_areas_section(self, focus_areas: list | None) -> str:
        if focus_areas:
            return "\n".join(f"- {area}" for area in focus_areas)
        return "- No specific areas specified — cover broadly"

    def build_context(
        self,
        situation: str = "",
        time_horizon: str = "12 months",
        context: str | None = None,
        focus_areas: list | None = None,
        mode: str = "strategic",
        **kwargs,
    ):
        """
        Build context for scenario planning.

        Args:
            situation: The decision or situation to plan for
            time_horizon: Planning horizon (e.g. "6 months", "3 years")
            context: Optional additional context
            focus_areas: Optional list of areas to focus the scenarios on
            mode: Planning scope — ``"strategic"`` (default, 10 sections)
                | ``"operational"`` (3 sections — response playbook only)
        """
        if mode not in VALID_MODES:
            raise ValueError(
                f"Invalid mode {mode!r}. Choose from: {sorted(VALID_MODES)}"
            )
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        context_section = self._render_context_section(context)
        focus_areas_section = self._render_focus_areas_section(focus_areas)
        directive_text = _build_directive(mode)
        directive_content = safe_format_template(
            directive_text,
            situation=situation,
            time_horizon=time_horizon,
            context_section=context_section,
            focus_areas_section=focus_areas_section,
        )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data={
                "situation": situation, "time_horizon": time_horizon,
                "context_section": context_section,
                "focus_areas_section": focus_areas_section,
            },
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["mode"] = mode
        return ctx

    def execute(
        self,
        provider: str = "openai",
        situation: str = "",
        time_horizon: str = "12 months",
        context: str | None = None,
        focus_areas: list | None = None,
        mode: str = "strategic",
        **kwargs,
    ):
        """
        Execute scenario planning.

        Args:
            provider: LLM provider to use
            situation: The decision or situation to plan for
            time_horizon: Planning horizon
            context: Optional additional context
            focus_areas: Optional list of focus areas
            mode: ``"strategic"`` (default) | ``"operational"``
            **kwargs: Provider parameters
        """
        provider_params = {
            "model", "temperature", "max_tokens", "top_p",
            "frequency_penalty", "presence_penalty", "stop",
            "user", "api_key", "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        ctx = self.build_context(
            situation=situation,
            time_horizon=time_horizon,
            context=context,
            focus_areas=focus_areas,
            mode=mode,
        )
        return ctx.execute(provider=provider, **provider_kwargs)
