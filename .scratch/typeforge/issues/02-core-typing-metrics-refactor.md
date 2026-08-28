# 02-core-typing-metrics-refactor

Type: task
Status: resolved
Blocked by: 01

## Question

How do we model and calculate immutable metrics, snapshots, and character outcomes matching the confirmed product definition?

### Scope
- Harmonize `app/models/typing.py`, `app/models/session.py`, and `app/core/utils/typing.py`.
- Implement Qualified Speed (WPM = correct chars / 5 / elapsed mins), Raw Speed (WPM = total chars / 5 / elapsed mins), Keystroke Accuracy (correct insertions / evaluable inputs), and Character Outcomes (`correct`, `incorrect`, `extra`, `missed`).
- Unify session snapshot contract (`SessionSnapshot`) across models, session, and widgets.

## Answer

- Standardized `TypingMetrics`, `CharacterOutcomes`, `TypingState`, and `SessionSnapshot` models.
- Implemented pure utility functions in `app/core/utils/typing.py` for Qualified WPM, Raw WPM, CPM, Raw CPM, Accuracy, Character Outcomes (`correct`, `incorrect`, `extra`, `missed`), and Word counts.
- Provided backward-compatible aliases for `TypingStats` and `SessionSnapShot`.
- Verified with comprehensive test coverage in `tests/test_metrics.py`.
