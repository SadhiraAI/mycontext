---
sidebar_position: 2
title: Performance Review Assistant
description: Structure consistent, fair performance reviews using RubricDesigner + FeedbackComposer + FormativeAssessmentFramework. A Blueprint for every manager in the org.
---

# Performance Review Assistant

**Scenario:** Performance reviews in your organisation are inconsistent. Some managers write detailed, actionable feedback. Others write vague platitudes. The result: reviews don't drive development, don't differentiate performance fairly, and don't hold up under scrutiny. You want every manager using the same structured, rubric-driven approach.

**Patterns used:**
- `RubricDesigner` — designs objective, behavioural criteria for performance dimensions
- `FeedbackComposer` — structures constructive, specific, developmentally useful feedback
- `FormativeAssessmentFramework` — frames the review as a development input, not just a rating

**Integration:** Blueprint — one template, consistent output across the whole organisation

---

```python
import mycontext

from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints
from mycontext.templates.enterprise.evaluation import RubricDesigner, FormativeAssessmentFramework
from mycontext.templates.enterprise.communication import FeedbackComposer
from mycontext.intelligence import QualityMetrics, TemplateIntegratorAgent
from pathlib import Path

metrics = QualityMetrics(mode="heuristic")

review_blueprint = Blueprint(
    name="performance_review",
    guidance=Guidance(
        role="People operations expert and executive coach writing performance reviews",
        rules=[
            "Every strength and development area must include a specific behavioural example",
            "Feedback must be developmentally useful: 'do more of X' not 'be better at X'",
            "Rating must follow directly from evidence — never from gut feel",
            "Development goals must be SMART: specific, measurable, achievable, relevant, time-bound",
            "Tone must be fair and honest — neither artificially positive nor punitive",
        ],
    ),
    directive_template=(
        "Write a performance review for:\n\n"
        "Name: {employee_name}, Role: {role}\n"
        "Review period: {review_period}\n"
        "Manager notes: {manager_notes}\n"
        "Self-assessment: {self_assessment}\n"
        "Key outcomes delivered: {outcomes}\n"
        "Behavioural examples: {examples}"
    ),
    constraints=Constraints(
        must_include=[
            "rating with justification",
            "3+ specific strengths with examples",
            "2+ development areas with specific suggestions",
            "SMART development goals",
            "career conversation starter",
        ],
        format_rules=["## headings for each section", "Rating at the top"],
    ),
    token_budget=3000,
    optimization="quality",
)


def generate_performance_review(review_data: dict, save_path: str | None = None) -> str:
    # Integrate all three patterns first for richer analysis
    integrator = TemplateIntegratorAgent(provider="openai")
    pre_analysis = integrator.integrate(
        templates=[RubricDesigner, FormativeAssessmentFramework, FeedbackComposer],
        input_data={
            "concept": f"Performance review for {review_data['role']}",
            "learner_level": "professional",
            "context_section": f"Manager notes: {review_data['manager_notes'][:500]}",
        },
    )

    ctx = review_blueprint.build(**review_data)
    ctx.knowledge = pre_analysis.context.execute(
        provider="openai", model="gpt-4o-mini"
    ).response[:1000]

    score = metrics.evaluate(ctx)
    print(f"Context quality: {score.overall:.0%}")

    review = ctx.execute(provider="openai", model="gpt-4o").response

    if save_path:
        Path(save_path).write_text(
            f"# Performance Review\n**{review_data['employee_name']} | {review_data['role']}**\n\n{review}"
        )

    return review


review = generate_performance_review(
    review_data={
        "employee_name": "Jordan Lee",
        "role": "Senior Software Engineer",
        "review_period": "H2 2025",
        "manager_notes": (
            "Jordan delivered the payments migration on time, a technically complex project. "
            "Very strong technically. Sometimes doesn't speak up in cross-team meetings even when they have important context. "
            "Mentored two junior engineers effectively. Can be slow to flag blockers."
        ),
        "self_assessment": (
            "I completed the payments migration and am proud of the technical quality. "
            "I want to improve my communication in large group settings and be better at proactive status updates."
        ),
        "outcomes": (
            "Delivered payments migration (Q4). Reduced processing latency 40%. "
            "Mentored 2 juniors. Contributed to 3 on-call rotations."
        ),
        "examples": (
            "Payments migration: proposed and implemented a zero-downtime approach. "
            "Mentoring: regularly pair-programmes with Ana and Ben. "
            "Cross-team meeting (Nov): had important info about API deprecation but didn't share until asked."
        ),
    },
    save_path="reviews/2025-H2/jordan-lee.md",
)
print(review)
```

## What You Get

A complete, fair performance review with:

- **Rating** based directly on evidence, not impression
- **Strengths:** specific behaviours with concrete examples ("During the payments migration, Jordan...")
- **Development areas:** actionable suggestions, not vague labels ("In future cross-team reviews, proactively share X by Y...")
- **SMART goals:** with measurable targets and time bounds
- **Career conversation opener:** a question or prompt to start the development discussion

The Blueprint ensures every manager — regardless of writing skill or natural inclination — produces reviews that meet the same quality bar.
