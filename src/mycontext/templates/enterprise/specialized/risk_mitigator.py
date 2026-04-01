"""
Risk Mitigator - Risk mitigation strategies

Develops comprehensive risk mitigation and contingency plans.
Based on risk management and business continuity principles.
"""

from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class RiskMitigator(Pattern):
    """
    Develop risk mitigation strategies.

    Creates:
    - Mitigation plans for identified risks
    - Contingency plans
    - Response strategies
    - Monitoring mechanisms

    Based on: Risk management frameworks

    Example:
        >>> mitigator = RiskMitigator()
        >>> context = mitigator.build_context(
        ...     risk="Key team member might leave",
        ...     impact="Critical project delays"
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert risk manager and business continuity planner. Develop "
        "a comprehensive mitigation strategy for the following risk.\n\n"
        "Risk: {risk}\n"
        "Potential impact: {impact}\n"
        "{context_section}\n\n"
        "Apply proactive risk mitigation methodology:\n"
        "(1) Profile the risk — assess likelihood (High/Medium/Low), impact "
        "severity, and overall priority rating. "
        "(2) Design mitigation strategies — develop 2-3 preventive actions that "
        "reduce the probability of occurrence, with estimated cost and "
        "effectiveness for each. "
        "(3) Build contingency plans — create Plan A and Plan B responses if the "
        "risk materializes, including trigger conditions, step-by-step actions, "
        "and required resources. "
        "(4) Define early warning indicators — identify 2-3 signals to monitor "
        "with specific thresholds and check frequencies. "
        "(5) Create a response timeline — outline immediate (0-24h), short-term "
        "(1-7 days), and long-term (recovery) actions. "
        "(6) Assign ownership — designate who owns the risk, who implements "
        "mitigation, and who monitors, plus a cost-benefit analysis of the "
        "mitigation investment vs. potential loss.\n\n"
        "Be practical and action-oriented. Every plan needs an owner.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="risk_mitigator",
            description="Risk mitigation strategies",
            guidance=Guidance(
                role="Expert Risk Manager and Continuity Planner",
                rules=[
                    "Develop proactive mitigation",
                    "Prepare contingencies",
                    "Assign ownership",
                    "Enable monitoring",
                    "Plan responses",
                ],
                style="proactive, thorough, pragmatic",
            ),
            directive_template="""Develop mitigation for:

**RISK**: {risk}

**POTENTIAL IMPACT**: {impact}

{context_section}

Risk mitigation:

1. **RISK PROFILE**
   - Risk: [Description]
   - Likelihood: [High/Med/Low]
   - Impact: [Severity]
   - Priority: [Critical/High/Med/Low]

2. **MITIGATION STRATEGIES** (Reduce likelihood)
   - Strategy 1: [Preventive action]
     - How: [Implementation]
     - Cost: [Investment]
     - Effectiveness: [% reduction]
   
   - Strategy 2: [Another prevention]

3. **CONTINGENCY PLANS** (Reduce impact if occurs)
   - Plan A: [Response if risk occurs]
     - Trigger: [When to activate]
     - Actions: [Steps to take]
     - Resources: [What's needed]
   
   - Plan B: [Backup plan]

4. **EARLY WARNING INDICATORS**
   Monitor these signals:
   - Indicator 1: [What to watch]
     - Threshold: [Warning level]
     - Check frequency: [How often]
   
   - Indicator 2: [Another signal]

5. **RESPONSE PLAN**
   If risk materializes:
   - Immediate (0-24hrs): [Actions]
   - Short-term (1-7 days): [Steps]
   - Long-term (recovery): [Plan]

6. **OWNERSHIP & ACCOUNTABILITY**
   - Risk owner: [Who's responsible]
   - Mitigation owner: [Who implements]
   - Monitor owner: [Who tracks]

7. **COST-BENEFIT**
   - Mitigation cost: $[Amount]
   - Potential loss if occurs: $[Amount]
   - ROI of mitigation: [Calculation]

**OUTPUT FORMAT**: Actionable mitigation plan with contingencies.""",
            input_schema={"risk": str, "impact": str, "context_section": str},
            constraints=Constraints(
                must_include=["mitigation", "contingency", "monitoring"],
                style_guide="Be practical and action-oriented",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(self, risk: str = "", impact: str = "", context: str | None = None, **kwargs):
        context_section = self._render_context_section(context)

        return super().build_context(
            risk=risk, impact=impact, context_section=context_section, **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        risk: str = "",
        impact: str = "",
        context: str | None = None,
        **kwargs,
    ):
        return super().execute(
            provider=provider, risk=risk, impact=impact, context=context, **kwargs
        )
