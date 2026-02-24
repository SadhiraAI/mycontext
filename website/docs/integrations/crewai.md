---
sidebar_position: 4
title: CrewAI
description: Power CrewAI agents and tasks with mycontext cognitive patterns. Convert any Context to CrewAI Agent role/goal/backstory and Task expected_output automatically.
---

# CrewAI

Use mycontext cognitive patterns to power CrewAI agents. The `to_crewai()` export automatically maps your `Context` to the role, goal, backstory, and expected_output fields CrewAI needs.

```bash
pip install mycontext-ai crewai
```

## Quick Start

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.integrations import CrewAIHelper
from crewai import Crew, Task

# Build cognitive context
ctx = RootCauseAnalyzer().build_context(
    problem="Customer churn increased 40% in Q3",
    depth="comprehensive",
)

# Create agent with the cognitive framework
agent = CrewAIHelper.create_agent(ctx, name="diagnostician")

# Create matching task
task = CrewAIHelper.create_task(
    ctx,
    description="Diagnose the root causes of the Q3 churn spike",
    agent=agent,
)

# Run the crew
crew = Crew(agents=[agent], tasks=[task], verbose=True)
result = crew.kickoff()
print(result)
```

## `ctx.to_crewai()`

The native export maps your Context to CrewAI's required fields:

```python
ctx = RootCauseAnalyzer().build_context(
    problem="Production database is 10x slower",
)
crew_cfg = ctx.to_crewai()

# {
#   "role": "Root Cause Analysis Specialist",
#   "goal": "Conduct systematic root cause analysis...",
#   "backstory": "You are a Root Cause Analysis Specialist...",
#   "context": "## Role\n...\n## Directive\n...",
#   "expected_output": "Output must include: root cause, contributing factors, prevention",
#   "tools": [],
#   "verbose": True
# }

from crewai import Agent, Task

agent = Agent(
    role=crew_cfg["role"],
    goal=crew_cfg["goal"],
    backstory=crew_cfg["backstory"],
    verbose=True,
)

task = Task(
    description=crew_cfg["goal"],
    expected_output=crew_cfg["expected_output"],
    agent=agent,
)
```

### How the mapping works

| CrewAI field | Source in Context |
|-------------|------------------|
| `role` | `guidance.role` |
| `goal` | `directive.content` |
| `backstory` | Full `guidance.render()` (role + rules + style) |
| `expected_output` | Derived from `constraints.must_include` items |
| `context` | Full `ctx.assemble()` |

## CrewAIHelper Methods

### `create_agent(context, name, tools, **kwargs)`

```python
agent = CrewAIHelper.create_agent(
    context=ctx,
    name="risk_analyst",
    tools=[search_tool, calculator_tool],
    memory=True,           # CrewAI kwargs pass through
    max_iter=10,
)
```

### `create_task(context, description, agent, expected_output, **kwargs)`

```python
task = CrewAIHelper.create_task(
    context=ctx,
    description="Conduct a comprehensive risk assessment",
    agent=agent,
    expected_output="Risk matrix with probability, impact, and mitigation for each risk",
)
```

## Multi-Agent Crew

Build a full research + analysis crew with different cognitive patterns powering each agent:

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer, HypothesisGenerator
from mycontext.templates.free.planning import ScenarioPlanner
from mycontext.templates.free.specialized import RiskAssessor
from mycontext.integrations import CrewAIHelper
from crewai import Crew, Process

# Agent 1: Root cause analyst
rca_ctx = RootCauseAnalyzer().build_context(
    problem="Enterprise churn spiked 40% in Q3",
    depth="comprehensive",
)
analyst = CrewAIHelper.create_agent(rca_ctx, name="root_cause_analyst")

# Agent 2: Hypothesis generator
hyp_ctx = HypothesisGenerator().build_context(
    observation="Churn spike correlates with new pricing rollout",
    domain="SaaS business",
)
scientist = CrewAIHelper.create_agent(hyp_ctx, name="hypothesis_generator")

# Agent 3: Risk assessor
risk_ctx = RiskAssessor().build_context(
    decision="Reverse the pricing change vs. offer discounts",
    depth="thorough",
)
risk_agent = CrewAIHelper.create_agent(risk_ctx, name="risk_assessor")

# Tasks
task1 = CrewAIHelper.create_task(
    rca_ctx,
    description="Diagnose the root causes of Q3 churn spike",
    agent=analyst,
)
task2 = CrewAIHelper.create_task(
    hyp_ctx,
    description="Generate testable hypotheses from the diagnosis",
    agent=scientist,
)
task3 = CrewAIHelper.create_task(
    risk_ctx,
    description="Assess risks of each proposed fix",
    agent=risk_agent,
)

# Sequential crew
crew = Crew(
    agents=[analyst, scientist, risk_agent],
    tasks=[task1, task2, task3],
    process=Process.sequential,
    verbose=True,
)
result = crew.kickoff()
```

## Using with Tools

```python
from crewai.tools import BaseTool
from mycontext.templates.free.analysis import DataAnalyzer
from mycontext.integrations import CrewAIHelper

ctx = DataAnalyzer().build_context(
    data_description="Customer usage metrics and support tickets",
    goal="Identify churn predictors",
)

# Pass tools to the agent
agent = CrewAIHelper.create_agent(
    ctx,
    name="data_analyst",
    tools=[
        database_query_tool,
        csv_reader_tool,
        chart_generator_tool,
    ],
)
```

## API Reference

### `CrewAIHelper`

| Method | Returns | Description |
|--------|---------|-------------|
| `create_agent(context, name, tools, **kwargs)` | `Agent` | CrewAI Agent |
| `create_task(context, description, agent, expected_output, **kwargs)` | `Task` | CrewAI Task |

### `ctx.to_crewai()`

```python
{
    "role": str,             # From guidance.role
    "goal": str,             # From directive.content
    "backstory": str,        # From guidance.render()
    "context": str,          # Full assembled context
    "expected_output": str,  # Derived from constraints.must_include
    "tools": list,           # Empty — user provides tools
    "verbose": bool,         # True
}
```
