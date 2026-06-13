"""
Dependency Mapper (Enterprise) - Map dependencies and relationships

Systematic identification and visualization of dependencies.
Based on dependency analysis and systems thinking.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class DependencyMapper(Pattern):
    """
    Map dependencies systematically.

    Identifies:
    - Direct dependencies
    - Indirect dependencies
    - Circular dependencies
    - Critical path
    - Dependency risks

    Based on: Dependency analysis and network theory

    Example:
        >>> mapper = DependencyMapper()
        >>> context = mapper.build_context(
        ...     system="Product development roadmap",
        ...     context="Q1-Q2 planning"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert systems analyst specializing in dependency analysis and network theory. "
        "Map all dependencies within the given system.\n\n"
        "System: {system}\n"
        "{context_section}\n\n"
        "Deliver your analysis:\n"
        "(1) Inventory all components and their descriptions.\n"
        "(2) Map direct dependencies — what depends on what, and what blocks what.\n"
        "(3) Identify indirect and transitive dependencies across the system.\n"
        "(4) Classify dependency types: hard (must-have), soft (nice-to-have), and circular.\n"
        "(5) Determine the critical path — the longest dependency chain limiting delivery.\n"
        "(6) Assess dependency risks: single points of failure, tight coupling, and fragile chains.\n"
        "(7) Recommend optimization: parallelization, decoupling, and reordering opportunities.\n\n"
        "Be thorough and visual. Present clear dependency tables and actionable improvements.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="dependency_mapper",
            description="Map dependencies and relationships",
            version="1.0.0",
            tags=["problem_solving", "enterprise", "dependencies", "mapping"],
            metadata={"category": "problem_solving", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Expert Systems Analyst and Dependency Mapping Specialist",
                rules=[
                    "Identify all dependencies",
                    "Map relationships clearly",
                    "Find critical path",
                    "Highlight risks",
                    "Suggest optimization",
                ],
                style="systematic, visual, clear",
            ),
            directive_template="""Map dependencies in:

**SYSTEM**: {system}

{context_section}

Dependency mapping:

1. **COMPONENTS INVENTORY**
   List all components/tasks:
   - Component A: [Description]
   - Component B: [Description]
   - Component C: [Description]

2. **DEPENDENCY ANALYSIS**
   | Component | Depends On | Blocks |
   |-----------|------------|--------|
   | A | - | B, C |
   | B | A | D |
   | C | A | E |

3. **DEPENDENCY TYPES**
   - Hard dependencies: [Must have]
   - Soft dependencies: [Nice to have]
   - Circular dependencies: [Problematic loops]

4. **CRITICAL PATH**
   Longest dependency chain:
   [A] → [B] → [D] → [F]
   Duration: [Time]

5. **DEPENDENCY RISKS**
   - Risk 1: [Single point of failure]
   - Risk 2: [Bottleneck]
   - Risk 3: [Circular dependency]

6. **OPTIMIZATION OPPORTUNITIES**
   - Parallelize: [What can run concurrently]
   - Decouple: [Remove unnecessary dependencies]
   - Reorder: [Better sequence]

**OUTPUT FORMAT**: Clear dependency map with optimization recommendations.""",
            input_schema={"system": str, "context_section": str},
            constraints=Constraints(
                must_include=["dependency_table", "critical_path", "risks"],
                style_guide="Be clear and actionable",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(self, system: str = "", context: str | None = None, **kwargs):
        context_section = self._render_context_section(context)

        return super().build_context(system=system, context_section=context_section, **kwargs)

    def execute(
        self, provider: str = "openai", system: str = "", context: str | None = None, **kwargs
    ):
        return super().execute(provider=provider, system=system, context=context, **kwargs)
