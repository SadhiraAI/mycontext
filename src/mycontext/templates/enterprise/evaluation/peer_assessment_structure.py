"""
PeerAssessmentStructure Pattern (Enterprise)

Design structured peer review frameworks.
Implements peer assessment best practices from Topping and others.

Research Foundation:
- Topping, K. J. (1998). Peer assessment between students in colleges and universities.
- Gielen, S., et al. (2010). A comparative study of peer and teacher feedback.
- Nicol, D., Thomson, A., & Breslin, C. (2014). Rethinking feedback practices in higher education.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class PeerAssessmentStructure(Pattern):
    """
    Design structured peer review frameworks.
    
    Benefits of Peer Assessment:
    - Develops evaluative judgment
    - Provides multiple perspectives
    - Increases engagement
    - Scales better than teacher-only feedback
    
    Use Cases:
    - Writing assignments
    - Project reviews
    - Presentations
    - Code review
    
    Example:
        >>> from mycontext.templates.enterprise.evaluation import PeerAssessmentStructure
        >>> 
        >>> pattern = PeerAssessmentStructure()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     assessment_task="Research paper peer review",
        ...     learning_objective="Evaluate research quality and provide constructive feedback"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a peer assessment design expert applying Topping's research on "
        "effective peer review. Structure a peer assessment framework.\n\n"
        "Assessment Task: {assessment_task}\n"
        "Learning Objective: {learning_objective}\n"
        "{context_section}\n\n"
        "Design the peer assessment: (1) Define review structure — type "
        "(single-blind, double-blind, open), number of reviewers per work (2-3), "
        "and assignment method. (2) Create reviewer training — teach criteria "
        "understanding, constructive feedback principles (specific, actionable, "
        "kind, balanced), and practice with sample work. (3) Design the review "
        "template — criterion-based evaluation with ratings, strengths, suggestions, "
        "and overall recommendation. (4) Establish feedback guidelines — what "
        "reviewers should DO (be specific, give examples, explain reasoning) and "
        "should NOT do (be vague, be harsh, impose personal style). "
        "(5) Build quality control — teacher monitoring, review-the-reviews "
        "meta-feedback, and accountability mechanisms.\n\n"
        "Include a peer review rubric assessing specificity, actionability, balance, "
        "thoroughness, and professionalism.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="peer_assessment_structure",
            description="Design structured peer review frameworks",
            version="1.0.0",
            tags=["evaluation", "enterprise", "peer-assessment", "feedback"],
            metadata={
                "category": "evaluation",
                "license": "enterprise",
                "tier": "enterprise"
            },
            guidance=Guidance(
                role="Peer Assessment Design Expert",
                rules=[
                    "Provide clear criteria and structure for peer review",
                    "Train reviewers in giving constructive feedback",
                    "Use anonymous or double-blind review when appropriate",
                    "Balance positive and critical feedback",
                    "Include accountability mechanisms"
                ],
                style="structured, constructive, fair, developmental"
            ),
            directive_template="""**PEER ASSESSMENT STRUCTURE**

**ASSESSMENT TASK**: {assessment_task}

**LEARNING OBJECTIVE**: {learning_objective}

---

## PEER ASSESSMENT RATIONALE

**Why peer assessment**:
- Develops critical evaluation skills
- Provides diverse perspectives
- Increases volume of feedback
- Promotes deeper learning
- Prepares for professional peer review

**Research evidence**: Peer assessment, when structured well, is as effective as teacher feedback (Gielen et al., 2010)

---

## PEER REVIEW STRUCTURE

**Type**: [Single-blind / Double-blind / Open]
**Number of reviewers per work**: [2-3 recommended]
**Review assignments**: [Random / Strategic / Self-selected]

---

## REVIEWER TRAINING

**Before peer assessment begins, train reviewers**:

**Session 1: Understanding criteria** (15 min)
- Review rubric or criteria
- Discuss what quality looks like
- Show exemplar work

**Session 2: Constructive feedback** (20 min)
- Teach feedback principles:
  - Specific (not vague)
  - Actionable (can be implemented)
  - Kind (respectful tone)
  - Balanced (strengths + improvements)

**Session 3: Practice** (25 min)
- Review sample work together
- Practice giving feedback
- Discuss common pitfalls

---

## PEER REVIEW CRITERIA

**Criteria reviewers will use**:

**Criterion 1**: [Specific aspect]
- Look for: [Observable indicators]
- Questions to consider: [Guiding questions]

**Criterion 2**: [Specific aspect]
- Look for: [Observable indicators]
- Questions to consider: [Guiding questions]

**Criterion 3**: [Specific aspect]
- Look for: [Observable indicators]
- Questions to consider: [Guiding questions]

[Add 4-6 criteria total]

---

## PEER REVIEW TEMPLATE

**Provide structured template for consistency**:

---

**PEER REVIEW FORM**

**Reviewer name**: [Or anonymous code]
**Author**: [Name or code]
**Date**: [Date]

---

### OVERALL IMPRESSION (1-2 sentences)
[What stands out about this work?]

---

### CRITERION-BASED EVALUATION

**Criterion 1: [Name]**
**Rating**: ⭐⭐⭐⭐⭐ (1-5)
**Strengths**: [What's working well for this criterion]
**Suggestions**: [Specific ways to improve]

**Criterion 2: [Name]**
**Rating**: ⭐⭐⭐⭐⭐
**Strengths**: [What's working]
**Suggestions**: [How to improve]

**Criterion 3: [Name]**
**Rating**: ⭐⭐⭐⭐⭐
**Strengths**: [What's working]
**Suggestions**: [How to improve]

[Repeat for all criteria]

---

### TOP 3 STRENGTHS
1. [Specific positive observation]
2. [Specific positive observation]
3. [Specific positive observation]

### TOP 3 SUGGESTIONS FOR IMPROVEMENT
1. [Specific, actionable suggestion]
2. [Specific, actionable suggestion]
3. [Specific, actionable suggestion]

---

### QUESTIONS FOR AUTHOR
[Any clarifying questions or areas needing explanation]

---

### OVERALL RECOMMENDATION
- [ ] Exceeds expectations
- [ ] Meets expectations
- [ ] Approaches expectations
- [ ] Needs significant revision

---

**END OF REVIEW FORM**

---

## FEEDBACK GUIDELINES

**Teach reviewers to give effective feedback**:

✅ **DO**:
- Be specific: "The introduction clearly states the thesis" not "Good intro"
- Be actionable: "Add data to support claim in paragraph 3"
- Be kind: Professional, respectful tone
- Explain reasoning: "This works because..."
- Give examples: "For instance, when you said X..."

❌ **DON'T**:
- Be vague: "This is confusing" (Say what's confusing and why)
- Be mean: Criticism should be constructive, not harsh
- Focus only on negatives: Balance criticism with positives
- Impose your style: Suggest improvements, don't demand your approach
- Review carelessly: Give thoughtful, thorough feedback

---

## QUALITY CONTROL

**Ensure peer reviews are helpful**:

**Teacher monitors reviews**:
- Read sample of peer reviews
- Check for quality and appropriateness
- Intervene if reviews are unhelpful or unkind

**Review the reviews** (metacognitive):
- Authors rate usefulness of feedback received
- Discuss what makes feedback helpful
- Improve review process based on meta-feedback

**Accountability**:
- Grade or credit for providing good reviews
- Rubric for assessing review quality
- Peer reviewers accountable for effort

---

## PEER REVIEW RUBRIC

**Assessing quality of peer review**:

| Criterion | Excellent (5) | Good (4) | Fair (3) | Poor (2) |
|-----------|--------------|----------|----------|----------|
| **Specificity** | Highly specific examples | Mostly specific | Somewhat vague | Very vague |
| **Actionability** | Clear, implementable suggestions | Mostly actionable | Somewhat helpful | Not actionable |
| **Balance** | Good balance of +/- | Slightly unbalanced | Mostly negative | All negative/positive |
| **Thoroughness** | Addresses all criteria | Addresses most | Addresses some | Incomplete |
| **Professionalism** | Respectful, constructive | Mostly professional | Adequate tone | Inappropriate tone |

---

## IMPLEMENTATION PROCESS

**Step 1**: Train reviewers (1 hour)
- Criteria understanding
- Feedback principles
- Practice with samples

**Step 2**: Assign reviews (1-2 days before due)
- Each work gets 2-3 reviews
- Distribute assignments
- Provide deadline

**Step 3**: Conduct reviews (3-5 days)
- Reviewers use structured template
- Submit by deadline
- Teacher monitors quality

**Step 4**: Authors receive feedback (same day)
- Get multiple perspectives
- Synthesize common themes
- Identify actionable improvements

**Step 5**: Revision opportunity (optional)
- Authors revise based on peer feedback
- Resubmit improved version
- Demonstrate responsiveness to feedback

**Step 6**: Reflection (15 min)
- "What did you learn from reviewing others' work?"
- "What feedback was most helpful?"
- "How did peer review improve your own work?"

---

## PEER ASSESSMENT VARIATIONS

**Anonymous vs. Open**:
- **Anonymous**: More honest, less social pressure
- **Open**: More accountability, relationship building

**Reciprocal vs. One-way**:
- **Reciprocal**: Partners review each other
- **One-way**: Different reviewers and authors

**Formative vs. Summative**:
- **Formative**: For improvement only (no grade impact)
- **Summative**: Counts toward grade (higher stakes)

**Recommendation**: Start with anonymous, formative, one-way

---

## CHALLENGES AND SOLUTIONS

**Challenge 1**: Unhelpful reviews ("Good job!")
- **Solution**: Require specific evidence and suggestions
- **Solution**: Grade review quality
- **Solution**: Provide sentence starters

**Challenge 2**: Harsh or mean feedback
- **Solution**: Train in constructive feedback
- **Solution**: Teacher reviews before sharing
- **Solution**: Anonymous reporting mechanism

**Challenge 3**: Free-riding (careless reviews)
- **Solution**: Assess review quality
- **Solution**: Require justification for ratings
- **Solution**: Meta-feedback from recipients

**Challenge 4**: Bias (friends give high ratings)
- **Solution**: Use anonymous review
- **Solution**: Multiple reviewers (outliers identified)
- **Solution**: Teacher moderation

---

## SUCCESS INDICATORS

**Peer assessment is working when**:

✅ Reviews are specific and actionable
✅ Authors find feedback useful
✅ Work quality improves through revision
✅ Reviewers develop evaluative judgment
✅ Process is fair and respectful

---

## REFLECTION PROMPTS

**For reviewers**:
- "What did reviewing others' work teach you?"
- "What surprised you about their approach?"
- "How will this inform your own work?"

**For authors**:
- "What feedback was most helpful? Why?"
- "What will you change based on peer feedback?"
- "Did reviewers identify issues you hadn't noticed?"

---

## INTEGRATION WITH TEACHER FEEDBACK

**Peer feedback + Teacher feedback = Comprehensive**:

- Peers provide volume and diverse perspectives
- Teacher provides expert guidance and final judgment
- Authors triangulate multiple sources of feedback
- Best of both worlds""",
            input_schema={
                "assessment_task": str,
                "learning_objective": str
            },
            constraints=Constraints(
                must_include=[
                    "reviewer_training",
                    "structured_template",
                    "feedback_guidelines",
                    "quality_control"
                ],
                must_not_include=[
                    "unstructured_review",
                    "no_training"
                ],
                style_guide="Structured and supportive. Train reviewers. Balance positive and critical feedback."
            )
        )

    def build_context(self, assessment_task="", learning_objective="", **kwargs):
        """Build context for peer assessment design."""
        return super().build_context(
            assessment_task=assessment_task,
            learning_objective=learning_objective,
            **kwargs
        )

    def execute(self, provider="openai", assessment_task="", learning_objective="", **kwargs):
        """Execute peer assessment structure design."""
        return super().execute(
            provider=provider,
            assessment_task=assessment_task,
            learning_objective=learning_objective,
            **kwargs
        )


__all__ = ["PeerAssessmentStructure"]
