# maoxuan/ — 毛选逐篇蒸馏

把《毛泽东选集》388 篇逐篇蒸馏成可执行的 Hermes skills。

- **方法**：cangjie-skill 的 RIA 六段（Reading / Interpretation / A1 过去应用 / A2 触发场景 / Execution / Boundary），降到「一篇一 skill」粒度。
- **节奏**：逐篇、一篇一篇来，每篇走一次「核对交互」（见下）。
- **原文**：`raw/`（gitignore，不提交整篇原文——只提交 ≤150 字的原文引用，符合版权与 cangjie 红线）。

## 目录结构

```
maoxuan/
├── MANIFEST.json          # 388 篇清单 + 状态（脚本读写）
├── scripts/maoxuan.py     # 机械层：fetch/next/status/mark
├── raw/<slug>.md          # 原文缓存（gitignore）
└── <slug>/                # 每篇的蒸馏产物
    ├── SKILL.md
    └── test-prompts.json
```

## 核对交互（每篇 3 拍）

1. **先睹** — 篇名 / 卷·年份 / 一句话主旨 / 一个原文金句。
2. **猜核心** — 这篇最该拆成一个什么 skill？给 2~3 个候选（含诱饵），你选，我揭晓。
3. **核 trigger** — 我给出 RIA 骨架，核对「什么时候该用」这个 trigger 是否真的会触发你。

## 进度

见 `MANIFEST.json`（`status` 字段：未抓 → fetched → distilled）。跑 `python3 scripts/maoxuan.py status` 看全量清单。
