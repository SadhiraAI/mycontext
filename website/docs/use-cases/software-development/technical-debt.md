---
sidebar_position: 5
title: Technical Debt Analysis
description: Scan a codebase module by module with BottleneckIdentifier + DependencyMapper + EfficiencyAnalyzer. Quality-gated batch pipeline produces a scored, ranked debt register.
---

# Technical Debt Analysis

**Scenario:** You have a legacy codebase and vague agreement that "tech debt is bad" but no systematic picture of where it lives, what it costs, or what to fix first. You want a structured, repeatable analysis that produces a ranked debt register across modules.

**Patterns used:**
- `BottleneckIdentifier` (enterprise) — finds complexity, coupling, or inefficiency that creates friction
- `DependencyMapper` (enterprise) — maps hidden dependencies that make changes risky
- `EfficiencyAnalyzer` (enterprise) — assesses operational and development efficiency costs

**Integration:** Blueprint for consistent per-module analysis + `QualityMetrics` quality gate + JSON report

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

import json
from pathlib import Path
from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints
from mycontext.templates.enterprise.problem_solving import (
    BottleneckIdentifier,
    DependencyMapper,
    EfficiencyAnalyzer,
)
from mycontext.intelligence import QualityMetrics, ContextAmplificationIndex

debt_blueprint = Blueprint(
    name="tech_debt_scanner",
    guidance=Guidance(
        role="Staff engineer specializing in legacy system modernization",
        rules=[
            "Score debt severity 1-10 with explicit reasoning",
            "Identify the specific change that would remove each debt item",
            "Estimate effort: hours for small, days for medium, weeks for large",
            "Flag blast radius: what breaks if you change this",
        ],
    ),
    directive_template=(
        "Analyze technical debt in this module:\n\n"
        "Module: {module_name}\n"
        "Language: {language}\n"
        "Description: {description}\n\n"
        "Code:\n```{language}\n{code}\n```"
    ),
    constraints=Constraints(
        must_include=["debt_score", "bottlenecks", "dependencies", "effort_estimate", "priority"],
        format_rules=["Respond with JSON only"],
    ),
    token_budget=3000,
    optimization="cost",
)


def analyze_codebase(modules: list[dict]) -> dict:
    metrics = QualityMetrics(mode="heuristic")
    results = []
    skipped = []

    for mod in modules:
        ctx = debt_blueprint.build(
            module_name=mod["name"],
            language=mod["language"],
            description=mod["description"],
            code=mod["code"][:3000],
        )

        score = metrics.evaluate(ctx)
        if score.overall < 0.55:
            skipped.append(mod["name"])
            continue

        result = ctx.execute(provider="openai", model="gpt-4o-mini")

        from mycontext.utils.parsers import JSONParser
        data = JSONParser(strict=False).parse(result.response) or {}
        data["module"] = mod["name"]
        data["context_quality"] = round(score.overall, 2)
        results.append(data)

    results.sort(key=lambda x: x.get("debt_score", 0), reverse=True)

    return {
        "total_modules": len(modules),
        "analyzed": len(results),
        "skipped": skipped,
        "debt_register": results,
        "top_priority": results[:3] if results else [],
    }


modules = [
    {
        "name": "payment_processor",
        "language": "Python",
        "description": "Handles payment transactions with legacy Stripe integration",
        "code": Path("src/payments/processor.py").read_text(),
    },
    {
        "name": "user_auth",
        "language": "Python",
        "description": "JWT auth with hardcoded secrets and no refresh token support",
        "code": Path("src/auth/handler.py").read_text(),
    },
]

report = analyze_codebase(modules)
Path("debt_report.json").write_text(json.dumps(report, indent=2))

print(f"Analyzed {report['analyzed']}/{report['total_modules']} modules")
print("\nTop 3 debt items:")
for item in report["top_priority"]:
    print(f"  [{item.get('debt_score', '?')}/10] {item['module']}")
```

## Deeper Analysis with All Three Patterns

For a single high-risk module, run all three patterns and compare perspectives:

```python
code_sample = Path("src/payments/processor.py").read_text()

bottleneck_ctx = BottleneckIdentifier().build_context(
    system="payment service", process=code_sample
)
dependency_ctx = DependencyMapper().build_context(
    project="payment processor", objective="understand coupling risks"
)
efficiency_ctx = EfficiencyAnalyzer().build_context(
    process=code_sample, objective="find development efficiency costs"
)

for name, ctx in [("bottleneck", bottleneck_ctx), ("dependency", dependency_ctx), ("efficiency", efficiency_ctx)]:
    result = ctx.execute(provider="openai", model="gpt-4o-mini")
    print(f"\n=== {name.upper()} ===")
    print(result.response[:500])
```

## What You Get

- Per-module debt score (1-10) with specific bottleneck descriptions
- Dependency risk map: which modules are tightly coupled and why that matters
- Effort estimates per debt item (hours/days/weeks)
- Prioritized top-3 fix list for sprint planning
- Reproducible: run the same analysis next quarter and compare scores
