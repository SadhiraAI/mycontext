---
sidebar_position: 4
title: DataAnalyzer
description: Systematic data analysis with 5 intents, 3 investment levels, pattern detection, anomaly identification, and ranked actionable insights.
---

# DataAnalyzer

**Category:** Analysis | **Module:** `mycontext.templates.free.analysis`

Systematically analyzes data and extracts actionable insights. Supports **5 intents** (executive, analyst, operations, summary, comprehensive) and **3 investment levels** (quick, standard, thorough) for fine-grained control over what sections are produced and how deep the analysis goes. Provides descriptive statistics, trend detection, anomaly identification, correlation analysis, comparative segmentation, and prioritized recommendations — always with explicit evidence and confidence ratings.

## When to Use

- Business metrics analysis (revenue, engagement, retention)
- Product analytics review
- Sales data investigation
- Operations and incident triage
- Log data pattern analysis
- Any structured dataset where you need to go from numbers to decisions

## Quick Start

```python
from mycontext.templates.free.analysis import DataAnalyzer

analyzer = DataAnalyzer()

# Full comprehensive analysis (default)
ctx = analyzer.build_context(
    data_description="Monthly sales data for past 12 months: Jan $120k, Feb $95k, Mar $140k, Apr $155k, May $148k, Jun $162k, Jul $108k, Aug $115k, Sep $178k, Oct $195k, Nov $210k, Dec $185k",
    goal="Identify growth patterns and seasonal trends",
)
result = ctx.execute(provider="openai")
print(result.response)

# Executive briefing — focused, fewer tokens
result = analyzer.execute(
    provider="openai",
    data_description="Monthly sales data...",
    goal="Key takeaways for leadership",
    intent="executive",
    investment="quick",
)
```

## Intents

The `intent` parameter controls *which* sections appear in the output:

| Intent | Sections | Best For |
|--------|:---:|---------|
| `executive` | 4 | C-level briefings — overview, insights, viz, recommendations |
| `analyst` | 4 | Data science — overview, statistics, patterns, correlations |
| `operations` | 3 | Ops triage — overview, anomaly detection, recommendations |
| `summary` | 3 | Quick decisions — overview, insights, recommendations |
| `comprehensive` | 11 | Full audit — all sections (default) |

## Investment Levels

The `investment` parameter controls *how deep* each section goes:

| Level | Token Budget | Behavior |
|-------|---:|---------|
| `quick` | ~1,500 | Concise bullet points, max 3 insights |
| `standard` | ~3,000 | Default depth, full section coverage |
| `thorough` | ~5,000 | Exhaustive analysis with detailed evidence chains |

Intent and investment compose freely — any of the **15 combinations** is valid.

## Methods

### `build_context(data_description, goal, context, intent, investment)`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data_description` | `str` | `""` | Description of the data — raw numbers, summaries, or structured text |
| `goal` | `str` | `"Extract insights"` | What you're trying to learn from the data |
| `context` | `str \| None` | `None` | Additional context: data source, time period, known events |
| `intent` | `str` | `"comprehensive"` | Report type: `executive` · `analyst` · `operations` · `summary` · `comprehensive` |
| `investment` | `str` | `"standard"` | Depth level: `quick` · `standard` · `thorough` |

### `execute(provider, data_description, goal, context, intent, investment, **kwargs)`

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
    intent="analyst",
    investment="thorough",
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

### Executive Briefing (quick)

```python
result = analyzer.execute(
    provider="openai",
    data_description="""
    Monthly Active Users by segment over 6 months:
    Enterprise: 450, 462, 471, 480, 488, 494 
    SMB: 2100, 1980, 1870, 1750, 1640, 1530
    Startup: 890, 920, 960, 1010, 1080, 1160
    """,
    goal="Segment health for board meeting",
    intent="executive",
    investment="quick",
)
```

### Analyst Deep-Dive (thorough)

```python
result = analyzer.execute(
    provider="openai",
    data_description="Product category revenue data with 24 months history, customer acquisition cost by channel, and return rates by product line",
    goal="Identify highest ROI product categories and channels for budget allocation",
    context="Fashion e-commerce, $5M annual revenue, US market",
    intent="analyst",
    investment="thorough",
)
```

### Operations Triage

```python
result = analyzer.execute(
    provider="openai",
    data_description="Server error rates past 24h: 0.1%, 0.2%, 0.1%, 0.8%, 2.1%, 4.5%, 3.2%",
    goal="Identify anomalies and immediate remediation steps",
    intent="operations",
    investment="standard",
)
```

### Generic Prompt Mode

```python
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

## Data Source Convenience Methods

Load data from common sources without manually building `data_description` strings.

### From a pandas DataFrame

```python
import pandas as pd

df = pd.read_csv("sales.csv")
ctx = analyzer.from_dataframe(df, goal="Growth drivers", intent="executive")
```

Auto-generates `data_description` from `df.info()`, `df.describe()`, null counts, and sample rows.

### From a CSV file path

```python
ctx = analyzer.from_csv_path("metrics.csv", goal="Trend analysis")
```

Reads the CSV into a DataFrame under the hood. Accepts any `pandas.read_csv()` keyword argument (`sep`, `encoding`, etc.).

### From JSON (API responses, configs)

```python
import requests

data = requests.get("https://api.example.com/metrics").json()
ctx = analyzer.from_json(data, goal="Spot anomalies", intent="operations")
```

Works with both `list[dict]` (array of records) and `dict` (single object). Infers keys, types, and includes a preview.

### From records (SQL results, ORMs)

```python
rows = cursor.fetchall()  # list of dicts from database
ctx = analyzer.from_records(rows, goal="Revenue trends", intent="analyst")

# Optionally filter columns
ctx = analyzer.from_records(rows, goal="...", columns=["name", "revenue", "region"])
```

Computes basic numeric statistics (min, max, mean) automatically and formats a sample table.

All convenience methods accept the same `goal`, `context`, `intent`, `investment`, and `output_format` parameters as `build_context()`.

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `build_context(data_description, goal, context, intent, investment)` | `Context` | Assembled context with parameterized sections |
| `execute(provider, data_description, goal, context, intent, investment, **kwargs)` | `ProviderResponse` | Execute analysis with auto token budget |
| `from_dataframe(df, goal, context, intent, investment)` | `Context` | Build context from pandas DataFrame |
| `from_csv_path(path, goal, context, intent, investment)` | `Context` | Build context from CSV file |
| `from_json(data, goal, context, intent, investment)` | `Context` | Build context from dict or list |
| `from_records(records, goal, context, intent, investment)` | `Context` | Build context from list of row-dicts |
| `generic_prompt(data_description, context_section, goal)` | `str` | Zero-cost prompt string |

| Class Attribute | Type | Description |
|----------------|------|-------------|
| `INTENTS` | `dict` | Maps intent names → section lists |
| `INVESTMENTS` | `dict` | Maps investment levels → constraints + token hints |
| `SECTION_BLOCKS` | `dict` | All 11 section templates |
