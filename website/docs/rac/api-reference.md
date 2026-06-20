---
sidebar_position: 9
title: API Reference — mycontext.rac
description: Every public symbol in mycontext.rac — signatures, parameters, return values, examples, and spec dictionary shapes. The single source of truth for the LLM-native RaC pipeline.
---

# API Reference — `mycontext.rac`

All RaC functions are **LLM-native**: every call routes through an LLM using
your own provider key. There is no offline/deterministic fallback. A provider
key is required for all generation, validation, and trace functions.

```python
from mycontext.rac import (
    # Step 0 — Intent assessment
    assess, IntakeBrief,
    # Step 1 — Product requirements (the what & why)
    product,
    # Step 2 — Technical requirements (the how)
    technical,
    # Step 3 — Review & alignment
    validate, trace, format_report,
    # Step 4 — Render for coding agents
    project, TARGETS,
    # Utilities
    to_yaml, score_output,
    # Cognitive-pattern grounding
    analyze, format_brief, select_patterns,
    # Structured-output contract (Pydantic)
    ProductSpec, TechnicalSpec,
    parse_product, parse_technical,
    check_product_integrity, check_technical_integrity,
    normalize_product, normalize_technical,
    # Error type
    LLMUnavailable,
)
```

---

## Step 0 — Intake

### `assess`

```python
assess(
    text: str,
    *,
    provider: str = "openai",
    model: str | None = None,
) -> IntakeBrief
```

Assess a raw intent and return a structured `IntakeBrief`. Fully LLM-native.
`text` may be a sentence, a paragraph, or the full contents of a `.txt` / `.md`
file.

The LLM analyses every facet of the intent — system name, task taxonomy, risk
level, must-never lines, tool candidates, stakeholders, volume, constraints, open
questions — and grounds the analysis in a set of dynamically selected cognitive
patterns.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | required | Raw intent (inline text or file contents). |
| `provider` | `str` | `"openai"` | LLM provider (`openai`, `anthropic`, `gemini`). |
| `model` | `str \| None` | `None` | Model name. `None` uses the provider's default (`gpt-4o-mini` for OpenAI). |

**Returns:** `IntakeBrief`

**Raises:** `LLMUnavailable` if no provider key is configured.

**Example:**
```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."

from mycontext.rac import assess

brief = assess(
    "A support bot that drafts replies to billing emails "
    "but never sends refunds without human approval."
)
print(brief.system_name)       # e.g. "billing-support-bot"
print(brief.kind)              # "agent"
print(brief.to_markdown())     # human-readable brief
print(brief.to_json())         # JSON string
```

---

### `IntakeBrief`

```python
@dataclass
class IntakeBrief:
    intent: str                    # the original input text
    data: dict[str, Any]           # full LLM-authored brief dict
    patterns_used: list[str]       # cognitive patterns that grounded the analysis

    @property
    def system_name(self) -> str   # kebab-case system name (e.g. "billing-support-bot")
    @property
    def kind(self) -> str          # "agent" | "rag" | "multi_agent" | "service"

    def to_dict(self) -> dict      # raw brief as a dict
    def to_json(self) -> str       # JSON string (pretty-printed)
    def to_markdown(self) -> str   # human/coding-agent-friendly Markdown
```

The `data` dict contains the full structured brief, including:

| Key | Type | Description |
|-----|------|-------------|
| `system_name` | `str` | Inferred kebab-case system name. |
| `kind` | `str` | System type: `agent` \| `rag` \| `multi_agent` \| `service`. |
| `summary` | `str` | Plain-language description of what the system does. |
| `primary_capabilities` | `list[str]` | Core capabilities inferred from the intent. |
| `task_types` | `list[dict]` | Each task with `name`, `example`, `freq_hint`, `risk`, `handling`. |
| `out_of_scope_categories` | `list[str]` | Named refusal categories. |
| `must_never` | `list[str]` | Hard safety boundaries. |
| `tools_or_actions` | `list[dict]` | Candidate tools with `reversible`, `worst_case`, `suggested_policy`. |
| `stakeholders` | `list[dict]` | Stakeholders and what they sign off on. |
| `constraints` | `dict` | `hitl`, `pii`, `money_actions`, `budget_per_task_usd`. |
| `risks` | `list[str]` | Pre-mortem failure modes. |
| `assumptions` | `list[str]` | Conditions the system takes for granted. |
| `open_questions` | `list[dict]` | `{id, question, why_it_matters, blocking}` — gaps to resolve before ratifying. |
| `recommended_patterns` | `list[str]` | Cognitive patterns worth running for deeper analysis. |
| `brief_markdown` | `str` | Full Markdown rendering of the brief. |

