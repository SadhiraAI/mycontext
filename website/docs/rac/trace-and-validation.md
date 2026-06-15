---
sidebar_position: 5
title: Trace & Validation
description: Keep product and technical requirements in sync with trace() — coverage, orphan detection, and code-diff impact analysis — and lint a single spec with validate().
---

# Trace & Validation

Two deterministic, offline checks keep your specs honest:

- **`trace(product, technical, diff=None)`** — does every risky product
  requirement have a technical control behind it? Did anything drift? Does a code
  change touch (or violate) a requirement?
- **`validate(spec)`** — structural best-practice lint on a single spec.

Both are pure functions (no LLM), so they are free and CI-safe.

## `trace()` — keep the two specs in sync

```python
from mycontext.rac import product, technical, trace, format_report

prod = product(INTENT)
tech = technical(product=prod)

report = trace(prod, tech)
print(format_report(report))
```

### Signature

```python
def trace(product: dict, technical: dict, diff: str | None = None) -> dict
```

| Parameter | Type | Meaning |
|-----------|------|---------|
| `product` | `dict` | A product-requirements spec. |
| `technical` | `dict` | A technical-requirements spec. |
| `diff` | `str \| None` | Optional unified diff (e.g. `git diff`) to analyze change impact. |

### What it answers

`trace()` answers three questions:

1. **Coverage** — every risk-bearing product requirement (tasks, safety,
   approval/forbidden actions, gates) should have at least one technical control
   whose `serves:` references it.
2. **Orphans** — does any technical `serves:` reference an ID that doesn't exist
   in the product spec (a typo or a stale link)?
3. **Diff impact** — if a diff is supplied, which requirement IDs does the change
   touch, and does it *violate* anything (e.g. introduce a forbidden tool)?

### The report shape

```python
{
  "status": "in_sync" | "review" | "drift_detected",
  "coverage": {
    "covered": ["T1", "P1", "P4", "A-3", "A-X", "G-1", ...],
    "uncovered": [{"id": "P2", "kind": "safety", "label": "..."}],
    "ratio": 1.0,
  },
  "orphans": [{"served_id": "T9", "location": "guardrails.output"}],
  "diff_impact": [{"file": "handlers/reply.py", "touches": ["A-3"], "forbidden_used": []}],
  "findings": ["[OK] Product and technical requirements are in sync."],
}
```

| `status` | Meaning | Exit code (CLI) |
|----------|---------|-----------------|
| `in_sync` | Full coverage, no findings. | `0` |
| `review` | Warnings only (e.g. orphan references). | `0` |
| `drift_detected` | At least one `[ERROR]` — an uncovered requirement or a forbidden-tool violation. | `1` |

Which product requirements **require coverage**:

| Requirement | Requires coverage? |
|-------------|--------------------|
| Tasks (`T*`) | Yes |
| Safety (`P*`) | Yes |
| Gates (`G*`) | Yes |
| Actions with `policy: approve` or `forbidden` | Yes |
| Actions with `policy: auto` | No |
| Rubrics (`R-*`) | No (referenced, but not coverage-required) |

### Catching drift in a code change

Pass a diff to see which requirements a change touches — and to fail when it
introduces a forbidden action:

```python
diff = """diff --git a/handlers/reply.py b/handlers/reply.py
--- a/handlers/reply.py
+++ b/handlers/reply.py
@@ -1 +1,2 @@
+    delete_record(order_id)
"""

report = trace(prod, tech, diff=diff)
print(report["status"])     # 'drift_detected'
# findings include: "[ERROR] handlers/reply.py: introduces forbidden tool/action 'delete_record' ..."
```

`trace()` keyword-matches added/removed lines against the product spec's tool
names and safety vocabulary. A forbidden tool appearing in the added lines is an
error; touching a known requirement is reported as impact.

### `format_report()` — readable markdown

```python
from mycontext.rac import format_report

print(format_report(report))
```

```markdown
# Requirements trace — IN_SYNC

Coverage: 12/12 risk-bearing requirements served (100%).

## Findings

- [OK] Product and technical requirements are in sync.
```

### On the command line

```bash
mycontext rac trace --product product.yaml --technical technical.yaml
mycontext rac trace --product product.yaml --technical technical.yaml --diff change.diff
mycontext rac trace --product product.yaml --technical technical.yaml --out trace-report.md
```

The command exits `1` when `status == "drift_detected"`, so it works directly as
a CI gate.

## `validate()` — lint a single spec

```python
from mycontext.rac import product, validate

issues = validate(product(INTENT))   # list of "[ERROR] ..." / "[WARN] ..."
```

`validate()` dispatches on `meta.spec_type`, so it lints both product and
technical specs through one entry point. Empty list = clean.

### Validation rules

#### Product specs

| Rule | Severity |
|------|----------|
| At least one task is defined | ERROR |
| Every task references a rubric that exists | ERROR |
| There is an out-of-scope / refusal (`no_draft`) task | WARN |
| Irreversible / money actions are never `policy: auto` | ERROR |
| Every safety entry is a `hard_gate` | ERROR |
| Every safety entry has a machine-checkable `assert` | WARN |
| Safety dataset slices have **no** `dev` split (contamination) | ERROR |
| There is an absolute safety release gate | WARN |
| Blocking open questions are unresolved | ERROR |
| Non-blocking open questions remain | WARN |
| `meta.status` is `ready` while `TODO(OQ-n)` markers remain | ERROR |

#### Technical specs

| Rule | Severity |
|------|----------|
| Required sections present (`architecture`, `guardrails`, `tools`, `cost`, `security`) | ERROR |
| Each guardrail layer (input/processing/output) has a control | WARN |
| Forbidden tools are declared | WARN |
| Blocking / non-blocking open questions | ERROR / WARN |

### On the command line

```bash
mycontext rac validate product.yaml
# OK — no issues found.    (exit 0)
# or prints issues; exit 1 if any [ERROR]
```

## A complete CI gate

```bash
# Fail the build if the spec is unsound or the implementation drifted.
mycontext rac validate product.yaml || exit 1
mycontext rac validate technical.yaml || exit 1
mycontext rac trace --product product.yaml --technical technical.yaml || exit 1
```

## Next

- Render specs for your tools: [Projections →](./projections)
- Auto-fill open questions with your LLM: [Cognitive-pattern grounding →](./cognitive-grounding)
