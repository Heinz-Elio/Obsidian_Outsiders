from pathlib import Path

import merge_notes


def _note(path: str, body_chars: int) -> merge_notes.Note:
    relative = Path(path)
    return merge_notes.Note(
        path=relative,
        group=relative.parent.as_posix(),
        title=relative.stem,
        body_chars=body_chars,
        rendered=f"## {relative.stem}\nSource: {relative.as_posix()}\n\nFact",
    )


def test_wikilink_alias_preserves_canonical_target():
    assert (
        merge_notes.resolve_wikilinks("[[SWI調查事務所|SWI]]")
        == "SWI (SWI調查事務所)"
    )


def test_long_notes_stay_standalone_and_short_notes_merge():
    outputs = merge_notes.build_outputs(
        [
            _note("IU7/01_character/short.md", 100),
            _note("IU7/01_character/long.md", merge_notes.LONG_NOTE_CHARS),
        ]
    )

    assert sum(output.kind == "standalone" for output in outputs) == 1
    assert sum(output.kind == "category_bundle" for output in outputs) == 1


def test_output_falls_back_to_source_limit(monkeypatch):
    monkeypatch.setattr(merge_notes, "NOTEBOOKLM_SOURCE_LIMIT", 2)
    notes = [
        _note("one/a.md", 100),
        _note("two/b.md", 100),
        _note("three/c.md", 100),
    ]

    outputs = merge_notes.build_outputs(notes)

    assert len(outputs) == 2
    assert all(output.kind == "mixed_bundle" for output in outputs)


def test_clean_body_drops_empty_template_sections():
    cleaned = merge_notes.clean_body(
        "# Example\n## 無\n-\n## Empty\nNone\n## Facts\nUseful fact",
        "Example",
    )

    assert "## 無" not in cleaned
    assert "Empty" not in cleaned
    assert "Useful fact" in cleaned
