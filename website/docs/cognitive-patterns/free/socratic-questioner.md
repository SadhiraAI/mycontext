---
sidebar_position: 13
title: SocraticQuestioner
description: Apply the Socratic method to deeply examine any statement or belief. Six categories of probing questions that surface assumptions, test evidence, and reveal implications.
---

# SocraticQuestioner

**Category:** Specialized | **Module:** `mycontext.templates.free.specialized`

Applies the classical Socratic method to examine statements, claims, and positions. Generates 2–3 penetrating questions across six categories: clarification, assumptions, evidence, alternative perspectives, implications, and meta-questions. Reveals what's taken for granted and what needs examination.

## When to Use

- Strategic decision examination before committing
- Evaluating business proposals or plans
- Critical thinking training
- Examining AI-generated conclusions
- Reviewing arguments or recommendations
- Philosophy, ethics, or policy analysis
- Challenging your own team's assumptions

## Quick Start

```python
from mycontext.templates.free.specialized import SocraticQuestioner

questioner = SocraticQuestioner()

ctx = questioner.build_context(
    statement="We should implement AI in our hiring process",
    depth="thorough",
)
result = ctx.execute(provider="openai")
print(result.response)
```

## Methods

### `build_context(statement, context="", depth="detailed")`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `statement` | `str` | required | The claim, belief, or position to examine |
| `context` | `str` | `""` | Background context for the statement |
| `depth` | `str` | `"detailed"` | Depth of inquiry |

### `execute(provider, statement, context="", depth="detailed", **kwargs)`

```python
result = questioner.execute(
    provider="openai",
    statement="Remote work is more productive than office work",
    depth="thorough",
)
```

## Six Categories of Socratic Questions

### 1. Clarifying Questions
Ensure the statement is precisely understood before examining it.
- *What exactly do you mean by "implement AI"?*
- *What specific part of hiring — screening, interviewing, selection?*
- *Does "we" mean all roles or specific ones?*

### 2. Probing Assumptions
Surface what's taken for granted without evidence.
- *What are you assuming about AI's ability to judge candidates?*
- *Are you assuming current hiring is unbiased?*
- *What would change if those assumptions were wrong?*

### 3. Probing Reasons and Evidence
Test the factual foundation of the statement.
- *What evidence shows AI improves hiring outcomes?*
- *What data do you have about current hiring quality?*
- *What would change your view on this?*

### 4. Questioning Viewpoints
Surface alternative perspectives.
- *How would a rejected candidate view this?*
- *What would an employment lawyer say?*
- *What does research on algorithmic bias show?*

### 5. Probing Implications
Follow the claim to its consequences.
- *If implemented, what legal obligations arise?*
- *If it works, what happens to human hiring expertise?*
- *What precedent does this set for other AI decisions?*

### 6. Questioning the Question
Examine whether this is even the right question.
- *Why is this the proposed solution? What problem are we solving?*
- *Is "implement AI" the right level of specificity?*
- *What better question should we be asking?*

## Depth Levels

| Depth | Questions per category | Use case |
|-------|----------------------|----------|
| `"basic"` | 1 | Quick assumption check |
| `"detailed"` | 2 | Standard Socratic examination |
| `"thorough"` | 3 | Deep, comprehensive inquiry |

## Examples

### Strategic Decision

```python
result = questioner.execute(
    provider="openai",
    statement="We should pivot from B2B to B2C to access a larger market",
    depth="thorough",
)
```

### Technical Claim

```python
result = questioner.execute(
    provider="anthropic",
    statement="Microservices are always better than monoliths for scalability",
    depth="detailed",
)
```

### Policy Examination

```python
result = questioner.execute(
    provider="gemini",
    statement="Mandatory office attendance 3 days per week will improve team collaboration",
    context="Post-pandemic policy proposal for a 200-person technology company",
    depth="thorough",
)
```

### AI Output Verification

```python
# Use Socratic questioning to critically examine LLM outputs
llm_conclusion = "Your product should target enterprise customers because they have higher LTV"

result = questioner.execute(
    provider="openai",
    statement=llm_conclusion,
    context="Early-stage startup, $0 revenue, B2C product currently",
    depth="detailed",
)
```

## The Synthesis Section

After the six categories, the pattern synthesizes the most important insights the questions collectively reveal — what they expose about the statement's strengths, weaknesses, and blind spots.

## Chaining with Other Patterns

Combine with `RiskAssessor` for complete decision examination:

```python
from mycontext.templates.free.specialized import SocraticQuestioner, RiskAssessor

statement = "We should acquire a competitor to accelerate growth"

# Step 1: Examine assumptions
soc_result = SocraticQuestioner().execute(
    provider="openai",
    statement=statement,
    depth="thorough",
)

# Step 2: Assess risks of proceeding
risk_result = RiskAssessor().execute(
    provider="openai",
    decision=statement,
    context=soc_result.response[:500],
    depth="comprehensive",
)
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(statement, context, depth)` | `Context` | Assembled context |
| `execute(provider, statement, context, depth, **kwargs)` | `ProviderResponse` | Execute questioning |
| `generic_prompt(statement, context_section, depth)` | `str` | Zero-cost prompt string |
