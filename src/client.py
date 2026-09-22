from __future__ import annotations
import os
import anthropic
from src.interfaces import TextGenerator

class ClaudeClient(TextGenerator):
    """Small adapter around the Anthropic Messages API."""
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        resolved_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not resolved_key:
            raise ValueError("No Anthropic API key found. Set ANTHROPIC_API_KEY or pass api_key explicitly.")
        self._client = anthropic.Anthropic(api_key=resolved_key)
        self.model = model or os.environ.get("DECISION_SIMULATOR_MODEL", "claude-sonnet-4-5-20250929")

    def generate(self, system_prompt: str, user_prompt: str, *, max_tokens: int = 600) -> str:
        if max_tokens < 1:
            raise ValueError("max_tokens must be positive.")
        response = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text_parts = [block.text for block in response.content if getattr(block, "type", None) == "text"]
        if not text_parts:
            raise RuntimeError("Anthropic returned no text content.")
        return "\n".join(text_parts).strip()
