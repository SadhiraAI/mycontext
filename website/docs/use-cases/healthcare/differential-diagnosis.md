---
sidebar_position: 2
title: Differential Diagnosis Support
description: Structure clinical reasoning with DifferentialDiagnoser + RiskMitigator + AnomalyDetector. A quality-gated decision support tool that surfaces what to rule out first.
---

# Differential Diagnosis Support

**Scenario:** A clinician is working through a complex presentation with multiple plausible diagnoses. They want structured clinical reasoning support that considers the full differential, flags atypical features, and prioritizes which diagnoses to rule out first based on urgency and treatability.

:::warning
This tool is for decision support only. All outputs require review by a qualified clinician before influencing patient care.
:::

**Patterns used:**
- `DifferentialDiagnoser` (enterprise) — applies systematic differential diagnosis methodology
- `RiskMitigator` (enterprise) — identifies what happens if high-risk diagnoses are missed
- `AnomalyDetector` (enterprise) — flags atypical features that don't fit the most obvious diagnosis

**Integration:** Raw `Context` + strict quality gate + `to_anthropic()` for Claude's longer reasoning

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from anthropic import Anthropic
from mycontext.templates.enterprise.diagnostic import DifferentialDiagnoser
from mycontext.templates.enterprise.specialized import RiskMitigator
from mycontext.templates.enterprise.analysis import AnomalyDetector
from mycontext.intelligence import QualityMetrics, TemplateIntegratorAgent

client = Anthropic()
metrics = QualityMetrics(mode="heuristic")

MINIMUM_QUALITY = 0.75  # Higher bar for clinical contexts


def differential_support(presentation: dict) -> dict:
    """
    presentation = {
        "chief_complaint": "chest pain, 3 hours",
        "history": "65yo male, hypertension, diabetes. Radiating to left arm. Diaphoresis.",
        "vitals": "BP 160/95, HR 102, O2 sat 96%, Temp 37.1",
        "labs": "Troponin I: 0.08 (borderline), ECG: ST depression V4-V6",
        "current_meds": "Metformin, Lisinopril",
    }
    """
    clinical_summary = "\n".join(f"{k}: {v}" for k, v in presentation.items())

    # Stage 1: Differential diagnosis
    diff_ctx = DifferentialDiagnoser().build_context(
        observation=clinical_summary,
        system="adult emergency medicine",
    )
    diff_score = metrics.evaluate(diff_ctx)
    if diff_score.overall < MINIMUM_QUALITY:
        raise ValueError(f"Differential context quality too low: {diff_score.overall:.0%}. Do not proceed.")

    # Stage 2: Risk stratification — what must NOT be missed
    risk_ctx = RiskMitigator().build_context(
        challenge=f"Managing patient with: {presentation['chief_complaint']}",
        context_section=clinical_summary,
    )

    # Stage 3: Anomaly detection — what doesn't fit
    anomaly_ctx = AnomalyDetector().build_context(
        data_description=clinical_summary,
        context_section="Identify features atypical for the leading diagnosis",
    )

    results = {}

    # Use Claude for clinical reasoning (longer context window, stronger reasoning)
    for name, ctx in [("differential", diff_ctx), ("risk", risk_ctx), ("anomalies", anomaly_ctx)]:
        score = metrics.evaluate(ctx)
        print(f"  {name}: quality {score.overall:.0%}")
        if score.overall < MINIMUM_QUALITY:
            results[name] = f"SKIPPED — quality {score.overall:.0%}"
            continue

        anthropic_args = ctx.to_anthropic()
        response = client.messages.create(
            **anthropic_args,
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": "Provide your analysis now."}],
        )
        results[name] = response.content[0].text

    return results


# Example clinical case
presentation = {
    "chief_complaint": "Chest pain for 3 hours",
    "history": "65-year-old male with hypertension and type 2 diabetes. Pain is substernal, radiating to left arm. Associated diaphoresis. No fever.",
    "vitals": "BP 162/94, HR 104 bpm, RR 18, O2 sat 96% on room air, Temp 37.0C",
    "labs": "Troponin I: 0.08 ng/mL (borderline high). ECG: ST depression V4-V6, no LBBB.",
    "current_meds": "Metformin 1000mg BD, Lisinopril 10mg OD",
}

analysis = differential_support(presentation)

print("\n=== DIFFERENTIAL DIAGNOSIS ===")
print(analysis["differential"][:800])
print("\n=== MUST-NOT-MISS CONDITIONS ===")
print(analysis["risk"][:500])
print("\n=== ATYPICAL FEATURES ===")
print(analysis["anomalies"][:400])
```

## What You Get

Three structured outputs that support the clinician's reasoning:

| Output | Content |
|--------|---------|
| **Differential** | Ranked list of diagnoses, likelihood assessment, key discriminating features for each |
| **Must-not-miss** | High-urgency diagnoses that must be ruled out first, with consequences of missing each |
| **Anomalies** | Features in the presentation that don't fit the leading diagnosis — flags for further investigation |

## Integration with EHR Systems

The context serializes cleanly for audit trails:

```python
import json
from pathlib import Path

# Save context + result for audit trail
audit = {
    "patient_id": "ANON-12345",
    "context_used": json.loads(diff_ctx.to_json()),
    "quality_score": diff_score.overall,
    "output": analysis["differential"],
    "timestamp": "2026-02-03T14:32:00Z",
    "reviewed_by": None,  # Clinician fills this in
}
Path(f"audit/diag_{audit['patient_id']}.json").write_text(json.dumps(audit, indent=2))
```
