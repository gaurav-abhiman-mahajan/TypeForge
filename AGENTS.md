# TypeForge Agent Guide

## Project purpose

TypeForge is a terminal-native typing practice application built with Python and Textual. Its core is intentionally event-driven: keyboard input becomes immutable domain events, a session validates those events against a policy, and a transition engine produces the next immutable typing state. Preserve that separation so sessions can eventually be tested deterministically, replayed, persisted, and synchronized.

The immediate product goal is the **Playable Local Practice MVP** described in `NEXT_PHASE.md`: launch a local test, type and correct input, finish or abort predictably, see results, and start another test. Persistence, accounts, networking, leaderboards, multiplayer, and broad analytics remain later-phase work.

## Read before changing code

- Read `README.md` for the high-level product and architectural intent.
- Read `version1.md` when changing modes, metrics, settings, difficulty, or the user flow.
- Read `NEXT_PHASE.md` when selecting or implementing MVP work. Its recommendations and acceptance criteria are useful; dated branch/revision observations are historical and must be rechecked against Git.
- Inspect `git status` before editing. Preserve unrelated and partially completed user changes.
- Trace the relevant model, session, engine, policy, widget, and call sites together before changing a contract; these layers are tightly connected while the metrics refactor is in progress.

## Architecture and ownership

```text
app/main.py                 legacy script entry point
app/app.py                  Textual application shell
app/screens/                screen composition
app/widgets/                input adaptation and rendering
app/core/session.py         session aggregate and lifecycle
app/core/engine.py          pure typing-state transitions
app/core/policies/          behavior and difficulty policy
app/core/validation/        event admission rules
app/core/utils/typing.py    pure typing calculations
app/models/                 immutable events, state, metrics, snapshots
app/static/                 bundled word lists and quotes
```

Keep dependencies pointed inward:

1. Models contain data and small data-derived properties.
2. Core code owns domain behavior and may depend on models.
3. Screens and widgets adapt Textual input to domain events and render snapshots.
4. Domain code must not import Textual or print UI errors.

Target generation is domain/content behavior, not widget behavior. New generation or loading work belongs in a presentation-independent package such as `app/content/`; widgets should receive or request a target through a narrow boundary.

## Session invariants

Maintain these rules unless a product decision explicitly changes them:

- A session is `IDLE` until its first accepted typing character.
- Rejected events do not mutate state, start timing, or enter accepted-event history.
- Character input and Backspace produce new immutable state values.
- Normal practice enables Backspace and rejects leading and consecutive spaces by default.
- Entering the final target character finishes the session immediately.
- `FINISHED` and `ABORTED` sessions reject later typing input.
- Final elapsed time and derived metrics freeze at the terminal transition.
- WPM is positionally correct characters divided by five, divided by active elapsed minutes.
- Current accuracy is positionally correct characters divided by the current typed length; an empty buffer reports zero.
- A restart constructs a fresh session rather than mutating a terminal session back to idle.

Keep aborting a test, returning to a screen, and exiting the application as distinct concepts. Map keys to those actions explicitly in the UI.

## Events, time, and determinism

- Represent user input and lifecycle changes with the event types in `app/models/events.py`.
- Use monotonic time for elapsed durations.
- Introduce an injectable clock before writing timing-sensitive tests; avoid sleeps in tests.
- Inject or seed randomness for target-provider tests. A provider must return the exact requested word count and define whether repeats are allowed.
- Expose immutable histories and snapshots at public boundaries.

## Metrics and model changes

Metrics are being expanded beyond the original `TypingStats` shape. When modifying them, update the entire contract in one coherent change: model construction, idle defaults, session calculation, snapshot fields, widget consumption, and tests. Check dataclass required fields and derived-property formulas directly; syntax compilation will not catch mismatched constructor or attribute names.

Use one term consistently for each concept. Prefer `TypingMetrics` for derived measurements and `SessionSnapshot` for the session view when a compatibility constraint does not require an older spelling.

## Imports and entry points

The current source mixes package-qualified and top-level imports, so its behavior depends on how it is launched. For touched modules, converge on package-qualified imports such as `from app.models.events import Event`, and keep each change internally runnable. The intended end state is an installable package with a console entry point; avoid adding another ad hoc path workaround.

Until packaging is added, the legacy launch form is:

```bash
python app/main.py
```

Do not assume `python -m app.main` works until imports are normalized and verified.

## Content and licensing

Files under `app/static/` include large language and quote datasets originally brought in for content experiments. Before retaining, moving, or shipping a dataset, record its upstream repository and revision, source path, license, required attribution, and local modifications in a third-party notice. A project license alone does not establish redistribution rights for bundled data.

Keep only data required by an implemented mode. Load and validate content outside widgets, report missing or malformed data clearly, and cache immutable loaded data rather than parsing a JSON file for every test.

## Error handling

Validate domain input at boundaries and raise meaningful, narrow exceptions. UI code may translate expected domain/content failures into visible Textual state. Unexpected programming errors should remain visible to development tooling; broad `except Exception` handlers and direct `print()` calls in widgets are not an error-reporting strategy.

## Setup and verification

There is currently no `pyproject.toml`, lock file, test suite, formatter/linter/type-checker configuration, or CI workflow. `requirements.txt` is an environment freeze rather than a curated list of direct dependencies.

For the current checkout:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m compileall -q app
.venv/bin/python app/main.py
```

Compilation is only a syntax check. Exercise the affected session flow manually when no automated test exists, and report that limitation. When tests and quality tools are introduced, expose canonical commands in `pyproject.toml` and update this section rather than creating competing scripts.

For behavior changes, add focused tests where practical in this order:

1. Pure calculation and engine transitions.
2. Policy validation and session lifecycle.
3. Deterministic content generation and schema failures.
4. Textual focus, key mapping, rendering, finish/abort, and restart integration.

Before handing off a change, run every configured formatter, linter, type check, and relevant test, then run `git status --short`. State exactly which checks ran and which could not run.

## Scope discipline

- Extend the existing session/engine architecture instead of introducing a parallel controller or mutable state path.
- Keep business rules out of Textual handlers.
- Make the smallest coherent change; do not fold unrelated cleanup into feature work.
- Add dependencies only with a documented need.
- Update `README.md` when install, launch, controls, or verified current features change.
- Treat `NEXT_PHASE.md` as the scope boundary for the MVP and defer its explicit out-of-scope features.
