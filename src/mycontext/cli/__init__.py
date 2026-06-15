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
    mycontext rac product "<intent>"      # natural language -> product requirements
    mycontext rac analyze "<intent>"      # render the cognitive-pattern brief (markdown)
    mycontext rac technical --from-product product.yaml   # -> technical requirements
    mycontext rac trace --product p.yaml --technical t.yaml --diff change.diff
    mycontext rac validate spec.yaml
    mycontext rac project spec.yaml --to agents-md
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


def _read_intent_text(args: argparse.Namespace) -> str:
    if getattr(args, "from_file", None):
        return Path(args.from_file).read_text(encoding="utf-8")
    if args.text:
        return args.text
    # Fall back to stdin (e.g. piped input).
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def _print_questions_and_validation(doc: dict, issues: list[str]) -> None:
    oqs = doc.get("open_questions", [])
    if oqs:
        print(f"\n# {len(oqs)} open question(s) recorded — resolve before trusting this spec:", file=sys.stderr)
        for q in oqs:
            flag = "(blocking) " if q.get("blocking") else ""
            print(f"#   {flag}{q['id']}: {q['question']}", file=sys.stderr)
    if issues:
        print("\n# validation:", file=sys.stderr)
        for i in issues:
            print(f"#   {i}", file=sys.stderr)


def _emit_doc(doc: dict, out: str | None) -> None:
    from .. import rac

    yaml_text = rac.to_yaml(doc)
    if out:
        Path(out).write_text(yaml_text, encoding="utf-8")
        print(f"Wrote {out}")
    else:
        print(yaml_text)


def _cmd_rac_product(args: argparse.Namespace) -> int:
    from .. import rac

    text = _read_intent_text(args).strip()
    if not text:
        print("Error: provide intent text, --from FILE, or pipe via stdin.", file=sys.stderr)
        return 1

    if args.intake_only:
        intake = rac.parse_intent(text)
        print(rac.to_yaml(intake.to_dict()))
        return 0

    try:
        doc = rac.product(text, execute=args.execute, provider=args.provider, model=args.model)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    _emit_doc(doc, args.out)
    _print_questions_and_validation(doc, rac.validate(doc))
    return 0


