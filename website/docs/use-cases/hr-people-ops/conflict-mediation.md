---
sidebar_position: 4
title: Conflict & Mediation Support
description: Structure workplace conflict resolution using ConflictResolver + MoralDilemmaResolver + StakeholderMapper. Raw Context builds with a quality gate for sensitive cases.
---

# Conflict & Mediation Support

**Scenario:** A manager or HR partner is mediating a workplace conflict. They need to understand each party's perspective without bias, identify underlying interests rather than stated positions, and guide the conversation toward resolution. Unstructured conversations often make conflicts worse.

**Patterns used:**
- `ConflictResolver` — applies principled negotiation (interests, not positions)
- `MoralDilemmaResolver` (enterprise) — navigates situations where values genuinely conflict
- `StakeholderMapper` — maps each party's interests and what resolution looks like for them

**Integration:** Raw Context builds for separate party preparation + quality-gated synthesis

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from mycontext import Context
from mycontext.foundation import Directive, Guidance, Constraints
from mycontext.templates.free.specialized import ConflictResolver
from mycontext.templates.enterprise.ethical_reasoning import MoralDilemmaResolver
from mycontext.templates.free.planning import StakeholderMapper
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics(mode="heuristic")
QUALITY_GATE = 0.68


def prepare_mediation(conflict: dict) -> dict:
    conflict_brief = "\n".join(f"{k}: {v}" for k, v in conflict.items())

    conflict_ctx = ConflictResolver().build_context(
        conflict=conflict_brief,
        context_section="Apply principled negotiation: separate people from problem, focus on interests not positions",
    )
    dilemma_ctx = MoralDilemmaResolver().build_context(
        conflict=conflict.get("core_tension", conflict_brief),
        context_section="Is there a genuine values conflict? If so, what are the competing values?",
    )
    stakeholder_ctx = StakeholderMapper().build_context(
        project="Workplace conflict resolution",
        objective=f"Resolve: {conflict.get('summary', '')}",
    )
    stakeholder_ctx.knowledge = conflict_brief

    results = {}
    for name, ctx, question in [
        ("analysis", conflict_ctx, "What are the underlying interests of each party? What would genuine resolution look like?"),
        ("values", dilemma_ctx, "Is there a genuine values conflict? How might competing values be reconciled?"),
        ("stakeholders", stakeholder_ctx, "Map each party's position, interests, and what resolution means for them."),
    ]:
        score = metrics.evaluate(ctx)
        print(f"  {name}: {score.overall:.0%}")
        if score.overall < QUALITY_GATE:
            results[name] = f"Quality too low ({score.overall:.0%})"
            continue
        results[name] = ctx.execute(provider="openai").response

    # Build mediator guide
    mediator_ctx = Context(
        guidance=Guidance(
            role="Expert workplace mediator",
            rules=[
                "Do not take sides",
                "Reflect feelings before addressing facts",
                "Ask open questions to surface interests",
                "Look for superordinate goals both parties share",
            ],
        ),
        directive=Directive(content=(
            "Prepare a mediation session guide based on:\n\n"
            + "\n\n".join(
                f"=== {k.upper()} ===\n{v}"
                for k, v in results.items()
                if isinstance(v, str) and len(v) > 50
            )
        )),
        constraints=Constraints(
            must_include=["opening statement", "key questions for each party", "common ground", "resolution options"],
        ),
    )
    guide_score = metrics.evaluate(mediator_ctx)
    if guide_score.overall >= QUALITY_GATE:
        results["mediator_guide"] = mediator_ctx.execute(provider="openai").response

    return results


conflict = {
    "summary": "Two senior engineers in conflict over technical direction",
    "party_a": "Alice (backend lead): wants microservices migration for scalability. Feels expertise is being ignored.",
    "party_b": "Bob (platform engineer): believes monolith is adequate, migration is premature risk. Feels Alice is CV-building.",
    "core_tension": "Architectural philosophy vs. pragmatism, and mutual professional respect",
    "context": "8-person startup, 18 months from Series A. Two public disagreements in planning meetings.",
}

mediation = prepare_mediation(conflict)
print("=== ANALYSIS ===")
print(mediation["analysis"][:500])
print("\n=== MEDIATOR GUIDE ===")
print(mediation.get("mediator_guide", "")[:600])
```

## What You Get

A mediation preparation pack:

- **Conflict analysis:** underlying interests of each party (Alice wants technical credibility and scalable infrastructure; Bob wants stability and no unnecessary risk — these are not incompatible)
- **Values analysis:** whether there is a genuine values conflict and how it might be reconciled
- **Stakeholder map:** what resolution looks like for each party, what they would never accept
- **Mediator guide:** opening statement, diagnostic questions for each party, identified common ground, resolution options

Mediators who prepare this way consistently reach resolution in fewer sessions with better compliance.
