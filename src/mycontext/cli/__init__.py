"""mycontext command-line interface.

Offline-first CLI for the open-source mycontext SDK. All commands run locally;
``run`` only contacts an LLM when you explicitly pass ``--execute`` with your
own API key.

Commands::

    mycontext list                        # list all 88 cognitive patterns
    mycontext skills export <name|all>    # emit progressive-disclosure SKILL.md packages
    mycontext skills export all --plugin  # emit a Claude Code / Cowork plugin directory
    mycontext run <pattern> "question"    # build a context (optionally execute)
    mycontext mcp                         # start the local stdio MCP server
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ..version import __version__


def _cmd_list(args: argparse.Namespace) -> int:
    from ..intelligence.pattern_catalog import NAME_TO_CATEGORY, NAME_TO_DESCRIPTION

    for name in sorted(NAME_TO_CATEGORY):
        desc = NAME_TO_DESCRIPTION.get(name, "")
        print(f"{name:32}  {desc}")
    print(f"\n{len(NAME_TO_CATEGORY)} cognitive patterns (all open source).")
    return 0


def _cmd_skills_export(args: argparse.Namespace) -> int:
    from . import skills_export

    out_dir = Path(args.out)
    if args.plugin:
        plugin_dir = skills_export.export_plugin(out_dir)
        print(f"Exported plugin directory: {plugin_dir}")
        return 0

    if args.target == "all":
        dirs = skills_export.export_all(out_dir)
        print(f"Exported {len(dirs)} skills to {out_dir}")
        return 0

    try:
        skill_dir = skills_export.export_skill(args.target, out_dir)
    except KeyError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Exported skill: {skill_dir}")
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    from ..skills.pattern_registry import get_pattern, get_pattern_build_params

    try:
        pattern = get_pattern(args.pattern)
    except KeyError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.generic:
        from ..intelligence.prompt_composer import get_generic_prompt_for

        prompt = get_generic_prompt_for(args.pattern, args.question)
        if prompt is None:
            print(
                f"Error: no pre-authored generic prompt for '{args.pattern}'",
                file=sys.stderr,
            )
            return 1
        print(prompt)
        return 0

    primary, _ = get_pattern_build_params(args.pattern)
    context = pattern.build_context(**{primary: args.question})

    if args.execute:
        result = context.execute(provider=args.provider)
        print(result if isinstance(result, str) else getattr(result, "response", result))
    else:
        print(context.assemble())
    return 0


def _cmd_mcp(args: argparse.Namespace) -> int:
    from . import mcp_server

    mcp_server.run()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mycontext",
        description="Offline-first CLI for the open-source mycontext SDK.",
    )
    parser.add_argument("--version", action="version", version=f"mycontext {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List all cognitive patterns.")
    p_list.set_defaults(func=_cmd_list)

    p_skills = sub.add_parser("skills", help="Skill packaging commands.")
    skills_sub = p_skills.add_subparsers(dest="skills_command", required=True)
    p_export = skills_sub.add_parser(
        "export", help="Export pattern(s) as progressive-disclosure SKILL.md packages."
    )
    p_export.add_argument("target", help="Pattern name, or 'all'.")
    p_export.add_argument(
        "--out", default="./skills", help="Output directory (default: ./skills)."
    )
    p_export.add_argument(
        "--plugin",
        action="store_true",
        help="Emit a Claude Code / Cowork plugin directory bundling all skills.",
    )
    p_export.set_defaults(func=_cmd_skills_export)

    p_run = sub.add_parser("run", help="Build (and optionally execute) a pattern.")
    p_run.add_argument("pattern", help="Pattern name (see `mycontext list`).")
    p_run.add_argument("question", help="The input/question for the pattern.")
    p_run.add_argument(
        "--generic",
        action="store_true",
        help="Emit the pre-authored generic prompt instead of the full scaffold.",
    )
    p_run.add_argument(
        "--execute",
        action="store_true",
        help="Execute with an LLM (requires a provider API key in your environment).",
    )
    p_run.add_argument("--provider", default="openai", help="LLM provider for --execute.")
    p_run.set_defaults(func=_cmd_run)

    p_mcp = sub.add_parser("mcp", help="Start the local stdio MCP server.")
    p_mcp.set_defaults(func=_cmd_mcp)

    return parser


def _force_utf8_stdio() -> None:
    """Avoid UnicodeEncodeError on consoles with a legacy code page (e.g. cp1252
    on Windows) when pattern text contains characters like the arrow ``→``."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):  # pragma: no cover - stream not reconfigurable
                pass


def main(argv: list[str] | None = None) -> int:
    _force_utf8_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
