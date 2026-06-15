---
sidebar_position: 8
title: CLI Reference — mycontext rac
description: Every mycontext rac subcommand — product, technical, analyze, trace, validate, project — with all flags, inputs, outputs, and exit codes.
---

# CLI Reference — `mycontext rac`

Installing `mycontext-ai` adds a `mycontext` console script. The `rac` subcommand
group exposes the full Requirements-as-Code workflow. Every command runs
**offline** except `--execute` / `analyze`, which contact an LLM through *your*
key.

```bash
mycontext rac --help
```

| Subcommand | Purpose |
|------------|---------|
| [`product`](#product) | Generate product requirements from intent. |
| [`technical`](#technical) | Generate technical requirements from a product spec or intent. |
| [`analyze`](#analyze) | Render the cognitive-pattern brief that grounds `--execute`. |
| [`trace`](#trace) | Check product/technical coverage (+ optional diff). |
| [`validate`](#validate) | Lint a single spec (product or technical). |
| [`project`](#project) | Render a spec to a target file format. |

## Common input options

`product`, `technical`, and `analyze` accept the intent three ways:

| Input | How |
|-------|-----|
| Inline argument | `mycontext rac product "your intent here"` |
| From a file | `--from intent.txt` |
| From stdin | `echo "your intent" \| mycontext rac product` |

Generation commands share these flags:

| Flag | Default | Meaning |
|------|---------|---------|
| `--out PATH` | stdout | Write the result here instead of printing. |
| `--execute` | off | Use an LLM to answer open questions (your key). |
| `--provider NAME` | `openai` | Provider for `--execute`. |
| `--model NAME` | provider default | Model for `--execute`. |

## `product`

Generate a product-requirements spec from intent. Aliased as `draft`.

```bash
mycontext rac product "Aurora drafts replies to billing emails; refunds need approval." --out product.yaml
mycontext rac product --from intent.txt --execute --model gpt-4o-mini --out product.yaml
mycontext rac product "..." --intake-only          # only print the parsed structured intent
```

| Flag | Meaning |
|------|---------|
| `--intake-only` | Print the parsed [intake](./product-requirements#how-your-intent-is-read-intake) (name, kind, constraints, gaps) and stop. |

After writing the spec, the command prints (to stderr) a summary of open
questions and any validation issues, so a missing-detail list is always visible.

## `technical`

Generate a technical-requirements spec.

```bash
# Rich path — from a saved product spec (full traceability)
mycontext rac technical --from-product product.yaml --out technical.yaml

# Bootstrap path — from intent alone
mycontext rac technical "A RAG assistant answers questions from our wiki; never invent answers."

# Include the frontier layer, and fill with an LLM
mycontext rac technical --from-product product.yaml --frontier --execute --out technical.yaml
```

| Flag | Meaning |
|------|---------|
| `--from-product PATH` | Derive from a product-requirements YAML (richer, traceable). |
| `--frontier` | Include the fine-tune / RL / computer-use layer. |

Provide `--from-product`, or intent text / `--from FILE`. Providing neither is an
error.

## `analyze`

Render the cognitive-pattern brief that grounds `--execute`, as markdown.
**Requires an LLM key.**

```bash
mycontext rac analyze "Aurora drafts replies to billing emails; refunds need approval." --kind product
mycontext rac analyze --from intent.txt --kind technical --model gpt-4o --out brief.md
```

| Flag | Default | Meaning |
|------|---------|---------|
| `--kind {product,technical}` | `product` | Which curated pattern set to run. |
| `--provider NAME` | `openai` | Provider (requires a key). |
| `--model NAME` | provider default | Model. |
| `--out PATH` | stdout | Write the markdown brief here. |

See [Cognitive-pattern grounding](./cognitive-grounding) for what this produces.

## `trace`

Check that a technical spec covers its product spec; optionally analyze a code
diff. **Exits `1` when drift is detected** — wire it into CI.

```bash
mycontext rac trace --product product.yaml --technical technical.yaml
mycontext rac trace --product product.yaml --technical technical.yaml --diff change.diff
mycontext rac trace --product product.yaml --technical technical.yaml --out trace-report.md
```

| Flag | Required | Meaning |
|------|----------|---------|
| `--product PATH` | yes | Product-requirements YAML. |
| `--technical PATH` | yes | Technical-requirements YAML. |
| `--diff PATH` | no | Unified diff to analyze for impact / violations. |
| `--out PATH` | no | Write the markdown report here. |

| Exit code | Meaning |
|-----------|---------|
| `0` | `in_sync` or `review` (warnings only). |
| `1` | `drift_detected` (uncovered requirement or forbidden-tool violation). |

## `validate`

Lint a single spec. Dispatches on `meta.spec_type`.

```bash
mycontext rac validate product.yaml
mycontext rac validate technical.yaml
```

| Exit code | Meaning |
|-----------|---------|
| `0` | No issues. |
| `1` | At least one `[ERROR]` (warnings alone still exit `0`). |

See the [validation rules](./trace-and-validation#validation-rules).

## `project`

Render a spec into a target file. See [Projections](./projections) for every
target.

```bash
mycontext rac project product.yaml   --to agents-md --out AGENTS.md
mycontext rac project product.yaml   --to cursor    --out .cursor/rules/aurora.mdc
mycontext rac project product.yaml   --to kiro      --out requirements.md
mycontext rac project technical.yaml --to adr       --out ARCHITECTURE.md
```

| Flag | Required | Meaning |
|------|----------|---------|
| `--to TARGET` | yes | `agents-md` \| `claude` \| `cursor` \| `spec-kit` \| `kiro` \| `adr`. |
| `--out PATH` | no | Write here instead of stdout. |

## End-to-end recipe

```bash
# 1. Idea -> product spec
mycontext rac product "$INTENT" --out product.yaml

# 2. Product spec -> technical spec (traceable)
mycontext rac technical --from-product product.yaml --out technical.yaml

# 3. Lint both, then prove coverage (any failure stops the build)
mycontext rac validate product.yaml   || exit 1
mycontext rac validate technical.yaml || exit 1
mycontext rac trace --product product.yaml --technical technical.yaml || exit 1

# 4. Render for the coding agent
mycontext rac project product.yaml --to agents-md --out AGENTS.md
```
