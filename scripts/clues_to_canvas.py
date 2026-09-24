"""Turn ```clues blocks into an Obsidian .canvas file.

Graphviz computes the layout (dot -Tjson); Obsidian Canvas provides the
interaction: pan, zoom, drag, group folding, [[links]] inside node text.
The .canvas sits next to the note and is fully regenerable.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clues_to_graphviz import (  # noqa: E402
    DEFAULT_STATUS,
    FADED,
    FONT,
    RELATION_STYLE,
    TYPE_STYLE,
    Graph,
    Node,
    cluster_ids,
    dot_escape,
    endpoint,
    parse,
    wrap,
)

NODE_WIDTH = 260          # px; fits ~14 CJK chars per line at Canvas default font
LINE_HEIGHT = 24
NODE_PADDING = 28
CLEARANCE = 6             # px kept between a connection and a node box
CURVE_SAMPLES = 24
CURVE_MARGIN = 3          # samples skipped at each end, where the line touches its own node
SIDE_NORMAL = {"top": (0, -1), "bottom": (0, 1), "left": (-1, 0), "right": (1, 0)}
EDGE_COLOR = {
    "支持": "#1F2937",
    "導致": "#EA580C",
    "推導": "#64748B",
    "矛盾": "#DC2626",
    "時序": "#94A3B8",
    "屬於": "#94A3B8",
}
UNDEFINED_EDGE_COLOR = "#94A3B8"


def cid(*parts: str) -> str:
    return hashlib.md5("|".join(parts).encode("utf-8")).hexdigest()[:16]


def card_text(node: Node) -> str:
    text = f"**{node.label}**\n\n{node.detail}" if node.detail else node.label
    if node.status != DEFAULT_STATUS[node.type]:
        text += f"\n\n`{node.status}`"
    return text


def node_box(node: Node) -> tuple[int, int]:
    lines = wrap(node.label).count("\n") + 1
    if node.detail:
        lines += wrap(node.detail).count("\n") + 2
    return NODE_WIDTH, lines * LINE_HEIGHT + NODE_PADDING


def layout_dot(graph: Graph) -> str:
    """DOT used only for coordinates: fixed node sizes in Canvas pixels (72 px = 1 in)."""
    out = [
        "digraph layout {",
        f'  graph [rankdir="{graph.rankdir}", newrank="true", nodesep="1.00", ranksep="1.60", fontname="{FONT}"];',
        '  node [shape="box", fixedsize="true", label=""];',
    ]
    ids = cluster_ids(graph)
    referenced = set(graph.group_refs.values())

    def emit(path: tuple[str, ...], indent: str) -> None:
        if path:
            out.append(f'{indent}subgraph {ids[path]} {{ label="{dot_escape(path[-1])}"; margin="24";')
            indent += "  "
        for label in graph.clusters.get(path, []):
            node = graph.nodes[label]
            w, h = node_box(node)
            out.append(f'{indent}{node.dot_id} [width="{w / 72:.3f}", height="{h / 72:.3f}"];')
        if path in referenced:
            out.append(f'{indent}{ids[path]}_anchor [width="0.1", height="0.1", style="invis"];')
        for child in sorted(p for p in graph.clusters if len(p) == len(path) + 1 and p[: len(path)] == path):
            emit(child, indent)
        if path:
            out.append(f"{indent[:-2]}}}")

    emit((), "  ")
    for edge in graph.edges:
        out.append(f"  {endpoint(graph, ids, edge.src)[0]} -> {endpoint(graph, ids, edge.dst)[0]};")

    times = list(graph.time_order)
    for node in graph.nodes.values():
        if node.time and node.time not in times:
            times.append(node.time)
    for i, t in enumerate(times):
        members = [n.dot_id for n in graph.nodes.values() if n.time == t]
        out.append(f'  time_{i:02d} [width="0.1", height="0.1", style="invis"];')
        out.append(f"  {{ rank=same; time_{i:02d}; {'; '.join(members)}; }}")
    for a in range(len(times) - 1):
        out.append(f'  time_{a:02d} -> time_{a + 1:02d} [style="invis", weight="50", minlen="2"];')
    out.append("}")
    return "\n".join(out)


def run_dot(dot: str) -> dict:
    executable = shutil.which("dot") or str(Path("Graphviz/bin/dot.exe"))
    result = subprocess.run([executable, "-Tjson"], input=dot.encode("utf-8"), capture_output=True)
    if result.returncode != 0 or not result.stdout:
        raise RuntimeError(result.stderr.decode("utf-8", "replace") or "dot 沒有輸出")
    return json.loads(result.stdout)


def anchor(rect: tuple[float, float, float, float], side: str) -> tuple[float, float]:
    x, y, w, h = rect
    return {
        "top": (x + w / 2, y),
        "bottom": (x + w / 2, y + h),
        "left": (x, y + h / 2),
        "right": (x + w, y + h / 2),
    }[side]


def curve(start: tuple[float, float], from_side: str, end: tuple[float, float], to_side: str) -> list[tuple[float, float]]:
    """Approximates the cubic bezier Obsidian draws between two node sides."""
    reach = max(30.0, math.dist(start, end) * 0.4)
    c1 = tuple(start[i] + SIDE_NORMAL[from_side][i] * reach for i in (0, 1))
    c2 = tuple(end[i] + SIDE_NORMAL[to_side][i] * reach for i in (0, 1))
    points = []
    for step in range(CURVE_SAMPLES + 1):
        t = step / CURVE_SAMPLES
        u = 1 - t
        points.append(tuple(
            u**3 * start[i] + 3 * u * u * t * c1[i] + 3 * u * t * t * c2[i] + t**3 * end[i]
            for i in (0, 1)
        ))
    return points


def side_candidates(dx: float, dy: float) -> list[tuple[str, str]]:
    """Straight-through pair first, then detours through a side gutter, then the rest."""
    if abs(dy) >= abs(dx):
        out_side, in_side = ("bottom", "top") if dy > 0 else ("top", "bottom")
        near, far = ("right", "left") if dx >= 0 else ("left", "right")
    else:
        out_side, in_side = ("right", "left") if dx > 0 else ("left", "right")
        near, far = ("bottom", "top") if dy >= 0 else ("top", "bottom")
    preferred = [
        (out_side, in_side),
        (near, near), (far, far),
        (near, in_side), (out_side, near),
        (far, in_side), (out_side, far),
    ]
    return preferred + [p for p in itertools.product(SIDE_NORMAL, repeat=2) if p not in preferred]


def blocked(points: list[tuple[float, float]], boxes: list[tuple[float, float, float, float]]) -> int:
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    lo_x, hi_x, lo_y, hi_y = min(xs), max(xs), min(ys), max(ys)
    count = 0
    for x0, y0, x1, y1 in boxes:
        if x1 < lo_x or x0 > hi_x or y1 < lo_y or y0 > hi_y:
            continue
        if any(x0 <= px <= x1 and y0 <= py <= y1 for px, py in points):
            count += 1
    return count


def route(
    src: tuple[float, float, float, float],
    dst: tuple[float, float, float, float],
    boxes: list[tuple[float, float, float, float]],
) -> tuple[str, str]:
    dx = (dst[0] + dst[2] / 2) - (src[0] + src[2] / 2)
    dy = (dst[1] + dst[3] / 2) - (src[1] + src[3] / 2)
    best: tuple[int, str, str] | None = None
    for from_side, to_side in side_candidates(dx, dy):
        points = curve(anchor(src, from_side), from_side, anchor(dst, to_side), to_side)
        hits = blocked(points[CURVE_MARGIN:-CURVE_MARGIN], boxes)
        if hits == 0:
            return from_side, to_side
        if best is None or hits < best[0]:
            best = (hits, from_side, to_side)
    return best[1], best[2]


def build_canvas(graph: Graph) -> dict:
    layout = run_dot(layout_dot(graph))
    _, _, _, total_h = (float(v) for v in layout["bb"].split(","))
    by_dot_id = {n.dot_id: n for n in graph.nodes.values()}
    ids = cluster_ids(graph)
    nodes: list[dict] = []
    rects: dict[str, tuple[float, float, float, float]] = {}
    group_rects: dict[str, tuple[float, float, float, float]] = {}

    for obj in layout["objects"]:
        name = obj["name"]
        if "bb" in obj and name.startswith("cluster_"):
            x0, y0, x1, y1 = (float(v) for v in obj["bb"].split(","))
            group = {
                "id": cid("group", name),
                "type": "group",
                "label": obj.get("label", ""),
                "x": round(x0), "y": round(total_h - y1),
                "width": round(x1 - x0), "height": round(y1 - y0),
            }
            group_rects[name] = (group["x"], group["y"], group["width"], group["height"])
            nodes.append(group)
            continue
        node = by_dot_id.get(name)
        if node is None:
            continue
        cx, cy = (float(v) for v in obj["pos"].split(","))
        w, h = node_box(node)
        x, y = round(cx - w / 2), round((total_h - cy) - h / 2)
        rects[node.label] = (x, y, w, h)
        entry = {
            "id": cid("node", node.label),
            "type": "text",
            "text": card_text(node),
            "x": x, "y": y, "width": w, "height": h,
        }
        if node.status == "排除":
            entry["color"] = FADED[1]
        elif node.type != "未分類":
            entry["color"] = TYPE_STYLE[node.type][1]
        nodes.append(entry)

    def card(name: str) -> tuple[str, tuple[float, float, float, float]]:
        if name in graph.nodes:
            return cid("node", name), rects[name]
        cluster = ids[graph.group_refs[name]]
        return cid("group", cluster), group_rects[cluster]

    obstacles = {
        label: (x + CLEARANCE, y + CLEARANCE, x + w - CLEARANCE, y + h - CLEARANCE)
        for label, (x, y, w, h) in rects.items()
    }
    edges: list[dict] = []
    for i, edge in enumerate(graph.edges):
        (src_id, src_rect), (dst_id, dst_rect) = card(edge.src), card(edge.dst)
        from_side, to_side = route(src_rect, dst_rect, list(obstacles.values()))
        entry = {
            "id": cid("edge", str(i), edge.src, edge.dst),
            "fromNode": src_id, "fromSide": from_side,
            "toNode": dst_id, "toSide": to_side,
            "color": EDGE_COLOR.get(edge.relation, UNDEFINED_EDGE_COLOR),
        }
        if edge.relation:
            entry["label"] = edge.relation
        if edge.relation == "屬於":
            entry["toEnd"] = "none"
        edges.append(entry)

    # groups first so Obsidian draws them underneath
    nodes.sort(key=lambda n: 0 if n["type"] == "group" else 1)
    return {"nodes": nodes, "edges": edges}


def clues_blocks(text: str) -> list[str]:
    blocks, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        if lines[i].strip() == "```clues":
            j = i + 1
            while j < len(lines) and lines[j].strip() != "```":
                j += 1
            blocks.append("\n".join(lines[i + 1 : j]))
            i = j
        i += 1
    return blocks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notes", nargs="+", type=Path)
    parser.add_argument("--out-dir", type=Path, help="預設與筆記同目錄")
    args = parser.parse_args()
    for note in args.notes:
        blocks = clues_blocks(note.read_text(encoding="utf-8"))
        for index, block in enumerate(blocks, 1):
            graph = parse(block)
            canvas = build_canvas(graph)
            suffix = "" if len(blocks) == 1 else f"-{index}"
            target = (args.out_dir or note.parent) / f"{note.stem}{suffix}.canvas"
            target.write_text(json.dumps(canvas, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
            groups = sum(1 for n in canvas["nodes"] if n["type"] == "group")
            print(f"{target}：{len(canvas['nodes']) - groups} 節點、{groups} 群組、{len(canvas['edges'])} 連線")
            for item in graph.audit:
                print(f"  - {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
