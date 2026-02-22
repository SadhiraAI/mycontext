"""
Decision Framework Pattern (Enterprise) - Systematic decision-making structure

Provides a comprehensive framework for making well-reasoned decisions.
Based on decision science and rational choice theory.

License: Enterprise
"""


from mycontext import Constraints, Guidance, Pattern


class DecisionFramework(Pattern):
    """
    Structured framework for systematic decision-making.
    
    Provides comprehensive decision analysis:
    - Problem definition
    - Option generation
    - Criteria establishment
    - Evaluation
    - Recommendation
    
    Based on: Decision science and multi-criteria decision analysis
    
    Example:
        >>> framework = DecisionFramework()
        >>> context = framework.build_context(
        ...     decision="Choose cloud provider for our app",
        ...     options=["AWS", "Google Cloud", "Azure"]
        ... )
    
    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert decision scientist. Apply a structured decision-making framework "
        "to analyze the given decision systematically.\n\n"
        "Decision: {decision}\n"
        "{context_section}\n"
        "Options: {options}\n"
        "Depth: {depth}\n\n"
        "Deliver your analysis:\n"
        "(1) Define the decision clearly — triggers, stakeholders, constraints, success criteria.\n"
        "(2) Generate and evaluate all viable options including creative alternatives.\n"
        "(3) Establish weighted decision criteria (must-have vs. nice-to-have).\n"
        "(4) Score each option against criteria in an evaluation matrix.\n"
        "(5) Assess risks and reversibility for top options.\n"
        "(6) Provide a primary recommendation with confidence level and implementation guidance.\n\n"
        "Be thorough, balanced, and decisive. Support recommendations with evidence.\n\n"
        "Note: For deeper analysis with specialized enterprise frameworks, upgrade to mycontext Enterprise."
    )

    def __init__(self):
        super().__init__(
            name="decision_framework",
            version="1.0.0",
            tags=["decision", "enterprise", "strategic", "analysis"],
            metadata={"category": "decision", "license": "enterprise", "tier": "enterprise"},
            description="Systematic decision-making framework",
            guidance=Guidance(
                role="Expert Decision Analyst and Strategic Advisor",
                rules=[
                    "Define decision clearly before analyzing",
                    "Generate comprehensive option set",
                    "Establish explicit criteria",
                    "Evaluate objectively with evidence",
                    "Consider short and long-term implications",
                    "Acknowledge uncertainty and risks",
                    "Provide actionable recommendations"
                ],
                style="analytical, balanced, decisive"
            ),
            directive_template="""Apply systematic decision framework:

**DECISION**: {decision}

{context_section}

{options_section}

**ANALYSIS DEPTH**: {depth}

Systematic decision analysis:

