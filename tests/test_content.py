import pytest
import random
from app.content.loader import load_word_list
from app.content.targets import WordListTargetProvider, get_default_target_provider


def test_load_word_list_default():
    words = load_word_list("english")
    assert len(words) >= 200
    assert "the" in words
    assert "time" in words


def test_load_word_list_missing_raises():
    with pytest.raises(FileNotFoundError):
        load_word_list("non_existent_language_123")


def test_target_provider_deterministic_seed():
    words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"]
    rng1 = random.Random(42)
    rng2 = random.Random(42)

    provider1 = WordListTargetProvider(words, rng=rng1)
    provider2 = WordListTargetProvider(words, rng=rng2)

    result1 = provider1.generate(4)
    result2 = provider2.generate(4)

    assert result1 == result2
    assert len(result1) == 4
    # No repeats when count <= len(words)
    assert len(set(result1)) == 4


def test_target_provider_invalid_count_raises():
    words = ["alpha", "bravo"]
    provider = WordListTargetProvider(words)

    with pytest.raises(ValueError):
        provider.generate(0)

    with pytest.raises(ValueError):
        provider.generate(-5)


def test_get_default_target_provider():
    provider = get_default_target_provider("english", rng=random.Random(123))
    target = provider.generate(25)
    assert len(target) == 25
    assert all(isinstance(w, str) for w in target)
