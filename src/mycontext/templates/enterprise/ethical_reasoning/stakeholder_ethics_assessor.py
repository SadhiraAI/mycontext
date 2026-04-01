"""
StakeholderEthicsAssessor Pattern (Enterprise)

Assess ethical impact on ALL stakeholders including marginalized groups.
Based on Freeman's stakeholder theory + Rawls' justice theory.

Research Foundation:
- Freeman, R. E. (1984). Strategic Management: A Stakeholder Approach.
- Rawls, J. (1971). A Theory of Justice.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class StakeholderEthicsAssessor(Pattern):
    """Assess ethical impact on all stakeholders. Enterprise Template."""

    GENERIC_PROMPT = (
        "You are a stakeholder analysis expert grounded in Freeman's stakeholder "
        "theory and Rawls' justice theory. Assess the ethical impact of the given "
        "decision on all affected groups.\n\n"
        "Decision: {decision}\n"
        "Known Stakeholders: {stakeholders}\n"
        "{context_section}\n\n"
        "Perform stakeholder ethics assessment: (1) Identify ALL stakeholders — "
        "direct, indirect, and vulnerable groups with the least power or voice. "
        "(2) For each stakeholder group, assess benefits, harms, net impact, and "
        "power level. (3) Apply Rawls' veil of ignorance test: if you didn't know "
        "which stakeholder you would be, would you accept this decision? "
        "(4) Identify who bears disproportionate burden and whether vulnerable "
        "groups are adequately protected. (5) Assess whether there is meaningful "
        "consent and fair representation in the decision process.\n\n"
        "Focus on fairness to all groups, especially those with the least power.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="stakeholder_ethics_assessor",
            description="Assess ethical impact on ALL stakeholders",
            version="1.0.0",
            tags=["ethical-reasoning", "enterprise", "stakeholders"],
            metadata={
                "category": "ethical_reasoning",
                "license": "enterprise",
                "tier": "enterprise",
            },
            guidance=Guidance(
                role="Stakeholder Analysis Expert",
                rules=[
                    "Identify ALL stakeholders including vulnerable",
                    "Assess impact on each group",
                    "Apply Rawls' veil of ignorance",
                ],
                style="inclusive, thorough, justice-focused",
            ),
            directive_template="""**STAKEHOLDER ETHICS ASSESSMENT**

**DECISION**: {decision}

**KNOWN STAKEHOLDERS**: {stakeholders}

## ANALYSIS

### 1. STAKEHOLDER IDENTIFICATION
- Direct: [Who directly affected?]
- Indirect: [Who indirectly affected?]
- Vulnerable: [Who has least power/voice?]

### 2. IMPACT ASSESSMENT
| Stakeholder | Benefits | Harms | Net Impact | Power Level |
|-------------|----------|-------|------------|-------------|
| [...] | [...] | [...] | [...] | High/Med/Low |

### 3. VEIL OF IGNORANCE TEST (Rawls)
If you didn't know which stakeholder you'd be, would you accept this decision?

### 4. ETHICAL CONCERNS
- Who bears disproportionate burden?
- Are vulnerable groups protected?
- Is there meaningful consent?""",
            input_schema={"decision": str, "stakeholders": str},
            constraints=Constraints(
                must_include=["vulnerable_groups", "power_analysis"],
                style_guide="Focus on fairness to all groups",
            ),
        )

    def build_context(self, decision="", stakeholders="", **kwargs):
        return super().build_context(decision=decision, stakeholders=stakeholders, **kwargs)

    def execute(self, provider="gemini", decision="", stakeholders="", **kwargs):
        return super().execute(
            provider=provider, decision=decision, stakeholders=stakeholders, **kwargs
        )


__all__ = ["StakeholderEthicsAssessor"]
