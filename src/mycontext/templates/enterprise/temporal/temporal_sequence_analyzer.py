"""
TemporalSequenceAnalyzer Pattern (Enterprise)

Analyze events across time to identify patterns, trends, and causal sequences.
Implements temporal reasoning and time-series analysis principles.

Research Foundation:
- Allen, J. F. (1983). Maintaining knowledge about temporal intervals.
- Klein, G. (1989). Recognition-primed decisions. Advances in man-machine systems research.

License: Enterprise
"""

from mycontext import Pattern, Guidance, Constraints

class TemporalSequenceAnalyzer(Pattern):
    """
    Analyze temporal sequences to identify patterns and causality.
    
    Capabilities:
    - Chronological ordering
    - Pattern identification across time
    - Trend analysis
    - Causal sequence detection
    - Temporal relationships (before, after, during, overlaps)
    
    Use Cases:
    - Historical analysis
    - Timeline construction
    - Event sequence understanding
    - Trend forecasting
    
    Example:
        >>> from mycontext.templates.enterprise.temporal import TemporalSequenceAnalyzer
        >>> 
        >>> pattern = TemporalSequenceAnalyzer()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     events="Company layoffs, stock price drop, CEO resignation",
        ...     time_span="Last 6 months"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert temporal analyst specializing in event sequence analysis and causality "
        "detection. Analyze the given events across time to identify patterns and causal relationships.\n\n"
        "Events: {events}\n"
        "Time Span: {time_span}\n"
        "{context_section}\n\n"
        "Deliver your analysis:\n"
        "(1) Establish precise chronological order with dates, durations, and temporal relationships.\n"
        "(2) Map temporal relationships — sequential, concurrent, and nested events.\n"
        "(3) Identify recurring patterns, cycles, and trends across the timeline.\n"
        "(4) Analyze causality — which earlier events likely caused later ones, with evidence.\n"
        "(5) Identify critical turning points and tipping moments in the sequence.\n"
        "(6) Provide forecasting implications — what temporal patterns suggest about the future.\n\n"
        "Be chronologically precise. Distinguish correlation from causation with evidence.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="temporal_sequence_analyzer",
            description="Analyze events across time to identify patterns and causality",
            version="1.0.0",
            tags=["temporal", "enterprise", "time-series", "causality"],
            metadata={
                "category": "temporal",
                "license": "enterprise",
                "tier": "enterprise"
            },
            guidance=Guidance(
                role="Temporal Analysis Expert and Historian",
                rules=[
                    "Establish clear chronological order",
                    "Identify temporal relationships (before/after/during/overlaps)",
                    "Distinguish correlation from causation",
                    "Recognize patterns and trends over time",
                    "Consider multiple timescales (immediate, medium, long-term)"
                ],
                style="analytical, precise, chronological, evidence-based"
            ),
            directive_template="""**TEMPORAL SEQUENCE ANALYSIS**

**EVENTS TO ANALYZE**: {events}

**TIME SPAN**: {time_span}

{context_section}

---

## CHRONOLOGICAL TIMELINE

**Establish precise temporal order**:

**Time T1** (earliest):
- Event: [What happened]
- Date/Period: [When]
- Duration: [How long]
- Key actors: [Who involved]

**Time T2**:
- Event: [What happened]
- Date/Period: [When]
- Duration: [How long]
- Temporal relation to T1: [X days/months after, overlaps with, etc.]

**Time T3**:
- Event: [What happened]
- Date/Period: [When]
- Temporal relation to previous: [Relationship]

[Continue for all events]

---

## TEMPORAL RELATIONSHIPS

**Map how events relate in time**:

**Sequential** (A then B):
- [Event A] → [Event B]
- Time gap: [Duration between]
- Relationship: [A preceded B by X time]

**Concurrent** (A and B simultaneously):
- [Event A] overlaps with [Event B]
- Overlap period: [Duration]

**Nested** (A during B):
- [Event A] occurred within timeframe of [Event B]
- Context: [B was the larger context for A]

---

## PATTERN IDENTIFICATION

**Recurring patterns across time**:

**Pattern 1**: [Description]
- Instances: [When it occurred: T1, T3, T5]
- Frequency: [How often]
- Context: [Conditions when it appears]

