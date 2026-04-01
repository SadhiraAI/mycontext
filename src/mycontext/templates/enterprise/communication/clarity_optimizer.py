"""
Clarity Optimizer - Improve clarity and precision of communication

Systematically improves clarity, reduces ambiguity, and enhances precision.
Based on clarity research and technical writing best practices.
"""

from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class ClarityOptimizer(Pattern):
    """
    Optimize text for maximum clarity.

    Improves:
    - Precision of language
    - Removal of ambiguity
    - Sentence structure
    - Word choice
    - Logical flow

    Based on: Technical writing and clarity research

    Example:
        >>> optimizer = ClarityOptimizer()
        >>> context = optimizer.build_context(
        ...     text="Original unclear text",
        ...     goal="Make it crystal clear"
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert technical writer and clarity specialist. Optimize the "
        "following text for maximum clarity, precision, and readability.\n\n"
        "Text to optimize: {text}\n"
        "Optimization goal: {goal}\n"
        "{context_section}\n\n"
        "Apply this clarity optimization methodology:\n"
        "(1) Identify all ambiguous terms, vague references, convoluted sentences, "
        "and redundant words in the original text. "
        "(2) Perform sentence-level analysis — for each unclear sentence, pinpoint "
        "the issue and determine a specific fix. "
        "(3) Replace imprecise words with concrete alternatives — swap vague terms "
        "like 'thing', 'stuff', 'very' for quantified, specific language. "
        "(4) Shorten complex sentences, add transitions, and improve logical flow "
        "between ideas. "
        "(5) Produce the fully optimized version with all improvements applied. "
        "(6) Summarize key gains: ambiguous terms removed, sentences shortened, "
        "and precision improvements made.\n\n"
        "Every word must earn its place. Be direct, precise, and actionable.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="clarity_optimizer",
            description="Optimize for maximum clarity",
            guidance=Guidance(
                role="Expert Technical Writer and Clarity Specialist",
                rules=[
                    "Eliminate ambiguity",
                    "Use precise language",
                    "Keep sentences short",
                    "Remove unnecessary words",
                    "Ensure logical flow",
                ],
                style="clear, precise, direct",
            ),
            directive_template="""Optimize clarity of:

**ORIGINAL TEXT**: {text}

{context_section}

**OPTIMIZATION GOAL**: {goal}

Clarity optimization:

1. **CLARITY ASSESSMENT**
   Current issues:
   - Ambiguity: [Unclear references]
   - Vagueness: [Imprecise terms]
   - Complexity: [Convoluted sentences]
   - Redundancy: [Unnecessary words]
   - Flow: [Logic gaps]

2. **SENTENCE-BY-SENTENCE ANALYSIS**
   [Break down each sentence]
   - Original: [Sentence]
   - Issue: [What's unclear]
   - Fix: [How to improve]

3. **WORD CHOICE OPTIMIZATION**
   Replace vague with precise:
   | Vague | Precise |
   |-------|---------|
   | thing | [specific term] |
   | stuff | [exact noun] |
   | very | [quantified] |

4. **STRUCTURE IMPROVEMENT**
   - Shorten long sentences
   - Add transitions
   - Improve paragraph breaks
   - Enhance logical flow

5. **OPTIMIZED VERSION**
   [Rewritten text with maximum clarity]

6. **KEY IMPROVEMENTS**
   - Removed [X] ambiguous terms
   - Shortened [Y] complex sentences
   - Added [Z] precise terms

**OUTPUT FORMAT**: Crystal-clear optimized text.""",
            input_schema={"text": str, "context_section": str, "goal": str},
            constraints=Constraints(
                must_include=["optimized_text", "improvements"], style_guide="Be clear and direct"
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def build_context(
        self, text: str = "", goal: str = "Maximum clarity", context: str | None = None, **kwargs
    ):
        context_section = self._render_context_section(context)

        return super().build_context(
            text=text, goal=goal, context_section=context_section, **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        text: str = "",
        goal: str = "Maximum clarity",
        context: str | None = None,
        **kwargs,
    ):
        return super().execute(provider=provider, text=text, goal=goal, context=context, **kwargs)
