---
sidebar_position: 3
title: suggest_patterns()
description: Recommend the best cognitive patterns for any question. Three modes — keyword (instant), llm (deep), hybrid (best of both).
---

# suggest_patterns()

`suggest_patterns()` recommends the optimal cognitive patterns for a given question and suggests a workflow chain order. Three modes: keyword matching (zero LLM calls), LLM-powered selection, or hybrid.

As of **v0.10.0**, modes **`llm`** and **`hybrid`** first call **`suggest_routes(max_routes=1)`** and map the best route into a `SuggestionResult`. If that fails, the legacy catalog-selection LLM path runs. For **multiple** differentiated routes and agent-level planning, use [`suggest_routes()`](./route-suggestion) directly.

```python
from mycontext.intelligence import suggest_patterns

result = suggest_patterns(
    "Why did our churn spike 40% this quarter?",
    mode="hybrid",
    llm_provider="openai",
)
print(result.suggested_chain)
# → ['root_cause_analyzer', 'data_analyzer', 'decision_framework']
```

## Function Signature

```python
suggest_patterns(
    question: str,
    include_enterprise: bool = True,
    suggest_chain: bool = True,
    max_patterns: int = 5,
    mode: str = "keyword",
    llm_provider: str = "openai",
    temperature: float = 0,
    model: str | None = None,
    **llm_kwargs,
) -> SuggestionResult
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `question` | `str` | required | Question or problem description |
| `include_enterprise` | `bool` | `True` | Deprecated and ignored — all 88 patterns are always available. Kept for backwards compatibility. |
| `suggest_chain` | `bool` | `True` | Order suggestions as a workflow chain |
| `max_patterns` | `int` | `5` | Maximum patterns to suggest |
| `mode` | `str` | `"keyword"` | Selection mode: `"keyword"`, `"llm"`, or `"hybrid"` |
| `llm_provider` | `str` | `"openai"` | LLM provider for `"llm"` or `"hybrid"` mode |
| `temperature` | `float` | `0` | Temperature for LLM selection (0 = deterministic) |
| `model` | `str \| None` | `None` | Override model name |

**Returns:** `SuggestionResult`

## Three Modes

### Mode 1: `"keyword"` (instant, 0 LLM calls)

Matches question keywords against a curated map of all 88 patterns. Fast, deterministic, and free.

```python
result = suggest_patterns(
    "Why is our conversion rate dropping?",
    mode="keyword",
)
print(result.source)  # "keyword"
print(result.suggested_patterns[0].name)  # "root_cause_analyzer"
print(result.suggested_patterns[0].confidence)  # 0.85
```

Best for:
- Real-time suggestions
- High-volume usage
- Deterministic routing pipelines
- Cost-sensitive applications

### Mode 2: `"llm"` (deep, 1 LLM call)

Sends the full 85-pattern catalog to an LLM with the question. The LLM reasons about domains, reasoning types, and pipeline order.

```python
result = suggest_patterns(
    "We're seeing a 40% churn increase and need to understand why and what to do",
    mode="llm",
    llm_provider="openai",
    temperature=0,
)
print(result.llm_reasoning[:200])  # LLM's raw reasoning
print(result.suggested_chain)
```

Best for:
- Complex, multi-domain questions
- When quality matters more than latency
- Novel question types

### Mode 3: `"hybrid"` (recommended, 1 LLM call)

Runs keyword analysis first, then sends keyword suggestions as hints to the LLM. The LLM can confirm, refine, or override keyword choices.

```python
result = suggest_patterns(
    "Should we build or buy our analytics infrastructure?",
    mode="hybrid",
    llm_provider="openai",
)
print(result.source)  # "hybrid"
```

Best for:
- Production applications
- High-quality suggestions with reasonable cost
- When you want the LLM to catch what keywords miss

## SuggestionResult

Every call returns a `SuggestionResult` dataclass:

```python
@dataclass
class SuggestionResult:
    question: str
    suggested_patterns: list[PatternSuggestion]  # Ordered suggestions
    suggested_chain: list[str] | None             # Workflow chain order
    reasoning: str                                # Why these patterns
    source: str                                   # "keyword" | "llm" | "hybrid"
    llm_reasoning: str | None                     # Raw LLM output (llm/hybrid only)
```

### PatternSuggestion

```python
@dataclass
class PatternSuggestion:
    name: str            # Pattern name (snake_case)
    category: str        # "free" | "enterprise"
    reason: str          # Why it was selected
    confidence: float    # 0.0 to 1.0
    chain_position: int | None  # Position in workflow chain
```

## Export Formats

`SuggestionResult` exports to multiple formats for integration:

```python
result = suggest_patterns("Why did our server crash?", mode="keyword")

# Markdown (for notebooks, dashboards)
print(result.to_markdown())

# JSON (for APIs, storage)
json_str = result.to_json()
# → {"question": "...", "suggested_patterns": [...], "suggested_chain": [...]}

# YAML (for config files, pipelines)
yaml_str = result.to_yaml()

