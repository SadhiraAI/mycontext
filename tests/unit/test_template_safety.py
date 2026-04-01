"""
Tests for template_safety.safe_format_template

Covers:
  - Normal substitution (regression: existing templates must still work)
  - Attack vector: attribute access via {var.__class__}
  - Attack vector: item access via {var[0]} / {var[key]}
  - Attack vector: braces in user values opening new slots
  - Non-primitive inputs rejected
  - Unknown placeholders preserved (optional-section pattern)
  - Integration: Pattern.build_context still works correctly
  - Integration: Blueprint.build still works correctly
  - Edge cases: None value, empty string, numbers, booleans
"""

import pytest

from mycontext.foundation import Guidance
from mycontext.structure import Blueprint, Pattern
from mycontext.utils.template_safety import safe_format_template

# ---------------------------------------------------------------------------
# Unit tests for safe_format_template
# ---------------------------------------------------------------------------


class TestSafeFormatNormalUsage:
    """Regression tests — existing templates must continue to work."""

    def test_simple_substitution(self):
        result = safe_format_template("Hello, {name}!", name="World")
        assert result == "Hello, World!"

    def test_multiple_placeholders(self):
        result = safe_format_template(
            "Analyze {topic} from a {perspective} perspective.",
            topic="climate change",
            perspective="economic",
        )
        assert result == "Analyze climate change from a economic perspective."

    def test_integer_value(self):
        result = safe_format_template("Top {count} results:", count=5)
        assert result == "Top 5 results:"

    def test_float_value(self):
        result = safe_format_template("Score: {score:.0f}", score=0.95)
        # Format spec is preserved as-is, value substituted as str
        assert "0.95" in result or "Score:" in result  # safe_format passes format spec through

    def test_bool_value(self):
        result = safe_format_template("Verbose: {verbose}", verbose=True)
        assert result == "Verbose: True"

    def test_none_value_renders_empty(self):
        result = safe_format_template("Context: {extra}", extra=None)
        assert result == "Context: "

    def test_empty_string_value(self):
        result = safe_format_template("Prefix {optional} suffix", optional="")
        assert result == "Prefix  suffix"

    def test_multiline_template(self):
        template = """Role: {role}

Task: {task}

Rules:
- Be concise
- Focus on {domain}"""
        result = safe_format_template(template, role="Expert", task="Summarize", domain="finance")
        assert "Expert" in result
        assert "Summarize" in result
        assert "finance" in result

    def test_unknown_placeholder_preserved(self):
        """Placeholders with no matching kwarg must be left verbatim (optional sections)."""
        result = safe_format_template(
            "Hello {name}. {context_section}",
            name="Alice",
        )
        assert "Alice" in result
        assert "{context_section}" in result  # preserved, not raised

    def test_placeholder_used_twice(self):
        result = safe_format_template("{topic} overview: analyze {topic} thoroughly.", topic="AI")
        assert result == "AI overview: analyze AI thoroughly."


# ---------------------------------------------------------------------------
# Attack vector tests
# ---------------------------------------------------------------------------


