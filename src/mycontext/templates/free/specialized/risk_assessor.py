"""
Risk Assessor Template - Identify and evaluate risks systematically.

Comprehensive risk analysis framework for decision-making.

Depth parameter now drives a genuinely different directive per level:
  basic         — 4 sections: situation + identification + top risks + go/no-go
  detailed      — 7 sections: + full risk analysis + mitigation + risk-benefit (default)
  comprehensive — all 9 sections (+ interdependencies + monitoring plan)

output_format controls how results are presented:
  structured (default) | narrative | brief | actionable | json | table
"""

from __future__ import annotations

from mycontext.foundation import Directive, Guidance
from mycontext.structure import Pattern
from mycontext.utils.format_directives import VALID_OUTPUT_FORMATS, get_format_directive

VALID_DEPTHS: frozenset[str] = frozenset({"basic", "detailed", "comprehensive"})


def _build_directive(depth: str, output_format: str = "structured") -> str:
    """Assemble the directive at runtime — scaffold never stored as a module-level constant."""
    fmt_directive = get_format_directive(output_format)

    def _summary(n: int) -> str:
        return (
            f"{n}. **RISK SUMMARY**\n"
            "   - Top 3\u20135 risks that need immediate attention\n"
            "   - Overall risk level: [Low / Medium / High]\n"
            "   - Recommended risk management approach\n"
            "   - **GO / NO-GO recommendation with reasoning**"
        )

    sections_map = {
        "situation": (
            "1. **SITUATION OVERVIEW**\n"
            "   - Context and objectives\n"
            "   - Stakeholders affected\n"
            "   - Time horizon\n"
            "   - Success criteria"
        ),
        "identification": (
            "2. **RISK IDENTIFICATION**\n"
            "   Identify risks across five categories:\n\n"
            "   **Strategic**: Market changes, competitive threats, reputation damage\n"
            "   **Operational**: Process failures, resource constraints, technical issues\n"
            "   **Financial**: Cost overruns, revenue shortfalls, budget constraints\n"
            "   **Compliance/Legal**: Regulatory changes, legal liabilities, compliance failures\n"
            "   **External**: Economic factors, political/social changes, environmental events"
        ),
        "analysis": (
            "3. **RISK ANALYSIS**\n"
            "   For each identified risk:\n"
            "   - Description: What could go wrong?\n"
            "   - Probability (1\u20135): Low \u2192 High | Impact (1\u20135): Low \u2192 High | Risk Score: P\u00d7I\n"
            "   - Triggers: Warning signs | Timeframe: When could this occur?"
        ),
        "prioritization": (
            "4. **RISK PRIORITIZATION**\n"
            "   - Critical (score 15\u201325): High probability \u00d7 High impact \u2014 immediate action\n"
            "   - Significant (score 8\u201314): Medium probability or impact \u2014 active management\n"
            "   - Minor (score 1\u20137): Low probability \u00d7 Low impact \u2014 monitor"
        ),
        "interdependencies": (
            "5. **RISK INTERDEPENDENCIES**\n"
            "   - Which risks could trigger others?\n"
            "   - Cascading effects and risk chains\n"
            "   - Compounding risks (where two moderate risks combine to critical)"
        ),
        "mitigation": (
            "6. **MITIGATION STRATEGIES**\n"
            "   For each major risk:\n"
            "   - Avoid: How to eliminate? | Reduce: How to decrease probability or impact?\n"
            "   - Transfer: Can it be shared or insured? | Accept: Is it acceptable as-is?\n"
            "   - Contingency: Backup plan if risk occurs"
        ),
        "risk_benefit": (
            "7. **RISK-BENEFIT ANALYSIS**\n"
            "   - Expected value of the decision\n"
            "   - Risk tolerance assessment\n"
            "   - Alternative approaches with different risk profiles"
        ),
        "monitoring": (
            "8. **MONITORING PLAN**\n"
            "   - Key risk indicators (KRIs) | Monitoring frequency\n"
            "   - Decision triggers | Escalation procedures"
        ),
    }

    configs = {
        "basic": {
            "keys": ["situation", "identification", "prioritization"],
            "summary_n": 4,
            "instruction": (
                "Provide a rapid risk overview. Identify the key risks, prioritise them, "
                "and give a clear go/no-go recommendation."
            ),
            "total": 4,
        },
        "detailed": {
            "keys": ["situation", "identification", "analysis", "prioritization", "mitigation", "risk_benefit"],
            "summary_n": 7,
            "instruction": (
                "Conduct a thorough risk assessment: identify, analyse with probability \u00d7 "
                "impact scoring, prioritise, propose mitigation strategies, perform a "
                "risk-benefit analysis, and give a go/no-go recommendation."
            ),
            "total": 7,
        },
        "comprehensive": {
            "keys": [
                "situation", "identification", "analysis", "prioritization",
                "interdependencies", "mitigation", "risk_benefit", "monitoring",
            ],
            "summary_n": 9,
            "instruction": (
                "Conduct a comprehensive risk assessment covering all dimensions: "
                "identification across 5 categories, full probability \u00d7 impact analysis, "
                "risk interdependencies and cascading effects, mitigation strategies, "
                "risk-benefit analysis, a monitoring plan with KRIs, and go/no-go recommendation."
            ),
            "total": 9,
        },
    }
    cfg = configs.get(depth, configs["detailed"])
    sections_list = [sections_map[k] for k in cfg["keys"]] + [_summary(cfg["summary_n"])]
    sections_text = "\n\n".join(sections_list)

    return (
        f'Conduct a risk assessment for:\n\n"{{decision}}"\n\n'
        f"{{context_section}}\n\n"
        f"**ASSESSMENT DEPTH**: {depth} ({cfg['total']} sections)\n\n"
        f"{cfg['instruction']}\n\n"
        f"{sections_text}\n\n"
        f"Be specific, quantitative where possible, and actionable.{fmt_directive}"
    )


