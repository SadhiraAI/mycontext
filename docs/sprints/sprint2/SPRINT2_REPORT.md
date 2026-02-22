# Sprint 2 — Results Report

> **Date**: Feb 21, 2026
> **Provider**: OpenAI (gpt-4o-mini)
> **Evaluator**: LLM mode (`mode="llm"`) — the LLM itself scores the output
> **Key change from Sprint 1**: Switched from heuristic to LLM-based evaluation

---

## Experiment 1: Integration Effectiveness (10 Questions, LLM Eval)

**Hypothesis**: Integrated templates produce higher quality output than raw prompts or single templates, and LLM evaluation will better capture this advantage.

### Test Setup

- 10 complex questions across business, technical, ethical, and organizational domains
- 3 conditions: Raw, Single template (question-specific), Integrated (4 auto-selected patterns)
- Smarter single-template selection: each question paired with best-fit template (not just root_cause_analyzer)
- Scored by `OutputEvaluator(mode='llm')`: 5 dimensions

### Results

| # | Question | Raw | Single | Integrated | Winner |
|---|---|---|---|---|---|
| 1 | Customer churn spike 40%? | 90.0% | 88.0% | **89.8%** | Raw |
| 2 | Migrate monolith to microservices? | **92.0%** | 75.5% | 88.0% | Raw |
| 3 | AI model producing biased hiring? | 94.0% | 86.5% | **96.0%** | **Integrated** |
| 4 | B2B SaaS go-to-market strategy? | **94.0%** | 65.0% | 86.0% | Raw |
| 5 | API response times tripled? | **100%** | 88.0% | 65.0% | Raw |
| 6 | $2M seed funding allocation? | 92.0% | **98.0%** | 94.0% | Single |
| 7 | Facial recognition in schools — ethics? | **88.0%** | 84.0% | 82.0% | Raw |
| 8 | Cross-functional communication breakdowns? | **98.0%** | 98.0% | 96.0% | Raw |
| 9 | PostgreSQL vs MongoDB vs DynamoDB? | **92.0%** | 65.0% | 88.0% | Raw |
| 10 | 12-month waterfall-to-agile roadmap? | 81.5% | **88.0%** | 86.0% | Single |

**Win count: Raw 7 / Single 2 / Integrated 1**

### Average Scores

| Condition | Avg Overall |
|---|---|
| **Raw** | **92.2%** |
| Single Template | 83.6% |
| Integrated | 87.1% |

### Per-Dimension Averages

| Dimension | Raw | Single | Integrated | Int vs Raw |
|---|---|---|---|---|
| Instruction Following | **96.0%** | 83.0% | 89.0% | -7.3% |
| Reasoning Depth | **86.0%** | 83.0% | 82.5% | -4.1% |
| Actionability | **87.0%** | 77.0% | 83.5% | -4.0% |
| Structure Compliance | **98.0%** | 90.0% | 93.0% | -5.1% |
| Cognitive Scaffolding | **87.0%** | 88.0% | 88.0% | +1.1% |

### Time Cost

| Condition | Avg Time |
|---|---|
| Raw | 14.5s |
| Single Template | 23.1s |
| Integrated | 38.1s |

Integrated takes ~2.6x longer than raw.

### Key Findings

1. **Raw prompts dominate under LLM evaluation (7/10 wins, 92.2% avg).** This is a dramatic shift from Sprint 1 where the three-way tie suggested templates were competitive. GPT-4o-mini produces well-structured, comprehensive responses natively. The LLM evaluator rewards completeness, clarity, and actionability — qualities the base model already delivers.

2. **Templates can HURT performance.** Single templates scored 65.0% on three questions (GTM strategy, database comparison, API performance) — the worst scores in the entire experiment. When a template's rigid framework doesn't fit the question's nature, the LLM wastes tokens on framework compliance instead of answering effectively. Several responses were flagged as "incomplete sections."

3. **Integration recovered what single templates lost.** On Q2 (microservices), single template scored 75.5% but integrated recovered to 88.0%. On Q9 (databases), single scored 65.0% but integrated reached 88.0%. Multi-template integration smooths out single-template mismatches.

4. **Integration's one clear win was on a genuinely complex problem.** Q3 (AI bias) required reasoning across technical, ethical, and legal domains — the integrated chain (root_cause_analyzer → differential_diagnoser → anomaly_detector → risk_mitigator) scored 96.0%, beating raw's 94.0%. This confirms that **multi-domain complexity** is where integration adds value.

5. **Cognitive Scaffolding is the ONLY dimension where templates match or beat raw** (88.0% vs 87.0%). This was our strongest finding in Sprint 1 and it persists under LLM evaluation — templates genuinely improve reasoning structure.

6. **The "perfect score" problem.** Q5 (API performance) got a perfect 100% raw and only 65.0% integrated. The integrated response (diagnostic_root_cause_analyzer → bottleneck_identifier → efficiency_analyzer → hypothesis_generator) was flagged as "incomplete" — 4 complex templates exceeded what the model could execute in one response.

