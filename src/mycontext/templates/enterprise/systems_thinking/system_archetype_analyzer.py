"""
SystemArchetypeAnalyzer Pattern (Enterprise)

Recognize common system behavior patterns using Senge's 10 archetypes.

Research Foundation:
- Senge, P. M. (1990). The Fifth Discipline: The Art & Practice of the Learning Organization.
- Kim, D. H. & Anderson, V. (1998). Systems Archetype Basics.
- Braun, W. (2002). The System Archetypes. The Systems Modeling Workbook.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class SystemArchetypeAnalyzer(Pattern):
    """
    Recognize common system behavior patterns using Senge's archetypes.

    The 10 system archetypes are recurring patterns of behavior that appear
    across vastly different systems. Recognizing the archetype unlocks
    known intervention strategies.

    Use Cases:
    - Diagnosing why organizational initiatives stall
    - Understanding competitive dynamics
    - Predicting unintended consequences of policy changes
    - Breaking recurring problematic patterns

    Example:
        >>> from mycontext.templates.enterprise.systems_thinking import SystemArchetypeAnalyzer
        >>>
        >>> pattern = SystemArchetypeAnalyzer()
        >>> context = pattern.build_context(
        ...     system="Engineering team keeps hiring but velocity isn't increasing",
        ...     pattern="We add people but get diminishing returns on output"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a systems thinking expert specializing in Senge's system "
        "archetypes. Diagnose the structural pattern driving behavior.\n\n"
        "System: {system}\n"
        "Observed Pattern: {pattern}\n"
        "{context_section}\n\n"
        "Screen against all 10 system archetypes: (1) Limits to Growth, "
        "(2) Shifting the Burden, (3) Eroding Goals, (4) Escalation, "
        "(5) Success to the Successful, (6) Tragedy of the Commons, "
        "(7) Fixes That Fail, (8) Growth and Underinvestment, "
        "(9) Accidental Adversaries, (10) Attractiveness Principle.\n\n"
        "For each, assess match confidence with evidence. For the primary match: "
        "map reinforcing and balancing loops to this system, identify the current "
        "behavioral phase, provide the archetype-specific intervention strategy, "
        "and warn about typical mistakes. Note any secondary archetypes that "
        "compound or counteract the primary one.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="system_archetype_analyzer",
            description="Recognize common system behavior patterns using Senge's archetypes",
            version="1.0.0",
            tags=["systems-thinking", "enterprise", "archetypes", "pattern-recognition"],
            metadata={
                "category": "systems_thinking",
                "license": "enterprise",
                "tier": "enterprise",
            },
            guidance=Guidance(
                role="Systems Thinking Expert specializing in system archetypes and organizational dynamics",
                rules=[
                    "Evaluate the situation against ALL 10 system archetypes",
                    "Identify the primary archetype match with confidence level",
                    "Show the structural diagram (loops) for the matched archetype",
                    "Provide the archetype-specific intervention strategy",
                    "Warn about the typical mistakes people make with this archetype",
                    "Consider whether multiple archetypes interact",
                ],
                style="diagnostic, pattern-focused, uses Senge's framework rigorously",
            ),
            directive_template="""**SYSTEM ARCHETYPE ANALYSIS**

**SYSTEM**: {system}

**OBSERVED PATTERN**: {pattern}

{context_section}

---

## 1. THE 10 SYSTEM ARCHETYPES — SCREENING

Evaluate each archetype against the observed pattern:

| # | Archetype | Match? | Confidence | Key Signal |
|---|-----------|--------|------------|------------|
| 1 | **Limits to Growth** — Success creates side effects that slow growth | [Yes/No/Partial] | [H/M/L] | [Evidence] |
| 2 | **Shifting the Burden** — A quick fix weakens the fundamental solution | [Yes/No/Partial] | [H/M/L] | [Evidence] |
| 3 | **Eroding Goals** — Pressure leads to lowering standards | [Yes/No/Partial] | [H/M/L] | [Evidence] |
| 4 | **Escalation** — Two parties each respond to the other's actions competitively | [Yes/No/Partial] | [H/M/L] | [Evidence] |
| 5 | **Success to the Successful** — Winner gets more resources, widening the gap | [Yes/No/Partial] | [H/M/L] | [Evidence] |
| 6 | **Tragedy of the Commons** — Individual overuse depletes shared resource | [Yes/No/Partial] | [H/M/L] | [Evidence] |
| 7 | **Fixes That Fail** — A fix works short-term but makes things worse long-term | [Yes/No/Partial] | [H/M/L] | [Evidence] |
| 8 | **Growth and Underinvestment** — Growth strains capacity, but investment is delayed | [Yes/No/Partial] | [H/M/L] | [Evidence] |
| 9 | **Accidental Adversaries** — Partners unintentionally undermine each other | [Yes/No/Partial] | [H/M/L] | [Evidence] |
| 10 | **Attractiveness Principle** — Resources flow to the most visible option | [Yes/No/Partial] | [H/M/L] | [Evidence] |

---

## 2. PRIMARY ARCHETYPE MATCH

### Archetype: [Name]

**Confidence**: [High / Medium / Low]

**Generic structure**:
```
[Reinforcing loop] → Growth / Action
        ↓
[Side effect / Delay]
        ↓
[Balancing loop] → Constraint / Unintended consequence
```

**Mapped to this system**:
- **Reinforcing loop**: [Specific to the system]
- **Balancing/limiting loop**: [Specific to the system]
- **Key delay**: [Where the lag occurs]
- **Trigger**: [What initiates the pattern]

---

## 3. BEHAVIORAL TRAJECTORY

**Phase 1 — Early**: [What the pattern looks like at the start]
**Phase 2 — Middle**: [How the pattern evolves]
**Phase 3 — Late**: [Where the pattern leads if unchecked]

**Current phase**: [Where is this system now?]

---

## 4. ARCHETYPE-SPECIFIC INTERVENTION

The known strategy for **[Archetype Name]**:

### What works:
- [Intervention 1]: [Why this addresses the root structure]
- [Intervention 2]: [Why this breaks the pattern]

### What doesn't work (common mistakes):
- [Typical mistake 1]: [Why it fails — usually pushes harder on the wrong loop]
- [Typical mistake 2]: [Why it backfires]

### Implementation sequence:
1. **Immediate**: [First step]
2. **Short-term** (1-3 months): [Next steps]
3. **Long-term** (3-12 months): [Structural changes]

---

## 5. SECONDARY ARCHETYPES

[If multiple archetypes interact, describe how they compound]

| Primary | Secondary | Interaction |
|---------|-----------|-------------|
| [Archetype A] | [Archetype B] | [How they reinforce or counteract each other] |

---

## 6. SUMMARY

**Primary archetype**: [Name] (Confidence: [H/M/L])
**Root cause**: [The structural element driving the pattern]
**Key leverage point**: [Where to intervene]
**Biggest mistake to avoid**: [The intuitive-but-wrong response]""",
            input_schema={
                "system": str,
                "pattern": str,
                "context_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "all_10_archetypes_screened",
                    "primary_archetype_match",
                    "structural_diagram",
                    "archetype_specific_intervention",
                ],
                must_not_include=[
                    "generic_advice_unlinked_to_archetype",
                    "skipping_archetype_screening",
                ],
                style_guide="Use Senge's archetype framework rigorously. Match structure, not just symptoms.",
            ),
        )

    def build_context(self, system="", pattern="", context="", **kwargs):
        """Build context for system archetype analysis."""
        context_section = f"**ADDITIONAL CONTEXT**: {context}" if context else ""
        kwargs.pop("context_section", None)
        return super().build_context(
            system=system, pattern=pattern, context_section=context_section, **kwargs
        )

    def execute(self, provider="gemini", system="", pattern="", context="", **kwargs):
        """Execute system archetype analysis."""
        return super().execute(
            provider=provider, system=system, pattern=pattern, context=context, **kwargs
        )


__all__ = ["SystemArchetypeAnalyzer"]
