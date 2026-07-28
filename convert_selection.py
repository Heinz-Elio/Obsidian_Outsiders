from __future__ import annotations

import argparse
import sys

from format_converter import convert_name


def read_clipboard() -> str:
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    try:
        return root.clipboard_get()
    finally:
        root.destroy()


def write_clipboard(text: str) -> None:
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    try:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
    finally:
        root.destroy()


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    parser = argparse.ArgumentParser(
        description="Convert selected normalized name text to ruby HTML."
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to convert. Defaults to clipboard contents.",
    )
    parser.add_argument(
        "--clipboard",
        action="store_true",
        help="Read from clipboard and write converted result back.",
    )
    args = parser.parse_args()

    source = args.text if args.text is not None else read_clipboard()
    result = convert_name(source.strip())
    if result == source.strip():
        print("No normalized name pattern matched.", file=sys.stderr)
        return 1

    if args.clipboard or args.text is None:
        write_clipboard(result)

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
