from unittest.mock import MagicMock, patch

import anthropic
import pytest

from decision_simulator.client import ClaudeClient


def make_client() -> ClaudeClient:
    with patch("decision_simulator.client.anthropic.Anthropic") as factory:
        client = ClaudeClient(api_key="test", model="test-model", max_retries=0)
        client._client = MagicMock()
        return client


def response_with_text(text: str):
    block = MagicMock()
    block.type = "text"
    block.text = text
    response = MagicMock()
    response.content = [block]
    return response


def test_generate_joins_text_blocks():
    client = make_client()
    client._client.messages.create.return_value = response_with_text("hello")
    assert client.generate("system", "user") == "hello"


def test_generate_rejects_invalid_max_tokens():
    client = make_client()
    with pytest.raises(ValueError):
        client.generate("system", "user", max_tokens=0)


def test_generate_rejects_empty_response():
    client = make_client()
    block = MagicMock()
    block.type = "image"
    response = MagicMock(content=[block])
    client._client.messages.create.return_value = response
    with pytest.raises(RuntimeError, match="no text"):
        client.generate("system", "user")


def test_connection_errors_are_retried():
    client = make_client()
    client.max_retries = 2
    client.backoff_seconds = 0
    client._client.messages.create.side_effect = [
        anthropic.APIConnectionError(request=MagicMock()),
        response_with_text("recovered"),
    ]
    assert client.generate("system", "user") == "recovered"
    assert client._client.messages.create.call_count == 2
