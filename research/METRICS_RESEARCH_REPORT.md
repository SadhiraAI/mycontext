# Metrics Research Report
## Quality & Output Evaluator — Audit, Gaps, and Hypotheses to Test

**Date**: February 2026  
**Based on**: Experiments 1 & 2 (H1 POS/Entropy, H2 TruthfulQA scale) + broader NLP/LLM evaluation literature  
**Files audited**: `src/mycontext/intelligence/quality_metrics.py`, `src/mycontext/intelligence/output_evaluator.py`

---

## Implementation Status

| Change | File | Hypothesis | Date |
|---|---|---|---|
| Pronoun ratio (tiered penalty/bonus) | `quality_metrics.py` — `_evaluate_clarity` | H2 experiment finding | Feb 2026 |
| Hedge density check | `quality_metrics.py` — `_evaluate_clarity` | H3 | Feb 2026 |
| Modal commitment ratio | `quality_metrics.py` — `_evaluate_clarity` | H10 | Feb 2026 |
| Directive-length penalty | `quality_metrics.py` — `_evaluate_efficiency` | H9 / Experiment 2 | Feb 2026 |
| Refusal/deflection detection | `output_evaluator.py` — `_score_instruction_following` | H11 | Feb 2026 |
| Numbered instruction coverage | `output_evaluator.py` — `_score_instruction_following` | H12 | Feb 2026 |
| Quantified claims scoring | `output_evaluator.py` — `_score_reasoning_depth` | H12 | Feb 2026 |
| Output hedge penalty | `output_evaluator.py` — `_score_actionability` | H3 output-side | Feb 2026 |

---

## What We Already Know (From Our Experiments)

| Finding | Experiment | Statistical strength |
|---|---|---|
| Pronoun ratio negatively predicts LLM accuracy | H2 TruthfulQA (n=200) | r=-0.187, p=0.008 ✅ significant |
| Shorter directive → better accuracy | H2 TruthfulQA (n=200) | r=-0.176, p=0.013 ✅ significant |
| Named entity count → directional but not generalizable | H1 only (n=10) | Did not survive H2 scale test |
| GPT-2 perplexity → no predictive power at scale | H2 TruthfulQA (n=200) | r=-0.000, p=0.999 ❌ useless |
| Semantic density (general embeddings) → mostly fails | H1 + H2 | Needs domain-specific embeddings |

**Already applied**: Pronoun ratio fix deployed to `_evaluate_clarity()` in `quality_metrics.py` (tiered thresholds at 5% and 10%, data-backed).

---

## Part 1 — `quality_metrics.py` Audit

### CLARITY dimension (weight: 0.20)

#### Gap 1: Hedge word detection is absent
**Problem**: The vague word list contains only 6 words (`thing`, `stuff`, `somehow`, `maybe`, `probably`, `whatever`). Instructions eroded by hedges like *"if applicable"*, *"when possible"*, *"try to"*, *"as needed"*, *"generally speaking"* lose binding force. A directive saying *"try to be concise when possible"* is fundamentally weaker than *"respond in exactly 3 sentences"* — currently both score identically.

**Research basis**: Hyland (1996) — hedging in academic and instructional discourse. Categorises hedge types: approximators, shields, plausibility shields, attribution shields.

> **Hypothesis H3**: Prompts with hedge density > 8% (hedges / total words) produce LLM outputs with higher structural variance — less predictable format — compared to prompts with explicit hard constraints. Testable by measuring output format consistency across N runs.

#### Gap 2: Sentence complexity / parse depth
**Problem**: Deeply nested clauses increase processing difficulty even for language models. *"The report that the analyst who the CEO hired wrote was inaccurate"* is harder to parse than *"The CEO hired an analyst. The analyst wrote a report. The report was inaccurate."* No check exists.

**Research basis**: Frazier & Fodor (1978) — Sausage Machine model of sentence processing. Gibson (1998) — dependency locality theory. Average dependency distance (mean number of tokens between a word and its head) is the standard metric.

> **Hypothesis H4**: Prompts with average dependency distance > 4 tokens produce outputs that miss sub-clauses of the original instruction at a measurably higher rate than prompts with average dependency distance ≤ 2. Testable with spaCy dependency parsing + output compliance scoring.

