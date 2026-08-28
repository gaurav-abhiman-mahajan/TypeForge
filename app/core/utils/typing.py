from app.models.typing import CharacterOutcomes


# ----------------- STATS ----------------------
def calculate_accuracy(correct_chars: int, total_typed: int) -> float:
    if total_typed <= 0:
        return 0.0
    return (correct_chars / total_typed) * 100.0


def calculate_wpm(correct_chars: int, elapsed_seconds: float) -> float:
    if elapsed_seconds <= 0:
        return 0.0
    return (correct_chars / 5.0) / (elapsed_seconds / 60.0)


def calculate_raw_wpm(total_typed_chars: int, elapsed_seconds: float) -> float:
    if elapsed_seconds <= 0:
        return 0.0
    return (total_typed_chars / 5.0) / (elapsed_seconds / 60.0)


def calculate_cpm(correct_chars: int, elapsed_seconds: float) -> float:
    if elapsed_seconds <= 0:
        return 0.0
    return correct_chars / (elapsed_seconds / 60.0)


def calculate_raw_cpm(total_typed_chars: int, elapsed_seconds: float) -> float:
    if elapsed_seconds <= 0:
        return 0.0
    return total_typed_chars / (elapsed_seconds / 60.0)


# ----------------- EVALUATION ----------------------
def count_correct_chars(target: str, typed: str) -> int:
    return sum(1 for i, ch in enumerate(typed) if i < len(target) and ch == target[i])


def calculate_character_outcomes(target: str, typed: str) -> CharacterOutcomes:
    correct = 0
    incorrect = 0
    extra = max(0, len(typed) - len(target))
    eval_len = min(len(typed), len(target))

    for i in range(eval_len):
        if typed[i] == target[i]:
            correct += 1
        else:
            incorrect += 1

    missed = max(0, len(target) - len(typed))
    return CharacterOutcomes(
        correct=correct,
        incorrect=incorrect,
        extra=extra,
        missed=missed,
    )


def evaluate_characters(target: str, typed: str) -> list[tuple[str, bool]]:
    return [(ch, i < len(target) and ch == target[i]) for i, ch in enumerate(typed)]


# ----------------- WORDS ----------------------
def count_words(target: str, typed: str) -> tuple[int, int]:
    """Returns (completed_words, correct_words)."""
    target_words = target.split()
    typed_words = typed.split()

    completed = len(typed_words)
    correct = 0

    for i, tw in enumerate(typed_words):
        if i < len(target_words) and tw == target_words[i]:
            correct += 1

    return completed, correct
