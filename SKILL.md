---
name: native-diagram
description: Generate editable technical architecture diagrams and workflows from structured JSON using an offline SVG renderer. Use for system architecture, pipelines, and capability maps.
---

# Native Diagram

1. Read `references/design-system.md` and `references/layout-rules.md`.
2. Translate requirements into JSON following `schemas/diagram.schema.json`.
3. Use `direction: TB` for layered systems and `LR` for pipelines.
4. Validate with `python scripts/validate.py <input.json>`.
5. Render with `python scripts/render.py <input.json> <output.svg>`.
6. Deliver both source JSON and SVG. Preserve node IDs when revising.

Do not invent domain relationships without identifying assumptions. Prefer hierarchy, whitespace, neutral surfaces, subtle borders, and restrained blue accents. Inspect complex graphs for crossings and overflow.

Outputs are static, editable SVG assets, not a live visual editor. Direct Figma synchronization and drag-and-drop editing are not implemented.
