"""
Builds "future self" personas for each path the user could take.

Each persona is a distinct voice: same underlying person, different
choice, different consequences. The system prompt for each persona is
constructed once and reused for every round of the debate so the voice
stays consistent instead of drifting turn to turn.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from src.client import ClaudeClient


@dataclass
class Persona:
    """A single future-self branch tied to one possible choice."""

    label: str          # e.g. "Future You: Took the scholarship"
    choice: str          # the underlying choice this persona represents
    system_prompt: str   # full system prompt used for every turn this persona speaks
    history: List[str] = field(default_factory=list)  # this persona's own past lines, for its own memory


def build_personas(decision: str, options: List[str], user_context: str) -> List[Persona]:
    """
    Create one Persona per option the user is deciding between.

    Args:
        decision: A short description of the decision being made
            (e.g. "Whether to accept the scholarship abroad or stay
            and grow my startup").
        options: The distinct choices to generate a future-self for.
            Must contain at least two options.
        user_context: Background/values/constraints the user has shared,
            used to keep each persona grounded in the user's real
            situation rather than generic advice.

    Returns:
        A list of Persona objects, one per option, in the same order
        as `options`.

    Raises:
        ValueError: If fewer than two options are provided.
    """
    if len(options) < 2:
        raise ValueError("Need at least two options to stage a debate.")

    personas = []
    for option in options:
        label = f"Future You: {option}"
        system_prompt = (
            "You are a future version of the user speaking from several years "
            "after making one specific choice. You are not a neutral advisor — "
            "you are this person, having lived with the consequences of the "
            f"decision: \"{decision}\".\n\n"
            f"The choice you made was: {option}\n\n"
            f"Background on the user making this decision: {user_context}\n\n"
            "Speak in first person, as this future self. Be honest about both "
            "what went well and what you'd warn your past self about. Stay "
            "grounded in the specific context given — do not give generic "
            "life advice. Keep each response to 3-5 sentences so the debate "
            "stays readable."
        )
        personas.append(Persona(label=label, choice=option, system_prompt=system_prompt))
    return personas
