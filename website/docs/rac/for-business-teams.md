---
sidebar_position: 2
title: For Business Teams (No Code Required)
description: A plain-language, end-to-end walkthrough of Requirements-as-Code for product owners, business analysts, and infrastructure teams — plus a glossary of every term.
---

# For Business Teams

This page is for **product owners, business analysts, project managers, and
infrastructure leads** who want to use Requirements-as-Code without writing
Python. It walks through a real scenario end to end and explains every term in
plain language.

:::tip You only need two things
1. A paragraph describing the AI system you want.
2. The `mycontext` command line (one `pip install mycontext-ai`), **or** a
   teammate who can paste a few lines of Python.

No API key is required for the default, offline workflow.
:::

## The problem RaC solves

When a team decides to build an AI assistant or agent, the hardest part is
usually not the code — it is **agreeing on what "done" and "safe" mean**:

- What exactly should it handle, and what should it refuse?
- How will we *grade* a good answer versus a bad one?
- Which actions are dangerous (sending money, deleting data) and need a human?
- What must it *never* do, and how would we test that?
- When are we allowed to ship?

RaC captures all of this in a structured document that everyone — product,
engineering, risk — can read and sign off on. It writes the first draft for you
and flags the questions you still need to answer.

## Step 1 — Describe the system in plain English

Write one paragraph. Mention the system's **name**, what it **does**, any actions
that need **approval**, and what success looks like (especially what must **never**
happen). Example:

> Brightcart support gets ~2,000 emails/day. We want **Aurora**: an agent that
> reads each email, looks up the order, and drafts (eventually sends) a reply —
> **refunds require human approval**. Success means faster replies **without**
> wrong refunds, leaked customer data, or brand-damaging replies.

RaC reads this the way a sharp analyst would. From that one paragraph it detects:

- the **name** (Aurora),
- that money actions exist and need **human approval** (the refund clause),
- the **hard "never" lines** (wrong refunds, data leaks, brand damage),
- the **volume** (~2,000/day, which drives how big the test sets should be).

Anything it cannot infer is turned into an **open question** rather than a guess.

## Step 2 — Generate the product requirements

On the command line:

```bash
mycontext rac product "Brightcart support gets ~2,000 emails/day. We want Aurora: an agent that reads each email, looks up the order, and drafts (eventually sends) a reply — refunds require human approval. Success means faster replies without wrong refunds, leaked customer data, or brand-damaging replies." --out product.yaml
```

This writes `product.yaml`. It is a **complete framework**: every section is
filled in, and the things you still need to decide are listed at the bottom as
open questions. You will see a summary like:

```
# 15 open question(s) recorded — resolve before trusting this spec:
#   (blocking) OQ-03: Name the specific out-of-scope categories ...
#   OQ-01: What is the cost budget per task (USD)?
#   ...
```

### What the product spec contains

Open `product.yaml` and you will find these sections (explained fully in
[Product requirements](./product-requirements)):

| Section | In plain language |
|---------|-------------------|
| `meta` | The system's name, intent, status, and a review checklist. |
| `tasks` | Every kind of request the system handles, each with a risk level — **including a mandatory "out-of-scope → route to a human" row**. |
| `rubrics` | The scorecard for each task: the specific criteria that make an answer "good." |
| `actions` | What the system is allowed to *do* (look up, draft, send, refund) and which actions need approval or are forbidden. |
| `safety` | A pre-mortem: the bad outcomes that must never happen, each with a test. |
| `datasets` | How many real examples to collect to test each task. |
| `baselines` | Reminders to measure the human/no-tool baseline so you can prove the agent is worth it. |
| `gates` | The release gates — the bar the system must clear before shipping. |
| `monitoring` | What to watch in production (drift, runaway cost, approval rates). |
| `open_questions` | Everything RaC could not infer, with stable IDs (`OQ-01`, ...). |

### Open questions and `TODO(OQ-n)` markers

Wherever a real value is missing, RaC writes a marker like `TODO(OQ-06)` directly
in the spec and adds a matching entry to `open_questions`. **Blocking** questions
(marked `blocking: true`) are the ones you must answer before trusting the spec;
the rest are nice-to-haves. This is how RaC stays honest — it never invents a
refund limit or a safety threshold.

## Step 3 — Generate the technical requirements

Hand the product spec to the technical generator:

```bash
mycontext rac technical --from-product product.yaml --out technical.yaml
```

`technical.yaml` describes **how** the system is built: its architecture,
guardrails (e.g. "treat user text as data, never instructions"), tool
permissions, cost ceilings, rollout plan, observability, and security controls.

