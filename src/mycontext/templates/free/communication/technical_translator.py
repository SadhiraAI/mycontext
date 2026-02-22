"""
Technical Translator - Translate technical to plain language

Converts technical jargon into accessible, understandable language.
Based on technical communication and plain language principles.
"""


from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


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

    GENERIC_PROMPT = (
        "You are a technical communicator and plain language specialist. Translate "
        "the following technical content into clear, accessible language:\n\n"
        "Technical content: {technical_text}\n"
        "Target audience: {target_audience}\n"
        "{context_section}\n\n"
        "Follow a structured translation approach: "
        "(1) Identify all jargon, acronyms, and domain-specific terms. "
        "(2) Create a translation map — for each technical term, provide the "
        "plain-language equivalent and a brief explanation. "
        "(3) Rewrite the entire content for the target audience, replacing jargon "
        "with common words, using concrete examples and everyday analogies, and "
        "maintaining factual accuracy. "
        "(4) Verify: apply the '12-year-old test' — would someone outside the field "
        "understand this? Confirm all key concepts are preserved, examples are "
        "relatable, and the tone is appropriate for the audience.\n\n"
        "Maintain accuracy while maximizing clarity. Never sacrifice correctness "
        "for simplicity."
    )

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

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        technical_text: str = "",
        target_audience: str = "general public",
        context: str | None = None,
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
        context: str | None = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            technical_text=technical_text,
            target_audience=target_audience,
            context=context,
            **kwargs
        )
