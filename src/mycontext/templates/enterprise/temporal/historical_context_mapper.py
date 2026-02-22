"""
HistoricalContextMapper Pattern (Enterprise)

Understand present through historical patterns and precedents.
Map historical context to inform current decisions.

Research Foundation:
- Neustadt, R. E., & May, E. R. (1986). Thinking in time: The uses of history for decision makers.
- Tosh, J. (2010). The pursuit of history.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class HistoricalContextMapper(Pattern):
    """
    Understand present situation through historical context.
    
    Approach:
    - Identify historical parallels
    - Analyze what happened then
    - Extract lessons for now
    - Understand patterns across time
    
    Use Cases:
    - Strategic decisions
    - Policy analysis
    - Crisis management
    - Understanding current events
    
    Example:
        >>> from mycontext.templates.enterprise.temporal import HistoricalContextMapper
        >>> 
        >>> pattern = HistoricalContextMapper()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     current_situation="Economic recession with high inflation",
        ...     question="What can history teach us about this situation?"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert historian and strategic analyst. Understand the present situation "
        "through historical context, precedents, and pattern analysis.\n\n"
        "Current Situation: {current_situation}\n"
        "Question: {question}\n\n"
        "Deliver your analysis:\n"
        "(1) Identify 2-3 relevant historical precedents with surface and deep structural parallels.\n"
        "(2) For each precedent: what happened (short/medium/long-term), causal factors, key decisions.\n"
        "(3) Analyze recurring patterns across the historical examples.\n"
        "(4) Compare similarities vs. differences — what is the same and what has fundamentally changed.\n"
        "(5) Extract transferable lessons with confidence levels and important caveats.\n"
        "(6) Document what worked and what failed historically, and assess applicability now.\n"
        "(7) Provide history-informed recommendations: what to do, what to avoid, what to monitor.\n\n"
        "Use multiple examples, not single cases. Note differences as carefully as similarities.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="historical_context_mapper",
            description="Understand present through historical patterns",
            version="1.0.0",
            tags=["temporal", "enterprise", "history", "context"],
            metadata={
                "category": "temporal",
                "license": "enterprise",
                "tier": "enterprise"
            },
            guidance=Guidance(
                role="Historian and Strategic Analyst",
                rules=[
                    "Identify truly relevant historical parallels (not superficial similarities)",
                    "Understand context differences (past ≠ present exactly)",
                    "Extract transferable lessons, not rigid rules",
                    "Consider multiple historical examples",
                    "Note both similarities AND differences"
                ],
                style="analytical, contextual, nuanced, evidence-based"
            ),
            directive_template="""**HISTORICAL CONTEXT MAPPING**

**CURRENT SITUATION**: {current_situation}

**QUESTION**: {question}

---

## HISTORICAL PRECEDENTS

**Identify relevant historical parallels**:

### PRECEDENT 1: [Historical event/period]

**When**: [Time period]

**Surface similarities** to current situation:
- [Similarity 1]
- [Similarity 2]
- [Similarity 3]

**Deeper structural parallels**:
- [Underlying pattern shared]
- [Causal mechanism in common]

**What happened**:
- Short-term: [Immediate outcomes]
- Medium-term: [Effects over years]
- Long-term: [Lasting impact]

**Why it happened** (causal factors):
1. [Factor 1]
2. [Factor 2]
3. [Factor 3]

**Key actors and decisions**:
- Who: [Decision-makers]
- What: [Critical choices made]
- Impact: [How decisions shaped outcome]

---

### PRECEDENT 2: [Another historical parallel]

[Same structure as Precedent 1]

---

### PRECEDENT 3: [Third example]

[Same structure]

---

## PATTERN ANALYSIS ACROSS HISTORY

**Recurring pattern identified**:
[What happens repeatedly across these historical examples]

**Common elements**:
- Condition A: [Present in all cases]
- Condition B: [Shared factor]
- Mechanism: [How pattern unfolds]

**Variations**:
- When outcome was X: [Conditions leading to X]
- When outcome was Y: [Different conditions → different result]

**Lesson**: [What history teaches about this pattern]

---

## SIMILARITIES VS. DIFFERENCES

**How current situation resembles history**:

**Similarities** (what's the same):
1. [Structural similarity]
2. [Causal similarity]
3. [Contextual similarity]

**Why these similarities matter**: [Implications]

---

**How current situation differs from history**:

**Differences** (what's changed):
1. [Technology difference]
2. [Social/political difference]
3. [Scale/scope difference]
4. [Knowledge/capability difference]

**Why these differences matter**: [How they might change outcomes]

---

## LESSONS FROM HISTORY

**Lesson 1**: [Transferable insight]
- Historical evidence: [What happened multiple times]
- Application to present: [How to apply now]
- Confidence: [High/Medium/Low]
- Caveat: [Important difference to consider]

**Lesson 2**: [Another lesson]
- Evidence: [Historical basis]
- Application: [Current use]
- Confidence: [Level]

**Lesson 3**: [Third insight]
[Same structure]

---

## WHAT WORKED / WHAT FAILED

**Historically successful responses**:

**Strategy A**: [What was tried]
- Context: [When/where]
- Outcome: [Success]
- Why it worked: [Mechanism]
- **Applicability now**: [Can we use this? How?]

**Strategy B**: [Another successful approach]
[Same analysis]

---

**Historically failed responses**:

**Mistake A**: [What was tried]
- Context: [When/where]
- Outcome: [Failure]
- Why it failed: [Reason]
- **Avoid now**: [How to not repeat this mistake]

**Mistake B**: [Another failure]
[Same analysis]

---

## HISTORICAL TRAJECTORIES

**Common paths this type of situation has taken**:

**Path 1**: [Trajectory A]
- Frequency: [How often in history]
- Conditions: [When this path was taken]
- Outcome: [Where it led]
- **Likelihood now**: [%]

**Path 2**: [Trajectory B]
- Frequency: [Historical occurrence]
- Conditions: [Different conditions]
- Outcome: [Different result]
- **Likelihood now**: [%]

**Path 3**: [Trajectory C]
[Same structure]

---

## HISTORICAL CONTEXT FOR DECISION-MAKING

**Inform current choices with historical wisdom**:

**Decision point**: [Current choice to make]

**Historical analogy**: [Similar decision in past]
- What they chose: [Decision]
- Why: [Reasoning]
- Outcome: [Result]
- **Implication for us**: [What to learn]

---

## CONTEMPORARY UNIQUENESS

**What's genuinely NEW about current situation** (no historical parallel):

**Novel element 1**: [Something unprecedented]
- Why unprecedented: [Never happened before]
- Uncertainty: [Can't rely on history for this]

**Novel element 2**: [Another new factor]

**Implication**: [Where history can't fully guide us]

---

## SYNTHESIS: HISTORY-INFORMED PERSPECTIVE

**What history teaches about current situation**:

**High confidence lessons** (strong historical pattern):
- [Lesson with clear precedent]

**Medium confidence lessons** (some historical support):
- [Lesson with partial precedent]

**Uncertain** (no clear historical guidance):
- [Area where history is ambiguous or irrelevant]

**Recommended approach**:
- Apply: [Historical lessons to use]
- Adapt: [Adjust for current differences]
- Innovate: [Where history doesn't apply]

---

## CRITICAL CAUTIONS

**Dangers of historical reasoning**:

❌ **False analogy**: Assuming past = present when key differences exist
❌ **Confirmation bias**: Cherry-picking history that supports preferred view  
❌ **Determinism**: Assuming history must repeat

✅ **Proper use of history**:
- Source of insights, not rigid rules
- Multiple examples, not single case
- Understand context deeply
- Note similarities AND differences

---

## IMMEDIATE RECOMMENDATIONS

**Based on historical analysis**:

**Do** (history shows this works):
1. [Action 1]
2. [Action 2]

**Avoid** (history shows this fails):
1. [Mistake to avoid]
2. [Another pitfall]

**Monitor** (early warning signs):
1. [Indicator from history]
2. [Pattern to watch for]""",
            input_schema={
                "current_situation": str,
                "question": str
            },
            constraints=Constraints(
                must_include=[
                    "historical_precedents",
                    "lessons_learned",
                    "similarities_and_differences",
                    "transferable_insights"
                ],
                must_not_include=[
                    "false_analogies",
                    "historical_determinism"
                ],
                style_guide="Analytical and contextual. Multiple precedents. Note differences. Transferable lessons."
            )
        )

    def build_context(self, current_situation="", question="", **kwargs):
        """Build context for historical analysis."""
        return super().build_context(
            current_situation=current_situation,
            question=question,
            **kwargs
        )

    def execute(self, provider="openai", current_situation="", question="", **kwargs):
        """Execute historical context mapping."""
        return super().execute(
            provider=provider,
            current_situation=current_situation,
            question=question,
            **kwargs
        )


__all__ = ["HistoricalContextMapper"]
