"""
Efficiency Analyzer (Enterprise) - Analyze and improve efficiency

Systematic efficiency analysis and optimization.
Based on process optimization and lean principles.

License: Enterprise
"""

from typing import Optional
from mycontext import Pattern, Guidance, Directive, Constraints


class EfficiencyAnalyzer(Pattern):
    """
    Analyze and improve efficiency.
    
    Analyzes:
    - Process efficiency
    - Resource utilization
    - Waste identification
    - Optimization opportunities
    
    Based on: Lean principles and process optimization
    
    Example:
        >>> analyzer = EfficiencyAnalyzer()
        >>> context = analyzer.build_context(
        ...     process="Customer onboarding workflow",
        ...     goal="Reduce time by 50%"
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert process optimization specialist grounded in lean principles. "
        "Analyze the efficiency of the given process and identify improvement opportunities.\n\n"
        "Process: {process}\n"
        "Goal: {goal}\n"
        "{context_section}\n\n"
        "Deliver your analysis:\n"
        "(1) Map current state — total time, steps, resources, and baseline efficiency.\n"
        "(2) Identify waste using the 7 Wastes of Lean (transport, inventory, motion, waiting, "
        "overproduction, over-processing, defects).\n"
        "(3) Create a value stream map — value-add time vs. wait time for each step.\n"
        "(4) Pinpoint bottlenecks and their root causes.\n"
        "(5) Prioritize optimization opportunities: quick wins (easy, high impact) and major improvements.\n"
        "(6) Project quantified improvements — time savings, cost savings, and target efficiency.\n\n"
        "Be pragmatic and results-focused. Quantify every improvement.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="efficiency_analyzer",
            description="Efficiency analysis and optimization",
            version="1.0.0",
            tags=["problem_solving", "enterprise", "efficiency", "lean"],
            metadata={"category": "problem_solving", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Expert Process Optimization and Lean Specialist",
                rules=[
                    "Measure current state",
                    "Identify waste",
                    "Find quick wins",
                    "Optimize bottlenecks",
                    "Quantify improvements"
                ],
                style="analytical, pragmatic, results-focused"
            ),
            directive_template="""Analyze efficiency of:

**PROCESS**: {process}

**OPTIMIZATION GOAL**: {goal}

{context_section}

Efficiency analysis:

1. **CURRENT STATE**
   - Total time: [Duration]
   - Steps: [Number]
   - Resources: [What's used]
   - Output: [Results]
   - Efficiency: [Current %]

2. **WASTE IDENTIFICATION** (7 Wastes of Lean)
   - Transport: [Unnecessary movement]
   - Inventory: [Excess stock]
   - Motion: [Wasted motion]
   - Waiting: [Idle time]
   - Overproduction: [Making too much]
   - Over-processing: [Unnecessary steps]
   - Defects: [Errors/rework]

3. **VALUE STREAM MAP**
   | Step | Value-Add Time | Wait Time | Waste? |
   |------|----------------|-----------|--------|
   | Step 1 | [Min] | [Min] | [Y/N] |
   | Step 2 | [Min] | [Min] | [Y/N] |

4. **BOTTLENECK ANALYSIS**
   - Primary bottleneck: [Where]
   - Impact: [How much slowdown]
   - Cause: [Why it's slow]

5. **OPTIMIZATION OPPORTUNITIES**
   **Quick Wins** (Easy, high impact):
   - [Opportunity 1]: [Expected gain]
   - [Opportunity 2]: [Expected gain]
   
   **Major Improvements**:
   - [Opportunity A]: [Significant gain]

6. **RECOMMENDED CHANGES**
   - Eliminate: [Remove these steps]
   - Automate: [Automate these]
   - Simplify: [Simplify these]
   - Parallelize: [Run concurrently]

7. **PROJECTED IMPROVEMENTS**
   - Current efficiency: [%]
   - Target efficiency: [%]
   - Time savings: [Amount]
   - Cost savings: [$]

**OUTPUT FORMAT**: Data-driven efficiency analysis with ROI projections.""",
            input_schema={
                "process": str,
                "goal": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=["waste_identification", "opportunities", "projections"],
                style_guide="Be quantitative and actionable"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        process: str = "",
        goal: str = "Maximize efficiency",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            process=process,
            goal=goal,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        process: str = "",
        goal: str = "Maximize efficiency",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            process=process,
            goal=goal,
            context=context,
            **kwargs
        )
