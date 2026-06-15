---
sidebar_position: 9
title: API Reference — mycontext.rac
description: Every public symbol in mycontext.rac — signatures, parameters, return values, and the spec dictionary shapes — plus the legacy authoring + scoring bridge.
---

# API Reference — `mycontext.rac`

Everything importable from `mycontext.rac`. All functions are pure and offline
unless they take a `provider`/`model` (used only with `execute=True`).

```python
from mycontext.rac import (
    product, technical, trace, format_report,    # generate + sync
    validate, project, TARGETS, to_yaml,          # check + render
    analyze, format_brief, complete,              # LLM grounding + fill
    parse_intent, Intake,                         # intake
    RequirementsArchitect, TechnicalArchitect,    # configurable classes
    architect,                                    # deprecated alias for product
    draft_requirements, score_output, RequirementsAuthor,  # legacy bridge
)
```

## Generation

### `product`

```python
product(text: str, *, execute=False, provider="openai", model=None) -> dict
```

Generate a **product-requirements** spec from natural-language intent. See
[Product requirements](./product-requirements). Returns a spec dict with
`meta.spec_type == "product_requirements"`.

### `technical`

```python
technical(text=None, *, product=None, frontier=False,
          execute=False, provider="openai", model=None) -> dict
```

Generate a **technical-requirements** spec from a product spec (`product=`) or
intent (`text`). See [Technical requirements](./technical-requirements). Pass
exactly one source; neither raises `ValueError`.

### `architect` (deprecated)

```python
architect(text: str, *, tier=1, execute=False, provider="openai", model=None) -> dict
```

Deprecated alias for `product()` with an extra `tier` argument. Prefer
`product()`.

### `RequirementsArchitect` / `TechnicalArchitect`

Configurable dataclasses behind `product()` / `technical()`:

```python
RequirementsArchitect(provider="openai", execute=False, model=None)
    .draft(text, *, tier=None) -> dict
    .draft_from_intake(intake: Intake) -> dict

TechnicalArchitect(provider="openai", execute=False, frontier=False, model=None)
    .draft(*, text=None, product=None) -> dict
```

Use these when you want to reuse one configuration across many drafts.

## Intake

### `parse_intent`

```python
parse_intent(text: str, *, tier=1) -> Intake
```

Parse free-text intent into a structured [`Intake`](#intake-1) (offline,
heuristic). Detects name, kind, must-never lines, volume, and constraints
(`pii`, `hitl`, `money_actions`, `budget_per_task_usd`); records everything else
as `Intake.gaps`.

### `Intake`

```python
@dataclass
class Intake:
    name: str | None
    kind: str                 # "agent" | "multi_agent" | "rag" | "service"
    intent: str
    must_never: list[str]
    volume: str | None
    constraints: dict[str, Any]
    tier: int
    gaps: list[Gap]
    def to_dict(self) -> dict
```

`Gap(question, affects, suggested_default=None, blocking=False)` represents one
missing/ambiguous input, surfaced later as an open question.

## Sync & validation

### `trace`

```python
trace(product: dict, technical: dict, diff: str | None = None) -> dict
```

Compare a product spec to a technical spec (and an optional code diff). Returns a
report with `status`, `coverage`, `orphans`, `diff_impact`, and `findings`. See
[Trace & validation](./trace-and-validation).

### `format_report`

```python
format_report(report: dict) -> str
```

Render a `trace()` report as readable markdown.

### `validate`

```python
validate(doc: dict) -> list[str]
```

