"""Local stdio MCP server exposing mycontext's offline capabilities.

Runs entirely on the user's machine — no network, no hosted service, no cost.
Exposes three tools to any MCP client (Claude Code, Cursor, Cowork, etc.):

- ``suggest_patterns``  — recommend cognitive patterns for a question (offline).
- ``transform``         — turn raw input into a structured, portable context.
- ``score_output``      — heuristic quality score of an LLM output vs. its context.

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

    return server


def run() -> None:
    """Start the stdio MCP server (blocks)."""
    server = build_server()
    server.run()
