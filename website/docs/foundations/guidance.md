---
sidebar_position: 2
title: Guidance
description: Complete reference for the Guidance class — defines who the AI is, its role, goal, persona scope, rules, style, and expertise.
---

# Guidance

`Guidance` defines the **identity** of the AI — its role, objective, behavioral rules, communication style, areas of expertise, and the boundaries within which the role applies. It becomes the system-level prompt that shapes every response.

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
    role: str,                          # required
    goal: str | None = None,
    persona_scope: str | None = None,
    rules: list[str] = [],
    style: str | None = None,
    expertise: list[str] | None = None,
)
```

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | `str` | **Yes** | The persona or identity the LLM adopts |
| `goal` | `str \| None` | No | The mission — rendered imperatively to drive completion |
| `persona_scope` | `str \| None` | No | Bounds the role's applicability — prevents scope drift |
| `rules` | `list[str]` | No | Behavioral rules to follow (numbered in output) |
| `style` | `str \| None` | No | Communication tone and style |
| `expertise` | `list[str] \| None` | No | Specific domains of knowledge |

### `goal` — imperative framing

`goal` renders as a mission statement, not a passive description:

```
Your mission: Identify every exploitable vulnerability — accomplish this fully.
```

This imperative framing drives completion rather than acknowledgment. The LLM is given a clear success criterion, not just a label. Declarative descriptions (`"Goal: find vulnerabilities"`) correlate with partial responses; imperative framing correlates with fuller task execution.

### `persona_scope` — bounding the role

`persona_scope` prevents the LLM from applying its role outside its intended domain:

```python
Guidance(
    role="Senior application security engineer",
    persona_scope="Limit review to application-layer code only. Do not assess infrastructure, network, or compliance.",
)
```

Without scope bounding, LLMs expand roles — a "security engineer" will start auditing deployment configs, Kubernetes manifests, and team practices if not constrained. `persona_scope` eliminates that drift.

### `goal` vs `directive`

`goal` belongs in `Guidance` — it defines what the AI is **optimising for** across the whole interaction. `Directive` contains the specific **task** to execute.

```python
Guidance(
    role="Senior data analyst",
    goal="Surface the root cause of the revenue anomaly and give the team one clear action",
)
# directive = Directive("Analyze Q3 revenue data: ...")
```

`goal` = success criterion. `directive` = concrete instruction.

## Basic Usage

```python
from mycontext import Guidance

