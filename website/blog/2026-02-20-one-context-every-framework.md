---
slug: one-context-every-framework
title: "One Context, Every Framework: Why We Built 13 Export Formats"
authors: [dhiraj]
tags: [integrations, langchain, crewai, autogen, context-engineering, mycontext-ai]
date: 2026-02-20
---

The AI framework landscape in early 2026 is messy in a specific way. There are good tools — LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel — and they serve genuinely different use cases. But they all want their own format. Their own message structure, their own agent config, their own prompt template shape.

The result is that if you want to experiment with your prompt across frameworks — or migrate from one to another — you end up rewriting the same context multiple times in different dialects.

We built mycontext-ai to fix this. The answer we landed on: **build your context once as a structured object, then export it to whatever shape the framework needs.**

<!-- truncate -->

## The fragmentation problem

Let me make this concrete. Say you have a well-designed context for a root cause analysis agent. You built it with care — good role definition, systematic analytical methodology, clear output constraints.

Now you want to try it in three different systems:

**LangChain:** needs a `SystemMessage` with the assembled prompt
**CrewAI:** needs `role`, `goal`, and `backstory` as separate strings for the `Agent` constructor, plus `expected_output` for the `Task`
**AutoGen:** needs `system_message` as a single string for `AssistantAgent`
**Direct Anthropic:** needs `system` as a string and `messages` as a separate list

Without a unified abstraction, you're maintaining four versions of the same context. They drift. They get inconsistent. When you improve one, you have to remember to update the others.

## The export approach

mycontext-ai's `Context` object has export methods for every major format:

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

ctx = RootCauseAnalyzer().build_context(
    problem="API latency tripled after deployment",
    depth="comprehensive",
)

# Each framework gets exactly the shape it expects
messages = ctx.to_messages()          # Standard messages array
oai     = ctx.to_openai()             # OpenAI kwargs dict
ant     = ctx.to_anthropic()          # Anthropic kwargs dict
goo     = ctx.to_google()             # Google Gemini kwargs dict
lc      = ctx.to_langchain()          # LangChain format
li      = ctx.to_llamaindex()         # LlamaIndex format
crew    = ctx.to_crewai()             # CrewAI Agent + Task dict
ag      = ctx.to_autogen()            # AutoGen format
raw     = ctx.assemble()              # Single string — works with anything
```

It's the same context, same analytical framework, same quality — just shaped differently for each consumer.

## Framework integrations in practice

The helper classes go further than just format conversion. They give you idiomatic integration with each framework's actual usage patterns.

**LangChain:**

```python
from mycontext.integrations import LangChainHelper
from langchain_openai import ChatOpenAI

helper = LangChainHelper(ctx)
chain = helper.to_lcel_chain(llm=ChatOpenAI(model="gpt-4o-mini"))
result = chain.invoke({"input": "Start the analysis"})
```

**CrewAI:**

```python
from mycontext.integrations import CrewAIHelper

helper = CrewAIHelper(ctx)
agent = helper.to_agent()  # crewai.Agent with role/goal/backstory populated
task  = helper.to_task()   # crewai.Task with description and expected_output
```

**AutoGen:**

```python
from mycontext.integrations import AutoGenHelper

helper = AutoGenHelper(ctx)
assistant = helper.to_assistant_agent(name="analyst")
# Ready to participate in multi-agent conversations
```

## Agent Skills: a portable standard for reusable instructions

Beyond individual contexts, we also support loading **Agent Skills** — `SKILL.md` files that follow a simple open standard for defining reusable agent instructions.

```python
from pathlib import Path
from mycontext.skills import SkillRunner

runner = SkillRunner()
result = runner.run(
    skill_path=Path("./skills/security-review"),
    task="Review this authentication handler",
    execute=True,
    provider="openai",
    quality_threshold=0.70,
)
```

A `SKILL.md` file travels with your project, can be shared across teams, and when loaded by `SkillRunner`, automatically gets quality-evaluated and optionally pattern-fused before execution.

Skills aren't a proprietary format — they're a simple YAML frontmatter + Markdown body convention. The integration with mycontext-ai is an extension of that standard.

## Why we support DSPy, Semantic Kernel, and Google ADK

We support six more frameworks beyond the most common ones. Let me explain why each matters.

**DSPy** is a different paradigm — instead of writing prompts, you write signatures and let the optimizer figure out the prompt. But you still need to seed your DSPy modules with a well-structured context. `ctx.assemble()` gives you that seed.

**Semantic Kernel** is Microsoft's SDK for building AI apps with a strong enterprise focus. If you're working in a Microsoft stack, Semantic Kernel is often the framework you're required to use. Having a clean integration path means you don't have to choose between mycontext-ai and your existing toolchain.

**Google ADK** is Google's framework for building multi-agent systems with Gemini. Its adoption is growing fast. The integration is straightforward — agent instructions map cleanly to `ctx.assemble()`.

## The honest trade-off

Supporting this many frameworks means each integration is necessarily somewhat shallow. We give you the basic conversion, not a deep wrapper around every framework feature.

For most use cases — passing a well-designed context into a framework's entry point — that's enough. For very specific framework features, you'll still need to read that framework's docs.

But the core value is there: you build the context once, to a quality standard, using a principled methodology, and then you can run it wherever you need to.

## auto_integrate for the impatient

If you just want a quick integration without choosing a specific helper:

```python
from mycontext.integrations import auto_integrate

result = auto_integrate(ctx, framework="langchain")
result = auto_integrate(ctx, framework="crewai")
result = auto_integrate(ctx, framework="autogen")
```

This handles the conversion automatically and returns the framework's native format.

---

All the integration documentation is in the [Integrations](/docs/integrations/overview) section. Each framework has its own page with usage examples and coverage of the less obvious use cases.

We're also adding integrations as new frameworks emerge. If there's one missing that matters to your workflow, open an issue on GitHub — we'll take a look.

— Dhiraj
