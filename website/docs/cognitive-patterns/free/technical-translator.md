---
sidebar_position: 12
title: TechnicalTranslator
description: Convert technical jargon into plain language with a full translation map. The "12-year-old test" — accurate, accessible, never condescending.
---

# TechnicalTranslator

**Category:** Communication | **Module:** `mycontext.templates.free.communication`

Converts technical content into plain, accessible language. Produces a jargon translation map, a fully rewritten plain-language version, and a verification checklist — all while maintaining factual accuracy. Applies the "12-year-old test": would someone outside the field understand this?

## When to Use

- Making developer docs readable by product managers
- Translating engineering updates for leadership
- Writing help center articles for non-technical users
- Simplifying legal or compliance language
- Creating accessible versions of technical specifications
- Press releases from technical announcements

## Quick Start

```python
from mycontext.templates.free.communication import TechnicalTranslator

translator = TechnicalTranslator()

ctx = translator.build_context(
    technical_text="Our microservices architecture uses event-driven patterns with Kafka for async message processing, enabling horizontal scaling without tight coupling between services",
    target_audience="business stakeholders",
)
result = ctx.execute(provider="openai")
print(result.response)
```

## Methods

### `build_context(technical_text, target_audience="general public", context=None)`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `technical_text` | `str` | `""` | The technical content to translate |
| `target_audience` | `str` | `"general public"` | Who needs to understand it |
| `context` | `str \| None` | `None` | Purpose of the translation |

### `execute(provider, technical_text, target_audience="general public", context=None, **kwargs)`

```python
result = translator.execute(
    provider="openai",
    technical_text="The LLM fine-tuning pipeline uses LoRA adapters with 4-bit quantization to reduce VRAM requirements while maintaining 95% of baseline performance on downstream task benchmarks",
    target_audience="marketing team",
)
```

## Output Structure

1. **Jargon Identification** — All technical terms, acronyms, domain-specific language found
2. **Translation Map** — Term-by-term table: technical term → plain language equivalent
3. **Translated Version** — Complete rewrite with no jargon remaining
4. **Verification**
   - Would a 12-year-old understand? (Yes/No)
   - Key concepts preserved? (Yes/No)
   - Examples included? (Yes/No)

## Translation Map Example

```
| Technical | Plain Language |
|-----------|---------------|
| Microservices | Small, independent programs that each do one job |
| Event-driven | The programs talk to each other by sending messages |
| Kafka | A messaging system that holds messages in order |
| Async processing | Handling tasks in the background without waiting |
| Horizontal scaling | Adding more computers to handle more work |
| Tight coupling | When programs depend so much on each other that a change in one breaks others |
```

## Examples

### AI/ML for Non-Technical

```python
result = translator.execute(
    provider="openai",
    technical_text="""
    Our transformer architecture with self-attention mechanisms and positional 
    encodings achieves SOTA results on multiple NLU benchmarks. The model uses 
    RLHF with a preference model trained on human feedback to align outputs 
    with human values.
    """,
    target_audience="product managers with no ML background",
)
```

### Infrastructure for Business

```python
result = translator.execute(
    provider="anthropic",
    technical_text="We've achieved 99.99% uptime SLA through multi-region active-active deployment with automated failover using health check endpoints and circuit breakers",
    target_audience="enterprise sales prospects",
)
```

### Legal/Compliance for End Users

```python
result = translator.execute(
    provider="gemini",
    technical_text="By accepting these terms, you grant us a non-exclusive, worldwide, royalty-free, sublicensable license to use, reproduce, modify, adapt, publish, translate, create derivative works from, distribute, perform, and display your User Content",
    target_audience="everyday users signing up for a service",
)
```

### API Docs for Beginners

```python
result = translator.execute(
    provider="openai",
    technical_text="""
    Authentication is performed via OAuth2 Bearer tokens. Include the Authorization 
    header with your JWT. Token refresh is handled via the /auth/token endpoint 
    using the refresh_token from your session store. Rate limiting applies at 
    1000 req/min per API key.
    """,
    target_audience="non-developer users trying to set up an integration",
)
```

## The 12-Year-Old Test

:::tip The gold standard for plain language
After translation, the pattern applies a simple test: "Would a 12-year-old who is smart but hasn't studied this topic understand every sentence?" This isn't about dumbing down — it's about removing unnecessary complexity. Every concept can be explained clearly; jargon just shortens explanations for experts who already know the terms.
:::

## Accuracy Preservation

The pattern explicitly warns against:
- Sacrificing technical correctness for simplicity
- Introducing misleading analogies that misrepresent the concept
- Omitting important caveats or conditions
- Overgeneralizing nuanced technical points

The verification step confirms all key concepts were preserved.

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(technical_text, target_audience, context)` | `Context` | Assembled context |
| `execute(provider, technical_text, target_audience, context, **kwargs)` | `ProviderResponse` | Execute translation |
| `generic_prompt(technical_text, target_audience, context_section)` | `str` | Zero-cost prompt string |
