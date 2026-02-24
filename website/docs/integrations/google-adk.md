---
sidebar_position: 8
title: Google ADK
description: Power Google Agent Development Kit agents with mycontext cognitive patterns. Convert any Context to an ADK Agent instruction string.
---

# Google ADK

Use mycontext cognitive patterns as the instruction for Google Agent Development Kit (ADK) agents. The `GoogleADKHelper` creates fully-configured ADK `Agent` objects from any `Context`.

```bash
pip install mycontext-ai google-adk
```

## Quick Start

```python
from mycontext.templates.free.reasoning import StepByStepReasoner
from mycontext.integrations import GoogleADKHelper

# Build cognitive context
ctx = StepByStepReasoner().build_context(
    problem="Design a scalable notification system for 10M users",
    domain="software architecture",
)

# Create Google ADK agent
agent = GoogleADKHelper.create_agent(
    context=ctx,
    name="architect",
    model="gemini-2.0-flash",
    description="Systems architect specializing in scalable infrastructure",
)

# Use the agent
from google.adk.runners import Runner
runner = Runner(agent=agent, app_name="architecture_advisor")
response = runner.run("What are the key considerations for the notification system?")
print(response)
```

## `ctx.to_instruction()` / `GoogleADKHelper.to_instruction()`

Both methods return the assembled context as a plain string for the ADK `instruction` field:

```python
# Via helper
from mycontext.integrations import GoogleADKHelper
instruction = GoogleADKHelper.to_instruction(ctx)

# Via Context method
instruction = ctx.assemble()
```

## GoogleADKHelper Methods

### `create_agent(context, name, model, description, tools, **kwargs)`

```python
agent = GoogleADKHelper.create_agent(
    context=ctx,
    name="risk_analyst",
    model="gemini-2.0-flash",        # Default
    description="Risk analysis specialist",
    tools=[search_tool, calculator],  # Optional ADK tools
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `context` | `Context` | required | mycontext Context |
| `name` | `str` | `"agent"` | Agent name |
| `model` | `str` | `"gemini-2.0-flash"` | Gemini model |
| `description` | `str \| None` | None | Auto-derived from directive |
| `tools` | `list \| None` | `[]` | ADK tool list |

### `to_instruction(context)`

```python
instruction = GoogleADKHelper.to_instruction(ctx)
# Returns the full assembled context string
```

## Multi-Agent ADK Pipeline

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.templates.free.planning import ScenarioPlanner
from mycontext.templates.free.specialized import RiskAssessor
from mycontext.integrations import GoogleADKHelper

# Each agent powered by a different cognitive framework
diagnostician = GoogleADKHelper.create_agent(
    RootCauseAnalyzer().build_context(
        problem="Mobile app retention dropped 35%",
        depth="comprehensive",
    ),
    name="diagnostician",
    model="gemini-2.0-flash",
)

planner = GoogleADKHelper.create_agent(
    ScenarioPlanner().build_context(
        topic="Mobile retention recovery strategies",
        timeframe="6 months",
    ),
    name="planner",
    model="gemini-2.0-flash",
)

risk_agent = GoogleADKHelper.create_agent(
    RiskAssessor().build_context(
        decision="Invest in onboarding redesign vs. feature expansion",
        depth="thorough",
    ),
    name="risk_analyst",
    model="gemini-2.0-flash",
)
```

## Direct Context Export

If you need more control, export the context string and build the ADK agent manually:

```python
from mycontext.templates.free.analysis import DataAnalyzer
from google.adk.agents import Agent

ctx = DataAnalyzer().build_context(
    data_description="User engagement metrics: DAU, session length, feature usage",
    goal="Identify leading indicators of premium conversion",
)

agent = Agent(
    model="gemini-2.0-flash",
    name="conversion_analyst",
    instruction=ctx.assemble(),     # mycontext cognitive framework
    description="Analyzes engagement data to predict premium conversion",
    tools=[bigquery_tool],
)
```

## API Reference

### `GoogleADKHelper`

| Method | Returns | Description |
|--------|---------|-------------|
| `to_instruction(context)` | `str` | Assembled context as ADK instruction |
| `create_agent(context, name, model, description, tools, **kwargs)` | `Agent` | Google ADK Agent |