guidance = Guidance(
    role="Senior Python developer with 15 years of experience",
    goal="Produce production-ready code with clear reasoning behind every decision",
    persona_scope="Limit advice to Python backend code — do not review frontend or infrastructure.",
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

`guidance.render()` produces the system prompt text. In the research flow, `role`, `goal`, `rules`, and `style` each occupy their own dedicated section for maximum clarity:

```
## ROLE

You are Senior Python developer with 15 years of experience.
Scope: Limit advice to Python backend code — do not review frontend or infrastructure.

## GOAL

**Your mission:** Produce production-ready code with clear reasoning behind every decision — accomplish this fully.

## RULES

**You MUST follow these rules at all times:**
  1. Always consider edge cases and error conditions
  2. Prefer readability and maintainability over cleverness
  3. Cite PEP standards where relevant
  4. Include type hints in all code examples

## STYLE

**Tone & voice:** technical but approachable — use plain English alongside code
```

When used outside `research_flow`, `render()` produces a compact single block with all fields inline.

### Provider-aware rendering

`render()` accepts an optional `provider` parameter that adjusts how the role and style are presented to match each provider's documented preferences:

```python
guidance.render(provider="gemini")
# → "You are Senior Python developer with 15 years of experience.
#    You are technical, approachable, precise."
# Gemini responds better to explicit trait adjectives on the role.

guidance.render(provider="anthropic")
# → Standard role + scope — no trait injection (Claude handles style separately)
```

You do not call `render()` directly in most usage — set `provider_hint` on `Context` and `assemble()` handles it automatically. See [Provider-Aware Assembly →](./research-flow#provider-aware-assembly).

## Common Patterns

### Minimal — just a role

```python
guidance = Guidance(role="Expert data scientist")
```

### Mission-driven with scope bound

```python
guidance = Guidance(
    role="Senior revenue analyst with 10 years of FP&A experience",
    goal="Surface every statistically significant anomaly in Q4 revenue",
    persona_scope="Limit analysis to revenue and margin data only.",
    rules=[
        "Back every claim with a specific data point or calculation",
        "Flag outliers above 2 standard deviations explicitly",
        "Separate root causes from symptoms in your findings",
    ],
    style="precise, analytical, direct",
)
```

### High-stakes with verification mandate

```python
guidance = Guidance(
    role="Senior information security engineer",
    goal="Produce a complete and accurate security assessment — no gaps or overclaiming",
    persona_scope="Limit review to application-layer security only.",
    rules=[
        "Every vulnerability must be backed by a specific code location or configuration",
        "Do not flag theoretical risks without evidence in the provided code",
        "State confidence level (high/medium/low) for every finding",
    ],
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

Use the full `Guidance` object when you need `goal`, `persona_scope`, `rules`, `style`, or `expertise`.

## Combining with Context

```python
from mycontext import Context, Guidance, Directive

ctx = Context(
    guidance=Guidance(
        role="Principal site reliability engineer",
        goal="Produce a post-incident review the team can act on immediately",
        persona_scope="Limit scope to the services involved — do not scope-creep into org process.",
        rules=[
            "Prioritize customer impact over technical elegance",
            "Always include rollback procedures",
            "Express SLO impact in concrete terms (e.g., 0.1% error budget consumed)",
        ],
        style="terse, bullet-pointed, no fluff",
        expertise=["incident response", "Kubernetes", "observability", "SRE practices"],
    ),
    directive=Directive(content="Write a post-incident review for the 3-hour database outage."),
    research_flow=True,
)

result = ctx.execute(provider="openai")
```

## Best Practices

**Be specific with the role.** Vague roles produce vague behavior.

```python
# Too vague
Guidance(role="an expert")

# Specific — signals seniority, domain, context
Guidance(role="Principal machine learning engineer focused on production ML systems at scale")
```

**Use `goal` to define completion, not just purpose.** The difference between a passive label and a completion-driving mission statement is in the phrasing — write the goal as something that can be fully accomplished, not just worked toward.

```python
# Passive — describes orientation, not a completable mission
goal="Be helpful with security topics"

# Completion-driving — the LLM knows what done looks like
goal="Identify every exploitable vulnerability and provide a concrete remediation for each"
```

**Use `persona_scope` when the role is broad.** Any role that could plausibly be applied to many domains should have a scope boundary. Without it, LLMs expand into adjacent areas.

```python
# Without scope: "security engineer" might audit infrastructure, team practices, and deployment pipelines
persona_scope="Limit review to application-layer code only."
```

**Rules are guarantees, not preferences.** Write rules the way you'd write acceptance criteria — concrete and verifiable.

```python
# Preference (weak)
rules=["Try to be thorough"]

# Guarantee (strong)
rules=["Every recommendation must include a concrete implementation example"]
```

**Keep expertise focused.** 3-6 domains is usually optimal. More expertise signals dilute the persona.

## API Reference

| Method / Field | Type | Description |
|----------------|------|-------------|
| `role` | `str` | Required. The persona the LLM adopts. |
| `goal` | `str \| None` | The mission — rendered imperatively: "Your mission: X — accomplish this fully." |
| `persona_scope` | `str \| None` | Bounds the role's domain — prevents scope drift. |
| `rules` | `list[str]` | Behavioral rules, rendered as a numbered list. |
| `style` | `str \| None` | Communication tone and style. |
| `expertise` | `list[str] \| None` | Domain expertise areas. |
| `render(provider="generic", include_goal=True, include_rules=True, include_style=True)` | `str` | Produces the system prompt text. `provider` adjusts presentation style. |

---

**Next:** [Directive →](./directive)
