"""
ConceptualChangeAnalyzer Pattern (Enterprise)

Help learners revise misconceptions and develop accurate mental models.
Implements conceptual change theory and misconception research.

Research Foundation:
- Posner, G. J., et al. (1982). Accommodation of a scientific conception.
- Chi, M. T. H. (2008). Three types of conceptual change: Belief revision, mental model transformation, and categorical shift.
- Vosniadou, S. (1994). Capturing and modeling the process of conceptual change.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class ConceptualChangeAnalyzer(Pattern):
    """
    Help learners revise misconceptions and build accurate mental models.
    
    Conceptual Change Process:
    1. Identify current conception (often flawed)
    2. Create dissatisfaction with current conception
    3. Present intelligible alternative
    4. Show plausibility of new conception
    5. Demonstrate fruitfulness (utility)
    
    Use Cases:
    - Science education (physics, biology misconceptions)
    - Mathematics (procedural vs conceptual understanding)
    - Medical education (clinical reasoning)
    - Technical training
    
    Example:
        >>> from mycontext.templates.enterprise.learning import ConceptualChangeAnalyzer
        >>> 
        >>> pattern = ConceptualChangeAnalyzer()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     topic="Newton's laws of motion",
        ...     current_understanding="Objects need continuous force to stay in motion"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a conceptual change expert and science educator applying Posner's "
        "framework. Help revise misconceptions and build accurate mental models.\n\n"
        "Topic: {topic}\n"
        "Current Understanding: {current_understanding}\n"
        "{context_section}\n\n"
        "Facilitate conceptual change through five steps: (1) Diagnose the "
        "misconception — classify its type (alternative framework, preconception, "
        "ontological miscategorization) and explain why it persists. "
        "(2) Create dissatisfaction — present anomalous data, internal "
        "inconsistencies, or counter-examples that the current model cannot explain. "
        "(3) Present an intelligible alternative — explain the correct conception "
        "using analogies, visual representations, and concrete examples. "
        "(4) Establish plausibility — provide scientific evidence and connect to "
        "prior knowledge to show the new conception is believable. "
        "(5) Demonstrate fruitfulness — show the new model solves problems, predicts "
        "phenomena, and has broader applications the old model lacked.\n\n"
        "Include a comparison table of old vs new conceptions and consolidation "
        "activities.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="conceptual_change_analyzer",
            description="Help learners revise misconceptions and build accurate models",
            version="1.0.0",
            tags=["learning", "enterprise", "misconceptions", "conceptual-change"],
            metadata={
                "category": "learning",
                "license": "enterprise",
                "tier": "enterprise"
            },
            guidance=Guidance(
                role="Conceptual Change Expert and Science Educator",
                rules=[
                    "Diagnose specific misconceptions, not just 'wrong answers'",
                    "Create cognitive conflict to motivate change",
                    "Present intelligible, plausible, and fruitful alternatives",
                    "Use Posner's conceptual change conditions",
                    "Address resistance to change (misconceptions are persistent)"
                ],
                style="diagnostic, empathetic, constructive, evidence-based"
            ),
            directive_template="""**CONCEPTUAL CHANGE ANALYSIS**

**TOPIC**: {topic}

**LEARNER'S CURRENT UNDERSTANDING**: {current_understanding}

---

## STEP 1: DIAGNOSE MISCONCEPTION

**Current mental model** (learner's conception):
[Describe learner's current understanding in detail]

**Type of misconception**:
- [ ] Alternative framework (coherent but incorrect theory)
- [ ] Preconception (everyday experience-based)
- [ ] Conceptual misunderstanding
- [ ] Procedural error (right steps, wrong reasoning)
- [ ] Ontological miscategorization

**Why this misconception exists**:
- Source: [Everyday experience / Intuition / Prior teaching / Analogy]
- Persistence: [Why it's hard to change]
- Internal consistency: [Does misconception "make sense" to learner?]

**Evidence of misconception**:
- [Observable signs in learner's reasoning]
- [Typical errors that result]

---

## STEP 2: CREATE DISSATISFACTION

**Make learner aware current conception is inadequate**

**Cognitive conflict strategies**:

**A. Anomalous data**: Show phenomenon current model can't explain
- Present: [Specific example that contradicts misconception]
- Ask: "How does your current understanding explain this?"
- Expected reaction: Confusion, recognition of inadequacy

**B. Internal inconsistency**: Show contradictions in their reasoning
- Point out: [Where their model contradicts itself]
- Ask: "Can both of these be true?"

**C. Counter-example**: Provide case that violates their rule
- Example: [Specific counter-example]
- Discuss: Why current model fails here

**Dissatisfaction goal**: Learner recognizes "My current understanding doesn't work"

---

## STEP 3: PRESENT INTELLIGIBLE ALTERNATIVE

**Introduce correct conception in understandable way**

**Scientific/correct conception**:
[Explain accurate understanding clearly]

**Make it intelligible (understandable)**:

**Use analogies**: Compare to familiar concepts
- Analogy: [Familiar situation that parallels correct concept]
- Mapping: [How analogy relates to target concept]

**Visual representations**: Diagrams, models
- Visual: [Specific diagram or model to use]
- Explain: How visual represents concept

**Concrete examples**: Real-world instances
- Example 1: [Concrete case showing correct concept]
- Example 2: [Another concrete case]

**Clear language**: Avoid jargon, define technical terms
- Key terms: [Define precisely]

**Check understanding**: Can learner explain it back?

---

## STEP 4: ESTABLISH PLAUSIBILITY

**Show new conception is believable and reasonable**

**Evidence supporting correct conception**:
1. [Scientific evidence / Experimental result]
2. [Expert consensus]
3. [Logical reasoning]

**Address doubts**:
- Common objection: [Anticipated resistance]
  - Response: [Why new conception handles this]

**Connect to prior knowledge**:
- Link to what learner already knows: [X, Y, Z]
- Show compatibility with accepted ideas

**Expert testimony**: "This is what scientists/experts think because..."

**Plausibility goal**: Learner thinks "This could be true"

---

## STEP 5: DEMONSTRATE FRUITFULNESS

**Show new conception is useful and powerful**

**Practical utility**:
- Solves problems old model couldn't: [Example 1]
- Predicts new phenomena: [Example 2]
- Explains previously confusing observations: [Example 3]

**Broader applications**:
- Use in [Real-world context 1]
- Use in [Real-world context 2]

**Predictive power**: New model lets you predict X, Y, Z

**Problem-solving**: Apply new conception to solve these problems:
1. [Problem 1 - unsolvable with old model]
2. [Problem 2 - easier with new model]

**Fruitfulness goal**: Learner thinks "This is useful! I can do more with this."

---

## CONCEPTUAL CHANGE STRATEGY

**Comparison table**:

| Aspect | Old Conception | New Conception |
|--------|---------------|----------------|
| Explanation | [Misconception's explanation] | [Correct explanation] |
| Limitations | [What it can't explain] | [What it CAN explain] |
| Evidence | [Weak/anecdotal] | [Strong/scientific] |
| Utility | [Limited] | [Broad applications] |

**Cognitive bridge**: Help learner transition

**What to keep** from old understanding:
- [Valid intuitions or partial truths]

**What to revise**:
- [Specific misconceptions to change]

**What to add**:
- [New knowledge not in old model]

---

## CONSOLIDATION ACTIVITIES

**Reinforce new conception through**:

1. **Contrast cases**: Compare old vs. new model predictions
   - Case: [Situation]
   - Old model predicts: [X]
   - New model predicts: [Y]
   - Actual result: [Y] ✅

2. **Explain phenomena**: Use new model to explain
   - Phenomenon 1: [Event to explain]
   - Phenomenon 2: [Event to explain]

3. **Generate predictions**: What does new model predict for...?
   - Scenario A: [Prediction]
   - Scenario B: [Prediction]

4. **Teach someone else**: Explain new conception to peer
   - Explain why old model was wrong
   - Explain why new model is better

---

## MONITORING CHANGE

**Check if conceptual change occurred**:

✅ **Surface indicators**:
- Gives correct answers
- Uses correct terminology

✅ **Deep indicators** (more important):
- Explains reasoning correctly
- Applies concept to new situations
- Recognizes when concept applies
- Can identify misconception in others

**Warning signs of incomplete change**:
- Correct answers but flawed reasoning
- Reverts to old model under pressure
- Can't apply to novel situations

**If change is incomplete**:
- Revisit cognitive conflict
- Provide more examples
- Address remaining doubts

---

## IMMEDIATE NEXT STEPS

1. Present cognitive conflict: [Specific anomaly to show]
2. Introduce correct conception: [Clear explanation]
3. Practice with: [3-5 problems requiring new model]
4. Check understanding: [Assessment questions]""",
            input_schema={
                "topic": str,
                "current_understanding": str
            },
            constraints=Constraints(
                must_include=[
                    "misconception_diagnosis",
                    "cognitive_conflict",
                    "plausible_alternative",
                    "fruitfulness"
                ],
                must_not_include=[
                    "simply_telling_correct_answer",
                    "ignoring_misconception"
                ],
                style_guide="Diagnostic and constructive. Create cognitive conflict, then guide change. Use Posner's framework."
            )
        )

    def build_context(self, topic="", current_understanding="", **kwargs):
        """Build context for conceptual change analysis."""
        return super().build_context(
            topic=topic,
            current_understanding=current_understanding,
            **kwargs
        )

    def execute(self, provider="openai", topic="", current_understanding="", **kwargs):
        """Execute conceptual change analysis."""
        return super().execute(
            provider=provider,
            topic=topic,
            current_understanding=current_understanding,
            **kwargs
        )


__all__ = ["ConceptualChangeAnalyzer"]
