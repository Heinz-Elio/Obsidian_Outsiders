from pathlib import Path

from app.chunker import chunk_document
from app.model import Document


def _document(text: str) -> Document:
    return Document(
        path=Path("01_character/test.md"),
        title="Test note",
        text=text,
        tags=[],
        aliases=[],
        links=[],
        headings=[],
        modified=0.0,
        category="character",
        metadata={},
        source_id="source",
        entity_names=["Test note"],
        relation_tags=[],
    )


def _body(chunk) -> str:
    parts = chunk.text.split("\n", 2 if chunk.heading else 1)
    return parts[-1]


def test_short_note_stays_single_chunk_despite_headings():
    chunks = chunk_document(
        _document("# Summary\nShort text.\n## Details\nMore text."),
        500,
        75,
    )

    assert len(chunks) == 1
    assert chunks[0].heading == ""
    assert "# Summary" in chunks[0].text
    assert "## Details" in chunks[0].text


def test_empty_document_has_no_chunks():
    assert chunk_document(_document(" \n\n "), 500, 75) == []


def test_long_document_skips_empty_heading_sections():
    text = "# Empty\n\n## Content\n" + ("x" * 2200)
    chunks = chunk_document(_document(text), 500, 75)

    assert chunks
    assert all(chunk.heading != "Empty" for chunk in chunks)
    assert all(_body(chunk) for chunk in chunks)


def test_section_under_window_is_not_split_at_overlap_step():
    text = "# Target\n" + ("a" * 1800) + "\n# Other\n" + ("b" * 300)
    chunks = chunk_document(_document(text), 500, 75)

    target = [chunk for chunk in chunks if chunk.heading == "Target"]
    assert len(target) == 1
    assert len(_body(target[0])) == 1800


def test_long_document_preserves_heading_boundaries():
    text = "# Alpha\n" + ("a" * 1100) + "\n# Beta\n" + ("b" * 1100)
    chunks = chunk_document(_document(text), 500, 75)

    assert [chunk.heading for chunk in chunks] == ["Alpha", "Beta"]
    assert [chunk.chunk_index for chunk in chunks] == [0, 1]


def test_long_section_uses_configured_overlap():
    chunks = chunk_document(_document("x" * 4500), 500, 75)
    bodies = [_body(chunk) for chunk in chunks]

    assert len(chunks) == 3
    assert bodies[0][-300:] == bodies[1][:300]
    assert bodies[1][-300:] == bodies[2][:300]


def test_chunk_ids_are_deterministic():
    document = _document("# Alpha\n" + ("a" * 1100) + "\n# Beta\n" + ("b" * 1100))

    first = chunk_document(document, 500, 75)
    second = chunk_document(document, 500, 75)

    assert [chunk.id for chunk in first] == [chunk.id for chunk in second]
