"""
Tests for enterprise gating, license activation, and SDK license management.

Covers:
- SDK pattern_suggester gating (include_enterprise=True/False)
- SDK license module (activate / deactivate / is_enterprise_active)
- License key model validation
- Enterprise template access control logic
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from mycontext.intelligence.pattern_catalog import FULL_PATTERN_CATALOG
from mycontext.intelligence.pattern_suggester import (
    ENTERPRISE_LICENSE_NOTE,
    get_pattern_class,
    suggest_patterns,
)
from mycontext.license import (
    activate_license,
    deactivate_license,
    is_enterprise_active,
)


class TestPatternSuggesterGating:
    """Test that enterprise patterns are gated correctly by include_enterprise flag."""

    def _enterprise_names(self):
        return [name for name, cat, _ in FULL_PATTERN_CATALOG if cat == "enterprise"]

    def _free_names(self):
        return [name for name, cat, _ in FULL_PATTERN_CATALOG if cat == "free"]

    def test_catalog_has_enterprise_and_free(self):
        ent = self._enterprise_names()
        free = self._free_names()
        assert len(ent) > 0, "Should have enterprise patterns"
        assert len(free) > 0, "Should have free patterns"
        assert len(ent) + len(free) == len(FULL_PATTERN_CATALOG)

    def test_get_pattern_class_enterprise_allowed(self):
        ent_names = self._enterprise_names()
        if not ent_names:
            pytest.skip("No enterprise patterns in catalog")
        cls = get_pattern_class(ent_names[0], include_enterprise=True)
        assert cls is not None, "Enterprise pattern should be returned when include_enterprise=True"

    def test_get_pattern_class_enterprise_blocked(self):
        ent_names = self._enterprise_names()
        if not ent_names:
            pytest.skip("No enterprise patterns in catalog")
        cls = get_pattern_class(ent_names[0], include_enterprise=False)
        assert cls is None, "Enterprise pattern should be None when include_enterprise=False"

    def test_get_pattern_class_free_always_works(self):
        free_names = self._free_names()
        if not free_names:
            pytest.skip("No free patterns in catalog")
        cls_on = get_pattern_class(free_names[0], include_enterprise=True)
        cls_off = get_pattern_class(free_names[0], include_enterprise=False)
        assert cls_on is not None
        assert cls_off is not None

    def test_suggest_patterns_shows_license_note_when_blocked(self):
        result = suggest_patterns(
            "Help me make an ethical decision about AI usage",
            include_enterprise=False,
            max_patterns=10,
        )
        ent_suggestions = [
            s for s in result.suggested_patterns if s.category == "enterprise"
        ]
        for s in ent_suggestions:
            assert ENTERPRISE_LICENSE_NOTE in s.reason, (
                f"Enterprise suggestion '{s.name}' should include license note"
            )

    def test_suggest_patterns_no_license_note_when_allowed(self):
        result = suggest_patterns(
            "Help me make an ethical decision about AI usage",
            include_enterprise=True,
            max_patterns=10,
        )
        ent_suggestions = [
            s for s in result.suggested_patterns if s.category == "enterprise"
        ]
        for s in ent_suggestions:
            assert ENTERPRISE_LICENSE_NOTE not in s.reason, (
                f"Enterprise suggestion '{s.name}' should NOT include license note"
            )


class TestSDKLicenseModule:
    """Test the SDK license activation/deactivation/query functions."""

    def setup_method(self):
        self._tmp = tempfile.mkdtemp()
        self._fake_file = Path(self._tmp) / "license.json"

    def teardown_method(self):
        if self._fake_file.exists():
            self._fake_file.unlink()
        Path(self._tmp).rmdir()

    @patch("mycontext.license._LICENSE_FILE")
    @patch("mycontext.license._LICENSE_DIR")
    @patch("mycontext.license._runtime_key", None)
    def test_activate_stores_key(self, mock_dir, mock_file):
        mock_dir.__truediv__ = lambda self, x: Path(self._tmp) / x
        mock_file.__eq__ = lambda s, o: False
        import mycontext.license as lic

        old_file = lic._LICENSE_FILE
        old_dir = lic._LICENSE_DIR
        try:
            lic._LICENSE_FILE = self._fake_file
            lic._LICENSE_DIR = Path(self._tmp)
            lic._runtime_key = None

            result = activate_license("MC-ENT-TEST123")
            assert result is True
            assert lic._runtime_key == "MC-ENT-TEST123"

            data = json.loads(self._fake_file.read_text(encoding="utf-8"))
            assert data["key"] == "MC-ENT-TEST123"
            assert data["active"] is True
        finally:
            lic._LICENSE_FILE = old_file
            lic._LICENSE_DIR = old_dir
            lic._runtime_key = None

    @patch("mycontext.license._LICENSE_FILE")
    @patch("mycontext.license._LICENSE_DIR")
    @patch("mycontext.license._runtime_key", None)
    def test_deactivate_clears_key(self, mock_dir, mock_file):
        import mycontext.license as lic

        old_file = lic._LICENSE_FILE
        old_dir = lic._LICENSE_DIR
        try:
            lic._LICENSE_FILE = self._fake_file
            lic._LICENSE_DIR = Path(self._tmp)
            lic._runtime_key = "MC-ENT-TEST123"

            deactivate_license()
            assert lic._runtime_key is None

            data = json.loads(self._fake_file.read_text(encoding="utf-8"))
            assert data["active"] is False
        finally:
            lic._LICENSE_FILE = old_file
            lic._LICENSE_DIR = old_dir
            lic._runtime_key = None

    def test_activate_empty_key_raises(self):
        with pytest.raises(ValueError, match="empty"):
            activate_license("")

    def test_activate_whitespace_key_raises(self):
        with pytest.raises(ValueError, match="empty"):
            activate_license("   ")

    def test_is_enterprise_active_with_runtime_key(self):
        import mycontext.license as lic

        old = lic._runtime_key
        try:
            lic._runtime_key = "MC-ENT-XXXX"
            assert is_enterprise_active() is True
        finally:
            lic._runtime_key = old

    def test_is_enterprise_active_without_key(self):
        import mycontext.license as lic

        old = lic._runtime_key
        old_file = lic._LICENSE_FILE
        try:
            lic._runtime_key = None
            lic._LICENSE_FILE = Path("/nonexistent/path/license.json")
            assert is_enterprise_active() is False
        finally:
            lic._runtime_key = old
            lic._LICENSE_FILE = old_file


class TestLicenseKeyFormat:
    """Test the CLI key generation format."""

    def test_key_format(self):
        import secrets
        key = f"MC-ENT-{secrets.token_hex(16).upper()}"
        assert key.startswith("MC-ENT-")
        assert len(key) == 7 + 32  # prefix + 32 hex chars

    def test_keys_are_unique(self):
        import secrets
        keys = {f"MC-ENT-{secrets.token_hex(16).upper()}" for _ in range(100)}
        assert len(keys) == 100, "All generated keys should be unique"
