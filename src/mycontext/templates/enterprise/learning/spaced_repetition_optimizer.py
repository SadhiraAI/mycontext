"""
SpacedRepetitionOptimizer Pattern (Enterprise)

Optimal timing for review based on forgetting curves and spaced repetition research.
Implements Ebbinghaus forgetting curve and modern SR algorithms.

Research Foundation:
- Ebbinghaus, H. (1885). Memory: A contribution to experimental psychology.
- Cepeda, N. J., et al. (2006). Distributed practice in verbal recall tasks: A review.
- Karpicke, J. D., & Roediger, H. L. (2008). The critical importance of retrieval for learning.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class SpacedRepetitionOptimizer(Pattern):
    """
    Optimize review timing based on forgetting curves.

    Implements:
    - Ebbinghaus forgetting curve
    - SuperMemo SM-2 algorithm principles
    - Retrieval practice effects

    Use Cases:
    - Flashcard systems (Anki, Quizlet)
    - Language learning apps
    - Medical education
    - Skill retention programs

    Example:
        >>> from mycontext.templates.enterprise.learning import SpacedRepetitionOptimizer
        >>>
        >>> pattern = SpacedRepetitionOptimizer()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     learning_material="Spanish vocabulary: 50 new words",
        ...     initial_mastery="Just learned today"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a memory science expert applying Ebbinghaus' forgetting curve "
        "and modern spaced repetition research. Optimize review timing for "
        "long-term retention.\n\n"
        "Learning Material: {learning_material}\n"
        "Initial Mastery: {initial_mastery}\n"
        "{context_section}\n\n"
        "Design an optimal spaced repetition schedule: (1) Assess material "
        "difficulty and expected forgetting rate. (2) Schedule reviews at expanding "
        "intervals — Review 1 at 1 day, Review 2 at 3-7 days, Review 3 at 2-4 "
        "weeks, then exponentially increasing (months, then annually). "
        "(3) Design retrieval practice for each review — use free recall, cued "
        "recall, and application problems instead of passive re-reading. "
        "(4) Define performance-based adjustments: strong performance (>90%) "
        "increases the interval, weak performance (<70%) decreases it. "
        "(5) Provide a concrete implementation calendar with dates and activities.\n\n"
        "Emphasize active retrieval over re-reading. Include tracking metrics "
        "(success rate, confidence, recall speed) for ongoing adjustment.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="spaced_repetition_optimizer",
            description="Optimize review timing based on forgetting curves",
            version="1.0.0",
            tags=["learning", "enterprise", "spaced-repetition", "memory"],
            metadata={"category": "learning", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Memory Science Expert and Learning Optimizer",
                rules=[
                    "Apply Ebbinghaus forgetting curve principles",
                    "Space reviews at optimal intervals (not too early, not too late)",
                    "Account for difficulty and retrieval success",
                    "Emphasize retrieval practice over re-reading",
                    "Adjust intervals based on performance",
                ],
                style="scientific, precise, adaptive, evidence-based",
            ),
            directive_template="""**SPACED REPETITION SCHEDULE**

**LEARNING MATERIAL**: {learning_material}

**INITIAL MASTERY LEVEL**: {initial_mastery}

{performance_section}

---

## FORGETTING CURVE ANALYSIS

**Ebbinghaus Forgetting Curve**:
- Without review: Retention drops to ~40% after 1 day, ~30% after 1 week
- With spaced review: Retention stays high (80%+)

**Material difficulty**: [Easy / Medium / Hard]

**Expected forgetting rate**: [Fast / Medium / Slow]

---

## OPTIMAL REVIEW SCHEDULE

### REVIEW 1: First Review
**Timing**: 1 day after initial learning
**Why**: Catch forgetting before it accelerates
**Method**: Active retrieval (test yourself, don't just re-read)
**Duration**: [X minutes]
**Success criterion**: [80%+ correct recall]

---

### REVIEW 2: Second Review
**Timing**: 3-7 days after Review 1 (based on performance)
- If Review 1 was easy (90%+): 7 days
- If Review 1 was moderate (70-89%): 5 days
- If Review 1 was hard (<70%): 3 days

**Why**: Strengthen memory trace before next forgetting cycle
**Method**: Mixed retrieval + application
**Duration**: [X minutes]
**Success criterion**: [85%+ correct recall]

---

### REVIEW 3: Third Review
**Timing**: 2-4 weeks after Review 2
- If Review 2 was easy: 4 weeks
- If Review 2 was moderate: 3 weeks
- If Review 2 was hard: 2 weeks

**Why**: Long-term consolidation
**Method**: Applied problem-solving
**Duration**: [X minutes]
**Success criterion**: [90%+ correct recall with application]

---

### REVIEW 4+: Subsequent Reviews
**Timing**: Exponentially increasing intervals
- Review 4: 1-2 months after Review 3
- Review 5: 3-4 months after Review 4
- Review 6: 6 months after Review 5
- Maintenance: Annually

**Why**: Maintain long-term retention
**Method**: Real-world application
**Success criterion**: [Fluent recall and use]

---

## RETRIEVAL PRACTICE DESIGN

**DON'T**: Re-read, highlight, summarize (passive review)

**DO**: Active retrieval methods

**Recommended techniques**:

1. **Free Recall**: Write everything you remember (no prompts)
2. **Cued Recall**: Answer specific questions
3. **Recognition + Explanation**: Identify correct answer AND explain why
4. **Application**: Use knowledge to solve new problems
5. **Teaching**: Explain concept to someone else

---

## PERFORMANCE-BASED ADJUSTMENTS

**After each review session**:

**If performance is STRONG (>90% correct)**:
- ✅ Increase next interval by 50-100%
- ✅ Reduce review duration
- ✅ Increase difficulty (harder questions)

**If performance is MODERATE (70-90% correct)**:
- ➡️ Keep current interval
- ➡️ Maintain review intensity

**If performance is WEAK (<70% correct)**:
- ❌ Decrease next interval by 50%
- ❌ Increase review duration
- ❌ Add more scaffolding
- ❌ Consider re-learning (not just review)

---

## IMPLEMENTATION CALENDAR

**Week 1**:
- Day 1: Initial learning + immediate practice
- Day 2: Review 1 (active retrieval)

**Week 2**:
- Day 5-7: Review 2 (based on performance)

**Week 4-5**:
- Day 21-28: Review 3

**Month 2-3**:
- Review 4

**Month 4-6**:
- Review 5

**Year 1+**:
- Annual maintenance

---

## TRACKING METRICS

**For each review, record**:
1. Date and time
2. Retrieval success rate (%)
3. Confidence level (1-5)
4. Time to recall (fast/slow)
5. Errors made (types)

**Adjust intervals based on these metrics**

---

## CRITICAL SUCCESS FACTORS

✅ **ACTIVE retrieval** (not passive re-reading)
✅ **Spacing** (distributed over time, not crammed)
✅ **Testing effect** (retrieval practice strengthens memory)
✅ **Difficulty** (make it challenging but achievable)
✅ **Feedback** (know what you got wrong)

---

## IMMEDIATE NEXT STEP

Schedule Review 1 for: [Date/Time]
Prepare retrieval practice questions: [List 5-10 questions]""",
            input_schema={
                "learning_material": str,
                "initial_mastery": str,
                "performance_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "forgetting_curve",
                    "review_schedule",
                    "retrieval_practice",
                    "performance_adjustments",
                ],
                must_not_include=["passive_review", "cramming"],
                style_guide="Scientific, precise intervals. Emphasize active retrieval over re-reading.",
            ),
        )

    def build_context(
        self, learning_material="", initial_mastery="", previous_performance="", **kwargs
    ):
        """Build context for spaced repetition optimization."""
        performance_section = (
            f"**PREVIOUS REVIEW PERFORMANCE**: {previous_performance}"
            if previous_performance
            else ""
        )
        kwargs.pop("performance_section", None)

        return super().build_context(
            learning_material=learning_material,
            initial_mastery=initial_mastery,
            performance_section=performance_section,
            **kwargs,
        )

    def execute(
        self,
        provider="openai",
        learning_material="",
        initial_mastery="",
        previous_performance="",
        **kwargs,
    ):
        """Execute spaced repetition schedule optimization."""
        performance_section = (
            f"**PREVIOUS REVIEW PERFORMANCE**: {previous_performance}"
            if previous_performance
            else ""
        )
        kwargs.pop("performance_section", None)

        return super().execute(
            provider=provider,
            learning_material=learning_material,
            initial_mastery=initial_mastery,
            performance_section=performance_section,
            **kwargs,
        )


__all__ = ["SpacedRepetitionOptimizer"]
