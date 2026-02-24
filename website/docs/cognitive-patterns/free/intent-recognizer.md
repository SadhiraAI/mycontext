---
sidebar_position: 16
title: IntentRecognizer
description: Uncover the true intent behind any request. Multi-layer analysis from surface to deep goals, motivations, implicit assumptions, and optimal response strategy.
---

# IntentRecognizer

**Category:** Specialized | **Module:** `mycontext.templates.free.specialized`

Recognizes the true intent behind a question or request by going beyond the surface-level interpretation. Performs multi-layer analysis: surface request → immediate goal → underlying goal → long-term goal → motivations → implicit assumptions → reformulated true intent. Returns the real question and the optimal response strategy.

## When to Use

- Customer support — understand what users really need
- Building chatbots and AI assistants
- Pre-processing questions before routing or answering
- Product requirement clarification
- Sales and consulting qualification
- Improving RAG retrieval by understanding the actual need
- Designing user research questions

## Quick Start

```python
from mycontext.templates.free.specialized import IntentRecognizer

recognizer = IntentRecognizer()

ctx = recognizer.build_context(
    input="What's the best programming language to learn?",
    context="Asking for a friend who wants to switch careers from accounting",
    depth="comprehensive",
)
result = ctx.execute(provider="openai")
print(result.response)
```

## Methods

### `build_context(input, context=None, depth="comprehensive")`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` | `str` | `""` | The question or request to analyze |
| `context` | `str \| None` | `None` | Who is asking and why |
| `depth` | `str` | `"comprehensive"` | Analysis depth |

### `execute(provider, input, context=None, depth="comprehensive", **kwargs)`

```python
result = recognizer.execute(
    provider="openai",
    input="Can you help me write a resignation letter?",
    depth="comprehensive",
)
```

## Multi-Layer Intent Analysis

The pattern reveals the full intent stack:

```
User asks: "What's the best programming language to learn?"

Surface: Information request about programming languages

Immediate goal: Get a language recommendation

Underlying goal: Pick the right language to start learning coding

Long-term goal: Change careers or add programming skills to land a better job

Motivation: Career advancement, higher income, more interesting work

Implicit assumptions: Assumes "best" is universal (it isn't), assumes they need 
to choose before starting, may not know that starting matters more than which

True intent: "Help me get started programming in a way that matches 
my career goals"

Optimal response: Ask about career goals first, then recommend Python/JS 
with a concrete 30-day starter path — not an abstract language comparison
```

## 8-Section Analysis

1. **Surface Analysis** — Explicit request, key terms, literal question type
2. **Goal Inference** — Immediate, underlying, and long-term goals; success criteria
3. **Motivation Analysis** — What's driving the request; pain points, constraints, urgency
4. **Context Interpretation** — Situation, background, stakeholders, environment
5. **Implicit Assumptions** — Unstated beliefs, potential biases, knowledge gaps, misconceptions
6. **Need Classification** — Information / decision / action / validation need
7. **Reformulated Intent** — True intent, real question, optimal response type
8. **Recommendation** — How to best respond, what to include, what to avoid

## Need Classification

| Need Type | Description | Optimal response |
|-----------|-------------|-----------------|
| **Information** | They need facts or knowledge | Direct answer with explanation |
| **Decision** | They need to choose between options | Framework or comparison |
| **Action** | They need to do something | Step-by-step guide |
| **Validation** | They need confirmation or reassurance | Evaluation with honest assessment |

## Examples

### Customer Support Intent

```python
customer_message = "How do I cancel my subscription?"

result = recognizer.execute(
    provider="openai",
    input=customer_message,
    context="Paying customer, 8 months active, submitted ticket after failed upgrade",
    depth="comprehensive",
)
# Likely reveals: True intent is frustration with upgrade, not cancellation desire
# Optimal response: Acknowledge frustration, offer help with upgrade issue first
```

### Sales Qualification

```python
result = recognizer.execute(
    provider="anthropic",
    input="Do you have an enterprise plan?",
    context="Inbound inquiry from Fortune 500 company, VP Engineering",
    depth="comprehensive",
)
# Reveals: Not just pricing inquiry — evaluating whether vendor is enterprise-ready
```

### Product Requirements

```python
result = recognizer.execute(
    provider="gemini",
    input="Can we add a way to export data?",
    context="Request from power user who uses the tool daily for analytics",
    depth="comprehensive",
)
# Reveals: May want scheduled exports, or specific format for a specific tool
```

### AI Assistant Pre-Processing

```python
# Use IntentRecognizer as a pre-processing step for your AI assistant
def handle_user_query(user_input: str, context: str = ""):
    # Step 1: Understand the real intent
    intent = IntentRecognizer().execute(
        provider="openai",
        input=user_input,
        context=context,
        depth="comprehensive",
    )
    
    # Step 2: Use the analysis to route to the right handler
    # or to enrich the question before answering
    return route_to_handler(intent.response, user_input)
```

## The Gap Between Asked and Needed

:::tip The stated question is rarely the full picture
Research in human-computer interaction consistently shows that users' stated questions are proxies for their actual goals. A question like "what's the weather tomorrow?" could mean:
- I'm deciding what to wear (action need)
- I'm deciding whether to cancel outdoor plans (decision need)
- I'm checking if my flight might be delayed (information need)

The intent determines the optimal response format and content.
:::

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(input, context, depth)` | `Context` | Assembled context |
| `execute(provider, input, context, depth, **kwargs)` | `ProviderResponse` | Execute analysis |
| `generic_prompt(input, context_section, depth)` | `str` | Zero-cost prompt string |
