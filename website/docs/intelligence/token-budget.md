---
sidebar_position: 10
title: Token-Budget Assembly
description: Fit any Context precisely within a model's context window using assemble_for_model() — tiktoken-accurate, priority-ordered section trimming.
---

# Token-Budget Assembly

`assemble_for_model()` produces a prompt that is guaranteed to fit within a model's context window. It counts tokens accurately with `tiktoken`, orders sections by priority, and trims only what doesn't fit — no guesswork, no silent overflow.

## Why It Matters

Standard `assemble()` returns the full prompt without checking whether it fits. For large knowledge documents, long examples, or complex constraints, this can exceed the model's context window and cause truncation or errors at the API level — silently, or with a cryptic token-limit error.

`assemble_for_model()` solves this by:

1. Counting every section's tokens accurately (per-model with `tiktoken`)
2. Including sections in priority order: role → directive → rules → constraints → knowledge → examples
3. Trimming the lowest-priority content to fit when the budget is tight
4. Always including the core role and directive

## Basic Usage

```python
from mycontext import Context, Guidance, Directive, Constraints

ctx = Context(
    guidance=Guidance(
        role="Senior security engineer",
        goal="Find all exploitable vulnerabilities",
        rules=["Flag every OWASP Top 10 risk", "Suggest concrete fixes"],
    ),
    directive=Directive("Audit this authentication middleware."),
    knowledge="[OWASP Top 10 2023 full text — 12,000 tokens]",
    constraints=Constraints(must_include=["severity rating", "code fix"]),
)

# Fit within gpt-4o-mini's default window
prompt = ctx.assemble_for_model(model="gpt-4o-mini")
print(f"Prompt: {len(prompt)} chars")

# Hard cap at a custom budget (e.g., leave room for response tokens)
prompt = ctx.assemble_for_model(model="gpt-4o", max_tokens=3000)
```

## Section Priority Order

When the budget is tight, sections are included in this order, and the last ones are trimmed first:

| Priority | Section | Always included? |
|----------|---------|-----------------|
| 1 | Role (`guidance.role`) | Yes |
| 2 | Directive (task) | Yes |
| 3 | Goal | When space allows |
| 4 | Rules | When space allows |
| 5 | Constraints | When space allows |
| 6 | Knowledge | Trimmed first when tight |
| 7 | Examples | Trimmed when tight |
| 8 | Style / expertise | Trimmed last |

The role and directive are always included — they define what the LLM is and what it needs to do. If even these exceed the budget, a `ValueError` is raised.

## Model-Specific Budgets

Pass `model` to use the model's known context window:

```python
# GPT-4o-mini — 128k tokens
prompt = ctx.assemble_for_model(model="gpt-4o-mini")

# GPT-4o — 128k tokens
prompt = ctx.assemble_for_model(model="gpt-4o")

# Claude 3.5 Sonnet — 200k tokens
prompt = ctx.assemble_for_model(model="claude-3-5-sonnet-20241022")

# Custom budget — useful inside agentic loops where you reserve space for history
prompt = ctx.assemble_for_model(model="gpt-4o", max_tokens=4000)
```

When `tiktoken` doesn't know the model, it falls back to `cl100k_base` encoding (GPT-4 standard).

## Token Counting Utilities

The token counting functions are available standalone:

```python
from mycontext.utils.tokens import count_tokens, fits_in_window, token_budget_remaining

# Count tokens for a string + model
n = count_tokens("Hello, world!", model="gpt-4o-mini")  # → 4

# Check if a prompt fits
ok = fits_in_window("Very long text...", model="gpt-4o-mini")  # → True/False

# How many tokens remain after a string
remaining = token_budget_remaining("System prompt text", model="gpt-4o-mini")
# → 127983 (128000 - 17)

# Estimate cost
from mycontext.utils.tokens import estimate_cost_usd
cost = estimate_cost_usd(input_tokens=1000, output_tokens=500, model="gpt-4o-mini")
# → 0.000225 (USD)
```

## With Long Knowledge Documents

`assemble_for_model()` is especially useful when you inject retrieved documents into `knowledge`:

```python
from mycontext import Context, Guidance, Directive

# Large retrieved context — 8,000 tokens
retrieved_docs = load_documents(query)

ctx = Context(
    guidance=Guidance(role="Research analyst"),
    directive=Directive("Summarize the key findings from the attached documents."),
    knowledge=retrieved_docs,
)

# Fits exactly within 4k budget, trimming knowledge if needed
prompt = ctx.assemble_for_model(model="gpt-4o-mini", max_tokens=4000)
result = ctx.execute(provider="openai", model="gpt-4o-mini")
```

## Combining with Async Execution

```python
async def analyze_with_budget(docs: str, question: str) -> str:
    ctx = Context(
        guidance=Guidance(role="Expert analyst"),
        directive=Directive(question),
        knowledge=docs,
    )
    # Build budget-aware prompt first
    prompt = ctx.assemble_for_model(model="gpt-4o-mini", max_tokens=8000)
    
    # Execute with the trimmed context
    result = await ctx.aexecute(provider="openai", model="gpt-4o-mini")
    return result.response
```

## Installation

`assemble_for_model()` requires `tiktoken` for accurate token counting:

```bash
pip install tiktoken
# or
pip install "mycontext-ai[tokens]"
```

Without `tiktoken`, the method falls back to a character-based estimate (approximately 4 chars per token). The fallback is safe but less precise.

## Reference

| Method | Signature | Description |
|--------|-----------|-------------|
| `ctx.assemble_for_model` | `(model, max_tokens?)` | Build token-budget-aware prompt |
| `count_tokens` | `(text, model)` | Count tokens for a string |
| `fits_in_window` | `(text, model)` | Check if text fits |
| `token_budget_remaining` | `(text, model)` | Remaining tokens after `text` |
| `estimate_cost_usd` | `(input_tokens, output_tokens, model)` | Estimated USD cost |

**Related:**
- [Async Execution →](./async-execution)
- [Context Object →](../foundations/context-object)
- [Security, Reliability & Performance →](../advanced/reliability)
