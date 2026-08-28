# TypeForge: Recommended Next Update and Development Phase

**Prepared:** 14 August 2026  
**Repository:** TypeForge  
**Proposed phase:** Playable Local Practice MVP  
**Suggested release target:** `0.2.0` (first explicitly versioned development release)

## Purpose of This Document

This document defines what TypeForge's next update should accomplish based on a fresh review of the complete repository and every current branch. It is an implementation plan, not a description of the long-term wishlist.

The recommended next phase is deliberately focused: make one local typing session correct, configurable, testable, installable, and pleasant to repeat before beginning persistence, analytics, synchronization, leaderboards, or multiplayer work.

## Repository and Branch Review

The remote currently contains exactly two branches, and the local branch tips match the remote tips:

| Branch | Revision | Role | Assessment |
| --- | --- | --- | --- |
| `main` | `5f214aa` | Current integration branch | Contains the redesigned session/engine architecture and a fixed target passage, but Escape and Backspace are disabled by the default policy. |
| `words_and_sentences` | `384b1d2` | Content-generation feature branch | Adds random English word sequences plus 14 language/quote JSON files copied from Monkeytype; it is two commits ahead of `main`. |

The branches have not diverged: `words_and_sentences` is a direct continuation of `main`. Its functional source change is small, but its data addition is large:

- 14 JSON files
- 10,953,437 bytes (10.45 MiB)
- 533,965 added lines in the complete branch diff
- 13 English word lists containing 200 to 450,029 entries
- one English quote collection containing 6,488 quotes
- one 18-line random word-sequence generator
- one widget change replacing a fixed target with generated text

All 21 Python files on `words_and_sentences` parse successfully. All added JSON files are valid JSON. The principal word lists contain unique entries, and the quote file has 6,488 unique IDs, no missing source labels, and no declared text-length mismatches.

Those structural checks do not establish the data's redistribution rights. Most files do not contain license or provenance metadata, and the repository itself does not contain a license or attribution notice covering the copied data.

## What Has Improved Since the Original Prototype

The newer `main` architecture is a meaningful improvement over the earlier controller prototype:

- `StateTransitionEngine` performs small immutable text transitions.
- `TypingSession` owns lifecycle, timing, policy enforcement, event history, state, and derived statistics.
- `perf_counter()` is now used consistently for elapsed duration.
- A session finishes immediately when typed length reaches target length.
- Session state and statistics are exposed together through an immutable snapshot.
- Events receive monotonic timestamps.
- Leading-space, consecutive-space, Backspace, and Escape rules have an explicit validation layer.
- Terminal lifecycle states prevent later input after finish or abort.
- The Textual widget consumes a session rather than managing engine details directly.

This direction should be retained. The next update should finish and harden it rather than introduce another architecture.

## Current Blockers

### 1. Default policy contradicts the intended controls

`TypingPolicy` declares `allow_backspace=True`, but `setup_policy()` defaults `allow_backspace=False`. It also defaults `allow_quit=False`. `TypingArea` calls `setup_policy()` without arguments, so both Backspace and Escape events are rejected.

A direct session check confirmed the result:

- typing a character starts the session;
- Backspace leaves the character unchanged;
- Escape leaves the session running;
- neither rejected event appears in event history.

This is the cause of the latest `main` commit's reported Escape bug and also disables advertised Backspace behavior.

### 2. Abort and application-exit behavior are not defined

Even with `allow_quit=True`, Escape would set the session to `ABORTED` and make the widget ignore all later input. It would not close the application, show a result, or offer a restart. “Quit test,” “abort session,” “return to menu,” and “exit TypeForge” need distinct, documented meanings.

### 3. The feature branch is not ready to merge as-is

The branch proves that data-driven targets are possible, but it currently:

