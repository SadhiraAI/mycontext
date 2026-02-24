---
sidebar_position: 3
title: Directive
description: Complete reference for the Directive class — the specific task instruction, its priority, constraints, and tags.
---

# Directive

`Directive` is the specific **task instruction** — the *what* of a context. It carries the content of what the LLM should do, a priority level, optional task-scoped constraints, and organizational tags.

While `Guidance` shapes identity, `Directive` shapes the work. A strong directive is specific, scoped, and unambiguous.

## Import

```python
from mycontext import Directive
# or
from mycontext.foundation import Directive
```

## Constructor

```python
Directive(
    content: str,                          # required
    priority: int = 5,                     # 1–10
    constraints: list[str] | None = None,
    tags: list[str] | None = None,
)
```

## Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `content` | `str` | **Yes** | — | The task instruction text |
| `priority` | `int` | No | `5` | Importance level, 1 (lowest) to 10 (highest) |
| `constraints` | `list[str] \| None` | No | `None` | Task-specific focus constraints |
| `tags` | `list[str] \| None` | No | `None` | Categorization labels |

:::note Directive constraints vs. Constraints class
`Directive.constraints` is a focused list like "Focus on SQL injection" — appended inline to the task instruction.
The separate `Constraints` class covers broader output requirements like must-include elements and format rules.
:::

## Basic Usage

```python
from mycontext import Directive

directive = Directive(
    content="Analyze the Q3 revenue data and identify the top 3 anomalies.",
    priority=8,
    constraints=[
        "Focus on month-over-month changes exceeding ±15%",
        "Cross-reference with marketing spend data",
    ],
    tags=["finance", "analytics", "quarterly-review"],
)
```

## How It Renders

`directive.render()` produces the instruction text:

```
Analyze the Q3 revenue data and identify the top 3 anomalies.
Focus on:
- Focus on month-over-month changes exceeding ±15%
- Cross-reference with marketing spend data
```

This rendered text appears last in the assembled `Context` — after guidance, constraints, and knowledge — so it's the final instruction the LLM reads before responding.

## Priority

Priority is a numeric signal (`1`–`10`) used by the intelligence layer and quality metrics to weigh directive importance. It doesn't directly change LLM behavior — it informs internal routing and scoring.

```python
# High-stakes production task
Directive(content="Write the incident remediation plan.", priority=9)

# Routine task
Directive(content="Summarize the meeting notes.", priority=3)

# Default (no opinion needed)
Directive(content="Translate this paragraph to French.")
# priority defaults to 5
```

## Common Patterns

### Analysis task

```python
Directive(
    content="Compare the three architectural proposals and recommend the most maintainable option.",
    constraints=[
        "Evaluate on: scalability, developer experience, operational cost",
        "Assume a team of 8 engineers with mixed seniority",
    ],
    tags=["architecture", "decision"],
)
```

### Code review

```python
Directive(
    content="Review the payment processing module for security vulnerabilities.",
    priority=10,
    constraints=[
        "Focus on: input validation, authentication checks, error handling",
        "Flag any secrets or credentials in the code",
        "Check for SQL injection and XSS vectors",
    ],
    tags=["security", "code-review"],
)
```

### Content creation

```python
Directive(
    content="Write a product launch announcement for our new API rate limiting feature.",
    constraints=[
        "Target audience: developers who use our REST API",
        "Tone: excited but technical",
        "Length: 300–400 words",
    ],
    tags=["marketing", "product", "api"],
)
```

### Template variable substitution

Directives work with Python format strings when used inside `Pattern.directive_template`:

```python
from mycontext.structure import Pattern
from mycontext.foundation import Guidance

pattern = Pattern(
    name="market_analyst",
    guidance=Guidance(role="Senior market analyst"),
    directive_template="Analyze the {industry} market for {company} targeting {audience}.",
)

ctx = pattern.build_context(
    industry="fintech",
    company="Acme Corp",
    audience="SMBs in Southeast Asia",
)
# Directive content → "Analyze the fintech market for Acme Corp targeting SMBs in Southeast Asia."
```

## String Shorthand

Passing a plain string to `Context(directive=...)` auto-promotes it to `Directive(content=...)`:

```python
from mycontext import Context

# These are equivalent:
ctx = Context(directive="Review this API for auth vulnerabilities.")
ctx = Context(directive=Directive(content="Review this API for auth vulnerabilities."))
```

Use the full `Directive` object when you need priority, constraints, or tags.

## Accessing Fields

```python
print(directive.content)        # "Analyze the Q3 revenue data..."
print(directive.priority)       # 8
print(directive.constraints)    # ["Focus on month-over-month...", ...]
print(directive.tags)           # ["finance", "analytics", "quarterly-review"]

# Render to string
print(directive.render())
```

## Best Practices

**Lead with the action verb.** The first word sets the frame. "Analyze", "Review", "Compare", "Generate", "Explain" — be explicit about what kind of thinking you want.

```python
# Ambiguous
Directive(content="The API authentication system.")

# Clear action
Directive(content="Audit the API authentication system for vulnerabilities.")
```

**Scope the task in the content, not just in constraints.** The content should be self-contained enough to stand alone.

```python
# Too open-ended
Directive(content="Review this.", constraints=["Focus on security", "Check auth"])

# Self-contained
Directive(content="Review the authentication module for security vulnerabilities, focusing on auth logic and input validation.")
```

**Use `constraints` for focus, not for instructions.** Constraints narrow the task — they don't add new requirements. New requirements belong in `content`.

**Tag for searchability.** Tags aren't used by the LLM, but they're useful for logging, filtering, and building skill libraries.

## API Reference

| Method / Field | Type | Description |
|----------------|------|-------------|
| `content` | `str` | Required. The task instruction text. |
| `priority` | `int` | 1–10 priority. Defaults to 5. |
| `constraints` | `list[str] \| None` | Focus constraints, appended to the task text. |
| `tags` | `list[str] \| None` | Organizational labels. |
| `render()` | `str` | Produces the final instruction text. |

---

**Next:** [Constraints →](./constraints)
