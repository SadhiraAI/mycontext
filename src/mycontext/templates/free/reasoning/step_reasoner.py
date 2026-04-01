"""
Step-by-Step Reasoner Template - Systematic problem solving with transparent reasoning.

Based on "step-by-step reasoning" cognitive tool and Chain-of-Thought methodology.

output_mode controls how much of the reasoning chain is shown in the response:
  visible        — full 5-phase output (default): all steps visible
  answer_focused — reasoning is abbreviated; conclusion is prominent (~40% fewer tokens)
  check_only     — given a proposed answer, runs VERIFY + CONCLUDE only

Free tier template - part of mycontext open source.
"""

from __future__ import annotations

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern

VALID_OUTPUT_MODES: frozenset[str] = frozenset({"visible", "answer_focused", "check_only"})


def _build_directive(output_mode: str) -> str:
    """Assemble the directive at runtime — scaffold never stored as a module-level constant."""
    if output_mode == "answer_focused":
        return (
            "Solve this problem. Show enough reasoning to be trustworthy, then deliver a clear answer.\n\n"
            "**PROBLEM**:\n{problem}\n\n"
            "{context_section}\n\n"
            "**DOMAIN**: {domain}\n\n"
            "## REASONING\n"
            "Work through the problem. Show the key steps and logic \u2014 skip obvious sub-steps, "
            "but show anything non-trivial.\n"
            "```\n[Key calculation or reasoning chain here]\n```\n\n"
            "## VERIFY\n"
            "One-line check: does the answer make sense? [Yes/No + brief reason]\n\n"
            "## ANSWER\n"
            "\U0001f3af **[Final answer \u2014 stated clearly and completely]**\n\n"
            "**Confidence**: [High / Medium / Low] \u2014 [one sentence why]\n\n"
            "---\n\n"
            '*Optimised for clarity and token efficiency. Full step-by-step available with output_mode="visible".*'
        )
    if output_mode == "check_only":
        return (
            "A proposed solution has been given for the following problem. "
            "Verify it and provide a final verdict.\n\n"
            "**PROBLEM**:\n{problem}\n\n"
            "{context_section}\n\n"
            "**PROPOSED ANSWER**:\n{proposed_answer}\n\n"
            "## VERIFY\n\n"
            "**Step 1 \u2014 Re-derive independently**:\n"
            "Work out the correct answer from scratch (briefly). Show only the essential steps.\n"
            "```\n[Your independent derivation]\n= [Your answer]\n```\n\n"
            "**Step 2 \u2014 Compare**:\n"
            "- Your answer: [What you got] | Proposed answer: [What was given] | Match: [Yes / No / Partially]\n\n"
            "**Step 3 \u2014 Error analysis** (if mismatch):\n"
            "- Where does the proposed answer go wrong?\n"
            "- What type of error? (arithmetic, logic, misunderstanding, sign error, etc.)\n\n"
            "## CONCLUDE\n\n"
            "**Verdict**: [CORRECT / INCORRECT / PARTIALLY CORRECT]\n\n"
            "**Corrected answer** (if needed): [State the right answer]\n\n"
            "**Confidence**: [High / Medium / Low] \u2014 [one sentence why]"
        )
    return (
        "Solve this problem by breaking it down into clear, logical steps.\n\n"
        "**PROBLEM**:\n{problem}\n\n"
        "{context_section}\n\n"
        "Follow this systematic process:\n\n"
        "## Step 1: UNDERSTAND\n\n"
        "**Restate the Problem**:\n"
        "- In your own words: [Reformulate the problem]\n"
        "- What we're looking for: [The unknown or goal]\n"
        "- Key information given: [All relevant facts, numbers, constraints]\n\n"
        "**Identify the Type**:\n"
        "- Problem category: [Mathematical, logical, analytical, etc.]\n"
        "- Required operations: [What calculations or reasoning steps]\n\n"
        "## Step 2: PLAN\n\n"
        "- Overall approach: [How you'll solve this]\n"
        "- Methods/techniques: [Specific formulas, algorithms, or reasoning patterns]\n"
        "- Solution path sketch: [Input] \u2192 [Step A] \u2192 [Step B] \u2192 [Solution]\n\n"
        "## Step 3: EXECUTE\n\n"
        "Work through each step methodically. For each step, show: **What** / **Why** / **How** / **Result**.\n\n"
        "### Step 3.1: [Description]\n"
        "- **Action**: [What operation or reasoning]\n"
        "- **Calculation/Logic**: ```[Show your work] = [intermediate result]```\n"
        "- **Result**: [What this step produces]\n\n"
        "### Step 3.2: [Description]\n"
        "[Same format \u2014 add as many steps as needed]\n\n"
        "## Step 4: VERIFY\n\n"
        "- Does this answer what was asked? [Yes/No + explanation]\n"
        "- Units correct? [If applicable] | Scale reasonable? [Sanity check]\n"
        "- Alternative verification: [Try solving another way if possible]\n\n"
        "## Step 5: CONCLUDE\n\n"
        "\U0001f3af **[State the answer clearly and explicitly]**\n\n"
        "- Complete statement: [Answer in a complete sentence with units/format]\n"
        "- Confidence: [High / Medium / Low] \u2014 [Why] \u2014 [What could change this]\n\n"
        "---\n\n"
        "**REQUIREMENTS**: Show ALL work. Explain WHY each step is necessary. Verify the solution."
    )


