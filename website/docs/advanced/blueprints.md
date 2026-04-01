---
sidebar_position: 1
title: Blueprints
description: Multi-component context architecture. Blueprints define reusable, parameterized context structures with token budget management and optimization strategies.
---

# Blueprints

A `Blueprint` is a reusable context template with a fixed structure, token budget, and optimization strategy. Where a `Context` is a single assembled context, a Blueprint is an architecture — instantiate it repeatedly with different inputs.

```python
from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints

blueprint = Blueprint(
    name="code_review_assistant",
    guidance=Guidance(
        role="Senior software engineer specializing in security and performance",
        rules=[
            "Rank findings by severity: Critical → High → Medium → Low",
            "Provide OWASP references for security issues",
            "Include concrete remediation code for each finding",
        ],
    ),
    directive_template="Review the following {language} code:\n\n```{language}\n{code}\n```",
    constraints=Constraints(
        must_include=["severity", "remediation", "code example"],
        format_rules=["Group by severity", "One finding per bullet"],
    ),
    token_budget=4000,
    optimization="quality",
)

# Reuse with different inputs
ctx1 = blueprint.build(language="Python", code=python_code)
ctx2 = blueprint.build(language="TypeScript", code=ts_code)
ctx3 = blueprint.build(language="Go", code=go_code)
```

## When to Use Blueprints

**Use a Blueprint when:**
- The same context structure is used repeatedly with different content
- You need token budget management across many contexts
- You want to codify a context architecture as a shareable, reusable unit
- You need multiple optimization profiles for the same structure

**Use a `Context` directly when:**
- You're building a one-off context
- You're using a cognitive pattern (patterns build Contexts internally)

## Constructor

```python
Blueprint(
    name: str,
    description: str | None = None,
    guidance: Guidance | None = None,
    directive_template: str | None = None,
    constraints: Constraints | None = None,
    components: list = [],
    token_budget: int = 4000,
    optimization: str = "balanced",
    priority_order: list[str] = ["guidance", "directive", "constraints", "knowledge", "memory"],
    metadata: dict = {},
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | required | Blueprint identifier |
| `description` | `str \| None` | `None` | What this blueprint produces |
| `guidance` | `Guidance \| None` | `None` | Fixed guidance for all builds |
| `directive_template` | `str \| None` | `None` | Template string with `{variable}` placeholders |
| `constraints` | `Constraints \| None` | `None` | Fixed constraints for all builds |
| `components` | `list` | `[]` | Additional components (e.g. document indexes) |
| `token_budget` | `int` | `4000` | Maximum token budget |
| `optimization` | `str` | `"balanced"` | Strategy: `"speed"`, `"quality"`, `"cost"`, `"balanced"` |
| `priority_order` | `list[str]` | `[...]` | Component priority for token trimming |

## `blueprint.build(**inputs)`

Instantiates the blueprint with specific inputs:

```python
ctx = blueprint.build(
    language="Python",
    code=my_code,
)
# Returns a fully assembled Context
result = ctx.execute(provider="openai")
```

The `directive_template` is formatted with `**inputs` using Python's `.format()`:

```python
# Template: "Review the following {language} code:\n\n{code}"
# Inputs: language="Python", code=my_code
# Result: "Review the following Python code:\n\n<my_code>"
```

All inputs are also stored in `ctx.data` for downstream use.

## Optimization Strategies

The `optimize()` method creates a copy with a different strategy applied:

```python
# Quality: +30% token budget, knowledge + guidance prioritized
quality_bp = blueprint.optimize("quality")

# Speed: -30% token budget, directive prioritized
fast_bp = blueprint.optimize("speed")

# Cost: -50% token budget, essentials only
cheap_bp = blueprint.optimize("cost")

# Balanced (default): no changes
balanced_bp = blueprint.optimize("balanced")
```

| Strategy | Token budget | Priority order | Use case |
|----------|-------------|----------------|---------|
| `"quality"` | +30% | guidance → knowledge → directive | Production, high-stakes |
| `"speed"` | -30% | directive → guidance → constraints | Real-time, interactive |
| `"cost"` | -50% | directive → constraints → guidance | Batch processing, high volume |
| `"balanced"` | unchanged | default order | General purpose |

```python
# Use the right profile for the job
if is_production_review:
    ctx = quality_blueprint.build(code=code, language=lang)
elif is_batch_job:
    ctx = cost_blueprint.build(code=code, language=lang)
