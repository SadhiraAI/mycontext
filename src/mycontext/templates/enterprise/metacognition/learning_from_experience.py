"""
LearningFromExperience Pattern (Enterprise)

Extract transferable lessons from successes and failures.
Implements Kolb's experiential learning cycle and reflective practice.

Research Foundation:
- Kolb, D. A. (1984). Experiential Learning. Prentice-Hall.
- Schön, D. A. (1983). The Reflective Practitioner. Basic Books.
- Ellis, S., & Davidi, I. (2005). After-event reviews. Journal of Applied Psychology, 90(5), 857-871.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class LearningFromExperience(Pattern):
    """
    Systematic reflection to extract transferable lessons from experience.

    Implements:
    - Kolb's Experiential Learning Cycle (1984)
    - Schön's Reflective Practice (1983)
    - US Army After Action Review methodology

    Use Cases:
    - Post-project retrospectives
    - Learning from mistakes
    - Capturing best practices
    - Skill improvement
    - Team learning

    Example:
        >>> from mycontext.templates.enterprise.metacognition import LearningFromExperience
        >>>
        >>> pattern = LearningFromExperience()
        >>> result = pattern.execute(
        ...     provider="gemini",
        ...     experience_description="Failed product launch",
        ...     outcome="50% below sales target",
        ...     initial_expectations="Expected 10k units, sold 5k"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a reflective practice coach and experiential learning expert. "
        "Extract transferable lessons from the given experience.\n\n"
        "Experience: {experience_description}\n"
        "Outcome: {outcome}\n"
        "Initial Expectations: {initial_expectations}\n"
        "{context_section}\n\n"
        "Apply Kolb's experiential learning cycle: (1) Concrete Experience — "
        "describe what happened objectively, noting key decision and turning points. "
        "(2) Reflective Observation — compare expected vs actual results with gap "
        "analysis. (3) Abstract Conceptualization — identify root causes, extract "
        "generalizable principles (not just specific facts), and update mental "
        "models. (4) Active Experimentation — define what to keep doing, stop doing, "
        "start doing, and do differently.\n\n"
        "Focus on TRANSFERABLE lessons that apply beyond this specific situation. "
        "Provide a one-sentence key lesson and a success pattern for the future.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="learning_from_experience",
            description="Extract transferable lessons from successes and failures",
            version="1.0.0",
            tags=["metacognition", "enterprise", "reflection", "learning"],
            metadata={"category": "metacognition", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Reflective Practice Coach and Experiential Learning Expert",
                rules=[
                    "Apply systematic reflection frameworks (Kolb, Schön, AAR)",
                    "Extract TRANSFERABLE lessons, not just specific facts",
                    "Distinguish context-specific from generalizable insights",
                    "Focus on actionable improvements for future",
                    "Balance success analysis with failure analysis",
                ],
                style="reflective, analytical, constructive, future-focused, honest",
            ),
            directive_template="""**LEARNING FROM EXPERIENCE**

**EXPERIENCE**: {experience_description}

**OUTCOME**: {outcome}

**INITIAL EXPECTATIONS**: {initial_expectations}

{context_section}

---

## SYSTEMATIC REFLECTION (Kolb 1984 + US Army AAR)

### 1. CONCRETE EXPERIENCE (What Happened?)

**Describe the experience objectively:**
- What did you/we do?
- What sequence of events occurred?
- Who was involved?
- What was the timeline?

**Key moments:**
- Decision points: [What decisions were made?]
- Turning points: [When did things change?]
- Critical incidents: [What had biggest impact?]

---

### 2. REFLECTIVE OBSERVATION (What Was Supposed to Happen vs. What Actually Happened?)

**Initial Plan/Expectations:**
- What were you trying to achieve?
- What approach did you plan to use?
- What did you expect would happen?

**Actual Results:**
- What actually happened?
- Where did reality differ from expectations?
- What surprised you?

**Gap Analysis:**
| Aspect | Expected | Actual | Gap |
|--------|----------|--------|-----|
| [Outcome] | [X] | [Y] | [Y-X] |
| [Process] | [...] | [...] | [...] |
| [Timeline] | [...] | [...] | [...] |

---

### 3. ABSTRACT CONCEPTUALIZATION (Why Did It Happen? What Can We Learn?)

**Root Cause Analysis:**
- What led to this outcome?
- What factors contributed most?
- What assumptions were wrong?
- What did we overlook?

**Success Factors** (What worked well?):
1. [Factor] - Why it worked: [Explanation]
2. [Factor] - Why it worked: [Explanation]

**Failure Factors** (What didn't work?):
1. [Factor] - Why it failed: [Explanation]
2. [Factor] - Why it failed: [Explanation]

**Key Insights** (Abstract principles, not just specifics):
- **Insight 1**: [Generalizable lesson]
  - Context: [When does this apply?]
  - Why: [Underlying principle]
  
- **Insight 2**: [Generalizable lesson]
  - Context: [When does this apply?]
  - Why: [Underlying principle]

**Mental Models Updated:**
- Before: [What I/we believed]
- After: [What I/we now understand]

---

### 4. ACTIVE EXPERIMENTATION (What Will I/We Do Differently?)

**Transferable Lessons** (Apply to future situations):

**A. KEEP DOING** (Effective practices to maintain):
1. [Practice] - Because: [Why it worked]
2. [Practice] - Because: [Why it worked]

**B. STOP DOING** (Ineffective practices to eliminate):
1. [Practice] - Because: [Why it failed]
2. [Practice] - Because: [Why it failed]

**C. START DOING** (New practices to adopt):
1. [New practice] - Expected benefit: [Why it should work]
2. [New practice] - Expected benefit: [Why it should work]

**D. DO DIFFERENTLY** (Practices to modify):
1. [Practice] - Change: [How to improve]
2. [Practice] - Change: [How to improve]

**Implementation Plan:**
- Next similar situation: [What I'll do]
- Different but related situation: [How to adapt lesson]
- Share with others: [Who else could benefit?]

---

### 5. CONSOLIDATION (Lock in the Learning)

**One-Sentence Lesson:**
[The single most important thing learned from this experience]

**Personal/Team Growth:**
- Skills improved: [What got better?]
- Knowledge gained: [What do I/we now know?]
- Capabilities developed: [What can I/we now do?]

**Warning Signs** (Early indicators if repeating mistakes):
- Watch for: [Red flags]
- If you notice: [What to do]

**Success Pattern** (Recipe for future success):
1. [Step/principle]
2. [Step/principle]
3. [Step/principle]

---

**CRITICAL**: Focus on TRANSFERABLE lessons that apply beyond this specific situation. Ask "What's the general principle?" not just "What happened?"

**Remember**: Both successes and failures are learning opportunities. Extract lessons from both.""",
            input_schema={
                "experience_description": str,
                "outcome": str,
                "initial_expectations": str,
                "context_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "transferable_lessons",
                    "abstract_principles",
                    "future_actions",
                    "success_and_failure_analysis",
                ],
                must_not_include=["blame_assignment", "only_specific_facts", "vague_generalities"],
                style_guide="Balance honest analysis with constructive future focus. Extract generalizable principles, not just specifics.",
            ),
        )

    def build_context(
        self, experience_description="", outcome="", initial_expectations="", context="", **kwargs
    ):
        """
        Build context for learning from experience.

        Args:
            experience_description: What happened (the experience to learn from)
            outcome: Result - was it success or failure? What was achieved?
            initial_expectations: What was supposed to happen?
            context: Optional situational factors
            **kwargs: Additional options

        Returns:
            Context object ready for use
        """
        context_section = f"**CONTEXTUAL FACTORS**: {context}" if context else ""
        kwargs.pop("context_section", None)

        return super().build_context(
            experience_description=experience_description,
            outcome=outcome,
            initial_expectations=initial_expectations,
            context_section=context_section,
            **kwargs,
        )

    def execute(
        self,
        provider="gemini",
        experience_description="",
        outcome="",
        initial_expectations="",
        context="",
        **kwargs,
    ):
        """
        Execute learning from experience reflection.

        Args:
            provider: LLM provider
            experience_description: What happened
            outcome: Result achieved
            initial_expectations: What was supposed to happen
            context: Optional situational factors
            **kwargs: Additional provider options

        Returns:
            ProviderResponse with reflection and lessons learned
        """
        context_section = f"**CONTEXTUAL FACTORS**: {context}" if context else ""
        kwargs.pop("context_section", None)

        return super().execute(
            provider=provider,
            experience_description=experience_description,
            outcome=outcome,
            initial_expectations=initial_expectations,
            context_section=context_section,
            **kwargs,
        )


__all__ = ["LearningFromExperience"]
