"""
Problem Decomposition Pattern (Enterprise) - Break complex problems into manageable parts

Systematically decomposes problems using hierarchical breakdown.
Based on systems thinking and problem-solving research.

License: Enterprise
"""


from mycontext import Constraints, Guidance, Pattern


class ProblemDecomposer(Pattern):
    """
    Break down complex problems into manageable sub-problems.
    
    Uses systematic decomposition:
    - Hierarchical breakdown
    - Dependency identification
    - Prioritization
    - Solution strategy
    
    Based on: Systems thinking and problem decomposition research
    
    Example:
        >>> decomposer = ProblemDecomposer()
        >>> context = decomposer.build_context(
        ...     problem="Build a scalable e-commerce platform",
        ...     constraints=["Budget: $50K", "Timeline: 6 months"]
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert systems analyst specializing in problem decomposition. "
        "Break down the complex problem into manageable, actionable sub-problems.\n\n"
        "Problem: {problem}\n"
        "{context_section}\n"
        "Constraints: {constraints}\n"
        "Depth: {depth}\n\n"
        "Deliver your analysis:\n"
        "(1) Define the core problem, desired outcome, current state, and gap.\n"
        "(2) Decompose into major components with description, purpose, and complexity.\n"
        "(3) Build a hierarchical breakdown — sub-components with dependencies and effort estimates.\n"
        "(4) Map dependencies: critical path, parallel opportunities, and bottlenecks.\n"
        "(5) Prioritize sub-problems by impact, effort, and risk in a prioritization matrix.\n"
        "(6) Provide a phased solution roadmap with integration plan and success metrics.\n\n"
        "Be systematic and practical. Ensure completeness with no gaps.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="problem_decomposer",
            description="Decompose complex problems systematically",
            version="1.0.0",
            tags=["problem_solving", "enterprise", "decomposition", "systems"],
            metadata={"category": "problem_solving", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Expert Systems Analyst and Problem-Solving Specialist",
                rules=[
                    "Break problems into independent sub-problems when possible",
                    "Identify dependencies clearly",
                    "Prioritize based on impact and urgency",
                    "Ensure completeness - no gaps",
                    "Maintain traceability to original problem"
                ],
                style="systematic, structured, clear"
            ),
            directive_template="""Decompose this complex problem:

**PROBLEM**: {problem}

{context_section}

**CONSTRAINTS**:
{constraints_section}

**DECOMPOSITION DEPTH**: {depth}

Systematic problem decomposition:

1. **PROBLEM UNDERSTANDING**
   - Core problem: [State in one sentence]
   - Desired outcome: [What does success look like?]
   - Current state: [Where are we now?]
   - Gap: [What needs to change?]

2. **TOP-LEVEL DECOMPOSITION**
   Break into major components:
   
   Component A: [Name]
   - Description: [What is this part?]
   - Purpose: [Why is it needed?]
   - Scope: [What's included?]
   - Complexity: [High/Medium/Low]
   
   Component B: [Name]
   - [Same structure]
   
   [Continue for all major components]

3. **HIERARCHICAL BREAKDOWN**
   For each major component, break into sub-components:
   
   Component A
   ├── Sub-component A.1
   │   - Description
   │   - Dependencies
   │   - Effort estimate
   ├── Sub-component A.2
   │   - [Same structure]
   └── Sub-component A.3
   
   [Continue hierarchy as needed]

4. **DEPENDENCY ANALYSIS**
   Map relationships between components:
   
   Critical Path:
   - [Component X must be done before Y]
   - [Rationale]
   
   Parallel Opportunities:
   - [Components that can be done simultaneously]
   
   Bottlenecks:
   - [Components that block others]

5. **PRIORITIZATION MATRIX**
   Rank sub-problems by:
   
   | Component | Impact | Effort | Risk | Priority |
   |-----------|--------|--------|------|----------|
   | A.1       | High   | Med    | Low  | P1       |
   | A.2       | Med    | Low    | Med  | P2       |
   | ...       | ...    | ...    | ...  | ...      |
   
   Priority Levels:
   - P1 (Critical): [Must have, high impact]
   - P2 (Important): [Should have, good ROI]
   - P3 (Nice-to-have): [Could have, low priority]

6. **SOLUTION STRATEGY**
   For each high-priority component:
   
   Component [Name]:
   - Approach: [How to solve]
   - Resources needed: [What's required]
   - Timeline: [How long]
   - Success criteria: [How to measure]
   - Risks: [What could go wrong]
   - Mitigation: [How to address risks]

7. **INTEGRATION PLAN**
   How sub-solutions combine:
   - Integration points: [Where components connect]
   - Integration order: [Sequence of assembly]
   - Testing strategy: [How to verify integration]
   - Validation: [How to confirm completeness]

8. **SUMMARY ROADMAP**
   **Phase 1** (Foundation):
   - [Components to address first]
   - [Timeline estimate]
   
   **Phase 2** (Core):
   - [Next components]
   - [Timeline estimate]
   
   **Phase 3** (Enhancement):
   - [Final components]
   - [Timeline estimate]
   
   **Success Metrics**: [How to measure overall success]

**OUTPUT FORMAT**: Clear hierarchical structure with actionable breakdown.""",
            input_schema={
                "problem": str,
                "context_section": str,
                "constraints_section": str,
                "depth": str
            },
            constraints=Constraints(
                must_include=[
                    "hierarchical_breakdown",
                    "dependencies",
                    "prioritization",
                    "solution_strategy"
                ],
                style_guide="Be thorough but practical, detailed but actionable"
            )
        )

    def _render_context_section(self, context: str | None) -> str:
        """Render optional context section."""
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def _render_constraints_section(self, constraints: list[str] | None) -> str:
        """Render constraints section."""
        if constraints:
            return "\n".join(f"- {c}" for c in constraints)
        return "- None specified"

    def build_context(
        self,
        problem: str = "",
        context: str | None = None,
        constraints: list[str] | None = None,
        depth: str = "detailed",
        **kwargs
    ):
        """
        Build context for problem decomposition.
        
        Args:
            problem: The complex problem to decompose
            context: Optional additional context
            constraints: Optional list of constraints
            depth: Decomposition depth ("overview", "detailed", "comprehensive")
            **kwargs: Additional options
        
        Returns:
            Context object ready for export/use
        """
        context_section = self._render_context_section(context)
        constraints_section = self._render_constraints_section(constraints)

        return super().build_context(
            problem=problem,
            context_section=context_section,
            constraints_section=constraints_section,
            depth=depth,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        problem: str = "",
        context: str | None = None,
        constraints: list[str] | None = None,
        depth: str = "detailed",
        **kwargs
    ):
        """
        Execute problem decomposition.
        
        Args:
            provider: LLM provider to use
            problem: The complex problem to decompose
            context: Optional additional context
            constraints: Optional list of constraints
            depth: Decomposition depth
            **kwargs: Provider parameters
        
        Returns:
            ProviderResponse with the decomposition
        """
        return super().execute(
            provider=provider,
            problem=problem,
            context=context,
            constraints=constraints,
            depth=depth,
            **kwargs
        )
