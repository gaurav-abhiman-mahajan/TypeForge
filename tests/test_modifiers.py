import random
from app.content.modifiers import apply_punctuation, apply_numbers


def test_apply_punctuation():
    words = ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
    rng = random.Random(42)
    modified = apply_punctuation(words, rng=rng)
    assert len(modified) == len(words)
    # At least first word is capitalized
    assert modified[0][0].isupper()
    # At least one word ends with punctuation mark
    assert any(w.endswith((".", ",", "!", "?", ";", ":", "'", '"')) for w in modified)


def test_apply_numbers():
    words = ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog", "runs"]
    rng = random.Random(42)
    modified = apply_numbers(words, rng=rng, frequency=0.3)
    assert len(modified) == len(words)
    # Some words are replaced with or contain numbers
    assert any(any(ch.isdigit() for ch in w) for w in modified)
