---
sidebar_position: 1
title: Export Formats
description: Export any Context to JSON, YAML, XML, Markdown, OpenAI, Anthropic, Google, LangChain, LlamaIndex, CrewAI, AutoGen, and raw message arrays. One context, every format.
---

# Export Formats

Every `Context` object can be exported to 13+ formats. Build your context once using the foundation objects or a cognitive pattern, then deliver it in any shape downstream consumers need.

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

ctx = RootCauseAnalyzer().build_context(
    problem="API response times tripled after Friday's deployment",
    depth="comprehensive",
)

# Same context, different shapes
messages  = ctx.to_messages()          # OpenAI-style messages array
json_str  = ctx.to_json()              # JSON string
yaml_str  = ctx.to_yaml()              # YAML string
xml_str   = ctx.to_xml()              # XML string
md_str    = ctx.to_markdown()         # Human-readable Markdown
oai       = ctx.to_openai()           # Ready for openai.chat.completions.create()
ant       = ctx.to_anthropic()        # Ready for anthropic.messages.create()
goo       = ctx.to_google()           # Ready for genai.GenerativeModel.generate_content()
lc        = ctx.to_langchain()        # LangChain/LangGraph format
li        = ctx.to_llamaindex()       # LlamaIndex format
crew      = ctx.to_crewai()           # CrewAI Agent + Task format
ag        = ctx.to_autogen()          # AutoGen AssistantAgent format
d         = ctx.to_dict()             # Raw Python dict
raw       = ctx.assemble()            # Single assembled string
```

## Format Reference

### `to_messages(user_message?)`

The universal format. Compatible with OpenAI, Anthropic, and any provider that accepts a messages array.

```python
messages = ctx.to_messages()
# [{"role": "system", "content": "<full assembled context>"}]

messages = ctx.to_messages(user_message="Why did latency spike?")
# [
#   {"role": "system", "content": "<assembled context>"},
#   {"role": "user", "content": "Why did latency spike?"}
# ]
```

Use this when you want raw provider control:

```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=ctx.to_messages(user_message="Start the analysis"),
)
```

### `to_openai()`

Returns an OpenAI `chat.completions.create()` kwargs dict with defaults baked in:

```python
oai = ctx.to_openai()
# {
#   "messages": [...],    # from to_messages()
#   "temperature": 0.7,
#   "max_tokens": 4096
# }

response = client.chat.completions.create(**oai, model="gpt-4o-mini")
```

Override any default by unpacking and adding your own values:

```python
response = client.chat.completions.create(
    **ctx.to_openai(),
    model="gpt-4o",
    temperature=0,          # Override default 0.7
    max_tokens=8192,        # Override default 4096
)
```

### `to_anthropic()`

Returns an Anthropic `messages.create()` kwargs dict:

```python
ant = ctx.to_anthropic()
# {
#   "system": "<assembled context>",
#   "messages": [],
#   "max_tokens": 4096
# }

from anthropic import Anthropic
client = Anthropic()
response = client.messages.create(
    **ctx.to_anthropic(),
    model="claude-3-5-sonnet-20241022",
)
```

### `to_google()`

Returns kwargs for Google Gemini's `generate_content()`:

```python
goo = ctx.to_google()
# {
#   "contents": "<assembled context>",
#   "generation_config": {
#     "temperature": 0.7,
#     "max_output_tokens": 4096
#   }
# }

import google.generativeai as genai
model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content(**ctx.to_google())
```

### `to_json()`

Serializes the full context structure to a JSON string. Ideal for storage, caching, APIs, or language-agnostic consumption:

```python
json_str = ctx.to_json()
# {
#   "guidance": {
#     "role": "Root cause analysis specialist",
#     "rules": ["..."],
#     "style": "..."
#   },
#   "directive": { "content": "...", "priority": 1 },
#   "constraints": { ... },
#   "knowledge": null,
#   "data": { ... },
#   "metadata": { ... }
# }

# Save to file
with open("context.json", "w") as f:
    f.write(ctx.to_json())

# Round-trip
from mycontext import Context
restored = Context.from_json(json_str)
```

### `to_yaml()`

YAML format — great for config files, human editing, and version control:

```python
yaml_str = ctx.to_yaml()

