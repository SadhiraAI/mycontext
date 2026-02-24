---
sidebar_position: 9
title: Async Execution
description: Non-blocking LLM execution with ctx.aexecute() — native async/await, concurrent pattern fan-out, and FastAPI integration.
---

# Async Execution

`ctx.aexecute()` is a native `async` coroutine backed by `litellm.acompletion`. It never blocks the event loop and integrates directly into any `async` application without a thread pool.

## Basic Usage

```python
import asyncio
from mycontext import Context, Guidance, Directive

ctx = Context(
    guidance=Guidance(
        role="Senior data analyst",
        goal="Identify revenue anomalies",
    ),
    directive=Directive("Analyze Q3 revenue: revenue dropped 18% in APAC."),
)

async def main():
    result = await ctx.aexecute(provider="openai", model="gpt-4o-mini")
    print(result.response)
    print(f"Tokens: {result.tokens_used} | Model: {result.model}")

asyncio.run(main())
```

## Concurrent Execution

Fan out multiple contexts in parallel. Wall-clock time equals the slowest call — not the sum:

```python
from mycontext import Context, Guidance, Directive
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.templates.free.specialized import RiskAssessor

async def parallel_analysis(problem: str):
    ctx_root_cause = RootCauseAnalyzer().build_context(problem=problem, depth="thorough")
    ctx_risk = RiskAssessor().build_context(decision=problem, depth="comprehensive")
    ctx_summary = Context(
        guidance=Guidance(role="Executive analyst"),
        directive=Directive(f"Give a 3-sentence executive summary of: {problem}"),
    )

    root_cause, risk, summary = await asyncio.gather(
        ctx_root_cause.aexecute(provider="openai"),
        ctx_risk.aexecute(provider="openai"),
        ctx_summary.aexecute(provider="anthropic"),
    )

    return {
        "root_cause": root_cause.response,
        "risk": risk.response,
        "summary": summary.response,
    }
```

With three independent LLM calls averaging 2 seconds each, the total wall time is ~2 seconds instead of ~6.

## FastAPI Integration

`aexecute()` fits directly into FastAPI route handlers — no `run_in_executor`, no thread pools:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from mycontext import Context, Guidance, Directive

app = FastAPI()

class AnalyzeRequest(BaseModel):
    question: str
    provider: str = "openai"

@app.post("/analyze")
async def analyze(body: AnalyzeRequest):
    ctx = Context(
        guidance=Guidance(role="Expert analyst"),
        directive=Directive(body.question),
    )
    result = await ctx.aexecute(provider=body.provider)
    return {
        "response": result.response,
        "tokens_used": result.tokens_used,
        "model": result.model,
    }
```

## Streaming (via LiteLLM)

Pass LiteLLM streaming kwargs through `aexecute()`:

```python
result = await ctx.aexecute(
    provider="openai",
    model="gpt-4o",
    stream=True,
)
```

Note: when `stream=True`, `result.response` contains the assembled text after the stream completes.

## Provider Configuration

All `execute()` kwargs are accepted by `aexecute()`:

```python
result = await ctx.aexecute(
    provider="openai",
    model="gpt-4o",
    temperature=0.2,
    max_tokens=2048,
    api_key="sk-...",   # override env var
)

# Anthropic
result = await ctx.aexecute(provider="anthropic", model="claude-3-5-sonnet-20241022")

# Google
result = await ctx.aexecute(provider="google", model="gemini-1.5-pro")
```

## Error Handling

`aexecute()` propagates provider errors as exceptions. Wrap in `try/except` for production use:

```python
async def safe_execute(ctx: Context) -> str | None:
    try:
        result = await ctx.aexecute(provider="openai")
        return result.response
    except Exception as exc:
        # Log and handle — e.g., fall back to a different provider
        print(f"LLM call failed: {exc}")
        return None
```

The underlying `LiteLLMProvider` retries transient errors (rate limits, 5xx) with exponential backoff before raising.

## How It Works

`aexecute()` calls `litellm.acompletion()` directly — the same model/provider routing as `execute()`, but in a true coroutine. The execution trace (tokens, cost, latency) is recorded in the same in-process `Tracer` whether you use sync or async:

```python
from mycontext.utils.tracing import get_tracer

result = await ctx.aexecute(provider="openai")

spans = get_tracer().get_spans()
print(spans[-1].metadata)
# {'model': 'gpt-4o-mini', 'tokens': 312, 'cost_usd': 0.00012, 'latency_ms': 1842}
```

## Reference

| Signature | Description |
|-----------|-------------|
| `await ctx.aexecute(provider, **kwargs)` | Async LLM execution |
| `await asyncio.gather(*[ctx.aexecute(...) for ctx in contexts])` | Parallel execution |

**Related:**
- [Execution Tracing →](../advanced/reliability#execution-tracing)
- [Token-Budget Assembly →](./token-budget)
- [smart_execute() →](./smart-execute)
