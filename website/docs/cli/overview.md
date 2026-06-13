---
sidebar_position: 1
title: CLI Overview
description: The mycontext command-line interface — list patterns, build and run contexts, export agent skills, and start a local MCP server. Offline-first, your own LLM key.
---

# Command-Line Interface

Installing `mycontext-ai` adds a `mycontext` console script. Every command runs
**locally and offline** — the only command that ever contacts an LLM is
`run --execute`, and only with your own API key.

```bash
mycontext --version
mycontext --help
```

## Commands

| Command | What it does |
|---------|--------------|
| [`mycontext list`](#list) | List all 88 cognitive patterns with descriptions |
| [`mycontext run`](#run) | Build a context from a pattern (optionally execute it) |
| [`mycontext skills export`](./skills-export) | Emit progressive-disclosure `SKILL.md` packages or a plugin |
| [`mycontext mcp`](./local-mcp) | Start the local stdio MCP server |

## `list`

List every pattern and its one-line description:

```bash
mycontext list
```

```text
audience_adapter                  Adapt a message for a specific audience
code_reviewer                     Security, performance, and maintainability review
decision_framework                Structured decision-making with weighted criteria
...
88 cognitive patterns (all open source).
```

## `run`

Build a structured context from any pattern. By default it prints the assembled,
portable prompt — no LLM call, no API key required:

```bash
mycontext run root_cause_analyzer "Why did our API latency spike after the deploy?"
```

### `--generic`

Print the pre-authored generic prompt for the pattern instead of the full
cognitive scaffold (the fastest, zero-dependency option):

```bash
mycontext run decision_framework "Which database should we standardize on?" --generic
```

### `--execute`

Execute the context against an LLM using your own key. Set the provider's API key
in your environment first (e.g. `OPENAI_API_KEY`):

```bash
export OPENAI_API_KEY="sk-..."
mycontext run risk_assessor "Assess the risk of migrating to a monorepo" --execute --provider openai
```

| Flag | Default | Description |
|------|---------|-------------|
| `--generic` | off | Emit the pre-authored generic prompt instead of the full scaffold |
| `--execute` | off | Run the context through an LLM (requires a provider API key) |
| `--provider` | `openai` | LLM provider used with `--execute` |

## Next steps

- [Export patterns as agent skills →](./skills-export)
- [Run the local MCP server →](./local-mcp)
- [Author Requirements-as-Code →](./requirements-as-code)
