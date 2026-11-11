#!/usr/bin/env python3
"""Render a validated Native Diagram JSON document to editable SVG."""
import html
import json
import sys
from pathlib import Path
from validate import validate


def escape(value):
    return html.escape(str(value), quote=True)


def render(data):
    errors = validate(data)
    if errors:
        raise ValueError("; ".join(errors))
    layers = data["layers"]
    nodes = {n["id"]: n for n in data["nodes"]}
    direction = data.get("direction", "TB")
    node_w, node_h, gap, layer_gap, margin, header = 224, 82, 20, 84, 52, 110
    maxcols = max(map(len, layers))
    if direction == "TB":
        width = max(660, maxcols * node_w + (maxcols - 1) * gap + margin * 2)
        height = header + len(layers) * node_h + (len(layers) - 1) * layer_gap + margin
    else:
        width = margin * 2 + len(layers) * node_w + (len(layers) - 1) * layer_gap
        height = header + maxcols * node_h + (maxcols - 1) * gap + margin
    positions = {}
    for li, layer in enumerate(layers):
        for ni, node_id in enumerate(layer):
            if direction == "TB":
                span = len(layer) * node_w + (len(layer) - 1) * gap
                x, y = (width - span) / 2 + ni * (node_w + gap), header + li * (node_h + layer_gap)
            else:
                span = len(layer) * node_h + (len(layer) - 1) * gap
                x = margin + li * (node_w + layer_gap)
                y = header + (maxcols * node_h + (maxcols - 1) * gap - span) / 2 + ni * (node_h + gap)
            positions[node_id] = (x, y)
    output = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(data["title"])}">',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#91A4BA"/></marker></defs>',
        f'<rect width="{width}" height="{height}" fill="#F7F9FC"/>',
        f'<text x="{margin}" y="43" font-family="Inter, Noto Sans, sans-serif" font-size="23" font-weight="700" fill="#142338">{escape(data["title"])}</text>',
        f'<text x="{margin}" y="66" font-family="Inter, Noto Sans, sans-serif" font-size="12" fill="#8290A1">{escape(data.get("subtitle", ""))}</text>',
    ]
    for edge in data.get("edges", []):
        a, b = positions[edge["from"]], positions[edge["to"]]
        if direction == "TB":
            x1, y1, x2, y2 = a[0] + node_w / 2, a[1] + node_h, b[0] + node_w / 2, b[1]
            mid = (y1 + y2) / 2
            path = f'M{x1:.1f},{y1:.1f} V{mid:.1f} H{x2:.1f} V{y2 - 5:.1f}'
        else:
            x1, y1, x2, y2 = a[0] + node_w, a[1] + node_h / 2, b[0], b[1] + node_h / 2
            mid = (x1 + x2) / 2
            path = f'M{x1:.1f},{y1:.1f} H{mid:.1f} V{y2:.1f} H{x2 - 5:.1f}'
        output.append(f'<path d="{path}" fill="none" stroke="#91A4BA" stroke-width="1.6" marker-end="url(#arrow)"/>')
    for node_id, (x, y) in positions.items():
        node = nodes[node_id]
        accent = node.get("accent", False)
        bg = "#EDF4FF" if accent else "#FFFFFF"
        stroke = "#A8C8F4" if accent else "#DDE5EF"
        bar = "#3776D6" if accent else "#B8C6D8"
        output.extend([
            f'<g id="node-{escape(node_id)}">',
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{node_w}" height="{node_h}" rx="12" fill="{bg}" stroke="{stroke}"/>',
            f'<rect x="{x + 14:.1f}" y="{y + 18:.1f}" width="5" height="32" rx="2.5" fill="{bar}"/>',
            f'<text x="{x + 30:.1f}" y="{y + 35:.1f}" font-family="Inter, Noto Sans, sans-serif" font-size="15" font-weight="600" fill="#142338">{escape(node["label"])}</text>',
            f'<text x="{x + 30:.1f}" y="{y + 56:.1f}" font-family="Inter, Noto Sans, sans-serif" font-size="11" fill="#526276">{escape(node.get("subtitle", ""))}</text>',
            '</g>',
        ])
    output.append('</svg>')
    return "\n".join(output)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python scripts/render.py <input.json> <output.svg>")
    source, target = Path(sys.argv[1]), Path(sys.argv[2])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(json.loads(source.read_text(encoding="utf-8"))), encoding="utf-8")
    print("Rendered", target)
