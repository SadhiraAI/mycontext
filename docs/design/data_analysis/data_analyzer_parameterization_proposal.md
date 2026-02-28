# Data Analyzer Parameterization: Brainstorm & Design Proposal

> **Status**: Planning / Brainstorm  
> **Created**: 2025-02-25  
> **Scope**: `src/mycontext/templates/free/analysis/data_analyzer.py`

---

## 1. Problem Statement

The current Data Analyzer template produces a **single monolithic report** with all 11 sections. Users cannot:

- **Request only specific sections** (e.g., correlation analysis for a data scientist, key insights + visualizations for an executive)
- **Control output length** or depth per section
- **Align output with budget** (token cost) or intent
- **Get a summary vs. comprehensive** report without running the full pipeline

---

## 2. Current Report Structure (11 Sections)

From `data_analyzer_report.md`:

| # | Section | Purpose | Typical Consumer |
|---|---------|---------|------------------|
| 1 | DATA OVERVIEW | Type, scope, variables, quality | All |
| 2 | DESCRIPTIVE STATISTICS | Mean, median, dispersion, distribution | Analysts, Data Scientists |
| 3 | PATTERN DETECTION | Trends, seasonality, clusters | Analysts |
| 4 | ANOMALY DETECTION | Outliers, severity, causes | Operations, QA |
| 5 | CORRELATION ANALYSIS | Variable relationships | Data Scientists |
| 6 | COMPARATIVE ANALYSIS | Segment comparison table | Product/Business |
| 7 | KEY INSIGHTS | Top findings, evidence, actions | Executives |
| 8 | HYPOTHESES | Possible explanations, tests | Research, Strategy |
| 9 | DATA LIMITATIONS | Caveats, gaps | Risk, Compliance |
| 10 | RECOMMENDATIONS | Actions, next steps | Decision Makers |
| 11 | VISUALIZATION SUGGESTIONS | Charts, dashboards | BI, Designers |

---

## 3. Proposed Parameterization

### 3.1 Section Selection

**Parameter**: `sections` (list[str] | Literal["all"])

```python
sections: list[str] = [
    "data_overview",
    "descriptive_statistics",
    "pattern_detection",
    "anomaly_detection",
    "correlation_analysis",
    "comparative_analysis",
    "key_insights",
    "hypotheses",
    "data_limitations",
    "recommendations",
    "visualization_suggestions"
]
# Or sections="all" for comprehensive
```

### 3.2 Report Types (Presets)

| Report Type | Sections Included | Use Case |
|-------------|-------------------|----------|
| **summary** | `data_overview`, `key_insights`, `recommendations` | Executive briefing |
| **executive** | `data_overview`, `key_insights`, `visualization_suggestions`, `recommendations` | Decision-maker with visuals |
| **analytical** | `descriptive_statistics`, `pattern_detection`, `correlation_analysis` | Data scientist deep dive |
| **operations** | `data_overview`, `anomaly_detection`, `recommendations` | Ops/QA focus |
| **comprehensive** | `all` | Full report |

### 3.3 Output Controls

| Parameter | Type | Purpose |
|-----------|------|---------|
| `sections` | list[str] \| "all" | Which sections to include |
| `report_type` | str | Preset: summary, executive, analytical, operations, comprehensive |
| `max_insights` | int | Cap on key insights (e.g., 3 vs. 5) |
| `max_anomalies` | int | Limit anomalies reported |
| `depth` | "brief" \| "standard" \| "detailed" | Per-section verbosity |
| `format` | "markdown" \| "json" \| "bullet_points" | Output shape |

### 3.4 Example API

```python
# Executive wants key insights + visuals only
analyzer.execute(
    data_description="Q4 sales by region",
    goal="Growth opportunities",
    report_type="executive"
)

# Data scientist needs only correlation analysis
analyzer.execute(
    data_description="Q4 sales by region",
    goal="Variable relationships",
    sections=["correlation_analysis"]
)

# Budget-conscious: summary + max 3 insights
analyzer.execute(
    data_description="Q4 sales by region",
    goal="Quick takeaways",
    report_type="summary",
    max_insights=3,
    depth="brief"
)
```

---

## 4. LLM Restriction & Truncation Avoidance

**Goal**: LLM respects limits without mid-output truncation.

**Approach**:

1. **Dynamic directive**  
   Build the directive from only the requested sections. Do not include sections that are disabled.

2. **Explicit constraints in prompt**  
   Add clear instructions:
   - "Generate exactly N key insights, no more."
   - "Limit anomaly detection to the top M anomalies."
   - "Keep each section under X sentences for brief mode."