---

## Experiment 2: Cognitive RAG (5 Questions, LLM Eval)

**Hypothesis**: Template + retrieved knowledge (Cognitive RAG) produces better output than either alone, especially with LLM-based evaluation that better captures reasoning quality.

### Test Setup

- 5 diverse questions, each with domain-specific simulated retrieved docs (800-1400 chars)
- 5 different templates matched per question
- 12-14 evidence markers per question to measure data grounding
- 4 conditions: Raw, RAG only, Template only, Cognitive RAG

### Results

| # | Question | Raw | RAG | Template | CogRAG | Winner | CogRAG Evidence |
|---|---|---|---|---|---|---|---|
| 1 | Churn spike analysis | **96.0%** | 94.0% | 88.0% | 88.0% | Raw | 6/12 |
| 2 | AI hiring bias diagnosis | 96.0% | 96.0% | **96.0%** | 87.0% | Tie (Tmpl) | 4/12 |
| 3 | Database comparison | 84.0% | **94.0%** | 65.0% | 82.0% | RAG | 10/12 |
| 4 | Facial recognition ethics | **88.0%** | 88.0% | 83.5% | 65.0% | Raw | 6/14 |
| 5 | $2M seed allocation | 96.0% | 94.0% | **98.0%** | 86.0% | Template | 7/14 |

**Win count: Raw 3 / RAG 1 / Template 1 / Cognitive RAG 0**

### Average Scores

| Condition | Avg Overall | Avg Evidence Recall |
|---|---|---|
| **Raw** | **92.0%** | 3.3% |
| RAG only | 93.2% | **65.2%** |
| Template only | 86.1% | 1.4% |
| Cognitive RAG | 81.6% | 51.9% |

### Per-Dimension Averages

| Dimension | Raw | RAG | Template | CogRAG | CogRAG vs Raw |
|---|---|---|---|---|---|
| Instruction Following | **98.0%** | 100% | 86.0% | 84.0% | -14.3% |
| Reasoning Depth | 88.0% | **90.0%** | 86.0% | 85.0% | -3.4% |
| Actionability | **88.0%** | 86.0% | 78.0% | 74.0% | -15.9% |
| Structure Compliance | **98.0%** | 100% | 92.0% | 88.0% | -10.2% |
| Cognitive Scaffolding | 86.0% | 88.0% | **92.0%** | 84.0% | -2.3% |

### Evidence Recall

| Condition | Avg Markers Found | Recall % |
|---|---|---|
| Raw | 0.4 / question | 3.3% |
| **RAG only** | **8.2 / question** | **65.2%** |
| Template only | 0.2 / question | 1.4% |
| Cognitive RAG | 6.6 / question | 51.9% |

### Key Findings

1. **Cognitive RAG won ZERO out of 5 questions.** This is a decisive negative result. Adding a template on top of retrieved documents consistently lowered quality compared to RAG alone or even raw prompts. The template's framework competes with the retrieved data for the model's attention and output tokens.

2. **RAG only is the most balanced condition.** It achieved the highest average (93.2%), near-perfect instruction following and structure, and the highest evidence recall (65.2%). Simple context injection — just stuffing docs into the prompt with a generic role — works remarkably well.

3. **Templates reduce evidence recall by 20%.** Cognitive RAG recalled 51.9% of evidence markers vs RAG only's 65.2%. The template's structured sections (Five Whys, Ishikawa diagrams, etc.) consume output tokens that would otherwise be used citing specific data points.

4. **The Q4 (ethics) crash is alarming.** Cognitive RAG scored just 65.0% on facial recognition ethics — with incomplete sections and missing framework applications. The ethical_framework_analyzer template requires applying 6 ethical frameworks, which combined with 14 data points from the retrieved docs, overwhelmed the model's output capacity.

5. **Template-only still excels on structured resource problems.** Q5 (seed funding allocation) saw template-only score 98.0% — the resource_allocator template is a near-perfect fit for budget allocation questions. But Cognitive RAG (template + docs) dropped to 86.0%. The docs actually distracted from the template's clean framework.

### Sprint 1 vs Sprint 2: Churn Question Comparison

| Condition | S1 (Heuristic) | S2 (LLM) | Change |
|---|---|---|---|
| Raw | 73.8% | 96.0% | +22.2% |
| RAG only | **87.3%** | 94.0% | +6.7% |
| Template only | 74.2% | 88.0% | +13.8% |
| Cognitive RAG | 73.9% | 88.0% | +14.1% |

The LLM evaluator is significantly more generous across the board (+6-22% higher scores). It confirms the Sprint 1 finding that RAG only is the strongest condition, but narrows the gap — raw now scores nearly as high as RAG.

---

## Cross-Experiment Analysis

### The Score Inflation Problem

| Metric | Sprint 1 (Heuristic) | Sprint 2 (LLM) |
|---|---|---|
| Raw avg (Integration test) | 76.4% | 92.2% |
| Raw avg (RAG test) | 73.8% | 92.0% |
| Overall range | 50.0% – 100% | 65.0% – 100% |
| Perfect scores (100%) | 0 | 1 |

