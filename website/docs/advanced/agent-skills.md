---
sidebar_position: 2
title: Agent Skills
description: Load SKILL.md files, validate parameters, fuse with cognitive patterns, and execute with quality gating. The bridge between the Agent Skills open standard and mycontext.
---

# Agent Skills

Agent Skills are reusable instructions for AI agents, defined as `SKILL.md` files. mycontext can load any SKILL.md, validate its parameters, optionally fuse the skill's content with a cognitive pattern, evaluate quality, and execute — all through `SkillRunner`.

```python
from pathlib import Path
from mycontext.skills import SkillRunner

runner = SkillRunner()
result = runner.run(
    skill_path=Path("./skills/code-review"),
    task="Review for SQL injection vulnerabilities",
    execute=True,
    provider="openai",
    quality_threshold=0.70,
)

print(f"Quality: {result.quality_score.overall:.1%}")
print(result.execution_result.response)
```

## SKILL.md Format

A `SKILL.md` file contains YAML frontmatter and a Markdown body:

```markdown
---
name: Code Security Review
description: Review code for security vulnerabilities with OWASP methodology
license: MIT
compatibility: ">=0.1.0"
input_schema:
  language: str
  focus_areas: str
pattern: code_reviewer
metadata:
  author: "mycontext team"
  version: "1.0.0"
---

## Instructions

Review {language} code focusing on: {focus_areas}

Apply OWASP Top 10 methodology. For each finding:
1. Identify the vulnerability type
2. Assess severity (Critical/High/Medium/Low)
3. Provide a concrete code fix
4. Reference the relevant OWASP category
```

### Frontmatter Fields

| Field | Required | Description |
|-------|---------|-------------|
| `name` | Yes | Human-readable skill name |
| `description` | Yes | What the skill does (used as Guidance role) |
| `license` | No | License identifier |
| `compatibility` | No | Compatible SDK version range |
| `input_schema` | No | Parameter names → types for validation |
| `pattern` | No | mycontext pattern name for fusion (e.g. `code_reviewer`) |
| `allowed-tools` | No | Allowed tools for the agent |
| `metadata` | No | Arbitrary key-value metadata |

### `input_schema` Types

```yaml
input_schema:
  code: str         # String
  line_count: int   # Integer
  score: float      # Float
  is_async: bool    # Boolean
  tags: list        # List
  config: dict      # Dictionary
```

## The `Skill` Class

Load and work with a skill directly:

```python
from pathlib import Path
from mycontext.skills.skill import Skill

skill = Skill.load(Path("./skills/code-review"))

print(skill.name)         # "Code Security Review"
print(skill.description)  # "Review code for security..."
print(skill.pattern)      # "code_reviewer"
print(skill.input_schema) # {"language": str, "focus_areas": str}

# Validate params before running
skill.validate_params({"language": "Python", "focus_areas": "SQL injection"})

# Get full instructions with substitution
text = skill.full_instructions({"language": "Python", "focus_areas": "auth"})

# Convert to Context (no pattern fusion)
ctx = skill.to_context(
    task="Review login.py",
    language="Python",
    focus_areas="authentication",
)

# Convert with references included
ctx = skill.to_context(
    task="Review login.py",
    include_references=True,
    language="Python",
)
```

## Pattern Fusion

When `pattern` is set in the frontmatter, `SkillRunner` fuses the skill's content with the named cognitive pattern. The skill body and task become the pattern's context section; the pattern's cognitive framework wraps everything.

```yaml
# SKILL.md
pattern: code_reviewer
```

```python
runner = SkillRunner()
ctx = runner.build_context(skill, task="Review auth.py", language="Python")

# ctx is now a CodeReviewer context, not a generic skill context
# → Full severity-ranked code review framework applied
# → Skill's specific instructions woven in as context
```

**Why this matters:** Instead of just running the skill instructions as a raw directive, pattern fusion gives you the full analytical methodology of the cognitive pattern — with your skill's specific focus and constraints applied on top.

## `SkillRunner`

The main entry point for running skills:

```python
from mycontext.skills import SkillRunner
from mycontext.intelligence import QualityMetrics

runner = SkillRunner(
    quality_metrics=QualityMetrics(mode="heuristic"),
    log_runs=True,           # Log results for improvement
    log_path=Path("./logs"), # Where to log
)
```

### `runner.run()` — Full Pipeline

