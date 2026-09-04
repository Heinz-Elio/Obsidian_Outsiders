"""One-off migration: export the draw.io SVG into the clue DSL used by
clues_to_graphviz.py, so nothing has to be retyped by hand.

Only the original legend colours are mapped to types; everything else is
exported as 未分類 for the author to reclassify. Edges carry no relation
because the original diagram has no edge labels.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawio_svg_to_graphviz import (  # noqa: E402
    DEFAULT_SOURCE,
    LEGEND_LABEL,
    SPLIT_STANDALONE_LABELS,
    clean_label,
    is_container,
    load_page,
    style_dict,
    valid_color,
)

LEGEND_TYPES = {
    "#FFE6CC": "事件",
    "#CCE5FF": "證據",
    "#CCCCFF": "證據",
    "#E6E6E6": "實體",
    "#E6FFCC": "實體",
    "#FFFFCC": "實體",
    "#CCFF99": "實體",
}
SUBSETS = {"reform": SPLIT_STANDALONE_LABELS}


def safe_label(label: str) -> str:
    text = " ".join(label.split())
    return text.replace("->", "→").replace(" = ", "＝").replace(" | ", "｜")


def export(
    graph_model: ET.Element,
    subset: set[str] | None,
    title: str,
    container_color: str | None = None,
    container_labels: set[str] | None = None,
    component_labels: set[str] | None = None,
) -> str:
    cells = [c for c in graph_model.findall(".//mxCell") if "id" in c.attrib]
    by_id = {c.attrib["id"]: c for c in cells}
    vertices = [c for c in cells if c.attrib.get("vertex") == "1"]
    edges = [c for c in cells if c.attrib.get("edge") == "1"]
    labels = {c.attrib["id"]: safe_label(clean_label(c.attrib.get("value"))) for c in vertices}
    containers = {c.attrib["id"] for c in vertices if is_container(c)}
    legend = {cid for cid in containers if labels[cid] == LEGEND_LABEL}

    def ancestors(cid: str) -> list[str]:
        chain: list[str] = []
        current = by_id[cid].attrib.get("parent", "")
        while current in by_id and by_id[current].attrib.get("vertex") == "1":
            chain.append(current)
            current = by_id[current].attrib.get("parent", "")
        return chain[::-1]

    def node_type(cell: ET.Element) -> str:
        fill = valid_color(style_dict(cell.attrib.get("style")).get("fillColor"), "")
        return LEGEND_TYPES.get(fill, "未分類")

    def container_fill(cid: str) -> str:
        style = style_dict(by_id[cid].attrib.get("style"))
        fill = style.get("fillColor")
        if not fill or fill.lower() in {"none", "default"}:
            fill = style.get("swimlaneFillColor")
        return valid_color(fill, "")

    root_component: set[str] = set()
    if component_labels:
        # 已獨立拆出的改革派策略節點也在根層，連通時不得把它們拉進來
        root_nodes = {
            c.attrib["id"] for c in vertices
            if c.attrib["id"] not in containers and labels[c.attrib["id"]]
            and labels[c.attrib["id"]] not in SPLIT_STANDALONE_LABELS
            and not any(a in containers for a in ancestors(c.attrib["id"]))
        }
        adjacency: dict[str, set[str]] = {}
        for edge in edges:
            s, t = edge.attrib.get("source", ""), edge.attrib.get("target", "")
            if s in root_nodes and t in root_nodes:
                adjacency.setdefault(s, set()).add(t)
                adjacency.setdefault(t, set()).add(s)
        stack = [cid for cid in root_nodes if any(labels[cid].startswith(seed) for seed in component_labels)]
        while stack:
            current = stack.pop()
            if current in root_component:
                continue
            root_component.add(current)
            stack.extend(adjacency.get(current, set()) - root_component)

    def keep(cid: str) -> bool:
        if cid in containers or not labels.get(cid):
            return False
        chain = ancestors(cid)
        if any(a in legend for a in chain):
            return False
        if container_color and not any(
            a in containers and container_fill(a) == container_color.upper() for a in chain
        ):
            return False
        if container_labels or component_labels:
            in_container = any(a in containers and labels[a] in (container_labels or set()) for a in chain)
            if not in_container and cid not in root_component:
                return False
        return subset is None or labels[cid] in subset

    kept = [c.attrib["id"] for c in vertices if keep(c.attrib["id"])]
    seen: dict[str, str] = {}
    duplicates: list[str] = []
    for cid in kept:
        if labels[cid] in seen:
            duplicates.append(labels[cid])
        seen.setdefault(labels[cid], cid)

    groups: dict[tuple[str, ...], list[str]] = {}
    for cid in kept:
        path = tuple(labels[a] or "未命名群組" for a in ancestors(cid) if a in containers)
        groups.setdefault(path, []).append(cid)

    out = [f"標題: {title}", "// 由 draw.io SVG 匯出；未分類 = 原圖非圖例顏色，請自行改類型", ""]
    for path in sorted(groups, key=lambda p: (len(p), p)):
        if path:
            out.append(f"{'#' * len(path)} {path[-1]}")
        for cid in groups[path]:
            if seen[labels[cid]] != cid:
                continue
            out.append(f"{node_type(by_id[cid])} {labels[cid]}")
        out.append("")
    if duplicates:
        out.append("// 以下標籤在原圖重複出現，只保留第一個：" + "、".join(sorted(set(duplicates))))

    kept_set = set(kept)
    dropped = 0
    interfaces: list[str] = []
    out.append("")
    for edge in edges:
        src, dst = edge.attrib.get("source", ""), edge.attrib.get("target", "")
        if src in kept_set and dst in kept_set:
            out.append(f"{labels[src]} -> {labels[dst]}")
        elif (src in kept_set) != (dst in kept_set) and labels.get(src) and labels.get(dst):
            outside = labels[dst] if src in kept_set else labels[src]
            interfaces.append(f"// 接口: {labels[src]} -> {labels[dst]}　（「{outside}」在本主題之外）")
        else:
            dropped += 1
    if interfaces:
        out += ["", "// 跨主題接口：需要時把對方寫成「未決 XXX（見 [[另一篇]]）」再連線"] + interfaces
    out.append(f"// 原圖連線中另有 {dropped} 條因端點缺失或不在本子集而未匯出")
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, required=True, help="輸出的 Markdown 筆記")
    parser.add_argument("--subset", choices=sorted(SUBSETS), help="只匯出預設子集")
    parser.add_argument("--title", default="線索與調查")
    parser.add_argument("--container-color", help="只匯出位於此填色容器內的節點，例如 #86A2CD")
    parser.add_argument("--containers", help="以逗號分隔的頂層容器標籤，匯出其內所有節點")
    parser.add_argument("--component", action="append", default=[], help="根層節點標籤（可為前綴）；匯出其所在的連通群，可重複")
    args = parser.parse_args()

    dsl = export(
        load_page(args.source),
        SUBSETS.get(args.subset),
        args.title,
        args.container_color,
        {c.strip() for c in args.containers.split(",")} if args.containers else None,
        set(args.component) or None,
    )
    note = (
        "---\ntags:\n  - investigation\n  - clues-dsl\ncssclasses:\n  - graphviz-large-preview\n---\n\n"
        f"# {args.title}\n\n"
        "> [!NOTE] 寫法\n"
        "> 只需維護下方 ```clues 區塊，執行 `python scripts/clues_to_graphviz.py <本檔>` 即重生下方圖。\n"
        "> - `# 群組`：cluster，`##` 為巢狀。\n"
        "> - `類型 內容 = 別名 @時點 #狀態`：類型可用 證據／事件／實體／假設／未決／矛盾；別名、時點、狀態皆可省略。\n"
        "> - `A -支持-> B | C`：關係可用 支持／導致／推導／矛盾／時序／屬於，省略即為「關係未定」的灰虛線。\n"
        "> - 填色與形狀＝類型；邊框粗細與虛實＝狀態（已確認／預定／推論／補丁）。\n\n"
        "```clues\n" + dsl + "```\n"
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(note, encoding="utf-8", newline="\n")
    print(f"已寫入 {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