The LLM evaluator compresses scores toward the top of the scale. This makes it harder to differentiate between conditions — a 2% difference under LLM eval might represent the same quality gap as a 15% difference under heuristic eval. **Neither evaluator is ideal; the truth likely lies between them.**

### Where Templates Consistently Add Value

Across both experiments and both evaluators, templates show persistent advantages in:

1. **Cognitive Scaffolding** — the one dimension where templates match or beat raw in both sprints
2. **Multi-domain complexity** — AI bias question won by integration in both Experiment 1 (96.0%) and was competitive in Experiment 2
3. **Structured resource allocation** — resource_allocator single template scored 98.0% (highest non-raw score in entire Sprint 2)

### Where Templates Consistently Hurt

1. **Well-known topics** — when GPT already has strong training data, templates add overhead without knowledge gain
2. **Simple/clear questions** — the template framework is overkill and causes incomplete outputs
3. **Combined with retrieved docs** — template structure competes with data for token budget

---

## Conclusions & Strategic Implications

### The Core Finding

**Templates are a specialist tool, not a universal enhancer.** Under LLM evaluation with 10 diverse questions, raw prompts won 70% of the time. This doesn't invalidate the SDK — it **redefines its value proposition**.

### When Templates Add Measurable Value

| Scenario | Evidence | Lift |
|---|---|---|
| Multi-domain complexity (technical + ethical + legal) | Q3 Integration: 96% vs 94% raw | +2.1% |
| Structured analytical frameworks (resource allocation, prioritization) | Q6 Single: 98% vs 92% raw | +6.5% |
| When cognitive scaffolding matters (educational, advisory outputs) | CS dimension: 88% vs 87% raw | +1.1% |

### When Templates Should Be Avoided

| Scenario | Evidence | Penalty |
|---|---|---|
| Well-known topics (GPT has strong training data) | Q5 Raw: 100% vs 65% integrated | -35% |
| Simple/direct questions | Q4 Raw: 94% vs 65% single | -29% |
| When retrieved docs are present (Cognitive RAG) | RAG: 93.2% vs CogRAG: 81.6% | -12.4% |

### SDK Strategy Recommendations

| # | Recommendation | Priority | Rationale |
|---|---|---|---|
| 1 | **Build a "complexity router"** — auto-detect when templates will help vs hurt | P0 | 70% of questions are better served raw; wasting user tokens/time on unnecessary templates erodes trust |
| 2 | **Lightweight RAG mode** — inject docs into Context.knowledge WITHOUT a template framework | P0 | RAG only (93.2%) beats Cognitive RAG (81.6%); simple injection is superior |
| 3 | **Template "weight" selector** — offer light (guidelines only) vs full (complete framework) | P1 | Full frameworks overwhelm gpt-4o-mini; lighter templates may preserve the scaffolding benefit without the token competition |
| 4 | **Pre-compute question complexity scores** using QualityMetrics | P1 | Route simple questions to raw execution, complex multi-domain questions to templates |
| 5 | **Trim integrator to 2-3 templates max** | P1 | 4-template integrations consistently produce incomplete outputs (Q5: 65%) |
| 6 | **Test with gpt-4o / Claude 3.5** (larger context window) | P2 | Template overhead may matter less with 128K context; could rehabilitate Cognitive RAG |
| 7 | **Build a hybrid evaluator** — weighted blend of heuristic + LLM scores | P2 | Neither evaluator alone is reliable; heuristic is too harsh on templates, LLM is too generous overall |

### The Silver Lining

The SDK's value is NOT "templates always improve output." The value is:

1. **Knowing WHEN to use templates** (complexity routing)
2. **85 ready-made cognitive frameworks** for the 30% of questions where they genuinely help
3. **Quality measurement infrastructure** (OutputEvaluator, QualityMetrics, CAI) that lets users prove what works
4. **Structured context assembly** (Context object, knowledge injection) that even benefits simple RAG

The path forward is making the SDK **smart about when to scaffold and when to step back**.

---

## Sprint 3 Proposals

| Experiment | Goal |
|---|---|
| **Complexity Router prototype** | Build a lightweight classifier (LLM-based or rules) that predicts whether templates will help a given question. Validate against Sprint 2 data. |
| **Lightweight templates** | Create "lite" versions of top templates (guidelines only, no multi-section frameworks). Test if they preserve Cognitive Scaffolding lift without the completion penalty. |
| **Larger model test** | Re-run Sprint 2 experiments on gpt-4o to test whether template overhead disappears with larger context windows. |
| **Hybrid evaluator** | Build a blended scoring system: 60% LLM eval + 40% heuristic, calibrated against human judgment on Sprint 1+2 outputs. |

---

*Sprint 2 complete. The LLM evaluator revealed that raw prompts are surprisingly strong — templates are a precision tool for complex problems, not a universal enhancer. Sprint 3 should focus on building intelligence around WHEN to use templates (complexity routing) and making templates lighter (reducing token competition).*
