---
sidebar_position: 4
title: Case Strategy Workshop
description: Adversarial case preparation using DecisionFramework + ScenarioPlanner + StakeholderMapper. A CrewAI crew that plays defence, prosecution, and judge simultaneously.
---

# Case Strategy Workshop

**Scenario:** A litigation team is preparing for trial. They need to stress-test their strategy from every angle: how will opposing counsel attack it, how will a judge view it, what are the factual weaknesses. You want a structured simulation that surfaces these perspectives before the courtroom does.

**Patterns used:**
- `DecisionFramework` (enterprise) — evaluates strategic options with explicit criteria
- `ScenarioPlanner` — plans for multiple case trajectory scenarios
- `StakeholderMapper` — maps each party's interests, motivations, and likely moves

**Integration:** CrewAI adversarial simulation

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from crewai import Agent, Task, Crew
from mycontext.templates.enterprise.decision import DecisionFramework
from mycontext.templates.free.planning import ScenarioPlanner, StakeholderMapper
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")


def case_strategy_workshop(case: dict) -> str:
    defence_ctx = DecisionFramework().build_context(
        decision=f"Best litigation strategy for: {case['our_position']}",
        context_section=f"Facts: {case['facts']}\nWeaknesses: {case['our_weaknesses']}",
    )
    prosecution_ctx = ScenarioPlanner().build_context(
        situation=f"Opposing position: {case['opposing_position']}",
        horizon="trial outcome",
    )
    stakeholder_ctx = StakeholderMapper().build_context(
        project=case["case_name"],
        objective="Map all parties' interests and predict their strategy",
    )

    defence_counsel = Agent(
        role="Senior Defence Counsel",
        goal="Develop the strongest possible defence strategy and identify weaknesses to address",
        backstory=defence_ctx.assemble(),
        verbose=False,
    )
    prosecution_counsel = Agent(
        role="Opposing Counsel Simulator",
        goal="Attack the defence position as aggressively as a skilled opposing counsel would",
        backstory=prosecution_ctx.assemble(),
        verbose=False,
    )
    judge = Agent(
        role="Neutral Judge",
        goal="Assess each side objectively and identify the decisive legal and factual issues",
        backstory=stakeholder_ctx.assemble(),
        verbose=False,
    )

    defence_task = Task(
        description=(
            f"Case: {case['case_name']}\n"
            f"Our position: {case['our_position']}\n"
            f"Key facts: {case['facts']}\n\n"
            "Develop the litigation strategy: theory of the case, key arguments, evidence priorities."
        ),
        expected_output="Litigation strategy memo: theory of case, top 5 arguments, evidence gaps to address",
        agent=defence_counsel,
    )
    attack_task = Task(
        description="Attack the defence strategy above as vigorously as possible. Find every weakness.",
        expected_output="Opposing counsel attacks: strongest arguments, evidence challenges, witness vulnerabilities",
        agent=prosecution_counsel,
        context=[defence_task],
    )
    assessment_task = Task(
        description="Neutral judicial assessment of both sides. What are the decisive issues?",
        expected_output=(
            "Which arguments are legally strongest, which facts are genuinely in dispute, "
            "likely outcome if argued as presented, what the defence must address before trial"
        ),
        agent=judge,
        context=[defence_task, attack_task],
    )

    crew = Crew(
        agents=[defence_counsel, prosecution_counsel, judge],
        tasks=[defence_task, attack_task, assessment_task],
        verbose=False,
    )
    return crew.kickoff()


case = {
    "case_name": "Meridian Corp v. DataSync Ltd",
    "our_position": "Defendant DataSync: contract frustrated by force majeure (supply chain disruption)",
    "opposing_position": "Plaintiff Meridian: force majeure does not cover software delivery delays; alternatives existed",
    "facts": (
        "DataSync contracted to deliver analytics platform by March 2024. "
        "8-month delay. DataSync cites offshore subcontractor unavailability. "
        "Meridian claims domestic alternatives existed. "
        "Force majeure clause covers natural disasters, acts of government, pandemics. "
        "No specific mention of supply chain."
    ),
    "our_weaknesses": "No written evidence domestic alternatives were unavailable; delayed notice to Meridian",
}

analysis = case_strategy_workshop(case)
print(analysis)
```

## What You Get

Three perspectives on the same case, surfaced before trial:

- **Defence strategy:** core theory, best arguments, evidence to prioritise
- **Opposing attacks:** every weakness opposing counsel will exploit
- **Judicial assessment:** which arguments land, what the decisive issues are, probable outcome

Teams consistently find 2-3 critical issues they had underweighted before running this exercise.
