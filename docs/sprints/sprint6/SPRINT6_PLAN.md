# Sprint 6 — Cognitive RAG Revisited

## Why Revisit

Sprints 1 & 2 tested Cognitive RAG (template + retrieved knowledge) and it **underperformed badly**:

| Sprint | Raw | RAG Only | Template Only | Cognitive RAG |
|---|---|---|---|---|
| Sprint 1 (1 Q) | 73.8% | **87.3%** | 74.2% | 73.9% |
| Sprint 2 (5 Qs) | **92.0%** | 93.2% | 86.1% | 81.6% |

Cognitive RAG scored **lowest** in Sprint 2 — worse than raw. The idea seemed dead.

## What Went Wrong (Root Causes)

We now understand the 4 root causes:

1. **Token competition**: Full templates (~3000-6000 chars) + retrieved docs (~2000 chars) = ~8000 chars of input instructions. The LLM was fighting to follow template structure AND incorporate docs, doing neither well.

2. **Wrong template selection**: Sprint 1-2 used the NLP-biased pattern catalog. Questions about business churn got matched to NLP templates.

3. **Unfair evaluation**: The evaluator penalized template outputs for not matching raw output style (fixed in Sprint 3B).

4. **Rigid template structure**: Full templates have prescriptive section requirements that clash with how RAG content should flow through a response.

## What's Changed Since Then (Sprints 3-5)

| Fix | Sprint | Impact |
|---|---|---|
| Enriched catalog + fair selection | S3 | Correct templates selected 9/10 times |
| Fair evaluation (all vs raw context) | S3B | Templates went from 86% → 96% |
| Complexity router (`assess_complexity`) | S3 | Right-sizes approach per question |
| **Generic prompts** (~800-1200 chars) | S5 | Lightweight scaffolding, no token competition |
| Prompt compilation pipeline | S4 | Compact multi-template prompts |
| Full enterprise generic prompts (85/85) | S5C | Every template has a concise prompt |

**The key insight: Generic prompts solve token competition.**

- Sprint 2 Cognitive RAG input: ~8000 chars (full template + docs) → 81.6%
- Sprint 6 target input: ~3000 chars (generic prompt + docs) → should be competitive

## Sprint 6 Hypothesis

**With generic prompts replacing full templates, Cognitive RAG will outperform both Raw and RAG-only by providing structured reasoning over retrieved knowledge without token competition.**

Specifically:
- Cognitive RAG (generic + docs) ≥ 95% (matching Sprint 5C GenEnterprise)
- Cognitive RAG > RAG-only by 2-5pp (reasoning structure adds value)
- Cognitive RAG > Raw by 3-5pp (both structure and data advantages)
- Total prompt size stays < 4000 chars (well within LLM sweet spot)

## Test Design — 6 Conditions × 10 Questions

| Condition | Template Mode | Knowledge | Prompt Size | LLM Calls |
|---|---|---|---|---|
| **Raw** | None | None | ~50 chars | 1 |
| **RAG Only** | None | Simulated docs | ~2000 chars | 1 |
| **GenFree** | Free generic prompt | None | ~1000 chars | 2 |
| **GenEnterprise** | Enterprise generic prompt | None | ~1000 chars | 2 |
| **CogRAG-Free** | Free generic prompt | Simulated docs | ~3000 chars | 2 |
| **CogRAG-Enterprise** | Enterprise generic prompt | Simulated docs | ~3000 chars | 2 |

The same 10 questions from all sprints, with realistic simulated retrieved documents for each.

## Simulated Retrieved Documents

For each question, we create 3-5 realistic "retrieved chunks" (~500-800 chars total) that contain:
- Specific data points (numbers, dates, names)
- Domain-specific context
- Evidence markers (unique facts the LLM wouldn't know)

These simulate what a real vector store retrieval would return. Evidence markers let us measure whether the LLM actually used the retrieved information.

## Implementation

The Cognitive RAG approach combines generic prompt + retrieved docs:

```python
# Get the generic prompt for the recommended template
generic_prompt = get_generic_prompt_for(template_name, question)

# Inject retrieved docs into the prompt
rag_prompt = f"{generic_prompt}\n\nRELEVANT RETRIEVED INFORMATION:\n{retrieved_docs}\n\nUse the above information as evidence in your analysis."

# Execute
ctx = Context(directive=Directive(content=rag_prompt))
result = ctx.execute(provider=PROVIDER)
```

No new code needed — just prompt assembly using existing infrastructure.

## Success Criteria

1. **CogRAG scores ≥ 95%** (matches non-RAG generic prompt performance)
2. **CogRAG > RAG-only** (reasoning structure adds measurable value)
3. **Evidence recall ≥ 60%** (uses retrieved docs, not just generic knowledge)
4. **Prompt size < 4000 chars** (no token competition)
5. **Zero raw_fallbacks for CogRAG-Free** (routing fix validated)

## Key Metrics to Track

- Quality scores (5 dimensions)
- Evidence recall (how many specific retrieved facts appear in output)
- Prompt size (chars)
- Response length (chars)
- Time per condition
- Cross-sprint comparison with Sprint 2 Cognitive RAG

---

**Estimated cost**: ~$2.50-3.50 (6 conditions × 10 questions × execution + evaluation)
**Estimated time**: ~35-50 min
