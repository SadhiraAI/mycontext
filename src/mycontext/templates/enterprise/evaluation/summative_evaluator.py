"""
SummativeEvaluator Pattern (Enterprise)

Design final evaluation of learning outcomes.
Implements backward design and authentic assessment principles.

Research Foundation:
- Wiggins, G., & McTighe, J. (2005). Understanding by Design.
- Bloom, B. S. (1956). Taxonomy of educational objectives.
- Pellegrino, J. W., et al. (2001). Knowing what students know.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class SummativeEvaluator(Pattern):
    """
    Design summative evaluation of learning outcomes.
    
    Key Principles:
    - Align with learning objectives
    - Measure what matters
    - Valid and reliable
    - Clear scoring criteria
    - Authentic when possible
    
    Use Cases:
    - Final exams
    - Course-end projects
    - Certification tests
    - Performance assessments
    
    Example:
        >>> from mycontext.templates.enterprise.evaluation import SummativeEvaluator
        >>> 
        >>> pattern = SummativeEvaluator()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     course_title="Introduction to Data Science",
        ...     learning_outcomes="Apply statistical methods, visualize data, build models"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a summative assessment design expert applying Wiggins and "
        "McTighe's backward design and Bloom's taxonomy. Design a rigorous final "
        "evaluation of learning outcomes.\n\n"
        "Course/Unit: {course_title}\n"
        "Learning Outcomes: {learning_outcomes}\n"
        "{context_section}\n\n"
        "Design the summative evaluation: (1) Map each learning outcome to Bloom's "
        "taxonomy level (Remember through Create) and determine the appropriate "
        "assessment type. (2) Design assessment components — mix item types "
        "(multiple choice, short answer, performance tasks) weighted to cover all "
        "outcomes. (3) Create an alignment table verifying every outcome is assessed "
        "with appropriate cognitive demand. (4) Build a scoring guide with clear "
        "criteria and grade conversion. (5) Validate — check content validity "
        "(covers all outcomes), construct validity (measures intended skills), and "
        "reliability (consistent scoring). (6) Ensure fairness and accessibility "
        "with accommodations.\n\n"
        "Include sample items and post-assessment analysis guidelines for "
        "continuous improvement.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="summative_evaluator",
            description="Design final evaluation of learning outcomes",
            version="1.0.0",
            tags=["evaluation", "enterprise", "summative", "final-assessment"],
            metadata={
                "category": "evaluation",
                "license": "enterprise",
                "tier": "enterprise"
            },
            guidance=Guidance(
                role="Summative Assessment Design Expert",
                rules=[
                    "Align assessment with learning outcomes (backward design)",
                    "Use appropriate cognitive levels (Bloom's taxonomy)",
                    "Ensure validity (measures what it claims)",
                    "Ensure reliability (consistent results)",
                    "Make scoring objective and fair"
                ],
                style="rigorous, comprehensive, fair, objective"
            ),
            directive_template="""**SUMMATIVE EVALUATION DESIGN**

**COURSE/UNIT**: {course_title}

**LEARNING OUTCOMES**: {learning_outcomes}

---

## BACKWARD DESIGN APPROACH

**Step 1**: Identify desired results (learning outcomes)
**Step 2**: Determine acceptable evidence (this assessment)
**Step 3**: Plan learning experiences (already done)

**This document**: Step 2 - Assessment design

---

## LEARNING OUTCOMES ANALYSIS

**Map outcomes to Bloom's taxonomy**:

**Outcome 1**: {outcome_1}
- Bloom's level: [Remember / Understand / Apply / Analyze / Evaluate / Create]
- Assessment type needed: [Knowledge test / Application problem / Analysis task / etc.]

**Outcome 2**: {outcome_2}
- Bloom's level: [Level]
- Assessment type needed: [Type]

**Outcome 3**: {outcome_3}
- Bloom's level: [Level]
- Assessment type needed: [Type]

---

## ASSESSMENT FORMAT

**Type**: [Exam / Project / Performance / Portfolio / Mixed]

**Duration**: [Time allowed]

**Setting**: [In-person / Online / Take-home]

**Resources allowed**: [Open-book / Closed-book / Specific materials]

---

## ASSESSMENT COMPONENTS

### COMPONENT 1: [Type - e.g., Multiple Choice]
**Purpose**: Assess [Which outcome?]
**Number of items**: [X]
**Points**: [Y] ([Z]% of total)
**Time**: [Minutes]

**Sample items**:
1. [Example question]
   - Correct answer: [X]
   - Distractors target: [Common errors]

2. [Example question]
   - Correct answer: [X]

---

### COMPONENT 2: [Type - e.g., Short Answer]
**Purpose**: Assess [Which outcome?]
**Number of items**: [X]
**Points**: [Y] ([Z]% of total)
**Time**: [Minutes]

**Sample items**:
1. [Question requiring explanation/application]
   - Expected response: [Key elements]
   - Scoring: [Rubric or point breakdown]

---

### COMPONENT 3: [Type - e.g., Performance Task]
**Purpose**: Assess [Which outcome?]
**Task description**: [Authentic task]
**Points**: [Y] ([Z]% of total)
**Time**: [Duration]

**Task prompt**:
[Detailed description of what learner must do]

**Scoring rubric**:
[Criteria and performance levels]

---

[Additional components as needed]

---

## ALIGNMENT TABLE

| Learning Outcome | Assessment Component | Bloom's Level | Points | % |
|------------------|---------------------|---------------|--------|---|
| [Outcome 1] | [Component X] | [Level] | [X] | [Y%] |
| [Outcome 2] | [Component Y] | [Level] | [X] | [Y%] |
| [Outcome 3] | [Component Z] | [Level] | [X] | [Y%] |

**Verification**: All outcomes assessed? ✅

---

## SCORING GUIDE

**Total points**: [Sum]

**Grading scale**:
- A: [Points range] ([%]
) - Exceptional mastery
- B: [Points range] ([%]) - Strong proficiency
- C: [Points range] ([%]) - Adequate proficiency
- D: [Points range] ([%]) - Minimal proficiency
- F: [Points range] ([%]) - Insufficient proficiency

**OR Mastery levels**:
- Mastery: [Points] - All outcomes met
- Proficiency: [Points] - Most outcomes met
- Developing: [Points] - Some outcomes met
- Beginning: [Points] - Few outcomes met

---

## VALIDITY CHECK

**Content validity**: Does assessment cover all important content?
- All learning outcomes assessed: ✅
- Appropriate balance of topics: ✅
- Representative sample of domain: ✅

**Construct validity**: Does it measure intended construct?
- Aligns with Bloom's levels: ✅
- Appropriate task types: ✅
- No construct-irrelevant variance: ✅

**Face validity**: Does it look like it measures what it claims?
- Clear connection to outcomes: ✅
- Recognizable as relevant: ✅

---

## RELIABILITY CONSIDERATIONS

**Scoring reliability**:
- Clear scoring criteria: [Rubrics, answer keys]
- Multiple raters agreement: [If applicable]
- Consistent application: [Training for graders]

**Test reliability**:
- Sufficient number of items: [Enough to measure consistently]
- Clear instructions: [No ambiguity]
- Appropriate difficulty: [Not too easy/hard]

---

## FAIRNESS AND ACCESSIBILITY

**Ensure assessment is fair**:

✅ **Bias review**: No cultural bias or stereotypes
✅ **Accessibility**: Accommodations available (extra time, assistive tech)
✅ **Clarity**: Instructions are crystal clear
✅ **Opportunity**: All learners had equal opportunity to learn content

**Accommodations**:
- Extended time: [For documented needs]
- Alternative format: [If required]
- Assistive technology: [As appropriate]

---

## ADMINISTRATION GUIDELINES

**Before assessment**:
1. Review instructions with learners
2. Clarify expectations
3. Answer logistical questions (not content)
4. Ensure environment is appropriate

**During assessment**:
1. Monitor for issues
2. Maintain test security (if applicable)
3. Answer procedural questions only
4. Document any incidents

**After assessment**:
1. Collect all materials
2. Score using rubrics consistently
3. Provide timely results
4. Offer feedback (even on summative)

---

## SCORING PROCEDURES

**Objective items** (multiple choice, true/false):
- Use answer key
- Automatic scoring (if possible)
- Check for ambiguous items

**Subjective items** (essays, projects):
- Use detailed rubric
- Score blindly (hide names if possible)
- Score same question across all learners
- Check inter-rater reliability

**Performance tasks**:
- Use rubric with specific criteria
- Observe/review entire performance
- Document evidence for score

---

## POST-ASSESSMENT ANALYSIS

**Item analysis** (for future improvement):
- Difficulty: What % got each item correct?
- Discrimination: Do high scorers get it right more often?
- Distractor analysis: Are distractors working?

**Outcome achievement**:
- Which outcomes were met?
- Which need more instructional time?
- Overall success rate?

**Assessment quality**:
- Were instructions clear?
- Was time sufficient?
- Were there any issues?

---

## FEEDBACK TO LEARNERS

**Even summative assessment should provide feedback**:

**Overall score**: [X/Y points = Grade]

**Breakdown by outcome**:
- Outcome 1: [Mastery / Proficiency / Developing]
- Outcome 2: [Level achieved]
- Outcome 3: [Level achieved]

**Strengths**: [What learner did well]

**Areas for future growth**: [What to focus on next]

---

## SECURITY AND INTEGRITY

**If high-stakes**:
- Test security protocols
- Identity verification
- Proctoring (if needed)
- Academic integrity statement
- Plagiarism detection (for written work)

**If formative-summative hybrid**:
- Allow revision based on feedback
- Reassessment opportunity
- Growth-focused scoring""",
            input_schema={
                "course_title": str,
                "learning_outcomes": str,
                "outcome_1": str,
                "outcome_2": str,
                "outcome_3": str
            },
            constraints=Constraints(
                must_include=[
                    "alignment_with_outcomes",
                    "blooms_taxonomy",
                    "scoring_rubric",
                    "validity_reliability"
                ],
                must_not_include=[
                    "misaligned_assessment",
                    "unclear_criteria"
                ],
                style_guide="Rigorous and comprehensive. Aligned with outcomes. Fair and valid. Clear scoring."
            )
        )

    def build_context(self, course_title="", learning_outcomes="", **kwargs):
        """Build context for summative evaluation design."""
        # Parse learning outcomes into individual outcomes
        outcomes_list = [o.strip() for o in learning_outcomes.split(',')]
        outcome_1 = outcomes_list[0] if len(outcomes_list) > 0 else ""
        outcome_2 = outcomes_list[1] if len(outcomes_list) > 1 else ""
        outcome_3 = outcomes_list[2] if len(outcomes_list) > 2 else ""

        kwargs.pop('outcome_1', None)
        kwargs.pop('outcome_2', None)
        kwargs.pop('outcome_3', None)

        return super().build_context(
            course_title=course_title,
            learning_outcomes=learning_outcomes,
            outcome_1=outcome_1,
            outcome_2=outcome_2,
            outcome_3=outcome_3,
            **kwargs
        )

    def execute(self, provider="openai", course_title="", learning_outcomes="", **kwargs):
        """Execute summative evaluation design."""
        # Parse learning outcomes
        outcomes_list = [o.strip() for o in learning_outcomes.split(',')]
        outcome_1 = outcomes_list[0] if len(outcomes_list) > 0 else ""
        outcome_2 = outcomes_list[1] if len(outcomes_list) > 1 else ""
        outcome_3 = outcomes_list[2] if len(outcomes_list) > 2 else ""

        kwargs.pop('outcome_1', None)
        kwargs.pop('outcome_2', None)
        kwargs.pop('outcome_3', None)

        return super().execute(
            provider=provider,
            course_title=course_title,
            learning_outcomes=learning_outcomes,
            outcome_1=outcome_1,
            outcome_2=outcome_2,
            outcome_3=outcome_3,
            **kwargs
        )


__all__ = ["SummativeEvaluator"]
