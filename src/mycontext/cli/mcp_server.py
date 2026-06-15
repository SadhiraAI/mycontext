"""Local stdio MCP server exposing mycontext's offline capabilities.

Runs entirely on the user's machine — no network, no hosted service, no cost.
Exposes three tools to any MCP client (Claude Code, Cursor, Cowork, etc.):

- ``suggest_patterns``     — recommend cognitive patterns for a question (offline).
- ``transform``            — turn raw input into a structured, portable context.
- ``score_output``         — heuristic quality score of an LLM output vs. its context.
- ``draft_requirements``   — natural language intent → PRODUCT requirements.yaml.
- ``draft_technical``      — product spec (or intent) → TECHNICAL requirements.yaml.
- ``trace_requirements``   — check product/technical sync (+ optional code diff).
- ``project_requirements`` — project a spec to AGENTS.md / CLAUDE.md / adr / etc.

The ``mcp`` package is an optional dependency; install with::

    pip install "mycontext-ai[mcp]"
"""

from __future__ import annotations


def _require_mcp():
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - depends on optional extra
        raise SystemExit(
            "The local MCP server requires the 'mcp' package.\n"
            'Install it with:  pip install "mycontext-ai[mcp]"'
        ) from exc
    return FastMCP


def build_server():
    """Construct the FastMCP server with mycontext tools registered."""
    FastMCP = _require_mcp()
    server = FastMCP("mycontext")

    @server.tool()
    def suggest_patterns(question: str, max_patterns: int = 5) -> dict:
        """Suggest cognitive patterns (offline) for a question or task.

        Returns the suggested patterns, an optional ordered chain, and the
        reasoning behind each suggestion. No LLM call is made.
        """
        from ..intelligence.pattern_suggester import suggest_patterns as _suggest

        result = _suggest(question, mode="keyword", max_patterns=max_patterns)
        return {
            "patterns": [
                {"name": s.name, "category": s.category, "reason": s.reason}
                for s in result.suggested_patterns
            ],
            "chain": result.suggested_chain or [],
            "reasoning": result.reasoning,
        }

    @server.tool()
    def transform(text: str, patterns: str = "auto") -> dict:
        """Transform raw input into a structured, portable context (offline).

        Returns the assembled prompt plus the patterns that were applied.
        """
        from ..intelligence.transformation_engine import transform as _transform

        ctx = _transform(text, patterns=patterns)
        return {
            "assembled": ctx.assemble(),
            "patterns_applied": ctx.metadata.get("patterns_applied", [])
            if ctx.metadata
            else [],
        }

    @server.tool()
    def score_output(context_prompt: str, output: str) -> dict:
        """Heuristically score an LLM ``output`` against the ``context_prompt``.

        Offline, deterministic scoring across quality dimensions. Returns the
        overall score, per-dimension scores, strengths, and weaknesses.
        """
        from ..core import Context
        from ..intelligence.output_evaluator import OutputEvaluator

        ctx = Context(directive=context_prompt)
        score = OutputEvaluator(mode="heuristic").evaluate(ctx, output)
        return {
            "overall": round(score.overall, 4),
            "dimensions": {d.value: round(v, 4) for d, v in score.dimensions.items()},
            "strengths": score.strengths,
            "weaknesses": score.weaknesses,
        }

    @server.tool()
    def draft_requirements(intent: str, tier: int = 1) -> dict:
        """Turn a natural-language intent into a framework ``requirements.yaml``.

        Generates the eval-first behavioral spec (tasks, rubrics, action risk
        matrix, safety pre-mortem, datasets, baselines, gates, monitoring) fully
        offline. Gaps never block: each becomes an ``open_questions`` entry with a
        ``TODO(OQ-n)`` marker. Returns the YAML text, the open questions, and
        best-practice validation issues.
        """
        from .. import rac

        doc = rac.architect(intent, tier=tier, execute=False)
        return {
            "requirements_yaml": rac.to_yaml(doc),
            "open_questions": doc.get("open_questions", []),
            "validation": rac.validate(doc),
        }

    @server.tool()
    def draft_technical(product_yaml: str = "", intent: str = "", frontier: bool = False) -> dict:
        """Generate TECHNICAL requirements (the *how*).

        Provide ``product_yaml`` (a product-requirements spec) for traceable
        controls that reference product IDs, or ``intent`` (natural language) to
        bootstrap. Set ``frontier=True`` for the fine-tune / RL / computer-use
        layer. Returns the YAML, open questions, and validation issues.
        """
        import yaml

        from .. import rac

        product_doc = yaml.safe_load(product_yaml) if product_yaml.strip() else None
        doc = rac.technical(text=intent or None, product=product_doc, frontier=frontier)
        return {
            "technical_yaml": rac.to_yaml(doc),
            "open_questions": doc.get("open_questions", []),
            "validation": rac.validate(doc),
        }

    @server.tool()
    def trace_requirements(product_yaml: str, technical_yaml: str, diff: str = "") -> dict:
        """Check whether product and technical requirements are in sync.

        Optionally pass a unified ``diff`` to see which requirement IDs a change
        touches and whether it violates a forbidden action. Returns the trace
        report plus a markdown rendering.
        """
        import yaml

        from .. import rac

        report = rac.trace(yaml.safe_load(product_yaml), yaml.safe_load(technical_yaml), diff=diff or None)
        report["markdown"] = rac.format_report(report)
        return report

    @server.tool()
    def project_requirements(requirements_yaml: str, to: str) -> dict:
        """Project a ``requirements.yaml`` (text) to a downstream target.

        ``to`` is one of: ``agents-md``, ``claude``, ``cursor``, ``spec-kit``,
        ``kiro``. Returns the rendered file contents.
        """
        import yaml

        from .. import rac

        doc = yaml.safe_load(requirements_yaml)
        return {"target": to, "content": rac.project(doc, to=to)}

    return server


def run() -> None:
    """Start the stdio MCP server (blocks)."""
    server = build_server()
    server.run()
