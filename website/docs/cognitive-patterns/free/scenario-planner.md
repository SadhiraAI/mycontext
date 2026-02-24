---
sidebar_position: 9
title: ScenarioPlanner
description: Strategic scenario planning with a 2×2 matrix methodology. Build four distinct futures, analyze implications, identify robust strategies, and establish signposts.
---

# ScenarioPlanner

**Category:** Planning | **Module:** `mycontext.templates.free.planning`

Develops multiple future scenarios using the classic 2×2 matrix methodology from Shell's scenario planning tradition. Identifies the two most critical uncertainties as axes, constructs four distinct scenarios, analyzes implications for each, finds strategies that are robust across scenarios, and establishes observable signposts.

## When to Use

- Strategic planning (1-5+ year horizons)
- Market entry decisions
- Technology investment under uncertainty
- Industry disruption analysis
- Organizational change planning
- Any decision with significant future uncertainty

## Quick Start

```python
from mycontext.templates.free.planning import ScenarioPlanner

planner = ScenarioPlanner()

ctx = planner.build_context(
    topic="The future of AI in enterprise software development",
    timeframe="2025-2030",
)
result = ctx.execute(provider="openai")
print(result.response)
```

## Methods

### `build_context(topic, timeframe="5 years", context=None)`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `topic` | `str` | `""` | Topic or decision domain to scenario-plan |
| `timeframe` | `str` | `"5 years"` | Planning horizon |
| `context` | `str \| None` | `None` | Current situation, relevant trends, constraints |

### `execute(provider, topic, timeframe="5 years", context=None, **kwargs)`

```python
result = planner.execute(
    provider="openai",
    topic="Future of remote work policies for technology companies",
    timeframe="2026-2031",
    context="Post-pandemic, AI productivity tools emerging, talent market shifting",
)
```

## The 2×2 Scenario Methodology

The pattern identifies two **critical uncertainties** — the most important, most uncertain factors that will shape the future. These become the two axes of a matrix, producing four distinct scenarios:

```
                    HIGH Uncertainty 2
                          ▲
                          │
     Scenario C  ─────────┼───────── Scenario A
                          │
LOW ◄──────────────────── ┼────────────────────► HIGH
 Uncertainty 1            │          Uncertainty 1
                          │
     Scenario D  ─────────┼───────── Scenario B
                          │
                    LOW Uncertainty 2
```

**Example axes** for AI in enterprise:
- Axis 1: AI capability speed (Gradual → Exponential)
- Axis 2: Regulatory environment (Permissive → Restrictive)

## 10-Section Analysis

1. **Current State Assessment** — Present situation, key trends, momentum
2. **Critical Uncertainties** — Two uncertainty axes with range and impact explanation
3. **Four Scenarios** — Name, description, key characteristics, driving forces, probability %, early indicators
4. **Implications Analysis** — For each scenario: opportunities, threats, required capabilities
5. **Robust Strategies** — No-regret moves, hedging, shaping actions, adaptive strategies
6. **Scenario-Specific Strategies** — Optimal approach if each scenario materializes
7. **Signposts & Triggers** — Observable indicators that signal which scenario is emerging
8. **Preparedness Plan** — Immediate actions, monitoring plan, contingency plans
9. **Scenario Comparison Table** — Side-by-side on likelihood, impact, and strategic fit
10. **Strategic Recommendations** — Most likely, preferred, and how to shape the future

## Examples

### Technology Investment

```python
result = planner.execute(
    provider="openai",
    topic="Investment strategy for quantum computing capabilities",
    timeframe="2025-2035",
    context="Fortune 500 manufacturing company, $50M R&D budget",
)
```

### Market Entry

```python
result = planner.execute(
    provider="anthropic",
    topic="Expansion into Southeast Asian markets for B2B SaaS",
    timeframe="3 years",
    context="Current: US/EU focused, $20M ARR, 60-person team",
)
```

### Workforce Planning

```python
result = planner.execute(
    provider="gemini",
    topic="Future of remote vs. hybrid work for our engineering organization",
    timeframe="2026-2029",
    context="Currently 70% remote, offices in SF and NYC, 200 engineers",
)
```

## Robust vs. Scenario-Specific Strategies

:::info Key insight
The most valuable output is often the "robust strategies" — actions that create value regardless of which scenario unfolds. These are your no-regret investments.
:::

| Strategy Type | Description | Example |
|--------------|-------------|---------|
| **No-regret moves** | Good in all scenarios | Build API-first architecture (valuable in all AI futures) |
| **Hedging** | Reduce downside in bad scenarios | Diversify customer concentration |
| **Shaping** | Influence which scenario emerges | Engage regulators proactively |
| **Adaptive** | Designed to pivot | Keep options open, avoid lock-in |
| **Scenario-specific** | Only valuable in one scenario | Aggressive hiring if AI is slower |

## Signposts

Signposts are concrete, observable events that indicate which scenario is unfolding. They enable the monitoring plan:

```
Signpost: "Major LLM provider announces API pricing cut > 80%"
- Signals: Scenario A (rapid AI adoption)
- When to check: Monthly monitoring of provider pricing
- Trigger: Accelerate AI integration roadmap

Signpost: "EU AI Act enforcement begins with first $10M+ fine"
- Signals: Scenario C (high regulation)
- When to check: Quarterly regulatory news review
- Trigger: Activate compliance contingency plan
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(topic, timeframe, context)` | `Context` | Assembled context |
| `execute(provider, topic, timeframe, context, **kwargs)` | `ProviderResponse` | Execute planning |
| `generic_prompt(topic, timeframe, context_section)` | `str` | Zero-cost prompt string |
