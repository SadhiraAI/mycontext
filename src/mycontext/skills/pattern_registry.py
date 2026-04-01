"""
Pattern registry - Map pattern name to Pattern class.

Single source of truth for resolving pattern names to classes.
Auto-discovers all patterns from free and enterprise template modules.
Used by: pattern_suggester.get_pattern_class(), skill fusion, chain orchestration.
"""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..structure import Pattern


def _build_registry() -> dict[str, type[Pattern]]:
    """Build name -> Pattern class from free and enterprise templates.

    Introspects both template packages to discover all Pattern subclasses,
    keyed by their ``name`` attribute (set in __init__).
    """
    from ..structure import Pattern as PatternBase
    from ..templates import free as free_pkg

    try:
        from ..templates import enterprise as ent_pkg
    except ImportError:
        ent_pkg = None

    registry: dict[str, type[Pattern]] = {}

    for pkg in (free_pkg, ent_pkg) if ent_pkg else (free_pkg,):
        for attr_name in dir(pkg):
            cls = getattr(pkg, attr_name)
            if isinstance(cls, type) and issubclass(cls, PatternBase) and cls is not PatternBase:
                try:
                    instance = cls()
                    pattern_name = getattr(instance, "name", None)
                    if pattern_name and pattern_name not in registry:
                        registry[pattern_name] = cls
                except Exception:
                    pass

    return registry


_REGISTRY: dict[str, type[Pattern]] | None = None


def get_pattern_registry() -> dict[str, type[Pattern]]:
    """Return the pattern name -> class registry (cached)."""
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = _build_registry()
    return _REGISTRY


def reset_registry() -> None:
    """Clear the cached registry (useful for testing)."""
    global _REGISTRY
    _REGISTRY = None


def get_pattern(name: str) -> Pattern:
    """
    Resolve a pattern by name and return a new instance.

    Args:
        name: Pattern name (e.g. "question_analyzer").

    Returns:
        A new instance of the Pattern.

    Raises:
        KeyError: If the pattern name is not registered.
    """
    registry = get_pattern_registry()
    if name not in registry:
        available = ", ".join(sorted(registry.keys())[:10])
        raise KeyError(f"Unknown pattern: {name!r}. Known patterns include: {available}...")
    return registry[name]()


def get_pattern_build_params(name: str) -> tuple:
    """Introspect a pattern's build_context() to derive (primary_key, defaults).

    Returns:
        (primary_input_key, {optional_key: default_value, ...})
        The primary key is the first positional-or-keyword arg after self
        (the one that receives chained input).  All remaining args go into
        the defaults dict with their default values.
    """
    registry = get_pattern_registry()
    cls = registry.get(name)
    if cls is None:
        return ("input", {})

    try:
        sig = inspect.signature(cls.build_context)
    except (ValueError, TypeError):
        return ("input", {})

    params = [
        p
        for p in sig.parameters.values()
        if p.name not in ("self", "kwargs")
        and p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]

    if not params:
        return ("input", {})

    primary = params[0].name
    defaults: dict[str, object] = {}

    for p in params[1:]:
        if p.default is inspect.Parameter.empty:
            defaults[p.name] = ""
        else:
            defaults[p.name] = p.default if p.default is not None else ""

    return (primary, defaults)
