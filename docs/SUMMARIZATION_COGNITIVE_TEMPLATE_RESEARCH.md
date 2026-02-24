# Summarization Cognitive Template: Research Hypothesis & Foundation

**mycontext-ai: Research-Backed Template for LLM Summarization**

**Document Version:** 1.0  
**Date:** February 23, 2025  
**Purpose:** Research foundation and hypothesis for a cognitive template that guides LLMs to produce high-quality summaries of long-context text

**Scope:** The template will be **fed into an LLM** as a directive—not a compression algorithm. The LLM performs summarization; the template provides the cognitive structure to do it well.

---

## Executive Summary

This document synthesizes research across cognitive science, psychology, AI, and linguistics to propose a **Summarization Cognitive Template** that addresses industry-wide failures in long-context summarization. The template encodes research-backed principles (Kintsch–van Dijk construction-integration, macrostructures, chunking, schema theory) into a structured directive that mitigates LLM-specific failures (hallucination, omission, positional bias) while preserving key information.

**Key Finding:** Existing products (ARC, SARC, UltraGist, RAPTOR) focus on *evaluation* or *compression* infrastructure. There is a gap for **cognitive methodology templates** that guide *how* summarization should be performed—regardless of underlying compression or loop implementation. Our 85 cognitive patterns provide precedent; this template fills the summarization gap.

---

## Table of Contents

