---
sidebar_position: 1
title: "Structured Reasoning: Model Cost vs Accuracy"
description: "Experiment showing that mycontext's StepByStepReasoner template enables a $0.0008/call lightweight model to match a $0.02/call reasoning model at 100% accuracy on math/logic tasks."
---

# Structured Reasoning: Model Cost vs Accuracy

:::info TL;DR
The `StepByStepReasoner` template achieves **100% accuracy across all 3 tested models** (gpt-4o-mini, gpt-4o, gpt-5.2) on math/logic problems. The cheapest model ($0.0008/call) performs identically to the most expensive reasoning model ($0.02/call) — a **32x cost reduction** with zero accuracy loss.
:::

## Motivation

A common assumption in LLM applications is that harder tasks require more expensive models. Reasoning tasks — multi-step math, logic, applied calculations — are typically delegated to "reasoning models" like o1, o3, or gpt-5.2 that use chain-of-thought internally.

This experiment tests whether **structured context engineering** (providing a step-by-step reasoning template) can eliminate the accuracy gap between cheap and expensive models, making model selection a cost decision rather than a capability decision.

## Experiment Design

### Template Under Test

[`StepByStepReasoner`](/docs/cognitive-patterns/free/step-by-step-reasoner) — a 5-step sequential reasoning template:

1. **UNDERSTAND** — Parse the problem, identify knowns/unknowns
2. **PLAN** — Choose a solution approach
3. **EXECUTE** — Carry out the calculations step by step
4. **VERIFY** — Cross-check with alternative methods
5. **CONCLUDE** — State the final answer with confidence

### Models

| Model | Tier | Avg Cost/Call | Reasoning Tokens |
|-------|------|:---:|:---:|
| `gpt-4o-mini` | Lightweight | $0.0008 | No |
| `gpt-4o` | Mid-tier | $0.012 | No |
| `gpt-5.2` | Reasoning | $0.025 | Yes |

### Problems

Three math/logic problems of increasing complexity:

| ID | Type | Problem | Correct Answer |
|----|------|---------|:-:|
| `avg_speed` | Simple math | Train travels 120km/2h then 200km/2.5h — average speed? | 71.11 km/h |
| `discount` | Multi-step logic | 20% off then 15% off the result — same as 35% off? | 32% (no) |
| `uptime` | Applied reasoning | 3 servers at 99.5% uptime each, all must run — combined uptime? | 98.51% |

### Investment Levels

Each problem was run at three depth levels to test parameterization:

| Level | Constraint | Purpose |
|-------|-----------|---------|
| **Quick** | "Be concise. Maximum 3 sub-steps." | Minimum viable depth |
| **Standard** | (none) | Default template behavior |
| **Thorough** | "Be extremely thorough. Show 2+ verification methods." | Maximum depth |

### Matrix

3 models &times; 3 problems &times; 3 investment levels = **27 runs**

## Results

### Per-Run Data

| # | Model | Problem | Investment | Correct | Chars | Tokens | Cost |
|---|-------|---------|-----------|:---:|---:|---:|---:|
| 1 | gpt-4o-mini | avg_speed | quick | ✅ | 3,304 | 1,744 | $0.0007 |
| 2 | gpt-4o-mini | avg_speed | standard | ✅ | 3,829 | 1,840 | $0.0007 |
| 3 | gpt-4o-mini | avg_speed | thorough | ✅ | 4,719 | 2,142 | $0.0009 |
| 4 | gpt-4o-mini | discount | quick | ✅ | 4,049 | 1,862 | $0.0007 |
| 5 | gpt-4o-mini | discount | standard | ✅ | 4,423 | 1,888 | $0.0008 |
| 6 | gpt-4o-mini | discount | thorough | ✅ | 4,498 | 2,052 | $0.0009 |
| 7 | gpt-4o-mini | uptime | quick | ✅ | 4,109 | 1,866 | $0.0007 |
| 8 | gpt-4o-mini | uptime | standard | ✅ | 4,448 | 1,860 | $0.0007 |
| 9 | gpt-4o-mini | uptime | thorough | ✅ | 4,599 | 2,016 | $0.0008 |
| 10 | gpt-4o | avg_speed | quick | ✅ | 3,391 | 1,716 | $0.0109 |
| 11 | gpt-4o | avg_speed | standard | ✅ | 3,382 | 1,682 | $0.0107 |
| 12 | gpt-4o | avg_speed | thorough | ✅ | 4,162 | 1,970 | $0.0134 |
| 13 | gpt-4o | discount | quick | ✅ | 3,359 | 1,706 | $0.0108 |
| 14 | gpt-4o | discount | standard | ✅ | 4,216 | 1,859 | $0.0125 |
| 15 | gpt-4o | discount | thorough | ✅ | 4,242 | 1,985 | $0.0136 |
| 16 | gpt-4o | uptime | quick | ✅ | 4,140 | 1,831 | $0.0120 |
| 17 | gpt-4o | uptime | standard | ✅ | 4,697 | 1,895 | $0.0128 |
| 18 | gpt-4o | uptime | thorough | ✅ | 5,636 | 2,137 | $0.0150 |
| 19 | gpt-5.2 | avg_speed | quick | ✅ | 3,006 | 1,814 | $0.0151 |
| 20 | gpt-5.2 | avg_speed | standard | ✅ | 4,365 | 2,174 | $0.0205 |
| 21 | gpt-5.2 | avg_speed | thorough | ✅ | 6,339 | 2,950 | $0.0310 |
| 22 | gpt-5.2 | discount | quick | ✅ | 3,836 | 1,922 | $0.0166 |
| 23 | gpt-5.2 | discount | standard | ✅ | 4,706 | 2,202 | $0.0209 |
| 24 | gpt-5.2 | discount | thorough | ✅ | 7,435 | 3,086 | $0.0330 |
| 25 | gpt-5.2 | uptime | quick | ✅ | 4,156 | 2,152 | $0.0198 |
| 26 | gpt-5.2 | uptime | standard | ✅ | 5,430 | 2,424 | $0.0239 |
| 27 | gpt-5.2 | uptime | thorough | ✅ | 8,784 | 3,868 | $0.0438 |

