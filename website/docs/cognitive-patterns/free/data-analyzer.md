---
sidebar_position: 4
title: DataAnalyzer
description: Systematic data analysis with pattern detection, anomaly identification, correlation analysis, and ranked, actionable insights.
---

# DataAnalyzer

**Category:** Analysis | **Module:** `mycontext.templates.free.analysis`

Systematically analyzes data and extracts actionable insights. Provides descriptive statistics, trend detection, anomaly identification, correlation analysis, comparative segmentation, and prioritized recommendations — always with explicit evidence and confidence ratings.

## When to Use

- Business metrics analysis (revenue, engagement, retention)
- Product analytics review
- Sales data investigation
- Log data pattern analysis
- Any structured dataset where you need to go from numbers to decisions

## Quick Start

```python
from mycontext.templates.free.analysis import DataAnalyzer

analyzer = DataAnalyzer()

ctx = analyzer.build_context(
    data_description="Monthly sales data for past 12 months: Jan $120k, Feb $95k, Mar $140k, Apr $155k, May $148k, Jun $162k, Jul $108k, Aug $115k, Sep $178k, Oct $195k, Nov $210k, Dec $185k",
    goal="Identify growth patterns and seasonal trends",
)
result = ctx.execute(provider="openai")
print(result.response)
```

## Methods

### `build_context(data_description, goal="Extract insights", context=None)`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data_description` | `str` | `""` | Description of the data — can be raw numbers, summaries, or structured text |
| `goal` | `str` | `"Extract insights"` | What you're trying to learn from the data |
| `context` | `str \| None` | `None` | Additional context: data source, time period, known events |

### `execute(provider, data_description, goal="Extract insights", context=None, **kwargs)`

```python
result = analyzer.execute(
    provider="openai",
    data_description="""
    Q1: 1200 signups, 340 conversions (28%)
    Q2: 1500 signups, 375 conversions (25%)
    Q3: 1800 signups, 360 conversions (20%)
    Q4: 2100 signups, 315 conversions (15%)
    """,
    goal="Understand conversion rate decline despite signup growth",
    context="SaaS product, B2B, annual contract",
)
```

## Analysis Framework

The 11-section analysis covers:

1. **Data Overview** — Type, coverage, variables, quality assessment
2. **Descriptive Statistics** — Central tendency, dispersion, distribution shape
3. **Pattern Detection** — Trends (direction, magnitude, timeframe), seasonality cycles, clusters
4. **Anomaly Detection** — Outliers with context, severity, and possible causes
5. **Correlation Analysis** — Variable relationships with causation-vs-correlation distinction
6. **Comparative Analysis** — Segment comparison table with key differences
7. **Key Insights** — 3–5 ranked insights, each with evidence, confidence rating, and recommended action
8. **Hypotheses** — Explanations for detected patterns with tests
9. **Data Limitations** — Gaps, biases, and what cannot be concluded
10. **Recommendations** — Immediate actions + further investigation
11. **Visualization Suggestions** — Chart types optimized for each finding

## Confidence Ratings

Every insight includes an explicit confidence level:

| Confidence | Meaning |
|-----------|---------|
| `High` | Pattern is clear, data is sufficient, alternative explanations are unlikely |
| `Medium` | Pattern visible but data limitations exist or alternatives are plausible |
| `Low` | Suggestive but insufficient to conclude — needs more data |

## Examples

### SaaS Metrics Analysis

```python
result = analyzer.execute(
    provider="openai",
    data_description="""
    Monthly Active Users by segment over 6 months:
    Enterprise: 450, 462, 471, 480, 488, 494 
    SMB: 2100, 1980, 1870, 1750, 1640, 1530
    Startup: 890, 920, 960, 1010, 1080, 1160
    """,
    goal="Understand segment-level growth divergence",
)
```

### E-commerce Data

```python
result = analyzer.execute(
    provider="anthropic",
    data_description="Product category revenue data with 24 months history, customer acquisition cost by channel, and return rates by product line",
    goal="Identify highest ROI product categories and channels for budget allocation",
    context="Fashion e-commerce, $5M annual revenue, US market",
)
```

### Generic Prompt Mode

```python
# Zero-cost analysis prompt
prompt = analyzer.generic_prompt(
    data_description="Monthly churn rates: 2.1%, 2.3%, 2.0%, 2.8%, 3.2%, 3.1%",
    goal="Identify if churn is trending up",
)
```

## Output Format

Insights are structured for immediate action:

```
**Insight #1**: Conversion rate is declining despite signup growth
- Evidence: Q1 28% → Q4 15%, consistent 3-5% quarterly decline
- Confidence: High
- Significance: Revenue impact is 40% below what signup growth implies
- Action: Audit onboarding flow for friction introduced in Q2 redesign

**Insight #2**: SMB segment is churning systematically
- Evidence: 27% decline in MAU over 6 months (-95 users/month average)
- Confidence: High
- Significance: Represents $180k ARR at risk annually
- Action: Conduct exit interviews with churned SMB accounts
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(data_description, goal, context)` | `Context` | Assembled context |
| `execute(provider, data_description, goal, context, **kwargs)` | `ProviderResponse` | Execute analysis |
| `generic_prompt(data_description, context_section, goal)` | `str` | Zero-cost prompt string |
