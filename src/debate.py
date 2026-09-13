"""
Runs the actual debate: each persona speaks in turn, sees what the
others have said so far, and responds. This is where the "future
selves arguing with each other" behavior comes from — it's just a
loop that feeds each persona a growing shared transcript.
"""

from __future__ import annotations

from typing import List

from src.client import ClaudeClient
from src.persona import Persona


class Debate:
    """Orchestrates a multi-round debate between future-self personas."""

    def __init__(self, client: ClaudeClient, personas: List[Persona], decision: str) -> None:
        """
        Args:
            client: An initialized ClaudeClient used to generate each turn.
            personas: The future-self personas participating in the debate.
            decision: The decision being debated, used to prompt the
                opening round.
        """
        self.client = client
        self.personas = personas
        self.decision = decision
        self.transcript: List[str] = []

    def run(self, rounds: int = 2) -> List[str]:
        """
        Run the debate for a fixed number of rounds.

        Each persona speaks once per round. From round 2 onward, each
        persona is shown the full transcript so far, so later turns can
        genuinely respond to what other personas said, not just restate
        their own position.

        Args:
            rounds: Number of full rounds to run (each round = every
                persona speaks once). Must be at least 1.

        Returns:
            The full transcript as a list of "Label: text" strings, in
            the order spoken.

        Raises:
            ValueError: If rounds is less than 1.
        """
        if rounds < 1:
            raise ValueError("Debate needs at least 1 round.")

        for round_number in range(1, rounds + 1):
            for persona in self.personas:
                prompt = self._build_prompt(persona, round_number)
                reply = self.client.generate(
                    system_prompt=persona.system_prompt,
                    user_prompt=prompt,
                )
                line = f"{persona.label}: {reply}"
                self.transcript.append(line)
                persona.history.append(reply)

        return self.transcript

    def _build_prompt(self, persona: Persona, round_number: int) -> str:
        """
        Build the user-turn prompt for one persona in one round.

        Round 1 asks the persona to state its position cold. Later
        rounds hand it the transcript so far and ask it to respond,
        specifically to disagree or push back where it genuinely would.
        """
        if round_number == 1:
            return (
                f"The decision on the table is: \"{self.decision}\". "
                "Give your honest take as the future self who made this "
                "choice. What's actually true about how it turned out?"
            )

        so_far = "\n".join(self.transcript)
        return (
            "Here is the debate so far between the different future "
            f"versions of the user:\n\n{so_far}\n\n"
            "Respond to what the others have said. Push back where you "
            "genuinely disagree based on your own lived experience — "
            "don't just restate your earlier point."
        )
