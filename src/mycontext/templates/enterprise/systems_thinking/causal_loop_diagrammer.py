"""
CausalLoopDiagrammer Pattern (Enterprise)

Build causal loop diagrams (CLDs) to visualize system causality and feedback.

Research Foundation:
- Sterman, J. D. (2000). Business Dynamics: Systems Thinking and Modeling for a Complex World.
- Richardson, G. P. (1986). Problems with causal-loop diagrams. System Dynamics Review.
- Lane, D. C. (2008). The emergence and use of diagramming in system dynamics.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class CausalLoopDiagrammer(Pattern):
    """
    Build causal loop diagrams to visualize system causality and feedback.

    CLDs are the primary visual tool in systems dynamics for mapping causal
    relationships, identifying feedback loops, and communicating system
    structure to stakeholders.

    Use Cases:
    - System dynamics modeling and workshops
    - Strategy sessions and root cause visualization
    - Policy analysis and impact mapping
    - Cross-functional problem-solving

    Example:
        >>> from mycontext.templates.enterprise.systems_thinking import CausalLoopDiagrammer
        >>>
        >>> pattern = CausalLoopDiagrammer()
        >>> context = pattern.build_context(
        ...     system="Customer satisfaction ecosystem",
        ...     variables="Product quality, Customer satisfaction, Word-of-mouth, New customers, Revenue, R&D investment"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert systems dynamics modeler. Build a causal loop diagram "
        "(CLD) for the given system.\n\n"
        "System: {system}\n"
        "Key Variables: {variables}\n"
        "{context_section}\n\n"
        "Construct the CLD: (1) Define each variable as a quantity that can increase "
        "or decrease. (2) Map every causal link with polarity: (+) same-direction, "
        "(-) opposite-direction, with rationale. (3) Identify all feedback loops and "
        "label them R (reinforcing) or B (balancing). (4) Verify each loop's polarity "
        "by counting negative signs. (5) Mark significant delays with estimated "
        "timeframes. (6) Determine the currently dominant loop and predict short-, "
        "medium-, and long-term system behavior.\n\n"
        "Provide a text-based CLD diagram. Highlight the highest-leverage causal "
        "link and any counter-intuitive findings.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="causal_loop_diagrammer",
            description="Build causal loop diagrams to map system causality",
            version="1.0.0",
            tags=["systems-thinking", "enterprise", "causal-loop-diagram", "visualization"],
            metadata={
                "category": "systems_thinking",
                "license": "enterprise",
                "tier": "enterprise",
            },
            guidance=Guidance(
                role="System Dynamics Modeler specializing in causal loop diagram construction",
                rules=[
                    "Use standard CLD notation: (+) for same-direction, (−) for opposite-direction links",
                    "Variables must be nouns or noun phrases that can increase or decrease",
                    "Every link must have a polarity sign and a brief rationale",
                    "Identify ALL feedback loops and label them R (reinforcing) or B (balancing)",
                    "Mark significant delays with || symbol on the link",
                    "Distinguish endogenous variables (inside the boundary) from exogenous (outside)",
                ],
                style="precise, visual, uses standard CLD conventions rigorously",
            ),
            directive_template="""**CAUSAL LOOP DIAGRAM CONSTRUCTION**

**SYSTEM**: {system}

**KEY VARIABLES**: {variables}

{context_section}

---

## 1. VARIABLE DEFINITION

Define each variable precisely. CLD variables must be quantities that can increase or decrease.

| Variable | Definition | Units / Scale | Type |
|----------|-----------|---------------|------|
| [Variable 1] | [Precise definition] | [How measured] | [Endogenous / Exogenous] |

**System boundary**: [What is inside vs outside the model?]

---

## 2. CAUSAL LINKS

Map every causal relationship between variables:

| From | → | To | Polarity | Rationale | Delay? |
|------|---|-----|----------|-----------|--------|
| [Var A] | → | [Var B] | (+) same direction | [When A ↑, B ↑ because...] | [No / Yes (timeframe)] |
| [Var C] | → | [Var D] | (−) opposite direction | [When C ↑, D ↓ because...] | [No / Yes (timeframe)] |

---

## 3. TEXT-BASED CAUSAL LOOP DIAGRAM

```
Variable A ──(+)──→ Variable B
    ↑                    │
    │                   (+)
    │                    ↓
Variable D ←──(−)── Variable C
         ║
      [delay]

Loop: R1 (Reinforcing) or B1 (Balancing)
```

[Draw the complete diagram using text notation]

---

## 4. FEEDBACK LOOP INVENTORY

### Reinforcing Loops (R)

**R1: [Name]**
- **Path**: A →(+) B →(+) C →(+) A
- **Polarity check**: [Even number of (−) signs = Reinforcing] ✓
- **Behavior**: [Growth / Decline spiral]
- **Narrative**: [In plain language, what this loop does]

[Continue for all R loops...]

### Balancing Loops (B)

**B1: [Name]**
- **Path**: A →(+) B →(−) A
- **Polarity check**: [Odd number of (−) signs = Balancing] ✓
- **Behavior**: [Goal-seeking / Oscillation]
- **Target**: [What equilibrium is this loop seeking?]
- **Narrative**: [In plain language, what this loop does]

[Continue for all B loops...]

---

## 5. DELAYS ANALYSIS

Delays are critical — they cause oscillation, overshoot, and counter-intuitive behavior.

| Link | Delay Duration | Type | Consequence |
|------|---------------|------|-------------|
| [A → B] | [Timeframe] | [Material / Information / Decision] | [Causes oscillation / Overshoot / Inertia] |

---

## 6. DOMINANT STRUCTURE

**Total loops identified**: [# R loops, # B loops]

**Dominant loop(s)**: [Which loop(s) drive current system behavior?]
**Why dominant**: [Structural reason — strength, gain, or delay]

**Dynamic behavior prediction**:
- Short-term: [What the system will do next]
- Medium-term: [Expected trajectory]
- Long-term: [Where the system settles or continues]

---

## 7. CLD QUALITY CHECK

| Check | Status |
|-------|--------|
| All variables are nouns that increase/decrease | [✓/✗] |
| All links have polarity signs (+/−) | [✓/✗] |
| All loops identified and labeled (R/B) | [✓/✗] |
| Loop polarity verified (count − signs) | [✓/✗] |
| Significant delays marked | [✓/✗] |
| System boundary defined | [✓/✗] |

---

## 8. INSIGHTS & RECOMMENDATIONS

**Key insight**: [What the CLD reveals about system behavior]
**Highest-leverage link**: [Which causal link, if changed, would have the biggest impact?]
**Counter-intuitive finding**: [What the CLD shows that isn't obvious?]""",
            input_schema={
                "system": str,
                "variables": str,
                "context_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "variable_definitions",
                    "polarity_on_every_link",
                    "loop_identification_and_labeling",
                    "delay_analysis",
                ],
                must_not_include=[
                    "links_without_polarity",
                    "variables_that_are_verbs",
                    "unlabeled_loops",
                ],
                style_guide="Use standard CLD notation. (+) = same direction, (−) = opposite. Label every loop R or B.",
            ),
        )

    def build_context(self, system="", variables="", context="", **kwargs):
        """Build context for causal loop diagram construction."""
        context_section = f"**ADDITIONAL CONTEXT**: {context}" if context else ""
        kwargs.pop("context_section", None)
        return super().build_context(
            system=system,
            variables=variables,
            context_section=context_section,
            **kwargs,
        )

    def execute(self, provider="gemini", system="", variables="", context="", **kwargs):
        """Execute causal loop diagram analysis."""
        return super().execute(
            provider=provider,
            system=system,
            variables=variables,
            context=context,
            **kwargs,
        )


__all__ = ["CausalLoopDiagrammer"]
