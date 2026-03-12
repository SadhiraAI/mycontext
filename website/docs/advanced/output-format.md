---
sidebar_position: 2
title: Output Format Control
description: Control how every template presents its LLM response — 10 formats across all 87 patterns. Switch between slides, email, JSON, actionable items, and more without changing what gets analyzed.
---

# Output Format Control

Every template in mycontext-ai accepts an `output_format` parameter that controls *how* the LLM presents its analysis — without changing *what* it analyzes. The format instruction is appended to the assembled directive at build time.

This is implemented once at the `Pattern` base class level, so all 87 templates inherit it automatically.

## Quick Example

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

rca = RootCauseAnalyzer()

# Default: structured sections with headers
ctx = rca.build_context(problem="API latency tripled after deploy")

# Slide-ready output for your post-incident review
ctx = rca.build_context(
    problem="API latency tripled after deploy",
    output_format="slides",
)

# Action items only — paste into your sprint board
ctx = rca.build_context(
    problem="API latency tripled after deploy",
    output_format="actionable",
)

# Raw JSON for a dashboard or downstream LLM call
ctx = rca.build_context(
    problem="API latency tripled after deploy",
    output_format="json",
)
```

`output_format` also works on `execute()` directly:

```python
result = rca.execute(
    provider="openai",
    problem="API latency tripled after deploy",
    output_format="email",
)
```

## All 10 Formats

### Human Formats

These control how the output is presented to a person.

| Format | Description | Best for |
|--------|-------------|----------|
| `structured` | **Default.** Sections with headers and bullet points. No directive appended — behavior unchanged. | All general use |
| `narrative` | Flowing prose paragraphs only. No headers, no lists. 2–4 paragraphs. | Executive reports, presentations |
| `brief` | 3–5 bullet points, max 150 words total. One sentence per bullet. Only the most critical findings. | Slack/Teams messages, notifications |
| `actionable` | 5–10 items only. Each starts with an imperative verb (Fix, Add, Remove, Update). No explanations. | Ticket creation, ops handoff |
| `slides` | 3–5 slides. Each slide has a title + 3–4 bullets. No prose. | PowerPoint/Google Slides prep |
| `email` | Subject line + opening + body paragraphs + clear next step + sign-off. | Executive communication |
| `qa` | Q&A pairs. Each finding becomes a Q: / A: pair. | FAQs, knowledge bases, onboarding docs |
| `checklist` | `- [ ]` items grouped by category. Each item is one concise action. | Review checklists, runbooks |

### Machine Formats

These control serialization for downstream processing.

| Format | Description | Best for |
|--------|-------------|----------|
| `json` | Raw JSON object only. No markdown fences, no prose. | Pipelines, dashboards, downstream LLM calls |
| `table` | Markdown table(s) only. Clear column headers. No prose outside tables. | Risk registers, comparison matrices |

:::tip Machine formats auto-set temperature
When `output_format` is `"json"` or `"table"`, the `execute()` method automatically sets `temperature=0.0` to maximize structural consistency — unless you explicitly override it with `temperature=...`.
:::

## Works on All 87 Templates

`output_format` is on the `Pattern` base class. Every template — free and enterprise — supports it:

```python
from mycontext.templates.free.specialized import CodeReviewer
from mycontext.templates.free.analysis import DataAnalyzer
from mycontext.templates.free.planning import ScenarioPlanner

# Code review as a checklist — perfect for PR descriptions
CodeReviewer().execute(
    provider="openai",
    code=pr_diff,
    language="TypeScript",
    output_format="checklist",
)

# Data analysis as JSON for a dashboard
DataAnalyzer().execute(
    provider="openai",
    data_description="Monthly revenue by region, 12 months",
    goal="Find regional growth drivers",
    output_format="json",
)

# Scenario planning as slides for a strategy session
ScenarioPlanner().execute(
    provider="openai",
    topic="AI regulation impact on our product roadmap",
    timeframe="18 months",
    output_format="slides",
)
```

## Combining with `output_format` from `utils.structured_output`

`output_format` on `build_context()` controls the *presentation* of the full analysis. The `output_format()` utility in `mycontext.utils.structured_output` adds a *schema* instruction to constrain the response to specific fields.

Use them together when you need both:

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.utils.structured_output import output_format as schema_format

# 1. Build the template context with JSON format
ctx = RootCauseAnalyzer().build_context(
    problem="API latency tripled after deploy",
    output_format="json",
)

# 2. Optionally add a schema constraint to the directive
ctx.directive.content += schema_format(
    "json",
    schema={"root_causes": "list", "recommendations": "list", "severity": "str"}
)

result = ctx.execute(provider="openai")
```

## Programmatic Format Detection

Use `mycontext.utils.format_directives` to check format types in your own code:

```python
from mycontext.utils.format_directives import (
    is_machine_format,
    VALID_OUTPUT_FORMATS,
    HUMAN_OUTPUT_FORMATS,
    MACHINE_OUTPUT_FORMATS,
)

print(VALID_OUTPUT_FORMATS)
# frozenset({'structured', 'narrative', 'brief', 'actionable', 'slides',
#            'email', 'qa', 'checklist', 'json', 'table'})

is_machine_format("json")   # True
is_machine_format("slides") # False
```

## Validation

Passing an unrecognised format raises `ValueError` immediately at `build_context()` time — before any LLM call is made:

```python
rca.build_context(problem="...", output_format="invalid")
# ValueError: Invalid output_format 'invalid'.
# Choose from: ['actionable', 'brief', 'checklist', 'email', 'json',
#               'narrative', 'qa', 'slides', 'structured', 'table']
```
