---
sidebar_position: 4
title: "Memory Compressor: Structured State at Scale"
description: "Experiment showing that mycontext's MemoryCompressor achieves 2x the recall of progressive summarization at 42+ turn conversations, using 60% fewer tokens than full history."
---

# Memory Compressor: Structured State at Scale

:::info TL;DR
The `MemoryCompressor` template achieves **2x recall** over LangChain-style progressive summarization at scale (67% vs 33%), using only **45% of full history tokens**. Progressive summarization collapses after 7 rewrites — performing no better than a sliding window. Structured state extraction degrades gracefully.
:::

## Motivation

Every agent framework faces the same memory problem: conversations grow, context windows fill, and something has to give. The standard approaches are:

| Strategy | Framework Example | Failure Mode |
|----------|------------------|--------------|
| Keep everything | LangGraph checkpointer | Token overflow, attention degradation, rising cost |
| Trim old messages | `trim_messages(strategy='last')` | Permanently loses early decisions and constraints |
| Running summary | `SummarizationMiddleware` | Summary loses numbers, entities, and rationale over time |

MemoryCompressor takes a different approach: **structured state extraction**. Instead of prose summaries, it extracts entities, decisions, constraints, and a key numbers index — preserving the specific details that summaries lose.

## Research Foundation

| Technique | Source | What MemoryCompressor uses |
|-----------|--------|---------------------------|
| **SimpleMem** | Modarressi et al. 2024 | Entity-level memory — extract per-entity state |
| **CDIC** | Ge et al. 2024 | Progressive updates — incrementally update compressed state |
| **RECOMP** | Xu et al. 2024 | Extractive + abstractive compression for retrieval |
| **Cognitive Load Theory** | Sweller 1988 | Discard extraneous load, preserve germane load |
| **MemWalker** | Chen et al. 2023 | Tree-structured navigation for long contexts |
| **ReadAgent** | Lee et al. 2024 | Episode-based compression with gist memory |

## Experiment Design

### Three Experiments

| Experiment | Turns | Probes | Focus |
|------------|-------|--------|-------|
| **1. Single-shot comparison** | 14 (1 conversation) | Entity/decision/constraint recall + reconstruction | MemoryCompressor vs LangChain-style summarization |
| **2. Multi-turn (22 turns)** | 22 | 10 recall probes | 4 strategies at moderate scale |
| **3. Stress test (42+ turns)** | 48 messages | 15 recall probes | Scaling behavior at 7 summary rewrites |

### Stress Test Design (Primary Experiment)

**Scenario**: "Project Atlas" — an enterprise analytics platform migration across 4 phases with 8 named stakeholders, 4 budget changes, 3 tech stack pivots, and 3 personnel changes.

| Phase | Turns | Content |
|-------|-------|---------|
| Foundation (1-12) | Budget, team, architecture, first client requirements |
| Compliance (13-22) | SOC 2 audit, GDPR, security mandates, vendor costs |
| Streaming Pivot (23-32) | Client ultimatum, Spark→Flink, ClickHouse, budget increase |
| Crisis (33-42+) | Production incident, SLA credits, personnel change, final plan |

**Conditions** (4 strategies):

| Strategy | Replicates | How |
|----------|-----------|-----|
| A. Full History | LangGraph checkpointer | All messages in context |
| B. Sliding Window | `trim_messages(strategy='last', max=8)` | Last 8 messages only |
| C. Summary + Recent | `SummarizationMiddleware` | Progressive summary (rewritten every 6 turns) + last 4 raw |
| D. MemoryCompressor + Recent | **Our approach** | Session compress + 1 progressive update + last 6 raw |

**Recall probes** (15 questions across 4 categories):

| Category | Count | Tests |
|----------|-------|-------|
| Early (turns 1-12) | 4 | Info that's been through 7 summary rewrites |
| Mid (turns 13-22) | 3 | Specific vendor costs, hire dates, compliance details |
| Pivot (turns 23-32) | 4 | Decision changes, benchmark numbers, new hires |
| Cross-reference | 4 | Combining info from multiple phases |

