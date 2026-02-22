"""
Impact Assessor - Assess impact and consequences

Systematic impact assessment across multiple dimensions.
Based on impact assessment methodologies and evaluation frameworks.
"""


from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class ImpactAssessor(Pattern):
    """
    Assess impact systematically across dimensions.
    
    Evaluates:
    - Short and long-term impact
    - Direct and indirect effects
    - Positive and negative consequences
    - Stakeholder impact
    - Risk and opportunity
    
    Based on: Impact assessment and evaluation frameworks
    
    Example:
        >>> assessor = ImpactAssessor()
        >>> context = assessor.build_context(
        ...     action="Implement 4-day work week",
        ...     context="50-person startup"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert impact assessment and evaluation specialist. Conduct "
        "a comprehensive, multi-dimensional impact assessment of the following "
        "action or decision.\n\n"
        "Action/Decision: {action}\n"
        "{context_section}\n\n"
        "Apply systematic impact assessment methodology:\n"
        "(1) Summarize the action — describe what is being done, why, when, and "
        "who is affected (all relevant stakeholders). "
        "(2) Assess direct impacts — identify immediate, obvious effects across "
        "positive, negative, and neutral dimensions. "
        "(3) Trace indirect impacts — map secondary ripple effects, downstream "
        "consequences, and unintended spillover effects. "
        "(4) Evaluate stakeholder impact — for each stakeholder group, describe "
        "the effect and rate its magnitude (High/Medium/Low). "
        "(5) Analyze across time horizons — assess impact at immediate (0-3 "
        "months), short-term (3-12 months), and long-term (1-5 years) stages. "
        "(6) Deliver an overall assessment — state the net impact (Positive/"
        "Negative/Mixed), your confidence level, and a clear recommendation "
        "to Proceed, Modify, or Reject.\n\n"
        "Be thorough and balanced. Quantify where possible.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="impact_assessor",
            description="Assess impact and consequences",
            guidance=Guidance(
                role="Expert Impact Assessment and Evaluation Specialist",
                rules=[
                    "Consider all dimensions",
                    "Include direct and indirect effects",
                    "Assess both positive and negative",
                    "Quantify where possible",
                    "Consider timeline"
                ],
                style="comprehensive, balanced, thorough"
            ),
            directive_template="""Assess impact of:

**ACTION/DECISION**: {action}

{context_section}

Impact assessment:

1. **ACTION OVERVIEW**
   - What: [Description]
   - Why: [Rationale]
   - When: [Timeline]
   - Who affected: [Stakeholders]

2. **DIRECT IMPACTS**
   Immediate, obvious effects:
   - Positive: [Benefits]
   - Negative: [Costs/drawbacks]
   - Neutral: [Changes]

3. **INDIRECT IMPACTS**
   Secondary, ripple effects:
   - Downstream: [What follows]
   - Spillover: [Unintended effects]

4. **STAKEHOLDER IMPACT**
   | Stakeholder | Impact | Magnitude |
   |-------------|--------|-----------|
   | [Group 1] | [Effect] | [High/Med/Low] |
   | [Group 2] | [Effect] | [High/Med/Low] |

5. **TIMELINE ASSESSMENT**
   - Immediate (0-3 months): [Impact]
   - Short-term (3-12 months): [Impact]
   - Long-term (1-5 years): [Impact]

6. **OVERALL ASSESSMENT**
   - Net impact: [Positive/Negative/Mixed]
   - Confidence: [High/Med/Low]
   - Recommendation: [Proceed/Modify/Reject]

**OUTPUT FORMAT**: Comprehensive multi-dimensional impact assessment.""",
            input_schema={
                "action": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=["direct_indirect", "stakeholders", "timeline"],
                style_guide="Be thorough and balanced"
            )
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        action: str = "",
        context: str | None = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)

        return super().build_context(
            action=action,
            context_section=context_section,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        action: str = "",
        context: str | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            action=action,
            context=context,
            **kwargs
        )
