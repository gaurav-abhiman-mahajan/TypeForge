# 01-session-policy-and-lifecycle

Type: task
Status: resolved
Blocked by:

## Question

How do we align session policy defaults, enforce terminal lifecycle states, and guarantee immutable state transitions in `app/core/`?

### Scope
- Align `TypingPolicy` and `setup_policy()` to enable Backspace and Escape by default.
- Ensure terminal session states (`FINISHED`, `ABORTED`) strictly reject subsequent events.
- Prevent rejected events from modifying timing, metrics, or accepted event history.
- Ensure clean session construction per attempt rather than mutable resets.

## Answer

- `TypingPolicy` and `setup_policy()` now default to `allow_backspace=True` and `allow_quit=True`.
- Engine transitions (`StateTransitionEngine`) perform pure dataclass replacements with immutable states.
- Session lifecycle strictly starts on first valid `CharacterTyped`, enters `FINISHED` when target length is reached or `ABORTED` on Escape, freezes active duration, and rejects later events.
- Injected clock support allows deterministic verification across all lifecycle states.
- Verified by unit tests in `tests/test_engine.py`, `tests/test_validation.py`, and `tests/test_session.py`.
