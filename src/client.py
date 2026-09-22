from __future__ import annotations

import os
import time
from collections.abc import Callable

import anthropic

from src.interfaces import TextGenerator


class ClaudeClient(TextGenerator):
    """Reliable adapter around the Anthropic Messages API."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        *,
        timeout: float = 30.0,
        max_retries: int = 2,
        backoff_seconds: float = 1.0,
    ) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be positive.")
        if max_retries < 0:
            raise ValueError("max_retries cannot be negative.")
        if backoff_seconds < 0:
            raise ValueError("backoff_seconds cannot be negative.")

        resolved_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not resolved_key:
            raise ValueError(
                "No Anthropic API key found. Set ANTHROPIC_API_KEY "
                "or pass api_key explicitly."
            )

        self._client = anthropic.Anthropic(api_key=resolved_key, timeout=timeout)
        self.model = model or os.environ.get(
            "DECISION_SIMULATOR_MODEL",
            "claude-sonnet-4-5-20250929",
        )
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        max_tokens: int = 600,
    ) -> str:
        if max_tokens < 1:
            raise ValueError("max_tokens must be positive.")

        return self._with_retry(
            lambda: self._generate_once(system_prompt, user_prompt, max_tokens)
        )

    def _generate_once(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
    ) -> str:
        response = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text_parts = [
            block.text
            for block in response.content
            if getattr(block, "type", None) == "text"
            and isinstance(getattr(block, "text", None), str)
        ]
        if not text_parts:
            raise RuntimeError("Anthropic returned no text content.")
        return "\n".join(text_parts).strip()

    def _with_retry(self, operation: Callable[[], str]) -> str:
        attempts = self.max_retries + 1
        for attempt in range(attempts):
            try:
                return operation()
            except (
                anthropic.APIConnectionError,
                anthropic.RateLimitError,
                anthropic.InternalServerError,
            ):
                if attempt == attempts - 1:
                    raise
                delay = self.backoff_seconds * (2**attempt)
                if delay:
                    time.sleep(delay)
        raise RuntimeError("Retry loop exited unexpectedly.")
