import random
from typing import Optional


def apply_punctuation(
    words: list[str], rng: Optional[random.Random] = None
) -> list[str]:
    """Applies punctuation and capitalization to a sequence of words."""
    if not words:
        return []

    r = rng or random.Random()
    result: list[str] = []
    capitalize_next = True

    for i, word in enumerate(words):
        w = word.capitalize() if capitalize_next else word
        capitalize_next = False

        is_last = i == len(words) - 1

        if is_last:
            mark = r.choice([".", ".", ".", "!", "?"])
            w = f"{w}{mark}"
        else:
            # Chance of clause punctuation
            roll = r.random()
            if roll < 0.15:
                w = f"{w},"
            elif roll < 0.18:
                w = f"{w};"
            elif roll < 0.22:
                # End of sentence mid-test
                mark = r.choice([".", "!", "?"])
                w = f"{w}{mark}"
                capitalize_next = True
            elif roll < 0.25:
                # Quotes
                w = f'"{w}"'

        result.append(w)

    return result


def apply_numbers(
    words: list[str],
    rng: Optional[random.Random] = None,
    frequency: float = 0.15,
) -> list[str]:
    """Replaces words occasionally with numbers."""
    if not words:
        return []

    r = rng or random.Random()
    result: list[str] = []
    has_number = False

    for word in words:
        if r.random() < frequency:
            num = str(r.choice([r.randint(0, 9), r.randint(10, 99), r.randint(100, 999), r.randint(1990, 2026)]))
            result.append(num)
            has_number = True
        else:
            result.append(word)

    # If no number was generated but frequency > 0 and list is large enough, force one
    if not has_number and frequency > 0 and len(result) >= 5:
        idx = r.randint(1, len(result) - 2)
        result[idx] = str(r.randint(1, 99))

    return result
