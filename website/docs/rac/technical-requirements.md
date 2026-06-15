---
sidebar_position: 4
title: Technical Requirements — technical()
description: Deep dive on mycontext.rac.technical() — the two entry paths, the serves traceability model, and every section of the generated technical-requirements spec.
---

# Technical Requirements — `technical()`

Where [`product()`](./product-requirements) answers *what* a system must do,
`technical()` answers **how it is built**: architecture, guardrails, tool
permissions, cost controls, deployment, observability, security, and failure
behavior — plus an optional `frontier` layer (fine-tune / RL / computer-use).

Its defining feature is **traceability**: every control carries a `serves:` list
of the product requirement IDs it implements, so [`trace()`](./trace-and-validation)
can prove coverage and catch drift.

```python
from mycontext.rac import product, technical, to_yaml

prod = product("Aurora drafts replies to billing emails; refunds need approval.")
tech = technical(product=prod)
print(to_yaml(tech))
```

## Signature & parameters

```python
def technical(
    text: str | None = None,
    *,
    product: dict | None = None,
    frontier: bool = False,
    execute: bool = False,
    provider: str = "openai",
    model: str | None = None,
) -> dict
```

| Parameter | Type | Default | Meaning |
|-----------|------|---------|---------|
| `text` | `str \| None` | `None` | Natural-language intent — the *bootstrap* path. Use when you don't have a product spec yet. |
| `product` | `dict \| None` | `None` | A product spec (from `product()`) — the *rich* path. Enables full `serves:` traceability. |
| `frontier` | `bool` | `False` | Include the advanced `frontier` layer (fine-tune, RL, computer-use, multimodal). |
| `execute` | `bool` | `False` | Use your LLM key to answer the open questions and return a filled spec. See [grounding](./cognitive-grounding). |
| `provider` | `str` | `"openai"` | Provider for `execute=True`. |
| `model` | `str \| None` | `None` | Model for `execute=True`; `None` → provider-aware default. |

You must pass **either** `product=` **or** `text`. Passing neither raises
`ValueError`.

**Returns** a `dict` with `meta.spec_type == "technical_requirements"`.

## Two entry paths

### Rich path — `technical(product=spec)` (recommended)

```python
tech = technical(product=prod, frontier=True)
```

When you pass a product spec, `technical()` reads its tasks, actions, safety
entries, rubrics, and gates, and **wires real `serves:` links** into every
control. This is what makes [`trace()`](./trace-and-validation) meaningful.

### Bootstrap path — `technical("<intent>")`

```python
tech = technical("A RAG assistant answers questions from our wiki; never invent answers.")
```

With only text, `technical()` still emits the full structure, but `serves:` links
that would point at product IDs are left as `TODO(OQ-n)` with a nudge to generate
a product spec first. `meta.source` will be `natural_language` instead of
`product_requirements`.

## The output, section by section

### `meta`

```yaml
meta:
  system_name: aurora
  spec_type: technical_requirements
  for_product: aurora
  kind: agent
  spec_version: 0.1.0
  status: draft
  generated_by: mycontext-ai 0.13.0 technical-architect
  source: product_requirements      # or 'natural_language'
  note: "Technical requirements authored by mycontext ... build/enforcement belongs to your stack."
  review_checklist:
    - Pin concrete model IDs, infra, and thresholds (replace TODO markers)
    - Confirm every `serves` reference resolves to a real product requirement
    - Run `mycontext rac trace` to verify product/technical coverage
```

### `architecture`

```yaml
architecture:
  pattern: "tool_augmented_agent (plan -> act -> observe loop)"   # chosen by kind
  orchestration:
    loop: "plan -> act -> observe"
    max_steps: TODO(OQ-n)        # suggested default 6
  state:
    short_term: "per-request scratchpad (conversation memory)"
    long_term: "vector store over the trusted source"   # for rag; else 'none'
  model_routing_ref: cost.routing
  serves: [T1]                   # the product tasks this architecture serves
```

The `pattern` is selected from `kind`: `tool_augmented_agent` (agent),
`supervisor_orchestrator` (multi_agent), `retrieve_then_generate` (rag), or
`stateless_request_handler` (service).

### `guardrails`

Three layers — input, processing, output — each a list of controls with a
`serves:` link:

```yaml
guardrails:
  input:
    - {control: "Treat all user/tool content as data, never instructions (prompt-injection defense)", serves: [P4]}
    - {control: "Schema + length validation on inbound payloads", serves: [T1]}
  processing:
    - {control: "Tool-call allowlist; calls outside the registry are rejected", serves: [A-X, A-3]}
    - {control: "Per-request step + token budget enforced", serves: [cost]}
  output:
    - {control: "Groundedness check — every claim traceable to source before send", serves: [R-T1]}
    - {control: "No claim that an approval-gated action completed before approval", serves: [A-3]}
    - {control: "PII / cross-customer data redaction on output", serves: [P2]}   # if leak safety exists
```

