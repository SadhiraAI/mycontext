"""Patch docs files with v0.5.0 updates."""
import re

EM = "\u2014"

# ── installation.md ──────────────────────────────────────────────────────────
path = r"c:\Users\dpokh\Desktop\mycontext\website\docs\getting-started\installation.md"
with open(path, encoding="utf-8") as f:
    c = f.read()

old = (
    "| **Intelligence Layer** | `transform()`, `suggest_patterns()`, `smart_execute()`, `smart_prompt()` |\n"
    "| **Quality Metrics** | 6-dimension context scoring + 5-dimension output evaluation |\n"
    f"| **CAI** | Context Amplification Index {EM} proves templates work |\n"
    "| **13 Export Formats** | OpenAI, Anthropic, Gemini, LangChain, YAML, JSON, XML, and more |\n"
    "| **7 Integrations** | LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel, Google ADK |"
)
new = (
    "| **Intelligence Layer** | `transform()`, `suggest_patterns()`, `smart_execute()`, `generate_context()` |\n"
    f"| **Async Execution** | `ctx.aexecute()` {EM} non-blocking LLM calls via `litellm.acompletion` |\n"
    f"| **Token-Budget Assembly** | `ctx.assemble_for_model(model, max_tokens)` {EM} tiktoken-accurate trimming |\n"
    "| **Validated Output Parsing** | Pydantic + `instructor` structured parsing with automatic retry |\n"
    "| **Quality Metrics** | 6-dimension context scoring + 5-dimension output evaluation |\n"
    f"| **CAI** | Context Amplification Index {EM} proves templates produce better output |\n"
    "| **13 Export Formats** | OpenAI, Anthropic, Gemini, LangChain, YAML, JSON, XML, and more |\n"
    "| **7 Integrations** | LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel, Google ADK |"
)
assert old in c, "installation table NOT FOUND"
c = c.replace(old, new)
with open(path, "w", encoding="utf-8") as f:
    f.write(c)
print("installation.md patched")
