"""
Multi-Objective Optimizer (Enterprise) - Balance multiple competing objectives

Optimizes for multiple objectives simultaneously using Pareto principles.
Based on multi-criteria decision analysis and Pareto optimization.

License: Enterprise
"""

from typing import Optional, List
from mycontext import Pattern, Guidance, Directive, Constraints


class MultiObjectiveOptimizer(Pattern):
    """
    Optimize for multiple objectives.
    
    Balances:
    - Competing goals
    - Trade-offs
    - Pareto frontiers
    - Weighted objectives
    
    Based on: Multi-criteria decision analysis
    
    Example:
        >>> optimizer = MultiObjectiveOptimizer()
        >>> context = optimizer.build_context(
        ...     objectives=["Minimize cost", "Maximize quality", "Minimize time"],
        ...     context="Product development"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert in multi-objective optimization and decision science. "
        "Analyze the competing objectives and find optimal balance points.\n\n"
        "Objectives: {objectives}\n"
        "{context_section}\n\n"
        "Deliver your analysis:\n"
        "(1) Define each objective — type (maximize/minimize), priority, relative weight.\n"
        "(2) Identify conflicts and trade-offs between objectives.\n"
        "(3) Generate multiple solution alternatives optimizing different objective combinations.\n"
        "(4) Determine Pareto frontier — solutions where no objective improves without worsening another.\n"
        "(5) Quantify trade-off rates between competing objectives.\n"
        "(6) Recommend the best balanced solution with clear rationale.\n\n"
        "Be analytical about compromises. Present multiple viable solutions with explicit trade-offs.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="multi_objective_optimizer",
            description="Multi-objective optimization",
            version="1.0.0",
            tags=["decision", "enterprise", "optimization", "pareto"],
            metadata={"category": "decision", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Expert Optimization and Decision Science Specialist",
                rules=[
                    "Identify all objectives clearly",
                    "Find Pareto optimal solutions",
                    "Consider trade-offs explicitly",
                    "Weight objectives appropriately",
                    "Provide multiple solutions"
                ],
                style="analytical, balanced, comprehensive"
            ),
            directive_template="""Optimize multiple objectives:

**OBJECTIVES**:
{objectives_section}

{context_section}

Multi-objective optimization:

1. **OBJECTIVES DEFINITION**
   | Objective | Type | Priority | Weight |
   |-----------|------|----------|--------|
   | [Obj 1] | [Max/Min] | [H/M/L] | [0-1] |
   | [Obj 2] | [Max/Min] | [H/M/L] | [0-1] |

2. **CONFLICTS & TRADE-OFFS**
   - [Obj A] vs [Obj B]: [How they conflict]
   - Can't optimize both: [Explanation]

3. **SOLUTION ALTERNATIVES**
   **Solution 1** (Balanced):
   - Obj 1: [Score]
   - Obj 2: [Score]
   - Obj 3: [Score]
   - Trade-offs: [What's sacrificed]
   
   **Solution 2** (Obj 1 optimized):
   - [Scores and trade-offs]
   
   **Solution 3** (Obj 2 optimized):
   - [Scores and trade-offs]

4. **PARETO FRONTIER**
   - Pareto optimal solutions: [Which can't be improved without worsening another]

5. **RECOMMENDED SOLUTION**
   - Choice: [Which solution]
   - Rationale: [Why this balance]
   - Expected outcomes: [Results]

**OUTPUT FORMAT**: Multiple solutions with clear trade-offs.""",
            input_schema={
                "objectives_section": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=["trade_offs", "alternatives", "recommendation"],
                style_guide="Be objective about compromises"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def _render_objectives_section(self, objectives: Optional[List[str]]) -> str:
        if objectives:
            return "\n".join(f"{i+1}. {obj}" for i, obj in enumerate(objectives))
        return "1. [Define objectives]"
    
    def build_context(
        self,
        objectives: Optional[List[str]] = None,
        context: Optional[str] = None,
        **kwargs
    ):
        objectives_section = self._render_objectives_section(objectives)
        context_section = self._render_context_section(context)
        
        return super().build_context(
            objectives_section=objectives_section,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        objectives: Optional[List[str]] = None,
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            objectives=objectives,
            context=context,
            **kwargs
        )
