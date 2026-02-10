"""
Data Analyzer - Systematic data analysis and insight extraction

Comprehensive data analysis with pattern detection and insights.
Based on data science and analytical reasoning frameworks.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class DataAnalyzer(Pattern):
    """
    Analyze data systematically and extract insights.
    
    Provides:
    - Descriptive statistics
    - Pattern detection
    - Trend analysis
    - Actionable insights
    
    Based on: Data analysis methodologies
    
    Example:
        >>> analyzer = DataAnalyzer()
        >>> context = analyzer.build_context(
        ...     data_description="Monthly sales data for past year",
        ...     goal="Identify growth opportunities"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """
    
    def __init__(self):
        super().__init__(
            name="data_analyzer",
            description="Systematic data analysis",
            guidance=Guidance(
                role="Expert Data Analyst and Insights Specialist",
                rules=[
                    "Start with descriptive understanding",
                    "Look for patterns and anomalies",
                    "Distinguish correlation from causation",
                    "Provide actionable insights",
                    "Acknowledge data limitations"
                ],
                style="analytical, evidence-based, clear"
            ),
            directive_template="""Analyze this data:

**DATA**: {data_description}

{context_section}

**ANALYSIS GOAL**: {goal}

Systematic data analysis:

1. **DATA OVERVIEW**
   - Data type: [What kind of data]
   - Time period: [Coverage]
   - Sample size: [How much data]
   - Variables: [What's measured]
   - Quality: [Completeness, accuracy]

2. **DESCRIPTIVE STATISTICS**
   Summary statistics:
   - Central tendency: [Mean, median, mode]
   - Dispersion: [Range, variance, std dev]
   - Distribution: [Shape, skewness]
   - Key figures: [Notable numbers]

3. **PATTERN DETECTION**
   
   **Trends**:
   - Trend 1: [Upward/downward/stable]
     - Evidence: [What shows this]
     - Magnitude: [How strong]
     - Timeframe: [Since when]
   
   **Seasonality**:
   - Pattern: [Recurring cycles]
   - Frequency: [How often repeats]
   - Amplitude: [How much variation]
   
   **Clusters**:
   - Group 1: [Similar data points]
   - Group 2: [Another cluster]
   - Characteristics: [What defines each]

4. **ANOMALY DETECTION**
   Outliers and unusual patterns:
   
   - Anomaly 1: [What's unusual]
     - Context: [When/where]
     - Severity: [How far from normal]
     - Possible cause: [Why it might occur]
   
   - Anomaly 2: [Another outlier]
     - [Same structure]

5. **CORRELATION ANALYSIS**
   Relationships between variables:
   
   - Correlation 1: [X relates to Y]
     - Strength: [Strong/moderate/weak]
     - Direction: [Positive/negative]
     - Note: [Correlation ≠ causation]
   
   - Correlation 2: [Another relationship]

6. **COMPARATIVE ANALYSIS**
   How do segments compare?
   
   | Segment | Metric A | Metric B | Insight |
   |---------|----------|----------|---------|
   | Seg 1 | [Value] | [Value] | [Finding] |
   | Seg 2 | [Value] | [Value] | [Finding] |
   
   Key differences:
   - [Segment X outperforms on Y]
   - [Segment A lags in B]

7. **KEY INSIGHTS**
   
   **Insight #1**: [Major finding]
   - Evidence: [What supports this]
   - Confidence: [High/Medium/Low]
   - Significance: [Why it matters]
   - Action: [What to do about it]
   
   **Insight #2**: [Another finding]
   - Evidence: [Supporting data]
   - Confidence: [Level]
   - Significance: [Impact]
   - Action: [Recommended response]
   
   **Insight #3**: [Third finding]
   - [Same structure]

8. **HYPOTHESES**
   Possible explanations:
   
   - Hypothesis 1: [Explanation for pattern]
     - Supporting evidence: [What fits]
     - Contradicting evidence: [What doesn't]
     - Test: [How to verify]
   
   - Hypothesis 2: [Alternative explanation]

9. **DATA LIMITATIONS**
   What to be cautious about:
   - Limitation 1: [Data gap or issue]
   - Limitation 2: [Bias or constraint]
   - Limitation 3: [Missing information]
   
   Confidence caveats:
   - [What we can't conclude from this data]

10. **RECOMMENDATIONS**
    Based on analysis:
    
    **Immediate Actions**:
    1. [Action based on insight 1]
    2. [Action based on insight 2]
    
    **Further Investigation**:
    - [What additional data needed]
    - [What analysis to run next]
    
    **Success Metrics**:
    - [How to measure if actions work]

11. **VISUALIZATION SUGGESTIONS**
    Best ways to present findings:
    - Chart 1: [Type] for [Data]
    - Chart 2: [Type] for [Pattern]
    - Dashboard: [Key metrics to track]

**OUTPUT FORMAT**: Clear, evidence-based analysis with actionable insights.""",
            input_schema={
                "data_description": str,
                "context_section": str,
                "goal": str
            },
            constraints=Constraints(
                must_include=[
                    "patterns",
                    "insights",
                    "recommendations"
                ],
                style_guide="Be analytical but accessible, rigorous but clear"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        data_description: str = "",
        goal: str = "Extract insights",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            data_description=data_description,
            goal=goal,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        data_description: str = "",
        goal: str = "Extract insights",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            data_description=data_description,
            goal=goal,
            context=context,
            **kwargs
        )