#### Gap 3: Internal contradiction detection
**Problem**: *"Be concise but comprehensive"*, *"Be brief but thorough"*, *"Keep it simple but detailed"* — these are self-contradicting instructions that appear regularly in real templates. No evaluation framework currently catches them.

> **Hypothesis H5**: Prompts containing antonym-pair instructions produce lower instruction-following scores than semantically equivalent prompts that resolve the contradiction explicitly (e.g., *"Respond in 5 bullet points, each under 15 words"*). Testable with a small antonym dictionary and controlled prompt pairs.

---

### SPECIFICITY dimension (weight: 0.15) — The weakest dimension

#### Gap 4: Concreteness scoring not used
**Problem**: The current implementation detects 13 generic domain indicator words (`algorithm`, `methodology`, `framework`, etc.) as a proxy for specificity. This is shallow — the word "framework" can appear in a vague or a specific prompt equally.

**Research basis**: Brysbaert et al. (2014) — concreteness ratings for 40,000 English words, publicly available. Every content word gets a 1–5 rating (dog = 4.9, algorithm = 2.8, truth = 1.5). Average concreteness of directive content words is a validated, data-backed measure of how grounded the instruction is.

> **Hypothesis H6**: Prompts whose directive content words average concreteness > 3.0 produce LLM outputs with more named entities and specific facts (measured by NE count in output) than prompts averaging < 2.0. Testable by joining directive words with the Brysbaert database.

#### Gap 5: Semantic specificity — hypernym depth not used
**Problem**: *"Retrieve the document"* and *"Retrieve the Q3 2024 board report on supply chain risk"* are both present-tense directives with similar word counts. The current scorer sees them as nearly equivalent. WordNet hypernym depth directly measures this: the deeper a noun in the taxonomy, the more specific it is.

> **Hypothesis H7**: Prompts with lower average word frequency (Zipf scale) in their directive — rarer, more specific vocabulary — produce answers with higher factual precision (FActScore) than prompts with common everyday vocabulary. Testable without external datasets using unigram frequency lists.

---

### COMPLETENESS dimension (weight: 0.25)

#### Gap 6: Frame Semantics role filling not checked
**Problem**: The current check is purely structural — does the prompt have a guidance section? A directive section? Constraints? It never checks whether the *semantic roles* required by the task verb are filled.

**Research basis**: Fillmore (1982) — Frame Semantics. FrameNet. Every task verb opens argument slots:
- `Summarize` requires: **Text** (what), **Length** (how long), **Audience** (for whom)
- `Analyze` requires: **Phenomenon** (what), **Manner** (how), **Result format**
- `Compare` requires: **Item 1**, **Item 2**, **Criteria**

If slots are unfilled, the model must hallucinate or guess.

> **Hypothesis H8**: Prompts that explicitly fill all required FrameNet argument slots for their primary action verb produce outputs that require fewer clarifying follow-up exchanges and have lower hallucination rates than prompts with unfilled obligatory roles. Testable by building a slot-filling checker for the 20 most common task verbs and comparing against outputs.

---

### EFFICIENCY dimension (weight: 0.10)

#### Gap 7: Direction is partially wrong for directive length
**Problem**: The current scorer rewards longer prompts up to 500 words and only penalizes above 1000. Our Experiment 2 found shorter *directives* → better accuracy (r=-0.176, p=0.013). These aren't contradictory — they measure different things:
- System prompt / template body: longer with more constraints is better
- The directive / question portion specifically: shorter is better

The scorer doesn't separate directive length from total assembled length.

> **Hypothesis H9**: Holding system prompt content constant, directives under 30 words produce measurably higher instruction-following accuracy than equivalent directives over 80 words on factual QA tasks. Testable by ablating directive length on a fixed benchmark.

---

### Missing dimension: Instruction Commitment / Binding Force

**Problem**: No existing dimension captures whether instructions are **binding** vs **suggestive**. A prompt full of *"should"*, *"try to"*, *"ideally"*, *"if possible"* is structurally a different class of instruction from one using *"must"*, *"always"*, *"never"*, *"exactly"*. Modal verb ratio is a direct, cheap measure.

