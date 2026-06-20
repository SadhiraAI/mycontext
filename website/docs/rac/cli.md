---
sidebar_position: 8
title: CLI Reference — mycontext rac
description: Every mycontext rac subcommand — intake, product, technical, analyze, trace, validate, project — with all flags, inputs, outputs, and exit codes.
---

# CLI Reference — `mycontext rac`

Installing `mycontext-ai` adds a `mycontext` console script. The `rac`
subcommand group exposes the full Requirements-as-Code workflow. **Every `rac`
command is LLM-native** — each one contacts a model through *your* API key. Set
your key before running any command:

```bash
export OPENAI_API_KEY="sk-..."          # bash / zsh
$env:OPENAI_API_KEY = "sk-..."          # PowerShell
```

```bash
mycontext rac --help
```

| Subcommand | Purpose |
|------------|---------|
| [`intake`](#intake) | Assess intent → structured brief (Markdown or JSON). |
| [`product`](#product) | Intent → eval-first product requirements YAML. |
| [`technical`](#technical) | Product spec (or intent) → technical requirements YAML. |
| [`analyze`](#analyze) | Render the cognitive-pattern grounding brief. |
| [`trace`](#trace) | Check product/technical coverage + optional code diff. |
| [`validate`](#validate) | Structural contract + LLM quality lint on a spec file. |
| [`project`](#project) | Render a spec to AGENTS.md / CLAUDE.md / Cursor / Spec Kit / Kiro / ADR. |

---

## Common input options

`intake`, `product`, `technical`, and `analyze` accept intent three ways:

| Source | How |
|--------|-----|
| Inline argument | `mycontext rac product "your intent here"` |
| From a file | `mycontext rac product --from intent.txt` |
| From stdin | `echo "your intent" \| mycontext rac product` |

Files may be `.txt` or `.md` — the full file contents are sent to the LLM as
intent text.

All generation commands share these flags:

| Flag | Default | Meaning |
|------|---------|---------|
| `--out PATH` | stdout | Write the result here instead of printing. |
| `--provider NAME` | `openai` | LLM provider (`openai`, `anthropic`, `gemini`). |
| `--model NAME` | provider default | Model name (`gpt-4o`, `claude-opus-4-5`, …). |

---

## `intake`

Assess a raw intent and print a structured **intent brief** — the same analysis
that `product` uses internally to drive spec generation.

```bash
mycontext rac intake "A support bot that drafts billing replies but never sends refunds"
mycontext rac intake --from intent.txt --format json
mycontext rac intake "..." --out brief.md --model gpt-4o
```

| Flag | Default | Meaning |
|------|---------|---------|
| `TEXT` | — | Inline intent text (positional). |
| `--from PATH` | — | Load intent from a `.txt` or `.md` file. |
| `--format {md,json}` | `md` | Output format: `md` for human-readable Markdown, `json` for the raw structured dict. |
| `--out PATH` | stdout | Write the brief here. |
| `--provider NAME` | `openai` | LLM provider. |
| `--model NAME` | provider default | Model name. |

The brief includes: inferred `system_name`, `kind`, `summary`,
`primary_capabilities`, `task_types` (each with freq/risk/handling),
`out_of_scope_categories`, `must_never` lines, `tools_or_actions` candidates,
`stakeholders`, `constraints` (hitl/pii/money), `risks`, `assumptions`, and
`open_questions`.

Use `intake` when you want to inspect or share the analysis step before
committing to spec generation.

**Example output (Markdown):**

```
# Intent Brief — billing-support-bot

**Kind:** agent
**Summary:** An agent that reads billing emails, looks up orders, and drafts
replies. Refunds are always queued for human approval; customer data is never
logged.

## Tasks
| Name | Example | Risk | Handling | Freq |
|------|---------|------|----------|------|
| draft_billing_reply | "Where is my refund?" | medium | draft_plus_approval | ~70% |
| out_of_scope | "Can I speak to a human?" | critical | route_to_human | ~30% |

## Must Never
- Send a refund without human approval
- Log raw customer PII to any external service
…
```

---

## `product`

Generate an eval-first **product requirements** spec from intent. Writes a YAML
file ready for `technical`, `validate`, and `project`.

```bash
# Inline intent → stdout
mycontext rac product "A support bot that drafts billing replies; refunds need approval"

# From a file → named output
mycontext rac product --from intent.txt --out product.yaml

# Choose a larger model for higher quality
mycontext rac product "..." --model gpt-4o --out product.yaml

# Use Anthropic instead
mycontext rac product "..." --provider anthropic --model claude-opus-4-5 --out product.yaml
```

| Flag | Default | Meaning |
|------|---------|---------|
| `TEXT` | — | Inline intent (positional). |
| `--from PATH` | — | Load intent from a `.txt` or `.md` file. |
| `--out PATH` | stdout | Write the YAML spec here. |
| `--provider NAME` | `openai` | LLM provider. |
| `--model NAME` | provider default | Model name. |

After writing the spec, the command prints (to stderr) any open questions and
validation issues, so gaps are always visible:

```
# 2 open question(s) recorded — resolve before trusting this spec:
#   OQ-01: What is the maximum refund amount that can be approved without manager sign-off?
#   OQ-02: Which CRM system holds the order lookup data?
# validation:
#   [WARN] assumptions list is empty.
```

**What the LLM decides:** how many tasks, rubric criteria, actions, safety
requirements, and release gates the intent warrants. The typed-ID grammar
(`T1`, `R-T1.3`, `A-2`, `P1`, `G-1`) is enforced by a Pydantic contract with a
self-repair loop.

---

## `technical`

Generate a **technical requirements** spec. Covers all 24 sections of the Fable
agentic-engineering template in two LLM passes (12 sections each).

```bash
# Rich path — from a saved product spec (full serves-link traceability)
mycontext rac technical --from-product product.yaml --out technical.yaml

# Same, with a larger model
mycontext rac technical --from-product product.yaml --model gpt-4o --out technical.yaml

# Include the frontier layer (fine-tune / RL / computer-use)
mycontext rac technical --from-product product.yaml --frontier --out technical.yaml

# Bootstrap path — from intent only (no product spec yet)
mycontext rac technical "A RAG assistant answers policy questions; never invents." --out technical.yaml

# From a .txt file
mycontext rac technical --from intent.txt --out technical.yaml
```

| Flag | Default | Meaning |
|------|---------|---------|
| `TEXT` | — | Inline intent (positional). Used when `--from-product` is not given. |
| `--from PATH` | — | Load intent from a `.txt` or `.md` file. |
| `--from-product PATH` | — | Derive from a product-requirements YAML. Gives every control a `serves` list of product IDs. **Recommended** for full traceability. |
| `--frontier` | off | Include detailed Tier-3 content (`model_layer_advanced`, `agent_rl`, `frontier_capabilities`). |
| `--out PATH` | stdout | Write the YAML spec here. |
| `--provider NAME` | `openai` | LLM provider. |
| `--model NAME` | provider default | Model name. |

Provide `--from-product`, intent text, or `--from FILE`. Providing none is an
error.

**What the spec covers:**

| Tier | Sections |
|------|----------|
| **Tier 1 — Functional** | `identity`, `ownership`, `architecture`, `autonomy`, `memory`, `guardrails`, `tools` |
| **Tier 1 — Non-functional** | `quality_gates`, `operational_constraints`, `cost`, `deployment`, `observability`, `security`, `failure_behavior` |
| **Tier 2** | `incident_response`, `audit`, `compliance`, `governance`, `promptops`, `caching`, `data_engineering`, `continuous_improvement` |
| **Tier 3** | `model_layer_advanced`, `agent_rl`, `frontier_capabilities`, `lifecycle` |

Sections that genuinely don't apply are present and marked
`not_applicable: true` with a reason — absence is never "decided".

---

## `analyze`

Render the cognitive-pattern grounding brief used internally by `product` and
`technical`. Useful for inspecting what lenses the LLM is applying to your
intent, or for sharing the analysis with stakeholders.

```bash
mycontext rac analyze "Aurora drafts replies to billing emails; refunds need approval" --kind product
mycontext rac analyze --from intent.txt --kind technical --model gpt-4o --out brief.md
```

| Flag | Default | Meaning |
|------|---------|---------|
| `TEXT` | — | Inline intent (positional). |
| `--from PATH` | — | Load intent from a `.txt` or `.md` file. |
| `--kind {product,technical}` | `product` | Which curated pattern set to run. |
| `--out PATH` | stdout | Write the Markdown brief here. |
| `--provider NAME` | `openai` | LLM provider. |
| `--model NAME` | provider default | Model name. |

---

## `trace`

Check that a technical spec covers its product spec. Optionally analyse a code
diff for forbidden-tool use or out-of-scope changes.

**Exits `1` when drift is detected** — wire it into CI.

```bash
# Basic coverage check
mycontext rac trace --product product.yaml --technical technical.yaml

# With a code diff (checks for forbidden tool use, out-of-scope changes)
mycontext rac trace \
  --product product.yaml \
  --technical technical.yaml \
  --diff "$(git diff main...HEAD)"

# From a diff file
mycontext rac trace --product product.yaml --technical technical.yaml --diff changes.patch

# Save the markdown report
mycontext rac trace \
  --product product.yaml \
  --technical technical.yaml \
  --out trace-report.md
```

| Flag | Required | Meaning |
|------|----------|---------|
| `--product PATH` | yes | Product-requirements YAML. |
| `--technical PATH` | yes | Technical-requirements YAML. |
| `--diff PATH` | no | Path to a unified diff file to check for violations. |
| `--out PATH` | no | Write the Markdown report here instead of stdout. |
| `--provider NAME` | `openai` | LLM provider. |
| `--model NAME` | provider default | Model name. |

| Exit code | Meaning |
|-----------|---------|
| `0` | `in_sync` or `review` (warnings only, all requirements covered). |
| `1` | `drift_detected` — an uncovered requirement or forbidden-tool violation was found. |

**What the report covers:**

- **Coverage** — every risk-bearing product requirement (`T*`, `P*`, `A-*`,
  `G-*`) either served by a technical control or listed as uncovered.
- **Orphans** — technical `serves` entries that point to a product ID that
  does not exist (stale link / typo).
- **Diff impact** — files changed, product IDs touched, any forbidden tool
  introduced by the diff.

---

## `validate`

Lint a single spec. Dispatches on `meta.spec_type` to apply the correct rules.
Applies normalization before checking, so a spec generated by an older version
is handled gracefully.

```bash
mycontext rac validate product.yaml
mycontext rac validate technical.yaml
mycontext rac validate product.yaml --model gpt-4o
```

| Flag | Default | Meaning |
|------|---------|---------|
| `PATH` | required | Product or technical YAML spec (positional). |
| `--provider NAME` | `openai` | LLM provider for the quality critique. |
| `--model NAME` | provider default | Model name. |

| Exit code | Meaning |
|-----------|---------|
| `0` | No `[ERROR]` items (warnings are OK). |
| `1` | At least one `[ERROR]` — structural contract violation. |

Two layers of checks:

1. **Structural contract** (mechanical, no LLM): typed-ID grammar, referential
   integrity, mandatory sections, non-empty criteria.
2. **LLM quality critique**: weak rubric anchors, vague criteria, ungated risky
   actions, missing refusal coverage.

Pass `--model` to choose a stronger model for higher-quality critique. The
structural checks are always applied regardless of provider.

---

## `project`

Render a spec into a target file. LLM-native — uses the model to produce
idiomatic output for each target format.

```bash
mycontext rac project product.yaml --to agents-md --out AGENTS.md
mycontext rac project product.yaml --to claude    --out CLAUDE.md
mycontext rac project product.yaml --to cursor    --out .cursor/rules/aurora.mdc
mycontext rac project product.yaml --to spec-kit  --out spec.yaml
mycontext rac project product.yaml --to kiro      --out requirements.md
mycontext rac project technical.yaml --to adr     --out ARCHITECTURE.md
```

| Flag | Required | Meaning |
|------|----------|---------|
| `PATH` | yes | Product or technical YAML spec (positional). |
| `--to TARGET` | yes | One of `agents-md`, `claude`, `cursor`, `spec-kit`, `kiro`, `adr`. |
| `--out PATH` | no | Write here instead of stdout. |
| `--provider NAME` | `openai` | LLM provider. |
| `--model NAME` | provider default | Model name. |

| Target | Output file | Works with |
|--------|------------|------------|
| `agents-md` | `AGENTS.md` — behavioral rules for coding agents | Product spec |
| `claude` | `CLAUDE.md` — Claude Code project instructions | Product spec |
| `cursor` | `.mdc` Cursor rule file | Product spec |
| `spec-kit` | Spec Kit YAML | Product spec |
| `kiro` | EARS-format requirements Markdown | Product spec |
| `adr` | Architecture Decision Record | Technical spec |

---

## Error handling

All commands catch `LLMUnavailable` (missing key) and `RuntimeError` (LLM
returned empty sections after the repair loop) and print a clear error message
to stderr with exit code `1`:

```
Error: mycontext rac is LLM-native and needs a 'openai' key.
Set OPENAI_API_KEY in your environment (or pass --provider/--model
for another provider). No offline/deterministic fallback exists.
```

---

## End-to-end recipe

```bash
export OPENAI_API_KEY="sk-..."

# 1. Assess the intent
mycontext rac intake "Sales follow-up email drafter; reps review before sending" \
  --format md --out brief.md

# 2. Product spec
mycontext rac product --from brief.md --model gpt-4o --out product.yaml

# 3. Technical spec (traceable)
mycontext rac technical --from-product product.yaml --model gpt-4o --out technical.yaml

# 4. Lint both
mycontext rac validate product.yaml   || exit 1
mycontext rac validate technical.yaml || exit 1

# 5. Coverage check
mycontext rac trace \
  --product product.yaml \
  --technical technical.yaml \
  --diff "$(git diff main...HEAD)" || exit 1

# 6. Render for the coding agent
mycontext rac project product.yaml --to agents-md  --out AGENTS.md
mycontext rac project product.yaml --to cursor     --out .cursor/rules/aurora.mdc
mycontext rac project technical.yaml --to adr      --out ARCHITECTURE.md
```

---

## Provider / model cheat sheet

| Provider | Flag | Default model | Notes |
|----------|------|---------------|-------|
| OpenAI | `--provider openai` | `gpt-4o-mini` | Set `OPENAI_API_KEY` |
| Anthropic | `--provider anthropic` | `claude-haiku-3-5` | Set `ANTHROPIC_API_KEY` |
| Gemini | `--provider gemini` | `gemini-1.5-flash` | Set `GEMINI_API_KEY` |

Pass `--model gpt-4o`, `--model claude-opus-4-5`, etc. for higher-quality
generation. The `product` and `technical` commands benefit most from a stronger
model.
