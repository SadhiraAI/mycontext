"""
Audience Adapter - Adapt communication for different audiences.

Tailors messages, tone, and content to specific audiences.
Based on communication theory and audience analysis.

output parameter controls section selection:
  full_analysis — all 11 sections (default): full audience analysis + adapted message
  message_only  — 3 sections: core message + adapted message + key changes made
"""

from __future__ import annotations

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern

VALID_OUTPUTS: frozenset[str] = frozenset({"full_analysis", "message_only"})


def _build_directive(output: str) -> str:
    """Assemble the directive at runtime — scaffold never stored as a module-level constant."""
    sections = {
        "audience_analysis": (
            "1. **TARGET AUDIENCE ANALYSIS**\n\n"
            "   **Who they are**:\n"
            "   - Role/position: [What they do]\n"
            "   - Background: [Education, experience level]\n"
            "   - Technical level: [Novice / Intermediate / Expert]\n"
            "   - Domain knowledge: [What they already know]\n\n"
            "   **What they care about**:\n"
            "   - Primary interests: [Top priorities]\n"
            "   - Pain points: [What concerns them most]\n"
            "   - Decision criteria: [How they evaluate information]\n\n"
            "   **Communication preferences**:\n"
            "   - Preferred style: [Formal / casual / technical / narrative]\n"
            "   - Detail level: [High-level / detailed]\n"
            "   - Attention span: [Short / medium / long form]"
        ),
        "language": (
            "2. **LANGUAGE ADAPTATION**\n\n"
            "   **Jargon Translation**:\n"
            "   | Original Term | Audience-Friendly Version |\n"
            "   |---------------|-------------------------|\n"
            "   | [Tech term 1] | [Plain language] |\n"
            "   | [Tech term 2] | [Accessible phrase] |\n\n"
            "   **Complexity adjustment**: [How simplified or enriched vs. original]"
        ),
        "core_message": (
            "3. **CORE MESSAGE EXTRACTION**\n\n"
            "   **Essential points** (preserve these in the adapted version):\n"
            "   1. [Key message 1]\n"
            "   2. [Key message 2]\n"
            "   3. [Key message 3]\n\n"
            "   **What to emphasise for this audience**: [What matters most to them]\n"
            "   **What to minimise**: [Less important for this audience]"
        ),
        "framing": (
            "4. **FRAMING FOR AUDIENCE**\n\n"
            "   **Their perspective**: [What frame of reference makes this immediately relevant?]\n\n"
            "   **Value proposition** (reframed):\n"
            "   - Business value: [ROI, risk, competitive advantage]\n"
            "   - Technical merit: [Correctness, elegance, maintainability]\n"
            "   - User benefit: [Ease, speed, outcome]\n"
            "   - Strategic fit: [Alignment to goals]"
        ),
        "examples": (
            "5. **EXAMPLE & ANALOGY ADAPTATION**\n\n"
            "   **Audience-appropriate examples**:\n"
            "   - Example 1: [Relatable to this audience] — why it resonates: [Connection]\n"
            "   - Example 2: [From their domain or experience]\n\n"
            "   **Analogy**: [Restate the core concept using something from their world]"
        ),
        "tone": (
            "6. **TONE & STYLE ADJUSTMENT**\n\n"
            "   - Original tone: [Description]\n"
            "   - Target tone: [What is appropriate for this audience]\n"
            "   - Formality shift: [More or less formal — and why]\n"
            "   - Energy shift: [More or less assertive — and why]"
        ),
        "structure": (
            "7. **STRUCTURE OPTIMISATION**\n\n"
            "   - Opening: [Hook that immediately connects to what they care about]\n"
            "   - Organisation: [How this audience processes information best]\n"
            "   - Closing: [Strong finish — what action or understanding to leave them with]"
        ),
        "adapted_message": (
            "8. **ADAPTED MESSAGE**\n\n"
            "[The full original message, completely rewritten for the target audience.\n"
            "Every sentence should reflect: their vocabulary, their priorities, their\n"
            "frame of reference, and the appropriate level of technical detail.\n"
            "Do not summarise — produce the full adapted version.]"
        ),
        "key_changes": (
            "9. **KEY ADAPTATIONS MADE**\n\n"
            "Summary of what changed and why:\n"
            "- Language: [Specific jargon replaced and with what]\n"
            "- Examples: [New examples used and why they resonate]\n"
            "- Focus: [What was emphasised vs. de-emphasised]\n"
            "- Tone: [How the register shifted]\n"
            "- Length: [Expanded or condensed — and why]"
        ),
        "questions": (
            "10. **ANTICIPATED QUESTIONS**\n\n"
            "What this audience is likely to ask:\n"
            "- Q1: [Most likely question] \u2192 A: [Prepared answer]\n"
            "- Q2: [Second likely question] \u2192 A: [Response]\n"
            "- Q3: [Third question] \u2192 A: [Answer]"
        ),
        "delivery": (
            "11. **DELIVERY RECOMMENDATIONS**\n\n"
            "- Medium: [Email / presentation / conversation / document]\n"
            "- Timing: [When to deliver for best reception]\n"
            "- Setting: [Formal / informal / one-on-one / group]\n"
            "- What to avoid: [Pitfalls with this specific audience]"
        ),
    }
    configs = {
        "full_analysis": {
            "keys": [
                "audience_analysis", "language", "core_message", "framing",
                "examples", "tone", "structure", "adapted_message", "key_changes",
                "questions", "delivery",
            ],
            "instruction": (
                "Conduct a full audience adaptation analysis, then deliver the adapted message "
                "and a comprehensive summary of changes made."
            ),
            "total": "11 sections",
        },
        "message_only": {
            "keys": ["core_message", "adapted_message", "key_changes"],
            "instruction": (
                "Extract the core message, produce the fully adapted version for the target "
                "audience, and briefly summarise what was changed. Skip the detailed analysis "
                "— focus on delivering the adapted message."
            ),
            "total": "3 sections",
        },
    }
    cfg = configs.get(output, configs["full_analysis"])
    sections_text = "\n\n".join(sections[k] for k in cfg["keys"])

    return (
        f"Adapt this communication for a different audience:\n\n"
        f"**ORIGINAL MESSAGE**: {{message}}\n\n"
        f"**CURRENT AUDIENCE**: {{current_audience}}\n\n"
        f"**TARGET AUDIENCE**: {{target_audience}}\n\n"
        f"{{context_section}}\n\n"
        f"**OUTPUT MODE**: {output} ({cfg['total']})\n\n"
        f"{cfg['instruction']}\n\n"
        f"{sections_text}\n\n"
        f"**OUTPUT FORMAT**: Fully adapted message. Preserve accuracy, maximise resonance."
    )


