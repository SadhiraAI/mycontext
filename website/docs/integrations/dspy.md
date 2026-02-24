---
sidebar_position: 6
title: DSPy
description: Use mycontext cognitive patterns as DSPy instructions and signatures. Convert any Context to DSPy-compatible prompt strings and signature dicts.
---

# DSPy

Use mycontext cognitive frameworks as the foundation for DSPy programs. Export any `Context` to a DSPy-compatible prompt string or signature dict, then optimize with DSPy's compilers.

```bash
pip install mycontext-ai dspy-ai
```

## Quick Start

```python
import dspy
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.integrations import DSPyHelper

# Configure DSPy
lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

# Build cognitive context
ctx = RootCauseAnalyzer().build_context(
    problem="Database query times increased 10x",
    depth="thorough",
)

# Get DSPy-compatible prompt
instructions = DSPyHelper.to_prompt(ctx)

# Use as instructions in a DSPy Signature
class RootCauseSignature(dspy.Signature):
    """Conduct systematic root cause analysis."""
    problem: str = dspy.InputField(desc="The problem to analyze")
    analysis: str = dspy.OutputField(desc="Comprehensive root cause analysis")

# Use the mycontext prompt as system context
predictor = dspy.Predict(RootCauseSignature)
result = predictor(problem="Database query times increased 10x")
print(result.analysis)
```

## DSPyHelper Methods

### `to_prompt(context)`

Returns the assembled context as a plain string — the universal format for any DSPy module:

```python
from mycontext.integrations import DSPyHelper

prompt = DSPyHelper.to_prompt(ctx)
# → Full assembled context string with role, rules, directive, constraints
```

### `to_signature(context)`

Returns a dict with the instructions and full context:

```python
sig = DSPyHelper.to_signature(ctx)
# {
#   "instructions": "## Role\nSenior analyst...\n## Directive\n...",
#   "context": {"guidance": {...}, "directive": {...}, ...}
# }
```

## DSPy ChainOfThought with mycontext

```python
import dspy
from mycontext.templates.free.reasoning import StepByStepReasoner
from mycontext.integrations import DSPyHelper

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

ctx = StepByStepReasoner().build_context(
    problem="Design a fault-tolerant message queue system",
    domain="distributed systems",
)

class ReasoningSignature(dspy.Signature):
    """Step-by-step systematic problem solving."""
    problem: str = dspy.InputField()
    solution: str = dspy.OutputField()

# Use ChainOfThought for additional reasoning depth
cot = dspy.ChainOfThought(ReasoningSignature)
result = cot(problem=ctx.directive.content)
print(result.solution)
```

## DSPy Program with mycontext Context

Build a full DSPy program that uses mycontext for its system instructions:

```python
import dspy
from mycontext.templates.free.specialized import RiskAssessor
from mycontext.integrations import DSPyHelper

class RiskAssessmentProgram(dspy.Module):
    def __init__(self):
        super().__init__()
        
        # Use mycontext framework as instructions
        ctx = RiskAssessor().build_context(
            decision="Launch new enterprise pricing tier",
            depth="comprehensive",
        )
        self.instructions = DSPyHelper.to_prompt(ctx)
        
        class RiskSig(dspy.Signature):
            decision: str = dspy.InputField(desc="Decision to assess")
            risk_assessment: str = dspy.OutputField(desc="Full risk assessment")
        
        self.assess = dspy.Predict(RiskSig)
    
    def forward(self, decision):
        return self.assess(decision=decision)

program = RiskAssessmentProgram()
result = program("Should we enter the EU market next quarter?")
print(result.risk_assessment)
```

## API Reference

### `DSPyHelper`

| Method | Returns | Description |
|--------|---------|-------------|
| `to_prompt(context)` | `str` | Assembled context as string |
| `to_signature(context)` | `dict` | Instructions + full context dict |
