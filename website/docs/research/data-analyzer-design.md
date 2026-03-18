---
sidebar_position: 7
title: "DataAnalyzer: Research Foundation"
description: "The academic and industry research behind DataAnalyzer's 11-section design — mapping each section to CRISP-DM, KDD, Tukey's EDA, anomaly detection literature, evidence-based reporting, and visualization science."
---

# DataAnalyzer: Research Foundation

:::info TL;DR
DataAnalyzer's 11-section structure is not arbitrary — it maps directly to four established analytical frameworks: **CRISP-DM** (the industry-standard data mining process), **Tukey's EDA** (exploratory data analysis methodology), **Chandola et al.'s anomaly detection survey** (ACM Computing Surveys, 2009), and **evidence-based insight reporting** practices. The intent system (executive, analyst, operations) maps to how real analyst personas actually consume data — each intent selects only the sections relevant to that role's decision-making needs.
:::

## Motivation

Most "data analysis" AI prompts ask the model to "analyze this data and give insights." The model complies — producing something plausible but structurally inconsistent. Different runs produce different sections. Evidence is implicit. Confidence is unrated. The distinction between a trend and an anomaly is blurred. Recommendations aren't tied to findings.

The academic and industry literature on data analysis is precise about what a complete analysis looks like. CRISP-DM documented it in 1999. Tukey formalized it in 1977. The anomaly detection literature structured it further. DataAnalyzer encodes that literature into binding directives — sections the LLM must produce, in a format that makes every claim traceable.

## Research Foundation

| Framework / Source | What It Contributes | Where It Appears |
|-------------------|---------------------|------------------|
| **CRISP-DM** (Chapman et al., 1999) | Industry-standard 6-phase data mining process | Sections 1–2 (Data Understanding), 3–6 (Modeling), 7–8 (Evaluation), 10–11 (Deployment) |
| **KDD Process** (Fayyad et al., 1996) | Knowledge Discovery in Databases pipeline | Sections 3–6 (Data Mining phase), 7–8 (Interpretation) |
| **Tukey, J.W. (1977)** | Exploratory Data Analysis — resistant statistics, pattern revelation | Sections 2 (median alongside mean), 3 (trend/seasonality), 11 (visualization) |
| **Chandola, Banerjee & Kumar (2009)** | Anomaly Detection Survey — ACM Computing Surveys | Section 4 (context + severity + possible cause structure) |
| **Peirce / Popper (1878 / 1959)** | Abductive reasoning; falsifiability requirement | Section 8 (hypotheses with supporting/contradicting evidence + testable prediction) |
| **Gneiting & Raftery (2007)** | Calibrated probability assessment | Section 7 (High/Medium/Low confidence ratings on every insight) |
| **Cleveland & McGill (1984)** | Graphical perception — chart-type-to-data-structure matching | Section 11 (chart type directive + justification field) |
| **Redman (1996)** | Data quality dimensions — accuracy, completeness, consistency, timeliness | Section 9 (data limitations with confidence caveats) |
| **Sackett et al. (1996)** | Evidence-based medicine — claims require cited evidence | Section 7 (Evidence field required for every insight) |

---

## Section-by-Section Mapping

### Section 1 — Data Overview

```
- Data type: [What kind of data]
- Time period: [Coverage]
- Sample size: [How much data]
- Variables: [What's measured]
- Quality: [Completeness, accuracy]
```

**CRISP-DM: Data Understanding phase.**
The first phase of CRISP-DM after Business Understanding is Data Understanding: collect data, describe it, explore it, verify quality. DataAnalyzer combines the "collect" (via connectors) and "describe" steps into the Data Overview — establishing data type, coverage, size, variables, and quality before any analysis begins.

**What it prevents:** Without this section, the LLM may produce analysis with unstated assumptions about what the data represents, how much of it there is, or whether it's complete. The Quality sub-field explicitly requires the model to flag missing values, coverage gaps, and accuracy concerns before drawing conclusions.

