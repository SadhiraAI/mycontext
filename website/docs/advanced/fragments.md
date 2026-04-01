---
sidebar_position: 2
title: Fragments
description: Reusable quality-enhancing building blocks for Blueprint composition and Context enrichment.
---

# Fragments

Fragments are composable, reusable quality-enhancing building blocks. Each fragment encapsulates a specific quality behavior — anti-fluff, objectivity, self-verification — and can be applied to any `Context` in a single call.

Fragments are the atoms that `Blueprint` orchestrates. They are designed to be layered: apply as many as you need, in any order.

## Import

```python
from mycontext.fragments import anti_fluff, objectivity, answer_first_fragment
```

## Quick Start

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.fragments import anti_fluff, objectivity, self_check_analysis

# Build a context from a template
ctx = RootCauseAnalyzer().build_context(
    problem="API response times tripled after deployment"
)

# Layer on quality fragments
anti_fluff.apply(ctx)           # Concise, no filler
objectivity.apply(ctx)          # Objectivity rules in guidance
self_check_analysis.apply(ctx)  # Verification questions for analysis tasks

result = ctx.execute(provider="openai")
```

## How Fragments Work

Each fragment carries:
- **Constraints kwargs** — fields like `verbosity`, `answer_first`, `forbidden_phrases` that are set on `Context.constraints`
- **Guidance rules** — behavioral rules appended to `Context.guidance.rules`

When you call `fragment.apply(ctx)`:
1. Constraints fields are set **only if not already present** — existing values are never overwritten
2. Guidance rules are **appended** with deduplication — no duplicates

This means fragments are safe to layer: applying `anti_fluff` and then `executive_brevity` will not conflict, and user-set values always take priority.

## Built-In Fragments

| Fragment | What it does |
|----------|-------------|
| `anti_fluff` | Sets `verbosity="minimal"`, bans common AI filler phrases |
| `answer_first_fragment` | Sets `answer_first=True` — conclusion before reasoning |
| `objectivity` | Adds objectivity-enforcing rules to guidance |
| `self_check_analysis` | Adds analysis-focused verification questions (correlation vs causation, data gaps, confidence) |
| `self_check_creative` | Adds creative-focused verification questions (unconventional ideas, feasibility) |
| `self_check_risk` | Adds risk-focused verification questions (blind spots, worst case, mitigation) |
| `structured_json` | Sets `output_contract` for valid JSON output |
| `grounding_strict` | Adds strict evidence-grounding rules to guidance |
| `educational_posture` | Sets `communication_posture="educational"` |
| `collaborative_posture` | Sets `communication_posture="collaborative"` |
| `hedging_ban` | Bans hedging phrases ("it depends", "arguably", "it could be") |
| `executive_brevity` | Sets `verbosity="minimal"`, `answer_first=True`, `communication_posture="direct"` |

## Using with Blueprint

Fragments are designed to work naturally with Blueprint-based architectures:

```python
from mycontext.structure import Blueprint
from mycontext.foundation import Guidance
from mycontext.fragments import executive_brevity, grounding_strict

blueprint = Blueprint(
    name="executive_report",
    guidance=Guidance(
        role="Senior business analyst",
        rules=["Base every claim on provided data"],
    ),
    directive_template="Analyze: {topic}\n\nData: {data}",
    token_budget=3000,
    optimization="speed",
)

ctx = blueprint.build(topic="Q3 revenue decline", data=revenue_csv)

# Apply fragments for executive output
executive_brevity.apply(ctx)    # Minimal, answer-first, direct
grounding_strict.apply(ctx)     # Evidence-grounded claims

result = ctx.execute(provider="openai")
```

## Creating Custom Fragments

```python
from mycontext.fragments import Fragment

my_fragment = Fragment(
    name="medical_safety",
    description="Safety guardrails for medical-adjacent tasks",
    _constraints_kwargs={
        "forbidden_phrases": [
            "you should take",
            "I recommend this medication",
            "this will cure",
        ],
        "communication_posture": "educational",
    },
    _guidance_rules=[
        "Never provide specific medical diagnoses or treatment recommendations",
        "Always recommend consulting a licensed healthcare professional",
    ],
)

# Use like any built-in fragment
ctx = some_template.build_context(...)
my_fragment.apply(ctx)
```

## Fragment API

### `Fragment`

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Fragment identifier |
| `description` | `str` | What this fragment does |

| Method | Returns | Description |
|--------|---------|-------------|
| `apply(ctx)` | `None` | Merge fragment settings into Context in-place |
| `constraints()` | `Constraints \| None` | Get the fragment's Constraints object |
| `guidance_rules()` | `list[str]` | Get the fragment's guidance rules list |
