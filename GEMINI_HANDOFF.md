# TypeForge Design Discovery Handoff

## Assignment

Continue the TypeForge product-discovery and design session with the user. The current task is to finish the Grilling interview, sharpen the domain model, and produce a terminal UX and application architecture plan. Do not implement the application during this phase.

Use these disciplines if their skill files are available:

- `domain-modeling`: challenge ambiguous terms and update `CONTEXT.md` when a term is settled.
- `grilling`: work the design tree in rounds, ask the full current frontier, recommend an answer for every question, then wait.
- `impeccable`: use `init` to write `PRODUCT.md`, then `shape` to plan the terminal UX. This is an Operate surface.
- `codebase-design`: design deep modules with small interfaces at clean seams. Use the terms Module, Interface, Implementation, Seam, Adapter, Depth, Leverage, and Locality exactly.

Read `AGENTS.md`, `CONTEXT.md`, `README.md`, `version1.md`, and `NEXT_PHASE.md` before continuing. Inspect `git status` and preserve all existing worktree changes.

## Interview protocol

1. Treat every decision under **Confirmed decisions** as closed. Reopen one only when the user contradicts it.
2. Start with **Next Grilling round** below. Ask those questions together and wait for the answers.
3. After each round, recompute the frontier. Ask decisions; investigate facts yourself.
4. When a domain term is resolved, update `CONTEXT.md` immediately. Keep it a glossary with no implementation details.
5. Continue until no material product, interaction, or architecture decision remains silently assumed.
6. Present the complete understanding for explicit confirmation.
7. Only after confirmation, write the product, UX, and architecture planning documents. Do not write application code unless the user starts a separate implementation phase.

Question format:

```markdown
❓ **Q<number>** - **<title>**: <decision and relevant choices>

➡️ <recommended answer and concrete reason>
```

Ask no more than three related questions per round. Never ask the user for a fact available in this repository or the local Monkeytype fork.

## Product understanding

TypeForge is a Python and Textual terminal application for deliberate typing practice and synchronous competitive typing. It is terminal-native and local-first. Linux terminals launched from Bash are the first supported environment; standard Windows and macOS terminals are later compatibility targets.

TypeForge uses Monkeytype as a functional benchmark, not as a product or visual template. Functional parity covers Test modes, limits, content selection, typing rules, meaningful settings, metrics, Results, replay, targeted practice, and history. TypeForge will have its own terminal interaction model, visual identity, data model, and competitive architecture.

The long-term design must support synchronized Typing Profiles and public ranked Races. The implementation roadmap still begins with the Playable Local Practice MVP in `NEXT_PHASE.md`.

## Confirmed decisions

### Audience and position

- Primary audiences are terminal-native developers and competitive typists.
- The product launches from the shell, is fully keyboard-operated, and works offline for practice.
- Practice is local-first. Online competition is fully connected and server-authoritative.
- The design covers the enduring product; implementation remains phased.

### Practice and Tests

- Launching `typeforge` opens a ready Test using the last or default configuration. There is no blocking home screen.
- The first accepted typing character starts an Attempt.
- The canonical Test Modes are Time, Words, Quote, Zen, and Custom.
- Code is a Content Set, not a Test Mode.
- Book content is a saved long-form Custom Test.
- Targeted Practice is a Practice Program, not a Test Mode.
- Corrections change the current text but never erase the original mistake from the Attempt Record.
- Results distinguish final character outcomes, Keystroke Accuracy, Qualified Speed, Raw Speed, corrections, and Backspace behavior.
- Functional settings should cover punctuation, numbers, language/content, Normal/Expert/Master difficulty, stop-on-error, confidence, deletion, and completion behavior.
- Browser-specific settings, sound packs, large theme catalogs, novelty modifiers, and DOM layout settings are not parity targets.

### Identity, data, and synchronization

- An account is optional for practice and mandatory for competition.
- All practice data synchronizes after sign-in, including complete Attempt Records. This data builds a detailed Typing Profile.
- Signing in must clearly explain full-history synchronization and ask before uploading existing local history.
- Typists can export and permanently delete their Typing Profile.
- Synchronized data is encrypted in transit and at rest.
- Attempt Records and detailed behavioral data are private by default.
- Public profiles expose only deliberately selected Results and aggregates.
- Competitive integrity evidence may use a declared retention exception.

### Competition

