---
sidebar_position: 5
title: Prompt Compilation
description: PromptComposer merges multiple template-generated prompts into one comprehensive, non-redundant prompt. Two modes — LLM-refined composition and zero-cost static compilation.
---

# Prompt Compilation

`PromptComposer` merges multiple template-generated prompts into a single, comprehensive prompt. Instead of running templates sequentially and integrating their outputs (which consumes output tokens), it generates compact prompts from each template and fuses them — then executes once.

```python
from mycontext.intelligence import PromptComposer

composer = PromptComposer()
result = composer.compose_from_templates(
    question="Why did churn spike 40%?",
    template_names=["root_cause_analyzer", "data_analyzer", "decision_framework"],
)
print(result.to_string())   # The composed prompt
response = result.execute(provider="openai")
```

## Why Prompt Compilation?

The naive approach to multi-template reasoning runs each template, gets a response, and tries to synthesize:

```
Template 1 → Response A (1000 tokens out)
Template 2 → Response B (1000 tokens out)
Template 3 → Response C (1000 tokens out)
Synthesis → Final answer (1000 tokens out)
= 4 LLM calls, 4000 output tokens
```

Prompt compilation instead:
```
Template 1 → Prompt component (200 tokens)
Template 2 → Prompt component (200 tokens)
Template 3 → Prompt component (200 tokens)
Compose → Merged prompt (600 tokens in)
Execute once → Final answer (1200 tokens out)
= 2-3 LLM calls (compose + execute), 1200 output tokens
```

## PromptComposer Class

### Constructor

```python
PromptComposer(
    include_enterprise: bool = True,
    provider: str = "openai",
    model: str = "gpt-4o-mini",
)
```

### Method 1: `compose_from_templates()`

Generate prompts from templates and compose them in one call:

```python
result = composer.compose_from_templates(
    question="Should we rebuild our authentication system?",
    template_names=["risk_assessor", "decision_framework"],
    refine=True,        # LLM-refine each template's prompt first
    provider="openai",
    model="gpt-4o-mini",
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `question` | `str` | required | User's question |
| `template_names` | `list[str]` | required | Template names to compose |
| `refine` | `bool` | `True` | LLM-refine individual prompts before composing |
| `provider` | `str \| None` | uses default | LLM provider |
| `model` | `str \| None` | uses default | Model override |

### Method 2: `compose()`

Merge pre-existing prompt strings:

```python
prompts = [
    "You are a risk analyst. Assess the risks of: ...",
    "You are a decision expert. Evaluate options for: ...",
]

result = composer.compose(
    prompts=prompts,
    question="Should we rebuild auth?",
    source_templates=["risk_assessor", "decision_framework"],
    provider="openai",
)
```

### Method 3: `compile_generic()`

Zero-cost static compilation using pre-authored generic prompts:

```python
result = composer.compile_generic(
    question="Why did our server crash?",
    template_names=["root_cause_analyzer", "step_by_step_reasoner"],
)

print(result.metadata["composition_mode"])  # "static_generic"
print(result.metadata["llm_calls"])         # 0
```

The static merge produces a multi-lens prompt:

```
You are a multi-disciplinary analyst. Answer the following question
by applying ALL of the analytical lenses below.

QUESTION: Why did our server crash?

[Lens 1: Root Cause Analyzer]
You are a root cause analysis specialist...
...

[Lens 2: Step By Step Reasoner]
You are an expert problem solver...
...

Integrate findings across all lenses. End with concrete Recommendations.
```

## ComposedPrompt Object

All three methods return a `ComposedPrompt`:

```python
@dataclass
class ComposedPrompt:
    prompt: str                    # The final merged prompt
    source_templates: list[str]    # Which templates contributed
    question: str                  # Original question
    component_prompts: list[str]   # Individual prompts before merging
    metadata: dict                 # Composition mode, model used, etc.
    
    def execute(self, provider, **kwargs) -> str   # Execute → response string
    def to_context(self) -> Context                # Convert to Context object
    def to_string(self) -> str                     # Get prompt as plain string
    def to_messages(self) -> list                  # OpenAI messages format
    def to_dict(self) -> dict                      # Serialize
