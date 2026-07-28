from __future__ import annotations

from pathlib import Path

from format_converter import convert_inline


PROJECT_ROOT = Path(__file__).resolve().parent
INPUT_DIR = PROJECT_ROOT / "Setting"
OUTPUT_DIR = PROJECT_ROOT / "rendered"


def convert_vault() -> int:
    converted = 0
    for source in sorted(INPUT_DIR.rglob("*.md")):
        relative = source.relative_to(INPUT_DIR)
        destination = OUTPUT_DIR / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            convert_inline(source.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
        converted += 1
    return converted


if __name__ == "__main__":
    count = convert_vault()
    print(f"Converted {count} Markdown files to {OUTPUT_DIR}")
