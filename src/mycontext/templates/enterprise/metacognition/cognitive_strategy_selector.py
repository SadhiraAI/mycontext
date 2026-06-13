"""
CognitiveStrategySelector Pattern (Enterprise)

Choose the most appropriate thinking strategy for a given task.
Implements conditional knowledge: knowing WHEN and WHY to use specific strategies.

Research Foundation:
- Pressley, M., & Harris, K. R. (2006). Cognitive strategies instruction. Handbook of Educational Psychology.
- Paris, S. G., et al. (1983). Becoming a strategic reader. Contemporary Educational Psychology, 8(3), 293-316.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class CognitiveStrategySelector(Pattern):
    """
    Select optimal cognitive strategy based on task characteristics.

    Implements strategic knowledge from Pressley & Harris (2006):
    - Declarative: What strategies exist?
    - Procedural: How to execute each strategy?
    - Conditional: WHEN and WHY to use each strategy?

    Use Cases:
    - Learning strategy selection
    - Problem-solving approach selection
    - Reading comprehension strategy choice
    - Study technique optimization

    Example:
        >>> from mycontext.templates.enterprise.metacognition import CognitiveStrategySelector
        >>>
        >>> selector = CognitiveStrategySelector()
        >>> result = selector.execute(
        ...     provider="gemini",
        ...     task_type="problem-solving",
        ...     task_characteristics="Complex, multi-step, unfamiliar domain"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a cognitive strategy expert and learning scientist. Select the "
        "optimal thinking strategy for the given task.\n\n"
        "Task Type: {task_type}\n"
        "Task Characteristics: {task_characteristics}\n"
        "{context_section}\n\n"
        "Perform strategy selection: (1) Analyze the task — complexity, familiarity, "
        "domain, cognitive demands, and time constraints. (2) Catalog relevant "
        "cognitive strategies for this task type (e.g., means-ends analysis, "
        "elaboration, decomposition, retrieval practice). (3) Match strategies to "
        "task characteristics with conditional knowledge — explain WHEN and WHY each "
        "strategy fits or doesn't. (4) Recommend a primary strategy with step-by-step "
        "procedural guidance. (5) Provide alternative strategies if the primary one "
        "stalls. (6) Identify strategies to AVOID for this task and explain why.\n\n"
        "Include implementation guidance: preparation steps, monitoring checkpoints, "
        "and success indicators.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="cognitive_strategy_selector",
            description="Select optimal cognitive strategy based on task characteristics",
            version="1.0.0",
            tags=["metacognition", "enterprise", "strategy-selection", "learning"],
            metadata={"category": "metacognition", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Cognitive Strategy Expert and Learning Scientist",
                rules=[
                    "Match strategies to task characteristics (complexity, familiarity, domain)",
                    "Provide declarative, procedural, AND conditional knowledge",
                    "Consider learner characteristics (prior knowledge, skills, preferences)",
                    "Recommend primary strategy with alternatives",
                    "Explain WHY each strategy is appropriate (or not) for this task",
                ],
                style="analytical, evidence-based, practical, educational, clear",
            ),
            directive_template="""**COGNITIVE STRATEGY SELECTION**

**TASK TYPE**: {task_type}

**TASK CHARACTERISTICS**: {task_characteristics}

{learner_section}

{available_section}

---

## STRATEGY SELECTION ANALYSIS

**1. TASK ANALYSIS** (What does this task require?)

Analyze task characteristics:
- **Complexity**: [Simple / Moderate / Complex] - Why?
- **Familiarity**: [Familiar / Partially familiar / Unfamiliar] - To whom?
- **Domain**: [What field/discipline?]
- **Cognitive demands**: [Memory / Analysis / Synthesis / Application / Evaluation]
- **Time constraints**: [Tight / Moderate / Flexible]
- **Output requirements**: [What must be produced?]

**2. STRATEGY CATALOG** (What strategies are available?)

List relevant cognitive strategies for this task type:

{strategy_catalog}

**3. STRATEGY MATCHING** (Which strategies fit this task?)

For each relevant strategy, evaluate fit:

| Strategy | Fit | Why? (Conditional Knowledge) |
|----------|-----|------------------------------|
| [Strategy A] | [High/Med/Low] | [Explain based on task characteristics] |
| [Strategy B] | [High/Med/Low] | [Explain] |
| ... | ... | ... |

**4. RECOMMENDATION**

**PRIMARY STRATEGY**: [Name]

**Why this strategy?** (Conditional knowledge)
- Task characteristic match: [Explain]
- Expected effectiveness: [Why it will work]
- Prerequisites: [What's needed to use this strategy]

**How to use it:** (Procedural knowledge)
1. [Step-by-step process]
2. [...]

**ALTERNATIVE STRATEGIES**: [If primary doesn't work, try...]

**Strategy to AVOID**: [Name] - Why: [Explain why it's unsuitable]

**5. IMPLEMENTATION GUIDANCE**

- **Before starting**: [Preparation steps]
- **During execution**: [Monitoring checkpoints]
- **If stuck**: [What to do when strategy isn't working]
- **Success indicators**: [How to know it's working]

**6. ADAPTATION PLAN**

- **If task proves easier/harder**: [How to adjust]
- **If prior knowledge insufficient**: [What to do]
- **If time runs short**: [Emergency strategies]""",
            input_schema={
                "task_type": str,
                "task_characteristics": str,
                "learner_section": str,
                "available_section": str,
                "strategy_catalog": str,
            },
            constraints=Constraints(
                must_include=[
                    "conditional_knowledge",
                    "procedural_knowledge",
                    "strategy_rationale",
                    "alternatives",
                ],
                must_not_include=["generic_advice", "strategies_without_rationale"],
                style_guide="Provide specific, justified strategy recommendations with clear conditional knowledge",
            ),
        )

    def _get_strategy_catalog(self, task_type: str) -> str:
        """Get relevant strategy catalog for task type."""

        catalogs = {
            "problem-solving": """
**Problem-Solving Strategies:**
- **Means-ends analysis**: Reduce difference between current and goal state
- **Working backward**: Start from goal, work toward current state
- **Analogical reasoning**: Use similar solved problems
- **Problem decomposition**: Break into smaller sub-problems
- **Trial and error**: Systematic testing of solutions
- **Algorithm**: Step-by-step procedure (if known)
- **Heuristic**: Rule of thumb for common cases
            """,
            "learning": """
**Learning Strategies:**
- **Elaboration**: Connect new to existing knowledge
- **Organization**: Create hierarchical structures
- **Rehearsal**: Repetition and practice
- **Retrieval practice**: Test yourself
- **Spaced repetition**: Distribute practice over time
- **Interleaving**: Mix different topics
- **Self-explanation**: Explain concepts in own words
- **Concept mapping**: Visual knowledge organization
            """,
            "reading": """
**Reading Comprehension Strategies:**
- **Previewing**: Survey text before reading
- **Questioning**: Generate questions while reading
- **Summarizing**: Condense main ideas
- **Clarifying**: Identify and resolve confusion
- **Predicting**: Anticipate what comes next
- **Visualizing**: Create mental images
- **Monitoring**: Track comprehension continuously
            """,
            "decision-making": """
**Decision-Making Strategies:**
- **Systematic comparison**: Pros/cons analysis
- **Multi-criteria**: Weight multiple factors
- **Satisficing**: First acceptable option
- **Elimination by aspects**: Remove unacceptable options
- **Intuitive judgment**: Pattern recognition (if experienced)
- **Decision matrix**: Formal scoring
            """,
            "writing": """
**Writing Strategies:**
- **Planning**: Outline before writing
- **Drafting**: Get ideas down first
- **Revising**: Improve content and structure
- **Editing**: Fix mechanics and style
- **Free writing**: Overcome writer's block
- **Audience analysis**: Adapt to readers
            """,
        }

        return catalogs.get(
            task_type,
            """
**General Cognitive Strategies:**
- **Analysis**: Break down into components
- **Synthesis**: Combine elements into whole
- **Evaluation**: Judge quality against criteria
- **Application**: Use knowledge in new situations
- **Comprehension**: Understand meaning
- **Memorization**: Encode and retrieve
        """,
        )

    def build_context(
        self,
        task_type="",
        task_characteristics="",
        learner_characteristics="",
        available_strategies="",
        **kwargs,
    ):
        """
        Build context for strategy selection.

        Args:
            task_type: Type of task (e.g., "problem-solving", "learning", "reading")
            task_characteristics: Key features of the task
            learner_characteristics: Optional learner traits (prior knowledge, skills)
            available_strategies: Optional list of strategies under consideration
            **kwargs: Additional options

        Returns:
            Context object ready for use
        """
        # Format optional sections
        learner_section = (
            f"**LEARNER CHARACTERISTICS**: {learner_characteristics}"
            if learner_characteristics
            else ""
        )
        available_section = (
            f"**STRATEGIES UNDER CONSIDERATION**: {available_strategies}"
            if available_strategies
            else ""
        )

        # Get strategy catalog for this task type
        strategy_catalog = self._get_strategy_catalog(task_type.lower())

        # Clean kwargs
        kwargs.pop("learner_section", None)
        kwargs.pop("available_section", None)
        kwargs.pop("strategy_catalog", None)

        return super().build_context(
            task_type=task_type,
            task_characteristics=task_characteristics,
            learner_section=learner_section,
            available_section=available_section,
            strategy_catalog=strategy_catalog,
            **kwargs,
        )

    def execute(
        self,
        provider="gemini",
        task_type="",
        task_characteristics="",
        learner_characteristics="",
        available_strategies="",
        **kwargs,
    ):
        """
        Execute cognitive strategy selection.

        Args:
            provider: LLM provider
            task_type: Type of task
            task_characteristics: Key features of the task
            learner_characteristics: Optional learner traits
            available_strategies: Optional strategies to consider
            **kwargs: Additional provider options

        Returns:
            ProviderResponse with strategy recommendation
        """
        learner_section = (
            f"**LEARNER CHARACTERISTICS**: {learner_characteristics}"
            if learner_characteristics
            else ""
        )
        available_section = (
            f"**STRATEGIES UNDER CONSIDERATION**: {available_strategies}"
            if available_strategies
            else ""
        )
        strategy_catalog = self._get_strategy_catalog(task_type.lower())

        kwargs.pop("learner_section", None)
        kwargs.pop("available_section", None)
        kwargs.pop("strategy_catalog", None)

        return super().execute(
            provider=provider,
            task_type=task_type,
            task_characteristics=task_characteristics,
            learner_section=learner_section,
            available_section=available_section,
            strategy_catalog=strategy_catalog,
            **kwargs,
        )


__all__ = ["CognitiveStrategySelector"]
