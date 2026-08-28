import json
from pathlib import Path
from typing import Optional

_CACHE: dict[str, list[str]] = {}
DEFAULT_LANG_DIR = Path(__file__).resolve().parents[1] / "static" / "languages"


def load_word_list(name: str = "english", directory: Optional[Path] = None) -> list[str]:
    """Load and cache a word list from the static datasets."""
    if name in _CACHE:
        return _CACHE[name]

    dir_path = directory or DEFAULT_LANG_DIR
    file_path = dir_path / f"{name}.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Word list file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict) or "words" not in data:
        raise ValueError(f"Invalid word list format in {file_path}")

    words = data["words"]
    if not isinstance(words, list) or not words:
        raise ValueError(f"Empty or non-list words in {file_path}")

    _CACHE[name] = words
    return words