The important part: **every technical control is linked back to a product
requirement** via a `serves:` field. For example, a guardrail that blocks data
leaks will list the safety requirement ID (`P2`) it implements. This is what makes
the next step possible.

## Step 4 — Prove the two specs agree

```bash
mycontext rac trace --product product.yaml --technical technical.yaml
```

This prints a coverage report: the percentage of risky product requirements that
have at least one technical control serving them, plus any problems:

- **Uncovered** requirement → a risky task/safety line/gate with no control.
- **Orphan** reference → a technical control pointing at a requirement that
  doesn't exist (a typo or a stale link).

If anything risk-bearing is uncovered, the command exits with a non-zero code, so
you can wire it into CI as a gate. You can also pass a code change (a *diff*) to
see which requirements a change touches and whether it introduces a forbidden
action — see [Trace & validation](./trace-and-validation).

## Step 5 — Hand the spec to your tools

Your coding agents and spec tools each want a different file. RaC renders the
same spec into any of them:

```bash
mycontext rac project product.yaml --to agents-md  --out AGENTS.md
mycontext rac project product.yaml --to cursor      --out .cursor/rules/aurora.mdc
mycontext rac project product.yaml --to kiro        --out requirements.md
mycontext rac project technical.yaml --to adr       --out ARCHITECTURE.md
```

See [Projections](./projections) for every target and what it produces.

## The full loop, on one screen

```bash
# 1. Idea -> product spec
mycontext rac product "<your paragraph>" --out product.yaml

# 2. Product spec -> technical spec
mycontext rac technical --from-product product.yaml --out technical.yaml

# 3. Prove they agree (CI gate)
mycontext rac trace --product product.yaml --technical technical.yaml

# 4. Render for your coding agent
mycontext rac project product.yaml --to agents-md --out AGENTS.md
```

## Glossary

| Term | Plain-language meaning |
|------|------------------------|
| **Requirements-as-Code (RaC)** | Treating your requirements as a structured, versionable document that tools can read — not a Word doc. |
| **Product requirements** | The *what & why*: tasks, success criteria, risky actions, safety lines, release gates. |
| **Technical requirements** | The *how*: architecture, guardrails, tools, cost, security, deployment. |
| **Intent** | Your plain-English description of the system. |
| **Intake** | The step that reads your intent and pulls out name, risks, volume, and constraints. |
| **Task** | One kind of request the system handles (e.g. "answer a billing question"). |
| **Out-of-scope task** | The mandatory row that says "if it's not in scope, produce no answer and route to a human." |
| **Rubric** | The scorecard for a task — the specific criteria that define a good answer. |
| **Criterion** | A single line on a rubric, graded either by `code` (automatic) or `judge` (an LLM/human reviewer). |
| **Action** | Something the system can *do* with a tool (look up, draft, send, refund). |
| **Policy** | How an action is controlled: `auto` (allowed), `approve` (needs a human), or `forbidden` (never). |
| **Safety requirement / pre-mortem** | A predicted bad outcome that must never happen, paired with a test. |
| **Hard gate** | A release blocker that cannot be waived without sign-off. |
| **Open question (`OQ-n`)** | A detail RaC could not infer; you fill it in. **Blocking** ones must be answered before trusting the spec. |
| **`TODO(OQ-n)` marker** | A placeholder left inline in the spec, matched to an open question. |
| **`serves`** | The list of product requirement IDs a technical control implements — the link that makes traceability work. |
| **Trace / coverage** | Checking that every risky product requirement has a technical control behind it. |
| **Orphan** | A technical control that references a product requirement that doesn't exist. |
| **Projection** | Rendering a spec into a specific tool's file (AGENTS.md, Cursor rules, Kiro, ...). |
| **`execute=True`** | An optional mode that uses *your* LLM key to answer the open questions automatically (see [grounding](./cognitive-grounding)). |
| **Cognitive pattern** | A reusable reasoning template (e.g. a pre-mortem) used to make the optional LLM answers smarter. |

## Frequently asked questions

**Do I need an API key?** No. The entire product/technical/trace/project flow is
offline and free. A key is only needed if you opt into `--execute` to auto-fill
open questions.

**Will it send my data anywhere?** No. Generation is local. Only `--execute`
contacts an LLM, and only through *your* key/provider.

**Can it enforce the rules it writes?** No — and that's deliberate. RaC writes
the contract; your CI, approval workflow, and runtime enforce it. See the
anti-goals on the [overview](./overview).

**What if RaC guesses something wrong?** It tries not to guess — missing facts
become open questions. Always review the open questions before trusting a spec.
