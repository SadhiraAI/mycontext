---
sidebar_position: 7
title: Semantic Kernel
description: Use mycontext cognitive patterns as Semantic Kernel functions. Convert any Context to a KernelFunctionFromPrompt and register it in your kernel.
---

# Semantic Kernel

Use mycontext cognitive patterns as Semantic Kernel functions. The `SemanticKernelHelper` creates a `KernelFunctionFromPrompt` from any `Context` and registers it in your kernel.

```bash
pip install mycontext-ai semantic-kernel
```

## Quick Start

```python
import asyncio
import semantic_kernel as sk
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.integrations import SemanticKernelHelper

async def main():
    # Build cognitive context
    ctx = RootCauseAnalyzer().build_context(
        problem="API latency tripled after deployment",
        depth="thorough",
    )

    # Create kernel
    kernel = sk.Kernel()
    kernel.add_service(sk.connectors.ai.open_ai.OpenAIChatCompletion(
        service_id="openai",
        ai_model_id="gpt-4o-mini",
    ))

    # Register mycontext as a semantic function
    fn = SemanticKernelHelper.create_semantic_function(
        kernel=kernel,
        context=ctx,
        function_name="diagnose",
        plugin_name="diagnostics",
    )

    result = await kernel.invoke(fn)
    print(result)

asyncio.run(main())
```

## SemanticKernelHelper Methods

### `create_semantic_function(kernel, context, function_name, plugin_name, **kwargs)`

Registers a `KernelFunctionFromPrompt` in the kernel:

```python
fn = SemanticKernelHelper.create_semantic_function(
    kernel=kernel,
    context=ctx,
    function_name="risk_assessment",
    plugin_name="analysis_tools",
)
```

### `to_prompt_template(context)`

Returns the assembled context as a plain string for manual use:

```python
template = SemanticKernelHelper.to_prompt_template(ctx)
# Use directly as prompt string in any SK component
```

## Multiple Functions in One Kernel

Register different cognitive patterns as different kernel functions:

```python
import semantic_kernel as sk
from mycontext.templates.free.reasoning import RootCauseAnalyzer, HypothesisGenerator
from mycontext.templates.free.planning import ScenarioPlanner
from mycontext.integrations import SemanticKernelHelper

kernel = sk.Kernel()
# ... add services ...

# Register multiple cognitive functions
rca_ctx = RootCauseAnalyzer().build_context(
    problem="{{$problem}}",
    depth="thorough",
)
SemanticKernelHelper.create_semantic_function(
    kernel, rca_ctx, function_name="diagnose", plugin_name="analysis"
)

hyp_ctx = HypothesisGenerator().build_context(
    observation="{{$observation}}",
    domain="{{$domain}}",
)
SemanticKernelHelper.create_semantic_function(
    kernel, hyp_ctx, function_name="generate_hypotheses", plugin_name="analysis"
)

plan_ctx = ScenarioPlanner().build_context(
    topic="{{$topic}}",
    timeframe="12 months",
)
SemanticKernelHelper.create_semantic_function(
    kernel, plan_ctx, function_name="plan_scenarios", plugin_name="analysis"
)
```

## API Reference

### `SemanticKernelHelper`

| Method | Returns | Description |
|--------|---------|-------------|
| `to_prompt_template(context)` | `str` | Assembled context as string |
| `create_semantic_function(kernel, context, function_name, plugin_name, **kwargs)` | `KernelFunctionFromPrompt` | Registered kernel function |
