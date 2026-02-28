---
sidebar_position: 0
title: Research Overview
description: "Empirical research validating mycontext's context engineering approach — structured templates, parameterization, and cost optimization."
---

# Research

Empirical experiments validating the core thesis of context engineering: **structured prompts normalize model performance, making the cheapest model as effective as the most expensive one.**

## Studies

### [Structured Reasoning: Model Cost vs Accuracy](./reasoner-model-comparison)

Tests the `StepByStepReasoner` template across three OpenAI model tiers on math/logic problems.

**Key result:** All three models (gpt-4o-mini, gpt-4o, gpt-5.2) achieve **100% accuracy** with the template. gpt-4o-mini delivers identical results at **32x lower cost**.

| Model | Accuracy | Cost/Call |
|-------|:---:|---:|
| gpt-4o-mini | 100% | $0.0008 |
| gpt-4o | 100% | $0.012 |
| gpt-5.2 | 100% | $0.025 |

---

### [Data Analysis: Parameterization vs Full Templates](./data-analyzer-parameterization)

Tests the `DataAnalyzer` template's intent-based parameterization — whether requesting fewer sections degrades quality.

**Key result:** The executive intent (4 sections) **outscores** the full comprehensive template (11 sections) at **51% fewer tokens**.

| Approach | Quality | Tokens |
|----------|:---:|---:|
| Executive (4 sections) | 9.5/10 | 900 |
| Comprehensive (11 sections) | 8.8/10 | 1,834 |
| Raw (no template) | 8.0/10 | 1,188 |

---

### [RAG Answerer: Grounding, Citation, and Abstention](./rag-answerer-grounding)

Tests the `RagAnswerer` template against a plain LangChain-style RAG prompt across 8 questions (factual, analytical, multi-hop, abstention) with 3 runs each.

**Key result:** RagAnswerer extracts **15% more evidence**, produces **6.75 citations/response** (vs zero for plain RAG), and achieves **100% abstention accuracy** — with no latency penalty.

| Metric | Plain RAG | RagAnswerer |
|--------|:---------:|:-----------:|
| Evidence marker recall | 67.4% | **77.1%** |
| Citations/response | 0.0 | **6.75** |
| Abstention accuracy | 100% | **100%** |
| Latency | 1.42s | 1.38s |

Incorporates generation-side best practices from CRAG, Self-RAG, and Chain-of-Note research.

---

### [Memory Compressor: Structured State at Scale](./memory-compressor-scaling)

Tests the `MemoryCompressor` template against LangChain-style progressive summarization, sliding windows, and full history across 3 experiments (single-shot, 22-turn, and 42+ turn stress test).

**Key result:** At scale (42+ turns), MemoryCompressor achieves **2x the recall** of progressive summarization (67% vs 33%), using only **45% of full history tokens**. Progressive summarization collapses after 7 rewrites — performing no better than a sliding window.

| Strategy | Recall | Tokens | Compression |
|----------|:------:|:------:|:-----------:|
| Full History | 100% | 5,871 | 1.00x |
| Summary+Recent (LangChain) | 33% | 1,048 | 0.18x |
| **MemoryCompressor** | **67%** | **2,664** | **0.45x** |
| Sliding Window | 27% | 1,178 | 0.20x |

Based on SimpleMem, CDIC, RECOMP, and Cognitive Load Theory research.

---

## Cross-Study Conclusions

All four experiments point to the same principles:

1. **Structure beats capability.** A well-structured template with a cheap model outperforms an unstructured prompt with an expensive model. The template provides the "reasoning scaffold" that makes model intelligence secondary.

2. **Less is more.** Requesting exactly the right sections (parameterization) produces higher quality than requesting everything (comprehensive). Focused prompts give the model a clearer task.

3. **Cost optimization is free.** Switching from gpt-5.2 to gpt-4o-mini with the same template saves 97% on cost with zero accuracy loss. Switching from comprehensive to executive intent saves 51% on tokens while improving quality.

4. **Complexity doesn't pay.** The two-pass "hidden context" approach added only +0.3 quality points — not enough to justify the extra API call. Simple, direct templates win.

5. **Generation-side RAG optimization works.** The RagAnswerer template applies CRAG, Self-RAG, and Chain-of-Note principles as concise prompt instructions — extracting 15% more evidence from the same retrieved chunks, with zero latency overhead. Most RAG improvement focuses on retrieval; this shows the generation prompt matters too.

6. **Structured extraction beats progressive summarization at scale.** After 7 rewrites, progressive summaries lose entity names, dollar amounts, and decision rationale — performing no better than discarding old messages. Structured state extraction (entities, decisions, constraints, key numbers) degrades gracefully, maintaining 2x recall advantage.

## Reproduce

All experiments include downloadable Jupyter notebooks:

- [reasoner_model_comparison.ipynb](/notebooks/reasoner_model_comparison.ipynb)
- [data_analyzer_comparison_raw_vs_template.ipynb](/notebooks/data_analyzer_comparison_raw_vs_template.ipynb)
- [langchain_rag_comparison.ipynb](/notebooks/langchain_rag_comparison.ipynb)
- [memory_compressor_stress_test.ipynb](/notebooks/memory_compressor_stress_test.ipynb)

Requirements: `pip install mycontext-ai litellm` and an `OPENAI_API_KEY`. RAG experiment additionally requires `langchain langchain-text-splitters langchain-community langchain-openai bs4`. Memory compressor experiment additionally requires `tiktoken`.