---

## Step 1 — Product requirements

### `product`

```python
product(
    intent: str | IntakeBrief,
    *,
    provider: str = "openai",
    model: str | None = None,
    brief: IntakeBrief | None = None,
) -> dict
```

Generate a complete **product requirements** spec (the *what & why*) from a
natural-language intent or a pre-computed `IntakeBrief`. The LLM decides how
many tasks, rubric criteria, actions, safety requirements, and release gates the
system warrants — there is no fixed skeleton. A Pydantic structured-output
contract enforces the typed-ID grammar and referential integrity, with a
self-repair loop.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `intent` | `str \| IntakeBrief` | required | Raw intent text, or a pre-computed `IntakeBrief` from `assess()`. |
| `provider` | `str` | `"openai"` | LLM provider. |
| `model` | `str \| None` | `None` | Model name; `None` uses the provider default. |
| `brief` | `IntakeBrief \| None` | `None` | Deprecated keyword alias for passing an `IntakeBrief` as `intent`. |

**Returns:** `dict` — a product spec with `meta.spec_type == "product_requirements"`.

**Raises:** `LLMUnavailable` if no key; `RuntimeError` if the LLM returns empty sections after the repair loop.

**Examples:**

```python
from mycontext.rac import assess, product, to_yaml

# From raw text
prod = product(
    "Brightcart support bot that drafts billing replies; "
    "refunds need human approval; never leak customer data."
)
print(prod["meta"]["system_name"])    # e.g. "brightcart-support-bot"
print(prod["meta"]["spec_type"])      # "product_requirements"
print(list(prod["tasks"].keys()))     # e.g. ["T1", "T2", "T_oos"]

# From a pre-computed IntakeBrief (reuse the assessment)
brief = assess("...", provider="openai", model="gpt-4o")
prod = product(brief, provider="openai", model="gpt-4o")

# Save to file
with open("product.yaml", "w") as f:
    f.write(to_yaml(prod))
```

**Product spec structure:**

| Key | Type | Description |
|-----|------|-------------|
| `meta` | `dict` | `system_name`, `spec_type`, `kind`, `status`, `intent`, `generated_by`, `generated_by_model`, `informed_by`. |
| `tasks` | `dict` | `T1`, `T2`, …, mandatory `T_oos`. Each has `name`, `example`, `risk`, `handling`, `rubric`, `no_draft`, `freq_hint`. |
| `rubrics` | `dict` | `R-T1`, `R-T2`, …, `R-T_oos`. Each has `criteria: [{id, anchor, grader, text}]`. Graders: `code` \| `judge` \| `human`. |
| `actions` | `list` | `[{id: "A-1", policy: "auto\|approve\|forbidden", reversible, worst_case, tools}]`. |
| `safety` | `list` | `[{id: "P1", incident, requirement, eval: {dataset, assert, hard_gate}}]`. |
| `datasets` | `dict` | Size, contamination rule, flywheel strategy. |
| `baselines` | `dict` | `human` and `bare_model` baselines for comparison. |
| `budgets` | `dict` | Cost/latency budgets per task. |
| `gates` | `dict` | `{items: [{id: "G-1", scope, metric, threshold, hard_gate}], on_failure}`. |
| `monitoring` | `dict` | Drift alarms, HITL stats. |
| `assumptions` | `list[str]` | Conditions this spec takes for granted. |
| `open_questions` | `list[dict]` | `{id: "OQ-01", question, affects, blocking, status}` — gaps to resolve. |

**Typed-ID grammar:**

| ID type | Pattern | Example |
|---------|---------|---------|
| Task | `T<n>` or `T_oos` | `T1`, `T_oos` |
| Rubric | `R-<task>` | `R-T2`, `R-T_oos` |
| Rubric criterion | `R-<task>.<n>` | `R-T2.3` |
| Action | `A-<n>` | `A-4` |
| Safety | `P<n>` | `P1` |
| Gate | `G-<n>` | `G-2b` |
| Open question | `OQ-<nn>` | `OQ-01` |

---

## Step 2 — Technical requirements

### `technical`

```python
technical(
    text: str | None = None,
    *,
    product: dict | str | None = None,
    frontier: bool = False,
    provider: str = "openai",
    model: str | None = None,
) -> dict
```

Generate a complete **technical requirements** spec (the *how*) covering all 24
sections of the Fable agentic-engineering template. The LLM authors every section
in two focused passes (12 sections each) to avoid token-budget truncation.

