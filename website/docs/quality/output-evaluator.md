---
sidebar_position: 2
title: OutputEvaluator
description: Evaluate LLM output quality against the context that produced it. Five dimensions measuring how well the response leverages the cognitive scaffolding.
---

# OutputEvaluator

`OutputEvaluator` scores **LLM outputs** — not prompts. It evaluates how well a response leverages the cognitive framework provided by its context, measuring five dimensions distinct from `QualityMetrics`' prompt-level scoring.

```python
from mycontext.intelligence import OutputEvaluator
from mycontext.templates.free.reasoning import RootCauseAnalyzer

# Build context and execute
ctx = RootCauseAnalyzer().build_context(
    problem="API response times tripled after deployment",
)
result = ctx.execute(provider="openai")

# Evaluate the output
evaluator = OutputEvaluator()
score = evaluator.evaluate(ctx, result.response)

print(f"Output quality: {score.overall:.1%}")
print(evaluator.report(score))
```

## The Five Output Dimensions

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Instruction Following | 25% | Did the output match the directive's action verbs and must-include terms? |
| Reasoning Depth | 20% | Multi-step reasoning markers, numbered steps, structured analysis |
| Actionability | 20% | Concrete, implementable recommendations with specific metrics |
| Structure Compliance | 15% | Does the output match the requested format (JSON, lists, headers)? |
| Cognitive Scaffolding | 20% | Does the output use the cognitive framework from the template? |

### QualityMetrics vs. OutputEvaluator

| Aspect | `QualityMetrics` | `OutputEvaluator` |
|--------|-----------------|------------------|
| Evaluates | The **context/prompt** | The **LLM response** |
| When to use | Before execution | After execution |
| Question | "Is this a good prompt?" | "Did the LLM do what I asked?" |

## Constructor

```python
OutputEvaluator(
    mode: str = "heuristic",
    provider: str = "openai",
    model: str = "gpt-4o-mini",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mode` | `str` | `"heuristic"` | `"heuristic"`, `"llm"`, or `"hybrid"` |
| `provider` | `str` | `"openai"` | LLM provider for LLM mode |
| `model` | `str` | `"gpt-4o-mini"` | Model for LLM mode |

## `evaluate(context, output)`

```python
score = evaluator.evaluate(context, llm_output)
```

**Returns:** `OutputQualityScore`

```python
@dataclass
class OutputQualityScore:
    overall: float                                # 0.0 to 1.0 weighted score
    dimensions: dict[OutputDimension, float]      # Per-dimension scores
    evidence: dict[OutputDimension, str]          # Why each dimension scored that way
    strengths: list[str]                          # Dimensions scoring >= 70%
    weaknesses: list[str]                         # Dimensions scoring < 40%
    metadata: dict                                # Mode, output word count
```

## `report(score)`

```python
print(evaluator.report(score))
```

Output:
```
Output Quality Report
=====================

Overall: 79.3%

Dimensions:
  [+] Instruction Following: 82.0%  (Matched 7/9 action verbs, 3/3 required terms)
  [+] Reasoning Depth: 74.0%  (8 reasoning markers, 12 numbered steps, 3 section headings)
  [+] Actionability: 76.0%  (11 action phrases, 6 action items, 4 concrete metrics)
  [~] Structure Compliance: 60.0%  (Headers found)
  [+] Cognitive Scaffolding: 85.0%  (Output uses 4/5 cognitive frameworks from context)
```

## Dimension Details

### Instruction Following

Checks whether the output actually does what the directive asked. Looks for:
- **Action verbs from the directive** — analyze, review, identify, evaluate, summarize, compare, diagnose, etc.
- **Must-include terms** — items listed in `Constraints.must_include`

```python
# If directive says "identify root causes and recommend solutions"
# and must_include = ["timeline", "impact"]
# → Checks: "identify" in output? "recommend" in output? "timeline" in output? "impact" in output?
```

### Reasoning Depth

Counts reasoning markers that indicate multi-step, non-surface-level responses:
- Causal: "because", "therefore", "consequently", "due to", "as a result"
- Contrast: "however", "on the other hand", "conversely", "although"
- Elaboration: "furthermore", "moreover", "nevertheless"
- Structure: numbered steps, section headings, nested lists

### Actionability

Measures how concrete and implementable the recommendations are:
- **Action phrases**: "should", "recommend", "implement", "next step", "prioritize"
- **Numbered/bulleted actions**: items containing action language
- **Concrete metrics**: percentages, dollar figures, time frames ("30 days", "15%")

### Structure Compliance

