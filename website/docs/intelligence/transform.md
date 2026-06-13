---
sidebar_position: 2
title: transform()
description: Automatically analyze any input, select the optimal cognitive pattern, and return a fully assembled Context — zero LLM calls.
---

# transform()

`transform()` is the core of the Intelligence Layer. It analyzes raw input, classifies it by type and complexity, selects the best cognitive pattern, and returns a `Context` object ready to execute — all without a single LLM call.

```python
from mycontext.intelligence import transform

ctx = transform("Should we migrate to microservices?")
result = ctx.execute(provider="openai")
```

## The Function

```python
from mycontext.intelligence import transform

context = transform(
    input="Should we migrate to microservices?",
    metadata={"domain": "software", "complexity": "high"},
    patterns="auto",  # or ["pattern1", "pattern2"] to force specific ones
    include_enterprise=True,
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` | `str` | required | The raw question, problem, or statement |
| `metadata` | `dict \| None` | `None` | Optional hints: `domain`, `complexity`, `user_level` |
| `patterns` | `str \| list \| None` | `"auto"` | Pattern selection strategy |
| `include_enterprise` | `bool` | `True` | Deprecated and ignored — all 88 patterns are always in the selection pool |

**Returns:** `Context` — fully assembled with `data["transformation_metadata"]`

## Pattern Selection Strategy

### `"auto"` (default)
Analyzes the input and selects patterns automatically based on type, complexity, and domain detection.

```python
ctx = transform("Why did our API latency spike?")
print(ctx.data["transformation_metadata"]["patterns_applied"])
# → ["root_cause_analyzer"]
```

### Specific patterns list
Force specific patterns regardless of auto-analysis:

```python
ctx = transform(
    "Why did our API latency spike?",
    patterns=["root_cause_analyzer", "step_by_step_reasoner"],
)
```

## What the Engine Analyzes

### Input Type Detection

The engine classifies every input into one of 9 types, each mapped to optimal patterns:

| Input Type | Trigger phrases | Default patterns |
|-----------|----------------|-----------------|
| `CAUSAL` | "why", "root cause", "spike", "outage", "caused" | `root_cause_analyzer`, `causal_reasoner` |
| `QUESTION` | ends with `?`, "what is", "explain" | `question_analyzer`, `step_by_step_reasoner` |
| `PROBLEM` | "fix", "solve", "troubleshoot", "bug", "broken" | `root_cause_analyzer`, `step_by_step_reasoner` |
| `DECISION` | "should i", "should we", "decide", "choose" | `decision_framework`, `risk_assessor` |
| `COMPARISON` | "compare", "versus", "vs", "better than" | `comparative_analyzer`, `tradeoff_analyzer` |
| `STATEMENT` | no question markers | `socratic_questioner`, `intent_recognizer` |
| `CONCEPT` | "what is", "explain", "how does" | `analogical_reasoner`, `question_analyzer` |
| `TASK` | action verbs without question marks | `step_by_step_reasoner` |
| `CONVERSATION` | conversational markers | `intent_recognizer` |

### Complexity Assessment

| Level | Word count | Patterns used |
|-------|-----------|--------------|
| `SIMPLE` | < 10 words | 1 pattern, `depth="quick"` |
| `MODERATE` | 10–30 words | 1–2 patterns, `depth="standard"` |
| `COMPLEX` | 30–60 words | 2–3 patterns, `depth="comprehensive"` |
| `HIGHLY_COMPLEX` | 60+ words | 3 patterns, `depth="comprehensive"` |

### Domain Inference

Automatically detects domain from keywords:

| Domain | Keywords |
|--------|---------|
| `technical` | code, software, program, api, database |
| `financial` | invest, money, cost, revenue, profit |
| `medical` | health, medical, patient, treatment |
| `business` | business, market, customer, strategy |
| `scientific` | research, experiment, hypothesis, theory |

## The TransformationEngine Class

`transform()` is a convenience wrapper around `TransformationEngine`. Use the class for more control:

```python
from mycontext.intelligence import TransformationEngine

engine = TransformationEngine(include_enterprise=True)

# Analyze without transforming
analysis = engine.analyze_input(
    input="Why did our churn spike 40% this quarter?",
    metadata={"domain": "business", "complexity": "high"},
)
print(analysis.input_type)         # InputType.CAUSAL
print(analysis.complexity)         # ComplexityLevel.MODERATE
print(analysis.domain)             # "business"
print(analysis.recommended_patterns)  # ['root_cause_analyzer', 'causal_reasoner']
print(analysis.confidence)         # 0.8

# Transform with the analyzed input
ctx = engine.transform(
    input="Why did our churn spike 40% this quarter?",
    metadata={"domain": "business"},
)
```

