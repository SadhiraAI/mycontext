---
sidebar_position: 6
title: "Query Planner: Pre-Retrieval Cognitive Analysis"
description: "Design rationale for the QueryPlanner template — a pre-retrieval cognitive step that classifies, decomposes, rewrites, and plans queries before they hit any retrieval system. Backed by research showing +36.7% MRR from decomposition and +27% accuracy from step-back prompting."
---

# Query Planner: Pre-Retrieval Cognitive Analysis

:::info TL;DR
The `QueryPlanner` template performs cognitive analysis on a user query **before** it reaches any retrieval system. It classifies query type, decomposes multi-hop questions into sub-queries, generates step-back abstractions and hypothetical answer documents (HyDE), and produces retrieval strategy hints. It complements the existing `RagAnswerer` (post-retrieval) to bookend any RAG pipeline — without replacing the retrieval pipeline itself.
:::

## Motivation

Most RAG implementations have a gap. They take the user's raw query and throw it directly at a vector store:

```
User: "How does RAPTOR compare to Adaptive RAG for multi-hop reasoning?"
  → embed query → vector search → top-k chunks → generate answer
```

This fails in predictable ways:

| Failure Mode | Why It Happens | How Often |
|-------------|----------------|-----------|
| **Query-document mismatch** | User asks a question (interrogative); documents contain answers (declarative). Embedding similarity between these forms is weak. | Common — the fundamental problem HyDE solves |
| **Multi-hop fragmentation** | A comparison question needs facts about entity A AND entity B, but vector search returns chunks about only one | Very common for analytical queries |
| **Over-retrieval** | Simple factual queries retrieve k=10 chunks when 1 would suffice, diluting signal with noise | Constant — most systems use fixed k |
| **Under-retrieval** | Complex queries need more context than the default k provides | Common for synthesis and comparison |
| **Temporal blindness** | "What changed in Q3?" retrieves all-time content because the query has no date filter | Common in business/ops contexts |

These are not retrieval engine problems — they're **query preparation problems**. The query reaches the retriever in a form that doesn't match how information is stored. Research shows that fixing the query before retrieval produces larger gains than improving the retriever itself.

## What the Research Says

### Query Decomposition

Breaking complex queries into focused sub-queries before retrieval:

- **+36.7% MRR@10** and **+11.6% F1** on MultiHop-RAG and HotpotQA benchmarks when pairing LLM-driven decomposition with cross-encoder reranking (2025 study)
- **UniRAG** (EMNLP 2025): Entity-grounded decomposition consistently improves across HotpotQA, 2WikiMultihopQA, MedMCQA, MedQA, FEVER, and SciFact
- **CoRAG** (2025): Chain-of-retrieval with step-by-step query reformulation yields +10 points on multi-hop QA
- **GenDec** (2024): Generative decomposition into independent, complete sub-questions with extracted evidence enhances LLM reasoning on MuSiQue and PokeMQA

The principle: a complex question split into 3 focused sub-queries retrieves better chunks than one complex query.

### Step-Back Prompting

Abstracting specific queries to their underlying concepts before retrieval:

- **+27% accuracy on TimeQA**, +7-11% on MMLU Physics and Chemistry, +7% on MuSiQue (Google DeepMind, ICLR 2024)
- Up to **+36% improvement** over chain-of-thought prompting on certain tasks
- For RAG specifically: boosts vector retrieval accuracy by enabling retrieval of more relevant conceptual context

The principle: "What are common causes of connection timeouts?" retrieves better than "Why does my service crash at 3am on Tuesdays?"

### Hypothetical Document Embeddings (HyDE)

Generating a hypothetical answer document and embedding that instead of the raw query:

- **Matches fine-tuned retrievers** in zero-shot dense retrieval across web search, QA, and fact verification (CMU 2023)
- Works across languages (Swahili, Korean, Japanese — not just English)
- +4.2% improvement when combined with sparse retrieval (BM25/Rocchio), with larger gains in low-resource domains
- Particularly effective in **medical retrieval and developer support** domains

The principle: a paragraph that looks like the answer you want is a better search query than the question itself.

### Query Classification

Routing queries to appropriate retrieval strategies based on type:

- **Dynamic RAG systems** (2025) classify queries into factual, procedural, conceptual, troubleshooting, comparative, and temporal types — each routing to different retrieval depth and strategy
- **Plan\*RAG** (2024): Test-time reasoning plans as directed acyclic graphs for atomic, precise retrievals — multi-hop queries decomposed into retrieval DAGs
- **RASTeR** (2025): Temporal query classification maintains 75% accuracy even with 40 irrelevant distractors by separating context evaluation from answer generation

The principle: a factual query and a comparison query need fundamentally different retrieval strategies.

## Design: Four-Phase Cognitive Flow

The QueryPlanner follows a sequential cognitive process:

### Phase 1: CLASSIFY

Determine what kind of query this is and what it needs:

