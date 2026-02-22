"""
CLI benchmark runner for cognitive templates.

Usage:
    python -m mycontext.benchmark_cli run --template diagnostic_root_cause_analyzer
    python -m mycontext.benchmark_cli run-all --output results.json
    python -m mycontext.benchmark_cli list
"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="mycontext.benchmark_cli",
        description="Run quality benchmarks for cognitive templates",
    )
    sub = parser.add_subparsers(dest="command")

    # list
    list_cmd = sub.add_parser("list", help="List available benchmarks")

    # run
    run_cmd = sub.add_parser("run", help="Run benchmark for a single template")
    run_cmd.add_argument("--template", required=True, help="Template name")
    run_cmd.add_argument("--provider", default="openai", help="LLM provider")
    run_cmd.add_argument("--eval-mode", default="heuristic", help="Evaluation mode")
    run_cmd.add_argument("--api-key", default=None, help="API key (or set env var)")
    run_cmd.add_argument("--model", default=None, help="LLM model override")
    run_cmd.add_argument("--output", default=None, help="Save results to JSON file")

    # run-all
    all_cmd = sub.add_parser("run-all", help="Run all benchmarks")
    all_cmd.add_argument("--provider", default="openai", help="LLM provider")
    all_cmd.add_argument("--eval-mode", default="heuristic", help="Evaluation mode")
    all_cmd.add_argument("--api-key", default=None, help="API key (or set env var)")
    all_cmd.add_argument("--model", default=None, help="LLM model override")
    all_cmd.add_argument("--output", default=None, help="Save results to JSON file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    from mycontext.intelligence.template_benchmark import TemplateBenchmark

    bench = TemplateBenchmark(
        provider=getattr(args, "provider", "openai"),
        eval_mode=getattr(args, "eval_mode", "heuristic"),
        model=getattr(args, "model", None),
    )

    if args.command == "list":
        names = bench.list_benchmarks()
        if not names:
            print("No benchmarks found.")
            return
        print("Available benchmarks:")
        for n in names:
            print("  - " + n)
        return

    kwargs = {}
    api_key = getattr(args, "api_key", None)
    if api_key:
        kwargs["api_key"] = api_key

    if args.command == "run":
        result = bench.run(args.template, **kwargs)
        print(TemplateBenchmark.report(result))
        if args.output:
            _save_json(args.output, _result_to_dict(result))
            print("\nResults saved to " + args.output)

    elif args.command == "run-all":
        results = bench.run_all(**kwargs)
        for name, result in results.items():
            print(TemplateBenchmark.report(result))
            print()
        if args.output:
            data = {name: _result_to_dict(r) for name, r in results.items()}
            _save_json(args.output, data)
            print("Results saved to " + args.output)


def _result_to_dict(result):
    return {
        "template_name": result.template_name,
        "total_cases": result.total_cases,
        "passed": result.passed,
        "failed": result.failed,
        "avg_score": result.avg_score,
        "avg_cai": result.avg_cai,
        "per_case": [
            {
                "question": c.question,
                "passed": c.passed,
                "output_score": c.output_score,
                "cai": c.cai,
                "issues": c.issues,
            }
            for c in result.per_case
        ],
    }


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
