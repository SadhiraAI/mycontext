"""Requirements-as-Code (RaC) — authoring + scoring bridge.

mycontext helps you *author* and *score* agent requirements; it deliberately
does **not** run them. This package uses the open-source cognitive patterns to
draft the sections of a ``requirements.yaml`` (task taxonomy, evaluation
rubrics, an action risk matrix, and a pre-mortem) and uses the evaluation stack
to score candidate outputs. The emitted ``requirements.yaml`` is then handed off
to *your own* ``spec compile`` / CI / human-in-the-loop tooling for enforcement.

ANTI-GOALS (by design — do not add these here):
- No requirements compiler.
- No CI gate executor.
- No human-in-the-loop / approval runtime.
- No budget or policy enforcement engine.

Authoring runs fully offline. Passing ``execute=True`` with a provider fills the
drafted sections with LLM output using your own API key (still no mycontext
server, still your cost only).
"""

from .architect import RequirementsArchitect, architect, product
from .author import RequirementsAuthor, draft_requirements, score_output, to_yaml
from .fill import complete
from .intake import Intake, parse_intent
from .patterns import analyze, format_brief
from .projections import TARGETS, project
from .technical import TechnicalArchitect, technical
from .trace import format_report, trace
from .validate import validate

__all__ = [
    # Product requirements (the what/why — natural language -> spec)
    "product",
    "RequirementsArchitect",
    "architect",  # deprecated alias for product
    "parse_intent",
    "Intake",
    # Technical requirements (the how — from a product spec or natural language)
    "technical",
    "TechnicalArchitect",
    # LLM completion pass (answer open questions -> filled spec)
    "complete",
    # Cognitive-pattern grounding behind execute (read/render the analyses)
    "analyze",
    "format_brief",
    # Trace (keep product + technical in sync, with optional code diff)
    "trace",
    "format_report",
    # Shared helpers
    "validate",
    "project",
    "TARGETS",
    "to_yaml",
    # Legacy authoring + scoring bridge
    "RequirementsAuthor",
    "draft_requirements",
    "score_output",
]
