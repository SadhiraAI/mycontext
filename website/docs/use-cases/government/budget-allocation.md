---
sidebar_position: 6
title: Budget Allocation Analysis
description: Optimise public budget allocation across competing priorities using CostBenefitAnalyzer + ResourceAllocator + MultiObjectiveOptimizer. Blueprint with OutputEvaluator scoring.
---

# Budget Allocation Analysis

**Scenario:** A government department must allocate a fixed budget across multiple competing programmes. Each programme has different outcomes, beneficiary groups, and evidence bases. You want structured analysis that applies consistent cost-benefit methodology and optimises for multiple objectives (welfare, equity, efficiency, political feasibility).

**Patterns used:**
- `CostBenefitAnalyzer` (enterprise) — applies rigorous cost-benefit analysis to each programme option
- `ResourceAllocator` (enterprise) — optimises allocation across competing uses under constraints
- `MultiObjectiveOptimizer` (enterprise) — finds allocations that balance multiple competing objectives

**Integration:** Blueprint + `OutputEvaluator` to score the quality of the allocation analysis

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints
from mycontext.templates.enterprise.decision import (
    CostBenefitAnalyzer,
    ResourceAllocator,
    MultiObjectiveOptimizer,
)
from mycontext.intelligence import QualityMetrics, OutputEvaluator, TemplateIntegratorAgent

metrics = QualityMetrics(mode="heuristic")
evaluator = OutputEvaluator()

allocation_blueprint = Blueprint(
    name="public_budget_allocation",
    guidance=Guidance(
        role="Senior HM Treasury economist applying Green Book methodology",
        rules=[
            "Apply HM Treasury Green Book cost-benefit methodology",
            "Quantify benefits in common units where possible (lives saved, QALYs, employment)",
            "Identify distributional effects: who benefits and who pays",
            "Distinguish evidence-based programmes from those with weaker evidence",
            "Flag political feasibility as a constraint, not a reason to abandon analysis",
        ],
    ),
    directive_template=(
        "Analyse budget allocation options:\n\n"
        "Total budget: {total_budget}\n"
        "Objectives: {objectives}\n"
        "Constraints: {constraints}\n\n"
        "Programmes under consideration:\n{programmes}"
    ),
    constraints=Constraints(
        must_include=[
            "cost-benefit ratios",
            "distributional effects",
            "evidence quality",
            "recommended allocation",
            "sensitivity analysis",
        ],
        format_rules=["Programmes as a comparison table", "Recommendation with explicit reasoning"],
    ),
    token_budget=5000,
    optimization="quality",
)


def budget_allocation_analysis(budget_scenario: dict) -> dict:
    ctx = allocation_blueprint.build(**budget_scenario)
    score = metrics.evaluate(ctx)
    print(f"Context quality: {score.overall:.0%}")

    # Deep integration: all three patterns fused
    integrator = TemplateIntegratorAgent(provider="openai")
    result = integrator.integrate(
        templates=[CostBenefitAnalyzer, ResourceAllocator, MultiObjectiveOptimizer],
        input_data={
            "decision": f"Allocate {budget_scenario['total_budget']} across programmes",
            "context_section": f"Objectives: {budget_scenario['objectives']}\nConstraints: {budget_scenario['constraints']}",
        },
    )

    final = result.context.execute(provider="openai", model="gpt-4o").response
    output_score = evaluator.evaluate(context=result.context, output=final)
    print(f"Output quality: {output_score.overall:.0%}")

    return {
        "analysis": final,
        "output_quality": round(output_score.overall, 2),
    }


scenario = {
    "total_budget": "120 million GBP over 3 years",
    "objectives": "Reduce child poverty, improve educational attainment, reduce NHS demand, economic growth",
    "constraints": "Min 20% to early years. No single programme >40%. Must show measurable outcomes within 3 years.",
    "programmes": (
        "A) Universal Credit work support expansion (employment outcomes, 8M beneficiaries)\n"
        "B) Early years nursery expansion (child development, 250K places)\n"
        "C) NHS mental health waiting list reduction (health outcomes, IAPT expansion)\n"
        "D) Adult skills reskilling (productivity, 50K training places)\n"
        "E) Housing support for vulnerable families (stability, 15K families)"
    ),
}

analysis = budget_allocation_analysis(scenario)
print(analysis["analysis"])
print(f"\nOutput quality score: {analysis['output_quality']:.0%}")
```

## What You Get

A structured budget allocation analysis including:

- **Cost-benefit table:** each programme assessed on benefits per pound, evidence quality, and distributional effects
- **Multi-objective optimisation:** allocation that best balances welfare, equity, efficiency, and feasibility
- **Recommended allocation:** specific percentage splits with explicit reasoning
- **Sensitivity analysis:** how the recommendation changes if key assumptions shift
- **Output quality score:** the `OutputEvaluator` validates that the analysis itself meets standards before you use it

This is the difference between a political allocation and a defensible, evidence-based one.
