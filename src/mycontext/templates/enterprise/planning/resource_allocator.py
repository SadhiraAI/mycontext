"""
Resource Allocator - Optimal resource allocation strategy

Systematic resource allocation using optimization frameworks.
Based on resource management and allocation optimization.
"""


from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class ResourceAllocator(Pattern):
    """
    Allocate resources optimally across competing needs.
    
    Optimizes:
    - Budget allocation
    - Time allocation
    - People allocation
    - Asset distribution
    
    Based on: Resource allocation optimization theory
    
    Example:
        >>> allocator = ResourceAllocator()
        >>> context = allocator.build_context(
        ...     resources={"budget": 100000, "people": 5},
        ...     needs=["Feature A", "Feature B", "Feature C"]
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert resource management and optimization specialist. "
        "Design an optimal allocation strategy for the following resources and "
        "competing needs.\n\n"
        "Available resources: {resources}\n"
        "Competing needs: {needs}\n"
        "Optimization goal: {goal}\n"
        "{context_section}\n\n"
        "Apply resource allocation optimization methodology:\n"
        "(1) Inventory resources — catalog all available budget, people, time, "
        "and assets with precise quantities and constraints. "
        "(2) Analyze each need — estimate resource requirements, expected ROI, "
        "priority level, and urgency timeline. "
        "(3) Model allocation scenarios — create at least two strategies "
        "(balanced vs. concentrated) and compare projected outcomes. "
        "(4) Optimize for ROI — allocate resources to maximize total return "
        "while respecting constraints and dependencies. "
        "(5) Balance time horizons — ensure the plan invests in both immediate "
        "deliverables and long-term strategic initiatives. "
        "(6) Produce a detailed allocation table with rationale, expected "
        "outcomes, and clear measurement criteria for each allocation.\n\n"
        "Be analytical and evidence-based. Justify every allocation.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="resource_allocator",
            description="Optimal resource allocation",
            guidance=Guidance(
                role="Expert Resource Management and Optimization Specialist",
                rules=[
                    "Maximize ROI and impact",
                    "Consider constraints",
                    "Balance short and long-term",
                    "Account for dependencies",
                    "Enable measurement"
                ],
                style="analytical, strategic, pragmatic"
            ),
            directive_template="""Allocate resources optimally:

**AVAILABLE RESOURCES**:
{resources_section}

**COMPETING NEEDS**:
{needs_section}

{context_section}

**OPTIMIZATION GOAL**: {goal}

Resource allocation optimization:

1. **RESOURCE INVENTORY**
   What we have:
   - Budget: [Amount]
   - People: [Headcount/hours]
   - Time: [Timeline]
   - Assets: [Equipment/tools]

2. **NEEDS ANALYSIS**
   For each need:
   - Need: [Name]
   - Resource requirements: [What it needs]
   - Expected ROI: [Return]
   - Priority: [High/Med/Low]
   - Urgency: [Timeline]

3. **ALLOCATION STRATEGY**
   | Need | Budget | People | Time | Rationale |
   |------|--------|--------|------|-----------|
   | [A] | [$] | [FTE] | [Weeks] | [Why] |

4. **RECOMMENDED ALLOCATION**
   Detailed plan with justification

5. **EXPECTED OUTCOMES**
   ROI and impact projections

**OUTPUT FORMAT**: Data-driven allocation plan.""",
            input_schema={
                "resources_section": str,
                "needs_section": str,
                "context_section": str,
                "goal": str
            },
            constraints=Constraints(
                must_include=["allocation_table", "roi_analysis"],
                style_guide="Be objective and data-driven"
            )
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def _render_resources_section(self, resources) -> str:
        if not resources:
            return "- [Define resources]"
        if isinstance(resources, str):
            return resources
        if isinstance(resources, dict):
            return "\n".join(f"- {k}: {v}" for k, v in resources.items())
        return str(resources)

    def _render_needs_section(self, needs) -> str:
        if not needs:
            return "1. [Define needs]"
        if isinstance(needs, str):
            parts = [t.strip() for t in needs.replace("\n", ",").split(",") if t.strip()]
            return "\n".join(f"{i+1}. {need}" for i, need in enumerate(parts))
        return "\n".join(f"{i+1}. {need}" for i, need in enumerate(needs))

    def build_context(
        self,
        resources: dict | None = None,
        needs: list[str] | None = None,
        goal: str = "Maximize ROI",
        context: str | None = None,
        **kwargs
    ):
        resources_section = self._render_resources_section(resources)
        needs_section = self._render_needs_section(needs)
        context_section = self._render_context_section(context)

        return super().build_context(
            resources_section=resources_section,
            needs_section=needs_section,
            goal=goal,
            context_section=context_section,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        resources: dict | None = None,
        needs: list[str] | None = None,
        goal: str = "Maximize ROI",
        context: str | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            resources=resources,
            needs=needs,
            goal=goal,
            context=context,
            **kwargs
        )
