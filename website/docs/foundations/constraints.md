---
sidebar_position: 4
title: Constraints
description: Complete reference for the Constraints class — output contract, style guide, must-include, must-not-include, format rules, and guardrails for LLM output.
---

# Constraints

`Constraints` defines the **hard boundaries** of a context — what the output must contain, what it must never contain, how it should be formatted, the output contract, and the tone and style requirements.

Unlike `Guidance` (which shapes identity) and `Directive` (which defines the task), constraints are guardrails: non-negotiable requirements applied to every response.

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
    output_contract: str | None = None,
    style_guide: str | None = None,
    max_length: int | None = None,
    language: str | None = None,
    output_schema: list[dict] | None = None,
)
```

All fields are optional. Use only what you need.

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `output_contract` | `str \| None` | Explicit statement of what the final response must look like — rendered first in section ⑦ |
| `style_guide` | `str \| None` | Tone, voice, and prose style — separate from structural format rules |
| `must_include` | `list[str] \| None` | Elements that must appear in the output |
| `must_not_include` | `list[str] \| None` | Elements that must never appear — rendered as positive redirects for Anthropic/Gemini |
| `format_rules` | `list[str] \| None` | Output formatting and structure requirements |
| `max_length` | `int \| None` | Maximum output length (tokens or chars — interpreted by the LLM) |
| `language` | `str \| None` | Required output language (e.g., `"en"`, `"Spanish"`) |
| `output_schema` | `list[dict] \| None` | Structured field schema for JSON responses — `[{"name": str, "type": str}]` |

### `output_contract` — explicit response shape

`output_contract` is a single binding statement that describes exactly what the response must look like. It renders before all other constraint content in the `## OUTPUT FORMAT` section — the highest-attention position for format instructions.

```python
Constraints(
    output_contract="Return ONLY a ranked bullet list of findings. Each finding: metric name, delta %, magnitude (σ), likely cause. No preamble, no conclusion.",
)
```

**Why it matters.** Format instructions buried in `format_rules` arrive after guard rails and are at lower attention. An `output_contract` at the start of section ⑦ is the last thing the LLM reads before it begins generating — maximising compliance.

### `style_guide` — tone separate from format

`style_guide` captures prose voice, register, and style requirements — distinct from structural `format_rules`. This separation allows you to change tone without changing format, and vice versa.

```python
Constraints(
    style_guide="Formal, third-person, present tense. No hedging language (avoid: probably, might, could be).",
    format_rules=["Use bullet points", "Include a one-line summary at the top"],
)
```

`format_rules` = structure (`"Use bullet points"`). `style_guide` = voice (`"Formal, third-person"`).

### `must_not_include` — positive rendering

`must_not_include` renders differently depending on the target provider. When `provider_hint="anthropic"` or `"gemini"` is set on the Context, items are reframed as positive redirects rather than negative prohibitions:

```
# Generic / OpenAI
Must NOT include:
  - speculation
  - vague language

# Anthropic / Gemini
Exclude the following (use alternatives where needed):
  - Omit speculation.
  - Omit vague language.
```

Anthropic's prompt engineering guide specifically documents that positive framing produces better constraint compliance than bare negation — the model is given a direction, not just a boundary. You do not set this manually; it is handled automatically by `provider_hint` on `Context`.

## Basic Usage

```python
from mycontext import Constraints

constraints = Constraints(
    output_contract="Return ONLY a numbered list of findings. Each finding: severity, affected component, remediation. No prose summary.",
    style_guide="Technical, direct, imperative voice. No hedging.",
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

`constraints.render()` produces the constraints block. The `output_contract` and `style_guide` always appear first:

```
CONSTRAINTS:

Output contract: Return ONLY a numbered list of findings. Each finding: severity, affected component, remediation. No prose summary.

Style: Technical, direct, imperative voice. No hedging.

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

In the assembled `Context` with `research_flow=True`:
- `output_contract` renders in **section ⑦ OUTPUT FORMAT** — just before guard rails
- `style_guide` renders in **section ④ STYLE** — alongside `Guidance.style`
- `must_not_include` and `must_include` render in **section ⑧ GUARD RAILS**

## Common Patterns

### Explicit output contract

```python
Constraints(
    output_contract="Return ONLY valid JSON matching this schema. No prose, no markdown wrapper.",
    output_schema=[
        {"name": "sentiment", "type": "str"},
        {"name": "confidence", "type": "float"},
        {"name": "reasoning", "type": "str"},
    ],
)
```

### Tone control

```python
Constraints(
    style_guide="Executive audience — lead with the so-what, not the how. No technical jargon. Max 3 bullet points per finding.",
    output_contract="Return a 3-part structure: Key Finding (1 sentence), Evidence (2-3 bullets), Recommended Action (1 sentence).",
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
    style_guide="Empathetic, plain language. Avoid clinical jargon without explanation.",
)
```

### Response length control

