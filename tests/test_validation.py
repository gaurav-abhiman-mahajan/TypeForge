from app.core.validation.transitions import is_valid_transition
from app.core.policies.typing import TypingPolicy, BehaviorPolicy, ConstraintPolicy
from app.models.typing import TypingState
from app.models.events import CharacterTyped, BackspacePressed, EscPressed


def test_leading_space_rejected_by_default():
    policy = TypingPolicy()
    state = TypingState(target_words=["hello"], typed="")
    assert not is_valid_transition(policy, state, CharacterTyped(" "))


def test_consecutive_space_rejected_by_default():
    policy = TypingPolicy()
    state = TypingState(target_words=["hello", "world"], typed="hello ")
    assert not is_valid_transition(policy, state, CharacterTyped(" "))


def test_valid_space_accepted():
    policy = TypingPolicy()
    state = TypingState(target_words=["hello", "world"], typed="hello")
    assert is_valid_transition(policy, state, CharacterTyped(" "))


def test_backspace_on_empty_buffer_rejected():
    policy = TypingPolicy()
    state = TypingState(target_words=["hello"], typed="")
    assert not is_valid_transition(policy, state, BackspacePressed())


def test_backspace_accepted_when_typed():
    policy = TypingPolicy()
    state = TypingState(target_words=["hello"], typed="h")
    assert is_valid_transition(policy, state, BackspacePressed())


def test_backspace_rejected_when_disabled_by_policy():
    policy = TypingPolicy(behavior=BehaviorPolicy(allow_backspace=False))
    state = TypingState(target_words=["hello"], typed="h")
    assert not is_valid_transition(policy, state, BackspacePressed())


def test_escape_rejected_when_disabled_by_policy():
    policy = TypingPolicy(behavior=BehaviorPolicy(allow_quit=False))
    state = TypingState(target_words=["hello"], typed="h")
    assert not is_valid_transition(policy, state, EscPressed())
