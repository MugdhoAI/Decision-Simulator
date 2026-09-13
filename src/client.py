"""
Thin wrapper around the Anthropic API.

Kept separate from the rest of the app so the persona/debate logic
never touches HTTP details directly, and so it can be swapped or
mocked easily in tests.
"""

from __future__ import annotations

import os
from typing import Optional

import anthropic


class ClaudeClient:
    """Wraps the Anthropic Messages API for single-turn text generation."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-5") -> None:
        """
        Args:
            api_key: Anthropic API key. If not provided, read from the
                ANTHROPIC_API_KEY environment variable.
            model: Model name to use for generation.

        Raises:
            ValueError: If no API key is available from either source.
        """
        resolved_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not resolved_key:
            raise ValueError(
                "No Anthropic API key found. Set the ANTHROPIC_API_KEY "
                "environment variable or pass api_key explicitly."
            )
        self._client = anthropic.Anthropic(api_key=resolved_key)
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 600) -> str:
        """
        Send a single-turn prompt to Claude and return the text response.

        Args:
            system_prompt: The system-level instruction (defines persona/role).
            user_prompt: The user-facing message content.
            max_tokens: Maximum tokens to generate in the response.

        Returns:
            The generated text, stripped of leading/trailing whitespace.

        Raises:
            anthropic.APIError: If the underlying API call fails.
        """
        response = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text.strip()
