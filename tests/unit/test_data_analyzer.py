"""
Tests for DataAnalyzer template — core API and convenience constructors.
"""

import pytest

from mycontext.templates.free.analysis import DataAnalyzer


@pytest.fixture
def analyzer():
    return DataAnalyzer()


# ── Core API ─────────────────────────────────────────────────────────


class TestDataAnalyzerCore:
    def test_creation(self, analyzer):
        assert analyzer.name == "data_analyzer"
        assert analyzer.guidance is not None

    def test_build_context_default(self, analyzer):
        ctx = analyzer.build_context(
            data_description="Monthly sales: $100k, $120k, $110k",
            goal="Find trends",
        )
        assert ctx.directive is not None
        assert "Monthly sales" in ctx.directive.content
        assert ctx.metadata["intent"] == "comprehensive"
        assert ctx.metadata["investment"] == "standard"

    def test_build_context_executive(self, analyzer):
        ctx = analyzer.build_context(
            data_description="Revenue data",
            goal="Key takeaways",
            intent="executive",
            investment="quick",
        )
        assert ctx.metadata["intent"] == "executive"
        assert ctx.metadata["investment"] == "quick"
        assert "KEY INSIGHTS" in ctx.directive.content
        assert "DESCRIPTIVE STATISTICS" not in ctx.directive.content

    def test_build_context_analyst(self, analyzer):
        ctx = analyzer.build_context(
            data_description="Metrics data",
            goal="Correlations",
            intent="analyst",
        )
        assert "DESCRIPTIVE STATISTICS" in ctx.directive.content
        assert "CORRELATION ANALYSIS" in ctx.directive.content

    def test_build_context_operations(self, analyzer):
        ctx = analyzer.build_context(
            data_description="Error rates",
            goal="Anomalies",
            intent="operations",
        )
        assert "ANOMALY DETECTION" in ctx.directive.content
        assert "RECOMMENDATIONS" in ctx.directive.content

    def test_invalid_intent_raises(self, analyzer):
        with pytest.raises(ValueError, match="Invalid intent"):
            analyzer.build_context(data_description="data", goal="g", intent="invalid")

    def test_invalid_investment_raises(self, analyzer):
        with pytest.raises(ValueError, match="Invalid investment"):
            analyzer.build_context(data_description="data", goal="g", investment="extreme")

    def test_invalid_output_format_raises(self, analyzer):
        with pytest.raises(ValueError, match="Invalid output_format"):
            analyzer.build_context(data_description="data", goal="g", output_format="xml")

    def test_output_formats(self, analyzer):
        for fmt in ("structured", "narrative", "brief", "actionable", "json", "table"):
            ctx = analyzer.build_context(data_description="data", goal="g", output_format=fmt)
            assert ctx.metadata["output_format"] == fmt

    def test_generic_prompt(self, analyzer):
        prompt = analyzer.generic_prompt(
            data_description="Sales data",
            goal="Find trends",
        )
        assert "Sales data" in prompt
        assert "Find trends" in prompt
        assert len(prompt) > 200


# ── Convenience: from_dataframe ──────────────────────────────────────


class TestFromDataFrame:
    @pytest.fixture
    def sample_df(self):
        pd = pytest.importorskip("pandas")
        return pd.DataFrame(
            {
                "month": ["Jan", "Feb", "Mar", "Apr"],
                "revenue": [100, 120, 110, 150],
                "units": [10, 12, 11, 15],
                "region": ["North", "South", "North", "East"],
            }
        )

    def test_from_dataframe_returns_context(self, analyzer, sample_df):
        ctx = analyzer.from_dataframe(sample_df, goal="Revenue trends")
        assert ctx.directive is not None
        assert ctx.metadata["pattern"] == "data_analyzer"
        assert "revenue" in ctx.directive.content.lower()

    def test_from_dataframe_includes_shape(self, analyzer, sample_df):
        ctx = analyzer.from_dataframe(sample_df, goal="Test")
        content = ctx.directive.content
        assert "4 rows" in content
        assert "4 columns" in content

    def test_from_dataframe_includes_columns(self, analyzer, sample_df):
        ctx = analyzer.from_dataframe(sample_df, goal="Test")
        content = ctx.directive.content
        assert "month" in content
        assert "revenue" in content

    def test_from_dataframe_respects_intent(self, analyzer, sample_df):
        ctx = analyzer.from_dataframe(
            sample_df, goal="Quick look", intent="executive", investment="quick"
        )
        assert ctx.metadata["intent"] == "executive"
        assert "KEY INSIGHTS" in ctx.directive.content

    def test_from_dataframe_max_sample_rows(self, analyzer, sample_df):
        ctx = analyzer.from_dataframe(sample_df, goal="Test", max_sample_rows=2)
        assert ctx.directive is not None


