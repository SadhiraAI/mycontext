"""
Scenario Planner - Create and analyze multiple future scenarios

Systematic scenario planning for strategic decision-making.
Based on scenario planning methodologies and futures thinking.
"""

from typing import Optional
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive, Constraints


class ScenarioPlanner(Pattern):
    """
    Create and analyze multiple future scenarios.
    
    Develops:
    - Plausible future scenarios
    - Key uncertainties and drivers
    - Strategic implications
    - Response strategies
    
    Based on: Scenario planning and strategic foresight
    
    Example:
        >>> planner = ScenarioPlanner()
        >>> context = planner.build_context(
        ...     topic="Future of remote work in next 5 years",
        ...     timeframe="2026-2031"
        ... )
    
    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "You are a strategic foresight analyst and scenario planner. Develop multiple "
        "future scenarios for the following:\n\n"
        "Topic: {topic}\n"
        "Timeframe: {timeframe}\n"
        "{context_section}\n\n"
        "Apply structured scenario methodology: "
        "(1) Assess the current state — key trends, forces, and baseline trajectory. "
        "(2) Identify the two most critical uncertainties as scenario axes. "
        "(3) Construct four distinct scenarios from the 2x2 matrix — give each a "
        "memorable name and describe its characteristics, driving forces, probability, "
        "and early indicators. "
        "(4) For each scenario, analyze opportunities, threats, and capabilities needed. "
        "(5) Identify robust strategies that perform well across most scenarios "
        "(no-regret moves). "
        "(6) Define scenario-specific strategies for high-impact scenarios. "
        "(7) Establish signposts — concrete, observable events that signal which "
        "scenario is unfolding. "
        "(8) Recommend a preparedness plan with immediate actions, monitoring "
        "framework, and contingency triggers.\n\n"
        "Create diverse, plausible scenarios — not just optimistic and pessimistic."
    )

    def __init__(self):
        super().__init__(
            name="scenario_planner",
            description="Create and analyze future scenarios",
            guidance=Guidance(
                role="Expert Strategic Foresight Analyst and Scenario Planner",
                rules=[
                    "Create diverse, plausible scenarios",
                    "Identify critical uncertainties",
                    "Explore implications thoroughly",
                    "Avoid single-point predictions",
                    "Focus on preparedness, not prediction"
                ],
                style="forward-thinking, comprehensive, strategic"
            ),
            directive_template="""Develop scenario analysis for:

**TOPIC**: {topic}

{context_section}

**TIMEFRAME**: {timeframe}

Comprehensive scenario planning:

