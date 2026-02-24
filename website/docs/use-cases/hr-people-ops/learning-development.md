---
sidebar_position: 5
title: Learning & Development Path Designer
description: Build personalised L&D plans using ScaffoldingFramework + SpacedRepetitionOptimizer + CognitiveLoadManager. AutoGen coaching loop that adapts to the learner.
---

# Learning & Development Path Designer

**Scenario:** Your organisation's L&D programmes are one-size-fits-all. New managers get the same course regardless of their background. Technical upskilling ignores what people already know. You want personalised learning paths that start at the learner's actual level and build progressively.

**Patterns used:**
- `ScaffoldingFramework` (enterprise) — progressive support structure that withdraws as competence grows
- `SpacedRepetitionOptimizer` (enterprise) — schedules learning for maximum retention
- `CognitiveLoadManager` (enterprise) — prevents overload by controlling complexity and pacing

**Integration:** AutoGen coaching conversation loop with adaptive path generation

---

```python
import mycontext
mycontext.activate_license("MC-ENT-YOUR-KEY")

from autogen import AssistantAgent, UserProxyAgent
from mycontext.templates.enterprise.learning import (
    ScaffoldingFramework,
    SpacedRepetitionOptimizer,
    CognitiveLoadManager,
)
from mycontext.intelligence import QualityMetrics, TemplateIntegratorAgent

metrics = QualityMetrics(mode="heuristic")


def design_learning_path(learner: dict, topic: str) -> dict:
    learner_profile = "\n".join(f"{k}: {v}" for k, v in learner.items())

    scaffold_ctx = ScaffoldingFramework().build_context(
        concept=topic,
        learner_level=learner.get("current_level", "beginner"),
        prior_knowledge=learner.get("background", ""),
    )
    spaced_ctx = SpacedRepetitionOptimizer().build_context(
        concept=topic,
        context_section=f"Learner timeline: {learner.get('available_time', '2 hours/week')}",
    )
    load_ctx = CognitiveLoadManager().build_context(
        complex_topic=topic,
        learner_level=learner.get("current_level", "beginner"),
    )

    for name, ctx in [("scaffold", scaffold_ctx), ("spaced", spaced_ctx), ("load", load_ctx)]:
        s = metrics.evaluate(ctx)
        print(f"  {name}: {s.overall:.0%}")

    integrator = TemplateIntegratorAgent(provider="openai")
    result = integrator.integrate(
        templates=[ScaffoldingFramework, SpacedRepetitionOptimizer, CognitiveLoadManager],
        input_data={
            "concept": topic,
            "learner_level": learner.get("current_level", "beginner"),
            "context_section": learner_profile,
        },
    )
    path_context = result.context

    learning_path = path_context.execute(provider="openai", model="gpt-4o").response

    # Build an interactive coaching agent for the learner
    coach = AssistantAgent(
        name="LearningCoach",
        system_message=(
            f"{scaffold_ctx.assemble()}\n\n"
            f"You are coaching {learner.get('name', 'the learner')} on: {topic}\n"
            f"Their background: {learner_profile}\n"
            "Adapt your explanations based on their responses. "
            "Check understanding regularly. Move faster when they demonstrate mastery."
        ),
        llm_config={"config_list": [{"model": "gpt-4o-mini"}]},
    )

    learner_agent = UserProxyAgent(
        name=learner.get("name", "Learner"),
        human_input_mode="ALWAYS",
        code_execution_config=False,
    )

    return {
        "learning_path": learning_path,
        "coach_agent": coach,
        "learner_agent": learner_agent,
    }


def generate_path_only(learner: dict, topic: str) -> str:
    """Generate without interactive coaching — for planning purposes."""
    scaffold_ctx = ScaffoldingFramework().build_context(
        concept=topic,
        learner_level=learner.get("current_level", "beginner"),
        prior_knowledge=learner.get("background", ""),
    )
    scaffold_ctx.knowledge = (
        f"Available time: {learner.get('available_time', '2h/week')}. "
        f"Timeline: {learner.get('timeline', '3 months')}. "
        f"Goal: {learner.get('goal', 'professional competence')}."
    )
    return scaffold_ctx.execute(provider="openai", model="gpt-4o").response


path = generate_path_only(
    learner={
        "name": "Jordan",
        "background": "5 years in customer success, strong Excel user, no coding experience",
        "current_level": "beginner",
        "available_time": "3 hours per week",
        "timeline": "3 months",
        "goal": "Learn Python to automate reporting and basic data analysis",
    },
    topic="Python for data analysis and automation",
)
print(path)
```

## What You Get

A personalised learning path including:

- **Phase structure:** what to learn in each phase (foundation, application, independence), matched to available time
- **Spaced repetition schedule:** when to review each concept to maximise retention (not just linear progression)
- **Cognitive load management:** how many new concepts per session, when to pause and consolidate
- **Checkpoints:** how to verify competence before advancing
- **Resources matched to level:** not generic links — resources appropriate for someone starting at this specific point

For Jordan's case: the path would start with scripting basics (not data science), move to file and API automation, then to pandas for data analysis — because that matches their actual use case and avoids the cognitive overload of starting with data science before programming basics are solid.
