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

from .author import RequirementsAuthor, draft_requirements, score_output, to_yaml

__all__ = [
    "RequirementsAuthor",
    "draft_requirements",
    "score_output",
    "to_yaml",
]