- places target-generation logic under `widgets`, although it is application/domain content logic;
- calls a random word sequence a “sentence” even though it has no grammar or punctuation;
- hard-codes `english.json` and a random length from 20 to 50 words;
- uses module-global randomness, preventing deterministic tests or replay;
- loads and parses the JSON on every generated target;
- has no typed validation or clear error for missing/malformed content;
- uses only the 200-word file while committing more than 10 MiB of other unused content;
- adds quote data without implementing quote mode;
- provides no project-level data attribution or redistribution/license record.

Random selection with replacement also allows repeated words in one target. That can be a valid typing-mode rule, but it should be intentional and tested.

### 4. The session is functional internally but incomplete as a product flow

There is no result view, restart/new-test command, visible lifecycle state, mode selector, setting model, or stable user flow after finish/abort. The only way to receive another target is to restart the program.

### 5. Engineering verification is missing

There are no tests, `pyproject.toml`, supported-Python declaration, formatter/linter/type-checker configuration, CI workflow, or documented installation/run steps. The dependency file resembles a complete environment freeze and includes packages that application code does not import directly.

### 6. Error handling remains presentation-hostile

`TypingArea` catches all exceptions and prints them. In a Textual application, printing is not an appropriate user-facing error path, and catching every `Exception` can hide programming defects.

## Decision: What the Next Phase Should Be

The next phase should be **Playable Local Practice MVP**.

Its outcome should be one polished local workflow:

```text
Launch
  -> generate or select a target
  -> type with working correction controls
  -> finish or abort predictably
  -> see results
  -> start a new test or exit
```

This phase should include a small, legally reviewable content source and a configurable word mode. It should not include all copied datasets, quote mode, persistence, user accounts, networking, synchronization, leaderboards, multiplayer, or advanced analytics.

## Product Decisions for This Phase

The following behavior should be made explicit and treated as acceptance criteria.

### Default controls

- Ordinary printable characters append to the typed buffer when valid.
- Backspace is enabled by default and removes the latest typed character.
- Leading and consecutive spaces remain disabled by default.
- Tab does not enter the target.
- Escape aborts an active test.
- Escape on an idle or completed result screen exits the application, or a separate `q` binding exits. Choose one convention and show it in the UI.
- `r` starts a new test after a finished or aborted test.

### Lifecycle

- A session remains `IDLE` until the first accepted typing character.
- Rejected control input must not start the timer.
- The final target character transitions the session to `FINISHED` immediately.
- An aborted or finished session accepts no further typing characters.
- Restart creates a new session, new target, clean history, zero statistics, and fresh timing values.

### Statistics

- WPM uses correct characters divided by five over active elapsed minutes.
- Accuracy for this phase remains current-buffer accuracy: positionally correct characters divided by current typed length.
- Backspacing a mistake therefore removes it from the displayed accuracy calculation.
- Final statistics freeze when the session finishes or aborts.

Historical keystroke accuracy and error analytics should be deferred until their semantics are designed separately.

### Initial content mode

- Name the mode **words**, not sentence.
- Use a configurable exact word count; default to 25.
- Start with one reviewed English list of modest size.
- Permit repeats only if that behavior is explicitly selected and tested.
- Accept an injected random-number generator or seed so target generation is deterministic in tests.
- Load and validate the word list once, not for every new test.

## Required Workstreams

### Workstream A: Stabilize session policy and lifecycle

1. Make `TypingPolicy` and `setup_policy()` defaults agree.
2. Enable Backspace for the normal mode.
3. Define and enable the expected abort control.
4. Add explicit terminal-state checks for all events.
5. Ensure rejected events do not enter history or alter timing.
6. Decide whether lifecycle events belong in the same history as input events, and document the decision.
7. Provide an explicit session reset/new-session construction path rather than mutating a terminal session.

Recommended design: keep `TypingSession` as the session aggregate and create a new instance for every test. Do not add a mutable `reset()` method that must remember to clear many internal fields.

### Workstream B: Extract and formalize target generation

Move generation out of `app/widgets/` into a presentation-independent package, for example:

```text
app/content/
  loader.py
  targets.py
  data/
    english.json
```

Introduce a small interface such as:

