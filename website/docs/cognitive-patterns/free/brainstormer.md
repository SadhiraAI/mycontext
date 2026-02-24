---
sidebar_position: 6
title: Brainstormer
description: Structured brainstorming with divergent-then-convergent thinking. 15-step facilitation framework with reverse brainstorming, role play ideation, and constraint removal.
---

# Brainstormer

**Category:** Creative | **Module:** `mycontext.templates.free.creative`

Facilitates structured brainstorming using proven divergent-then-convergent techniques. Goes beyond simple idea listing to include reverse brainstorming, role-play ideation, constraint removal, idea clustering, and prioritized selection of top ideas.

## When to Use

- Product feature ideation
- Business model exploration
- Marketing campaign concepts
- Problem-solving under constraints
- Name, title, and positioning brainstorms
- Innovation workshops
- Any creative challenge needing quantity + quality

## Quick Start

```python
from mycontext.templates.free.creative import Brainstormer

brainstormer = Brainstormer()

ctx = brainstormer.build_context(
    topic="Ways to reduce customer churn for our SaaS product",
    goal="Find creative retention strategies that can be tested in Q1",
    constraints=["Budget under $50k", "Must be implementable in 4 weeks"],
)
result = ctx.execute(provider="openai")
print(result.response)
```

## Methods

### `build_context(topic, goal="Generate creative solutions", context=None, constraints=None)`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `topic` | `str` | `""` | The brainstorming topic |
| `goal` | `str` | `"Generate creative solutions"` | What a successful brainstorm produces |
| `context` | `str \| None` | `None` | Background information |
| `constraints` | `list[str] \| None` | `None` | Constraints to work within |

### `execute(provider, topic, goal, context=None, constraints=None, **kwargs)`

```python
result = brainstormer.execute(
    provider="openai",
    topic="New product features for our developer tool",
    goal="10+ concrete feature ideas for our Q2 roadmap",
    constraints=[
        "Must be buildable in 2-week sprints",
        "No new backend infrastructure",
        "Must appeal to senior engineers",
    ],
)
```

## 15-Step Brainstorming Framework

The pattern runs through a comprehensive facilitation structure:

| Step | Technique | Purpose |
|------|-----------|---------|
| 1 | **Warm-up** | Get creative thinking flowing |
| 2 | **Topic Framing** | Define what's in/out of scope |
| 3 | **Ground Rules** | Defer judgment, encourage wild ideas |
| 4 | **Rapid Generation** | 30+ quick-fire ideas |
| 5 | **Build-On Session** | "Yes, and…" extensions of top ideas |
| 6 | **Reverse Brainstorm** | What would make it worse? (then flip) |
| 7 | **Random Stimulus** | Force unexpected connections |
| 8 | **Role Play Ideation** | What would Jobs/a child/a competitor suggest? |
| 9 | **Constraint Removal** | Unlimited resources moonshots → scaled down |
| 10 | **Category Exploration** | Technology, process, people, partnership ideas |
| 11 | **Idea Clustering** | Group related ideas into themes |
| 12 | **Dot Voting** | Prioritize by potential |
| 13 | **Top Ideas Refinement** | Polish the winners with rationale and first steps |
| 14 | **Dark Horses** | Flag unconventional but potentially transformative ideas |
| 15 | **Next Steps** | Immediate actions and follow-up session |

## Examples

### Product Ideation

```python
result = brainstormer.execute(
    provider="openai",
    topic="New monetization models for our free open-source tool",
    goal="5 viable revenue streams to test",
    context="Currently 50k GitHub stars, 2k daily active users, no revenue",
)
```

### Marketing Campaigns

```python
result = brainstormer.execute(
    provider="anthropic",
    topic="Launch campaign for our AI writing assistant",
    goal="10 campaign concept directions with distinct angles",
    constraints=["$20k budget", "Digital channels only", "Launch in 3 weeks"],
)
```

### Team Problem Solving

```python
result = brainstormer.execute(
    provider="gemini",
    topic="How to improve our engineering team's delivery speed",
    goal="Actionable process improvements that don't require headcount",
    context="10-person team, 2-week sprints, 40% time spent on bugs",
)
```

## Constraints vs. No Constraints

:::tip When to set constraints
Constraints are productive in brainstorming — they force creativity within real boundaries. But also include "constraint removal" in the session to discover what's possible before scaling back. The pattern does both.
:::

```python
# With constraints — practical ideas
brainstormer.execute(
    topic="Office redesign",
    constraints=["$10k budget", "No structural changes", "Done in a weekend"],
)

# No constraints — bigger ideas, then scale
brainstormer.execute(
    topic="Office redesign",
    goal="Dream office concepts we could work toward over 3 years",
)
```

## Output Format

The output is an energetic, structured brainstorm document:

```
## 4. RAPID IDEA GENERATION
1. [Idea 1]
2. [Idea 2]
...
30+. [And more]

## 6. REVERSE BRAINSTORM
Bad idea: [Guaranteed failure]
Flipped: → [Creative solution derived from reversal]

## 13. TOP IDEAS REFINEMENT
**Idea #1**: [Memorable Name]
- What it is: [One-line description]
- Why exciting: [Core promise]
- How to test: [Validation approach]
- First step: [This week]
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(topic, goal, context, constraints)` | `Context` | Assembled context |
| `execute(provider, topic, goal, context, constraints, **kwargs)` | `ProviderResponse` | Execute brainstorm |
| `generic_prompt(topic, goal, context_section, constraints)` | `str` | Zero-cost prompt string |
