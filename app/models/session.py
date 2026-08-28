from dataclasses import dataclass
from enum import Enum
from app.models.events import Event
from app.models.typing import TypingMetrics, TypingState


class SessionLifecycle(Enum):
    IDLE = "idle"
    RUNNING = "running"
    FINISHED = "finished"
    ABORTED = "aborted"


@dataclass(frozen=True)
class SessionSnapshot:
    state: TypingState
    metrics: TypingMetrics
    lifecycle: SessionLifecycle
    elapsed_time: float
    event_history: tuple[Event, ...] = ()
    start_time: float | None = None
    end_time: float | None = None

    @property
    def stats(self) -> TypingMetrics:
        """Compatibility alias for metrics."""
        return self.metrics


SessionSnapShot = SessionSnapshot
