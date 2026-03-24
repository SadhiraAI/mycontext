---
sidebar_position: 1
title: Context Object
description: Complete reference for the Context class — the central object that combines Guidance, Directive, Constraints, and Knowledge into a portable, provider-agnostic unit.
---

# Context Object

The `Context` is the central object in mycontext-ai. It combines everything an LLM needs — role, instructions, guardrails, and knowledge — into a single portable unit that exports to any provider or framework.

## Import

```python
from mycontext import Context
# or
from mycontext.core import Context
```

## Constructor

```python
Context(
    guidance: str | Guidance | None = None,
    directive: str | Directive | None = None,
    constraints: Constraints | None = None,
    knowledge: str | None = None,
    data: dict = {},
    metadata: dict = {},
    thinking_strategy: str | None = None,
    examples: list[dict[str, str]] | None = None,
    research_flow: bool = False,
    provider_hint: str | None = None,  # "openai" | "anthropic" | "gemini" | "generic"
    task_contract: TaskContract | None = None,
)
```

Strings are automatically promoted to their corresponding objects:

```python
# String shorthand — both are equivalent
ctx = Context("You are a senior data analyst")
ctx = Context(guidance=Guidance(role="You are a senior data analyst"))
```

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `guidance` | `Guidance \| str \| None` | No | System-level behavioral rules — who the AI is |
| `directive` | `Directive \| str \| None` | No | The specific task — what the AI should do |
| `constraints` | `Constraints \| None` | No | Hard limits and guardrails |
| `knowledge` | `str \| None` | No | Retrieved documents, memory, or domain context |
| `data` | `dict` | No | Arbitrary key-value inputs passed to templates |
| `metadata` | `dict` | No | Tags, version info, pattern name, etc. |
| `thinking_strategy` | `str \| None` | No | Reasoning strategy injected before the task. Options: `step_by_step`, `multiple_angles`, `verify`, `explain_simply`, `creative` |
| `examples` | `list[dict] \| None` | No | Few-shot examples as `[{"input": "...", "output": "..."}]` |
| `research_flow` | `bool` | No | When `True`, uses research-backed 9-section prompt ordering. Default: `False` |
| `provider_hint` | `str \| None` | No | Target provider for assembly tweaks (`openai`, `anthropic`, `gemini`). Does not change `execute()` routing. |
| `task_contract` | `TaskContract \| None` | No | L0 metadata (domain, audience, genre, grounding, metaphor). Rendered first when `research_flow=True`. See [Task Contract](./task-contract). |

## Basic Usage

```python
from mycontext import Context, Guidance, Directive, Constraints

ctx = Context(
    guidance=Guidance(
        role="Senior security engineer",
        rules=["Prioritize security over convenience", "Always suggest concrete fixes"],
        style="concise, actionable",
    ),
    directive=Directive(
        content="Audit this authentication middleware for vulnerabilities.",
        priority=9,
    ),
    constraints=Constraints(
        must_include=["severity rating", "code fix example"],
        must_not_include=["generic disclaimers"],
        format_rules=["Use markdown tables for findings"],
    ),
    knowledge="OWASP Top 10 2023: A01 Broken Access Control, A02 Cryptographic Failures...",
)
```

## Assembly

`assemble()` converts the Context into the formatted text sent to the LLM. With `research_flow=True`, if you set `task_contract` (or legacy `metadata["l0"]`), an **L0 — TASK CONTRACT** table is rendered **before** the nine main sections:

```
L0 TASK CONTRACT (optional) → ① ROLE → ② GOAL → … → ⑨ TASK
```

Otherwise the main chain is:

```
① ROLE → ② GOAL → ③ RULES → ④ STYLE → ⑤ REASONING → ⑥ EXAMPLES → ⑦ OUTPUT FORMAT → ⑧ GUARD RAILS → ⑨ TASK
```

Sections that have no corresponding data are omitted automatically. The task (`directive`) always appears last.

```python
ctx = Context(
    guidance=Guidance(
        role="Senior security engineer",
        goal="Find all exploitable vulnerabilities and give concrete fixes",
        rules=["Flag every OWASP Top 10 risk", "Always include a severity rating"],
        style="direct and actionable",
    ),
    directive=Directive("Audit this authentication middleware: ..."),
    thinking_strategy="step_by_step",
    examples=[
        {"input": "session.permanent = True", "output": "Medium — sessions never expire, add a timeout"},
    ],
    constraints=Constraints(must_include=["severity", "fix example"]),
    research_flow=True,
)

text = ctx.assemble()
```

See [Prompt Assembly & Thinking Strategies →](./research-flow) for a full walkthrough of every section and the reasoning behind the ordering.