**Research basis**: Deontic logic in linguistics — obligation (must) vs permission (may) vs suggestion (should) carry fundamentally different illocutionary force. Applied to instruction following in Ouyang et al. (2022) — InstructGPT implicitly relies on this distinction.

> **Hypothesis H10**: Prompts with modal verb ratio (must/shall/will vs should/could/might) > 0.7 produce outputs with higher constraint satisfaction rates than prompts with ratio < 0.3. Testable with a simple regex count + compliance scoring.

---

## Part 2 — `output_evaluator.py` Audit

### INSTRUCTION_FOLLOWING dimension (weight: 0.25) — Biggest gap

#### Gap 8: Refusal and deflection are completely invisible
**Problem**: The scorer checks whether action verbs from the context appear in the output. Base score is 0.3. It never detects refusal or deflection. When the model outputs *"I can't help with that"* or *"As an AI language model, I don't have access to..."*, the scorer assigns 0.3 and potentially adds bonuses for coincidental action verbs. A compliant and a refusing model can receive the same score.

**Research basis**: IFEval (Zhou et al., 2023) — instruction-following evaluation. Identifies non-compliance detection as the most critical gap in automatic evaluation. SELF-RAG (Asai et al., 2023) — self-reflection on compliance.

Common refusal patterns:
- "I can't / I cannot / I'm unable to / I don't have the ability to"
- "As an AI / As a language model / I'm just an AI"
- "This falls outside / beyond my capabilities"
- "I don't have access to real-time / current / live"
- "I'd recommend consulting a professional"
- "I need to clarify that I cannot"

> **Hypothesis H11**: A refusal/deflection detector (regex matching 20 common refusal phrases) reduces false-positive instruction-following scores by > 30% compared to the current scorer on a test set of intentionally refused outputs. This is testable immediately with no external data needed.

#### Gap 9: Numbered instruction coverage not measured
**Problem**: If the directive says *"Do the following 5 things: 1. X 2. Y 3. Z 4. A 5. B"*, the scorer doesn't check how many of the 5 items appear in the output. An output addressing only items 1 and 3 scores as well as one addressing all 5.

> **Hypothesis H12 (output)**: Outputs that address ≥ 80% of numbered items from the directive have significantly higher human quality ratings than outputs addressing < 50%, independent of overall output length. Testable with numbered instruction extraction + output coverage scoring.

---

### REASONING_DEPTH dimension (weight: 0.20)

#### Gap 10: Markers without logic — surface markers vs actual reasoning
**Problem**: A model can write *"Therefore, the answer is X. However, it should be noted that... Consequently..."* repeatedly with no logical chain and score highly. The scorer counts discourse markers without verifying they're doing logical work.

**Research basis**: Habernal & Gurevych (2016) — argumentation quality corpus. Wachsmuth et al. (2017) — computational argumentation quality. Consistent finding: **quantified claims** are the strongest signal of reasoning depth.

#### Gap 11: Quantification as depth signal not used
**Problem**: The single strongest marker of reasoning depth — specific numbers, percentages, dates, measurements — is not measured. *"Performance declined significantly"* (shallow) vs *"Performance declined 23% YoY from Q2 2023 to Q2 2024"* (deep).

> **Hypothesis H12**: Outputs containing ≥ 2 specific quantified claims (number + unit/context) correlate with higher human quality ratings than outputs of equal length with zero quantified claims, independent of discourse marker count. Testable by annotating quantified claims with regex + correlation against human ratings.

