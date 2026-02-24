---
sidebar_position: 6
title: Chain Orchestration
description: build_workflow_chain() uses an LLM to select, order, and generate parameters for a complete multi-pattern workflow — fully automatic.
---

# Chain Orchestration

`build_workflow_chain()` designs and returns a complete multi-pattern workflow: which patterns to use, in what order, with what parameters. The LLM acts as an architect, analyzing the question and building the optimal chain.

```python
from mycontext.intelligence import build_workflow_chain

result = build_workflow_chain(
    question="Why has our mobile app retention dropped 25% since iOS 18?",
    provider="openai",
)
print(result.chain)
# → ["root_cause_analyzer", "data_analyzer", "scenario_planner"]

print(result.chain_params)
# → {"root_cause_analyzer": {"problem": "...", "depth": "comprehensive"}, ...}

print(result.selection_reasoning)
# → {"root_cause_analyzer": "Diagnoses the iOS 18 retention issue...", ...}
```

## Function Signature

```python
build_workflow_chain(
    question: str,
    include_enterprise: bool = True,
    max_patterns: int | None = None,
    use_question_analyzer: bool = True,
    provider: str = "openai",
    temperature: float = 0,
    model: str | None = None,
    **llm_kwargs,
) -> WorkflowChainResult
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `question` | `str` | required | Question or task description |
| `include_enterprise` | `bool` | `True` | Include enterprise patterns |
| `max_patterns` | `int \| None` | `None` | Cap the chain length |
| `use_question_analyzer` | `bool` | `True` | Run QuestionAnalyzer first for decomposition |
| `provider` | `str` | `"openai"` | LLM provider |
| `temperature` | `float` | `0` | Temperature (0 = deterministic chain design) |
| `model` | `str \| None` | `None` | Override model |

**Returns:** `WorkflowChainResult`

## How it Works

### Step 1: Question Decomposition (optional)

When `use_question_analyzer=True` (default), the `QuestionAnalyzer` pattern runs first to decompose the question into its domains, requirements, and complexity. This output is fed to the chain designer as context.

### Step 2: Chain Design

The LLM receives the full 85-pattern catalog and analyzes:
1. **Domains** — business, technical, ethical, legal, etc.
2. **Reasoning type** — diagnostic, comparative, strategic, creative
3. **Complexity** — low, medium, high
4. **Pattern selection** — 2–4 patterns that directly address the question
5. **Parameter generation** — `build_context()` params for each pattern

### Step 3: Chain Execution

The returned `WorkflowChainResult` contains everything needed to execute the chain:

```python
result = build_workflow_chain("Why did churn spike?", provider="openai")

# Manual execution
for pattern_name in result.chain:
    klass = get_pattern_class(pattern_name)
    params = result.chain_params[pattern_name]
    ctx = klass().build_context(**params)
    response = ctx.execute(provider="openai")
    print(f"[{pattern_name}]: {response.response[:200]}")
```

## WorkflowChainResult

```python
@dataclass
class WorkflowChainResult:
    chain: list[str]                      # Ordered pattern names
    chain_params: dict[str, dict]         # build_context() params per pattern
    reasoning: str                        # Overall chain reasoning
    selection_reasoning: dict[str, str]   # Per-pattern selection reason
    pattern_categories: dict[str, str]    # "free" | "enterprise" per pattern
    question_analysis: dict | None        # Domains, reasoning type, complexity
    template_decomposition: str | None    # QuestionAnalyzer output (if used)
    llm_raw: str | None                   # Raw LLM response (for debugging)
    
    def to_chain_params_tuple_format(self) -> dict[str, tuple]
```

### `to_chain_params_tuple_format()`

Converts chain params to the `(primary_key, extra_kwargs)` tuple format needed for the orchestration loop:

```python
tuple_params = result.to_chain_params_tuple_format()
# → {
#     "root_cause_analyzer": ("problem", {"depth": "comprehensive"}),
#     "scenario_planner": ("topic", {"timeframe": "6 months"}),
# }
```

## Complete Execution Loop

Here's the full pattern for building and executing a chain:

```python
from mycontext.intelligence import build_workflow_chain, get_pattern_class

# 1. Design the chain
result = build_workflow_chain(
    question="Our SaaS enterprise churn is increasing. Diagnose and prescribe.",
    provider="openai",
    max_patterns=3,
)

print("Question analysis:", result.question_analysis)
print("Chain:", result.chain)
print("Reasoning:", result.reasoning)
print()
for name, reason in result.selection_reasoning.items():
    cat = result.pattern_categories.get(name, "?")
    print(f"  [{cat}] {name}: {reason}")