3. **Token budgeting (optional)**  
   - Estimate tokens per section
   - Pass `max_tokens` to the provider based on requested sections
   - Reduces truncation risk

4. **Section-level templating**  
   Each section has its own sub-template with length/depth instructions. Only the active sections are concatenated.

---

## 5. Pros & Cons

### Pros

| Benefit | Description |
|---------|-------------|
| **User control** | Users choose exactly what they need |
| **Cost efficiency** | Fewer sections → fewer tokens → lower cost |
| **Intent alignment** | Executive vs. analyst vs. ops get tailored output |
| **Faster responses** | Shorter prompts and outputs |
| **Better quality** | LLM can focus on fewer sections instead of diluting across 11 |
| **Reusability** | Same template serves multiple personas |
| **Testability** | Section-level A/B tests and quality metrics |
| **Chaining** | Run section A, then section B with different params |

### Cons

| Risk | Mitigation |
|------|------------|
| **Cross-section dependencies** | Some sections rely on others (e.g., insights from patterns). Add optional `require_context` sections that auto-include lightweight precursors. |
| **API complexity** | More params can confuse users. Mitigate with presets (`report_type`) and sensible defaults. |
| **Maintenance** | More moving parts. Mitigate with clear section registry and docstrings. |
| **Inconsistent ordering** | Order might matter (overview before insights). Define fixed section order and only filter by inclusion. |
| **Template sprawl** | Many sub-templates. Mitigate by keeping a single template with conditional section blocks. |

---

## 6. Implementation Plan

### Phase 1: Design & Schema

- [ ] Define section IDs and stable ordering
- [ ] Define `report_type` presets (mapping to section lists)
- [ ] Extend `input_schema` with `sections`, `report_type`, `depth`, `max_insights`, etc.

### Phase 2: Template Refactor

- [ ] Split `directive_template` into section blocks (dict or list)
- [ ] Add `_build_directive(sections)` that concatenates only requested sections
- [ ] Add depth-specific instructions per section (brief/standard/detailed)
- [ ] Add explicit limits (max_insights, max_anomalies) into prompt text

### Phase 3: API & Integration

- [ ] Update `build_context()` and `execute()` signatures
- [ ] Resolve `report_type` → `sections` when `sections` not provided
- [ ] Ensure backward compatibility: `sections="all"` or omit → current behavior

### Phase 4: Validation & Testing

- [ ] Unit tests: section filtering, preset resolution
- [ ] Quality tests: compare full vs. section-only output quality
- [ ] Token/cost comparison: summary vs. comprehensive
- [ ] Update notebooks and docs

### Phase 5: Optional Enhancements

- [ ] `max_tokens` estimation from selected sections
- [ ] `format` (markdown, json, bullet_points) handling
- [ ] Section-level `require_context` for dependencies

---

## 7. Dependency & Context Handling

Some sections benefit from prior sections:

| Section | Benefits from |
|---------|---------------|
| KEY INSIGHTS | Descriptive stats, patterns, anomalies |
| RECOMMENDATIONS | Key insights |
| HYPOTHESES | Patterns, anomalies |
| VISUALIZATION SUGGESTIONS | Patterns, comparative analysis |

**Options**:

1. **Strict**: Only requested sections. User accepts that insights may be thinner if patterns not requested.
2. **Auto-context**: Requesting `key_insights` without `pattern_detection` auto-adds a minimal `data_overview` + `pattern_detection` as context (possibly brief). Document this behavior.
3. **Explicit**: User must request dependencies. Keep it simple.

**Recommendation**: Start with **Strict** for clarity. Add auto-context in a later phase if users request it.

---

## 8. Open Questions

1. Should `report_type` override `sections`, or can they be combined? (e.g., `report_type="summary"` + `sections=["correlation_analysis"]` to add correlation to summary)
2. Should we support custom section combinations as user-defined presets?
3. Output format: keep markdown-only initially, or support JSON/bullets from day one?
4. Should `depth` apply globally or per-section? (e.g., brief insights but detailed correlation)

---

## 9. Success Metrics

- Users can request a single section (e.g., correlation) and get focused output
- Summary report is measurably shorter (tokens, chars) than comprehensive
- No increase in truncation rate when using section filters
- Quality (e.g., insight relevance) maintained or improved for focused runs
- Clear documentation and examples for each report type

---

## 10. Next Steps

1. **Review & prioritize** – Confirm which parameters to implement first
2. **Resolve open questions** – Especially `report_type` vs. `sections` interaction
3. **Prototype** – Implement Phase 1–2 in a branch
4. **Validate** – Run against existing data analyzer demos
5. **Document** – Update tutorials, API docs, and cognitive patterns
6. **Iterate** – Add format, auto-context, token budgeting as needed
