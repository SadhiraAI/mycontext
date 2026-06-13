---
sidebar_position: 5
title: Crisis Response Planning
description: Coordinate multi-agency crisis response using ScenarioPlanner + RiskMitigator + FutureScenarioPlanner + StakeholderMapper. A CrewAI emergency response crew.
---

# Crisis Response Planning

**Scenario:** An emergency management agency needs to develop a crisis response plan for a major incident (flood, cyber attack, pandemic surge, industrial accident). Effective plans coordinate multiple agencies, anticipate escalation scenarios, and assign resources before the crisis hits — not during it.

**Patterns used:**
- `ScenarioPlanner` — develops detailed crisis scenarios and escalation paths
- `RiskMitigator` — identifies risk reduction interventions at each scenario stage
- `FutureScenarioPlanner` — models how the crisis might evolve over time
- `StakeholderMapper` — maps all agencies, their roles, and coordination points

**Integration:** CrewAI multi-agency simulation crew

---

```python
import mycontext

from crewai import Agent, Task, Crew
from mycontext.templates.free.planning import ScenarioPlanner, StakeholderMapper
from mycontext.templates.enterprise.specialized import RiskMitigator
from mycontext.templates.enterprise.temporal import FutureScenarioPlanner
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")


def crisis_response_plan(crisis: dict) -> str:
    crisis_brief = "\n".join(f"{k}: {v}" for k, v in crisis.items())

    scenario_ctx = ScenarioPlanner().build_context(
        situation=crisis_brief,
        horizon="72 hours initial + 30 days sustained response",
    )
    risk_ctx = RiskMitigator().build_context(
        challenge=crisis["type"],
        context_section=crisis_brief,
    )
    future_ctx = FutureScenarioPlanner().build_context(
        situation=crisis_brief,
        horizon="30 days",
    )
    stakeholder_ctx = StakeholderMapper().build_context(
        project=f"Crisis response: {crisis['type']}",
        objective="Coordinate multi-agency response effectively",
    )

    for name, ctx in [("scenario", scenario_ctx), ("risk", risk_ctx), ("future", future_ctx), ("stakeholders", stakeholder_ctx)]:
        s = metrics.evaluate(ctx)
        print(f"  {name}: {s.overall:.0%}")

    incident_commander = Agent(
        role="Incident Commander",
        goal="Develop the immediate response plan for the first 72 hours",
        backstory=scenario_ctx.assemble(),
        verbose=False,
    )
    risk_specialist = Agent(
        role="Risk Mitigation Specialist",
        goal="Identify and mitigate escalation risks at every stage of the response",
        backstory=risk_ctx.assemble(),
        verbose=False,
    )
    strategic_planner = Agent(
        role="Strategic Crisis Planner",
        goal="Plan for how this crisis might evolve over 30 days and position resources accordingly",
        backstory=future_ctx.assemble(),
        verbose=False,
    )
    coordination_lead = Agent(
        role="Multi-Agency Coordination Lead",
        goal="Map all agencies, assign clear roles, and design the coordination structure",
        backstory=stakeholder_ctx.assemble(),
        verbose=False,
    )

    immediate_task = Task(
        description=f"Crisis: {crisis['type']}\n{crisis_brief}\n\nDevelop the 72-hour immediate response plan: first actions, resource deployment, command structure.",
        expected_output="Hour-by-hour response plan for first 72 hours with resource assignments",
        agent=incident_commander,
    )
    risk_task = Task(
        description="What are the top 5 escalation risks in this response? What mitigations should be pre-positioned?",
        expected_output="Risk register with mitigation actions and triggers for each escalation scenario",
        agent=risk_specialist,
        context=[immediate_task],
    )
    sustained_task = Task(
        description="How might this crisis evolve over 30 days? What resources and capabilities must be sustained?",
        expected_output="30-day scenario map with decision points and resource requirements at each stage",
        agent=strategic_planner,
        context=[immediate_task, risk_task],
    )
    coordination_task = Task(
        description="Design the multi-agency coordination structure: who does what, how do they communicate, who resolves conflicts?",
        expected_output="RACI matrix, communication protocols, escalation paths, inter-agency agreements needed",
        agent=coordination_lead,
        context=[immediate_task, risk_task, sustained_task],
    )

    crew = Crew(
        agents=[incident_commander, risk_specialist, strategic_planner, coordination_lead],
        tasks=[immediate_task, risk_task, sustained_task, coordination_task],
        verbose=False,
    )
    return crew.kickoff()


crisis = {
    "type": "Major flooding — coastal city",
    "scale": "Estimated 50,000 residents affected, 8,000 requiring evacuation",
    "current_status": "Category 3 storm making landfall in 18 hours. Rivers at 85% flood capacity.",
    "available_resources": "2 emergency management teams, National Guard on standby, 15 shelters, hospital at 70% capacity",
    "key_vulnerabilities": "3 care homes in flood zone, power grid at risk, 1 bridge likely impassable",
    "agencies_involved": "Emergency Management, Police, Fire, National Guard, Health Service, Utilities, Red Cross",
}

plan = crisis_response_plan(crisis)
print(plan)
```

## What You Get

A complete, pre-positioned crisis response plan:

- **72-hour immediate response:** hour-by-hour actions, resource assignments, command structure
- **Risk register:** top 5 escalation risks with pre-positioned mitigations
- **30-day scenario map:** how the crisis might evolve, decision points, sustained resource needs
- **RACI matrix:** who is responsible, accountable, consulted, and informed — across all agencies

Running this exercise before a crisis is the difference between coordinated response and improvised reaction.
