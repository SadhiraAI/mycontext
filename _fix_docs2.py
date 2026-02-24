"""Patch docs files — context-object, api overview, intelligence overview, quickstart."""

EM = "\u2014"

# ── context-object.md: Full API Reference table ───────────────────────────────
path = r"c:\Users\dpokh\Desktop\mycontext\website\docs\foundations\context-object.md"
with open(path, encoding="utf-8") as f:
    c = f.read()

old = (
    "| `assemble()` | `str` | Combine all fields into the text sent to the LLM. Uses classic or research-backed ordering depending on `research_flow` |\n"
    "| `execute(provider, **kwargs)` | `ProviderResponse` | Execute against an LLM |\n"
    "| `to_prompt(refine, provider, model)` | `str` | Export as a reusable prompt string (zero-cost or LLM-refined) |\n"
    "| `to_messages(user_message)` | `list[dict]` | Universal message list |"
)
new = (
    "| `assemble()` | `str` | Combine all fields into the text sent to the LLM |\n"
    f"| `assemble_for_model(model, max_tokens?)` | `str` | Token-budget-aware assembly {EM} trims to fit within the model's window |\n"
    "| `execute(provider, **kwargs)` | `ProviderResponse` | Execute against an LLM (synchronous) |\n"
    "| `aexecute(provider, **kwargs)` | `Coroutine[ProviderResponse]` | Execute asynchronously {EM} native `async`/`await` |\n".format(EM=EM)
    + "| `to_prompt(refine, provider, model)` | `str` | Export as a reusable prompt string (zero-cost or LLM-refined) |\n"
    "| `to_messages(user_message)` | `list[dict]` | Universal message list |"
)
assert old in c, f"context-object table NOT FOUND\n---\n{repr(c[c.find('assemble()'):c.find('assemble()')+200])}"
c = c.replace(old, new)
with open(path, "w", encoding="utf-8") as f:
    f.write(c)
print("context-object.md patched")


# ── api/overview.md: Context.execute section ─────────────────────────────────
path = r"c:\Users\dpokh\Desktop\mycontext\website\docs\api\overview.md"
with open(path, encoding="utf-8") as f:
    c = f.read()

old_exec = (
    "| `execute` | `execute(provider, **kwargs)` | `ProviderResponse` | Run with an LLM |\n"
    "| `to_prompt` | `to_prompt(refine=False, provider=\"openai\", model=\"gpt-4o-mini\")` | `str` | Zero-cost restructuring (`refine=False`) or LLM-distilled prompt (`refine=True`) |"
)
new_exec = (
    "| `execute` | `execute(provider, **kwargs)` | `ProviderResponse` | Run with an LLM (synchronous) |\n"
    f"| `aexecute` | `aexecute(provider, **kwargs)` | `Coroutine[ProviderResponse]` | Run asynchronously {EM} native `async`/`await` |\n"
    f"| `assemble_for_model` | `assemble_for_model(model, max_tokens?)` | `str` | Token-budget assembly {EM} tiktoken-accurate, trims to fit |\n"
    "| `to_prompt` | `to_prompt(refine=False, provider=\"openai\", model=\"gpt-4o-mini\")` | `str` | Zero-cost restructuring (`refine=False`) or LLM-distilled prompt (`refine=True`) |"
)
if old_exec in c:
    c = c.replace(old_exec, new_exec)
    print("api/overview.md Execution section patched")
else:
    print("api/overview.md Execution section NOT FOUND — skipping")

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

print("Done.")