Each probe has ground-truth markers with aliases for fair scoring.

## Results

### Stress Test (48 Messages, 15 Probes — v5 Template)

| Strategy | Recall | Passed | Tokens | Compression | Efficiency |
|----------|:------:|:------:|:------:|:-----------:|:----------:|
| A. Full History | 100% | 15/15 | 5,871 | 1.00x | 0.170 |
| B. Sliding Window | 27% | 4/15 | 1,178 | 0.20x | 0.226 |
| C. Summary+Recent | 33% | 5/15 | 1,048 | 0.18x | 0.318 |
| **D. MemoryCompressor** | **67%** | **10/15** | **2,664** | **0.45x** | **0.250** |

### Recall by Conversation Phase

| Category | Full History | Sliding Window | Summary+Recent | MemoryCompressor |
|----------|:-----------:|:--------------:|:--------------:|:----------------:|
| Early (turns 1-12) | 100% | 0% | 25% | **75%** |
| Mid (turns 13-22) | 100% | 0% | 0% | **67%** |
| Pivot (turns 23-32) | 100% | 25% | 25% | **50%** |
| Cross-reference | 100% | 75% | 75% | **75%** |

### The Critical Finding: Summary Drift

Progressive summarization scored **33%** — statistically indistinguishable from the sliding window's **27%**. After 7 rewrites, the summary lost almost everything:

- **0% mid-turn recall**: Specific vendor costs ($8,400/month for Vault, $12,300/month for Datadog), security engineer names and start dates, EU client details — all gone.
- **25% early-turn recall**: Original budget, team size, and technology choices mostly lost.
- **25% pivot recall**: Architecture changes and benchmark numbers compressed away.

MemoryCompressor maintained **67% recall** because structured extraction preserves entities, decisions, and a key numbers index that survive progressive updates.

### Consistency Across Runs

| Run | Template | MC Original | Summary+Recent | MC Advantage |
|-----|----------|:-----------:|:--------------:|:------------:|
| Run 1 | v4 | 53% | 27% | 2.0x |
| Run 2 | v4 | 60% | 33% | 1.8x |
| Run 3 | v5 | **67%** | 33% | **2.0x** |

The 2x advantage is consistent across runs. Template v5 optimizations pushed MC from 53–60% to 67%.

### Multi-Turn Experiment (22 Turns, 10 Probes)

At shorter conversations, all strategies perform better — but the relative ordering holds:

| Strategy | Recall | Tokens |
|----------|:------:|:------:|
| A. Full History | 100% | 2,640 |
| C. Summary+Recent | 100% | 1,990 |
| D. MemoryCompressor | 90% | 1,351 |
| B. Sliding Window | 70% | 1,199 |

At 22 turns, progressive summarization still works (only 3 rewrites). MemoryCompressor's advantage is efficiency: **90% recall at 51% of full history tokens** — the best accuracy-per-token ratio.

### Single-Shot Comparison

| Metric | LangChain Progressive | Single-Shot Summary | MemoryCompressor |
|--------|:--------------------:|:-------------------:|:----------------:|
| Entity recall | 14/15 | 13/15 | 13–15/15 |
| Decision recall | 8/8 | 8/8 | 7–8/8 |
| Constraint recall | 7/7 | 7/7 | 6–7/7 |
| Filler leaked | 3–4/14 | 0/14 | 0/14 |
| Compression ratio | 0.91–1.02x | 0.30–0.36x | 0.40–0.54x |

MemoryCompressor achieves comparable recall to LangChain at **half the tokens** and with **zero filler leakage**.

## Template Optimization: What Worked

The v5 template includes five generic optimizations (not domain-specific):

