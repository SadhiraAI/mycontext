---
sidebar_position: 4
title: suggest_routes()
description: Multi-route template planning for complex questions. Each route is an ordered agent pipeline — ideal for LangGraph, CrewAI, or custom orchestrators.
---

# suggest_routes()

`suggest_routes()` analyzes a question with an LLM and returns **several differentiated analysis paths** (routes). Each route is an ordered list of **steps** that map cleanly to agents in a multi-agent system: template name, role, what each step receives, and what it produces.

Use it when you want users (or your app) to **choose an analytical angle** — diagnostic vs risk vs trend vs strategic — instead of a single best pipeline.

```python
from mycontext.intelligence import suggest_routes

result = suggest_routes(
    "What are the main drivers of churn in Q3 for our B2B SaaS?",
    max_routes=4,
    provider="openai",
    model="gpt-4o",
)

print(result.question_decomposition)
print(result.recommendation)

for route in result.routes:
    print(f"\n{route.label} ({route.dimension})")
    print(f"  Final output: {route.final_output}")
    for step in route.steps:
        print(f"    [{step.template}] {step.agent_role}")
        print(f"      ← {step.receives}")
        print(f"      → {step.produces}")
```

## Function signature

```python
def suggest_routes(
    question: str,
    max_routes: int = 4,
    include_enterprise: bool = True,
    provider: str = "openai",
    temperature: float = 0,
    model: str | None = None,
    **kwargs,
) -> RouteAnalysis
```

| Parameter | Description |
|-----------|-------------|
| `question` | User question or task |
| `max_routes` | How many alternative routes to generate (clamped 2–6) |
| `include_enterprise` | Deprecated and ignored — all 88 patterns are always available |
| `provider` / `model` / `temperature` | Passed to the LLM (same pattern as other intelligence APIs) |
| `**kwargs` | e.g. `max_tokens`, `top_p` when using the instructor path |

## Return type: `RouteAnalysis`

| Field | Type | Description |
|-------|------|-------------|
| `question_decomposition` | `str` | Dimensions, stakeholders, scope |
| `routes` | `list[AnalysisRoute]` | Ordered by relevance |
| `recommendation` | `str` | Which route to start with and why |

### `AnalysisRoute`

| Field | Description |
|-------|-------------|
| `label` | Human-readable name (e.g. “Diagnostic deep-dive”) |
| `dimension` | e.g. diagnostic, predictive, strategic, risk |
| `rationale` | Why this angle matters for **this** question |
| `steps` | Ordered `RouteStep` list |
| `final_output` | Deliverable description for the full pipeline |

### `RouteStep` (one agent)

| Field | Description |
|-------|-------------|
| `template` | Catalog template name (`snake_case`) |
| `agent_role` | Plain-language role |
| `receives` | `user_input` or reference to prior step output |
| `produces` | What this step outputs |
| `params` | Suggested `build_context` kwargs (may be empty) |

## Relationship to other APIs

| API | Role |
|-----|------|
| **`suggest_routes()`** | Multiple routes, agent-level detail — **planning** for orchestration |
| **`suggest_patterns()`** | Single ranked list; `llm` / `hybrid` modes may use `suggest_routes` internally |
| **`build_workflow_chain()`** | **Deprecated** — use `suggest_routes()` for new code |
| **`TemplateIntegratorAgent`** | Fuse **selected** templates into **one** context for a single LLM call |

## Requirements

- Requires API keys / provider setup like other LLM-backed intelligence functions.
- Uses structured output (instructor when available, otherwise JSON parse + validation).

## See also

- [Pattern suggestion](./pattern-suggestion) — `suggest_patterns()` for a single pipeline
- [Chain orchestration](./chain-orchestration) — legacy `build_workflow_chain()` (deprecated)
- [Template integrator](./template-integrator) — fusion into one prompt
