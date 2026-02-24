---
sidebar_position: 4
title: Architecture Decision Records (ADRs)
description: Generate structured, well-reasoned ADRs using DecisionFramework + TradeoffAnalyzer + ConstraintOptimizer. Blueprint-based, reusable across every team.
---

# Architecture Decision Records (ADRs)

**Scenario:** Your team makes architectural decisions constantly — new databases, framework migrations, API design choices. You want consistent, well-reasoned documentation that captures alternatives considered, constraints weighed, and the rationale — not just the conclusion.

**Patterns used:**
- `DecisionFramework` (enterprise) — structured multi-criteria decision analysis
- `TradeoffAnalyzer` (enterprise) — explicit tradeoff mapping across dimensions
- `ConstraintOptimizer` (enterprise) — identifies which constraints are hard vs. negotiable

**Integration:** Blueprint for reusable ADR generation + `to_markdown()` export

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints
from mycontext.templates.enterprise.decision import (
    DecisionFramework,
    TradeoffAnalyzer,
)
from mycontext.templates.enterprise.problem_solving import ConstraintOptimizer
from mycontext.intelligence import TemplateIntegratorAgent, QualityMetrics

# Reusable ADR blueprint — define once, use for every architecture decision
adr_blueprint = Blueprint(
    name="architecture_decision_record",
    description="Generates a complete, structured ADR from a decision statement",
    guidance=Guidance(
        role="Principal software architect with expertise in distributed systems",
        rules=[
            "Evaluate at least 3 alternatives, including the status quo",
            "Make constraints explicit — distinguish hard constraints from preferences",
            "Quantify tradeoffs where possible (latency, cost, complexity, risk)",
            "State the decision clearly at the top, reasoning below",
            "Identify what would need to change to revisit this decision",
        ],
    ),
    directive_template=(
        "Generate an Architecture Decision Record for:\n\n"
        "{decision}\n\n"
        "Team context: {team_context}\n"
        "Hard constraints: {constraints}\n"
        "Alternatives to consider: {alternatives}"
    ),
    constraints=Constraints(
        must_include=[
            "status (proposed/accepted/deprecated/superseded)",
            "context",
            "decision",
            "alternatives considered",
            "consequences",
            "tradeoffs",
        ],
        format_rules=[
            "Use standard ADR format with ## headings",
            "Decision section must be a single, unambiguous sentence",
        ],
    ),
    token_budget=5000,
    optimization="quality",
)


def generate_adr(
    decision: str,
    team_context: str,
    constraints: str,
    alternatives: str,
    save_path: str | None = None,
) -> str:
    # Build context from blueprint
    ctx = adr_blueprint.build(
        decision=decision,
        team_context=team_context,
        constraints=constraints,
        alternatives=alternatives,
    )

    # Score before executing
    score = QualityMetrics().evaluate(ctx)
    print(f"Context quality: {score.overall:.0%}")

    result = ctx.execute(provider="openai", model="gpt-4o")
    adr_text = result.response

    # Also export as markdown for version control
    header = ctx.to_markdown()
    full_doc = f"<!-- Context used to generate this ADR -->\n<!--\n{header}\n-->\n\n{adr_text}"

    if save_path:
        from pathlib import Path
        Path(save_path).write_text(full_doc)
        print(f"Saved to {save_path}")

    return adr_text


# Example: database selection decision
adr = generate_adr(
    decision="Choose between PostgreSQL and MongoDB for our new user events service",
    team_context="10-engineer team, existing PostgreSQL expertise, 50M events/day target",
    constraints="Must support ACID transactions for billing events; max 100ms p99 write latency",
    alternatives="PostgreSQL, MongoDB, Cassandra, TimescaleDB",
    save_path="docs/adr/0042-events-database.md",
)
print(adr)
```

## Deeper Analysis with Template Integration

For high-stakes decisions, use `TemplateIntegratorAgent` to run all three analytical lenses simultaneously and fuse them:

```python
integrator = TemplateIntegratorAgent(provider="openai")
result = integrator.integrate(
    templates=[DecisionFramework, TradeoffAnalyzer, ConstraintOptimizer],
    input_data={
        "decision": "Migrate from monolith to microservices",
        "system": "e-commerce platform, 3M daily users",
        "constraints": "zero downtime, 18-month timeline, 45 engineers",
    },
)
print(result.context.execute(provider="openai").response)
```

## What You Get

A complete ADR with:
- Clear decision statement
- Context and problem framing
- 3+ alternatives with explicit tradeoff analysis
- Hard constraints vs. preferences distinguished
- Consequences (positive and negative)
- Conditions that would trigger revisiting the decision

Drop it directly into your `docs/adr/` folder — it's version-controllable and consistent across every team that uses the blueprint.
