---
sidebar_position: 6
title: Clinical Note Error Detection
description: Scan clinical notes for inconsistencies, contradictions, and omissions using ErrorDetectionFramework + DiagnosticRootCauseAnalyzer + SystemHealthAuditor. Blueprint with OutputEvaluator scoring.
---

# Clinical Note Error Detection

**Scenario:** Clinical notes contain errors: medications listed without dosages, contradictions between history and assessment, missing allergy documentation, or discrepancies between note sections. Catching these manually is time-consuming. You want an automated scan that flags issues for clinician review before notes are finalised.

**Patterns used:**
- `ErrorDetectionFramework` — systematically identifies errors, omissions, and inconsistencies
- `DiagnosticRootCauseAnalyzer` — traces each error to its likely cause
- `SystemHealthAuditor` — assesses the overall completeness and reliability of the note

**Integration:** Blueprint + `OutputEvaluator` to score the quality of the scan itself

---

```python
import mycontext

from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints
from mycontext.templates.enterprise.metacognition import ErrorDetectionFramework
from mycontext.templates.enterprise.diagnostic import (
    DiagnosticRootCauseAnalyzer,
    SystemHealthAuditor,
)
from mycontext.intelligence import QualityMetrics, OutputEvaluator
from mycontext.utils.parsers import JSONParser

metrics = QualityMetrics(mode="heuristic")
evaluator = OutputEvaluator()

note_audit_blueprint = Blueprint(
    name="clinical_note_auditor",
    guidance=Guidance(
        role="Clinical documentation specialist and patient safety officer",
        rules=[
            "Flag every inconsistency between note sections",
            "Identify missing mandatory elements (allergies, code status, medication doses)",
            "Flag contradictions between subjective, objective, assessment, and plan sections",
            "Assign severity: Critical (must fix before signing), Major, Minor",
            "Do not suggest clinical decisions -- only documentation completeness issues",
        ],
    ),
    directive_template=(
        "Audit this clinical note for documentation errors and omissions:\n\n"
        "Note type: {note_type}\n\n"
        "{clinical_note}"
    ),
    constraints=Constraints(
        must_include=["critical_issues", "major_issues", "minor_issues", "completeness_score"],
        format_rules=["Respond with JSON only"],
    ),
    token_budget=3000,
    optimization="quality",
)


def audit_clinical_note(note: str, note_type: str = "Discharge Summary") -> dict:
    # Stage 1: Error detection pass
    ctx = note_audit_blueprint.build(clinical_note=note, note_type=note_type)
    score = metrics.evaluate(ctx)
    print(f"Context quality: {score.overall:.0%}")

    result = ctx.execute(provider="openai", model="gpt-4o-mini")
    parsed = JSONParser(strict=False).parse(result.response) or {}

    # Stage 2: Evaluate the audit output quality
    output_score = evaluator.evaluate(context=ctx, output=result.response)
    print(f"Audit output quality: {output_score.overall:.0%}")

    # Stage 3: Root cause trace for critical issues
    critical = parsed.get("critical_issues", [])
    root_causes = {}
    if critical:
        rca_ctx = DiagnosticRootCauseAnalyzer().build_context(
            observation=f"Critical documentation errors found:\n" + "\n".join(str(i) for i in critical),
            system="clinical documentation workflow",
        )
        rca_result = rca_ctx.execute(provider="openai", model="gpt-4o-mini")
        root_causes = {"analysis": rca_result.response}

    # Stage 4: Overall note health score
    health_ctx = SystemHealthAuditor().build_context(
        system="clinical note",
        observation=note,
    )
    health_result = health_ctx.execute(provider="openai", model="gpt-4o-mini")

    return {
        "issues": parsed,
        "completeness_score": parsed.get("completeness_score", "N/A"),
        "critical_count": len(critical),
        "root_causes": root_causes,
        "overall_health": health_result.response[:300],
        "audit_quality": round(output_score.overall, 2),
        "requires_review": len(critical) > 0,
    }


# Example note with deliberate errors
clinical_note = """
DISCHARGE SUMMARY
Patient: John D., 54M
Admitted: 2026-01-28 | Discharged: 2026-01-31

HPI: Patient admitted with chest pain. Cardiac workup negative.

PMH: Hypertension, diabetes (on metformin -- dose not documented), 
     penicillin allergy (reaction type not documented)

Assessment: Musculoskeletal chest pain. Plan to discharge on NSAIDs.

Medications on Discharge:
- Ibuprofen 400mg TID (no duration specified)
- Continue home medications

Follow-up: Primary care (no timeframe given)

Code status: Not documented
"""

audit = audit_clinical_note(clinical_note, "Discharge Summary")

print(f"\nCompleteness: {audit['completeness_score']}")
print(f"Critical issues: {audit['critical_count']}")
print(f"Requires review: {audit['requires_review']}")

if audit["issues"].get("critical_issues"):
    print("\nCritical issues:")
    for issue in audit["issues"]["critical_issues"]:
        print(f"  CRITICAL: {issue}")
```

## What Gets Flagged

In the example note above, the system catches:

| Severity | Issue |
|----------|-------|
| **Critical** | NSAIDs prescribed despite undocumented penicillin allergy (cross-reactivity risk documentation gap) |
| **Critical** | Code status not documented |
| **Major** | Metformin dose not specified |
| **Major** | Ibuprofen duration not specified |
| **Major** | Allergy reaction type not documented |
| **Minor** | Follow-up timeframe missing |

## Workflow Integration

```python
# Batch scan all unsigned notes
from pathlib import Path

unsigned_notes = Path("notes/unsigned/").glob("*.txt")
for note_file in unsigned_notes:
    note = note_file.read_text()
    audit = audit_clinical_note(note)
    if audit["requires_review"]:
        print(f"HOLD: {note_file.name} — {audit['critical_count']} critical issues")
```
