"""
ValueConflictNavigator Pattern (Enterprise)

Resolve competing values (security vs privacy, efficiency vs fairness).
Based on Rest's four-component model and Schwartz's value theory.

Research Foundation:
- Rest, J. R. (1986). Moral Development: Advances in Research and Theory.
- Schwartz, S. H. (1992). Universals in values. Advances in Experimental Social Psychology, 25, 1-65.

License: Enterprise
"""

from mycontext import Pattern, Guidance, Directive, Constraints


class ValueConflictNavigator(Pattern):
    """Navigate competing values. Enterprise Template."""

    GENERIC_PROMPT = (
        "You are a value systems expert grounded in Schwartz's value theory and "
        "Rest's moral development model. Navigate the conflict between competing "
        "values.\n\n"
        "Situation: {situation}\n"
        "Competing Values: {competing_values}\n"
        "{context_section}\n\n"
        "Navigate the value conflict: (1) Identify each core value at stake — "
        "define {value_a} and {value_b}, articulating why each matters and what it "
        "protects. (2) Analyze the specific context — historical precedent, cultural "
        "factors, legal requirements, and stakeholder expectations that shape how "
        "these values should be weighed. (3) Assess priority — which value takes "
        "precedence in this particular context and why? Consider both universal "
        "principles and situational factors. (4) Explore synthesis options — can "
        "both values be partially honored through creative alternatives? "
        "(5) Recommend a resolution with clear reasoning that acknowledges the "
        "importance of both values.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="value_conflict_navigator",
            description="Resolve competing values",
            version="1.0.0",
            tags=["ethical-reasoning", "enterprise", "values"],
            metadata={"category": "ethical_reasoning", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Value Systems Expert",
                rules=["Identify core values in conflict", "Assess relative priority in context", "Find synthesis when possible"],
                style="balanced, context-aware"
            ),
            directive_template="""**VALUE CONFLICT RESOLUTION**

**SITUATION**: {situation}

**COMPETING VALUES**: {competing_values}

## ANALYSIS

### 1. VALUE IDENTIFICATION
- Value A: {value_a} - Why important: [...]
- Value B: {value_b} - Why important: [...]

### 2. CONTEXT ANALYSIS
In this specific context:
- Historical precedent: [...]
- Cultural factors: [...]
- Legal requirements: [...]

### 3. PRIORITY ASSESSMENT
Which value takes precedence and why?

### 4. SYNTHESIS OPTIONS
Can both values be partially honored?
- Option 1: [...]
- Option 2: [...]

### 5. RECOMMENDATION
[Balance or priority with reasoning]""",
            input_schema={"situation": str, "competing_values": str, "value_a": str, "value_b": str},
            constraints=Constraints(must_include=["context_specific_reasoning"], style_guide="Acknowledge both values' importance")
        )
    
    def build_context(self, situation="", competing_values="", value_a="", value_b="", **kwargs):
        return super().build_context(situation=situation, competing_values=competing_values, value_a=value_a, value_b=value_b, **kwargs)
    
    def execute(self, provider="gemini", situation="", competing_values="", value_a="", value_b="", **kwargs):
        return super().execute(provider=provider, situation=situation, competing_values=competing_values, value_a=value_a, value_b=value_b, **kwargs)


__all__ = ["ValueConflictNavigator"]