#### Gap 12: Counterfactual consideration not measured
**Problem**: High-quality reasoning considers alternatives. *"An alternative interpretation is..."*, *"This assumes X; if instead Y were true..."*, *"A counterargument would be..."* These are structural markers of evaluative depth (Bloom's level 5). Not measured.

**Research basis**: Tree of Thought (Yao et al., 2023). Self-Consistency (Wang et al., 2022). Both show alternative-path consideration is a strong predictor of final answer quality.

---

### ACTIONABILITY dimension (weight: 0.20)

#### Gap 13: Vague recommendations not penalised
**Problem**: The current scorer rewards action phrases (`should`, `implement`, `recommend`) regardless of specificity. It cannot distinguish:
- *"You should improve the system"* — actionable phrase, zero specificity
- *"Refactor the authentication module to use RS256 JWT tokens by end of Q2"* — fully actionable

**Research basis**: Decision science and consulting research on recommendation quality. Three components of a truly actionable recommendation: **Specificity** (what exactly), **Ownership** (who does it), **Time-boundedness** (by when). Currently only "what" is loosely checked.

> **Hypothesis H13**: Adding an ownership detection check (named actor/role + verb + specific action) increases correlation with human-rated actionability scores by > 0.15 Pearson r compared to the current keyword-match approach. Testable with a small human-rated actionability dataset.

#### Gap 14: Vague hedge penalty absent in outputs
**Problem**: Outputs full of *"it depends"*, *"generally speaking"*, *"in most cases"*, *"this varies"* without ever committing to a specific answer are low quality — but currently score well on actionability if they contain "should" and "recommend". This is the output-side version of Gap 1.

---

### STRUCTURE_COMPLIANCE dimension (weight: 0.15)

#### Gap 15: Length and count constraints not verified
**Problem**: If a directive says *"List exactly 5 risks"* or *"Respond in under 200 words"*, the current scorer checks for the presence of lists and headers — it never counts whether 5 items are present or measures word count.

**Research basis**: IFEval (Zhou et al., 2023) — verifiable instruction constraints. Classifies instructions into: word count, format, section count, keyword inclusion, prohibition. Shows these are the most objectively scorable dimension.

> **Hypothesis H14 (structure)**: An IFEval-style verifiable constraint checker (extracting numeric constraints like "5 items", "200 words", "3 sections" from the directive and verifying in output) achieves higher agreement with human compliance scores than the current structure keyword matching. Immediately testable.

---

### COGNITIVE_SCAFFOLDING dimension (weight: 0.20) — Most novel, least validated

#### Gap 16: Bloom's Taxonomy gap not measured
**Problem**: The current implementation checks if the output uses the same framework keywords as the context. But a deeper question is: does the output operate at the cognitive level the context requested?

**Research basis**: Bloom's Taxonomy (1956), revised Anderson et al. (2001). Six levels:
1. Remember — recall facts
2. Understand — explain concepts
3. Apply — use in new situation
4. Analyze — break into parts, find relationships
5. Evaluate — make judgements
6. Create — synthesize new things

A context asking for synthesis (level 6) receiving a factual recall output (level 1) is a scaffolding mismatch.

> **Hypothesis H15**: Classifying both context directive and output by Bloom's Taxonomy level (using a fine-tuned classifier) and measuring the cognitive gap between them predicts human quality ratings better than the current framework keyword matching. Requires annotation effort but would be a publishable contribution.

#### Gap 17: Given/new information structure not used
**Problem**: Good scaffolded answers build from what the prompt established before introducing new information. Outputs that start with conclusions before establishing context violate cognitive coherence.

**Research basis**: Clark & Haviland (1977) — given/new contract in discourse comprehension.

---

## Priority Ranking: What to Test First

| Priority | Hypothesis | Effort | Expected impact | Requires | Status |
|---|---|---|---|---|---|
| 1 | **H11** — Refusal detection in instruction following | Low | High — closes biggest scorer gap | 20 regex patterns | **IMPLEMENTED** |
| 2 | **H3** — Hedge density → output variance | Medium | High — common real-world failure | Hedge wordlist + N-run experiment | **IMPLEMENTED** |
| 3 | **H6** — Concreteness ratings → output factuality | Medium | High — validated in linguistics | Brysbaert dataset (public) | pending |
| 4 | **H12** — Quantified claims → reasoning depth | Low | Medium-High | Regex + human ratings | **IMPLEMENTED** |
| 5 | **H10** — Modal commitment ratio → constraint satisfaction | Low | Medium | Regex modal lists | **IMPLEMENTED** |
| 6 | **H14** — IFEval-style verifiable constraints | Medium | Medium-High | Constraint extractor | pending |
| 7 | **H13** — Ownership detection → actionability | Low | Medium | Named actor patterns | pending |
| 8 | **H8** — Frame Semantics role filling | High | High | FrameNet integration | pending |
| 9 | **H5** — Contradiction detection | Medium | Medium | Antonym dictionary | pending |
| 10 | **H15** — Bloom's Taxonomy gap | High | Unknown — novel | Annotation effort | pending |
| 11 | **H4** — Dependency distance → missed sub-instructions | High | Medium | spaCy parsing | pending |
| 12 | **H9** — Directive length ablation | Low | Medium (replicates H2) | Controlled prompt set | **IMPLEMENTED** |

---

## Recommended next experiments (in order)

### Experiment 3 — Refusal Detection Validation (H11)
Build a test set of 50 compliant outputs and 50 refused/deflected outputs. Measure current scorer vs refusal-aware scorer. Expected result: near-zero false positives on refusals. Fast to build, immediate production value.

### Experiment 4 — Hedge Density Study (H3)
Take 20 real prompt templates from the codebase. Create hedged and unhedged versions of each directive. Run 5 times each. Measure: output format consistency, constraint satisfaction. Estimated cost: ~$2 in API calls.

### Experiment 5 — Concreteness Study (H6)
Join the Brysbaert (2014) concreteness database with TruthfulQA question vocabularies. Correlate average concreteness with accuracy. Pure data analysis — no new LLM calls needed if we use the H2 results file.

---

## Next Phase — Research Experiments (in progress)

All four experiment notebooks are in `research/experiments/`:

| Notebook | Track | Status | Runs needed |
|---|---|---|---|
| `track_b_ifeval_constraints_experiment.ipynb` | B — IFEval constraint extraction | Ready to run | No LLM calls (pure Python) |
| `track_c_brysbaert_concreteness_experiment.ipynb` | C — Brysbaert concreteness scoring | Ready to run | No LLM calls (1 download) |
| `track_d_calibration_study.ipynb` | D — Human calibration | Ready to run | ~$1 (50 × LLM eval) |
| `track_e_cai_cross_model.ipynb` | E — Cross-model CAI study | Ready to run | ~$3–5 (6 templates × 3 models × 3 runs) |

### Run order
1. **Track B** first — pure Python, validates IFEval before code deployment
2. **Track C** second — one download, validates concreteness before code deployment
3. **Track D** third — LLM calibration study (Phase 1: ~$1)
4. **Track E** last — most expensive, builds on Track D insights

---

## References

- Brysbaert, M. et al. (2014). *Concreteness ratings for 40 thousand generally known English word lemmas.* Behavior Research Methods.
- Clark, H. & Haviland, S. (1977). *Comprehension and the given-new contract.* Discourse production and comprehension.
- Fillmore, C. (1982). *Frame Semantics.* Linguistics in the Morning Calm.
- Frazier, L. & Fodor, J. (1978). *The Sausage Machine: A new two-stage parsing model.* Cognition.
- Gibson, E. (1998). *Linguistic complexity: Locality of syntactic dependencies.* Cognition.
- Habernal, I. & Gurevych, I. (2016). *Which argument is more convincing?* ACL.
- Hyland, K. (1996). *Writing without conviction? Hedging in science research articles.* Applied Linguistics.
- IFEval — Zhou, J. et al. (2023). *Instruction-Following Evaluation for Large Language Models.* arXiv.
- InstructGPT — Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback.* NeurIPS.
- SELF-RAG — Asai, A. et al. (2023). *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection.* arXiv.
- Tree of Thought — Yao, S. et al. (2023). *Tree of Thoughts: Deliberate Problem Solving with Large Language Models.* arXiv.
- Wachsmuth, H. et al. (2017). *Computational argumentation quality assessment in natural language.* EACL.
- Wang, X. et al. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* arXiv.

---

*Research report — mycontext/research/METRICS_RESEARCH_REPORT.md*  
*Companion notebooks: hypothesis_1_pos_entropy_experiment.ipynb, hypothesis_2_truthfulqa_scale.ipynb*
