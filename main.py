from __future__ import annotations

import argparse
import json
import sys

import anthropic

from src import __version__
from src.client import ClaudeClient
from src.debate import Debate
from src.interfaces import TextGenerator
from src.persona import build_personas
from src.report import build_report, write_report
from src.validation import validate_decision, validate_options


def prompt(text: str) -> str:
    return input(f"{text}\n> ").strip()


def collect_inputs() -> tuple[str, list[str], str]:
    decision = prompt("What decision are you wrestling with?")
    if not decision:
        raise ValueError("Decision cannot be empty.")
    options: list[str] = []
    print("\nList the choices you're weighing (at least 2). Type 'done' when finished.")
    while True:
        option = prompt(f"Option {len(options) + 1} (or 'done')")
        if option.lower() == "done":
            if len(options) >= 2:
                break
            print("Need at least 2 options before you can finish.")
            continue
        if not option:
            print("Option cannot be empty.")
            continue
        if option.casefold() in {existing.casefold() for existing in options}:
            print("Options must be distinct.")
            continue
        options.append(option)
    user_context = prompt("\nAny context that matters (values, constraints, what you care about)?")
    return decision, options, user_context


def run_simulation(
    decision: str,
    options: list[str],
    user_context: str,
    client: TextGenerator,
    *,
    rounds: int = 2,
) -> list[str]:
    personas = build_personas(decision, options, user_context)
    return Debate(client, personas, decision).run(rounds=rounds)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Stress-test a decision by debating simulated future selves."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--decision", help="Decision to stress-test.")
    parser.add_argument("--option", action="append", dest="options", help="Decision option. Repeat for each option.")
    parser.add_argument("--context", default="", help="Background, values, and constraints.")
    parser.add_argument("--rounds", type=int, default=2, help="Number of debate rounds (default: 2).")
    parser.add_argument("--json", action="store_true", help="Print the completed report as JSON.")
    parser.add_argument("--output", type=str, help="Write the completed report to a local JSON file.")
    return parser


def main(argv: list[str] | None = None, client: TextGenerator | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.decision is None and args.options is None:
            decision, options, user_context = collect_inputs()
        elif args.decision is None or not args.options:
            parser.error("--decision and at least two --option values must be provided together.")
        else:
            decision = validate_decision(args.decision)
            options = validate_options(args.options)
            user_context = args.context.strip()

        if args.rounds < 1:
            parser.error("--rounds must be at least 1.")

        generator = client or ClaudeClient()
        transcript = run_simulation(
            decision, options, user_context, generator, rounds=args.rounds
        )
        report = build_report(
            decision, options, user_context, args.rounds, transcript, __version__
        )

        if args.output:
            write_report(report, args.output)
        if args.json:
            print(report.to_json(), end="")
        else:
            print("\n--- Debate ---\n")
            for line in transcript:
                print(line + "\n")
    except (ValueError, anthropic.APIError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
