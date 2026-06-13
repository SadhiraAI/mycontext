---
sidebar_position: 5
title: Financial Report Narrative
description: Turn raw financial data into executive-ready narrative with DataAnalyzer + SynthesisBuilder + NarrativeBuilder. A Blueprint that converts numbers into story.
---

# Financial Report Narrative

**Scenario:** Your finance team produces detailed reports full of accurate numbers that nobody reads. Leadership wants narrative: what does this data mean, what changed, why, and what should we do about it. Turning tables into prose currently takes a senior analyst 3–4 hours per report.

**Patterns used:**
- `DataAnalyzer` — extracts meaningful insights from numerical and tabular data
- `SynthesisBuilder` — synthesises insights into a coherent narrative
- `NarrativeBuilder` — crafts the final narrative with appropriate structure, tone, and emphasis

**Integration:** Blueprint + `to_markdown()` export for direct document insertion

---

```python
import mycontext

from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints
from mycontext.templates.free.analysis import DataAnalyzer
from mycontext.templates.free.reasoning import SynthesisBuilder
from mycontext.templates.enterprise.communication import NarrativeBuilder
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")

narrative_blueprint = Blueprint(
    name="financial_narrative",
    guidance=Guidance(
        role="Chief Financial Officer writing for a board audience",
        rules=[
            "Lead with the headline number and whether it is good or bad",
            "Explain variances against budget and prior period — not just the number",
            "Connect financial performance to operational decisions",
            "Flag risks and opportunities explicitly",
            "Keep the narrative under 400 words per section",
        ],
    ),
    directive_template=(
        "Write an executive narrative for this financial data:\n\n"
        "Period: {period}\n"
        "Audience: {audience}\n\n"
        "Revenue data:\n{revenue_data}\n\n"
        "Cost data:\n{cost_data}\n\n"
        "Key metrics:\n{key_metrics}\n\n"
        "Prior period comparison:\n{prior_period}"
    ),
    constraints=Constraints(
        must_include=["headline performance", "key variances", "drivers", "outlook", "risks"],
        format_rules=[
            "Use ## headings for each section",
            "Numbers must include % change vs prior period",
            "Bold the most important number in each section",
        ],
    ),
    token_budget=3000,
    optimization="quality",
)


def generate_narrative(financials: dict, save_path: str | None = None) -> str:
    # Stage 1: Analyse the data
    data_ctx = DataAnalyzer().build_context(
        data_description="\n".join(f"{k}: {v}" for k, v in financials.items()),
        analysis_type="financial performance analysis",
    )
    score = metrics.evaluate(data_ctx)
    print(f"Data analysis context: {score.overall:.0%}")
    data_analysis = data_ctx.execute(provider="openai", model="gpt-4o-mini").response

    # Stage 2: Synthesise key findings
    synth_ctx = SynthesisBuilder().build_context(
        sources=data_analysis,
        topic="financial performance summary",
    )
    synthesis = synth_ctx.execute(provider="openai", model="gpt-4o-mini").response

    # Stage 3: Build the executive narrative
    narrative_ctx = narrative_blueprint.build(**financials)
    narrative_ctx.knowledge = f"Pre-analysis:\n{synthesis}"

    final = narrative_ctx.execute(provider="openai", model="gpt-4o").response

    if save_path:
        from pathlib import Path
        Path(save_path).write_text(f"# Financial Report — {financials.get('period', '')}\n\n{final}")

    return final


financials = {
    "period": "Q4 2025",
    "audience": "Board of Directors",
    "revenue_data": (
        "Total revenue: $28.4M (budget: $26.1M, Q4 2024: $23.8M)\n"
        "SaaS recurring: $19.2M (+22% YoY), Professional services: $9.2M (+10% YoY)\n"
        "New logos: 47 (budget: 40), churn rate: 3.2% (budget: 4.0%)"
    ),
    "cost_data": (
        "COGS: $8.9M (31% of revenue, budget: 33%)\n"
        "R&D: $6.1M (+15% YoY, 1 new hire vs plan)\n"
        "Sales & Marketing: $7.4M (below budget by $0.6M due to delayed campaign)"
    ),
    "key_metrics": (
        "EBITDA: $5.2M (18.3% margin, budget: 15.8%)\n"
        "ARR: $76.8M (+28% YoY)\n"
        "NRR: 118%, CAC payback: 14 months"
    ),
    "prior_period": "Q3 2025 revenue: $25.1M, EBITDA: $3.9M (15.5% margin)",
}

narrative = generate_narrative(financials, save_path="reports/Q4_2025_board_narrative.md")
print(narrative)
```

## What You Get

A board-ready narrative that explains the numbers rather than repeating them:

> **Q4 2025 beat revenue budget by 8.8%, driven by stronger-than-expected SaaS growth and best-in-class churn performance.**
>
> **Revenue** came in at **$28.4M**, 8.8% above the $26.1M budget and 19.3% above Q4 2024. The SaaS business — now 68% of total revenue — grew 22% year on year as the mid-market expansion strategy delivered 47 new logos against a budget of 40.
>
> **Margins** improved meaningfully. EBITDA margin of **18.3%** exceeded the 15.8% budget by 250bps, primarily from better-than-expected COGS efficiency and a $0.6M underspend in Sales & Marketing due to a delayed campaign now planned for Q1 2026...