- Competition consists only of public skill-based Matchmaking. There are no private rooms.
- A Match is a synchronous four-typist Race.
- Competitive Playlists lock the Test, Content Set, limit, Rule Set, and rating pool.
- The first Standard Ranked playlist is Words 50, English 1K, punctuation and numbers off, Normal difficulty, and Backspace allowed.
- Every competitor receives the same server-selected target. The final word must be correct.
- Placement uses valid completion time; Keystroke Accuracy breaks a tie.
- Each playlist has a separate visible Skill Rating and tier. Rating changes use Placement, opponent strength, and rating certainty rather than direct WPM.
- New competitors complete provisional Matches.
- Matchmaking starts with narrow rating and latency windows, expands the rating window over time, and preserves a hard latency ceiling.
- Ranked Matches never use bots.
- A disconnect before the countdown completes cancels the Match and requeues the remaining typists.
- A disconnect after the start does not pause the Race. A short authenticated reconnection window restores server-accepted progress; failure to return becomes a Forfeit.
- Repeated abandonment may cause escalating queue restrictions.
- The Match Authority owns the exact Test, Rule Set, countdown, accepted event order, finish window, Result, Placement, and rating update.
- The client renders immediately and submits evidence. Client-calculated metrics and finish times are never authoritative.
- Integrity validation uses terminal-observable input and monotonic timestamps. Enhanced press/release evidence may be used when available but cannot be required.
- Integrity checks may detect impossible timing, event order, target knowledge, duplicates, automation patterns, and clock anomalies.
- Integrity checks do not scan processes, install global keyboard hooks, capture screenshots, or monitor the wider system.
- Public Match Summaries show playlist, date, Placement, Qualified Speed, Keystroke Accuracy, completion state, and rating change.
- Raw Attempt Records, key timings, corrections, and behavioral analysis remain private.
- Suspicious Matches withhold rating changes pending review rather than publicly accusing a typist.

### Terminal contract

- The complete interface works at `80×24` and uses enhanced layouts on wider terminals.
- Every function is keyboard-accessible; mouse input is optional.
- ANSI color may enhance the interface, but color is never the only signal.
- Rendering supports high-contrast, monochrome, reduced-motion, and ASCII-safe fallbacks.
- The interface does not depend on a particular terminal font or shell theme.

## Next Grilling round

These questions were asked but not answered. Resume here without renumbering them.

❓ **Q26** - **Terminal surface map**: Should TypeForge use a focused app shell with no persistent home screen or navigation chrome?

➡️ Recommend eight surfaces: Practice, Result, Command Palette, History, Matchmaking, Race, Match Summary, and Account/Sync. Launch into Practice; reach every other surface through commands or Result actions.

❓ **Q27** - **Global command model**: Should commands use explicit control-key bindings so ordinary typing characters are never overloaded?

➡️ Recommend `Ctrl+K` for the command palette, `Ctrl+R` for a fresh Test, `Ctrl+Q` to quit, `Esc` to close an overlay or abandon an active Attempt, `Enter` for the next Test from a Result, and `Shift+Enter` to finish an open-ended Test. Confirm destructive actions during long Tests. Leaving an active Race is a Forfeit.

❓ **Q28** - **Typing-surface hierarchy**: What should remain visible while typing?

➡️ Recommend target text as the dominant element. Practice shows progress or time plus optional live Qualified Speed and Keystroke Accuracy. Race replaces secondary diagnostics with four compact progress tracks and current Placement. Detailed diagnostics belong on Result.

## Likely later frontiers

Ask these only after Q26-Q28 are settled and only when their prerequisites are closed:

- Result hierarchy: summary, charts, Character Outcomes, replay, repeat, next Test, and targeted practice.
- Command Palette information architecture and whether key bindings are configurable.
- Account authentication from a terminal, token storage, signed-out-to-signed-in migration, and sync status/error recovery.
- Matchmaking states: searching, widening range, Match found, loading, countdown, cancellation, reconnecting, Forfeit, and integrity review.
- Race feedback: opponent identity, exact versus approximate progress, network degradation, finish transitions, and post-finish spectating.
- Public profile, privacy defaults, retention periods, export, and deletion flows.
- Narrow-terminal degradation below `80×24` and unsupported terminal capability messaging.
- Accessibility beyond color and motion, including focus, readable status text, and assistive-terminal behavior.
- TypeForge's visual direction. Do not copy Monkeytype's appearance or choose a visual world before Impeccable product initialization is complete.
- The exact deep-module interfaces and phased migration from the current code.

## Monkeytype fork findings

The official Monkeytype fork is at `/home/gaurav/gamoventure/monkeytype`. Use it to verify behavior, not to copy architecture or presentation.

### Behavior worth retaining

