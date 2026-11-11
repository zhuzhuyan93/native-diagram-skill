#!/usr/bin/env python3
"""Validate Native Diagram documents with the Python standard library."""
import json
import sys
from pathlib import Path


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["Root must be an object"]
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        errors.append("title must be a nonempty string")
    if data.get("direction", "TB") not in ("TB", "LR"):
        errors.append("direction must be TB or LR")
    nodes, layers, edges = data.get("nodes"), data.get("layers"), data.get("edges", [])
    if not isinstance(nodes, list) or not nodes:
        return errors + ["nodes must be a nonempty array"]
    if not isinstance(layers, list) or not layers:
        return errors + ["layers must be a nonempty array"]
    if not isinstance(edges, list):
        return errors + ["edges must be an array"]
    ids = []
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get("id"), str) or not node["id"] or not isinstance(node.get("label"), str) or not node["label"]:
            errors.append("each node needs a nonempty string id and label")
        else:
            ids.append(node["id"])
    if len(ids) != len(set(ids)):
        errors.append("duplicate node IDs")
    flat = []
    for layer in layers:
        if not isinstance(layer, list) or not layer or not all(isinstance(x, str) for x in layer):
            errors.append("each layer must be a nonempty array of node IDs")
        else:
            flat.extend(layer)
    if len(flat) != len(set(flat)):
        errors.append("node appears in multiple layers")
    if set(ids) != set(flat):
        errors.append("layers must contain every node exactly once")
    for edge in edges:
        if not isinstance(edge, dict) or edge.get("from") not in ids or edge.get("to") not in ids:
            errors.append("edge references unknown node")
    return errors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/validate.py <diagram.json>")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        sys.exit("\n".join("ERROR: " + x for x in errors))
    print("OK: diagram valid")
