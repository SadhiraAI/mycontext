---
sidebar_position: 4
title: Task Contract (L0)
description: Declare domain, audience, genre, and grounding in one model — rendered first in research-flow prompts and used by PromptArchitect for format alignment.
---

# Task Contract (L0)

`TaskContract` is **Layer 0** metadata: it describes *what kind of task* the model is doing before the nine main sections (Role, Goal, Rules, …). It calibrates vocabulary, tone, output shape, and evidential rules in one place.

## Import

```python
from mycontext import TaskContract, Context, Guidance, Directive
# or
from mycontext.foundation import TaskContract
```

## Fields

All fields are optional. Only populated fields appear in the assembled L0 table.

| Field | Type | Description |
|-------|------|-------------|
| `domain` | `str \| None` | Subject area and scenario (anchors vocabulary). |
| `audience` | `str \| None` | Who reads the output (formality, assumed knowledge). |
| `genre` | `str \| None` | Output genre — e.g. `internal brief`, `blog post`, `tutorial`, `api reference`. Should align with how you want the model to answer (markdown vs JSON). |
| `grounding` | `str \| None` | Evidential standard — e.g. trace claims to a provided packet; use a literal fallback token when evidence is missing. |
| `metaphor` | `str \| None` | Whether analogical language is allowed. |

## Helpers

- `has_content()` — `True` if any field is set.
- `to_dict()` — only non-null fields as a plain dict.
- `TaskContract.from_dict(d)` — build from a dict (e.g. legacy `metadata["l0"]`).

## With `Context` and research flow

When `research_flow=True`, a populated `task_contract` is rendered as **L0 — TASK CONTRACT** at the very top of the assembled prompt (before Role), as a small markdown table.

```python
from mycontext import Context, Guidance, Directive, TaskContract

ctx = Context(
    task_contract=TaskContract(
        domain="Software engineering — service observability",
        audience="Staff engineers",
        genre="internal brief",
        grounding="Every claim must trace to the MATERIAL PACKET. If absent, write [NOT IN PACKET].",
    ),
    guidance=Guidance(
        role="You are a senior technical writer",
        goal="Produce an evidence-based decision brief",
        rules=["Use ## headings as specified in the user message"],
    ),
    directive=Directive(content="Follow the user’s structure and tables."),
    research_flow=True,
)

print(ctx.assemble()[:500])
```

## Backward compatibility

If you do **not** set `task_contract` but put an L0 dict on `metadata`, the assembler still works:

```python
Context(
    metadata={
        "l0": {
            "domain": "...",
            "audience": "...",
            "genre": "internal brief",
            "grounding": "...",
        }
    },
    research_flow=True,
    ...
)
```

Prefer `task_contract=TaskContract(...)` for type safety and clarity.

## With `PromptArchitect`

Pass the same contract (and ideally the real **`user_message`**) into `improve()` or `build()` so the rewriter can align `output_contract` with the user’s requested format:

```python
from mycontext import TaskContract
from mycontext.intelligence import PromptArchitect

tc = TaskContract(
    genre="internal brief",
    audience="Engineering leadership",
    grounding="Use [NOT IN PACKET] when the source lacks data.",
)

arch = PromptArchitect(model="gpt-4o-mini")
result = arch.improve(
    "You are a writer. Draft an internal brief from user materials.",
    user_message=user_message_text,
    task_contract=tc,
)
```

See [PromptArchitect](../intelligence/prompt-architect) for full API details.

## See also

- [Context Object](./context-object) — `task_contract` field
- [Prompt Assembly & Thinking Strategies](./research-flow) — where L0 sits in the nine-section layout
