from app.core.session import TypingSession
from app.core.policies.typing import TypingPolicy
from app.models.typing import TypingState
from app.models.events import CharacterTyped, BackspacePressed, EscPressed
from app.models.session import SessionLifecycle


class MockClock:
    def __init__(self, start_time: float = 100.0):
        self._current = start_time

    def advance(self, seconds: float):
        self._current += seconds

    def __call__(self) -> float:
        return self._current


def test_session_starts_idle():
    clock = MockClock()
    state = TypingState(target_words=["hello"], typed="")
    session = TypingSession(TypingPolicy(), state, clock=clock)
    assert session.lifecycle == SessionLifecycle.IDLE
    assert session.stats.wpm == 0.0
    assert len(session.event_history) == 0


def test_rejected_event_does_not_start_or_enter_history():
    clock = MockClock()
    state = TypingState(target_words=["hello"], typed="")
    session = TypingSession(TypingPolicy(), state, clock=clock)

    # Leading space is rejected
    session.process(CharacterTyped(" "))
    assert session.lifecycle == SessionLifecycle.IDLE
    assert len(session.event_history) == 0
    assert session.state.typed == ""


def test_first_accepted_char_starts_session():
    clock = MockClock()
    state = TypingState(target_words=["hi"], typed="")
    session = TypingSession(TypingPolicy(), state, clock=clock)

    session.process(CharacterTyped("h"))
    assert session.lifecycle == SessionLifecycle.RUNNING
    assert session.state.typed == "h"
    assert len(session.event_history) >= 1


def test_backspace_removes_char():
    clock = MockClock()
    state = TypingState(target_words=["hello"], typed="")
    session = TypingSession(TypingPolicy(), state, clock=clock)

    session.process(CharacterTyped("h"))
    session.process(CharacterTyped("e"))
    assert session.state.typed == "he"

    session.process(BackspacePressed())
    assert session.state.typed == "h"


def test_escape_aborts_running_session():
    clock = MockClock()
    state = TypingState(target_words=["hello"], typed="")
    session = TypingSession(TypingPolicy(), state, clock=clock)

    session.process(CharacterTyped("h"))
    assert session.lifecycle == SessionLifecycle.RUNNING

    session.process(EscPressed())
    assert session.lifecycle == SessionLifecycle.ABORTED

    # Later input rejected
    session.process(CharacterTyped("e"))
    assert session.state.typed == "h"


def test_finishing_target_freezes_metrics():
    clock = MockClock(10.0)
    state = TypingState(target_words=["hi"], typed="")
    session = TypingSession(TypingPolicy(), state, clock=clock)

    session.process(CharacterTyped("h"))
    clock.advance(5.0)  # active elapsed = 5s
    session.process(CharacterTyped("i"))  # target reached!

    assert session.lifecycle == SessionLifecycle.FINISHED
    assert session.state.typed == "hi"

    finished_wpm = session.stats.wpm
    finished_elapsed = session.snapshot.elapsed_time

    # Advance clock further; metrics must remain frozen
    clock.advance(10.0)
    snapshot = session.snapshot
    assert snapshot.elapsed_time == finished_elapsed
    assert snapshot.stats.wpm == finished_wpm

    # Extra typing rejected
    session.process(CharacterTyped("!"))
    assert session.state.typed == "hi"