# ---------------------------------------------------------------------------
# Template class
# ---------------------------------------------------------------------------

class AudienceAdapter(Pattern):
    """
    Adapt communication for a target audience.

    Rewrites content for a different audience by adjusting language level,
    framing, examples, tone, and structure.

    The **output** parameter controls how much analysis is shown:

    - ``full_analysis`` (11 sections, default): Full audience profiling,
      jargon translation table, framing analysis, tone adjustment, structure
      optimisation, adapted message, changes summary, anticipated questions,
      and delivery recommendations.  Use when you want to understand *why*
      the adaptation works, or need to brief someone on how to present it.
    - ``message_only`` (3 sections): Core message → Adapted message →
      Key changes.  Use when you just need the adapted text — the most common
      use case.  ~75% fewer sections.

    Examples:
        >>> adapter = AudienceAdapter()
        >>> # Just get the adapted message
        >>> result = adapter.execute(
        ...     provider="openai",
        ...     message="Our ML pipeline uses gradient boosting with SHAP explainability",
        ...     current_audience="data scientists",
        ...     target_audience="CFO and finance team",
        ...     output="message_only",
        ... )
        >>> # Full analysis for a comms team to use
        >>> result = adapter.execute(
        ...     provider="openai",
        ...     message="We are migrating to a microservices architecture",
        ...     current_audience="engineering team",
        ...     target_audience="board of directors",
        ...     output="full_analysis",
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "Adapt the following content for a different audience:\n\n"
        "Original message: {message}\n"
        "Current audience: {current_audience}\n"
        "Target audience: {target_audience}\n"
        "{context_section}\n\n"
        "Profile the target audience, extract the core message, adjust language and "
        "technical level, reframe with audience-appropriate examples, adapt tone, and "
        "deliver a fully adapted version. Note key changes made.\n\n"
        "Preserve accuracy. Maximise resonance for the target audience."
    )

    def __init__(self):
        super().__init__(
            name="audience_adapter",
            description="Adapt communication for audiences",
            guidance=Guidance(
                role="Expert Communication Strategist and Audience Specialist",
                rules=[
                    "Understand the target audience deeply before adapting",
                    "Match technical level precisely",
                    "Use examples and analogies from the target audience's world",
                    "Preserve the core message's factual accuracy",
                    "Focus on what matters to them, not what matters to the sender",
                ],
                style="adaptive, empathetic, clear",
            ),
            directive_template=_build_directive("full_analysis"),
            input_schema={
                "message": str,
                "current_audience": str,
                "target_audience": str,
                "context_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "adapted_message",
                    "key_changes",
                ],
                style_guide="Be respectful of both audiences — not condescending to either",
            ),
        )

    def _render_context_section(self, context: str | None) -> str:
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        message: str = "",
        current_audience: str = "general",
        target_audience: str = "specific group",
        context: str | None = None,
        output: str = "full_analysis",
        **kwargs,
    ):
        """
        Build context for audience adaptation.

        Args:
            message: The original message to adapt
            current_audience: Who the message is currently written for
            target_audience: Who it needs to be rewritten for
            context: Optional additional context
            output: ``"full_analysis"`` (default, 11 sections)
                | ``"message_only"`` (3 sections — adapted message + changes)
        """
        if output not in VALID_OUTPUTS:
            raise ValueError(
                f"Invalid output {output!r}. Choose from: {sorted(VALID_OUTPUTS)}"
            )
        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        context_section = self._render_context_section(context)
        directive_text = _build_directive(output)
        directive_content = safe_format_template(
            directive_text,
            message=message,
            current_audience=current_audience,
            target_audience=target_audience,
            context_section=context_section,
        )

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data={
                "message": message,
                "current_audience": current_audience,
                "target_audience": target_audience,
                "context_section": context_section,
            },
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["output"] = output
        return ctx

    def execute(
        self,
        provider: str = "openai",
        message: str = "",
        current_audience: str = "general",
        target_audience: str = "specific group",
        context: str | None = None,
        output: str = "full_analysis",
        **kwargs,
    ):
        """
        Execute audience adaptation.

        Args:
            provider: LLM provider to use
            message: The original message to adapt
            current_audience: Who the message is currently written for
            target_audience: Who it needs to be rewritten for
            context: Optional additional context
            output: ``"full_analysis"`` (default) | ``"message_only"``
            **kwargs: Provider parameters
        """
        provider_params = {
            "model", "temperature", "max_tokens", "top_p",
            "frequency_penalty", "presence_penalty", "stop",
            "user", "api_key", "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        ctx = self.build_context(
            message=message,
            current_audience=current_audience,
            target_audience=target_audience,
            context=context,
            output=output,
        )
        return ctx.execute(provider=provider, **provider_kwargs)
