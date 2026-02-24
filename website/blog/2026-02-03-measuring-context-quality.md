---
slug: measuring-context-quality
title: "We Finally Have a Way to Measure Context Quality. Here's How We Built It."
authors: [dhiraj]
tags: [quality-metrics, context-engineering, measurement, mycontext-ai]
date: 2026-02-03
---

One of the most frustrating things about LLM development is how hard it is to improve anything systematically. You change a prompt, run it a few times, look at the outputs, form a vague impression, and maybe change it again. It's slow, it's subjective, and it doesn't scale.

The underlying problem is that you're evaluating outputs without measuring the thing that produced them. You're doing quality assurance on finished goods without any inspection of the manufacturing process.

We built the quality measurement tools in mycontext-ai specifically to fix this. And it changed how I think about context development more than any other feature.

<!-- truncate -->

## Why measuring prompts is hard

The standard approach to LLM quality measurement focuses entirely on outputs. You write test cases, run your prompts against them, judge the outputs (sometimes with another LLM, sometimes manually), and compute a pass rate.

That's not useless. But it has two serious limitations.

First, it's expensive. Every quality check requires an LLM call. If you want to evaluate a context before deploying it, you need to generate outputs, which costs time and money.

Second, it tells you whether your outputs were good — not why. If your pass rate drops, you don't know if it's because your guidance is weak, your directive is ambiguous, your constraints are too loose, or the pattern you chose is wrong for the problem.

What we needed was a way to evaluate the context itself, not just its outputs.

## QualityMetrics: scoring contexts before execution

`QualityMetrics` evaluates a `Context` object on six dimensions:

| Dimension | What it measures |
|-----------|-----------------|
| **Clarity** | Are the instructions unambiguous and consistent? |
| **Completeness** | Does the context have all the components a good context should have? |
| **Specificity** | Are the instructions concrete or vague? |
| **Relevance** | Does each component serve the task? |
| **Structure** | Is the context well-organized? |
| **Efficiency** | Is the context token-efficient without losing precision? |

```python
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")  # No LLM calls needed
score = metrics.evaluate(ctx)

print(f"Overall: {score.overall:.1%}")
# → Overall: 83.4%

for issue in score.issues:
    print(f"  {issue}")
# → Directive is vague — add specific success criteria
# → Missing constraints — LLM has no output format requirements
```

The heuristic mode runs entirely locally with no LLM calls. It's fast enough to run on every context in a batch job. The LLM mode does a deeper analysis for cases where you want richer feedback.

## OutputEvaluator: closing the loop on responses

The second tool goes in the other direction: given an output, how well did the LLM actually respond to this specific context?

`OutputEvaluator` scores responses on five dimensions that mirror what you'd look for in a rigorous thinker:

- **Instruction Following** — did it do what the directive asked?
- **Reasoning Depth** — did it think carefully or respond superficially?
- **Actionability** — are the outputs actually usable?
- **Structure Compliance** — did it respect the format constraints?
- **Cognitive Scaffolding** — did it build understanding, not just provide answers?

```python
from mycontext.intelligence import OutputEvaluator

evaluator = OutputEvaluator()
output_score = evaluator.evaluate(context=ctx, output=result.response)

print(f"Output quality: {output_score.overall:.1%}")
report = evaluator.report(output_score)
print(report)
```

The combination of both tools gives you something useful: **context quality + output quality** as separate signals. When output quality is low, you can check whether it's because the context was poor (fix the context) or because the model failed despite a good context (consider a different model, retry, or flag for human review).

## Context Amplification Index: proving the pattern is worth it

The third tool is one I find particularly interesting: the `ContextAmplificationIndex` (CAI).

The basic question CAI answers is: **how much better is my structured context, compared to just asking the raw question?**

```python
from mycontext.intelligence import ContextAmplificationIndex
from mycontext.templates.free.reasoning import RootCauseAnalyzer

cai = ContextAmplificationIndex()
result = cai.measure(
    template=RootCauseAnalyzer,
    input_data={"problem": "API latency tripled after deployment"},
    provider="openai",
)

print(f"CAI score: {result.cai_score:.2f}x")
print(f"Verdict: {result.verdict}")
# → CAI score: 1.47x
# → Verdict: significant_improvement
```

A score above 1.0 means the structured context is producing better outputs than the raw question. A score of 1.47 means 47% better quality by the output evaluation rubric.

This is valuable for two reasons. It helps you validate that a pattern is actually useful for a given problem type — some patterns add real value, others add overhead without improving outputs. And it gives you data to justify the cost of structured context development to stakeholders.

## How this changes the development workflow

Before we had these tools, LLM development felt like tuning by instinct. You had a vague sense that some changes helped and others didn't, but you couldn't quantify it.

Now my workflow looks like this:

1. Build a context using a pattern
2. Run `QualityMetrics` — score it, address flagged issues
3. Execute against a test case
4. Run `OutputEvaluator` — understand where the model fell short
5. Decide: fix the context, try a different pattern, or try a different model
6. Run CAI periodically to confirm the structured approach is earning its complexity

This is a tighter feedback loop. It's closer to how you'd develop and test any other piece of software. And it produces more consistent results because you're reasoning about causes instead of just observing effects.

---

The quality tools are documented in full in the [Quality & Metrics](/docs/quality/quality-metrics) section. If you're already using mycontext-ai, these are the tools I'd recommend integrating into your workflow first.

— Dhiraj
