---
name: csv-file-reader
description: Read and load CSV files, inspect columns and rows. Use when the user has a CSV file or wants to load tabular data with pandas.
---
# CSV File Reading

## Quick start
Use the **pandas** library to read CSV files.

```python
import pandas as pd
df = pd.read_csv("path/to/file.csv")
# inspect
print(df.shape)
print(df.columns.tolist())
df.head()
```

## Instructions
- Identify the CSV path or URL the user provided.
- Use `pd.read_csv()` to load the file; set `encoding="utf-8"` (or the right encoding) and `sep=","` if needed.
- If the user asks for columns, shape, dtypes, or a preview, return those clearly.
- For large files, use `nrows` or `chunksize` to avoid loading everything at once.
