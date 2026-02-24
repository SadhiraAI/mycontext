---
sidebar_position: 2
title: Product Opportunity Analysis
description: Evaluate new product ideas with IdeaGenerator + InnovationFramework + SWOTAnalyzer + DecisionFramework. A CrewAI ideation crew that goes from raw idea to investment decision.
---

# Product Opportunity Analysis

**Scenario:** Your product team has a new product idea. Before committing resources, you want structured analysis: how good is the idea, what are the risks, who are the competitors, and is this worth pursuing? You want to move from "we have an idea" to "here is a structured go/no-go with rationale" in hours, not weeks.

**Patterns used:**
- `IdeaGenerator` (enterprise) — expands the initial idea space and identifies adjacent opportunities
- `InnovationFramework` (enterprise) — evaluates feasibility, desirability, and viability
- `SWOTAnalyzer` (enterprise) — structured competitive and strategic assessment
- `DecisionFramework` (enterprise) — structured go/no-go with explicit criteria

**Integration:** CrewAI four-agent crew: ideation, innovation assessment, competitive analysis, decision

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from crewai import Agent, Task, Crew
from mycontext.templates.enterprise.creative import IdeaGenerator, InnovationFramework
from mycontext.templates.enterprise.analysis import SWOTAnalyzer
from mycontext.templates.enterprise.decision import DecisionFramework
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")


def product_opportunity_analysis(idea: dict) -> str:
    idea_brief = f"Product idea: {idea['name']}\nDescription: {idea['description']}\nTarget market: {idea['market']}"

    idea_ctx = IdeaGenerator().build_context(
        topic=idea_brief,
        constraints=f"Budget: {idea.get('budget', 'unspecified')}, Timeline: {idea.get('timeline', 'unspecified')}",
    )
    innovation_ctx = InnovationFramework().build_context(
        challenge=idea_brief,
        context_section="Apply desirability, feasibility, viability framework",
    )
    swot_ctx = SWOTAnalyzer().build_context(
        situation=idea_brief,
        context_section=f"Competitive context: {idea.get('competitive_context', 'unknown')}",
    )
    decision_ctx = DecisionFramework().build_context(
        decision=f"Should we build: {idea['name']}?",
        context_section=f"Success criteria: {idea.get('success_criteria', 'profitability, market fit')}",
    )

    ideator = Agent(
        role="Product Strategist",
        goal="Expand the idea, identify the strongest version, and surface adjacent opportunities",
        backstory=idea_ctx.assemble(),
        verbose=False,
    )
    innovator = Agent(
        role="Innovation Analyst",
        goal="Evaluate desirability, feasibility, and viability rigorously",
        backstory=innovation_ctx.assemble(),
        verbose=False,
    )
    competitive_analyst = Agent(
        role="Competitive Intelligence Analyst",
        goal="Map the competitive landscape and identify genuine differentiation opportunities",
        backstory=swot_ctx.assemble(),
        verbose=False,
    )
    decision_maker = Agent(
        role="Investment Decision Lead",
        goal="Make a clear go/no-go recommendation with evidence-based rationale",
        backstory=decision_ctx.assemble(),
        verbose=False,
    )

    ideation_task = Task(
        description=f"Expand and stress-test this idea:\n{idea_brief}",
        expected_output="Strongest version of the idea, 3 adjacent variations, key assumptions to validate",
        agent=ideator,
    )
    innovation_task = Task(
        description="Assess desirability, feasibility, and viability with evidence",
        expected_output="DFV assessment with scores (1-10), key risks, and minimum viable assumptions",
        agent=innovator,
        context=[ideation_task],
    )
    swot_task = Task(
        description=f"SWOT analysis for: {idea['name']}",
        expected_output="SWOT matrix with competitive positioning and differentiation strategy",
        agent=competitive_analyst,
        context=[ideation_task],
    )
    decision_task = Task(
        description="Make the investment recommendation based on all analysis",
        expected_output=(
            "Go/no-go recommendation with: confidence level, key risks, "
            "conditions for proceeding, next 3 steps if green-lit"
        ),
        agent=decision_maker,
        context=[innovation_task, swot_task],
    )

    crew = Crew(
        agents=[ideator, innovator, competitive_analyst, decision_maker],
        tasks=[ideation_task, innovation_task, swot_task, decision_task],
        verbose=False,
    )
    return crew.kickoff()


idea = {
    "name": "AI-powered context engineering platform for LLMs",
    "description": "SDK that transforms raw LLM prompts into structured, measurable contexts using cognitive patterns from psychology and epistemology",
    "market": "Enterprise development teams building production LLM applications",
    "competitive_context": "LangChain, DSPy, PromptLayer — none have structured cognitive pattern libraries",
    "budget": "$500K seed for 18 months",
    "timeline": "MVP in 6 months, enterprise launch in 12 months",
    "success_criteria": "100 enterprise customers paying >$10K ARR within 18 months",
}

analysis = product_opportunity_analysis(idea)
print(analysis)
```

## What You Get

A complete opportunity assessment covering:

- **Strongest version of the idea** — the ideator finds the most compelling framing
- **DFV scores** — Desirability, Feasibility, Viability each scored 1-10 with evidence
- **SWOT matrix** — including competitive positioning against named competitors
- **Go/no-go recommendation** — with confidence level, key risks, and conditions for proceeding

The four-agent structure means you get genuinely independent analytical perspectives before the decision synthesises them — not a single LLM doing everything in one pass.
