---
sidebar_position: 3
title: Structured Output
description: Get validated JSON, Pydantic models, lists, and code blocks from LLM responses. Output parsers, schema enforcement, and format instructions built in.
---

# Structured Output

mycontext provides utilities for extracting structured data from LLM responses: output parsers, Pydantic model validation, JSON schema enforcement, and format instructions that tell the LLM exactly what shape to produce.

## Quick Start

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.utils.structured_output import extract_json, StructuredOutputMixin
from pydantic import BaseModel

class RCAResult(BaseModel):
    root_causes: list[str]
    contributing_factors: list[str]
    recommendations: list[str]
    confidence: float

# Execute with JSON format instruction
from mycontext import Context
from mycontext.foundation import Directive, Guidance, Constraints

ctx = Context(
    guidance=Guidance(role="Root cause analysis specialist"),
    directive=Directive(content="""Analyze why our API latency tripled.
    
Respond ONLY with valid JSON matching this schema:
{
  "root_causes": ["..."],
  "contributing_factors": ["..."],
  "recommendations": ["..."],
  "confidence": 0.0
}"""),
)

result = ctx.execute(provider="openai")

# Parse and validate
data = extract_json(result.response)
parsed = RCAResult(**data)
print(parsed.root_causes)
print(f"Confidence: {parsed.confidence:.1%}")
```

## Output Parsers

Five parsers for different response formats, all in `mycontext.utils.parsers`:

### `JSONParser`

```python
from mycontext.utils.parsers import JSONParser

parser = JSONParser(strict=True)

# Extracts JSON from code blocks OR raw text
data = parser.parse("""
Here's the analysis:
```json
{"issues": ["SQL injection", "CSRF"], "severity": "critical"}
```
""")
# → dict with "issues" list and "severity" key

# Get the format instruction to add to your prompt
instruction = parser.get_format_instruction()
# → "**OUTPUT FORMAT**: Respond with valid JSON only..."
```

### `ListParser`

```python
from mycontext.utils.parsers import ListParser

parser = ListParser(numbered=True, bullet=True)

items = parser.parse("""
Key findings:
1. Response times increased 300%
2. Database connections exhausted
- Memory usage at 95%
- Cache miss rate doubled
""")
# → ["Response times increased 300%", "Database connections exhausted",
#     "Memory usage at 95%", "Cache miss rate doubled"]
```

### `CodeBlockParser`

```python
from mycontext.utils.parsers import CodeBlockParser

# Extract specific language
parser = CodeBlockParser(language="python")
code = parser.parse(result.response)
# → "def fixed_function():\n    ..."

# Extract all code blocks
parser_all = CodeBlockParser()
blocks = parser_all.parse(result.response)
# → dict: python code, sql code, bash code
```

### `MarkdownParser`

```python
from mycontext.utils.parsers import MarkdownParser

parser = MarkdownParser()
structure = parser.parse(result.response)
# → dict with keys: headers, sections, lists, code_blocks, links
```

### Convenience Functions

```python
from mycontext.utils.parsers import (
    parse_json_response,
    parse_code_blocks,
    parse_list_items,
    parse_markdown_structure,
)

# Quick single-call parsing
data = parse_json_response(result.response)
code = parse_code_blocks(result.response, language="python")
items = parse_list_items(result.response)
md = parse_markdown_structure(result.response)
```

## Pydantic Model Output

### `StructuredOutputMixin`

Add to any class that calls `execute()`:

```python
from mycontext.utils.structured_output import StructuredOutputMixin
from pydantic import BaseModel

class RiskReport(BaseModel):
    overall_risk: str           # "low" | "medium" | "high" | "critical"
    risk_score: float           # 0.0 to 10.0
    top_risks: list[str]
    mitigation_steps: list[str]
    go_no_go: str               # "go" | "no-go" | "conditional"

# Parse from any LLM response
from mycontext.utils.structured_output import StructuredOutputMixin

response_text = my_context.execute(provider="openai").response
report = StructuredOutputMixin.parse_structured(response_text, RiskReport)
print(f"Risk: {report.overall_risk} ({report.risk_score}/10)")
print(f"Decision: {report.go_no_go}")
```

### `PydanticOutput` Decorator

```python
from mycontext.utils.structured_output import PydanticOutput
from pydantic import BaseModel

class CodeReviewResult(BaseModel):
    issues: list[dict]          # [{"type": "...", "severity": "...", "fix": "..."}]
    security_score: int         # 0-100
    performance_score: int      # 0-100
    recommendations: list[str]

