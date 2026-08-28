# 04-textual-ui-practice-and-results

Type: task
Status: resolved
Blocked by: 02, 03

## Question

How do we construct the Textual UI surfaces for Practice and Result with predictable keyboard navigation and zero unhandled exceptions?

### Scope
- Build `Practice` view displaying target text with distinct character styles (pending, cursor, correct, incorrect) and live metrics.
- Build `Result` view showing headline metrics, character outcomes tally, and single-keystroke action bindings (`Enter` -> Next Test, `Ctrl+R` -> Repeat, `Ctrl+Q`/`Esc` -> Exit).
- Handle graceful focus and eliminate bare exception printing.

## Answer

- Implemented `TypingArea` with distinct styling for correct characters, incorrect characters, active cursor position, and pending text.
- Implemented `ResultScreen` displaying Qualified Speed, Keystroke Accuracy, Raw Speed, active duration, character outcomes tally (`correct`, `incorrect`, `extra`, `missed`), and word statistics.
- Wired seamless transition: typing completion pushes `ResultScreen`; `Enter` launches a fresh test; `Ctrl+R`/`r` repeats the target; `Ctrl+Q`/`Esc` exits.
- Verified with Textual async pilot integration tests in `tests/test_ui.py`.