## Thinking Strategies

`thinking_strategy` injects a structured reasoning instruction into section ⑤ of the assembled prompt — positioned between style and examples so the model understands how to reason before it sees demonstrations.

| Key | Cognitive approach | When to reach for it |
|-----|--------------------|----------------------|
| `step_by_step` | Chain of Thought | Multi-step reasoning, debugging, analysis where the path matters |
| `multiple_angles` | Tree of Thought | Decisions with genuine trade-offs — explore before converging |
| `verify` | Self-Reflection | High-stakes outputs where errors are costly |
| `explain_simply` | Simplification | Non-technical audiences, onboarding, user-facing content |
| `creative` | Divergent Thinking | Ideation, reframing, novelty is the explicit goal |

```python
ctx = Context(
    guidance=Guidance(role="Expert code reviewer"),
    directive=Directive("Review this pull request for correctness and security"),
    thinking_strategy="verify",
    research_flow=True,
)
```

Each strategy has detailed criteria for when it applies. See [Prompt Assembly & Thinking Strategies →](./research-flow) for the complete guide.

## Few-Shot Examples

`examples` provides input→output demonstrations that calibrate the model's format and reasoning style. They appear in section ⑥ — after the reasoning strategy, before guard rails:

```python
ctx = Context(
    guidance=Guidance(role="Sentiment analyst"),
    directive=Directive("Classify this review: ..."),
    examples=[
        {"input": "Best purchase ever!", "output": "Positive — confidence: 0.95"},
        {"input": "Broke after a week.", "output": "Negative — confidence: 0.88"},
        {"input": "Fast delivery but bad quality.", "output": "Mixed — confidence: 0.80"},
    ],
    research_flow=True,
)
```

Use 2–4 examples. Aim for variety that covers edge cases and boundary conditions, not just the happy path.

## Execution

Execute a context against any LLM via LiteLLM:

```python
result = ctx.execute(provider="openai")
print(result.response)

# Switch providers with no code changes
result = ctx.execute(provider="anthropic")
result = ctx.execute(provider="google")

# Pass model or other LLM kwargs
result = ctx.execute(provider="openai", model="gpt-4o", temperature=0.3)
```

:::info
`ctx.execute()` requires `litellm` and a valid API key. Set `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GOOGLE_API_KEY` as environment variables.
:::

### Async Execution

`aexecute()` is a native `async` coroutine — no blocking, no thread pools. Use it directly in `async` applications, FastAPI routes, and agent loops:

```python
import asyncio

result = await ctx.aexecute(provider="openai", model="gpt-4o-mini")
print(result.response)

# Fan out multiple contexts concurrently
results = await asyncio.gather(
    ctx1.aexecute(provider="openai"),
    ctx2.aexecute(provider="anthropic"),
)
```

See [Async Execution →](../intelligence/async-execution) for patterns and best practices.

## Prompt Export

Convert a context into a reusable prompt string without executing it:

```python
# Zero-cost: restructures the context into a clean prompt (no LLM call)
prompt = ctx.to_prompt()

# LLM-refined: distills the cognitive framework into an optimized 800-1200 char prompt
prompt = ctx.to_prompt(refine=True, provider="openai", model="gpt-4o-mini")
```

The refined prompt is self-contained and provider-agnostic — it can be executed on any LLM.

### Token-Budget Assembly

`assemble_for_model()` builds a prompt guaranteed to fit within a model's context window. Sections are prioritised and trimmed using `tiktoken` — accurate to the token, not a character estimate:

```python
# Fit into gpt-4o-mini's default window
prompt = ctx.assemble_for_model(model="gpt-4o-mini")

# Cap at a custom budget (e.g., leaving room for response tokens)
prompt = ctx.assemble_for_model(model="gpt-4o", max_tokens=2000)
```

Without `tiktoken`, the SDK falls back to a safe character-based estimate. Install via `pip install tiktoken` or `pip install "mycontext-ai[tokens]"`.

See [Token-Budget Assembly →](../intelligence/token-budget) for full details.

## Export Formats

One context, 13 output formats. Build once, run anywhere.

### Provider Formats

```python
# OpenAI Chat API — {"messages": [...], "temperature": 0.7, "max_tokens": 4096}
payload = ctx.to_openai()
from openai import OpenAI
response = OpenAI().chat.completions.create(**payload, model="gpt-4o")

# Anthropic Claude — {"system": "...", "messages": [], "max_tokens": 4096}
payload = ctx.to_anthropic()
from anthropic import Anthropic
response = Anthropic().messages.create(**payload, model="claude-3-5-sonnet-20241022")

# Google Gemini — {"contents": "...", "generation_config": {...}}
payload = ctx.to_google()
```

