from app.router import normalise_scope, resolve_scope


def test_explicit_scope_aliases():
    assert normalise_scope("角色") == "characters"
    assert normalise_scope("events") == "events"
    assert normalise_scope("unknown") is None


def test_single_category_is_detected():
    assert resolve_scope("星降神臨是甚麼法術？", None) == "srunes"
    assert resolve_scope("介紹北太平洋王國的組織", None) == "organizations"


def test_ambiguous_query_uses_all_documents():
    assert resolve_scope("海因茨和諾愛爾的關係", None) is None


def test_explicit_unknown_scope_falls_back_to_all():
    assert resolve_scope("anything", "not-a-scope") is None
