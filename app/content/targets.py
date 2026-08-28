import random
from typing import Protocol, Sequence, Optional
from app.content.loader import load_word_list
from app.content.modifiers import apply_numbers, apply_punctuation


class TargetProvider(Protocol):
    def generate(
        self,
        count: int = 25,
        punctuation: bool = False,
        numbers: bool = False,
    ) -> list[str]:
        """Generate a sequence of target words with optional modifiers."""
        ...


class WordListTargetProvider:
    def __init__(
        self,
        words: Sequence[str],
        rng: Optional[random.Random] = None,
        allow_repeats: bool = False,
    ):
        if not words:
            raise ValueError("Word list cannot be empty")
        self._words = list(words)
        self._rng = rng or random.Random()
        self._allow_repeats = allow_repeats

    def generate(
        self,
        count: int = 25,
        punctuation: bool = False,
        numbers: bool = False,
    ) -> list[str]:
        if count <= 0:
            raise ValueError(f"Word count must be positive, got {count}")

        if not self._allow_repeats and count <= len(self._words):
            selected = self._rng.sample(self._words, k=count)
        else:
            selected = self._rng.choices(self._words, k=count)

        if numbers:
            selected = apply_numbers(selected, rng=self._rng)

        if punctuation:
            selected = apply_punctuation(selected, rng=self._rng)

        return selected


def get_default_target_provider(
    word_list_name: str = "english",
    rng: Optional[random.Random] = None,
) -> WordListTargetProvider:
    words = load_word_list(word_list_name)
    return WordListTargetProvider(words=words, rng=rng)
