# Key Use Cases and Code Clippings

**Why mycontext-ai is a pathbreaking context engineering engine**

This document lists the main scenarios where mycontext-ai directly addresses industry prompt and context problems: iterative prompt hacking, lack of pattern selection, no way to measure quality, and vendor lock-in. Each scenario includes the **industry pain**, what **mycontext does**, a **minimal code clipping**, and the **key API**.

---

## 1. Create a custom prompt from scratch

**Pain:** Teams don't know how to structure system vs. user content, or how to combine role, rules, and task in one portable object.

**Solution:** mycontext gives a single `Context` that holds `Guidance` (role + rules + style) and `Directive` (the actual task). No guesswork—clear structure from the start.

```python
from mycontext import Context, Guidance, Directive

ctx = Context(
    guidance=Guidance(
        role="Senior security reviewer",
        rules=["Flag every injection risk", "Suggest concrete fixes"],
        style="concise, actionable",
    ),
    directive=Directive(content="Review this API for auth and input validation."),
)
# Use with any LLM: ctx.to_openai(), ctx.to_anthropic(), or ctx.execute(provider="openai")
```

**Key API:** `Context`, `Guidance`, `Directive` (core).

---

## 2. Turn a raw question into a perfect prompt (auto pattern)

**Pain:** Users don't know which reasoning pattern fits their question (decision, comparison, root cause, etc.), so they write generic prompts and get generic answers.

**Solution:** One call to `transform()` analyzes the input and applies the right cognitive pattern automatically—no need to pick from 85 templates.

```python
from mycontext.intelligence import transform

context = transform("Should we migrate to microservices? Compare tradeoffs.")
# Engine selects e.g. DecisionFramework or ComparativeAnalyzer and builds the context
print(context.to_markdown())  # or context.execute(provider="openai")
```

**Key API:** `transform()` (intelligence layer).

---

## 3. Use a built-in cognitive template from scratch

**Pain:** Teams want a specific method (Five Whys, decision framework, comparison matrix) but don't want to hand-craft the full prompt.

**Solution:** Pick a research-backed pattern, call `build_context()` with your inputs—you get a complete, structured prompt for that method.

```python
from mycontext.templates.free.decision import DecisionFramework

df = DecisionFramework()
ctx = df.build_context(
    decision="Choose database for new service",
    options=["Postgres", "MongoDB", "DynamoDB"],
    depth="comprehensive",
)
# ctx is ready for export or execute; no API key needed to build
```

**Key API:** `Pattern.build_context()` (e.g. `DecisionFramework`, `RootCauseAnalyzer`, `ComparativeAnalyzer`).

---

## 4. Auto-suggest which template(s) to use

**Pain:** With 85 patterns available, users don't know which one (or which chain) fits their question.

**Solution:** `suggest_patterns(question)` maps the question to the best patterns and can return an ordered workflow chain (keyword or hybrid with LLM).

```python
from mycontext.intelligence import suggest_patterns

result = suggest_patterns(
    "Why did churn spike? Timeline, root cause, and future scenarios.",
    suggest_chain=True,
)
print(result.suggested_chain)  # e.g. temporal_sequence_analyzer -> root_cause_analyzer -> ...
print(result.to_markdown())   # structured output
```

**Key API:** `suggest_patterns()` (pattern_suggester).

---

## 5. Chain multiple patterns (workflow)

**Pain:** Complex questions need several steps (e.g. timeline, then root cause, then scenarios)—manually chaining prompts is error-prone.

**Solution:** Use `suggest_patterns(..., suggest_chain=True)` to get an ordered list, then run each pattern with `get_pattern_class()` and pass the previous output into the next `build_context()`.

```python
from mycontext.intelligence import suggest_patterns, get_pattern_class

result = suggest_patterns("Outage last week: what happened and what futures?", suggest_chain=True)
chain = result.suggested_chain or []
prev = "Outage last week: what happened and what futures?"
for name in chain[:3]:
    cls = get_pattern_class(name)
    if cls and hasattr(cls(), "build_context"):
        ctx = cls().build_context(problem=prev[:500], symptoms=prev[:2000] if "root_cause" in name else prev)
        prev = ctx.directive.content
# prev is the final context; optionally ctx.execute(provider="openai")
```

**Key API:** `suggest_patterns(suggest_chain=True)`, `get_pattern_class()`, chained `build_context()`.

---

## 6. Measure prompt/context quality

**Pain:** There's no objective way to know if a prompt is good—teams iterate blindly.

**Solution:** `QualityMetrics` scores a context on six dimensions (clarity, completeness, specificity, relevance, structure, efficiency) and returns issues and strengths.

```python
from mycontext.intelligence import QualityMetrics
from mycontext import Context, Guidance, Directive

ctx = Context(
    guidance=Guidance(role="Analyst", rules=["Be precise"]),
    directive=Directive(content="Analyze Q3 sales data."),
)
metrics = QualityMetrics()
score = metrics.evaluate(ctx)
print(metrics.report(score))  # overall, dimensions, issues, strengths, suggestions
```

