---
sidebar_position: 1
title: QualityMetrics
description: Measure context quality across six dimensions before you execute. Catch weak prompts, get specific improvement suggestions, and compare two contexts side by side.
---

# QualityMetrics

`QualityMetrics` evaluates a `Context` object across six dimensions and returns a score with issues, strengths, and specific improvement suggestions — before you send anything to an LLM.

```python
from mycontext.intelligence import QualityMetrics
from mycontext.templates.free.reasoning import RootCauseAnalyzer

ctx = RootCauseAnalyzer().build_context(
    problem="API response times tripled after deployment",
    depth="comprehensive",
)

metrics = QualityMetrics()
score = metrics.evaluate(ctx)

print(f"Quality: {score.overall:.1%}")
print(metrics.report(score))
```

## Why Measure Context Quality?

A poorly structured context produces poor responses. `QualityMetrics` lets you:
- **Catch weak prompts before execution** — save tokens and API costs
- **Improve iteratively** — specific suggestions tell you exactly what to fix
- **Compare approaches** — `compare()` shows exactly how much improvement you made
- **Validate in CI** — assert minimum quality thresholds before deploying

## The Six Dimensions

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Completeness | 25% | Are all components present? (role, goal, directive, rules, constraints, examples) |
| Clarity | 20% | Clear, unambiguous instructions. Checks pronoun ratio, hedge density, and modal commitment |
| Reasoning Depth | 20% | Chain-of-thought markers, structured steps, depth of analysis |
| Actionability | 20% | Concrete, implementable recommendations with specific metrics |
| Specificity | 15% | Concrete domain terms, detailed directives, not generic phrases |
| Efficiency | 10% | Concise without being incomplete. Directive length is scored separately from total length |

### Scoring Scale

```
0–25%   Broken / empty / placeholder
25–45%  Minimal / generic ("Expert Assistant, be helpful")
45–65%  Adequate basics but missing depth
65–80%  Good: clear role, specific directive, some constraints
80–95%  Very good: comprehensive, examples, tight constraints
95–100% Exceptional: publishable quality
```

## Constructor

```python
QualityMetrics(
    mode: str = "heuristic",
    llm_provider: str = "openai",
    llm_model: str = "gpt-4o-mini",
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mode` | `str` | `"heuristic"` | Evaluation mode: `"heuristic"`, `"llm"`, or `"hybrid"` |
| `llm_provider` | `str` | `"openai"` | Provider for LLM mode |
| `llm_model` | `str` | `"gpt-4o-mini"` | Model for LLM mode |

### Three Evaluation Modes

| Mode | Speed | Cost | Best for |
|------|-------|------|---------|
| `"heuristic"` | Instant | Free | CI/CD, bulk evaluation, development |
| `"llm"` | ~2s | ~$0.02/eval | Authoritative scoring, production QA |
| `"hybrid"` | Fast | Low | Best of both: heuristic for clear cases, LLM for borderline (0.45–0.75) |

## `evaluate(context)`

```python
score = metrics.evaluate(context)
```

**Returns:** `QualityScore`

```python
@dataclass
class QualityScore:
    overall: float                              # 0.0 to 1.0 weighted score
    dimensions: dict[QualityDimension, float]   # Per-dimension scores
    issues: list[str]                           # Specific problems found
    strengths: list[str]                        # What's working well
    suggestions: list[str]                      # Actionable improvements
    metadata: dict                              # Mode, word count, etc.
```

## `report(score)`

Generate a human-readable quality report:

```python
metrics = QualityMetrics()
score = metrics.evaluate(ctx)
print(metrics.report(score))
```

Output:
```
Context Quality Report
=====================

Overall Score: 84.2% ✅

Dimension Scores:
  ✅ Clarity: 88.0%
  ✅ Completeness: 90.0%
  ✅ Specificity: 78.0%
  ✅ Relevance: 85.0%
  ✅ Structure: 82.0%
  ⚠️  Efficiency: 71.0%

Strengths (5):
  ✓ Clear role and directive structure
  ✓ Specific role/guidance defined
  ✓ Well-defined rules (4)
  ✓ Good formatting with headers and lists
  ✓ Rich domain-specific terminology

Issues (1):
  ✗ No examples — add concrete examples of expected input/output

Suggestions for Improvement:
  1. Strong prompt. Consider adding edge cases or constraints for even better results.
```

