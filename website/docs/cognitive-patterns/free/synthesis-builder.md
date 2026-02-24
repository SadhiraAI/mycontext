---
sidebar_position: 14
title: SynthesisBuilder
description: Synthesize multiple sources into a coherent integrated understanding. Identify themes, resolve contradictions, and extract meta-insights no single source reveals.
---

# SynthesisBuilder

**Category:** Specialized | **Module:** `mycontext.templates.free.specialized`

Builds comprehensive syntheses from multiple information sources. Finds common themes, identifies complementary insights, resolves contradictions, and produces a unified narrative greater than the sum of its parts. Includes an evidence matrix mapping claims to sources.

## When to Use

- Research literature review synthesis
- Market research consolidation
- Multiple report summarization
- Customer feedback synthesis
- Expert opinion integration
- Due diligence across multiple sources
- Any task requiring coherent integration of diverse inputs

## Quick Start

```python
from mycontext.templates.free.specialized import SynthesisBuilder

builder = SynthesisBuilder()

ctx = builder.build_context(
    sources=[
        "McKinsey report: AI adoption in enterprise increased 40% in 2024, with ROI averaging 3.5x",
        "Gartner survey: 68% of CIOs say talent gap is the biggest AI barrier, not technology",
        "MIT study: Companies with AI governance frameworks see 2x better outcomes than ungoverned",
        "Internal data: Our customer AI adoption is 23%, below 40% industry average",
    ],
    goal="Unified picture of enterprise AI adoption landscape and strategic implications",
)
result = ctx.execute(provider="openai")
print(result.response)
```

## Methods

### `build_context(sources=None, goal="Unified understanding", context=None)`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sources` | `list[str] \| None` | `None` | List of source descriptions or summaries |
| `goal` | `str` | `"Unified understanding"` | What the synthesis should produce |
| `context` | `str \| None` | `None` | Purpose or framing for the synthesis |

### `execute(provider, sources=None, goal="Unified understanding", context=None, **kwargs)`

```python
result = builder.execute(
    provider="openai",
    sources=[
        "Research Paper A: Deep learning approach shows 92% accuracy",
        "Industry Report B: Interpretability is top concern for 78% of practitioners",
        "Case Study C: Company X achieved 2x efficiency but needed 6 months training",
    ],
    goal="Guide for organizations evaluating deep learning adoption",
)
```

## 8-Section Synthesis Framework

1. **Source Analysis** — Each source: key points, perspective, evidence strength
2. **Common Themes** — Patterns that emerge across multiple sources
3. **Complementary Insights** — How sources complete each other's picture
4. **Contradictions & Tensions** — Where sources disagree and how to resolve
5. **Synthesis Narrative** — Integrated understanding (more than sum of parts)
6. **Meta-Insights** — Patterns and gaps that only emerge by viewing sources together
7. **Evidence Matrix** — Claims × Sources × Confidence table
8. **Synthesis Quality Assessment** — Completeness, coherence, insight depth, limitations

## The Evidence Matrix

The synthesis produces a structured evidence table:

```
| Claim | Source A | Source B | Source C | Strength |
|-------|----------|----------|----------|---------|
| AI ROI averages 3.5x | ✓ Strong | — | Partial | Strong |
| Talent gap is primary barrier | — | ✓ Strong | ✓ Medium | Strong |
| Governance improves outcomes | — | — | ✓ Strong | Medium |
| Our adoption lags industry | — | — | — | High (internal) |
```

## Handling Contradictions

The synthesis explicitly addresses where sources disagree — a common weakness in manual synthesis that this pattern forces you to resolve:

```
Contradiction: Research Paper A claims 92% accuracy. 
Industry Report B says "real-world accuracy drops to 60-70% in production."

Resolution: These are measuring different things. Lab benchmarks vs. 
production deployment — real-world performance includes distribution shift, 
edge cases, and poor input quality. Both are correct in their context.
```

## Examples

### Research Synthesis

```python
result = builder.execute(
    provider="anthropic",
    sources=[
        "Paper 1: Intermittent fasting reduces insulin resistance (n=127, RCT)",
        "Paper 2: Time-restricted eating shows no significant metabolic benefit (n=89, RCT)",
        "Meta-analysis: Effect size d=0.3, significant heterogeneity across studies",
        "Clinical guidelines: IF not recommended for Type 1 diabetics",
    ],
    goal="Clinical guidance summary for general practitioners",
)
```

### Competitive Intelligence

```python
result = builder.execute(
    provider="openai",
    sources=[
        "Competitor A: Launched enterprise tier, pricing at 3x our current rate",
        "Review site analysis: Customers value ease-of-use over advanced features 2:1",
        "Sales loss interviews: 40% cite missing feature X, 35% cite pricing",
        "Analyst report: Market growing 45% YoY, consolidation expected in 18 months",
    ],
    goal="Strategic positioning recommendations for our product roadmap",
)
```

### Customer Feedback Synthesis

```python
feedback_sources = [
    "NPS survey: 42 average, top detractor reason: slow customer support (n=312)",
    "Churn interviews: 6/10 churned customers mention missing integration with Salesforce",
    "Support tickets: 35% of volume is about the same 3 configuration questions",
    "User forum: Power users requesting API-first access (847 upvotes)",
]

result = builder.execute(
    provider="openai",
    sources=feedback_sources,
    goal="Priority list for product improvements that address the most critical friction",
)
```

## Meta-Insights

The most valuable output is often the meta-insights — patterns that only emerge when you see all sources together:

```
Meta-insight 1: All sources agree on the opportunity (AI is valuable) 
but disagree on the HOW. The debate isn't about whether, but about 
sequencing. Sources suggesting "slow down" are about implementation 
risk, not strategic merit.

Meta-insight 2: There's a systematic gap — no source addresses the 
mid-market. All evidence is either enterprise (McKinsey, Gartner) or 
startup (tech press). Our SMB customers are an underresearched segment.
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(sources, goal, context)` | `Context` | Assembled context |
| `execute(provider, sources, goal, context, **kwargs)` | `ProviderResponse` | Execute synthesis |
| `generic_prompt(sources, goal, context_section)` | `str` | Zero-cost prompt string |
