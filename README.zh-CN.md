# Native Diagram Skill

基于结构化 JSON 的轻量级技术架构图 Skill，可离线生成可编辑 SVG。

## 快速开始

```bash
python scripts/validate.py examples/architecture.json
python scripts/render.py examples/architecture.json output/architecture.svg
python -m unittest discover -s tests -v
```

将本仓库放入支持 SKILL.md 的 AI 编程代理的 Skills 目录，或按客户端文档配置 Skill 路径。

目前支持 TB/LR 分层布局、节点卡片、正交连线。暂不支持可视化拖拽、自动避让和原生 Figma 同步。

详见 [English README](README.md)。
