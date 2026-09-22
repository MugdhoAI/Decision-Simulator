from __future__ import annotations
from typing import Protocol

class TextGenerator(Protocol):
    """Interface required by the debate engine to generate text."""
    def generate(self, system_prompt: str, user_prompt: str, *, max_tokens: int = 600) -> str:
        """Generate one text response."""
        ...
