---
sidebar_position: 2
title: Quick Start
description: Build your first context, export to any LLM, and use the intelligence layer — in under 5 minutes.
---

# Quick Start

Build your first context in 30 seconds. Use the intelligence layer in 60. This guide assumes you've already [installed mycontext-ai](./installation).

## Your First Context

A `Context` combines four building blocks: **who the AI should be** (Guidance), **what it should do** (Directive), **what it must not do** (Constraints), and optional **thinking strategies and examples** that improve reasoning quality.

```python
from mycontext import Context, Guidance, Directive, Constraints

ctx = Context(
    guidance=Guidance(
        role="Senior security reviewer",
        goal="Find all exploitable vulnerabilities and give concrete fixes",
        rules=["Flag every injection risk", "Suggest concrete fixes"],
        style="concise, actionable",
    ),
    directive=Directive(
        content="Review this API endpoint for authentication and input validation vulnerabilities."
    ),
    constraints=Constraints(
        must_include=["severity rating", "code fix"],
        must_not_include=["generic advice"],
        format_rules=["Use markdown tables for findings"],
    ),
)
```

## Export to Any LLM

One context, every provider. No rewriting.

```python
# OpenAI
messages = ctx.to_openai()
# → [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]

# Anthropic (Claude)
payload = ctx.to_anthropic()
# → {"system": "...", "messages": [{"role": "user", "content": "..."}]}

# Google (Gemini)
payload = ctx.to_google()

# LangChain
messages = ctx.to_langchain()

# Or any of 13 formats
ctx.to_yaml()        # Portable config
ctx.to_json()        # JSON
ctx.to_xml()         # XML
ctx.to_markdown()    # Human-readable
ctx.to_messages()    # Universal message list
```

## Execute Directly

Skip the export step — send the context straight to an LLM:

```python
# Requires: pip install litellm
# Requires: OPENAI_API_KEY environment variable

result = ctx.execute(provider="openai")
print(result)
```

This routes through LiteLLM, giving you access to 100+ models. Change `provider="anthropic"` or `provider="google"` to switch — no code changes needed.

## Structure Your Context for Maximum Quality

Use `research_flow=True`, `thinking_strategy`, and `examples` together to get a structured nine-section prompt. The task always arrives last, the reasoning strategy shapes how the model approaches the problem, and examples calibrate its output format before it sees the actual task:

```python
from mycontext import Context, Guidance, Directive, Constraints

ctx = Context(
    guidance=Guidance(
        role="Senior security reviewer",
        goal="Find all exploitable vulnerabilities and give concrete fixes",
        rules=["Flag every injection risk", "Suggest concrete fixes with code"],
        style="concise, actionable",
    ),
    directive=Directive(
        content="Review this authentication middleware for vulnerabilities."
    ),
    thinking_strategy="verify",
    examples=[
        {
            "input": "session.permanent = True",
            "output": "Medium — sessions never expire; add SESSION_LIFETIME config",
        },
    ],
    constraints=Constraints(
        must_include=["severity rating", "code fix"],
        output_schema=[
            {"name": "finding", "type": "str"},
            {"name": "severity", "type": "str"},
            {"name": "fix", "type": "str"},
        ],
    ),
    research_flow=True,
)
```

Five thinking strategies are available — `step_by_step`, `multiple_angles`, `verify`, `explain_simply`, `creative` — each encoding a distinct cognitive approach. [Full strategy guide →](../foundations/research-flow)

## Use Cognitive Patterns

Cognitive patterns are pre-built context templates backed by real research. Instead of writing ad-hoc prompts, use proven reasoning frameworks:

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

ctx = RootCauseAnalyzer().build_context(
    problem="API response times tripled after last deployment",
    depth="comprehensive",
)

# The context now contains Five Whys + Ishikawa analysis methodology
print(ctx.to_markdown())

# Execute it
result = ctx.execute(provider="openai")
```

There are **16 free patterns** covering analysis, reasoning, planning, communication, and specialized tasks. [See all patterns →](../cognitive-patterns/overview)

## Let the Intelligence Layer Choose

Don't know which pattern fits? Let the SDK figure it out:

```python
from mycontext.intelligence import smart_execute

response, meta = smart_execute(
    "Why did API response times triple after last deployment?",
    provider="openai",
)

print(meta["templates_used"])  # ['root_cause_analyzer']
print(meta["mode"])            # 'single_template'
print(response)                # Structured root cause analysis
```

`smart_execute` analyzes your question, selects the optimal pattern, builds the context, and returns the response — all in one call.

## Measure Quality

Score any context on 6 dimensions — no more guessing:

```python
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics()
score = metrics.evaluate(ctx)

print(f"Overall: {score.overall:.2f}")
print(f"Clarity: {score.dimensions['clarity']:.2f}")
print(f"Completeness: {score.dimensions['completeness']:.2f}")
print(metrics.report(score))
```

## Three Ways to Use mycontext-ai

| Approach | When to use | Example |
|----------|-------------|---------|
| **Build manually** | You know exactly what context you need | `Context(guidance=..., directive=...)` |
| **Use a pattern** | You know the reasoning method | `RootCauseAnalyzer().build_context(...)` |
| **Let the SDK choose** | You have a question, want the best answer | `smart_execute("Your question")` |

## What's Next

- **[Core Concepts](./core-concepts)** — understand Context, Guidance, Directive, Constraints, and the research flow
- **[Prompt Assembly & Thinking Strategies](../foundations/research-flow)** — the nine-section structure, each thinking strategy in depth, and how few-shot examples are placed
- **[Cognitive Patterns](../cognitive-patterns/overview)** — browse all 85 patterns
- **[Intelligence Layer](../intelligence/overview)** — auto-transform, pattern suggestion, multi-template fusion
- **[Quality Metrics](../quality/quality-metrics)** — score and compare contexts
- **[Integrations](../integrations/overview)** — drop into LangChain, CrewAI, AutoGen, and more
