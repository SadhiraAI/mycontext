"""
Technical Translator - Translate technical to plain language

Converts technical jargon into accessible, understandable language.
Based on technical communication and plain language principles.
"""


from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern
from mycontext.utils.format_directives import VALID_OUTPUT_FORMATS, get_format_directive


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
        "Translate the following technical content into clear, accessible language:\n\n"
        "Technical content: {technical_text}\n"
        "Target audience: {target_audience}\n"
        "{context_section}\n\n"
        "Identify jargon and domain-specific terms, provide plain-language equivalents, "
        "rewrite the content for the target audience using concrete examples and everyday "
        "analogies, and verify the translation is understandable to a non-specialist.\n\n"
        "Maintain accuracy. Never sacrifice correctness for simplicity."
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
        output_format: str = "structured",
        **kwargs,
    ):
        """
        Build context for technical translation.

        Args:
            technical_text: The technical content to translate
            target_audience: Who the translation is for
            context: Optional additional context
            output_format: How to present results — ``"structured"`` (default)
                gives the full 4-section output; ``"narrative"`` gives just the
                translated text as prose; ``"brief"`` gives a compact version.
        """
        if output_format not in VALID_OUTPUT_FORMATS:
            raise ValueError(
                f"Invalid output_format {output_format!r}. "
                f"Choose from: {sorted(VALID_OUTPUT_FORMATS)}"
            )
        context_section = self._render_context_section(context)
        ctx = super().build_context(
            technical_text=technical_text,
            target_audience=target_audience,
            context_section=context_section,
            **kwargs,
        )
        fmt = get_format_directive(output_format)
        if fmt and ctx.directive:
            ctx.directive = Directive(content=ctx.directive.content + fmt)
            ctx.metadata["output_format"] = output_format
        return ctx

    def execute(
        self,
        provider: str = "openai",
        technical_text: str = "",
        target_audience: str = "general public",
        context: str | None = None,
        output_format: str = "structured",
        **kwargs,
    ):
        """
        Execute technical translation.

        Args:
            provider: LLM provider to use
            technical_text: The technical content to translate
            target_audience: Who the translation is for
            context: Optional additional context
            output_format: How to present results — ``"structured"`` (default)
                | ``"narrative"`` | ``"brief"`` | ``"actionable"``
        """
        provider_params = {
            "model", "temperature", "max_tokens", "top_p",
            "frequency_penalty", "presence_penalty", "stop",
            "user", "api_key", "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        ctx = self.build_context(
            technical_text=technical_text,
            target_audience=target_audience,
            context=context,
            output_format=output_format,
        )
        return ctx.execute(provider=provider, **provider_kwargs)