Structural lint for a product or technical spec (dispatches on
`meta.spec_type`). Returns `["[ERROR] ...", "[WARN] ..."]`; empty == clean. See
the [rule set](./trace-and-validation#validation-rules).

## Rendering

### `project`

```python
project(doc: dict, to: str) -> str
```

Render a spec into a target file format. See [Projections](./projections).

### `TARGETS`

```python
TARGETS = ("agents-md", "claude", "cursor", "spec-kit", "kiro", "adr")
```

### `to_yaml`

```python
to_yaml(requirements: dict) -> str
```

Serialize any spec dict to YAML (UTF-8, key order preserved).

## LLM grounding & fill

### `analyze`

```python
analyze(text: str, *, kind="product", provider="openai", model=None) -> dict[str, dict[str, str]]
```

Run the curated cognitive patterns for `kind` (`"product"`/`"technical"`) and
return `{section: {pattern_name: analysis_text}}`. Requires a key. See
[grounding](./cognitive-grounding#analyze--read-the-grounding-directly).

### `format_brief`

```python
format_brief(notes: dict[str, dict[str, str]]) -> str
```

Render `analyze()` output as markdown (friendly placeholder when empty).

### `complete`

```python
complete(doc: dict, *, provider="openai", model=None, extra_context=None) -> dict
```

Fill a draft spec's `open_questions` with LLM answers and substitute them in.
Returns a new dict (input not mutated). See
[grounding](./cognitive-grounding#complete--fill-an-existing-draft).

### `models`

```python
from mycontext.rac.models import resolve_model, DEFAULT_MODELS

resolve_model(provider: str, model: str | None) -> str
```

Returns `model` if given, else the provider's default; raises `ValueError` for a
provider with no known default. `DEFAULT_MODELS` maps `openai`, `anthropic`,
`gemini`, `google`. See
[provider-aware models](./cognitive-grounding#provider-aware-default-models).

## Spec dictionary shapes

### Product spec (top-level keys)

| Key | Type | Notes |
|-----|------|-------|
| `meta` | dict | `system_name`, `spec_type`, `kind`, `status`, `intent`, `review_checklist`, (`informed_by`, `filled_by` after execute). |
| `tasks` | dict | `T1`, optional `T2`, mandatory `T_oos`. |
| `rubrics` | dict | One per task. |
| `actions` | list | The action risk matrix (`policy`: auto/approve/forbidden). |
| `safety` | list | Pre-mortem; each a hard gate with a test. |
| `datasets` | dict | Slices, anonymization, contamination rule, flywheel. |
| `baselines` | dict | `human`, `bare_model`. |
| `gates` | dict | `items`, `on_failure`. |
| `monitoring` | dict | Drift alarms, HITL stats. |
| `assumptions` | list | Empty by default. |
| `open_questions` | list | `{id, question, affects, suggested_default?, blocking, status}`. |

### Technical spec (top-level keys)

| Key | Type | Notes |
|-----|------|-------|
| `meta` | dict | `spec_type`, `source` (`product_requirements`/`natural_language`). |
| `architecture` | dict | Pattern, orchestration, state. |
| `guardrails` | dict | `input` / `processing` / `output` control lists. |
| `tools` | dict | `registry`, `forbidden`, `non_human_identity`. |
| `cost` | dict | Budgets + model routing. |
| `deployment` | dict | Rollout, rollback, canary. |
| `observability` | dict | Metrics, tracing, audit log. |
| `security` | dict | OWASP agentic top-10, secrets, data handling. |
| `failure_behavior` | dict | Tool error, low confidence, degraded mode. |
| `frontier` | dict | Only when `frontier=True`. |
| `open_questions` | list | Same shape as product. |

Risk-bearing controls carry a `serves: [<product IDs>]` list — the basis for
`trace()` coverage.

## Legacy authoring + scoring bridge

These predate the product/technical generators and remain for backwards
compatibility. New code should use `product()` / `technical()`.

### `draft_requirements`

```python
draft_requirements(task: str, provider="openai", execute=False, **kwargs) -> dict
```

Draft a legacy `requirements.yaml` structure whose sections (`task_taxonomy`,
`rubrics`, `action_risk_matrix`, `pre_mortem`) are authored by a fixed mapping of
cognitive patterns. Offline by default; `execute=True` fills each section with
LLM output.

### `RequirementsAuthor`

```python
RequirementsAuthor(provider="openai", execute=False, sections=...).draft(task, **kwargs) -> dict
```

The configurable class behind `draft_requirements`.

### `score_output`

```python
score_output(context_prompt: str, output: str, mode="heuristic") -> dict
```

Score a candidate output against the context that produced it, via
`OutputEvaluator`. Returns `{overall, dimensions, strengths, weaknesses}`.
Offline in `heuristic` mode. This is still useful on its own — e.g. to score
candidate rubric answers before handing a spec to your gates.

```python
from mycontext.rac import score_output

result = score_output(
    "Identify the root causes of the outage and propose fixes.",
    "Root cause: a misconfigured timeout. Fix: add validation. Step 1: ...",
)
print(result["overall"])      # e.g. 0.78
print(result["dimensions"])   # per-dimension scores
```
