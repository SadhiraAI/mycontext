---
sidebar_position: 5
title: Strategic Roadmap Generator
description: Build a 3-year strategic roadmap using FutureScenarioPlanner + ResourceAllocator + StakeholderMapper. A quality-gated Blueprint that produces a complete strategy document.
---

# Strategic Roadmap Generator

**Scenario:** Your leadership team needs to align on a 3-year strategic direction. The process is usually either too top-down (leadership dictates) or too bottom-up (death by stakeholder workshop). You want a structured approach that develops scenarios, maps stakeholder realities, allocates resources against priorities, and produces a document everyone can react to.

**Patterns used:**
- `FutureScenarioPlanner` — develops the strategic landscape over the planning horizon
- `ResourceAllocator` — optimises resource allocation across strategic initiatives
- `StakeholderMapper` — maps stakeholder interests, priorities, and likely resistance points

**Integration:** Blueprint + `QualityMetrics` gate + `to_markdown()` export for document delivery

---

```python
import mycontext

from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints
from mycontext.templates.enterprise.temporal import FutureScenarioPlanner
from mycontext.templates.enterprise.planning import ResourceAllocator
from mycontext.templates.free.planning import StakeholderMapper
from mycontext.intelligence import QualityMetrics, TemplateIntegratorAgent
from pathlib import Path

metrics = QualityMetrics(mode="heuristic")

strategy_blueprint = Blueprint(
    name="strategic_roadmap",
    guidance=Guidance(
        role="Strategy consultant facilitating a leadership team's 3-year planning",
        rules=[
            "Ground every strategic choice in a specific scenario assumption",
            "Allocate resources to initiatives, not just goals",
            "Name the stakeholders who will resist each initiative and why",
            "Define success metrics for each year: Year 1 (foundation), Year 2 (scale), Year 3 (lead)",
            "Include what you are explicitly NOT doing and why",
        ],
    ),
    directive_template=(
        "Generate a 3-year strategic roadmap for:\n\n"
        "Company: {company}\n"
        "Current position: {current_position}\n"
        "Strategic ambition: {ambition}\n"
        "Resources: {resources}\n"
        "Key constraints: {constraints}\n"
        "Stakeholders: {stakeholders}"
    ),
    constraints=Constraints(
        must_include=[
            "strategic scenarios",
            "year 1/2/3 milestones",
            "resource allocation",
            "stakeholder plan",
            "key risks",
            "not-doing list",
        ],
        format_rules=[
            "Use ## for each year",
            "Resource allocation as percentages",
            "Milestones as measurable outcomes",
        ],
    ),
    token_budget=6000,
    optimization="quality",
)


def generate_roadmap(company_info: dict, save_path: str | None = None) -> str:
    # Pre-analysis: scenarios + stakeholders independently
    scenario_ctx = FutureScenarioPlanner().build_context(
        situation=company_info["current_position"],
        horizon="3 years",
    )
    resource_ctx = ResourceAllocator().build_context(
        project=company_info["company"],
        objective=company_info["ambition"],
    )
    stakeholder_ctx = StakeholderMapper().build_context(
        project=company_info["company"],
        objective=company_info["ambition"],
    )

    pre_analysis = {}
    for name, ctx in [("scenarios", scenario_ctx), ("resources", resource_ctx), ("stakeholders", stakeholder_ctx)]:
        score = metrics.evaluate(ctx)
        print(f"  {name}: {score.overall:.0%}")
        if score.overall >= 0.65:
            pre_analysis[name] = ctx.execute(provider="openai", model="gpt-4o-mini").response

    # Build the main roadmap context with pre-analysis as knowledge
    ctx = strategy_blueprint.build(**company_info)
    if pre_analysis:
        ctx.knowledge = "\n\n".join(
            f"=== {k.upper()} PRE-ANALYSIS ===\n{v}" for k, v in pre_analysis.items()
        )

    final_score = metrics.evaluate(ctx)
    print(f"Final roadmap context: {final_score.overall:.0%}")

    roadmap = ctx.execute(provider="openai", model="gpt-4o").response

    if save_path:
        full_doc = f"# Strategic Roadmap: {company_info['company']}\n\n{roadmap}"
        Path(save_path).write_text(full_doc)

    return roadmap


roadmap = generate_roadmap(
    company_info={
        "company": "mycontext-ai (SadhiraAI)",
        "current_position": "v0.6.0, 88 cognitive patterns, growing developer community, pre-revenue",
        "ambition": "Become the standard context engineering SDK for enterprise AI teams",
        "resources": "$1.2M seed, team of 6, 18-month runway",
        "constraints": "Small team, no dedicated sales, competing with well-funded LangChain ecosystem",
        "stakeholders": "Enterprise engineering teams, AI platform leads, open-source community, investors",
    },
    save_path="strategy/roadmap-2026-2028.md",
)
print(roadmap)
```

## What You Get

A complete strategy document including:

- **Scenario assumptions:** the 2-3 futures the strategy is designed for
- **Year-by-year milestones:** measurable outcomes (not activities) for each year
- **Resource allocation:** what percentage of team/budget goes to each initiative
- **Stakeholder plan:** who will support, who will resist, and how to engage each
- **Not-doing list:** explicit decisions about what you are deprioritising and why

The pre-analysis step (scenarios, resources, stakeholders run independently first) enriches the final roadmap with dedicated specialist thinking before the synthesis.
