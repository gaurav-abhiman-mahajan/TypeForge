from collections.abc import Callable
from time import perf_counter

from app.core.engine import StateTransitionEngine
from app.core.policies.typing import TypingPolicy
from app.core.utils.typing import (
    calculate_accuracy,
    calculate_character_outcomes,
    calculate_cpm,
    calculate_raw_cpm,
    calculate_raw_wpm,
    calculate_wpm,
    count_correct_chars,
    count_words,
)
from app.core.validation.transitions import is_valid_transition
from app.models.events import (
    CharacterTyped,
    EscPressed,
    Event,
    SessionEnded,
    SessionStarted,
)
from app.models.session import SessionLifecycle, SessionSnapshot
from app.models.typing import TypingMetrics, TypingState, init_metrics_at_idle


class TypingSession:
    def __init__(
        self,
        policy: TypingPolicy,
        state: TypingState,
        clock: Callable[[], float] = perf_counter,
    ):
        self._engine = StateTransitionEngine()
        self._current_state = state
        self._policy = policy
        self._clock = clock
        self._metrics = init_metrics_at_idle()
        self._event_history: list[Event] = []
        self._lifecycle = SessionLifecycle.IDLE
        self._start_time: float | None = None
        self._end_time: float | None = None
        self._last_input_time: float | None = None

    def _is_first_typing_event(self, event: Event) -> bool:
        return self._lifecycle is SessionLifecycle.IDLE and isinstance(
            event, CharacterTyped
        )

    def _should_finish(self) -> bool:
        return len(self._current_state.typed) >= len(self._current_state.target)

    def _start_session(self):
        self._start_time = self._clock()
        self._event_history.append(SessionStarted())
        self._lifecycle = SessionLifecycle.RUNNING

    def _end_session(
        self, lifecycle: SessionLifecycle = SessionLifecycle.FINISHED
    ):
        if self._lifecycle in (
            SessionLifecycle.FINISHED,
            SessionLifecycle.ABORTED,
        ):
            return
        self._end_time = self._clock()
        self._event_history.append(SessionEnded())
        self._lifecycle = lifecycle

    def _get_elapsed_time(self) -> float:
        if self._start_time is None:
            return 0.0
        end = self._end_time if self._end_time is not None else self._clock()
        return max(0.0, end - self._start_time)

    def _update_metrics(self):
        elapsed = self._get_elapsed_time()
        target = self._current_state.target
        typed = self._current_state.typed

        correct_chars = count_correct_chars(target, typed)
        typed_chars = len(typed)
        incorrect_chars = typed_chars - correct_chars
        completed_words, correct_words = count_words(target, typed)
        outcomes = calculate_character_outcomes(target, typed)

        self._metrics = TypingMetrics(
            wpm=calculate_wpm(correct_chars, elapsed),
            raw_wpm=calculate_raw_wpm(typed_chars, elapsed),
            cpm=calculate_cpm(correct_chars, elapsed),
            raw_cpm=calculate_raw_cpm(typed_chars, elapsed),
            accuracy=calculate_accuracy(correct_chars, typed_chars),
            typed_chars=typed_chars,
            correct_chars=correct_chars,
            incorrect_chars=incorrect_chars,
            completed_words=completed_words,
            correct_words=correct_words,
            outcomes=outcomes,
        )

    def process(self, event: Event):
        if self._lifecycle in (
            SessionLifecycle.ABORTED,
            SessionLifecycle.FINISHED,
        ):
            return

        if not is_valid_transition(self._policy, self._current_state, event):
            return

        if self._is_first_typing_event(event):
            self._start_session()
        elif self._lifecycle is SessionLifecycle.IDLE:
            # Non-typing event when IDLE (e.g. Backspace or Escape) does not start session
            return

        self._last_input_time = self._clock()
        self._event_history.append(event)

        if isinstance(event, EscPressed):
            self._end_session(SessionLifecycle.ABORTED)
            self._update_metrics()
            return

        self._current_state = self._engine.process_event(
            self._current_state, event
        )

        if self._should_finish():
            self._end_session(SessionLifecycle.FINISHED)

        self._update_metrics()

    @property
    def state(self) -> TypingState:
        return self._current_state

    @property
    def metrics(self) -> TypingMetrics:
        return self._metrics

    @property
    def stats(self) -> TypingMetrics:
        """Compatibility alias for metrics."""
        return self._metrics

    @property
    def event_history(self) -> tuple[Event, ...]:
        return tuple(self._event_history)

    @property
    def lifecycle(self) -> SessionLifecycle:
        return self._lifecycle

    @property
    def snapshot(self) -> SessionSnapshot:
        return SessionSnapshot(
            state=self._current_state,
            metrics=self._metrics,
            lifecycle=self._lifecycle,
            elapsed_time=self._get_elapsed_time(),
            event_history=tuple(self._event_history),
            start_time=self._start_time,
            end_time=self._end_time,
        )