@PydanticOutput(CodeReviewResult)
def review_code(code: str, language: str):
    from mycontext.templates.free.specialized import CodeReviewer
    return CodeReviewer().execute(
        provider="openai",
        code=code,
        language=language,
    )

result = review_code(my_code, "Python")
# result is a validated CodeReviewResult, not a raw string
print(f"Security score: {result.security_score}/100")
for issue in result.issues:
    print(f"  [{issue['severity']}] {issue['type']}: {issue['fix']}")
```

### `JSONOutput` Decorator

```python
from mycontext.utils.structured_output import JSONOutput

@JSONOutput(schema={"risks": list, "score": float, "recommendation": str})
def assess_risk(decision: str):
    from mycontext.templates.free.specialized import RiskAssessor
    return RiskAssessor().execute(provider="openai", decision=decision)

data = assess_risk("Should we launch in Europe next quarter?")
# data is a validated dict
print(data["recommendation"])
```

## `output_format()` — Format Instructions

Add structured output instructions directly to your context:

```python
from mycontext.utils.structured_output import output_format
from mycontext import Context
from mycontext.foundation import Directive

# JSON schema instruction
json_instruction = output_format("json", schema={
    "root_causes": "list of strings",
    "severity": "critical|high|medium|low",
    "confidence": "float 0-1",
})

ctx = Context(
    directive=Directive(content=f"Analyze why our API latency spiked.\n\n{json_instruction}")
)

# List instruction
list_instruction = output_format("markdown")

# Code instruction
code_instruction = output_format("code", language="python")

# Available formats
for fmt in ["json", "yaml", "xml", "markdown", "code"]:
    print(output_format(fmt))
```

## Pattern + Structured Output

The cleanest pattern: use a cognitive template to build the analytical framework, add format instructions via `Constraints`, then parse the output:

```python
from mycontext import Context
from mycontext.foundation import Constraints
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.utils.structured_output import extract_json
from pydantic import BaseModel

class RCAStructured(BaseModel):
    root_causes: list[str]
    contributing_factors: list[str]
    prevention_steps: list[str]
    confidence_level: str

# Build context from cognitive pattern
ctx = RootCauseAnalyzer().build_context(
    problem="API response times tripled after deployment",
    depth="comprehensive",
)

# Add JSON output constraint
ctx.constraints = Constraints(
    must_include=["root_causes", "prevention_steps"],
    format_rules=[
        "Respond ONLY with valid JSON",
        'Schema: {"root_causes": [], "contributing_factors": [], "prevention_steps": [], "confidence_level": "high|medium|low"}',
    ],
)

result = ctx.execute(provider="openai")

# Parse
data = extract_json(result.response)
if data:
    structured = RCAStructured(**data)
    print("Root causes:")
    for cause in structured.root_causes:
        print(f"  - {cause}")
```

## `response_format` via Provider

For OpenAI's native JSON mode, pass `response_format` directly to `execute()`:

```python
from mycontext.templates.free.specialized import RiskAssessor

ctx = RiskAssessor().build_context(
    decision="Launch new pricing tier",
    depth="comprehensive",
)

# OpenAI JSON mode — guaranteed JSON output
result = ctx.execute(
    provider="openai",
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
)

import json
data = json.loads(result.response)
```

## API Reference

### Parsers (`mycontext.utils.parsers`)

| Class | Method | Returns |
|-------|--------|---------|
| `JSONParser(strict)` | `parse(text)` | `dict \| list \| None` |
| `ListParser(numbered, bullet)` | `parse(text)` | `list[str]` |
| `CodeBlockParser(language)` | `parse(text)` | `str \| dict` |
| `MarkdownParser()` | `parse(text)` | `dict` |

### Structured Output (`mycontext.utils.structured_output`)

| Function / Class | Description |
|-----------------|-------------|
| `extract_json(text)` | Extract JSON string from any text |
| `StructuredOutputMixin.parse_structured(text, model)` | Parse into Pydantic model |
| `StructuredOutputMixin.parse_json(text)` | Parse JSON dict |
| `JSONOutput(schema, strict)` | Decorator for JSON output |
| `PydanticOutput(model)` | Decorator for Pydantic output |
| `output_format(format_type, **options)` | Format instruction string |
| `validate_schema(data, schema)` | Validate dict against schema |