- Canonical modes are Time, Words, Quote, Custom, and Zen.
- Code is represented as content/language.
- Input starts on the first admitted insertion.
- Explicit input events retain original correctness after corrections.
- Accuracy derives from historical insertions, not the final buffer.
- Qualified WPM credits correct completed words; Raw WPM includes final correct, incorrect, and extra characters.
- Results separate correct, incorrect, extra, and missed characters.
- Difficulty, stop-on-error, confidence, deletion, and completion rules are distinct behaviors.
- A command palette is central to keyboard-driven configuration.

Relevant source:

- `frontend/src/ts/test/events/types.ts`
- `frontend/src/ts/test/events/stats.ts`
- `frontend/src/ts/test/test-logic.ts`
- `frontend/src/ts/test/words-generator.ts`
- `frontend/src/ts/input/handlers/insert-text.ts`
- `frontend/src/ts/input/handlers/before-delete.ts`
- `frontend/src/ts/input/helpers/fail-or-finish.ts`
- `frontend/src/ts/config/metadata.tsx`
- `packages/schemas/src/configs.ts`
- `packages/schemas/src/results.ts`

### Architecture to avoid

- Monkeytype mixes behavioral, presentation, and novelty settings in one broad global configuration.
- Its test orchestration depends on global signals and browser DOM state.
- Its signed-out history and retry behavior are not durable offline synchronization.
- The public fork contains no synchronous multiplayer, Matchmaking, shared countdown, opponent progress, or Match Authority.
- The public anti-cheat implementation is intentionally a stub.

TypeForge therefore needs its own Race, synchronization, and integrity design.

## Deep-module architecture hypothesis

This is a working hypothesis, not a confirmed design. Stress-test it after the product and UX frontier closes.

- **Test Definition module**: immutable Test Mode, Content Set, limit, and Rule Set.
- **Target Preparation module**: prepares a deterministic local Test or consumes the exact Test supplied by a Match Authority.
- **Attempt Engine module**: accepts a normalized typing command and monotonic time, then returns the next immutable Attempt transition. It owns admission, corrections, lifecycle, and finish rules.
- **Result Evaluator module**: derives a Result from an Attempt Record. The same rules run locally and under online authority.
- **Local Journal module**: transactionally persists settings, Attempt Records, Results, and synchronization state.
- **Sync Coordinator module**: reconciles stable local records with an Account through a durable outbox, idempotent record identities, retries, and explicit acceptance or rejection states.
- **Match Gateway module**: carries authenticated Match commands and evidence without leaking networking into the Attempt Engine.
- **Match Authority module**: owns competitive Test state, time, accepted evidence, Results, Placement, and rating updates.
- **Terminal Adapter**: decodes terminal input into normalized commands and renders derived state. Terminal escape sequences never enter the domain model.

Apply the deep-module tests:

- Keep each Interface smaller than the behavior it hides.
- Put caller and test access at the same Seam.
- Accept clocks, randomness, storage, and networking dependencies.
- Return transitions and results instead of mutating presentation state.
- Introduce an Adapter only when at least two real implementations justify the Seam.
- Use the deletion test: removing a Module should force its complexity back into several callers.

## Current TypeForge repository state

- The current branch contains an unfinished metrics and policy refactor. Models, session construction, snapshots, policy access, and widget call sites do not yet agree.
- The app has no `pyproject.toml`, automated tests, formatter/linter/type-checker configuration, or CI workflow.
- Imports mix package-qualified and top-level forms.
- `requirements.txt` is an environment freeze rather than a curated direct dependency list.
- Bundled language and quote data is about 11 MiB and needs provenance and redistribution review before release.
- Existing modified and untracked files belong to the user. Preserve them.
- `CONTEXT.md` contains the glossary confirmed during this interview.
- `PRODUCT.md` and `DESIGN.md` do not yet exist.

The local MVP remains the first implementation milestone: one correct, configurable, repeatable Practice flow with tests and packaging. Networking, accounts, synchronization, and competition should shape interfaces now but remain later implementation phases.

## Completion criteria for the design session

The handoff is complete when all of these conditions hold:

1. The Grilling frontier is empty and the user explicitly confirms the shared understanding.
2. `CONTEXT.md` contains every settled project-specific term and no implementation details.
3. `PRODUCT.md` records confirmed product truth, platform, users, purpose, positioning, constraints, evidence, principles, and accessibility.
4. The terminal UX brief covers every surface, state, transition, content range, command, responsive condition, failure mode, and accessibility rule that implementation must not invent.
5. The architecture plan defines the deep Modules, their Interfaces, Seams, Adapters, invariants, error modes, and test surfaces.
6. The roadmap separates the local Practice MVP from synchronization and competitive phases.
7. The documents identify open decisions rather than filling gaps with assumptions.
