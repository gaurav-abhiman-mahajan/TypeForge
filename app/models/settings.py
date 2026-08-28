from dataclasses import dataclass
from app.core.policies.typing import TypingPolicy, REGULAR, HARD, EXPERT


@dataclass
class PracticeSettings:
    word_count: int = 25
    language: str = "english"
    punctuation: bool = False
    numbers: bool = False
    difficulty: str = "regular"

    def get_policy(self) -> TypingPolicy:
        if self.difficulty.lower() == "hard":
            return HARD
        elif self.difficulty.lower() == "expert":
            return EXPERT
        return REGULAR
