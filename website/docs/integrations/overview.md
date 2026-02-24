---
sidebar_position: 1
title: Integrations Overview
description: Use mycontext-ai with LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel, and Google ADK. Every Context exports to the right format for each framework.
---

# Integrations

mycontext-ai is framework-agnostic. Every `Context` object can export itself into the native format of any major AI framework — no adapters, no glue code, no fighting with APIs.

## How Integration Works

The `Context` object is the universal unit. Once you build one (from scratch or via a cognitive pattern), it can export itself to any framework:

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

# Build once
ctx = RootCauseAnalyzer().build_context(
    problem="API latency tripled after deployment",
    depth="comprehensive",
)

# Export anywhere
messages   = ctx.to_messages()          # OpenAI / universal messages
lc_format  = ctx.to_langchain()         # LangChain
li_format  = ctx.to_llamaindex()        # LlamaIndex
crew_cfg   = ctx.to_crewai()            # CrewAI Agent + Task
autogen_cfg = ctx.to_autogen()          # AutoGen AssistantAgent
```

## Supported Frameworks

| Framework | Install | Helper class | Native export |
|-----------|---------|-------------|--------------|
| [LangChain](./langchain) | `pip install langchain-core` | `LangChainHelper` | `ctx.to_langchain()` |
| [LlamaIndex](./llamaindex) | `pip install llama-index` | `LlamaIndexHelper` | `ctx.to_llamaindex()` |
| [CrewAI](./crewai) | `pip install crewai` | `CrewAIHelper` | `ctx.to_crewai()` |
| [AutoGen](./autogen) | `pip install pyautogen` | `AutoGenHelper` | `ctx.to_autogen()` |
| [DSPy](./dspy) | `pip install dspy-ai` | `DSPyHelper` | `ctx.assemble()` |
| [Semantic Kernel](./semantic-kernel) | `pip install semantic-kernel` | `SemanticKernelHelper` | `ctx.assemble()` |
| [Google ADK](./google-adk) | `pip install google-adk` | `GoogleADKHelper` | `ctx.assemble()` |

## Two Integration Paths

### Path 1: Native Context export methods

Every `Context` has built-in export methods:

```python
from mycontext import Context
from mycontext.foundation import Guidance, Directive

ctx = Context(
    guidance=Guidance(role="Senior data analyst"),
    directive=Directive(content="Identify anomalies in the sales data"),
)

# Universal messages format
messages = ctx.to_messages()
# → [{"role": "system", "content": "..."}]

# LangChain
lc = ctx.to_langchain()
# → {"system_message": "...", "context": {...}}

# CrewAI
crew = ctx.to_crewai()
# → {"role": "...", "goal": "...", "backstory": "...", "expected_output": "..."}

# AutoGen
ag = ctx.to_autogen()
# → {"system_message": "...", "description": "...", ...}

# LlamaIndex
li = ctx.to_llamaindex()
# → {"template": "...", "system_prompt": "...", "query_instruction": "..."}

# Provider-specific
openai_cfg  = ctx.to_openai()     # {"messages": [...], "temperature": 0.7}
anthropic_cfg = ctx.to_anthropic() # {"system": "...", "messages": [...]}
```

### Path 2: Helper classes

The helper classes add framework-specific functionality on top of the export methods:

```python
from mycontext.integrations import (
    LangChainHelper,
    LlamaIndexHelper,
    CrewAIHelper,
    AutoGenHelper,
    DSPyHelper,
    SemanticKernelHelper,
    GoogleADKHelper,
)
```

### `auto_integrate()` — One-liner

```python
from mycontext.integrations import auto_integrate

ctx = RootCauseAnalyzer().build_context(problem="API latency spiked")

# Detect and export automatically
messages = auto_integrate(ctx, "langchain")
agent    = auto_integrate(ctx, "crewai", name="analyst", tools=my_tools)
prompt   = auto_integrate(ctx, "dspy")
adk_agent = auto_integrate(ctx, "google_adk", name="diagnostician")
```

**Supported framework strings:** `"langchain"`, `"llamaindex"`, `"crewai"`, `"autogen"`, `"dspy"`, `"semantic_kernel"`, `"google_adk"`

## The Shared Pattern

Every integration follows the same pattern:

```
1. Build a Context (from scratch or via a cognitive pattern)
2. Export it to the framework's native format
3. Use the framework normally — mycontext just powered the prompt
```

This means your framework code doesn't change. You're just replacing ad-hoc system prompts with research-backed cognitive frameworks.

## All Context Export Methods

| Method | Returns | Use with |
|--------|---------|---------|
| `ctx.to_messages()` | `list[dict]` | Any OpenAI-compatible API |
| `ctx.to_openai()` | `dict` | OpenAI Python client |
| `ctx.to_anthropic()` | `dict` | Anthropic Python client |
| `ctx.to_langchain()` | `dict` | LangChain / LangGraph |
| `ctx.to_llamaindex()` | `dict` | LlamaIndex query/chat engines |
| `ctx.to_crewai()` | `dict` | CrewAI Agent + Task |
| `ctx.to_autogen()` | `dict` | AutoGen AssistantAgent |
| `ctx.assemble()` | `str` | Any framework accepting a string |
| `ctx.to_markdown()` | `str` | Documentation, debugging |
| `ctx.to_json()` | `str` | Storage, APIs |
| `ctx.to_yaml()` | `str` | Config files |
| `ctx.to_xml()` | `str` | XML-based systems |

## Install Integration Dependencies

```bash
# Install only what you need
pip install mycontext-ai                  # Core only

pip install mycontext-ai langchain-core   # + LangChain
pip install mycontext-ai llama-index      # + LlamaIndex
pip install mycontext-ai crewai           # + CrewAI
pip install mycontext-ai pyautogen        # + AutoGen
pip install mycontext-ai dspy-ai          # + DSPy
pip install mycontext-ai semantic-kernel  # + Semantic Kernel
pip install mycontext-ai google-adk       # + Google ADK

# Or all at once
pip install "mycontext-ai[all]"
```
