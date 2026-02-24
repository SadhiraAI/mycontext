---
sidebar_position: 3
title: Context Amplification Index
description: Measure how much a cognitive template lifts LLM output quality compared to a raw prompt. CAI > 1.0 means the template added value.
---

# Context Amplification Index (CAI)

The Context Amplification Index measures the quality lift a cognitive template provides over a raw, unstructured prompt. It runs the same question twice — once raw, once with the template — then computes the ratio.

```
CAI = templated_output_score / raw_output_score
```

- **CAI > 1.0** — the template improved output quality
- **CAI = 1.0** — neutral (template had no effect)
- **CAI < 1.0** — the template hurt output quality

```python
from mycontext.intelligence import ContextAmplificationIndex

cai = ContextAmplificationIndex(provider="openai")
result = cai.measure(
    question="Why are API response times 3x slower after the deploy?",
    template_name="root_cause_analyzer",
)

print(f"CAI: {result.cai_overall:.2f}x  ({result.verdict})")
print(cai.report(result))
```

Output:
```
CAI: 1.64x  (significant lift)
```

## Constructor

```python
ContextAmplificationIndex(
    provider: str = "openai",
    eval_mode: str = "heuristic",
    model: str | None = None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | `str` | `"openai"` | LLM provider for execution AND evaluation |
| `eval_mode` | `str` | `"heuristic"` | How to score outputs: `"heuristic"`, `"llm"`, `"hybrid"` |
| `model` | `str \| None` | `None` | Override model name |

## `measure()` — Single Template vs Raw

```python
result = cai.measure(
    question="Why are API response times 3x slower after the deploy?",
    template_name="root_cause_analyzer",
)
```

Runs two LLM calls:
1. Raw: `Context(directive=question).execute(provider=...)`
2. Templated: `RootCauseAnalyzer().build_context(problem=question).execute(provider=...)`

Then scores both with `OutputEvaluator` and returns the ratio.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The question to test |
| `template_name` | `str` | Pattern name (snake_case) |
| `model` | `str` | Override model (keyword arg) |
| `api_key` | `str` | Pass API key explicitly |

**Returns:** `CAIResult`

## `measure_chain()` — Chain vs Single Template

Compare a chain of templates against using only the first one:

```python
result = cai.measure_chain(
    question="Should we migrate our monolith to microservices?",
    chain=["decision_framework", "risk_assessor", "stakeholder_mapper"],
)

print(f"Chain CAI: {result.cai_overall:.2f}x  ({result.verdict})")
# Chain vs. just decision_framework
```

## CAIResult

```python
@dataclass
class CAIResult:
    question: str
    template_name: str           # Template tested (or "chain[...]")
    raw_output: str              # Raw LLM response
    templated_output: str        # Templated LLM response
    raw_score: OutputQualityScore
    templated_score: OutputQualityScore
    cai_overall: float           # templated / raw overall
    cai_dimensions: dict[OutputDimension, float]  # Per-dimension CAI
    verdict: str                 # Human-readable verdict
    metadata: dict
```

### CAI Verdicts

| CAI range | Verdict |
|-----------|---------|
| >= 1.5 | "significant lift" |
| >= 1.2 | "moderate lift" |
| >= 1.05 | "slight lift" |
| >= 0.95 | "neutral" |
| < 0.95 | "negative lift" |

## `report()` — Full CAI Report

```python
print(cai.report(result))
```

Output:
```
Context Amplification Index (CAI) Report
=========================================

Question: Why are API response times 3x slower after the deploy?...
Template: root_cause_analyzer
CAI Overall: 1.64x  (significant lift)

Per-Dimension CAI:
  Instruction Following: 1.80x  (raw=45.0% -> templated=81.0%)
  Reasoning Depth: 1.72x  (raw=38.0% -> templated=65.0%)
  Actionability: 1.55x  (raw=42.0% -> templated=65.0%)
  Structure Compliance: 1.40x  (raw=50.0% -> templated=70.0%)
  Cognitive Scaffolding: 1.63x  (raw=30.0% -> templated=49.0%)

Raw Overall:      43.8%
Templated Overall: 71.8%
```

## Examples

### Validate a New Pattern Before Shipping

```python
from mycontext.intelligence import ContextAmplificationIndex

cai = ContextAmplificationIndex(provider="openai", eval_mode="heuristic")

