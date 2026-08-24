from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_EXTENSIONS = {".mw", ".markwhen"}


def clean_links(text: str) -> str:
    # [[角色]] -> 角色
    return re.sub(r"\[\[\s*(.*?)\s*\]\]", r"\1", text)


def convert_line(line: str):
    line = line.strip()

    if not line:
        return ""

    # heading
    if line.startswith("#"):
        return line

    # remove wiki syntax
    line = clean_links(line)

    # date/range/timestamp parser
    m = re.match(
        r"^([0-9]{4}(?:-[0-9]{2})?(?:-[0-9]{2})?(?:\s+[0-9]{2}:[0-9]{2})?"
        r"(?:\s*/\s*[0-9]{4}(?:-[0-9]{2})?(?:-[0-9]{2})?)?)\s*:\s*(.+)$",
        line,
    )

    if m:
        date = m.group(1)
        content = m.group(2)

        # tags -> [TAG]
        content = re.sub(r"#([A-Za-z0-9_\-]+)", r"[\1]", content)

        return f"- {date} — {content}"

    return f"- {line}"


def convert_markwhen(text: str) -> str:
    out = []

    for raw in text.splitlines():
        converted = convert_line(raw)

        if converted:
            out.append(converted)

    return "\n".join(out) + "\n"


def convert_file(path: Path):
    text = path.read_text(encoding="utf-8")

    md = convert_markwhen(text)

    output_path = path.with_suffix(".md")
    output_path.write_text(md, encoding="utf-8")

    print(f"Converted: {path.name} -> {output_path.name}")


def main():
    INPUT_DIR = PROJECT_ROOT / "Setting"

    EXCLUDE_FOLDERS = {
        ".obsidian",
        ".git",
        ".smart-env",
        ".venv",
        "copilot",
        "Excalidraw",
        "Markwhen",
        "Templates",
        "trash",
        "archive",
        "00_總覽"
    }

    files = []
    for path in INPUT_DIR.rglob("*.mw"):
        if any(part in EXCLUDE_FOLDERS for part in path.parts):
            continue
        files.append(path)

    if not files:
        print("No Markwhen files found.")
        return

    for file in files:
        convert_file(file)


if __name__ == "__main__":
    main()