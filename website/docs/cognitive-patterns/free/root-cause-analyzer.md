---
sidebar_position: 1
title: RootCauseAnalyzer
description: Systematic root cause investigation using Five Whys and Ishikawa (fishbone) analysis. Find true causes, not just symptoms.
---

# RootCauseAnalyzer

**Category:** Reasoning | **Module:** `mycontext.templates.free.reasoning`

Systematic root cause investigation based on quality management and systems thinking methodologies. Uses Five Whys, Ishikawa (fishbone) analysis, and contributing factor identification to uncover the true cause of problems — not just their visible symptoms.

## When to Use

- Engineering incidents and outages
- Product quality defects
- Business performance drops
- Customer experience failures
- Process breakdowns
- Any situation where symptoms are visible but causes are unclear

## Quick Start

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

rca = RootCauseAnalyzer()

# Full context mode — richest output
ctx = rca.build_context(
    problem="Website performance degraded by 50% after the v2.3 deployment",
    context="Started Tuesday at 3pm, affects only authenticated users",
    depth="thorough",
)
result = ctx.execute(provider="openai")
print(result.response)
```

## Constructor

```python
rca = RootCauseAnalyzer()
```

No arguments required. The pattern initializes with built-in guidance, directive template, and constraints.

## Methods

### `build_context(problem, context=None, depth="thorough")`

Builds a `Context` object without executing. Use this when you want to:
- Export to a specific format (OpenAI, Anthropic, LangChain, etc.)
- Integrate into an existing workflow
- Inspect the assembled prompt before running

```python
ctx = rca.build_context(
    problem="Conversion rate dropped 35% this week",
    context="No code changes were deployed",
    depth="standard",
)

# Export to different formats
print(ctx.to_openai())        # OpenAI messages format
print(ctx.to_anthropic())     # Anthropic format  
print(ctx.to_yaml())          # YAML serialization
print(ctx.to_langchain())     # LangChain messages
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `problem` | `str` | `""` | The problem to investigate |
| `context` | `str \| None` | `None` | Additional context, timeline, observed conditions |
| `depth` | `str` | `"thorough"` | Analysis depth: `"quick"`, `"standard"`, or `"thorough"` |

### `execute(provider, problem, context=None, depth="thorough", **kwargs)`

Build and execute in one call.

```python
result = rca.execute(
    provider="openai",
    problem="Customer churn increased 40% in Q3",
    context="No pricing changes, competitors unchanged",
    depth="thorough",
    temperature=0.3,
)
print(result.response)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | `str` | `"openai"` | LLM provider: `"openai"`, `"anthropic"`, `"gemini"` |
| `problem` | `str` | `""` | The problem to investigate |
| `context` | `str \| None` | `None` | Additional context |
| `depth` | `str` | `"thorough"` | Analysis depth |
| `**kwargs` | | | Provider parameters (`model`, `temperature`, `max_tokens`) |

### `generic_prompt(problem, context_section="", depth="thorough")`

Returns a zero-cost prompt string. No context assembly, no extra LLM calls — pure string substitution.

```python
prompt = rca.generic_prompt(
    problem="API latency spiked to 8 seconds",
    depth="thorough",
)
print(prompt)
# → "You are a root cause analysis specialist... Problem: API latency spiked..."
```

## Analysis Framework

The `thorough` depth produces a 10-section investigation:

1. **Problem Definition** — Precise description separating symptoms from causes
2. **Symptom vs. Cause** — Explicit distinction between observable effects and underlying causes  
3. **Five Whys Analysis** — Iterative "Why?" questioning to drill beneath surface explanations
4. **Ishikawa (Fishbone)** — 6-category analysis: People, Process, Technology, Environment, Materials, Management
5. **Contributing Factors** — Primary root cause + secondary factors + interactions
6. **Cause Verification** — Hypothesis testing for each suspected cause
7. **Systemic Analysis** — Design flaws, feedback loops, hidden dependencies
8. **Root Cause Statement** — Clear, specific statement with causal mechanism
9. **Prevention Strategy** — Short-term fix + root cause fix + monitoring
10. **Lessons Learned** — Broader implications and similar problem areas

## Depth Levels

| Depth | Use case | Output scope |
|-------|----------|-------------|
| `quick` | Time-sensitive triage | Abbreviated investigation |
| `standard` | Routine incidents | Standard 10-section analysis |
| `thorough` | Critical incidents, post-mortems | Deep investigation with full framework |

## Examples

### Engineering Incident

```python
result = rca.execute(
    provider="openai",
    problem="Database queries taking 30+ seconds during peak hours",
    context="Happens every weekday between 9-11am. No index changes. DB size has doubled.",
    depth="thorough",
)
```

### Business Performance Drop

```python
result = rca.execute(
    provider="anthropic",
    problem="Sales pipeline dropped 60% last month",
    context="New CRM deployed 6 weeks ago. Three senior AEs left.",
    depth="standard",
)
```

### Process Failure

```python
result = rca.execute(
    provider="gemini",
    problem="Customer onboarding takes 3x longer than target",
    context="Problem started after team restructuring",
    depth="quick",
)
```

## Chaining with Other Patterns

Root cause analysis pairs well with `HypothesisGenerator` (validate hypotheses about causes) and `ScenarioPlanner` (plan for recurrence scenarios):

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer, HypothesisGenerator

rca_ctx = RootCauseAnalyzer().build_context(problem="Service downtime every Friday")
rca_result = rca_ctx.execute(provider="openai")

# Feed RCA findings into hypothesis testing
hyp_ctx = HypothesisGenerator().build_context(
    observation=rca_result.response[:1500],
    domain="infrastructure",
)
hyp_result = hyp_ctx.execute(provider="openai")
```

## Output Format

The response includes structured markdown with numbered sections, clear symptom/cause distinctions, and a prioritized prevention strategy. The `Root Cause Statement` section always provides a single, falsifiable root cause.

## Research Basis

- **Five Whys**: Taiichi Ohno, Toyota Production System
- **Ishikawa Diagrams**: Kaoru Ishikawa, quality management methodology  
- **Systems Thinking**: Peter Senge, *The Fifth Discipline*
- **Incident Investigation**: NTSB methodology, healthcare root cause analysis standards

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(problem, context, depth)` | `Context` | Assembled context object |
| `execute(provider, problem, context, depth, **kwargs)` | `ProviderResponse` | Execute and return response |
| `generic_prompt(problem, context_section, depth)` | `str` | Zero-cost prompt string |
| `to_dict()` | `dict` | Serialize pattern to dict |
| `save(path)` | `None` | Save pattern to YAML/JSON |
| `load(path)` | `RootCauseAnalyzer` | Load from file |
