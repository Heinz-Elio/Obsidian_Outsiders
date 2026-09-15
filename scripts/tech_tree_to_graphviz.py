"""Render ``tech-tree`` Markdown blocks into fixed-layout Graphviz DOT/SVG.

DSL, one statement per line:

    標題: IU7 科技樹
    時序: 遠古, 1960s, 1970s, 1980s, 2000s, 年份待補
    輸出DOT: IU7_tech_tree.dot
    輸出SVG: iu7_tech_tree.svg
    # 種類
    ## 細項分支
    武器 M2法力弩 = m2 @1972
    m2 -> m3 : 改型
    m2 ~> bm1 : 關聯項目

``->`` is a solid inheritance edge. ``~>`` is a dashed related-item edge.
Headings define category/branch lanes; node type controls its colour.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
import re
import subprocess
import sys
import textwrap

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawio_svg_to_graphviz import dot_escape  # noqa: E402


FONT = "Microsoft JhengHei"
AUTO_MARK = "// tech-tree-auto 由上方 tech-tree 區塊生成，請勿手改"
TYPE_STYLES = {
    "技術": ("#1D4ED8", "#60A5FA"),
    "材料": ("#92400E", "#F59E0B"),
    "武器": ("#7F1D1D", "#EF4444"),
    "彈藥": ("#5B21B6", "#A78BFA"),
    "工具": ("#065F46", "#10B981"),
    "機器": ("#0E7490", "#22D3EE"),
}
TYPE_ALIASES = {
    **{name: name for name in TYPE_STYLES},
    "科技": "技術",
    "物料": "材料",
    "機械": "機器",
    "設備": "機器",
}
UNKNOWN_TIMES = {"", "?", "未知", "年代未定", "年份待補"}
DIRECTIVE_RE = re.compile(
    r"^(?P<key>標題|時序|輸出DOT|輸出SVG|DOT|SVG)[:：]\s*(?P<value>.+)$",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^(?P<level>#+)\s+(?P<title>.+)$")
NODE_RE = re.compile(r"^(?P<type>\S+)\s+(?P<rest>.+)$")
TAIL_RE = re.compile(r"\s+(?:@(?P<time>\S+)|=\s*(?P<alias>\S+))$")
EDGE_RE = re.compile(
    r"^(?P<src>\S+)\s*(?P<op>->|~>)\s*(?P<targets>[^:：]+?)"
    r"(?:\s*[:：]\s*(?P<label>.+))?$"
)
YEAR_RE = re.compile(r"^(?P<year>\d{4})年?$")
DECADE_RE = re.compile(r"^(?P<decade>\d{4})s$", re.IGNORECASE)


@dataclass
class Node:
    label: str
    type: str
    alias: str
    time: str | None
    category: str
    branch: str
    dot_id: str
    index: int
    line: int


@dataclass
class Edge:
    src: str
    dst: str
    kind: str
    label: str
    line: int


@dataclass
class Graph:
    title: str = "科技樹"
    time_order: list[str] = field(default_factory=list)
    dot_output: str | None = None
    svg_output: str | None = None
    nodes: list[Node] = field(default_factory=list)
    aliases: dict[str, Node] = field(default_factory=dict)
    branches: dict[tuple[str, str], list[Node]] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    audit: list[str] = field(default_factory=list)


@dataclass
class Layout:
    bands: list[str]
    node_positions: dict[str, tuple[float, float]]
    branch_positions: dict[tuple[str, str], float]
    category_positions: dict[str, float]
    band_positions: dict[str, tuple[float, float]]
    header_y: float
    legend_y: float


def split_list(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[,，、]", value) if part.strip()]


def parse(text: str) -> Graph:
    graph = Graph()
    category = "未分類"
    branch = "其他"

    for line_no, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("//"):
            continue

        if match := DIRECTIVE_RE.match(line):
            key = match["key"].upper()
            value = match["value"].strip()
            if key == "標題":
                graph.title = value
            elif key == "時序":
                graph.time_order = split_list(value)
            elif key in {"輸出DOT", "DOT"}:
                graph.dot_output = value
            else:
                graph.svg_output = value
            continue

        if match := HEADING_RE.match(line):
            level = len(match["level"])
            title = match["title"].strip()
            if level == 1:
                category, branch = title, "其他"
            elif level == 2:
                branch = title
            else:
                graph.audit.append(f"第 {line_no} 行：僅支援 # 種類與 ## 細項分支")
                branch = title
            continue

        if match := EDGE_RE.match(line):
            kind = "inheritance" if match["op"] == "->" else "related"
            label = (match["label"] or "").strip()
            for target in (part.strip() for part in match["targets"].split("|")):
                if target:
                    graph.edges.append(
                        Edge(match["src"], target, kind, label, line_no)
                    )
            continue

        if match := NODE_RE.match(line):
            node_type = TYPE_ALIASES.get(match["type"])
            if node_type is None:
                graph.audit.append(f"第 {line_no} 行：未知項目類型「{match['type']}」")
                continue

            rest = match["rest"].strip()
            alias = time = None
            while tail := TAIL_RE.search(rest):
                alias = tail["alias"] or alias
                time = tail["time"] or time
                rest = rest[: tail.start()].rstrip()

            if not rest:
                graph.audit.append(f"第 {line_no} 行：項目缺少名稱")
                continue

            alias = alias or rest
            if alias in graph.aliases:
                graph.audit.append(f"第 {line_no} 行：別名「{alias}」重複")
                continue

            node = Node(
                label=rest,
                type=node_type,
                alias=alias,
                time=time,
                category=category,
                branch=branch,
                dot_id=f"n{len(graph.nodes) + 1:03d}",
                index=len(graph.nodes),
                line=line_no,
            )
            graph.nodes.append(node)
            graph.aliases[alias] = node
            graph.aliases.setdefault(rest, node)
            graph.branches.setdefault((category, branch), []).append(node)
            continue

        graph.audit.append(f"第 {line_no} 行：無法解析：{line}")

    resolve_edges(graph)
    return graph


def resolve_edges(graph: Graph) -> None:
    valid: list[Edge] = []
    for edge in graph.edges:
        missing = [name for name in (edge.src, edge.dst) if name not in graph.aliases]
        if missing:
            graph.audit.append(
                f"第 {edge.line} 行：未定義項目「{'、'.join(missing)}」，連線已略過"
            )
            continue
        valid.append(edge)
    graph.edges = valid


def node_band(node: Node, bands: list[str]) -> str:
    time = (node.time or "").strip()
    unknown = next((band for band in bands if band in UNKNOWN_TIMES), None)

    if time in UNKNOWN_TIMES:
        return unknown or "年份待補"
    if time in bands:
        return time
    if YEAR_RE.match(time):
        year = int(YEAR_RE.match(time)["year"])
        decade = f"{year // 10 * 10}s"
        if decade in bands:
            return decade
        return decade
    if "年前" in time or time == "遠古":
        return "遠古" if "遠古" in bands else time
    return time


def time_key(node: Node) -> tuple[int, int | str]:
    time = (node.time or "").strip()
    if match := YEAR_RE.match(time):
        return (0, int(match["year"]))
    if "千萬年前" in time:
        return (-2, time)
    if "年前" in time or time == "遠古":
        return (-1, time)
    if time in UNKNOWN_TIMES:
        return (2, node.index)
    return (1, time)


def insert_band_in_time_order(bands: list[str], band: str) -> None:
    """Insert an unseen decade chronologically; unknown always remains last."""
    if band in bands:
        return
    match = DECADE_RE.match(band)
    if match:
        decade = int(match["decade"])
        for index, existing in enumerate(bands):
            existing_match = DECADE_RE.match(existing)
            if existing_match and int(existing_match["decade"]) > decade:
                bands.insert(index, band)
                return
    unknown_index = next(
        (index for index, value in enumerate(bands) if value in UNKNOWN_TIMES),
        len(bands),
    )
    bands.insert(unknown_index, band)


def assign_branch_tracks(
    graph: Graph,
    branch_key: tuple[str, str],
    nodes: list[Node],
    node_x: dict[str, float],
) -> tuple[dict[str, int], int]:
    """Place forks and multiple roots on separate tracks within one branch."""
    node_ids = {node.dot_id for node in nodes}
    incoming: dict[str, list[str]] = defaultdict(list)
    outgoing: dict[str, list[str]] = defaultdict(list)
    for edge in graph.edges:
        src = graph.aliases[edge.src]
        dst = graph.aliases[edge.dst]
        if (
            src.dot_id not in node_ids
            or dst.dot_id not in node_ids
            or (src.category, src.branch) != branch_key
            or (dst.category, dst.branch) != branch_key
        ):
            continue
        incoming[dst.dot_id].append(src.dot_id)
        outgoing[src.dot_id].append(dst.dot_id)

    by_id = {node.dot_id: node for node in nodes}
    indegree = {node.dot_id: len(incoming[node.dot_id]) for node in nodes}
    ready = sorted(
        (node.dot_id for node in nodes if indegree[node.dot_id] == 0),
        key=lambda dot_id: (node_x[dot_id], by_id[dot_id].index),
    )
    ordered: list[str] = []
    while ready:
        current = ready.pop(0)
        ordered.append(current)
        for child in outgoing[current]:
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
                ready.sort(key=lambda dot_id: (node_x[dot_id], by_id[dot_id].index))
    ordered.extend(
        node.dot_id
        for node in sorted(nodes, key=lambda item: (node_x[item.dot_id], item.index))
        if node.dot_id not in ordered
    )

    tracks: dict[str, int] = {}
    next_track = 0
    for dot_id in ordered:
        predecessors = [source for source in incoming[dot_id] if source in tracks]
        if not predecessors:
            tracks[dot_id] = next_track
            next_track += 1
            continue

        primary = predecessors[0]
        siblings = outgoing[primary]
        if siblings.index(dot_id) == 0:
            tracks[dot_id] = tracks[primary]
        else:
            tracks[dot_id] = next_track
            next_track += 1

    return tracks, max(1, next_track)


def build_layout(graph: Graph) -> Layout:
    bands = list(graph.time_order)
    if not bands:
        has_ancient = any(
            node.time and ("年前" in node.time or node.time == "遠古")
            for node in graph.nodes
        )
        decades = sorted(
            {
                int(YEAR_RE.match(node.time)["year"]) // 10 * 10
                for node in graph.nodes
                if node.time and YEAR_RE.match(node.time)
            }
        )
        bands = (["遠古"] if has_ancient else []) + [f"{year}s" for year in decades]
        bands.append("年份待補")

    for node in graph.nodes:
        band = node_band(node, bands)
        if band not in bands:
            insert_band_in_time_order(bands, band)

    branch_time_counts: dict[tuple[str, str], Counter[tuple[str, str]]] = {}
    for key, nodes in graph.branches.items():
        branch_time_counts[key] = Counter(
            (node_band(node, bands), (node.time or "年份待補")) for node in nodes
        )

    slots_by_band: dict[str, list[tuple[str, int]]] = {}
    for band in bands:
        time_values = {
            (node.time or "年份待補")
            for node in graph.nodes
            if node_band(node, bands) == band
        }
        ordered_times = sorted(
            time_values,
            key=lambda value: min(
                (
                    time_key(node)
                    for node in graph.nodes
                    if node_band(node, bands) == band
                    and (node.time or "年份待補") == value
                ),
                default=(2, value),
            ),
        )
        slots: list[tuple[str, int]] = []
        for value in ordered_times or [band]:
            repetitions = max(
                (
                    counts[(band, value)]
                    for counts in branch_time_counts.values()
                ),
                default=1,
            )
            slots.extend((value, occurrence) for occurrence in range(repetitions))
        slots_by_band[band] = slots

    x_step = 190.0
    band_gap = 65.0
    cursor = 300.0
    slot_x: dict[tuple[str, str, int], float] = {}
    band_positions: dict[str, tuple[float, float]] = {}
    for band in bands:
        slots = slots_by_band[band]
        first = cursor
        for value, occurrence in slots:
            slot_x[(band, value, occurrence)] = cursor
            cursor += x_step
        last = cursor - x_step
        width_points = max(170.0, last - first + 170.0)
        band_positions[band] = ((first + last) / 2.0, width_points / 72.0)
        cursor += band_gap

    occurrences: defaultdict[tuple[tuple[str, str], str, str], int] = defaultdict(int)
    node_x: dict[str, float] = {}
    for node in graph.nodes:
        branch_key = (node.category, node.branch)
        band = node_band(node, bands)
        value = node.time or "年份待補"
        occurrence_key = (branch_key, band, value)
        occurrence = occurrences[occurrence_key]
        occurrences[occurrence_key] += 1
        node_x[node.dot_id] = slot_x[(band, value, occurrence)]

    branch_tracks: dict[tuple[str, str], dict[str, int]] = {}
    branch_track_counts: dict[tuple[str, str], int] = {}
    for key, nodes in graph.branches.items():
        tracks, count = assign_branch_tracks(graph, key, nodes, node_x)
        branch_tracks[key] = tracks
        branch_track_counts[key] = count

    branches = list(graph.branches)
    branch_positions: dict[tuple[str, str], float] = {}
    branch_bases: dict[tuple[str, str], float] = {}
    track_step = 82.0
    branch_gap = 58.0
    category_gap = 82.0
    y = 180.0
    lower_category: str | None = None
    for key in reversed(branches):
        if lower_category is not None and key[0] != lower_category:
            y += category_gap
        count = branch_track_counts[key]
        branch_bases[key] = y
        branch_positions[key] = y + (count - 1) * track_step / 2.0
        y += count * track_step + branch_gap
        lower_category = key[0]

    node_positions: dict[str, tuple[float, float]] = {}
    for node in graph.nodes:
        key = (node.category, node.branch)
        count = branch_track_counts[key]
        track = branch_tracks[key][node.dot_id]
        node_y = branch_bases[key] + (count - 1 - track) * track_step
        node_positions[node.dot_id] = (node_x[node.dot_id], node_y)

    category_positions: dict[str, float] = {}
    for category in dict.fromkeys(key[0] for key in branches):
        category_keys = [key for key in branches if key[0] == category]
        top = max(
            branch_bases[key] + (branch_track_counts[key] - 1) * track_step
            for key in category_keys
        )
        category_positions[category] = top + 72.0

    header_y = max(category_positions.values(), default=y) + 110.0

    return Layout(
        bands=bands,
        node_positions=node_positions,
        branch_positions=branch_positions,
        category_positions=category_positions,
        band_positions=band_positions,
        header_y=header_y,
        legend_y=35.0,
    )


def wrapped_label(node: Node) -> str:
    wrapped = "\n".join(
        textwrap.wrap(node.label, width=16, break_long_words=True, break_on_hyphens=False)
    )
    return wrapped + "\n" + (node.time or "年份待補")


def emit_dot(graph: Graph) -> str:
    layout = build_layout(graph)
    out = [
        AUTO_MARK,
        "// 以 neato -n2 讀取固定位置；時間由左至右，分支由上至下。",
    ]
    out.extend(f"// 稽核：{message}" for message in graph.audit)
    out.extend(
        [
            "digraph technology_tree {",
            "  graph [",
            '    layout="neato", bgcolor="#10151C", outputorder="edgesfirst",',
            '    overlap="false", splines="ortho", pad="0.20", margin="0.10",',
            f'    fontname="{FONT}", fontcolor="#F3F4F6", label="{dot_escape(graph.title)}",',
            '    labelloc="t", fontsize="18"',
            "  ];",
            f'  node [fontname="{FONT}", fixedsize="true", pin="true", shape="box",',
            '        width="2.25", height="0.82", style="rounded,filled",',
            '        fontsize="10", fontcolor="#FFFFFF", penwidth="2"];',
            f'  edge [fontname="{FONT}", fontsize="8", fontcolor="#D1D5DB",',
            '        color="#9CA3AF", penwidth="2.0", arrowsize="0.65"];',
            "",
            "  // 時間標題",
        ]
    )

    for index, band in enumerate(layout.bands):
        x, width = layout.band_positions[band]
        out.append(
            f'  time_{index:02d} [label="{dot_escape(band)}", pos="{x:.1f},{layout.header_y:.1f}!", '
            f'width="{width:.3f}", height="0.55", fillcolor="#252D38", '
            'color="#667085", fontsize="12"];'
        )

    category_index: dict[str, int] = {}
    for category, _ in graph.branches:
        category_index.setdefault(category, len(category_index))

    for category, cat_index in category_index.items():
        out.extend(
            [
                "",
                f"  subgraph cluster_{cat_index:02d} {{",
                f'    label="{dot_escape(category)}"; color="#374151"; fontcolor="#D1D5DB";',
                f'    fontname="{FONT}"; fontsize="12"; style="rounded,dashed";',
                f'    category_{cat_index:02d} [label="{dot_escape(category)}", '
                f'pos="95.0,{layout.category_positions[category]:.1f}!", width="1.85", '
                'height="0.48", fillcolor="#111827", color="#64748B"];',
            ]
        )
        for (node_category, branch), nodes in graph.branches.items():
            if node_category != category:
                continue
            y = layout.branch_positions[(node_category, branch)]
            branch_id = f"branch_{cat_index:02d}_{list(graph.branches).index((node_category, branch)):02d}"
            out.append(
                f'    {branch_id} [label="{dot_escape(branch)}", pos="95.0,{y:.1f}!", '
                'width="1.85", height="0.60", fillcolor="#202833", color="#4B5563"];'
            )
            for node in nodes:
                fill, stroke = TYPE_STYLES[node.type]
                x, node_y = layout.node_positions[node.dot_id]
                out.append(
                    f'    {node.dot_id} [label="{dot_escape(wrapped_label(node))}", '
                    f'pos="{x:.1f},{node_y:.1f}!", fillcolor="{fill}", color="{stroke}"];'
                )
        out.append("  }")

    out.extend(["", "  // 明示連線；位置不由連線推斷。"])
    for edge in graph.edges:
        src = graph.aliases[edge.src].dot_id
        dst = graph.aliases[edge.dst].dot_id
        attrs = (
            'style="solid", color="#9CA3AF"'
            if edge.kind == "inheritance"
            else 'style="dashed", color="#C084FC"'
        )
        if edge.label:
            attrs += f', xlabel="{dot_escape(edge.label)}"'
        out.append(f"  {src} -> {dst} [{attrs}];")

    legend_y = layout.legend_y
    out.extend(
        [
            "",
            "  // 左下圖例",
            f'  legend_title [label="圖例", pos="70.0,{legend_y + 35:.1f}!", '
            'width="1.10", height="0.45", fillcolor="#202833", color="#4B5563"];',
            f'  legend_s1 [shape="point", width="0.05", height="0.05", '
            f'pos="165.0,{legend_y + 50:.1f}!", fillcolor="#9CA3AF", color="#9CA3AF"];',
            f'  legend_s2 [shape="point", width="0.05", height="0.05", '
            f'pos="225.0,{legend_y + 50:.1f}!", fillcolor="#9CA3AF", color="#9CA3AF"];',
            f'  legend_st [shape="plaintext", label="技術繼承", pos="300.0,{legend_y + 50:.1f}!", '
            'width="1.20", height="0.30", fontcolor="#D1D5DB"];',
            f'  legend_r1 [shape="point", width="0.05", height="0.05", '
            f'pos="165.0,{legend_y + 10:.1f}!", fillcolor="#C084FC", color="#C084FC"];',
            f'  legend_r2 [shape="point", width="0.05", height="0.05", '
            f'pos="225.0,{legend_y + 10:.1f}!", fillcolor="#C084FC", color="#C084FC"];',
            f'  legend_rt [shape="plaintext", label="關聯項目", pos="300.0,{legend_y + 10:.1f}!", '
            'width="1.20", height="0.30", fontcolor="#D1D5DB"];',
            '  legend_s1 -> legend_s2 [style="solid", color="#9CA3AF"];',
            '  legend_r1 -> legend_r2 [style="dashed", color="#C084FC"];',
            "}",
        ]
    )
    return "\n".join(out)


def replace_generated_dot(markdown: str, dot: str) -> str:
    lines = markdown.splitlines()
    result: list[str] = []
    i = 0
    while i < len(lines):
        result.append(lines[i])
        if lines[i].strip() != "```tech-tree":
            i += 1
            continue
        i += 1
        while i < len(lines):
            result.append(lines[i])
            if lines[i].strip() == "```":
                i += 1
                break
            i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        if (
            i + 1 < len(lines)
            and lines[i].strip() == "```dot"
            and lines[i + 1].startswith(AUTO_MARK)
        ):
            i += 2
            while i < len(lines) and lines[i].strip() != "```":
                i += 1
            if i < len(lines):
                i += 1
        result.extend(["", "```dot", dot, "```"])
    suffix = "\n" if markdown.endswith("\n") else ""
    return "\n".join(result) + suffix


def extract_block(markdown: str) -> str:
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != "```tech-tree":
            continue
        end = index + 1
        while end < len(lines) and lines[end].strip() != "```":
            end += 1
        if end == len(lines):
            raise ValueError("tech-tree 區塊沒有結束標記")
        return "\n".join(lines[index + 1 : end])
    raise ValueError("找不到 ```tech-tree 區塊")


def output_path(note: Path, configured: str | None, suffix: str) -> Path:
    return note.parent / configured if configured else note.with_suffix(suffix)


def render_svg(dot_path: Path, svg_path: Path, project_root: Path) -> str:
    executable = project_root / "Graphviz" / "bin" / "neato.exe"
    if not executable.exists():
        raise RuntimeError(f"找不到 Graphviz：{executable}")
    result = subprocess.run(
        [str(executable), "-n2", "-Tsvg", str(dot_path), "-o", str(svg_path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Graphviz 生成失敗")
    return result.stderr.strip()


def process_note(note: Path, project_root: Path, check: bool) -> list[str]:
    original = note.read_text(encoding="utf-8")
    graph = parse(extract_block(original))
    dot = emit_dot(graph)
    updated = replace_generated_dot(original, dot)
    note.write_text(updated, encoding="utf-8", newline="\n")

    dot_path = output_path(note, graph.dot_output, ".dot")
    svg_path = output_path(note, graph.svg_output, ".svg")
    dot_path.write_text(dot + "\n", encoding="utf-8", newline="\n")
    warning = render_svg(dot_path, svg_path, project_root)

    messages = [
        f"{note}：{len(graph.nodes)} 項目、{len(graph.edges)} 連線",
        f"DOT：{dot_path}",
        f"SVG：{svg_path}",
    ]
    messages.extend(f"稽核：{item}" for item in graph.audit)
    if warning:
        messages.append(f"Graphviz 警告：{warning}")
    if check and (not dot_path.exists() or not svg_path.exists()):
        raise RuntimeError("輸出檔案不存在")
    return messages


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notes", nargs="+", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parent.parent

    try:
        for note in args.notes:
            for message in process_note(note, project_root, args.check):
                print(message)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"錯誤：{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