Compares what the context requested with what the output delivered:
- If context requested JSON → checks for valid JSON in output
- If context requested bullet lists → checks for list formatting
- If context requested headers/sections → checks for `##` or `Section:` formatting

### Cognitive Scaffolding

The most distinctive dimension: does the output actually use the cognitive framework the template was designed to apply?

Checks for 14 framework patterns:

| Framework | Keywords checked in output |
|-----------|--------------------------|
| Root Cause | "root cause", "underlying cause", "primary cause" |
| SWOT | "strength", "weakness", "opportunity", "threat" |
| Stakeholder | "stakeholder", "impact analysis", "affected party" |
| Causal | "causal", "cause and effect", "chain of causation" |
| Risk | "risk", "mitigation", "probability", "impact" |
| Hypothesis | "hypothesis", "null hypothesis", "test" |
| Decision Matrix | "decision matrix", "weighted criteria" |
| Gap Analysis | "current state", "desired state", "gap" |
| Trade-off | "trade-off", "tension", "balance between" |
| Temporal | "timeline", "temporal", "sequence of events" |
| Feedback Loop | "feedback loop", "reinforcing", "balancing" |
| Leverage Point | "leverage point", "intervention", "high-impact" |
| Diagnostic | "symptom", "diagnosis", "differential" |
| Pros/Cons | "advantage", "disadvantage", "pro", "con" |

## Examples

### Full Evaluate-and-Report Loop

```python
from mycontext.intelligence import OutputEvaluator
from mycontext.templates.free.specialized import RiskAssessor

ctx = RiskAssessor().build_context(
    decision="Launch a new B2B pricing tier at $5,000/month",
    depth="thorough",
)
result = ctx.execute(provider="openai")

evaluator = OutputEvaluator()
score = evaluator.evaluate(ctx, result.response)

print(evaluator.report(score))

# Check if output meets quality bar
if score.overall < 0.65:
    print("Low quality output — consider re-running or using a better model")
    for weakness in score.weaknesses:
        print(f"  Weak: {weakness}")
```

### Quality Gate in Production

```python
def execute_with_quality_gate(ctx, provider="openai", min_output_quality=0.65, retries=2):
    evaluator = OutputEvaluator(mode="heuristic")
    
    for attempt in range(retries + 1):
        result = ctx.execute(provider=provider)
        score = evaluator.evaluate(ctx, result.response)
        
        if score.overall >= min_output_quality:
            return result.response, score
        
        if attempt < retries:
            print(f"Attempt {attempt+1}: quality {score.overall:.1%} below {min_output_quality:.1%}, retrying...")
    
    return result.response, score  # Return best attempt

response, score = execute_with_quality_gate(ctx, min_output_quality=0.70)
```

### LLM-Mode for High-Stakes Evaluation

```python
evaluator = OutputEvaluator(
    mode="llm",
    provider="openai",
    model="gpt-4o",  # Use more capable model for scoring
)
score = evaluator.evaluate(ctx, llm_output)
print(f"LLM-evaluated quality: {score.overall:.1%}")
print("Evidence:")
for dim, evidence in score.evidence.items():
    print(f"  {dim.value}: {evidence}")
```

### Hybrid Mode (Recommended for Production)

```python
# Heuristic for obvious cases (fast), LLM only for borderline 0.35–0.75
evaluator = OutputEvaluator(mode="hybrid", provider="openai")
score = evaluator.evaluate(ctx, output)
print(f"Mode used: {score.metadata['mode']}")  # "hybrid_fast" or "hybrid_llm"
```

## OutputDimension Enum

```python
from mycontext.intelligence import OutputDimension

class OutputDimension(Enum):
    INSTRUCTION_FOLLOWING = "instruction_following"
    REASONING_DEPTH = "reasoning_depth"
    ACTIONABILITY = "actionability"
    STRUCTURE_COMPLIANCE = "structure_compliance"
    COGNITIVE_SCAFFOLDING = "cognitive_scaffolding"
```

## API Reference

### `OutputEvaluator`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(mode, provider, model)` | — | Initialize |
| `evaluate(context, output, **kwargs)` | `OutputQualityScore` | Score an output |
| `report(score)` | `str` | Human-readable report |

### `OutputQualityScore`

| Field | Type | Description |
|-------|------|-------------|
| `overall` | `float` | Weighted score (0.0–1.0) |
| `dimensions` | `dict[OutputDimension, float]` | Per-dimension scores |
| `evidence` | `dict[OutputDimension, str]` | Why each dimension scored that way |
| `strengths` | `list[str]` | Dimensions scoring >= 70% |
| `weaknesses` | `list[str]` | Dimensions scoring < 40% |
| `metadata` | `dict` | Mode, output word count |
