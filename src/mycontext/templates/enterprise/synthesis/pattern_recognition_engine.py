"""
PatternRecognitionEngine Pattern (Enterprise)

Identify recurring patterns across data, events, and systems.
Find hidden structures and regularities.

Research Foundation:
- Simon, H. A. (1969). The sciences of the artificial.
- Alexander, C. (1979). The timeless way of building.
- Data mining and pattern recognition research.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class PatternRecognitionEngine(Pattern):
    """
    Identify recurring patterns and structures.

    Pattern Types:
    - Structural patterns (how things are organized)
    - Behavioral patterns (how things act)
    - Temporal patterns (how things change over time)
    - Relational patterns (how things connect)

    Use Cases:
    - Data analysis
    - System understanding
    - Trend identification
    - Insight generation

    Example:
        >>> from mycontext.templates.enterprise.synthesis import PatternRecognitionEngine
        >>>
        >>> pattern = PatternRecognitionEngine()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     data="Customer churn data: 500 cases with demographics, usage, support tickets",
        ...     pattern_focus="Why customers leave"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert pattern recognition analyst. Identify recurring patterns, hidden "
        "structures, and meaningful regularities in the given data.\n\n"
        "Data: {data}\n"
        "Pattern Focus: {pattern_focus}\n\n"
        "Deliver your analysis:\n"
        "(1) Identify structural patterns — how elements are organized, with frequency and examples.\n"
        "(2) Detect behavioral patterns — triggers, sequences, and outcomes of recurring behaviors.\n"
        "(3) Find temporal patterns — trends, cycles, seasonality, and periodicity.\n"
        "(4) Map relational patterns — how elements connect and influence each other.\n"
        "(5) Quantify pattern strength — frequency, consistency, and statistical significance.\n"
        "(6) Uncover hidden patterns that are not immediately obvious, with discovery evidence.\n"
        "(7) Distinguish signal from noise. Provide pattern-based predictions and actionable insights.\n\n"
        "Be analytical and systematic. Explain why patterns occur, not just that they exist.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="pattern_recognition_engine",
            description="Identify recurring patterns across data and systems",
            version="1.0.0",
            tags=["synthesis", "enterprise", "patterns", "recognition"],
            metadata={"category": "synthesis", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Pattern Recognition and Data Analysis Expert",
                rules=[
                    "Identify multiple types of patterns (structural, behavioral, temporal)",
                    "Distinguish signal from noise",
                    "Quantify pattern strength and significance",
                    "Find both obvious and hidden patterns",
                    "Explain why patterns occur",
                ],
                style="analytical, systematic, insightful, quantitative",
            ),
            directive_template="""**PATTERN RECOGNITION ANALYSIS**

**DATA/DOMAIN**: {data}

**PATTERN FOCUS**: {pattern_focus}

---

## PATTERN TYPES TO IDENTIFY

**Analyze across multiple dimensions**:

### 1. STRUCTURAL PATTERNS

**How elements are organized**:

**Pattern A**: [Structural pattern name]
- **Structure**: [How things are arranged]
- **Instances**: [Where this appears]
  - Example 1: [Specific case]
  - Example 2: [Another case]
  - Example 3: [Third case]
- **Frequency**: [How often: X% of cases]
- **Why this structure**: [Reason for this organization]

**Pattern B**: [Another structural pattern]
[Same analysis]

---

### 2. BEHAVIORAL PATTERNS

**How elements behave or act**:

**Pattern A**: [Behavioral pattern name]
- **Behavior**: [What happens]
- **Trigger**: [What causes this behavior]
- **Sequence**: [Steps in the pattern]
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- **Instances**: [Where this occurs]
- **Frequency**: [How often]
- **Outcome**: [Result of this behavior]

**Pattern B**: [Another behavioral pattern]
[Same analysis]

---

### 3. TEMPORAL PATTERNS

**How things change over time**:

**Pattern A**: [Temporal pattern name]
- **Type**: [Trend/Cycle/Seasonality/Rhythm]
- **Description**: [What changes and how]
- **Timeline**: [When/how long]
- **Examples**:
  - Time period 1: [Instance]
  - Time period 2: [Recurrence]
  - Time period 3: [Recurrence]
- **Frequency**: [Periodicity if cyclical]
- **Driving factors**: [What causes this pattern]

**Pattern B**: [Another temporal pattern]
[Same analysis]

---

### 4. RELATIONAL PATTERNS

**How elements connect and relate**:

**Pattern A**: [Relational pattern name]
- **Relationship type**: [How elements connect]
- **Network structure**: [Topology]
- **Examples**:
  - [Entity A] ↔ [Entity B]: [Relationship]
  - [Entity C] ↔ [Entity D]: [Same pattern]
- **Frequency**: [How common]
- **Significance**: [Why this relationship matters]

**Pattern B**: [Another relational pattern]
[Same analysis]

---

## PATTERN HIERARCHY

**Patterns within patterns** (nested structure):

**Meta-pattern**: [Higher-level pattern]
- Contains sub-patterns:
  1. [Sub-pattern 1]
  2. [Sub-pattern 2]
  3. [Sub-pattern 3]
- **Relationship**: [How sub-patterns relate to meta-pattern]

---

## PATTERN STRENGTH ANALYSIS

**Quantify how strong each pattern is**:

| Pattern | Frequency | Consistency | Significance | Strength |
|---------|-----------|-------------|--------------|----------|
| [Pattern 1] | [X%] | [High/Med/Low] | [p-value/effect size] | [Strong/Moderate/Weak] |
| [Pattern 2] | [X%] | [Consistency] | [Statistical sig] | [Strength] |
| [Pattern 3] | [X%] | [Consistency] | [Significance] | [Strength] |

**Strongest patterns**: [Which patterns are most robust]

**Weak patterns** (possible noise): [Which might be random]

---

## HIDDEN PATTERNS

**Non-obvious patterns discovered**:

**Hidden pattern 1**: [Surprising discovery]
- **Why hidden**: [Not immediately obvious]
- **Discovery method**: [How we found it]
- **Evidence**: [Supporting data]
- **Implication**: [What this reveals]

**Hidden pattern 2**: [Another non-obvious pattern]
[Same analysis]

---

## PATTERN EXCEPTIONS

**Cases that don't fit the patterns**:

**Exception type 1**: [Outlier category]
- Instances: [Specific cases]
- Frequency: [X% of data]
- **Why exception**: [What makes these different]
- **Implication**: [What exceptions teach us]

**Important insight from exceptions**: [What outliers reveal]

---

## CAUSAL PATTERNS

**Patterns that suggest causation** (not just correlation):

**Causal pattern 1**: [X → Y]
- **Hypothesis**: [X causes Y]
- **Evidence**:
  - Temporal: [X precedes Y]
  - Consistency: [When X, then Y]
  - Mechanism: [How X could cause Y]
  - Dose-response: [More X → More Y]
- **Confidence**: [High/Medium/Low]

**Causal pattern 2**: [Another causal relationship]
[Same analysis]

---

## PATTERN INTERACTIONS

**How patterns combine and interact**:

**Interaction 1**: [Pattern A + Pattern B]
- **Type**: [Reinforcing/Balancing/Independent]
- **Effect**: [Combined effect stronger/weaker/different]
- **Examples**: [Where this interaction occurs]

**Interaction 2**: [Another interaction]
[Same analysis]

---

## PATTERN-BASED PREDICTIONS

**Use patterns to predict**:

**Prediction 1**: Based on [Pattern X]
- **Predict**: [What should happen]
- **When**: [Timeline]
- **Confidence**: [%]
- **Test**: [How to verify prediction]

**Prediction 2**: Based on [Pattern Y]
[Same structure]

---

## PATTERN DRIVERS

**Why do these patterns exist?**

**Pattern 1 drivers**:
- **Root cause**: [Underlying reason]
- **Enabling factors**: [What allows this pattern]
- **Reinforcing loops**: [What keeps pattern going]

**Pattern 2 drivers**:
[Same analysis]

---

## ACTIONABLE INSIGHTS

**What patterns tell us**:

**Insight 1**: [Key finding from patterns]
- **Evidence**: [Which patterns support this]
- **Implication**: [What to do about it]
- **Action**: [Specific recommendation]

**Insight 2**: [Another insight]
[Same structure]

**Insight 3**: [Third insight]
[Same structure]

---

## PATTERN VISUALIZATION

**Visual representation of patterns**:

```
[Diagram/chart showing main patterns]

Example:
Pattern A: ████████████░░░░ (75%)
Pattern B: ██████░░░░░░░░░░ (40%)
Pattern C: ███████████████░ (95%)

Timeline:
T1 ----[Pattern A appears]----
T2 -------[Pattern B]----------
T3 ----[Patterns overlap]------
     ↓         ↓          ↓
  [Effect1] [Effect2] [Result]
```

---

## PATTERN LIBRARY

**Document discovered patterns** (for future reference):

**Pattern name**: [Descriptive name]
- **Type**: [Structural/Behavioral/Temporal/Relational]
- **Description**: [What it is]
- **Conditions**: [When it appears]
- **Frequency**: [How often]
- **Significance**: [Why it matters]
- **Examples**: [Instances]

[Repeat for each significant pattern]

---

## PATTERN-BASED STRATEGY

**Leverage patterns for decisions**:

**Strategy 1**: [Based on Pattern X]
- **Approach**: [How to use this pattern]
- **Expected outcome**: [What to achieve]

**Strategy 2**: [Based on Pattern Y]
- **Approach**: [Different strategy]
- **Expected outcome**: [Result]

---

## SUMMARY

**Key patterns identified**: [Count]

**Strongest patterns**:
1. [Pattern 1 - Frequency X%, Strength: Strong]
2. [Pattern 2 - Frequency Y%, Strength: Strong]

**Most surprising pattern**: [Which one was unexpected]

**Most actionable pattern**: [Which has clearest implications]

**Recommended next steps**: [What to do with these patterns]""",
            input_schema={"data": str, "pattern_focus": str},
            constraints=Constraints(
                must_include=[
                    "multiple_pattern_types",
                    "pattern_strength",
                    "hidden_patterns",
                    "actionable_insights",
                ],
                must_not_include=["pattern_overfitting", "seeing_patterns_in_noise"],
                style_guide="Analytical and systematic. Multiple pattern types. Quantified strength. Actionable insights.",
            ),
        )

    def build_context(self, data="", pattern_focus="", **kwargs):
        """Build context for pattern recognition."""
        return super().build_context(data=data, pattern_focus=pattern_focus, **kwargs)

    def execute(self, provider="openai", data="", pattern_focus="", **kwargs):
        """Execute pattern recognition analysis."""
        return super().execute(provider=provider, data=data, pattern_focus=pattern_focus, **kwargs)


__all__ = ["PatternRecognitionEngine"]
