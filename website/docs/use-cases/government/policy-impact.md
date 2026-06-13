---
sidebar_position: 2
title: Policy Impact Analysis
description: Assess proposed policy using ImpactAssessor + ConsequentialistAnalyzer + StakeholderEthicsAssessor. Raw Context with full JSON audit trail for public consultation.
---

# Policy Impact Analysis

**Scenario:** A government agency is evaluating proposed legislation. They need to assess who is affected, how, at what cost, and whether the policy achieves its stated objectives without harmful unintended consequences. The analysis must be documentable and auditable.

**Patterns used:**
- `ImpactAssessor` — maps direct, indirect, and second-order impacts across time horizons
- `ConsequentialistAnalyzer` — evaluates net welfare outcomes across affected groups
- `StakeholderEthicsAssessor` — assesses the policy from each stakeholder's ethical position

**Integration:** Raw Context builds + `QualityMetrics` gate + JSON audit trail

---

```python
import mycontext

import json
from pathlib import Path
from datetime import datetime
from mycontext.templates.enterprise.specialized import ImpactAssessor
from mycontext.templates.enterprise.ethical_reasoning import (
    ConsequentialistAnalyzer,
    StakeholderEthicsAssessor,
)
from mycontext.intelligence import QualityMetrics, OutputEvaluator

metrics = QualityMetrics(mode="heuristic")
evaluator = OutputEvaluator()
QUALITY_GATE = 0.72


def policy_impact_analysis(policy: dict, output_dir: str = "policy_assessments") -> dict:
    policy_brief = "\n".join(f"{k}: {v}" for k, v in policy.items())

    contexts = {
        "impact": ImpactAssessor().build_context(
            situation=policy_brief,
            context_section="Assess impacts at 1, 3, and 10 years. Include unintended consequences.",
        ),
        "consequentialist": ConsequentialistAnalyzer().build_context(
            situation=policy_brief,
            context_section="Which groups benefit? Which bear costs? Is aggregate welfare improved?",
        ),
        "stakeholder_ethics": StakeholderEthicsAssessor().build_context(
            situation=policy_brief,
            context_section=f"Key stakeholders: {policy.get('affected_groups', 'all affected parties')}",
        ),
    }

    results = {}
    for name, ctx in contexts.items():
        score = metrics.evaluate(ctx)
        print(f"  {name}: {score.overall:.0%}")
        if score.overall < QUALITY_GATE:
            results[name] = {"status": f"BLOCKED quality {score.overall:.0%}"}
            continue
        response = ctx.execute(provider="openai", model="gpt-4o").response
        output_score = evaluator.evaluate(context=ctx, output=response)
        results[name] = {
            "analysis": response,
            "context_quality": round(score.overall, 2),
            "output_quality": round(output_score.overall, 2),
        }

    audit = {
        "policy_id": policy.get("id", "POLICY-" + datetime.now().strftime("%Y%m%d")),
        "policy": policy,
        "timestamp": datetime.now().isoformat(),
        "contexts": {name: json.loads(ctx.to_json()) for name, ctx in contexts.items()},
        "results": results,
    }

    Path(output_dir).mkdir(exist_ok=True)
    Path(f"{output_dir}/{audit['policy_id']}.json").write_text(json.dumps(audit, indent=2))
    return results


policy = {
    "id": "POLICY-2026-AI-001",
    "title": "Mandatory AI Transparency Act 2026",
    "summary": (
        "All public-facing AI systems deployed by organisations with >100 employees "
        "must disclose: that AI is in use, the decision criteria, and a human review option. "
        "Non-compliance fines: up to 2% of annual global turnover."
    ),
    "affected_groups": "Large tech companies, SMEs, consumers, AI vendors, regulators",
    "stated_objective": "Increase public trust in AI and protect citizens from unexplained automated decisions",
    "timeline": "12 months to compliance",
}

assessment = policy_impact_analysis(policy)
print("=== IMPACT ===")
print(assessment["impact"]["analysis"][:700])
print("\n=== STAKEHOLDER ETHICS ===")
print(assessment["stakeholder_ethics"]["analysis"][:500])
```

## What You Get

- **Impact map:** direct costs, compliance burden, consumer benefits, 1/3/10-year projections, unintended consequences
- **Consequentialist analysis:** net welfare assessment — who benefits and who bears costs, and is the distribution equitable?
- **Stakeholder ethics:** how each group is affected, whose interests the policy prioritises, ethical tensions
- **Full audit trail:** serialized contexts, quality scores, model used — suitable for public consultation submissions
