"""
Step-by-Step Reasoner Template - Systematic problem solving with transparent reasoning.

Based on "step-by-step reasoning" cognitive tool and Chain-of-Thought methodology.
Free tier template - part of mycontext open source.
"""

from mycontext import Pattern, Guidance, Directive, Constraints


class StepByStepReasoner(Pattern):
    """
    Guide systematic problem-solving through clear, logical steps.
    
    This cognitive tool implements Chain-of-Thought reasoning,
    breaking down complex problems into manageable sequential steps
    with transparent reasoning at each stage.
    
    Based on:
    - "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., 2023)
    - IBM Zurich cognitive tools research (2025)
    
    Examples:
        >>> from mycontext.templates.free import StepByStepReasoner
        >>> 
        >>> reasoner = StepByStepReasoner()
        >>> result = reasoner.execute(
        ...     provider="gemini",
        ...     problem="If a train travels 120km in 2 hours, then speeds up to travel 200km in the next 2.5 hours, what is its average speed?"
        ... )
        >>> print(result.response)
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are an expert problem solver and educator. Solve the following problem "
        "using explicit, step-by-step reasoning:\n\n"
        "Problem: {problem}\n"
        "{context_section}\n"
        "Domain: {domain}\n\n"
        "Follow a structured problem-solving methodology: "
        "(1) UNDERSTAND — restate the problem in your own words, identify the problem "
        "type, and clarify what is being asked. "
        "(2) PLAN — outline your solution strategy and explain why this approach is "
        "appropriate. "
        "(3) EXECUTE — work through each step methodically, showing what you are doing, "
        "why, how, and the intermediate result at each stage. "
        "(4) VERIFY — check your answer against the original problem, apply an "
        "alternative verification method if possible. "
        "(5) CONCLUDE — state the final answer, assess your confidence level, and "
        "highlight key insights.\n\n"
        "Show all work. Explain the reasoning behind each step. Make your thought "
        "process transparent."
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
                    "Make the thought process transparent and teachable"
                ],
                style="systematic, clear, educational, thorough"
            ),
            directive_template="""Solve this problem by breaking it down into clear, logical steps.

**PROBLEM**:
{problem}

{context_section}

Follow this systematic process:

## Step 1: UNDERSTAND

**Restate the Problem**:
- In your own words: [Reformulate the problem]
- What we're looking for: [The unknown or goal]
- Key information given: [List all relevant facts, numbers, constraints]

**Identify the Type**:
- Problem category: [Mathematical, logical, analytical, etc.]
- Required operations: [What calculations or reasoning steps]

## Step 2: PLAN

**Strategy**:
- Overall approach: [How you'll solve this]
- Methods/techniques to use: [Specific formulas, algorithms, or reasoning patterns]
- Expected sub-steps: [Rough outline of the solution path]

**Sketch the Solution Path**:
```
[Input] → [Step A] → [Step B] → [Step C] → [Solution]
```

## Step 3: EXECUTE

Work through each step methodically. For each step, show:
- **What** you're doing
- **Why** you're doing it
- **How** you do it
- The **result**

### Step 3.1: [Description]
- **Action**: [What operation or reasoning]
- **Calculation/Logic**: 
  ```
  [Show your work in detail]
  = [intermediate result]
  ```
- **Result**: [What this step produces]
- **Verification**: [Quick check that this makes sense]

### Step 3.2: [Description]
[Same format]

### Step 3.3: [Description]
[Continue with as many steps as needed]

[Add more steps as required to reach the solution]

## Step 4: VERIFY

**Check Against Original Problem**:
- Does this answer what was asked? [Yes/No + explanation]
- Units correct? [If applicable]
- Scale reasonable? [Sanity check]

**Alternative Verification** (if possible):
- Different approach: [Try solving another way]
- Estimation check: [Does the answer roughly match expectations?]
- Edge cases: [Does the solution handle boundary conditions?]

## Step 5: CONCLUDE

**Final Answer**:
🎯 **[State the answer clearly and explicitly]**

**Answer with Context**:
- Complete statement: [Answer the question in a complete sentence]
- Units/Format: [With appropriate units or formatting]
- Precision: [To appropriate significant figures if applicable]

**Confidence Assessment**:
- Confidence level: [High / Medium / Low]
- Why: [Reasoning for confidence level]
- What could change this: [What assumptions or factors affect certainty]

**Key Insights** (if any):
- [Any interesting patterns or lessons from solving this]

---

**REQUIREMENTS**:
- Show ALL work - don't skip steps
- Explain WHY each step is necessary
- Use clear notation and formatting
- Verify the solution
- State the final answer explicitly""",
            input_schema={
                "problem": str,
                "context_section": str,
                "domain": str
            },
            constraints=Constraints(
                must_include=[
                    "clear step-by-step breakdown",
                    "show all work and calculations",
                    "verification of solution",
                    "explicit final answer"
                ],
                must_not_include=[
                    "skipped steps",
                    "unexplained leaps in logic"
                ],
                style_guide="Use numbered steps, show calculations, provide clear headings"
            )
        )
    
    def _render_context_section(self, context):
        """Render optional context section."""
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        problem="",
        context=None,
        domain="general",
        **kwargs
    ):
        """
        Build context for step-by-step reasoning (without executing).
        
        Args:
            problem: The problem to solve
            context: Optional additional context
            domain: Problem domain ("mathematical", "logical", "scientific", "general")
            **kwargs: Additional options
        
        Returns:
            Context object ready for export/use
        """
        # Provide defaults for optional fields
        if context is None:
            context = ""
        
        context_section = self._render_context_section(context)
        
        # Remove context_section from kwargs if present to avoid duplicate
        kwargs.pop('context_section', None)
        
        # Only pass template variables (not 'context', only 'context_section')
        return super().build_context(
            problem=problem,
            context_section=context_section,
            domain=domain,
            **kwargs
        )
    
    def execute(
        self,
        provider="gemini",
        problem="",
        context=None,
        domain="general",
        temperature=0.3,  # Lower temp for more consistent reasoning
        **kwargs
    ):
        """
        Execute step-by-step reasoning.
        
        Args:
            provider: LLM provider to use ("gemini", "openai", "anthropic")
            problem: The problem to solve
            context: Optional additional context
            domain: Problem domain ("mathematical", "logical", "scientific", "general")
            temperature: Lower values (0.2-0.4) recommended for consistent reasoning
            **kwargs: Additional provider options
        
        Returns:
            ProviderResponse with the step-by-step solution
        """
        # Provide defaults for optional fields
        if context is None:
            context = ""
        
        context_section = self._render_context_section(context)
        
        # Remove context_section from kwargs if present to avoid duplicate
        kwargs.pop('context_section', None)
        
        # Only pass template variables (not 'context', only 'context_section')
        return super().execute(
            provider=provider,
            problem=problem,
            context_section=context_section,
            domain=domain,
            temperature=temperature,
            **kwargs
        )
