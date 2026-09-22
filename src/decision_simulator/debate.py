from __future__ import annotations
from decision_simulator.interfaces import TextGenerator
from decision_simulator.persona import Persona

class Debate:
    """Orchestrate a multi-round debate between future-self personas."""
    def __init__(self, client: TextGenerator, personas: list[Persona], decision: str) -> None:
        self.client = client
        self.personas = personas
        self.decision = decision
        self.transcript: list[str] = []

    def run(self, rounds: int = 2) -> list[str]:
        """Run the debate and return its transcript."""
        if rounds < 1:
            raise ValueError("Debate needs at least 1 round.")
        if not self.personas:
            raise ValueError("Debate needs at least one persona.")
        self.transcript = []
        for persona in self.personas:
            persona.history.clear()
        for round_number in range(1, rounds + 1):
            for persona in self.personas:
                prompt = self._build_prompt(persona, round_number)
                reply = self.client.generate(system_prompt=persona.system_prompt, user_prompt=prompt).strip()
                if not reply:
                    raise ValueError(f"{persona.label} returned an empty response.")
                line = f"{persona.label}: {reply}"
                self.transcript.append(line)
                persona.history.append(reply)
        return list(self.transcript)

    def _build_prompt(self, persona: Persona, round_number: int) -> str:
        if round_number == 1:
            return (
                f'The decision on the table is: "{self.decision}". '
                "Give your honest take as the future self who made this choice. "
                "What's actually true about how it turned out?"
            )
        so_far = "\n".join(self.transcript)
        return (
            "Here is the debate so far between the different future versions "
            f"of the user:\n\n{so_far}\n\n"
            "Respond to what the others have said. Push back where you genuinely "
            "disagree based on your own lived experience — don't just restate "
            "your earlier point."
        )