**Key API:** `QualityMetrics().evaluate(context)`, `metrics.report(score)`.

---

## 7. Refine existing prompt with quality feedback

**Pain:** Iterating on prompts without concrete feedback wastes time.

**Solution:** Same as scenario 6: evaluate the context, then use `score.issues` and `score.suggestions` to improve. Optionally use `QualityMetrics.compare(context_before, context_after)` to verify improvement.

```python
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics()
score = metrics.evaluate(context)
for issue in score.issues:
    print("Issue:", issue)
for suggestion in score.suggestions:
    print("Suggestion:", suggestion)
# Revise context (e.g. add rules, clarify directive), then re-evaluate
revised_context = Context(...)  # your improved context
score2 = metrics.evaluate(revised_context)
diff = metrics.compare(context, revised_context)
```

**Key API:** `score.issues`, `score.suggestions`, `QualityMetrics.compare(context_before, context_after)`.

---

## 8. Enforce structured output (JSON / Markdown)

**Pain:** LLMs return free-form text; production needs parseable output (JSON, YAML, or consistent Markdown).

**Solution:** Add `output_format(...)` to the directive so the model is instructed to respond in the chosen format. Parse responses with `extract_json()` or `parse_structured()` from the same module.

```python
from mycontext import Context, Directive
from mycontext.utils.structured_output import output_format

instruction = output_format("json", schema={"summary": "str", "risks": "list", "recommendation": "str"})
ctx = Context(directive=Directive(content=f"Analyze this project proposal.\n\n{instruction}"))
# result = ctx.execute(provider="openai"); then parse result.response
```

**Key API:** `output_format("json", schema=...)`, `output_format("markdown")` (utils.structured_output).

---

## 9. One context, any LLM or framework

**Pain:** Prompts are tied to one vendor or framework; switching means rewriting.

**Solution:** Build one `Context` and export to the format you need—OpenAI, Anthropic, LangChain, YAML, etc.

```python
from mycontext.intelligence import transform

context = transform("What are the main risks of this migration?")
openai_format = context.to_openai()
claude_format = context.to_anthropic()
langchain_msgs = context.to_langchain()
yaml_config = context.to_yaml()
```

**Key API:** `context.to_openai()`, `context.to_anthropic()`, `context.to_langchain()`, `context.to_yaml()`.

---

## 10. Explain why a pattern was chosen

**Pain:** Users want to understand why the engine picked a given pattern for their input.

**Solution:** `TransformationEngine().explain_selection(input)` returns a human-readable explanation (input type, complexity, domain, recommended patterns, confidence).

```python
from mycontext.intelligence import TransformationEngine

engine = TransformationEngine()
explanation = engine.explain_selection("Should we use Kubernetes or ECS?")
print(explanation)
```

**Key API:** `TransformationEngine().explain_selection(input)`.

---

## Advanced use cases

These scenarios show why teams adopt mycontext-ai for production: context chaining, Agent Skills with quality gates, prompt/skill refinement, pattern fusion, and framework integration.

---

### 11. Context chaining (multi-stage pipeline)

**Pain:** Strategic questions need several reasoning steps (timeline, then root cause, then scenarios, then synthesis). Manually piping prompts is fragile and inconsistent.

**Solution:** Chain enterprise patterns so each stage’s output becomes the next stage’s input. Build the full pipeline with `build_context()` only (no LLM cost until you call `execute()` once on the final context).

```python
from mycontext.templates.enterprise.temporal import TemporalSequenceAnalyzer, FutureScenarioPlanner
from mycontext.templates.enterprise.diagnostic import RootCauseAnalyzer
from mycontext.templates.enterprise.synthesis import HolisticIntegrator

raw = "Q3: Complaints up 40%. Q2: Competitor launched. Q1: Support tickets doubled."
temporal = TemporalSequenceAnalyzer()
ctx1 = temporal.build_context(events=raw, time_span="12 months", context="SaaS decline")
stage1 = ctx1.directive.content

ctx2 = RootCauseAnalyzer().build_context(problem="Satisfaction collapse", symptoms=stage1[:2500])
stage2 = ctx2.directive.content

ctx3 = FutureScenarioPlanner().build_context(
    focal_question="How will retention evolve?", time_horizon="18 months",
    current_situation=stage2[:2000])
stage3 = ctx3.directive.content

ctx4 = HolisticIntegrator().build_context(
    topic="Recovery strategy",
    perspectives=f"Temporal: {stage1[:600]}...\nRCA: {stage2[:600]}...\nScenarios: {stage3[:600]}...")
# One LLM call for full analysis: result = ctx4.execute(provider="openai")
```

**Key API:** Chained `Pattern.build_context()` with each stage’s `directive.content` as the next stage’s input; final `Context.execute()`.

---

### 12. Run Agent Skills (SKILL.md) with a quality gate

