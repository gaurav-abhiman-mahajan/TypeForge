import json
import random
from pathlib import Path

LANGUAGE_DIR = Path(__file__).resolve().parents[2] / "static" / "languages"


def random_sentence_english():
    path = LANGUAGE_DIR / "english.json"

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
        words: list[str] = data.get("words")

        k = random.randint(20, 50)
        sentence = random.choices(words, k=k)

        return " ".join(sentence)
