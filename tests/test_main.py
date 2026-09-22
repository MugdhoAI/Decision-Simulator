import pytest

from main import collect_inputs, run_simulation


class FakeClient:
    def __init__(self, reply="ok"):
        self.reply = reply
        self.calls = []

    def generate(self, system_prompt: str, user_prompt: str, *, max_tokens: int = 600) -> str:
        self.calls.append((system_prompt, user_prompt))
        return self.reply


def test_run_simulation_isolated_and_deterministic():
    client = FakeClient()
    result = run_simulation("D", ["A", "B"], "context", client, rounds=1)
    assert result == ["Future You: A: ok", "Future You: B: ok"]
    assert len(client.calls) == 2


def test_run_simulation_rejects_invalid_options():
    with pytest.raises(ValueError, match="distinct"):
        run_simulation("D", ["A", "a"], "", FakeClient())


def test_run_simulation_rejects_empty_generator_response():
    with pytest.raises(ValueError, match="empty response"):
        run_simulation("D", ["A", "B"], "", FakeClient(reply=""))


def test_collect_inputs_rejects_empty_decision(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "   ")
    with pytest.raises(ValueError, match="Decision"):
        collect_inputs()


def test_collect_inputs_accepts_two_options(monkeypatch):
    answers = iter(["Choose", "A", "B", "done", "context"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert collect_inputs() == ("Choose", ["A", "B"], "context")
