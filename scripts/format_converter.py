from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Match


# css styles
CSS_STYLE = r"""
<style>
.ruby-container {
  display: inline-flex;
  flex-direction: column;
  text-align: center;
  vertical-align: bottom;
}

.anno-c {
  font-size: 0.7em;
  opacity: 0.8;
  line-height: 1;
  letter-spacing: 2em;
  margin-right: -2em;
}

.anno-w {
  font-size: 0.7em;
  opacity: 0.8;
  line-height: 1;
}

.emphasis-dot {
  background-image: radial-gradient(circle at center, currentColor 1.5px, transparent 1.5px);
  background-position: 0 bottom;
  background-size: 1em 0.3em;
  background-repeat: repeat-x;
  padding-bottom: 0.25em;
}

.spoiler {
  background: #222;
  border-radius: 0.2em;
  color: transparent;
  cursor: pointer;
  padding: 0 0.15em;
}

.spoiler:hover,
.spoiler:focus,
.spoiler:focus-visible {
  background: transparent;
  color: inherit;
  outline: none;
}
</style>
"""

# Protected Markdown regions
PROTECTED_PATTERN = re.compile(
    r"""
    ```.*?```            |   # fenced code block
    `[^`\n]+`            |   # inline code
    \[\[[^\]]+\]\]       |   # Obsidian wikilink
    \[[^\]]+\]\([^)]+\)  |   # Markdown link
    <[^>]+>                  # existing HTML
    """,
    re.DOTALL | re.VERBOSE,
)


# Transformation rules
@dataclass
class Rule:
    pattern: re.Pattern[str]
    handler: Callable[[Match[str]], str]


# Annotation
ANNOTATION_PATTERN = re.compile(
    r"\{\{(?P<class>anno-[cw]):(?P<anno>[^|{}]+)\|(?P<base>[^{}]+)\}\}"
)


def convert_annotation(match: Match[str]) -> str:
    css_class = match.group("class")
    annotation = match.group("anno")
    base = match.group("base")

    return (
        '<span class="ruby-container">'
        f'<span class="{css_class}">'
        f"{html.escape(annotation)}"
        "</span>"
        f"<span>{html.escape(base)}</span>"
        "</span>"
    )


# Emphasis dot
DOT_PATTERN = re.compile(r"\{\{(?:dot|anno-dot):(?P<text>[^{}]+)\}\}")

def convert_dot(match: Match[str]) -> str:
    text = match.group("text")

    return (
        '<span class="emphasis-dot">'
        f"{html.escape(text)}"
        "</span>"
    )


# Center
CENTER_PATTERN = re.compile(r"\{\{center:(?P<text>[^{}]+)\}\}")

def convert_center(match: Match[str]) -> str:
    text = match.group("text")

    return (
        '<p align="center"><strong>'
        f"{html.escape(text)}"
        "</strong><p>"
    )


# Spoiler
SPOILER_PATTERN = re.compile(r"\|\|(?P<text>[^|\n]+?)\|\|")


def convert_spoiler(match: Match[str]) -> str:
    text = match.group("text")

    return (
        '<span class="spoiler" tabindex="0" role="button">'
        f"{html.escape(text)}"
        "</span>"
    )

# Rules order matters

RULES = [
    Rule(SPOILER_PATTERN, convert_spoiler),
    Rule(ANNOTATION_PATTERN, convert_annotation),
    Rule(DOT_PATTERN, convert_dot),
    Rule(CENTER_PATTERN, convert_center),
]


# Conversion
def convert_unprotected(text: str) -> str:
    """
    Apply rules repeatedly.
    Allows nested syntax.
    """

    while True:
        previous = text

        for rule in RULES:
            text = rule.pattern.sub(rule.handler, text)

        if text == previous:
            break

    return text


def convert_inline(text: str) -> str:
    output: list[str] = []

    cursor = 0

    for match in PROTECTED_PATTERN.finditer(text):
        output.append(
            convert_unprotected(
                text[cursor:match.start()]
            )
        )

        output.append(match.group(0))

        cursor = match.end()

    output.append(
        convert_unprotected(text[cursor:])
    )

    return "".join(output)


# File handling
def convert_file(
    source: Path,
    destination: Path,
    *,
    prefix: str = "",
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8")
    destination.write_text(
        prefix + CSS_STYLE + convert_inline(text),
        encoding="utf-8",
    )


# Conversion modes
STARGAZER_FILENAME = "The Outsiders [Vol. Stargazer].md"
PAGES_INDEX = Path("docs") / "index.md"
PAGES_FRONT_MATTER = """---
title: "The Outsiders [Vol. Stargazer]"
---
"""


def convert_all(project_root: Path) -> None:
    input_dir = project_root / "Story"
    output_dir = project_root / "HackMD"

    for source in sorted(input_dir.glob("*.md")):
        relative = source.relative_to(input_dir)
        destination = output_dir / relative
        convert_file(source, destination)


def convert_main(project_root: Path) -> None:
    """Convert the main story to the GitHub Pages entry point."""
    source = project_root / "Story" / STARGAZER_FILENAME
    destination = project_root / PAGES_INDEX
    convert_file(source, destination, prefix=PAGES_FRONT_MATTER)


# CLI
def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Story Markdown files.")
    parser.add_argument(
        "--mode",
        choices=("all", "standard"),
        default="all",
        help="Conversion scope; 'standard' writes the fixed story to docs/index.md.",
    )
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parent.parent

    if args.mode == "standard":
        convert_main(project_root)
    else:
        convert_all(project_root)


if __name__ == "__main__":
    main()