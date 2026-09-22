from __future__ import annotations
import sys
import anthropic
from src.client import ClaudeClient
from src.debate import Debate
from src.persona import build_personas

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

def main() -> int:
    print("=== Decision Simulator ===")
    print("Stage a debate between your possible future selves.\n")
    try:
        decision, options, user_context = collect_inputs()
        client = ClaudeClient()
        personas = build_personas(decision, options, user_context)
        transcript = Debate(client, personas, decision).run(rounds=2)
    except (ValueError, anthropic.APIError) as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"\nUnexpected error: {exc}", file=sys.stderr)
        return 1
    print("\n--- Debate ---\n")
    for line in transcript:
        print(line + "\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
