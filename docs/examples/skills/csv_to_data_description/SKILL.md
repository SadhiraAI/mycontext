---
name: CSV to Data Description
description: Given raw CSV content, produce a structured data description suitable for a downstream data analysis agent (e.g. DataAnalyzer). Uses the LLM to infer columns, types, and quality.
input_schema:
  csv_content: string
---

Produce a **structured data description** that another agent (e.g. a data analysis template) can use to analyze the dataset.

## Input
- **csv_content**: Raw CSV text (header + rows). If very long, describe structure and a representative sample; you may summarize the rest.

## Output
Write a concise data description that includes:

1. **Columns and types** – Column names and inferred types (e.g. date, categorical, numeric).
2. **Row count** – Number of rows (if visible or inferable).
3. **Sample / summary** – A few example rows or value ranges so the reader knows what the data looks like.
4. **Data quality notes** – Completeness, obvious issues (e.g. missing values, duplicates), or caveats.

Keep the description self-contained and under ~800 words so it fits as input to a downstream analysis step. Output only the description; no preamble like "Here is the description."

---

**CSV content to describe:**

{csv_content}