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
| `build(task)` | Yes | You have a plain task description and want a complete 9-section prompt generated from scratch |
| `improve(prompt)` | Yes | You have an existing prompt and want it upgraded in place, with a diff |

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
| `original_prompt` | `str` | Input prompt |
| `improved_prompt` | `str` | Rewritten prompt |
| `improved_context` | `Context` | SDK `Context` object equivalent |
| `parsed` | `ParsedPrompt` | Section detection result |
| `before_score` | `QualityScore` | Pre-improvement quality score |
| `after_score` | `QualityScore` | Post-improvement quality score |
| `score_delta` | `float` | `after_score.overall - before_score.overall` |
| `diffs` | `list[SectionDiff]` | Per-section what changed and why |

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

- [GuidanceOptimizer](./guidance-optimizer) — upgrade `Guidance` objects in SDK templates
- [Prompt Optimization Workflow](../quality/prompt-optimization-workflow) — end-to-end workflow using both tools
- [QualityMetrics](../quality/quality-metrics) — score any `Context` across 6 dimensions
