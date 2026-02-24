---
sidebar_position: 5
title: Patterns & Blueprints
description: Complete reference for the Pattern base class and Blueprint — reusable context templates, directive variable substitution, generic prompts, and multi-component context architecture.
---

# Patterns & Blueprints

Patterns and Blueprints are the composition layer. **Patterns** are reusable context templates backed by cognitive frameworks. **Blueprints** are multi-component architectures for production applications.

## Pattern

A `Pattern` is a reusable, parameterized context template. All 85 cognitive templates (RootCauseAnalyzer, CodeReviewer, etc.) extend `Pattern`. You can also build custom patterns.

### Import

```python
from mycontext import Pattern
# or
from mycontext.structure import Pattern
```

### Using a Cognitive Pattern

The most common usage — pick one of the 85 built-in patterns:

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

rca = RootCauseAnalyzer()
ctx = rca.build_context(
    problem="API response times tripled after last deployment",
    depth="comprehensive",
)
result = ctx.execute(provider="openai")
```

Each pattern's `build_context()` has typed, documented inputs specific to its methodology. See [Cognitive Patterns](../cognitive-patterns/overview) for all 85 patterns.

### Building a Custom Pattern

```python
from mycontext import Pattern
from mycontext.foundation import Guidance, Constraints

competitor_analyst = Pattern(
    name="competitor_analyst",
    description="Structured competitive analysis for a product or company",
    guidance=Guidance(
        role="Senior competitive intelligence analyst",
        rules=[
            "Base every claim on the provided data — flag gaps explicitly",
            "Quantify advantages and disadvantages where possible",
            "Always include actionable recommendations",
        ],
        style="direct, evidence-based",
        expertise=["competitive analysis", "market research", "product strategy"],
    ),
    directive_template=(
        "Analyze {competitor} as a competitor to {our_product}.\n\n"
        "Context: {context}\n\n"
        "Focus on: {focus_areas}"
    ),
    constraints=Constraints(
        must_include=["strengths", "weaknesses", "strategic threats", "recommendations"],
        format_rules=["Use a SWOT-style structure", "Bullet points throughout"],
    ),
    input_schema={
        "competitor": str,
        "our_product": str,
        "context": str,
        "focus_areas": str,
    },
    tags=["strategy", "competitive-intelligence"],
    version="1.0.0",
)

ctx = competitor_analyst.build_context(
    competitor="Competitor X",
    our_product="Our SaaS Platform",
    context="We are losing deals to Competitor X in the mid-market segment.",
    focus_areas="pricing model, enterprise integrations, customer support quality",
)

result = ctx.execute(provider="openai")
```

### Pattern Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `str` | **Yes** | Unique identifier |
| `description` | `str \| None` | No | What this pattern does |
| `guidance` | `Guidance \| None` | No | Default system guidance |
| `directive_template` | `str \| None` | No | Template string with `{variable}` placeholders |
| `constraints` | `Constraints \| None` | No | Output guardrails |
| `input_schema` | `dict[str, type]` | No | Required inputs and their types |
| `output_schema` | `dict[str, type]` | No | Expected output structure |
| `tags` | `list[str]` | No | Categorization labels |
| `version` | `str` | No | Semantic version, default `"1.0.0"` |
| `metadata` | `dict` | No | Arbitrary metadata |

### `build_context(**inputs)` → `Context`

Builds a fully assembled `Context` from the pattern and provided inputs.

```python
ctx = pattern.build_context(
    problem="Server crashes under load",
    depth="comprehensive",
)
# Returns a Context with guidance, directive (built from template), constraints, and data
```

The built `Context` automatically carries pattern metadata:

```python
ctx.metadata["pattern"]         # "root_cause_analyzer"
ctx.metadata["pattern_version"] # "1.0.0"
```

### `execute(provider, mode, **inputs)` → response

Build and execute in a single call. Accepts all `build_context` inputs plus any provider kwargs (`model`, `temperature`, etc.):

```python
result = pattern.execute(
    provider="openai",
    mode="full",          # "full" (default) or "generic"
    problem="Server crashes under load",
    depth="comprehensive",
    model="gpt-4o",
    temperature=0.2,
)
```

`mode="generic"` uses the pattern's `GENERIC_PROMPT` — a zero-cost pre-authored prompt that skips context assembly.

### Generic Prompts — Zero-Cost Execution

Every built-in pattern carries a `GENERIC_PROMPT` — a hand-crafted ~600–1200 char prompt that distills the pattern's cognitive methodology into a self-contained instruction.

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

rca = RootCauseAnalyzer()

# Zero-cost: no LLM call, no context assembly
prompt = rca.generic_prompt(problem="Server crashes during peak hours")
print(len(prompt))  # ~950 chars
print(prompt)       # "You are performing a systematic root cause analysis..."
```

Two execution modes compared:

