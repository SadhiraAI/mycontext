---
sidebar_position: 4
title: Benchmarking
description: TemplateBenchmark runs automated YAML-defined test suites against cognitive templates, scoring output quality and computing CAI for each test case.
---

# Benchmarking

`TemplateBenchmark` runs automated test suites against cognitive templates. Each benchmark is a YAML file defining test questions, minimum score thresholds, and required output terms. The benchmark runs every test case and reports pass/fail rates, average quality scores, and CAI values.

```python
from mycontext.intelligence import TemplateBenchmark

bench = TemplateBenchmark(provider="openai")

result = bench.run("root_cause_analyzer")
print(f"Passed {result.passed}/{result.total_cases}")
print(f"Avg score: {result.avg_score:.1%}")
print(f"Avg CAI:   {result.avg_cai:.2f}x")
print(TemplateBenchmark.report(result))
```

## Constructor

```python
TemplateBenchmark(
    provider: str = "openai",
    eval_mode: str = "heuristic",
    benchmarks_dir: Path | None = None,
    model: str | None = None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | `str` | `"openai"` | LLM provider for execution and evaluation |
| `eval_mode` | `str` | `"heuristic"` | How to score outputs: `"heuristic"`, `"llm"`, `"hybrid"` |
| `benchmarks_dir` | `Path \| None` | SDK benchmarks dir | Custom directory for benchmark YAML files |
| `model` | `str \| None` | `None` | Override model name |

## Running Benchmarks

### `run(template_name)` — Single Template

```python
result = bench.run(
    "root_cause_analyzer",
    api_key="sk-...",   # Optional: pass API key explicitly
)
```

**Returns:** `BenchmarkResult`

### `run_all()` — All Templates

```python
all_results = bench.run_all()
for template_name, result in all_results.items():
    status = "PASS" if result.passed == result.total_cases else "PARTIAL"
    print(f"[{status}] {template_name}: {result.passed}/{result.total_cases} ({result.avg_cai:.2f}x CAI)")
```

**Returns:** `dict[str, BenchmarkResult]`

### `list_benchmarks()` — Discover Available Benchmarks

```python
available = bench.list_benchmarks()
print(available)
# → ['root_cause_analyzer', 'step_by_step_reasoner', 'hypothesis_generator', ...]
```

## Benchmark YAML Format

Benchmark files live at `src/mycontext/benchmarks/<template_name>.yaml`. Each file defines test cases:

```yaml
template: root_cause_analyzer
description: Benchmark for root cause analysis quality

test_cases:
  - question: "Why did our API response times triple after the last deployment?"
    expected:
      min_score: 0.60           # Minimum OutputEvaluator score (0.0–1.0)
      must_contain:             # Terms that must appear in the output
        - "root cause"
        - "recommendation"

  - question: "Our mobile app crash rate spiked 300% on iOS 17 devices."
    expected:
      min_score: 0.65
      must_contain:
        - "cause"
        - "impact"

  - question: "Database query times increased 10x after migrating to a new server."
    expected:
      min_score: 0.55
      must_contain:
        - "investigate"
```

### Writing Your Own Benchmarks

Create a YAML file in your benchmarks directory:

```yaml
template: my_custom_template
description: Tests for my domain-specific template

test_cases:
  - question: "Your test question here"
    expected:
      min_score: 0.60
      must_contain:
        - "term that must appear"
        - "another required term"
```

Then run with a custom directory:

```python
from pathlib import Path
from mycontext.intelligence import TemplateBenchmark

bench = TemplateBenchmark(
    provider="openai",
    benchmarks_dir=Path("./my-benchmarks"),
)
result = bench.run("my_custom_template")
```

## Result Objects

### `BenchmarkResult`

```python
@dataclass
class BenchmarkResult:
    template_name: str
    total_cases: int
    passed: int
    failed: int
    avg_score: float           # Average OutputEvaluator score across all cases
    avg_cai: float             # Average CAI across all cases
    per_case: list[CaseResult]
    metadata: dict             # Provider, eval_mode
```

### `CaseResult`

```python
@dataclass
class CaseResult:
    question: str
    passed: bool
    output_score: float        # OutputEvaluator score for this case
    cai: float                 # CAI for this case
    issues: list[str]          # Why it failed (empty if passed)
    details: dict              # raw_score, verdict
```

## `report()` — Detailed Report

```python
print(TemplateBenchmark.report(result))
```

Output:
```
Benchmark Report: root_cause_analyzer
======================================

Cases: 3  |  Passed: 3  |  Failed: 0
Avg Output Score: 71.4%
Avg CAI: 1.58x

  [PASS] Case 1: score=74.2%, CAI=1.71x
         Q: Why did our API response times triple after the last deployment?...
  [PASS] Case 2: score=69.8%, CAI=1.54x
         Q: Our mobile app crash rate spiked 300% on iOS 17 devices....
  [PASS] Case 3: score=70.3%, CAI=1.48x
         Q: Database query times increased 10x after migrating to a new server....
