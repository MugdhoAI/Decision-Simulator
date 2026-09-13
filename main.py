"""
Decision Simulator — CLI entry point.

Stages a debate between multiple "future you" personas, each shaped
by a different choice, so you can hear the case for and against a
real decision before you commit to it.

Usage:
    python main.py
"""

from __future__ import annotations

import sys

from src.client import ClaudeClient
from src.debate import Debate
from src.persona import build_personas


def prompt(text: str) -> str:
    """Print a prompt and return the user's stripped input."""
    return input(f"{text}\n> ").strip()


def collect_inputs() -> tuple[str, list[str], str]:
    """
    Interactively collect the decision, options, and context from the user.

    Returns:
        A tuple of (decision, options, user_context).
    """
    decision = prompt("What decision are you wrestling with?")

    options: list[str] = []
    print("\nList the choices you're weighing (at least 2). Type 'done' when finished.")
    while True:
        option = prompt(f"Option {len(options) + 1} (or 'done')")
        if option.lower() == "done":
            if len(options) >= 2:
                break
            print("Need at least 2 options before you can finish.")
            continue
        options.append(option)

    user_context = prompt(
        "\nAny context that matters (values, constraints, what you care about)?"
    )
    return decision, options, user_context


def main() -> int:
    """Run the CLI. Returns a process exit code."""
    print("=== Decision Simulator ===")
    print("Stage a debate between your possible future selves.\n")

    try:
        decision, options, user_context = collect_inputs()
        client = ClaudeClient()
    except ValueError as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        return 1

    personas = build_personas(decision, options, user_context)
    debate = Debate(client=client, personas=personas, decision=decision)

    print("\n--- Debate ---\n")
    try:
        transcript = debate.run(rounds=2)
    except Exception as exc:  # noqa: BLE001 - surface any API failure clearly to the user
        print(f"\nDebate failed: {exc}", file=sys.stderr)
        return 1

    for line in transcript:
        print(line + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
