"""
Conflict Resolver - Resolve conflicts and disagreements

Systematic conflict resolution using proven frameworks.
Based on conflict resolution theory and mediation practices.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


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
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        conflict: str = "",
        parties: str = "",
        context: Optional[str] = None,
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
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            conflict=conflict,
            parties=parties,
            context=context,
            **kwargs
        )
