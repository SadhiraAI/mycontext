"""
Priority Setter - Systematic prioritization framework

Helps prioritize tasks, features, or initiatives using multiple frameworks.
Based on prioritization methodologies (Eisenhower, RICE, MoSCoW, etc.)
"""


from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class PrioritySetter(Pattern):
    """
    Systematic prioritization across multiple frameworks.
    
    Methods:
    - Eisenhower Matrix (Urgent/Important)
    - RICE Score (Reach, Impact, Confidence, Effort)
    - MoSCoW (Must, Should, Could, Won't)
    - Value vs Effort
    
    Based on: Prioritization frameworks and decision theory
    
    Example:
        >>> setter = PrioritySetter()
        >>> context = setter.build_context(
        ...     items=["Feature A", "Bug fix B", "Tech debt C"],
        ...     context="Product roadmap planning"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert priority and resource management specialist. "
        "Systematically prioritize the following items using proven frameworks.\n\n"
        "Items to prioritize: {items}\n"
        "Goal: {goal}\n"
        "{context_section}\n\n"
        "Apply multi-framework prioritization methodology:\n"
        "(1) Eisenhower Matrix — categorize each item by urgency and importance "
        "into four quadrants: Do First, Schedule, Delegate, and Eliminate. "
        "(2) RICE scoring — for each item, estimate Reach (how many affected), "
        "Impact (magnitude 0.25-3), Confidence (percentage), and Effort "
        "(person-time), then rank by (R x I x C) / E. "
        "(3) Value vs. Effort analysis — plot items on a 2x2 grid to identify "
        "quick wins, major projects, fill-ins, and time sinks. "
        "(4) Dependency mapping — identify blocking relationships and the "
        "critical path that constrains execution order. "
        "(5) Synthesize a final priority ranking (P1-P4) with clear rationale "
        "drawn from all frameworks, including key trade-off decisions. "
        "(6) Produce a concrete execution plan: what to tackle this week, this "
        "month, and this quarter.\n\n"
        "Be objective and data-driven, not arbitrary.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="priority_setter",
            description="Systematic prioritization",
            guidance=Guidance(
                role="Expert Priority and Resource Management Specialist",
                rules=[
                    "Use multiple prioritization frameworks",
                    "Be objective about effort and impact",
                    "Consider dependencies",
                    "Balance quick wins with long-term value",
                    "Provide clear rationale for priorities"
                ],
                style="systematic, objective, pragmatic"
            ),
            directive_template="""Prioritize these items:

**ITEMS TO PRIORITIZE**:
{items_section}

{context_section}

**GOAL**: {goal}

Comprehensive prioritization:

1. **ITEMS OVERVIEW**
   List all items with basic info:
   
   | # | Item | Description | Initial gut feeling |
   |---|------|-------------|---------------------|
   | 1 | [Item] | [What it is] | [High/Med/Low] |
   | 2 | [Item] | [What it is] | [High/Med/Low] |

2. **EISENHOWER MATRIX**
   Categorize by Urgent/Important:
   
   **Quadrant 1: URGENT + IMPORTANT** (Do First):
   - [Item X]: [Why urgent AND important]
   - [Item Y]: [Crisis or deadline]
   
   **Quadrant 2: NOT URGENT + IMPORTANT** (Schedule):
   - [Item A]: [Strategic value]
   - [Item B]: [Long-term benefit]
   
   **Quadrant 3: URGENT + NOT IMPORTANT** (Delegate/Minimize):
   - [Item M]: [Urgent but low value]
   
   **Quadrant 4: NOT URGENT + NOT IMPORTANT** (Eliminate):
   - [Item Z]: [Can skip]

3. **RICE SCORING**
   Calculate RICE scores:
   
   **Item 1**: [Name]
   - Reach: [How many affected] → Score: X
   - Impact: [How much impact] (0.25-3) → Score: Y
   - Confidence: [How sure] (%) → Score: Z
   - Effort: [Person-months] → Score: E
   - **RICE Score**: (R × I × C) / E = [Number]
   
   [Repeat for each item]
   
   **Ranked by RICE**:
   1. [Item] - RICE: [Score]
   2. [Item] - RICE: [Score]
   3. [Item] - RICE: [Score]

