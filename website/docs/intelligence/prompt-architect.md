---
sidebar_position: 11
title: PromptArchitect
description: Apply the 9-section prompt architecture to any raw prompt — parse, score, rewrite, and diff.
---

# PromptArchitect

`PromptArchitect` takes any raw prompt string and upgrades it to the 9-section architecture. It detects which sections exist, scores quality before and after, rewrites weak or missing sections using an LLM, and returns a section-level diff with score deltas.

## Why it exists

The 9-section architecture (Role → Goal → Rules → Style → Reasoning Strategy → Examples → Output Contract → Guard Rails → Task) is research-backed and encoded in every mycontext cognitive template. But teams often write raw prompts outside the SDK. `PromptArchitect` brings those prompts up to the same structural standard without requiring them to be rewritten as `Context` objects.

## Import

```python
from mycontext.intelligence import PromptArchitect
```

## Three entry points

| Method | LLM call | Use when |
|--------|----------|----------|
| `parse(prompt)` | No | You want to see which sections exist and what quality score the current prompt gets |
| `build(task, …)` | Yes | You have a plain task description and want a complete 9-section prompt generated from scratch |
| `improve(prompt, …)` | Yes | You have an existing prompt and want it upgraded in place, with a diff |

### Optional arguments (`build` / `improve`)

Both methods share the same optional **named** parameters below, plus any extra keyword arguments passed through to the internal `Context.execute` / LiteLLM call (for example `api_key`, `max_tokens`, or an explicit `temperature` override).

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_message` | `str \| None` | The real user/task message the model will see at runtime. When set, the rewriter can infer required headings, markers (e.g. `[NOT IN PACKET]`), and output shape so `output_contract` matches the task. Also used as the primary text for **auto generation routing** when `auto_generation_params` is true. |
| `task_contract` | `TaskContract \| None` | L0 metadata (`domain`, `audience`, `genre`, `grounding`, `metaphor`). Calibrates every generated section; **genre** is used to avoid mismatches (e.g. internal brief vs JSON-only contract). When auto-routing is on, **genre** and **metaphor** help classify the task (e.g. JSON API vs creative). |
| `auto_generation_params` | `bool` | Default `false`. When `true`, the SDK merges decoding kwargs before the internal rewriter LLM call: `temperature` / `top_p` / `n` on normal chat models, or `reasoning_effort` (and no custom `temperature`) on reasoning-style model ids. See [Auto generation routing](#auto-generation-routing). |
| `generation_profile` | `"internal" \| "downstream" \| "both"` | Default `"internal"`. With `auto_generation_params=true`: `"internal"` only records what was used for the **internal** JSON build/rewrite call; `"downstream"` or `"both"` also fills `result.metadata["suggested_execute_kwargs"]` for the **user’s** later `Context.execute` on the improved prompt (warmer presets for creative tasks, etc.). |

Explicit execute kwargs **always win** on key clashes (for example `temperature=0.01` overrides the auto preset).

```python
from mycontext import TaskContract
from mycontext.intelligence import PromptArchitect

tc = TaskContract(genre="internal brief", audience="Engineering leadership")

arch = PromptArchitect(model="gpt-4o-mini")
result = arch.improve(
    flat_system_prompt,
    user_message=full_user_message,
    task_contract=tc,
)

# Auto routing: internal call stays cold; metadata carries suggested kwargs for your execute()
result = arch.build(
    "Brainstorm launch angles for a B2B SaaS",
    auto_generation_params=True,
    generation_profile="both",
)
print(result.metadata.get("suggested_execute_kwargs"))
```

## Auto generation routing

The rewriter inside `build` / `improve` must return **valid JSON**. That path should stay **low-variance** even when the user’s task is creative. Auto routing implements a small **caller-side policy** (no extra model training):

1. **Classify** the task from `user_message` or `task` (and optional `task_contract`) using fast heuristics — structured JSON, judge/rubric language, brainstorm/creative cues, explore/multi-draft language, etc.
2. **Pick presets** — internal mode uses a cold default for chat models; downstream mode maps intent to `temperature`, `top_p`, and sometimes `n > 1` (for “several options” style asks; Gemini routing forces `n=1` because batched completions differ by API).
3. **Respect the model id** — OpenAI-style **reasoning** SKUs (`o1`–`o4`, `gpt-5` without `chat` in the name, etc.) are treated as **not** accepting arbitrary `temperature` / `top_p` for that internal call; the SDK omits those and sets `reasoning_effort` instead. Ids such as `gpt-5-chat` / `gpt-5.2-chat-latest` are treated as **chat** models where sampling kwargs apply.

LiteLLM is configured with `drop_params=True` in the provider, but the SDK still **omits** `temperature` when possible for reasoning-style ids to avoid edge-case API errors.

### Metadata keys (when `auto_generation_params=True`)

| Key | Description |
|-----|-------------|
| `internal_generation_kwargs` | Dict merged into the internal rewriter call (before your explicit overrides). |
| `internal_generation_kwargs_rationale` | Short string explaining the routing decision. |
| `suggested_execute_kwargs` | Present when `generation_profile` is `"downstream"` or `"both"` — suggested kwargs for **your** `Context.execute(...)` using the improved prompt. |
| `suggested_execute_kwargs_rationale` | Rationale for the downstream preset. |

### Using routing outside `PromptArchitect`

For custom tooling you can call the same helpers the architect uses:

```python
from mycontext.intelligence import (
    classify_generation_intent,
    model_allows_sampling,
    resolve_generation_kwargs,
)

