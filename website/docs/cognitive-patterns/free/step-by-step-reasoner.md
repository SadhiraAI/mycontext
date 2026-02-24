---
sidebar_position: 2
title: StepByStepReasoner
description: Chain-of-Thought reasoning with transparent, teachable step-by-step problem solving. Based on Wei et al. (2023) and IBM Zurich cognitive tools research.
---

# StepByStepReasoner

**Category:** Reasoning | **Module:** `mycontext.templates.free.reasoning`

Guides systematic problem solving through clear, logical steps. Implements Chain-of-Thought methodology with transparent reasoning — every step shows what, why, how, and the intermediate result. Ideal for math, logic, analysis, and any problem where showing your work matters.

Based on:
- *"Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"* (Wei et al., 2023)
- IBM Zurich cognitive tools research (2025)

## When to Use

- Mathematical and quantitative problems
- Multi-step logical reasoning
- Scientific analysis with intermediate calculations
- Problems where you need to verify the solution
- Educational contexts where transparent reasoning matters
- Debugging complex processes step-by-step

## Quick Start

```python
from mycontext.templates.free.reasoning import StepByStepReasoner

reasoner = StepByStepReasoner()

result = reasoner.execute(
    provider="gemini",
    problem="If a train travels 120km in 2 hours, then speeds up to travel 200km in the next 2.5 hours, what is its average speed for the whole journey?",
    domain="mathematical",
    temperature=0.3,
)
print(result.response)
```

## Constructor

```python
reasoner = StepByStepReasoner()
```

## Methods

### `build_context(problem, context=None, domain="general")`

```python
ctx = reasoner.build_context(
    problem="A company's revenue grew 15% in Y1 and 22% in Y2 from a base of $1M. What's the compound growth?",
    domain="mathematical",
)

# Export and use with any LLM or framework
print(ctx.to_openai())
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `problem` | `str` | `""` | The problem to solve |
| `context` | `str \| None` | `None` | Additional context or constraints |
| `domain` | `str` | `"general"` | Problem domain — affects framing |

### `execute(provider, problem, context=None, domain="general", temperature=0.3, **kwargs)`

```python
result = reasoner.execute(
    provider="gemini",
    problem="Prove that the sum of any two consecutive odd numbers is divisible by 4",
    domain="mathematical",
    temperature=0.3,
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | `str` | `"gemini"` | LLM provider (gemini recommended for reasoning) |
| `problem` | `str` | `""` | The problem to solve |
| `context` | `str \| None` | `None` | Additional context |
| `domain` | `str` | `"general"` | Problem domain |
| `temperature` | `float` | `0.3` | Lower = more consistent reasoning. Keep between 0.2–0.4 |
| `**kwargs` | | | Additional provider parameters |

## Domain Options

The `domain` parameter adjusts framing for the problem type:

| Domain | Best for |
|--------|----------|
| `"mathematical"` | Calculations, proofs, quantitative problems |
| `"logical"` | Deductive/inductive reasoning, logic puzzles |
| `"scientific"` | Hypothesis testing, experimental analysis |
| `"analytical"` | Business analysis, data interpretation |
| `"general"` | Any problem not in above categories |

## Reasoning Framework

The pattern enforces a 5-phase problem-solving approach:

### Phase 1: UNDERSTAND
Restate the problem, identify problem type, list all known information and constraints. Forces the model to engage with the problem before solving it.

### Phase 2: PLAN
Define solution strategy and methods. Sketch the solution path visually:
```
[Input] → [Step A] → [Step B] → [Step C] → [Solution]
```

### Phase 3: EXECUTE
Work through each step with four elements per step:
- **What** you're doing
- **Why** you're doing it
- **How** you do it (calculations, reasoning)
- The **result** of this step

### Phase 4: VERIFY
Check against original problem. Apply alternative verification method if possible. Sanity-check scale and units.

### Phase 5: CONCLUDE
State the final answer explicitly. Assess confidence level and explain it.

## Examples

### Mathematical Problem

```python
result = reasoner.execute(
    provider="gemini",
    problem="""
    A store sells shirts at 40% markup over cost.
    During a sale, they discount 25%.
    What's the actual profit margin as a percentage of cost?
    """,
    domain="mathematical",
    temperature=0.3,
)
```

### Logical Reasoning

```python
result = reasoner.execute(
    provider="openai",
    problem="""
    All managers attend the Monday meeting.
    Sarah doesn't attend the Monday meeting.
    Sam attends the Monday meeting.
    Can we conclude that Sam is a manager?
    """,
    domain="logical",
)
```

### Scientific Analysis

```python
result = reasoner.execute(
    provider="anthropic",
    problem="""
    An experiment shows Drug A reduces blood pressure by 12mmHg in a sample of 150 patients.
    The standard deviation is 8mmHg. Calculate the 95% confidence interval
    and determine if results are statistically significant (p < 0.05).
    """,
    domain="scientific",
    temperature=0.2,
)
```

## Temperature Guidance

:::tip Temperature matters for reasoning
Lower temperatures produce more deterministic, reproducible step-by-step solutions. For mathematical/logical problems:
- `0.2` — Most consistent, minimal creativity
- `0.3` — Recommended default (balance)
- `0.5+` — More varied but less reliable for calculations
:::

## Integration with Quality Metrics

Pair with `QualityMetrics` to measure solution thoroughness:

```python
from mycontext.templates.free.reasoning import StepByStepReasoner
from mycontext.intelligence import QualityMetrics

ctx = StepByStepReasoner().build_context(
    problem="Calculate the ROI of a $500k investment with 12% annual return over 5 years",
    domain="mathematical",
)
result = ctx.execute(provider="openai")
metrics = QualityMetrics.evaluate(ctx, result.response)
print(f"Completeness: {metrics.completeness}")
```

## Output Format

```
## Step 1: UNDERSTAND
**Restate the Problem**: ...
- What we're looking for: ...
- Key information given: ...

## Step 2: PLAN
**Strategy**: ...
**Sketch the Solution Path**:
[Input] → [Step A] → [Step B] → [Solution]

## Step 3: EXECUTE
### Step 3.1: [Description]
- **Action**: ...
- **Calculation**: ...
  = [intermediate result]
- **Result**: ...

## Step 4: VERIFY
...

## Step 5: CONCLUDE
🎯 **[Final Answer]**
Confidence: High
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(problem, context, domain)` | `Context` | Assembled context |
| `execute(provider, problem, context, domain, temperature, **kwargs)` | `ProviderResponse` | Execute reasoning |
| `generic_prompt(problem, context_section, domain)` | `str` | Zero-cost prompt string |
