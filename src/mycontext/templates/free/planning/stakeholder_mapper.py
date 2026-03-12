"""
Stakeholder Mapper - Map and manage stakeholder relationships.

Identifies and analyses stakeholders for effective engagement.
Based on stakeholder management and change management frameworks.

view parameter controls section selection:
  full         — all 10 sections (default): complete stakeholder landscape
  executive    — 4 sections: identification + power-interest matrix + top blockers/champions + action plan
  operational  — 4 sections: stakeholder profiles + engagement strategies + communication plan + action plan
"""

from __future__ import annotations

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern

VALID_VIEWS: frozenset[str] = frozenset({"full", "executive", "operational"})


def _build_directive(view: str) -> str:
    """Assemble the directive at runtime — scaffold never stored as a module-level constant."""

    def _engagement(n: int) -> str:
        return (
            f"{n}. **ENGAGEMENT STRATEGIES**\n\n"
            "   Tailored approach by stakeholder:\n"
            "   - **[Stakeholder 1]**: [Approach] \u2014 Frequency: [How often] \u2014 Owner: [Who]\n"
            "   - **[Stakeholder 2]**: [Approach] \u2014 Frequency: [How often] \u2014 Owner: [Who]\n\n"
            "   Engagement principles:\n"
            "   - Consult before deciding on [decisions that affect them]\n"
            "   - Involve them in [areas where their input adds value]\n"
            "   - Inform only for [decisions already made]"
        )

    def _comms_plan(n: int) -> str:
        return (
            f"{n}. **COMMUNICATION PLAN**\n\n"
            "   | Stakeholder | Message | Format | Frequency | Channel | Owner |\n"
            "   |-------------|---------|--------|-----------|---------|-------|\n"
            "   | [Name 1] | [Key message] | [Report/meeting] | [Weekly/monthly] | [Channel] | [Owner] |\n"
            "   | [Name 2] | [Tailored message] | [Format] | [Frequency] | [Channel] | [Owner] |\n\n"
            "   Communication schedule:\n"
            "   - [Date/event] \u2192 [Who needs to hear what]"
        )

    def _action_plan(n: int) -> str:
        return (
            f"{n}. **ACTION PLAN**\n\n"
            "   Immediate actions (next 2 weeks):\n"
            "   - [ ] Meet with [key blocker] to understand their concern \u2014 Owner: [Name] \u2014 by [Date]\n"
            "   - [ ] Brief [executive champion] \u2014 Owner: [Name] \u2014 by [Date]\n"
            "   - [ ] Set up [communication channel/cadence] \u2014 Owner: [Name] \u2014 by [Date]\n\n"
            "   Ongoing engagement rhythm:\n"
            "   - Weekly: [Stakeholder A] check-in\n"
            "   - Bi-weekly: [Stakeholder B, C] update\n"
            "   - Monthly: [Executive] steering review\n\n"
            "   Review this map at: [Milestone / date when stakeholder landscape may shift]"
        )

    identification = (
        "1. **STAKEHOLDER IDENTIFICATION**\n\n"
        "   All relevant stakeholders for: {project}\n\n"
        "   **Internal Stakeholders**:\n"
        "   - [Stakeholder 1] \u2014 Role: [Title/function] | Relationship: [How involved]\n"
        "   - [Stakeholder 2] \u2014 Role: [Title/function] | Relationship: [How involved]\n\n"
        "   **External Stakeholders**:\n"
        "   - [Stakeholder A] \u2014 Type: [Customer / partner / regulator / community]\n"
        "   - [Stakeholder B] \u2014 Type: [Category]"
    )
    power_interest = (
        "2. **POWER-INTEREST MATRIX**\n\n"
        "   | Stakeholder | Power (H/M/L) | Interest (H/M/L) | Quadrant | Strategy |\n"
        "   |-------------|---------------|------------------|----------|---------|\n"
        "   | [Name 1] | H | H | **Manage closely** | [High engagement] |\n"
        "   | [Name 2] | H | L | **Keep satisfied** | [Regular updates] |\n"
        "   | [Name 3] | L | H | **Keep informed** | [Transparency] |\n"
        "   | [Name 4] | L | L | **Monitor** | [Minimal touch] |"
    )
    influence_network = (
        "3. **INFLUENCE NETWORK**\n\n"
        "   Key relationships and alliances:\n"
        "   - [Stakeholder A] \u2194 influences \u2194 [Stakeholder B]: [How and why]\n\n"
        "   Informal power centres:\n"
        "   - [Person/group] has informal influence because: [Trusted advisor / domain expert]\n\n"
        "   Coalition possibilities:\n"
        "   - Potential champion coalition: [Who can act together to support us]\n"
        "   - Potential blocker coalition: [Who might resist together and why]"
    )
    profiles = (
        "4. **STAKEHOLDER PROFILES**\n\n"
        "   For each high-priority stakeholder:\n\n"
        "   **[Stakeholder 1]**:\n"
        "   - Goals: [What they are trying to achieve]\n"
        "   - Concerns: [What they are worried about]\n"
        "   - Success criteria: [How they will judge this project's success]\n"
        "   - Communication style: [Direct / formal / data-driven / narrative]\n"
        "   - Best channel: [Email / meeting / report]\n"
        "   - What they need from us: [Information, input, decisions, reassurance]\n\n"
        "   **[Stakeholder 2]**: [Same structure]\n"
        "   **[Stakeholder 3]**: [Same structure]"
    )
    support_analysis = (
        "5. **SUPPORT ANALYSIS**\n\n"
        "   **Champions** (advocates who will actively support):\n"
        "   - [Name]: [Why they support us] | [How to leverage their support]\n\n"
        "   **Blockers** (likely resistors):\n"
        "   - [Name]: [Why they resist] | [Concern to address] | [Approach]\n\n"
        "   **Neutral / Fence-sitters** (could go either way):\n"
        "   - [Name]: [What would move them to support] | [Risk if they move against us]\n\n"
        "   **Top blockers to resolve first**:\n"
        "   1. [Name] \u2014 Root concern: [Core issue] \u2014 Resolution path: [Approach]"
    )
    risks = (
        "8. **STAKEHOLDER RISKS**\n\n"
        "   | Risk | Stakeholder | Likelihood | Impact | Mitigation |\n"
        "   |------|-------------|------------|--------|------------|\n"
        "   | [Risk 1] | [Who] | H/M/L | H/M/L | [How to reduce] |\n"
        "   | [Risk 2] | [Who] | H/M/L | H/M/L | [Mitigation] |"
    )
    monitoring = (
        "10. **MONITORING & REASSESSMENT**\n\n"
        "   Track signals that stakeholder positions are shifting:\n"
        "   - [Signal 1]: [Who might be moving against us]\n"
        "   - [Signal 2]: [Who needs more attention]\n\n"
        "   Reassess this map after [key decision / milestone] or if [triggering event] occurs."
    )

    configs = {
        "full": {
            "sections": [
                identification, power_interest, influence_network, profiles, support_analysis,
                _engagement(6), _comms_plan(7), risks, _action_plan(9), monitoring,
            ],
            "instruction": (
                "Produce a complete stakeholder map and management plan. Cover all "
                "stakeholders \u2014 internal and external \u2014 with detailed profiles, engagement "
                "strategies, communication plan, risk register, and a concrete action plan."
            ),
            "total": "10 sections",
        },
        "executive": {
            "sections": [identification, power_interest, support_analysis, _action_plan(4)],
            "instruction": (
                "Deliver an executive stakeholder briefing: who the stakeholders are, "
                "their power-interest positions, key blockers and champions with resolution "
                "paths, and a prioritised action plan."
            ),
            "total": "4 sections",
        },
        "operational": {
            "sections": [profiles, _engagement(2), _comms_plan(3), _action_plan(4)],
            "instruction": (
                "Produce an operational engagement kit: detailed stakeholder profiles, "
                "tailored engagement strategies, a communication schedule, and a "
                "concrete task list with owners and dates."
            ),
            "total": "4 sections",
        },
    }
    cfg = configs.get(view, configs["full"])
    sections_text = "\n\n".join(cfg["sections"])

    return (
        f"Map and manage stakeholders for:\n\n"
        f"**PROJECT/INITIATIVE**: {{project}}\n\n"
        f"{{context_section}}\n\n"
        f"**GOALS**:\n{{goals_section}}\n\n"
        f"**VIEW**: {view} ({cfg['total']})\n\n"
        f"{cfg['instruction']}\n\n"
        f"{sections_text}\n\n"
        f"**OUTPUT FORMAT**: Structured stakeholder management document with specific, actionable insights."
    )