4. **MOSCOW PRIORITIZATION**
   
   **Must Have** (Critical, can't launch without):
   - [Item]: [Why essential]
   - [Item]: [Non-negotiable]
   
   **Should Have** (Important but not critical):
   - [Item]: [High value]
   - [Item]: [Strong impact]
   
   **Could Have** (Nice to have):
   - [Item]: [Beneficial but optional]
   
   **Won't Have** (Not now):
   - [Item]: [Deferred or rejected]

5. **VALUE VS EFFORT MATRIX**
   Plot items on 2x2 grid:
   
   **Quick Wins** (High Value, Low Effort):
   - [Item]: Do these first!
   
   **Major Projects** (High Value, High Effort):
   - [Item]: Plan carefully
   
   **Fill-ins** (Low Value, Low Effort):
   - [Item]: Do if time permits
   
   **Time Sinks** (Low Value, High Effort):
   - [Item]: Avoid or eliminate

6. **DEPENDENCY ANALYSIS**
   What must happen in what order?
   
   - [Item A] blocks [Item B, C]
   - [Item D] requires [Item E]
   - [Item F] is independent
   
   **Critical Path**: [Sequence of must-dos]

7. **RISK ASSESSMENT**
   Prioritize by risk level:
   
   - High Risk, High Impact: [Item] - Do early
   - High Risk, Low Impact: [Item] - Mitigate
   - Low Risk items: [Can defer]

8. **STAKEHOLDER IMPACT**
   Who cares most about what?
   
   - CEO cares about: [Items]
   - Customers want: [Items]
   - Team needs: [Items]
   - Compliance requires: [Items]

9. **FINAL PRIORITY RANKING**
   Synthesized from all frameworks:
   
   **Priority 1 (P1) - Do Now**:
   1. [Item]: [Rationale]
   2. [Item]: [Why first]
   3. [Item]: [Critical reason]
   
   **Priority 2 (P2) - Do Next**:
   1. [Item]: [Why second tier]
   2. [Item]: [Importance]
   
   **Priority 3 (P3) - Do Later**:
   1. [Item]: [Can wait]
   2. [Item]: [Future consideration]
   
   **Priority 4 (P4) - Don't Do**:
   1. [Item]: [Why excluded]

10. **EXECUTION PLAN**
    **This Week**:
    - [ ] [P1 Item 1]
    - [ ] [P1 Item 2]
    
    **This Month**:
    - [ ] [P1 remaining]
    - [ ] [P2 start]
    
    **This Quarter**:
    - [ ] [P2 complete]
    - [ ] [P3 begin]

11. **TRADE-OFFS & DECISIONS**
    Key decisions made:
    - Chose [X] over [Y] because: [Reason]
    - Deferred [Z] because: [Rationale]
    - Cut [W] to focus on: [Priority]

**OUTPUT FORMAT**: Clear priority ranking with multi-framework justification.""",
            input_schema={
                "items_section": str,
                "context_section": str,
                "goal": str
            },
            constraints=Constraints(
                must_include=[
                    "multiple_frameworks",
                    "final_ranking",
                    "execution_plan"
                ],
                style_guide="Be systematic and objective, not arbitrary"
            )
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def _render_items_section(self, items) -> str:
        if not items:
            return "1. [Items to prioritize]"
        if isinstance(items, str):
            parts = [t.strip() for t in items.replace("\n", ",").split(",") if t.strip()]
            return "\n".join(f"{i+1}. {item}" for i, item in enumerate(parts))
        return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))

    def build_context(
        self,
        items: list[str] | None = None,
        goal: str = "Optimize resource allocation",
        context: str | None = None,
        **kwargs
    ):
        items_section = self._render_items_section(items)
        context_section = self._render_context_section(context)

        return super().build_context(
            items_section=items_section,
            goal=goal,
            context_section=context_section,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        items: list[str] | None = None,
        goal: str = "Optimize resource allocation",
        context: str | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            items=items,
            goal=goal,
            context=context,
            **kwargs
        )
