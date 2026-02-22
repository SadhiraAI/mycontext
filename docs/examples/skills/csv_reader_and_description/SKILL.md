---
name: csv-reader-and-description
description: Read a CSV file with pandas and produce a structured data description for the DataAnalyzer template. Combines csv_file_reader + csv_to_data_description into one skill.
input_schema:
  csv_content: string
---

# CSV Reader and Data Description

Read CSV with **pandas** and produce a **structured data description** for the **DataAnalyzer** template. One skill for both loading and description.

## Step 1: Load the CSV

If you have a path, use pandas:

```python
import pandas as pd
df = pd.read_csv(path, encoding="utf-8", sep=",")
```

If you have raw CSV content, use `pd.read_csv(io.StringIO(csv_content))`. For large files, use `nrows` or `chunksize`.

## Step 2: Build the data description

Use pandas to produce the description (no LLM needed when running code):

```python
import io
buf = io.StringIO()
df.info(buf=buf)
data_description = f"""Columns: {list(df.columns)}
Shape: {df.shape[0]} rows, {df.shape[1]} columns

Info:
{buf.getvalue()}

Describe:
{df.describe().to_string()}

Sample (first 5 rows):
{df.head().to_string()}
"""
```

## Output for DataAnalyzer

Return the data description. It must include:

1. **Columns and types** – Column names and dtypes (from `df.info()`).
2. **Shape** – Row and column counts.
3. **Describe** – Summary statistics (from `df.describe()`).
4. **Sample** – First 5 rows (from `df.head().to_string()`).

Keep the output self-contained so it can be passed directly to **DataAnalyzer** as the `data_description` argument. Output only the description; no preamble.

---

**CSV content:**

{csv_content}
