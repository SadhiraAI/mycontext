"""
MetacognitiveMonitor Pattern (Enterprise)

Monitor thinking process and detect comprehension errors.
Enables "thinking about thinking" - critical for learning and self-improvement.

Research Foundation:
- Flavell, J. H. (1979). Metacognition and cognitive monitoring: A new area of
  cognitive–developmental inquiry. American Psychologist, 34(10), 906-911.
- Schraw, G., & Dennison, R. S. (1994). Assessing metacognitive awareness.
  Contemporary Educational Psychology, 19(4), 460-475.
- Dunlosky, J., & Metcalfe, J. (2009). Metacognition. Sage Publications.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class MetacognitiveMonitor(Pattern):
    """
    Monitor thinking process and detect comprehension errors.

    Enables systematic self-monitoring across 5 dimensions:
    1. Comprehension Check: Do I understand what I'm trying to achieve?
    2. Strategy Evaluation: Is my current approach working?
    3. Error Detection: Have I made mistakes or wrong assumptions?
    4. Progress Assessment: How much have I accomplished?
    5. Adjustment Planning: What should I do differently?

    Use Cases:
    - Learning new skills or concepts
    - Debugging complex problems
    - Self-directed study
    - Performance improvement
    - Tutoring systems

    Research Foundation:
    Flavell (1979) established that effective learners actively monitor their
    comprehension and adjust strategies. Schraw & Dennison (1994) identified
    key metacognitive processes that distinguish experts from novices.

    Example:
        >>> from mycontext.templates.enterprise.metacognition import MetacognitiveMonitor
        >>>
        >>> monitor = MetacognitiveMonitor()
        >>> result = monitor.execute(
        ...     provider="gemini",
        ...     task_description="Learn Python programming",
        ...     current_approach="Reading tutorials",
        ...     progress_so_far="Completed 3 chapters"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are a metacognitive coach and learning scientist. Monitor the thinking "
        "process and detect comprehension errors.\n\n"
        "Task: {task_description}\n"
        "Current Approach: {current_approach}\n"
        "Progress So Far: {progress_so_far}\n"
        "{context_section}\n\n"
        "Conduct systematic metacognitive analysis across 5 dimensions: "
        "(1) Comprehension Status — assess understanding level, identify unclear "
        "concepts, test self-explanation ability. (2) Strategy Assessment — evaluate "
        "whether the current approach is effective, stalled, or ineffective, with "
        "reasoning. (3) Error Detection — identify mistakes, knowledge gaps, and "
        "confusion points by type (conceptual, procedural, cognitive bias). "
        "(4) Progress Evaluation — estimate completion percentage, on-track status, "
        "and work quality. (5) Recommended Adjustments — specify the immediate next "
        "action, strategy changes, and resources needed.\n\n"
        "Be honest and specific. Provide concrete, actionable guidance.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="metacognitive_monitor",
            description="Monitor thinking process and detect comprehension errors",
            version="1.0.0",
            tags=["metacognition", "enterprise", "self-regulation", "learning"],
            metadata={"category": "metacognition", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Metacognitive Coach and Learning Scientist",
                rules=[
                    "Monitor thinking systematically across 5 dimensions (Comprehension, Strategy, Errors, Progress, Adjustments)",
                    "Be brutally honest about comprehension gaps and mistakes",
                    "Focus on metacognitive awareness (HOW you're thinking), not just task execution",
                    "Provide specific, actionable adjustments with clear reasoning",
                    "Use evidence-based metacognitive frameworks (Flavell 1979, Schraw & Dennison 1994)",
                ],
                style="analytical, honest, constructive, evidence-based, systematic",
            ),
            directive_template="""**METACOGNITIVE MONITORING ANALYSIS**

**TASK**: {task_description}

**CURRENT APPROACH**: {current_approach}

**PROGRESS SO FAR**: {progress_so_far}

{challenges_section}

Conduct a systematic metacognitive analysis across all 5 dimensions:

---

## 1. COMPREHENSION STATUS

**Guiding Questions**:
- Do I understand what I'm trying to achieve?
- Are there any terms or concepts I'm unclear about?
- Can I explain this task in my own words?
- Do I know what success looks like?

**Provide**:
- **Understanding Level**: [Clear / Partial / Confused]
- **Unclear Concepts**: [List specific concepts or terms]
- **Self-Explanation Test**: [Can/Cannot explain in own words - demonstrate]
- **Evidence**: [What demonstrates this level of understanding?]

---

## 2. STRATEGY ASSESSMENT

**Guiding Questions**:
- Is my current approach working?
- Am I making progress toward my goal?
- Is there a better strategy I should try?
- Am I using the right tools/resources?

**Provide**:
- **Effectiveness**: [Effective / Somewhat Effective / Ineffective]
- **Progress Rate**: [Good / Slow / Stalled]
- **Strategy Recommendation**: [Continue / Adjust / Change completely]
- **Reasoning**: [WHY is this strategy working or not working?]

---

## 3. ERRORS DETECTED

**Guiding Questions**:
- Have I made any mistakes or wrong assumptions?
- Are there gaps in my understanding?
- What am I confused or uncertain about?
- Have I checked my work for errors?

**Provide**:
- **Mistakes Identified**: [List specific mistakes with examples]
- **Knowledge Gaps**: [Missing prerequisite knowledge or skills]
- **Confusion Points**: [What is confusing or unclear?]
- **Error Types**: [Conceptual / Procedural / Knowledge gaps / Cognitive biases]
- **Severity**: [How serious are these errors? Critical/Moderate/Minor]

---

## 4. PROGRESS EVALUATION

**Guiding Questions**:
- How much have I accomplished?
- What remains to be done?
- Am I on track to complete this successfully?
- What milestones have I achieved?

**Provide**:
- **Completed**: [X% or specific milestones achieved]
- **Remaining**: [Y% or tasks/milestones remaining]
- **On Track**: [Yes / No / At risk]
- **Quality Check**: [Is the work so far high quality? Any concerns?]
- **Time Assessment**: [Time spent vs. expected time remaining]

---

## 5. RECOMMENDED ADJUSTMENTS

**Guiding Questions**:
- What should I do differently?
- What resources or help do I need?
- What's my next immediate step?
- How will I know if the adjustment works?

**Provide**:
- **Immediate Action**: [Specific next step to take RIGHT NOW]
- **Strategy Changes**: [What to do differently going forward]
- **Resources Needed**: [Help, tools, tutorials, or materials needed]
- **Success Criteria**: [How to know if these adjustments work]

**Action Types to Consider**:
- Strategy change (switch to different approach)
- Seek help (ask expert, find tutorial, consult documentation)
- Break down problem (simplify into smaller steps)
- Review fundamentals (go back to basics)
- Practice more (deliberate practice on weak areas)
- Change environment (reduce distractions, use better tools)

---

**CRITICAL**: Be honest and specific. Vague advice like "work harder" or "be more careful" is useless. Provide concrete, actionable guidance based on the evidence.""",
            input_schema={
                "task_description": str,
                "current_approach": str,
                "progress_so_far": str,
                "challenges_section": str,  # Will be auto-generated from challenges
            },
            constraints=Constraints(
                must_include=[
                    "comprehension_status",
                    "strategy_assessment",
                    "errors_detected",
                    "progress_evaluation",
                    "recommended_adjustments",
                ],
                must_not_include=["vague_advice", "generic_encouragement"],
                style_guide="Use structured format with clear sections, specific evidence, and actionable recommendations. Be brutally honest about gaps and mistakes.",
            ),
        )

    def _render_challenges_section(self, challenges):
        """Render optional challenges section."""
        if challenges:
            return f"\n**CHALLENGES ENCOUNTERED**: {challenges}\n"
        return ""

    def build_context(
        self, task_description="", current_approach="", progress_so_far="", challenges="", **kwargs
    ):
        """
        Build context for metacognitive monitoring (without executing).

        Args:
            task_description: The cognitive task being performed
            current_approach: Current thinking/strategy being used
            progress_so_far: What has been accomplished/understood
            challenges: Optional difficulties or confusions (will be formatted)
            **kwargs: Additional options

        Returns:
            Context object ready for export/use
        """
        # Format challenges section
        challenges_section = self._render_challenges_section(challenges)

        # Remove challenges from kwargs if present to avoid duplicate
        kwargs.pop("challenges", None)
        kwargs.pop("challenges_section", None)

        # Build context using parent's method with template variables
        return super().build_context(
            task_description=task_description,
            current_approach=current_approach,
            progress_so_far=progress_so_far,
            challenges_section=challenges_section,
            **kwargs,
        )

    def execute(
        self,
        provider="gemini",
        task_description="",
        current_approach="",
        progress_so_far="",
        challenges="",
        **kwargs,
    ):
        """
        Execute metacognitive monitoring.

        Args:
            provider: LLM provider to use ("gemini", "openai", "anthropic")
            task_description: The cognitive task being performed
            current_approach: Current thinking/strategy being used
            progress_so_far: What has been accomplished/understood
            challenges: Optional difficulties or confusions
            **kwargs: Additional provider options (temperature, max_tokens, etc.)

        Returns:
            ProviderResponse with the metacognitive analysis
        """
        # Format challenges section
        challenges_section = self._render_challenges_section(challenges)

        # Remove challenges from kwargs if present to avoid duplicate
        kwargs.pop("challenges", None)
        kwargs.pop("challenges_section", None)

        # Execute using parent's method
        return super().execute(
            provider=provider,
            task_description=task_description,
            current_approach=current_approach,
            progress_so_far=progress_so_far,
            challenges_section=challenges_section,
            **kwargs,
        )


# Export
__all__ = ["MetacognitiveMonitor"]