def _cmd_rac_technical(args: argparse.Namespace) -> int:
    import yaml

    from .. import rac

    product_doc = None
    if args.from_product:
        product_doc = yaml.safe_load(Path(args.from_product).read_text(encoding="utf-8"))
    text = _read_intent_text(args).strip() if not product_doc else None

    if not product_doc and not text:
        print("Error: provide --from-product FILE, or intent text / --from FILE.", file=sys.stderr)
        return 1

    try:
        doc = rac.technical(
            text=text, product=product_doc, frontier=args.frontier,
            execute=args.execute, provider=args.provider, model=args.model,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    _emit_doc(doc, args.out)
    _print_questions_and_validation(doc, rac.validate(doc))
    return 0


def _cmd_rac_trace(args: argparse.Namespace) -> int:
    import yaml

    from .. import rac

    product_doc = yaml.safe_load(Path(args.product).read_text(encoding="utf-8"))
    technical_doc = yaml.safe_load(Path(args.technical).read_text(encoding="utf-8"))
    diff_text = Path(args.diff).read_text(encoding="utf-8") if args.diff else None

    report = rac.trace(product_doc, technical_doc, diff=diff_text)
    if args.out:
        Path(args.out).write_text(rac.format_report(report), encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(rac.format_report(report))
    return 1 if report["status"] == "drift_detected" else 0


def _cmd_rac_validate(args: argparse.Namespace) -> int:
    import yaml

    from .. import rac

    doc = yaml.safe_load(Path(args.requirements).read_text(encoding="utf-8"))
    issues = rac.validate(doc)
    if not issues:
        print("OK — no issues found.")
        return 0
    for i in issues:
        print(i)
    return 1 if any(i.startswith("[ERROR]") for i in issues) else 0


def _cmd_rac_project(args: argparse.Namespace) -> int:
    import yaml

    from .. import rac

    doc = yaml.safe_load(Path(args.requirements).read_text(encoding="utf-8"))
    try:
        out = rac.project(doc, to=args.to)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(out)
    return 0


def _cmd_rac_analyze(args: argparse.Namespace) -> int:
    from .. import rac

    text = _read_intent_text(args).strip()
    if not text:
        print("Error: provide intent text, --from FILE, or pipe via stdin.", file=sys.stderr)
        return 1

    try:
        notes = rac.analyze(text, kind=args.kind, provider=args.provider, model=args.model)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    markdown = rac.format_brief(notes)
    if args.out:
        Path(args.out).write_text(markdown, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(markdown)
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

    p_rac = sub.add_parser(
        "rac", help="Requirements Architect: product + technical requirements from intent."
    )
    rac_sub = p_rac.add_subparsers(dest="rac_command", required=True)

    def _add_gen_args(p: argparse.ArgumentParser) -> None:
        p.add_argument("text", nargs="?", help="Natural-language intent (or use --from / stdin).")
        p.add_argument("--from", dest="from_file", help="Read intent from a text/markdown file.")
        p.add_argument("--out", help="Write the spec here (default: stdout).")
        p.add_argument(
            "--execute", action="store_true",
            help="Use an LLM to answer open questions and return a filled spec (your API key).",
        )
        p.add_argument("--provider", default="openai", help="LLM provider for --execute.")
        p.add_argument("--model", default=None, help="Model for --execute (default: gpt-4o-mini).")

    # product (the what/why) — also aliased as `draft` for back-compat.
    for name, help_text in (("product", "Generate PRODUCT requirements from intent."),
                            ("draft", "Alias for `product`.")):
        p_prod = rac_sub.add_parser(name, help=help_text)
        _add_gen_args(p_prod)
        p_prod.add_argument(
            "--intake-only", action="store_true", help="Only print the parsed structured intent."
        )
        p_prod.set_defaults(func=_cmd_rac_product)

    # technical (the how)
    p_tech = rac_sub.add_parser("technical", help="Generate TECHNICAL requirements (from a product spec or intent).")
    _add_gen_args(p_tech)
    p_tech.add_argument("--from-product", dest="from_product", help="Derive from a product-requirements.yaml (richer, traceable).")
    p_tech.add_argument("--frontier", action="store_true", help="Include the frontier layer (fine-tune / RL / computer-use).")
    p_tech.set_defaults(func=_cmd_rac_technical)

    # analyze (the cognitive-pattern brief that grounds execute)
    p_analyze = rac_sub.add_parser(
        "analyze", help="Render the cognitive-pattern brief that grounds --execute (markdown)."
    )
    p_analyze.add_argument("text", nargs="?", help="Natural-language intent (or use --from / stdin).")
    p_analyze.add_argument("--from", dest="from_file", help="Read intent from a text/markdown file.")
    p_analyze.add_argument(
        "--kind", choices=("product", "technical"), default="product",
        help="Which curated pattern set to run (default: product).",
    )
    p_analyze.add_argument("--provider", default="openai", help="LLM provider (requires API key).")
    p_analyze.add_argument("--model", default=None, help="Model (default: gpt-4o-mini).")
    p_analyze.add_argument("--out", help="Write the markdown brief here (default: stdout).")
    p_analyze.set_defaults(func=_cmd_rac_analyze)

    # trace (sync check)
    p_trace = rac_sub.add_parser("trace", help="Check product/technical sync (+ optional code diff).")
    p_trace.add_argument("--product", required=True, help="Path to product-requirements.yaml.")
    p_trace.add_argument("--technical", required=True, help="Path to technical-requirements.yaml.")
    p_trace.add_argument("--diff", help="Optional unified-diff file to check change impact.")
    p_trace.add_argument("--out", help="Write the trace report here (default: stdout).")
    p_trace.set_defaults(func=_cmd_rac_trace)

    p_validate = rac_sub.add_parser("validate", help="Best-practice checks on a spec (product or technical).")
    p_validate.add_argument("requirements", help="Path to a requirements.yaml.")
    p_validate.set_defaults(func=_cmd_rac_validate)

    p_project = rac_sub.add_parser("project", help="Project a spec to a target file.")
    p_project.add_argument("requirements", help="Path to a requirements.yaml.")
    p_project.add_argument(
        "--to", required=True, help="Target: agents-md | claude | cursor | spec-kit | kiro | adr."
    )
    p_project.add_argument("--out", help="Write output here (default: stdout).")
    p_project.set_defaults(func=_cmd_rac_project)

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