# ---------------------------------------------------------------------------
# Template class
# ---------------------------------------------------------------------------

class RiskAssessor(Pattern):
    """
    Risk assessment for identifying and evaluating risks systematically.

    The **depth** parameter drives a genuinely different prompt per level:

    - ``basic`` (4 sections): Situation → Identification → Prioritisation → Go/No-Go.
      Fast — good for quick decision checks or early-stage evaluation.
    - ``detailed`` (7 sections, default): + Full risk analysis + Mitigation + Risk-benefit.
      Good for most business decisions, project launches, and change management.
    - ``comprehensive`` (9 sections): + Interdependencies + Monitoring plan.
      Good for major strategic decisions, compliance-heavy contexts, and board reporting.

    The **output_format** parameter controls presentation:

    - ``structured`` (default): Sections with headers and bullet points
    - ``table``: Risk register format (ideal for project trackers)
    - ``brief``: Top 3 risks + verdict only
    - ``actionable``: Mitigation actions only
    - ``json``: Machine-readable for dashboards or downstream automation
    - ``narrative``: Prose format for reports

    Examples:
        >>> assessor = RiskAssessor()
        >>> # Quick go/no-go check
        >>> result = assessor.execute(
        ...     provider="openai",
        ...     decision="Launch new product line in Q3",
        ...     depth="basic",
        ...     output_format="brief",
        ... )
        >>> # Risk register for project tracker
        >>> result = assessor.execute(
        ...     provider="openai",
        ...     decision="Migrate production database to cloud",
        ...     depth="detailed",
        ...     output_format="table",
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "Assess the risks associated with the following decision or situation:\n\n"
        "Decision/Situation: {decision}\n"
        "{context_section}\n"
        "Depth: {depth}\n\n"
        "Summarise the context, identify risks across strategic/operational/financial/"
        "compliance/external categories, analyse probability and impact, prioritise by "
        "severity, develop mitigation strategies, perform a risk-benefit analysis, and "
        "provide an overall risk level with a go/no-go recommendation.\n\n"
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
                    "Prioritise risks by severity",
                    "Propose actionable mitigation strategies",
                    "Balance risk aversion with opportunity",
                    "Use evidence and historical data when available",
                    "Consider different stakeholder perspectives",
                ],
                style="thorough, balanced, pragmatic",
            ),
            directive_template=_build_directive("detailed"),
            input_schema={
                "decision": str,
                "context_section": str,
                "depth": str,
            },
        )

    def _render_context_section(self, context: str) -> str:
        if not context or context.strip() == "":
            return ""
        return f"\nAdditional Context:\n{context}\n"

    def build_context(
        self,
        decision: str,
        context: str = "",
        depth: str = "detailed",
        output_format: str = "structured",
        **kwargs,
    ):
        """
        Build a context for risk assessment.

        Args:
            decision: The decision, project, or situation to assess
            context: Optional additional context
            depth: Assessment depth — ``"basic"`` | ``"detailed"`` (default)
                | ``"comprehensive"``
            output_format: How to present results — ``"structured"`` (default)
                | ``"narrative"`` | ``"brief"`` | ``"actionable"``
                | ``"json"`` | ``"table"``
            **kwargs: Additional parameters

        Returns:
            Context configured for risk assessment
        """
        if depth not in VALID_DEPTHS:
            raise ValueError(
                f"Invalid depth {depth!r}. Choose from: {sorted(VALID_DEPTHS)}"
            )
        if output_format not in VALID_OUTPUT_FORMATS:
            raise ValueError(
                f"Invalid output_format {output_format!r}. "
                f"Choose from: {sorted(VALID_OUTPUT_FORMATS)}"
            )
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        context_section = self._render_context_section(context or "")
        directive_text = _build_directive(depth, output_format)
        directive_content = safe_format_template(
            directive_text, decision=decision, context_section=context_section, depth=depth
        )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data={"decision": decision, "context_section": context_section, "depth": depth},
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["depth"] = depth
        ctx.metadata["output_format"] = output_format
        return ctx

    def execute(
        self,
        provider: str = "openai",
        decision: str = None,
        context: str = "",
        depth: str = "detailed",
        output_format: str = "structured",
        **kwargs,
    ):
        """
        Execute risk assessment.

        Args:
            provider: LLM provider to use
            decision: The decision to assess
            context: Additional context
            depth: Assessment depth — ``"basic"`` | ``"detailed"`` (default)
                | ``"comprehensive"``
            output_format: How to present results — ``"structured"`` (default)
                | ``"narrative"`` | ``"brief"`` | ``"actionable"``
                | ``"json"`` | ``"table"``
            **kwargs: Provider parameters (model, temperature, max_tokens, etc.)

        Returns:
            Provider response with risk assessment
        """
        provider_params = {
            "model", "temperature", "max_tokens", "top_p",
            "frequency_penalty", "presence_penalty", "stop",
            "user", "api_key", "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        ctx = self.build_context(
            decision=decision,
            context=context,
            depth=depth,
            output_format=output_format,
        )
        return ctx.execute(provider=provider, **provider_kwargs)
