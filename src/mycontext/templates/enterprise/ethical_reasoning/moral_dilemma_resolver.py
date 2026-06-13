"""
MoralDilemmaResolver Pattern (Enterprise)

Navigate situations where ethical principles conflict.
Based on Greene's dual-process theory of moral judgment.

Research Foundation:
- Greene, J. D. (2014). The cognitive neuroscience of moral judgment. The Cognitive Neurosciences V.
- Kohlberg, L. (1981). Essays on Moral Development. Harper & Row.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class MoralDilemmaResolver(Pattern):
    """
    Resolve moral dilemmas where principles conflict.

    Use Cases:
    - Healthcare triage decisions
    - Autonomous vehicle programming
    - Resource allocation
    - Policy trade-offs

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a moral philosophy expert specializing in ethical dilemmas. "
        "Navigate the situation where principles conflict.\n\n"
        "Dilemma: {dilemma}\n"
        "Conflicting Principles: {conflicting_principles}\n"
        "{context_section}\n\n"
        "Resolve the moral dilemma: (1) Map the dilemma structure — identify each "
        "competing principle, what action it demands, and why they are incompatible. "
        "(2) Analyze stakeholder impact — for each possible resolution, who benefits "
        "and who is harmed? (3) Apply deontological reasoning — which principle is "
        "more fundamental? Are there absolute duties at stake? (4) Apply "
        "consequentialist reasoning — which choice produces better overall outcomes "
        "across short- and long-term horizons? (5) Synthesize a recommended "
        "resolution with clear reasoning, acknowledging the moral cost of what must "
        "be sacrificed.\n\n"
        "Avoid oversimplification. Acknowledge moral uncertainty and the genuine "
        "difficulty of the trade-off.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="moral_dilemma_resolver",
            description="Navigate situations where ethical principles conflict",
            version="1.0.0",
            tags=["ethical-reasoning", "enterprise", "dilemma", "ethics"],
            metadata={
                "category": "ethical_reasoning",
                "license": "enterprise",
                "tier": "enterprise",
            },
            guidance=Guidance(
                role="Moral Philosophy Expert",
                rules=[
                    "Identify conflicting principles clearly",
                    "Consider both deontological and consequentialist perspectives",
                    "Acknowledge moral uncertainty",
                    "Provide reasoning for recommended resolution",
                ],
                style="balanced, thoughtful, nuanced",
            ),
            directive_template="""**MORAL DILEMMA ANALYSIS**

**DILEMMA**: {dilemma}

**CONFLICTING PRINCIPLES**: {conflicting_principles}

{context_section}

## ANALYSIS

### 1. DILEMMA STRUCTURE
- Principle A: [What principle?] → Action: [What it demands]
- Principle B: [What principle?] → Action: [What it demands]
- Why they conflict: [Explain incompatibility]

### 2. STAKEHOLDER IMPACT
| Stakeholder | If A chosen | If B chosen |
|-------------|-------------|-------------|
| [...] | [...] | [...] |

### 3. DEONTOLOGICAL VIEW (Rules/Duties)
- Which principle is more fundamental?
- Are there absolute duties involved?

### 4. CONSEQUENTIALIST VIEW (Outcomes)
- Which choice produces better outcomes?
- Long-term vs short-term consequences?

### 5. RECOMMENDATION
**Suggested resolution**: [...]
**Reasoning**: [...]
**Moral cost**: [What is sacrificed?]""",
            input_schema={"dilemma": str, "conflicting_principles": str, "context_section": str},
            constraints=Constraints(
                must_include=["both_perspectives", "stakeholder_analysis", "moral_cost"],
                must_not_include=["oversimplification"],
                style_guide="Acknowledge complexity and moral cost of decisions",
            ),
        )

    def build_context(self, dilemma="", conflicting_principles="", context="", **kwargs):
        context_section = f"**CONTEXT**: {context}" if context else ""
        kwargs.pop("context_section", None)
        return super().build_context(
            dilemma=dilemma,
            conflicting_principles=conflicting_principles,
            context_section=context_section,
            **kwargs,
        )

    def execute(
        self, provider="gemini", dilemma="", conflicting_principles="", context="", **kwargs
    ):
        context_section = f"**CONTEXT**: {context}" if context else ""
        kwargs.pop("context_section", None)
        return super().execute(
            provider=provider,
            dilemma=dilemma,
            conflicting_principles=conflicting_principles,
            context_section=context_section,
            **kwargs,
        )


__all__ = ["MoralDilemmaResolver"]