Pass `product=<spec>` for traceable controls whose `serves` lists reference the
product's task/action/safety/gate IDs. Pass `text` to bootstrap from intent
when no product spec exists yet.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str \| None` | `None` | Natural-language intent. Required if `product` is not given. |
| `product` | `dict \| str \| None` | `None` | Product spec dict **or** a YAML/JSON string. When a string is passed it is parsed automatically with `yaml.safe_load`. |
| `frontier` | `bool` | `False` | Include detailed content for `model_layer_advanced`, `agent_rl`, and `frontier_capabilities` (Tier-3 sections). |
| `provider` | `str` | `"openai"` | LLM provider. |
| `model` | `str \| None` | `None` | Model name. `None` uses the provider default. |

Exactly one of `text` or `product` must be supplied; passing neither raises
`ValueError`.

**Returns:** `dict` — a technical spec with `meta.spec_type == "technical_requirements"`.

**Raises:** `LLMUnavailable` if no key; `RuntimeError` if the LLM returns empty Tier-1 sections after the repair loop.

**Examples:**

```python
from mycontext.rac import product, technical, to_yaml

prod = product("Billing support bot; refunds need approval.")

# Rich path — traceable controls (recommended)
tech = technical(product=prod, provider="openai", model="gpt-4o")
print(tech["meta"]["source"])            # "product_requirements"
print(tech["architecture"]["pattern"])   # e.g. "typed_stateful_orchestrator"

# Bootstrap path — from text only
tech = technical(
    "A RAG assistant that answers policy questions; never invents answers.",
    provider="openai",
)
print(tech["meta"]["source"])            # "natural_language"

# Frontier mode — add fine-tune / RL / computer-use layer
tech = technical(product=prod, frontier=True, model="gpt-4o")

# Accepts a YAML string (e.g. loaded from disk as str)
with open("product.yaml") as f:
    prod_yaml = f.read()
tech = technical(product=prod_yaml)

# Save
with open("technical.yaml", "w") as f:
    f.write(to_yaml(tech))
```

**Technical spec — 24 sections:**

The spec has three tiers. Tier-1 sections are required for every production agent.
Tier-2 are common operational concerns. Tier-3 are advanced model-layer topics
(usually marked `not_applicable: true` unless `frontier=True`).

| Tier | Sections |
|------|----------|
| **Tier 1 — Functional** | `identity`, `ownership`, `architecture`, `autonomy`, `memory`, `guardrails`, `tools` |
| **Tier 1 — Non-functional** | `quality_gates`, `operational_constraints`, `cost`, `deployment`, `observability`, `security`, `failure_behavior` |
| **Tier 2** | `incident_response`, `audit`, `compliance`, `governance`, `promptops`, `caching`, `data_engineering`, `continuous_improvement` |
| **Tier 3** | `model_layer_advanced`, `agent_rl`, `frontier_capabilities`, `lifecycle` |

Each section may be marked `{not_applicable: true, reason: "..."}` if it
genuinely does not apply — absence is never "decided". Controls that implement
a product requirement carry a `serves: ["T1", "P1", "A-2"]` list for
traceability.

**`meta` keys in technical specs:**

| Key | Description |
|-----|-------------|
| `system_name` | Canonical name (always taken from the product spec, never the LLM's placeholder). |
| `spec_type` | `"technical_requirements"` |
| `for_product` | Same as `system_name` — the product this technical spec implements. |
| `kind` | Agent kind (`agent`, `rag`, etc.). |
| `source` | `"product_requirements"` or `"natural_language"`. |
| `intent` | The original intent text. |
| `product_ids` | List of all product IDs available for traceability (only present when `product=` was supplied and non-empty). |
| `informed_by` | Cognitive patterns used to ground the generation. |
| `generated_by` | `"mycontext-ai <version> technical-architect"` |
| `generated_by_model` | Model that authored the spec. |

---

## Step 3 — Review & alignment

### `validate`

```python
validate(
    doc: dict,
    *,
    provider: str = "openai",
    model: str | None = None,
    llm: bool = True,
) -> list[str]
```

Run structural contract checks plus an LLM quality critique on a product or
technical spec. Dispatches on `doc["meta"]["spec_type"]`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `doc` | `dict` | required | Product or technical spec dict. |
| `provider` | `str` | `"openai"` | LLM provider for the quality critique. |
| `model` | `str \| None` | `None` | Model name. |
| `llm` | `bool` | `True` | `False` for structural-only checks (no LLM call). |

**Returns:** `list[str]` — each item prefixed `[ERROR]`, `[WARN]`, or `[INFO]`.
An empty list means clean. `[ERROR]` items indicate structural violations that
must be fixed before the spec is usable. `[WARN]` items are quality issues.

**Examples:**

```python
from mycontext.rac import validate

