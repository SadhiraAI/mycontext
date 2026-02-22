"""
Skill model - Parse SKILL.md (Agent Skills open standard) with optional extensions.

Supports standard frontmatter (name, description) plus optional:
- input_schema: parameter names to types for executable skills
- pattern: mycontext template name for pattern-anchored skills
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Type

import yaml

from ..foundation import Directive, Guidance


def _parse_frontmatter_and_body(content: str) -> tuple[Dict[str, Any], str]:
    """Split SKILL.md into YAML frontmatter and Markdown body."""
    content = content.strip()
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    _, frontmatter_str, body = parts
    frontmatter_str = frontmatter_str.strip()
    body = body.strip() if body else ""
    try:
        data = yaml.safe_load(frontmatter_str) or {}
    except yaml.YAMLError:
        data = {}
    return data, body


def _normalize_schema_type(t: Any) -> Type:
    """Map YAML schema type string to Python type."""
    if t is None:
        return str
    if isinstance(t, type):
        return t
    s = str(t).lower()
    if s in ("str", "string"):
        return str
    if s in ("int", "integer"):
        return int
    if s in ("float", "number"):
        return float
    if s in ("bool", "boolean"):
        return bool
    if s in ("list", "array"):
        return list
    if s in ("dict", "object", "map"):
        return dict
    return str


class Skill:
    """
    Parsed Agent Skill (SKILL.md) with optional mycontext extensions.

    Standard fields: name, description (required); license, compatibility, metadata (optional).
    Extension fields: input_schema (optional), pattern (optional).
    """

    def __init__(
        self,
        name: str,
        description: str,
        body: str = "",
        path: Optional[Path] = None,
        *,
        license: Optional[str] = None,
        compatibility: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        allowed_tools: Optional[str] = None,
        input_schema: Optional[Dict[str, Any]] = None,
        pattern: Optional[str] = None,
    ):
        self.name = name
        self.description = description
        self.body = body
        self.path = path
        self.license = license
        self.compatibility = compatibility
        self.metadata = metadata or {}
        self.allowed_tools = allowed_tools
        self.input_schema = input_schema or {}
        self.pattern = pattern

    @classmethod
    def load(cls, path: Path) -> "Skill":
        """
        Load a skill from a directory containing SKILL.md.

        Args:
            path: Directory path (e.g. skill-name/) or path to SKILL.md file.

        Returns:
            Skill instance.

        Raises:
            FileNotFoundError: If SKILL.md not found.
            ValueError: If frontmatter is invalid (missing name/description).
        """
        if path.is_file():
            skill_file = path
            root = path.parent
        else:
            skill_file = path / "SKILL.md"
            root = path
        if not skill_file.exists():
            raise FileNotFoundError(f"SKILL.md not found: {skill_file}")
        content = skill_file.read_text(encoding="utf-8", errors="replace")
        data, body = _parse_frontmatter_and_body(content)
        name = data.get("name")
        description = data.get("description")
        if not name or not description:
            raise ValueError(
                "SKILL.md frontmatter must include 'name' and 'description'"
            )
        # Optional standard fields
        license_val = data.get("license")
        compatibility = data.get("compatibility")
        metadata = data.get("metadata")
        if isinstance(metadata, dict):
            metadata = {str(k): str(v) for k, v in metadata.items()}
        else:
            metadata = {}
        allowed_tools = data.get("allowed-tools")
        # Optional extension fields
        input_schema_raw = data.get("input_schema")
        input_schema = {}
        if isinstance(input_schema_raw, dict):
            for k, v in input_schema_raw.items():
                input_schema[str(k)] = _normalize_schema_type(v)
        pattern = data.get("pattern")
        if pattern is not None:
            pattern = str(pattern).strip()
        return cls(
            name=name,
            description=description,
            body=body,
            path=root,
            license=license_val,
            compatibility=compatibility,
            metadata=metadata,
            allowed_tools=allowed_tools,
            input_schema=input_schema,
            pattern=pattern,
        )

    def summary(self) -> str:
        """Short summary for browse mode (name + description)."""
        return f"# {self.name}\n\n{self.description}"

    def full_instructions(self, params: Optional[Dict[str, Any]] = None) -> str:
        """Full instruction text, with optional template substitution."""
        params = params or {}
        if not params or not self.body:
            return self.body
        try:
            return self.body.format(**params)
        except KeyError:
            # Leave placeholders intact if param missing
            out = self.body
            for k, v in params.items():
                out = out.replace("{" + str(k) + "}", str(v))
            return out

    def validate_params(self, params: Dict[str, Any]) -> None:
        """Validate params against input_schema. Raises ValueError if invalid."""
        if not self.input_schema:
            return
        for key, typ in self.input_schema.items():
            if key not in params:
                raise ValueError(f"Missing required parameter: {key}")
            val = params[key]
            if typ in (list, dict) and not isinstance(val, typ):
                # allow list/dict from schema
                pass
            elif typ not in (list, dict) and not isinstance(val, (str, int, float, bool)):
                raise ValueError(
                    f"Parameter '{key}' must be {typ.__name__}, got {type(val).__name__}"
                )

    def to_context(
        self,
        task: Optional[str] = None,
        include_references: bool = False,
        **params: Any,
    ) -> "Context":
        """
        Build a mycontext Context from this skill (no pattern fusion).

        Uses description for Guidance role/summary and body (or task) for Directive.
        Pattern fusion is handled by SkillRunner when skill.pattern is set.
        """
        from ..core import Context

        self.validate_params(params)
        instruction = self.full_instructions(params)
        if task:
            instruction = f"{instruction}\n\nTask: {task}"
        guidance = Guidance(
            role=f"Skill: {self.name}",
            rules=[self.description[:500]],
            style="Follow the skill instructions precisely.",
        )
        directive = Directive(content=instruction)
        knowledge = None
        if include_references and self.path:
            ref_dir = self.path / "references"
            if ref_dir.exists():
                parts = []
                for f in sorted(ref_dir.glob("*.md")):
                    parts.append(f.read_text(encoding="utf-8", errors="replace"))
                if parts:
                    knowledge = "\n\n---\n\n".join(parts)
        ctx = Context(
            guidance=guidance,
            directive=directive,
            knowledge=knowledge,
            data={"skill": self.name, "task": task, **params},
            metadata={"skill_name": self.name, "skill_path": str(self.path) if self.path else None},
        )
        return ctx
