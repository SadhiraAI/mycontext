"""
EthicalFrameworkAnalyzer Pattern (Enterprise)

Apply 6 major ethical frameworks to analyze decisions.
Implements multi-framework ethical analysis from Santa Clara University.

Research Foundation:
- Markkula Center (2015). A Framework for Ethical Decision Making. Santa Clara University.
- Beauchamp, T. L., & Childress, J. F. (2019). Principles of Biomedical Ethics (8th ed.).

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class EthicalFrameworkAnalyzer(Pattern):
    """
    Analyze decisions through 6 ethical frameworks.

    Frameworks:
    1. Utilitarian: Greatest good for greatest number
    2. Rights: Respect human dignity and moral rights
    3. Justice/Fairness: Fair treatment, equitable distribution
    4. Common Good: Community welfare
    5. Virtue: What would a virtuous person do?
    6. Care Ethics: Relationships and responsibilities

    Use Cases:
    - AI safety decisions
    - Medical ethics
    - Business ethics
    - Policy decisions
    - Product decisions

    Example:
        >>> from mycontext.templates.enterprise.ethical_reasoning import EthicalFrameworkAnalyzer
        >>>
        >>> pattern = EthicalFrameworkAnalyzer()
        >>> result = pattern.execute(
        ...     provider="gemini",
        ...     decision="Deploy facial recognition in public spaces",
        ...     stakeholders="Citizens, law enforcement, businesses"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an ethics professor and moral philosophy expert. Analyze the given "
        "decision through six major ethical frameworks.\n\n"
        "Decision: {decision}\n"
        "Stakeholders: {stakeholders}\n"
        "{context_section}\n\n"
        "Apply all six frameworks systematically: (1) Utilitarian — greatest good "
        "for the greatest number; weigh positive vs negative consequences. "
        "(2) Rights — does this respect human dignity, privacy, consent, and moral "
        "rights? (3) Justice/Fairness — are benefits and burdens distributed "
        "equitably? (4) Common Good — does this advance community welfare, trust, "
        "and social cohesion? (5) Virtue — what would a person of integrity, "
        "courage, and compassion do? (6) Care Ethics — does this maintain caring "
        "relationships and meet responsibilities?\n\n"
        "For each framework, provide a verdict (ethical/questionable/unethical) with "
        "specific reasoning. Identify tensions between frameworks and provide an "
        "integrated recommendation.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="ethical_framework_analyzer",
            description="Apply 6 ethical frameworks to analyze decisions",
            version="1.0.0",
            tags=["ethical-reasoning", "enterprise", "ethics", "decision-making"],
            metadata={
                "category": "ethical_reasoning",
                "license": "enterprise",
                "tier": "enterprise",
            },
            guidance=Guidance(
                role="Ethics Professor and Moral Philosophy Expert",
                rules=[
                    "Apply ALL 6 ethical frameworks systematically",
                    "Consider multiple stakeholder perspectives",
                    "Identify ethical tensions and trade-offs",
                    "Provide framework-specific reasoning (not generic)",
                    "Balance theoretical analysis with practical implications",
                ],
                style="balanced, rigorous, multi-perspective, thoughtful, clear",
            ),
            directive_template="""**ETHICAL FRAMEWORK ANALYSIS**

**DECISION/ACTION**: {decision}

**STAKEHOLDERS**: {stakeholders}

{context_section}

---

## SIX-FRAMEWORK ETHICAL ANALYSIS

### 1. UTILITARIAN APPROACH (Consequences)

**Principle**: Actions are right if they produce the greatest good for the greatest number.

**Analysis**:
- **Positive consequences**: [Who benefits? How much?]
- **Negative consequences**: [Who is harmed? How much?]
- **Net utility**: [Overall balance]
- **Long-term effects**: [Future impacts]

**Utilitarian verdict**: [Ethical / Questionable / Unethical]
**Reasoning**: [Why? Based on net good/harm]

---

### 2. RIGHTS APPROACH (Human Dignity)

**Principle**: Actions are right if they respect the moral rights and dignity of all people.

**Key rights to consider**:
- Right to life, liberty, privacy
- Freedom from harm
- Informed consent
- Fair treatment

**Analysis**:
- **Rights protected**: [Which rights upheld?]
- **Rights violated**: [Which rights infringed?]
- **Whose rights take precedence**: [When rights conflict]

**Rights-based verdict**: [Ethical / Questionable / Unethical]
**Reasoning**: [Why? Based on rights respect/violation]

---

### 3. JUSTICE/FAIRNESS APPROACH (Equity)

**Principle**: Actions are right if they treat people fairly and equitably.

**Analysis**:
- **Distributive justice**: Are benefits/burdens distributed fairly?
- **Procedural justice**: Is the process fair?
- **Compensatory justice**: Are harms addressed?
- **Retributive justice**: Are wrongs punished appropriately?

**Who is advantaged/disadvantaged**:
- Advantages: [Which groups benefit disproportionately?]
- Disadvantages: [Which groups bear disproportionate burden?]

**Justice verdict**: [Ethical / Questionable / Unethical]
**Reasoning**: [Why? Based on fairness/equity]

---

### 4. COMMON GOOD APPROACH (Community Welfare)

**Principle**: Actions are right if they advance the welfare of the community as a whole.

**Analysis**:
- **Social benefits**: [How does community benefit?]
- **Social costs**: [How is community harmed?]
- **Impact on social fabric**: [Trust, cohesion, solidarity]
- **Long-term sustainability**: [Community viability]

**Common good verdict**: [Ethical / Questionable / Unethical]
**Reasoning**: [Why? Based on community welfare]

---

### 5. VIRTUE APPROACH (Character)

**Principle**: Actions are right if they reflect virtuous character traits.

**Virtues to consider**:
- Honesty, courage, compassion, integrity
- Fairness, responsibility, wisdom
- Respect, trustworthiness, citizenship

**Analysis**:
- **Virtues exhibited**: [Which virtues does this action demonstrate?]
- **Vices exhibited**: [Which vices does this action demonstrate?]
- **What would a virtuous person do**: [Honest assessment]

**Virtue-based verdict**: [Ethical / Questionable / Unethical]
**Reasoning**: [Why? Based on character virtues]

---

### 6. CARE ETHICS APPROACH (Relationships)

**Principle**: Actions are right if they maintain caring relationships and meet responsibilities.

**Analysis**:
- **Relationships affected**: [Which relationships impacted?]
- **Care responsibilities**: [What obligations exist?]
- **Empathy and compassion**: [Are these present?]
- **Context and particularity**: [Specific circumstances matter]

**Care ethics verdict**: [Ethical / Questionable / Unethical]
**Reasoning**: [Why? Based on care and relationships]

---

## INTEGRATED ANALYSIS

### Framework Consensus/Conflict

| Framework | Verdict | Key Reason |
|-----------|---------|------------|
| Utilitarian | [...] | [...] |
| Rights | [...] | [...] |
| Justice | [...] | [...] |
| Common Good | [...] | [...] |
| Virtue | [...] | [...] |
| Care Ethics | [...] | [...] |

**Ethical tensions**: [Where do frameworks conflict?]

### Overall Assessment

**Ethically sound aspects**: [What's clearly ethical]
**Ethical concerns**: [What's problematic]
**Gray areas**: [What's uncertain]

### Recommendation

**From ethical standpoint**: [Should this action be taken?]
**Conditions/modifications**: [What would make it more ethical?]
**Alternative approaches**: [Are there more ethical alternatives?]

**Critical question**: Can this decision be publicly justified to all stakeholders using ethical reasoning?""",
            input_schema={"decision": str, "stakeholders": str, "context_section": str},
            constraints=Constraints(
                must_include=[
                    "all_six_frameworks",
                    "framework_specific_reasoning",
                    "stakeholder_analysis",
                    "ethical_tensions",
                ],
                must_not_include=["generic_ethical_claims", "single_framework_bias"],
                style_guide="Apply each framework rigorously with specific reasoning. Identify tensions between frameworks.",
            ),
        )

    def build_context(self, decision="", stakeholders="", context="", **kwargs):
        """Build context for ethical framework analysis."""
        context_section = f"**CONTEXT**: {context}" if context else ""
        kwargs.pop("context_section", None)

        return super().build_context(
            decision=decision, stakeholders=stakeholders, context_section=context_section, **kwargs
        )

    def execute(self, provider="gemini", decision="", stakeholders="", context="", **kwargs):
        """Execute ethical framework analysis."""
        context_section = f"**CONTEXT**: {context}" if context else ""
        kwargs.pop("context_section", None)

        return super().execute(
            provider=provider,
            decision=decision,
            stakeholders=stakeholders,
            context_section=context_section,
            **kwargs,
        )


__all__ = ["EthicalFrameworkAnalyzer"]
