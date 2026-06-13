---
sidebar_position: 5
title: Clinical Ethics Consultation
description: Simulate a multi-perspective ethics board with EthicalFrameworkAnalyzer + MoralDilemmaResolver + StakeholderEthicsAssessor. A CrewAI ethics consultation crew.
---

# Clinical Ethics Consultation

**Scenario:** A hospital faces an ethically complex case: a patient with diminishing capacity, disagreeing family members, resource constraints, and conflicting clinical recommendations. The ethics committee needs a structured consultation that applies multiple ethical frameworks and surfaces all stakeholder perspectives.

**Patterns used:**
- `EthicalFrameworkAnalyzer` — applies deontological, consequentialist, and virtue ethics lenses
- `MoralDilemmaResolver` — navigates the specific tension between competing moral claims
- `StakeholderEthicsAssessor` — maps each stakeholder's ethical position and interests

**Integration:** CrewAI multi-agent simulation — patient advocate, clinical ethics specialist, and family mediator

---

```python
import mycontext

from crewai import Agent, Task, Crew
from mycontext.templates.enterprise.ethical_reasoning import (
    EthicalFrameworkAnalyzer,
    MoralDilemmaResolver,
    StakeholderEthicsAssessor,
)
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")


def ethics_consultation(case: dict) -> str:
    """
    case = {
        "patient": "82F, advanced dementia, no advance directive",
        "dilemma": "Family requesting aggressive treatment; clinical team recommends comfort care",
        "stakeholders": "patient (limited capacity), adult children (divided), clinical team, hospital ethics board",
        "context": "Limited ICU capacity, patient has pneumonia, poor prognosis",
    }
    """
    case_brief = "\n".join(f"{k}: {v}" for k, v in case.items())

    ethics_ctx = EthicalFrameworkAnalyzer().build_context(
        situation=case_brief,
        context_section="Apply multiple ethical frameworks: autonomy, beneficence, non-maleficence, justice",
    )
    dilemma_ctx = MoralDilemmaResolver().build_context(
        conflict=case["dilemma"],
        context_section=case_brief,
    )
    stakeholder_ctx = StakeholderEthicsAssessor().build_context(
        situation=case_brief,
        context_section=case["stakeholders"],
    )

    for name, ctx in [("ethics frameworks", ethics_ctx), ("dilemma", dilemma_ctx), ("stakeholders", stakeholder_ctx)]:
        score = metrics.evaluate(ctx)
        print(f"  {name}: {score.overall:.0%}")

    patient_advocate = Agent(
        role="Patient Advocate",
        goal="Represent the patient's best interests and any discernible wishes",
        backstory=ethics_ctx.assemble(),
        verbose=False,
    )
    ethics_specialist = Agent(
        role="Clinical Ethics Specialist",
        goal="Apply systematic ethical frameworks to identify the most defensible course of action",
        backstory=dilemma_ctx.assemble(),
        verbose=False,
    )
    family_mediator = Agent(
        role="Family Mediator",
        goal="Map all stakeholder positions and find common ground",
        backstory=stakeholder_ctx.assemble(),
        verbose=False,
    )

    advocate_task = Task(
        description=f"From the patient's perspective, what would they most likely want?\n\n{case_brief}",
        expected_output="Patient-centred analysis: inferred wishes, dignity considerations, prior values if any",
        agent=patient_advocate,
    )
    ethics_task = Task(
        description=f"Apply deontological, consequentialist, and virtue ethics to: {case['dilemma']}",
        expected_output="Multi-framework analysis with a recommended course of action and rationale",
        agent=ethics_specialist,
    )
    stakeholder_task = Task(
        description=f"Map each stakeholder's position, interests, and the ethical basis for their view",
        expected_output="Stakeholder map with ethical analysis of each position and mediation recommendations",
        agent=family_mediator,
    )
    synthesis_task = Task(
        description="Synthesise the three perspectives into a consultation report with a clear recommendation",
        expected_output=(
            "Ethics consultation report: summary of dilemma, perspectives, "
            "recommended action with justification, dissenting views, documentation guidance"
        ),
        agent=ethics_specialist,
        context=[advocate_task, ethics_task, stakeholder_task],
    )

    crew = Crew(
        agents=[patient_advocate, ethics_specialist, family_mediator],
        tasks=[advocate_task, ethics_task, stakeholder_task, synthesis_task],
        verbose=False,
    )
    return crew.kickoff()


case = {
    "patient": "82-year-old woman with advanced dementia, no advance directive on file",
    "dilemma": "Two adult children requesting full resuscitation and ICU admission; clinical team recommends DNR and comfort-focused care given poor prognosis and patient's current quality of life",
    "stakeholders": "Patient (diminished capacity), two adult children (divided), attending physician, ICU team, hospital ethics committee",
    "context": "Aspiration pneumonia with sepsis. ICU beds limited. Prognosis: <20% survival to discharge with treatment.",
}

report = ethics_consultation(case)
print(report)
```

## What You Get

A structured ethics consultation report that:

- Applies three ethical frameworks to the same dilemma
- Documents each stakeholder's position and its ethical basis
- Makes a clear recommendation with explicit justification
- Records dissenting views
- Provides documentation guidance for the medical record

This does not replace a human ethics committee — it gives them a thorough structured starting point that typically takes several hours of committee work to produce manually.
