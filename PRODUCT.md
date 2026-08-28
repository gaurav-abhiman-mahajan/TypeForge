# Product

<!-- impeccable:product-schema 1 -->

## Platform

terminal

## Users

Terminal-native software engineers and competitive typists who practice keyboard efficiency from the command line and seek low-latency, distraction-free typing metrics and synchronous ranked racing.

## Product Purpose

TypeForge provides a terminal-native, local-first typing practice and competitive racing environment. It turns raw typing input into immutable event records to compute precise qualified and raw speed, keystroke accuracy, and error diagnostics without relying on browser DOM overhead or mouse interaction.

## Positioning

Unlike browser-based typing tests (such as Monkeytype) or simple terminal typing scripts, TypeForge operates on an event-driven, immutable-transition core with local-first offline journaling, server-authoritative 4-typist ranked matchmaking, and deep typing diagnostics.

## Operating Context

Runs directly in Linux/POSIX terminal emulators (with macOS and Windows standard terminal compatibility) inside standard shells (Bash/Zsh/Fish) or terminal multiplexers (tmux/zellij). Operates primarily at an 80×24 minimum column/row footprint, fully driven via keyboard shortcuts without mouse dependency.

## Capabilities and Constraints

- **Local Practice**: Immediate launch into active test (zero home/splash blocking). Word, Time, Quote, Zen, and Custom modes with configurable difficulty rules (Normal, Expert, Master), punctuation, numbers, and backspace behavior.
- **Engine Invariants**: Pure deterministic state transitions; Attempt starts on first valid keystroke; corrections mutate buffer but preserve error history in Attempt Records; terminal states freeze metrics and reject subsequent input.
- **Diagnostics & Results**: Qualified Speed (WPM), Raw Speed (WPM), Keystroke Accuracy (%), Character Outcomes (`correct`, `incorrect`, `extra`, `missed`), and error cluster analysis.
- **Sync & Privacy**: 100% offline-first local journal with idempotent UUIDv7 records and outbox sync. Private by default; public profiles expose only aggregates and public match summaries.
- **Ranked Competition**: Public 4-typist synchronous races; server-authoritative Match Authority; monotonic clock integrity validation.
- **Hardware & Terminal Constraints**: Minimum 80×24 dimensions; maximum centered 70–80 character reading column on wide displays; truecolor default with ANSI-256 and monochrome fallback.

## Brand Commitments

- Name: TypeForge
- Tone & Atmosphere: Industrial craft, minimalist, high-contrast, distraction-free.
- Interaction: 100% keyboard-accessible; explicit control bindings (`Ctrl+K`, `Ctrl+R`, `Ctrl+Q`, `Esc`, `Enter`, `Shift+Enter`).

## Evidence on Hand

- Core event-driven prototype in `app/core/`.
- Monkeytype functional benchmark for modes, scoring, and rule mechanics.
- Bundled word lists and quote datasets in `app/static/`.

## Product Principles

1. **Local-First & Immediate**: Launch straight into typing; zero network latency or splash screens block practice.
2. **Immutable Truth**: Keystroke mistakes are never erased from history, ensuring true Keystroke Accuracy and deterministic replays.
3. **Pure Separation of Concerns**: Core engine is pure Python with zero UI dependencies; terminal presentation is a thin, swappable adapter.
4. **Authoritative Fairness**: Practice is private and client-side; ranked racing is strictly server-authoritative with tamper-evident event streaming.

## Accessibility & Inclusion

- Complete keyboard navigation without mouse requirement.
- Redundant typographic and symbol styling (underlines, dimming, cursor focus) alongside color coding so all states are distinct in monochrome and high-contrast terminal environments.
- Graceful viewport resizing notices.
