---
sidebar_position: 3
title: Prompt Optimization Workflow
description: A step-by-step workflow for turning any weak prompt into a high-quality 9-section context — covering parse, score, rewrite, diff, and validate with the PromptArchitect and GuidanceOptimizer tools.
---

# Prompt Optimization Workflow

mycontext provides a complete, reproducible pipeline for turning any prompt — from a one-liner to a partially-structured paragraph — into a high-quality 9-section context. This document covers the full journey: what the workflow is, when to use each tool, and how to run it end to end.

---

## The Two Workflows

Depending on what you're optimizing, there are two distinct paths:

| You have... | Use | What it does |
|---|---|---|
| A raw prompt string | [`PromptArchitect`](#promptarchitect-for-raw-prompts) | Parse → Score → Rewrite all 9 sections → Diff |
| An SDK template `Guidance` object | [`GuidanceOptimizer`](#guidanceoptimizer-for-sdk-templates) | Audit rules → Detect weak language → Rewrite to binding rules |

Both tools share the same underlying principle: the **9-Section Prompt Architecture**.

---

## The 9-Section Architecture

Every high-quality prompt has nine components in a specific order, grounded in LLM attention research:

```
PRIMACY ZONE    → ① Role          Who the model is
                  ② Goal          What success looks like
INSTRUCTIONS    → ③ Rules         Binding behavioral constraints
                  ④ Style         Tone and voice
MIDDLE          → ⑤ Reasoning     Thinking strategy to apply
                  ⑥ Examples      Negative + positive demonstrations
LATE            → ⑦ Output Contract  Exact structure required
                  ⑧ Guard Rails   What to avoid, edge-case handling
RECENCY ZONE    → ⑨ Task          The final, clearest imperative sentence
```

Research basis: Liu et al. 2023 (primacy-recency bias), Li et al. 2023 (+9.7 BLEU for task-last placement), CO-STAR (Ng, 2024).

The key differentiators from generic prompts:
- **Rules use binding language** — `must`/`always`/`never`, not `should`/`try to`/`ideally`
- **Goal is imperative** — "Identify the root cause" not "You will look at..."
- **Examples include negative cases** — show the WRONG approach before the correct one
- **Task restates the request last** — the recency zone is the final attention anchor

---

## PromptArchitect — for raw prompts

Use `PromptArchitect` when you have a raw string prompt that needs to be evaluated and improved.

### Quick start

```python
from mycontext.intelligence import PromptArchitect

arch = PromptArchitect(provider="openai", model="gpt-4o-mini")

# Option A: Improve an existing prompt
result = arch.improve("You are an analyst. Summarize this customer feedback.")
print(result.summary())
# Score: 28% → 79%  (+51%)
# Added sections: goal, rules, style, reasoning, examples, output_contract, guard_rails
# Resolved 4 issue(s): Missing guidance/role component; No behavioral rules defined; ...

print(result.diff_report())  # Section-by-section what changed and why
print(result.improved_prompt)  # The full assembled prompt, ready to use

# Option B: Build from scratch
result = arch.build("Analyze customer churn and identify at-risk segments")
print(result.improved_prompt)

# Option C: Just inspect — zero LLM calls
parsed = arch.parse("You are an analyst. Summarize this customer feedback.")
print(parsed.present())   # ['role', 'task']
print(parsed.missing())   # ['goal', 'rules', 'style', 'reasoning', 'examples', 'output_contract', 'guard_rails']
```

### The `improve()` pipeline

`improve()` runs five steps internally:

```
1. PARSE   — heuristically detect which sections already exist (no LLM)
2. SCORE   — QualityMetrics on the original context
3. REWRITE — LLM fills missing sections, strengthens weak ones
4. SCORE   — QualityMetrics on the improved context
5. DIFF    — section-by-section change record with rationale
```

### Result object

```python
@dataclass
class ArchitectResult:
    improved_context: Context       # Full mycontext Context, ready for .execute()
    improved_prompt: str            # Assembled prompt string
    before_score: float             # QualityMetrics score before (0.0–1.0)
    after_score: float              # QualityMetrics score after (0.0–1.0)
    score_delta: float              # Improvement
    parsed: ParsedSections          # What was detected in the original
    diffs: list[SectionDiff]        # Per-section change records
    before_issues: list[str]        # Issues found in original
    after_issues: list[str]         # Remaining issues after rewrite
    resolved_issues: list[str]      # Issues that were fixed
    metadata: dict                  # Mode, model, provider
```

### `parse()` — zero-cost inspection

```python
parsed = opt.parse(prompt)

parsed.present()    # ['role', 'task']
parsed.missing()    # ['goal', 'rules', ...]

# Access what was found per section
parsed.role         # "data analyst"
parsed.rules        # ["Must include actionable recommendations"]
parsed.task         # "Summarize the attached feedback report"
```

### Reading the diff report

```python
print(result.diff_report())
```

```
── SECTION DIFF ──────────────────────────────────────────

[ADDED]  § ROLE
  AFTER:  Senior data analyst with expertise in customer success and churn analytics
  WHY:    Section was absent; added using 9-section principle: Include seniority level

[STRENGTHENED]  § RULES
  BEFORE: Be helpful and accurate
  AFTER:  Always quantify findings with specific metrics; Never speculate beyond the data provided; ...
  WHY:    Existing content was weak; upgraded to binding language (must/always/never)

[ADDED]  § EXAMPLES
  AFTER:  WRONG: "Customers seem unhappy with onboarding." CORRECT: "42% of churned users (Q3 cohort) ...
  WHY:    Section was absent; added using 9-section principle: Include negative + positive examples

──────────────────────────────────────────────────────
```

### Constructor

```python
PromptArchitect(
    provider: str = "openai",
    model: str = "gpt-4o-mini",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | `str` | `"openai"` | LLM provider for rewrite calls |
| `model` | `str` | `"gpt-4o-mini"` | Model for rewrite calls |

`parse()` makes no LLM calls. `improve()` and `build()` make one LLM call each.

---

## GuidanceOptimizer — for SDK templates

Use `GuidanceOptimizer` when you're working with a `Guidance` object inside an SDK template and want to automatically upgrade its rules to binding, evidence-backed language.

```python
from mycontext.intelligence import GuidanceOptimizer
from mycontext.foundation import Guidance

guidance = Guidance(
    role="Data analyst",
    rules=[
        "Try to look for patterns",
        "You should mention limitations",
        "Be accurate",
    ],
)

opt = GuidanceOptimizer(provider="openai", model="gpt-4o-mini")
result = opt.optimize(guidance)

print(result.optimized_guidance.rules)
# [
#   "Identify and quantify every pattern — report the specific metric and its value.",
#   "State data limitations explicitly: what is absent, what it prevents, what is needed.",
#   "Every claim must trace to a specific data point — no unsupported assertions.",
# ]

print(f"Rule strength: {result.before_score:.0%} → {result.after_score:.0%}")
```

### What it optimizes

`GuidanceOptimizer` targets three specific weaknesses that degrade template quality:

| Problem | Example before | Example after |
|---------|---------------|---------------|
| **Suggestive modals** | "Should mention limitations" | "Must explicitly state each data gap and what it prevents" |
| **Vague directives** | "Be accurate" | "Every claim must cite the specific metric that supports it" |
| **Under-specified rules** | "Try to look for patterns" | "Identify and quantify every pattern — report the metric and its magnitude" |

### The audit report

```python
print(result.audit_report())
```

```
── GUIDANCE AUDIT ────────────────────────────────────────
Role:  Data analyst
Rules: 3 total  |  0 binding  |  3 weak

WEAK RULES DETECTED:
  [1] "Try to look for patterns"
      Issue: suggestive modal ("try to")
      Fix:   "Identify and quantify every pattern..."

  [2] "You should mention limitations"
      Issue: weak modal ("should")
      Fix:   "Must explicitly state each data gap..."

  [3] "Be accurate"
      Issue: vague directive (< 5 words, no measurable criterion)
      Fix:   "Every claim must cite the specific metric..."

Rule strength score: 15% → 91%
──────────────────────────────────────────────────────────
```

---

## End-to-End Workflow

Here is the full recommended flow when improving a prompt from scratch to production-ready:

```python
from mycontext.intelligence import PromptArchitect, QualityMetrics

arch = PromptArchitect(provider="openai", model="gpt-4o-mini")
qm = QualityMetrics()

# ── Step 1: Inspect ────────────────────────────────────────
raw_prompt = """
You are a helpful assistant. Analyze the customer support data and
provide insights. Be thorough and helpful.
"""

parsed = opt.parse(raw_prompt)
print("Present:", parsed.present())   # ['role', 'task']
print("Missing:", parsed.missing())   # ['goal', 'rules', 'style', ...]

# ── Step 2: Score the original ─────────────────────────────
from mycontext import Context
from mycontext.foundation import Guidance, Directive

original_ctx = Context(
    guidance=Guidance(role="helpful assistant", rules=[]),
    directive=Directive(content=raw_prompt),
)
before = qm.evaluate(original_ctx)
print(f"Before: {before.overall:.1%}")        # 29%
print("Issues:", before.issues[:3])

# ── Step 3: Improve ────────────────────────────────────────
result = arch.improve(raw_prompt)
print(result.summary())
# Score: 29% → 82%  (+53%)

# ── Step 4: Inspect the diff ───────────────────────────────
print(result.diff_report())

# ── Step 5: Execute the improved prompt ────────────────────
response = result.improved_context.execute(provider="openai")
print(response.response)

# ── Step 6: Evaluate the output ────────────────────────────
from mycontext.intelligence import OutputEvaluator

evaluator = OutputEvaluator(mode="heuristic")
output_score = evaluator.evaluate(result.improved_context, response.response)
print(f"Output quality: {output_score.overall:.1%}")
```

---

## Typical Score Lifts

Based on internal experiments across prompt categories:

| Prompt type | Typical before | Typical after | Common additions |
|-------------|---------------|---------------|-----------------|
| One-liner ("Summarize this") | 15–25% | 70–85% | role, goal, rules, output contract |
| Role-only ("You are an analyst. Analyze this.") | 28–35% | 75–88% | goal, rules, examples, guard rails |
| Partially structured | 45–60% | 78–90% | strengthened rules, examples, guard rails |
| Already structured | 65–75% | 80–92% | binding language upgrades, gap examples |

The largest single gains come from:
1. **Adding binding rules** — typically +15–20% on `clarity` and `completeness`
2. **Adding examples** — typically +10–15% on `specificity`  
3. **Adding an output contract** — typically +8–12% on `structure`

---

## Quality Gate Integration

Use `PromptOptimizer` as a pre-execution quality gate:

```python
from mycontext.intelligence import PromptArchitect, QualityMetrics

def ensure_quality(prompt: str, min_score: float = 0.70) -> str:
    """Return an architected prompt that meets the quality bar."""
    qm = QualityMetrics()
    
    # Build a minimal context to check the raw prompt
    from mycontext import Context
    from mycontext.foundation import Guidance, Directive
    ctx = Context(
        guidance=Guidance(role="Assistant"),
        directive=Directive(content=prompt),
    )
    score = qm.evaluate(ctx)
    
    if score.overall >= min_score:
        return prompt  # Already good enough
    
    # Improve and return the upgraded prompt
    arch = PromptArchitect()
    result = arch.improve(prompt)
    print(f"Auto-improved: {score.overall:.0%} → {result.after_score:.0%}")
    return result.improved_prompt

# In production
prompt = ensure_quality("You are an assistant. Review this contract.")
response = Context(directive=Directive(content=prompt)).execute(provider="openai")
```

---

## Choosing Between the Two Tools

```
Have a raw string prompt?
  └─ Use PromptArchitect.improve() or .build()

Working on an SDK template's Guidance?
  └─ Use GuidanceOptimizer.optimize()

Want to inspect without changing anything?
  └─ Use PromptOptimizer.parse() — zero LLM calls

Want to score before/after?
  └─ Use QualityMetrics.compare(ctx_before, ctx_after)

Want to evaluate the output too?
  └─ Use OutputEvaluator after .execute()
```

---

## Related

- [QualityMetrics →](./quality-metrics) — Score a context before sending it
- [OutputEvaluator →](./output-evaluator) — Score an LLM response after receiving it
- [Research: 9-Section Ordering →](../research/prompt-engineering-foundation) — Why the order matters
