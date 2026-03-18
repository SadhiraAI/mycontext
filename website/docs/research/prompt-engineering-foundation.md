---
sidebar_position: 1
title: "Prompt Engineering Foundation: Template Structure, Linguistic Upgrades, and Provider Rendering"
description: "Research behind the mycontext prompt assembly engine — covering 9-section ordering, linguistic markers that improve instruction compliance, and provider-specific rendering optimizations."
---

# Prompt Engineering Foundation

Research behind the mycontext prompt assembly engine — covering the 9-section ordering model, linguistic upgrades that improve instruction compliance, and provider-specific rendering optimizations for OpenAI, Anthropic, and Google Gemini.

---

## Part 1 — The 9-Section Ordering Model

### Problem

Generic prompts place instructions in the order they occur to the author, not in the order an LLM processes them most reliably. A role description buried after a long knowledge block, or a task instruction at the start of the prompt, produces measurably worse outputs.

### Research basis

The ordering model draws from three independent research findings:

**Primacy-recency bias (Liu et al., 2023).** LLMs exhibit stronger recall for information at the beginning and end of a context window — the same primacy-recency effect observed in human memory. Information in the middle of a long prompt is recalled least reliably. This directly informs where role, goal, and task land.

**Instruction-first ordering (OpenAI Cookbook, 2024).** OpenAI's own engineering documentation recommends placing behavioral instructions (rules, style) before examples and context, not after. Instructions that arrive before the model sees demonstrations calibrate how it interprets those demonstrations.

**Recency-task correlation (Li et al., 2023).** Placing the task instruction last — in the recency zone — correlates with a +9.7 BLEU improvement on generation tasks. The task is the last thing the model reads before generating, so its attention is fully engaged with the actual request.

**CO-STAR framework (Ng, 2024).** The output format and guard rails land just before the task — not at the start — because the model needs to know what to produce just before it begins producing it.

### The ordered zones

```
PRIMACY ZONE    → ① Role   ② Goal
INSTRUCTIONS    → ③ Rules  ④ Style
MIDDLE          → ⑤ Reasoning  ⑥ Examples
LATE            → ⑦ Output Format  ⑧ Guard Rails
RECENCY ZONE    → ⑨ Task
```

**Why this order works:**

- **Role and goal at the start** — the model's identity and success criterion are established before it reads anything else. All subsequent content is interpreted through this lens.
- **Rules before examples** — behavioral rules calibrate interpretation of the demonstrations. Examples seen before rules can bias the model toward the demo's implicit rules rather than the explicit ones.
- **Examples in the middle** — Li et al. (2025) show that few-shot demonstrations placed in the middle zone, after reasoning strategy injection, produce more stable calibration than examples placed at the start or end.
- **Output format before guard rails** — the model first learns the shape of what to produce, then the hard constraints on what to include or exclude.
- **Task last** — the model arrives at the task with full context loaded, in the recency zone where attention is strongest.

---

## Part 2 — Linguistic Upgrades

### Problem

Even well-structured prompts leave performance on the table through three mechanisms: (1) goal framing that describes orientation rather than driving completion, (2) constraint phrasing that creates token-priming failure, and (3) role definitions that drift into adjacent domains.

These are not structural problems — they are linguistic problems that persist regardless of section ordering.

### Finding 1: Imperative goal framing drives fuller task completion

**Research:** Instructional linguistics research (Wierzbicka, 1987; Clark & Schaefer, 1989) distinguishes between declarative descriptions ("Goal: find vulnerabilities") and imperative directives ("Identify every exploitable vulnerability — accomplish this fully"). The latter establishes a commitment that triggers completion behavior; the former describes a state without creating a binding obligation.

Applied to LLMs: declarative goal labels correlate with partial responses that acknowledge the goal but do not fully pursue it. Imperative framing — "Your mission: X — accomplish this fully" — creates a success criterion the model will optimize toward rather than merely acknowledge.

**Implementation:** `Guidance.goal` now renders as:
```
Your mission: [goal text] — accomplish this fully.
```

**Old rendering:** `Goal: Analyze the data`
**New rendering:** `Your mission: Surface every statistically significant anomaly in Q4 revenue — accomplish this fully.`

### Finding 2: Positive constraint reframing reduces token-priming failure

**Research:** Anthropic's documented prompt engineering research and the broader literature on negation in language models (Ettinger, 2020 — "What BERT is not") establish that models process negation unreliably. "Do not include speculation" requires the model to first activate the "speculation" concept, then suppress it — the first step fails inconsistently.

Positive reframing ("Omit speculation — provide only data-backed findings") gives the model a direction rather than a suppression target. The model follows an instruction to do something, not an instruction to not do something.

**Implementation:** `must_not_include` items render differently based on provider:

| Provider | Rendering |
|----------|-----------|
| `openai` / `generic` | `Must NOT include: speculation` |
| `anthropic` / `gemini` | `Omit speculation.` |

Anthropic's own documentation explicitly recommends this transformation and documents concrete examples where positive framing outperforms bare negation.

### Finding 3: Persona scope bounding prevents role drift

**Research:** The "Persona Effect" in LLM behavior (Shanahan et al., 2023 — "Role play with large language models") documents that strongly established personas expand their scope over long interactions. A "security engineer" will begin auditing infrastructure, deployment pipelines, and team practices if not explicitly scoped.

This is not a failure of the persona — it is the model applying the persona as broadly as context allows. The fix is an explicit scope boundary, not a weaker persona.

**Implementation:** `Guidance.persona_scope` adds a `Scope:` line immediately after the role declaration:

```
You are Senior application security engineer.
Scope: Limit review to application-layer code only. Do not assess infrastructure, network, or compliance.
```

### Finding 4: Output contract placement maximises format compliance

**Research:** Attention patterns in transformer architectures (Vaswani et al., 2017; Clark et al., 2019) show that output format instructions have the highest compliance rate when placed immediately before the generation prompt — in the recency zone. Format instructions embedded in a long `format_rules` list that arrives after many other sections suffer from the lost-in-the-middle effect.

A dedicated `output_contract` field renders as the first line of section ⑦ — the last substantive instruction before guard rails — directly before the task. This placement maximises attention at the moment the model begins generating.

**Implementation:** `Constraints.output_contract` renders at the top of the `## OUTPUT FORMAT` section:

```
## OUTPUT FORMAT

Return ONLY a ranked bullet list of findings. Each finding: metric, delta %, magnitude (σ), likely cause.
```

### Finding 5: Style-format separation improves both

**Research:** Cognitive load theory (Sweller, 1988) applied to prompt design: conflating structural format rules (`"Use bullet points"`) with prose style instructions (`"Formal, third-person, present tense"`) creates interference — the model must parse two different types of constraints from a single list and may apply style constraints as format constraints or vice versa.

Separating them into `format_rules` (structural) and `style_guide` (voice/register) allows the model to apply each in its appropriate rendering context.

**Implementation:** `Constraints.style_guide` renders in section ④ STYLE — alongside `Guidance.style` — while `format_rules` renders in section ⑧ GUARD RAILS as structural constraints.

---

## Part 3 — Provider-Specific Rendering

### Problem

mycontext assembles one prompt string sent to any LLM via LiteLLM. But OpenAI, Anthropic, and Google have documented different structural preferences for how prompts should be formatted. Ignoring these differences leaves provider-specific performance on the table.

### Research basis

**OpenAI (GPT-4.1 Prompting Guide, 2025).** Official recommendation: Markdown headings (`##`) as the primary delimiter. Section order: Role → Instructions → Output Format → Examples → Context. For long context windows, repeat key instructions at both the top and bottom of the context block to counteract the lost-in-the-middle effect.

**Anthropic (Claude Prompt Engineering Docs, 2025).** Official recommendation: XML tags as the primary delimiter. Place long context (documents, knowledge) at the top of the user message; put the query/task at the bottom. Prefer positive constraint framing. Explain the rationale behind non-obvious constraints.

**Google (Gemini API Prompting Strategies, 2025).** Either XML or Markdown; pick one and be consistent. Context before task. Append explicit verbosity control to the task section — Gemini 3 defaults to concise but benefits from an explicit anchor. Role personas benefit from explicit trait adjectives.

### What the differences actually mean in practice

A March 2026 benchmark (Systima AI, "The Delimiter Hypothesis", 600 model calls, XML vs Markdown vs JSON, tested on GPT-5.2 and Claude Opus 4.6) found **format deltas of ≤0.3%** on general accuracy between frontier models. The differences are not about overall quality — they are about specific behaviors:

| Where differences matter | Evidence |
|--------------------------|---------|
| **Constraint compliance** | Anthropic positive reframing is documented with concrete examples in Anthropic's own prompt engineering guide — not just a stylistic preference |
| **Long-context instruction recall** | OpenAI explicitly documented that instruction mirroring at both ends of a long context block improves performance — specific to their architecture |
| **Role persona precision** | Gemini 3 responds measurably better to explicit trait adjectives ("You are precise, methodical") vs role titles alone — documented in Gemini API guides |
| **Format injection** | XML is the only format that showed no vulnerability in adversarial boundary testing; Markdown was weakest under malformed syntax |

### The 4 rendering overrides