# ---------------------------------------------------------------------------
# Template class
# ---------------------------------------------------------------------------

class StakeholderMapper(Pattern):
    """
    Map and manage stakeholder relationships for a project or initiative.

    The **view** parameter selects which sections to produce:

    - ``full`` (10 sections, default): Complete stakeholder landscape —
      identification, power-interest matrix, influence network, detailed
      profiles, support analysis (blockers/champions), engagement strategies,
      communication plan, risk register, action plan, and monitoring framework.
    - ``executive`` (4 sections): Identification → power-interest matrix →
      blockers/champions with resolution paths → action plan.  Use for
      steering committee briefings.
    - ``operational`` (4 sections): Profiles → engagement strategies →
      communication schedule → action plan with owners.  Use for the team
      that manages stakeholder relationships day-to-day.

    Examples:
        >>> mapper = StakeholderMapper()
        >>> # Full stakeholder analysis
        >>> result = mapper.execute(
        ...     provider="openai",
        ...     project="Rolling out mandatory two-factor authentication across all teams",
        ...     view="full",
        ... )
        >>> # Exec briefing
        >>> result = mapper.execute(
        ...     provider="openai",
        ...     project="New data retention policy implementation",
        ...     view="executive",
        ... )
        >>> # Ops kit for the team
        >>> result = mapper.execute(
        ...     provider="openai",
        ...     project="Product launch to enterprise customers Q2 2026",
        ...     view="operational",
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "Map and analyse stakeholders for:\n\n"
        "Project: {project}\n"
        "{context_section}\n"
        "Goals: {goals}\n\n"
        "Identify all relevant stakeholders (internal and external), analyse power and "
        "interest, map influence networks, profile each stakeholder's goals and concerns, "
        "classify as champions/blockers/neutral, develop engagement and communication "
        "strategies, identify risks, and build a concrete action plan.\n\n"
        "Focus on actionable insights and practical engagement plans."
    )

    def __init__(self):
        super().__init__(
            name="stakeholder_mapper",
            description="Map and manage stakeholder relationships",
            guidance=Guidance(
                role="Expert Stakeholder Management Specialist",
                rules=[
                    "Consider all stakeholder groups — do not overlook silent influencers",
                    "Understand each stakeholder's perspective and goals",
                    "Identify both formal and informal power structures",
                    "Focus on building genuine relationships, not just managing people",
                    "Make engagement strategies specific and actionable",
                ],
                style="analytical, empathetic, practical",
            ),
            directive_template=_build_directive("full"),
            input_schema={
                "project": str,
                "context_section": str,
                "goals_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "stakeholder_identification",
                    "engagement_strategy",
                    "action_plan",
                ],
                style_guide="Be specific about individuals and their positions — not generic",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def _render_goals_section(self, goals: list | None) -> str:
        if goals:
            return "\n".join(f"- {g}" for g in goals)
        return "- Not specified — infer from project description"

    def build_context(
        self,
        project: str = "",
        context: str | None = None,
        goals: list | None = None,
        view: str = "full",
        **kwargs,
    ):
        """
        Build context for stakeholder mapping.

        Args:
            project: The project or initiative to map stakeholders for
            context: Optional additional context
            goals: Optional list of project goals
            view: Level of detail — ``"full"`` (default, 10 sections)
                | ``"executive"`` (4 sections — strategic briefing)
                | ``"operational"`` (4 sections — engagement and comms kit)
        """
        if view not in VALID_VIEWS:
            raise ValueError(
                f"Invalid view {view!r}. Choose from: {sorted(VALID_VIEWS)}"
            )
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        context_section = self._render_context_section(context)
        goals_section = self._render_goals_section(goals)
        directive_text = _build_directive(view)
        directive_content = safe_format_template(
            directive_text,
            project=project,
            context_section=context_section,
            goals_section=goals_section,
        )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data={
                "project": project,
                "context_section": context_section,
                "goals_section": goals_section,
            },
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["view"] = view
        return ctx

    def execute(
        self,
        provider: str = "openai",
        project: str = "",
        context: str | None = None,
        goals: list | None = None,
        view: str = "full",
        **kwargs,
    ):
        """
        Execute stakeholder mapping.

        Args:
            provider: LLM provider to use
            project: The project or initiative
            context: Optional additional context
            goals: Optional list of project goals
            view: ``"full"`` (default) | ``"executive"`` | ``"operational"``
            **kwargs: Provider parameters
        """
        provider_params = {
            "model", "temperature", "max_tokens", "top_p",
            "frequency_penalty", "presence_penalty", "stop",
            "user", "api_key", "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        ctx = self.build_context(
            project=project, context=context, goals=goals, view=view,
        )
        return ctx.execute(provider=provider, **provider_kwargs)
