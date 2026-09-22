from __future__ import annotations

def validate_decision(decision: str) -> str:
    value = decision.strip()
    if not value:
        raise ValueError("Decision cannot be empty.")
    return value

def validate_options(options: list[str]) -> list[str]:
    cleaned = [option.strip() for option in options]
    if len(cleaned) < 2:
        raise ValueError("Need at least two options to stage a debate.")
    if any(not option for option in cleaned):
        raise ValueError("Options cannot be empty.")
    if len({option.casefold() for option in cleaned}) != len(cleaned):
        raise ValueError("Options must be distinct.")
    return cleaned
