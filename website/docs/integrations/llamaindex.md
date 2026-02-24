---
sidebar_position: 3
title: LlamaIndex
description: Power LlamaIndex query engines and chat engines with mycontext cognitive patterns. Use any Context as a system prompt or text QA template.
---

# LlamaIndex

Use mycontext cognitive patterns as the system prompt or QA template in LlamaIndex query and chat engines. The `to_llamaindex()` export provides the right format for LlamaIndex's engine constructors.

```bash
pip install mycontext-ai llama-index llama-index-llms-openai
```

## Quick Start

```python
from mycontext.templates.free.analysis import DataAnalyzer
from mycontext.integrations import LlamaIndexHelper
from llama_index.core import VectorStoreIndex, Document

# Build cognitive context
ctx = DataAnalyzer().build_context(
    data_description="Customer support tickets and usage logs",
    goal="Identify churn risk patterns",
)

# Build index from your documents
documents = [Document(text=doc) for doc in your_documents]
index = VectorStoreIndex.from_documents(documents)

# Create query engine powered by mycontext
query_engine = LlamaIndexHelper.create_query_engine(index, ctx)
response = query_engine.query("What patterns correlate with customer churn?")
print(response)
```

## `ctx.to_llamaindex()`

The native export returns a dict with all LlamaIndex-compatible formats:

```python
li = ctx.to_llamaindex()
# {
#   "template": "## Role\nSenior data analyst...\n## Directive\n...",
#   "system_prompt": "You are a Senior data analyst...",
#   "query_instruction": "Identify churn risk patterns...",
#   "context_str": "## Role\n...",
#   "metadata": {...}
# }
```

## LlamaIndexHelper Methods

### `create_query_engine(index, context, **kwargs)`

Creates a query engine with the mycontext system prompt:

```python
from mycontext.integrations import LlamaIndexHelper

query_engine = LlamaIndexHelper.create_query_engine(
    index=index,
    context=ctx,
    similarity_top_k=5,  # LlamaIndex kwargs pass through
)

response = query_engine.query("Your question here")
print(str(response))
```

### `create_chat_engine(index, context, **kwargs)`

Creates a chat engine with the mycontext system prompt:

```python
chat_engine = LlamaIndexHelper.create_chat_engine(
    index=index,
    context=ctx,
    chat_mode="condense_plus_context",
)

response = chat_engine.chat("What are the main risk factors?")
print(str(response))
```

### `to_prompt(context)`

Returns the assembled context as a plain string for manual use:

```python
prompt = LlamaIndexHelper.to_prompt(ctx)
# Use directly as system_prompt in any LlamaIndex component
```

## Query Engine with Custom LLM

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.integrations import LlamaIndexHelper
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI

ctx = RootCauseAnalyzer().build_context(
    problem="Support ticket volume up 300% after last release",
    depth="thorough",
)

llm = OpenAI(model="gpt-4o-mini", temperature=0)
index = VectorStoreIndex.from_documents(your_documents)

query_engine = LlamaIndexHelper.create_query_engine(
    index=index,
    context=ctx,
    llm=llm,
    similarity_top_k=10,
)

response = query_engine.query(
    "What release changes correlate with the support ticket spike?"
)
print(str(response))
```

## Document Analysis Pipeline

Use a cognitive pattern to analyze a set of documents:

```python
from mycontext.templates.free.specialized import SynthesisBuilder
from mycontext.integrations import LlamaIndexHelper
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load your documents
documents = SimpleDirectoryReader("./reports").load_data()
index = VectorStoreIndex.from_documents(documents)

# Synthesis context
ctx = SynthesisBuilder().build_context(
    sources="Multiple quarterly reports and market analyses",
    goal="Synthesize key trends and strategic implications",
)

query_engine = LlamaIndexHelper.create_query_engine(index, ctx)

questions = [
    "What are the 3 most significant trends across all reports?",
    "Where do the reports contradict each other?",
    "What are the strategic implications for 2026?",
]

for q in questions:
    print(f"\nQ: {q}")
    print(f"A: {query_engine.query(q)}")
```

## API Reference

### `LlamaIndexHelper`

| Method | Returns | Description |
|--------|---------|-------------|
| `to_prompt(context)` | `str` | Assembled context as string |
| `create_query_engine(index, context, **kwargs)` | query engine | LlamaIndex query engine |
| `create_chat_engine(index, context, **kwargs)` | chat engine | LlamaIndex chat engine |

### `ctx.to_llamaindex()`

```python
{
    "template": str,           # Full assembled context
    "system_prompt": str,      # Guidance section only
    "query_instruction": str,  # Directive section only
    "context_str": str,        # Full assembled context (alias)
    "metadata": dict,          # Context metadata
}
```
