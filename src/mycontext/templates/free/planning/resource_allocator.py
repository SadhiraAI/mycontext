"""
Resource Allocator - Optimal resource allocation strategy

Systematic resource allocation using optimization frameworks.
Based on resource management and allocation optimization.
"""

from typing import Optional, List
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


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
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def _render_resources_section(self, resources: Optional[dict]) -> str:
        if resources:
            return "\n".join(f"- {k}: {v}" for k, v in resources.items())
        return "- [Define resources]"
    
    def _render_needs_section(self, needs: Optional[List[str]]) -> str:
        if needs:
            return "\n".join(f"{i+1}. {need}" for i, need in enumerate(needs))
        return "1. [Define needs]"
    
    def build_context(
        self,
        resources: Optional[dict] = None,
        needs: Optional[List[str]] = None,
        goal: str = "Maximize ROI",
        context: Optional[str] = None,
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
        resources: Optional[dict] = None,
        needs: Optional[List[str]] = None,
        goal: str = "Maximize ROI",
        context: Optional[str] = None,
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