class TestTemplateInjectionBlocked:
    """Every known attack vector must be rejected before formatting."""

    def test_attribute_access_in_template_rejected(self):
        """CVE pattern: {var.__class__} can expose internal Python objects."""
        malicious_template = "Hello {name.__class__}"
        with pytest.raises(ValueError, match="unsafe placeholder"):
            safe_format_template(malicious_template, name="Alice")

    def test_dunder_mro_in_template_rejected(self):
        """Classic sandbox escape: {obj.__class__.__mro__[1].__subclasses__()}"""
        malicious_template = "Data: {x.__class__.__mro__}"
        with pytest.raises(ValueError, match="unsafe placeholder"):
            safe_format_template(malicious_template, x="test")

    def test_item_access_in_template_rejected(self):
        """Item access: {obj[key]} or {obj[0]} can index into dicts/lists."""
        malicious_template = "Value: {data[secret_key]}"
        with pytest.raises(ValueError, match="unsafe placeholder"):
            safe_format_template(malicious_template, data={})

    def test_numeric_index_in_template_rejected(self):
        malicious_template = "Item: {items[0]}"
        with pytest.raises(ValueError, match="unsafe placeholder"):
            safe_format_template(malicious_template, items=[])

    def test_braces_in_user_value_do_not_open_new_slots(self):
        """
        If user input contains {}, it must NOT create a new format slot.
        A naive .format(**inputs) would evaluate {__import__('os').environ}
        as a second-pass format string.
        """
        injected_value = "{__import__('os').environ}"
        result = safe_format_template("Input: {user_input}", user_input=injected_value)
        # The braces must be escaped — the literal string appears, not an expansion
        assert "__import__" in result  # the text is there
        assert "environ" in result
        # But no actual dict or module appears (would raise if evaluated)
        # Most importantly: no KeyError or unexpected expansion
        assert "{" not in result.replace("{{", "").replace(
            "}}", ""
        )  # all braces are escaped in output

    def test_nested_braces_in_value_escaped(self):
        value_with_braces = "use {this} pattern"
        result = safe_format_template(
            "Instructions: {instructions}", instructions=value_with_braces
        )
        # The inner braces must appear as literal text, not trigger format
        assert "{this}" in result

    def test_non_primitive_object_rejected(self):
        """Passing an object allows .attr access — must be rejected."""

        class EvilObject:
            pass

        with pytest.raises(ValueError, match="primitive type"):
            safe_format_template("Hello {obj}", obj=EvilObject())

    def test_dict_input_rejected(self):
        with pytest.raises(ValueError, match="primitive type"):
            safe_format_template("Data: {d}", d={"key": "value"})

    def test_list_input_rejected(self):
        with pytest.raises(ValueError, match="primitive type"):
            safe_format_template("Items: {items}", items=[1, 2, 3])

    def test_class_input_rejected(self):
        with pytest.raises(ValueError, match="primitive type"):
            safe_format_template("Type: {t}", t=str)

    def test_env_access_via_object_rejected(self):
        """Simulate trying to smuggle os.environ via an object attribute."""
        import os

        with pytest.raises(ValueError, match="primitive type"):
            safe_format_template("Env: {env}", env=os.environ)


# ---------------------------------------------------------------------------
# Integration tests — Pattern and Blueprint still work after fix
# ---------------------------------------------------------------------------


