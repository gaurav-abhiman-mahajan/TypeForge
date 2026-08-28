from dataclasses import dataclass, field


@dataclass(frozen=True)
class TypingState:
    target_words: list[str] | tuple[str, ...]
    typed: str = ""

    @property
    def target(self) -> str:
        if isinstance(self.target_words, str):
            return self.target_words
        return " ".join(self.target_words)

    @property
    def cursor(self) -> int:
        return len(self.typed)


@dataclass(frozen=True)
class CharacterOutcomes:
    correct: int = 0
    incorrect: int = 0
    extra: int = 0
    missed: int = 0


@dataclass(frozen=True)
class TypingMetrics:
    wpm: float = 0.0
    raw_wpm: float = 0.0
    cpm: float = 0.0
    raw_cpm: float = 0.0
    accuracy: float = 0.0
    typed_chars: int = 0
    correct_chars: int = 0
    incorrect_chars: int = 0
    completed_words: int = 0
    correct_words: int = 0
    outcomes: CharacterOutcomes = field(default_factory=CharacterOutcomes)


# Alias TypingStats to TypingMetrics for compatibility if required
TypingStats = TypingMetrics


def init_metrics_at_idle() -> TypingMetrics:
    return TypingMetrics()