```python
class TargetProvider(Protocol):
    def generate(self, word_count: int) -> str: ...
```

The exact abstraction name is flexible; the important boundary is that `TypingArea` requests a target and does not read files or own random-selection logic.

The provider should:

- validate that `word_count` is positive;
- validate the file exists and has a non-empty string list;
- report malformed content with a meaningful error;
- cache immutable loaded data;
- accept an injectable random generator;
- return exactly the requested number of words;
- have tests for empty data, bad schema, deterministic selection, repeat policy, and output length.

Avoid creating a broad plugin system in this phase. One provider boundary is enough.

### Workstream C: Resolve content provenance before merging data

Do not merge the feature branch's complete asset dump until each retained dataset has documented:

- upstream repository and exact revision;
- original file path;
- applicable license;
- whether redistribution and modification are permitted;
- required attribution or notices;
- local modifications, if any.

Add a `THIRD_PARTY_NOTICES.md` or equivalent attribution file for retained third-party content. Add the project license separately; a project license does not automatically establish rights to bundled datasets.

For the MVP, retain only the one reviewed list actually used by word mode. Defer the 450,029-word list and the 6,488-quote collection until a real product mode requires them. This keeps the release smaller and the legal/quality review bounded.

### Workstream D: Complete the terminal interaction loop

The UI should render four states clearly:

1. **Idle:** target visible, metrics at zero, concise control hint.
2. **Running:** typed correctness and live metrics visible.
3. **Finished:** final results plus restart/exit controls.
4. **Aborted:** aborted status plus restart/exit controls.

At minimum, add:

- visible current lifecycle/result status;
- restart/new-target behavior;
- a documented application-exit binding;
- clear focus behavior;
- cursor/current-character indication;
- no direct `print()` calls from widget event handling.

Catch only expected domain/content exceptions at the UI boundary. Unexpected exceptions should remain visible to development tooling rather than being converted into an unresponsive widget.

### Workstream E: Make the project installable and reproducible

1. Add `pyproject.toml` with project metadata and supported Python range.
2. Use consistent package-qualified imports.
3. Expose a console command such as `typeforge`.
4. Separate direct runtime dependencies from development tools.
5. Document virtual-environment setup, installation, launch, controls, and tests.
6. Add a project license and third-party notices.

The runtime dependency declaration should list packages TypeForge imports directly. Exact environment reproducibility can be handled by a lock file rather than treating every transitive package as a manually maintained direct requirement.

### Workstream F: Establish automated tests and quality gates

Add fast tests before expanding behavior.

#### Session tests

- first accepted character starts the session;
- invalid leading/double spaces do not start or mutate it;
- Backspace works under the default policy;
- Backspace can be disabled by policy;
- Escape produces the chosen abort behavior;
- Escape can be disabled by policy;
- final character finishes immediately;
- terminal sessions reject later input;
- new sessions have clean state and timing;
- snapshots contain immutable event histories;
- WPM and elapsed-time behavior are deterministic through an injected clock.

#### Engine and utility tests

- single-character validation;
- append and Backspace transitions;
- correct-character counting;
- zero/partial/full accuracy;
- zero and known-duration WPM;
- non-positive elapsed-time handling.

#### Content tests

- content schema validation;
- exact generated word count;
- deterministic seeded output;
- defined repeat behavior;
- missing, empty, and malformed data failures.

#### Textual integration tests

- widget receives focus;
- characters and Backspace reach the session;
- Escape follows the selected product behavior;
- correct/incorrect/current characters render as expected;
- finish and abort states display controls;
- restart supplies a fresh target and session.

Configure formatting/linting and run tests in CI on every branch and pull request. Type checking is recommended after the package/import layout is stable.

## Branch Integration Strategy

Do not merge `words_and_sentences` wholesale into `main` in its current form.

Use this sequence:

