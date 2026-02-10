"""
Trend Identifier - Detect and analyze trends in data or phenomena

Systematic trend detection, analysis, and forecasting.
Based on time series analysis and pattern recognition research.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class TrendIdentifier(Pattern):
    """
    Identify and analyze trends systematically.
    
    Detects:
    - Directional trends (up/down/stable)
    - Cyclical patterns
    - Emerging trends
    - Trend strength and sustainability
    
    Based on: Time series analysis and trend detection
    
    Example:
        >>> identifier = TrendIdentifier()
        >>> context = identifier.build_context(
        ...     data_description="Monthly user engagement over 2 years",
        ...     domain="product analytics"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """
    
    def __init__(self):
        super().__init__(
            name="trend_identifier",
            description="Detect and analyze trends",
            guidance=Guidance(
                role="Expert Trend Analyst and Pattern Recognition Specialist",
                rules=[
                    "Distinguish signal from noise",
                    "Quantify trend strength",
                    "Identify inflection points",
                    "Project trends cautiously",
                    "Consider external factors"
                ],
                style="analytical, data-driven, cautious"
            ),
            directive_template="""Identify trends in:

**DATA/PHENOMENON**: {data_description}

{context_section}

**DOMAIN**: {domain}

**TIME PERIOD**: {timeframe}

Comprehensive trend analysis:

1. **DATA OVERVIEW**
   - Subject: [What's being measured]
   - Timespan: [Duration]
   - Frequency: [How often measured]
   - Baseline: [Starting point]
   - Current state: [Where we are now]

2. **PRIMARY TREND DETECTION**
   
   **Overall Direction**:
   - Trend: [Upward/Downward/Stable/Volatile]
   - Magnitude: [How strong]
   - Consistency: [How steady]
   - Duration: [How long]
   
   **Trend Characterization**:
   - Linear: [Steady rate of change]
   - Exponential: [Accelerating growth/decline]
   - S-curve: [Initial slow, rapid middle, plateau]
   - Logarithmic: [Rapid then slowing]

3. **TREND QUANTIFICATION**
   
   - Rate of change: [X% per period]
   - Acceleration: [Speeding up/slowing down]
   - Volatility: [How much fluctuation]
   - R-squared: [Trend fit quality, if applicable]
   
   **Key Metrics**:
   - Start value: [Beginning]
   - End value: [Current]
   - Total change: [Difference]
   - Percent change: [Percentage]
   - CAGR: [Compound annual growth rate]

4. **INFLECTION POINTS**
   Critical changes in direction:
   
   - Point 1: [Time/date]
     - What happened: [Change description]
     - Trigger: [Likely cause]
     - Impact: [Effect on trend]
   
   - Point 2: [Another inflection]
     - [Same structure]

5. **CYCLICAL PATTERNS**
   Recurring patterns:
   
   - Cycle detected: [Yes/No]
   - Period: [Length of cycle]
   - Amplitude: [Peak to trough]
   - Seasonality: [Time-based patterns]
   
   Examples:
   - [Pattern 1]: Peaks every [period]
   - [Pattern 2]: Dips during [time]

6. **TREND DECOMPOSITION**
   
   **Long-term trend**: [Overall direction]
   **Seasonal component**: [Recurring patterns]
   **Cyclical component**: [Business cycles]
   **Random noise**: [Unexplained variation]

7. **SUPPORTING TRENDS**
   Related trends that reinforce:
   
   - Trend A: [Related metric]
     - Correlation: [How related]
     - Significance: [Why it matters]
   
   - Trend B: [Another metric]
     - [Same structure]

8. **COUNTER TRENDS**
   Opposing forces or trends:
   
   - Counter-trend 1: [What opposes]
     - Strength: [How strong]
     - Impact: [Effect on main trend]
   
   - Counter-trend 2: [Another opposition]

9. **EMERGING TRENDS**
   New patterns just appearing:
   
   - Emerging 1: [New pattern]
     - Evidence: [Early signals]
     - Strength: [Nascent/Building/Strong]
     - Potential: [Could become major]
   
   - Emerging 2: [Another new trend]

10. **CAUSAL FACTORS**
    What's driving the trend?
    
    **Primary Drivers**:
    - Factor 1: [Main cause]
      - Evidence: [Why we think this]
      - Impact: [How much influence]
    
    - Factor 2: [Another driver]
    
    **External Factors**:
    - Market conditions: [Effect]
    - Technology changes: [Impact]
    - Regulatory changes: [Influence]
    - Competitive dynamics: [Role]

11. **TREND SUSTAINABILITY**
    Will this continue?
    
    **Sustainability Assessment**: [High/Medium/Low]
    
    **Factors supporting continuation**:
    - [Reason 1]
    - [Reason 2]
    
    **Factors that could reverse trend**:
    - [Risk 1]
    - [Risk 2]
    
    **Expected trajectory**: [Forecast]

12. **FUTURE PROJECTION**
    If current trend continues:
    
    **Short-term (3-6 months)**:
    - Projection: [Expected value]
    - Confidence: [High/Med/Low]
    - Range: [Min to Max]
    
    **Medium-term (6-12 months)**:
    - Projection: [Expected value]
    - Confidence: [Decreases over time]
    - Range: [Wider uncertainty]
    
    **Scenarios**:
    - Bull case: [Optimistic projection]
    - Base case: [Most likely]
    - Bear case: [Pessimistic projection]

13. **LEADING INDICATORS**
    Early warning signals to monitor:
    
    - Indicator 1: [What to watch]
      - Why it leads: [Predictive value]
      - Where to track: [Source]
    
    - Indicator 2: [Another signal]

14. **ACTIONABLE INSIGHTS**
    What to do about these trends:
    
    **If trend continues**:
    - Action 1: [Response]
    - Action 2: [Strategy]
    
    **If trend reverses**:
    - Contingency 1: [Backup plan]
    - Contingency 2: [Alternative]
    
    **Opportunities**:
    - [How to capitalize on trend]
    
    **Risks**:
    - [How to hedge against trend]

**OUTPUT FORMAT**: Data-driven trend analysis with projections and recommendations.""",
            input_schema={
                "data_description": str,
                "context_section": str,
                "domain": str,
                "timeframe": str
            },
            constraints=Constraints(
                must_include=[
                    "trend_direction",
                    "quantification",
                    "drivers",
                    "projection"
                ],
                style_guide="Be analytical but not overconfident in projections"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        data_description: str = "",
        domain: str = "general",
        timeframe: str = "past year",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            data_description=data_description,
            domain=domain,
            timeframe=timeframe,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        data_description: str = "",
        domain: str = "general",
        timeframe: str = "past year",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            data_description=data_description,
            domain=domain,
            timeframe=timeframe,
            context=context,
            **kwargs
        )
