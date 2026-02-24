---
sidebar_position: 2
title: Guidance
description: Complete reference for the Guidance class — defines who the AI is, its role, goal, rules, style, and expertise.
---

# Guidance

`Guidance` defines the **identity** of the AI — its role, objective, behavioral rules, communication style, and areas of expertise. It becomes the system-level prompt that shapes every response.

Think of Guidance as the job description: it tells the LLM who it is, what it is trying to achieve, how it should think, and what standards it should hold itself to.

## Import

```python
from mycontext import Guidance
# or
from mycontext.foundation import Guidance
```

## Constructor

```python
Guidance(
    role: str,                        # required
    goal: str | None = None,
    rules: list[str] = [],
    style: str | None = None,
    expertise: list[str] | None = None,
)
```

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | `str` | **Yes** | The persona or identity the LLM adopts |
| `goal` | `str \| None` | No | The objective — what success looks like for this interaction |
| `rules` | `list[str]` | No | Behavioral rules to follow (numbered in output) |
| `style` | `str \| None` | No | Communication tone and style |
| `expertise` | `list[str] \| None` | No | Specific domains of knowledge |

### `goal` vs `directive`

`goal` belongs in `Guidance` — it defines what the AI is **optimising for** across the whole interaction. `Directive` contains the specific **task** to execute. Think of `goal` as the success criterion and `directive` as the concrete instruction.

```python
Guidance(
    role="Senior data analyst",
    goal="Identify the root cause of the revenue anomaly and give the team one clear action",
)
# directive = Directive("Analyze Q3 revenue data: ...")
```

## Basic Usage

```python
from mycontext import Guidance

guidance = Guidance(
    role="Senior Python developer with 15 years of experience",
    goal="Produce production-ready code with clear reasoning behind every decision",
    rules=[
        "Always consider edge cases and error conditions",
        "Prefer readability and maintainability over cleverness",
        "Cite PEP standards where relevant",
        "Include type hints in all code examples",
    ],
    style="technical but approachable — use plain English alongside code",
    expertise=["Python", "async/await", "API design", "testing", "performance"],
)
```

## How It Renders

`guidance.render()` produces the system prompt text. Given the example above:

```
You are Senior Python developer with 15 years of experience.
Goal: Produce production-ready code with clear reasoning behind every decision
Your areas of expertise include: Python, async/await, API design, testing, performance.

Follow these rules:
1. Always consider edge cases and error conditions
2. Prefer readability and maintainability over cleverness
3. Cite PEP standards where relevant
4. Include type hints in all code examples

Communication style: technical but approachable — use plain English alongside code
```

This rendered string becomes the system message in the assembled `Context`.

When used with `research_flow=True`, `goal` gets its own **## GOAL** section — second position in the assembled prompt, where the LLM's attention is strongest. See [Prompt Assembly →](./research-flow).

## Common Patterns

### Minimal — just a role

```python
guidance = Guidance(role="Expert data scientist")
```

### With explicit goal

```python
guidance = Guidance(
    role="Medical content reviewer",
    goal="Ensure content is accurate, safe, and understandable to a non-specialist audience",
    rules=[
        "Never provide specific medical advice",
        "Always recommend consulting a licensed physician",
        "Cite peer-reviewed sources when possible",
        "Use plain language — avoid unnecessary jargon",
    ],
    style="empathetic and informative",
)
```

### Technical reviewer

```python
guidance = Guidance(
    role="Staff-level software engineer specializing in distributed systems",
    rules=[
        "Flag every single point of failure",
        "Quantify performance trade-offs when possible",
        "Suggest concrete architectural alternatives, not just problems",
    ],
    style="direct and precise",
    expertise=["distributed systems", "Kubernetes", "event-driven architecture", "PostgreSQL"],
)
```

### Customer-facing communicator

```python
guidance = Guidance(
    role="Customer success specialist for a B2B SaaS company",
    rules=[
        "Lead with empathy — acknowledge the customer's frustration first",
        "Offer concrete next steps, never vague reassurances",
        "Escalate issues that cannot be resolved within 2 steps",
    ],
    style="warm, professional, solution-oriented",
)
```

## String Shorthand

When passing guidance to `Context`, you can pass a plain string — it's automatically promoted to `Guidance(role=...)`:

```python
from mycontext import Context

# These are equivalent:
ctx = Context(guidance="Expert security engineer")
ctx = Context(guidance=Guidance(role="Expert security engineer"))
```

Use the full `Guidance` object when you need rules, style, or expertise.

## Combining with Context

```python
from mycontext import Context, Guidance, Directive

ctx = Context(
    guidance=Guidance(
        role="Principal site reliability engineer",
        rules=[
            "Prioritize customer impact over technical elegance",
            "Always include rollback procedures",
            "Express SLO impact in concrete terms (e.g., 0.1% error budget consumed)",
        ],
        style="terse, bullet-pointed, no fluff",
        expertise=["incident response", "Kubernetes", "observability", "SRE practices"],
    ),
    directive=Directive(content="Write a post-incident review for the 3-hour database outage."),
)

result = ctx.execute(provider="openai")
```

## Accessing Fields

```python
print(guidance.role)       # "Senior Python developer with 15 years of experience"
print(guidance.rules)      # ["Always consider edge cases...", ...]
print(guidance.style)      # "technical but approachable..."
print(guidance.expertise)  # ["Python", "async/await", ...]

# Render to string
print(guidance.render())
```

## Best Practices

**Be specific with the role.** Vague roles produce vague behavior.

```python
# Too vague
Guidance(role="an expert")

# Specific — signals seniority, domain, context
Guidance(role="Principal machine learning engineer focused on production ML systems at scale")
```

**Rules are guarantees, not preferences.** Write rules the way you'd write acceptance criteria — concrete and verifiable.

```python
# Preference (weak)
rules=["Try to be thorough"]

# Guarantee (strong)
rules=["Every recommendation must include a concrete implementation example"]
```

**Style shapes tone, not substance.** Use style to control how results are delivered, not what they contain — use rules for that.

```python
style="concise, no preamble, lead with the most important finding"
```

**Keep expertise focused.** 3-6 domains is usually optimal. More expertise signals dilutes the persona.

## API Reference

| Method / Field | Type | Description |
|----------------|------|-------------|
| `role` | `str` | Required. The persona the LLM adopts. |
| `goal` | `str \| None` | The objective — what success looks like. Rendered after `role`. |
| `rules` | `list[str]` | Behavioral rules, rendered as a numbered list. |
| `style` | `str \| None` | Communication tone and style. |
| `expertise` | `list[str] \| None` | Domain expertise areas. |
| `render()` | `str` | Produces the system prompt text. |

---

**Next:** [Directive →](./directive)
