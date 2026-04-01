"""
CognitiveLoadManager Pattern (Enterprise)

Manage intrinsic, extraneous, and germane cognitive load for optimal learning.
Implements Sweller's Cognitive Load Theory.

Research Foundation:
- Sweller, J. (1988). Cognitive load during problem solving.
- Chandler, P., & Sweller, J. (1991). Cognitive load theory and the format of instruction.
- Mayer, R. E., & Moreno, R. (2003). Nine ways to reduce cognitive load in multimedia learning.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class CognitiveLoadManager(Pattern):
    """
    Optimize cognitive load for effective learning.

    Three Types of Cognitive Load:
    1. Intrinsic: Inherent difficulty of material
    2. Extraneous: Unnecessary cognitive burden (reduce this!)
    3. Germane: Effort toward schema construction (increase this!)

    Use Cases:
    - Instructional design
    - Educational content creation
    - Training program design
    - Learning interface design

    Example:
        >>> from mycontext.templates.enterprise.learning import CognitiveLoadManager
        >>>
        >>> pattern = CognitiveLoadManager()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     learning_material="Quantum mechanics course module",
        ...     learner_background="Undergraduate physics students"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a cognitive load expert and instructional designer applying "
        "Sweller's Cognitive Load Theory. Optimize learning by managing three types "
        "of cognitive load.\n\n"
        "Learning Material: {learning_material}\n"
        "Learner Background: {learner_background}\n"
        "{context_section}\n\n"
        "Analyze and optimize cognitive load: (1) Intrinsic load — assess inherent "
        "material difficulty (element interactivity, concept complexity, prerequisite "
        "knowledge). If too high, break into smaller chunks or teach prerequisites "
        "first. (2) Extraneous load — REDUCE by eliminating split attention, "
        "redundancy, unclear instructions, poor organization, and distracting "
        "elements. Apply Mayer's multimedia principles. (3) Germane load — INCREASE "
        "by adding worked examples, self-explanation prompts, comparison activities, "
        "schema activation, and varied practice.\n\n"
        "Stay within working memory limits (7 +/- 2 chunks). Provide a phased "
        "optimization plan and a chunking strategy with estimated durations.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="cognitive_load_manager",
            description="Manage cognitive load for optimal learning",
            version="1.0.0",
            tags=["learning", "enterprise", "cognitive-load", "instructional-design"],
            metadata={"category": "learning", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Cognitive Load Expert and Instructional Designer",
                rules=[
                    "Apply Sweller's Cognitive Load Theory",
                    "Reduce extraneous load (unnecessary complexity)",
                    "Optimize intrinsic load (appropriate difficulty)",
                    "Increase germane load (schema-building effort)",
                    "Stay within working memory limits (7±2 chunks)",
                ],
                style="analytical, precise, learner-centered, evidence-based",
            ),
            directive_template="""**COGNITIVE LOAD ANALYSIS**

**LEARNING MATERIAL**: {learning_material}

**LEARNER BACKGROUND**: {learner_background}

---

## WORKING MEMORY CAPACITY

**Human working memory**: Limited to 7±2 chunks simultaneously
**Implication**: Must carefully manage cognitive demands

---

## THREE-TYPE LOAD ANALYSIS

### 1. INTRINSIC LOAD (Material Difficulty)
**Definition**: Inherent complexity of the material itself

**Current intrinsic load**: [Low / Medium / High]

**Factors contributing to intrinsic load**:
- Number of interacting elements: [X]
- Concept difficulty: [Simple / Complex]
- Prior knowledge required: [None / Some / Extensive]

**Intrinsic load assessment**:
- Too low → Material too simple, not challenging enough
- Optimal → Appropriate for learner level
- Too high → Overwhelms learner, needs prerequisite work

**Recommendation for intrinsic load**:
[If too high]: Reduce by breaking into smaller chunks, teaching prerequisites first
[If optimal]: Maintain current level
[If too low]: Increase difficulty, add complexity

---

### 2. EXTRANEOUS LOAD (Unnecessary Burden) ❌ REDUCE THIS

**Definition**: Cognitive load from poor presentation, not the material itself

**Current sources of extraneous load** (identify and eliminate):

❌ **Split attention**: Information sources separated
- Example: [Text far from diagram]
- Fix: [Integrate text and diagram]

❌ **Redundancy**: Same information presented multiple ways unnecessarily
- Example: [Text that duplicates what diagram shows]
- Fix: [Remove redundant text]

❌ **Unclear instructions**: Confusing or ambiguous directions
- Example: [Vague wording]
- Fix: [Clear, concise instructions]

❌ **Poor organization**: Illogical sequence or structure
- Example: [Random order of topics]
- Fix: [Logical progression]

❌ **Distracting elements**: Irrelevant information or decorations
- Example: [Unnecessary animations, backgrounds]
- Fix: [Remove distractions]

❌ **Cognitive overload**: Too much at once
- Example: [30 new terms in one lesson]
- Fix: [Chunk into smaller units]

**Extraneous load reduction strategies**:
1. [Specific fix 1]
2. [Specific fix 2]
3. [Specific fix 3]

**Expected extraneous load after fixes**: [Minimal]

---

### 3. GERMANE LOAD (Schema Building) ✅ INCREASE THIS

**Definition**: Cognitive effort directed toward learning and schema construction

**Current germane load**: [Low / Medium / High]

**Ways to increase germane load** (productive learning effort):

✅ **Worked examples**: Show expert solutions with explanations
- Include: [Example problems with detailed reasoning]

✅ **Self-explanation prompts**: Ask learner to explain
- Prompts: ["Why does this work?", "What principle is this?"]

✅ **Comparisons**: Contrast correct and incorrect approaches
- Show: [Good example vs. common error]

✅ **Schema activation**: Connect to prior knowledge
- Links: [Relate new concept to X they already know]

✅ **Completion problems**: Partially worked problems
- Provide: [Solution steps 1-3, learner completes 4-6]

✅ **Variability**: Multiple examples showing concept variety
- Examples: [3-5 diverse applications]

**Germane load enhancement plan**:
1. [Specific technique 1]
2. [Specific technique 2]
3. [Specific technique 3]

---

## LOAD BALANCING STRATEGY

**Total cognitive load = Intrinsic + Extraneous + Germane**

**Current state**:
- Intrinsic: [Level]
- Extraneous: [Level] → **Reduce**
- Germane: [Level] → **Increase**
- Total: [Manageable / Overload]

**Optimization plan**:

**Phase 1**: Reduce extraneous load
- Remove: [Distractions, split attention, redundancy]
- Expected reduction: [X%]

**Phase 2**: Adjust intrinsic load (if needed)
- [Break into chunks / Teach prerequisites / Maintain]

**Phase 3**: Increase germane load
- Add: [Worked examples, self-explanation, etc.]
- Target productive effort on schema building

**Result**: Optimal load for learning

---

## CHUNKING STRATEGY

**Break material into manageable chunks**:

**Chunk 1**: [Topic]
- Elements: [3-5 related concepts]
- Duration: [15-20 minutes]
- Cognitive load: [Manageable]

**Chunk 2**: [Topic]
- Elements: [3-5 related concepts]
- Duration: [15-20 minutes]
- Cognitive load: [Manageable]

...

**Integration phase**: Combine chunks into coherent whole
- After learners master individual chunks
- Show how chunks relate

---

## MAYER'S PRINCIPLES (Reduce Extraneous Load)

Apply these evidence-based principles:

1. **Coherence**: Remove extraneous content
2. **Signaling**: Highlight essential material
3. **Redundancy**: Avoid unnecessary duplication
4. **Spatial contiguity**: Place related info together
5. **Temporal contiguity**: Present related info simultaneously
6. **Segmenting**: Break into learner-paced segments
7. **Pre-training**: Teach components before complex process
8. **Modality**: Use audio + visual (not just visual)
9. **Personalization**: Use conversational style

**Applied to this material**: [Which principles to use and how]

---

## IMPLEMENTATION CHECKLIST

Before presenting material, ensure:

✅ Extraneous load minimized (removed distractions)
✅ Intrinsic load appropriate (right difficulty level)
✅ Germane load optimized (productive learning effort)
✅ Chunked appropriately (7±2 elements per chunk)
✅ Clear instructions (no ambiguity)
✅ Worked examples included
✅ Self-explanation prompts added

---

## MONITORING & ADJUSTMENT

**Signs of cognitive overload**:
- Learner confusion or frustration
- Many errors
- Slow progress
- Giving up

**If overload occurs**:
1. Reduce extraneous load immediately
2. Break into smaller chunks
3. Provide more scaffolding
4. Slow down pace

**Success indicators**:
- Learner engagement
- Steady progress
- Able to explain concepts
- Applying knowledge""",
            input_schema={"learning_material": str, "learner_background": str},
            constraints=Constraints(
                must_include=[
                    "three_load_types",
                    "extraneous_reduction",
                    "germane_increase",
                    "chunking_strategy",
                ],
                must_not_include=["cognitive_overload", "poor_organization"],
                style_guide="Analytical and precise. Focus on load optimization. Evidence-based principles.",
            ),
        )

    def build_context(self, learning_material="", learner_background="", **kwargs):
        """Build context for cognitive load management."""
        return super().build_context(
            learning_material=learning_material, learner_background=learner_background, **kwargs
        )

    def execute(self, provider="openai", learning_material="", learner_background="", **kwargs):
        """Execute cognitive load analysis."""
        return super().execute(
            provider=provider,
            learning_material=learning_material,
            learner_background=learner_background,
            **kwargs,
        )


__all__ = ["CognitiveLoadManager"]
