---
sidebar_position: 4
title: Assessment & Rubric Designer
description: Generate complete assessment suites from learning objectives using RubricDesigner + FormativeAssessmentFramework + SummativeEvaluator. A Blueprint for consistent, rigorous assessment design.
---

# Assessment & Rubric Designer

**Scenario:** A teacher or course designer has a learning objective. They need an assessment that actually measures whether students have achieved it — not just whether they can recall facts. Building a complete rubric with formative checkpoints, summative evaluation, and feedback criteria from scratch takes hours.

**Patterns used:**
- `RubricDesigner` — builds detailed assessment rubrics aligned to learning objectives
- `FormativeAssessmentFramework` — designs checkpoints that reveal learning progress
- `SummativeEvaluator` — creates summative assessments that measure deep understanding

**Integration:** Blueprint — reusable for any subject, level, or assessment type

---

```python
import mycontext

from mycontext.structure import Blueprint
from mycontext.foundation import Guidance, Constraints
from mycontext.templates.enterprise.evaluation import (
    RubricDesigner,
    FormativeAssessmentFramework,
    SummativeEvaluator,
)
from mycontext.intelligence import QualityMetrics, TemplateIntegratorAgent
from pathlib import Path

metrics = QualityMetrics(mode="heuristic")

assessment_blueprint = Blueprint(
    name="assessment_designer",
    guidance=Guidance(
        role="Expert curriculum designer with expertise in evidence-based assessment",
        rules=[
            "Align every assessment component directly to the stated learning objective",
            "Include Bloom's Taxonomy levels: from recall through to evaluation and creation",
            "Formative checks must be low-stakes and frequent",
            "Rubric descriptors must be specific enough that two markers give the same score",
            "Include at least one application task (students apply knowledge to new situation)",
        ],
    ),
    directive_template=(
        "Design a complete assessment suite for:\n\n"
        "Learning objective: {learning_objective}\n"
        "Subject: {subject}\n"
        "Level: {level}\n"
        "Students: {student_description}\n"
        "Assessment format: {format}"
    ),
    constraints=Constraints(
        must_include=[
            "formative check-ins",
            "summative assessment tasks",
            "scoring rubric with descriptors",
            "feedback criteria",
            "model answer or exemplar",
        ],
        format_rules=["Use ## headings for each section", "Rubric as a markdown table"],
    ),
    token_budget=5000,
    optimization="quality",
)


def design_assessment(
    learning_objective: str,
    subject: str,
    level: str,
    student_description: str,
    assessment_format: str = "written + practical",
    save_path: str | None = None,
) -> str:
    # Build blueprint context
    ctx = assessment_blueprint.build(
        learning_objective=learning_objective,
        subject=subject,
        level=level,
        student_description=student_description,
        format=assessment_format,
    )
    score = metrics.evaluate(ctx)
    print(f"Context quality: {score.overall:.0%}")

    # Deep integration: all three patterns fused
    integrator = TemplateIntegratorAgent(provider="openai")
    result = integrator.integrate(
        templates=[RubricDesigner, FormativeAssessmentFramework, SummativeEvaluator],
        input_data={
            "concept": learning_objective,
            "learner_level": level,
            "context_section": f"Subject: {subject}, Students: {student_description}",
        },
    )

    final = result.context.execute(
        provider="openai",
        model="gpt-4o",
    ).response

    if save_path:
        Path(save_path).write_text(f"# Assessment Design\n\n**Objective:** {learning_objective}\n\n{final}")

    return final


assessment = design_assessment(
    learning_objective=(
        "Students will be able to design a normalised relational database schema "
        "from a set of business requirements, justify their design decisions, "
        "and identify trade-offs between normalisation and performance"
    ),
    subject="Database Systems",
    level="Second-year undergraduate",
    student_description="CS students with SQL basics, no prior schema design experience",
    assessment_format="written assignment + database implementation + oral defence",
    save_path="assessments/db-normalisation.md",
)
print(assessment)
```

## What You Get

A complete assessment suite including:

**Formative checkpoints:**
- Week 2: Identify entities and attributes from a plain-English scenario (ungraded quiz)
- Week 3: Draw an ER diagram for a simple case (peer review)
- Week 4: Find normalisation violations in a given schema (in-class exercise)

**Summative assessment:**
- Design task: given business requirements, produce a normalised schema with justification
- Implementation: build the schema in SQL with sample data
- Oral defence: 10-minute Q&A explaining design decisions and trade-offs

**Rubric (excerpt):**

| Criterion | Distinction | Merit | Pass | Fail |
|-----------|-------------|-------|------|------|
| 3NF compliance | All relations in 3NF, no anomalies | Minor deviations, self-corrected | 2NF met, 3NF partially | Below 2NF |
| Justification | Every design choice linked to requirements | Most choices justified | Key choices justified | Minimal justification |
