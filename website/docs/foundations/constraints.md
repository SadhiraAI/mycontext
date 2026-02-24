---
sidebar_position: 4
title: Constraints
description: Complete reference for the Constraints class — hard limits, must-include requirements, format rules, and guardrails for LLM output.
---

# Constraints

`Constraints` defines the **hard boundaries** of a context — what the output must contain, what it must never contain, how it should be formatted, and limits like maximum length and language.

Unlike guidance (which shapes identity) and directives (which define the task), constraints are guardrails: non-negotiable requirements applied to every response.

## Import

```python
from mycontext import Constraints
# or
from mycontext.foundation import Constraints
```

## Constructor

```python
Constraints(
    must_include: list[str] | None = None,
    must_not_include: list[str] | None = None,
    format_rules: list[str] | None = None,
    max_length: int | None = None,
    language: str | None = None,
)
```

All fields are optional. Use only what you need.

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `must_include` | `list[str] \| None` | Elements that must appear in the output |
| `must_not_include` | `list[str] \| None` | Elements that must never appear |
| `format_rules` | `list[str] \| None` | Output formatting and structure requirements |
| `max_length` | `int \| None` | Maximum output length (tokens or chars — interpreted by the LLM) |
| `language` | `str \| None` | Required output language (e.g., `"en"`, `"Spanish"`) |

## Basic Usage

```python
from mycontext import Constraints

constraints = Constraints(
    must_include=[
        "severity rating (critical/high/medium/low)",
        "affected code snippet",
        "remediation steps with code example",
    ],
    must_not_include=[
        "generic security advice",
        "caveats about not being a licensed security auditor",
    ],
    format_rules=[
        "Use a markdown table for findings summary",
        "Code examples must be in Python",
        "Number all findings",
    ],
    max_length=2000,
    language="en",
)
```

## How It Renders

`constraints.render()` produces the constraints block that's inserted into the assembled context:

```
CONSTRAINTS:

Must include:
  - severity rating (critical/high/medium/low)
  - affected code snippet
  - remediation steps with code example

Must NOT include:
  - generic security advice
  - caveats about not being a licensed security auditor

Format rules:
  - Use a markdown table for findings summary
  - Code examples must be in Python
  - Number all findings

Maximum length: 2000

Language: en
```

In the assembled `Context`, this block appears **after Guidance and before Knowledge** — establishing the output contract early in the system prompt.

## Common Patterns

### Structured output enforcement

```python
Constraints(
    must_include=["executive_summary", "findings (list)", "recommendation", "confidence_score"],
    format_rules=[
        "Respond in valid JSON only",
        "Use the schema: {executive_summary: str, findings: list, recommendation: str, confidence_score: float}",
    ],
)
```

### Content safety

```python
Constraints(
    must_not_include=[
        "specific medical diagnoses",
        "medication dosage recommendations",
        "statements that could be construed as professional medical advice",
    ],
    must_include=["a recommendation to consult a licensed physician"],
)
```

### Response length control

```python
Constraints(
    max_length=500,
    format_rules=["Lead with the conclusion — no preamble", "Use bullet points, not prose paragraphs"],
)
```

### Multi-language output

```python
Constraints(
    language="Spanish",
    must_include=["technical terms in both Spanish and English on first use"],
)
```

### Code review standards

```python
Constraints(
    must_include=[
        "security impact assessment",
        "performance implications",
        "suggested refactoring with code diff",
    ],
    must_not_include=[
        "praise for good code — focus only on improvements",
        "style suggestions unrelated to correctness",
    ],
    format_rules=[
        "Group findings by severity: Critical → High → Medium → Low",
        "Each finding: one-sentence summary, code snippet, fix",
    ],
)
```

## Using with Context

```python
from mycontext import Context, Guidance, Directive, Constraints

ctx = Context(
    guidance=Guidance(
        role="Financial analyst specializing in startup metrics",
        rules=["Base every claim on the provided data", "Flag missing data explicitly"],
    ),
    directive=Directive(
        content="Analyze the monthly recurring revenue trend for Q3–Q4.",
        priority=8,
    ),
    constraints=Constraints(
        must_include=["MoM growth rate", "churn contribution", "net new MRR"],
        must_not_include=["speculation about future performance", "comparisons to competitors"],
        format_rules=["Use a table for month-by-month breakdown", "Summarize in ≤ 3 bullet points"],
        max_length=800,
    ),
    knowledge="MRR data: Jul $120k, Aug $132k, Sep $145k, Oct $138k, Nov $150k, Dec $167k",
)

result = ctx.execute(provider="openai")
```

## Combining with `Directive.constraints`

There are two places to express constraints:

| | `Constraints` class | `Directive.constraints` |
|--|--------------------|-----------------------|
| **Scope** | Output-wide guardrails | Task-specific focus |
| **Position in prompt** | After Guidance, before Knowledge | Appended to Directive content |
| **Examples** | "Must include severity rating", "Respond in JSON" | "Focus on SQL injection only", "Ignore CSS files" |

Use both when needed:

```python
ctx = Context(
    directive=Directive(
        content="Review the authentication module.",
        constraints=["Focus only on auth logic — ignore utility functions"],  # task scope
    ),
    constraints=Constraints(
        must_include=["CVSS score", "PoC exploit outline"],  # output contract
        format_rules=["Respond in markdown with code blocks"],
    ),
)
```

## Integration with CrewAI

`Constraints.must_include` is used to derive `expected_output` when exporting to CrewAI:

```python
crew = ctx.to_crewai()
print(crew["expected_output"])
# → "Output must include: CVSS score, PoC exploit outline"
```

## Best Practices

**`must_include` = your acceptance criteria.** Think of these as the checklist a reviewer would use to approve the output.

**`must_not_include` = your rejection criteria.** Use this to suppress unwanted content: disclaimers, hedging language, off-topic digressions, or hallucination-prone patterns.

**`format_rules` = your output contract.** Be precise. "Use JSON" is weaker than "Respond in valid JSON matching this schema: `{...}`".

**Don't over-constrain.** Each constraint narrows the response space. Too many constraints, especially contradictory ones, cause LLMs to produce awkward or incomplete responses. Keep constraints to what's genuinely non-negotiable.

**`max_length` is a soft limit.** Most LLMs treat it as a target rather than a hard cap. Reinforce it with a format rule: "Response must not exceed 500 words."

## API Reference

| Method / Field | Type | Description |
|----------------|------|-------------|
| `must_include` | `list[str] \| None` | Required output elements. |
| `must_not_include` | `list[str] \| None` | Forbidden output elements. |
| `format_rules` | `list[str] \| None` | Output format requirements. |
| `max_length` | `int \| None` | Maximum length (1 or higher). |
| `language` | `str \| None` | Required response language. |
| `render()` | `str` | Produces the formatted constraints block. |

---

**Next:** [Patterns →](./patterns)