---

### Section 2 — Descriptive Statistics

```
- Central tendency: [Mean, median, mode — if mean and median diverge
  significantly, state the skew direction and which metric better represents
  the typical value for this distribution]
- Dispersion: [Range, variance, std dev]
- Distribution: [Shape, skewness]
- Key figures: [Notable numbers]
```

**Tukey (1977): Resistance principle.**
Tukey's foundational EDA principle distinguishes *resistant* statistics (robust to outliers) from non-resistant ones. The median is a resistant statistic — it barely moves when extreme values change. The mean is not — one outlier shifts it materially. The template does two things: it requests both statistics, and it adds a binding interpretation instruction — if they diverge, state the skew direction and declare which metric is the more reliable representation of the typical value. This is the Tukey principle operationalized: not just "report both," but "interpret what the difference means."

**CRISP-DM: Data Understanding — "explore data" step.**
CRISP-DM's data exploration step requires summary statistics as the starting point before modeling.

**What it prevents:** A mean reported without context on skewed data (income, revenue, error rates, response times) is routinely misleading. Sales data with a few enterprise contracts will show a mean 3x above the median — the mean describes the portfolio, the median describes the typical customer. Reporting both without interpretation leaves this gap open. The divergence instruction closes it.

---

### Section 3 — Pattern Detection

```
Trends: direction, evidence, magnitude, timeframe
Seasonality: pattern, frequency, amplitude
Clusters: groups, characteristics
```

**Tukey (1977): Re-expression and Revelation.**
Two of Tukey's four EDA principles directly shape this section. *Re-expression* (transforming data to reveal structure) is implied by asking for seasonality decomposition — separating cyclical patterns from trends. *Revelation* (displaying data to reveal otherwise-hidden structure) drives the tri-partite structure: trends (monotonic changes), seasonality (periodic changes), and clusters (cross-sectional groupings) cover the three primary pattern types EDA identifies.

**KDD: Data Mining phase — pattern recognition.**
The KDD process defines data mining as "finding patterns that are potentially useful" (Fayyad et al., 1996). The three sub-types (trend, seasonality, cluster) map to KDD's core mining tasks: classification/regression (trend direction), sequence discovery (seasonality), and clustering.

**What it prevents:** Unstructured pattern detection produces whatever pattern the model finds first. Separating trends from seasonality from clusters forces the model to look for all three, not just the most obvious.

---

### Section 4 — Anomaly Detection

```
- Anomaly: [What's unusual]
  - Context: [When/where]
  - Severity: [How far from normal]
  - Possible cause: [Why it might occur]
```

**Chandola, Banerjee & Kumar (2009): "Anomaly Detection: A Survey."**
This ACM Computing Surveys paper — the most cited survey in anomaly detection literature — defines an anomaly report as requiring three components: *characterization* (what is unusual), *context* (the conditions under which it is anomalous), and *severity* (how anomalous). DataAnalyzer's anomaly block implements all three, with "Possible cause" added as an interpretation layer.

The Chandola taxonomy also distinguishes *point anomalies* (single unusual data point), *contextual anomalies* (unusual only in context), and *collective anomalies* (unusual as a group). The "Context: When/where" field captures this distinction — forcing the model to specify whether the anomaly is absolute or context-dependent.

**What it prevents:** Anomaly detection without context produces false alarms. A spike in website traffic is anomalous in isolation but expected after a product launch. The "Context" field forces the model to situate every anomaly before assigning severity.

---

### Section 5 — Correlation Analysis

```
- Correlation 1: [X relates to Y]
  - Strength: [Strong/moderate/weak]
  - Direction: [Positive/negative]
  - Note: [Correlation ≠ causation]
```

**Pearson (1896) / Spearman (1904): Correlation coefficients.**
The strength/direction framework (strong/moderate/weak, positive/negative) encodes Pearson and Spearman's correlation coefficient interpretation conventions, translated into language accessible to business analysts without requiring numerical scores.

