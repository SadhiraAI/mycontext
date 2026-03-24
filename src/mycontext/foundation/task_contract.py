"""
TaskContract (L0) — Declares domain, audience, genre, and grounding protocol.

The Task Contract sits at the very top of a research-flow prompt (primacy zone)
and acts as the single source of truth for *what kind of output* the model should
produce.  It calibrates every downstream section:

- **domain** anchors the vocabulary and reasoning register.
- **audience** sets formality, assumed knowledge, and tone.
- **genre** constrains the output format (markdown brief ≠ JSON API response).
- **grounding** defines the evidential standard and the fallback phrase for
  missing data (e.g. ``[NOT IN PACKET]``).
- **metaphor** controls whether creative/analogical language is permitted.

Use ``TaskContract`` when building a ``Context`` manually::

    from mycontext import Context, Guidance, TaskContract

    ctx = Context(
        guidance=Guidance(role="Staff technical writer", ...),
        task_contract=TaskContract(
            domain="Software engineering — microservices observability",
            audience="Engineering leadership (assume technical literacy)",
            genre="internal brief",
            grounding=(
                "Every claim must trace to the MATERIAL PACKET. "
                "If absent, write the literal token [NOT IN PACKET]."
            ),
        ),
        research_flow=True,
    )

``PromptArchitect`` can also accept a ``TaskContract`` and will use it to
calibrate all 9 sections it generates.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class TaskContract(BaseModel):
    """L0 metadata that calibrates every section of a research-flow prompt.

    All fields are optional — provide whichever dimensions are known.  When
    rendered by ``Context._assemble_research_flow()``, only populated fields
    appear in the L0 table.
    """

    domain: str | None = Field(
        default=None,
        description=(
            "Subject area and scenario — anchors vocabulary and reasoning. "
            "e.g. 'Software engineering — microservices observability'"
        ),
    )

    audience: str | None = Field(
        default=None,
        description=(
            "Who will read the output — sets formality and assumed knowledge. "
            "e.g. 'Staff engineers at a SaaS company'"
        ),
    )

    genre: str | None = Field(
        default=None,
        description=(
            "Output genre — constrains format and tone. "
            "Common values: 'internal brief', 'blog post', 'tutorial', "
            "'API reference', 'email', 'executive summary'. "
            "The genre MUST align with the output_contract format."
        ),
    )

    grounding: str | None = Field(
        default=None,
        description=(
            "Evidential standard — how claims must be sourced and what to "
            "write when evidence is absent. "
            "e.g. 'Trace to MATERIAL PACKET. Fallback: [NOT IN PACKET]'"
        ),
    )

    metaphor: str | None = Field(
        default=None,
        description=(
            "Whether creative/analogical language is permitted. "
            "e.g. 'Off unless the user explicitly asks for analogy.'"
        ),
    )

    def has_content(self) -> bool:
        """True if at least one dimension is populated."""
        return any(
            getattr(self, f) is not None
            for f in ("domain", "audience", "genre", "grounding", "metaphor")
        )

    def to_dict(self) -> dict[str, str]:
        """Return only populated dimensions as a plain dict."""
        return {
            k: v
            for k in ("domain", "audience", "genre", "grounding", "metaphor")
            if (v := getattr(self, k)) is not None
        }

    @classmethod
    def from_dict(cls, d: dict) -> TaskContract:
        """Construct from a plain dict (e.g. Context.metadata['l0'])."""
        return cls(
            domain=d.get("domain"),
            audience=d.get("audience"),
            genre=d.get("genre"),
            grounding=d.get("grounding"),
            metaphor=d.get("metaphor"),
        )

    def __repr__(self) -> str:
        populated = [k for k in ("domain", "audience", "genre", "grounding") if getattr(self, k)]
        return f"TaskContract({', '.join(populated)})"
