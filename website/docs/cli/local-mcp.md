---
sidebar_position: 3
title: Local MCP Server
description: Run a local stdio MCP server that exposes mycontext's offline capabilities — suggest_patterns, transform, and score_output — to any MCP client.
---

# Local MCP Server

`mycontext mcp` starts a [Model Context Protocol](https://modelcontextprotocol.io)
server over stdio. It runs **entirely on your machine** — no network, no hosted
service, no cost — and exposes mycontext's offline capabilities to any MCP client
(Claude Code, Cursor, Cowork, and others).

## Install

The MCP server needs the optional `mcp` extra:

```bash
pip install "mycontext-ai[mcp]"
```

## Run

```bash
mycontext mcp
```

The process speaks MCP over stdio and blocks until the client disconnects.

## Tools exposed

| Tool | LLM call? | Description |
|------|-----------|-------------|
| `suggest_patterns` | No | Recommend cognitive patterns for a question, with an optional ordered chain and reasoning |
| `transform` | No | Turn raw input into a structured, portable context (assembled prompt + patterns applied) |
| `score_output` | No | Heuristically score an LLM output against the context that produced it |

All three are deterministic and offline.

### `suggest_patterns(question, max_patterns=5)`

```json
{
  "patterns": [
    {"name": "root_cause_analyzer", "category": "reasoning", "reason": "..."}
  ],
  "chain": ["root_cause_analyzer", "data_analyzer"],
  "reasoning": "..."
}
```

### `transform(text, patterns="auto")`

```json
{
  "assembled": "ROLE: ...\nTASK: ...",
  "patterns_applied": ["decision_framework"]
}
```

### `score_output(context_prompt, output)`

```json
{
  "overall": 0.82,
  "dimensions": {"instruction_following": 0.9, "reasoning_depth": 0.8},
  "strengths": ["..."],
  "weaknesses": ["..."]
}
```

## Wiring it into a client

Point your MCP client at the command. For example, in a client that uses a JSON
server config:

```json
{
  "mcpServers": {
    "mycontext": {
      "command": "mycontext",
      "args": ["mcp"]
    }
  }
}
```