**Causation-correlation distinction — enforced.**
The explicit "Correlation ≠ causation" note is binding language — not a footnote suggestion, but a required field in every correlation finding. This implements the statistical reasoning principle documented in Pearl (2000) and routinely violated in practice. LLMs without this constraint routinely slide from "X and Y are correlated" to "X causes Y."

**What it prevents:** Correlation sections without the causation caveat produce action recommendations based on spurious relationships. The binding note forces the model to acknowledge the limitation before the reader acts on it.

---

### Section 6 — Comparative Analysis

```
| Segment | Metric A | Metric B | Insight |
```

**CRISP-DM: Comparative modeling — subgroup analysis.**
CRISP-DM's modeling phase includes comparative analysis as a core technique: running the same analysis across subgroups and comparing results. The structured table format enforces side-by-side comparison rather than sequential description, which research on decision-making shows aids comparative judgment (Payne, Bettman & Johnson, 1993 — *The Adaptive Decision Maker*).

**What it prevents:** Narrative segment comparisons (first North, then South, then East) make direct comparisons difficult. The table format forces quantitative side-by-side presentation. The Insight column forces segment-specific conclusions rather than overall observations.

---

### Section 7 — Key Insights

```
Insight #N: [Major finding]
- Evidence: [What supports this]
- Confidence: [High/Medium/Low]
- Significance: [Why it matters]
- Action: [What to do about it]
```

**Evidence-based practice (Sackett et al., 1996).**
Evidence-based medicine established the principle that every clinical recommendation requires cited evidence. The same principle applies to data analysis recommendations. DataAnalyzer's Evidence field enforces this: every insight must reference the specific data point, trend, or statistical finding that supports it. An insight without evidence is an opinion.

**Calibrated confidence (Gneiting & Raftery, 2007).**
Gneiting and Raftery's work on probabilistic forecasting establishes that calibrated uncertainty communication — explicitly stating confidence levels — produces better decision-making than point estimates presented as certainties. The High/Medium/Low scale is a deliberate simplification of their framework, trading statistical rigor for operational accessibility:

| Confidence | Meaning in DataAnalyzer |
|-----------|------------------------|
| High | Pattern is unambiguous, data is sufficient, alternative explanations are unlikely |
| Medium | Pattern visible but data limitations exist, or alternatives are plausible |
| Low | Suggestive but insufficient to conclude — needs more data or additional analysis |

**Storytelling with Data (Nussbaumer Knaflic, 2015).**
The Significance + Action fields implement Knaflic's principle that insights must be anchored to business impact and must drive action. "Revenue declined" is a description. "Revenue declined 15% in East region, driven by churn increase in SMB segment (Confidence: High) — indicating the regional pricing change introduced in Q3 is affecting price-sensitive customers; recommend reverting or adding a grandfathering clause" is an insight.

**What it prevents:** Insights without evidence are unverifiable. Insights without confidence ratings appear equally reliable regardless of data quality. Insights without action are reports, not analysis.

---

### Section 8 — Hypotheses

```
- Hypothesis: [Explanation for pattern]
  - Supporting evidence: [What fits]
  - Contradicting evidence: [What doesn't]
  - Test: [How to verify]
```

**Abductive reasoning — Peirce (1878).**
Peirce's logic of abduction (inference to the best explanation) is the formal basis for hypothesis generation from observation. Given a surprising fact, abductive reasoning generates the most plausible explanation. DataAnalyzer's hypothesis structure implements this: the "Hypothesis" field is the abduced explanation, "Supporting evidence" confirms it, "Contradicting evidence" stress-tests it.

**Falsifiability — Popper (1959).**
Popper's criterion for scientific hypotheses is that they must be falsifiable — there must be a possible observation that would prove them wrong. The "Test: [How to verify]" field enforces falsifiability. Every hypothesis must include a concrete test that would confirm or disconfirm it. Without this field, the LLM generates unfalsifiable explanations ("the market changed") that cannot guide investigation.

