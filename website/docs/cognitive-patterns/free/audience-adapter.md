---
sidebar_position: 11
title: AudienceAdapter
description: Adapt any message for a different audience — adjust language, framing, examples, tone, and structure while preserving core accuracy.
---

# AudienceAdapter

**Category:** Communication | **Module:** `mycontext.templates.free.communication`

Adapts content for a different audience. Analyzes the target audience's expertise level, interests, and communication preferences — then rewrites the message with appropriate language, relevant examples, adjusted tone, and optimized structure. Preserves accuracy while maximizing resonance.

## When to Use

- Translating technical content for executives
- Adapting developer documentation for end-users
- Preparing the same announcement for different teams
- Sales pitches customized by industry or role
- Research findings summarized for different audiences
- Internal memos adapted for external publishing

## Quick Start

```python
from mycontext.templates.free.communication import AudienceAdapter

adapter = AudienceAdapter()

ctx = adapter.build_context(
    message="Our new transformer-based NLP pipeline achieves 94% F1 score on the benchmark with 2.3B parameters",
    current_audience="ML engineers",
    target_audience="C-suite executives",
)
result = ctx.execute(provider="openai")
print(result.response)
```

## Methods

### `build_context(message, current_audience="general", target_audience="specific group", context=None)`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `message` | `str` | `""` | The content to adapt |
| `current_audience` | `str` | `"general"` | Who the message was written for |
| `target_audience` | `str` | `"specific group"` | Who you want to reach |
| `context` | `str \| None` | `None` | Purpose or additional context |

### `execute(provider, message, current_audience, target_audience, context=None, **kwargs)`

```python
result = adapter.execute(
    provider="openai",
    message=your_technical_message,
    current_audience="engineering team",
    target_audience="board of directors",
)
```

## Adaptation Dimensions

The pattern adjusts content across six dimensions simultaneously:

| Dimension | What changes |
|-----------|-------------|
| **Language** | Technical level, jargon replacement, complexity |
| **Framing** | What's emphasized based on audience priorities |
| **Examples & Analogies** | Swapped for ones relevant to the target audience's domain |
| **Tone** | Formal/casual, authoritative/collaborative, detail/big-picture |
| **Structure** | Reorganized for how this audience consumes information |
| **Length** | Condensed or expanded based on attention span |

## Common Adaptations

### Technical → Executive

```python
result = adapter.execute(
    provider="openai",
    message="We've implemented a Redis-based distributed cache with LRU eviction, reducing p99 latency from 850ms to 120ms",
    current_audience="DevOps engineers",
    target_audience="VP of Product",
)
```

Adaptation effects:
- Redis/LRU → "smart memory system"
- p99 latency → "slowest 1% of requests"
- Framing shifts from technical spec → business value (8x faster = better user experience)

### Developer Docs → End User Docs

```python
result = adapter.execute(
    provider="anthropic",
    message="Configure OAuth2 PKCE flow with token refresh via the /auth/refresh endpoint with Bearer authentication",
    current_audience="developers",
    target_audience="non-technical business users",
)
```

### Research → General Public

```python
result = adapter.execute(
    provider="gemini",
    message="Meta-analysis of 23 RCTs (n=4,521) shows MBSR intervention has statistically significant effect on GAD-7 scores (p<0.001, d=0.48)",
    current_audience="clinical researchers",
    target_audience="people managing anxiety",
)
```

## 12-Section Output

1. **Target Audience Analysis** — Who they are, what they care about, communication preferences
2. **Language Adaptation** — Technical level adjustment, jargon translation table
3. **Core Message Extraction** — Essential points to preserve, what to emphasize/minimize
4. **Framing for Audience** — Value proposition reframed through their lens
5. **Example & Analogy Adaptation** — New examples relevant to target domain
6. **Tone & Style Adjustment** — Formality, energy, confidence levels
7. **Structure Optimization** — Opening, organization, flow, closing
8. **Adapted Message** — Fully rewritten version
9. **Key Adaptations Made** — Summary of every change and why
10. **Potential Questions** — What this audience will likely ask (with prepared answers)
11. **Delivery Recommendations** — Medium, timing, setting, support materials
12. **Success Indicators** — How to know the adaptation worked

## Multiple Audiences

Adapt the same message for multiple audiences:

```python
message = "We're rebuilding our infrastructure on Kubernetes with a 3-month migration timeline"

audiences = {
    "engineering": "DevOps and platform engineers",
    "sales": "Account executives closing enterprise deals",
    "investors": "Series B investors reviewing technical roadmap",
}

for key, audience in audiences.items():
    result = adapter.execute(
        provider="openai",
        message=message,
        current_audience="CTO",
        target_audience=audience,
    )
    print(f"\n--- For {key} ---")
    print(result.response)
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(message, current_audience, target_audience, context)` | `Context` | Assembled context |
| `execute(provider, message, current_audience, target_audience, context, **kwargs)` | `ProviderResponse` | Execute adaptation |
| `generic_prompt(message, current_audience, target_audience, context_section)` | `str` | Zero-cost prompt string |