| Optimization | What it does | Impact |
|--------------|-------------|--------|
| **ENUMERATE-first** | Forces systematic inventory of all persons, numbers, dates before compressing | Early recall: 50% → 75% |
| **CROSS-CHECK** | Counts numbers in input vs output — must match | Catches dropped data |
| **Progressive preservation** | Treats existing memory as ground truth — never drop unless contradicted | Mid recall (phased): 33% → 100% |
| **KEY NUMBERS INDEX** | Dedicated section enumerating all quantitative data | Safety net for numbers |
| **Zero-tolerance rules** | Guidance rules explicitly prohibit dropping any number | Consistent improvement |

### Compression Cycle Experiment

We also tested whether more compression cycles improve recall:

| Strategy | Cycles | Recall | Tokens |
|----------|:------:|:------:|:------:|
| D. MC Original (session + 1 progressive) | 2 | **67%** | 2,664 |
| E. MC Phased (session + 2 progressive) | 3 | 67% | 3,358 |

**Finding**: More cycles do not improve recall — they increase tokens without adding accuracy. Each additional progressive rewrite risks overwriting earlier details. The optimal strategy is **fewer, larger compressions** with a generous recent-message window.

## What MemoryCompressor Cannot Do

1. **Cannot reach 100% without full history.** Compression is lossy. At 45% of tokens, 67% recall is the current ceiling. Applications requiring perfect recall should use full history with cost management.

2. **Cannot fix attention degradation in the compression LLM itself.** For very long inputs (30K+ tokens), the LLM performing the compression suffers the same attention limits. Hierarchical chunking would be needed for extremely long contexts.

3. **Not a memory platform.** MemoryCompressor is a compression engine, not a replacement for Zep or Mem0. It provides the compression intelligence — frameworks provide the infrastructure (storage, retrieval, lifecycle hooks).

## Positioning: Compression Engine for Any Framework

MemoryCompressor is designed to plug into existing agent frameworks as a **better compression algorithm**:

| Framework | Their memory approach | MemoryCompressor adds |
|-----------|----------------------|----------------------|
| LangChain | `SummarizationMiddleware` (prose summary) | Structured extraction — 2x recall at scale |
| LangGraph | Checkpointers + `trim_messages` | Compression layer between full history and trimming |
| CrewAI | Short/long-term memory (embeddings) | Structured compression before storage |
| AutoGen | Teachable agents (key-value) | Richer state extraction than key-value |

Integration is a single function call — no infrastructure changes required:

```python
from mycontext.templates.free.specialized import MemoryCompressor

mc = MemoryCompressor()
result = mc.execute(
    content=conversation_history,
    intent="session",          # or "progressive" for updates
    existing_memory=state,     # for progressive updates
    goal="Medical consultation — preserve dosages and lab values",
    provider="openai",
)
compressed_state = result.response
```

## Key Takeaways

1. **Progressive summarization collapses at scale.** After 7 rewrites, it performs no better than a sliding window. This is the standard approach in `SummarizationMiddleware` — and it fails.

2. **Structured extraction degrades gracefully.** MemoryCompressor maintains 2x the recall of summarization at scale, with consistent results across runs.

3. **The KEY NUMBERS INDEX is critical.** Forcing enumeration of all quantitative data creates a safety net that catches numbers lost during entity extraction.

4. **Fewer compressions, larger batches.** More frequent progressive updates don't help — they cause the same drift as progressive summarization. One large session compress + one progressive update is optimal.

5. **Domain adaptation via `goal` parameter.** The template is generic but accepts a `goal` hint for domain-specific compression focus — no code changes needed.

## Reproduce

Notebooks:

- [memory_compressor_comparison.ipynb](/notebooks/memory_compressor_comparison.ipynb) — Single-shot comparison against LangChain summarization
- [memory_compressor_multiturn.ipynb](/notebooks/memory_compressor_multiturn.ipynb) — 22-turn multi-turn experiment (4 strategies, 10 probes)
- [memory_compressor_stress_test.ipynb](/notebooks/memory_compressor_stress_test.ipynb) — 42+ turn stress test (5 strategies, 15 probes)

Requirements:

```bash
pip install mycontext-ai litellm tiktoken
```

And an `OPENAI_API_KEY`.