**What it prevents:** Analysis without hypothesis generation leaves patterns unexplained — the analyst knows what happened but not why. Analysis with hypotheses but without contradicting evidence produces confirmation bias: the model generates only explanations that fit. The contradicting evidence field forces the model to actively look for disconfirming observations.

---

### Section 9 — Data Limitations

```
- Limitation 1: [Data gap or issue]
- Limitation 2: [Bias or constraint]
- Limitation 3: [Missing information]
Confidence caveats: [What we can't conclude]
```

**Data quality dimensions — Redman (1996).**
Redman's framework identifies four core data quality dimensions: accuracy (does the data reflect reality?), completeness (is anything missing?), consistency (are values coherent across records?), and timeliness (is the data current?). The three limitation fields map to three of these: data gaps cover completeness, biases cover accuracy, and missing information covers consistency. Timeliness is captured indirectly in Section 1's "Time period: [Coverage]" field. Section 9 is where these quality assessments translate into explicit caveats on conclusions — not just "the data has gaps" but "therefore we cannot conclude X."

**What it prevents:** Analyses without stated limitations invite overconfident decision-making. The "What we can't conclude" confidence caveats field is particularly important — it forces the model to enumerate invalid inferences, not just note data quality issues in the abstract.

---

### Section 10 — Recommendations

```
Immediate Actions: [Evidence-based actions]
Further Investigation: [What data needed, what to run next]
Success Metrics: [How to measure if actions work]
```

**CRISP-DM: Deployment phase.**
CRISP-DM's final phase (Deployment) requires not just delivering findings but specifying how they will be acted on. DataAnalyzer's Recommendations section implements this: Immediate Actions are the deployment actions, Further Investigation closes the loop back to the data understanding phase (CRISP-DM is explicitly iterative), and Success Metrics define the evaluation criteria for the deployment.

**OKR-style measurability.**
The Success Metrics field implements the principle from OKR methodology (Doerr, 2018): every recommended action should have a measurable outcome. "Investigate East region churn" is a task. "Target: reduce East region churn from 11% to 8% in Q1, measured by monthly cohort analysis" is an actionable recommendation.

**What it prevents:** Recommendations without success metrics cannot be evaluated. Further Investigation without specificity ("we need more data") produces infinite analysis loops. The structure forces the model to close the analytical loop.

---

### Section 11 — Visualization Suggestions

```
Best ways to present findings — match chart type to data structure:
line/area charts for time-series trends; bar/column charts for category
comparison; scatter plots for correlations; histograms or box plots for
distributions; heatmaps for multi-variable relationships.
- Chart 1: [Type] for [Data] — [Why this chart fits this pattern]
- Chart 2: [Type] for [Pattern] — [Why this chart fits this pattern]
- Dashboard: [Key metrics to track]
```

**Cleveland & McGill (1984): Graphical perception.**
Cleveland and McGill's landmark study established that different chart types encode data with different perceptual accuracy — position along a common scale is the most accurately perceived, followed by length, then angle, area, and color. The template's chart-type directive encodes this directly: line charts for time-series (position along a common temporal scale), bar/column charts for category comparison (length), scatter plots for correlations (position on two scales), histograms for distributions (length). The "Why this chart fits this pattern" field forces the model to justify each chart selection, not just list a type — implementing the match-chart-to-data-structure principle explicitly rather than leaving it to model priors.

**Tukey (1977): Revelation principle.**
Tukey's fourth EDA principle (*Revelation*) requires that analysis culminate in visual displays that reveal the structure found in the data. Visualization suggestions as a required section — not an optional appendix — implements this principle.

