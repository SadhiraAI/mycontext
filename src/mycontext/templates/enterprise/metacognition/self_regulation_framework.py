"""
SelfRegulationFramework Pattern (Enterprise)

Plan → Monitor → Evaluate performance in a cyclical process.
Implements Zimmerman's (2002) three-phase self-regulated learning model.

Research Foundation:
- Zimmerman, B. J. (2002). Becoming a self-regulated learner. Theory Into Practice, 41(2), 64-70.
- Efklides, A. (2024). Revisiting the MASRL model. Educational Psychology Review, 36(1), Article 14.
- Pintrich, P. R. (2000). The role of goal orientation in self-regulated learning.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class SelfRegulationFramework(Pattern):
    """
    Cyclical self-regulation: Plan → Monitor → Evaluate → Adjust.
    
    Implements Zimmerman's (2002) three-phase model:
    1. FORETHOUGHT: Goal setting, strategic planning, motivation
    2. PERFORMANCE: Self-control, self-monitoring, strategy execution
    3. SELF-REFLECTION: Self-evaluation, causal attribution, adaptation
    
    Use Cases:
    - Learning skills systematically
    - Performance improvement
    - Goal achievement
    - Skill development coaching
    
    Example:
        >>> from mycontext.templates.enterprise.metacognition import SelfRegulationFramework
        >>> 
        >>> framework = SelfRegulationFramework()
        >>> result = framework.execute(
        ...     provider="gemini",
        ...     goal="Master data structures",
        ...     current_phase="forethought"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a self-regulated learning coach applying Zimmerman's three-phase "
        "model. Guide cyclical self-regulation for the given goal.\n\n"
        "Goal: {goal}\n"
        "Current Phase: {current_phase}\n"
        "{context_section}\n\n"
        "Apply Zimmerman's (2002) three-phase cycle:\n"
        "FORETHOUGHT: Set specific, measurable goals with sub-milestones. Select "
        "strategies based on task analysis. Activate motivation through intrinsic "
        "interest, outcome expectations, and self-efficacy.\n"
        "PERFORMANCE: Execute strategies while self-monitoring progress and quality. "
        "Maintain focus and attention. Track what's working and what isn't.\n"
        "SELF-REFLECTION: Evaluate outcomes honestly. Apply accurate causal "
        "attribution — focus on changeable factors (strategy, effort, preparation), "
        "not fixed traits or luck. Plan specific improvements for the next cycle.\n\n"
        "Self-regulation is cyclical: each phase informs the next. Always specify "
        "what to do in the NEXT phase of the cycle.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="self_regulation_framework",
            description="Cyclical self-regulation: Plan → Monitor → Evaluate → Adjust",
            version="1.0.0",
            tags=["metacognition", "enterprise", "self-regulation", "goal-setting"],
            metadata={
                "category": "metacognition",
                "license": "enterprise",
                "tier": "enterprise"
            },
            guidance=Guidance(
                role="Self-Regulated Learning Coach and Performance Scientist",
                rules=[
                    "Apply Zimmerman's three-phase cycle: Forethought → Performance → Self-Reflection",
                    "Integrate metacognition, motivation, and affect (MASRL 2024 model)",
                    "Focus on actionable strategies for each phase",
                    "Emphasize accurate causal attribution (not just luck/talent)",
                    "Plan the NEXT cycle based on reflection results"
                ],
                style="systematic, evidence-based, actionable, motivational, growth-oriented"
            ),
            directive_template="""**SELF-REGULATED LEARNING FRAMEWORK**

**GOAL**: {goal}

**CURRENT PHASE**: {current_phase}

{context_section}

{performance_section}

---

{phase_specific_directive}

---

**CRITICAL**: At the end, specify what to do in the NEXT phase of the cycle.

Self-regulation is CYCLICAL:
Forethought → Performance → Self-Reflection → [Adjust Forethought] → Performance → ...

Each phase informs the next. Always plan the transition.""",
            input_schema={
                "goal": str,
                "current_phase": str,  # forethought | performance | self-reflection
                "context_section": str,
                "performance_section": str,
                "phase_specific_directive": str
            },
            constraints=Constraints(
                must_include=[
                    "specific_strategies",
                    "next_phase_actions",
                    "cyclical_connection"
                ],
                must_not_include=[
                    "generic_advice",
                    "attributions_to_luck_or_fixed_traits"
                ],
                style_guide="Use systematic framework with clear phase-specific actions and cyclical connections"
            )
        )

    def _get_phase_directive(self, phase: str) -> str:
        """Get phase-specific directive."""

        if phase == "forethought":
            return """## FORETHOUGHT PHASE: Planning Before Action

**Purpose**: Set goals, plan strategies, and activate motivation BEFORE beginning.

**Task Analysis:**
1. **Goal Setting** (Zimmerman 2002)
   - Specific goal: [What exactly do you want to achieve?]
   - Measurable criteria: [How will you know you succeeded?]
   - Time frame: [By when?]
   - Sub-goals: [Break into smaller milestones]

2. **Strategic Planning**
   - Task analysis: [What's required? What steps?]
   - Strategy selection: [What approach will you use?]
   - Resources needed: [What tools, help, materials?]
   - Potential obstacles: [What could go wrong?]
   - Contingency plans: [If X happens, then Y]

**Self-Motivation:**
3. **Intrinsic Interest** (Why this matters to you personally)
4. **Outcome Expectations** (What will success enable?)
5. **Self-Efficacy** (Confidence in ability - based on past evidence)
6. **Goal Orientation** (Learning-focused, not just performance-focused)

**OUTPUT**: Create a detailed plan with goals, strategies, timeline, and motivation triggers.

**NEXT PHASE**: Move to PERFORMANCE with this plan."""

        elif phase == "performance":
            return """## PERFORMANCE PHASE: Executing While Monitoring

**Purpose**: Execute strategies while monitoring progress and maintaining focus.

**Self-Control** (Zimmerman 2002):
1. **Self-Instruction**
   - What specific steps are you taking?
   - Are you following your plan?
   - What adjustments are you making in real-time?

2. **Attention Focusing**
   - Are you staying focused on the task?
   - What distractions are you managing?
   - How are you maintaining concentration?

3. **Task Strategies**
   - Which strategies are you using right now?
   - Are they working as expected?
   - Do you need to switch strategies?

**Self-Observation** (Metacognitive Monitoring):
4. **Progress Tracking**
   - How much have you accomplished?
   - Are you on pace to meet your goals?
   - What's working? What's not?

5. **Quality Monitoring**
   - Is your work meeting your standards?
   - Are there errors or issues?
   - Do you need to adjust approach?

**Motivation Maintenance:**
6. How are you staying motivated?
7. What's helping you persist through difficulties?

**OUTPUT**: Report on execution, progress, obstacles encountered, and real-time adjustments.

**NEXT PHASE**: Move to SELF-REFLECTION when task/session is complete."""

        elif phase == "self-reflection":
            return """## SELF-REFLECTION PHASE: Evaluating After Action

**Purpose**: Evaluate outcomes, understand WHY, and plan improvements for next cycle.

**Self-Judgment** (Zimmerman 2002):
1. **Self-Evaluation**
   - Did you achieve your goal? [Yes/Partial/No]
   - Quality of outcome: [Rate 1-10 with evidence]
   - Compared to plan: [Better/As expected/Worse]
   - Compared to past performance: [Better/Same/Worse]

2. **Causal Attribution** (CRITICAL - avoid fixed mindset)
   - What led to this outcome?
   - **Strategy effectiveness**: [Which strategies worked/didn't work?]
   - **Effort quality**: [Sufficient/Insufficient effort? Effective/Ineffective?]
   - **External factors**: [Environment, resources, circumstances]
   
   **AVOID**: Attributing to fixed traits ("I'm just not good at this") or pure luck.
   **FOCUS**: Changeable factors (strategies, effort, preparation).

**Self-Reaction**:
3. **Self-Satisfaction**
   - How do you feel about the outcome? Why?
   - What are you proud of?
   - What disappointed you?

4. **Adaptive Response** (Plan next cycle improvements)
   - What will you do differently next time?
   - What strategies should you keep/drop/modify?
   - What new strategies should you try?
   - What support or resources do you need?

**OUTPUT**: 
- Honest evaluation with accurate causal attribution
- Specific improvements for NEXT CYCLE
- Updated goals and strategies

**NEXT PHASE**: Return to FORETHOUGHT with improved plan based on learning."""

        else:
            return f"**ERROR**: Unknown phase '{phase}'. Must be 'forethought', 'performance', or 'self-reflection'."

    def build_context(
        self,
        goal="",
        current_phase="forethought",
        context="",
        performance_data="",
        **kwargs
    ):
        """
        Build context for self-regulation framework.
        
        Args:
            goal: The learning or performance goal
            current_phase: "forethought" | "performance" | "self-reflection"
            context: Optional situational context
            performance_data: Performance results (for reflection phase)
            **kwargs: Additional options
        
        Returns:
            Context object ready for use
        """
        # Validate phase
        valid_phases = ["forethought", "performance", "self-reflection"]
        if current_phase not in valid_phases:
            current_phase = "forethought"  # Default

        # Format optional sections
        context_section = f"**CONTEXT**: {context}" if context else ""
        performance_section = f"**PERFORMANCE DATA**: {performance_data}" if performance_data else ""

        # Get phase-specific directive
        phase_specific_directive = self._get_phase_directive(current_phase)

        # Clean kwargs
        kwargs.pop('context_section', None)
        kwargs.pop('performance_section', None)
        kwargs.pop('phase_specific_directive', None)

        return super().build_context(
            goal=goal,
            current_phase=current_phase.upper(),
            context_section=context_section,
            performance_section=performance_section,
            phase_specific_directive=phase_specific_directive,
            **kwargs
        )

    def execute(
        self,
        provider="gemini",
        goal="",
        current_phase="forethought",
        context="",
        performance_data="",
        **kwargs
    ):
        """
        Execute self-regulation framework.
        
        Args:
            provider: LLM provider
            goal: The learning or performance goal
            current_phase: "forethought" | "performance" | "self-reflection"
            context: Optional situational context
            performance_data: Performance results (for reflection phase)
            **kwargs: Additional provider options
        
        Returns:
            ProviderResponse with phase-specific guidance
        """
        # Validate phase
        valid_phases = ["forethought", "performance", "self-reflection"]
        if current_phase not in valid_phases:
            current_phase = "forethought"

        # Format optional sections
        context_section = f"**CONTEXT**: {context}" if context else ""
        performance_section = f"**PERFORMANCE DATA**: {performance_data}" if performance_data else ""

        # Get phase-specific directive
        phase_specific_directive = self._get_phase_directive(current_phase)

        # Clean kwargs
        kwargs.pop('context_section', None)
        kwargs.pop('performance_section', None)
        kwargs.pop('phase_specific_directive', None)

        return super().execute(
            provider=provider,
            goal=goal,
            current_phase=current_phase.upper(),
            context_section=context_section,
            performance_section=performance_section,
            phase_specific_directive=phase_specific_directive,
            **kwargs
        )


__all__ = ["SelfRegulationFramework"]
