"""Tests for src/persona.py"""

import pytest

from decision_simulator.persona import build_personas


def test_build_personas_creates_one_per_option():
    personas = build_personas(
        decision="Take the scholarship or stay and grow the startup",
        options=["Took the scholarship", "Stayed and grew the startup"],
        user_context="Founder of an early-stage agri-tech startup in Bangladesh",
    )
    assert len(personas) == 2
    assert personas[0].choice == "Took the scholarship"
    assert personas[1].choice == "Stayed and grew the startup"


def test_persona_system_prompt_includes_decision_and_choice():
    decision = "Move abroad or stay"
    options = ["Moved abroad", "Stayed home"]
    personas = build_personas(decision=decision, options=options, user_context="")

    for persona, option in zip(personas, options):
        assert decision in persona.system_prompt
        assert option in persona.system_prompt
        assert persona.label == f"Future You: {option}"


def test_build_personas_requires_at_least_two_options():
    with pytest.raises(ValueError):
        build_personas(decision="Some decision", options=["Only one option"], user_context="")


def test_persona_history_starts_empty():
    personas = build_personas(decision="Decision", options=["A", "B"], user_context="context")
    assert all(persona.history == [] for persona in personas)