1. [Industry Issues: Summarization & Memory](#1-industry-issues-summarization--memory)
2. [Cognitive Science Foundations](#2-cognitive-science-foundations)
3. [Linguistic & Psycholinguistic Theory](#3-linguistic--psycholinguistic-theory)
4. [AI & Evaluation Research](#4-ai--evaluation-research)
5. [Proposed Template Design (Research Hypothesis)](#5-proposed-template-design-research-hypothesis)
6. [Alignment with 85 Cognitive Patterns](#6-alignment-with-85-cognitive-patterns)
7. [References](#7-references)

---

## 1. Industry Issues: Summarization & Memory

### 1.1 Long-Context Summarization Failures

| Issue | Description | Source |
|-------|-------------|--------|
| **Omission of critical information** | LLMs often omit salient arguments, especially when they are sparsely distributed across long documents | ARC framework (2025), ArgCMV benchmark |
| **Hallucination** | Summaries include information not grounded in source—factual and non-factual | TofuEval, ACUEval, Mixed-Context Hallucination research |
| **Positional bias** | Context window position affects what gets retained (early/middle/late bias) | ARC findings on instruction-following LLMs |
| **Loss of nuance** | Over-compression flattens important distinctions, caveats, and qualifiers | Extractive vs. abstractive research |
| **Argument role loss** | In high-stakes domains (law, science), argument structure (claim, evidence, warrant) is dropped | ARC, Argument Representation Coverage |
| **Memory/retention tradeoff** | Summaries intended for downstream use (RAG, agents) lose fidelity under compression | SARA, RAPTOR, Dodo compression studies |

### 1.2 Memory-Specific Challenges

- **Chunk capacity**: Human working memory (Miller’s 7±2, Cowan’s ~4 chunks) motivates hierarchical summarization—summaries must themselves be chunkable.
- **Retrieval structure**: Summaries often serve as retrieval keys; missing structure impairs downstream recall.
- **Schema alignment**: Users expect summaries to align with domain schemas (e.g., legal: holding, reasoning, disposition; scientific: hypothesis, methods, results, conclusion).

---

## 2. Cognitive Science Foundations

### 2.1 Kintsch Construction–Integration Model (1988, 2004)

**Two-phase comprehension:**

1. **Construction (bottom-up)**  
   - Word meanings → propositions → local coherence  
   - Inferences and elaborations form a network  

2. **Integration (top-down)**  
   - Context and prior knowledge integrate elements into coherent semantic structure  
   - Produces **situation model** (macrostructure) and **text base** (microstructure)

**Implication for template:** Encode a two-phase summarization process: (1) construct local propositions and relationships, (2) integrate into global macrostructure before producing final summary.

**Citation:** Kintsch, W. (1988). The role of knowledge in discourse comprehension: A construction-integration model. *Psychological Review*, 95(2), 163–182.

### 2.2 Van Dijk Macrostructures

**Macro-operators** reduce text to gist:

- **Deletion**: Remove irrelevant propositions  
- **Generalization**: Replace specifics with superordinates  
- **Construction**: Infer high-level propositions from lower-level ones  

**Macrostructural categories** (narrative): Introduction, Complication, Resolution.

**Implication for template:** Include explicit macro-operators (delete, generalize, construct) and structural categories appropriate to domain (e.g., scientific, legal, narrative).

**Citation:** Van Dijk, T. A. (1980). *Macrostructures: An interdisciplinary study of global structures in discourse, interaction, and cognition*. Lawrence Erlbaum.

### 2.3 Chunking & Data Compression (Cognitive)

- Chunking increases effective capacity by grouping related items into meaningful units.  
- Chunk formation relates to **data compressibility**—redundancy is reduced via structure.  
- Untrained participants form chunks from stimulus associations; expertise improves chunk size and quality.

**Implication for template:** Encourage chunk-based summarization—identify natural boundaries (paragraphs, sections, arguments) and summarize at multiple granularities (local chunk → section → document).

**Citation:** Gobet, F., et al. (2016). Chunk formation in immediate memory and how it relates to data compression. *Cognition*, 155, 96–107.

### 2.4 Schema Theory (Bartlett, Piaget, Schank & Abelson)

- Schemas organize categories of information and their relationships.  
- They guide attention and absorption—people notice schema-relevant content.  
- Schemas have slots (e.g., legal case: parties, holding, reasoning, disposition).

**Implication for template:** Allow user-specified or domain-typical schemas. Template should prompt: “Identify schema slots present in the source; ensure summary preserves each populated slot.”

**Citation:** Bartlett, F. C. (1932). *Remembering*. Cambridge University Press.  
Schank, R. C., & Abelson, R. P. (1977). *Scripts, plans, goals, and understanding*. Lawrence Erlbaum.

---

## 3. Linguistic & Psycholinguistic Theory

### 3.1 Microstructure vs. Macrostructure

- **Microstructure**: Local coherence (sentence-to-sentence).  
- **Macrostructure**: Global theme, main ideas, high-level organization.  
- Summarization is primarily a **macrostructure** task, but must respect microstructure where critical (e.g., causal links, qualifiers).

**Implication for template:** Separate instructions for (a) preserving critical local links and (b) building coherent macro-level gist.

### 3.2 Argument Structure (Toulmin, Argument Mining)

- **Claim, Data, Warrant, Backing, Rebuttal**—argument roles are central in law, science, policy.  
- ARC shows LLMs often drop argument roles when they are distributed across long documents.

**Implication for template:** Add an argument-structure pass: identify roles, ensure each is represented in the summary, flag if omitted.

---

## 4. AI & Evaluation Research

### 4.1 Extractive vs. Abstractive

- **Extractive**: Higher faithfulness, lower fluency; preserves verbatim text.  
- **Abstractive**: More natural, mimics human summarization; higher hallucination risk.  
- **Hybrid (extract-then-abstract)** can reduce error accumulation.

**Implication for template:** Support a hybrid workflow: (1) extract key spans/sentences, (2) abstract into coherent narrative, (3) verify faithfulness of abstracted content against extracts.

### 4.2 ARC (Argument Representation Coverage)

- Bottom-up evaluation: atomic facts → argument roles → ARCscore.  
- Separates **omissions** from **factual errors**.  
- Finds: sparsely distributed arguments and positional bias cause omissions.

**Implication for template:** Add explicit passes for (a) argument role identification and (b) coverage check (“For each identified argument role, is it represented in the summary?”).

### 4.3 Hallucination Mitigation

- LLMs introduce intrinsic knowledge when evaluating summaries, biasing hallucination detection.  
- Faithfulness metrics (e.g., factual consistency) are more reliable when grounded in source spans.  
- Explicit instruction: “Include only information present in the source; if uncertain, omit.”

**Implication for template:** Hard constraints and self-check: (1) No unsupported claims, (2) Trace each summary claim to source span, (3) Flag low-confidence items.

### 4.4 Existing Approaches (What We Are NOT Building)

| Approach | Focus | Our Stance |
|----------|-------|------------|
| **ARC** | Evaluation framework | Use principles (argument coverage, omission vs. error) to *design* the template |
| **ARC-Encoder, UltraGist** | Token compression | Infrastructure; template is orthogonal |
| **SARA, RAPTOR** | Retrieval + compression | Same |
| **SynthesisBuilder** | Multi-source synthesis | Complementary; summarization is single-source condensation |
| **SimplificationEngine** | Complex → simple | Different goal (accessibility vs. key-info preservation) |

---

## 5. Proposed Template Design (Research Hypothesis)

### 5.1 Core Hypothesis

**A cognitive template that encodes Kintsch–van Dijk macro-operators, argument-structure preservation, chunk-based hierarchy, schema alignment, and faithfulness checks will produce consistently better summaries from instruction-following LLMs than unstructured or minimal prompts.**

### 5.2 Proposed Template Sections

Based on the research above, the template should guide the LLM through the following phases:

| Section | Research Basis | Purpose |
|---------|----------------|---------|
| **1. Source & Domain Analysis** | Schema theory | Identify domain type (legal, scientific, narrative, etc.) and expected schema slots |
| **2. Proposition/Chunk Extraction** | Kintsch construction | Build local proposition network; identify chunk boundaries |
| **3. Argument Structure Map** | Toulmin, ARC | Map claims, evidence, warrants, rebuttals; flag sparse distribution |
| **4. Macro-Operator Application** | Van Dijk | Apply delete, generalize, construct to produce gist |
| **5. Hierarchical Summary** | Chunking | Produce summaries at multiple levels (chunk, section, document) |
| **6. Coverage Check** | ARC | For each argument role and key proposition: verify representation in summary |
| **7. Faithfulness Verification** | Hallucination research | Trace claims to source; flag unsupported content; omit uncertain items |
| **8. Output Structuring** | User/domain schema | Format summary to match expected schema (e.g., executive summary, key points, evidence matrix) |

### 5.3 Integration with Loops & Compression

The template is **agnostic** to implementation:

- **Single pass**: Template instructs one comprehensive pass over context.  
- **Multi-pass / MapReduce**: Template sections can map to phases (e.g., Phase 1 = sections 1–3, Phase 2 = 4–5, Phase 3 = 6–8).  
- **Hierarchical compression**: Each chunk summarized separately, then rolled up—template guides each level.  
- **RAG integration**: Summary as index—template ensures retrieval-relevant structure is preserved.

### 5.4 Key Input Parameters (Hypothesis)

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` or `text` | str | Long-context input to summarize |
| `goal` | str | What the summary is for (e.g., “executive decision”, “legal holding”, “research synthesis”) |
| `target_length` | str or int | “Brief”, “Moderate”, “Comprehensive” or token count |
| `domain` | str | Optional: legal, scientific, narrative, technical, general |
| `schema` | list or str | Optional: expected slots (e.g., ["claim", "evidence", "conclusion"]) |
| `preserve` | list | Optional: what must not be dropped (e.g., ["numbers", "citations", "caveats"]) |

---

## 6. Alignment with 85 Cognitive Patterns

### 6.1 Related Existing Patterns

| Pattern | Relationship |
|---------|--------------|
| **SynthesisBuilder** | Multi-source synthesis → different task; SummarizationTemplate is single-source condensation |
| **SimplificationEngine** | Simplification for accessibility → different goal; SummarizationTemplate preserves key info at reduced length |
| **ContentOutliner** | Hierarchical content structure → complementary; Summarization can feed into ContentOutliner |
| **DataAnalyzer** | Pattern extraction from data → analogous “extract key info” but for numerical/structured data |
| **QuestionAnalyzer** | Decompose before answering → analogous “analyze before summarizing” |
| **StepByStepReasoner** | Transparent chain-of-thought → template can use stepwise structure |

### 6.2 Placement in Pattern Taxonomy

- **Category**: Specialized (free) or Advanced Communication (enterprise)  
- **Module**: `mycontext.templates.free.specialized` or `mycontext.templates.enterprise.communication`  
- **Unique value**: Only pattern explicitly focused on *condensation with key-information preservation* backed by construction-integration and macrostructural theory.

---

## 7. References

### Cognitive Science & Psychology

- Bartlett, F. C. (1932). *Remembering*. Cambridge University Press.
- Cowan, N. (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences*, 24(1), 87–114.
- Gobet, F., et al. (2016). Chunk formation in immediate memory and how it relates to data compression. *Cognition*, 155, 96–107.
- Kintsch, W. (1988). The role of knowledge in discourse comprehension: A construction-integration model. *Psychological Review*, 95(2), 163–182.
- Kintsch, W. (2004). The construction-integration model of text comprehension and its implications for instruction. In R. B. Ruddell & N. Unrau (Eds.), *Theoretical models and processes of reading* (5th ed., pp. 1270–1328). International Reading Association.
- Schank, R. C., & Abelson, R. P. (1977). *Scripts, plans, goals, and understanding*. Lawrence Erlbaum.
- Van Dijk, T. A. (1980). *Macrostructures: An interdisciplinary study of global structures in discourse, interaction, and cognition*. Lawrence Erlbaum.
- Van Dijk, T. A., & Kintsch, W. (1983). *Strategies of discourse comprehension*. Academic Press.

### Linguistics & Argumentation

- Toulmin, S. E. (1958). *The uses of argument*. Cambridge University Press.

### AI & Summarization Evaluation

- ARC: Argument Representation and Coverage (2025). *arXiv:2505.23654*.
- ACUEval: Fine-grained Hallucination Evaluation (2024). *ACL Findings*.
- TofuEval: Hallucinations on Topic-Focused Dialogue Summarization. *arXiv:2402.13249*.
- What Have We Achieved on Text Summarization? (2020). *arXiv:2010.04529*.
- Extractive vs. Abstractive: Experimental Review. *MDPI Applied Sciences* (2023).

### Compression & Long-Context (Infrastructure Context)

- UltraGist (2024). *arXiv:2405.16635*.
- RAPTOR: Recursive Abstractive Processing (2024). *arXiv*.
- Dodo: Dynamic Contextual Compression (2024). *ACL*.

---

## Next Steps

1. **Validate hypothesis**: A/B test template vs. minimal prompt on long legal/scientific documents; measure ARC-style coverage, hallucination rate, user preference.
2. **Implement template**: Create `SummarizationCognitiveTemplate` (or `KeyInfoPreserver`) as a Pattern with `directive_template`, `build_context()`, `execute()`, `generic_prompt()`.
3. **Integrate with loops**: Design chunk-level and document-level flows (single pass vs. hierarchical) that invoke the template at each stage.
4. **Add to COGNITIVE_PATTERNS_RESEARCH_FOUNDATIONS.md**: Register this template and its citations in the main research foundations document.
