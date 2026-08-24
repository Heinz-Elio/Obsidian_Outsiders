import json
from pathlib import Path

from app.config import load_config
from app.editor import classify_question, find_document
from app.loader import load_documents


def _documents():
    return list(load_documents(load_config().vault.path))


def test_editor_eval_targets_and_negative_case():
    cases = json.loads(Path("editor_eval_cases.json").read_text(encoding="utf-8"))
    documents = _documents()
    for case in cases:
        document = find_document(documents, case["target"])
        if case["expected_category"] is None:
            assert document is None
        else:
            assert document is not None
            assert document.category == case["expected_category"]


def test_suspense_question_classification():
    assert classify_question("這件事為什麼會發生？") == "因果未知"
    assert classify_question("之後會發生甚麼？") == "未來未知"
    assert classify_question("過去是如何發展至此？") == "過去未知"