# 2. Execute each pattern in sequence
previous_output = None
for pattern_name in result.chain:
    klass = get_pattern_class(pattern_name, include_enterprise=True)
    if klass is None:
        continue
    
    params = result.chain_params[pattern_name]
    
    # Feed previous output into next pattern if it uses a primary input
    if previous_output and list(params.keys()):
        primary_key = list(params.keys())[0]
        params[primary_key] = previous_output[:2000]  # Truncate to fit context
    
    ctx = klass().build_context(**params)
    response = ctx.execute(provider="openai")
    previous_output = response.response
    
    print(f"\n{'='*60}")
    print(f"PATTERN: {pattern_name}")
    print(response.response)
```

## chain_params Structure

The `chain_params` dict maps each pattern name to its `build_context()` parameters:

```python
print(result.chain_params)
# {
#   "root_cause_analyzer": {
#       "problem": "Enterprise churn increasing. Diagnose and prescribe.",
#       "depth": "comprehensive"
#   },
#   "stakeholder_mapper": {
#       "project": "<from previous step>",  # filled at runtime
#   },
#   "scenario_planner": {
#       "topic": "<from previous step>",
#       "timeframe": "12 months"
#   }
# }
```

The `"<from previous step>"` placeholder signals you should inject the previous pattern's output.

## Examples

### Business Diagnostic Chain

```python
result = build_workflow_chain(
    question="Our enterprise customer health scores are declining. What's happening and what should we do?",
    provider="openai",
    max_patterns=3,
)
# Typical chain: root_cause_analyzer → stakeholder_mapper → decision_framework
```

### Technical Architecture Decision

```python
result = build_workflow_chain(
    question="Should we migrate from MongoDB to PostgreSQL? We have 50TB data, 200 services, 18 months runway.",
    provider="openai",
    include_enterprise=True,
    max_patterns=4,
)
# Typical chain: tradeoff_analyzer → risk_assessor → decision_framework → scenario_planner
```

### Free Patterns Only

```python
result = build_workflow_chain(
    question="Why is our new feature adoption so low?",
    provider="openai",
    include_enterprise=False,  # Only use the 16 free patterns
    max_patterns=3,
)
# Enterprise patterns still appear in suggestions but with license notes
```

### Without Question Decomposition (faster)

```python
result = build_workflow_chain(
    question="Quick risk assessment for new vendor",
    provider="openai",
    use_question_analyzer=False,  # Skip decomposition step, saves 1 LLM call
    max_patterns=2,
)
```

## Inspecting the Question Analysis

The `question_analysis` field reveals how the LLM understood your question:

```python
if result.question_analysis:
    qa = result.question_analysis
    print("Domains:", qa.get("domains", []))
    # → ["customer success", "product", "business operations"]
    
    print("Reasoning type:", qa.get("reasoning_type", ""))
    # → "diagnostic"
    
    print("Complexity:", qa.get("complexity", ""))
    # → "high"
    
    print("Decomposition:", qa.get("decomposition", ""))
    # → "Diagnose why enterprise health scores are declining..."
```

## PATTERN_BUILD_CONTEXT_REGISTRY

The dynamic registry that maps pattern names to their `build_context()` signatures — introspected at runtime from the actual pattern classes:

```python
from mycontext.intelligence import PATTERN_BUILD_CONTEXT_REGISTRY

# Get the primary input key and default params for any pattern
primary_key, defaults = PATTERN_BUILD_CONTEXT_REGISTRY["root_cause_analyzer"]
print(primary_key)  # "problem"
print(defaults)     # {"depth": "comprehensive"}

# Check if a pattern is registered
print("risk_assessor" in PATTERN_BUILD_CONTEXT_REGISTRY)  # True

# List all registered patterns
for name, (primary, defaults) in PATTERN_BUILD_CONTEXT_REGISTRY.items():
    print(f"{name}: primary={primary}, defaults={defaults}")
```

## API Reference

### `build_workflow_chain()`

```python
def build_workflow_chain(
    question: str,
    include_enterprise: bool = True,
    max_patterns: int | None = None,
    use_question_analyzer: bool = True,
    provider: str = "openai",
    temperature: float = 0,
    model: str | None = None,
    **llm_kwargs,
) -> WorkflowChainResult
```

### `WorkflowChainResult`

| Attribute | Type | Description |
|-----------|------|-------------|
| `chain` | `list[str]` | Ordered pattern names |
| `chain_params` | `dict[str, dict]` | `build_context()` params per pattern |
| `reasoning` | `str` | Overall reasoning |
| `selection_reasoning` | `dict[str, str]` | Per-pattern selection reason |
| `pattern_categories` | `dict[str, str]` | `"free"` or `"enterprise"` per pattern |
| `question_analysis` | `dict \| None` | Domains, type, complexity |
| `template_decomposition` | `str \| None` | QuestionAnalyzer output |
| `llm_raw` | `str \| None` | Raw LLM JSON response |
