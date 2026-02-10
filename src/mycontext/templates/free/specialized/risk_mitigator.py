"""
Risk Mitigator - Risk mitigation strategies

Develops comprehensive risk mitigation and contingency plans.
Based on risk management and business continuity principles.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


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
                    "Plan responses"
                ],
                style="proactive, thorough, pragmatic"
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
            input_schema={
                "risk": str,
                "impact": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=["mitigation", "contingency", "monitoring"],
                style_guide="Be practical and action-oriented"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        risk: str = "",
        impact: str = "",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            risk=risk,
            impact=impact,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        risk: str = "",
        impact: str = "",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            risk=risk,
            impact=impact,
            context=context,
            **kwargs
        )