```python
result = runner.run(
    skill_path=Path("./skills/security-review"),
    task="Find authentication bypass vulnerabilities",
    execute=True,
    provider="openai",
    quality_threshold=0.65,   # Skip execution if quality < 65%
    # Skill params
    language="Python",
    focus_areas="auth, session management",
    # Provider params
    model="gpt-4o-mini",
    temperature=0,
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skill_path` | `Path` | required | Path to skill directory or SKILL.md |
| `task` | `str \| None` | `None` | Task text (appended to directive) |
| `execute` | `bool` | `False` | Execute the context with an LLM |
| `provider` | `str` | `"openai"` | LLM provider |
| `include_references` | `bool` | `True` | Include `references/` folder in knowledge |
| `quality_threshold` | `float \| None` | `None` | Skip execution if quality below threshold |
| `**params` | | | Skill params + provider kwargs |

**Returns:** `SkillRunResult`

```python
@dataclass
class SkillRunResult:
    context: Context               # The built context
    quality_score: QualityScore    # QualityMetrics result
    execution_result: Any | None   # LLM response (if execute=True)
    skill: Skill | None            # The loaded skill
    metadata: dict                 # skill_path, task
    gated: bool                    # True if skipped due to quality_threshold
```

### `runner.build_context()` — Build Without Executing

```python
ctx = runner.build_context(
    skill=skill,
    task="Find auth vulnerabilities",
    include_references=True,
    language="Python",
)

# Inspect before executing
from mycontext.intelligence import QualityMetrics
score = QualityMetrics().evaluate(ctx)
print(f"Quality: {score.overall:.1%}")

# Execute manually
result = ctx.execute(provider="openai")
```

## Skill Directory Structure

```
skills/
  code-review/
    SKILL.md            ← Required
    README.md           ← Optional documentation
    references/
      owasp-top10.md    ← Automatically included in knowledge
      secure-patterns.md
```

The `references/` directory contents are automatically appended to `context.knowledge` when `include_references=True`.

## Examples

### Security Review with Quality Gate

```python
from pathlib import Path
from mycontext.skills import SkillRunner

runner = SkillRunner(log_runs=True)

result = runner.run(
    skill_path=Path("./skills/security"),
    task=f"Review this code:\n\n```python\n{my_code}\n```",
    execute=True,
    provider="openai",
    quality_threshold=0.70,  # Don't execute poor quality contexts
    language="Python",
    model="gpt-4o-mini",
)

if result.gated:
    print(f"Skipped — quality too low: {result.quality_score.overall:.1%}")
    for issue in result.quality_score.issues:
        print(f"  {issue}")
else:
    print(result.execution_result.response)
```

### Load and Inspect Without Running

```python
from pathlib import Path
from mycontext.skills.skill import Skill
from mycontext.intelligence import QualityMetrics

skill = Skill.load(Path("./skills/data-analysis"))

print(f"Name: {skill.name}")
print(f"Pattern: {skill.pattern}")
print(f"Schema: {skill.input_schema}")

# Build and score without executing
runner = SkillRunner()
ctx = runner.build_context(
    skill=skill,
    task="Analyze Q3 sales data",
    dataset="monthly_sales.csv",
)

metrics = QualityMetrics()
score = metrics.evaluate(ctx)
print(f"Quality: {score.overall:.1%}")
print(metrics.report(score))
```

### Minimal SKILL.md (No Pattern)

```markdown
---
name: Tone Adjuster
description: Rewrite content for a specific tone and audience
input_schema:
  tone: str
  audience: str
---

Rewrite the following content with a {tone} tone, targeting {audience}:

{task}

Preserve all key information while adapting the style appropriately.
```

### Pattern-Fused SKILL.md

```markdown
---
name: Risk-Aware Code Review
description: Security-focused code review with risk scoring
input_schema:
  language: str
pattern: risk_assessor
---

Assess the security risks in this {language} code.

Apply the risk scoring framework to each vulnerability found.
Output a go/no-go recommendation for deployment.
```

## API Reference

### `SkillRunner`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(quality_metrics, log_runs, log_path)` | — | Initialize |
| `load_skill(path)` | `Skill` | Load skill from path |
| `build_context(skill, task, include_references, **params)` | `Context` | Build without executing |
| `run(skill_path, task, execute, provider, ...)` | `SkillRunResult` | Full pipeline |

### `Skill`

| Method | Returns | Description |
|--------|---------|-------------|
| `load(path)` | `Skill` | Load from directory or SKILL.md file |
| `summary()` | `str` | Name + description |
| `full_instructions(**params)` | `str` | Body with template substitution |
| `validate_params(params)` | `None` | Raises ValueError if invalid |
| `to_context(task, include_references, **params)` | `Context` | Build Context (no pattern fusion) |
