---
slug: 85-cognitive-patterns
title: 85 Cognitive Patterns — The Library I Wish Had Existed Three Years Ago
authors: [dhiraj]
tags: [cognitive-patterns, context-engineering, mycontext-ai]
date: 2026-01-20
---

When I first started using LLMs seriously for work, I noticed something that took me a while to articulate. The same question, asked slightly differently, would get radically different quality answers. And when I looked at what "slightly differently" actually meant in the cases that worked, I kept seeing the same thing: **structure**.

The best prompts I wrote weren't better because of their vocabulary. They were better because they embedded a reasoning methodology. They told the LLM not just what to do but how to think about the problem.

The issue was that I had to reinvent that structure from scratch every time.

<!-- truncate -->

## The problem with ad-hoc prompts

If you've done serious LLM development, you've probably built a personal prompt library. A Notion page or a folder somewhere with templates for different tasks. Things like "the code review template," "the root cause analysis template," "the decision framework template."

Most developers do this informally. The problem is that these templates are usually underdocumented, not tested against each other, and not portable across projects or colleagues. When a new engineer joins the team, they start from scratch.

More fundamentally, you're not building on top of any underlying theory. You're just accumulating patterns that happened to work for you, without knowing why they worked or when they'd fail.

## What a cognitive pattern actually is

A cognitive pattern in mycontext-ai is a structured reasoning framework encoded as a Python class. It's not a template string. It's a reusable context architecture that encodes a specific way of approaching a category of problem.

The `RootCauseAnalyzer`, for example, doesn't just tell the LLM "find the root cause." It encodes a complete methodology: distinguish immediate causes from contributing factors, build a causal chain, separate what happened from why it happened, quantify confidence, and generate prevention steps.

That methodology is grounded in how root cause analysis is actually done — borrowed from fields like systems engineering, safety analysis, and incident response. It's not invented; it's codified.

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

ctx = RootCauseAnalyzer().build_context(
    problem="Feature adoption dropped 40% after the redesign",
    depth="comprehensive",
)
```

The `ctx` you get back contains a full Context object with Guidance, Directive, and Constraints already set. The reasoning framework is baked in. You're not writing a prompt — you're instantiating a proven analytical approach.

## The 16 free patterns cover most everyday work

We ship 16 patterns that are free to use with no license required:

**Reasoning:** RootCauseAnalyzer, StepByStepReasoner, HypothesisGenerator, SynthesisBuilder

**Analysis:** DataAnalyzer, QuestionAnalyzer

**Creative:** Brainstormer

**Specialized:** CodeReviewer, RiskAssessor, ConflictResolver, SocraticQuestioner, IntentRecognizer

**Planning:** ScenarioPlanner, StakeholderMapper

**Communication:** AudienceAdapter, TechnicalTranslator

These cover the tasks that come up most often in software development, research, and decision-making work.

## The enterprise tier goes deeper

The 71 enterprise patterns cover domains where the reasoning methodology matters even more: strategic decision-making, systems thinking, ethical analysis, organizational learning, metacognition, complex diagnostics, and specialized intelligence (RagAnswerer, MemoryCompressor).

Patterns like `DecisionFramework`, `TradeoffAnalyzer`, `FeedbackLoopIdentifier`, `EthicalFrameworkAnalyzer`, and `MetacognitiveMonitor` are designed for situations where you're not just looking for an answer — you're trying to think rigorously about a genuinely hard problem.

I'm particularly proud of the systems thinking category. When you're debugging a complex system (technical or organizational), linear cause-and-effect thinking is usually inadequate. The `FeedbackLoopIdentifier` and `SystemArchetypeAnalyzer` patterns encode non-linear reasoning that most ad-hoc prompts completely miss.

## Why 87 (and counting)?

That's how many we could build to a standard we were happy with. Each pattern is based on documented frameworks — root cause analysis methods from aviation safety, decision theory, the Socratic method, various epistemological frameworks. The count isn't a marketing number; it's just where we are.

Since this post was first published, we've added specialized intelligence patterns like RagAnswerer (grounded RAG with citation and abstention) and MemoryCompressor (structured state extraction for agent memory) — both research-validated. We'll keep adding more. If there's a specific analytical framework you use regularly that isn't represented here, I'd genuinely want to hear about it.

## What building on patterns changes

The most practical change I've noticed since we switched to pattern-based context building: **debugging became a reasoning problem instead of a trial-and-error problem.**

When an LLM output is poor, "which part of my context caused this?" is now a question with a structured answer. Was it the guidance (role/rules)? The directive (the task framing)? The constraints (output requirements)? The pattern choice (wrong analytical framework)?

You can isolate variables. You can run quality metrics to score each component. You can swap patterns and compare results. None of that was possible when everything was a string.

That shift from "tweak the prompt and hope" to "identify the problem and fix it" is the main reason we built this as a pattern library rather than a prompt library.

---

If you want to explore the patterns: [Cognitive Patterns](/docs/cognitive-patterns/overview). All 16 free patterns have individual documentation pages with examples.

And if you're curious about the enterprise patterns (now 71): [Enterprise Overview](/docs/cognitive-patterns/enterprise-overview).

— Dhiraj