**What it prevents:** Without chart-type guidance, models default to bar charts for everything. The directive forces chart selection to follow data structure: a time-series trend should not be presented as a bar chart (which loses the temporal continuity that makes the trend visible). The justification field prevents arbitrary selection.

---

## Intent System: Persona-Specific Analysis

The five intents select different section subsets. Each selection reflects how real analyst personas actually consume data:

| Intent | Sections | Research Basis |
|--------|----------|----------------|
| `executive` | Overview, Insights, Viz, Recommendations | C-suite research (McKinsey, 2022): executives prioritize "so what" and "do what" over methodology. Statistical sections create noise. |
| `analyst` | Overview, Statistics, Patterns, Correlations, Hypotheses | Standard data science workflow (CRISP-DM data understanding + modeling phases) — the analytical building blocks plus hypothesis generation (Peirce/Popper), which an analyst running a deep-dive needs to explain the patterns they find. |
| `operations` | Overview, Anomaly Detection, Recommendations | ITIL/SRE incident management practice: ops triage requires anomaly characterization and immediate action, not trend analysis. |
| `summary` | Overview, Insights, Recommendations | Management communication research (Minto, 1987 — Pyramid Principle): decision support requires a situation-complication-resolution structure, not full methodology. |
| `comprehensive` | All 11 | Full CRISP-DM + KDD pipeline — appropriate for audit-grade, regulatory, or deep research contexts. |

**The parameterization finding validates the intent design.** In our [parameterization study](/docs/research/data-analyzer-parameterization), executive intent (4 sections) scored 9.5/10 while comprehensive (11 sections) scored 8.8/10. The executive selection isn't a subset — for a business context, it's the right set. Focused attention on the sections that match the decision context outperforms exhaustive coverage.

---

## What We Chose Not to Include

Honest accounting of what the research recommends that DataAnalyzer deliberately omits:

| Research Recommendation | Why Omitted |
|------------------------|-------------|
| **Formal statistical tests** (p-values, confidence intervals) — standard in CDA | LLMs cannot reliably compute statistics from raw text descriptions; formal tests require the data, not a description of it. Users should run pandas/scipy first and pass results as data. |
| **Data Preparation guidance** (CRISP-DM phase 3) | Users prepare data before passing it; connectors (from_dataframe, from_csv_path) handle serialization. Prompting the LLM to describe data prep steps it cannot perform produces hallucinated methodology. |
| **Model selection** (CRISP-DM phase 4 — ML model choice) | DataAnalyzer targets business analysis, not predictive modeling. Adding model selection for analysis that doesn't require it would produce noise for 90% of use cases. |
| **Deployment planning** (CRISP-DM phase 6 — beyond recommendations) | Implementation planning depends on organizational context the LLM doesn't have. Success Metrics in Section 10 is the proxy — it specifies measurability without pretending to plan deployment. |

---

## Hypotheses for Future Testing

The section design is research-backed but not empirically validated at the section level. The following experiments should be run:

| # | Hypothesis | How to Test |
|---|-----------|-------------|
| 1 | The causation-correlation explicit note in Section 5 reduces spurious action recommendations | Compare recommendations quality when note is present vs. absent; use human judges to rate whether recommended actions are based on correlational vs. causal evidence |
| 2 | The contradicting-evidence field in Section 8 reduces confirmation bias in hypotheses | Compare hypothesis quality (diversity of explanations, balance of evidence) with/without the contradicting evidence requirement |
| 3 | The confidence rating in Section 7 improves decision quality downstream | Present same insights with and without confidence ratings to decision-makers; measure decision quality and calibration |
| 4 | The evidence field in Section 7 reduces hallucinated insights | Run template with/without the Evidence requirement; measure how often insights cite specific data vs. make unsubstantiated claims |
| 5 | The Success Metrics field in Section 10 improves recommendation actionability | Have practitioners rate recommendations with/without success metrics on a 1–10 actionability scale |

