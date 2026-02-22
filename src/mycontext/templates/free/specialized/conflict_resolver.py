"""
Conflict Resolver - Resolve conflicts and disagreements

Systematic conflict resolution using proven frameworks.
Based on conflict resolution theory and mediation practices.
"""


from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class ConflictResolver(Pattern):
    """
    Resolve conflicts systematically.
    
    Addresses:
    - Interpersonal conflicts
    - Team disagreements
    - Stakeholder conflicts
    - Value conflicts
    - Resource conflicts
    
    Based on: Conflict resolution theory and mediation
    
    Example:
        >>> resolver = ConflictResolver()
        >>> context = resolver.build_context(
        ...     conflict="Team disagrees on technical approach",
        ...     parties=["Engineering team", "Product team"]
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert mediator and conflict resolution specialist. Analyze "
        "and resolve the following conflict:\n\n"
        "Conflict: {conflict}\n"
        "Parties involved: {parties}\n"
        "{context_section}\n\n"
        "Apply structured mediation methodology: "
        "(1) Analyze the conflict — classify its type (interpersonal, structural, "
        "value-based, interest-based), assess severity, duration, and key triggers. "
        "(2) Map each party's perspective — their stated position, underlying "
        "interests, core concerns, and what they fear losing. "
        "(3) Identify common ground — shared goals, values, constraints, and mutual "
        "dependencies. "
        "(4) Diagnose root causes — what underlying issues are driving the "
        "surface-level disagreement? "
        "(5) Generate resolution options: (a) Compromise — each side gives something; "
        "(b) Collaboration — expand the pie; (c) Creative — reframe the problem "
        "entirely. For each option, outline pros, cons, and feasibility. "
        "(6) Recommend the best resolution with a clear rationale, implementation "
        "steps, and follow-up plan.\n\n"
        "Stay neutral. Understand all perspectives before proposing solutions."
    )

    def __init__(self):
        super().__init__(
            name="conflict_resolver",
            description="Resolve conflicts systematically",
            guidance=Guidance(
                role="Expert Mediator and Conflict Resolution Specialist",
                rules=[
                    "Stay neutral and objective",
                    "Understand all perspectives",
                    "Find common ground",
                    "Focus on interests, not positions",
                    "Seek win-win solutions"
                ],
                style="diplomatic, empathetic, solution-focused"
            ),
            directive_template="""Resolve this conflict:

**CONFLICT**: {conflict}

**PARTIES INVOLVED**: {parties}

{context_section}

Conflict resolution:

1. **CONFLICT ANALYSIS**
   - Type: [Interpersonal/Resource/Value/Process]
   - Severity: [High/Medium/Low]
   - Duration: [How long]
   - Triggers: [What sparked it]

2. **PERSPECTIVES**
   **Party A viewpoint**:
   - Position: [What they want]
   - Interests: [Why they want it]
   - Concerns: [What worries them]
   
   **Party B viewpoint**:
   - [Same structure]

3. **COMMON GROUND**
   What they agree on:
   - Shared goal: [Mutual objective]
   - Shared values: [Common beliefs]
   - Shared constraints: [Common limitations]

4. **ROOT CAUSES**
   Underlying issues:
   - Cause 1: [Real issue]
   - Cause 2: [Another factor]

5. **RESOLUTION OPTIONS**
   **Option A** (Compromise):
   - [Solution]
   - Pros/Cons
   
   **Option B** (Collaboration):
   - [Win-win solution]
   - Pros/Cons
   
   **Option C** (Creative):
   - [Novel approach]
   - Pros/Cons

6. **RECOMMENDED RESOLUTION**
   - Solution: [Best approach]
   - Why: [Rationale]
   - Implementation: [How to execute]
   - Follow-up: [Ensure it sticks]

**OUTPUT FORMAT**: Balanced resolution with implementation plan.""",
            input_schema={
                "conflict": str,
                "parties": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=["perspectives", "common_ground", "resolution"],
                style_guide="Be neutral and constructive"
            )
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        conflict: str = "",
        parties: str = "",
        context: str | None = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)

        return super().build_context(
            conflict=conflict,
            parties=parties,
            context_section=context_section,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        conflict: str = "",
        parties: str = "",
        context: str | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            conflict=conflict,
            parties=parties,
            context=context,
            **kwargs
        )
