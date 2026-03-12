---
sidebar_position: 7
title: CodeReviewer
description: Risk-aware code review using the ORIENT→ANALYZE→ASSESS→RECOMMEND cognitive flow. Focuses on 7 dimensions linters can't catch — deliberately excludes style to eliminate bikeshedding.
---

# CodeReviewer

**Category:** Specialized | **Module:** `mycontext.templates.free.specialized`

Performs risk-aware code reviews using the **ORIENT→ANALYZE→ASSESS→RECOMMEND** cognitive flow from the Code Review as Decision-Making (CRDM) model. Focuses exclusively on the 7 dimensions that linters cannot catch — correctness, security, performance, design, resilience, testing, and maintainability — and deliberately excludes style/formatting to eliminate the bikeshedding that accounts for 85% of low-value review comments.

:::info Research Basis
Based on the CRDM model (2026), Bacchelli & Bird (2013) — *Modern Code Review* (Microsoft Research), Google eng-practices, and Fagan (1976) formal inspection methodology.
:::

## When to Use

- Pull request review
- Security audit
- Pre-production deployment check
- Failure-mode and risk assessment
- Onboarding code quality check
- Legacy code assessment

## Quick Start

```python
from mycontext.templates.free.specialized import CodeReviewer

reviewer = CodeReviewer()

code = """
def fetch_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
"""

result = reviewer.execute(
    provider="openai",
    code=code,
    language="Python",
    focus_areas=["security", "correctness"],
)
print(result.response)
```

## The CRDM Cognitive Flow

The review follows four sequential phases that mirror how senior engineers actually review code:

```
ORIENT       → Understand architecture, intent, and blast radius
    ↓
ANALYZE      → Examine each dimension systematically (no style)
    ↓
ASSESS       → Severity-rank findings (Critical / High / Medium / Low)
    ↓
RECOMMEND    → Concrete fixes with working code examples
```

This prevents the most common failure mode in code review: jumping straight to line-level comments without first understanding what the code is supposed to do.

## Review Dimensions

The 7 dimensions CodeReviewer evaluates — all things linters cannot catch:

| Dimension | What gets reviewed |
|-----------|-------------------|
| **Correctness** | Logic errors, off-by-one, race conditions, type mismatches |
| **Security** | Injection vectors, auth gaps, data exposure, crypto misuse |
| **Performance** | N+1 queries, algorithmic complexity, memory leaks, blocking I/O |
| **Design** | SOLID violations, coupling, cohesion, interface clarity |
| **Resilience** | Error handling, retry logic, timeout coverage, degraded-mode behavior |
| **Testing** | Coverage gaps, missing edge cases, test brittleness |
| **Maintainability** | Complexity, documentation, testability, modularity |

Style, formatting, and naming conventions are **explicitly excluded** — those are for linters and formatters, not reviewers.

## Methods

### `build_context(code, language, context, focus_areas, output_format)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `code` | `str` | `""` | The code to review |
| `language` | `str` | `"Python"` | Programming language |
| `context` | `str \| None` | `None` | Architecture, purpose, constraints |
| `focus_areas` | `list[str] \| None` | All 7 | Which dimensions to prioritize |
| `output_format` | `str` | `"structured"` | Output presentation format |

### `execute(provider, code, language, context, focus_areas, output_format, **kwargs)`

```python
result = reviewer.execute(
    provider="openai",
    code=your_code,
    language="Python",
    context="Payment processing module, PCI-DSS compliance required",
    focus_areas=["security", "resilience"],
)
```

## Output Format Control

Use `output_format` to change how findings are presented without changing what gets analyzed:

```python
# Default: structured sections with severity headers
result = reviewer.execute(provider="openai", code=code, language="Python")

# Action items only — for creating tickets
result = reviewer.execute(
    provider="openai", code=code, language="Python",
    output_format="actionable",
)

# Slide-ready findings for a sprint review
result = reviewer.execute(
    provider="openai", code=code, language="Python",
    output_format="slides",
)

# Raw JSON for CI pipeline integration
result = reviewer.execute(
    provider="openai", code=code, language="Python",
    output_format="json",
)
```

**Available formats:** `structured` (default) · `narrative` · `brief` · `actionable` · `slides` · `email` · `qa` · `checklist` · `json` · `table`

## Severity Framework

Every finding is severity-ranked with a working fix:

### 🔴 Critical — Must Fix Before Merge
Security vulnerabilities, critical bugs, data exposure. Each finding includes: exact location, risk explanation, corrected code.

```
### Security: SQL Injection
- **Location**: `fetch_user()`, line 2 — f-string interpolation
- **Risk**: Attacker can execute arbitrary SQL: `user_id=1; DROP TABLE users`
- **Fix**:
  ```python
  # Before
  query = f"SELECT * FROM users WHERE id = {user_id}"

  # After
  query = "SELECT * FROM users WHERE id = ?"
  return db.execute(query, (user_id,))
  ```
```

### 🟠 High — Should Fix
Performance bottlenecks, missing error handling, design violations with production risk.

### 🟡 Medium — Consider Fixing
Code quality, resilience gaps, testability improvements.

### 🟢 Low — Nice to Have
Minor improvements that won't cause production issues.

### ✅ Strengths
What the code does well — keeps feedback constructive and balanced.

## Examples

### Security + Correctness Audit

```python
code = """
import os
import pickle

def load_user_data(filename):
    with open(f"/user_data/{filename}", 'rb') as f:
        return pickle.load(f)

def execute_command(cmd):
    os.system(cmd)
"""

result = reviewer.execute(
    provider="openai",
    code=code,
    language="Python",
    focus_areas=["security", "correctness"],
)
# Catches: path traversal, arbitrary code execution via pickle,
# and command injection via os.system
```

### Full Review with Architecture Context

```python
result = reviewer.execute(
    provider="openai",
    code=api_handler_code,
    language="Python",
    context="FastAPI endpoint handling user auth and payment processing. PCI-DSS in scope.",
    focus_areas=["security", "resilience", "performance"],
)
```

### Checklist Output for PR Description

```python
result = reviewer.execute(
    provider="openai",
    code=pr_diff,
    language="TypeScript",
    output_format="checklist",
)
# → - [ ] Fix missing null check on user.id (line 24)
# → - [ ] Add retry logic to payment API call (line 67)
# → - [ ] Handle 429 rate-limit response in fetchOrders()
```

### JavaScript XSS Detection

```python
js_code = """
function getUserInput() {
    const input = document.getElementById('userInput').value;
    document.getElementById('output').innerHTML = input;
}
"""

result = reviewer.execute(
    provider="openai",
    code=js_code,
    language="JavaScript",
    focus_areas=["security"],
)
# Catches XSS via direct innerHTML assignment
```

## Generic Prompt Mode

```python
# Zero-cost review — no context assembly, just string substitution
prompt = reviewer.generic_prompt(
    code="def greet(name): return f'Hello {name}'",
    language="Python",
    focus_areas="security, correctness",
)
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(code, language, context, focus_areas, output_format)` | `Context` | Assembled context |
| `execute(provider, code, language, context, focus_areas, output_format, **kwargs)` | `ProviderResponse` | Execute review |
| `generic_prompt(code, language, context_section, focus_areas)` | `str` | Zero-cost prompt string |