## `compare(context1, context2)`

Measure improvement between two contexts:

```python
from mycontext import Context
from mycontext.foundation import Guidance, Directive, Constraints

# Before: generic
ctx_before = Context(
    guidance=Guidance(role="Expert Assistant"),
    directive=Directive(content="Analyze the problem"),
)

# After: specific
from mycontext.templates.free.reasoning import RootCauseAnalyzer
ctx_after = RootCauseAnalyzer().build_context(
    problem="API response times tripled after deployment",
    depth="comprehensive",
)

metrics = QualityMetrics()
comparison = metrics.compare(ctx_before, ctx_after)

print(f"Before: {comparison['original_score']:.1%}")
print(f"After:  {comparison['improved_score']:.1%}")
print(f"Lift:   +{comparison['improvement_percentage']:.1f}%")

print("\nDimension changes:")
for dim, delta in comparison['dimension_changes'].items():
    arrow = "↑" if delta > 0.05 else "↓" if delta < -0.05 else "→"
    print(f"  {arrow} {dim.value}: {delta:+.1%}")

print("\nResolved issues:", comparison['resolved_issues'])
print("New strengths:", comparison['new_strengths'])
```

**Returns dict:**
```python
{
    "original_score": 0.28,
    "improved_score": 0.84,
    "improvement": 0.56,
    "improvement_percentage": 56.0,
    "dimension_changes": {QualityDimension.COMPLETENESS: +0.70, ...},
    "resolved_issues": {"Missing guidance/role component", ...},
    "new_strengths": {"Clear role and directive structure", ...},
}
```

## Examples

### Evaluate a Pattern-Built Context

```python
from mycontext.intelligence import QualityMetrics
from mycontext.templates.free.planning import ScenarioPlanner

ctx = ScenarioPlanner().build_context(
    topic="AI regulation impact on our SaaS business",
    timeframe="3 years",
)

metrics = QualityMetrics()
score = metrics.evaluate(ctx)
print(f"Score: {score.overall:.1%}")
for suggestion in score.suggestions:
    print(f"  → {suggestion}")
```

### Assert Minimum Quality in CI

```python
from mycontext.intelligence import QualityMetrics

def validate_context(ctx, min_quality=0.70):
    metrics = QualityMetrics(mode="heuristic")
    score = metrics.evaluate(ctx)
    
    if score.overall < min_quality:
        issues = "\n".join(f"  - {i}" for i in score.issues)
        raise ValueError(
            f"Context quality {score.overall:.1%} below minimum {min_quality:.1%}\n{issues}"
        )
    return score

# In your pipeline
ctx = build_my_context()
score = validate_context(ctx, min_quality=0.75)
result = ctx.execute(provider="openai")
```

### Iterative Improvement Loop

```python
from mycontext import Context
from mycontext.foundation import Guidance, Directive, Constraints
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics()

# Start with basic context
ctx = Context(
    guidance=Guidance(role="Analyst"),
    directive=Directive(content="Analyze our churn problem"),
)
score = metrics.evaluate(ctx)
print(f"v1: {score.overall:.1%}")
print("Issues:", score.issues)

# Improve based on suggestions
ctx = Context(
    guidance=Guidance(
        role="Senior customer success analyst with SaaS retention expertise",
        rules=[
            "Identify root causes using the Five Whys methodology",
            "Quantify impact: revenue at risk, affected cohorts, trend direction",
            "Distinguish correlation from causation",
            "Provide 3 prioritized recommendations with implementation timeline",
        ],
    ),
    directive=Directive(
        content="""Analyze our customer churn problem.
        
Context: 40% churn increase in Q3. New enterprise tier launched Q2.
Analyze: cohort patterns, product usage correlation, support ticket themes.
Output: root causes ranked by confidence, immediate actions, 90-day plan.""",
    ),
    constraints=Constraints(
        must_include=["cohort analysis", "revenue impact", "root cause", "recommendations"],
        format_rules=["Executive summary first", "Each finding supported by evidence"],
    ),
)
score = metrics.evaluate(ctx)
print(f"v2: {score.overall:.1%}")
```