1. **CURRENT STATE ASSESSMENT**
   - Present situation: [Where we are now]
   - Key trends: [What's happening]
   - Momentum: [Direction of change]

2. **CRITICAL UNCERTAINTIES**
   Identify 2 key uncertainties that will shape the future:
   
   **Uncertainty Axis 1**: [e.g., Technology adoption]
   - Dimension: [What varies]
   - Range: [Low to High]
   - Impact: [Why it matters]
   
   **Uncertainty Axis 2**: [e.g., Regulation]
   - Dimension: [What varies]
   - Range: [Low to High]
   - Impact: [Why it matters]

3. **FOUR SCENARIOS** (2x2 Matrix)
   
   **Scenario A**: [Name] (High Axis1, High Axis2)
   - Description: [What this world looks like]
   - Key characteristics:
     - [Characteristic 1]
     - [Characteristic 2]
     - [Characteristic 3]
   - Driving forces: [What leads to this]
   - Probability: [X%]
   - Indicators: [Early warning signs]
   
   **Scenario B**: [Name] (High Axis1, Low Axis2)
   - Description: [What this world looks like]
   - Key characteristics:
     - [Characteristic 1]
     - [Characteristic 2]
     - [Characteristic 3]
   - Driving forces: [What leads to this]
   - Probability: [X%]
   - Indicators: [Early warning signs]
   
   **Scenario C**: [Name] (Low Axis1, High Axis2)
   - Description: [What this world looks like]
   - Key characteristics:
     - [Characteristic 1]
     - [Characteristic 2]
     - [Characteristic 3]
   - Driving forces: [What leads to this]
   - Probability: [X%]
   - Indicators: [Early warning signs]
   
   **Scenario D**: [Name] (Low Axis1, Low Axis2)
   - Description: [What this world looks like]
   - Key characteristics:
     - [Characteristic 1]
     - [Characteristic 2]
     - [Characteristic 3]
   - Driving forces: [What leads to this]
   - Probability: [X%]
   - Indicators: [Early warning signs]

4. **IMPLICATIONS ANALYSIS**
   For each scenario:
   
   **Scenario A Implications**:
   - Opportunities: [What becomes possible]
   - Threats: [What challenges arise]
   - Required capabilities: [What we'd need]
   
   **Scenario B Implications**:
   - Opportunities: [Benefits in this world]
   - Threats: [Risks in this world]
   - Required capabilities: [What we'd need]
   
   [Continue for C and D]

5. **ROBUST STRATEGIES**
   Strategies that work across multiple scenarios:
   
   - No-regret moves: [Good in any scenario]
   - Hedging strategies: [Reduce downside risk]
   - Shaping actions: [Influence which scenario emerges]
   - Adaptive strategies: [Flexible to pivot]

6. **SCENARIO-SPECIFIC STRATEGIES**
   
   **If Scenario A emerges**:
   - Strategy: [Optimal approach]
   - Timing: [When to execute]
   
   **If Scenario B emerges**:
   - Strategy: [Best response]
   - Timing: [When to execute]
   
   [Continue for C and D]

7. **SIGNPOSTS & TRIGGERS**
   Early warning indicators to monitor:
   
   - Signpost 1: [Indicator]
     - What it signals: [Which scenario]
     - When to check: [Frequency]
   
   - Signpost 2: [Indicator]
     - What it signals: [Direction]
     - When to check: [Timeline]
   
   **Trigger Events**: [Events that would require strategy pivot]

8. **PREPAREDNESS PLAN**
   
   **Immediate Actions** (Now):
   - [Build capabilities that help in all scenarios]
   - [Reduce vulnerabilities]
   - [Gather intelligence]
   
   **Monitoring Plan**:
   - What to track: [Key indicators]
   - How often: [Frequency]
   - Review cycle: [When to reassess]
   
   **Contingency Plans**:
   - If Scenario A: [Rapid response plan]
   - If Scenario B: [Adaptation strategy]
   - If surprise: [General contingency]

9. **SCENARIO COMPARISON**
   
   | Dimension | Scenario A | Scenario B | Scenario C | Scenario D |
   |-----------|------------|------------|------------|------------|
   | Best for us | [Rating] | [Rating] | [Rating] | [Rating] |
   | Likelihood | [%] | [%] | [%] | [%] |
   | Impact | [H/M/L] | [H/M/L] | [H/M/L] | [H/M/L] |

10. **STRATEGIC RECOMMENDATIONS**
    **Most likely scenario**: [Which one]
    **Preferred scenario**: [Which we want]
    **How to shape future**: [Actions to influence]
    **Key investments**: [Where to focus resources]
    **Risk mitigation**: [How to hedge]

**OUTPUT FORMAT**: Comprehensive scenario analysis with strategic guidance.""",
            input_schema={
                "topic": str,
                "context_section": str,
                "timeframe": str
            },
            constraints=Constraints(
                must_include=[
                    "four_scenarios",
                    "implications",
                    "robust_strategies"
                ],
                style_guide="Be exploratory but practical, imaginative but grounded"
            )
        )
    
    def _render_context_section(self, context: Optional[str]) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""
    
    def build_context(
        self,
        topic: str = "",
        timeframe: str = "5 years",
        context: Optional[str] = None,
        **kwargs
    ):
        context_section = self._render_context_section(context)
        
        return super().build_context(
            topic=topic,
            timeframe=timeframe,
            context_section=context_section,
            **kwargs
        )
    
    def execute(
        self,
        provider: str = "openai",
        topic: str = "",
        timeframe: str = "5 years",
        context: Optional[str] = None,
        **kwargs
    ):
        return super().execute(
            provider=provider,
            topic=topic,
            timeframe=timeframe,
            context=context,
            **kwargs
        )
