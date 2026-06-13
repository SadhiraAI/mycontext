---
sidebar_position: 7
title: Template Integrator Agent
description: Fuse multiple cognitive templates into a single unified context that combines the strongest methodology from each. No concatenation. True integration.
---

# Template Integrator Agent

`TemplateIntegratorAgent` fuses multiple cognitive templates into **one integrated context**. Unlike running templates in sequence, the integrator asks an LLM to extract the best methodology from each template and weave them into a single, cohesive reasoning framework tailored to your specific question.

```python
from mycontext.intelligence import TemplateIntegratorAgent

agent = TemplateIntegratorAgent()

# Manual template selection
result = agent.integrate(
    question="Should we migrate to microservices?",
    template_names=["decision_framework", "risk_assessor", "stakeholder_mapper"],
    provider="openai",
)

ctx = result.to_context()
response = ctx.execute(provider="openai")
print(response.response)
```

## Why Integrate Instead of Chain?

**Chaining** runs templates sequentially — each one sees the previous output. Good for analysis pipelines where stage 1 feeds stage 2.

**Integration** fuses the methodologies into one prompt — a single LLM call gets the combined reasoning power of all templates applied simultaneously.

| Approach | When to use | LLM calls |
|----------|------------|-----------|
| Chain | Pipeline analysis (root cause → hypothesis → scenario) | N+1 |
| Integration | Comprehensive single-question analysis | 2 (integrate + execute) |

## Two Usage Patterns

### 1. Manual Template Selection: `integrate()`

You choose which templates to combine:

```python
result = agent.integrate(
    question="Should we rebuild our authentication system from scratch?",
    template_names=["risk_assessor", "decision_framework"],
    provider="openai",
    temperature=0.2,
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `question` | `str` | required | User's question |
| `template_names` | `list[str]` | required | Templates to integrate |
| `provider` | `str` | `"openai"` | LLM provider |
| `selection_reasoning` | `dict \| None` | `None` | Per-template reason (used as context for integration) |
| `temperature` | `float` | `0.2` | Temperature for integration |
| `model` | `str \| None` | `None` | Override model |

### 2. All-in-One: `suggest_and_integrate()`

Auto-suggest templates and integrate them in one call:

```python
result = agent.suggest_and_integrate(
    question="Why did our churn spike 40% in Q3?",
    provider="openai",
    max_patterns=3,
    mode="hybrid",       # keyword | llm | hybrid
    integration_mode="focused",  # "focused" (2-3 templates) | "full" (up to max)
)
ctx = result.to_context()
response = ctx.execute(provider="openai")
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `question` | `str` | required | User's question |
| `provider` | `str` | `"openai"` | LLM provider |
| `max_patterns` | `int` | `3` | Maximum templates to integrate |
| `mode` | `str` | `"hybrid"` | Template suggestion mode |
| `integration_mode` | `str` | `"focused"` | `"focused"` (2–3 templates) or `"full"` |

### 3. Suggest and Compile: `suggest_and_compile()`

Like `suggest_and_integrate()` but returns a `ComposedPrompt` instead of `IntegrationResult` — uses `PromptComposer` for the merging step:

```python
composed = agent.suggest_and_compile(
    question="How do we reduce our cloud infrastructure costs by 40%?",
    provider="openai",
    max_patterns=3,
    refine=True,
)
response = composed.execute(provider="openai")
```

## IntegrationResult

All integration methods return an `IntegrationResult`:

```python
@dataclass
class IntegrationResult:
    question: str
    source_templates: list[str]      # Templates that were integrated
    integrated_context: str          # Human-readable fused prompt text (v0.10+: never a sentinel)
    role: str                        # Combined expert role
    rules: list[str]                 # Merged analytical rules (max 6)
    directive: str                   # Step-by-step integrated instructions
    output_requirements: list[str]   # Required output sections (5-7 max)
    raw_llm_response: str            # Same readable text as integrated_context when structured
    integration_rationale: str       # Why the merge works (v0.10+)

    def to_context(self) -> Context  # Convert to executable Context
```

### Inspecting Integration Output

