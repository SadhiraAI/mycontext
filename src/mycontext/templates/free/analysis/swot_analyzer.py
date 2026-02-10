"""
SWOT Analyzer - Systematic strengths, weaknesses, opportunities, threats analysis

Comprehensive SWOT analysis with actionable strategic insights.
Based on strategic management and business analysis frameworks.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class SWOTAnalyzer(Pattern):
    """
    Conduct comprehensive SWOT analysis.
    
    Analyzes:
    - Internal Strengths
    - Internal Weaknesses
    - External Opportunities
    - External Threats
    - Strategic implications
    
    Based on: Strategic management frameworks
    
    Example:
        >>> analyzer = SWOTAnalyzer()
        >>> context = analyzer.build_context(
        ...     subject="Our AI startup",
        ...     context="Entering B2B SaaS market"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """
    
    def __init__(self):
        super().__init__(
            name="swot_analyzer",
            description="Comprehensive SWOT analysis",
            guidance=Guidance(
                role="Expert Strategic Analyst and Business Consultant",
                rules=[
                    "Distinguish internal (SW) from external (OT) factors",
                    "Be honest about weaknesses",
                    "Identify actionable opportunities",
                    "Assess realistic threats",
                    "Provide strategic recommendations"
                ],
                style="analytical, balanced, strategic"
            ),
            directive_template="""Conduct SWOT analysis for:

**SUBJECT**: {subject}

{context_section}

Comprehensive SWOT analysis:

1. **STRENGTHS** (Internal Positive)
   What advantages do we have?
   
   - Strength 1: [Specific strength]
     - Evidence: [Why this is a strength]
     - Impact: [How it helps]
     
   - Strength 2: [Another strength]
     - Evidence: [Supporting data]
     - Impact: [Competitive advantage]
     
   - Strength 3: [Additional strength]
   - Strength 4: [More strengths]
   - Strength 5: [Continue...]
   
   **Key Differentiators**: [What makes us unique?]

2. **WEAKNESSES** (Internal Negative)
   What disadvantages do we face?
   
   - Weakness 1: [Specific weakness]
     - Impact: [How it hinders us]
     - Urgency: [High/Medium/Low]
     
   - Weakness 2: [Another weakness]
     - Impact: [Effect on performance]
     - Urgency: [Priority level]
     
   - Weakness 3: [Additional weakness]
   - Weakness 4: [More weaknesses]
   - Weakness 5: [Continue...]
   
   **Critical Gaps**: [Most significant limitations]

3. **OPPORTUNITIES** (External Positive)
   What favorable external factors exist?
   
   - Opportunity 1: [Market opportunity]
     - Potential: [Size/value of opportunity]
     - Timing: [Window of opportunity]
     - Fit: [How well it matches our strengths]
     
   - Opportunity 2: [Another opportunity]
     - Potential: [Expected benefit]
     - Timing: [When to pursue]
     - Fit: [Strategic alignment]
     
   - Opportunity 3: [Additional opportunity]
   - Opportunity 4: [More opportunities]
   - Opportunity 5: [Continue...]
   
   **Best Opportunities**: [Most promising to pursue]

4. **THREATS** (External Negative)
   What external challenges do we face?
   
   - Threat 1: [Competitive threat]
     - Severity: [High/Medium/Low]
     - Likelihood: [Probability]
     - Timeline: [When it could impact us]
     
   - Threat 2: [Market threat]
     - Severity: [Impact level]
     - Likelihood: [How likely]
     - Timeline: [Time horizon]
     
   - Threat 3: [Additional threat]
   - Threat 4: [More threats]
   - Threat 5: [Continue...]
   
   **Critical Threats**: [Most dangerous to address]

5. **SWOT MATRIX STRATEGIES**
   
   **SO Strategies** (Use Strengths to capture Opportunities):
   - Strategy 1: [Strength X + Opportunity Y]
   - Strategy 2: [Another SO combination]
   
   **ST Strategies** (Use Strengths to mitigate Threats):
   - Strategy 1: [Strength X to defend against Threat Y]
   - Strategy 2: [Another ST approach]
   
   **WO Strategies** (Overcome Weaknesses to pursue Opportunities):
   - Strategy 1: [Address Weakness X to capture Opportunity Y]
   - Strategy 2: [Another WO strategy]
   
   **WT Strategies** (Minimize Weaknesses and avoid Threats):
   - Strategy 1: [Address Weakness X and avoid Threat Y]
   - Strategy 2: [Another WT defensive strategy]

6. **PRIORITY ACTIONS**
   
   **Immediate (0-3 months)**:
   1. [Most urgent action]
   2. [Quick win opportunity]
   3. [Critical threat mitigation]
   
   **Short-term (3-6 months)**:
   1. [Important strength building]
   2. [Opportunity capture]
   3. [Weakness addressing]
   
   **Long-term (6-12 months)**:
   1. [Strategic positioning]
   2. [Capability building]
   3. [Market positioning]

7. **SUCCESS METRICS**
   How to measure progress:
   - Metric 1: [Measurement]
   - Metric 2: [KPI]
   - Metric 3: [Indicator]

8. **SWOT SUMMARY**
   **Strongest Assets**: [Key strengths to leverage]
   **Most Critical Gaps**: [Key weaknesses to address]
   **Best Opportunities**: [Focus areas]
   **Biggest Threats**: [Watch out for]
   
   **Overall Assessment**: [Strategic position]
   **Recommended Focus**: [Where to concentrate efforts]

**OUTPUT FORMAT**: Structured SWOT with strategic recommendations.""",
            input_schema={
                "subject": str,
                "context_section": str
            },
            constraints=Constraints(
                must_include=[
                    "all_four_swot_quadrants",
                    "strategic_recommendations",
                    "priority_actions"
                ],
                style_guide="Be balanced, honest, and strategic"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        subject: str = "",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            subject=subject,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        subject: str = "",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            subject=subject,
            context=context,
            **kwargs
        )