**Pain:** Skills or reusable prompts run without quality checks; bad prompts waste cost and produce poor results.

**Solution:** Load a skill (SKILL.md), build a Context (with optional pattern fusion), evaluate quality, and run only if the score meets a threshold. Execution is gated when quality is below the threshold.

```python
from pathlib import Path
from mycontext import Context
from mycontext.skills import SkillRunner, improvement_report

runner = SkillRunner()
result = runner.run(
    Path("path/to/your_skill"),  # directory with SKILL.md
    task="Compare microservices vs monolith for our team",
    topic="microservices vs monolith",
    depth="detailed",
    execute=False,
    quality_threshold=0.7,
)
print("Quality:", result.quality_score.overall)
print("Gated (skipped execute):", result.gated)
print(improvement_report(result))
```

**Key API:** `SkillRunner().run(skill_path, task=..., quality_threshold=...)`, `improvement_report(result)`.

---

### 13. Refine SKILL.md with improvement_report and suggested_edits

**Pain:** Skill authors don’t know how to improve a SKILL.md; they need concrete, actionable feedback.

**Solution:** After running a skill, use `improvement_report(result)` for a quality summary and `suggested_edits(result)` for concrete edit suggestions (e.g. “Add output format”, “Replace vague language”). Apply edits manually or use `improve_skill_with_llm()` to get a rewritten SKILL.md (requires API key).

```python
from mycontext.skills import SkillRunner, improvement_report, suggested_edits

result = runner.run(Path("my_skill"), task="Analyze risks", execute=False)
report = improvement_report(result)
edits = suggested_edits(result)
print(report)
for e in edits[:5]:
    print("-", e)
# Optional: improved_content = improve_skill_with_llm(result, skill_path=Path("my_skill"), provider="openai")
```

**Key API:** `improvement_report(result)`, `suggested_edits(result)`, `improve_skill_with_llm(result, ...)` (optional).

---

### 14. Pattern fusion: anchor a skill to a cognitive template

**Pain:** A skill is just markdown; you want it to use a proven reasoning structure (e.g. comparative analysis, root cause) without rewriting the skill from scratch.

**Solution:** In SKILL.md frontmatter set `pattern: comparative_analyzer` (or any mycontext pattern name). SkillRunner fuses the skill body and task with that pattern’s `build_context()` so the generated context follows the template structure.

```yaml
# SKILL.md frontmatter
name: Compare options
description: Compare two or more options on criteria.
input_schema:
  topic: string
  criteria: string
pattern: comparative_analyzer
---
Compare the following: **{topic}**. Criteria: **{criteria}**.
```

```python
ctx = Context.from_skill(Path("my_skill"), topic="Cloud providers", criteria="Cost, latency, SLA")
# Context is built via ComparativeAnalyzer with your skill content; export or execute
```

**Key API:** `pattern: <pattern_name>` in SKILL.md, `Context.from_skill(path, **params)`, `SkillRunner().build_context(skill, task=..., **params)`.

---

### 15. Hybrid pattern suggestion (keyword + LLM)

**Pain:** Keyword-only suggestion can miss nuance; LLM-only can hallucinate pattern names. You want the best of both.

**Solution:** `suggest_patterns(question, mode="hybrid")` runs keyword matching first, then asks an LLM to pick from the catalog, and merges the results in a sensible workflow order. Use when you have an API key and want higher-quality suggestions.

```python
from mycontext.intelligence import suggest_patterns

result = suggest_patterns(
    "Why did revenue drop? Timeline, root cause, and what to do next.",
    mode="hybrid",
    llm_provider="openai",
    suggest_chain=True,
)
print(result.source)  # "hybrid"
print(result.suggested_chain)
print(result.to_markdown())
```

**Key API:** `suggest_patterns(..., mode="hybrid", llm_provider="openai")`.

---

### 16. Drop-in framework integration (e.g. LangChain)

**Pain:** You already use LangChain, CrewAI, or AutoGen; you want to plug in mycontext contexts without rewriting your pipeline.

**Solution:** Build or transform a context once, then export to the format your framework expects. Integrations provide helpers for LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel.

```python
from mycontext.intelligence import transform
from mycontext.integrations import LangChainHelper

context = transform("What are the top 3 risks for this launch?")
lc_messages = LangChainHelper.to_messages(context)
# Use lc_messages in your LangChain chain or agent
```

**Key API:** `context.to_langchain()`, `LangChainHelper.to_messages(context)`, and equivalent helpers for other frameworks.

---

## Next steps

- Run the companion notebook: `examples/key_use_cases_code_clippings.ipynb` (includes scenarios 1–10 and advanced 11–16).
- Try `context.execute(provider="openai")` (or your provider) with an API key for full LLM runs.
- Use a skill directory that contains `SKILL.md` (e.g. `examples/skills/compare_options`) for scenarios 12–14.
- See README and other docs for more patterns and integrations.