issues = validate(prod)
errors = [i for i in issues if i.startswith("[ERROR]")]
if errors:
    print("Spec has contract violations:", errors)

# Structural-only (no LLM call, good for CI smoke check)
issues = validate(prod, llm=False)
```

---

### `trace`

```python
trace(
    product: dict,
    technical: dict,
    diff: str | None = None,
    *,
    provider: str = "openai",
    model: str | None = None,
) -> dict
```

Compare a product spec to a technical spec and return a coverage/drift report.
Optionally analyse a unified code diff for forbidden-tool use and
out-of-scope changes.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `product` | `dict` | required | Product requirements spec dict. |
| `technical` | `dict` | required | Technical requirements spec dict. |
| `diff` | `str \| None` | `None` | Unified diff string (e.g. from `git diff`). Truncated to 8 000 chars internally. |
| `provider` | `str` | `"openai"` | LLM provider. |
| `model` | `str \| None` | `None` | Model name. |

**Returns:** `dict` with these keys:

| Key | Type | Description |
|-----|------|-------------|
| `status` | `str` | `"in_sync"` \| `"review"` \| `"drift_detected"`. |
| `coverage` | `dict` | `{covered: [IDs], uncovered: [{id, kind, label}], ratio: float}`. |
| `orphans` | `list` | Technical `serves` references to non-existent product IDs. |
| `diff_impact` | `list` | `[{file, touches: [IDs], forbidden_used: [tool]}]`. |
| `findings` | `list[str]` | Human-readable findings, each prefixed `[ERROR]`, `[WARN]`, or `[OK]`. |
| `markdown` | `str` | Full Markdown report. |

**Example:**

```python
from mycontext.rac import trace, format_report
import subprocess

diff = subprocess.check_output(["git", "diff", "main...HEAD"], text=True)
report = trace(prod, tech, diff=diff)
print(format_report(report))
if report["status"] == "drift_detected":
    raise SystemExit(1)   # CI gate