test_questions = [
    "Why did our mobile app crash rate spike 300%?",
    "What caused the database query times to increase?",
    "Why is our background job queue backing up?",
]

for question in test_questions:
    result = cai.measure(question, template_name="root_cause_analyzer")
    status = "PASS" if result.cai_overall >= 1.2 else "WARN" if result.cai_overall >= 1.0 else "FAIL"
    print(f"[{status}] CAI={result.cai_overall:.2f}x  ({result.verdict})")
    print(f"       Q: {question}")
```

### Compare Two Templates on the Same Question

```python
cai = ContextAmplificationIndex(provider="openai")

question = "Our enterprise customers are churning. Why and what do we do?"

r1 = cai.measure(question, template_name="root_cause_analyzer")
r2 = cai.measure(question, template_name="stakeholder_mapper")

print(f"root_cause_analyzer: {r1.cai_overall:.2f}x ({r1.verdict})")
print(f"stakeholder_mapper:  {r2.cai_overall:.2f}x ({r2.verdict})")
print(f"Winner: {'root_cause_analyzer' if r1.cai_overall > r2.cai_overall else 'stakeholder_mapper'}")
```

### Chain CAI vs. Single Template

```python
cai = ContextAmplificationIndex(provider="openai")

question = "Should we expand into the EU market next year?"

# Does the chain outperform the best single template?
single = cai.measure(question, template_name="decision_framework")
chain = cai.measure_chain(
    question=question,
    chain=["decision_framework", "risk_assessor", "scenario_planner"],
)

print(f"Single template CAI: {single.cai_overall:.2f}x")
print(f"Chain CAI:           {chain.cai_overall:.2f}x")
improvement = (chain.cai_overall / single.cai_overall - 1) * 100
print(f"Chain vs single:     +{improvement:.1f}%")
```

### Access Raw vs. Templated Outputs

```python
result = cai.measure("Why did our revenue drop?", template_name="root_cause_analyzer")

print("=== RAW OUTPUT ===")
print(result.raw_output[:500])

print("\n=== TEMPLATED OUTPUT ===")
print(result.templated_output[:500])

print(f"\nRaw score:      {result.raw_score.overall:.1%}")
print(f"Template score: {result.templated_score.overall:.1%}")
print(f"CAI:            {result.cai_overall:.2f}x")

# Per-dimension breakdown
from mycontext.intelligence import OutputDimension
for dim in OutputDimension:
    raw = result.raw_score.dimensions[dim]
    tmpl = result.templated_score.dimensions[dim]
    label = dim.value.replace("_", " ").title()
    print(f"  {label}: {raw:.1%} → {tmpl:.1%}  ({result.cai_dimensions[dim]:.2f}x)")
```

## Understanding CAI Numbers

A CAI of 1.64x means the template produced output scoring 64% higher on the evaluation rubric than the raw prompt. This is a composite of all five output dimensions.

High CAI dimensions tell you **where** the template adds the most value:

| High CAI dimension | Interpretation |
|-------------------|----------------|
| Instruction Following | Template's directive is much more specific |
| Reasoning Depth | Template enforces structured multi-step reasoning |
| Actionability | Template's framework produces concrete recommendations |
| Structure Compliance | Template defines output format; raw prompt doesn't |
| Cognitive Scaffolding | Template's methodology is reflected in the output |

## API Reference

### `ContextAmplificationIndex`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(provider, eval_mode, model)` | — | Initialize |
| `measure(question, template_name, **kwargs)` | `CAIResult` | Template vs raw |
| `measure_chain(question, chain, **kwargs)` | `CAIResult` | Chain vs single |
| `report(result)` | `str` | Human-readable report |

### `CAIResult`

| Field | Type | Description |
|-------|------|-------------|
| `question` | `str` | Test question |
| `template_name` | `str` | Template or chain tested |
| `raw_output` | `str` | Raw LLM response |
| `templated_output` | `str` | Template LLM response |
| `raw_score` | `OutputQualityScore` | Raw response scores |
| `templated_score` | `OutputQualityScore` | Template response scores |
| `cai_overall` | `float` | Overall CAI ratio |
| `cai_dimensions` | `dict[OutputDimension, float]` | Per-dimension ratios |
| `verdict` | `str` | "significant lift", "moderate lift", etc. |