## `QualityDimension` Enum

```python
from mycontext.intelligence import QualityDimension

class QualityDimension(Enum):
    CLARITY = "clarity"
    COMPLETENESS = "completeness"
    SPECIFICITY = "specificity"
    RELEVANCE = "relevance"
    STRUCTURE = "structure"
    EFFICIENCY = "efficiency"
```

Access a specific dimension score:

```python
score = metrics.evaluate(ctx)
print(score.dimensions[QualityDimension.COMPLETENESS])  # 0.90
print(score.dimensions[QualityDimension.CLARITY])       # 0.88
```

## What Gets Penalized

Common issues detected automatically:

| Issue | Dimension | Penalty |
|-------|-----------|---------|
| Extremely short content (< 10 words) | Global | Up to 60% |
| Minimal generic prompt ("Expert Assistant, be helpful") | Global | 45% |
| Generic role + generic rules | Global | 30% |
| Very short prompt (< 30 words) | Global | 30% |
| Missing role, directive, or goal | Global | 15% each |
| Empty JSON schema | Global | 10% |
| Likely typos detected | Global | 5% per typo |
| High pronoun ratio (> 10%) — ambiguous references | Clarity | 15% |
| Moderate pronoun ratio (5–10%) | Clarity | 7% |
| High hedge density — "try to", "if applicable", "ideally" | Clarity | 12% |
| Weak modal commitment — more should/could than must/shall | Clarity | 8% |
| Directive too long (> 100 words) — dilutes the core instruction | Efficiency | 10% |

## Research Foundation

The heuristics in `QualityMetrics` are grounded in two internal experiments and peer-reviewed NLP research.

### Empirical experiments

**Experiment 1 — POS Profile & Entropy (n=10 prompt pairs)**
Tested whether linguistic features (parts of speech, perplexity, semantic density) predict output quality. Key finding: named entity count and noun-to-pronoun ratio showed directional signal on a small controlled dataset.

**Experiment 2 — TruthfulQA Scale Test (n=200, gpt-4o-mini)**
Scaled the most promising features to the TruthfulQA benchmark. Statistically significant findings that directly shaped the Clarity and Efficiency scorers:

| Feature | Correlation with accuracy | p-value | Applied to |
|---------|--------------------------|---------|------------|
| Pronoun ratio | r = −0.187 | p = 0.008 | Clarity — tiered penalty at 5% and 10% |
| Directive length | r = −0.176 | p = 0.013 | Efficiency — penalty for directives > 100 words |

### Academic foundations

| Heuristic | Source |
|-----------|--------|
| Pronoun ratio & ambiguity | Experiment 2 (TruthfulQA, n=200) |
| Hedge density | Hyland (1996) — hedging in instructional discourse |
| Modal commitment ratio | Deontic logic; Ouyang et al. (2022) InstructGPT |
| Concreteness preference | Brysbaert et al. (2014) — concreteness ratings for 40k English words |
| Frame Semantics completeness | Fillmore (1982) — FrameNet argument slots |
| Sentence complexity | Gibson (1998) — dependency locality theory |

---

## API Reference

### `QualityMetrics`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(mode, llm_provider, llm_model)` | — | Initialize |
| `evaluate(context, reference)` | `QualityScore` | Evaluate a context |
| `compare(context1, context2)` | `dict` | Compare two contexts |
| `report(score)` | `str` | Human-readable report |

### `QualityScore`

| Field | Type | Description |
|-------|------|-------------|
| `overall` | `float` | Weighted score (0.0–1.0) |
| `dimensions` | `dict[QualityDimension, float]` | Per-dimension scores |
| `issues` | `list[str]` | Problems found |
| `strengths` | `list[str]` | What's working |
| `suggestions` | `list[str]` | Actionable improvements |
| `metadata` | `dict` | Mode, word count, component flags |