```

---

### `format_report`

```python
format_report(report: dict) -> str
```

Render a `trace()` report dict as readable Markdown. Uses `report["markdown"]`
if present (the LLM-authored version), otherwise assembles a fallback from
`coverage` and `findings`.

---

## Step 4 — Render for coding agents

### `project`

```python
project(
    doc: dict,
    to: str,
    *,
    provider: str = "openai",
    model: str | None = None,
) -> str
```

Render a product or technical spec into a downstream file format. LLM-native.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `doc` | `dict` | required | Product or technical spec dict. |
| `to` | `str` | required | Target format — must be one of `TARGETS`. |
| `provider` | `str` | `"openai"` | LLM provider. |
| `model` | `str \| None` | `None` | Model name. |

**Returns:** `str` — rendered file content.

**Raises:** `ValueError` if `to` is not in `TARGETS`, or if a product-only target
is given a technical spec.

### `TARGETS`

```python
TARGETS = ("agents-md", "claude", "cursor", "spec-kit", "kiro", "adr")
```

| Target | Output | Use with |
|--------|--------|----------|
| `agents-md` | `AGENTS.md` behavioral rules | Product spec |
| `claude` | `CLAUDE.md` for Claude Code | Product spec |
| `cursor` | `.cursor/rules/*.mdc` | Product spec |
| `spec-kit` | Spec Kit YAML | Product spec |
| `kiro` | EARS-format requirements | Product spec |
| `adr` | Architecture Decision Record | Technical spec |

**Example:**

```python
from mycontext.rac import project

agents_md = project(prod, "agents-md")
with open("AGENTS.md", "w") as f:
    f.write(agents_md)

adr = project(tech, "adr")
with open("ARCHITECTURE.md", "w") as f:
    f.write(adr)
```

---

## Utilities

### `to_yaml`

```python
to_yaml(doc: dict) -> str
```

Serialize any spec dict to YAML (UTF-8, key order preserved, `assert` alias
handled for safety eval blocks).

```python
from mycontext.rac import to_yaml

print(to_yaml(prod))   # print to console
with open("product.yaml", "w") as f:
    f.write(to_yaml(prod))
```

### `score_output`

```python
score_output(context_prompt: str, output: str) -> dict
```

Score a candidate LLM output against the context that produced it. Returns
`{overall: float, dimensions: dict, strengths: list, weaknesses: list}`. Runs
offline via `OutputEvaluator`.

### `LLMUnavailable`

```python
class LLMUnavailable(RuntimeError): ...
```

Raised when a provider key is required but not found in the environment. Catch
this to show a user-friendly message.

```python
from mycontext.rac import LLMUnavailable, product

try:
    prod = product("...")
except LLMUnavailable as exc:
    print(f"Set your API key first: {exc}")
```

---

## Cognitive-pattern grounding

### `analyze`

```python
analyze(
    text: str,
    *,
    kind: str = "product",
    provider: str = "openai",
    model: str | None = None,
) -> dict[str, dict[str, str]]
```

Run the curated cognitive patterns for `kind` (`"product"` or `"technical"`)
against a raw intent and return the grounding briefs that `product()` /
`technical()` use internally. Call this when you want to inspect or extend the
LLM analysis before spec generation.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | required | Raw intent text. |
| `kind` | `str` | `"product"` | Which pattern set to run (`"product"` or `"technical"`). |
| `provider` | `str` | `"openai"` | LLM provider. |
| `model` | `str \| None` | `None` | Model name. |

**Returns:** `dict[section, dict[pattern_name, analysis_text]]`

### `format_brief`

```python
format_brief(notes: dict[str, dict[str, str]]) -> str
```

Render `analyze()` output as Markdown.

### `select_patterns`

```python
select_patterns(
    intent: str,
    *,
    kind: str = "product",
    provider: str,
    model: str | None,
) -> list[str]
```

Ask an LLM to select the most relevant cognitive patterns for `intent` and
`kind`. Used internally by `product()` and `technical()`.

---

## Structured-output contract

These are the mechanical validation layer — used internally by the generators
and available to callers who want to validate specs programmatically.

### `parse_product` / `parse_technical`

```python
parse_product(data: dict) -> ProductSpec      # raises ValidationError
parse_technical(data: dict) -> TechnicalSpec  # raises ValidationError
```

Parse a raw dict into a Pydantic model. Raises `pydantic.ValidationError` on
any schema violation. The generators call this after every repair pass to confirm
the contract is satisfied.

### `check_product_integrity` / `check_technical_integrity`

```python
check_product_integrity(data: dict) -> list[str]
check_technical_integrity(data: dict) -> list[str]
```

Return `[ERROR]` / `[WARN]` messages for structural violations. Does **not**
raise — the generators use the list to drive the self-repair loop.

```python
from mycontext.rac import check_product_integrity

issues = check_product_integrity(prod)
errors = [i for i in issues if i.startswith("[ERROR]")]
print(f"{len(errors)} contract violations")
```

### `normalize_product` / `normalize_technical`

```python
normalize_product(data: dict) -> dict
normalize_technical(data: dict) -> dict
```

Fix common LLM structural mistakes in-place and return the dict:

- Rubric criteria placed as sibling keys → moved inside `criteria` list
- Gate dicts placed as sibling keys → moved inside `gates.items`
- `suggested_policy` → renamed to `policy`
- Empty `baselines` / `budgets` / `monitoring` → replaced with `_note` stubs
- String `open_questions` items → converted to dicts with auto-assigned IDs
- Stray root-level keys that belong in `meta` → removed
- `meta.assumptions` with empty root `assumptions` → rescued to root (technical)

Call these before `validate()` or `parse_*()` if you loaded a spec from a file
that may not have been generated by the current version.

---

## End-to-end Python example

```python
import os
from mycontext.rac import (
    assess, product, technical, trace, format_report,
    validate, project, to_yaml, LLMUnavailable,
)

os.environ["OPENAI_API_KEY"] = "sk-..."

INTENT = (
    "Sales spends too much time writing follow-up emails after demos. "
    "We want to speed that up while keeping our tone on-brand. "
    "Reps still review everything before it goes to a prospect."
)

try:
    # Step 0 — Understand the intent
    brief = assess(INTENT, model="gpt-4o")
    print(brief.to_markdown())

    # Step 1 — What & why
    prod = product(brief, model="gpt-4o")

    # Step 2 — How (traceable to product IDs)
    tech = technical(product=prod, model="gpt-4o")

    # Step 3 — Validate both
    for spec, name in [(prod, "product"), (tech, "technical")]:
        issues = validate(spec, llm=False)
        errors = [i for i in issues if i.startswith("[ERROR]")]
        if errors:
            print(f"[{name}] contract violations:", errors)

    # Step 4 — Check coverage
    report = trace(prod, tech)
    print(format_report(report))

    # Step 5 — Render for your coding agent
    agents_md = project(prod, "agents-md")
    print(agents_md)

    # Save YAML
    with open("product.yaml", "w") as f:
        f.write(to_yaml(prod))
    with open("technical.yaml", "w") as f:
        f.write(to_yaml(tech))

except LLMUnavailable as exc:
    print(f"API key required: {exc}")
```
