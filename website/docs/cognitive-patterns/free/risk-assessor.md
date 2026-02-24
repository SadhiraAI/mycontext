---
sidebar_position: 8
title: RiskAssessor
description: Systematic risk identification and evaluation across 5 categories — strategic, operational, financial, compliance, and external. Probability × impact scoring with mitigation strategies.
---

# RiskAssessor

**Category:** Specialized | **Module:** `mycontext.templates.free.specialized`

Comprehensive risk assessment using enterprise risk management frameworks. Identifies risks across five categories, scores them by probability × impact, maps interdependencies, develops mitigation strategies, and produces a go/no-go recommendation.

## When to Use

- Before a major business decision or investment
- Project kickoff risk identification
- Product launch preparation
- Vendor or partnership evaluation
- Strategic initiative planning
- Technical architecture review

## Quick Start

```python
from mycontext.templates.free.specialized import RiskAssessor

assessor = RiskAssessor()

ctx = assessor.build_context(
    decision="Launching a new enterprise product line targeting Fortune 500 companies",
    depth="comprehensive",
)
result = ctx.execute(provider="openai")
print(result.response)
```

## Methods

### `build_context(decision, context="", depth="detailed")`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `decision` | `str` | required | The decision, project, or situation to assess |
| `context` | `str` | `""` | Additional context about the situation |
| `depth` | `str` | `"detailed"` | Assessment depth |

### `execute(provider, decision, context="", depth="detailed", **kwargs)`

```python
result = assessor.execute(
    provider="openai",
    decision="Migrating production database from PostgreSQL to MongoDB",
    context="5TB database, 200 microservices dependent, zero downtime required",
    depth="comprehensive",
)
```

## Risk Categories

The pattern systematically identifies risks across five domains:

| Category | Examples |
|----------|---------|
| **Strategic** | Market changes, competitive threats, reputation damage |
| **Operational** | Process failures, resource constraints, technical issues |
| **Financial** | Cost overruns, revenue shortfalls, budget constraints |
| **Compliance/Legal** | Regulatory changes, legal liabilities, compliance failures |
| **External** | Economic factors, political/social changes, natural events |

## Risk Scoring

Each risk is scored using the standard risk matrix:

```
Risk Score = Probability (1-5) × Impact (1-5)

Critical:    15-25 (Immediate action required)
Significant:  8-14 (Should address before proceeding)
Minor:         1-7  (Monitor and document)
```

## Assessment Framework

9-section structured assessment:

1. **Situation Overview** — Context, objectives, stakeholders, success criteria
2. **Risk Identification** — All risks across 5 categories
3. **Risk Analysis** — Per-risk: description, probability, impact, score, triggers, timeframe
4. **Risk Prioritization** — Risk matrix with critical/significant/minor tiers
5. **Risk Interdependencies** — Cascading effects and compounding risks
6. **Mitigation Strategies** — Avoid / Reduce / Transfer / Accept / Contingency for each major risk
7. **Risk-Benefit Analysis** — Expected value, risk tolerance, alternative profiles
8. **Monitoring Plan** — Key Risk Indicators (KRIs), review frequency, escalation procedures
9. **Risk Summary** — Top 3–5 risks, overall level, go/no-go recommendation

## Depth Levels

| Depth | Use case | Coverage |
|-------|----------|---------|
| `"basic"` | Quick screen before small decisions | 5-section lightweight |
| `"detailed"` | Standard project assessment | Full 9-section analysis |
| `"comprehensive"` | Major decisions, board-level | Deep interdependency mapping + scenario analysis |

## Examples

### Technology Decision

```python
result = assessor.execute(
    provider="openai",
    decision="Replacing our monolith with microservices architecture",
    context="Legacy PHP app, 15-year-old codebase, 3M users, 12 engineers",
    depth="comprehensive",
)
```

### Business Expansion

```python
result = assessor.execute(
    provider="anthropic",
    decision="Opening an engineering office in a new country",
    context="UK team of 50, considering Poland or India, budget $2M/year",
    depth="detailed",
)
```

### Product Launch Risk

```python
result = assessor.execute(
    provider="gemini",
    decision="Launching AI-powered feature requiring user data processing",
    context="GDPR/CCPA compliance required, EU and US users, launch in 8 weeks",
    depth="comprehensive",
)
```

## Mitigation Strategies

For each high-risk item, the pattern evaluates four strategies:

| Strategy | Description | When to use |
|----------|-------------|-------------|
| **Avoid** | Eliminate the risk entirely (change approach) | When risk score is Critical and mitigation is costly |
| **Reduce** | Lower probability or impact | Most common — add safeguards |
| **Transfer** | Insurance, contracts, SLAs, partnerships | When risk is financial or legal |
| **Accept** | Document and proceed | When risk is Low or cost of mitigation exceeds benefit |
| **Contingency** | Backup plan if risk materializes | For risks that can't be avoided but are manageable |

## Output: Go/No-Go Recommendation

Every assessment concludes with a clear recommendation:

```
## RISK SUMMARY

**Overall Risk Level**: High

**Top 3 Risks**:
1. Data migration failure (Score: 20/25) — Zero-downtime constraint conflicts with scope
2. Team capability gap (Score: 15/25) — No MongoDB expertise in team
3. Downstream service disruption (Score: 15/25) — 200 dependent microservices

**Recommendation**: CONDITIONAL GO
- Proceed only after: (1) Proof-of-concept with non-critical data, (2) MongoDB training
  completed, (3) Parallel-run period with rollback capability defined
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(decision, context, depth)` | `Context` | Assembled context |
| `execute(provider, decision, context, depth, **kwargs)` | `ProviderResponse` | Execute assessment |
| `generic_prompt(decision, context_section, depth)` | `str` | Zero-cost prompt string |
