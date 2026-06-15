---
sidebar_position: 4
title: Requirements-as-Code
description: Author and score Requirements-as-Code with mycontext. Draft a requirements.yaml from cognitive patterns and score candidate outputs — authoring and scoring only, never a runtime.
---

# Requirements-as-Code (Authoring + Scoring)

:::tip Looking for the full Requirements-as-Code guide?
This page documents the original **authoring + scoring bridge**
(`draft_requirements`, `score_output`). The modern workflow — `product()`,
`technical()`, `trace()`, `project()`, `validate()`, and `analyze()` — has its
own comprehensive section: **[Requirements-as-Code →](../rac/overview)**. New
projects should start there.
:::

The `mycontext.rac` package helps you **author** and **score** agent requirements.
It drafts the sections of a `requirements.yaml` using the open-source cognitive
patterns and scores candidate outputs with the evaluation stack. The emitted
`requirements.yaml` is then handed to **your own** `spec compile` / CI / human
review for enforcement.

:::warning Authoring and scoring only — by design
mycontext does **not** ship a requirements compiler, a CI gate executor, or a
human-in-the-loop / budget runtime. It authors and scores; your stack enforces.
:::

## How sections map to patterns

Each `requirements.yaml` section is drafted by the patterns best suited to it:

| Section | Drafting patterns |
|---------|-------------------|
| `task_taxonomy` | `question_analyzer`, `intent_recognizer`, `stakeholder_mapper` |
| `rubrics` | `code_reviewer`, `comparative_analyzer`, `socratic_questioner` |
| `action_risk_matrix` | `risk_assessor`, `impact_assessor` |
| `pre_mortem` | `future_scenario_planner`, `conflict_resolver` |

## Draft a requirements.yaml (offline)

By default, authoring is fully offline — each section emits the prompt you can run
anywhere:

```python
from mycontext.rac import draft_requirements, to_yaml

doc = draft_requirements(
    "Build a support copilot that drafts replies to billing tickets."
)
print(to_yaml(doc))
```

The emitted document carries an explicit anti-goal note in its metadata:

```yaml
version: 1
task: Build a support copilot that drafts replies to billing tickets.
metadata:
  generated_by: mycontext-ai 0.12.0
  mode: authoring
  note: >-
    Authored and scored by mycontext (authoring + scoring only). Enforcement ...
    is the responsibility of your own stack.
task_taxonomy:
  templates: [question_analyzer, intent_recognizer, stakeholder_mapper]
  drafts:
    - template: question_analyzer
      prompt: "ROLE: ..."
```

## Fill the drafts with an LLM (your key)

Pass `execute=True` to run each section's pattern and fill in the drafted content
using your own API key (still no mycontext server, still your cost only):

```python
doc = draft_requirements(task, provider="openai", execute=True)
```

## Score candidate outputs

Score a candidate rubric answer or agent output against the context that produced
it. Offline and deterministic by default:

```python
from mycontext.rac import score_output

result = score_output(
    "Identify the root causes of the outage and propose fixes.",
    "Root cause: a misconfigured timeout. Fix: add validation. Step 1: ...",
)
print(result["overall"])      # e.g. 0.78
print(result["dimensions"])   # per-dimension scores
```

## API

| Symbol | Purpose |
|--------|---------|
| `RequirementsAuthor(provider, execute)` | Configurable author; `.draft(task)` returns the requirements dict |
| `draft_requirements(task, provider, execute)` | One-shot drafting helper |
| `to_yaml(requirements)` | Serialize a drafted structure to YAML |
| `score_output(context_prompt, output, mode)` | Score an output against its context |
