# 03-target-provider-boundary

Type: task
Status: resolved
Blocked by: 01

## Question

How do we decouple target content generation from presentation widgets into a clean, testable domain package?

### Scope
- Create `app/content/` with `TargetProvider` protocol, `WordListTargetProvider`, and loader.
- Support deterministic seeded generation for tests and configurable word counts (default 25).
- Bundle reviewed, lightweight, and attributed English wordlist.
- Remove ad-hoc generator in `app/widgets/generator/sentence.py`.

## Answer

- Implemented `app/content/loader.py` with memory caching and schema validation for word lists.
- Implemented `app/content/targets.py` with `TargetProvider` protocol, `WordListTargetProvider` with RNG injection, non-repeat guarantees, and `get_default_target_provider`.
- Removed legacy `app/widgets/generator/` ad-hoc module.
- All target generation behaviors verified with deterministic tests in `tests/test_content.py`.