### `engine.analyze_input(input, metadata)`

Returns an `InputAnalysis` dataclass:

```python
@dataclass
class InputAnalysis:
    input_type: InputType         # The classified input type
    complexity: ComplexityLevel   # Simple/Moderate/Complex/HighlyComplex
    domain: str                   # Inferred domain
    key_concepts: list[str]       # Extracted concept words
    requires_reasoning: bool      # Contains why/how/explain
    requires_comparison: bool     # Contains compare/versus/better
    requires_verification: bool   # Contains verify/check/confirm
    ambiguity_level: str          # "low", "medium", "high"
    recommended_patterns: list[str]
    confidence: float             # 0.0 to 1.0
```

### `engine.explain_selection(input, metadata)`

Get a human-readable explanation of why patterns were selected:

```python
explanation = engine.explain_selection(
    input="Should we adopt GraphQL or stick with REST?",
)
print(explanation)
# → Input Type: comparison
#   Complexity: simple
#   Domain: technical
#   Ambiguity Level: low
#   Recommended Patterns:
#   1. comparative_analyzer
#   2. tradeoff_analyzer
#   Confidence in selection: 80.0%
```

### `engine.get_available_patterns()`

List all patterns the engine can use:

```python
patterns = engine.get_available_patterns()
# → ['question_analyzer', 'step_by_step_reasoner', 'socratic_questioner', ...]
```

## Reading Transformation Metadata

Every `transform()` call annotates the returned `Context` with detailed metadata:

```python
ctx = transform("Why is our CI pipeline failing on Tuesdays?")

meta = ctx.data["transformation_metadata"]
print(meta["patterns_applied"])     # ['root_cause_analyzer']
print(meta["confidence"])           # 0.8
print(meta["input_analysis"]["type"])       # 'causal'
print(meta["input_analysis"]["complexity"]) # 'moderate'
print(meta["input_analysis"]["domain"])     # 'technical'
print(meta["input_analysis"]["ambiguity"])  # 'low'
```

## Examples

### Business Causal Question

```python
ctx = transform("Why did our NPS drop 15 points after the product update?")
# → Detects: CAUSAL type, business domain
# → Selects: root_cause_analyzer
result = ctx.execute(provider="openai")
```

### Technical Decision

```python
ctx = transform(
    "Should we use Postgres or MongoDB for our new service?",
    metadata={"domain": "technical"},
)
# → Detects: COMPARISON type
# → Selects: comparative_analyzer, tradeoff_analyzer
result = ctx.execute(provider="openai")
```

### Force Specific Pattern

```python
# Override auto-selection
ctx = transform(
    "Analyze our Q3 revenue trends",
    patterns=["data_analyzer"],
)
result = ctx.execute(provider="openai")
```

## Fallback Behavior

If no pattern matches or pattern loading fails, `transform()` returns a basic `Context` with:
- `Guidance(role="Helpful Assistant", rules=["Be clear and helpful"])`
- `Directive(content=input)`

This ensures the function always returns something executable.

## API Reference

### `transform()`

```python
def transform(
    input: str,
    metadata: dict | None = None,
    patterns: str | list | None = "auto",
    include_enterprise: bool = True,
) -> Context
```

### `TransformationEngine`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(include_enterprise)` | — | Initialize engine |
| `analyze_input(input, metadata)` | `InputAnalysis` | Analyze without transforming |
| `transform(input, metadata, patterns)` | `Context` | Full transformation |
| `explain_selection(input, metadata)` | `str` | Human-readable explanation |
| `get_available_patterns()` | `list[str]` | All available pattern names |
| `get_pattern(name)` | `Pattern \| None` | Get specific pattern instance |

### `InputType` Enum

```python
class InputType(Enum):
    QUESTION = "question"
    PROBLEM = "problem"
    DECISION = "decision"
    CONCEPT = "concept"
    COMPARISON = "comparison"
    CAUSAL = "causal"
    STATEMENT = "statement"
    TASK = "task"
    CONVERSATION = "conversation"
```

### `ComplexityLevel` Enum

```python
class ComplexityLevel(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    HIGHLY_COMPLEX = "highly_complex"
```
