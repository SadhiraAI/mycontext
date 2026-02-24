---
sidebar_position: 3
title: HypothesisGenerator
description: Generate well-formed, testable hypotheses following scientific method — with null hypotheses, experimental designs, and falsifiability built in.
---

# HypothesisGenerator

**Category:** Reasoning | **Module:** `mycontext.templates.free.reasoning`

Generates well-formed, testable hypotheses from observations. Implements the scientific method: primary hypothesis (H1), null hypothesis (H0), alternative hypotheses, testable predictions, experimental design, success criteria, and rival hypotheses. Every hypothesis produced is falsifiable by design.

## When to Use

- Research and experimentation planning
- A/B test hypothesis formulation
- Product analytics investigations
- Scientific research methodology
- Business hypothesis-driven decision making
- Explaining unexpected observations

## Quick Start

```python
from mycontext.templates.free.reasoning import HypothesisGenerator

gen = HypothesisGenerator()

result = gen.execute(
    provider="openai",
    observation="Sales increase significantly when we send email reminders 24 hours before subscription renewal",
    domain="e-commerce",
)
print(result.response)
```

## Methods

### `build_context(observation, domain="general", context=None)`

```python
ctx = gen.build_context(
    observation="Users who complete onboarding in under 10 minutes have 3x higher 90-day retention",
    domain="SaaS product",
    context="Sample of 10,000 users over 6 months",
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `observation` | `str` | `""` | The observed phenomenon to explain |
| `domain` | `str` | `"general"` | Domain context — shapes variable selection and examples |
| `context` | `str \| None` | `None` | Additional context about the observation |

### `execute(provider, observation, domain="general", context=None, **kwargs)`

```python
result = gen.execute(
    provider="openai",
    observation="Mobile users have 2x higher bounce rate than desktop users",
    domain="web analytics",
    context="E-commerce site, Q4 data, all user segments",
)
```

## Generated Output Structure

Each run produces a 10-section scientific document:

1. **Observation Analysis** — What exactly was observed, context, significance
2. **Background Knowledge** — Relevant theory, prior findings, possible mechanisms
3. **Hypothesis Formulation**
   - **H1 (Primary)**: Cause-effect statement, variables, mechanism
   - **H0 (Null)**: No-effect statement
   - **H2, H3 (Alternatives)**: Other possible explanations
4. **Testable Predictions** — Specific outcomes if H1 is true vs. false
5. **Variables & Controls** — Independent, dependent, control, confounding variables
6. **Experimental Design** — Method, sample size, conditions, measurements
7. **Success Criteria** — Statistical thresholds and practical significance
8. **Limitations & Assumptions** — Boundary conditions
9. **Rival Hypotheses** — Competing explanations and how to distinguish them
10. **Next Steps** — Immediate, short-term, and long-term actions

## Examples

### Product A/B Test Hypothesis

```python
result = gen.execute(
    provider="openai",
    observation="Users who see the pricing page before signing up convert at 18% vs 12% for direct sign-up",
    domain="SaaS conversion optimization",
)
```

### Scientific Research

```python
result = gen.execute(
    provider="anthropic",
    observation="Patients who exercise 3x/week report 40% reduction in chronic pain scores after 8 weeks",
    domain="clinical research",
    context="Retrospective study, N=200, ages 40-65",
)
```

### Business Analytics

```python
result = gen.execute(
    provider="gemini",
    observation="Customer support tickets spike every Tuesday afternoon by 300%",
    domain="customer operations",
    context="B2B SaaS product, global customer base",
)
```

## The Falsifiability Principle

All hypotheses generated follow the Popperian principle of falsifiability — they must be testable and potentially refutable by evidence. The pattern enforces this through:

- **Testable predictions**: Specific outcomes that would confirm or deny H1
- **Null hypothesis**: Explicit no-effect baseline for statistical testing
- **Success criteria**: Quantitative thresholds for accepting or rejecting H0
- **Rival hypotheses**: Alternative explanations that must also be tested

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(observation, domain, context)` | `Context` | Assembled context |
| `execute(provider, observation, domain, context, **kwargs)` | `ProviderResponse` | Execute and return hypotheses |
| `generic_prompt(observation, domain, context_section)` | `str` | Zero-cost prompt string |
