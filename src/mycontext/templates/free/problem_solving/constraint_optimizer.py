"""
Constraint Optimizer - Optimize within constraints

Find optimal solutions within given constraints and limitations.
Based on constrained optimization theory and operations research.
"""

from typing import Optional, List
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints as ConstraintsClass


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
    
    Free Template - Part of mycontext open source edition.
    """
    
    def __init__(self):
        super().__init__(
            name="constraint_optimizer",
            description="Optimize within constraints",
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
            constraints=ConstraintsClass(
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
