from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


RUBY_PATTERN = re.compile(r"\{\{ruby:([^|{}]+)\|([^{}]+)\}\}")
DOT_WORD_PATTERN = re.compile(
    r"(?P<word>[^\s．、，,。！？!?]．"
    r"[^\s．、，,。！？!?]．"
    r"[^\s．、，,。！？!?]．"
    r"[^\s．、，,。！？!?])"
)
PROTECTED_PATTERN = re.compile(
    r"```.*?```|`[^`\n]+`|\[\[[^\]]+\]\]",
    re.DOTALL,
)
NAME_PATTERN = re.compile(
    r"^(?P<base>.+?)"
    r"（(?P<reading>[^，,）]+)"
    r"(?:[，,](?P<abbr>[^）]+))?"
    r"）$"
)


def _convert_ruby(match: re.Match[str]) -> str:
    base, reading = match.groups()
    return (
        f"<ruby>{html.escape(base)}"
        f"<rt>{html.escape(reading)}</rt></ruby>"
    )


def _convert_dot_word(match: re.Match[str]) -> str:
    word = match.group("word")
    characters = word.replace("．", "")
    return (
        '<span class="bouten" data-source="'
        f"{html.escape(word, quote=True)}\">{html.escape(characters)}</span>"
    )


def convert_name(text: str) -> str:
    """Convert 中文（English） or 中文（English，ABBR） to ruby HTML."""
    match = NAME_PATTERN.fullmatch(text.strip())
    if not match:
        return text

    base = html.escape(match.group("base"))
    reading = html.escape(match.group("reading"))
    abbreviation = match.group("abbr")

    result = f"<ruby>{base}<rt>{reading}</rt></ruby>"
    if abbreviation:
        result += f"（{html.escape(abbreviation)}）"
    return result


def _convert_unprotected(text: str) -> str:
    text = RUBY_PATTERN.sub(_convert_ruby, text)
    return DOT_WORD_PATTERN.sub(_convert_dot_word, text)


def convert_inline(text: str) -> str:
    """Convert ruby and exactly-four-character dot notation."""
    output: list[str] = []
    cursor = 0
    for match in PROTECTED_PATTERN.finditer(text):
        output.append(_convert_unprotected(text[cursor:match.start()]))
        output.append(match.group(0))
        cursor = match.end()
    output.append(_convert_unprotected(text[cursor:]))
    return "".join(output)


def convert_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        convert_inline(source.read_text(encoding="utf-8")),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert ruby and Japanese emphasis-dot notation."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    convert_file(args.source, args.destination)


if __name__ == "__main__":
    main()
