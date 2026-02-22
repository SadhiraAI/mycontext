# Context Amplification Index (CAI) – SDK Guide

The **Context Amplification Index (CAI)** measures how much a cognitive template improves LLM output quality compared to a raw, unstructured prompt.

**Formula:** `CAI = templated_score / raw_score` (per dimension and overall)

- **CAI > 1.0** → Template amplified output quality
- **CAI = 1.0** → No change
- **CAI < 1.0** → Template didn't help (or made it worse)

---

## Installation / Import

```python
from mycontext import ContextAmplificationIndex, CAIResult
```

---

## Basic Usage

### 1. Measure a single template

```python
cai = ContextAmplificationIndex(provider="openai")

result = cai.measure(
    question="Why are API response times 3x slower after deploy?",
    template_name="diagnostic_root_cause_analyzer",
    api_key="sk-...",
)

print(f"CAI: {result.cai_overall:.2f}x  ({result.verdict})")
```

**What it does:**  
Runs the same question twice (raw vs. template-built), scores both outputs, and computes the ratio.

### 2. Heuristic-only evaluation (no LLM, no API key)

```python
cai = ContextAmplificationIndex(provider="openai", eval_mode="heuristic")
result = cai._measure_heuristic_only(
    question="Why are API response times 3x slower?",
    template_name="diagnostic_root_cause_analyzer",
)
```

This compares **context quality** (raw question vs. assembled template), not actual LLM responses. Useful for quick, free checks.

### 3. Measure a chain vs. single template

```python
result = cai.measure_chain(
    question="Why are API response times 3x slower after deploy?",
    chain=["diagnostic_root_cause_analyzer", "options_comparison"],
    api_key="sk-...",
)
```

Compares output from an integrated chain of templates vs. using just the first template.

---

## Constructor Options

| Parameter   | Default      | Description                                      |
|------------|--------------|--------------------------------------------------|
| `provider` | `"openai"`   | LLM provider for execution                      |
| `eval_mode`| `"heuristic"`| Scoring: `"heuristic"` or LLM-based              |
| `model`    | `None`       | Optional model override for execution/eval       |

---

## CAIResult Fields

| Field            | Type                        | Description                          |
|------------------|-----------------------------|--------------------------------------|
| `question`       | `str`                       | The prompt/question used             |
| `template_name`  | `str`                       | Template or chain name                |
| `raw_output`     | `str`                       | Response from raw question            |
| `templated_output`| `str`                      | Response from template-built context |
| `raw_score`      | `OutputQualityScore`        | Quality score for raw output          |
| `templated_score`| `OutputQualityScore`        | Quality score for templated output    |
| `cai_overall`    | `float`                     | Overall CAI (templated/raw)           |
| `cai_dimensions` | `Dict[OutputDimension, float]` | CAI per quality dimension         |
| `verdict`        | `str`                       | `"significant lift"`, `"moderate lift"`, etc. |
| `metadata`       | `Dict[str, Any]`            | Extra info (provider, eval_mode, ...)|

---

## Verdict Thresholds

| CAI Range   | Verdict           |
|-------------|-------------------|
| ≥ 1.5       | significant lift  |
| ≥ 1.2       | moderate lift     |
| ≥ 1.05      | slight lift       |
| 0.95–1.05   | neutral           |
| < 0.95      | negative lift     |

---

## Generating a report

```python
report_text = cai.report(result)
print(report_text)
```

Prints a formatted CAI report including per-dimension scores and raw vs. templated overall percentages.

---

## Related types and exports

- `CAIResult` – Result of a CAI measurement
- `OutputQualityScore` / `OutputDimension` – Quality dimensions used in evaluation  
- See `docs/CAI_METRICS_EXPLAINED_SIMPLE.md` for kid-friendly descriptions of the five metrics.