**Pattern 2**: [Description]
- Instances: [When]
- Regularity: [Periodic/Irregular]

**Cycles**: [Any cyclical patterns]
- Period: [Length of cycle]
- Amplitude: [Intensity variation]

---

## TREND ANALYSIS

**Direction over time**:

**Increasing trends**:
- What's growing: [Metric/phenomenon]
- Rate: [Speed of increase]
- Inflection points: [Where trend changed]

**Decreasing trends**:
- What's declining: [Metric]
- Rate: [Speed]
- Stabilization: [Where trend levels off]

**Stable periods**:
- What remained constant: [Metric]
- Duration: [How long stable]

---

## CAUSAL ANALYSIS

**Temporal causality** (earlier events → later effects):

**Likely causal sequence**:
1. [Event A at T1] → [Event B at T2]
   - Evidence of causation: [Why A likely caused B]
   - Mechanism: [How A led to B]
   - Time lag: [Delay between cause and effect]

2. [Event B] → [Event C]
   - Causal chain: [How effects propagate]

**Correlation vs. Causation**:
- Correlated but not causal: [Events that co-occur but don't cause each other]
- Confounding factors: [Third variables affecting both]

---

## CRITICAL MOMENTS

**Turning points in the sequence**:

**Decision point**: [Time when path diverged]
- What happened: [Event]
- Alternatives: [What could have happened instead]
- Impact: [How it shaped later events]

**Tipping point**: [When gradual change became rapid]
- Buildup: [Slow accumulation before]
- Trigger: [What caused acceleration]
- Cascade: [Rapid effects after]

---

## TEMPORAL CONTEXT

**Understanding events in their time context**:

**Historical precedents**:
- Similar past events: [When/what]
- Outcomes then: [What happened]
- Lessons: [What history teaches]

**Contemporary factors**:
- What else was happening: [Concurrent events]
- Environment: [Conditions at the time]
- Constraints: [Temporal limitations]

---

## FORECASTING IMPLICATIONS

**What temporal patterns suggest about future**:

**If current trends continue**:
- Short-term (next period): [Prediction]
- Medium-term: [Projection]
- Long-term: [Extrapolation]

**Pattern-based predictions**:
- If pattern recurs: [What to expect]
- Cycle timing: [When next occurrence]

**Warning signs to monitor**:
- Leading indicators: [Early signals]
- Trigger conditions: [What would change trajectory]

---

## TIMELINE VISUALIZATION

**Temporal map of events**:

```
T1 ----[Event A]----
T2 -------[Event B]-------------[Event C]----
T3 ----[Event D (during B)]----
T4 ----------------[Event E]----
      ↓         ↓           ↓
   [Pattern] [Trend]   [Consequence]
```

**Key**:
- Horizontal: Time progression
- Vertical alignment: Concurrent events
- Arrows: Causal relationships

---

## SYNTHESIS

**Overall temporal narrative**:

**The sequence shows**: [Summary of pattern]

**Key insight**: [What temporal analysis reveals]

**Critical periods**: [Most important timeframes]

**Causality summary**: [How events drove each other]""",
            input_schema={
                "events": str,
                "time_span": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=[
                    "chronological_order",
                    "temporal_relationships",
                    "pattern_identification",
                    "causal_analysis"
                ],
                must_not_include=[
                    "temporal_confusion",
                    "causation_without_evidence"
                ],
                style_guide="Chronological and precise. Clear temporal relationships. Evidence-based causality."
            )
        )
    
    def build_context(self, events="", time_span="", context="", **kwargs):
        """Build context for temporal sequence analysis."""
        context_section = f"**CONTEXT**: {context}" if context else ""
        kwargs.pop('context_section', None)
        
        return super().build_context(
            events=events,
            time_span=time_span,
            context_section=context_section,
            **kwargs
        )
    
    def execute(self, provider="openai", events="", time_span="", context="", **kwargs):
        """Execute temporal sequence analysis."""
        context_section = f"**CONTEXT**: {context}" if context else ""
        kwargs.pop('context_section', None)
        
        return super().execute(
            provider=provider,
            events=events,
            time_span=time_span,
            context_section=context_section,
            **kwargs
        )


__all__ = ["TemporalSequenceAnalyzer"]
