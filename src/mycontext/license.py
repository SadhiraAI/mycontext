"""Enterprise license management for mycontext SDK.

Stores the license key locally in ~/.mycontext/license.json.
When a valid key is present, enterprise patterns are unlocked.

Usage:
    import mycontext
    mycontext.activate_license("MC-ENT-XXXX...")
    print(mycontext.is_enterprise_active())  # True
    mycontext.deactivate_license()
"""

import json
from pathlib import Path

_LICENSE_DIR = Path.home() / ".mycontext"
_LICENSE_FILE = _LICENSE_DIR / "license.json"

_runtime_key: str | None = None


def _read_stored() -> dict:
    """Read the stored license data from disk."""
    if _LICENSE_FILE.exists():
        try:
            return json.loads(_LICENSE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _write_stored(data: dict) -> None:
    """Persist license data to disk."""
    _LICENSE_DIR.mkdir(parents=True, exist_ok=True)
    _LICENSE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def activate_license(key: str) -> bool:
    """Activate an enterprise license key.

    Stores the key locally so enterprise patterns are unlocked in all future
    sessions. Returns True if the key was stored successfully.

    Args:
        key: Enterprise license key (e.g. MC-ENT-XXXX...)
    """
    global _runtime_key
    key = key.strip()
    if not key:
        raise ValueError("License key cannot be empty.")
    _runtime_key = key
    _write_stored({"key": key, "active": True})
    return True


def deactivate_license() -> None:
    """Remove the stored license key and revert to free tier."""
    global _runtime_key
    _runtime_key = None
    _write_stored({"key": None, "active": False})


def get_license_key() -> str | None:
    """Return the current license key or None."""
    if _runtime_key:
        return _runtime_key
    data = _read_stored()
    if data.get("active") and data.get("key"):
        return data["key"]
    return None


def is_enterprise_active() -> bool:
    """Check whether an enterprise license key is present."""
    return get_license_key() is not None
