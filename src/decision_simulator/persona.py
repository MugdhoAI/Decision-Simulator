from __future__ import annotations
from dataclasses import dataclass, field
from decision_simulator.validation import validate_decision, validate_options

@dataclass
class Persona:
    """A single future-self branch tied to one possible choice."""
    label: str
    choice: str
    system_prompt: str
    history: list[str] = field(default_factory=list)

def build_personas(decision: str, options: list[str], user_context: str) -> list[Persona]:
    """Create one grounded future-self persona for each decision option."""
    decision = validate_decision(decision)
    options = validate_options(options)
    context = user_context.strip()
    personas: list[Persona] = []
    for option in options:
        label = f"Future You: {option}"
        system_prompt = (
            "You are a future version of the user speaking from several years "
            "after making one specific choice. You are not a neutral advisor — "
            "you are this person, having lived with the consequences of the "
            f'decision: "{decision}".\n\n'
            f"The choice you made was: {option}\n\n"
            f"Background on the user making this decision: {context}\n\n"
            "Speak in first person, as this future self. Be honest about both "
            "what went well and what you'd warn your past self about. Stay "
            "grounded in the specific context given — do not give generic "
            "life advice. Keep each response to 3-5 sentences so the debate "
            "stays readable."
        )
        personas.append(Persona(label=label, choice=option, system_prompt=system_prompt))
    return personas
