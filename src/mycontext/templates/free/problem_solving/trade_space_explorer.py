"""
Trade Space Explorer - Explore solution space and alternatives

Systematic exploration of solution space and design alternatives.
Based on systems engineering and design space exploration.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


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
    
    Free Template - Part of mycontext open source edition.
    """
    
    def __init__(self):
        super().__init__(
            name="trade_space_explorer",
            description="Explore solution space",
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
