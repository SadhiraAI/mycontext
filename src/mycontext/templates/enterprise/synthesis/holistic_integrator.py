"""
HolisticIntegrator Pattern (Enterprise)

Integrate multiple perspectives, data sources, and insights into coherent whole.
See the forest AND the trees - balance detail with big picture.

Research Foundation:
- von Bertalanffy, L. (1968). General System Theory.
- Senge, P. (1990). The Fifth Discipline: The Art and Practice of the Learning Organization.
- Systems thinking and holistic analysis frameworks.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class HolisticIntegrator(Pattern):
    """
    Integrate multiple perspectives into coherent whole.

    Integration Levels:
    - Data integration (combine information)
    - Conceptual integration (unify frameworks)
    - Perspective integration (multiple viewpoints)
    - System integration (see whole system)

    Use Cases:
    - Strategic planning
    - Research synthesis
    - Decision-making
    - System understanding

    Example:
        >>> from mycontext.templates.enterprise.synthesis import HolisticIntegrator
        >>>
        >>> pattern = HolisticIntegrator()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     topic="Company digital transformation",
        ...     perspectives="Technical, Business, Cultural, Customer"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert holistic systems integrator. Combine multiple perspectives into a "
        "coherent, unified understanding that reveals emergent insights.\n\n"
        "Topic: {topic}\n"
        "Perspectives: {perspectives}\n\n"
        "Deliver your analysis:\n"
        "(1) Analyze from each perspective — key concerns, insights, strengths, and blind spots.\n"
        "(2) Map cross-perspective connections — synergies, tensions, and integration points.\n"
        "(3) Identify emergent insights visible only through the combination of perspectives.\n"
        "(4) Resolve tensions — find higher-level views that reconcile conflicting perspectives.\n"
        "(5) Integrate across system levels: micro (elements), meso (interactions), macro (whole).\n"
        "(6) Synthesize a unified framework with leverage points for maximum impact.\n"
        "(7) Provide integrated recommendations that serve multiple perspectives simultaneously.\n\n"
        "Balance detail with big picture. No single perspective should dominate.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="holistic_integrator",
            description="Integrate multiple perspectives into coherent whole",
            version="1.0.0",
            tags=["synthesis", "enterprise", "integration", "holistic"],
            metadata={"category": "synthesis", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Holistic Systems Integrator",
                rules=[
                    "Consider multiple perspectives simultaneously",
                    "Find connections between disparate elements",
                    "Balance detail with big picture",
                    "Identify emergent properties of the whole",
                    "Create coherent unified understanding",
                ],
                style="integrative, comprehensive, balanced, systems-oriented",
            ),
            directive_template="""**HOLISTIC INTEGRATION**

**TOPIC/SYSTEM**: {topic}

**PERSPECTIVES TO INTEGRATE**: {perspectives}

---

## MULTI-PERSPECTIVE ANALYSIS

**Examine from each perspective**:

### PERSPECTIVE 1: [Name]

**View from this angle**:
- Key concerns: [What matters from this perspective]
- Insights: [What this view reveals]
- Strengths: [What this perspective sees well]
- Blind spots: [What this perspective misses]
- **Key takeaway**: [Main insight from this view]

---

### PERSPECTIVE 2: [Name]

[Same structure]

---

### PERSPECTIVE 3: [Name]

[Same structure]

---

### PERSPECTIVE 4: [Name]

[Same structure]

---

## CROSS-PERSPECTIVE CONNECTIONS

**How perspectives relate**:

**Connection 1**: [Perspective A ↔ Perspective B]
- **Link**: [How they connect]
- **Synergy**: [How they reinforce each other]
- **Tension**: [Where they conflict]
- **Integration**: [How to reconcile]

**Connection 2**: [Perspective A ↔ Perspective C]
[Same analysis]

**Connection 3**: [Perspective B ↔ Perspective D]
[Same analysis]

---

## EMERGENT INSIGHTS

**What emerges from integration** (not visible from single perspective):

**Emergent Insight 1**: [Holistic understanding]
- **Not visible from**: [Single perspective]
- **Emerges from**: [Combination of perspectives]
- **Significance**: [Why this matters]

**Emergent Insight 2**: [Another whole-system insight]
- **Synthesis**: [How this arises from integration]
- **Implication**: [What this means]

---

## TENSIONS AND TRADE-OFFS

**Where perspectives conflict**:

**Tension 1**: [Perspective A vs. Perspective B]
- **Conflict**: [Contradiction]
- **Root cause**: [Why they disagree]
- **Resolution**: [How to balance both]
- **Synthesis**: [Higher-level view that reconciles]

**Tension 2**: [Another tension]
[Same analysis]

---

## SYSTEM LEVELS

**Integrate across system levels**:

### MICRO LEVEL (Individual elements)
- **Elements**: [Components]
- **Details**: [Fine-grained view]
- **Mechanisms**: [How parts work]

### MESO LEVEL (Interactions)
- **Relationships**: [How elements connect]
- **Patterns**: [Interaction patterns]
- **Dynamics**: [How relationships evolve]

### MACRO LEVEL (Whole system)
- **Structure**: [Overall organization]
- **Behavior**: [System-level patterns]
- **Properties**: [Emergent characteristics]

### META LEVEL (Context)
- **Environment**: [External context]
- **Constraints**: [Boundary conditions]
- **Evolution**: [How system changes over time]

---

## INTEGRATION MAP

**Visual/conceptual map of integrated understanding**:

```
                [HOLISTIC VIEW]
                       ↑
        ┌──────────────┼──────────────┐
        │              │              │
   [Perspective A] [Perspective B] [Perspective C]
        │              │              │
        └──────────────┼──────────────┘
                       ↓
              [Emergent Insights]
                       ↓
              [Integrated Actions]
```

**Key connections**: [Major links in the system]

---

## DATA INTEGRATION

**Combine information from multiple sources**:

**Data Source 1**: [Source]
- **Contributes**: [What information]
- **Quality**: [Reliability]
- **Gaps**: [What's missing]

**Data Source 2**: [Source]
[Same structure]

**Integrated dataset**:
- **Completeness**: [Coverage]
- **Consistency**: [Conflicts resolved]
- **Insights from combination**: [What integrated data reveals]

---

## CONCEPTUAL INTEGRATION

**Unify frameworks and models**:

**Framework 1**: [Name]
- **Explains**: [What it covers]
- **Limitations**: [What it doesn't cover]

**Framework 2**: [Name]
- **Explains**: [Coverage]
- **Overlaps with Framework 1**: [Where they agree]
- **Extends Framework 1**: [What it adds]

**Integrated framework**:
- **Unified model**: [How frameworks combine]
- **Explanatory power**: [What integrated model explains]
- **New predictions**: [What unified view suggests]

---

## BALANCED SCORECARD

**Balance multiple dimensions**:

| Dimension | Status | Metric | Target | Gap | Priority |
|-----------|--------|--------|--------|-----|----------|
| [Dimension 1] | [Current] | [Measure] | [Goal] | [Difference] | [High/Med/Low] |
| [Dimension 2] | [Status] | [Metric] | [Target] | [Gap] | [Priority] |
| [Dimension 3] | [Status] | [Metric] | [Target] | [Gap] | [Priority] |
| [Dimension 4] | [Status] | [Metric] | [Target] | [Gap] | [Priority] |

**Overall balance**: [Assessment]

**Areas needing attention**: [Which dimensions]

---

## STAKEHOLDER INTEGRATION

**Integrate needs of all stakeholders**:

**Stakeholder 1**: [Name]
- **Needs**: [What they want]
- **Constraints**: [Their limitations]
- **Impact**: [How decisions affect them]

**Stakeholder 2**: [Name]
[Same structure]

**Integrated solution** (satisfies multiple stakeholders):
- [Solution that works for all]
- [Trade-offs made]
- [How different needs are balanced]

---

## TEMPORAL INTEGRATION

**Integrate across time**:

**Past** (historical context):
- [What history teaches]
- [Legacy issues]

**Present** (current state):
- [Current situation]
- [Immediate concerns]

**Future** (forward-looking):
- [Trends]
- [Future implications]

**Integrated timeline**: [How past → present → future connects]

---

## WHOLE-SYSTEM UNDERSTANDING

**Synthesized view of entire system**:

**System structure**:
- **Components**: [Key elements]
- **Relationships**: [How they connect]
- **Boundaries**: [System limits]

**System behavior**:
- **Dynamics**: [How system operates]
- **Feedback loops**: [Reinforcing/balancing]
- **Equilibria**: [Stable states]

**System evolution**:
- **Current trajectory**: [Where system is heading]
- **Drivers**: [What's driving change]
- **Possible futures**: [Different paths]

---

## SYNTHESIS STATEMENT

**Integrated understanding in clear language**:

**The big picture**: [Comprehensive view]

**Key themes**: [Main insights]
1. [Theme 1]
2. [Theme 2]
3. [Theme 3]

**Critical relationships**: [Most important connections]

**Leverage points**: [Where to intervene for maximum impact]

---

## INTEGRATED STRATEGY

**Strategy that addresses multiple perspectives**:

**Strategic direction**: [Unified approach]

**How it serves multiple perspectives**:
- Perspective A: [How strategy addresses this]
- Perspective B: [How strategy addresses this]
- Perspective C: [How strategy addresses this]

**Integration benefits**: [Advantages of holistic approach]

**Implementation**:
1. [Action 1 - serves [perspectives]]
2. [Action 2 - serves [perspectives]]
3. [Action 3 - serves [perspectives]]

---

## MONITORING HOLISTIC HEALTH

**Track system health across dimensions**:

**Health indicators**:
- [Indicator 1 - measures [dimension]]
- [Indicator 2 - measures [dimension]]
- [Indicator 3 - measures [dimension]]

**Balance check**: [Are all dimensions healthy?]

**Early warning**: [Signs of imbalance]

**Correction**: [How to rebalance]

---

## INTEGRATION QUALITY

**Assess quality of integration**:

✅ **Comprehensive**: All perspectives considered
✅ **Coherent**: Unified understanding achieved
✅ **Balanced**: No single perspective dominates
✅ **Actionable**: Clear implications for decisions
✅ **Emergent**: New insights from synthesis

**Areas for deeper integration**: [Where more work needed]

---

## RECOMMENDATIONS

**Based on holistic analysis**:

**Recommendation 1**: [Action]
- **Rationale**: [Why - addresses multiple perspectives]
- **Expected impact**: [Outcomes across dimensions]
- **Priority**: [High/Medium/Low]

**Recommendation 2**: [Action]
[Same structure]

**Recommendation 3**: [Action]
[Same structure]

---

## SUMMARY

**Integrated conclusion**:

**Holistic insight**: [Main takeaway from integration]

**Critical success factors**: [What matters most]

**Next steps**: [Immediate actions]

**Long-term vision**: [Where holistic approach leads]""",
            input_schema={"topic": str, "perspectives": str},
            constraints=Constraints(
                must_include=[
                    "multiple_perspectives",
                    "cross_perspective_connections",
                    "emergent_insights",
                    "integrated_strategy",
                ],
                must_not_include=["single_perspective_bias", "superficial_integration"],
                style_guide="Comprehensive and balanced. Multiple perspectives. Emergent insights. Coherent synthesis.",
            ),
        )

    def build_context(self, topic="", perspectives="", **kwargs):
        """Build context for holistic integration."""
        return super().build_context(topic=topic, perspectives=perspectives, **kwargs)

    def execute(self, provider="openai", topic="", perspectives="", **kwargs):
        """Execute holistic integration."""
        return super().execute(provider=provider, topic=topic, perspectives=perspectives, **kwargs)


__all__ = ["HolisticIntegrator"]