| Mode | Method | LLM Calls | Output |
|------|--------|-----------|--------|
| **Generic** | `pattern.generic_prompt(**inputs)` | 0 (compilation) | Pre-authored prompt string |
| **Generic execute** | `pattern.execute(mode="generic", ...)` | 1 (just the LLM call) | Response from generic prompt |
| **Full** | `pattern.build_context(**inputs)` → `.execute()` | 1 | Response from rich structured context |

### Saving and Loading Patterns

```python
from pathlib import Path

# Save to YAML
pattern.save(Path("patterns/competitor_analyst.yaml"))

# Load from YAML
loaded = Pattern.load("competitor_analyst", library_path=Path("patterns/"))
```

---

## Blueprint

`Blueprint` is for production applications that need **more than one template** — orchestrating multiple components (guidance, dynamic knowledge, reasoning steps) with token budget management.

### Import

```python
from mycontext import Blueprint
# or
from mycontext.structure import Blueprint
```

### Basic Usage

```python
from mycontext import Blueprint
from mycontext.foundation import Guidance, Constraints

blueprint = Blueprint(
    name="research_assistant",
    description="Deep research assistant with topic-specific knowledge injection",
    guidance=Guidance(
        role="Expert research analyst",
        rules=[
            "Cite sources whenever possible",
            "Distinguish between confirmed facts and reasoned inferences",
            "Structure findings from most to least important",
        ],
        style="precise, analytical",
    ),
    directive_template="Research and explain the following: {topic}\n\nScope: {scope}",
    constraints=Constraints(
        must_include=["key findings", "knowledge gaps", "further reading"],
        format_rules=["Use H2 headers for major sections", "Include a TL;DR at the top"],
    ),
    token_budget=4000,
    optimization="balanced",
)

ctx = blueprint.build(
    topic="Quantum computing advances in error correction",
    scope="Focus on developments from 2023–2025 relevant to near-term practical applications",
)

result = ctx.execute(provider="openai")
```

### Blueprint Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | required | Blueprint identifier |
| `description` | `str \| None` | `None` | What this blueprint creates |
| `guidance` | `Guidance \| None` | `None` | Primary system guidance |
| `directive_template` | `str \| None` | `None` | Template with `{variable}` placeholders |
| `constraints` | `Constraints \| None` | `None` | Output guardrails |
| `components` | `list` | `[]` | Additional components (documents, sessions, etc.) |
| `token_budget` | `int` | `4000` | Max token target (100–1,000,000) |
| `optimization` | `str` | `"balanced"` | Strategy: `"speed"`, `"quality"`, `"cost"`, or `"balanced"` |
| `priority_order` | `list[str]` | see below | Assembly priority order |

**Default priority order:** `guidance → directive → constraints → knowledge → memory`

### Optimization Strategies

The `optimize()` method produces a modified copy of the blueprint tuned for a strategy:

```python
# Quality: +30% token budget, prioritizes guidance + knowledge
quality_bp = blueprint.optimize("quality")

# Speed: -30% token budget, directive-first
speed_bp = blueprint.optimize("speed")

# Cost: -50% token budget, essentials only
cost_bp = blueprint.optimize("cost")

# Balanced (default): unchanged
balanced_bp = blueprint.optimize("balanced")
```

| Strategy | Token Budget | Priority Order |
|----------|-------------|----------------|
| `"quality"` | `budget × 1.3` | guidance → knowledge → directive → constraints |
| `"speed"` | `budget × 0.7` | directive → guidance → constraints → knowledge |
| `"cost"` | `budget × 0.5` | directive → constraints → guidance |
| `"balanced"` | unchanged | default order |

### Token Estimation

```python
estimated = blueprint.estimate_tokens()
print(f"Estimated tokens: {estimated}")
# Compare against your budget
print(f"Budget: {blueprint.token_budget}")
```

### Components

Components are objects with a `.render()` or `.to_string()` method — their output is assembled into the `knowledge` field of the built context:

```python
class DocumentChunk:
    def __init__(self, text):
        self.text = text
    def render(self):
        return self.text

blueprint = Blueprint(
    name="doc_qa",
    guidance=Guidance(role="Technical documentation expert"),
    directive_template="Answer the question: {question}",
    components=[
        DocumentChunk("API Reference: POST /v1/contexts — creates a new context..."),
        DocumentChunk("Rate limits: 1000 requests/minute on the Pro plan..."),
    ],
    token_budget=3000,
)

ctx = blueprint.build(question="What are the rate limits for the API?")
# ctx.knowledge → combined text from both DocumentChunks
```

### When to Use Blueprint vs. Pattern

| Use | Tool |
|-----|------|
| Single-step reasoning with a specific methodology | `Pattern` / cognitive template |
| Multi-component production context with token budget | `Blueprint` |
| Parameterized template with fixed structure | `Pattern` with `directive_template` |
| Dynamic knowledge injection + guidance + constraints | `Blueprint` with components |
| Multi-step chains of reasoning | Chain patterns or `build_workflow_chain()` |

---

**Next:** [Cognitive Patterns →](../cognitive-patterns/overview)