```

## Examples

### Regression Testing in CI

```python
import os
from mycontext.intelligence import TemplateBenchmark

def test_template_quality():
    bench = TemplateBenchmark(
        provider="openai",
        eval_mode="heuristic",
    )
    
    critical_templates = [
        "root_cause_analyzer",
        "risk_assessor",
        "decision_framework",
    ]
    
    for template_name in critical_templates:
        result = bench.run(template_name)
        
        # Assert minimum pass rate
        pass_rate = result.passed / result.total_cases if result.total_cases > 0 else 0
        assert pass_rate >= 0.80, (
            f"{template_name}: only {result.passed}/{result.total_cases} passed"
        )
        
        # Assert minimum average quality
        assert result.avg_score >= 0.60, (
            f"{template_name}: avg score {result.avg_score:.1%} below 60%"
        )
        
        # Assert positive CAI (template adds value)
        assert result.avg_cai >= 1.1, (
            f"{template_name}: CAI {result.avg_cai:.2f}x — template not adding value"
        )
        
        print(f"[PASS] {template_name}: {result.passed}/{result.total_cases}, "
              f"avg={result.avg_score:.1%}, CAI={result.avg_cai:.2f}x")
```

### Inspect Failures

```python
bench = TemplateBenchmark(provider="openai")
result = bench.run("risk_assessor")

for case in result.per_case:
    if not case.passed:
        print(f"FAILED: {case.question}")
        for issue in case.issues:
            print(f"  - {issue}")
        print(f"  Score: {case.output_score:.1%}, CAI: {case.cai:.2f}x")
        print(f"  Raw score was: {case.details.get('raw_score', 0):.1%}")
```

### Compare Two Models

```python
from mycontext.intelligence import TemplateBenchmark

template = "root_cause_analyzer"

bench_mini = TemplateBenchmark(provider="openai", model="gpt-4o-mini")
bench_full = TemplateBenchmark(provider="openai", model="gpt-4o")

r1 = bench_mini.run(template)
r2 = bench_full.run(template)

print(f"gpt-4o-mini: {r1.avg_score:.1%} avg score, {r1.avg_cai:.2f}x CAI")
print(f"gpt-4o:      {r2.avg_score:.1%} avg score, {r2.avg_cai:.2f}x CAI")
print(f"Quality delta: +{(r2.avg_score - r1.avg_score) * 100:.1f}%")
```

### Run Full Suite, Filter Poor Performers

```python
bench = TemplateBenchmark(provider="openai", eval_mode="heuristic")
all_results = bench.run_all()

print("Templates with CAI < 1.2 (may need improvement):")
for name, result in all_results.items():
    if result.total_cases > 0 and result.avg_cai < 1.2:
        print(f"  {name}: CAI={result.avg_cai:.2f}x, score={result.avg_score:.1%}")

print("\nTop performers by CAI:")
sorted_by_cai = sorted(
    [(n, r) for n, r in all_results.items() if r.total_cases > 0],
    key=lambda x: x[1].avg_cai,
    reverse=True,
)
for name, result in sorted_by_cai[:5]:
    print(f"  {name}: CAI={result.avg_cai:.2f}x, score={result.avg_score:.1%}")
```

## API Reference

### `TemplateBenchmark`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(provider, eval_mode, benchmarks_dir, model)` | — | Initialize |
| `run(template_name, **kwargs)` | `BenchmarkResult` | Run benchmark for one template |
| `run_all(**kwargs)` | `dict[str, BenchmarkResult]` | Run all available benchmarks |
| `list_benchmarks()` | `list[str]` | Names of available benchmark files |
| `report(result)` | `str` | Human-readable report (static method) |

### `BenchmarkResult`

| Field | Type | Description |
|-------|------|-------------|
| `template_name` | `str` | Template that was benchmarked |
| `total_cases` | `int` | Total test cases |
| `passed` | `int` | Cases that passed all criteria |
| `failed` | `int` | Cases that failed |
| `avg_score` | `float` | Average output quality score |
| `avg_cai` | `float` | Average Context Amplification Index |
| `per_case` | `list[CaseResult]` | Individual case results |

### `CaseResult`

| Field | Type | Description |
|-------|------|-------------|
| `question` | `str` | Test question |
| `passed` | `bool` | Whether all criteria were met |
| `output_score` | `float` | OutputEvaluator score |
| `cai` | `float` | CAI for this case |
| `issues` | `list[str]` | Failure reasons |
| `details` | `dict` | `raw_score`, `verdict` |