```python
Constraints(
    output_contract="Response must not exceed 500 words. Lead with the conclusion — no preamble.",
    format_rules=["Use bullet points, not prose paragraphs"],
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
    output_contract="Return findings grouped by severity: Critical → High → Medium → Low. Each finding: one-sentence summary, code snippet, fix.",
    must_include=[
        "security impact assessment",
        "performance implications",
        "suggested refactoring with code diff",
    ],
    must_not_include=[
        "praise for good code — focus only on improvements",
        "style suggestions unrelated to correctness",
    ],
    style_guide="Direct, technical, no preamble. Write as a senior engineer in a PR review.",
)
```

## Using with Context

```python
from mycontext import Context, Guidance, Directive, Constraints

ctx = Context(
    guidance=Guidance(
        role="Financial analyst specializing in startup metrics",
        goal="Surface the revenue story in 3 actionable findings",
        rules=["Base every claim on the provided data", "Flag missing data explicitly"],
    ),
    directive=Directive(
        content="Analyze the monthly recurring revenue trend for Q3–Q4.",
        priority=8,
    ),
    constraints=Constraints(
        output_contract="Return exactly 3 findings in bullet form. Each: metric, value, trend direction, implication.",
        style_guide="Concise, CFO-audience. No financial jargon without explanation.",
        must_include=["MoM growth rate", "churn contribution", "net new MRR"],
        must_not_include=["speculation about future performance", "comparisons to competitors"],
        format_rules=["Use a table for month-by-month breakdown"],
        max_length=800,
    ),
    knowledge="MRR data: Jul $120k, Aug $132k, Sep $145k, Oct $138k, Nov $150k, Dec $167k",
    research_flow=True,
)

result = ctx.execute(provider="openai")
```

## Provider-Aware Rendering

`Constraints.render()` accepts a `provider` parameter that adjusts how `must_not_include` items are phrased. You do not call this directly — set `provider_hint` on the `Context` and it is applied automatically:

```python
ctx = Context(
    constraints=Constraints(must_not_include=["speculation", "vague language"]),
    research_flow=True,
    provider_hint="anthropic",   # → positive reframe applied automatically
)
```

| Provider | `must_not_include` rendering |
|----------|------------------------------|
| `openai` / `generic` | `Must NOT include: speculation` |
| `anthropic` / `gemini` | `Omit speculation.` (positive redirect) |

See [Provider-Aware Assembly →](./research-flow#provider-aware-assembly).

## Combining with `Directive.constraints`

There are two places to express constraints:

| | `Constraints` class | `Directive.constraints` |
|--|--------------------|-----------------------|
| **Scope** | Output-wide guardrails | Task-specific focus |
| **Position in prompt** | Sections ⑦–⑧ | Appended to Directive content |
| **Examples** | `"Return ONLY JSON"`, `"Must include severity"` | `"Focus on SQL injection only"`, `"Ignore CSS files"` |

Use both when needed:

```python
ctx = Context(
    directive=Directive(
        content="Review the authentication module.",
        constraints=["Focus only on auth logic — ignore utility functions"],  # task scope
    ),
    constraints=Constraints(
        output_contract="Return findings as a numbered list. No preamble.",
        must_include=["CVSS score", "PoC exploit outline"],
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

**Use `output_contract` for the shape, `format_rules` for the details.** The contract states the overall form (`"Return ONLY a bullet list"`); format rules specify the internal structure (`"Each bullet: metric, delta, cause"`).

**Separate `style_guide` from `format_rules`.** Style is about voice; format is about structure. Mixing them makes both harder to maintain.

**`must_not_include` = your rejection criteria.** Use this to suppress unwanted content: disclaimers, hedging language, off-topic digressions, speculation, and hallucination-prone patterns.

**Don't over-constrain.** Each constraint narrows the response space. Too many constraints — especially contradictory ones — cause LLMs to produce awkward or incomplete responses. Keep constraints to what's genuinely non-negotiable.

**`max_length` is a soft limit.** Most LLMs treat it as a target rather than a hard cap. Reinforce it with an `output_contract`: `"Response must not exceed 500 words."` is stronger than `max_length=500` alone.

## API Reference

| Method / Field | Type | Description |
|----------------|------|-------------|
| `output_contract` | `str \| None` | Explicit output shape statement — rendered first in section ⑦. |
| `style_guide` | `str \| None` | Tone, voice, and prose style — rendered in section ④ STYLE. |
| `must_include` | `list[str] \| None` | Required output elements — rendered in section ⑧ GUARD RAILS. |
| `must_not_include` | `list[str] \| None` | Forbidden elements — rendered as positive redirects for Anthropic/Gemini. |
| `format_rules` | `list[str] \| None` | Structural format requirements. |
| `output_schema` | `list[dict] \| None` | JSON field schema — `[{"name": str, "type": str}]`. |
| `max_length` | `int \| None` | Maximum length (1 or higher). |
| `language` | `str \| None` | Required response language. |
| `render(provider="generic")` | `str` | Produces the formatted constraints block. `provider` adjusts `must_not_include` phrasing. |

---

**Next:** [Patterns →](./patterns)