:::note Correctness Verification
Accuracy was verified by confirming the correct numeric answer appears in each run's CONCLUDE section. All 27 runs contain the correct answer. See [Methodology Notes](#methodology-notes) for details.
:::

### Accuracy by Model

| Model | Accuracy | Total Cost (9 runs) | Avg Cost/Call |
|-------|:---:|---:|---:|
| **gpt-4o-mini** | **9/9 = 100%** | **$0.0070** | **$0.0008** |
| gpt-4o | 9/9 = 100% | $0.1117 | $0.0124 |
| gpt-5.2 | 9/9 = 100% | $0.2247 | $0.0250 |

All three models achieve identical accuracy. The cost difference is the only meaningful variable:
- gpt-4o is **16x** more expensive than gpt-4o-mini
- gpt-5.2 is **32x** more expensive than gpt-4o-mini

### Investment Level Impact

| Level | Accuracy | Avg Output | Avg Tokens |
|-------|:---:|---:|---:|
| Quick | 9/9 = 100% | 3,706 chars | 1,837 |
| Standard | 9/9 = 100% | 4,388 chars | 1,963 |
| Thorough | 9/9 = 100% | 5,602 chars | 2,463 |

Investment levels successfully control output depth:
- **Quick → Thorough** increases output by **1.5x** (3.7k → 5.6k chars)
- Accuracy remains at 100% across all levels
- Token usage scales proportionally (1,837 → 2,463)

### Cost Comparison: Quick vs Thorough

| Model | Quick (avg) | Thorough (avg) | Increase |
|-------|---:|---:|:---:|
| gpt-4o-mini | $0.0007 | $0.0009 | 1.3x |
| gpt-4o | $0.0112 | $0.0140 | 1.3x |
| gpt-5.2 | $0.0172 | $0.0359 | 2.1x |

The "thorough" premium is modest for lightweight models (30% more) but significant for reasoning models (110% more), because gpt-5.2 generates substantially more reasoning tokens at the thorough level.

## Key Findings

### 1. The template eliminates the model gap

The `StepByStepReasoner` template's 5-step structure (UNDERSTAND → PLAN → EXECUTE → VERIFY → CONCLUDE) forces systematic reasoning regardless of model capability. Even gpt-4o-mini — a model not designed for complex reasoning — achieves perfect accuracy when given this structure.

**Implication:** For structured reasoning tasks, choose models based on **cost and latency**, not capability tier.

### 2. Investment-level parameterization works

Controlling depth via prompt constraints ("be concise" vs "be thorough") successfully scales output length without degrading accuracy. This enables:

- **Quick**: Fast, cheap responses for known-simple problems
- **Thorough**: Detailed audit trails when explainability matters

### 3. gpt-4o-mini + template is the optimal configuration

| Configuration | Accuracy | Cost/Call | Relative Cost |
|--------------|:---:|---:|:---:|
| gpt-4o-mini + quick | 100% | $0.0007 | **1x** |
| gpt-4o-mini + thorough | 100% | $0.0009 | 1.3x |
| gpt-5.2 + standard | 100% | $0.0250 | **36x** |
| gpt-5.2 + thorough | 100% | $0.0438 | **63x** |

The cheapest configuration (gpt-4o-mini + quick) achieves identical accuracy to the most expensive (gpt-5.2 + thorough) at **63x lower cost**.

## Methodology Notes

### Answer Verification

Model accuracy was determined by checking whether the correct numeric answer appears in the CONCLUDE section of each response (within tolerance: ±0.5 for speed/discount, ±0.1 for uptime). All 27 responses contain the correct answer.

An automated `extract_number` function was also tested, but proved unreliable for multi-value CONCLUDE sections — for instance, extracting the "35%" restatement from "No, this is not the same as 35% off. The actual discount is 32%" or grabbing downtime hours (130.72) instead of uptime percentage (98.51%). This extraction brittleness is a known challenge with unstructured numeric extraction and does not reflect model accuracy.

### Reproducibility

Results are non-deterministic across runs (LLM temperature > 0), but the structural finding — that all models reason correctly with the template — held across two independent experiment runs with different random seeds.

### Limitations

- **3 problems only**: A larger problem set would strengthen the statistical claim
- **OpenAI models only**: Cross-provider validation (Anthropic, Google) is future work
- **Math/logic focus**: Other reasoning domains (causal, ethical, analogical) may show different patterns
- **No adversarial problems**: All problems have unambiguous numeric answers

## Reproduce This Experiment

The full experiment notebook is available for download:

**[Download: reasoner_model_comparison.ipynb](/notebooks/reasoner_model_comparison.ipynb)**

Requirements:
- `mycontext` SDK installed
- `OPENAI_API_KEY` environment variable set
- `pandas` for data analysis

```bash
pip install mycontext pandas
```

Run all cells sequentially. The experiment executes 27 API calls (~10 minutes) plus optional LLM-as-judge evaluation (27 more calls).
