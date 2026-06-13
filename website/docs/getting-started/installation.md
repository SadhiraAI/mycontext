---
sidebar_position: 1
title: Installation
description: Install mycontext-ai with pip, uv, poetry, or conda. Configure providers and verify your setup.
---

# Installation

Get mycontext-ai installed and ready in under a minute.

## Requirements

- **Python 3.11+** — [Download Python](https://www.python.org/downloads/)
- **pip**, **uv**, **poetry**, or **conda** as your package manager

## Install the SDK

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs groupId="package-manager">
  <TabItem value="pip" label="pip" default>

```bash
pip install mycontext-ai
```

  </TabItem>
  <TabItem value="uv" label="uv">

```bash
uv add mycontext-ai
```

  </TabItem>
  <TabItem value="poetry" label="Poetry">

```bash
poetry add mycontext-ai
```

  </TabItem>
  <TabItem value="conda" label="Conda">

```bash
conda install -c conda-forge mycontext-ai
```

  </TabItem>
</Tabs>

This installs the core SDK with **all 88 cognitive patterns** (open source — no tiers or license keys), the full intelligence layer, quality metrics, and all 13 export formats.

## Add LLM Execution (Recommended)

To execute contexts against LLMs, install with LiteLLM — which gives you access to **100+ LLM providers** through a single interface:

<Tabs groupId="package-manager">
  <TabItem value="pip" label="pip" default>

```bash
pip install mycontext-ai litellm
```

  </TabItem>
  <TabItem value="uv" label="uv">

```bash
uv add mycontext-ai litellm
```

  </TabItem>
  <TabItem value="poetry" label="Poetry">

```bash
poetry add mycontext-ai litellm
```

  </TabItem>
</Tabs>

## Provider-Specific Extras

Install the official SDK for your preferred provider:

<Tabs groupId="package-manager">
  <TabItem value="pip" label="pip" default>

```bash
# OpenAI
pip install "mycontext-ai[openai]"

# Anthropic (Claude)
pip install "mycontext-ai[anthropic]"

# Google (Gemini)
pip install "mycontext-ai[google]"

# All providers at once
pip install "mycontext-ai[all]"
```

  </TabItem>
  <TabItem value="uv" label="uv">

```bash
# OpenAI
uv add "mycontext-ai[openai]"

# Anthropic (Claude)
uv add "mycontext-ai[anthropic]"

# Google (Gemini)
uv add "mycontext-ai[google]"

# All providers
uv add "mycontext-ai[all]"
```

  </TabItem>
  <TabItem value="poetry" label="Poetry">

```bash
# OpenAI
poetry add "mycontext-ai[openai]"

# Anthropic (Claude)
poetry add "mycontext-ai[anthropic]"

# Google (Gemini)
poetry add "mycontext-ai[google]"

# All providers
poetry add "mycontext-ai[all]"
```

  </TabItem>
</Tabs>

### What each extra includes

| Extra | Package | Use case |
|-------|---------|----------|
| `openai` | `openai>=2.0.0` | Direct OpenAI API usage |
| `anthropic` | `anthropic>=0.79.0` | Direct Anthropic API usage |
| `google` | `google-genai>=1.0.0` | Direct Google Gemini API usage |
| `tokens` | `tiktoken>=0.7.0` | Token counting and optimization |
| `all` | All of the above | Full provider support |

:::tip You don't need provider extras for basic usage
LiteLLM handles routing to all providers. The extras install the provider's own SDK for cases where you need direct API access.
:::

## Optional: Structured Output Parsing

Install `instructor` to enable JSON-mode LLM output with automatic retry on validation failure in the intelligence layer:

```bash
pip install instructor
```

When installed, all intelligence-layer LLM calls (`suggest_patterns`, `generate_context`, `TemplateIntegratorAgent`) use structured function-calling mode (~98% parse success). Without it, the SDK falls back to its Pydantic + regex parser transparently — no code changes needed.

## Optional: Accurate Token Counting

For `assemble_for_model()` token-budget assembly and token-aware context trimming, install `tiktoken`:

```bash
pip install "mycontext-ai[tokens]"
# or directly:
pip install tiktoken
```

Without `tiktoken`, the SDK falls back to character-based estimation. Install `[all]` to get everything at once.

## Orchestration Extras

If you're integrating with agent frameworks:

```bash
pip install "mycontext-ai[orchestration]"
```

This includes LangChain, LangGraph, CrewAI, AutoGen, and Semantic Kernel.

## Development Install

To contribute to mycontext-ai or develop locally:

```bash
git clone https://github.com/SadhiraAI/mycontext.git
cd mycontext
pip install -e ".[dev]"
```

This installs the SDK in editable mode with pytest, mypy, ruff, black, and other dev tools.

## Verify Installation

```bash
python -c "import mycontext; print(f'mycontext-ai v{mycontext.__version__} installed successfully')"
```

Expected output:

```
mycontext-ai v0.6.0 installed successfully
```

## Command-Line Interface

The package installs a `mycontext` console script for working with patterns and exporting agent skills — all offline:

```bash
mycontext list                                 # list all 88 patterns
mycontext run root_cause_analyzer --generic    # print a pre-authored prompt
mycontext skills export all -o ./skills        # export progressive-disclosure SKILL.md packages
mycontext mcp                                  # start the local stdio MCP server
```

The local MCP server requires the optional `mcp` extra:

```bash
pip install "mycontext-ai[mcp]"
```

See the [CLI reference](../cli/overview) for full details.

## Configure Your API Key

Set the API key for your LLM provider as an environment variable:

<Tabs>
  <TabItem value="openai" label="OpenAI" default>

```bash
export OPENAI_API_KEY="sk-..."
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "sk-..."
```

  </TabItem>
  <TabItem value="anthropic" label="Anthropic">

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

  </TabItem>
  <TabItem value="google" label="Google">

```bash
export GOOGLE_API_KEY="AI..."
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY = "AI..."
```

  </TabItem>
</Tabs>

Or use a `.env` file in your project root:

```bash title=".env"
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AI...
```

:::info No API key needed for context building
You only need an API key when **executing** contexts against an LLM (`ctx.execute()`, `smart_execute()`, etc.). Building, exporting, and scoring contexts works entirely offline.
:::

## What's Included

| Component | Description |
|-----------|-------------|
| **Core SDK** | `Context`, `Guidance`, `Directive`, `Constraints` classes |
| **88 Cognitive Patterns** | All open source — RootCauseAnalyzer, CodeReviewer, DecisionFramework, and 85 more |
| **CLI** | `mycontext` console script — `list`, `run`, `skills export`, `mcp` |
| **Intelligence Layer** | `transform()`, `suggest_patterns()`, `smart_execute()`, `generate_context()` |
| **Async Execution** | `ctx.aexecute()` — non-blocking LLM calls via `litellm.acompletion` |
| **Token-Budget Assembly** | `ctx.assemble_for_model(model, max_tokens)` — tiktoken-accurate trimming |
| **Validated Output Parsing** | Pydantic + `instructor` structured parsing with automatic retry |
| **Quality Metrics** | 6-dimension context scoring + 5-dimension output evaluation |
| **CAI** | Context Amplification Index — proves templates produce better output |
| **13 Export Formats** | OpenAI, Anthropic, Gemini, LangChain, YAML, JSON, XML, and more |
| **7 Integrations** | LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel, Google ADK |

## Troubleshooting

### `ModuleNotFoundError: No module named 'mycontext'`

Make sure you installed the package (not a directory named `mycontext`):

```bash
pip install mycontext-ai  # ← correct
# NOT: pip install mycontext
```

### Python version errors

mycontext-ai requires Python 3.11+. Check your version:

```bash
python --version
```

If you have multiple Python versions, try:

```bash
python3.11 -m pip install mycontext-ai
# or
python3.12 -m pip install mycontext-ai
```

### LiteLLM import errors

If you see errors related to LiteLLM, install it explicitly:

```bash
pip install litellm>=1.55.0
```

---

**Next:** [Quick Start →](./quickstart)
