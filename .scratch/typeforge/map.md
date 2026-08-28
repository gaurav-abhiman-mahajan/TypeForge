## Destination

Implement the Playable Local Practice MVP (Phase 1) for TypeForge: pure immutable session engine, decoupled target content provider, predictable lifecycle & controls (Backspace/Escape/Restart), clean Textual UI loop, packaging, and test suite.

## Notes

- Domain: Terminal-native typing practice and competitive typing.
- Disciplines: `domain-modeling`, `codebase-design`, `impeccable`, `tdd`, `unslop`.
- Stack: Python 3.10+, Textual, pytest.
- Constraints: Maintain pure core domain with no Textual dependencies in `app/core/` and `app/models/`. Keep working tree clean.

## Decisions so far

<!-- the index — one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [01-session-policy-and-lifecycle](issues/01-session-policy-and-lifecycle.md) — Aligned default policy (backspace/escape enabled), immutable transitions, and terminal freeze invariants.
- [02-core-typing-metrics-refactor](issues/02-core-typing-metrics-refactor.md) — Unified TypingMetrics, SessionSnapshot, Qualified/Raw WPM, Accuracy, and Character Outcomes.
- [03-target-provider-boundary](issues/03-target-provider-boundary.md) — Decoupled target generation to `app/content/` with caching, deterministic RNG, and verified English corpus.
- [04-textual-ui-practice-and-results](issues/04-textual-ui-practice-and-results.md) — Built Practice and Result Textual screens with seamless keyboard transitions (Enter next, Ctrl+R repeat, Esc/Ctrl+Q exit).
- [05-packaging-tests-and-quality-gates](issues/05-packaging-tests-and-quality-gates.md) — Standardized `pyproject.toml`, console entry point `typeforge`, curated requirements, and 31 automated pytest tests.

## Not yet specified

- Phase 2: Local Modes (Time, Quote, Zen, Custom), SQLite persistence, and Targeted Practice algorithms.
- Phase 3: OAuth Device Authorization and journal outbox cloud synchronization.
- Phase 4: Server-authoritative 4-player ranked matchmaking and Race protocol.

## Out of scope

- Direct Monkeytype DOM/browser features, large theme catalogs, sound packs, novelty modifiers.
- Private multiplayer lobbies or bot-filled ranked queues.