# ---------------------------------------------------------------------------
# Template class
# ---------------------------------------------------------------------------


class StepByStepReasoner(Pattern):
    """
    Guide systematic problem-solving through clear, logical steps.

    Implements Chain-of-Thought reasoning, breaking complex problems into
    manageable sequential steps with transparent reasoning at each stage.

    The **output_mode** parameter controls how much of the reasoning is shown:

    - ``visible`` (default): Full 5-phase output — UNDERSTAND → PLAN → EXECUTE →
      VERIFY → CONCLUDE.  Every step, every calculation, every decision shown.
      Best for teaching, debugging, or when the reasoning process matters.
    - ``answer_focused``: Abbreviated reasoning + prominent conclusion.
      ~40% fewer tokens.  Best when you trust the model and just need the answer
      with enough reasoning to be trustworthy.
    - ``check_only``: Pass a ``proposed_answer`` and the template independently
      re-derives and verifies it.  Best for checking existing work.

    Based on:
    - "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
      (Wei et al., 2023)
    - IBM Zurich cognitive tools research (2025)

    Examples:
        >>> from mycontext.templates.free import StepByStepReasoner
        >>>
        >>> reasoner = StepByStepReasoner()
        >>>
        >>> # Full visible reasoning (default)
        >>> result = reasoner.execute(
        ...     provider="gemini",
        ...     problem="A train travels 120 km in 2 h, then 200 km in 2.5 h. Average speed?",
        ... )
        >>>
        >>> # Compact answer — same reasoning, less output
        >>> result = reasoner.execute(
        ...     provider="gemini",
        ...     problem="What is the compound interest on $5,000 at 6% for 3 years?",
        ...     output_mode="answer_focused",
        ... )
        >>>
        >>> # Verify someone else's work
        >>> result = reasoner.execute(
        ...     provider="gemini",
        ...     problem="What is 15% of 240?",
        ...     proposed_answer="38",
        ...     output_mode="check_only",
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "Solve the following problem using explicit, step-by-step reasoning:\n\n"
        "Problem: {problem}\n"
        "{context_section}\n"
        "Domain: {domain}\n\n"
        "Restate the problem in your own words, plan your approach, work through each "
        "step methodically showing your reasoning at each stage, verify the answer, "
        "and state the final answer clearly with a confidence assessment.\n\n"
        "Show all work. Make your thought process transparent."
    )

    def __init__(self):
        super().__init__(
            name="step_by_step_reasoner",
            guidance=Guidance(
                role="Expert Problem Solver and Educator",
                rules=[
                    "Break problems into clear, logical steps",
                    "Show all work and intermediate calculations",
                    "Explain the reasoning behind each step",
                    "Verify the solution makes sense",
                    "Use clear mathematical or logical notation",
                    "Make the thought process transparent and teachable",
                ],
                style="systematic, clear, educational, thorough",
            ),
            directive_template=_build_directive("visible"),
            input_schema={
                "problem": str,
                "context_section": str,
                "domain": str,
            },
            constraints=Constraints(
                must_include=[
                    "verification of solution",
                    "explicit final answer",
                ],
                must_not_include=[
                    "unexplained leaps in logic",
                ],
                style_guide="Use numbered steps, show calculations, provide clear headings",
            ),
        )

    def _render_context_section(self, context):
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        problem: str = "",
        context: str | None = None,
        domain: str = "general",
        output_mode: str = "visible",
        proposed_answer: str | None = None,
        **kwargs,
    ):
        """
        Build context for step-by-step reasoning.

        Args:
            problem: The problem to solve
            context: Optional additional context
            domain: Problem domain ("mathematical", "logical", "scientific", "general")
            output_mode: ``"visible"`` (default) | ``"answer_focused"``
                | ``"check_only"``
            proposed_answer: Required when output_mode is ``"check_only"`` —
                the answer to verify
            **kwargs: Additional options

        Returns:
            Context object ready for export/use
        """
        if output_mode not in VALID_OUTPUT_MODES:
            raise ValueError(
                f"Invalid output_mode {output_mode!r}. Choose from: {sorted(VALID_OUTPUT_MODES)}"
            )
        if output_mode == "check_only" and not proposed_answer:
            raise ValueError("output_mode='check_only' requires a proposed_answer to verify.")

        from mycontext.core import Context
        from mycontext.utils.template_safety import safe_format_template

        context_section = self._render_context_section(context)
        directive_text = _build_directive(output_mode)

        fmt_kwargs: dict = {
            "problem": problem,
            "context_section": context_section,
            "domain": domain,
        }
        if output_mode == "check_only":
            fmt_kwargs["proposed_answer"] = proposed_answer or ""

        directive_content = safe_format_template(directive_text, **fmt_kwargs)

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=self.constraints,
            data=fmt_kwargs,
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["output_mode"] = output_mode
        self._apply_default_self_check(
            ctx,
            [
                "Does each step logically follow from the previous?",
                "Is any step a leap of logic that skips intermediate reasoning?",
            ],
        )
        if ctx.examples is None:
            ctx.examples = [
                {
                    "input": "If a store has 3-for-2 deals and I buy 7 items at $10 each, what do I pay?",
                    "output": (
                        "Step 1: Group items into sets of 3. 7 items = 2 full sets of 3 + 1 remaining item.\n"
                        "Step 2: Each set of 3, I pay for 2. Cost per set: 2 × $10 = $20.\n"
                        "Step 3: 2 sets × $20 = $40.\n"
                        "Step 4: The remaining 1 item is at full price: $10.\n"
                        "Step 5: Total = $40 + $10 = $50.\n"
                        "Verification: Without the deal, 7 × $10 = $70. Discount = $20 (2 free items). $70 − $20 = $50. ✓"
                    ),
                }
            ]
        return ctx

    def execute(
        self,
        provider: str = "gemini",
        problem: str = "",
        context: str | None = None,
        domain: str = "general",
        output_mode: str = "visible",
        proposed_answer: str | None = None,
        temperature: float = 0.3,
        **kwargs,
    ):
        """
        Execute step-by-step reasoning.

        Args:
            provider: LLM provider to use ("gemini", "openai", "anthropic")
            problem: The problem to solve
            context: Optional additional context
            domain: Problem domain ("mathematical", "logical", "scientific", "general")
            output_mode: ``"visible"`` (default) | ``"answer_focused"``
                | ``"check_only"``
            proposed_answer: Required when output_mode is ``"check_only"``
            temperature: Lower values (0.2–0.4) recommended for consistent reasoning
            **kwargs: Additional provider options

        Returns:
            ProviderResponse with the solution
        """
        provider_params = {
            "model",
            "max_tokens",
            "top_p",
            "frequency_penalty",
            "presence_penalty",
            "stop",
            "user",
            "api_key",
            "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        provider_kwargs["temperature"] = temperature

        ctx = self.build_context(
            problem=problem,
            context=context,
            domain=domain,
            output_mode=output_mode,
            proposed_answer=proposed_answer,
        )
        return ctx.execute(provider=provider, **provider_kwargs)
