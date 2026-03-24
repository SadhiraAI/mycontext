---
sidebar_position: 2
title: OutputEvaluator
description: Evaluate LLM output quality against the context that produced it. Seven dimensions with configurable weights, distinct from QualityMetrics prompt-level scoring.
---

# OutputEvaluator

`OutputEvaluator` scores **LLM outputs** — not prompts. It evaluates how well a response fits the assembled context across **seven** dimensions (instruction following, reasoning depth, actionability, structure, scaffolding, groundedness, register). Weights are customizable for task-specific evaluation.

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

## The seven output dimensions (default weights)

| Dimension | Default weight | What it measures |
|-----------|----------------|------------------|
| Instruction Following | 20% | Directive action verbs, must-include terms, numbered instruction coverage |
| Reasoning Depth | 15% | Multi-step markers, structure, quantified claims |
| Actionability | 15% | Concrete recommendations, metrics, low hedge |
| Structure Compliance | 10% | Requested format (JSON, lists, headers) vs delivery |
| Cognitive Scaffolding | 15% | Use of cognitive frameworks implied by the context |
| Groundedness | 15% | Stays within knowledge boundaries; low unsupported speculation |
| Register Fit | 10% | Tone and formality match role/style in the context |

Pass **`dimension_weights`** to the constructor to override (keys are snake_case strings matching `OutputDimension.value`, e.g. `instruction_following`). Values should be non-negative. The built-in defaults sum to **1.0**; custom maps are applied as-is (no renormalization), so if you override, prefer weights that sum to 1.0 to keep `overall` in the usual 0–1 range.

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
    dimension_weights: dict[str, float] | None = None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mode` | `str` | `"heuristic"` | `"heuristic"`, `"llm"`, or `"hybrid"` |
| `provider` | `str` | `"openai"` | LLM provider for LLM mode |
| `model` | `str` | `"gpt-4o-mini"` | Model for LLM mode |
| `dimension_weights` | `dict[str, float] \| None` | `None` | Per-dimension multipliers; keys like `instruction_following`, `reasoning_depth`, … |

### Custom weights example

```python
# Emphasize instruction following and structure for a formatting-heavy task
evaluator = OutputEvaluator(
    mode="llm",
    model="gpt-4o",
    dimension_weights={
        "instruction_following": 0.35,
        "structure_compliance": 0.25,
        "reasoning_depth": 0.10,
        "actionability": 0.10,
        "cognitive_scaffolding": 0.10,
        "groundedness": 0.05,
        "register_fit": 0.05,
    },
)
```

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
- **Refusal / deflection** — checked first. If the output matches a known refusal pattern ("I can't help with that", "As an AI language model...", "I don't have access to real-time data"), the score is hard-capped at **0.05** regardless of other signals. This closes the most common false-positive gap.
- **Action verbs from the directive** — analyze, review, identify, evaluate, summarize, compare, diagnose, etc.
- **Must-include terms** — items listed in `Constraints.must_include`
- **Numbered instruction coverage** — if the directive lists 3+ numbered items, checks how many the output actually addresses. < 50% addressed → −15%; ≥ 80% addressed → +10%.

```python
# If directive says "identify root causes and recommend solutions"
# and must_include = ["timeline", "impact"]
# → First: is this a refusal? If yes → 0.05
# → Checks: "identify" in output? "recommend" in output? "timeline" in output? "impact" in output?
# → If directive had 5 numbered items, how many are covered?
```

### Reasoning Depth

Counts reasoning markers that indicate multi-step, non-surface-level responses:
- Causal: "because", "therefore", "consequently", "due to", "as a result"
- Contrast: "however", "on the other hand", "conversely", "although"
- Elaboration: "furthermore", "moreover", "nevertheless"
- Structure: numbered steps, section headings, nested lists
- **Quantified claims** — specific numbers, percentages, dates, and measurements score higher than discourse markers. "Performance declined 23% YoY from Q2 2023 to Q2 2024" outscores "performance declined significantly". Patterns detected: `23%`, `3x`, `Q3 2024`, `$50`, `2 weeks`, etc. Each quantified claim contributes 0.4 depth units vs. 0.07 per discourse marker.

### Actionability

Measures how concrete and implementable the recommendations are:
- **Action phrases**: "should", "recommend", "implement", "next step", "prioritize"
- **Numbered/bulleted actions**: items containing action language
- **Concrete metrics**: percentages, dollar figures, time frames ("30 days", "15%")
- **Output hedge penalty**: outputs that avoid committing to answers are penalized. Detected phrases include "it depends", "generally speaking", "in most cases", "could potentially", "there are many factors". ≥ 3 such phrases → −15%; ≥ 1 → −5%. An output that hedges every recommendation is not actionable regardless of how many "should" keywords it contains.

### Structure Compliance

Compares what the context requested with what the output delivered:
- If context requested JSON → checks for valid JSON in output
- If context requested bullet lists → checks for list formatting
- If context requested headers/sections → checks for `##` or `Section:` formatting

### Groundedness and register fit

- **Groundedness** — penalizes outputs that invent facts or drift from supplied knowledge when the context implies evidence-bound answers.
- **Register fit** — whether tone and vocabulary match the stated role and style in the context.

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

## Research Foundation

The `OutputEvaluator` heuristics are grounded in empirical experiments and established argumentation quality research.

### Why refusal detection matters

Without explicit refusal detection, a compliant output and a refusing output ("As an AI, I can't help with that") can score identically — both get the 0.3 base score from verb matching. This was the highest-priority gap identified in our internal audit. The fix: 8 regex patterns checked before any other scoring, with a hard floor of 0.05 on match.

### Why quantified claims outweigh discourse markers

Habernal & Gurevych (2016) and Wachsmuth et al. (2017) consistently find that **specific numerical evidence** is the strongest signal of argument quality. "Declined 23% YoY" is fundamentally different from "declined significantly" — one is verifiable, one is hedged. Quantified claims are therefore weighted at 0.4 depth units each, vs. 0.07 for standard discourse markers like "therefore" or "however".

### Why output hedges hurt actionability

An output full of "it depends", "generally speaking", and "without more context" is providing meta-commentary instead of answers. This is the output-side equivalent of instructional hedging in the prompt — it erodes the value delivered to the user even when the structural signals (bullet points, "recommend" keywords) look positive.

### Academic foundations

| Heuristic | Source |
|-----------|--------|
| Quantified claims → reasoning depth | Habernal & Gurevych (2016); Wachsmuth et al. (2017) |
| Refusal/deflection detection | IFEval — Zhou et al. (2023) |
| Numbered instruction coverage | IFEval — Zhou et al. (2023) |
| Actionability = specificity + ownership + time | Decision science; consulting research |
| Cognitive scaffolding framework matching | Bloom's Taxonomy (1956); Anderson et al. (2001) |

---

## OutputDimension Enum

```python
from mycontext.intelligence import OutputDimension

class OutputDimension(Enum):
    INSTRUCTION_FOLLOWING = "instruction_following"
    REASONING_DEPTH = "reasoning_depth"
    ACTIONABILITY = "actionability"
    STRUCTURE_COMPLIANCE = "structure_compliance"
    COGNITIVE_SCAFFOLDING = "cognitive_scaffolding"
    GROUNDEDNESS = "groundedness"
    REGISTER_FIT = "register_fit"
```

## API Reference

### `OutputEvaluator`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(mode, provider, model, dimension_weights?)` | — | Initialize |
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
