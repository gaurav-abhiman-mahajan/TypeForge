# TypeForge

TypeForge is a terminal-native, local-first typing practice and competitive typing application built in Python using the Textual framework.

Unlike traditional terminal typing scripts, TypeForge is designed around an event-driven and immutable state transition engine. Keyboard input is converted into immutable domain events, validated by policies, and evaluated into deterministic states and accurate metrics (Qualified Speed, Raw Speed, Keystroke Accuracy, and Character Outcomes).

## Installation & Setup

Requirements: Python 3.10+

```bash
# Clone the repository
git clone https://github.com/your-username/TypeForge.git
cd TypeForge

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

## Running TypeForge

Launch the application directly from your shell:

```bash
typeforge
```

Or run via module entry point:

```bash
python -m app.main
```

## Controls

| Key | Action |
| --- | --- |
| `Printable Character` | Append character to typing buffer |
| `Backspace` | Erase previous character (enabled by default) |
| `Esc` | Abort active test / Exit from result screen |
| `Ctrl+R` | Restart test with a fresh target |
| `Ctrl+Q` | Quit TypeForge immediately |
| `Enter` (Result Screen) | Start next test with fresh words |
| `r` / `Ctrl+R` (Result Screen) | Repeat the exact same target |

## Verified Features (v0.2.0 MVP)

* **Terminal-Native TUI**: Centered, responsive layout built with Textual and high-contrast color/character styling.
* **Deterministic Content Engine**: Independent `TargetProvider` boundary with cached, validated English corpora and seeded RNG support.
* **Pure Transition Engine**: Pure immutable typing state transitions with strict terminal lifecycle states (`IDLE`, `RUNNING`, `FINISHED`, `ABORTED`).
* **Accurate Metrics**:
  * **Qualified Speed (WPM)**: Positionally correct characters / 5 / active minutes.
  * **Raw Speed (WPM)**: Total typed characters / 5 / active minutes.
  * **Keystroke Accuracy (%)**: Correct character ratio against evaluable keystrokes.
  * **Character Outcomes**: Detailed breakdown (`correct`, `incorrect`, `extra`, `missed`).
* **Post-Test Result Flow**: Detailed results view with single-keystroke retry, repeat, and exit actions.

## Running Tests

Run the automated test suite with pytest:

```bash
pytest
```
