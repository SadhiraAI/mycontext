---
sidebar_position: 5
title: Security, Reliability & Performance
description: How mycontext-ai is built to be secure, reliable, and fast — injection prevention, structured error handling, token accuracy, caching, and async I/O.
---

# Security, Reliability & Performance

mycontext-ai is designed to be dropped into production systems. This page covers the engineering decisions that make it safe, predictable, and fast.

---

## Security

### Template Injection Prevention

Every template variable substitution goes through a hardened `safe_format_template` validator before values are inserted into prompt strings. Inputs that contain Python format-string escape sequences (`{attr.method}`, `{obj[key]}`, `__class__`, `__dict__`) are rejected with a clear `ValueError`.

This eliminates a class of prompt-injection attacks where adversarial user input could reshape the system prompt at runtime.

```python
from mycontext.utils.template_safety import safe_format_template

# Safe substitution
prompt = safe_format_template("Analyze {topic} for {audience}.", topic="revenue", audience="CFO")

# Rejected — attribute access could expose internals
safe_format_template("{obj.secret}", obj=some_object)
# → ValueError: Directive template contains unsafe placeholders
```

The validator distinguishes legitimate format specifiers (`{score:.2f}`) from attribute access (`{score.hidden}`) — only the latter is blocked.

### Structured Logging — No Silent Failures

Every exception in the intelligence layer is logged at `WARNING` level with full `exc_info=True` before falling back to an alternative path. Nothing is silently swallowed. If a call fails, you see it:

```
WARNING mycontext.intelligence.pattern_suggester:
  _suggest_with_llm: instructor path failed (ValidationError), falling back to regex parse.
  Error: 1 validation error for PatternSuggestionResponse …
```

This means you can wire your existing log aggregator (Datadog, Sentry, CloudWatch) to `mycontext.*` loggers and get full observability without any extra instrumentation.

---

## Reliability

### Pydantic-Validated Structured Output

All LLM responses that carry structured data (`suggest_patterns`, `generate_context`, `TemplateIntegratorAgent`) are parsed through Pydantic schemas with field validators. The parsing pipeline has three tiers:

1. **Instructor path** (when `instructor` is installed) — function-calling mode with up to 2 automatic retries. Parse failures re-prompt the model before surfacing an error.
2. **Pydantic + JSON extraction** — strips markdown fences, extracts the first JSON object, validates with the schema.
3. **Regex fallback** — field-by-field extraction for the rare case where the LLM returns free text.

```python
from mycontext.intelligence.schemas import PatternSuggestionResponse, parse_with_fallback

# parse_with_fallback tries JSON → Pydantic → raises ValueError with details
response = parse_with_fallback(PatternSuggestionResponse, raw_llm_text)
```

This three-tier approach means a single transient LLM formatting error will not break your pipeline.

### Execution Tracing

Every LLM call through `LiteLLMProvider` is wrapped in a lightweight `Span` that records model, provider, tokens used, latency, cost estimate, and any errors — all in-process, zero-overhead when not read:

```python
from mycontext.utils.tracing import get_tracer

tracer = get_tracer()
result = ctx.execute(provider="openai", model="gpt-4o-mini")

spans = tracer.get_spans()
for span in spans:
    print(f"{span.name} | {span.metadata['model']} | {span.duration_ms:.0f}ms | {span.metadata['tokens']} tokens")
```

Spans are stored in a thread-local `deque` with a configurable max size — no database, no network calls, no latency impact.

### Retry Logic

The LiteLLM provider retries transient failures (rate limits, timeouts, 5xx errors) with exponential backoff. Retry count and delays are configurable per call:

```python
result = ctx.execute(
    provider="openai",
    model="gpt-4o",
    max_retries=3,
)
```

---

## Performance

### Async-First Execution

`ctx.aexecute()` calls `litellm.acompletion` directly — a true non-blocking coroutine. FastAPI routes, async agent loops, and notebook cells can all `await` it without a thread pool:

```python
# FastAPI route — never blocks the event loop
@router.post("/analyze")
async def analyze(body: AnalyzeRequest) -> dict:
    ctx = build_context(body)
    result = await ctx.aexecute(provider="openai")
    return {"response": result.response}
```

Fan out multiple independent contexts in parallel — wall-clock time equals the slowest call, not the sum:

```python
results = await asyncio.gather(
    ctx_risk.aexecute(provider="openai"),
    ctx_synthesis.aexecute(provider="anthropic"),
    ctx_summary.aexecute(provider="openai"),
)
```

### In-Process Semantic Cache

Repeated identical prompts within a session are served from an in-process cache keyed by SHA-256 of the assembled prompt. Cache hits return immediately with zero LLM latency:

```python
from mycontext.utils import get_default_cache

cache = get_default_cache()
print(f"Cache size: {cache.size()} entries")

# Clear when context changes substantially
cache.clear()
```

The cache uses LRU eviction (configurable max size) and per-entry TTL. It is thread-safe via `threading.Lock`.

### Heuristic-First Routing

`smart_execute()` classifies question complexity before spending an LLM call on routing. Short, factual questions skip pattern selection entirely. Only genuinely complex, multi-domain questions go through the full LLM-based router. This cuts median latency for simple questions from ~2 LLM round-trips to 1.

### Parallel Template Refinement

When `PromptComposer` refines multiple templates simultaneously, it uses `ThreadPoolExecutor` to fan out the refinement calls — all templates are processed in parallel, not sequentially.

### Token-Accurate Truncation

`to_prompt()` and `assemble_for_model()` use `tiktoken` to count tokens precisely per model. The old character-based 6000-char cap is replaced by a model-aware token budget — so gpt-4o-mini contexts use their full 128k window efficiently, and nothing is over-truncated.

### Lazy Pattern Loading

The 85-pattern registry is loaded once and cached as a module-level singleton. Subsequent `TransformationEngine` instantiations reuse the same registry object — no repeated imports, no repeated reflection.

```python
# First call: loads and caches all patterns (~20ms one-time)
engine1 = TransformationEngine()

# Second call: reuses cached registry (<1ms)
engine2 = TransformationEngine()
```

---

## Summary

| Concern | Mechanism | Benefit |
|---------|-----------|---------|
| Prompt injection | `safe_format_template` validator | Blocks attribute/item access in templates |
| Silent failures | Structured `WARNING` logging + `exc_info=True` | Full stack trace in any log aggregator |
| LLM parse failures | 3-tier: instructor → Pydantic → regex | Single transient error doesn't break pipeline |
| Observability | In-process `Span` / `Tracer` | Token cost + latency per call, zero overhead |
| Transient errors | Exponential backoff retry | Handles rate limits and 5xx automatically |
| Blocking I/O | `ctx.aexecute()` native coroutine | Event loops never stall |
| Redundant LLM calls | SHA-256 keyed in-process cache | Zero latency on repeated prompts |
| Routing overhead | Heuristic-first complexity classifier | Simple questions skip LLM routing |
| Context overflow | `assemble_for_model()` token-accurate trimming | Guaranteed fit, no silent truncation |
| Pattern startup | Lazy singleton registry | One-time 20ms load, instant reuse |
