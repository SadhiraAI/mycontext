"""
Causal Reasoner Template - Analyze cause-effect relationships

Structured causal analysis for understanding relationships between events.
"""

from mycontext.foundation import Guidance
from mycontext.structure import Pattern


class CausalReasoner(Pattern):
    """
    Causal reasoning template for analyzing cause-effect relationships.

    Systematically examines:
    - Root causes
    - Contributing factors
    - Causal chains
    - Effects and consequences
    - Correlation vs causation

    Based on: Causal inference and systems thinking frameworks

    Example:
        ```python
        from mycontext.templates.free import CausalReasoner

        reasoner = CausalReasoner()
        context = reasoner.build_context(
            phenomenon="Declining customer retention",
            depth="thorough"
        )
        ```

    Input Schema:
        - phenomenon (str): The effect or outcome to analyze
        - context_section (str, optional): Additional context
        - depth (str): Analysis depth ("basic", "detailed", "thorough")
    """

    GENERIC_PROMPT = (
        "You are an expert in causal inference and systems thinking. Conduct "
        "a systematic causal analysis of the following:\n\n"
        "Phenomenon: {phenomenon}\n"
        "{context_section}\n"
        "Analysis Depth: {depth}\n\n"
        "Apply this methodology: "
        "(1) Describe the phenomenon - clearly define the effect or outcome "
        "being analyzed, its significance, and timeline. "
        "(2) Identify immediate causes - determine the direct triggers and "
        "events that immediately preceded the phenomenon. "
        "(3) Trace root causes - dig deeper to find fundamental underlying "
        "factors, system-level conditions, and structural enablers. "
        "(4) Map causal chains - construct the sequence from root causes "
        "through intermediate steps to the final effect, including feedback "
        "loops and reinforcing cycles. "
        "(5) Distinguish correlation from causation - critically evaluate "
        "which relationships are truly causal vs. merely correlated, and "
        "identify confounding variables. "
        "(6) Perform counterfactual analysis - consider what would have "
        "happened if key causes were absent, and what interventions could "
        "change outcomes.\n\n"
        "Use evidence, logic, and systems thinking throughout.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, "
        "upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="causal_reasoner",
            description="Analyze cause-effect relationships systematically",
            guidance=Guidance(
                role="Expert Systems Analyst and Causal Inference Specialist",
                rules=[
                    "Distinguish between correlation and causation",
                    "Identify both direct and indirect causes",
                    "Consider multiple causal factors",
                    "Examine causal chains and feedback loops",
                    "Use evidence to support causal claims",
                    "Acknowledge uncertainty and alternative explanations",
                    "Consider temporal sequences (cause must precede effect)",
                    "Identify confounding variables",
                ],
                style="analytical, evidence-based, systematic",
            ),
            directive_template="""Analyze the causes and effects related to:

"{phenomenon}"

{context_section}

Analysis depth: {depth}

Causal Analysis Framework:

1. PHENOMENON DESCRIPTION
   - Clear description of the effect/outcome being analyzed
   - When did it start/occur?
   - How significant is it?

2. IMMEDIATE CAUSES (Direct Triggers)
   - What directly caused this?
   - What events immediately preceded it?
   - Evidence for each cause

3. ROOT CAUSES (Underlying Factors)
   - What are the fundamental causes?
   - Why did the immediate causes occur?
   - System-level factors

4. CONTRIBUTING FACTORS
   - What conditions enabled this?
   - What factors made it worse/better?
   - Environmental/contextual influences

5. CAUSAL CHAINS
   - Map the sequence: Root → Intermediate → Immediate → Effect
   - Identify feedback loops
   - Show interconnections

6. CORRELATION VS. CAUSATION
   - What might be correlated but not causal?
   - What alternative explanations exist?
   - What evidence distinguishes correlation from causation?

7. EFFECTS AND CONSEQUENCES
   - Primary effects
   - Secondary effects
   - Long-term consequences
   - Unintended consequences

8. CAUSAL MECHANISMS
   - HOW does X cause Y?
   - Through what mechanisms?
   - What's the theoretical basis?

9. COUNTERFACTUAL ANALYSIS
   - What if the cause(s) hadn't occurred?
   - What if conditions were different?
   - What would prevent this effect?

10. SYNTHESIS
    - Primary causal pathway (most likely)
    - Confidence level for each causal claim
    - Key uncertainties or gaps in understanding

Use evidence, logic, and systems thinking throughout.""",
            input_schema={"phenomenon": str, "context_section": str, "depth": str},
        )

    def _render_context_section(self, context: str) -> str:
        """Render the context section"""
        if not context or context.strip() == "":
            return ""
        return f"\nAdditional Context:\n{context}\n"

    def build_context(self, phenomenon: str, context: str = "", depth: str = "detailed", **kwargs):
        """
        Build a context for causal analysis.

        Args:
            phenomenon: The effect or outcome to analyze
            context: Optional additional context
            depth: Analysis depth
            **kwargs: Additional parameters

        Returns:
            Context configured for causal reasoning
        """
        context_section = self._render_context_section(context or "")

        # Clean up kwargs
        kwargs.pop("context", None)
        kwargs.pop("context_section", None)

        return super().build_context(
            phenomenon=phenomenon, context_section=context_section, depth=depth, **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        phenomenon: str = None,
        context: str = "",
        depth: str = "detailed",
        **kwargs,
    ):
        """
        Execute causal analysis directly.

        Args:
            provider: LLM provider to use
            phenomenon: The effect to analyze
            context: Additional context
            depth: Analysis depth
            **kwargs: Provider parameters

        Returns:
            Provider response with causal analysis
        """
        context_section = self._render_context_section(context or "")

        # Separate provider kwargs
        provider_params = {}
        provider_param_names = {
            "model",
            "temperature",
            "max_tokens",
            "top_p",
            "frequency_penalty",
            "presence_penalty",
            "stop",
            "user",
            "api_key",
            "base_url",
        }

        for key in list(kwargs.keys()):
            if key in provider_param_names:
                provider_params[key] = kwargs.pop(key)

        # Clean up
        kwargs.pop("context", None)
        kwargs.pop("context_section", None)

        return super().execute(
            provider=provider,
            phenomenon=phenomenon,
            context_section=context_section,
            depth=depth,
            **provider_params,
        )
