"""
RubricDesigner Pattern (Enterprise)

Create clear, objective assessment criteria and scoring rubrics.
Implements rubric design best practices from Brookhart and others.

Research Foundation:
- Brookhart, S. M. (2013). How to create and use rubrics for formative assessment and grading.
- Andrade, H. G. (2000). Using rubrics to promote thinking and learning.
- Stevens, D. D., & Levi, A. J. (2013). Introduction to rubrics.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class RubricDesigner(Pattern):
    """
    Design clear, objective assessment rubrics.

    Rubric Components:
    1. Criteria: What aspects are being assessed?
    2. Performance levels: How many levels (3-5 typically)?
    3. Descriptors: What does each level look like?
    4. Scoring: How are points assigned?

    Use Cases:
    - Educational assessment
    - Performance evaluation
    - Project grading
    - Peer review frameworks

    Example:
        >>> from mycontext.templates.enterprise.evaluation import RubricDesigner
        >>>
        >>> pattern = RubricDesigner()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     assessment_task="Research paper on climate change",
        ...     learning_objectives="Synthesize sources, critical analysis, clear writing"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an assessment design expert and rubric specialist applying "
        "Brookhart's rubric design principles. Create clear, objective assessment "
        "rubrics.\n\n"
        "Assessment Task: {assessment_task}\n"
        "Learning Objectives: {learning_objectives}\n"
        "{context_section}\n\n"
        "Design the rubric: (1) Identify 3-6 criteria aligned to learning "
        "objectives, each with a weight reflecting its importance. (2) Define 4 "
        "performance levels — Exemplary, Proficient, Developing, Beginning — with "
        "clear, observable, measurable descriptors for each criterion at each level. "
        "(3) Ensure descriptors are distinct with no overlap between levels and a "
        "clear progression. (4) Create a scoring guide with total points and grade "
        "conversion. (5) Validate with a quality checklist: clarity, alignment, "
        "objectivity, distinctiveness, completeness, and usability.\n\n"
        "Avoid vague terms like 'good' or 'adequate.' Use specific, observable "
        "behaviors. Provide a sample scoring application.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="rubric_designer",
            description="Create clear, objective assessment rubrics",
            version="1.0.0",
            tags=["evaluation", "enterprise", "rubric", "assessment"],
            metadata={"category": "evaluation", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Assessment Design Expert and Rubric Specialist",
                rules=[
                    "Create criterion-referenced (not norm-referenced) rubrics",
                    "Use clear, observable, measurable descriptors",
                    "Align criteria with learning objectives",
                    "Provide 3-5 performance levels",
                    "Make descriptors distinct and specific",
                ],
                style="clear, objective, specific, actionable",
            ),
            directive_template="""**RUBRIC DESIGN**

**ASSESSMENT TASK**: {assessment_task}

**LEARNING OBJECTIVES**: {learning_objectives}

{rubric_type_section}

---

## RUBRIC STRUCTURE

**Type**: [Analytic / Holistic] Rubric
**Performance levels**: 4 (Exemplary, Proficient, Developing, Beginning)
**Scoring**: [Points per criterion]

---

## CRITERIA IDENTIFICATION

**What will be assessed?**

**Criterion 1**: [Specific aspect to evaluate]
- Aligned with objective: [Which learning objective?]
- Weight: [% of total score or points]

**Criterion 2**: [Specific aspect]
- Aligned with objective: [Which learning objective?]
- Weight: [% of total score or points]

**Criterion 3**: [Specific aspect]
- Aligned with objective: [Which learning objective?]
- Weight: [% of total score or points]

[Add 3-6 criteria total]

---

## PERFORMANCE LEVEL DESCRIPTORS

### CRITERION 1: [Name]

**Level 4 - Exemplary** (Exceeds expectations)
- [Specific, observable descriptor]
- [What exemplary performance looks like]
- [Concrete examples]
- **Points**: [X]

**Level 3 - Proficient** (Meets expectations)
- [Specific, observable descriptor]
- [What proficient performance looks like]
- [Concrete examples]
- **Points**: [X]

**Level 2 - Developing** (Approaching expectations)
- [Specific, observable descriptor]
- [What developing performance looks like]
- [What's missing or needs improvement]
- **Points**: [X]

**Level 1 - Beginning** (Below expectations)
- [Specific, observable descriptor]
- [What beginning performance looks like]
- [Major gaps]
- **Points**: [X]

---

### CRITERION 2: [Name]

**Level 4 - Exemplary**
- [Specific descriptor]
- **Points**: [X]

**Level 3 - Proficient**
- [Specific descriptor]
- **Points**: [X]

**Level 2 - Developing**
- [Specific descriptor]
- **Points**: [X]

**Level 1 - Beginning**
- [Specific descriptor]
- **Points**: [X]

---

### CRITERION 3: [Name]

[Same structure as above]

---

[Repeat for all criteria]

---

## SCORING GUIDE

**Total possible points**: [Sum of all criteria]

**Grade conversion** (if applicable):
- A: [Points range]
- B: [Points range]
- C: [Points range]
- D: [Points range]
- F: [Points range]

**OR Performance categories**:
- Exemplary: [Total points range]
- Proficient: [Total points range]
- Developing: [Total points range]
- Beginning: [Total points range]

---

## RUBRIC QUALITY CHECKLIST

✅ **Clarity**: Descriptors are clear and understandable
- Avoid vague terms like "good" or "adequate"
- Use specific, observable behaviors

✅ **Alignment**: Criteria match learning objectives
- Each criterion links to specific objective

✅ **Objectivity**: Different raters would score similarly
- Minimize subjective judgment
- Focus on observable evidence

✅ **Distinctiveness**: Each level is clearly different
- No overlap between levels
- Clear progression from level to level

✅ **Completeness**: Covers all important aspects
- No major gaps in assessment

✅ **Usability**: Easy to apply consistently
- Not too complex
- Clear scoring method

---

## USAGE GUIDELINES

**For assessors**:
1. Read entire rubric before scoring
2. Evaluate each criterion independently
3. Look for evidence of descriptors
4. Assign level based on best fit
5. Sum points for total score

**For learners** (share rubric in advance):
- Understand expectations clearly
- Self-assess before submission
- Target "Exemplary" descriptors
- Use as revision guide

---

## RUBRIC APPLICATION EXAMPLE

**Sample work excerpt**: [Brief example]

**Scoring**:
- Criterion 1: Level [X] - [Brief justification]
- Criterion 2: Level [X] - [Brief justification]
- Criterion 3: Level [X] - [Brief justification]

**Total score**: [X/Y points] = [Grade/Level]

---

## CONTINUOUS IMPROVEMENT

**After using rubric**:

**Check inter-rater reliability**:
- Do multiple raters score similarly?
- Where do disagreements occur?

**Gather feedback**:
- Is rubric clear to users?
- Are any descriptors confusing?

**Revise**:
- Clarify ambiguous descriptors
- Adjust weights if needed
- Add examples""",
            input_schema={
                "assessment_task": str,
                "learning_objectives": str,
                "rubric_type_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "clear_criteria",
                    "performance_levels",
                    "specific_descriptors",
                    "scoring_guide",
                ],
                must_not_include=["vague_descriptors", "subjective_terms"],
                style_guide="Clear, specific, observable descriptors. Aligned with objectives. 3-5 performance levels.",
            ),
        )

    def build_context(
        self, assessment_task="", learning_objectives="", rubric_type="analytic", **kwargs
    ):
        """Build context for rubric design."""
        rubric_type_section = f"**RUBRIC TYPE**: {rubric_type.capitalize()}" if rubric_type else ""
        kwargs.pop("rubric_type_section", None)

        return super().build_context(
            assessment_task=assessment_task,
            learning_objectives=learning_objectives,
            rubric_type_section=rubric_type_section,
            **kwargs,
        )

    def execute(
        self,
        provider="openai",
        assessment_task="",
        learning_objectives="",
        rubric_type="analytic",
        **kwargs,
    ):
        """Execute rubric design."""
        rubric_type_section = f"**RUBRIC TYPE**: {rubric_type.capitalize()}" if rubric_type else ""
        kwargs.pop("rubric_type_section", None)

        return super().execute(
            provider=provider,
            assessment_task=assessment_task,
            learning_objectives=learning_objectives,
            rubric_type_section=rubric_type_section,
            **kwargs,
        )


__all__ = ["RubricDesigner"]