# ── Convenience: from_json ───────────────────────────────────────────


class TestFromJson:
    def test_from_json_list_of_dicts(self, analyzer):
        data = [
            {"name": "Alice", "score": 95, "grade": "A"},
            {"name": "Bob", "score": 82, "grade": "B"},
            {"name": "Carol", "score": 78, "grade": "C"},
        ]
        ctx = analyzer.from_json(data, goal="Grade distribution")
        content = ctx.directive.content
        assert "3 records" in content
        assert "Alice" in content
        assert ctx.metadata["pattern"] == "data_analyzer"

    def test_from_json_dict(self, analyzer):
        data = {
            "total_users": 5000,
            "active_users": 3200,
            "churn_rate": 0.04,
            "regions": ["US", "EU", "APAC"],
        }
        ctx = analyzer.from_json(data, goal="User health metrics")
        content = ctx.directive.content
        assert "4 keys" in content
        assert "total_users" in content

    def test_from_json_respects_intent(self, analyzer):
        ctx = analyzer.from_json({"metric": 42}, goal="Test", intent="summary")
        assert ctx.metadata["intent"] == "summary"

    def test_from_json_empty_dict(self, analyzer):
        ctx = analyzer.from_json({}, goal="Test")
        assert ctx.directive is not None

    def test_from_json_empty_list(self, analyzer):
        ctx = analyzer.from_json([], goal="Test")
        content = ctx.directive.content
        assert "0 records" in content


# ── Convenience: from_records ────────────────────────────────────────


class TestFromRecords:
    def test_from_records_basic(self, analyzer):
        records = [
            {"id": 1, "name": "Widget A", "revenue": 1200, "units": 100},
            {"id": 2, "name": "Widget B", "revenue": 800, "units": 60},
            {"id": 3, "name": "Widget C", "revenue": 1500, "units": 130},
        ]
        ctx = analyzer.from_records(records, goal="Product performance")
        content = ctx.directive.content
        assert "3 rows" in content
        assert "Widget A" in content
        assert ctx.metadata["pattern"] == "data_analyzer"

    def test_from_records_numeric_summary(self, analyzer):
        records = [
            {"product": "A", "revenue": 100},
            {"product": "B", "revenue": 200},
            {"product": "C", "revenue": 300},
        ]
        ctx = analyzer.from_records(records, goal="Test")
        content = ctx.directive.content
        assert "min=" in content
        assert "max=" in content
        assert "mean=" in content

    def test_from_records_custom_columns(self, analyzer):
        records = [
            {"id": 1, "name": "A", "secret": "xxx", "revenue": 100},
            {"id": 2, "name": "B", "secret": "yyy", "revenue": 200},
        ]
        ctx = analyzer.from_records(records, goal="Test", columns=["name", "revenue"])
        content = ctx.directive.content
        assert "name" in content
        assert "revenue" in content

    def test_from_records_empty_raises(self, analyzer):
        with pytest.raises(ValueError, match="non-empty"):
            analyzer.from_records([], goal="Test")

    def test_from_records_respects_intent(self, analyzer):
        records = [{"x": 1}, {"x": 2}]
        ctx = analyzer.from_records(
            records, goal="Test", intent="operations", investment="thorough"
        )
        assert ctx.metadata["intent"] == "operations"
        assert ctx.metadata["investment"] == "thorough"


# ── Convenience: from_csv_path ───────────────────────────────────────


class TestFromCsvPath:
    def test_from_csv_path(self, analyzer, tmp_path):
        pd = pytest.importorskip("pandas")
        csv_file = tmp_path / "test_data.csv"
        csv_file.write_text("month,revenue,units\nJan,100,10\nFeb,120,12\nMar,110,11\n")
        ctx = analyzer.from_csv_path(str(csv_file), goal="Trend analysis")
        content = ctx.directive.content
        assert "3 rows" in content
        assert "revenue" in content
        assert ctx.metadata["pattern"] == "data_analyzer"

    def test_from_csv_path_nonexistent_raises(self, analyzer):
        with pytest.raises(Exception):
            analyzer.from_csv_path("nonexistent_file.csv", goal="Test")
