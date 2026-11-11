# Native Diagram Skill

A portable, offline Skill and Python SVG renderer for editable technical diagrams.

## Quick start

```bash
python scripts/validate.py examples/architecture.json
python scripts/render.py examples/architecture.json output/architecture.svg
python -m unittest discover -s tests -v
```

No external Python dependencies. SVG is editable in vector editors. JSON is the authoritative source.

## Project status

Early-stage v0.1.0. Supports layered TB/LR diagrams, nodes and orthogonal edges; not a live drag-and-drop editor or a direct Figma integration.

## Documentation

- [中文说明](README.zh-CN.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Changelog](CHANGELOG.md)
- [MIT License](LICENSE)

Independent implementation; no proprietary ChatGPT UI components are included.
