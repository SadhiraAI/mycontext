"""Export cognitive patterns as progressive-disclosure Agent Skill packages.

Each exported skill follows the Agent Skills 3-tier progressive-disclosure model:

- Tier 1 (always loaded): YAML frontmatter ``name`` + ``description`` so an agent
  can decide *whether* the skill is relevant without reading the body.
- Tier 2 (loaded on demand): the SKILL.md body — when to use, inputs, the
  pre-authored prompt, and how the full ``build_context`` scaffold works.
- Tier 3 (referenced as needed): files under ``references/`` — the input/output
  schema and research basis.

Everything runs offline; all 88 cognitive patterns are open source and ship in
the package, so the full template scaffold is included in every export.
"""

from __future__ import annotations

import json
from pathlib import Path

from ..intelligence.pattern_catalog import (
    ENRICHED_CATALOG,
    NAME_TO_CATEGORY,
    NAME_TO_DESCRIPTION,
)
from ..skills.pattern_registry import get_pattern_build_params, get_pattern_registry


def _title(name: str) -> str:
    return name.replace("_", " ").title()


def _build_skill_md(name: str) -> str:
    registry = get_pattern_registry()
    cls = registry[name]
    instance = cls()

    desc = NAME_TO_DESCRIPTION.get(name, getattr(instance, "description", name) or name)
    enrich = ENRICHED_CATALOG.get(name, {})
    when_to_use = enrich.get("when_to_use", "")
    use_cases = enrich.get("use_cases", [])
    output_type = enrich.get("output_type", "")
    theme = enrich.get("theme", "")

    primary, defaults = get_pattern_build_params(name)
    generic = getattr(instance, "GENERIC_PROMPT", None)

    # Tier-1 description (kept concise — this is what the agent always sees).
    tier1_desc = desc.strip()
    if when_to_use:
        sep = "" if tier1_desc.endswith((".", "!", "?")) else "."
        tier1_desc = f"{tier1_desc}{sep} {when_to_use}"
    tier1_desc = tier1_desc.replace("\n", " ").strip()

    lines: list[str] = []
    lines.append("---")
    lines.append(f"name: {_title(name)}")
    lines.append(f"description: {tier1_desc}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {_title(name)}")
    lines.append("")
    if theme:
        lines.append(f"*Theme: {theme}*")
        lines.append("")
    lines.append("## When to use")
    lines.append("")
    lines.append(when_to_use or desc)
    lines.append("")
    if use_cases:
        lines.append("Typical use cases:")
        lines.append("")
        for uc in use_cases:
            lines.append(f"- {uc}")
        lines.append("")
    lines.append("## Inputs")
    lines.append("")
    lines.append(f"- `{primary}` (primary input)")
    for key, default in defaults.items():
        default_str = "" if default in ("", None) else f" (default: `{default}`)"
        lines.append(f"- `{key}`{default_str}")
    lines.append("")
    if output_type:
        lines.append("## Output")
        lines.append("")
        lines.append(output_type)
        lines.append("")
    if generic:
        lines.append("## Pre-authored prompt")
        lines.append("")
        lines.append(
            "Use this directly with any LLM (substitute your own input where the "
            "template references it):"
        )
        lines.append("")
        lines.append("```text")
        lines.append(generic.strip())
        lines.append("```")
        lines.append("")
    lines.append("## Full cognitive scaffold (mycontext SDK)")
    lines.append("")
    lines.append(
        "For the complete, structured context (guidance + directive + constraints), "
        "run the pattern offline with the open-source mycontext SDK:"
    )
    lines.append("")
    lines.append("```python")
    lines.append("from mycontext.skills.pattern_registry import get_pattern")
    lines.append("")
    lines.append(f"pattern = get_pattern({name!r})")
    arg_bits = [f'{primary}="..."'] + [f'{k}="..."' for k in defaults]
    lines.append(f"context = pattern.build_context({', '.join(arg_bits)})")
    lines.append("print(context.assemble())          # portable prompt for any LLM")
    lines.append('# context.execute(provider="openai")  # run with your own API key')
    lines.append("```")
    lines.append("")
    lines.append("See `references/` for the input/output schema and research basis.")
    lines.append("")
    return "\n".join(lines)


def _build_schema(name: str) -> dict:
    primary, defaults = get_pattern_build_params(name)
    enrich = ENRICHED_CATALOG.get(name, {})
    return {
        "name": name,
        "title": _title(name),
        "category": NAME_TO_CATEGORY.get(name, "free"),
        "inputs": {
            "primary": primary,
            "optional": {k: ("" if v is None else v) for k, v in defaults.items()},
        },
        "output_type": enrich.get("output_type", ""),
        "theme": enrich.get("theme", ""),
    }


def _build_research_md(name: str) -> str:
    cls = get_pattern_registry()[name]
    instance = cls()
    enrich = ENRICHED_CATALOG.get(name, {})
    research = getattr(instance, "research_basis", None) or getattr(
        instance, "research", None
    )
    lines = [f"# Research basis — {_title(name)}", ""]
    if enrich.get("theme"):
        lines += [f"**Theme:** {enrich['theme']}", ""]
    if research:
        lines += ["**Research foundation:**", "", str(research), ""]
    else:
        lines += [
            "This pattern is grounded in mycontext's research-backed cognitive "
            "framework library. See https://mycontext-docs.pages.dev/ for citations.",
            "",
        ]
    return "\n".join(lines)


def export_skill(name: str, out_dir: Path) -> Path:
    """Export a single pattern as a progressive-disclosure skill package."""
    if name not in get_pattern_registry():
        raise KeyError(f"Unknown pattern: {name!r}")
    skill_dir = out_dir / name
    refs = skill_dir / "references"
    refs.mkdir(parents=True, exist_ok=True)

    (skill_dir / "SKILL.md").write_text(_build_skill_md(name), encoding="utf-8")
    (refs / "schema.json").write_text(
        json.dumps(_build_schema(name), indent=2), encoding="utf-8"
    )
    (refs / "research.md").write_text(_build_research_md(name), encoding="utf-8")
    return skill_dir


def export_all(out_dir: Path) -> list[Path]:
    """Export every pattern as a skill package. Returns the created directories."""
    return [export_skill(name, out_dir) for name in sorted(get_pattern_registry())]


def export_plugin(out_dir: Path) -> Path:
    """Emit a Claude Code / Cowork plugin directory bundling all skills.

    Produces ``<out_dir>/mycontext-patterns/`` containing a ``plugin.json``
    manifest and a ``skills/`` folder with one progressive-disclosure skill per
    cognitive pattern. Fully local — no marketplace or network required.
    """
    plugin_dir = out_dir / "mycontext-patterns"
    skills_dir = plugin_dir / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    export_all(skills_dir)

    manifest = {
        "name": "mycontext-patterns",
        "description": "88 open-source cognitive patterns from mycontext, packaged "
        "as progressive-disclosure Agent Skills.",
        "version": "1.0.0",
        "skills": "./skills",
        "homepage": "https://mycontext-docs.pages.dev/",
    }
    (plugin_dir / "plugin.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return plugin_dir
