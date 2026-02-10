"""
Deadline Manager - Time management and deadline optimization

Systematic deadline management and schedule optimization.
Based on time management and project scheduling principles.
"""

from typing import Optional, List
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


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
                    "Communicate proactively"
                ],
                style="pragmatic, organized, proactive"
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
            input_schema={
                "tasks_section": str,
                "deadline": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=["feasibility", "critical_path", "schedule"],
                style_guide="Be realistic, not optimistic"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def _render_tasks_section(self, tasks: Optional[List[str]]) -> str:
        if tasks:
            return "\n".join(f"{i+1}. {task}" for i, task in enumerate(tasks))
        return "1. [Define tasks]"
    
    def build_context(
        self,
        tasks: Optional[List[str]] = None,
        deadline: str = "",
        context: Optional[str] = None,
        **kwargs
    ):
        tasks_section = self._render_tasks_section(tasks)
        context_section = self._render_context_section(context)
        
        return super().build_context(
            tasks_section=tasks_section,
            deadline=deadline,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        tasks: Optional[List[str]] = None,
        deadline: str = "",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            tasks=tasks,
            deadline=deadline,
            context=context,
            **kwargs
        )
