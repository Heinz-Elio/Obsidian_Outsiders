"""Convert the first draw.io page embedded in an SVG to Graphviz Markdown.

The converter preserves draw.io swimlanes as nested Graphviz clusters and
uses coarse source Y-coordinate bands to retain the diagram's top-to-bottom
timeline without inventing dates.
"""

from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import textwrap
import xml.etree.ElementTree as ET


DEFAULT_SOURCE = Path("線索-Clues and Investigation.drawio.svg")
DEFAULT_OUTPUT = Path("Excalidraw/線索-Graphviz.md")
PAGE_NAME = "Clues and Investigation"
TIME_BAND_HEIGHT = 300
LEGEND_LABEL = "圖例"
SPLIT_TOPIC_NOTES = (
    "線索-人魚公主真相與杜溫",
    "線索-改革派對付保守派策略",
)
SPLIT_CONTAINER_LABELS = {"杜溫"}
MERMAID_TRUTH_GROUP_COLOR = "#86A2CD"
SPLIT_STANDALONE_LABELS = {
    "星降神臨崩壞",
    "諾愛爾、可伶被處以星盡",
    "水妖不斷襲擊人魚公主，使干擾反覆解除",
    "只有埃爾確有能力與動機製造這樣的危機",
    "海底不安全，需要留在陸地",
    "康士坦絲的不滿與懷疑達至峰值",
    "長時間留在陸地",
    "人魚公主違抗命令",
    "人魚公主與人類、彭達拉薩人過於親近",
    "可伶未有按時報告",
    "塞雷亞策劃送兩人到陸地，阿德萊德以管不住諾愛爾解釋",
    "星盡需要五位大長老",
    "康士坦絲對阿德萊德產生不滿",
    "迫阿德萊德下台",
    "與諾愛爾、可伶一同行動",
    "達姬放任人魚公主與他們接觸",
    "埃爾確解封，海都襲擊人魚王國",
    "星羅誕生時水妖與彭達拉薩人出現",
    "烏蘇拉截下報告",
    "阿德萊德叛變證據",
    "對克洛德懷疑加劇，想收回控制權",
    "懷疑與海都事件有關",
    "削弱星降神臨力量",
    "魅影小隊將逃亡的人魚公主帶到陸地",
    "認為人魚公主脫離控制",
    "迫使人魚公主在陸地集結，貿然分開回到王國反而危險",
    "營造必須仰賴北太平洋王國的局面",
    "VPTS企圖綁架",
    "需要有人阻止VPTS成功",
    "彭達拉薩族介入者",
    "人魚公主對長老有所懷疑",
    "米迦勒襲擊人魚公主",
    "暗示人魚公主的真相",
    "水妖掌握人魚公主行蹤",
}
UNIVERSAL_RENDERER_SETTINGS = Path(
    ".obsidian/plugins/universal-renderer/data.json"
)


class _DrawioHTMLParser(HTMLParser):
    BLOCK_TAGS = {"br", "div", "p", "li", "tr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag.lower() in self.BLOCK_TAGS and self.parts:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self.BLOCK_TAGS and self.parts:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def clean_label(value: str | None) -> str:
    if not value:
        return ""
    parser = _DrawioHTMLParser()
    parser.feed(value)
    text = html.unescape("".join(parser.parts))
    text = text.replace("\xa0", " ").replace("\u200b", "")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def wrapped_label(value: str, width: int = 22) -> str:
    if not value:
        return "（原圖無文字）"
    output: list[str] = []
    for line in value.splitlines():
        output.extend(
            textwrap.wrap(
                line,
                width=width,
                break_long_words=True,
                break_on_hyphens=False,
            )
            or [""]
        )
    return "\n".join(output)


def dot_escape(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "")
        .replace("\n", "\\n")
    )


