---
sidebar_position: 15
title: ConflictResolver
description: Mediate conflicts systematically. Surface each party's interests, find common ground, and generate compromise, collaboration, and creative resolution options.
---

# ConflictResolver

**Category:** Specialized | **Module:** `mycontext.templates.free.specialized`

Systematic conflict resolution using proven mediation methodology. Analyzes both parties' stated positions and underlying interests, identifies common ground, diagnoses root causes, and generates three types of resolution options: compromise, collaboration, and creative reframing.

## When to Use

- Team disagreements on technical approaches
- Stakeholder conflicts on priorities or resources
- Cross-functional disputes (product vs. engineering, sales vs. product)
- Interpersonal conflicts needing neutral analysis
- Value-based disagreements within organizations
- Negotiation preparation (understand all sides)

## Quick Start

```python
from mycontext.templates.free.specialized import ConflictResolver

resolver = ConflictResolver()

ctx = resolver.build_context(
    conflict="Engineering team wants to rewrite the system from scratch. Product team insists on incremental improvements to ship features faster",
    parties="Engineering team (CTO-backed), Product team (CPO-backed)",
)
result = ctx.execute(provider="openai")
print(result.response)
```

## Methods

### `build_context(conflict, parties, context=None)`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `conflict` | `str` | `""` | Description of the conflict |
| `parties` | `str` | `""` | Who is involved (names, roles, or groups) |
| `context` | `str \| None` | `None` | Organizational context, history, stakes |

### `execute(provider, conflict, parties, context=None, **kwargs)`

```python
result = resolver.execute(
    provider="openai",
    conflict="Sales team committed to a feature that engineering says will take 6 months to build properly",
    parties="Sales team (VP Sales), Engineering team (VP Engineering), Customer (signed contract)",
    context="$500k contract, 3-month delivery timeline promised, feature impacts core architecture",
)
```

## Resolution Framework

### 1. Conflict Analysis

Classifies the conflict type and severity:

| Type | Description | Resolution focus |
|------|-------------|-----------------|
| **Interpersonal** | Between specific individuals | Relationship and communication |
| **Resource** | Competition for limited resources | Allocation and prioritization |
| **Value** | Different fundamental beliefs/principles | Shared values identification |
| **Process** | Disagreement on how to do things | Best practice research |
| **Interest** | Different underlying goals | Win-win solution design |

### 2. Perspective Analysis

Goes beyond stated positions to underlying interests:

```
Engineering team
- Position: "Rewrite the system"
- Interests: "We want to ship features faster and not fear deployments"
- Concerns: "Technical debt is slowing us down by 60%"
- Fears: "We'll never get permission to fix this if not now"

Product team
- Position: "No rewrite, ship features"
- Interests: "We want to stay competitive and retain customers"
- Concerns: "A rewrite could take years and we'd fall behind"
- Fears: "We'll lose market position while engineering is distracted"
```

### 3. Common Ground

Both teams actually want the same outcome (faster, reliable feature shipping) — they disagree on method. This is the foundation for resolution.

### 4. Resolution Options

Three types of resolution are always generated:

| Option Type | Description |
|-------------|-------------|
| **Compromise** | Each side gives something; partial win for both |
| **Collaboration** | Expand the solution space; both get more than compromise |
| **Creative** | Reframe the problem entirely; find a third way |

### 5. Recommended Resolution

The pattern recommends the best option with:
- Rationale for why it's optimal
- Implementation steps
- Success metrics
- Follow-up plan to ensure it sticks

## Examples

### Technical Architecture Conflict

```python
result = resolver.execute(
    provider="openai",
    conflict="Backend team prefers GraphQL API. Frontend team insists on REST because they know it better",
    parties="Backend engineering team, Frontend engineering team",
    context="New product under 6-week deadline, both teams have equal say",
)
```

### Resource Conflict

```python
result = resolver.execute(
    provider="anthropic",
    conflict="Marketing wants dedicated engineering resources for a campaign landing page. Engineering says all capacity is allocated to product roadmap",
    parties="Marketing team, Engineering team",
    context="Q4 campaign, high-priority product launch same quarter, CTO and CMO both escalating to CEO",
)
```

### Stakeholder Priority Conflict

```python
result = resolver.execute(
    provider="gemini",
    conflict="Customer A paid for a custom feature. Customer B has a critical bug that blocks their workflow. Same engineering team can't do both",
    parties="Customer Success (representing both customers), Engineering team",
    context="Both customers are Fortune 500, both threatening churn, 2-person engineering team",
)
```

## Interests vs. Positions

:::tip The key insight in conflict resolution
Most conflicts are about *positions* (what people say they want). Resolution comes from understanding *interests* (why they want it). When you know the underlying interests, you can often find solutions that satisfy both — which no amount of position-based negotiation would reveal.

Example:
- Position: "I want the window open"
- Position: "I want the window closed"
- Interest A: "I'm hot"
- Interest B: "I have a cold"
- Solution: Open the window in the next room — fresh air for A, no draft for B
:::

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(conflict, parties, context)` | `Context` | Assembled context |
| `execute(provider, conflict, parties, context, **kwargs)` | `ProviderResponse` | Execute resolution |
| `generic_prompt(conflict, parties, context_section)` | `str` | Zero-cost prompt string |
