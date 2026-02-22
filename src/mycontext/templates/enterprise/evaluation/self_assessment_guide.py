"""
SelfAssessmentGuide Pattern (Enterprise)

Help learners evaluate their own work and develop metacognitive skills.
Implements self-regulated learning and evaluative judgment research.

Research Foundation:
- Boud, D. (1995). Enhancing learning through self-assessment.
- Andrade, H., & Valtcheva, A. (2009). Promoting learning and achievement through self-assessment.
- Panadero, E., et al. (2016). A review of self-regulated learning: Six models and four directions.

License: Enterprise
"""

from mycontext import Pattern, Guidance, Constraints

class SelfAssessmentGuide(Pattern):
    """
    Help learners evaluate their own work.
    
    Self-Assessment Benefits:
    - Develops metacognitive awareness
    - Promotes ownership of learning
    - Improves self-regulation
    - Builds evaluative judgment
    - Prepares for lifelong learning
    
    Use Cases:
    - Portfolio assessment
    - Reflective practice
    - Goal-setting systems
    - Learning journals
    
    Example:
        >>> from mycontext.templates.enterprise.evaluation import SelfAssessmentGuide
        >>> 
        >>> pattern = SelfAssessmentGuide()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     work_to_assess="Final project: Mobile app prototype",
        ...     success_criteria="Functional UI, meets requirements, clean code"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a self-assessment and metacognition expert applying Boud's "
        "self-assessment research. Guide honest, evidence-based self-evaluation.\n\n"
        "Work to Assess: {work_to_assess}\n"
        "Success Criteria: {success_criteria}\n"
        "{context_section}\n\n"
        "Guide the self-assessment process: (1) Clarify criteria — define what "
        "excellent, adequate, and poor performance looks like for each success "
        "criterion. (2) Evidence-based evaluation — for each criterion, rate "
        "performance with specific evidence from the work, identifying strengths "
        "and weaknesses. (3) Honest reflection — what worked, what didn't, what "
        "was surprising, and what was harder than expected. (4) Metacognitive "
        "analysis — evaluate the approach used, what to change if starting over, "
        "and lessons about personal learning style. (5) Goal setting — define "
        "specific, measurable improvement goals with action steps and timelines.\n\n"
        "Promote growth mindset: reframe weaknesses as 'not yet proficient' with "
        "clear paths to improvement. Include a calibration check against external "
        "feedback.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="self_assessment_guide",
            description="Help learners evaluate their own work",
            version="1.0.0",
            tags=["evaluation", "enterprise", "self-assessment", "metacognition"],
            metadata={
                "category": "evaluation",
                "license": "enterprise",
                "tier": "enterprise"
            },
            guidance=Guidance(
                role="Self-Assessment and Metacognition Expert",
                rules=[
                    "Provide clear criteria for self-evaluation",
                    "Guide honest, evidence-based self-assessment",
                    "Promote growth mindset (mistakes are learning opportunities)",
                    "Link self-assessment to goal-setting and improvement",
                    "Develop evaluative judgment skills"
                ],
                style="reflective, honest, growth-oriented, structured"
            ),
            directive_template="""**SELF-ASSESSMENT GUIDE**

**WORK TO ASSESS**: {work_to_assess}

**SUCCESS CRITERIA**: {success_criteria}

---

## PURPOSE OF SELF-ASSESSMENT

**NOT about grading yourself** - About honest reflection and improvement

**Goals**:
1. Develop awareness of your strengths and weaknesses
2. Take ownership of your learning
3. Set specific goals for improvement
4. Build evaluative judgment skills

---

## STEP 1: UNDERSTAND THE CRITERIA

**Before assessing, clarify what "good" looks like**:

