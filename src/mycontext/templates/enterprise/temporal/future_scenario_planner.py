"""
FutureScenarioPlanner Pattern (Enterprise)

Multi-horizon scenario planning for strategic decision-making.
Implements Shell's scenario planning methodology and futures thinking.

Research Foundation:
- Schoemaker, P. J. (1995). Scenario planning: A tool for strategic thinking.
- Schwartz, P. (1996). The art of the long view: Planning for the future in an uncertain world.
- van der Heijden, K. (2005). Scenarios: The art of strategic conversation.

License: Enterprise
"""

from mycontext import Constraints, Guidance, Pattern


class FutureScenarioPlanner(Pattern):
    """
    Create multiple future scenarios for strategic planning.

    Scenario Planning Process:
    1. Identify focal question
    2. Determine key forces and uncertainties
    3. Develop scenario logics
    4. Flesh out scenarios
    5. Identify implications and strategies

    Use Cases:
    - Strategic planning
    - Risk management
    - Long-term forecasting
    - Contingency planning

    Example:
        >>> from mycontext.templates.enterprise.temporal import FutureScenarioPlanner
        >>>
        >>> pattern = FutureScenarioPlanner()
        >>> result = pattern.execute(
        ...     provider="openai",
        ...     focal_question="How will AI transform our industry?\",
        ...     time_horizon=\"10 years\"
        ... )

    Enterprise Template - Requires Enterprise license.
    """

    GENERIC_PROMPT = (
        "You are an expert strategic futurist specializing in scenario planning. "
        "Develop multiple plausible future scenarios to inform strategic decisions.\n\n"
        "Focal Question: {focal_question}\n"
        "Time Horizon: {time_horizon}\n"
        "Current Situation: {current_situation}\n\n"
        "Deliver your analysis:\n"
        "(1) Identify predetermined elements (certainties) and critical uncertainties.\n"
        "(2) Select the two most impactful uncertainties to form a 2x2 scenario matrix.\n"
        "(3) Develop 3-4 distinct, plausible scenarios — each with a narrative arc, key assumptions, "
        "and implications (opportunities, threats, strategic response).\n"
        "(4) Define early warning indicators for each scenario.\n"
        "(5) Identify robust strategies that work across all scenarios (no-regret moves).\n"
        "(6) Provide scenario-specific contingent strategies and a monitoring plan.\n\n"
        "Create diverse futures, not just best/worst case. Be strategic and imaginative.\n\n"
    )

    def __init__(self):
        super().__init__(
            name="future_scenario_planner",
            description="Multi-horizon scenario planning for strategic decisions",
            version="1.0.0",
            tags=["temporal", "enterprise", "scenario-planning", "futures"],
            metadata={"category": "temporal", "license": "enterprise", "tier": "enterprise"},
            guidance=Guidance(
                role="Scenario Planning Expert and Strategic Futurist",
                rules=[
                    "Create 2-4 plausible, distinct scenarios (not predictions)",
                    "Base scenarios on key uncertainties, not certainties",
                    "Make scenarios internally consistent and detailed",
                    "Avoid best/worst case only - create diverse futures",
                    "Derive strategic implications for each scenario",
                ],
                style="strategic, imaginative, rigorous, multi-perspective",
            ),
            directive_template="""**FUTURE SCENARIO PLANNING**

**FOCAL QUESTION**: {focal_question}

**TIME HORIZON**: {time_horizon}

**CURRENT SITUATION**: {current_situation}

---

## STEP 1: KEY FORCES ANALYSIS

**Predetermined elements** (will definitely happen):
1. [Trend/force that's certain]
2. [Another certainty]
3. [Demographic/technological inevitability]

**Critical uncertainties** (could go either way):
1. [Uncertainty A] - Could be [X or Y]
2. [Uncertainty B] - Could be [X or Y]
3. [Uncertainty C] - Could be [X or Y]

**Most impactful uncertainties**: [Which 2 create most different futures?]

---

## STEP 2: SCENARIO LOGICS

**Two key uncertainties create 2x2 matrix**:

**Axis 1**: [Uncertainty A]
- High: [Description]
- Low: [Description]

**Axis 2**: [Uncertainty B]  
- High: [Description]
- Low: [Description]

**Four scenario spaces**:
1. High A, High B: [Scenario 1 name]
2. High A, Low B: [Scenario 2 name]
3. Low A, High B: [Scenario 3 name]
4. Low A, Low B: [Scenario 4 name]

---

## SCENARIO 1: [Memorable Name]

**Tagline**: [One-sentence description]

**Key assumptions**:
- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

**Narrative** (How we get there):

**Year 1-2** (Near-term):
[Early developments that set trajectory]

**Year 3-5** (Medium-term):
[Acceleration of trends]

**By target horizon** (End state):
[Fully realized scenario]

**Implications**:
- **Opportunities**: [What becomes possible]
- **Threats**: [What becomes risky]
- **Strategic response**: [What to do in this scenario]

---

## SCENARIO 2: [Name]

**Tagline**: [Description]

**Key assumptions**:
- [Different from Scenario 1]

**Narrative**:

**Year 1-2**: [Different early path]
**Year 3-5**: [Different mid-path]
**By target horizon**: [Different end state]

**Implications**:
- **Opportunities**: [Unique to this scenario]
- **Threats**: [Unique risks]
- **Strategic response**: [Different strategy]

---

## SCENARIO 3: [Name]

[Same structure]

---

## SCENARIO 4: [Name]

[Same structure]

---

## EARLY WARNING INDICATORS

**Signals telling us which scenario is emerging**:

**Scenario 1 signals**:
- If we see [X], Scenario 1 is becoming more likely
- Monitor: [Specific metric/event]

**Scenario 2 signals**:
- If we see [Y], Scenario 2 is likely
- Monitor: [Metric]

**Scenario 3 signals**:
- If [Z] occurs, Scenario 3 pathway
- Monitor: [Metric]

**Scenario 4 signals**:
- If [W] happens, Scenario 4 emerging
- Monitor: [Metric]

---

## ROBUST STRATEGIES

**What works across ALL scenarios** (no-regret moves):
1. [Strategy that's valuable in any future]
2. [Another robust strategy]
3. [Core capability to build regardless]

**Hedging strategies** (prepare for uncertainty):
- [Flexible option that keeps multiple paths open]
- [Reversible investment]

**Scenario-specific strategies** (contingent):
- If Scenario 1: [Specific strategy]
- If Scenario 2: [Different strategy]
- If Scenario 3: [Another strategy]
- If Scenario 4: [Yet another strategy]

---

## DECISION FRAMEWORK

**Use scenarios to test strategies**:

**Strategy X**:
- Scenario 1: [Outcome if this future occurs]
- Scenario 2: [Outcome in this future]
- Scenario 3: [Outcome]
- Scenario 4: [Outcome]
- **Verdict**: [Robust / Risky / Conditional]

**Strategy Y**:
[Same analysis]

---

## MONITORING PLAN

**Track which future is emerging**:

**Quarterly review**:
- Check early warning indicators
- Update scenario probabilities
- Adjust strategies accordingly

**Scenario refresh**:
- Annual: Review and update scenarios
- When: Major unexpected event occurs

---

## WILD CARDS

**Low-probability, high-impact events** (could disrupt all scenarios):

**Wild card 1**: [Unexpected event]
- Probability: [Low]
- Impact: [High/Transformative]
- Implications: [How it would change everything]

**Wild card 2**: [Another disruptive possibility]
- Probability: [Very low]
- Impact: [Extreme]

**Contingency**: [Basic preparation even for unlikely events]

---

## IMMEDIATE ACTIONS

**Based on scenario analysis**:

**Do now** (robust across scenarios):
1. [Action 1]
2. [Action 2]

**Prepare options** (keep flexibility):
1. [Option to develop]
2. [Capability to build]

**Monitor closely** (early warnings):
1. [Indicator 1]
2. [Indicator 2]""",
            input_schema={
                "focal_question": str,
                "time_horizon": str,
                "current_situation": str,
                "context_section": str,
            },
            constraints=Constraints(
                must_include=[
                    "multiple_scenarios",
                    "scenario_logics",
                    "early_warning_indicators",
                    "robust_strategies",
                ],
                must_not_include=["single_prediction", "best_worst_only"],
                style_guide="Strategic and imaginative. 2-4 distinct scenarios. Implications for each. Robust strategies.",
            ),
        )

    def build_context(self, focal_question="", time_horizon="", current_situation="", **kwargs):
        """Build context for scenario planning."""
        context_section = ""
        kwargs.pop("context_section", None)

        return super().build_context(
            focal_question=focal_question,
            time_horizon=time_horizon,
            current_situation=current_situation,
            context_section=context_section,
            **kwargs,
        )

    def execute(
        self, provider="openai", focal_question="", time_horizon="", current_situation="", **kwargs
    ):
        """Execute scenario planning."""
        context_section = ""
        kwargs.pop("context_section", None)

        return super().execute(
            provider=provider,
            focal_question=focal_question,
            time_horizon=time_horizon,
            current_situation=current_situation,
            context_section=context_section,
            **kwargs,
        )


__all__ = ["FutureScenarioPlanner"]