# Save as config
with open("context.yaml", "w") as f:
    f.write(ctx.to_yaml())
```

Requires `pyyaml`: `pip install pyyaml`

### `to_xml()`

Pretty-printed XML with all fields as nested elements:

```xml
<?xml version="1.0" ?>
<context>
  <guidance>
    <role>Root cause analysis specialist</role>
    <rules>
      <rule>Identify all contributing factors...</rule>
    </rules>
  </guidance>
  <directive>
    <content>Analyze why our API latency tripled...</content>
    <priority>1</priority>
  </directive>
  <constraints>
    <must_include>
      <item>root cause</item>
      <item>remediation steps</item>
    </must_include>
  </constraints>
</context>
```

```python
xml_str = ctx.to_xml()
# Use with XML pipelines, SOAP APIs, or legacy systems
```

### `to_markdown()`

Human-readable Markdown. Ideal for documentation, debugging, code review, or displaying in UI:

```python
md = ctx.to_markdown()
print(md)
```

Output:

```markdown
# Context

## Guidance
**Role:** Root cause analysis specialist
**Rules:**
- Identify all contributing factors
- Distinguish immediate vs. root causes
**Style:** Analytical and precise

## Directive
Analyze why our API response times tripled...

## Constraints
**Must Include:**
- root cause
- contributing factors
- remediation steps
```

### `assemble()`

The raw assembled string — everything merged into a single prompt-ready text. This is what all other export formats use internally:

```python
text = ctx.assemble()
# Full system prompt as a single string

# Use directly with any SDK
import anthropic
response = anthropic.Anthropic().messages.create(
    model="claude-3-5-sonnet-20241022",
    system=ctx.assemble(),
    messages=[{"role": "user", "content": "Begin analysis"}],
    max_tokens=4096,
)
```

### `to_dict()` / `from_dict()`

Round-trip serialization to/from a plain Python dict:

```python
d = ctx.to_dict()
restored = Context.from_dict(d)

# Store in Redis, database, etc.
import redis
r = redis.Redis()
r.set("my_context", ctx.to_json())
stored = Context.from_json(r.get("my_context"))
```

### Framework Formats

These are covered in depth in the [Integrations](/docs/integrations/overview) section. Quick summary:

| Method | Use with |
|--------|----------|
| `to_langchain()` | `SystemMessage`, LCEL chains, LangGraph |
| `to_llamaindex()` | `VectorStoreIndex`, query engines |
| `to_crewai()` | `Agent`, `Task` constructors |
| `to_autogen()` | `AssistantAgent`, `ConversableAgent` |

## Format Selection Guide

| Goal | Format |
|------|--------|
| Direct OpenAI API call | `to_openai()` |
| Direct Anthropic API call | `to_anthropic()` |
| Direct Google Gemini call | `to_google()` |
| Any provider via messages | `to_messages()` |
| Full provider control | `assemble()` |
| Store / cache / transmit | `to_json()` |
| Config files, version control | `to_yaml()` |
| XML pipelines / legacy | `to_xml()` |
| Human review / debugging | `to_markdown()` |
| LangChain / LangGraph | `to_langchain()` |
| LlamaIndex | `to_llamaindex()` |
| CrewAI | `to_crewai()` |
| AutoGen | `to_autogen()` |

## Caching Contexts

Because contexts are serializable, you can cache expensive pattern builds:

```python
import json
from pathlib import Path
from mycontext import Context
from mycontext.templates.free.reasoning import RootCauseAnalyzer

CACHE = Path(".context_cache")
CACHE.mkdir(exist_ok=True)

def get_or_build(problem: str) -> Context:
    key = problem[:40].replace(" ", "_")
    cache_file = CACHE / f"{key}.json"
    
    if cache_file.exists():
        return Context.from_json(cache_file.read_text())
    
    ctx = RootCauseAnalyzer().build_context(problem=problem)
    cache_file.write_text(ctx.to_json())
    return ctx
```

## Streaming

For streaming responses, use `to_messages()` with the provider's streaming API directly:

```python
from openai import OpenAI

client = OpenAI()
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=ctx.to_messages(user_message="Analyze the issue"),
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```