**Success criteria** (what you're aiming for):
{detailed_criteria}

**For each criterion, ask**:
- What does excellent performance look like?
- What does adequate performance look like?
- What are common mistakes or weaknesses?

**Review examples**:
- Exemplar work (if available)
- Your own previous work
- Peer work (with permission)

---

## STEP 2: EVIDENCE-BASED SELF-EVALUATION

**For each criterion, gather evidence**:

### CRITERION 1: [Name]

**My self-rating**: ⭐⭐⭐⭐⭐ (1-5)

**Evidence supporting this rating**:
- [Specific example from my work]
- [Another piece of evidence]

**Strengths** (what I did well):
- [Specific strength]
- [Another strength]

**Weaknesses** (what needs improvement):
- [Specific gap or error]
- [Another area needing work]

**Comparison to criteria**:
- Meets criterion? [Yes / Partially / No]
- Why or why not? [Reasoning]

---

### CRITERION 2: [Name]

**My self-rating**: ⭐⭐⭐⭐⭐

**Evidence**:
- [Specific examples]

**Strengths**:
- [What worked]

**Weaknesses**:
- [What needs work]

**Comparison to criteria**:
- [Assessment]

---

[Repeat for all criteria]

---

## STEP 3: OVERALL SELF-EVALUATION

**Summary of strengths** (Top 3):
1. [Specific strength with evidence]
2. [Specific strength with evidence]
3. [Specific strength with evidence]

**Summary of weaknesses** (Top 3):
1. [Specific weakness with evidence]
2. [Specific weakness with evidence]
3. [Specific weakness with evidence]

**Overall self-rating**: [Exemplary / Proficient / Developing / Beginning]

**Justification**: [Why this rating? Reference specific evidence]

---

## STEP 4: HONEST REFLECTION

**Be brutally honest with yourself**:

**What did I do well?** (Celebrate successes)
- [Accomplishment 1]
- [Accomplishment 2]

**What didn't work?** (No judgment, just facts)
- [Issue 1]
- [Issue 2]

**What surprised me?** (Unexpected outcomes)
- [Surprise 1]
- [Surprise 2]

**What was harder than expected?**
- [Challenge 1]
- [Challenge 2]

**What was easier than expected?**
- [Success 1]
- [Success 2]

---

## STEP 5: METACOGNITIVE ANALYSIS

**Thinking about your thinking**:

**My approach** (How did I tackle this?):
- Strategy used: [Describe]
- Why I chose this approach: [Reasoning]

**If I could start over, I would**:
- Change: [What]
- Because: [Why]

**I got stuck when**:
- Problem: [Describe]
- How I solved it (or didn't): [Approach]

**I learned that I**:
- Am good at: [Strength discovered]
- Need to work on: [Weakness identified]
- Thought process works best when: [Condition]

---

## STEP 6: GOAL SETTING

**Based on self-assessment, set specific improvement goals**:

**Goal 1**: [Specific, measurable improvement goal]
- **Why**: [Why this goal matters]
- **How**: [Concrete steps to achieve]
- **When**: [Timeline]
- **Success looks like**: [How to know goal is met]

**Goal 2**: [Specific goal]
- **Why**: [Reason]
- **How**: [Action steps]
- **When**: [Deadline]
- **Success looks like**: [Indicator]

**Goal 3**: [Specific goal]
- **Why**: [Reason]
- **How**: [Steps]
- **When**: [Timeline]
- **Success looks like**: [Metric]

---

## STEP 7: ACTION PLAN

**Immediate next steps** (this week):
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Short-term** (this month):
1. [Action 1]
2. [Action 2]

**Long-term** (this term/semester):
1. [Major goal]
2. [Development area]

---

## CALIBRATION CHECK

**Compare your self-assessment to external feedback**:

**My self-rating**: [X]

**Teacher/expert rating**: [Y] (if available)

**Peer ratings**: [Z] (if available)

**Calibration analysis**:
- If ratings match (±1): Good self-awareness ✅
- If I rated myself higher: May be overconfident - need to be more critical
- If I rated myself lower: May be underconfident - recognize strengths

**Adjustment** (if needed):
- What I learned about my evaluative judgment: [Insight]
- How to improve accuracy of self-assessment: [Plan]

---

## GROWTH MINDSET REFRAME

**Turn weaknesses into growth opportunities**:

**Instead of**: "I'm bad at X"
**Reframe as**: "I'm not yet proficient at X, but I can improve by..."

**For each weakness identified**:
- Weakness: [X]
- Growth opportunity: "I'm developing skill in X by..."
- Evidence of progress: [How I'll know I'm improving]

---

## REFLECTION PROMPTS

**Deep thinking questions**:

**About the work**:
- What am I most proud of? Why?
- What was most challenging? What did I learn from it?
- If I had more time, what would I change?

**About the process**:
- How did I approach this work?
- What strategies worked? Which didn't?
- When did I feel most engaged? Most frustrated?

**About learning**:
- What did I learn about the content/skill?
- What did I learn about myself as a learner?
- How will this experience inform future work?

---

## TRACKING PROGRESS OVER TIME

**Review past self-assessments**:

**Comparison to previous work**:
- What has improved? [Specific growth]
- What remains challenging? [Persistent struggles]
- What patterns do I notice? [Trends]

**Progress on goals**:
- Previous goal: [X]
- Did I achieve it? [Yes/No/Partially]
- Evidence of progress: [Specific examples]

**Trajectory**:
- Overall trend: [Improving / Maintaining / Declining]
- Rate of growth: [Fast / Steady / Slow]
- Areas of most growth: [Strengths]
- Areas needing more focus: [Development needs]

---

## SELF-ASSESSMENT QUALITY CHECK

**Evaluate your own self-assessment**:

✅ **Honest**: Did I assess truthfully, not inflate or deflate?
✅ **Specific**: Did I use concrete evidence, not vague statements?
✅ **Balanced**: Did I recognize both strengths and weaknesses?
✅ **Actionable**: Did I identify specific improvements to make?
✅ **Growth-oriented**: Did I frame as learning opportunities?

**If any checkbox is empty, revise that section**

---

## BENEFITS OF REGULAR SELF-ASSESSMENT

**By practicing self-assessment, you develop**:
- **Metacognitive awareness**: Understanding your own thinking
- **Evaluative judgment**: Knowing what quality looks like
- **Self-regulation**: Managing your own learning
- **Independence**: Less reliant on external validation
- **Lifelong learning**: Skills for continuous improvement

**Make it a habit**: Self-assess regularly, not just for major projects

---

## FINAL REFLECTION

**Overall, this self-assessment process helped me**:
- Realize: [Insight 1]
- Appreciate: [Strength I didn't notice]
- Recognize: [Area needing attention]
- Commit to: [Specific improvement action]

**I will use self-assessment in the future by**:
- [How to integrate into regular practice]

---

**Remember**: The goal isn't perfection - it's continuous improvement. Every assessment is a learning opportunity.""",
            input_schema={
                "work_to_assess": str,
                "success_criteria": str,
                "detailed_criteria": str
            },
            constraints=Constraints(
                must_include=[
                    "evidence_based_evaluation",
                    "metacognitive_reflection",
                    "goal_setting",
                    "growth_mindset"
                ],
                must_not_include=[
                    "vague_self_praise",
                    "harsh_self_criticism"
                ],
                style_guide="Reflective and honest. Evidence-based. Growth-oriented. Link to improvement goals."
            )
        )
    
    def build_context(self, work_to_assess="", success_criteria="", **kwargs):
        """Build context for self-assessment guide."""
        newline = '\n- '
        detailed_criteria = f"- {success_criteria.replace(',', newline)}" if success_criteria else ""
        kwargs.pop('detailed_criteria', None)
        
        return super().build_context(
            work_to_assess=work_to_assess,
            success_criteria=success_criteria,
            detailed_criteria=detailed_criteria,
            **kwargs
        )
    
    def execute(self, provider="openai", work_to_assess="", success_criteria="", **kwargs):
        """Execute self-assessment guide creation."""
        newline = '\n- '
        detailed_criteria = f"- {success_criteria.replace(',', newline)}" if success_criteria else ""
        kwargs.pop('detailed_criteria', None)
        
        return super().execute(
            provider=provider,
            work_to_assess=work_to_assess,
            success_criteria=success_criteria,
            detailed_criteria=detailed_criteria,
            **kwargs
        )


__all__ = ["SelfAssessmentGuide"]