### Framework Formats

```python
# LangChain — {"system_message": "...", "context": {...}, ...}
lc = ctx.to_langchain()
from langchain_core.messages import SystemMessage
msg = SystemMessage(content=lc["system_message"])

# LlamaIndex — {"template": "...", "system_prompt": "...", ...}
li = ctx.to_llamaindex()

# CrewAI — {"role": "...", "goal": "...", "backstory": "...", "expected_output": "..."}
crew = ctx.to_crewai()
from crewai import Agent, Task
agent = Agent(role=crew["role"], goal=crew["goal"], backstory=crew["backstory"])
task = Task(description=crew["goal"], expected_output=crew["expected_output"])

# AutoGen — {"system_message": "...", "description": "...", ...}
ag = ctx.to_autogen()
from autogen import AssistantAgent
agent = AssistantAgent(name="analyst", system_message=ag["system_message"])
```

### Serialization Formats

```python
# Universal message list — OpenAI-compatible
messages = ctx.to_messages()
messages = ctx.to_messages(user_message="What are the top risks?")
# → [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]

# Human-readable Markdown
md = ctx.to_markdown()

# JSON string
json_str = ctx.to_json()

# YAML string (requires pyyaml)
yaml_str = ctx.to_yaml()

# XML string
xml_str = ctx.to_xml()

# Python dict
d = ctx.to_dict()
```

## Serialization & Deserialization

Round-trip a context through JSON:

```python
# Serialize
json_str = ctx.to_json()

# Deserialize
ctx2 = Context.from_json(json_str)

# Or via dict
d = ctx.to_dict()
ctx3 = Context.from_dict(d)
```

## Build from an Agent Skill

Load a context from a SKILL.md file:

```python
from pathlib import Path
from mycontext import Context

ctx = Context.from_skill(
    Path("my_skill/"),
    task="Compare microservices vs monolith",
)
```

This is a convenience wrapper for `SkillRunner().build_context()`. See [Agent Skills](../advanced/agent-skills) for full details.

## The `data` and `metadata` fields

`data` holds arbitrary key-value inputs — typically the template's variable substitutions:

```python
ctx = Context(
    directive=Directive(content="Analyze the {industry} market for {company}."),
    data={"industry": "fintech", "company": "Acme Corp"},
)
```

`metadata` is populated automatically by templates and blueprints, and is useful for tracking:

```python
# After building from a pattern:
ctx.metadata["pattern"]         # "root_cause_analyzer"
ctx.metadata["pattern_version"] # "1.0.0"

# After building from a blueprint:
ctx.metadata["blueprint"]       # "research_assistant"
ctx.metadata["token_budget"]    # 4000
ctx.metadata["optimization"]    # "balanced"
```

## String Representation

```python
ctx = Context(
    guidance=Guidance(role="Expert analyst"),
    directive=Directive(content="Analyze quarterly revenue trends"),
)
print(repr(ctx))
# Context(guidance=Expert analyst, directive=Analyze quarterly revenue trends...)
```

## Full API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `assemble()` | `str` | Combine all fields into the text sent to the LLM |
| `assemble_for_model(model, max_tokens?)` | `str` | Token-budget-aware assembly — trims to fit within the model's window |
| `execute(provider, **kwargs)` | `ProviderResponse` | Execute against an LLM (synchronous) |
| `aexecute(provider, **kwargs)` | `Coroutine[ProviderResponse]` | Execute asynchronously — native `async`/`await` |
| `to_prompt(refine, provider, model)` | `str` | Export as a reusable prompt string (zero-cost or LLM-refined) |
| `to_messages(user_message)` | `list[dict]` | Universal message list |
| `to_openai()` | `dict` | OpenAI Chat API format |
| `to_anthropic()` | `dict` | Anthropic Claude format |
| `to_google()` | `dict` | Google Gemini format |
| `to_langchain()` | `dict` | LangChain integration format |
| `to_llamaindex()` | `dict` | LlamaIndex integration format |
| `to_crewai()` | `dict` | CrewAI Agent/Task format |
| `to_autogen()` | `dict` | AutoGen agent format |
| `to_markdown()` | `str` | Human-readable Markdown |
| `to_json()` | `str` | JSON string |
| `to_yaml()` | `str` | YAML string |
| `to_xml()` | `str` | XML string |
| `to_dict()` | `dict` | Python dictionary |
| `from_dict(data)` | `Context` | Deserialize from dict |
| `from_json(json_str)` | `Context` | Deserialize from JSON |
| `from_skill(path, task, **params)` | `Context` | Build from SKILL.md |

---

**Next:** [Guidance →](./guidance)
