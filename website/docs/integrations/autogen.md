---
sidebar_position: 5
title: AutoGen
description: Power Microsoft AutoGen agents with mycontext cognitive patterns. Convert any Context to an AssistantAgent system message.
---

# AutoGen

Use mycontext cognitive patterns as the system message for Microsoft AutoGen agents. The `to_autogen()` export maps your `Context` directly to AutoGen's `AssistantAgent` format.

```bash
pip install mycontext-ai pyautogen
```

## Quick Start

```python
from mycontext.templates.free.specialized import CodeReviewer
from mycontext.integrations import AutoGenHelper
import autogen

# Build cognitive context
ctx = CodeReviewer().build_context(
    code=my_code,
    language="Python",
    focus_areas=["security", "performance"],
)

# LLM config
llm_config = {"model": "gpt-4o-mini", "api_key": "sk-..."}

# Create AutoGen assistant with mycontext system message
assistant = AutoGenHelper.create_assistant(
    ctx,
    name="code_reviewer",
    llm_config=llm_config,
)

# Create user proxy
user = AutoGenHelper.create_user_proxy(name="developer")

# Start conversation
user.initiate_chat(
    assistant,
    message="Please review the authentication code I provided",
)
```

## `ctx.to_autogen()`

The native export maps your Context to AutoGen's `AssistantAgent` format:

```python
ag = ctx.to_autogen()
# {
#   "system_message": "## Role\nSenior code reviewer...\n## Directive\n...",
#   "description": "Review the following code for security...",
#   "max_consecutive_auto_reply": 10,
#   "human_input_mode": "NEVER",
#   "code_execution_config": False,
# }

import autogen
assistant = autogen.AssistantAgent(
    name="reviewer",
    system_message=ag["system_message"],
    llm_config=llm_config,
)
```

## AutoGenHelper Methods

### `create_assistant(context, name, llm_config, **kwargs)`

```python
assistant = AutoGenHelper.create_assistant(
    context=ctx,
    name="analyst",
    llm_config={
        "model": "gpt-4o-mini",
        "api_key": "sk-...",
        "temperature": 0,
    },
    max_consecutive_auto_reply=5,  # AutoGen kwargs pass through
)
```

### `create_user_proxy(name, **kwargs)`

```python
user = AutoGenHelper.create_user_proxy(
    name="user",
    human_input_mode="TERMINATE",
    code_execution_config={"work_dir": "coding"},
)
```

## Multi-Agent Conversation

Use different cognitive patterns for different agents in a group chat:

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer, HypothesisGenerator
from mycontext.templates.free.planning import ScenarioPlanner
from mycontext.integrations import AutoGenHelper
import autogen

llm_config = {"model": "gpt-4o-mini", "api_key": "sk-..."}

# Specialist agents with different cognitive frameworks
rca_ctx = RootCauseAnalyzer().build_context(
    problem="Revenue dropped 20% in November",
    depth="thorough",
)
diagnostician = AutoGenHelper.create_assistant(
    rca_ctx, name="diagnostician", llm_config=llm_config
)

hyp_ctx = HypothesisGenerator().build_context(
    observation="Revenue drop correlates with competitor pricing change",
    domain="SaaS business",
)
scientist = AutoGenHelper.create_assistant(
    hyp_ctx, name="scientist", llm_config=llm_config
)

plan_ctx = ScenarioPlanner().build_context(
    topic="Revenue recovery strategies",
    timeframe="6 months",
)
strategist = AutoGenHelper.create_assistant(
    plan_ctx, name="strategist", llm_config=llm_config
)

user = AutoGenHelper.create_user_proxy(name="product_manager")

# Group chat
groupchat = autogen.GroupChat(
    agents=[user, diagnostician, scientist, strategist],
    messages=[],
    max_round=12,
)
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
)

user.initiate_chat(
    manager,
    message="Our November revenue dropped 20%. Diagnose, hypothesize, and plan recovery.",
)
```

## API Reference

### `AutoGenHelper`

| Method | Returns | Description |
|--------|---------|-------------|
| `create_assistant(context, name, llm_config, **kwargs)` | `AssistantAgent` | AutoGen assistant |
| `create_user_proxy(name, **kwargs)` | `UserProxyAgent` | AutoGen user proxy |

### `ctx.to_autogen()`

```python
{
    "system_message": str,              # Full assembled context
    "description": str,                 # From directive.content
    "max_consecutive_auto_reply": int,  # 10
    "human_input_mode": str,            # "NEVER"
    "code_execution_config": bool,      # False
}
```