### `tools`

The tool registry (with least-privilege scopes), forbidden tools, and the
non-human-identity (service account) principle:

```yaml
tools:
  registry:
    - {name: draft_reply, access: write, requires_approval: false, scope: TODO(OQ-n), serves: [A-2]}
    - {name: send_reply,  access: write, requires_approval: true,  scope: TODO(OQ-n), serves: [A-3]}
  forbidden:
    - {tools: [delete_record, modify_history, merge_records], policy: forbidden, serves: [A-X]}
  non_human_identity:
    principle: "least privilege per tool; short-lived credentials"
    scopes: TODO(OQ-n)
```

### `cost`

```yaml
cost:
  budget_per_task_usd: TODO(OQ-n)   # suggested default 0.40
  routing:
    draft_model: TODO(OQ-n)
    escalation_model: TODO(OQ-n)
    rule: "strong model for high/critical-risk tasks and on low confidence; cheap model otherwise"
    serves: [T1]
  daily_budget_usd: TODO(OQ-n)      # suggested default 200
  on_exhaustion: "degrade to draft-only / escalate to human; never silently drop work"
```

### `deployment`, `observability`, `security`, `failure_behavior`

```yaml
deployment:
  rollout: {strategy: "shadow -> canary -> full", stages: ["5% shadow", "25% canary", "100%"], gated_by: [G-1, G-2, G-3]}
  rollback: "auto-rollback if any hard gate regresses in canary"
  canary_dimensions: [task risk tier, new tool usage, cost per task]

observability:
  metrics:
    - {name: rubric_pass_rate, serves: [G-1, G-2, G-3]}
    - {name: hitl_approval_and_rejection_rate, serves: [A-3]}
    - {name: cost_per_task, serves: [cost]}
    - {name: "unmapped_task_rate (charter drift)", serves: [T1]}
  tracing: "span per plan/act/observe step, each tool call, and each approval decision"
  audit_log: {what: "all write + approval actions, immutable", serves: [A-3]}

security:
  owasp_agentic_top10:
    - {risk: Excessive Agency,  mitigation: "forbidden-tool list + approval gates", serves: [A-X, A-3]}
    - {risk: Prompt Injection,  mitigation: "input-as-data guard; risky actions stay HITL", serves: [P4]}
    - {risk: Sensitive Information Disclosure, mitigation: "output PII/cross-customer redaction", serves: [P2]}
  secrets: "no secrets in prompts/logs; pull from a secrets manager at call time"
  data_handling: "PII minimized + redacted in traces"   # when pii detected

failure_behavior:
  on_tool_error: {strategy: "retry with backoff then escalate", max_retries: TODO(OQ-n)}
  on_low_confidence: {strategy: "route to human; never guess", serves: [T_oos, P1, P4]}
  degraded_mode: "draft-only / read-only when a dependency is down; surface status, don't fail silently"
```

### `frontier` (optional, `frontier=True`)

```yaml
frontier:
  model_layer_advanced: {fine_tune: TODO(OQ-n), distillation: "...", self_host: "..."}
  agent_rl: {enabled: false, note: TODO(OQ-n)}
  frontier_capabilities: {computer_use: false, multimodal: TODO(OQ-n), voice: false, agent_to_agent: false}
  serves: [T1]
```

## The `serves` traceability model

Every risk-bearing control links to the product requirement ID(s) it implements:

| Product ID prefix | What it is |
|-------------------|------------|
| `T*` | A task (e.g. `T1`, `T_oos`) |
| `A*` | An action (e.g. `A-3`, `A-X`) |
| `P*` | A safety requirement (e.g. `P1`, `P4`) |
| `G*` | A release gate (e.g. `G-1`) |
| `R-*` | A rubric (e.g. `R-T1`) |
| `cost` | The cost section (a non-ID anchor) |

`trace()` uses these links to compute coverage. See
[Trace & validation](./trace-and-validation).

## Validate a technical spec

```python
from mycontext.rac import technical, validate

issues = validate(technical(product=prod))
# Technical validator checks required sections, guardrail layers, forbidden tools,
# and open-question bookkeeping. It never emits the product-only "Uncovered" errors.
```

## Next

- Prove the two specs agree: [Trace & validation →](./trace-and-validation)
- Render the technical spec to an ADR / AGENTS.md: [Projections →](./projections)
