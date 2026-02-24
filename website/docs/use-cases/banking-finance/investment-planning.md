---
sidebar_position: 3
title: Investment Scenario Planning
description: Multi-scenario investment analysis with FutureScenarioPlanner + MultiObjectiveOptimizer + DecisionFramework. A CrewAI crew of macro analyst, risk manager, and portfolio strategist.
---

# Investment Scenario Planning

**Scenario:** Your investment team needs to evaluate a major allocation decision under uncertainty. Multiple scenarios are plausible (rate cuts, recession, geopolitical shock), each implying different optimal positions. You want structured multi-perspective analysis that surfaces the decision's sensitivity to each scenario.

**Patterns used:**
- `FutureScenarioPlanner` (enterprise) — develops plausible futures with probability weights
- `MultiObjectiveOptimizer` (enterprise) — finds allocations satisfying competing objectives
- `DecisionFramework` (enterprise) — structures the final decision with explicit criteria

**Integration:** CrewAI three-agent crew — macro analyst, risk manager, portfolio strategist

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from crewai import Agent, Task, Crew
from mycontext.templates.enterprise.temporal import FutureScenarioPlanner
from mycontext.templates.enterprise.decision import MultiObjectiveOptimizer, DecisionFramework
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")


def investment_scenario_analysis(decision: dict) -> str:
    scenario_ctx = FutureScenarioPlanner().build_context(
        situation=decision["situation"],
        horizon=decision["horizon"],
    )
    optimizer_ctx = MultiObjectiveOptimizer().build_context(
        decision=decision["allocation_question"],
        context_section=f"Objectives: {decision['objectives']}",
    )
    decision_ctx = DecisionFramework().build_context(
        decision=decision["allocation_question"],
        context_section=f"Constraints: {decision['constraints']}",
    )

    macro_analyst = Agent(
        role="Macro Research Analyst",
        goal="Develop plausible economic scenarios with probability weights and implications",
        backstory=scenario_ctx.assemble(),
        verbose=False,
    )
    risk_manager = Agent(
        role="Portfolio Risk Manager",
        goal="Find allocations satisfying return, risk, and liquidity objectives simultaneously",
        backstory=optimizer_ctx.assemble(),
        verbose=False,
    )
    strategist = Agent(
        role="Portfolio Strategist",
        goal="Make the final allocation recommendation with scenario sensitivity analysis",
        backstory=decision_ctx.assemble(),
        verbose=False,
    )

    scenario_task = Task(
        description=(
            f"Develop 4 scenarios for the next {decision['horizon']}:\n"
            f"Market: {decision['situation']}\n"
            "For each scenario: name, probability, key drivers, asset class implications"
        ),
        expected_output="4 named scenarios with probability, narrative, and asset implications",
        agent=macro_analyst,
    )
    optimise_task = Task(
        description=(
            f"Given the 4 scenarios, find allocations satisfying:\n"
            f"Objectives: {decision['objectives']}\n"
            f"Constraints: {decision['constraints']}"
        ),
        expected_output="Optimal allocation ranges per scenario with objective trade-off scores",
        agent=risk_manager,
        context=[scenario_task],
    )
    decision_task = Task(
        description="Synthesise scenario analysis and optimisation into a final allocation recommendation",
        expected_output=(
            "Investment memo: recommended allocation, rationale, scenario sensitivity, "
            "risk mitigants, triggers to reassess"
        ),
        agent=strategist,
        context=[scenario_task, optimise_task],
    )

    crew = Crew(
        agents=[macro_analyst, risk_manager, strategist],
        tasks=[scenario_task, optimise_task, decision_task],
        verbose=False,
    )
    return crew.kickoff()


decision = {
    "situation": "Fed signalling rate cuts in H2 2026, elevated geopolitical risk, AI equity rally showing fatigue",
    "horizon": "12 months",
    "allocation_question": "Allocate $50M institutional portfolio across equities, fixed income, alternatives, cash",
    "objectives": "Target 8% return, max 12% volatility, maintain 15% liquidity, ESG screen applied",
    "constraints": "No single position >8%, min 20% fixed income, EM max 15%",
}

memo = investment_scenario_analysis(decision)
print(memo)
```

## What You Get

An investment memo structured around scenarios rather than a single point forecast:

- 4 named scenarios (e.g. Soft Landing, Stagflation, Rate Shock, AI Productivity Boom) with probability weights
- Optimal allocation for each scenario given your specific objectives and constraints
- Recommended allocation that performs acceptably across all scenarios, not just the base case
- Trigger conditions: what market signals would cause you to shift from the recommended allocation

The key insight: "overweight duration if rates fall" is a single-scenario bet. This approach gives you a portfolio that is robust across plausible futures.
