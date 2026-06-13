---
sidebar_position: 2
title: Skills Export
description: Export any cognitive pattern as a progressive-disclosure SKILL.md package, or emit a Claude Code / Cowork plugin directory. Fully offline.
---

# Skills Export

`mycontext skills export` turns cognitive patterns into **progressive-disclosure
`SKILL.md` packages** that any agent runtime (Claude Code, Cursor, Cowork, or your
own framework) can load. Because mycontext is fully open source, the exported
skill contains everything needed to run the pattern offline — no server, no key
to call mycontext.

## Export one pattern

```bash
mycontext skills export decision_framework -o ./skills
```

This writes `./skills/decision_framework/SKILL.md` plus a `references/` folder.

## Export all patterns

```bash
mycontext skills export all -o ./skills
```

```text
Exported 88 skills to ./skills
```

## Export a plugin directory

Bundle every skill into a Claude Code / Cowork plugin manifest:

```bash
mycontext skills export all --plugin -o ./plugin
```

```text
Exported plugin directory: ./plugin
```

## What a SKILL.md contains (progressive disclosure)

Each package is organized so an agent only loads what it needs, in tiers:

| Tier | Content | When it loads |
|------|---------|---------------|
| **Tier 1** | YAML frontmatter: `name` + a `description` that includes when to use the pattern | Always in the agent's context |
| **Tier 2** | Markdown body: inputs, output shape, the pre-authored prompt, and an SDK scaffold | When the agent opens the skill |
| **Tier 3** | `references/` — input/output schema and research basis | On demand, only if needed |

A trimmed example:

```markdown
---
name: Decision Framework
description: Structured decision-making with weighted criteria. Use when the question requires choosing between options with weighted criteria evaluation.
---

# Decision Framework

## When to use
Use when the question requires choosing between options...

## Inputs
- `decision` (primary input)
- `options`
- `depth` (default: `comprehensive`)

## Pre-authored prompt
```text
You are an expert decision scientist...
```

## Full cognitive scaffold (mycontext SDK)
```python
from mycontext.skills.pattern_registry import get_pattern

pattern = get_pattern('decision_framework')
context = pattern.build_context(decision="...", options="...")
print(context.assemble())
```
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `target` | required | A pattern name (see `mycontext list`) or `all` |
| `--out` | `./skills` | Output directory |
| `--plugin` | off | Emit a Claude Code / Cowork plugin directory instead of bare skills |
