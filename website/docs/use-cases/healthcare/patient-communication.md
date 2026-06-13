---
sidebar_position: 3
title: Patient Communication Simplifier
description: Convert clinical discharge notes into plain language with SimplificationEngine + AudienceAdapter + ClarityOptimizer. Streaming FastAPI endpoint for patient portals.
---

# Patient Communication Simplifier

**Scenario:** Clinical discharge summaries are written for clinicians, not patients. Patients often do not understand their own discharge instructions, which leads to avoidable readmissions. You want to automatically translate clinical language into plain English calibrated to the patient's health literacy level.

:::warning
All outputs require review by a qualified clinician before being delivered to patients.
:::

**Patterns used:**
- `SimplificationEngine` — strips jargon without losing clinical accuracy
- `AudienceAdapter` — calibrates vocabulary and examples to the specific audience
- `ClarityOptimizer` — ensures instructions are unambiguous and actionable

**Integration:** Blueprint + LangChain streaming (FastAPI)

---

```python
import mycontext

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_openai import ChatOpenAI
from mycontext.templates.enterprise.communication import SimplificationEngine, ClarityOptimizer
from mycontext.templates.free.communication import AudienceAdapter
from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints
from mycontext.intelligence import QualityMetrics

app = FastAPI()
llm = ChatOpenAI(model="gpt-4o-mini", streaming=True, temperature=0.2)
metrics = QualityMetrics(mode="heuristic")

patient_blueprint = Blueprint(
    name="patient_communication",
    guidance=Guidance(
        role="Patient educator specialising in health communication",
        rules=[
            "Use grade 6-8 reading level unless specified otherwise",
            "Replace every medical term with a plain-language equivalent in brackets",
            "Make every instruction specific and actionable",
            "Use short sentences. One idea per sentence.",
            "Always include: what to do, when, why it matters, when to call the doctor",
        ],
    ),
    directive_template=(
        "Translate this clinical note for a patient:\n\n"
        "{clinical_note}\n\n"
        "Patient profile: {patient_profile}\n"
        "Include sections for: diagnosis explanation, medications, follow-up, warning signs"
    ),
    constraints=Constraints(
        must_include=["diagnosis in plain language", "medication instructions", "warning signs", "who to call"],
        must_not_include=["unexplained medical abbreviations", "Latin terms"],
        format_rules=["Use numbered lists for instructions", "Bold warning signs"],
    ),
    token_budget=2000,
    optimization="quality",
)


@app.post("/simplify")
async def simplify_note(clinical_note: str, patient_profile: str = "adult, standard literacy"):
    ctx = patient_blueprint.build(clinical_note=clinical_note, patient_profile=patient_profile)
    score = metrics.evaluate(ctx)
    if score.overall < 0.70:
        return {"error": f"Quality too low: {score.overall:.0%}", "issues": score.issues}

    messages = ctx.to_messages(user_message="Generate the patient communication now.")

    async def generate():
        async for chunk in llm.astream(messages):
            if chunk.content:
                yield chunk.content

    return StreamingResponse(generate(), media_type="text/plain")


# Standalone usage
def simplify_sync(clinical_note: str, patient_profile: str) -> str:
    ctx = patient_blueprint.build(
        clinical_note=clinical_note,
        patient_profile=patient_profile,
    )
    return ctx.execute(provider="openai").response


clinical_note = (
    "Pt is a 68F with PMHx of T2DM, HTN, and HFrEF (EF 35%) presenting with "
    "acute decompensated heart failure. Started on IV furosemide 80mg BID for diuresis. "
    "Transitioned to PO torsemide 40mg OD on discharge. Uptitrate Entresto to 97/103mg BID. "
    "F/U with cardiology in 2 weeks. Daily weights. Strict 2L fluid restriction. "
    "Sodium restriction 2g/day. If weight increases >2kg in 2 days, call office."
)

result = simplify_sync(clinical_note, "68-year-old retired teacher, comfortable reader")
print(result)
```

## What You Get

**Input (clinical):**
> "Uptitrate Entresto to 97/103mg BID. Strict 2L fluid restriction. If weight increases >2kg in 2 days, call office."

**Output (patient-friendly):**
> **Your Heart Medication — Entresto**
> Take one tablet in the morning and one in the evening.
> This medicine helps your heart pump more effectively.
>
> **How Much to Drink Each Day**
> Drink no more than 8 cups (2 litres) of liquid per day, including water, juice, soup, and tea.
>
> **Daily Weigh-In**
> Weigh yourself every morning. If your weight goes up by more than 2 kg in two days, **call us immediately**. This usually means fluid is building up in your body.

## Multilingual Extension

```python
ctx = patient_blueprint.build(
    clinical_note=clinical_note,
    patient_profile="Spanish-speaking patient, low health literacy",
)
ctx.constraints.format_rules.append("Translate entire output to Spanish")
result = ctx.execute(provider="openai").response
```