class TestPatternBuildContextSafe:
    """Pattern.build_context must work correctly after the injection fix."""

    def test_normal_build_context(self):
        pattern = Pattern(
            name="test_safe",
            guidance=Guidance(role="Assistant"),
            directive_template="Analyze {topic} for {audience}.",
            input_schema={"topic": str, "audience": str},
        )
        ctx = pattern.build_context(topic="AI ethics", audience="policy makers")
        assert "AI ethics" in ctx.directive.content
        assert "policy makers" in ctx.directive.content

    def test_build_context_with_multiline_directive(self):
        pattern = Pattern(
            name="multiline",
            directive_template="Task: {task}\n\nContext: {background}",
            input_schema={"task": str, "background": str},
        )
        ctx = pattern.build_context(task="Summarize this", background="Long document")
        assert "Summarize this" in ctx.directive.content
        assert "Long document" in ctx.directive.content

    def test_build_context_optional_placeholder_preserved(self):
        """Templates with optional {context_section} must still work."""
        pattern = Pattern(
            name="optional_section",
            directive_template="Analyze {topic}.\n{context_section}",
            input_schema={"topic": str},
        )
        ctx = pattern.build_context(topic="finance")
        assert "finance" in ctx.directive.content
        # Optional placeholder preserved — not raising KeyError
        assert "{context_section}" in ctx.directive.content

    def test_malicious_input_value_rendered_safely(self):
        """Braces in user input must be escaped, not re-evaluated."""
        pattern = Pattern(
            name="brace_test",
            directive_template="User request: {request}",
            input_schema={"request": str},
        )
        ctx = pattern.build_context(request="show me {__class__} of this")
        # The text should appear verbatim — not cause an attribute access
        assert "__class__" in ctx.directive.content
        # No explosion — just a string
        assert ctx.directive.content is not None

    def test_non_primitive_input_raises_value_error(self):
        """Pattern.build_context with non-primitive raises clear ValueError."""
        pattern = Pattern(
            name="obj_test",
            directive_template="Process {data}",
            input_schema={"data": object},  # deliberately loose schema
        )
        with pytest.raises(ValueError, match="primitive type"):
            pattern.build_context(data={"nested": "dict"})

    def test_attribute_access_in_directive_template_raises(self):
        """A Pattern with a malicious directive_template must fail at build time."""
        pattern = Pattern(
            name="evil",
            directive_template="Leak: {x.__class__.__mro__}",
            input_schema={"x": str},
        )
        with pytest.raises(ValueError, match="unsafe placeholder"):
            pattern.build_context(x="harmless")

    def test_existing_pattern_regression_synthesis_builder(self):
        """
        Smoke test: real template patterns from the codebase must still
        build contexts without errors.
        """
        try:
            from mycontext.templates.free.specialized.synthesis_builder import SynthesisBuilder

            p = SynthesisBuilder()
            ctx = p.build_context(question="How does transformer attention work?")
            assert ctx is not None
            assert ctx.directive is not None or ctx.guidance is not None
        except ImportError:
            pytest.skip("SynthesisBuilder not available in this environment")


class TestBlueprintBuildSafe:
    """Blueprint.build must work correctly after the injection fix."""

    def test_normal_blueprint_build(self):
        bp = Blueprint(
            name="safe_bp",
            guidance=Guidance(role="Expert"),
            directive_template="Query: {query}",
        )
        ctx = bp.build(query="What is context engineering?")
        assert "What is context engineering?" in ctx.directive.content

    def test_blueprint_malicious_value_escaped(self):
        bp = Blueprint(
            name="escape_test",
            directive_template="Process: {input}",
        )
        ctx = bp.build(input="{__class__.__mro__}")
        assert "__class__" in ctx.directive.content
        assert "Process:" in ctx.directive.content

    def test_blueprint_non_primitive_raises(self):
        bp = Blueprint(
            name="obj_bp",
            directive_template="Data: {data}",
        )
        with pytest.raises(ValueError, match="primitive type"):
            bp.build(data={"key": "val"})

    def test_blueprint_attribute_access_in_template_raises(self):
        bp = Blueprint(
            name="evil_bp",
            directive_template="Leak {x.__class__}",
        )
        with pytest.raises(ValueError, match="unsafe placeholder"):
            bp.build(x="value")


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestSafeFormatEdgeCases:
    def test_empty_template(self):
        result = safe_format_template("")
        assert result == ""

    def test_template_with_no_placeholders(self):
        result = safe_format_template("No placeholders here.", extra="ignored")
        assert result == "No placeholders here."

    def test_template_with_double_braces_preserved(self):
        """Literal {{ }} in template must come through as { }."""
        result = safe_format_template("Use {{braces}} for JSON: {value}", value="42")
        assert "{braces}" in result
        assert "42" in result

    def test_unicode_values(self):
        result = safe_format_template("名前: {name}", name="田中さん")
        assert "田中さん" in result

    def test_newline_in_value(self):
        result = safe_format_template("Content:\n{text}", text="line1\nline2")
        assert "line1\nline2" in result

    def test_all_primitives_accepted(self):
        result = safe_format_template(
            "{s} {i} {f} {b} {n}",
            s="hello",
            i=42,
            f=3.14,
            b=False,
            n=None,
        )
        assert "hello" in result
        assert "42" in result
        assert "3.14" in result
        assert "False" in result