else:
    ctx = blueprint.build(code=code, language=lang)
```

## `blueprint.estimate_tokens()`

Rough token count estimate before building:

```python
tokens = blueprint.estimate_tokens()
print(f"Estimated tokens: ~{tokens}")
# → Estimated tokens: ~320

if tokens > blueprint.token_budget:
    print("Warning: exceeds token budget")
```

## Serialization

Blueprints are Pydantic models — they serialize cleanly:

```python
# To dict / JSON
d = blueprint.to_dict()
bp2 = Blueprint.from_dict(d)

# Pydantic model_dump()
raw = blueprint.model_dump()
```

## Examples

### Research Assistant Blueprint

```python
from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints

research_bp = Blueprint(
    name="research_assistant",
    description="Deep research synthesis for technical topics",
    guidance=Guidance(
        role="Senior research analyst with expertise in synthesizing technical information",
        rules=[
            "Cite specific evidence for each claim",
            "Distinguish between established facts and emerging research",
            "Identify research gaps and open questions",
            "Quantify uncertainty where relevant",
        ],
    ),
    directive_template=(
        "Research and synthesize information on: {topic}\n\n"
        "Focus area: {focus}\n"
        "Audience: {audience}\n"
        "Depth: {depth}"
    ),
    constraints=Constraints(
        must_include=["key findings", "evidence", "limitations", "recommendations"],
        format_rules=["Use numbered sections", "Executive summary first"],
    ),
    token_budget=6000,
    optimization="quality",
)

# Use for different research tasks
ctx = research_bp.build(
    topic="Transformer attention mechanisms",
    focus="efficiency improvements in 2024-2025",
    audience="ML engineers",
    depth="comprehensive",
)
result = ctx.execute(provider="openai", model="gpt-4o")
```

### Customer Support Blueprint

```python
support_bp = Blueprint(
    name="support_agent",
    guidance=Guidance(
        role="Customer support specialist for SaaS products",
        rules=[
            "Acknowledge the issue before providing solutions",
            "Provide step-by-step instructions when applicable",
            "Offer escalation path if issue is complex",
        ],
    ),
    directive_template=(
        "Help the customer with: {issue}\n\n"
        "Customer tier: {tier}\n"
        "Product version: {version}"
    ),
    token_budget=2000,
    optimization="speed",  # Fast responses for support
)

# Quick build, cheap responses
ctx = support_bp.build(
    issue="Cannot connect to database after upgrade",
    tier="enterprise",
    version="3.2.1",
)
```

### Multiple Profiles from One Blueprint

```python
base_bp = Blueprint(
    name="analysis_engine",
    guidance=Guidance(role="Senior analyst"),
    directive_template="Analyze: {input}",
    token_budget=4000,
)

# Derive variants
draft_bp = base_bp.optimize("speed")     # Quick drafts
final_bp = base_bp.optimize("quality")   # Final deliverables
batch_bp = base_bp.optimize("cost")      # Bulk processing

# Use the right one
if is_draft:
    ctx = draft_bp.build(input=my_input)
else:
    ctx = final_bp.build(input=my_input)
```

## Using Fragments with Blueprints

Fragments are composable quality atoms designed to work with Blueprint-based architectures. Apply them after `build()` to enhance any Context:

```python
from mycontext.structure import Blueprint
from mycontext.foundation import Guidance
from mycontext.fragments import anti_fluff, objectivity, self_check_analysis

blueprint = Blueprint(
    name="analysis_engine",
    guidance=Guidance(role="Senior analyst"),
    directive_template="Analyze: {input}",
    token_budget=4000,
)

ctx = blueprint.build(input="Why did revenue drop 40% in Q3?")

# Layer on quality fragments
anti_fluff.apply(ctx)          # Concise output, no filler
objectivity.apply(ctx)         # Objectivity rules in guidance
self_check_analysis.apply(ctx) # Analysis verification questions

result = ctx.execute(provider="openai")
```

See the [Fragments API reference](../api/overview#fragments--mycontextfragments) for the full list of built-in fragments.

## API Reference

### `Blueprint`

| Method | Returns | Description |
|--------|---------|-------------|
| `build(**inputs)` | `Context` | Instantiate with specific inputs |
| `optimize(strategy)` | `Blueprint` | Create optimized copy |
| `estimate_tokens()` | `int` | Rough token estimate |
| `to_dict()` | `dict` | Serialize to dict |
| `from_dict(data)` | `Blueprint` | Deserialize from dict |
