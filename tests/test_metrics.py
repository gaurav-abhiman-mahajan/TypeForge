from app.core.utils.typing import (
    calculate_accuracy,
    calculate_wpm,
    calculate_character_outcomes,
    count_correct_chars,
)
from app.models.typing import init_metrics_at_idle


def test_calculate_wpm():
    # 50 correct characters in 30 seconds = (50 / 5) / (30 / 60) = 10 / 0.5 = 20 WPM
    assert calculate_wpm(50, 30.0) == 20.0
    assert calculate_wpm(0, 30.0) == 0.0
    assert calculate_wpm(50, 0.0) == 0.0


def test_calculate_accuracy():
    assert calculate_accuracy(95, 100) == 95.0
    assert calculate_accuracy(0, 0) == 0.0
    assert calculate_accuracy(10, 20) == 50.0


def test_count_correct_chars():
    target = "the quick"
    typed = "the quack"
    # Position matches: t, h, e, ' ', q, u, c (typed 'a' != 'i', typed 'k' != 'c'...)
    # index 0: 't'=='t' (1)
    # index 1: 'h'=='h' (2)
    # index 2: 'e'=='e' (3)
    # index 3: ' '==' ' (4)
    # index 4: 'q'=='q' (5)
    # index 5: 'u'=='u' (6)
    # index 6: 'a'!='i'
    # index 7: 'c'!='c'
    # index 8: 'k'!='k'
    assert count_correct_chars(target, "the qu") == 6
    assert count_correct_chars(target, typed) == 8  # 0..5 match, 6 fails ('a' vs 'i'), 7 matches ('c' vs 'c'), 8 matches ('k' vs 'k')


def test_calculate_character_outcomes():
    target = "hello"
    typed = "help"
    outcomes = calculate_character_outcomes(target, typed)
    assert outcomes.correct == 3  # h, e, l
    assert outcomes.incorrect == 1  # p != l
    assert outcomes.missed == 1  # o
    assert outcomes.extra == 0


def test_init_metrics_at_idle():
    metrics = init_metrics_at_idle()
    assert metrics.wpm == 0.0
    assert metrics.raw_wpm == 0.0
    assert metrics.accuracy == 0.0
    assert metrics.typed_chars == 0
