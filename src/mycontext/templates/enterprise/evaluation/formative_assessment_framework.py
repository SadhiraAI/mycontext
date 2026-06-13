"""
FormativeAssessmentFramework Pattern (Enterprise)

Design ongoing assessment for learning (not just of learning).
Implements Black & Wiliam's formative assessment framework.

Research Foundation:
- Black, P., & Wiliam, D. (1998). Assessment and classroom learning.
- Wiliam, D., & Thompson, M. (2008). Integrating assessment with learning.
- Sadler, D. R. (1989). Formative assessment and the design of instructional systems.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class FormativeAssessmentFramework(Pattern):
    """
    Design formative assessment for ongoing learning.

    Five Key Strategies (Black & Wiliam):
    1. Clarify learning intentions and success criteria
    2. Engineer effective classroom discussions
    3. Provide feedback that moves learning forward
    4. Activate students as learning resources for each other
    5. Activate students as owners of their own learning

    Use Cases:
    - Classroom assessment
    - Online learning platforms
    - Tutoring systems
    - Self-paced learning

    Example:
        >>> from mycontext.templates.enterprise.evaluation import FormativeAssessmentFramework
        >>>
        >>> pattern = FormativeAssessmentFramework()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     learning_unit="Quadratic equations module",
        ...     learning_goal="Solve quadratic equations using multiple methods"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a formative assessment expert applying Black and Wiliam's "
        "framework. Design ongoing assessment FOR learning, not just OF learning.\n\n"
        "Learning Unit: {learning_unit}\n"
        "Learning Goal: {learning_goal}\n"
        "{context_section}\n\n"
        "Apply the five key strategies: (1) Clarify learning intentions — state "
        "exactly what learners should know or do, with observable success criteria "
        "and exemplars. (2) Engineer effective discussions — design prompts that "
        "reveal thinking and uncover misconceptions. (3) Provide feedback that moves "
        "learning forward — specify where the learner is, where they need to go, and "
        "concrete steps to close the gap. (4) Activate learners as resources for "
        "each other — structure peer review with criteria checklists and constructive "
        "feedback training. (5) Activate learners as owners of their own learning — "
        "build self-assessment tools and metacognitive prompts.\n\n"
        "Include quick-check techniques (exit tickets, diagnostic questions) and a "
        "continuous feedback loop: assess, analyze gaps, adjust instruction, "
        "reassess.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="formative_assessment_framework",
            description="Design ongoing assessment for learning",
            version="1.0.0",
            tags=["evaluation", "enterprise", "formative", "assessment"],
            metadata={"category": "evaluation", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Formative Assessment Expert",
                rules=[
                    "Focus on assessment FOR learning, not just OF learning",
                    "Provide actionable feedback that guides improvement",
                    "Make success criteria transparent",
                    "Use assessment to adjust instruction",
                    "Involve learners in self-assessment",
                ],
                style="developmental, actionable, learner-centered, continuous",
            ),
            directive_template="""**FORMATIVE ASSESSMENT FRAMEWORK**

**LEARNING UNIT**: {learning_unit}

**LEARNING GOAL**: {learning_goal}

---

## PURPOSE OF FORMATIVE ASSESSMENT

**NOT for grading** - For learning and improvement
**Goal**: Identify where learner is, where they need to go, how to get there

---

## STRATEGY 1: CLARIFY LEARNING INTENTIONS

**Learning intention** (What will learner learn?):
- [Specific, clear statement of what learner should know/do]

**Success criteria** (How will learner know they succeeded?):
1. [Criterion 1 - Observable evidence of success]
2. [Criterion 2 - Observable evidence]
3. [Criterion 3 - Observable evidence]

**Share with learners**:
- At start of unit: "By the end, you will be able to..."
- Show examples of successful work
- Contrast with unsuccessful work

---

## STRATEGY 2: ENGINEER EFFECTIVE DISCUSSIONS

**Discussion prompts**:
- [Question 1 - reveals thinking]
- [Question 2 - uncovers misconceptions]
- [Question 3 - promotes reasoning]

**Listen for**:
- Common errors: [Anticipated mistakes]
- Misconceptions: [Typical misunderstandings]
- Partially correct reasoning: [Emerging understanding]

**Respond by**:
- Probing: "Why do you think that?"
- Redirecting: "What if we changed X?"
- Comparing: "How is your approach different from..."

---

## STRATEGY 3: PROVIDE FEEDBACK THAT MOVES LEARNING FORWARD

**Feedback principles** (Sadler):
1. Where learner is now (current performance)
2. Where learner needs to go (goal)
3. How to close the gap (specific actions)

**Feedback template**:

**Strengths** (What's working):
- [Specific positive observation]
- [Evidence of understanding]

**Growth areas** (What needs improvement):
- [Specific area needing work]
- [Gap identified]

**Next steps** (How to improve):
1. [Specific action learner can take]
2. [Another specific action]
3. [Resource or strategy to use]

**Feedback timing**: [Within 24-48 hours while still fresh]

**Feedback mode**: [Written / Verbal / Combination]

---

## STRATEGY 4: ACTIVATE LEARNERS AS RESOURCES FOR EACH OTHER

**Peer assessment**:
- **Structure**: Use rubric or checklist
- **Focus**: Specific criteria, not general "good/bad"
- **Training**: Teach how to give constructive feedback

**Peer learning activities**:

**A. Peer review**:
- Exchange work
- Use criteria checklist
- Provide 2 strengths + 1 suggestion

**B. Think-pair-share**:
- Think individually (2 min)
- Discuss with partner (3 min)
- Share with group

**C. Reciprocal teaching**:
- Learner A explains concept to Learner B
- Learner B asks clarifying questions
- Switch roles

---

## STRATEGY 5: ACTIVATE LEARNERS AS OWNERS OF LEARNING

**Self-assessment**:

**Before starting**:
- "What do I already know about this?"
- "What do I need to learn?"
- "How will I know if I'm successful?"

**During learning**:
- "Am I understanding this?"
- "What's confusing me?"
- "Do I need to ask for help?"

**After completing**:
- "Did I meet the success criteria?"
- "What did I do well?"
- "What would I do differently next time?"

**Self-assessment tool**: [Checklist or rubric for learner to use]

---

## ASSESSMENT TECHNIQUES

**Quick checks** (5-10 minutes):

**1. Exit tickets**:
- Last 5 min of session
- Question: [Specific prompt to check understanding]
- Purpose: Identify who needs help

**2. Thumbs up/down**:
- "Show me how confident you feel: 👍 👎 👌"
- Quick gauge of class understanding

**3. One-minute paper**:
- "Write for 1 minute: What was most important? What's still confusing?"

**4. Whiteboard responses**:
- All learners solve problem on whiteboard simultaneously
- Teacher scans for errors

**5. Concept maps**:
- Draw connections between ideas
- Reveals understanding of relationships

---

## DIAGNOSTIC QUESTIONS

**Good diagnostic questions**:
- Have one correct answer
- Reveal common misconceptions through wrong answers
- Give insight into thinking

**Example for this unit**:

**Question**: [Specific problem]

**Correct answer**: [X] - Shows: [Understanding]

**Distractor A**: [Y] - Reveals misconception: [Z]

**Distractor B**: [W] - Reveals misconception: [V]

---

## FEEDBACK LOOP

**Continuous cycle**:

1. **Assess**: Check current understanding
   - Method: [Quick check technique]

2. **Analyze**: Identify gaps
   - Look for: [Common errors, misconceptions]

3. **Adjust**: Modify instruction
   - If most struggle: Re-teach differently
   - If some struggle: Small group support
   - If few struggle: Advanced challenges

4. **Reassess**: Check again
   - Same concept, different context

---

## IMPLEMENTATION SCHEDULE

**Daily formative checks**:
- Start: "What do you remember from last time?"
- Middle: "Show me on whiteboard"
- End: "Exit ticket"

**Weekly deeper assessment**:
- Self-assessment using criteria
- Peer review with feedback
- Teacher conference (if needed)

**Bi-weekly adjustment**:
- Review aggregate data
- Adjust pacing and approach
- Reteach key concepts

---

## SUCCESS INDICATORS

**Formative assessment is working when**:

✅ Learners can articulate what they're learning
✅ Learners can assess their own progress
✅ Instruction adjusts based on evidence
✅ Feedback is specific and actionable
✅ Learning improves over time

**Warning signs**:
❌ Only assessing at end of unit
❌ Feedback is too late to be useful
❌ Learners don't understand criteria
❌ No adjustments made based on data""",
            input_schema={"learning_unit": str, "learning_goal": str},
            constraints=Constraints(
                must_include=[
                    "five_strategies",
                    "success_criteria",
                    "actionable_feedback",
                    "self_assessment",
                ],
                must_not_include=["summative_only", "late_feedback"],
                style_guide="Developmental and continuous. Assessment FOR learning. Specific, actionable guidance.",
            ),
        )

    def build_context(self, learning_unit="", learning_goal="", **kwargs):
        """Build context for formative assessment design."""
        return super().build_context(
            learning_unit=learning_unit, learning_goal=learning_goal, **kwargs
        )

    def execute(self, provider="openai", learning_unit="", learning_goal="", **kwargs):
        """Execute formative assessment framework design."""
        return super().execute(
            provider=provider, learning_unit=learning_unit, learning_goal=learning_goal, **kwargs
        )


__all__ = ["FormativeAssessmentFramework"]
