"""
Trade Space Explorer (Enterprise) - Explore solution space and alternatives

Systematic exploration of solution space and design alternatives.
Based on systems engineering and design space exploration.

License: Enterprise
"""

from typing import Optional
from mycontext import Pattern, Guidance, Directive, Constraints


class TradeSpaceExplorer(Pattern):
    """
    Explore trade space systematically.
    
    Investigates:
    - Solution alternatives
    - Design space
    - Parameter trade-offs
    - Feasible regions
    
    Based on: Systems engineering and design optimization
    
    Example:
        >>> explorer = TradeSpaceExplorer()
        >>> context = explorer.build_context(
        ...     problem="Design optimal database architecture",
        ...     parameters=["Performance", "Cost", "Scalability"]
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert systems engineer specializing in design space exploration. "
        "Systematically explore the solution trade space for the given problem.\n\n"
        "Problem: {problem}\n"
        "Key Parameters: {parameters}\n"
        "{context_section}\n\n"
        "Deliver your analysis:\n"
        "(1) Define the design space — parameters, their ranges, and meaningful combinations.\n"
        "(2) Analyze corner solutions — what happens at each extreme of the parameter space.\n"
        "(3) Map the feasible region — valid combinations, constraints, and infeasible zones.\n"
        "(4) Identify interesting regions with unique characteristics and trade-off balances.\n"
        "(5) Evaluate solution candidates across all parameters with composite scores.\n"
        "(6) Pinpoint sweet spots — optimal balances where multiple objectives align.\n"
        "(7) Summarize key trade-offs, dominant solutions, and surprising findings.\n\n"
        "Be exploratory and thorough. Document trade-offs at every decision point.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="trade_space_explorer",
            description="Explore solution space",
            version="1.0.0",
            tags=["problem_solving", "enterprise", "design-space", "exploration"],
            metadata={"category": "problem_solving", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Expert Systems Engineer and Design Specialist",
                rules=[
                    "Map full solution space",
                    "Identify feasible regions",
                    "Explore extremes and middle ground",
                    "Find sweet spots",
                    "Document trade-offs"
                ],
                style="exploratory, systematic, comprehensive"
            ),
            directive_template="""Explore trade space for:

**PROBLEM**: {problem}

**KEY PARAMETERS**: {parameters}

{context_section}

Trade space exploration:

1. **DESIGN SPACE DEFINITION**
   Parameters and ranges:
   - Param 1: [Min-Max]
   - Param 2: [Min-Max]
   - Param 3: [Min-Max]

2. **CORNER SOLUTIONS** (Extremes)
   - Max Param 1: [What if we maximize this]
     - Pros: [Benefits]
     - Cons: [Costs]
   
   - Max Param 2: [Opposite extreme]
     - Pros/Cons

3. **FEASIBLE REGION**
   Valid combinations:
   - Constraints: [What limits us]
   - Feasible zone: [What's possible]
   - Infeasible zone: [What's not possible]

4. **INTERESTING REGIONS**
   Areas worth exploring:
   - Region A: [Description]
     - Characteristics: [What's special]
     - Trade-offs: [Balances]
   
   - Region B: [Another promising area]

5. **SOLUTION CANDIDATES**
   | Solution | Param 1 | Param 2 | Param 3 | Score |
   |----------|---------|---------|---------|-------|
   | A | [Val] | [Val] | [Val] | [Overall] |
   | B | [Val] | [Val] | [Val] | [Overall] |

6. **SWEET SPOTS**
   Optimal balances:
   - Sweet Spot 1: [Description]
     - Why optimal: [Rationale]
   
   - Sweet Spot 2: [Alternative]

7. **EXPLORATION INSIGHTS**
   What we learned:
   - Key trade-offs: [Main compromises]
   - Dominant solutions: [Best overall]
   - Surprising findings: [Unexpected results]

**OUTPUT FORMAT**: Comprehensive design space analysis.""",
            input_schema={
                "problem": str,
                "parameters": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=["extremes", "feasible_region", "sweet_spots"],
                style_guide="Be exploratory and thorough"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        problem: str = "",
        parameters: str = "",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            problem=problem,
            parameters=parameters,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        problem: str = "",
        parameters: str = "",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            problem=problem,
            parameters=parameters,
            context=context,
            **kwargs
        )
