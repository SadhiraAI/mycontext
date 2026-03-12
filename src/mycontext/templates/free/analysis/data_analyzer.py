"""
Data Analyzer - Systematic data analysis and insight extraction

Comprehensive data analysis with pattern detection and insights.
Supports intent-based parameterization (executive, analyst, operations,
summary, comprehensive) and investment levels (quick, standard, thorough).

Convenience constructors (``from_dataframe``, ``from_json``,
``from_records``) auto-build ``data_description`` from common data sources
so users don't have to manually serialize their data.

Based on data science and analytical reasoning frameworks.
"""

from __future__ import annotations

import io
from typing import Any

from mycontext.foundation import Constraints, Directive, Guidance
from mycontext.structure import Pattern
from mycontext.utils.format_directives import VALID_OUTPUT_FORMATS, get_format_directive

VALID_INTENTS: frozenset[str] = frozenset(
    {"executive", "analyst", "operations", "summary", "comprehensive"}
)
VALID_INVESTMENTS: frozenset[str] = frozenset({"quick", "standard", "thorough"})


class DataAnalyzer(Pattern):
    """
    Analyze data systematically and extract insights.

    Supports two new parameters:

    * **intent** — controls *which* sections are produced:
      ``"executive"`` | ``"analyst"`` | ``"operations"`` | ``"summary"``
      | ``"comprehensive"`` (default, all 11 sections).

    * **investment** — controls *depth / token budget*:
      ``"quick"`` | ``"standard"`` (default) | ``"thorough"``.

    Backward compatible: omitting both gives the original full report.

    Example:
        >>> analyzer = DataAnalyzer()
        >>> # Full report (original behaviour)
        >>> ctx = analyzer.build_context(
        ...     data_description="Monthly sales data",
        ...     goal="Identify growth opportunities",
        ... )
        >>>
        >>> # Executive summary
        >>> ctx = analyzer.build_context(
        ...     data_description="Monthly sales data",
        ...     goal="Key takeaways for leadership",
        ...     intent="executive",
        ...     investment="quick",
        ... )
        >>>
        >>> # Analyst deep-dive on correlations
        >>> result = analyzer.execute(
        ...     data_description="Monthly sales data",
        ...     goal="Variable relationships",
        ...     intent="analyst",
        ...     investment="thorough",
        ... )

    Free Template - Part of mycontext open source edition.
    """

    GENERIC_PROMPT = (
        "Analyze the following data and extract actionable insights.\n\n"
        "Data: {data_description}\n"
        "{context_section}\n"
        "Goal: {goal}\n\n"
        "Provide a thorough analysis covering patterns, anomalies, and key findings. "
        "Summarize what the data shows, highlight the most significant insights, and "
        "recommend concrete next steps. Be evidence-based and actionable."
    )

    def __init__(self):
        super().__init__(
            name="data_analyzer",
            description="Systematic data analysis",
            guidance=Guidance(
                role="Expert Data Analyst and Insights Specialist",
                rules=[
                    "Start with descriptive understanding",
                    "Look for patterns and anomalies",
                    "Distinguish correlation from causation",
                    "Provide actionable insights",
                    "Acknowledge data limitations",
                ],
                style="analytical, evidence-based, clear",
            ),
            input_schema={
                "data_description": str,
                "context_section": str,
                "goal": str,
            },
            constraints=Constraints(
                must_include=["patterns", "insights", "recommendations"],
                style_guide="Be analytical but accessible, rigorous but clear",
            ),
        )

    # ------------------------------------------------------------------
    # Private scaffold — assembled at runtime, never exposed as attributes
    # ------------------------------------------------------------------

    @staticmethod
    def _section_blocks() -> dict[str, str]:
        return {
            "data_overview": (
                "1. **DATA OVERVIEW**\n"
                "   - Data type: [What kind of data]\n"
                "   - Time period: [Coverage]\n"
                "   - Sample size: [How much data]\n"
                "   - Variables: [What's measured]\n"
                "   - Quality: [Completeness, accuracy]"
            ),
            "descriptive_statistics": (
                "2. **DESCRIPTIVE STATISTICS**\n"
                "   Summary statistics:\n"
                "   - Central tendency: [Mean, median, mode — if mean and median diverge "
                "significantly, state the skew direction and which metric better represents "
                "the typical value for this distribution]\n"
                "   - Dispersion: [Range, variance, std dev]\n"
                "   - Distribution: [Shape, skewness]\n"
                "   - Key figures: [Notable numbers]"
            ),
            "pattern_detection": (
                "3. **PATTERN DETECTION**\n"
                "   \n"
                "   **Trends**:\n"
                "   - Trend 1: [Upward/downward/stable]\n"
                "     - Evidence: [What shows this]\n"
                "     - Magnitude: [How strong]\n"
                "     - Timeframe: [Since when]\n"
                "   \n"
                "   **Seasonality**:\n"
                "   - Pattern: [Recurring cycles]\n"
                "   - Frequency: [How often repeats]\n"
                "   - Amplitude: [How much variation]\n"
                "   \n"
                "   **Clusters**:\n"
                "   - Group 1: [Similar data points]\n"
                "   - Group 2: [Another cluster]\n"
                "   - Characteristics: [What defines each]"
            ),
            "anomaly_detection": (
                "4. **ANOMALY DETECTION**\n"
                "   Outliers and unusual patterns:\n"
                "   \n"
                "   - Anomaly 1: [What's unusual]\n"
                "     - Context: [When/where]\n"
                "     - Severity: [How far from normal]\n"
                "     - Possible cause: [Why it might occur]\n"
                "   \n"
                "   - Anomaly 2: [Another outlier]\n"
                "     - [Same structure]"
            ),
            "correlation_analysis": (
                "5. **CORRELATION ANALYSIS**\n"
                "   Relationships between variables:\n"
                "   \n"
                "   - Correlation 1: [X relates to Y]\n"
                "     - Strength: [Strong/moderate/weak]\n"
                "     - Direction: [Positive/negative]\n"
                "     - Note: [Correlation \u2260 causation]\n"
                "   \n"
                "   - Correlation 2: [Another relationship]"
            ),
            "comparative_analysis": (
                "6. **COMPARATIVE ANALYSIS**\n"
                "   How do segments compare?\n"
                "   \n"
                "   | Segment | Metric A | Metric B | Insight |\n"
                "   |---------|----------|----------|--------|\n"
                "   | Seg 1 | [Value] | [Value] | [Finding] |\n"
                "   | Seg 2 | [Value] | [Value] | [Finding] |\n"
                "   \n"
                "   Key differences:\n"
                "   - [Segment X outperforms on Y]\n"
                "   - [Segment A lags in B]"
            ),
            "key_insights": (
                "7. **KEY INSIGHTS**\n"
                "   \n"
                "   **Insight #1**: [Major finding]\n"
                "   - Evidence: [What supports this]\n"
                "   - Confidence: [High/Medium/Low]\n"
                "   - Significance: [Why it matters]\n"
                "   - Action: [What to do about it]\n"
                "   \n"
                "   **Insight #2**: [Another finding]\n"
                "   - Evidence: [Supporting data]\n"
                "   - Confidence: [Level]\n"
                "   - Significance: [Impact]\n"
                "   - Action: [Recommended response]\n"
                "   \n"
                "   **Insight #3**: [Third finding]\n"
                "   - [Same structure]"
            ),
            "hypotheses": (
                "8. **HYPOTHESES**\n"
                "   Possible explanations:\n"
                "   \n"
                "   - Hypothesis 1: [Explanation for pattern]\n"
                "     - Supporting evidence: [What fits]\n"
                "     - Contradicting evidence: [What doesn't]\n"
                "     - Test: [How to verify]\n"
                "   \n"
                "   - Hypothesis 2: [Alternative explanation]"
            ),
            "data_limitations": (
                "9. **DATA LIMITATIONS**\n"
                "   What to be cautious about:\n"
                "   - Limitation 1: [Data gap or issue]\n"
                "   - Limitation 2: [Bias or constraint]\n"
                "   - Limitation 3: [Missing information]\n"
                "   \n"
                "   Confidence caveats:\n"
                "   - [What we can't conclude from this data]"
            ),
            "recommendations": (
                "10. **RECOMMENDATIONS**\n"
                "    Based on analysis:\n"
                "    \n"
                "    **Immediate Actions**:\n"
                "    1. [Action based on insight 1]\n"
                "    2. [Action based on insight 2]\n"
                "    \n"
                "    **Further Investigation**:\n"
                "    - [What additional data needed]\n"
                "    - [What analysis to run next]\n"
                "    \n"
                "    **Success Metrics**:\n"
                "    - [How to measure if actions work]"
            ),
            "visualization_suggestions": (
                "11. **VISUALIZATION SUGGESTIONS**\n"
                "    Best ways to present findings — match chart type to data structure:\n"
                "    line/area charts for time-series trends; bar/column charts for category "
                "comparison; scatter plots for correlations; histograms or box plots for "
                "distributions; heatmaps for multi-variable relationships.\n"
                "    - Chart 1: [Type] for [Data] — [Why this chart fits this pattern]\n"
                "    - Chart 2: [Type] for [Pattern] — [Why this chart fits this pattern]\n"
                "    - Dashboard: [Key metrics to track]"
            ),
        }

    @staticmethod
    def _intent_sections() -> dict[str, list[str] | None]:
        return {
            "executive": [
                "data_overview", "key_insights",
                "visualization_suggestions", "recommendations",
            ],
            "analyst": [
                "data_overview", "descriptive_statistics",
                "pattern_detection", "correlation_analysis", "hypotheses",
            ],
            "operations": [
                "data_overview", "anomaly_detection", "recommendations",
            ],
            "summary": [
                "data_overview", "key_insights", "recommendations",
            ],
            "comprehensive": None,
        }

    @staticmethod
    def _investment_config() -> dict[str, dict[str, Any]]:
        return {
            "quick": {
                "constraint": (
                    "Be concise. Maximum 3 key insights. Use brief bullet points. "
                    "Omit lengthy elaboration."
                ),
                "max_tokens_hint": 1500,
            },
            "standard": {
                "constraint": "",
                "max_tokens_hint": 3000,
            },
            "thorough": {
                "constraint": (
                    "Be comprehensive. Include full evidence, detailed reasoning, "
                    "and thorough analysis for every section."
                ),
                "max_tokens_hint": 5000,
            },
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _render_context_section(context: str | None) -> str:
        if context:
            return f"\n**CONTEXT**: {context}\n"
        return ""

    @classmethod
    def _build_intent_directive(
        cls,
        data_description: str,
        goal: str,
        context_section: str,
        intent: str,
        investment: str,
        output_format: str = "structured",
    ) -> str:
        """Assemble a directive at runtime — scaffold never stored as a class attribute."""
        blocks_map = cls._section_blocks()
        all_ids = list(blocks_map.keys())
        intent_map = cls._intent_sections()
        inv_cfg = cls._investment_config()

        section_ids = intent_map.get(intent) or all_ids
        blocks = [blocks_map[sid] for sid in section_ids]
        body = "\n\n".join(blocks)

        inv = inv_cfg.get(investment, inv_cfg["standard"])
        constraint_line = ""
        if inv["constraint"]:
            constraint_line = f"\n**CONSTRAINTS**: {inv['constraint']}"

        fmt_directive = get_format_directive(output_format)

        return (
            f"Analyze this data:\n\n"
            f"**DATA**: {data_description}\n\n"
            f"{context_section}\n\n"
            f"**ANALYSIS GOAL**: {goal}\n\n"
            f"Produce ONLY these sections (in order):\n\n"
            f"{body}"
            f"{constraint_line}"
            f"{fmt_directive}"
        )

    @staticmethod
    def _validate_intent_investment(intent: str, investment: str) -> None:
        if intent not in VALID_INTENTS:
            raise ValueError(
                f"Invalid intent {intent!r}. Choose from: {sorted(VALID_INTENTS)}"
            )
        if investment not in VALID_INVESTMENTS:
            raise ValueError(
                f"Invalid investment {investment!r}. Choose from: {sorted(VALID_INVESTMENTS)}"
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_context(
        self,
        data_description: str = "",
        goal: str = "Extract insights",
        context: str | None = None,
        intent: str = "comprehensive",
        investment: str = "standard",
        output_format: str = "structured",
        **kwargs,
    ):
        """Build a Context for this analysis.

        Parameters
        ----------
        data_description : str
            Description of the data to analyze.
        goal : str
            What the analysis should achieve.
        context : str, optional
            Extra context (domain knowledge, constraints, etc.).
        intent : str
            Report type: ``"executive"`` | ``"analyst"`` | ``"operations"``
            | ``"summary"`` | ``"comprehensive"`` (default).
        investment : str
            Depth level: ``"quick"`` | ``"standard"`` (default) | ``"thorough"``.
        output_format : str
            How to present results: ``"structured"`` (default) | ``"narrative"``
            | ``"brief"`` | ``"actionable"`` | ``"json"`` | ``"table"``.
        """
        self._validate_intent_investment(intent, investment)
        if output_format not in VALID_OUTPUT_FORMATS:
            raise ValueError(
                f"Invalid output_format {output_format!r}. "
                f"Choose from: {sorted(VALID_OUTPUT_FORMATS)}"
            )
        context_section = self._render_context_section(context)

        from mycontext.core import Context

        directive_content = self._build_intent_directive(
            data_description, goal, context_section, intent, investment, output_format,
        )

        inv_cfg = self._investment_config()
        inv = inv_cfg.get(investment, inv_cfg["standard"])
        if inv["constraint"]:
            constraints = Constraints(
                must_include=["insights"],
                style_guide=inv["constraint"],
            )
        else:
            constraints = self.constraints

        ctx = Context(
            guidance=self.guidance,
            directive=Directive(content=directive_content),
            constraints=constraints,
            data={
                "data_description": data_description,
                "goal": goal,
                "context_section": context_section,
            },
        )
        ctx.metadata["pattern"] = self.name
        ctx.metadata["pattern_version"] = self.version
        ctx.metadata["intent"] = intent
        ctx.metadata["investment"] = investment
        ctx.metadata["output_format"] = output_format
        return ctx

    def execute(
        self,
        provider: str = "openai",
        data_description: str = "",
        goal: str = "Extract insights",
        context: str | None = None,
        intent: str = "comprehensive",
        investment: str = "standard",
        output_format: str = "structured",
        **kwargs,
    ):
        """Execute the analysis and return provider response.

        Accepts the same parameters as :meth:`build_context` plus
        provider kwargs (``model``, ``temperature``, ``max_tokens``, etc.).
        The ``output_format`` parameter controls how results are presented:
        ``"structured"`` (default) | ``"narrative"`` | ``"brief"``
        | ``"actionable"`` | ``"json"`` | ``"table"``.
        """
        self._validate_intent_investment(intent, investment)

        provider_params = {
            "model", "temperature", "max_tokens", "top_p",
            "frequency_penalty", "presence_penalty", "stop",
            "user", "api_key", "base_url",
        }
        provider_kwargs = {k: v for k, v in kwargs.items() if k in provider_params}
        template_kwargs = {k: v for k, v in kwargs.items() if k not in provider_params}

        if "max_tokens" not in provider_kwargs:
            inv_cfg = self._investment_config()
            hint = inv_cfg.get(investment, {}).get("max_tokens_hint")
            if hint and intent != "comprehensive":
                provider_kwargs["max_tokens"] = hint

        ctx = self.build_context(
            data_description=data_description,
            goal=goal,
            context=context,
            intent=intent,
            investment=investment,
            output_format=output_format,
            **template_kwargs,
        )
        return ctx.execute(provider=provider, **provider_kwargs)

    # ------------------------------------------------------------------
    # Convenience constructors — auto-build data_description from sources
    # ------------------------------------------------------------------

    @staticmethod
    def _describe_dataframe(df: Any, *, max_sample_rows: int = 5) -> str:
        """Build a structured data description from a pandas DataFrame.

        Works with any object that exposes the pandas DataFrame API
        (``columns``, ``shape``, ``dtypes``, ``describe``, ``head``,
        ``info``).  Pandas is NOT required at import time — only when
        this method is actually called.
        """
        buf = io.StringIO()
        df.info(buf=buf)
        info_str = buf.getvalue()

        describe_str = df.describe(include="all").to_string()
        sample_str = df.head(max_sample_rows).to_string()
        null_counts = df.isnull().sum()
        nulls_str = null_counts[null_counts > 0].to_string() or "None"

        return (
            f"Columns: {list(df.columns)}\n"
            f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
            f"Dtypes: {dict(df.dtypes)}\n\n"
            f"Info:\n{info_str}\n"
            f"Descriptive statistics:\n{describe_str}\n\n"
            f"Missing values:\n{nulls_str}\n\n"
            f"Sample (first {min(max_sample_rows, len(df))} rows):\n{sample_str}"
        )

    def from_dataframe(
        self,
        df: Any,
        goal: str = "Extract insights",
        context: str | None = None,
        intent: str = "comprehensive",
        investment: str = "standard",
        output_format: str = "structured",
        *,
        max_sample_rows: int = 5,
    ):
        """Build a Context directly from a pandas DataFrame.

        Automatically generates ``data_description`` from the DataFrame's
        schema, statistics, null counts, and a sample of rows.

        Parameters
        ----------
        df : pandas.DataFrame
            The data to analyze. Pandas must be installed.
        goal : str
            What the analysis should achieve.
        context : str, optional
            Extra domain knowledge or constraints.
        intent : str
            Report type (see :meth:`build_context`).
        investment : str
            Depth level (see :meth:`build_context`).
        output_format : str
            Presentation format (see :meth:`build_context`).
        max_sample_rows : int
            How many sample rows to include in the description (default 5).

        Returns
        -------
        Context
            Ready to ``.assemble()`` or ``.execute()``.

        Example
        -------
        >>> import pandas as pd
        >>> df = pd.read_csv("sales.csv")
        >>> ctx = DataAnalyzer().from_dataframe(df, goal="Identify growth drivers")
        """
        desc = self._describe_dataframe(df, max_sample_rows=max_sample_rows)
        return self.build_context(
            data_description=desc,
            goal=goal,
            context=context,
            intent=intent,
            investment=investment,
            output_format=output_format,
        )

    def from_json(
        self,
        data: dict | list,
        goal: str = "Extract insights",
        context: str | None = None,
        intent: str = "comprehensive",
        investment: str = "standard",
        output_format: str = "structured",
    ):
        """Build a Context from a JSON-serializable dict or list.

        Automatically generates ``data_description`` by inspecting the
        structure, keys, types, and a sample of the data.  Ideal for API
        responses, configuration dumps, or any JSON payload.

        Parameters
        ----------
        data : dict | list
            JSON-serializable data.  If a list of dicts, the first few
            items are used as a sample and keys are inferred.
        goal : str
            What the analysis should achieve.
        context : str, optional
            Extra domain knowledge or constraints.
        intent : str
            Report type (see :meth:`build_context`).
        investment : str
            Depth level (see :meth:`build_context`).
        output_format : str
            Presentation format (see :meth:`build_context`).

        Returns
        -------
        Context

        Example
        -------
        >>> response = requests.get("https://api.example.com/metrics").json()
        >>> ctx = DataAnalyzer().from_json(response, goal="Spot anomalies")
        """
        desc = self._describe_json(data)
        return self.build_context(
            data_description=desc,
            goal=goal,
            context=context,
            intent=intent,
            investment=investment,
            output_format=output_format,
        )

    @staticmethod
    def _describe_json(data: dict | list, *, max_sample: int = 5) -> str:
        """Build a structured data description from a JSON object."""
        import json

        if isinstance(data, list):
            n = len(data)
            sample = data[:max_sample]
            keys = sorted({k for item in sample if isinstance(item, dict) for k in item})
            types = {}
            for k in keys:
                vals = [item.get(k) for item in sample if isinstance(item, dict) and k in item]
                types[k] = type(vals[0]).__name__ if vals else "unknown"
            sample_str = json.dumps(sample, indent=2, default=str)
            return (
                f"Type: list of {n} records\n"
                f"Keys: {keys}\n"
                f"Field types (inferred from sample): {types}\n\n"
                f"Sample ({min(max_sample, n)} items):\n{sample_str}"
            )
        elif isinstance(data, dict):
            keys = list(data.keys())
            types = {k: type(v).__name__ for k, v in data.items()}
            truncated = {}
            for k, v in data.items():
                if isinstance(v, (list, dict)):
                    truncated[k] = f"<{type(v).__name__} with {len(v)} items>"
                elif isinstance(v, str) and len(v) > 200:
                    truncated[k] = v[:200] + "..."
                else:
                    truncated[k] = v
            preview = json.dumps(truncated, indent=2, default=str)
            return (
                f"Type: dict with {len(keys)} keys\n"
                f"Keys: {keys}\n"
                f"Field types: {types}\n\n"
                f"Preview:\n{preview}"
            )
        else:
            return f"Type: {type(data).__name__}\nValue: {str(data)[:2000]}"

    def from_records(
        self,
        records: list[dict],
        goal: str = "Extract insights",
        context: str | None = None,
        intent: str = "comprehensive",
        investment: str = "standard",
        output_format: str = "structured",
        *,
        columns: list[str] | None = None,
    ):
        """Build a Context from a list of row-dicts (SQL results, ORMs, etc.).

        This is the go-to constructor for database query results, ORM
        dumps, or any ``list[dict]`` where each dict is one row.

        Parameters
        ----------
        records : list[dict]
            Row dictionaries.  All dicts should share the same keys.
        goal : str
            What the analysis should achieve.
        context : str, optional
            Extra domain knowledge or constraints.
        intent : str
            Report type (see :meth:`build_context`).
        investment : str
            Depth level (see :meth:`build_context`).
        output_format : str
            Presentation format (see :meth:`build_context`).
        columns : list[str], optional
            Column names to include.  If ``None``, all keys from the
            first record are used.

        Returns
        -------
        Context

        Example
        -------
        >>> rows = cursor.fetchall()  # list of dicts from DB
        >>> ctx = DataAnalyzer().from_records(rows, goal="Revenue trends")
        """
        if not records:
            raise ValueError("records must be a non-empty list of dicts")

        cols = columns or sorted(records[0].keys())
        n = len(records)
        sample = records[:5]

        # Build a simple table representation
        header = " | ".join(cols)
        sep = " | ".join(["---"] * len(cols))
        rows_str = "\n".join(
            " | ".join(str(row.get(c, "")) for c in cols)
            for row in sample
        )

        # Infer types from first record
        types = {}
        for c in cols:
            val = records[0].get(c)
            types[c] = type(val).__name__ if val is not None else "unknown"

        # Compute basic numeric stats if possible
        numeric_summary = []
        for c in cols:
            vals = [r.get(c) for r in records if isinstance(r.get(c), (int, float))]
            if vals and len(vals) >= 3:
                numeric_summary.append(
                    f"  {c}: min={min(vals)}, max={max(vals)}, "
                    f"mean={sum(vals)/len(vals):.2f}, count={len(vals)}"
                )

        stats_block = ""
        if numeric_summary:
            stats_block = "\nNumeric summary:\n" + "\n".join(numeric_summary) + "\n"

        desc = (
            f"Records: {n} rows, {len(cols)} columns\n"
            f"Columns: {cols}\n"
            f"Column types (inferred): {types}\n"
            f"{stats_block}\n"
            f"Sample ({min(5, n)} rows):\n"
            f"{header}\n{sep}\n{rows_str}"
        )

        return self.build_context(
            data_description=desc,
            goal=goal,
            context=context,
            intent=intent,
            investment=investment,
            output_format=output_format,
        )

    def from_csv_path(
        self,
        path: str,
        goal: str = "Extract insights",
        context: str | None = None,
        intent: str = "comprehensive",
        investment: str = "standard",
        output_format: str = "structured",
        *,
        max_sample_rows: int = 5,
        **read_csv_kwargs,
    ):
        """Build a Context by loading a CSV file directly.

        Reads the CSV into a pandas DataFrame and delegates to
        :meth:`from_dataframe`.  Accepts any keyword arguments that
        ``pandas.read_csv`` supports (``sep``, ``encoding``, etc.).

        Parameters
        ----------
        path : str
            Path to the CSV file.
        goal : str
            What the analysis should achieve.
        context : str, optional
            Extra domain knowledge or constraints.
        intent : str
            Report type (see :meth:`build_context`).
        investment : str
            Depth level (see :meth:`build_context`).
        output_format : str
            Presentation format (see :meth:`build_context`).
        max_sample_rows : int
            How many sample rows to include (default 5).
        **read_csv_kwargs
            Passed through to ``pandas.read_csv()``.

        Returns
        -------
        Context

        Example
        -------
        >>> ctx = DataAnalyzer().from_csv_path("sales.csv", goal="Growth drivers")
        """
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "pandas is required for from_csv_path(). "
                "Install it with: pip install pandas"
            ) from exc

        df = pd.read_csv(path, **read_csv_kwargs)
        return self.from_dataframe(
            df,
            goal=goal,
            context=context,
            intent=intent,
            investment=investment,
            output_format=output_format,
            max_sample_rows=max_sample_rows,
        )
