# Agent Skills with mycontext

This folder contains **example Agent Skills** — executable, quality-assured instructions that mycontext can run with optional **pattern fusion** and **semantic selection**.

## What are Agent Skills?

Agent Skills use the open [SKILL.md](https://github.com/cursor/agent-skills) format. mycontext extends it optionally with:

- **`input_schema`** — Typed parameters; the body can use `{topic}`, `{depth}` placeholders.
- **`pattern`** — A mycontext cognitive pattern (e.g. `comparative_analyzer`, `step_by_step_reasoner`) that provides the reasoning structure; the skill body and task fill the content.

## Example: Compare Options

The `compare_options/` skill uses the **comparative_analyzer** pattern:

```python
from pathlib import Path
from mycontext import SkillRunner, improvement_report

runner = SkillRunner()
result = runner.run(
    Path("examples/skills/compare_options"),
    task="REST vs GraphQL for our new API",
    execute=False,  # set True to call the LLM
    topic="REST vs GraphQL",
    depth="detailed",
)

print(f"Quality score: {result.quality_score.overall:.2f}")
if result.gated:
    print(improvement_report(result))
# result.context.assemble() gives the full prompt
```

## Creating your own skill

1. Create a directory (e.g. `my_skill/`) with a **SKILL.md** file.
2. Required frontmatter: `name`, `description`.
3. Optional: `input_schema` (YAML map of param names to types), `pattern` (e.g. `comparative_analyzer`, `step_by_step_reasoner`, `code_reviewer`).
4. Body: Markdown instructions; use `{param_name}` for templating if you defined `input_schema`.

See [AGENT_SKILLS_INTEGRATION_PLAN.md](../../docs/AGENT_SKILLS_INTEGRATION_PLAN.md) for the full implementation plan and API.

## Semantic selection (optional)

With `pip install mycontext[skills]` you can select skills by task:

```python
from pathlib import Path
from mycontext import SkillSelector

sel = SkillSelector(skills_root=Path("examples/skills"))
result = sel.run_best("Compare two database options", execute=False)
# Uses RAG to pick the best skill and runs it
```

## Quality gate and feedback

- **Quality gate:** `runner.run(..., quality_threshold=0.7)` — skips LLM call if context quality is below 0.7.
- **Improvement report:** `improvement_report(result)` — issues, strengths, suggestions.
- **Feedback loop:** `SkillRunner(log_runs=True, log_path=Path("skill_log.jsonl"))` then `skill_health_report(log_path=...)` for aggregate health per skill.
