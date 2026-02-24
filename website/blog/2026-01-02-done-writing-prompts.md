---
slug: done-writing-prompts
title: I'm Done Writing Prompts. Here's What I Do Instead.
authors: [dhiraj]
tags: [context-engineering, prompt-engineering, mycontext-ai]
date: 2026-01-02
---

I've been building with LLMs since early 2023. In that time I've written thousands of prompts. Some were good. Most were mediocre. And for a long time, I couldn't tell the difference until I saw the output — sometimes days later in production logs.

That frustration is what eventually led me to build mycontext-ai. And it started with a simple realization: **the problem was never how I was asking the question. It was the absence of any structure around the question itself.**

<!-- truncate -->

## The prompt engineering phase

When I started, the advice was consistent: be specific, give examples, use chain-of-thought. Write better prompts. That advice isn't wrong, but it addresses symptoms, not the root issue.

The root issue is that a prompt is just a string. There's no type system, no schema, no way to separate "who is the AI being" from "what should it do" from "what are the hard rules." Everything is mashed into one blob of text. When it doesn't work, you don't know which part to fix.

I'd spend hours tweaking prompt wording, moving sentences around, adding more context — and getting inconsistent results that I couldn't reason about systematically.

## What changed my thinking

In mid-2025, I started paying attention to a term that was appearing more often in the research community: **context engineering**. The framing was different from prompt engineering. Instead of "how do I ask this better," the question was "how do I construct the information environment that will make this LLM genuinely useful for this task?"

That shift matters. It turns a creative writing problem into an engineering problem. And engineering problems can be solved systematically.

The research I was reading pointed to something clear: LLMs behave consistently when given structured context. The variance in output quality is largely a function of how well the context is constructed, not which exact words you use.

## The approach we took with mycontext-ai

We built mycontext-ai around the idea of **Context as Code** — treating the context you give to an LLM as a first-class structured artifact, not a string you compose in your head.

A context in mycontext-ai has four distinct parts:

- **Guidance** — who the LLM is being (role, rules, communication style)
- **Directive** — what it's being asked to do right now
- **Constraints** — the hard rules about the output
- **Knowledge** — grounding information it needs to do the task

These map cleanly onto how good human experts operate. A doctor diagnosing a patient isn't just "answering a question" — they have a role, a systematic methodology, constraints (don't cause harm, stay evidence-based), and knowledge (the patient's history, test results).

When you encode that structure explicitly rather than hoping the LLM infers it from a blob of text, the outputs get more consistent, more predictable, and — when you instrument it — measurably better.

## What this means practically

Here's what my workflow looks like now versus two years ago:

**Before:**
```python
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Analyze why our API latency tripled after the deployment"}]
)
```

**Now:**
```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

ctx = RootCauseAnalyzer().build_context(
    problem="API latency tripled after Friday's deployment",
    depth="comprehensive",
)
result = ctx.execute(provider="openai", model="gpt-4o")
```

The second version doesn't just produce better output. It produces output I can reason about. The context itself has a quality score. I can compare two versions of a context. I can benchmark it across models. I can serialize it, cache it, and reuse it.

None of that is possible with a string.

## This is not a complete solution

I want to be honest: mycontext-ai doesn't solve every problem in LLM development. Model quality still matters enormously. Retrieval architecture still matters. Fine-tuning still has its place.

But it does solve a specific, real problem that I've personally spent hundreds of hours fighting: **the lack of a principled way to construct, measure, and iterate on the information you give to LLMs.**

If you're building anything serious with LLMs right now and you're still working at the raw prompt level, I'd encourage you to try a different abstraction. Not because it's fancy, but because it'll save you time and make your systems more reliable.

Give it a try:

```bash
pip install mycontext-ai
```

We're at v0.3.0 with 85 cognitive patterns, quality metrics, and integrations for most major frameworks. The [docs](/docs/getting-started/quickstart) are here if you want to dig in.

— Dhiraj
