# Layout rules

- TB: top-to-bottom for architectural layers.
- LR: left-to-right for sequential workflows.
- Each node appears in exactly one layer.
- Prefer a small number of nodes per layer; split dense diagrams.
- Orthogonal connectors are generated from the layer structure.
- Keep labels short: the current renderer does not automatically wrap text.
- Inspect SVG after rendering; crossing edges and long text need manual review.