| Type | Description | Example | Retrieval Implication |
|------|-------------|---------|----------------------|
| **factual** | Single fact lookup | "What is RAPTOR?" | Low k, single retrieval pass |
| **analytical** | Requires reasoning over evidence | "How does X affect Y?" | Medium k, may need diverse chunks |
| **multi-hop** | Chains across multiple pieces of information | "What did A do at B before C?" | Decompose into sub-queries, retrieve separately |
| **comparison** | Parallel retrieval of multiple entities | "Compare X and Y" | Retrieve for each entity independently |
| **temporal** | Time-sensitive, needs date filtering | "What changed in Q3 2025?" | Add date filters/constraints |
| **procedural** | Step-by-step instructions | "How do I set up X?" | Retrieve from how-to/tutorial sources |

This classification drives decisions in the following phases.

### Phase 2: DECOMPOSE

For multi-hop and comparison queries, break into independent sub-queries. For simple factual queries, pass through unchanged.

- Multi-hop: "How did RAPTOR's tree indexing improve over Adaptive RAG for multi-hop reasoning?" becomes:
  1. "What is RAPTOR's tree indexing approach?"
  2. "How does Adaptive RAG handle multi-hop reasoning?"
  3. "What are the performance differences between RAPTOR and Adaptive RAG on multi-hop benchmarks?"

- Comparison: "Compare Redis and Memcached for session storage" becomes:
  1. "What are Redis's characteristics for session storage?"
  2. "What are Memcached's characteristics for session storage?"

- Factual: "What is RAPTOR?" passes through unchanged.

### Phase 3: REWRITE

For each sub-query, generate alternative query forms that improve retrieval:

- **Step-back version** — abstract to the underlying concept. "Why does my Flask app crash under load?" becomes "What are common causes of Python web application performance degradation?"
- **Expanded version** — add synonyms and related terms for better recall. "RAPTOR RAG" becomes "RAPTOR recursive abstractive processing tree-organized retrieval hierarchical indexing"
- **HyDE document** — generate a short hypothetical answer paragraph. This bridges the query-document semantic gap for embedding-based retrieval.

### Phase 4: PLAN

Produce advisory retrieval hints (not executable code):

- **Suggested k** per sub-query (factual: k=3, analytical: k=5, multi-hop: k=5 per sub-query)
- **Source type hints** (documentation, codebase, database, web)
- **Filter suggestions** (date range, entity type, category)
- **Strategy notes** (e.g., "retrieve for each entity separately, then combine chunks before generation")

These hints are advisory — the retrieval pipeline can use or ignore them.

## What This Template Does NOT Do

Honest boundaries:

1. **Does not execute retrieval.** It produces text output (sub-queries, HyDE documents, hints) that a retrieval pipeline consumes. It doesn't call vector stores, APIs, or databases.

2. **Does not implement RAPTOR, CRAG, or Adaptive RAG.** Those are pipeline architectures requiring code execution (clustering, embedding, API routing). This template is the cognitive analysis step that sits upstream of any pipeline.

3. **Does not replace your retrieval stack.** It works with LangChain, LlamaIndex, custom pipelines, or no framework at all. The output is plain text that any system can parse.

4. **Does not guarantee retrieval improvement.** If the documents aren't in your index, no query rewriting will find them. The template improves query quality — retrieval quality depends on the index.

## Complementary Pair: QueryPlanner + RagAnswerer

The two templates bookend any RAG pipeline:

| Step | Template | What It Does |
|------|----------|-------------|
| Pre-retrieval | **QueryPlanner** | Classify, decompose, rewrite, plan |
| Retrieval | *(your pipeline)* | Vector search, keyword search, hybrid, web |
| Post-retrieval | **RagAnswerer** | Extract, cite, abstain, ground |

```
User Query → [QueryPlanner] → sub-queries + HyDE + hints
    → [Any Retriever] → chunks
    → [RagAnswerer] → grounded answer with citations
```

This separation keeps each template focused on one cognitive task, following the same principle that made the `RagAnswerer` template effective: concise inline rules beat verbose multi-step scaffolding.

## Research References

1. **Query Decomposition for RAG (2025).** LLM-driven decomposition with cross-encoder reranking: +36.7% MRR@10, +11.6% F1 on MultiHop-RAG and HotpotQA.

2. **UniRAG (EMNLP 2025).** Entity-grounded query decomposition with break-down reasoning verification and iterative query rewriting. Consistent improvements across HotpotQA, 2WikiMultihopQA, MedMCQA, MedQA, FEVER, SciFact.

3. **Step-Back Prompting (ICLR 2024, Google DeepMind).** Abstracting specific queries to high-level concepts: +27% TimeQA, +7-11% MMLU, +7% MuSiQue.

4. **HyDE — Hypothetical Document Embeddings (CMU 2023).** Zero-shot dense retrieval matching fine-tuned retrievers. Generates hypothetical answer documents for embedding, bridging the query-document semantic gap.

5. **CoRAG — Chain-of-Retrieval (2025).** Step-by-step retrieval and reasoning with dynamic query reformulation: +10 points on multi-hop QA.

6. **Plan\*RAG (2024).** Test-time reasoning plans as directed acyclic graphs for atomic, precise retrieval operations.

7. **FB-RAG — Forward-Backward RAG (2025).** Uses lighter LLM to "peek" into future generations for context selection: 48% latency reduction while matching baseline.

8. **RASTeR (2025).** Temporal reasoning with structured knowledge graphs: maintains 75% accuracy even with 40 irrelevant distractors.
