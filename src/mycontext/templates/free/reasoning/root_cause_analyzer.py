"""
Root Cause Analysis Pattern - Identify underlying causes of problems

Systematic investigation to find true root causes, not just symptoms.
Based on systems thinking and quality management methodologies (5 Whys, Ishikawa).
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class RootCauseAnalyzer(Pattern):
    """
    Systematic root cause analysis for problem investigation.
    
    Uses multiple techniques:
    - 5 Whys method
    - Ishikawa (fishbone) analysis
    - Contributing factor identification
    - Verification and validation
    
    Based on: Quality management and systems thinking research
    
    Example:
        >>> analyzer = RootCauseAnalyzer()
        >>> context = analyzer.build_context(
        ...     problem="Website performance degraded by 50%",
        ...     context="Started after recent deployment"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are a root cause analysis specialist and systems thinker. "
        "Investigate the following problem to identify its true root cause:\n\n"
        "Problem: {problem}\n"
        "{context_section}\n"
        "Analysis depth: {depth}\n\n"
        "Apply a rigorous diagnostic methodology: "
        "(1) Define the problem precisely, separating symptoms from underlying causes. "
        "(2) Conduct a Five Whys analysis — ask 'why' iteratively to drill beneath "
        "surface-level explanations. "
        "(3) Perform an Ishikawa (fishbone) analysis examining causes across people, "
        "process, technology, environment, management, and materials. "
        "(4) Identify contributing factors and their interactions. "
        "(5) Verify each candidate cause with available evidence. "
        "(6) Assess systemic factors and feedback loops. "
        "(7) State the root cause clearly and explain the causal chain from root to "
        "symptoms. "
        "(8) Recommend specific prevention strategies and lessons learned.\n\n"
        "Distinguish symptoms from causes throughout. Be systematic and evidence-driven."
    )

    def __init__(self):
        super().__init__(
            name="root_cause_analyzer",
            description="Systematic root cause investigation",
            guidance=Guidance(
                role="Expert Root Cause Analysis Specialist and Systems Thinker",
                rules=[
                    "Distinguish symptoms from causes",
                    "Dig deep with systematic questioning",
                    "Consider multiple contributing factors",
                    "Use evidence, not speculation",
                    "Verify root causes with tests",
                    "Consider systemic and organizational factors"
                ],
                style="investigative, thorough, evidence-based"
            ),
            directive_template="""Conduct systematic root cause analysis:

**PROBLEM**: {problem}

{context_section}

**ANALYSIS DEPTH**: {depth}

Root cause investigation framework:

1. **PROBLEM DEFINITION**
   - Problem statement: [Clear, specific description]
   - Observable symptoms: [What we can see/measure]
   - Impact: [Severity and scope]
   - When started: [Timeline]
   - Who affected: [Stakeholders]

2. **SYMPTOM VS. CAUSE**
   Distinguish what's visible from what's underlying:
   
   Symptoms (Observable effects):
   - Symptom 1: [What we observe]
   - Symptom 2: [Another observable]
   
   Immediate causes (Surface-level):
   - Cause A: [Direct trigger]
   - Cause B: [Another trigger]
   
   We need to go deeper...

3. **FIVE WHYS ANALYSIS**
   Iterative questioning to reach root:
   
   Problem: {problem}
   
   Why? → [Answer 1]
   
   Why [Answer 1]? → [Answer 2]
   
   Why [Answer 2]? → [Answer 3]
   
   Why [Answer 3]? → [Answer 4]
   
   Why [Answer 4]? → [ROOT CAUSE]

4. **ISHIKAWA (FISHBONE) ANALYSIS**
   Examine categories of potential causes:
   
   **People**:
   - [Human factors]
   - [Skills, knowledge, behavior]
   
   **Process**:
   - [Procedural issues]
   - [Workflow problems]
   
   **Technology**:
   - [Technical failures]
   - [System issues]
   
   **Environment**:
   - [External factors]
   - [Contextual issues]
   
   **Materials/Data**:
   - [Input quality]
   - [Resource issues]
   
   **Management/Organization**:
   - [Structural issues]
   - [Decision-making problems]

5. **CONTRIBUTING FACTORS**
   Multiple factors that combine:
   
   Primary Root Cause: [Main underlying cause]
   - Evidence: [What supports this?]
   - Mechanism: [How does it cause the problem?]
   - Confidence: [High/Medium/Low]
   
   Secondary Factors: [Contributing causes]
   - Factor 1: [What it contributes]
   - Factor 2: [How it amplifies]
   
   Interactions: [How factors combine]

6. **CAUSE VERIFICATION**
   Test if identified causes are real:
   
   For each suspected root cause:
   - Hypothesis: [If this is the cause, then...]
   - Test: [How to verify]
   - Evidence: [What data supports/refutes?]
   - Confidence: [How certain are we?]

7. **SYSTEMIC ANALYSIS**
   Broader system issues:
   
   - System design flaws: [Structural issues]
   - Feedback loops: [Reinforcing problems]
   - Emergent issues: [From system complexity]
   - Hidden dependencies: [Unexpected connections]

8. **ROOT CAUSE STATEMENT**
   **Primary Root Cause**: [Clear, specific statement]
   
   **How It Causes the Problem**:
   [Detailed causal mechanism]
   
   **Why It Wasn't Obvious**:
   [What obscured the root cause]
   
   **Verification Method**:
   [How to confirm this is really the root]

9. **PREVENTION STRATEGY**
   How to prevent recurrence:
   
   - Short-term fix: [Address symptoms immediately]
   - Root cause fix: [Address underlying cause]
   - Preventive measures: [Stop it happening again]
   - Monitoring: [Early warning systems]
   - Continuous improvement: [Systemic changes]

10. **LESSONS LEARNED**
    **Key Insights**:
    - [What we learned about the system]
    - [What we learned about diagnosis]
    
    **Similar Problems**:
    - [Other areas with same root cause?]
    - [Broader implications?]

**OUTPUT FORMAT**: Systematic investigation with clear root cause identification.""",
            input_schema={
                "problem": str,
                "context_section": str,
                "depth": str
            },
            constraints=Constraints(
                must_include=[
                    "five_whys",
                    "root_cause_statement",
                    "verification_method"
                ],
                style_guide="Be thorough but focused, investigative but not speculative"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        """Render optional context section."""
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        problem: str = "",
        context: Optional[str] = None,
        depth: str = "thorough",
        **kwargs
    ):
        """
        Build context for root cause analysis.
        
        Args:
            problem: The problem to investigate
            context: Optional additional context
            depth: Analysis depth ("quick", "standard", "thorough")
            **kwargs: Additional options
        
        Returns:
            Context object ready for export/use
        """
        context_section = self._render_context_section(context)
        
        return super().build_context(
            problem=problem,
            context_section=context_section,
            depth=depth,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        problem: str = "",
        context: Optional[str] = None,
        depth: str = "thorough",
        **kwargs
    ):
        """
        Execute root cause analysis.
        
        Args:
            provider: LLM provider to use
            problem: The problem to investigate
            context: Optional additional context
            depth: Analysis depth
            **kwargs: Provider parameters
        
        Returns:
            ProviderResponse with the analysis
        """
        return super().execute(
            provider=provider,
            problem=problem,
            context=context,
            depth=depth,
            **kwargs
        )
