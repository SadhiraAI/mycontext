"""
Hypothesis Generator - Generate testable hypotheses systematically

Creates well-formed hypotheses following scientific method.
Based on scientific reasoning and experimental design research.
"""

from mycontext.foundation import Constraints, Guidance
from mycontext.structure import Pattern


class HypothesisGenerator(Pattern):
    """
    Generate testable hypotheses systematically.
    
    Creates:
    - Well-formed hypotheses
    - Null and alternative hypotheses
    - Testable predictions
    - Experimental designs
    
    Based on: Scientific method and hypothesis formation research
    
    Example:
        >>> generator = HypothesisGenerator()
        >>> context = generator.build_context(
        ...     observation="Sales increase when we send email reminders",
        ...     domain="e-commerce"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are a scientific researcher and hypothesis specialist. Generate testable "
        "hypotheses from the following observation:\n\n"
        "Observation: {observation}\n"
        "Domain: {domain}\n"
        "{context_section}\n\n"
        "Apply rigorous scientific methodology: "
        "(1) Analyze the observation — what exactly has been observed, in what context, "
        "and with what frequency? "
        "(2) Identify relevant background knowledge and prior findings. "
        "(3) Generate hypotheses: formulate a primary hypothesis (H1), a null "
        "hypothesis (H0), and 2-3 alternative hypotheses — each must state a clear "
        "cause-effect relationship. "
        "(4) For each hypothesis, define testable predictions, identify independent "
        "and dependent variables plus potential confounds, and outline an experimental "
        "design to test it. "
        "(5) Define success criteria — what evidence would support or refute each? "
        "(6) Acknowledge limitations and assumptions. "
        "(7) Consider rival hypotheses and explain why they are less likely. "
        "(8) Recommend concrete next steps for investigation.\n\n"
        "All hypotheses must be testable and falsifiable."
    )

    def __init__(self):
        super().__init__(
            name="hypothesis_generator",
            description="Generate testable hypotheses systematically",
            guidance=Guidance(
                role="Expert Scientific Researcher and Hypothesis Specialist",
                rules=[
                    "Hypotheses must be testable and falsifiable",
                    "State clear cause-effect relationships",
                    "Include null and alternative hypotheses",
                    "Provide measurable predictions",
                    "Consider confounding variables"
                ],
                style="rigorous, scientific, precise"
            ),
            directive_template="""Generate testable hypotheses:

**OBSERVATION**: {observation}

{context_section}

**DOMAIN**: {domain}

Systematic hypothesis generation:

1. **OBSERVATION ANALYSIS**
   - Core observation: [What did we observe?]
   - Pattern: [What pattern or relationship?]
   - Context: [Under what conditions?]
   - Significance: [Why is this interesting?]

2. **BACKGROUND KNOWLEDGE**
   - Known theory: [What existing theory applies?]
   - Prior evidence: [What's already known?]
   - Mechanisms: [What could explain this?]
   - Gaps: [What's unknown?]

3. **HYPOTHESIS FORMULATION**
   
   **Primary Hypothesis (H1)**:
   - Statement: [Clear cause-effect statement]
   - Independent variable: [What we manipulate]
   - Dependent variable: [What we measure]
   - Relationship: [Expected relationship]
   - Mechanism: [Why would this happen?]
   
   **Null Hypothesis (H0)**:
   - Statement: [No effect statement]
   - Basis: [Default assumption]
   
   **Alternative Hypotheses** (if applicable):
   - H2: [Alternative explanation]
   - H3: [Another possibility]

4. **TESTABLE PREDICTIONS**
   If primary hypothesis is true:
   - Prediction 1: [Specific testable outcome]
   - Prediction 2: [Another testable outcome]
   - Prediction 3: [Additional prediction]
   
   If hypothesis is false:
   - What we'd observe instead: [Null result]

5. **VARIABLES & CONTROLS**
   
   Independent Variables:
   - [Variable 1]: [How to manipulate]
   - [Variable 2]: [Alternative manipulation]
   
   Dependent Variables:
   - [Variable 1]: [How to measure]
   - [Variable 2]: [Additional measures]
   
   Control Variables:
   - [Variable 1]: [What to hold constant]
   - [Variable 2]: [Another control]
   
   Confounding Variables:
   - [Variable 1]: [Potential confounder]
   - [Mitigation]: [How to address]

6. **EXPERIMENTAL DESIGN**
   
   Method:
   - Design type: [Experimental, observational, etc.]
   - Sample size: [Estimated needed]
   - Duration: [Time required]
   - Procedure: [High-level steps]
   
   Conditions:
   - Treatment group: [What they receive]
   - Control group: [Comparison group]
   - Randomization: [How to assign]
   
   Measurements:
   - Primary outcome: [Key metric]
   - Secondary outcomes: [Additional metrics]
   - Timing: [When to measure]

7. **SUCCESS CRITERIA**
   
   Support for hypothesis:
   - Statistical: [p < 0.05, effect size, etc.]
   - Practical: [Meaningful difference]
   - Consistency: [Across conditions]
   
   Reject hypothesis if:
   - [Specific conditions]
   - [Statistical criteria]

8. **LIMITATIONS & ASSUMPTIONS**
   
   Assumptions:
   - [Assumption 1]
   - [Assumption 2]
   
   Limitations:
   - [Limitation 1]
   - [Limitation 2]
   
   Boundary conditions:
   - [When hypothesis may not apply]

9. **RIVAL HYPOTHESES**
   Consider alternative explanations:
   
   Rival Hypothesis A:
   - Statement: [Alternative explanation]
   - How to test against: [Distinguish from H1]
   
   Rival Hypothesis B:
   - Statement: [Another alternative]
   - How to test against: [How to rule out]

10. **NEXT STEPS**
    - Immediate: [First action]
    - Short-term: [Early tests]
    - Long-term: [Comprehensive study]
    - Resources needed: [What's required]

**OUTPUT FORMAT**: Scientific, rigorous hypothesis with clear testing plan.""",
            input_schema={
                "observation": str,
                "context_section": str,
                "domain": str
            },
            constraints=Constraints(
                must_include=[
                    "testable_hypothesis",
                    "null_hypothesis",
                    "predictions",
                    "experimental_design"
                ],
                style_guide="Be scientific but accessible, rigorous but practical"
            )
        )

    def _render_context_section(self, context: str | None) -> str:
        """Render optional context section."""
        if context:
            return f"\n**ADDITIONAL CONTEXT**: {context}\n"
        return ""

    def build_context(
        self,
        observation: str = "",
        domain: str = "general",
        context: str | None = None,
        **kwargs
    ):
        """
        Build context for hypothesis generation.
        
        Args:
            observation: The observation to explain
            domain: Domain context
            context: Optional additional context
            **kwargs: Additional options
        
        Returns:
            Context object ready for export/use
        """
        context_section = self._render_context_section(context)

        return super().build_context(
            observation=observation,
            domain=domain,
            context_section=context_section,
            **kwargs
        )

    def execute(
        self,
        provider: str = "openai",
        observation: str = "",
        domain: str = "general",
        context: str | None = None,
        **kwargs
    ):
        """
        Execute hypothesis generation.
        
        Args:
            provider: LLM provider to use
            observation: The observation to explain
            domain: Domain context
            context: Optional additional context
            **kwargs: Provider parameters
        
        Returns:
            ProviderResponse with hypotheses
        """
        return super().execute(
            provider=provider,
            observation=observation,
            domain=domain,
            context=context,
            **kwargs
        )
