"""
Deadline Manager - Time management and deadline optimization

Systematic deadline management and schedule optimization.
Based on time management and project scheduling principles.
"""

from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class DeadlineManager(Pattern):
    """
    Manage deadlines and schedules systematically.

    Optimizes:
    - Timeline feasibility
    - Resource allocation over time
    - Buffer management
    - Critical path scheduling
    - Deadline negotiation

    Based on: Project management and time optimization

    Example:
        >>> manager = DeadlineManager()
        >>> context = manager.build_context(
        ...     tasks=["Design", "Development", "Testing"],
        ...     deadline="3 months from now"
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert project manager and scheduling specialist. Create a "
        "realistic deadline management plan for the following work.\n\n"
        "Tasks: {tasks}\n"
        "Target deadline: {deadline}\n"
        "{context_section}\n\n"
        "Apply critical-path scheduling methodology:\n"
        "(1) Break down each task — estimate duration, effort hours, and priority "
        "for every item, being realistic rather than optimistic. "
        "(2) Map dependencies — identify which tasks must complete before others "
        "can start, and which can run in parallel. "
        "(3) Determine the critical path — find the longest sequential chain "
        "that defines the minimum project duration. "
        "(4) Assess feasibility — compare required time against available time, "
        "flag the gap, and rate as Feasible, Tight, or Unrealistic. "
        "(5) Build in risk buffers — add contingency time for high-risk tasks "
        "and an overall project buffer of 15-20%. "
        "(6) Produce a milestone schedule — week-by-week plan with clear "
        "checkpoints, and if the deadline is infeasible, propose scope or "
        "timeline negotiation options.\n\n"
        "Be pragmatic. Under-promise and over-deliver.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="deadline_manager",
            description="Deadline and time management",
            guidance=Guidance(
                role="Expert Project Manager and Scheduling Specialist",
                rules=[
                    "Be realistic about time estimates",
                    "Include buffer time",
                    "Identify critical path",
                    "Plan for risks",
                    "Communicate proactively",
                ],
                style="pragmatic, organized, proactive",
            ),
            directive_template="""Manage deadlines for:

**TASKS**: {tasks_section}

**TARGET DEADLINE**: {deadline}

{context_section}

Deadline management:

1. **TASK BREAKDOWN**
   | Task | Duration | Effort | Priority |
   |------|----------|--------|----------|
   | [Task 1] | [Days] | [Hours] | [P1] |
   | [Task 2] | [Days] | [Hours] | [P2] |

2. **DEPENDENCIES**
   - [Task A] must complete before [Task B]
   - [Task C] can run parallel with [Task D]

3. **CRITICAL PATH**
   Longest sequence:
   [Task 1] → [Task 2] → [Task 5]
   Total: [X days]

4. **TIMELINE FEASIBILITY**
   - Required time: [X days]
   - Available time: [Y days]
   - Buffer: [Z days]
   - Assessment: [Feasible/Tight/Unrealistic]

5. **SCHEDULE OPTIMIZATION**
   - Parallel tasks: [What can overlap]
   - Fast-tracking: [What to accelerate]
   - Scope reduction: [What to cut if needed]

6. **RISK BUFFER**
   - Contingency time: [X%]
   - High-risk tasks: [Extra buffer]

7. **RECOMMENDED SCHEDULE**
   Week-by-week plan with milestones

8. **DEADLINE NEGOTIATION** (if needed)
   - Current estimate: [Realistic time]
   - Requested deadline: [Target]
   - Gap: [Difference]
   - Options: [How to close gap]

**OUTPUT FORMAT**: Realistic schedule with risk management.""",
            input_schema={"tasks_section": str, "deadline": str, "context_section": str},
            constraints=Constraints(
                must_include=["feasibility", "critical_path", "schedule"],
                style_guide="Be realistic, not optimistic",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def _render_tasks_section(self, tasks) -> str:
        if not tasks:
            return "1. [Define tasks]"
        if isinstance(tasks, str):
            items = [t.strip() for t in tasks.replace("\n", ",").split(",") if t.strip()]
            return "\n".join(f"{i + 1}. {task}" for i, task in enumerate(items))
        return "\n".join(f"{i + 1}. {task}" for i, task in enumerate(tasks))

    def build_context(
        self,
        tasks: list[str] | None = None,
        deadline: str = "",
        context: str | None = None,
        **kwargs,
    ):
        tasks_section = self._render_tasks_section(tasks)
        context_section = self._render_context_section(context)

        return super().build_context(
            tasks_section=tasks_section,
            deadline=deadline,
            context_section=context_section,
            **kwargs,
        )

    def execute(
        self,
        provider: str = "openai",
        tasks: list[str] | None = None,
        deadline: str = "",
        context: str | None = None,
        **kwargs,
    ):
        return super().execute(
            provider=provider, tasks=tasks, deadline=deadline, context=context, **kwargs
        )