intent = classify_generation_intent("Return strictly valid JSON", task_contract=None)
kwargs, rationale = resolve_generation_kwargs(
    question="Brainstorm ten ideas",
    provider="openai",
    model="gpt-4o-mini",
    task_contract=None,
    mode="downstream",
)
```

## `parse()` — detect sections, no LLM

```python
arch = PromptArchitect()

parsed = arch.parse("You are a helpful assistant. Summarize this report concisely.")
print(parsed.detected_sections)
# {'role': True, 'goal': False, 'rules': False, 'style': True, 'reasoning': False,
#  'examples': False, 'output_contract': False, 'guard_rails': False, 'task': True}

print(f"Coverage: {parsed.coverage:.0%}")   # 33%
print(parsed.missing_sections)              # ['goal', 'rules', 'reasoning', 'examples', 'output_contract', 'guard_rails']
```

`parse()` uses heuristic pattern matching — zero cost, instant.

## `build()` — generate from scratch

```python
arch = PromptArchitect(provider="openai", model="gpt-4o-mini")

result = arch.build("Analyze customer churn data and identify at-risk segments")
print(result.improved_prompt)
# === ROLE ===
# You are a senior customer analytics specialist ...
# === GOAL ===
# Identify customer segments at risk of churn ...
# ...

print(result.after_score.overall)   # e.g. 0.81
```

## `improve()` — upgrade and diff

```python
result = arch.improve(
    "You are an analyst. Look at this data and try to find patterns. Be thorough."
)

print(result.summary())
# Score: 0.22 → 0.79  (+0.57)
# Sections added: goal, rules, reasoning, output_contract, guard_rails
# Issues resolved: missing_goal; weak_role; suggestive_modals (try to); missing_output_contract

print(result.diff_report())
# [ROLE] Expanded — added expertise anchors and domain framing
# [GOAL] Added — was missing entirely
# [RULES] Added — 4 binding rules generated
# [STYLE] Kept — already adequate
# [REASONING] Added — step-by-step reasoning strategy injected
# ...
```

## Return type: `ArchitectResult`

| Attribute | Type | Description |
|-----------|------|-------------|
| `improved_prompt` | `str` | Assembled 9-section prompt string |
| `improved_context` | `Context` | SDK `Context` equivalent to `improved_prompt` |
| `parsed` | `ParsedSections` | Heuristic section detection (`build` uses a minimal baseline) |
| `before_score` | `float` | Overall quality score before (`0.0`–`1.0`) |
| `after_score` | `float` | Overall quality score after |
| `score_delta` | `float` | `after_score - before_score` |
| `diffs` | `list[SectionDiff]` | Per-section what changed and why |
| `before_issues` / `after_issues` | `list[str]` | Issue tags from `QualityMetrics` |
| `resolved_issues` | `list[str]` | Issues present before but not after |
| `metadata` | `dict` | Always includes `mode`, `model`, `provider`, `target_provider`; may include generation-routing keys above |

## Combine with `QualityMetrics` for a quality gate

```python
from mycontext.intelligence import PromptArchitect, QualityMetrics

arch = PromptArchitect(provider="openai", model="gpt-4o-mini")
result = arch.improve(raw_prompt)

if result.after_score.overall < 0.70:
    print("Still below threshold — inspect diffs:")
    print(result.diff_report())
else:
    print("Prompt approved — ready to use")
    print(result.improved_prompt)
```

## See also

- [Task Contract (L0)](../foundations/task-contract) — shared L0 model for manual `Context` builds and `PromptArchitect` (including routing hints)
- [GuidanceOptimizer](./guidance-optimizer) — upgrade `Guidance` objects in SDK templates
- [Prompt Optimization Workflow](../quality/prompt-optimization-workflow) — end-to-end workflow using both tools
- [QualityMetrics](../quality/quality-metrics) — score any `Context` across 6 dimensions
