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


# Abbreviation
ABBR_PATTERN = re.compile(
    r"\{\{abbr:(?P<key>[^|{}]+)\|(?P<zh>[^|{}]+)\|(?P<en>[^{}]+)\}\}"
)


def convert_abbreviation(match: Match[str]) -> str:
    key = match.group("key").strip()
    chinese = match.group("zh").strip()
    english = match.group("en").strip()
    return render_abbreviation(key, chinese, english)


def render_abbreviation(key: str, chinese: str, english: str) -> str:
    title = f"{chinese} / {english}"

    return (
        '<abbr class="abbr-term"'
        f' data-key="{html.escape(key, quote=True)}"'
        f' data-zh="{html.escape(chinese, quote=True)}"'
        f' data-en="{html.escape(english, quote=True)}"'
        f' title="{html.escape(title, quote=True)}">'
        f"{html.escape(key)}"
        "</abbr>"
    )


# Existing acronym followed by an annotation, for example:
# UVAP({{anno-w:通用視覺擴展程式|Universal Vision Augment Program}})
ACRONYM_ANNOTATION_PATTERN = re.compile(
    r"(?P<key>[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)"
    r"\(\{\{anno-w:(?P<zh>[^|{}]+)\|(?P<en>[^{}]+)\}\}\)"
)


def convert_acronym_annotation(match: Match[str]) -> str:
    key = match.group("key")
    chinese = match.group("zh").strip()
    english = match.group("en").strip()

    return (
        f"{render_abbreviation(key, chinese, english)}("
        f"{render_annotation('anno-w', chinese, english)})"
    )


# Annotation
ANNOTATION_PATTERN = re.compile(
    r"\{\{(?P<class>anno-[cw]):(?P<anno>[^|{}]+)\|(?P<base>[^{}]+)\}\}"
)


def render_annotation(css_class: str, annotation: str, base: str) -> str:
    return (
        '<span class="ruby-container">'
        f'<span class="{css_class}">'
        f"{html.escape(annotation)}"
        "</span>"
        f"<span>{html.escape(base)}</span>"
        "</span>"
    )


def convert_annotation(match: Match[str]) -> str:
    return render_annotation(
        match.group("class"),
        match.group("anno"),
        match.group("base"),
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
    Rule(ABBR_PATTERN, convert_abbreviation),
    Rule(ACRONYM_ANNOTATION_PATTERN, convert_acronym_annotation),
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


CODE_BLOCK_PATTERN = re.compile(r"```.*?```", re.DOTALL)


def escape_liquid_in_code_blocks(text: str) -> str:
    """Keep literal template-looking text safe for Jekyll/Liquid."""

    def escape_block(match: Match[str]) -> str:
        return (
            match.group(0)
            .replace("{{", "&#123;&#123;")
            .replace("}}", "&#125;&#125;")
        )

    return CODE_BLOCK_PATTERN.sub(escape_block, text)


# File handling
def convert_file(
    source: Path,
    destination: Path,
    *,
    prefix: str = "",
    include_css: bool = True,
    escape_liquid: bool = False,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8")
    converted = convert_inline(text)
    if escape_liquid:
        converted = escape_liquid_in_code_blocks(converted)

    destination.write_text(
        prefix + (CSS_STYLE if include_css else "") + converted,
        encoding="utf-8",
    )


# Conversion modes
STARGAZER_FILENAME = "The Outsiders [Vol. Stargazer].md"
PAGES_INDEX = Path("docs") / "index.md"
PAGES_FRONT_MATTER = """---
layout: default
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
    convert_file(
        source,
        destination,
        prefix=PAGES_FRONT_MATTER,
        include_css=False,
        escape_liquid=True,
    )


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