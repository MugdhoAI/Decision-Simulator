"""Tests for src/debate.py

Uses a fake client so no real API calls or API key are needed to run
the test suite.
"""

import pytest

from src.debate import Debate
from src.persona import build_personas


class FakeClaudeClient:
    """Stand-in for ClaudeClient that returns deterministic canned replies."""

    def __init__(self):
        self.calls = []

    def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 600) -> str:
        self.calls.append((system_prompt, user_prompt))
        return f"reply #{len(self.calls)}"


def test_debate_runs_expected_number_of_turns():
    personas = build_personas(
        decision="Take the scholarship or stay",
        options=["Took it", "Stayed"],
        user_context="",
    )
    client = FakeClaudeClient()
    debate = Debate(client=client, personas=personas, decision="Take the scholarship or stay")

    transcript = debate.run(rounds=2)

    # 2 personas * 2 rounds = 4 turns total
    assert len(transcript) == 4
    assert len(client.calls) == 4


def test_debate_rejects_zero_rounds():
    personas = build_personas(decision="D", options=["A", "B"], user_context="")
    debate = Debate(client=FakeClaudeClient(), personas=personas, decision="D")

    with pytest.raises(ValueError):
        debate.run(rounds=0)


def test_round_two_prompt_includes_transcript_so_far():
    personas = build_personas(decision="D", options=["A", "B"], user_context="")
    client = FakeClaudeClient()
    debate = Debate(client=client, personas=personas, decision="D")

    debate.run(rounds=2)

    # The 3rd call (first persona, round 2) should reference round-1 output
    third_call_user_prompt = client.calls[2][1]
    assert "reply #1" in third_call_user_prompt
    assert "reply #2" in third_call_user_prompt


def test_transcript_lines_are_labelled_by_persona():
    personas = build_personas(decision="D", options=["Path A", "Path B"], user_context="")
    client = FakeClaudeClient()
    debate = Debate(client=client, personas=personas, decision="D")

    transcript = debate.run(rounds=1)

    assert transcript[0].startswith("Future You: Path A:")
    assert transcript[1].startswith("Future You: Path B:")
