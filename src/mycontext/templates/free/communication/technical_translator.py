"""
Technical Translator - Translate technical to plain language

Converts technical jargon into accessible, understandable language.
Based on technical communication and plain language principles.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class TechnicalTranslator(Pattern):
    """
    Translate technical content to plain language.
    
    Converts:
    - Technical jargon → Plain language
    - Complex concepts → Simple terms
    - Specialist knowledge → General understanding
    
    Based on: Plain language principles and technical communication
    
    Example:
        >>> translator = TechnicalTranslator()
        >>> context = translator.build_context(
        ...     technical_text="Our microservices architecture uses event-driven patterns",
        ...     target_audience="business stakeholders"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """
    
    def __init__(self):
        super().__init__(
            name="technical_translator",
            description="Technical to plain language",
            guidance=Guidance(
                role="Expert Technical Communicator and Plain Language Specialist",
                rules=[
                    "Replace jargon with common words",
                    "Use concrete examples",
                    "Maintain accuracy",
                    "Test understanding",
                    "Respect audience intelligence"
                ],
                style="clear, accessible, respectful"
            ),
            directive_template="""Translate to plain language:

**TECHNICAL TEXT**: {technical_text}

**TARGET AUDIENCE**: {target_audience}

{context_section}

Translation:

1. **JARGON IDENTIFICATION**
   Technical terms to translate:
   - [Term 1]
   - [Term 2]
   - [Term 3]

2. **TRANSLATION MAP**
   | Technical | Plain Language |
   |-----------|----------------|
   | [Jargon 1] | [Simple term] |
   | [Jargon 2] | [Accessible phrase] |

3. **TRANSLATED VERSION**
   [Complete text rewritten in plain language]

4. **VERIFICATION**
   - Would a 12-year-old understand? [Yes/No]
   - Key concepts preserved? [Yes/No]
   - Examples included? [Yes/No]

**OUTPUT FORMAT**: Clear, accessible translation.""",
            input_schema={
                "technical_text": str,
                "target_audience": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=["translation_map", "plain_version"],
                style_guide="Be clear without being condescending"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        technical_text: str = "",
        target_audience: str = "general public",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            technical_text=technical_text,
            target_audience=target_audience,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        technical_text: str = "",
        target_audience: str = "general public",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            technical_text=technical_text,
            target_audience=target_audience,
            context=context,
            **kwargs
        )