```python
result = agent.integrate(
    question="Should we launch in Germany given GDPR, competition, and budget constraints?",
    template_names=["risk_assessor", "stakeholder_mapper", "decision_framework"],
    provider="openai",
)

print("Role:", result.role)
# → "Strategic Risk Analyst and Decision Architect"

print("Rules:")
for rule in result.rules:
    print(f"  - {rule}")
# → - Apply both regulatory risk assessment and stakeholder mapping simultaneously
# → - Weight decision criteria against budget constraints and market opportunity
# → ...

print("Output requirements:")
for req in result.output_requirements:
    print(f"  - {req}")
# → - Regulatory risk matrix (GDPR, data sovereignty)
# → - Key stakeholder analysis with influence mapping
# → - Weighted decision criteria
# → - Go/no-go recommendation with confidence level
# → - 90-day action plan if proceeding
```

### Executing the Integration

```python
ctx = result.to_context()

# The context contains:
# - Guidance with the integrated role + rules
# - Directive with the combined analytical instructions
# - Constraints with the output requirements

response = ctx.execute(provider="openai", model="gpt-4o")
print(response.response)
```

## What the Integration Agent Does

The integration process follows this structure:

1. **Gather template capabilities** — uses each template’s **`GENERIC_PROMPT`** (concise methodology fingerprint) plus catalog descriptions and “when to use” notes (**v0.10+**; replaces brittle directive line heuristics). Default integration model is **`gpt-4o`**. Optional **`max_tokens`** / **`top_p`** pass through to the structured LLM call.
2. **Build a fusion prompt** — tells the LLM: "merge the best of these templates for this specific question"
3. **Parse the integrated output** — extracts ROLE, RULES, DIRECTIVE, and OUTPUT MUST INCLUDE sections
4. **Returns structured result** — directly usable as a `Context`

### Integration Constraints

The agent instructs the composition LLM to:
- Draw the **best techniques** from each template (not all sections)
- Keep the framework completable in a **single LLM response** (5–7 output sections max)
- Every output section must **directly address** the user's question
- **Prioritize answering the question** over methodological completeness
- Target 3,500–4,500 character output (depth over breadth)

## Constructor

```python
TemplateIntegratorAgent(
    include_enterprise: bool = True
)
```

The `include_enterprise` flag is deprecated and ignored — all 88 patterns can always be integrated. It is kept only for backwards compatibility.

## Examples

### Product Strategy Decision

```python
agent = TemplateIntegratorAgent()

result = agent.integrate(
    question="Should we pivot from B2C to B2B? We have 50k users, $500k MRR, 18mo runway.",
    template_names=["decision_framework", "stakeholder_mapper", "scenario_planner"],
    provider="openai",
    model="gpt-4o",
)

ctx = result.to_context()
response = ctx.execute(provider="openai")
```

### Incident Post-Mortem

```python
result = agent.suggest_and_integrate(
    question="We had a major outage last week. Conduct a thorough post-mortem and prevention plan.",
    provider="openai",
    max_patterns=3,
    mode="keyword",
)
ctx = result.to_context()
response = ctx.execute(provider="openai")
```

### Research Synthesis

```python
result = agent.integrate(
    question="Synthesize findings from our user research: 15 interviews, NPS data, and support tickets.",
    template_names=["synthesis_builder", "data_analyzer", "audience_adapter"],
    provider="openai",
    selection_reasoning={
        "synthesis_builder": "Core synthesis framework for integrating multiple data sources",
        "data_analyzer": "Extracts patterns from quantitative NPS data",
        "audience_adapter": "Frames findings for executive vs. engineering audiences",
    },
)
```

## Comparison: integrate() vs chain vs compose

| Method | What it produces | Best for |
|--------|-----------------|----------|
| `integrate()` | Single fused Context | Comprehensive single-question analysis |
| `build_workflow_chain()` | Sequential chain with params | Multi-stage analytical pipelines |
| `compose_from_templates()` | Merged prompt string | Cost-efficient multi-template analysis |

## API Reference

### `TemplateIntegratorAgent`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(include_enterprise)` | — | Initialize |
| `integrate(question, template_names, ...)` | `IntegrationResult` | Integrate selected templates |
| `suggest_and_integrate(question, ...)` | `IntegrationResult` | Auto-suggest + integrate |
| `suggest_and_compile(question, ...)` | `ComposedPrompt` | Auto-suggest + compose |

### `IntegrationResult`

| Attribute | Type | Description |
|-----------|------|-------------|
| `question` | `str` | Original question |
| `source_templates` | `list[str]` | Templates integrated |
| `integrated_context` | `str` | Full integration output |
| `role` | `str` | Combined expert role |
| `rules` | `list[str]` | Merged behavioral rules |
| `directive` | `str` | Integrated instructions |
| `output_requirements` | `list[str]` | Required output sections |
| `to_context()` | `Context` | Convert to executable Context |
