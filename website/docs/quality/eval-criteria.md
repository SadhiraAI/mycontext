---
sidebar_position: 6
title: Eval Criteria
description: Pre-built LLM-judge rubrics for DeepEval GEval — ten research-backed criteria organized into five bundles.
---

# Eval Criteria

`eval_criteria` provides a catalog of pre-built `GEvalCriteria` objects for use with [DeepEval's](https://github.com/confident-ai/deepeval) `GEval` metric. Each criterion is an LLM-judge rubric — a name, scoring steps, and threshold — validated against mycontext's own template evaluation experiments.

:::note Optional dependency
`eval_criteria` requires DeepEval: `pip install deepeval`. It is not needed for `QualityMetrics` or `OutputEvaluator`, which run without any extra dependencies.
:::

## When to use this (vs the native evaluators)

| Tool | When to use |
|------|-------------|
| `QualityMetrics` | Score any prompt/context on 6 dimensions — instant, no LLM call, use in every experiment |
| `OutputEvaluator` | Score LLM output on 5 dimensions — fast heuristic, use in every experiment |
| `eval_criteria` + DeepEval | Validate specific behavioral properties (gap honesty, causation discipline) on a sample — use when you need LLM-judge confidence on a targeted criterion |

## Import

```python
from mycontext.intelligence import get_criteria, to_deepeval_metrics
from mycontext.intelligence.eval_criteria import (
    EVIDENCE_CITATION,
    CAUSATION_DISCIPLINE,
    DATA_GAP_HONESTY,
    INSTRUCTION_ADHERENCE,
    ACTIONABILITY,
    REASONING_SOUNDNESS,
    STRUCTURE_COMPLIANCE,
    COGNITIVE_SCAFFOLDING_USE,
    CODE_REVIEW_SEVERITY_ACCURACY,
    CODE_REVIEW_ACTIONABILITY,
)
```

## The ten criteria

| Criterion | Bundle | What it measures |
|-----------|--------|-----------------|
| `EVIDENCE_CITATION` | `data_analysis`, `reasoning` | Does every claim cite the specific data point supporting it? |
| `CAUSATION_DISCIPLINE` | `data_analysis`, `reasoning` | Does the response avoid inferring causation from correlation? |
| `DATA_GAP_HONESTY` | `data_analysis` | Does the response explicitly name what data is missing and what that prevents? |
| `INSTRUCTION_ADHERENCE` | `instruction_following`, `general` | Does the output follow all explicit instructions in the context? |
| `ACTIONABILITY` | `general` | Are recommendations specific enough to act on without further research? |
| `REASONING_SOUNDNESS` | `reasoning` | Is the reasoning chain logically valid and free of fallacies? |
| `STRUCTURE_COMPLIANCE` | `instruction_following` | Does the output match the requested format/structure? |
| `COGNITIVE_SCAFFOLDING_USE` | `general` | Does the output use the reasoning framework specified in the template? |
| `CODE_REVIEW_SEVERITY_ACCURACY` | `code_review` | Are severity labels (critical/medium/low) applied correctly? |
| `CODE_REVIEW_ACTIONABILITY` | `code_review` | Does each finding include a concrete, executable fix? |

## Using a bundle

```python
from mycontext.intelligence import get_criteria, to_deepeval_metrics

criteria = get_criteria("data_analysis")
# → [EVIDENCE_CITATION, CAUSATION_DISCIPLINE, DATA_GAP_HONESTY]

metrics = to_deepeval_metrics(criteria)
# → list[deepeval.metrics.GEval]
```

## Full example with DeepEval

```python
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from mycontext.intelligence import get_criteria, to_deepeval_metrics
from mycontext.templates.free.analysis import DataAnalyzer

template = DataAnalyzer()
ctx = template.build_context(dataset_description="Monthly sales by product line, Q1–Q4 2024")
response = ctx.execute(provider="openai")

test_case = LLMTestCase(
    input=ctx.assemble(),
    actual_output=response.response,
)

metrics = to_deepeval_metrics(get_criteria("data_analysis"))
evaluate([test_case], metrics)
```

## Using individual criteria

```python
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams
from mycontext.intelligence.eval_criteria import DATA_GAP_HONESTY

metric = GEval(
    name=DATA_GAP_HONESTY.name,
    evaluation_steps=DATA_GAP_HONESTY.evaluation_steps,
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=DATA_GAP_HONESTY.threshold,
)
```

## Using as a quality gate in experiments

```python
from mycontext.intelligence import QualityMetrics, OutputEvaluator, get_criteria, to_deepeval_metrics

qm = QualityMetrics()
evaluator = OutputEvaluator()

# Step 1: fast heuristic pass (always)
prompt_score = qm.evaluate(ctx)
output_score = evaluator.evaluate(ctx, response.response)

# Step 2: targeted LLM-judge pass (on samples that pass step 1)
if output_score.overall > 0.70:
    metrics = to_deepeval_metrics(get_criteria("data_analysis"))
    # run deepeval evaluate(...) on this sample
```

## See also

- [Prompt Optimization Workflow](./prompt-optimization-workflow) — where these criteria fit in the full workflow
- [OutputEvaluator](./output-evaluator) — the primary (heuristic) output evaluation tool
- [QualityMetrics](./quality-metrics) — the primary (heuristic) prompt quality tool
