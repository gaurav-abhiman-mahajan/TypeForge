import pytest
from app.core.engine import StateTransitionEngine
from app.models.typing import TypingState
from app.models.events import CharacterTyped, BackspacePressed


def test_character_typed_appends_character():
    engine = StateTransitionEngine()
    initial = TypingState(target_words=["hello", "world"], typed="")
    next_state = engine.process_event(initial, CharacterTyped("h"))
    assert next_state.typed == "h"
    assert next_state.cursor == 1


def test_backspace_removes_last_character():
    engine = StateTransitionEngine()
    state = TypingState(target_words=["hello"], typed="hel")
    next_state = engine.process_event(state, BackspacePressed())
    assert next_state.typed == "he"
    assert next_state.cursor == 2


def test_backspace_on_empty_is_noop():
    engine = StateTransitionEngine()
    state = TypingState(target_words=["hello"], typed="")
    next_state = engine.process_event(state, BackspacePressed())
    assert next_state.typed == ""
    assert next_state.cursor == 0


def test_multi_char_raises_value_error():
    engine = StateTransitionEngine()
    state = TypingState(target_words=["hello"], typed="")
    with pytest.raises(ValueError):
        engine.process_event(state, CharacterTyped("he"))
