from scripts.tech_tree_to_graphviz import (
    AUTO_MARK,
    build_layout,
    emit_dot,
    parse,
    replace_generated_dot,
)


SAMPLE = """\
標題: 測試科技樹
時序: 1960s, 1970s, 年份待補

# 武器
## 步槍
武器 舊式步槍 = old @1968
武器 新式步槍 = new @1972
武器 同年改型 = variant @1972
武器 年份未定 = unknown
old -> new : 繼承
new ~> unknown : 關聯

## 弩
武器 獨立弩 = bow @1969
"""


def test_parse_edge_semantics_and_branches() -> None:
    graph = parse(SAMPLE)

    assert len(graph.nodes) == 5
    assert [edge.kind for edge in graph.edges] == ["inheritance", "related"]
    assert list(graph.branches) == [("武器", "步槍"), ("武器", "弩")]
    assert graph.audit == []


def test_layout_orders_time_and_separates_same_year() -> None:
    graph = parse(SAMPLE)
    layout = build_layout(graph)

    old_x = layout.node_positions[graph.aliases["old"].dot_id][0]
    new_x = layout.node_positions[graph.aliases["new"].dot_id][0]
    variant_x = layout.node_positions[graph.aliases["variant"].dot_id][0]
    unknown_x = layout.node_positions[graph.aliases["unknown"].dot_id][0]
    new_y = layout.node_positions[graph.aliases["new"].dot_id][1]
    variant_y = layout.node_positions[graph.aliases["variant"].dot_id][1]

    assert old_x < new_x < variant_x < unknown_x
    assert new_y != variant_y
    assert layout.branch_positions[("武器", "步槍")] != layout.branch_positions[
        ("武器", "弩")
    ]


def test_unlisted_decade_is_inserted_chronologically() -> None:
    graph = parse(
        """\
時序: 1980s, 2000s, 年份待補
# 工具
## 紀錄
工具 可互動紀錄板 = board @1997
工具 小型紀錄晶片 = chip @2001
"""
    )

    assert build_layout(graph).bands == ["1980s", "1990s", "2000s", "年份待補"]


def test_dot_styles_and_markdown_replacement_are_idempotent() -> None:
    graph = parse(SAMPLE)
    dot = emit_dot(graph)

    assert 'style="solid"' in dot
    assert 'style="dashed"' in dot
    assert "// 左下圖例" in dot

    markdown = f"```tech-tree\n{SAMPLE}```\n"
    once = replace_generated_dot(markdown, dot)
    twice = replace_generated_dot(once, dot)

    assert once == twice
    assert once.count(AUTO_MARK) == 1
