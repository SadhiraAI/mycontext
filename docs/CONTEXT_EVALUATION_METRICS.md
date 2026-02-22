# SadhiraAI Context Evaluation Metrics

**Comprehensive Guide to Context and Output Quality Measurement**

**Document Version:** 1.0  
**Date:** February 15, 2026  
**Author:** SadhiraAI  

---

## 1. Introduction

SadhiraAI's **Context Evaluation Metrics** provide a research-backed framework for measuring the quality of LLM prompts (contexts) and the outputs they produce. This document defines each metric, explains intrinsic vs. extrinsic evaluation, and describes how to measure them in the mycontext SDK.

**Two evaluation levels:**

| Level | What Is Evaluated | Metrics | Purpose |
|-------|-------------------|---------|---------|
| **Context quality** | The input prompt/context | 6 dimensions | Is the prompt well-formed? |
| **Output quality** | The LLM's response | 5 dimensions | Did the output meet expectations? |

Both levels combine **intrinsic** qualities (observable in the text itself) and **extrinsic** qualities (usefulness for downstream tasks). The framework is calibrated against ICLR, ACL, and related benchmarks.

---

## 2. Research Backing

Our metrics are grounded in peer-reviewed work:

### 2.1 ResearchRubrics (ICLR 2026)

**Paper:** [ResearchRubrics: A Benchmark of Prompts and Rubrics For Evaluating Deep Research Agents](https://arxiv.org/abs/2511.07685)

ResearchRubrics evaluates deep research agent outputs on three core dimensions:

- **Factual grounding** — accuracy and evidence-backing of claims
- **Reasoning soundness** — logical validity of multi-step reasoning  
- **Clarity** — quality of presentation and communication

Our **clarity** dimension (context and output) and **reasoning depth** (output) align with these rubrics. We extend the framework to prompt/context quality and task-specific dimensions.

### 2.2 LMUNIT (ACL 2025)

**Reference:** LMUNIT — decomposed natural language unit tests for LLM evaluation.

LMUNIT decomposes evaluation into testable sub-dimensions rather than a single overall score. Our multi-dimensional approach (6 context + 5 output dimensions) follows this decomposition principle.

### 2.3 FLASK (ICLR 2024)

**Paper:** [FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets](https://arxiv.org/abs/2307.10928)

FLASK decomposes coarse evaluation into 12+ fine-grained skills across domains and difficulty levels. We adopt the same idea: each metric is a distinct skill that can be scored and improved independently.

### 2.4 Standard NLP Quality Criteria

**Reference:** ACL Findings 2025 — standardized assessment practices for NLP systems.

We align our scoring calibration and dimension definitions with best practices for prompt and output evaluation.

---

## 3. Intrinsic vs. Extrinsic Evaluation

Evaluation in NLP is traditionally split into:

| Type | Definition | What We Measure | Our Dimensions |
|------|------------|-----------------|----------------|
| **Intrinsic** | Quality of the text itself, in isolation | Fluency, coherence, structure, terminology | Clarity, Structure, Reasoning Depth, Structure Compliance |
| **Extrinsic** | Utility for downstream tasks and users | Does it help the user accomplish something? | Actionability, Relevance |

### 3.1 Intrinsic Metrics

Measured by inspecting the text directly, without user studies or task completion:

- **Clarity** — unambiguous language, precise terms, no vague referents
- **Structure** — organization, hierarchy, formatting
- **Reasoning depth** — explicit logical markers and stepwise reasoning
- **Structure compliance** — adherence to requested format

### 3.2 Extrinsic Metrics

Measured by considering downstream usefulness:

- **Actionability** — presence of concrete, implementable recommendations
- **Relevance** — focus on the task and avoidance of off-topic content

### 3.3 Our Measurement Approach

- **Heuristic mode:** Rule-based signals (e.g., action verbs, reasoning markers, list structure). Fast, no API cost, suitable for intrinsic and some extrinsic proxies.
- **LLM mode:** An LLM judge scores each dimension. Better for extrinsic and nuanced intrinsic assessment.
- **Hybrid mode:** Heuristic first; LLM only when scores are borderline (e.g., 0.45–0.75).

---

## 4. Context Quality Metrics (Input/Prompt)

These six dimensions evaluate the **prompt/context** before it is sent to the LLM.

### 4.1 Clarity (Weight: 20%)

**Definition:** Every instruction is clear and unambiguous. Well-defined terms. No vague or misleading language.

**What we mean:**
- No vague words (thing, stuff, somehow, maybe, whatever) without clear referents
- Clear role (who/what) and directive (what to do)
- Output format specified when needed
- No excessive ambiguous pronouns (it, this, that) without referents

**How we measure:**
- Count vague terms and penalize above a threshold
- Detect role/directive structure (e.g., "you are", "## instructions")
- Check for output format indicators (JSON schema, "respond with")
- Check for defined terms ("defined as", "i.e.", "specifically")

**Research link:** ResearchRubrics "clarity"; FLASK fine-grained presentation quality.

---

### 4.2 Completeness (Weight: 25%)

**Definition:** All necessary prompt components are present.

**What we mean:**
- **Guidance/Role** — who the model should act as
- **Directive** — what to do, with enough detail
- **Goal** — explicit objective
- **Rules** — behavioral or procedural rules
- **Constraints** — must_include, must_not_include, format_rules
- **Examples** — concrete input/output samples

**How we measure:**
- Detect presence of each component (structured or inferred from text)
- Reward substantive directives (>15 words)
- Reward multiple rules and constraints

**Research link:** LMUNIT decomposition; FLASK skill completeness.

---

### 4.3 Specificity (Weight: 15%)

**Definition:** Instructions are concrete and detailed, not generic.

**What we mean:**
- Domain-specific terminology where appropriate
- Concrete examples instead of abstract advice
- Measurable criteria (scores, percentages, scales)
- Avoid generic phrasing ("be helpful", "do your best")

**How we measure:**
- Penalize generic phrases
- Reward domain indicators (algorithm, framework, criteria, etc.)
- Reward examples and structured constraints
- Reward measurable criteria

**Research link:** ResearchRubrics factual grounding; FLASK domain and difficulty annotation.

---

### 4.4 Relevance (Weight: 15%)

**Definition:** Everything is focused on the task; no unnecessary information.

**What we mean:**
- Directive is well-scoped (not too brief, not overly verbose)
- Role aligns with directive
- Constraints keep focus
- Knowledge/context is task-relevant

**How we measure:**
- Directive word count and internal structure
- Presence of knowledge and constraints
- Role–directive alignment checks

**Research link:** Intrinsic "focus" (NLP evaluation); FLASK coherence.

---

### 4.5 Structure (Weight: 15%)

**Definition:** Content is well-organized with clear hierarchy.

**What we mean:**
- Section breaks and logical flow
- Headers and lists for readability
- Guidance → Directive → Constraints hierarchy
- Dedicated constraints section

**How we measure:**
- Count section breaks and formatting markers
- Detect headers and lists
- Check for guidance/directive/constraints structure

**Research link:** FLASK structure and coherence; InstructScore structure.

---

### 4.6 Efficiency (Weight: 10%)

**Definition:** Concise without being incomplete. No redundancy.

**What we mean:**
- Sufficient length (roughly 30+ words for minimal, 80+ for adequate, 150+ for good)
- Low redundancy (unique word ratio)
- No unnecessary repetition

**How we measure:**
- Word count vs. thresholds
- Unique-word ratio (redundancy)
- Balance between brevity and completeness

**Research link:** FLASK conciseness; standard NLP efficiency metrics.

---

## 5. Output Quality Metrics (LLM Response)

These five dimensions evaluate the **LLM output** given the context that produced it.

### 5.1 Instruction Following (Weight: 25%)

**Definition:** The output follows the directive, rules, and constraints from the context.

**What we mean:**
- Action verbs from the context appear in the output
- Required terms ("must include") are present
- Constraints are respected

**How we measure:**
- Extract action verbs from context; count matches in output
- Check required terms
- Combine into a weighted score

**Research link:** FLASK instruction-following skills; ResearchRubrics rubric compliance.

---

### 5.2 Reasoning Depth (Weight: 20%)

**Definition:** Multi-step reasoning; not surface-level answers.

**What we mean:**
- Causal and logical markers (because, therefore, as a result, etc.)
- Numbered steps, headings, nested structure
- Visible reasoning chain

**How we measure:**
- Count reasoning markers
- Count numbered steps and headings
- Combine into a depth score

**Research link:** ResearchRubrics "reasoning soundness"; FLASK reasoning skills.

---

### 5.3 Actionability (Weight: 20%)

**Definition:** Concrete, implementable recommendations the user can act on.

**What we mean:**
- Action-oriented language (recommend, implement, next step, etc.)
- Numbered or bulleted action items
- Concrete specifics (percentages, dates, dollar amounts)

**How we measure:**
- Count action phrases
- Count numbered/bulleted action items
- Count concrete metrics

**Research link:** Extrinsic evaluation; task-utility alignment.

---

### 5.4 Structure Compliance (Weight: 15%)

**Definition:** Output matches the requested format.

**What we mean:**
- JSON when JSON was requested
- Lists when lists were requested
- Headers/sections when structure was requested

**How we measure:**
- Parse context for format cues (json, list, headers)
- Check output for matching structure
- Score based on alignment

**Research link:** FLASK format compliance; InstructScore structure.

---

### 5.5 Cognitive Scaffolding (Weight: 20%)

**Definition:** Output uses the cognitive framework from the template (e.g., pros/cons, root cause, SWOT).

**What we mean:**
- Framework terms from context appear in output
- Output reflects the reasoning structure requested (e.g., Pros/Cons sections)

**How we measure:**
- Detect frameworks in context (root cause, SWOT, pros/cons, etc.)
- Count framework keywords in output
- Compute use ratio

**Research link:** Metacognitive scaffolding (Flavell, Schraw); cognitive tools theory (Brachman & Zucker).

---

## 6. How to Measure

### 6.1 Context Quality (QualityMetrics)

```python
from mycontext import Context
from mycontext.intelligence import QualityMetrics
from mycontext.intelligence.quality_metrics import QualityDimension

metrics = QualityMetrics(mode="heuristic")  # or "llm", "hybrid"
context = Context(
    guidance="Senior data analyst",
    directive="Analyze the CSV and identify trends",
    constraints=...,
)

score = metrics.evaluate(context)

print(f"Overall: {score.overall:.1%}")
print(f"Clarity: {score.dimensions[QualityDimension.CLARITY]:.1%}")
print(f"Completeness: {score.dimensions[QualityDimension.COMPLETENESS]:.1%}")
# ... (specificity, relevance, structure, efficiency)

for issue in score.issues:
    print(f"  - {issue}")
for suggestion in score.suggestions:
    print(f"  + {suggestion}")
```

**Modes:**
- `heuristic` — rule-based, no API calls
- `llm` — LLM judge (~$0.02/eval)
- `hybrid` — heuristic first; LLM for borderline scores

---

### 6.2 Output Quality (OutputEvaluator)

```python
from mycontext import Context
from mycontext.intelligence import OutputEvaluator, OutputDimension

evaluator = OutputEvaluator(mode="heuristic")  # or "llm", "hybrid"
context = Context(guidance="...", directive="...")
llm_output = "..."  # the actual model response

score = evaluator.evaluate(context, llm_output)

print(f"Overall: {score.overall:.1%}")
for dim in OutputDimension:
    val = score.dimensions.get(dim, 0)
    ev = score.evidence.get(dim, "")
    print(f"  {dim.value}: {val:.1%} ({ev})")
```

---

### 6.3 Context Amplification Index (CAI)

CAI measures how much a template improves output quality vs. a raw prompt:

```python
from mycontext import ContextAmplificationIndex

cai = ContextAmplificationIndex(provider="openai")
result = cai.measure(
    question="Why are API response times 3x slower after deploy?",
    template_name="diagnostic_root_cause_analyzer",
    api_key="sk-...",
)

print(f"CAI: {result.cai_overall:.2f}x ({result.verdict})")
# Per-dimension CAI in result.cai_dimensions
```

See `docs/CAI_SDK_GUIDE.md` for full CAI usage.

---

## 7. Scoring Calibration

**Context quality (0–100%):**

| Range | Interpretation |
|-------|----------------|
| 0–25% | Broken / empty / placeholder |
| 25–45% | Minimal / generic |
| 45–65% | Adequate but improvable |
| 65–80% | Good: clear role, specific directive, constraints |
| 80–95% | Very good: comprehensive, examples, tight constraints |
| 95–100% | Exceptional |

**Output quality:** Dimensions use 0.0–1.0. Overall is a weighted average. Scores &lt; 0.4 indicate weakness; ≥ 0.7 indicate strength.

---

## 8. Summary Table

| Dimension | Level | Intrinsic/Extrinsic | One-Line Definition |
|-----------|-------|---------------------|---------------------|
| Clarity | Context | Intrinsic | Unambiguous, well-defined instructions |
| Completeness | Context | Intrinsic | All necessary components present |
| Specificity | Context | Intrinsic | Concrete, detailed, non-generic |
| Relevance | Context | Both | Focused on the task |
| Structure | Context | Intrinsic | Clear hierarchy and organization |
| Efficiency | Context | Intrinsic | Concise, not redundant |
| Instruction Following | Output | Extrinsic | Follows directive and rules |
| Reasoning Depth | Output | Intrinsic | Multi-step, explicit reasoning |
| Actionability | Output | Extrinsic | Concrete, implementable recommendations |
| Structure Compliance | Output | Intrinsic | Matches requested format |
| Cognitive Scaffolding | Output | Both | Uses the template's reasoning framework |

---

## 9. Related Documents

- [CAI_METRICS_EXPLAINED_SIMPLE.md](./CAI_METRICS_EXPLAINED_SIMPLE.md) — Kid-friendly explanation of output metrics and CAI
- [CAI_SDK_GUIDE.md](./CAI_SDK_GUIDE.md) — CAI SDK usage
- [COGNITIVE_PATTERNS_RESEARCH_FOUNDATIONS.md](./COGNITIVE_PATTERNS_RESEARCH_FOUNDATIONS.md) — Research basis for cognitive patterns
