---
sidebar_position: 12
title: GuidanceOptimizer
description: Audit and rewrite weak rules in SDK Guidance objects — converts suggestive modals to binding directives automatically.
---

# GuidanceOptimizer

`GuidanceOptimizer` audits `Guidance` objects in SDK templates for three structural weaknesses and rewrites only the weak rules using an LLM. Strong, binding rules are kept exactly as written.

## Why it exists

Template rules written with suggestive language (`should`, `try to`, `ideally`) are statistically less likely to be followed by LLMs than binding rules (`must`, `always`, `never`). `GuidanceOptimizer` automates the audit and rewrite, closing this gap without requiring a full template rebuild.

## Import

```python
from mycontext.intelligence import GuidanceOptimizer
```

## The three weakness patterns it targets

| Pattern | Example weak rule | Example rewritten |
|---------|-------------------|-------------------|
| **Suggestive modal** | `"Try to find patterns"` | `"Identify and quantify every pattern — report the metric and its value"` |
| **Vague directive** | `"Be accurate"` | `"Every numeric claim must reference the exact figure from the source data"` |
| **Under-specified** | `"Check data"` | `"Verify completeness of every required field before proceeding"` |

Rules that are already binding (`must`, `always`, `never`, `do not`) are left untouched.

## `audit()` — inspect without rewriting

```python
from mycontext.foundation import Guidance
from mycontext.intelligence import GuidanceOptimizer

guidance = Guidance(
    role="Data analyst",
    rules=[
        "Try to look for patterns",
        "You should mention limitations",
        "Be accurate",
        "Every claim must cite the specific data point that supports it",
    ],
)

opt = GuidanceOptimizer()
audit = opt.audit(guidance)

print(audit.summary())
# Rules: 4 total  |  1 binding  |  3 weak  |  Strength: 28%

for r in audit.rule_audits:
    print(f"  [{r.status}] {r.rule[:60]}  — {r.weakness_type or 'ok'}")
# [WEAK]    Try to look for patterns                    — suggestive_modal
# [WEAK]    You should mention limitations              — suggestive_modal
# [WEAK]    Be accurate                                 — vague_directive
# [BINDING] Every claim must cite the specific data ... — ok
```

`audit()` makes no LLM calls — instant, cost-free.

## `optimize()` — audit + rewrite

```python
opt = GuidanceOptimizer(provider="openai", model="gpt-4o-mini")
result = opt.optimize(guidance)

print(result.summary())
# Rule strength: 28% → 91%  (+63%)  |  3/4 rules rewritten

print(result.optimized_guidance.rules)
# [
#   "Identify and quantify every pattern — report the metric and its value.",
#   "Must explicitly state each data gap: what is absent and what it prevents.",
#   "Every numeric claim must reference the exact figure from the dataset.",
#   "Every claim must cite the specific data point that supports it.",  ← unchanged
# ]
```

## Return types

### `GuidanceAuditResult`

| Attribute | Type | Description |
|-----------|------|-------------|
| `rule_audits` | `list[RuleAudit]` | Per-rule analysis |
| `rule_strength_score` | `float` | Fraction of binding rules (0–1) |
| `weak_count` | `int` | Number of weak rules |
| `binding_count` | `int` | Number of already-binding rules |

### `RuleAudit`

| Attribute | Type | Description |
|-----------|------|-------------|
| `rule` | `str` | Original rule text |
| `status` | `"BINDING" \| "WEAK"` | Classification |
| `weakness_type` | `str \| None` | `"suggestive_modal"`, `"vague_directive"`, `"under_specified"`, or `None` |

### `OptimizedGuidance`

| Attribute | Type | Description |
|-----------|------|-------------|
| `original_guidance` | `Guidance` | Input |
| `optimized_guidance` | `Guidance` | Rewritten output (binding rules kept, weak rules replaced) |
| `audit` | `GuidanceAuditResult` | Audit result |
| `before_score` | `float` | Rule strength before (0–1) |
| `after_score` | `float` | Rule strength after (0–1) |
| `score_delta` | `float` | Improvement |
| `rewrites` | `list[RuleRewrite]` | Per-rule original → rewritten pairs |

## Use with any template

```python
from mycontext.templates.free.analysis import DataAnalyzer
from mycontext.intelligence import GuidanceOptimizer

template = DataAnalyzer()
ctx = template.build_context(dataset_description="Monthly sales by region")

opt = GuidanceOptimizer(provider="openai", model="gpt-4o-mini")
result = opt.optimize(ctx.guidance)

# Use the upgraded guidance in a new context
import dataclasses
upgraded_ctx = dataclasses.replace(ctx, guidance=result.optimized_guidance)
response = upgraded_ctx.execute(provider="openai")
```

## See also

- [PromptArchitect](./prompt-architect) — upgrade raw prompt strings (not `Guidance` objects)
- [Prompt Optimization Workflow](../quality/prompt-optimization-workflow) — end-to-end workflow
- [OutputEvaluator](../quality/output-evaluator) — measure whether stronger rules improve output