# XML (for XML-based systems)
xml_str = result.to_xml()

# Dict (for Python processing)
d = result.to_dict()

# Round-trip
loaded = SuggestionResult.from_json(json_str)
loaded2 = SuggestionResult.from_dict(d)
```

## Workflow Chains

When `suggest_chain=True` (default), patterns are ordered into a logical workflow pipeline:

```
investigation/analysis → reasoning/comparison → synthesis/decision
```

The chain ordering priority:
1. `temporal_sequence_analyzer` — establish timeline first
2. `historical_context_mapper` — historical context
3. `root_cause_analyzer` / `diagnostic_root_cause_analyzer` — diagnosis
4. `causal_reasoner` — causal chain
5. `differential_diagnoser` — differential diagnosis
6. `future_scenario_planner` — future states
7. `pattern_recognition_engine` — patterns
8. `cross_domain_synthesizer` / `holistic_integrator` — synthesis

```python
result = suggest_patterns("Why is our product stagnating?", mode="hybrid")
print(result.suggested_chain)
# → ['root_cause_analyzer', 'data_analyzer', 'scenario_planner']
#     │ diagnosis          │ evidence       │ future options
```

## All Patterns Considered

Suggestions are always drawn from the full set of 88 patterns — there is no gating. The `include_enterprise` argument is deprecated and ignored:

```python
result = suggest_patterns(
    "Complex multi-domain business question",
    mode="keyword",
)
for pattern in result.suggested_patterns:
    print(f"{pattern.name} [{pattern.category}]: {pattern.reason}")
# → decision_framework [decision]: ...
# → root_cause_analyzer [reasoning]: ...
```

## Examples

### Simple Root Cause Analysis

```python
result = suggest_patterns(
    "Why is our API response time increasing?",
    mode="keyword",
    max_patterns=3,
)
# Suggested: root_cause_analyzer, step_by_step_reasoner
```

### Complex Strategic Decision

```python
result = suggest_patterns(
    "Should we expand into European markets given Brexit uncertainty, competitive pressure, and our limited runway?",
    mode="hybrid",
    llm_provider="anthropic",
    max_patterns=4,
)
# Likely: scenario_planner, risk_assessor, decision_framework, stakeholder_mapper
```

### Code Review Request

```python
result = suggest_patterns(
    "Review my Python authentication code for security issues",
    mode="keyword",
)
# Suggested: code_reviewer, risk_assessor
```

### Using Results to Execute

After getting suggestions, execute the top pattern:

```python
from mycontext.intelligence import suggest_patterns
from mycontext.templates.free.reasoning import RootCauseAnalyzer

result = suggest_patterns("Why did our conversion drop?", mode="keyword")
top_pattern = result.suggested_patterns[0].name

if top_pattern == "root_cause_analyzer":
    rca_result = RootCauseAnalyzer().execute(
        provider="openai",
        problem="Conversion rate dropped 30% after the redesign",
    )
```

## `assess_complexity()` — Should You Even Use Templates?

Before suggesting patterns, check if templates will actually add value:

```python
from mycontext.intelligence import assess_complexity

assessment = assess_complexity(
    "What is the capital of France?",
    provider="openai",
)
print(assessment.complexity)        # "low"
print(assessment.recommendation)   # "raw"
print(assessment.reasoning)        # "Simple factual question..."

assessment2 = assess_complexity(
    "Should we migrate our 10-year monolith to microservices given our team structure?",
    provider="openai",
)
print(assessment2.complexity)      # "high"
print(assessment2.recommendation)  # "integrated"
print(assessment2.domains)         # ["technical", "organizational", "strategic"]
print(assessment2.reasoning_type)  # "strategic"
```

**ComplexityResult:**

```python
@dataclass
class ComplexityResult:
    complexity: str       # "low", "medium", "high"
    domains: list[str]    # Knowledge domains involved
    reasoning_type: str   # "diagnostic", "comparative", "strategic", etc.
    recommendation: str   # "raw", "single_template", "integrated"
    reasoning: str        # Why this recommendation
    best_template: str | None  # For "single_template" recommendation
```

## API Reference

### `suggest_patterns()`

```python
def suggest_patterns(
    question: str,
    include_enterprise: bool = True,
    suggest_chain: bool = True,
    max_patterns: int = 5,
    mode: str = "keyword",
    llm_provider: str = "openai",
    temperature: float = 0,
    model: str | None = None,
    **llm_kwargs,
) -> SuggestionResult
```

### `assess_complexity()`

```python
def assess_complexity(
    question: str,
    provider: str = "openai",
    temperature: float = 0,
    model: str | None = None,
    **kwargs,
) -> ComplexityResult
```

### `get_pattern_class()`

```python
def get_pattern_class(
    pattern_name: str,
    include_enterprise: bool = True,
) -> type | None
```

Returns the pattern class for a given name, or `None` if not found. The `include_enterprise` argument is deprecated and ignored — all 88 patterns are always available.
