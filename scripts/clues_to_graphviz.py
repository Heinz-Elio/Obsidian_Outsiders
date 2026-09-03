"""Render a minimal clue DSL (```clues blocks in Markdown) into Graphviz DOT.

Layout is delegated entirely to Graphviz; the author only writes content.

DSL, one statement per line:

    標題: 改革派策略              directive (標題 / 方向 TB|LR / 時序 a, b, c)
    # 群組名                     cluster; more '#' = nested cluster
    證據 內容 = 別名 @時點 #狀態  node; only 類型 and 內容 are required
    A -支持-> B | C              edge; relation optional ("A -> B"); '|' = many targets
    // 註解

類型: 證據 事件 實體 假設 未決 矛盾 未分類  (aliases below)
狀態: 已確認 預定 推論 補丁
關係: 支持 導致 推導 矛盾 時序 屬於 (others are printed as edge labels)
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys
import textwrap

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawio_svg_to_graphviz import dot_escape  # noqa: E402

FONT = "Microsoft JhengHei, Noto Sans CJK TC, PingFang TC, sans-serif"
LABEL_WIDTH = 14
AUTO_MARK = "// clues-auto"

TYPE_ALIASES = {
    "證據": "證據", "物證": "證據", "文件": "證據", "證言": "證據", "觀察": "證據",
    "事件": "事件", "行動": "事件",
    "實體": "實體", "人物": "實體", "地點": "實體", "組織": "實體", "物件": "實體",
    "假設": "假設", "主張": "假設", "結論": "假設", "推論": "假設", "解釋": "假設",
    "未決": "未決", "缺口": "未決", "問題": "未決",
    "矛盾": "矛盾", "澄清": "矛盾",
    "未分類": "未分類", "節點": "未分類",
}

# type -> (fill, stroke, shape, extra style)
TYPE_STYLE = {
    "證據": ("#DBEAFE", "#2563EB", "note", ""),
    "事件": ("#FFEDD5", "#EA580C", "box", "rounded"),
    "實體": ("#DCFCE7", "#16A34A", "ellipse", ""),
    "假設": ("#EDE9FE", "#7C3AED", "box", ""),
    "未決": ("#F1F5F9", "#64748B", "octagon", ""),
    "矛盾": ("#FEE2E2", "#DC2626", "box", ""),
    "未分類": ("#FFFFFF", "#94A3B8", "box", ""),
}
DEFAULT_STATUS = {
    "證據": "已確認", "事件": "已確認", "實體": "已確認",
    "假設": "推論", "未決": "推論", "矛盾": "補丁", "未分類": "推論",
}
# status -> (penwidth, extra style, peripheries)
STATUS_STYLE = {
    "已確認": ("2.0", "", 1),
    "預定": ("1.0", "", 1),
    "推論": ("1.2", "dashed", 1),
    "補丁": ("2.6", "", 1),
}
# relation -> attributes
RELATION_STYLE = {
    "支持": 'color="#1F2937"',
    "導致": 'color="#EA580C"',
    "推導": 'color="#1F2937", style="dashed"',
    "矛盾": 'color="#DC2626", arrowhead="tee", penwidth="1.6"',
    "時序": 'color="#94A3B8", style="dotted"',
    "屬於": 'color="#94A3B8", style="dotted", arrowhead="none"',
}
UNDEFINED_RELATION = 'color="#94A3B8", style="dashed"'

NODE_RE = re.compile(r"^(?P<type>\S+)\s+(?P<rest>.+)$")
EDGE_RE = re.compile(r"^(?P<src>.+?)\s+-(?P<rel>[^\s>]*?)-?>\s+(?P<dst>.+)$")
TAIL_RE = re.compile(r"\s+(?:#(?P<status>\S+)|@(?P<time>\S+)|=\s*(?P<alias>\S+))$")
DIRECTIVE_RE = re.compile(r"^(?P<key>標題|方向|時序)[:：]\s*(?P<value>.+)$")
HEADING_RE = re.compile(r"^(?P<level>#+)\s+(?P<title>.+)$")


@dataclass
class Node:
    label: str
    type: str
    status: str
    time: str | None
    cluster: tuple[str, ...]
    dot_id: str
    line: int


@dataclass
class Edge:
    src: str
    dst: str
    relation: str
    line: int


@dataclass
class Graph:
    title: str = ""
    rankdir: str = "TB"
    time_order: list[str] = field(default_factory=list)
    nodes: dict[str, Node] = field(default_factory=dict)
    aliases: dict[str, str] = field(default_factory=dict)
    clusters: dict[tuple[str, ...], list[str]] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    audit: list[str] = field(default_factory=list)


def parse(text: str) -> Graph:
    graph = Graph()
    stack: list[str] = []
    for line_no, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("//"):
            continue
        if m := DIRECTIVE_RE.match(line):
            key, value = m["key"], m["value"].strip()
            if key == "標題":
                graph.title = value
            elif key == "方向":
                graph.rankdir = "LR" if value.upper() == "LR" else "TB"
            else:
                graph.time_order = [t.strip() for t in re.split(r"[,，、]", value) if t.strip()]
            continue
        if m := HEADING_RE.match(line):
            level = len(m["level"])
            del stack[level - 1:]
            stack.append(m["title"].strip())
            graph.clusters.setdefault(tuple(stack), [])
            continue
        if m := EDGE_RE.match(line):
            targets = [t.strip() for t in m["dst"].split("|") if t.strip()]
            for target in targets:
                graph.edges.append(Edge(m["src"].strip(), target, m["rel"], line_no))
            continue
        if m := NODE_RE.match(line):
            type_name = TYPE_ALIASES.get(m["type"])
            if type_name is None:
                graph.audit.append(f"第 {line_no} 行：無法辨識的類型或語法：{line}")
                continue
            rest = m["rest"].strip()
            status = time = alias = None
            while tail := TAIL_RE.search(rest):
                status = tail["status"] or status
                time = tail["time"] or time
                alias = tail["alias"] or alias
                rest = rest[: tail.start()].rstrip()
            label = rest
            if not label:
                graph.audit.append(f"第 {line_no} 行：節點沒有內容")
                continue
            if status and status not in STATUS_STYLE:
                graph.audit.append(f"第 {line_no} 行：未知狀態 #{status}，改用預設")
                status = None
            if label in graph.nodes:
                graph.audit.append(f"第 {line_no} 行：重複定義節點「{label}」")
                continue
            node = Node(
                label=label,
                type=type_name,
                status=status or DEFAULT_STATUS[type_name],
                time=time,
                cluster=tuple(stack),
                dot_id=f"n{len(graph.nodes) + 1:03d}",
                line=line_no,
            )
            graph.nodes[label] = node
            if alias and alias != label:
                if alias in graph.aliases or alias in graph.nodes:
                    graph.audit.append(f"第 {line_no} 行：別名「{alias}」已被使用")
                else:
                    graph.aliases[alias] = label
            graph.clusters.setdefault(tuple(stack), []).append(label)
            continue
        graph.audit.append(f"第 {line_no} 行：無法解析：{line}")
    resolve_edges(graph)
    return graph


def resolve_edges(graph: Graph) -> None:
    for edge in graph.edges:
        for attr in ("src", "dst"):
            name = getattr(edge, attr)
            label = graph.aliases.get(name, name)
            if label not in graph.nodes:
                graph.audit.append(f"第 {edge.line} 行：「{name}」未定義，已自動加入為未決節點")
                graph.nodes[label] = Node(
                    label=label, type="未決", status="推論", time=None,
                    cluster=(), dot_id=f"n{len(graph.nodes) + 1:03d}", line=edge.line,
                )
                graph.clusters.setdefault((), []).append(label)
            setattr(edge, attr, label)
        if edge.relation and edge.relation not in RELATION_STYLE:
            graph.audit.append(f"第 {edge.line} 行：關係「{edge.relation}」不在預設表中，僅作文字標籤")


def wrap(label: str) -> str:
    lines = []
    for part in label.splitlines():
        lines.extend(textwrap.wrap(part, LABEL_WIDTH, break_long_words=True, break_on_hyphens=False) or [""])
    return "\n".join(lines)


def node_attrs(node: Node) -> str:
    fill, stroke, shape, type_style = TYPE_STYLE[node.type]
    penwidth, status_style, peripheries = STATUS_STYLE[node.status]
    styles = ["filled"] + [s for s in (type_style, status_style) if s]
    attrs = [
        f'label="{dot_escape(wrap(node.label))}"',
        f'shape="{shape}"',
        f'style="{",".join(styles)}"',
        f'fillcolor="{fill}"',
        f'color="{stroke}"',
        f'penwidth="{penwidth}"',
    ]
    if peripheries != 1:
        attrs.append(f'peripheries="{peripheries}"')
    return ", ".join(attrs)


def emit_dot(graph: Graph) -> str:
    out: list[str] = [AUTO_MARK + " 由上方 clues 區塊生成，請勿手改；重新執行 scripts/clues_to_graphviz.py"]
    for item in graph.audit:
        out.append(f"// 稽核：{item}")
    out += [
        "digraph clues {",
        "  graph [",
        f'    rankdir="{graph.rankdir}", bgcolor="#FFFFFF", newrank="true", compound="true",',
        '    splines="polyline", nodesep="0.30", ranksep="0.60", pad="0.15",',
        f'    fontname="{FONT}", fontsize="16", labelloc="t",',
        f'    label="{dot_escape(graph.title)}"',
        "  ];",
        f'  node [fontname="{FONT}", fontsize="9", fontcolor="#1F2937", margin="0.10,0.06"];',
        f'  edge [fontname="{FONT}", fontsize="8", fontcolor="#475569", arrowsize="0.65"];',
        "",
    ]

    cluster_ids = {path: f"cluster_{i:02d}" for i, path in enumerate(sorted(graph.clusters)) if path}

    def emit_cluster(path: tuple[str, ...], indent: str) -> None:
        if path:
            out.extend([
                f"{indent}subgraph {cluster_ids[path]} {{",
                f'{indent}  label="{dot_escape(path[-1])}"; color="#CBD5E1"; fillcolor="#FAFAFA";',
                f'{indent}  fontcolor="#1F2937"; fontsize="11"; style="filled,rounded";',
            ])
            indent += "  "
        for label in graph.clusters.get(path, []):
            node = graph.nodes[label]
            out.append(f"{indent}{node.dot_id} [{node_attrs(node)}];")
        for child in sorted(p for p in graph.clusters if len(p) == len(path) + 1 and p[: len(path)] == path):
            emit_cluster(child, indent)
        if path:
            out.append(f"{indent[:-2]}}}")

    emit_cluster((), "  ")
    out.append("")
    for edge in graph.edges:
        src, dst = graph.nodes[edge.src].dot_id, graph.nodes[edge.dst].dot_id
        if edge.relation in RELATION_STYLE:
            attrs = RELATION_STYLE[edge.relation]
        elif edge.relation:
            attrs = f'{UNDEFINED_RELATION}, label="{dot_escape(edge.relation)}"'
        else:
            attrs = UNDEFINED_RELATION
        out.append(f"  {src} -> {dst} [{attrs}];")

    times = [t for t in graph.time_order]
    for node in graph.nodes.values():
        if node.time and node.time not in times:
            times.append(node.time)
    if times:
        out.append("")
        out.append("  // 時序帶：@時點 相同的節點同層；帶與帶之間只約束先後")
        for i, t in enumerate(times):
            anchor = f"time_{i:02d}"
            members = [n.dot_id for n in graph.nodes.values() if n.time == t]
            out.append(f'  {anchor} [shape="plaintext", label="{dot_escape("@" + t)}", fontsize="8", fontcolor="#94A3B8"];')
            out.append(f"  {{ rank=same; {anchor}; {'; '.join(members)}; }}")
        for a, b in zip(range(len(times)), range(1, len(times))):
            out.append(f'  time_{a:02d} -> time_{b:02d} [style="invis", weight="50", minlen="2"];')
    out.append("}")
    return "\n".join(out)


def render_markdown(text: str) -> tuple[str, list[str], list[str]]:
    lines = text.splitlines()
    result: list[str] = []
    messages: list[str] = []
    dots: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip() != "```clues":
            result.append(lines[i])
            i += 1
            continue
        start = i
        i += 1
        while i < len(lines) and lines[i].strip() != "```":
            i += 1
        block = lines[start + 1 : i]
        result.extend(lines[start : i + 1])
        i += 1
        graph = parse("\n".join(block))
        dot = emit_dot(graph)
        dots.append(dot)
        messages.append(
            f"{graph.title or '（無標題）'}：{len(graph.nodes)} 節點、{len(graph.edges)} 連線、{len(graph.audit)} 稽核"
        )
        messages.extend(f"  - {item}" for item in graph.audit)
        j = i
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j + 1 < len(lines) and lines[j].strip() == "```dot" and lines[j + 1].startswith(AUTO_MARK):
            k = j + 1
            while k < len(lines) and lines[k].strip() != "```":
                k += 1
            i = k + 1
        result += ["", "```dot", dot, "```"]
    return "\n".join(result) + ("\n" if text.endswith("\n") else ""), messages, dots


def check_dot(dot: str) -> str:
    """Run dot -Tsvg and insist on real output; an empty SVG means nothing was drawn."""
    import shutil
    import subprocess

    executable = shutil.which("dot") or str(Path("Graphviz/bin/dot.exe"))
    if not Path(executable).exists():
        return "找不到 dot；已略過驗證"
    result = subprocess.run([executable, "-Tsvg"], input=dot.encode("utf-8"), capture_output=True)
    stderr = result.stderr.decode("utf-8", "replace").strip()
    if result.returncode != 0:
        raise RuntimeError(f"Graphviz 驗證失敗：{stderr}")
    if b"<svg" not in result.stdout:
        raise RuntimeError("Graphviz 沒有輸出任何圖形")
    return "Graphviz DOT 驗證通過" + (f"（警告：{stderr}）" if stderr else "")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("notes", nargs="+", type=Path, help="含 ```clues 區塊的 Markdown 檔")
    parser.add_argument("--check", action="store_true", help="以 dot 驗證生成結果")
    args = parser.parse_args()
    status = 0
    for note in args.notes:
        original = note.read_text(encoding="utf-8")
        updated, messages, dots = render_markdown(original)
        if updated != original:
            note.write_text(updated, encoding="utf-8", newline="\n")
        print(f"{note}：{'已更新' if updated != original else '無變更'}")
        for message in messages:
            print("  " + message)
        if args.check:
            for dot in dots:
                try:
                    print("  " + check_dot(dot))
                except RuntimeError as error:
                    print(f"  {error}")
                    status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
