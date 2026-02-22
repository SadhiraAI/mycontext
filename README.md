# mycontext-ai

<div align="center">

**Context engineering for LLMs. Build once, run anywhere, measure everything.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/mycontext-ai.svg)](https://pypi.org/project/mycontext-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[The Problem](#the-problem) · [Core Strengths](#core-strengths) · [Quick Start](#quick-start) · [Use Cases](#use-cases) · [Patterns](#85-cognitive-patterns)

</div>

---

## The Problem

Every team building with LLMs hits the same wall:

- **Prompt roulette.** You tweak wording for hours. Sometimes it works, sometimes it doesn't. There's no way to know *why*.
- **Vendor lock-in.** Your prompts are written for OpenAI. Now the team wants Claude. Rewrite everything.
- **No structure.** System messages, user messages, constraints, output format — every developer invents their own convention.
- **No measurement.** Is this prompt good? Better than yesterday's? Nobody knows until production breaks.
- **Reinventing the wheel.** Root cause analysis, decision frameworks, comparative reasoning — proven cognitive methods exist, but teams write ad-hoc prompts from scratch every time.
- **No way to prove templates help.** You built a prompt template, but can you *prove* it produces better output than a raw question?

## How It Works

mycontext-ai gives you a **structured `Context` object** that separates *what the AI should know* (guidance) from *what it should do* (directive) and *what it must not do* (constraints). You build the context once and export it to any LLM or framework.

```
Raw question
    ↓
[ Intelligence Layer ] — auto-selects the right cognitive pattern
    ↓
Three execution tiers:
  ├─ Static Generic  — zero-cost compiled prompt (1 LLM call)
  ├─ Dynamic Compiled — LLM-refined prompt artifact (2-3 calls)
  └─ Full Response    — complete template execution (2-3 calls)
    ↓
Export: OpenAI │ Anthropic │ Gemini │ LangChain │ YAML │ 13 formats
    ↓
[ Quality Metrics ] — score, compare, improve
    ↓
[ CAI ] — prove the template made a measurable difference
```

The engine doesn't generate answers. It generates the *best possible question* for the LLM you're sending it to — and it can *prove* it.

---

## Core Strengths

These are capabilities that exist in mycontext-ai and, to our knowledge, do not exist in any other open-source context or prompt engineering library.

### 1. 85 Research-Backed Cognitive Patterns

Not generic "write a poem" templates. Each pattern implements a real cognitive framework — Five Whys, fishbone analysis, Socratic method, temporal reasoning, systems archetypes, ethical frameworks — backed by **150+ peer-reviewed papers** from cognitive science, decision theory, and systems thinking.

Every pattern has a structured `build_context()` method with validated inputs, a research-grounded directive, and constraints tuned for the method.

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

ctx = RootCauseAnalyzer().build_context(
    problem="API response times tripled after last deployment",
    depth="comprehensive",
)
```

### 2. Quality Metrics — Score Any Context on 6 Dimensions

No more guessing. `QualityMetrics` evaluates any context across six calibrated dimensions: **clarity, completeness, specificity, relevance, structure, efficiency**. Returns a numeric score, concrete issues, strengths, and actionable suggestions.

Compare two contexts to measure improvement:

```python
from mycontext.intelligence import QualityMetrics

metrics = QualityMetrics()
score = metrics.evaluate(ctx)
print(metrics.report(score))
# → Overall: 0.87 | Clarity: 0.92 | Completeness: 0.85 | ...
# → Issues: ["Directive could be more specific about output format"]
# → Suggestions: ["Add constraints for response length"]

# Compare before/after
diff = metrics.compare(old_ctx, new_ctx)
```

### 3. Context Amplification Index (CAI) — Prove Templates Work

CAI is a quantitative metric that answers: *"Did this template actually produce better LLM output than a raw prompt?"*

It runs the same question through a raw prompt and a template-built context, evaluates both outputs, and computes the ratio:

**CAI = templated_score / raw_score**

A CAI of 1.3x means the template produced 30% better output. No opinions — numbers.

```python
from mycontext.intelligence import ContextAmplificationIndex

cai = ContextAmplificationIndex(provider="openai")
result = cai.measure(
    question="Why are API response times 3x slower after deploy?",
    template_name="root_cause_analyzer",
)
print(f"CAI: {result.cai_overall:.2f}x ({result.verdict})")
# → CAI: 1.42x (significant lift)
```

### 4. Output Evaluator — Score LLM Responses, Not Just Prompts

Other tools score prompts. mycontext also scores the *output*. The Output Evaluator measures LLM responses across five dimensions that are distinct from prompt quality:

- **Instruction Following** — did it do what the context asked?
- **Reasoning Depth** — shallow bullet points or genuine analysis?
- **Actionability** — can you act on the recommendations?
- **Structure Compliance** — did it follow the requested format?
- **Cognitive Scaffolding** — did it use the reasoning framework from the template?

```python
from mycontext.intelligence import OutputEvaluator, OutputDimension

evaluator = OutputEvaluator()
score = evaluator.evaluate(ctx, llm_response)
print(f"Output quality: {score.overall:.2f}")
print(f"Reasoning depth: {score.dimensions[OutputDimension.REASONING_DEPTH]:.2f}")
```

### 5. Template Integrator Agent — Fuse Multiple Patterns Into One

When a question needs multiple cognitive methods (e.g., root cause *and* scenario planning *and* stakeholder analysis), the Template Integrator doesn't just concatenate them. It uses an LLM to **intelligently merge** methodologies from multiple templates into a single unified context — one role, one set of rules, one directive.

```python
from mycontext.intelligence import TemplateIntegratorAgent

integrator = TemplateIntegratorAgent()
result = integrator.suggest_and_integrate(
    "Revenue dropped 40% — what happened, what are the scenarios, who's affected?",
    provider="openai",
)
ctx = result.to_context()
ctx.execute(provider="openai")
```

### 6. Chain Orchestration Agent — Auto-Build Multi-Step Workflows

Complex questions need multiple reasoning steps. The Chain Orchestration Agent analyzes your question, selects and orders patterns from the full catalog, and generates the `build_context()` parameters for each step — automatically.

```python
from mycontext.intelligence import build_workflow_chain

result = build_workflow_chain(
    "Outage last week caused churn spike. What happened, root cause, and recovery plan?",
    provider="openai",
)
print(result.chain)        # ['temporal_sequence_analyzer', 'root_cause_analyzer', 'future_scenario_planner']
print(result.chain_params) # auto-generated build_context params for each step
```

### 7. Intelligent Pattern Suggestion — Keyword, LLM, or Hybrid

Don't know which pattern fits? `suggest_patterns()` maps your question to the best patterns using keyword matching, LLM reasoning, or both:

```python
from mycontext.intelligence import suggest_patterns

result = suggest_patterns(
    "Why did revenue drop? Timeline, root cause, and what to do next.",
    mode="hybrid",
    llm_provider="openai",
    suggest_chain=True,
)
print(result.suggested_chain)
# → ['temporal_sequence_analyzer', 'root_cause_analyzer', 'future_scenario_planner']
print(result.to_markdown())
```

### 8. Auto-Transform Any Question → Perfect Context

One call. No pattern selection needed. The Transformation Engine analyzes your input (type, complexity, domain, key concepts) and builds the right context automatically:

```python
from mycontext.intelligence import transform

ctx = transform("Should we migrate to microservices? Compare tradeoffs.")
# Engine detects: comparison + decision → selects ComparativeAnalyzer
print(ctx.to_markdown())
```

### 9. Blueprint — Multi-Component Context Architecture

For production applications that need more than a single template. Blueprints orchestrate multiple components (guidance, knowledge, reasoning) with **token budget management** and strategy-based optimization (speed / quality / cost / balanced):

```python
from mycontext.structure import Blueprint
from mycontext.foundation import Guidance

blueprint = Blueprint(
    name="research_assistant",
    guidance=Guidance(role="Expert research analyst"),
    directive_template="Research and explain: {topic}",
    token_budget=4000,
    optimization="balanced",
)
ctx = blueprint.build(topic="Quantum computing advances in 2025")
```

### 10. 13 Export Formats — True Vendor Neutrality

Build once, export everywhere. One context works with every LLM and framework:

```python
ctx.to_openai()       # OpenAI Chat API
ctx.to_anthropic()    # Claude
ctx.to_google()       # Gemini
ctx.to_langchain()    # LangChain messages
ctx.to_llamaindex()   # LlamaIndex
ctx.to_crewai()       # CrewAI
ctx.to_autogen()      # AutoGen
ctx.to_yaml()         # Portable config
ctx.to_json()         # JSON
ctx.to_xml()          # XML
ctx.to_markdown()     # Human-readable
ctx.to_messages()     # Universal message list
ctx.to_dict()         # Python dict
```

Plus dedicated integration helpers for **LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel, and Google ADK**.

### 11. Agent Skills with Quality Gates

Define reusable skills as SKILL.md files. Fuse them with cognitive patterns. Gate execution on quality — if the generated context scores below threshold, it blocks *before* wasting an API call:

```python
from mycontext.skills import SkillRunner, improvement_report, suggested_edits

runner = SkillRunner()
result = runner.run(
    Path("skills/compare_options"),
    task="Compare microservices vs monolith",
    quality_threshold=0.7,
)
print(f"Quality: {result.quality_score.overall}, Gated: {result.gated}")

# Get concrete improvement suggestions for the skill
print(improvement_report(result))
for edit in suggested_edits(result):
    print(f"  → {edit}")
```

Skills can declare `pattern: comparative_analyzer` in frontmatter — the runner fuses the skill body with that cognitive pattern automatically.

### 12. Template Benchmarking with CAI

Automated test suites for cognitive templates. Load YAML test cases, run templates through questions, evaluate output quality, and compute CAI scores — in CI or from the CLI:

```bash
python -m mycontext.benchmark_cli run --template diagnostic_root_cause_analyzer
python -m mycontext.benchmark_cli run-all --output results.json
```

### 13. Generic Prompts — Zero-Cost Cognitive Scaffolding

Every template carries a hand-crafted `GENERIC_PROMPT` (~600-1200 chars) that distills its core methodology into a self-contained prompt. No LLM call needed — just string substitution.

Two modes per template: **generic** (fast, lightweight) or **full** (rich, structured):

```python
from mycontext.templates.free.reasoning import RootCauseAnalyzer

# Generic mode — zero-cost prompt
rca = RootCauseAnalyzer()
prompt = rca.generic_prompt(problem="Server crashes during peak hours")
print(len(prompt))  # ~946 chars

# Or get any template's generic prompt with automatic fallback
from mycontext.intelligence import get_generic_prompt_for

prompt = get_generic_prompt_for("root_cause_analyzer", "Why did sales drop?")
```

### 14. Prompt Compilation Pipeline — Reusable Prompt Artifacts

Instead of executing templates and getting responses, compile them into **reusable, provider-agnostic prompts** that can be executed on any LLM:

```python
from mycontext.intelligence import smart_prompt

composed = smart_prompt("Should we migrate to microservices?", provider="openai")
print(composed.to_string())    # reusable prompt artifact
response = composed.execute()  # or execute directly
```

### 15. Static Generic Compilation — Maximum Cost Efficiency

Compile generic prompts from multiple templates with **zero LLM calls for compilation**. The only LLM call is the complexity assessment:

```python
from mycontext.intelligence import smart_generic_prompt

# 1 LLM call (assessment) + 0 (compilation) → optimized prompt
composed = smart_generic_prompt(
    "Our team has communication breakdowns. Diagnose and solve.",
    provider="openai"
)
print(composed.source_templates)  # e.g. ['root_cause_analyzer']
response = composed.execute()     # execute with 1 more call
```

### 16. Three-Tier Execution Model

Choose your cost/quality tradeoff:

| Tier | Function | LLM Calls | Validated Quality |
|------|----------|-----------|-------------------|
| **Static Generic** | `smart_generic_prompt()` | 1 + 0 | ~95% avg |
| **Dynamic Compiled** | `smart_prompt()` | 1 + 1-3 | ~95% avg |
| **Full Response** | `smart_execute()` | 1 + 1-2 | ~96% avg |

All three tiers validated across 6 sprints of controlled experimentation (60+ experimental runs, 10 diverse questions, 5 evaluation dimensions).

### 17. Complexity Router — Automatic Template Selection

`assess_complexity()` classifies your question and decides the optimal approach *before* running anything:

```python
from mycontext.intelligence import assess_complexity, smart_execute

# Automatic: routes to raw, single template, or integrated
response, meta = smart_execute("Why did churn spike 40%?", provider="openai")
print(meta['mode'])            # 'single_template' or 'integrated'
print(meta['templates_used'])  # ['root_cause_analyzer']
```

### 18. Built-In Retry & Timeout

All LLM calls include automatic retry with exponential backoff (rate limits, timeouts, server errors) and configurable timeout — production-ready out of the box.

---

## At a Glance

| Capability | mycontext-ai | Typical prompt libraries |
|-----------|-------------|------------------------|
| Cognitive patterns | 85 research-backed (16 free + 69 enterprise) | 10-20 generic templates |
| Generic prompts (zero-cost) | 85 pre-authored, compilable | None |
| Prompt compilation pipeline | Static + dynamic + full (3 tiers) | None |
| Complexity router | Auto-selects optimal approach per question | None |
| Context quality scoring | 6 dimensions + issues + suggestions | None |
| Output quality scoring | 5 dimensions (separate from prompt quality) | None |
| Template effectiveness proof | CAI (quantitative lift measurement) | None |
| Pattern suggestion | Keyword + LLM + hybrid modes | Manual selection |
| Multi-template fusion | Intelligent merge (not concatenation) | None |
| Workflow chain generation | Auto-select + auto-parameterize | Manual |
| Export formats | 13 (OpenAI, Anthropic, LangChain, YAML, ...) | 1-2 |
| Framework integrations | 7 (LangChain, CrewAI, AutoGen, DSPy, ...) | 0-1 |
| Agent Skills + quality gate | Pattern-fused skills with threshold gating | None |
| Retry + timeout | Built-in exponential backoff | DIY |
| Research citations | 150+ peer-reviewed papers | 0-5 |

---

## Quick Start

```bash
pip install mycontext-ai

# Add LLM execution (recommended)
pip install litellm
```

```python
from mycontext import Context, Guidance, Directive

ctx = Context(
    guidance=Guidance(
        role="Senior security reviewer",
        rules=["Flag every injection risk", "Suggest concrete fixes"],
        style="concise, actionable",
    ),
    directive=Directive(content="Review this API for auth and input validation."),
)

# Export to any LLM
ctx.to_openai()      # → OpenAI messages
ctx.to_anthropic()   # → Claude format
ctx.to_langchain()   # → LangChain messages

# Or execute directly (requires litellm)
result = ctx.execute(provider="openai")
```

All providers route through LiteLLM, giving you access to 100+ models. You can also register custom providers (e.g., Ollama for local models).

---

## Use Cases

### Chain patterns for complex analysis

Strategic questions need multiple reasoning steps. Chain patterns so each stage feeds the next:

```python
# Enterprise templates — requires license (see Enterprise Patterns section)
from mycontext.templates.enterprise.temporal import TemporalSequenceAnalyzer
from mycontext.templates.free.reasoning import RootCauseAnalyzer
from mycontext.templates.enterprise.synthesis import HolisticIntegrator

# Stage 1: Timeline
ctx1 = TemporalSequenceAnalyzer().build_context(
    events="Q1: Support tickets doubled. Q2: Competitor launched. Q3: Complaints up 40%.",
    time_span="12 months",
)

# Stage 2: Root cause (fed by Stage 1 output)
ctx2 = RootCauseAnalyzer().build_context(
    problem="Customer satisfaction collapse",
    symptoms=ctx1.directive.content[:2500],
)

# Stage 3: Synthesis
ctx3 = HolisticIntegrator().build_context(
    topic="Recovery strategy",
    perspectives=f"Timeline: {ctx1.directive.content[:600]}\nRCA: {ctx2.directive.content[:600]}",
)
result = ctx3.execute(provider="openai")
```

### Drop into any orchestrator

mycontext contexts work as tools inside LangChain, CrewAI, smolagents, AutoGen, Semantic Kernel, and Google ADK:

```python
from mycontext.intelligence import transform
from mycontext.integrations import LangChainHelper

ctx = transform("What are the top 3 risks for this launch?")
messages = LangChainHelper.to_messages(ctx)
# → Use in your LangChain chain or agent
```

Integration helpers are available for all 7 frameworks out of the box.

### Enforce structured output

```python
from mycontext.utils.structured_output import output_format

instruction = output_format("json", schema={"summary": "str", "risks": "list", "recommendation": "str"})
ctx = Context(directive=Directive(content=f"Analyze this proposal.\n\n{instruction}"))
```

---

## 85 Cognitive Patterns

### Free Patterns (16)

Included in every install. Production-ready for analysis, decision-making, reasoning, and communication.

| Pattern | What it does |
|---------|-------------|
| **RootCauseAnalyzer** | Five Whys + fishbone + systematic diagnosis |
| **DataAnalyzer** | Data description → analysis plan → insights |
| **QuestionAnalyzer** | Decompose complex questions into structured inquiry |
| **StepByStepReasoner** | Chain-of-thought with explicit reasoning steps |
| **HypothesisGenerator** | Generate and evaluate competing hypotheses |
| **ScenarioPlanner** | Future scenarios with probability assessment |
| **RiskAssessor** | Risk identification, scoring, and mitigation |
| **Brainstormer** | Structured ideation with divergent/convergent phases |
| **CodeReviewer** | Security, performance, and maintainability review |
| **TechnicalTranslator** | Translate technical content for different audiences |
| **AudienceAdapter** | Adapt message for specific audience and context |
| **SocraticQuestioner** | Guided inquiry through Socratic method |
| **SynthesisBuilder** | Integrate multiple sources into coherent synthesis |
| **StakeholderMapper** | Map stakeholders, interests, and influence |
| **ConflictResolver** | Mediate conflicts by identifying interests and common ground |
| **IntentRecognizer** | Identify core intent, goals, and motivations behind a statement |

### Enterprise Patterns (+69)

Advanced patterns for temporal reasoning, diagnostics, systems thinking, ethical analysis, metacognition, learning science, and cross-domain synthesis. **Enterprise patterns require a valid license key.** Contact us to obtain a license.

The SDK will warn you when an enterprise template is accessed without a license and automatically suggest free alternatives:

```python
import mycontext

# Without license — SDK warns and falls back to best free template
from mycontext.intelligence import smart_execute
response, meta = smart_execute("Analyze this...", include_enterprise=False)
# → UserWarning: Template 'causal_reasoner' requires an enterprise license.
#   Free alternatives (16 templates) are available.

# With license — full access
mycontext.activate_license("MC-ENT-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
response, meta = smart_execute("Analyze this...", include_enterprise=True)
```

**Categories:** Metacognition · Ethical Reasoning · Systems Thinking · Learning & Knowledge Building · Evaluation & Assessment · Temporal Reasoning · Diagnostic & Troubleshooting · Synthesis & Integration · Advanced Decision · Advanced Problem Solving · Advanced Planning · Advanced Analysis · Advanced Reasoning · Advanced Creative · Advanced Communication · Advanced Specialized

---

## Web Application

mycontext also ships as a full-featured **web application** — a context engineering workbench with a visual pattern library, chain builder, and an AI-powered Context Copilot that guides you through building and refining contexts step by step. The web app is available separately from the SDK.

---

## Installation

```bash
# Core SDK (includes 16 free patterns, intelligence layer, quality metrics)
pip install mycontext-ai

# Add LLM execution support (recommended)
pip install mycontext-ai litellm

# Optional: provider-specific SDKs
pip install "mycontext-ai[openai]"       # OpenAI SDK
pip install "mycontext-ai[anthropic]"    # Anthropic SDK
pip install "mycontext-ai[google]"       # Google GenAI SDK
pip install "mycontext-ai[all]"          # All provider SDKs
```

---

## What This Is (and Isn't)

**mycontext-ai is a context engineering library.** It structures and transforms your questions into high-quality prompts using research-backed cognitive patterns. It measures prompt quality *and* output quality. It proves templates work with quantitative metrics. It exports to any LLM format.

**It is not** a prompt template string library. It is not an LLM wrapper. It is not an agent framework. It works *with* your existing agent framework (LangChain, CrewAI, AutoGen, etc.) by giving it better inputs.

The core insight: **the quality of an LLM's output is bounded by the quality of its input.** mycontext engineers that input — and proves it.

---

## License

MIT. Free edition includes 16 patterns and the full intelligence layer. Enterprise edition (+69 advanced patterns) requires a license key.

---

<div align="center">

**The quality of an LLM's output is bounded by the quality of its input.**

[Get Started](#quick-start)

</div>
