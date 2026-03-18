---
sidebar_position: 0
title: Research Overview
description: "Empirical research validating mycontext's context engineering approach — structured templates, parameterization, and cost optimization."
---

# Research

Empirical experiments validating the core thesis of context engineering: **structured prompts normalize model performance, making the cheapest model as effective as the most expensive one.**

## Studies

### [Prompt Engineering Foundation: Structure, Linguistics, and Provider Rendering](./prompt-engineering-foundation)

Research behind the mycontext prompt assembly engine — the 9-section ordering model, five linguistic upgrades that improve instruction compliance, and provider-specific rendering optimizations for OpenAI, Anthropic, and Gemini.

**Key findings:**

- The 9-section ordering (primacy zone → instructions → middle → late → recency zone) is grounded in three independent research findings: primacy-recency bias (Liu et al. 2023), instruction-first ordering (OpenAI Cookbook), and recency-task correlation (+9.7 BLEU, Li et al. 2023)
- Imperative goal framing ("Your mission: X — accomplish this fully") drives completion; declarative descriptions correlate with partial responses
- Positive constraint reframing ("Omit X" vs "Must NOT include X") reduces token-priming failure — directly validated by Anthropic's own prompt engineering team
- Persona scope bounding (`persona_scope`) prevents the Persona Effect (Shanahan et al. 2023) — roles expanding into unintended domains
- Output contract placement in section ⑦ (recency zone) maximises format compliance
- Provider delimiter differences matter for constraint compliance and long-context recall — not overall accuracy. A 2026 benchmark found ≤0.3% accuracy deltas between XML and Markdown on frontier models

| Upgrade | Mechanism | Measured signal |
|---------|-----------|----------------|
| Imperative goal | Linguistic commitment → completion drive | Goal completion rate (live eval) |
| Positive constraint reframe | Eliminates negation processing failure | Constraint violation rate |
| Persona scope | Explicit domain boundary on role | Role drift prevention |
| Output contract | Section ⑦ recency placement | Format compliance rate |
| Provider hint | XML/Markdown + 4 rendering overrides | Per-provider compliance |

---

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

### [Code Review: Cognitive Restructuring](./code-reviewer-optimization)

Research-backed redesign of the `CodeReviewer` template — replacing a flat "list issues by severity" prompt with a four-phase cognitive flow (ORIENT → ANALYZE → ASSESS → RECOMMEND) based on industry findings.

**Key insight:** 85% of code review comments are low-value style bikeshedding, and the #1 unmet need is code/change understanding. The restructured template adds an orientation phase before critique, uses risk-weighted severity (impact × likelihood × blast radius) instead of flat labels, and excludes style/formatting entirely — redirecting attention to the 7 dimensions linters cannot catch.

| Problem | Research Finding |
|---------|-----------------|
| 85% bikeshedding | Only 15% of review comments find real defects (CodePulse 2025) |
| No understanding phase | Code/change understanding is #1 unmet need (Bacchelli & Bird, Microsoft) |
| Flat severity labels | Senior engineers prioritize by risk, not severity (Google eng-practices) |

Based on CRDM (2026), Bacchelli & Bird (2013), Google eng-practices, and Fagan (1976).

---

### [DataAnalyzer: Research Foundation](./data-analyzer-design)

The academic and industry research behind DataAnalyzer's 11-section design — mapping each section to CRISP-DM, KDD, Tukey's EDA, anomaly detection literature, evidence-based reporting, and visualization science.

**Key insight:** DataAnalyzer's 11 sections are not arbitrary — each maps to a specific finding from established analytical frameworks. The causation-correlation note in Section 5 is binding (enforced by Pearson/Pearl). The confidence ratings in Section 7 implement Gneiting & Raftery's calibrated probability assessment. The hypothesis structure in Section 8 enforces Popper's falsifiability criterion.

| Section | Research Source |
|---------|----------------|
| Data Overview + Descriptive Statistics | CRISP-DM Data Understanding phase |
| Pattern Detection | Tukey (1977) — Revelation & Re-expression principles |
| Anomaly Detection | Chandola, Banerjee & Kumar (2009) — ACM Computing Surveys |
| Key Insights | Sackett et al. (1996) — Evidence-based practice; Gneiting & Raftery (2007) — calibrated confidence |
| Hypotheses | Peirce (1878) abductive reasoning + Popper (1959) falsifiability |
| Data Limitations | Redman (1996); Wilkinson et al. FAIR principles (2016) |
| Visualization Suggestions | Cleveland & McGill (1984) — graphical perception hierarchy |

---

## Cross-Study Conclusions

All six studies point to the same principles:

1. **Structure beats capability.** A well-structured template with a cheap model outperforms an unstructured prompt with an expensive model. The template provides the "reasoning scaffold" that makes model intelligence secondary.

2. **Less is more.** Requesting exactly the right sections (parameterization) produces higher quality than requesting everything (comprehensive). Focused prompts give the model a clearer task.

3. **Cost optimization is free.** Switching from gpt-5.2 to gpt-4o-mini with the same template saves 97% on cost with zero accuracy loss. Switching from comprehensive to executive intent saves 51% on tokens while improving quality.

4. **Complexity doesn't pay.** The two-pass "hidden context" approach added only +0.3 quality points — not enough to justify the extra API call. Simple, direct templates win.

5. **Generation-side RAG optimization works.** The RagAnswerer template applies CRAG, Self-RAG, and Chain-of-Note principles as concise prompt instructions — extracting 15% more evidence from the same retrieved chunks, with zero latency overhead. Most RAG improvement focuses on retrieval; this shows the generation prompt matters too.

6. **Structured extraction beats progressive summarization at scale.** After 7 rewrites, progressive summaries lose entity names, dollar amounts, and decision rationale — performing no better than discarding old messages. Structured state extraction (entities, decisions, constraints, key numbers) degrades gracefully, maintaining 2x recall advantage.

7. **Cognitive structure matters as much as content structure.** The CodeReviewer study shows that fixing *how* a template thinks (orient before analyze, assess risk not just severity) is as important as fixing *what* it outputs. A flat severity list encourages bikeshedding; a cognitive flow (understand → analyze → assess risk → recommend) redirects attention to high-value findings.

## Reproduce

All experiments include downloadable Jupyter notebooks:

- [reasoner_model_comparison.ipynb](/notebooks/reasoner_model_comparison.ipynb)
- [data_analyzer_comparison_raw_vs_template.ipynb](/notebooks/data_analyzer_comparison_raw_vs_template.ipynb)
- [langchain_rag_comparison.ipynb](/notebooks/langchain_rag_comparison.ipynb)
- [memory_compressor_stress_test.ipynb](/notebooks/memory_compressor_stress_test.ipynb)

Requirements: `pip install mycontext-ai litellm` and an `OPENAI_API_KEY`. RAG experiment additionally requires `langchain langchain-text-splitters langchain-community langchain-openai bs4`. Memory compressor experiment additionally requires `tiktoken`.
