---
sidebar_position: 10
title: StakeholderMapper
description: Identify, profile, and map all project stakeholders using the power-interest matrix. Build engagement strategies, communication plans, and influence maps.
---

# StakeholderMapper

**Category:** Planning | **Module:** `mycontext.templates.free.planning`

Comprehensively maps all stakeholders for a project or initiative — including hidden ones. Profiles each by power and interest, positions them on a power-interest matrix, maps influence relationships, and produces tailored engagement strategies and a communication plan.

## When to Use

- Before launching a major initiative or project
- Organizational change management
- Product launch stakeholder alignment
- Fundraising or partnership development
- Policy or process change management
- Any situation with multiple parties with different interests

## Quick Start

```python
from mycontext.templates.free.planning import StakeholderMapper

mapper = StakeholderMapper()

ctx = mapper.build_context(
    project="Implement company-wide AI tools policy",
    context="B2B tech company, 500 employees, leadership is divided on AI adoption",
)
result = ctx.execute(provider="openai")
print(result.response)
```

## Methods

### `build_context(project, context=None)`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `project` | `str` | `""` | The project or initiative to map stakeholders for |
| `context` | `str \| None` | `None` | Organizational context, known dynamics |

### `execute(provider, project, context=None, **kwargs)`

```python
result = mapper.execute(
    provider="openai",
    project="Launch new enterprise tier product",
    context="B2B SaaS, current product is SMB-focused, CEO championing enterprise push",
)
```

## Power-Interest Matrix

The core output is a power-interest matrix with four quadrants and tailored engagement strategies for each:

```
                    HIGH Interest
                         ▲
                         │
    Keep Satisfied  ─────┼───────── Manage Closely
    (High Power,         │          (High Power,
     Low Interest)       │           High Interest)
                         │
LOW ◄────────────────────┼────────────────────► HIGH
Power                    │                      Power
                         │
    Monitor         ─────┼───────── Keep Informed
    (Low Power,          │          (Low Power,
     Low Interest)       │           High Interest)
                         │
                    LOW Interest
```

| Quadrant | Strategy | Engagement frequency |
|----------|----------|---------------------|
| **Manage Closely** | Involve in decisions, frequent updates | Weekly or more |
| **Keep Satisfied** | Regular updates, no surprises | Bi-weekly |
| **Keep Informed** | Regular communication, gather feedback | Monthly |
| **Monitor** | Minimal effort, situational awareness | Quarterly |

## 10-Section Analysis

1. **Stakeholder Identification** — Primary (directly affected), secondary (indirectly affected), and hidden stakeholders
2. **Stakeholder Profiles** — For each key stakeholder: role, interest level, power level, current stance, wants, fears, influence mechanisms
3. **Power-Interest Matrix** — Classified placement with engagement strategy per quadrant
4. **Needs & Concerns** — What each group requires and how to address their top concerns
5. **Influence Mapping** — Who influences whom, potential coalitions, blockers
6. **Engagement Strategies** — Tailored approach for supporters, neutrals, and opponents
7. **Communication Plan** — Table with stakeholder, message, channel, frequency, and owner
8. **Risk Management** — Stakeholder risks with likelihood, impact, and mitigation
9. **Success Metrics** — How to measure engagement effectiveness
10. **Action Plan** — Week 1, Month 1, and ongoing actions

## Examples

### Product Launch

```python
result = mapper.execute(
    provider="openai",
    project="Launch AI-powered customer service platform",
    context="Replaces 40% of current support workflow, affecting 200 support agents",
)
```

### Technical Migration

```python
result = mapper.execute(
    provider="anthropic",
    project="Migrate from on-premise to cloud infrastructure",
    context="Healthcare company, HIPAA compliance critical, CTO is skeptic",
)
```

### Organizational Change

```python
result = mapper.execute(
    provider="gemini",
    project="Restructure engineering organization into product teams",
    context="50-person eng team, currently functional structure (FE/BE/Data/DevOps)",
)
```

## Hidden Stakeholders

:::tip Don't miss hidden stakeholders
The pattern explicitly prompts for hidden and indirect stakeholders — people who can affect the outcome but aren't obviously connected. Common hidden stakeholders include:
- Compliance and legal teams (often blockers)
- IT security (approval bottlenecks)
- Finance (budget gatekeepers)
- Future users who aren't in planning discussions
- External regulators and auditors
:::

## Influence Mapping

Beyond the matrix, the pattern maps influence chains:

```
CEO (High Power) → Board (High Power)
Engineering Leads (Medium) → Engineers (High Interest)
Legal Team (High Power) → Product Team ← Finance (High Power)

Potential blocker: CISO — can halt AI tool rollout
Strategy: Schedule 1:1 early, involve in security review
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(project, context)` | `Context` | Assembled context |
| `execute(provider, project, context, **kwargs)` | `ProviderResponse` | Execute mapping |
| `generic_prompt(project, context_section)` | `str` | Zero-cost prompt string |
