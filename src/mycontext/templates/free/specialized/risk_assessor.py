"""
Risk Assessor Template - Identify and evaluate risks systematically

Comprehensive risk analysis framework for decision-making.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive


class RiskAssessor(Pattern):
    """
    Risk assessment template for identifying and evaluating risks.
    
    Provides structured risk analysis:
    - Risk identification
    - Probability and impact assessment
    - Risk prioritization
    - Mitigation strategies
    - Risk-benefit analysis
    
    Based on: Enterprise risk management frameworks
    
    Example:
        ```python
        from mycontext.templates.free import RiskAssessor
        
        assessor = RiskAssessor()
        context = assessor.build_context(
            decision="Launching a new product line",
            depth="comprehensive"
        )
        ```
    
    Input Schema:
        - decision (str): The decision, project, or situation to assess
        - context_section (str, optional): Additional context
        - depth (str): Analysis depth ("basic", "detailed", "comprehensive")
    """

    GENERIC_PROMPT = (
        "You are a risk management consultant and strategic advisor. Assess the "
        "risks associated with the following decision or situation:\n\n"
        "Decision/Situation: {decision}\n"
        "{context_section}\n"
        "Depth: {depth}\n\n"
        "Apply systematic risk assessment: "
        "(1) Summarize the situation and decision context. "
        "(2) Identify risks across five categories: strategic, operational, "
        "financial, compliance/legal, and external/environmental. Include both "
        "obvious and hidden risks. "
        "(3) Analyze each risk: description, probability (1-5), impact (1-5), "
        "risk score (P*I), triggers, and timeframe. "
        "(4) Prioritize risks using a matrix — critical (score 15-25), significant "
        "(8-14), and minor (1-7). "
        "(5) Map risk interdependencies — cascading risks, compounding effects, and "
        "risk chains. "
        "(6) Develop mitigation strategies for top risks: avoid, reduce, transfer, "
        "accept, or contingency plan. "
        "(7) Perform a risk-benefit analysis — do the potential gains justify the risks? "
        "(8) Define a monitoring plan with key risk indicators, review frequency, and "
        "escalation triggers. "
        "(9) Provide an overall risk level assessment and a go/no-go recommendation.\n\n"
        "Consider cascading and compounding risks. Be thorough but pragmatic."
    )

    def __init__(self):
        super().__init__(
            name="risk_assessor",
            description="Identify and evaluate risks systematically",
            guidance=Guidance(
                role="Expert Risk Management Consultant and Strategic Advisor",
                rules=[
                    "Identify both obvious and hidden risks",
                    "Assess probability and impact objectively",
                    "Consider cascading and compounding risks",
                    "Prioritize risks by severity",
                    "Propose actionable mitigation strategies",
                    "Balance risk aversion with opportunity",
                    "Use evidence and historical data when available",
                    "Consider different stakeholder perspectives"
                ],
                style="thorough, balanced, pragmatic"
            ),
            directive_template="""Conduct a comprehensive risk assessment for:

"{decision}"

{context_section}

Assessment depth: {depth}

Risk Assessment Framework:

1. SITUATION OVERVIEW
   - Context and objectives
   - Stakeholders affected
   - Time horizon
   - Success criteria

2. RISK IDENTIFICATION
   Identify risks across categories:
   
   a) Strategic Risks
      - Market changes
      - Competitive threats
      - Reputation damage
   
   b) Operational Risks
      - Process failures
      - Resource constraints
      - Technical issues
   
   c) Financial Risks
      - Cost overruns
      - Revenue shortfalls
      - Budget constraints
   
   d) Compliance/Legal Risks
      - Regulatory changes
      - Legal liabilities
      - Compliance failures
   
   e) External Risks
      - Economic factors
      - Political/social changes
      - Natural events

3. RISK ANALYSIS
   For each identified risk:
   - Description: What could go wrong?
   - Probability: Low/Medium/High (or %)
   - Impact: Low/Medium/High (or scale 1-10)
   - Risk Score: Probability × Impact
   - Triggers: Warning signs
   - Timeframe: When could this occur?

4. RISK PRIORITIZATION
   Create a risk matrix:
   - Critical risks (High probability × High impact)
   - Significant risks (Medium probability or impact)
   - Minor risks (Low probability × Low impact)

5. RISK INTERDEPENDENCIES
   - Which risks could trigger others?
   - Cascading effects
   - Compounding risks

6. MITIGATION STRATEGIES
   For each major risk:
   - Avoid: How to eliminate the risk?
   - Reduce: How to decrease probability or impact?
   - Transfer: Can the risk be shared/insured?
   - Accept: Is the risk acceptable?
   - Contingency: Backup plans if risk occurs

7. RISK-BENEFIT ANALYSIS
   - Expected value of the decision
   - Risk tolerance assessment
   - Alternative approaches with different risk profiles

8. MONITORING PLAN
   - Key risk indicators (KRIs)
   - Monitoring frequency
   - Decision triggers
   - Escalation procedures

9. RISK SUMMARY
   - Top 3-5 risks that need immediate attention
   - Overall risk level (Low/Medium/High)
   - Recommended risk management approach
   - Go/no-go recommendation with reasoning

Be specific, quantitative where possible, and actionable.""",
            input_schema={
                "decision": str,
                "context_section": str,
                "depth": str
            }
        )
    
    def _render_context_section(self, context: str) -> str:
        """Render the context section"""
        if not context or context.strip() == "":
            return ""
        return f"\nAdditional Context:\n{context}\n"
    
    def build_context(
        self,
        decision: str,
        context: str = "",
        depth: str = "detailed",
        **kwargs
    ):
        """
        Build a context for risk assessment.
        
        Args:
            decision: The decision, project, or situation to assess
            context: Optional additional context
            depth: Assessment depth
            **kwargs: Additional parameters
            
        Returns:
            Context configured for risk assessment
        """
        context_section = self._render_context_section(context or "")
        
        # Clean up kwargs
        kwargs.pop('context', None)
        kwargs.pop('context_section', None)
        
        return super().build_context(
            decision=decision,
            context_section=context_section,
            depth=depth,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        decision: str = None,
        context: str = "",
        depth: str = "detailed",
        **kwargs
    ):
        """
        Execute risk assessment directly.
        
        Args:
            provider: LLM provider to use
            decision: The decision to assess
            context: Additional context
            depth: Assessment depth
            **kwargs: Provider parameters
            
        Returns:
            Provider response with risk assessment
        """
        context_section = self._render_context_section(context or "")
        
        # Separate provider kwargs
        provider_params = {}
        provider_param_names = {'model', 'temperature', 'max_tokens', 'top_p', 
                               'frequency_penalty', 'presence_penalty', 'stop', 
                               'user', 'api_key', 'base_url'}
        
        for key in list(kwargs.keys()):
            if key in provider_param_names:
                provider_params[key] = kwargs.pop(key)
        
        # Clean up
        kwargs.pop('context', None)
        kwargs.pop('context_section', None)
        
        return super().execute(
            provider=provider,
            decision=decision,
            context_section=context_section,
            depth=depth,
            **provider_params
        )
