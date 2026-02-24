---
sidebar_position: 5
title: Regulatory Impact Assessment
description: Assess the impact of proposed regulation using ImpactAssessor + ConsequentialistAnalyzer + StakeholderEthicsAssessor. Raw Context with QualityMetrics CI quality gate.
---

# Regulatory Impact Assessment

**Scenario:** A policy team or affected business needs to assess the full impact of proposed legislation or regulatory change. Beyond "what does this cost us" — they need to understand second-order effects, stakeholder impacts, and whether the regulation achieves its stated ethical objectives.

**Patterns used:**
- `ImpactAssessor` (enterprise) — maps direct, indirect, and second-order impacts
- `ConsequentialistAnalyzer` (enterprise) — evaluates outcomes across all affected parties
- `StakeholderEthicsAssessor` (enterprise) — assesses the regulation from each stakeholder's ethical position

**Integration:** Raw `Context` with `QualityMetrics` gate — suitable for CI/CD policy review pipelines

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from mycontext import Context
from mycontext.foundation import Guidance, Directive, Constraints
from mycontext.templates.enterprise.specialized import ImpactAssessor
from mycontext.templates.enterprise.ethical_reasoning import (
    ConsequentialistAnalyzer,
    StakeholderEthicsAssessor,
)
from mycontext.intelligence import QualityMetrics, OutputEvaluator

metrics = QualityMetrics(mode="heuristic")
evaluator = OutputEvaluator()

QUALITY_GATE = 0.72


def regulatory_impact_assessment(proposal: dict) -> dict:
    brief = "\n".join(f"{k}: {v}" for k, v in proposal.items())

    impact_ctx = ImpactAssessor().build_context(
        situation=brief,
        context_section="Assess direct, indirect, and second-order impacts over 1, 3, and 10 years",
    )
    consequentialist_ctx = ConsequentialistAnalyzer().build_context(
        situation=brief,
        context_section="Evaluate outcomes for each affected group. Does aggregate welfare improve?",
    )
    ethics_ctx = StakeholderEthicsAssessor().build_context(
        situation=brief,
        context_section=f"Stakeholders: {proposal.get('stakeholders', 'all affected parties')}",
    )

    results = {}
    for name, ctx in [
        ("impact", impact_ctx),
        ("consequentialist", consequentialist_ctx),
        ("ethics", ethics_ctx),
    ]:
        score = metrics.evaluate(ctx)
        print(f"  {name}: {score.overall:.0%}")
        if score.overall < QUALITY_GATE:
            print(f"  BLOCKED — quality below {QUALITY_GATE:.0%}")
            results[name] = None
            continue

        result = ctx.execute(provider="openai", model="gpt-4o")
        output_score = evaluator.evaluate(context=ctx, output=result.response)
        results[name] = {
            "analysis": result.response,
            "output_quality": round(output_score.overall, 2),
        }

    # Save context serializations for audit trail
    audit = {
        "proposal": proposal,
        "contexts": {
            name: ctx.to_dict()
            for name, ctx in [
                ("impact", impact_ctx),
                ("consequentialist", consequentialist_ctx),
                ("ethics", ethics_ctx),
            ]
        },
        "results": results,
    }

    return audit


proposal = {
    "regulation": "Mandatory AI Impact Assessment Act 2026",
    "summary": (
        "All companies with >50 employees must conduct and publish an AI Impact Assessment "
        "before deploying any AI system that makes or assists in decisions affecting employees, "
        "customers, or members of the public."
    ),
    "affected_sectors": "Technology, financial services, healthcare, retail, government",
    "timeline": "18 months to compliance",
    "enforcement": "Fines up to 4% of annual global turnover for non-compliance",
    "stakeholders": (
        "Large enterprises, SMEs, AI vendors, affected individuals, "
        "regulators, civil society, workers"
    ),
}

assessment = regulatory_impact_assessment(proposal)
print(assessment["results"]["impact"]["analysis"][:800])
print("\n=== CONSEQUENTIALIST ANALYSIS ===")
print(assessment["results"]["consequentialist"]["analysis"][:600])
```

## What You Get

A three-dimensional regulatory impact assessment:

| Dimension | Content |
|-----------|---------|
| **Impact map** | Direct costs, compliance burden, 1/3/10-year effects, unintended consequences |
| **Consequentialist analysis** | Net welfare assessment: who wins, who loses, whether aggregate outcomes justify the regulation |
| **Stakeholder ethics** | How each stakeholder group is affected, whose interests are prioritised, ethical tensions |

The output includes a full audit trail (serialized contexts, quality scores) suitable for regulatory submissions.