def style_dict(style: str | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in (style or "").split(";"):
        if not item:
            continue
        if "=" in item:
            key, value = item.split("=", 1)
            result[key] = value
        else:
            result[item] = "1"
    return result


def valid_color(value: str | None, fallback: str) -> str:
    if not value or value.lower() in {"none", "default"}:
        return fallback
    if re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        return value.upper()
    return fallback


def geometry(cell: ET.Element) -> tuple[float, float, float, float]:
    geo = cell.find("mxGeometry")
    if geo is None:
        return 0.0, 0.0, 0.0, 0.0

    def number(name: str) -> float:
        try:
            return float(geo.attrib.get(name, "0"))
        except ValueError:
            return 0.0

    return number("x"), number("y"), number("width"), number("height")


def is_container(cell: ET.Element) -> bool:
    style = style_dict(cell.attrib.get("style"))
    return cell.attrib.get("vertex") == "1" and "swimlane" in style


def load_page(source: Path) -> ET.Element:
    svg_root = ET.parse(source).getroot()
    embedded = svg_root.attrib.get("content")
    if not embedded:
        raise ValueError("SVG 根元素沒有 draw.io content 屬性")
    mxfile = ET.fromstring(embedded)
    diagrams = mxfile.findall("diagram")
    if not diagrams:
        raise ValueError("draw.io mxfile 內沒有 diagram")
    diagram = next(
        (item for item in diagrams if item.attrib.get("name") == PAGE_NAME),
        diagrams[0],
    )
    if not list(diagram):
        raise ValueError("目標 diagram 沒有可解析的 mxGraphModel")
    return list(diagram)[0]


def build_dot(graph_model: ET.Element) -> tuple[str, dict[str, object]]:
    cells_in_order = graph_model.findall(".//mxCell")
    cells = {
        cell.attrib["id"]: cell for cell in cells_in_order if "id" in cell.attrib
    }
    vertices = [
        cell for cell in cells_in_order if cell.attrib.get("vertex") == "1"
    ]
    edges = [cell for cell in cells_in_order if cell.attrib.get("edge") == "1"]
    node_ids = {cell.attrib["id"]: f"n{i:03d}" for i, cell in enumerate(vertices, 1)}
    labels = {
        cell.attrib["id"]: clean_label(cell.attrib.get("value")) for cell in vertices
    }

    parent_of = {
        cell_id: cell.attrib.get("parent", "") for cell_id, cell in cells.items()
    }

    absolute_cache: dict[str, tuple[float, float]] = {}

    def absolute_position(cell_id: str, trail: set[str] | None = None) -> tuple[float, float]:
        if cell_id in absolute_cache:
            return absolute_cache[cell_id]
        trail = set() if trail is None else trail
        if cell_id in trail:
            return 0.0, 0.0
        trail.add(cell_id)
        cell = cells[cell_id]
        x, y, _, _ = geometry(cell)
        parent_id = parent_of.get(cell_id, "")
        if parent_id in cells and cells[parent_id].attrib.get("vertex") == "1":
            parent_x, parent_y = absolute_position(parent_id, trail)
            x += parent_x
            y += parent_y
        absolute_cache[cell_id] = (x, y)
        return x, y

    containers = {cell.attrib["id"] for cell in vertices if is_container(cell)}
    legend_containers = {
        cell_id for cell_id in containers if labels.get(cell_id) == LEGEND_LABEL
    }

    def is_split_container(cell_id: str) -> bool:
        if labels.get(cell_id) in SPLIT_CONTAINER_LABELS:
            return True
        style = style_dict(cells[cell_id].attrib.get("style"))
        raw_fill = style.get("fillColor")
        if not raw_fill or raw_fill.lower() in {"none", "default"}:
            raw_fill = style.get("swimlaneFillColor")
        group_color = valid_color(raw_fill, "")
        return not labels.get(cell_id) and group_color == MERMAID_TRUTH_GROUP_COLOR

    def has_ancestor(cell_id: str, ancestors: set[str]) -> bool:
        seen: set[str] = set()
        current = parent_of.get(cell_id, "")
        while current and current not in seen:
            if current in ancestors:
                return True
            seen.add(current)
            current = parent_of.get(current, "")
        return False

    excluded = set(legend_containers)
    excluded.update(
        cell.attrib["id"]
        for cell in vertices
        if has_ancestor(cell.attrib["id"], legend_containers)
    )
    split_containers = {
        cell_id for cell_id in containers if is_split_container(cell_id)
    }
    split_excluded = set(split_containers)
    split_excluded.update(
        cell.attrib["id"]
        for cell in vertices
        if has_ancestor(cell.attrib["id"], split_containers)
    )
    split_excluded.update(
        cell.attrib["id"]
        for cell in vertices
        if labels.get(cell.attrib["id"]) in SPLIT_STANDALONE_LABELS
    )
    excluded.update(split_excluded)

    def nearest_container(cell_id: str) -> str | None:
        seen: set[str] = set()
        current = parent_of.get(cell_id, "")
        while current and current not in seen:
            if current in containers and current not in excluded:
                return current
            seen.add(current)
            current = parent_of.get(current, "")
        return None

    child_containers: dict[str | None, list[str]] = {}
    content_nodes: dict[str | None, list[str]] = {}
    for cell in vertices:
        cell_id = cell.attrib["id"]
        if cell_id in excluded:
            continue
        parent_container = nearest_container(cell_id)
        if cell_id in containers:
            child_containers.setdefault(parent_container, []).append(cell_id)
        else:
            content_nodes.setdefault(parent_container, []).append(cell_id)

    def source_style(cell_id: str) -> tuple[str, str, str]:
        style = style_dict(cells[cell_id].attrib.get("style"))
        raw_fill = style.get("fillColor")
        if not raw_fill or raw_fill.lower() in {"none", "default"}:
            raw_fill = style.get("swimlaneFillColor")
        fill = valid_color(raw_fill, "#FFFFFF")
        stroke = valid_color(style.get("strokeColor"), "#64748B")
        font = valid_color(style.get("fontColor"), "#111827")
        return fill, stroke, font

    def emit_node(cell_id: str, indent: str, title: bool = False) -> list[str]:
        fill, stroke, font = source_style(cell_id)
        label = labels.get(cell_id) or "（原圖無文字）"
        attrs = [
            f'label="{dot_escape(wrapped_label(label, 26 if title else 22))}"',
            'shape="box"',
            f'fillcolor="{fill}"',
            f'color="{stroke}"',
            f'fontcolor="{font}"',
        ]
        if title:
            attrs.extend(['style="filled,bold,rounded"', 'penwidth="1.6"'])
        else:
            attrs.append('style="filled,rounded"')
        return [f"{indent}{node_ids[cell_id]} [{', '.join(attrs)}];"]

    lines = [
        "digraph clues {",
        "  graph [",
        '    rankdir="TB",',
        '    bgcolor="#FFFFFF",',
        '    compound="true",',
        '    newrank="true",',
        '    outputorder="edgesfirst",',
        '    splines="ortho",',
        '    nodesep="0.28",',
        '    ranksep="0.70",',
        '    pad="0.20",',
        '    fontname="Microsoft JhengHei",',
        '    label="線索與調查｜依原圖容器分類，上至下為粗略時序",',
        '    labelloc="t",',
        '    fontsize="20"',
        "  ];",
        "",
        "  node [",
        '    fontname="Microsoft JhengHei",',
        '    fontsize="10",',
        '    margin="0.10,0.07"',
        "  ];",
        "",
        "  edge [",
        '    fontname="Microsoft JhengHei",',
        '    fontsize="8",',
        '    color="#64748B",',
        '    arrowsize="0.60"',
        "  ];",
        "",
    ]

    def emit_container(cell_id: str, indent: str = "  ") -> None:
        fill, stroke, _ = source_style(cell_id)
        cluster_name = f"cluster_{node_ids[cell_id]}"
        label = labels.get(cell_id) or "未命名群組（原圖無標題）"
        lines.extend(
            [
                f"{indent}subgraph {cluster_name} {{",
                f'{indent}  label="{dot_escape(wrapped_label(label, 30))}";',
                f'{indent}  color="{stroke}";',
                f'{indent}  fillcolor="{fill}22";',
                f'{indent}  fontcolor="#111827";',
                f'{indent}  fontname="Microsoft JhengHei";',
                f'{indent}  fontsize="12";',
                f'{indent}  style="filled,rounded";',
                f'{indent}  penwidth="1.4";',
                "",
            ]
        )
        lines.extend(emit_node(cell_id, indent + "  ", title=True))
        for node_id in content_nodes.get(cell_id, []):
            lines.extend(emit_node(node_id, indent + "  "))
        for child_id in child_containers.get(cell_id, []):
            lines.append("")
            emit_container(child_id, indent + "  ")
        lines.extend([f"{indent}}}", ""])

    for root_container in child_containers.get(None, []):
        emit_container(root_container)

    lines.extend(
        [
            "  // 原圖未放入任何事件／場地容器的節點；保留在根圖，不另行臆測分類。",
        ]
    )
    root_nodes = content_nodes.get(None, [])
    for cell_id in root_nodes:
        lines.extend(emit_node(cell_id, "  "))
    lines.append("")

    complete_edges = 0
    split_edges = 0
    incomplete_edges: list[tuple[str, str, str]] = []
    lines.append("  // 原圖連線：所有邊的文字皆為空，因此不增添關係標籤。")
    for index, edge in enumerate(edges, 1):
        source = edge.attrib.get("source", "")
        target = edge.attrib.get("target", "")
        if source in split_excluded or target in split_excluded:
            split_edges += 1
            continue
        if (
            not source
            or not target
            or source not in node_ids
            or target not in node_ids
            or source in excluded
            or target in excluded
        ):
            incomplete_edges.append(
                (
                    f"e{index:03d}",
                    labels.get(source, source or "缺失"),
                    labels.get(target, target or "缺失"),
                )
            )
            continue
        edge_style = style_dict(edge.attrib.get("style"))
        attrs: list[str] = []
        stroke = edge_style.get("strokeColor")
        if stroke and stroke.lower() not in {"none", "default"}:
            attrs.append(f'color="{valid_color(stroke, "#64748B")}"')
        if edge_style.get("dashed") == "1":
            attrs.append('style="dashed"')
        if edge_style.get("endArrow") == "none":
            attrs.append('arrowhead="none"')
        attr_text = f" [{', '.join(attrs)}]" if attrs else ""
        lines.append(f"  {node_ids[source]} -> {node_ids[target]}{attr_text};")
        complete_edges += 1

    # Retain only the broad vertical chronology of top-level containers/nodes.
    representatives = [
        cell_id
        for cell_id in child_containers.get(None, []) + root_nodes
        if labels.get(cell_id)
    ]
    if representatives:
        min_y = min(absolute_position(cell_id)[1] for cell_id in representatives)
        bands: dict[int, list[str]] = {}
        for cell_id in representatives:
            _, y = absolute_position(cell_id)
            band = math.floor((y - min_y) / TIME_BAND_HEIGHT)
            bands.setdefault(band, []).append(cell_id)

        lines.extend(
            [
                "",
                "  // 粗略時序約束：依原圖頂層項目的 Y 座標分帶，上方較早、下方較晚。",
            ]
        )
        anchor_ids: list[str] = []
        for sequence, band in enumerate(sorted(bands)):
            anchor = f"time_anchor_{sequence:02d}"
            anchor_ids.append(anchor)
            ordered = sorted(bands[band], key=lambda item: absolute_position(item)[0])
            references = "; ".join([anchor, *(node_ids[item] for item in ordered)])
            lines.append(
                f'  {anchor} [shape="point", width="0.01", label="", style="invis"];'
            )
            lines.append(f"  {{ rank=same; {references}; }}")
        for first, second in zip(anchor_ids, anchor_ids[1:]):
            lines.append(
                f'  {first} -> {second} [style="invis", weight="100", minlen="2"];'
            )

    lines.extend(
        [
            "",
            "  // 原圖圖例",
            "  subgraph cluster_legend {",
            '    label="原圖分類圖例";',
            '    color="#CBD5E1";',
            '    style="rounded,dashed";',
            '    fontname="Microsoft JhengHei";',
            '    legend_evidence [label="證物", shape="box", style="filled", fillcolor="#CCE5FF"];',
            '    legend_evidence_detail [label="證物細節", shape="box", style="filled", fillcolor="#CCCCFF"];',
            '    legend_scene [label="現場", shape="box", style="filled", fillcolor="#E6FFCC"];',
            '    legend_scene_detail [label="現場細節", shape="box", style="filled", fillcolor="#FFFFCC"];',
            '    legend_person [label="重要人物", shape="box", style="filled", fillcolor="#E6E6E6"];',
            '    legend_event [label="事件", shape="box", style="filled", fillcolor="#FFE6CC"];',
            "  }",
            "}",
        ]
    )

    stats: dict[str, object] = {
        "vertices": len(vertices),
        "rendered_vertices": len(vertices) - len(excluded),
        "text_vertices": sum(
            1
            for cell in vertices
            if cell.attrib["id"] not in excluded and labels.get(cell.attrib["id"])
        ),
        "containers": len(containers - legend_containers - split_containers),
        "edges": len(edges),
        "complete_edges": complete_edges,
        "split_edges": split_edges,
        "incomplete_edges": incomplete_edges,
        "time_bands": len(set(
            math.floor(
                (absolute_position(cell_id)[1] - min(
                    absolute_position(item)[1] for item in representatives
                ))
                / TIME_BAND_HEIGHT
            )
            for cell_id in representatives
        )) if representatives else 0,
    }
    return "\n".join(lines), stats


def build_markdown(source: Path, dot: str, stats: dict[str, object]) -> str:
    incomplete = stats["incomplete_edges"]
    assert isinstance(incomplete, list)
    audit_lines = [
        f"- `{edge_id}`：`{source_label}` → `{target_label}`"
        for edge_id, source_label, target_label in incomplete
    ]
    audit = "\n".join(audit_lines) or "- 無"
    topic_links = "、".join(f"[[{note}]]" for note in SPLIT_TOPIC_NOTES)
    return f"""---
tags:
  - investigation
  - graphviz
  - clues
source: "[[{source.name}]]"
cssclasses:
  - graphviz-large-preview
---

# 線索與調查（Graphviz）

本圖由 `{source.name}` 第一頁 `{PAGE_NAME}` 轉換。

- 依原圖容器保留事件、場地、人物與證物分類。
- 上至下沿用原圖的粗略時序；不把空間位置改寫成精確日期。
- 原圖未置於容器的節點保留在根圖，不擅自分類。
- 專題推理已拆至 {topic_links}，並在專題筆記中區分原圖、設定與未決內容。
- 原圖連線沒有文字標籤，因此只保留方向、顏色與虛實線，不補寫「支持／矛盾」等語意。
- 本圖有文字節點：{stats["text_vertices"]}（其中容器 {stats["containers"]}）；完整連線：{stats["complete_edges"]}；拆出連線：{stats["split_edges"]}；粗略時序帶：{stats["time_bands"]}。

## Graphviz 圖

```dot
{dot}
```

## 轉換稽核

以下連線在原始 mxGraphModel 中缺少來源或目標，未加入圖中，以免猜測：

{audit}

> [!NOTE]
> 要重新同步 SVG，可在 vault 根目錄執行：
> `python scripts/drawio_svg_to_graphviz.py --check`
"""


def graphviz_check(dot: str) -> tuple[bool, str]:
    executable = shutil.which("dot")
    if not executable and UNIVERSAL_RENDERER_SETTINGS.exists():
        try:
            settings = json.loads(
                UNIVERSAL_RENDERER_SETTINGS.read_text(encoding="utf-8")
            )
            configured = Path(settings.get("dotPath", ""))
            if configured.is_file():
                executable = str(configured)
        except (OSError, ValueError, TypeError):
            executable = None
    if not executable:
        return False, "找不到 dot；已略過 Graphviz 執行驗證"
    result = subprocess.run(
        [executable, "-Tsvg"],
        input=dot.encode("utf-8"),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        check=False,
    )
    message = result.stderr.decode("utf-8", errors="replace").strip()
    if result.returncode != 0:
        raise RuntimeError(f"Graphviz 驗證失敗：\n{message}")
    return True, message or "Graphviz DOT 驗證通過"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    graph_model = load_page(args.source)
    dot, stats = build_dot(graph_model)
    markdown = build_markdown(args.source, dot, stats)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8", newline="\n")

    print(
        f"已寫入 {args.output}："
        f"{stats['text_vertices']} 個有文字節點、"
        f"{stats['containers']} 容器、"
        f"{stats['complete_edges']} 完整連線"
    )
    if args.check:
        checked, message = graphviz_check(dot)
        print(message)
        return 0 if checked or "略過" in message else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
