"""
Socratic Questioner Template - Question assumptions through dialogue

Based on the Socratic method of inquiry through questioning.
Helps users examine beliefs, assumptions, and reasoning.
"""

from typing import Optional
from ...structure.pattern import Pattern
from ...foundation import Guidance, Directive


class SocraticQuestioner(Pattern):
    """
    Socratic questioning template for deep inquiry and assumption examination.
    
    Uses the Socratic method to:
    - Question underlying assumptions
    - Explore implications
    - Examine evidence
    - Challenge reasoning
    - Promote critical thinking
    
    Based on: Classical Socratic dialogue method
    
    Example:
        ```python
        from mycontext.templates.free import SocraticQuestioner
        
        questioner = SocraticQuestioner()
        context = questioner.build_context(
            statement="We should implement AI in our hiring process",
            depth="thorough"
        )
        
        # Use the context with any provider
        result = context.execute(provider="openai", model="gpt-4o-mini")
        ```
    
    Input Schema:
        - statement (str): The claim, belief, or position to examine
        - context_section (str, optional): Additional context
        - depth (str): Level of inquiry ("basic", "detailed", "thorough")
    """
    
    def __init__(self):
        super().__init__(
            name="socratic_questioner",
            description="Question assumptions and beliefs through Socratic dialogue",
            guidance=Guidance(
                role="Socratic Philosopher and Critical Thinking Expert",
                rules=[
                    "Ask probing questions rather than making statements",
                    "Question underlying assumptions systematically",
                    "Explore implications and consequences",
                    "Challenge reasoning with evidence",
                    "Guide toward deeper understanding through inquiry",
                    "Be respectful and intellectually humble",
                    "Focus on clarifying thinking, not attacking the person"
                ],
                style="inquisitive, patient, thought-provoking"
            ),
            directive_template="""Apply Socratic questioning to examine this statement:

"{statement}"

{context_section}

Depth of inquiry: {depth}

Use these Socratic questioning categories:

1. CLARIFYING QUESTIONS
   - What exactly do you mean by...?
   - Can you give me an example?
   - How does this relate to...?

2. PROBING ASSUMPTIONS
   - What are you assuming here?
   - Why would someone assume that?
   - What if we assumed the opposite?

3. PROBING REASONS AND EVIDENCE
   - What evidence supports this?
   - How do we know this is true?
   - What are the sources of this belief?

4. QUESTIONING VIEWPOINTS
   - What alternative perspectives exist?
   - How might others view this differently?
   - What are the strengths/weaknesses of this view?

5. PROBING IMPLICATIONS
   - What are the consequences of this?
   - If this is true, what else must be true?
   - What might be unintended consequences?

6. QUESTIONING THE QUESTION
   - Why is this question important?
   - What assumptions does the question contain?
   - Is this the right question to ask?

For each category relevant to the statement, generate 2-3 thought-provoking questions.
Then synthesize the key insights these questions reveal.""",
            input_schema={
                "statement": str,
                "context_section": str,
                "depth": str
            }
        )
    
    def _render_context_section(self, context: str) -> str:
        """Render the context section for the directive template"""
        if not context or context.strip() == "":
            return ""
        return f"\nAdditional Context:\n{context}\n"
    
    def build_context(
        self,
        statement: str,
        context: str = "",
        depth: str = "detailed",
        **kwargs
    ):
        """
        Build a context for Socratic questioning.
        
        Args:
            statement: The claim, belief, or position to examine
            context: Optional additional context
            depth: Level of inquiry ("basic", "detailed", "thorough")
            **kwargs: Additional parameters
            
        Returns:
            Context configured for Socratic questioning
        """
        if not context:
            context = ""
        
        context_section = self._render_context_section(context)
        
        # Remove context from kwargs to avoid passing it to parent
        kwargs.pop('context', None)
        kwargs.pop('context_section', None)
        
        return super().build_context(
            statement=statement,
            context_section=context_section,
            depth=depth,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        statement: str = None,
        context: str = "",
        depth: str = "detailed",
        **kwargs
    ):
        """
        Execute Socratic questioning directly.
        
        Args:
            provider: LLM provider to use
            statement: The claim to examine
            context: Optional additional context
            depth: Level of inquiry
            **kwargs: Provider parameters (model, temperature, etc.)
            
        Returns:
            Provider response with Socratic questions and insights
        """
        if not context:
            context = ""
        
        context_section = self._render_context_section(context)
        
        # Separate provider kwargs
        provider_params = {}
        provider_param_names = {'model', 'temperature', 'max_tokens', 'top_p', 
                               'frequency_penalty', 'presence_penalty', 'stop', 
                               'user', 'api_key', 'base_url'}
        
        for key in list(kwargs.keys()):
            if key in provider_param_names:
                provider_params[key] = kwargs.pop(key)
        
        # Remove context-related params
        kwargs.pop('context', None)
        kwargs.pop('context_section', None)
        
        return super().execute(
            provider=provider,
            statement=statement,
            context_section=context_section,
            depth=depth,
            **provider_params
        )
