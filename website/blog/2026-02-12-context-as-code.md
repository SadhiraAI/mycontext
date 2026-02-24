---
slug: context-as-code
title: "Context as Code: The Abstraction That Changes How You Build with LLMs"
authors: [dhiraj]
tags: [context-as-code, architecture, context-engineering, mycontext-ai]
date: 2026-02-12
---

Software development has a long history of finding the right abstraction and watching it unlock an entire class of capabilities. Relational databases gave us SQL and normalized data. Version control gave us reproducible history. Containers gave us environment portability.

Each time, the abstraction wasn't just a convenience — it changed what was possible to build and reason about.

I think context engineering is at a similar inflection point. And the abstraction we're missing is treating context as a structured, version-controllable, measurable artifact — **Context as Code**.

<!-- truncate -->

## What we're doing today, and why it's not enough

Right now, most LLM applications store prompts as strings. Sometimes in code, sometimes in databases, sometimes in configuration files. When something breaks, you look at the string. When you want to improve it, you edit the string.

This approach has worked up to a point. But it has a ceiling. You can't type-check a string. You can't measure the quality of a string without running it. You can't compare two versions of a string systematically. You can't compose two strings and know what you'll get.

As LLM applications get more complex — multi-agent systems, long-running workflows, applications that need to maintain quality standards across hundreds of different prompts — the string-as-prompt model breaks down.

## What "Context as Code" means in practice

In mycontext-ai, a `Context` is a first-class structured object:

```python
from mycontext import Context
from mycontext.foundation import Guidance, Directive, Constraints

ctx = Context(
    guidance=Guidance(
        role="Senior security engineer",
        rules=[
            "Apply OWASP Top 10 methodology",
            "Rank findings by CVSS score",
            "Provide concrete remediation code for each issue",
        ],
    ),
    directive=Directive(
        content="Review this Python authentication handler for security vulnerabilities",
    ),
    constraints=Constraints(
        must_include=["severity", "remediation", "OWASP reference"],
        format_rules=["Group by severity tier", "One issue per bullet"],
    ),
)
```

This context is:
- **Typed** — each field has a schema, not an arbitrary string
- **Composable** — you can combine contexts, layer patterns, merge prompts
- **Measurable** — run `QualityMetrics` on it before you spend a single token
- **Serializable** — export it to JSON, YAML, XML, or any LLM format
- **Portable** — export it to OpenAI, Anthropic, LangChain, CrewAI, or any of 13 formats
- **Version-controllable** — it's code, so it lives in your repo

## The three-tier execution model

One thing that took me a while to get right was the layering. mycontext-ai has three tiers of abstraction, and understanding when to use each makes the whole SDK more useful.

**Tier 1 — Core Context API:** You build contexts manually from `Guidance`, `Directive`, and `Constraints`. Full control. Best for novel use cases where no pattern exists.

**Tier 2 — Pattern API:** You use one of the 85 cognitive patterns. Less work, better defaults, built-in analytical frameworks. Best for the common categories of LLM work.

**Tier 3 — Intelligence Layer:** You describe what you want and the SDK figures out the right pattern and builds the context for you. Least friction, most magic. Best for prototyping and for cases where input type is variable.

```python
# Tier 1 — manual
ctx = Context(guidance=Guidance(...), directive=Directive(...))

# Tier 2 — pattern
ctx = RootCauseAnalyzer().build_context(problem="...", depth="comprehensive")

# Tier 3 — intelligence
ctx = transform("Why did our API latency triple?")
```

You can mix these freely. Start at Tier 3 to prototype, drop to Tier 2 when you know what pattern you need, drop to Tier 1 when you need full control.

## The intelligence layer is where it gets interesting

The intelligence layer is the part of mycontext-ai I'm most proud of, and also the part that required the most thought to design.

The core challenge was: **if someone gives you an arbitrary text input, how do you automatically select the right cognitive framework for it?**

Our answer was `suggest_patterns()` with three modes:
- **keyword mode** — fast, local, no LLM calls, pattern matching on input characteristics
- **LLM mode** — uses a small LLM call to understand input semantics more deeply
- **hybrid mode** — keyword mode first, LLM to resolve ambiguity

The `transform()` function wraps this into a one-liner:

```python
from mycontext import transform

ctx = transform("Should we rewrite our legacy monolith or extend it incrementally?")
# Automatically selects a decision/tradeoff analysis pattern
# Returns a fully structured Context
result = ctx.execute(provider="openai")
```

There's also `smart_execute()` which does all of this and executes in one call, and `build_workflow_chain()` which asks an LLM to design a multi-step analytical workflow for complex goals.

## What this architecture makes possible

When context is structured code, a few things become possible that weren't before:

**CI/CD for LLM quality.** You can run `QualityMetrics` in your test suite. If a context's quality score drops below a threshold, fail the build. This is context testing — the same way we test our application logic.

**Context blueprints as shared infrastructure.** A `Blueprint` in mycontext-ai is a reusable context template that your whole team builds on. One engineer defines the architecture; everyone else instantiates it with their specific data. No more each engineer reinventing their own prompt templates.

**Serialization and caching.** A context is JSON-serializable. Cache expensive pattern builds, store contexts for audit trails, replay them in debugging sessions.

**Cross-framework portability.** Build a context once. Deploy it to OpenAI today, Anthropic tomorrow, a LangChain agent next week — without rewriting anything.

## This is where context engineering is heading

I've been watching the field evolve for the past two years. The direction is clear: the teams doing the best work with LLMs are treating context as a disciplined engineering concern, not a creative writing problem.

That means type systems. It means version control. It means quality metrics. It means reusable components and shared architecture.

mycontext-ai is our attempt to provide those tools in one coherent SDK. We're not there yet on every dimension — this is v0.3.0, not v1.0. But the architecture is right, and the problems it solves are real.

If you want to dig into the three-tier model: [Three-Tier Execution](/docs/intelligence/three-tier-execution). And if you want to understand the intelligence layer more deeply: [Intelligence Layer Overview](/docs/intelligence/overview).

— Dhiraj
