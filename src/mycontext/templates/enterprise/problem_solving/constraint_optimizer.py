"""
Constraint Optimizer (Enterprise) - Optimize within constraints

Find optimal solutions within given constraints and limitations.
Based on constrained optimization theory and operations research.

License: Enterprise
"""

from typing import Optional, List
from mycontext import Pattern, Guidance, Directive, Constraints


class ConstraintOptimizer(Pattern):
    """
    Optimize within constraints.
    
    Handles:
    - Budget constraints
    - Time constraints  
    - Resource constraints
    - Policy constraints
    - Trade-offs
    
    Based on: Constrained optimization and operations research
    
    Example:
        >>> optimizer = ConstraintOptimizer()
        >>> context = optimizer.build_context(
        ...     objective="Maximize feature delivery",
        ...     constraints=["Budget: $50K", "Time: 3 months"]
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert in constrained optimization and operations research. "
        "Find the best solution within the given constraints.\n\n"
        "Objective: {objective}\n"
        "Constraints: {constraints}\n"
        "{context_section}\n\n"
        "Deliver your analysis:\n"
        "(1) Define the objective precisely — what to maximize or minimize, and how to measure success.\n"
        "(2) Classify each constraint (hard vs. soft) and assess its impact on the solution space.\n"
        "(3) Identify binding constraints — which ones actually limit the optimal solution.\n"
        "(4) Perform sensitivity analysis — how does relaxing each constraint improve the outcome?\n"
        "(5) Generate feasible solutions that satisfy all constraints.\n"
        "(6) Recommend the optimal solution with expected outcomes and creative alternatives.\n\n"
        "Be creative within boundaries. Suggest constraint relaxation where high-value.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="constraint_optimizer",
            description="Optimize within constraints",
            version="1.0.0",
            tags=["problem_solving", "enterprise", "optimization", "constraints"],
            metadata={"category": "problem_solving", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Expert Operations Research and Optimization Specialist",
                rules=[
                    "Respect all constraints",
                    "Find creative solutions",
                    "Identify binding constraints",
                    "Maximize objective within limits",
                    "Suggest constraint relaxation if needed"
                ],
                style="analytical, creative, pragmatic"
            ),
            directive_template="""Optimize within constraints:

**OBJECTIVE**: {objective}

**CONSTRAINTS**:
{constraints_section}

{context_section}

Constrained optimization:

1. **OBJECTIVE DEFINITION**
   - Goal: [What to maximize/minimize]
   - Success metric: [How to measure]

2. **CONSTRAINT ANALYSIS**
   List all constraints:
   - Constraint 1: [Limit]
     - Type: [Hard/Soft]
     - Impact: [How it limits]
   - Constraint 2: [Limit]

3. **BINDING CONSTRAINTS**
   Which constraints actually limit us:
   - [Most restrictive constraint]

4. **OPTIMIZATION STRATEGY**
   Best approach given constraints:
   - Strategy: [Approach]
   - Expected outcome: [Result]

5. **RECOMMENDED SOLUTION**
   Optimal solution within all constraints

**OUTPUT FORMAT**: Optimal solution respecting all constraints.""",
            input_schema={
                "objective": str,
                "constraints_section": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=["binding_constraints", "optimal_solution"],
                style_guide="Be creative within boundaries"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def _render_constraints_section(self, constraints: Optional[List[str]]) -> str:
        if constraints:
            return "\n".join(f"- {c}" for c in constraints)
        return "- [Define constraints]"
    
    def build_context(
        self,
        objective: str = "",
        constraints: Optional[List[str]] = None,
        context: Optional[str] = None,
        **kwargs
    ):
        constraints_section = self._render_constraints_section(constraints)
        context_section = self._render_context_section(context)
        
        return super().build_context(
            objective=objective,
            constraints_section=constraints_section,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        objective: str = "",
        constraints: Optional[List[str]] = None,
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            objective=objective,
            constraints=constraints,
            context=context,
            **kwargs
        )
