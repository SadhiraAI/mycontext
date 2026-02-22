"""
ScaffoldingFramework Pattern (Enterprise)

Provide temporary support structures that fade as learner gains competence.
Implements Vygotsky's scaffolding principle and Wood et al.'s framework.

Research Foundation:
- Wood, D., Bruner, J. S., & Ross, G. (1976). The role of tutoring in problem solving.
- Vygotsky, L. S. (1978). Mind in society: The development of higher psychological processes.
- van de Pol, J., Volman, M., & Beishuizen, J. (2010). Scaffolding in teacher-student interaction.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class ScaffoldingFramework(Pattern):
    """
    Provide temporary support that fades as competence increases.
    
    Scaffolding Types:
    1. Modeling - Demonstrate the skill
    2. Coaching - Provide hints and feedback
    3. Articulation - Have learner explain thinking
    4. Reflection - Compare performance to experts
    5. Exploration - Encourage problem-solving
    6. Fading - Gradually remove support
    
    Use Cases:
    - Tutoring systems
    - Skill development
    - Complex task training
    - Personalized learning
    
    Example:
        >>> from mycontext.templates.enterprise.learning import ScaffoldingFramework
        >>> 
        >>> pattern = ScaffoldingFramework()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     task="Learn to write recursive functions",
        ...     current_skill_level="Can write loops, unfamiliar with recursion"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert instructor applying Vygotsky's scaffolding principle. "
        "Design temporary support structures that fade as competence grows.\n\n"
        "Task: {task}\n"
        "Current Skill Level: {current_skill_level}\n"
        "Goal: {goal}\n"
        "{context_section}\n\n"
        "Design a scaffolding strategy: (1) Assess current competence — what the "
        "learner can do independently, what they can do with support (Zone of "
        "Proximal Development), and what is beyond current reach. (2) Select "
        "scaffolding types — modeling (demonstrate), coaching (hints and feedback), "
        "articulation (explain thinking), reflection (compare to experts), and "
        "exploration (guided discovery). (3) Build a phased support structure — "
        "Phase 1: maximum support, Phase 2: moderate support, Phase 3: minimal "
        "support, Phase 4: independence. (4) Define a fading strategy with explicit "
        "triggers for reducing support. (5) Include checkpoint questions to verify "
        "understanding before fading.\n\n"
        "Provide just enough support — not too much, not too little.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="scaffolding_framework",
            description="Provide temporary support structures that fade as competence increases",
            version="1.0.0",
            tags=["learning", "enterprise", "scaffolding", "vygotsky"],
            metadata={
                "category": "learning",
                "license": "enterprise",
                "tier": "enterprise"
            },
            guidance=Guidance(
                role="Expert Instructor and Learning Scaffold Designer",
                rules=[
                    "Apply Vygotsky's scaffolding principle: support within Zone of Proximal Development",
                    "Provide JUST ENOUGH support - not too much, not too little",
                    "Plan explicit fading strategy (how support will be removed)",
                    "Use multiple scaffolding types (modeling, coaching, articulation)",
                    "Check for understanding before reducing support"
                ],
                style="supportive, adaptive, structured, encouraging"
            ),
            directive_template="""**SCAFFOLDING FRAMEWORK**

**TASK**: {task}

**LEARNER'S CURRENT SKILL LEVEL**: {current_skill_level}

{goal_section}

---

## SCAFFOLDING STRATEGY

### 1. ASSESS CURRENT COMPETENCE

**What learner can do independently**: [List capabilities]

**What learner can do with support**: [Zone of Proximal Development]

**What is beyond current reach**: [Future learning]

**Gap to bridge**: [Specific skills/knowledge needed]

---

### 2. SCAFFOLDING TYPE SELECTION

Choose appropriate scaffolding types (use multiple):

**A. MODELING** (Demonstrate):
- When: [When to show examples]
- What to model: [Specific skills/processes to demonstrate]
- How: [Demonstration method]

**B. COACHING** (Hints & Feedback):
- Hints: [Progressive hints from light to heavy]
- Feedback: [Specific, actionable feedback]
- Questions: [Guiding questions]

**C. ARTICULATION** (Explain Thinking):
- Prompts: [Get learner to verbalize reasoning]
- Think-aloud: [Have learner explain steps]

**D. REFLECTION** (Compare to Experts):
- Expert comparison: [Show expert approach]
- Self-assessment: [Help learner evaluate own work]

**E. EXPLORATION** (Guided Discovery):
- Challenges: [Problems to solve]
- Constraints: [Helpful boundaries]
- Resources: [Tools/materials available]

---

### 3. SUPPORT STRUCTURE (Detailed)

**PHASE 1: MAXIMUM SUPPORT** (Initial learning)

Step-by-step guidance:
1. [First step with heavy support]
2. [Second step with heavy support]
...

Provided resources:
- [Templates, examples, checklists]

---

**PHASE 2: MODERATE SUPPORT** (Developing competence)

Reduced guidance:
1. [First step with medium support]
2. [Second step with medium support]
...

Provided resources:
- [Fewer templates, more open-ended]

---

**PHASE 3: MINIMAL SUPPORT** (Near independence)

Light guidance:
1. [First step with light support]
2. [Second step with light support]
...

Provided resources:
- [Just-in-time help, references]

---

**PHASE 4: INDEPENDENCE** (Full competence)

Self-directed:
- [No scaffolding, learner works independently]
- [Available if needed]

---

### 4. FADING STRATEGY

**How to remove support gradually**:

**Triggers for fading** (move to next phase when):
- Learner demonstrates X
- Success rate reaches Y%
- Can explain reasoning clearly

**Fading method**:
- [Gradual reduction plan]
- [Checkpoints for assessment]

**Monitoring**:
- [How to know if fading too fast]
- [How to know if maintaining support too long]

---

### 5. CHECKPOINT QUESTIONS

Before fading support, check:

1. **Understanding**: Can learner explain WHY, not just HOW?
2. **Application**: Can learner apply to new examples?
3. **Independence**: Can learner work without prompting?
4. **Error detection**: Can learner find own mistakes?

---

### 6. IMPLEMENTATION PLAN

**Immediate next steps**:
1. [Start with this scaffolding]
2. [Provide this support]
3. [Check for this understanding]

**Success criteria**: [How to know scaffolding is working]

**Warning signs**: [Indicators that support needs adjustment]""",
            input_schema={
                "task": str,
                "current_skill_level": str,
                "goal_section": str
            },
            constraints=Constraints(
                must_include=[
                    "assess_competence",
                    "scaffolding_types",
                    "fading_strategy",
                    "checkpoint_questions"
                ],
                must_not_include=[
                    "one_size_fits_all",
                    "permanent_support"
                ],
                style_guide="Adaptive support that gradually reduces. Balance help with independence."
            )
        )

    def build_context(self, task="", current_skill_level="", goal="", **kwargs):
        """Build context for scaffolding design."""
        goal_section = f"**GOAL**: {goal}" if goal else ""
        kwargs.pop('goal_section', None)

        return super().build_context(
            task=task,
            current_skill_level=current_skill_level,
            goal_section=goal_section,
            **kwargs
        )

    def execute(self, provider="openai", task="", current_skill_level="", goal="", **kwargs):
        """Execute scaffolding framework design."""
        goal_section = f"**GOAL**: {goal}" if goal else ""
        kwargs.pop('goal_section', None)

        return super().execute(
            provider=provider,
            task=task,
            current_skill_level=current_skill_level,
            goal_section=goal_section,
            **kwargs
        )


__all__ = ["ScaffoldingFramework"]
