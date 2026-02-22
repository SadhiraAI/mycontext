"""
EmergenceDetector Pattern (Enterprise)

Identify emergent properties arising from system component interactions.

Research Foundation:
- Holland, J. H. (1998). Emergence: From Chaos to Order.
- Johnson, S. (2001). Emergence: The Connected Lives of Ants, Brains, Cities, and Software.
- Bar-Yam, Y. (1997). Dynamics of Complex Systems.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class EmergenceDetector(Pattern):
    """
    Identify emergent properties that arise from interactions between system components.

    Emergence occurs when a system exhibits properties that none of its individual
    parts possess — the whole becomes more (or different) than the sum of its parts.

    Use Cases:
    - Organizational culture analysis (culture emerges from individual behaviors)
    - Market dynamics (market trends emerge from individual transactions)
    - Technology ecosystem evolution (platform effects emerge from user interactions)
    - Team dynamics (team capability emerges from individual skills + interactions)

    Example:
        >>> from mycontext.templates.enterprise.systems_thinking import EmergenceDetector
        >>>
        >>> pattern = EmergenceDetector()
        >>> context = pattern.build_context(
        ...     system="Remote-first engineering team of 50 across 8 time zones",
        ...     components="Async communication, code reviews, stand-ups, documentation, social channels"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a complex systems analyst specializing in emergence. Detect "
        "emergent properties arising from component interactions.\n\n"
        "System: {system}\n"
        "Components: {components}\n"
        "{context_section}\n\n"
        "Perform emergence analysis: (1) Catalog each component and its properties "
        "in isolation. (2) Map interactions between components — cooperation, "
        "competition, information flows, and constraints. (3) Identify emergent "
        "properties of the whole that no individual part possesses. (4) For each "
        "emergent property, trace the specific micro-interactions producing the "
        "macro-level property. (5) Classify emergence type: weak (predictable from "
        "parts) vs strong (surprising). (6) Assess whether each property is "
        "beneficial or harmful. (7) Suggest interventions targeting interactions to "
        "nurture beneficial or dampen harmful emergence.\n\n"
        "Remember: emergent properties cannot be controlled directly — only the "
        "underlying interactions can be changed.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="emergence_detector",
            description="Identify emergent properties from system component interactions",
            version="1.0.0",
            tags=["systems-thinking", "enterprise", "emergence", "complexity"],
            metadata={
                "category": "systems_thinking",
                "license": "enterprise",
                "tier": "enterprise",
            },
            guidance=Guidance(
                role="Complex Systems Analyst specializing in emergence and self-organization",
                rules=[
                    "Distinguish clearly between properties of parts vs properties of the whole",
                    "Identify the specific INTERACTIONS that give rise to emergent properties",
                    "Classify emergence type: weak (predictable) vs strong (surprising)",
                    "Assess whether emergent properties are beneficial or harmful",
                    "Suggest how to nurture beneficial emergence or dampen harmful emergence",
                    "Consider multiple scales — emergence at team, department, and organization level",
                ],
                style="analytical, multi-scale, traces causation from micro to macro",
            ),
            directive_template="""**EMERGENCE ANALYSIS**

**SYSTEM**: {system}

**COMPONENTS**: {components}

{context_section}

---

## 1. COMPONENT INVENTORY

Map each component and its individual properties in isolation:

| Component | Individual Properties | Behavior in Isolation |
|-----------|----------------------|-----------------------|
| [Component 1] | [What it does alone] | [How it behaves without others] |

---

## 2. INTERACTION MAP

Identify how components interact with each other:

| Component A | Component B | Interaction Type | Frequency | Strength |
|-------------|-------------|-----------------|-----------|----------|
| [A] | [B] | [Cooperation / Competition / Information flow / Constraint] | [High/Med/Low] | [Strong/Weak] |

**Key interaction patterns**:
- [Cluster 1]: [Which components interact most tightly?]
- [Cluster 2]: [Which components are loosely coupled?]
- [Bridges]: [Which components connect otherwise separate clusters?]

---

## 3. EMERGENT PROPERTIES

Properties of the WHOLE system that no individual component possesses:

### Emergent Property 1: [Name]
- **Description**: [What is this property?]
- **Type**: [Weak emergence (predictable from parts) / Strong emergence (surprising)]
- **Arises from**: [Which specific interactions produce this?]
- **Mechanism**: [Step-by-step: how do micro-interactions create macro-property?]
- **Observable evidence**: [How do you see/measure this property?]
- **Value**: [Beneficial / Harmful / Neutral] — [Why?]

### Emergent Property 2: [Name]
[Continue for all identified emergent properties...]

---

## 4. EMERGENCE CLASSIFICATION

| Property | Type | Source Interactions | Beneficial? | Controllable? |
|----------|------|-------------------|-------------|---------------|
| [Property 1] | [Weak/Strong] | [Interactions] | [Yes/No/Mixed] | [High/Low/None] |

---

## 5. MULTI-SCALE ANALYSIS

Emergence often occurs at multiple levels:

**Micro level** (individual components):
- [What patterns appear at the smallest scale?]

**Meso level** (clusters/teams):
- [What emerges at the group level?]

**Macro level** (entire system):
- [What system-wide properties emerge?]

**Cross-scale effects**:
- [How does micro behavior shape macro properties?]
- [How do macro properties constrain micro behavior?]

---

## 6. INTERVENTION STRATEGIES

### To NURTURE beneficial emergence:
| Emergent Property | Intervention | Mechanism |
|-------------------|-------------|-----------|
| [Beneficial property] | [Action to strengthen it] | [How this helps the interaction pattern] |

### To DAMPEN harmful emergence:
| Emergent Property | Intervention | Mechanism |
|-------------------|-------------|-----------|
| [Harmful property] | [Action to weaken it] | [How this disrupts the interaction pattern] |

**Warning**: Direct control of emergent properties is usually impossible.
Interventions must target the interactions, not the emergent property itself.

---

## 7. SUMMARY

**Key emergent properties**: [List the most significant ones]
**Dominant emergence type**: [Weak / Strong / Mixed]
**Most impactful finding**: [The single most important emergent property]
**Recommended focus**: [Which interactions to nurture or dampen]""",
            input_schema={
                "system": str,
                "components": str,
                "context_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "component_analysis",
                    "interaction_mapping",
                    "emergent_properties_identification",
                    "micro_to_macro_mechanism",
                ],
                must_not_include=[
                    "conflating_component_properties_with_emergent_properties",
                    "listing_properties_without_explaining_how_they_emerge",
                ],
                style_guide="Always trace the path from component interactions to emergent property. Whole > sum of parts.",
            ),
        )

    def build_context(self, system="", components="", context="", **kwargs):
        """Build context for emergence analysis."""
        context_section = f"**ADDITIONAL CONTEXT**: {context}" if context else ""
        kwargs.pop("context_section", None)
        return super().build_context(
            system=system,
            components=components,
            context_section=context_section,
            **kwargs,
        )

    def execute(self, provider="gemini", system="", components="", context="", **kwargs):
        """Execute emergence analysis."""
        return super().execute(
            provider=provider,
            system=system,
            components=components,
            context=context,
            **kwargs,
        )


__all__ = ["EmergenceDetector"]