1. **DECISION DEFINITION**
   - Core decision: [State clearly]
   - Why now?: [What triggers this decision?]
   - Stakeholders: [Who's affected?]
   - Constraints: [What limits choices?]
   - Success definition: [What does good outcome look like?]

2. **OPTION GENERATION**
   List all viable options:
   
   {provided_options}
   
   Additional Options to Consider:
   - [Any missing alternatives?]
   - [Creative solutions?]
   - [Hybrid approaches?]
   - [Do-nothing option?]

3. **CRITERIA ESTABLISHMENT**
   Decision criteria (what matters):
   
   Must-Have Criteria (Deal-breakers):
   - [Criterion 1]: [Why essential?]
   - [Criterion 2]: [Why essential?]
   
   Important Criteria (High weight):
   - [Criterion A]: [Why important?] [Weight: X/10]
   - [Criterion B]: [Why important?] [Weight: Y/10]
   
   Nice-to-Have Criteria (Lower weight):
   - [Criterion X]: [Why beneficial?] [Weight: Z/10]

4. **DETAILED EVALUATION**
   For each option against each criterion:
   
   | Option | Must-Have 1 | Must-Have 2 | Important A | Important B | Nice X |
   |--------|-------------|-------------|-------------|-------------|--------|
   | Opt 1  | ✓/✗         | ✓/✗         | 8/10        | 6/10        | 7/10   |
   | Opt 2  | ✓/✗         | ✓/✗         | 7/10        | 9/10        | 5/10   |
   
   For each rating, provide brief justification.

5. **COMPARATIVE ANALYSIS**
   Strengths and Weaknesses:
   
   Option 1:
   - Strengths: [What it does best]
   - Weaknesses: [Where it falls short]
   - Best for: [What scenarios]
   
   [Continue for all options]

6. **SCENARIO ANALYSIS**
   Best choice under different scenarios:
   
   If [Criterion A] is most important: Choose [Option X]
   - Reasoning: [Why this choice]
   
   If [Criterion B] is most important: Choose [Option Y]
   - Reasoning: [Why this choice]
   
   Balanced scenario: Choose [Option Z]
   - Reasoning: [Why this is balanced]

7. **RISK ASSESSMENT**
   For top 2-3 options:
   
   Option [Name]:
   - Implementation risk: [High/Med/Low]
   - Reversibility: [Can we undo this?]
   - Downside: [Worst case scenario]
   - Mitigation: [How to reduce risk]

8. **DECISION RECOMMENDATION**
   **Primary Recommendation**: [Option X]
   
   **Reasoning**:
   - [Key factor 1]
   - [Key factor 2]
   - [Key factor 3]
   
   **Confidence Level**: [High/Medium/Low] based on [reasoning]
   
   **Alternative Recommendation**: [Option Y]
   - When to consider: [Conditions]
   - Trade-offs: [What you give up/gain]
   
   **Decision Dependencies**:
   - Information needed: [What else do we need to know?]
   - Timing: [When should this be decided?]
   - Reversibility: [Can we change later?]

9. **IMPLEMENTATION GUIDANCE**
   If you choose [Primary Recommendation]:
   - Next steps: [What to do immediately]
   - Success metrics: [How to measure]
   - Review points: [When to reassess]
   - Exit criteria: [When to pivot]

10. **FINAL SUMMARY**
    **Decision**: [Restate the decision]
    **Recommendation**: [Clear, actionable recommendation]
    **Confidence**: [Level and why]
    **Key Success Factors**: [What needs to go right]
    **Red Flags**: [Warning signs to watch for]

**OUTPUT FORMAT**: Structured decision analysis with clear recommendation.""",
            input_schema={
                "decision": str,
                "context_section": str,
                "options_section": str,
                "provided_options": str,
                "depth": str
            },
            constraints=Constraints(
                must_include=[
                    "criteria",
                    "evaluation_matrix",
                    "recommendation",
                    "implementation_guidance"
                ],
                style_guide="Be thorough but decisive, balanced but opinionated when evidence supports it"
            )
        )

    def _render_context_section(self, context: str | None) -> str:
        """Render optional context section."""
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    def _render_options_section(self, options: list[str] | None) -> str:
        """Render options section."""
        if options:
            formatted = "**OPTIONS UNDER CONSIDERATION**:\n"
            for i, opt in enumerate(options, 1):
                formatted += f"{i}. {opt}\n"
            return formatted
        return "**OPTIONS**: To be identified during analysis\n"

    def _format_provided_options(self, options: list[str] | None) -> str:
        """Format provided options for template."""
        if options:
            return "\n".join(f"- {opt}" for opt in options)
        return "- To be identified"

    def build_context(
        self,
        decision: str = "",
        context: str | None = None,
        options: list[str] | None = None,
        depth: str = "comprehensive",
        **kwargs
    ):
        """
        Build context for decision framework.
        
        Args:
            decision: The decision to be made
            context: Optional additional context
            options: Optional list of options to consider
            depth: Analysis depth ("quick", "standard", "comprehensive")
            **kwargs: Additional options
        
        Returns:
            Context object ready for export/use
        """
        context_section = self._render_context_section(context)
        options_section = self._render_options_section(options)
        provided_options = self._format_provided_options(options)

        return super().build_context(
            decision=decision,
            context_section=context_section,
            options_section=options_section,
            provided_options=provided_options,
            depth=depth,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        decision: str = "",
        context: str | None = None,
        options: list[str] | None = None,
        depth: str = "comprehensive",
        **kwargs
    ):
        """
        Execute decision framework analysis.
        
        Args:
            provider: LLM provider to use
            decision: The decision to be made
            context: Optional additional context
            options: Optional list of options to consider
            depth: Analysis depth
            **kwargs: Provider parameters
        
        Returns:
            ProviderResponse with the analysis
        """
        return super().execute(
            provider=provider,
            decision=decision,
            context=context,
            options=options,
            depth=depth,
            **kwargs
        )
