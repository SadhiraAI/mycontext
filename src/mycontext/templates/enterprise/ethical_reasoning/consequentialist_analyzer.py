"""
ConsequentialistAnalyzer Pattern (Enterprise)

Evaluate long-term ethical consequences across time horizons.
Implements utilitarian analysis + longtermism considerations.

Research Foundation:
- Smart, J. J. C., & Williams, B. (1973). Utilitarianism: For and Against.
- Ord, T. (2020). The Precipice: Existential Risk and the Future of Humanity.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class ConsequentialistAnalyzer(Pattern):
    """Analyze long-term consequences. Enterprise Template."""

    GENERIC_PROMPT = (
        "You are a consequentialist ethics expert. Analyze the long-term ethical "
        "consequences of the given action across multiple time horizons.\n\n"
        "Action: {action}\n"
        "Scope: {scope}\n"
        "{context_section}\n\n"
        "Perform consequentialist analysis: (1) Immediate consequences (0-1 year) — "
        "identify positive outcomes, negative outcomes, and net impact. "
        "(2) Medium-term consequences (1-10 years) — assess second-order effects, "
        "unintended side effects, and systemic changes. (3) Long-term consequences "
        "(10+ years) — evaluate lasting structural changes, precedent effects, and "
        "irreversible impacts. (4) Probability x Magnitude — calculate expected value "
        "for key outcomes, weighing likelihood against severity. (5) Stakeholder "
        "impact distribution — who bears costs vs who gains benefits.\n\n"
        "Provide a net consequentialist assessment (positive/negative/uncertain) "
        "with a clear recommendation.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="consequentialist_analyzer",
            description="Evaluate long-term ethical consequences",
            version="1.0.0",
            tags=["ethical-reasoning", "enterprise", "consequences"],
            metadata={
                "category": "ethical_reasoning",
                "license": "enterprise",
                "tier": "enterprise",
            },
            guidance=Guidance(
                role="Consequentialist Ethics Expert",
                rules=[
                    "Analyze consequences across time horizons",
                    "Consider second-order effects",
                    "Assess probability and magnitude",
                ],
                style="rigorous, forward-looking",
            ),
            directive_template="""**CONSEQUENTIALIST ANALYSIS**

**ACTION**: {action}

**SCOPE**: {scope}

## CONSEQUENCE ANALYSIS

### IMMEDIATE (0-1 year)
- Positive: [...]
- Negative: [...]
- Net: [...]

### MEDIUM-TERM (1-10 years)
- Positive: [...]
- Negative: [...]
- Unintended effects: [...]

### LONG-TERM (10+ years)
- Positive: [...]
- Negative: [...]
- Systemic changes: [...]

### PROBABILITY × MAGNITUDE
Expected value calculation for key outcomes

### RECOMMENDATION
Net consequentialist assessment: [Positive/Negative/Uncertain]""",
            input_schema={"action": str, "scope": str},
            constraints=Constraints(
                must_include=["time_horizons", "second_order_effects"],
                style_guide="Consider long-term impacts",
            ),
        )

    def build_context(self, action="", scope="", **kwargs):
        return super().build_context(action=action, scope=scope, **kwargs)

    def execute(self, provider="gemini", action="", scope="", **kwargs):
        return super().execute(provider=provider, action=action, scope=scope, **kwargs)


__all__ = ["ConsequentialistAnalyzer"]