These experiments would follow the methodology of the [DataAnalyzer parameterization study](/docs/research/data-analyzer-parameterization): controlled conditions, consistent dataset, LLM-as-judge scoring, external validator (DeepEval GEval).

---

## Research References

1. **Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (1999).** "CRISP-DM 1.0: Step-by-step data mining guide." SPSS Inc. The industry-standard 6-phase data mining process: Business Understanding → Data Understanding → Data Preparation → Modeling → Evaluation → Deployment. DataAnalyzer covers phases 2, 4, 5, and 6.

2. **Fayyad, U., Piatetsky-Shapiro, G., & Smyth, P. (1996).** "From Data Mining to Knowledge Discovery in Databases." *AI Magazine*, 17(3), 37–54. Defined the KDD pipeline and established pattern interpretation/evaluation as distinct from pattern detection.

3. **Tukey, J.W. (1977).** *Exploratory Data Analysis.* Addison-Wesley. Foundational text establishing resistant statistics (median alongside mean), residual analysis, and the revelation principle (analysis should culminate in visual structure). Directly implemented in Sections 2, 3, and 11.

4. **Chandola, V., Banerjee, A., & Kumar, V. (2009).** "Anomaly Detection: A Survey." *ACM Computing Surveys*, 41(3), 1–58. The most cited anomaly detection survey. Defines anomaly characterization as requiring: what is unusual, the context in which it is anomalous, and its severity. Section 4 implements this structure.

5. **Peirce, C.S. (1878).** "Deduction, Induction, and Hypothesis." *Popular Science Monthly*, 13, 470–482. Formalized abductive reasoning (inference to the best explanation) — the logical basis for the hypothesis generation structure in Section 8.

6. **Popper, K. (1959).** *The Logic of Scientific Discovery.* Hutchinson. Established falsifiability as the criterion for scientific hypotheses. Section 8's "Test: [How to verify]" field directly enforces falsifiability — every hypothesis must specify what would confirm or disconfirm it.

7. **Gneiting, T., & Raftery, A.E. (2007).** "Strictly Proper Scoring Rules, Prediction, and Estimation." *Journal of the American Statistical Association*, 102(477), 359–378. Established calibrated probability assessment as a standard for reliable uncertainty communication. Section 7's confidence rating (High/Medium/Low) implements accessible calibration.

8. **Sackett, D.L., Rosenberg, W.M.C., Gray, J.A.M., Haynes, R.B., & Richardson, W.S. (1996).** "Evidence based medicine: what it is and what it isn't." *BMJ*, 312, 71–72. Established the principle that clinical (and analytical) claims require explicitly cited evidence. Section 7's Evidence field directly implements this requirement.

9. **Cleveland, W.S., & McGill, R. (1984).** "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods." *Journal of the American Statistical Association*, 79(387), 531–554. Established the perceptual hierarchy of visual encodings. Section 11's chart-type recommendations are grounded in this hierarchy.

10. **Redman, T.C. (1996).** *Data Quality for the Information Age.* Artech House. Defined data quality dimensions — accuracy, completeness, consistency, timeliness — that map directly to Section 9's Limitation and Confidence Caveat fields.

11. **Nussbaumer Knaflic, C. (2015).** *Storytelling with Data: A Data Visualization Guide for Business Professionals.* Wiley. Established that insights must be anchored to business significance and drive action — not just describe patterns. Sections 7 and 10 implement this through Significance and Action fields.

12. **Minto, B. (1987).** *The Pyramid Principle: Logic in Writing and Thinking.* Pitman. The summary intent's section selection (Overview → Insights → Recommendations) implements the Minto Pyramid: situation → complication → resolution — the minimal structure for decision support communication.

13. **Payne, J.W., Bettman, J.R., & Johnson, E.J. (1993).** *The Adaptive Decision Maker.* Cambridge University Press. Research on how humans compare alternatives shows that aligned, tabular formats support comparative judgment better than sequential narrative descriptions. Section 6's table format implements this.
