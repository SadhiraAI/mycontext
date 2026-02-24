"""
Template Safety — Secure directive template formatting.

Replaces raw Python str.format(**inputs) with a validated, injection-resistant
alternative.  The vulnerability being fixed:

    directive_template.format(**inputs)   # UNSAFE

Python's str.format() allows attribute access ({var.__class__}) and item lookup
({var[key]}), which can expose internal object state, environment variables, and
class hierarchies when user-supplied values are interpolated into templates.
This class of attack is documented in:
  - LangChain security advisory GHSA-6qv9-48xg-fc7f (2024)
  - OWASP LLM Prompt Injection Prevention Cheat Sheet (2024)

Design decisions:
  1. Primitive-only values  — non-primitive inputs are rejected before formatting.
  2. Brace-escaping in values — user strings containing { or } are escaped so they
     cannot open new format slots.
  3. Unknown placeholder passthrough — extra placeholders in the template that have
     no matching kwarg are left as-is (no KeyError), preserving optional sections.
  4. No dependency on string.Template — keeps the familiar {variable} syntax that
     all existing directive templates already use.
"""

from __future__ import annotations

import re
from typing import Any

# Types safe to embed directly into a prompt string.
_PRIMITIVE_TYPES = (str, int, float, bool, type(None))

# Regex that matches any placeholder, capturing the bare field name.
# Supports {name} and {name!r} / {name!s} / {name:.2f} etc. but NOT {name.attr}
# or {name[key]}, which are the attack vectors.
_PLACEHOLDER_RE = re.compile(
    r"""
    \{
      (?P<field>[a-zA-Z_][a-zA-Z0-9_]*)   # valid Python identifier — no dots, no brackets
      (?:[!:][^}]*)?                        # optional conversion / format spec
    \}
    """,
    re.VERBOSE,
)

# Reject placeholders that contain attribute access ({obj.attr}) or item
# indexing ({obj[key]}).  These are the injection vectors.
#
# Safe patterns to allow:
#   {name}          — plain identifier
#   {name!r}        — conversion flag
#   {name:>10}      — format spec starting with ':'
#   {name:.2f}      — format spec with dot AFTER colon
#
# Unsafe patterns to reject:
#   {obj.attr}      — dot BEFORE any colon (attribute access)
#   {obj[key]}      — bracket access
#
# Strategy: split at the first ':' (format spec separator).  If the field
# part (before ':') contains a '.' or '[', it's attribute/item access.
_UNSAFE_PLACEHOLDER_RE = re.compile(
    r"""
    \{
      (?P<field_part>[^}:!]*)  # field name, conversion, no colon yet
      [.\[]                    # dot OR open bracket — attack vector
      [^}]*                    # rest of placeholder
    \}
    """,
    re.VERBOSE,
)


def safe_format_template(template: str, **inputs: Any) -> str:
    """Format *template* with *inputs* in an injection-safe way.

    Differences from ``template.format(**inputs)``:

    * Only primitive values (str, int, float, bool, None) are accepted.
      Passing an object would allow ``.attr`` / ``[key]`` access.
    * Curly braces inside string values are escaped before substitution,
      so a value like ``"{__class__}"`` cannot open a new format slot.
    * Placeholders in the template that reference attributes/items (e.g.
      ``{obj.attr}`` or ``{obj[key]}``) raise ``ValueError`` immediately.
    * Placeholders for which no kwarg was supplied are left unchanged
      (useful for optional template sections rendered elsewhere).

    Args:
        template: The directive template string containing ``{variable}`` slots.
        **inputs: Keyword values to substitute.  Must all be primitive types.

    Returns:
        The formatted string with safe substitution applied.

    Raises:
        ValueError: If any input is non-primitive OR the template contains
                    attribute/item access placeholders.
    """
    # 1. Reject unsafe placeholders in the template itself.
    unsafe = _UNSAFE_PLACEHOLDER_RE.findall(template)
    if unsafe:
        raise ValueError(
            f"Directive template contains unsafe placeholders (attribute/item access "
            f"is not allowed): {unsafe!r}. "
            "Use only simple identifiers like {{variable_name}}."
        )

    # 2. Validate and sanitize all input values.
    safe_inputs: dict[str, str] = {}
    for key, value in inputs.items():
        if not isinstance(value, _PRIMITIVE_TYPES):
            raise ValueError(
                f"Template input '{key}' must be a primitive type "
                f"(str, int, float, bool, or None), got {type(value).__name__!r}. "
                "Convert complex objects to strings before passing them as template inputs."
            )
        # Escape braces in string values so they cannot open new format slots.
        str_value = "" if value is None else str(value)
        str_value = str_value.replace("{", "{{").replace("}", "}}")
        safe_inputs[key] = str_value

    # 3. Replace only the known safe placeholders; leave unknown ones intact.
    def _replace(match: re.Match) -> str:
        field_name = match.group("field")
        if field_name in safe_inputs:
            return safe_inputs[field_name]
        # Unknown placeholder — preserve it verbatim (optional section pattern).
        return match.group(0)

    return _PLACEHOLDER_RE.sub(_replace, template)
