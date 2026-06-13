---
sidebar_position: 2
title: Credit Risk Assessment
description: Structure loan and credit decisions with RiskAssessor + RiskMitigator + ImpactAssessor + CausalReasoner. A Blueprint-based assessment that produces a scored risk report.
---

# Credit Risk Assessment

**Scenario:** Your credit team reviews dozens of loan applications daily. Reviews are inconsistent, risk factors are weighted differently by different analysts, and the reasoning is rarely documented. You want a structured assessment that applies the same analytical framework to every application and produces an auditable risk report.

**Patterns used:**
- `RiskAssessor` — evaluates risk dimensions and likelihood of adverse outcomes
- `RiskMitigator` — identifies what would reduce or offset each risk
- `ImpactAssessor` — quantifies the severity of each risk scenario
- `CausalReasoner` — maps the causal chain from risk factors to potential default

**Integration:** Blueprint + `to_openai()` direct call + JSON output

---

```python
import mycontext

from openai import OpenAI
from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints
from mycontext.templates.free.specialized import RiskAssessor
from mycontext.templates.enterprise.specialized import RiskMitigator, ImpactAssessor
from mycontext.templates.enterprise.reasoning import CausalReasoner
from mycontext.intelligence import QualityMetrics, TemplateIntegratorAgent
from mycontext.utils.parsers import JSONParser

client = OpenAI()
metrics = QualityMetrics(mode="heuristic")

credit_blueprint = Blueprint(
    name="credit_risk_assessment",
    guidance=Guidance(
        role="Senior credit risk analyst with 15 years of commercial lending experience",
        rules=[
            "Evaluate the 5 Cs: Character, Capacity, Capital, Collateral, Conditions",
            "Assign a risk score 1-10 for each dimension with explicit reasoning",
            "Identify the single most likely default scenario and its trigger chain",
            "Separate controllable from uncontrollable risk factors",
            "Never approve based on relationship alone — all decisions must be evidence-based",
        ],
    ),
    directive_template=(
        "Assess credit risk for this application:\n\n"
        "Business: {business_name} ({industry})\n"
        "Loan amount: {loan_amount}\n"
        "Purpose: {loan_purpose}\n"
        "Financial summary: {financials}\n"
        "Credit history: {credit_history}\n"
        "Collateral: {collateral}"
    ),
    constraints=Constraints(
        must_include=[
            "risk_score", "five_cs_breakdown", "key_risk_factors",
            "mitigants", "recommendation", "conditions_if_approved"
        ],
        format_rules=["Respond with JSON only"],
    ),
    token_budget=4000,
    optimization="quality",
)


def assess_credit_risk(application: dict) -> dict:
    ctx = credit_blueprint.build(**application)
    score = metrics.evaluate(ctx)
    print(f"Context quality: {score.overall:.0%}")

    oai_args = ctx.to_openai()
    response = client.chat.completions.create(
        **oai_args,
        model="gpt-4o",
        temperature=0,
        response_format={"type": "json_object"},
    )
    assessment = JSONParser(strict=False).parse(response.choices[0].message.content) or {}

    # Deep causal analysis for high-risk applications
    if assessment.get("risk_score", 0) >= 7:
        causal_ctx = CausalReasoner().build_context(
            phenomenon=f"Potential default on {application['loan_amount']} loan",
            context_section=f"Risk factors: {assessment.get('key_risk_factors', [])}",
        )
        causal_result = causal_ctx.execute(provider="openai", model="gpt-4o-mini")
        assessment["causal_default_chain"] = causal_result.response

    assessment["context_quality"] = round(score.overall, 2)
    assessment["application_id"] = application.get("application_id", "N/A")
    return assessment


application = {
    "application_id": "APP-2026-0342",
    "business_name": "Meridian Logistics Ltd",
    "industry": "freight and logistics",
    "loan_amount": "$2.4M over 7 years",
    "loan_purpose": "fleet expansion (12 heavy trucks)",
    "financials": "Revenue: $8.2M (2025), EBITDA margin: 11%, D/E ratio: 1.8, current ratio: 1.3",
    "credit_history": "No defaults, 2 late payments in 2023, existing $500K facility with 18 months remaining",
    "collateral": "12 trucks (estimated resale value $1.8M), personal guarantee from sole director",
}

result = assess_credit_risk(application)
print(f"Risk score: {result.get('risk_score')}/10")
print(f"Recommendation: {result.get('recommendation')}")
if result.get("conditions_if_approved"):
    print(f"Conditions: {result['conditions_if_approved']}")
```

## What You Get

A structured credit assessment with:
- **5 Cs breakdown** — each scored 1–10 with explicit reasoning
- **Key risk factors** — ranked by likelihood and severity
- **Mitigants** — what reduces each risk, including conditions you can attach
- **Causal default chain** — for high-risk applications, the step-by-step scenario from trigger to default
- **Recommendation** — approve / conditional / decline with documented basis

All outputs are JSON, making them directly ingestible into your loan origination system.

## Audit Trail

```python
import json, hashlib
from pathlib import Path

audit_record = {
    "application_id": result["application_id"],
    "assessment": result,
    "context_json": json.loads(ctx.to_json()),
    "model": "gpt-4o",
    "timestamp": "2026-02-03T09:14:00Z",
    "reviewed_by": None,
}
record_hash = hashlib.sha256(json.dumps(audit_record, sort_keys=True).encode()).hexdigest()
audit_record["integrity_hash"] = record_hash
Path(f"audit/{result['application_id']}.json").write_text(json.dumps(audit_record, indent=2))
```
