"""Deprecated license shims for mycontext SDK.

mycontext is now fully open source: all cognitive patterns ship in the package
and there are no license tiers. The functions below are retained as no-ops for
one release so existing imports keep working, and they emit a DeprecationWarning.
They will be removed in a future version.
"""

import warnings


def _warn(name: str) -> None:
    warnings.warn(
        f"mycontext.{name}() is deprecated and has no effect. All cognitive "
        "patterns are now open source and available without a license. This "
        "shim will be removed in a future release.",
        DeprecationWarning,
        stacklevel=3,
    )


def activate_license(key: str | None = None) -> bool:
    """Deprecated no-op. All patterns are available without a license."""
    _warn("activate_license")
    return True


def deactivate_license() -> None:
    """Deprecated no-op. All patterns are available without a license."""
    _warn("deactivate_license")


def get_license_key() -> str | None:
    """Deprecated no-op. Always returns None."""
    _warn("get_license_key")
    return None


def is_enterprise_active() -> bool:
    """Deprecated no-op. Always returns True (all patterns are available)."""
    _warn("is_enterprise_active")
    return True
