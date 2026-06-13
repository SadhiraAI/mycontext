"""
FeedbackLoopIdentifier Pattern (Enterprise)

Map reinforcing and balancing feedback loops in complex systems.

Research Foundation:
- Sterman, J. D. (2000). Business Dynamics: Systems Thinking and Modeling for a Complex World.
- Senge, P. M. (1990). The Fifth Discipline: The Art & Practice of the Learning Organization.
- Meadows, D. H. (2008). Thinking in Systems: A Primer.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class FeedbackLoopIdentifier(Pattern):
    """
    Map reinforcing and balancing feedback loops in complex systems.

    Identifies two fundamental loop types:
    - Reinforcing (R) loops: amplify change — drive growth or decline
    - Balancing (B) loops: resist change — seek equilibrium or targets

    Use Cases:
    - Business model dynamics (growth engines, churn spirals)
    - Organizational change (resistance vs momentum)
    - Product growth loops (viral loops, network effects)
    - Ecosystem and market analysis

    Example:
        >>> from mycontext.templates.enterprise.systems_thinking import FeedbackLoopIdentifier
        >>>
        >>> pattern = FeedbackLoopIdentifier()
        >>> context = pattern.build_context(
        ...     system="SaaS product: Users → Content → More Users → Revenue → Features",
        ...     behavior="Growth plateaued despite increasing marketing spend"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a systems dynamics expert. Identify all feedback loops driving "
        "behavior in the given system.\n\n"
        "System: {system}\n"
        "Observed Behavior: {behavior}\n"
        "{context_section}\n\n"
        "Analyze feedback loops: (1) Identify key system variables and their "
        "current trends. (2) Map all reinforcing (R) loops that amplify change — "
        "trace each causal chain with polarity signs (+/-) and explain the growth "
        "or decline dynamic. (3) Map all balancing (B) loops that resist change — "
        "identify the target or limit each loop seeks. (4) Determine which loop is "
        "currently dominant and explain why using structural reasoning. "
        "(5) Characterize the behavioral signature: S-shaped growth, oscillation, "
        "collapse, or equilibrium. (6) Recommend high-leverage interventions that "
        "shift loop dominance toward desired behavior.\n\n"
        "Use standard R/B notation with numbered labels (R1, B1, etc.).\n\n"
    )

    def __init__(self):
        super().__init__(
            name="feedback_loop_identifier",
            description="Map reinforcing and balancing feedback loops",
            version="1.0.0",
            tags=["systems-thinking", "enterprise", "feedback-loops", "dynamics"],
            metadata={
                "category": "systems_thinking",
                "license": "enterprise",
                "tier": "enterprise",
            },
            guidance=Guidance(
                role="Systems Dynamics Expert specializing in feedback loop analysis",
                rules=[
                    "Identify ALL reinforcing (R) and balancing (B) loops in the system",
                    "Use standard R/B notation with numbered labels (R1, B1, etc.)",
                    "Trace the causal chain for each loop explicitly",
                    "Explain the polarity of each link (+ same direction, − opposite direction)",
                    "Identify which loop is currently dominant and why",
                    "Suggest interventions that shift loop dominance",
                ],
                style="systematic, precise, uses standard systems dynamics notation",
            ),
            directive_template="""**FEEDBACK LOOP ANALYSIS**

**SYSTEM**: {system}

**OBSERVED BEHAVIOR**: {behavior}

{context_section}

---

## 1. SYSTEM VARIABLES

Identify the key variables (stocks and measurable quantities) in this system:

| Variable | Type | Current Trend |
|----------|------|---------------|
| [Variable 1] | [Stock / Rate / State] | [↑ / ↓ / → ] |

---

## 2. REINFORCING LOOPS (Amplify Change)

Reinforcing loops drive exponential growth or decline. Trace each loop:

### R1: [Name]
**Loop**: A →(+) B →(+) C →(+) A
**Narrative**: When A increases, B increases, which causes C to increase, further increasing A.
**Current effect**: [Growth engine / Vicious cycle / Dormant]
**Evidence**: [What data shows this loop is active?]

### R2: [Name]
[Continue for all reinforcing loops...]

---

## 3. BALANCING LOOPS (Seek Equilibrium)

Balancing loops resist change and push toward a target or limit.

### B1: [Name]
**Loop**: A →(+) B →(−) A
**Target/Limit**: [What is this loop trying to achieve or constrain?]
**Narrative**: When A increases, B increases, which pushes A back down.
**Current effect**: [Constraining growth / Preventing decline / Inactive]
**Evidence**: [What data shows this loop is active?]

### B2: [Name]
[Continue for all balancing loops...]

---

## 4. LOOP INTERACTION MAP

Show how loops interact and which dominate:

```
[Variable] ←── R1 (growth) vs B1 (constraint)
              Currently dominant: [R1 / B1]
              Shift point: [What would flip dominance?]
```

---

## 5. DOMINANT LOOP ANALYSIS

**Currently dominant loop**: [R_ or B_]
**Why it dominates**: [Explain the structural reason]
**Behavioral signature**: [What observable pattern does this create?]
  - S-shaped growth → early R dominance shifting to B dominance
  - Oscillation → delayed balancing loops
  - Collapse → reinforcing decline overpowering balancing loops

---

## 6. LEVERAGE POINTS & INTERVENTIONS

| Intervention | Target Loop | Expected Effect | Risk |
|-------------|-------------|-----------------|------|
| [Action 1] | [R_/B_] | [Strengthen/weaken loop] | [Side effects] |

---

## 7. SUMMARY

**Key insight**: [One-sentence synthesis]
**Dominant dynamic**: [Which loop type controls current behavior]
**Recommended action**: [Highest-leverage intervention]""",
            input_schema={
                "system": str,
                "behavior": str,
                "context_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "reinforcing_loops",
                    "balancing_loops",
                    "dominant_loop_identification",
                    "causal_chain_tracing",
                ],
                must_not_include=[
                    "unlabeled_loops",
                    "missing_polarity_signs",
                ],
                style_guide="Use standard R/B loop notation. Trace every causal link explicitly.",
            ),
        )

    def build_context(self, system="", behavior="", context="", **kwargs):
        """Build context for feedback loop analysis."""
        context_section = f"**ADDITIONAL CONTEXT**: {context}" if context else ""
        kwargs.pop("context_section", None)
        return super().build_context(
            system=system,
            behavior=behavior,
            context_section=context_section,
            **kwargs,
        )

    def execute(self, provider="gemini", system="", behavior="", context="", **kwargs):
        """Execute feedback loop analysis."""
        return super().execute(
            provider=provider,
            system=system,
            behavior=behavior,
            context=context,
            **kwargs,
        )


__all__ = ["FeedbackLoopIdentifier"]
