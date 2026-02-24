---
sidebar_position: 6
title: Culture & Org Health Analysis
description: Diagnose organisational culture and health using FeedbackLoopIdentifier + SWOTAnalyzer + SystemArchetypeAnalyzer. A CrewAI diagnostic crew for People Ops.
---

# Culture & Org Health Analysis

**Scenario:** Your organisation ran an engagement survey. The results are mixed — some things are good, some are not, and the root causes are unclear. You want a structured diagnosis that goes beyond survey scores to identify the cultural dynamics at play and what interventions would actually improve things.

**Patterns used:**
- `FeedbackLoopIdentifier` (enterprise) — maps the cultural reinforcing loops that sustain current behaviour
- `SWOTAnalyzer` (enterprise) — assesses cultural strengths to build on and weaknesses to address
- `SystemArchetypeAnalyzer` (enterprise) — identifies systemic patterns (shifting the burden, eroding goals) in the culture

**Integration:** CrewAI diagnostic crew — culture analyst, systems thinker, intervention designer

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from crewai import Agent, Task, Crew
from mycontext.templates.enterprise.systems_thinking import (
    FeedbackLoopIdentifier,
    SystemArchetypeAnalyzer,
)
from mycontext.templates.enterprise.analysis import SWOTAnalyzer
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")


def org_culture_diagnosis(org_data: dict) -> str:
    org_brief = "\n".join(f"{k}: {v}" for k, v in org_data.items())

    feedback_ctx = FeedbackLoopIdentifier().build_context(
        system="organisational culture",
        observation=org_brief,
    )
    swot_ctx = SWOTAnalyzer().build_context(
        situation=f"Organisational culture: {org_data.get('company', '')}",
        context_section=org_brief,
    )
    archetype_ctx = SystemArchetypeAnalyzer().build_context(
        system="organisational culture",
        observation=org_brief,
    )

    for name, ctx in [("feedback", feedback_ctx), ("swot", swot_ctx), ("archetype", archetype_ctx)]:
        s = metrics.evaluate(ctx)
        print(f"  {name}: {s.overall:.0%}")

    culture_analyst = Agent(
        role="Organisational Culture Analyst",
        goal="Diagnose the cultural feedback loops that are sustaining current behaviour (good and bad)",
        backstory=feedback_ctx.assemble(),
        verbose=False,
    )
    swot_analyst = Agent(
        role="Organisational SWOT Analyst",
        goal="Identify cultural strengths to build on and weaknesses to address with evidence",
        backstory=swot_ctx.assemble(),
        verbose=False,
    )
    systems_thinker = Agent(
        role="Organisational Systems Thinker",
        goal="Name the system archetype in play and predict its trajectory if unaddressed",
        backstory=archetype_ctx.assemble(),
        verbose=False,
    )
    intervention_designer = Agent(
        role="People Ops Intervention Designer",
        goal="Design 3-5 specific, high-leverage interventions based on the diagnosis",
        backstory=(
            "You are a senior People Operations leader with 15 years of culture transformation experience. "
            "You design interventions that are structural, not cosmetic — addressing root causes, not symptoms."
        ),
        llm_config={"config_list": [{"model": "gpt-4o-mini"}]},
        verbose=False,
    )

    feedback_task = Task(
        description=f"Analyse the cultural dynamics:\n{org_brief}\n\nMap the reinforcing loops that sustain current behaviours.",
        expected_output="Cultural feedback loops: what sustains the good behaviours and what sustains the problematic ones",
        agent=culture_analyst,
    )
    swot_task = Task(
        description="SWOT analysis of the organisational culture",
        expected_output="Cultural SWOT matrix with specific evidence from the data",
        agent=swot_analyst,
        context=[feedback_task],
    )
    archetype_task = Task(
        description="Name the systemic archetype(s) in play and predict what happens if nothing changes",
        expected_output="Archetype name, description, trajectory prediction, structural intervention required",
        agent=systems_thinker,
        context=[feedback_task, swot_task],
    )
    intervention_task = Task(
        description="Design 3-5 specific, structural interventions based on the full diagnosis",
        expected_output=(
            "Intervention plan: each with objective, mechanism, who owns it, "
            "how success is measured, and timeline"
        ),
        agent=intervention_designer,
        context=[feedback_task, swot_task, archetype_task],
    )

    crew = Crew(
        agents=[culture_analyst, swot_analyst, systems_thinker, intervention_designer],
        tasks=[feedback_task, swot_task, archetype_task, intervention_task],
        verbose=False,
    )
    return crew.kickoff()


org_data = {
    "company": "TechCo (200 people, B2B SaaS)",
    "survey_scores": "Engagement: 68%, Psychological safety: 55%, Manager effectiveness: 61%, Growth: 59%",
    "qualitative_themes": (
        "Top positive: smart colleagues, interesting work, flat structure. "
        "Top negative: unclear priorities, too many meetings, recognition gaps, "
        "feedback culture weak (people afraid to raise issues)."
    ),
    "observable_behaviours": (
        "Decisions escalated to senior leadership routinely. "
        "Postmortems focus on blame not learning. "
        "High performers leaving. "
        "Lots of 'yes' in meetings, issues raised only in Slack DMs."
    ),
    "context": "Company grew 3x in 18 months. Original team 40 people, now 200. Most managers promoted internally with no management training.",
}

diagnosis = org_culture_diagnosis(org_data)
print(diagnosis)
```

## What You Get

A four-stage culture diagnosis:

| Stage | Output |
|-------|--------|
| **Feedback loops** | What cultural dynamics are self-reinforcing (e.g. "managers promoted without training escalate decisions, reinforcing the belief that senior leadership must decide everything") |
| **SWOT** | Cultural strengths to deliberately preserve + specific weaknesses with evidence |
| **Archetype** | Which classic systemic pattern is in play (often "Shifting the Burden" — symptomatic fixes like more all-hands instead of structural change) |
| **Interventions** | 3-5 structural changes that address root causes, each with owner, metric, and timeline |

The intervention list is specific, not generic. Not "improve psychological safety" — but "introduce blameless postmortem format, train all managers in 30 days, measure change in issues raised per retrospective."