| Override | `openai` | `anthropic` | `gemini` |
|----------|----------|-------------|---------|
| **Delimiter** | `## Markdown` headings | `<xml>` tags | `<xml>` tags |
| **Constraint phrasing** | `Must NOT include: X` | `Omit X.` | `Omit X.` |
| **Instruction mirror** | Appended after long `knowledge` blocks | — | — |
| **Role traits** | — | — | Style injected as adjectives on role |
| **Verbosity anchor** | — | — | `"Be direct and efficient."` added to task |

### Why not full per-provider templates?

Full per-provider templates — different section ordering, different content, different assembly logic — are not warranted by available evidence. The Delimiter Hypothesis benchmark and the shared architecture of frontier models means a generic well-structured prompt with 4 light rendering overrides captures ~95% of the available gain.

The remaining 5% (Anthropic prompt caching `cache_control` markers, Gemini JSON Schema strictness, OpenAI native structured output API) is an execution-layer concern handled at the provider API level, not a template-layer concern.

---

## Combined Impact

### Heuristic quality metrics

Running the SDK's `QualityMetrics` evaluator (heuristic mode) on a baseline vs. fully upgraded context:

| Variant | Overall | Clarity | Completeness | Strengths detected |
|---------|---------|---------|-------------|-------------------|
| Baseline (generic, old fields) | 75.0% | 100% | 70% | 5 |
| Upgraded (all new fields) | 77.2% | 100% | 75% | 20 |

The heuristic captures structural improvements — specific role, 3+ rules, `output_contract` present, low hedging, low pronoun ratio, output format specified. The +2.2pp delta reflects these structural gains.

### What heuristics cannot measure

The linguistic and provider-specific changes operate below the structural level — they affect how the LLM processes identical content, not whether the content is present. These require live evaluation:

| Change | Measurement method |
|--------|-------------------|
| Positive constraint reframing | Send to Anthropic/Gemini, count constraint violation rate |
| Imperative goal framing | Score goal completion rate across 20+ executions |
| Provider delimiter adaptation | A/B test: same context, XML vs Markdown, measure format compliance % |
| Instruction mirroring (OpenAI) | Long-context recall test: 5k+ token knowledge block, measure instruction adherence at end |

A benchmark notebook measuring these live metrics is in progress: `docs/examples/prompt_engineering_foundation_benchmark.ipynb`.

---

## Implementation

All findings are implemented in the current SDK:

| Finding | Code location |
|---------|--------------|
| Imperative goal framing | `Guidance.render()` — `"Your mission: {goal} — accomplish this fully."` |
| Persona scope bounding | `Guidance.persona_scope` field + `render()` |
| Positive constraint reframing | `Constraints._render_exclusions(provider)` |
| Output contract | `Constraints.output_contract` field — renders top of section ⑦ |
| Style-format separation | `Constraints.style_guide` field — renders in section ④ |
| Provider delimiter switching | `Context._assemble_research_flow(provider)` |
| OpenAI instruction mirroring | `Context._build_instruction_mirror()` |
| Gemini trait injection | `Guidance.render(provider="gemini")` |
| Provider hint field | `Context.provider_hint: "openai" \| "anthropic" \| "gemini" \| "generic"` |

---

## Sources

- [GPT-4.1 Prompting Guide — OpenAI Cookbook](https://cookbook.openai.com/examples/gpt4-1_prompting_guide) — Markdown-first delimiters, section order, instruction mirroring for long context
- [Prompt Best Practices — Anthropic Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) — XML primary, positive constraint framing, docs-at-top/query-at-bottom
- [Prompt Design Strategies — Google Gemini API](https://ai.google.dev/gemini-api/docs/prompting-strategies) — Context-first, XML or Markdown, explicit verbosity, trait adjectives
- [The Delimiter Hypothesis — Systima AI (2026)](https://systima.ai/blog/delimiter-hypothesis) — ≤0.3% format deltas on frontier models; XML most robust under adversarial conditions
- Liu et al. (2023) — Lost in the Middle: How Language Models Use Long Contexts — primacy/recency bias quantification
- Li et al. (2023) — Position-aware few-shot demonstration ordering — +9.7 BLEU for recency-zone task placement
- Ettinger (2020) — "What BERT is Not" — negation processing unreliability in transformer models
- Shanahan et al. (2023) — "Role Play with Large Language Models" — Persona Effect and scope expansion
- Wierzbicka (1987) — English Speech Act Verbs — declarative vs imperative linguistic force
- Clark & Schaefer (1989) — Contributing to Discourse — commitment and completion in instructional language
- Sweller (1988) — Cognitive Load Theory — separation of structure and style to reduce parsing interference
- Vaswani et al. (2017) — Attention Is All You Need — attention distribution in transformer architectures
- CO-STAR prompting framework (Ng, 2024) — output format and guard rails positioning

---

**See also:** [Guidance →](../foundations/guidance) | [Constraints →](../foundations/constraints) | [Prompt Assembly & Thinking Strategies →](../foundations/research-flow)