```

### Executing ComposedPrompt

```python
# Execute and get response text
response = result.execute(provider="openai", model="gpt-4o")

# Or convert to Context first (for more control)
ctx = result.to_context()
response = ctx.execute(provider="anthropic", temperature=0.3)

# Or use as a string in your own system
prompt_str = result.to_string()
# → Send to any LLM API directly
```

## `get_generic_prompt_for()` — Single Template Utility

Get a single template's generic prompt with automatic enterprise fallback:

```python
from mycontext.intelligence import get_generic_prompt_for

# Get generic prompt for any template
prompt = get_generic_prompt_for(
    template_name="root_cause_analyzer",
    question="Why did our API latency spike?",
    include_enterprise=True,
)
print(prompt)

# With enterprise fallback (if enterprise not licensed, uses free alternative)
prompt = get_generic_prompt_for(
    template_name="causal_reasoner",  # enterprise pattern
    question="Why did our revenue drop?",
    include_enterprise=False,  # will use root_cause_analyzer as fallback
)
```

## Composition Rules

When merging prompts, the LLM composition engine follows these rules:

1. Produce a **single self-contained prompt** (not an answer)
2. Preserve every unique analytical technique from the components
3. **Remove redundancy** — if two templates both ask for stakeholder analysis, include it once
4. Structure clearly: role → analytical approach → output sections
5. Target **1000–1800 characters** — concise but comprehensive
6. **Always end with Recommendations / Next Steps**

## Examples

### Business Diagnostic

```python
from mycontext.intelligence import PromptComposer

composer = PromptComposer(provider="openai")

result = composer.compose_from_templates(
    question="Our enterprise customers are churning at 8%/month. Why and what should we do?",
    template_names=["root_cause_analyzer", "stakeholder_mapper", "scenario_planner"],
    refine=True,
)

print(f"Templates: {result.source_templates}")
print(f"Prompt length: {len(result.to_string())} chars")
response = result.execute(provider="openai", model="gpt-4o")
```

### Security Review

```python
result = composer.compose_from_templates(
    question="Comprehensive security review of our authentication system",
    template_names=["code_reviewer", "risk_assessor"],
    refine=False,  # Faster without refinement
)
response = result.execute(provider="openai")
```

### Zero-Cost Compilation Pipeline

```python
from mycontext.intelligence import PromptComposer

composer = PromptComposer()

# Compile 3 templates into one prompt — zero LLM calls
result = composer.compile_generic(
    question="How should we price our new enterprise tier?",
    template_names=["risk_assessor", "stakeholder_mapper", "scenario_planner"],
)

print(f"Composition mode: {result.metadata['composition_mode']}")  # "static_generic"
print(f"LLM calls for compilation: {result.metadata['llm_calls']}")  # 0

# Now execute once
response = result.execute(provider="openai")
```

## Comparison: compose_from_templates vs compile_generic

| Method | LLM calls for composition | Output quality |
|--------|--------------------------|----------------|
| `compose_from_templates(refine=True)` | 2+ (refine + compose) | Highest |
| `compose_from_templates(refine=False)` | 1 (compose only) | High |
| `compile_generic()` | 0 | ~90% of composed |

## API Reference

### `PromptComposer`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(include_enterprise, provider, model)` | — | Initialize |
| `compose(prompts, question, source_templates, ...)` | `ComposedPrompt` | Merge prompt strings |
| `compose_from_templates(question, template_names, refine, ...)` | `ComposedPrompt` | Generate + compose |
| `compile_generic(question, template_names, **kwargs)` | `ComposedPrompt` | Zero-cost compile |

### `get_generic_prompt_for()`

```python
def get_generic_prompt_for(
    template_name: str,
    question: str,
    include_enterprise: bool = True,
    **kwargs,
) -> str | None
```
