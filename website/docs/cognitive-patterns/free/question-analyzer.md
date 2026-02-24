---
sidebar_position: 5
title: QuestionAnalyzer
description: Systematically decompose and analyze questions before answering them. Based on IBM Zurich cognitive tools research — understand before you answer.
---

# QuestionAnalyzer

**Category:** Analysis | **Module:** `mycontext.templates.free.analysis`

Analyzes questions before answering them. Classifies question type, identifies required cognitive actions, surfaces implicit assumptions, rates complexity, and recommends an optimal answer strategy. Based on IBM Zurich's research on eliciting reasoning in language models.

:::info Note
This pattern analyzes the question — it does **not** answer it. The output is a structured analysis that prepares for a high-quality answer. Use it before complex questions or pipe its output into another pattern.
:::

## When to Use

- Before feeding a complex question to an LLM
- Identifying why a question is hard or ambiguous
- Discovering implicit assumptions in user queries
- Routing questions to the right expert or system
- Building RAG pipelines that understand what's being asked
- Intent classification with full semantic decomposition

## Quick Start

```python
from mycontext.templates.free.analysis import QuestionAnalyzer

analyzer = QuestionAnalyzer()

result = analyzer.execute(
    provider="gemini",
    question="How does quantum entanglement work?",
    depth="comprehensive",
)
print(result.response)
```

## Methods

### `build_context(question, context=None, depth="comprehensive")`

```python
ctx = analyzer.build_context(
    question="Should we expand into the European market now?",
    depth="comprehensive",
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `question` | `str` | `""` | The question to analyze |
| `context` | `str \| None` | `None` | Additional context about who is asking and why |
| `depth` | `str` | `"comprehensive"` | Analysis depth |

### `execute(provider, question, context=None, depth="comprehensive", **kwargs)`

```python
result = analyzer.execute(
    provider="gemini",
    question="What's the best way to structure a microservices architecture?",
    context="Mid-size startup, 15 engineers, currently monolith",
    depth="comprehensive",
)
```

## Analysis Sections

### 1. Question Type Classification

Identifies the primary and secondary question type:

| Type | Description | Example |
|------|-------------|---------|
| **Factual** | Seeking specific information | "What year was Python released?" |
| **Conceptual** | Exploring ideas or theories | "What is recursion?" |
| **Analytical** | Breaking down and examining | "Why did our conversion drop?" |
| **Evaluative** | Making judgments or comparisons | "Is Postgres better than MongoDB?" |
| **Procedural** | Explaining how to do something | "How do I deploy to Kubernetes?" |
| **Causal** | Explaining why something happens | "Why do startups fail?" |

### 2. Core Task Identification
What cognitive action is required (explain, compare, analyze, evaluate) and what the expected output format is.

### 3. Key Components
Primary concepts, related domains, relationships, and scope boundaries.

### 4. Knowledge Prerequisites
Required, helpful, and advanced knowledge needed to answer well.

### 5. Implicit Assumptions
Unstated assumptions in the question, context clues, and potential ambiguities.

### 6. Complexity Assessment (1–10 scale)
- Conceptual difficulty
- Breadth of knowledge required
- Reasoning depth needed
- Interdisciplinary connections

### 7. Answer Strategy Recommendation
Optimal approach, structure, key considerations, and pitfalls to avoid.

### 8. Clarified Restatement
The original question reformulated with all implicit elements made explicit.

## Depth Levels

| Depth | Use case |
|-------|----------|
| `"brief"` | Quick routing — just type + restatement |
| `"moderate"` | Standard analysis — type, assumptions, strategy |
| `"comprehensive"` | Full 8-section analysis with complexity rating |

## Examples

### Business Strategy Question

```python
result = analyzer.execute(
    provider="gemini",
    question="Should we build or buy this feature?",
    context="B2B SaaS company, 50-person engineering team",
    depth="comprehensive",
)
```

Expected output highlights:
- Type: **Evaluative** (primary) + **Analytical** (secondary)
- Implicit assumptions: assumes clear feature definition, budget availability
- Complexity: 7/10 — requires build vs. buy framework, org context
- Strategy: Use a decision matrix, compare on: cost, speed, maintenance, core competency

### Technical Question

```python
result = analyzer.execute(
    provider="openai",
    question="How does transformer self-attention work?",
    depth="moderate",
)
```

### Customer Support Routing

```python
questions = [
    "My account got locked",
    "How do I export my data?",
    "Is this GDPR compliant?",
    "What's your pricing?",
]

for q in questions:
    ctx = analyzer.build_context(question=q, depth="brief")
    # Export to your routing system
    payload = ctx.to_dict()
```

## Two-Stage Pipeline Pattern

Use `QuestionAnalyzer` as a pre-processing stage before answering:

```python
from mycontext.templates.free.analysis import QuestionAnalyzer
from mycontext.templates.free.reasoning import StepByStepReasoner

question = "How should we price our enterprise tier?"

# Stage 1: Analyze the question
analysis_result = QuestionAnalyzer().execute(
    provider="gemini",
    question=question,
    depth="comprehensive",
)

# Stage 2: Use analysis to inform answer strategy
# (extract complexity and recommended approach from analysis)
solution_result = StepByStepReasoner().execute(
    provider="openai",
    problem=question,
    context=analysis_result.response[:500],
    domain="analytical",
)
```

## Research Basis

Based on IBM Zurich's paper: *"Eliciting Reasoning in Language Models with Cognitive Tools"* (June 2025). The research showed that pre-analyzing questions before answering them significantly improves response quality and reduces hallucination rates.

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(question, context, depth)` | `Context` | Assembled context |
| `execute(provider, question, context, depth, **kwargs)` | `ProviderResponse` | Execute analysis |
| `generic_prompt(question, context_section, depth)` | `str` | Zero-cost prompt string |