1. Create the phase branch from `main`, not from the feature branch.
2. Fix and test policy/lifecycle behavior first.
3. Add the target-provider boundary and tests without copied production data.
4. Review upstream licensing/provenance.
5. Bring across only the approved minimal word list and the useful generator concept.
6. Add attribution alongside the data in the same change.
7. Complete the UI result/restart flow.
8. Add packaging, documentation, and CI.
9. Merge only after the acceptance criteria below pass from a clean environment.

Keep `words_and_sentences` until the approved parts have been recovered and compared. Then close/delete it only through the project's normal branch-management process; this plan does not require rewriting its history.

## Suggested Implementation Order

### Update 1: Core behavior correction

- Align policy defaults.
- Make Backspace and abort behavior work.
- Add core/session tests.
- Narrow exception handling.

This should be the first small merge because it restores behavior already claimed by the README.

### Update 2: Target content boundary

- Add the target provider/loader.
- Add exact word-count settings and deterministic generation.
- Add provider tests.
- Retain one approved word list with attribution.

### Update 3: Complete local user flow

- Add lifecycle/result presentation.
- Add restart/new target and exit controls.
- Add Textual integration tests.

### Update 4: Distribution and project hygiene

- Add `pyproject.toml` and console entry point.
- Reduce/separate dependencies.
- Add README setup and control documentation.
- Add license, third-party notices, formatting/linting, and CI.

These can be separate pull requests under one phase. Each update should leave the branch runnable and tests passing.

## Explicitly Out of Scope

The following should not be added during this phase:

- user accounts;
- databases or session persistence;
- online synchronization;
- global leaderboards;
- multiplayer races;
- anti-cheat systems;
- replay UI;
- detailed historical analytics;
- theme/plugin architecture;
- every language/word list;
- quote mode and the full quote dataset;
- animations beyond what is necessary for clear state feedback.

These are valuable later, but they would distract from proving the core local loop and introduce schema, service, security, and product decisions prematurely.

## Definition of Done

The Playable Local Practice MVP phase is complete only when all of the following are true:

- A clean environment can install and launch TypeForge using documented commands.
- The normal mode generates exactly the configured number of words from an approved, attributed source.
- Backspace works by default.
- Leading and consecutive spaces follow the documented policy.
- Escape and application exit behave exactly as documented.
- Timing begins only on the first accepted typing character.
- Live WPM and accuracy update during typing.
- Entering the final target character finishes immediately.
- Finished and aborted sessions display an explicit result/status.
- A user can start a fresh target without restarting the process.
- No widget catches all exceptions or prints errors directly to the terminal UI stream.
- The chosen content has recorded provenance and redistribution terms.
- Unused large datasets are not included in the MVP artifact.
- Domain, content, and minimal UI tests pass.
- Formatting/lint checks and tests run in CI.
- The README's “Current Features” section matches verified behavior.
- The Git working tree is clean after the verification commands.

## Verification Checklist

Run from a new virtual environment:

```text
install project with development dependencies
run formatter check
run linter
run type checker, if configured
run complete test suite
launch the packaged console command
manually complete one perfect test
manually complete one test containing corrected mistakes
manually abort and restart a test
verify exit behavior
verify final Git status is clean
```

Exact commands should be documented once the tools are selected in `pyproject.toml`.

## What Should Follow This Phase

After this MVP is stable, the next logical phase should be **Local Modes and Session History**:

- formal settings model;
- word-count presets;
- reviewed quote mode;
- duration-based mode;
- versioned local session records;
- historical accuracy/error semantics;
- results history and basic analytics;
- replay based on timestamped accepted input events.

That later phase should define storage and replay schemas before synchronization or multiplayer is considered.

## Final Recommendation

TypeForge should build on the session architecture now present in `main`, correct its default-control regression, and selectively recover the feature branch's content-generation idea behind a tested content boundary. The copied datasets should be treated as inputs requiring provenance and scope review, not as a ready-to-merge feature.

The next release should prove that TypeForge is a dependable local typing application. Once installation, controls, lifecycle, target generation, results, restart, and automated verification all work together, the repository will be ready for additional modes and persistent analytics without carrying unresolved core defects forward.
