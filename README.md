# Julia's Skills

Collection of Hermes Agent skills. Each skill lives in its own directory with a `SKILL.md`.

## Research Pipeline（论文流水线）

A 5-skill pipeline for taking a research idea from "I know nothing about this domain" to "model ready for Deck construction and writing."

```
territory-mapper → idea-rebel → gap-validator → model-builder → contribution-shaper
      ↓                                                              ↓
   (Phase 1)      (Phase 2a)    (Phase 2b)       (Phase 3a)       (Phase 3b)
                                                                       ↓
                                                         academic-writing-sop (已有)
```

| # | Skill | What it does | Status |
|---|-------|-------------|--------|
| 1 | `territory-mapper` | 铺地图 — 概念卡片 + 学者档案 + 饱和检测 | ✅ v1.0 |
| 2 | `idea-rebel` | 造反 — 从概念地图生成候选 idea（10 个算子） | 🏗️ skeleton — 待从《直觉泵》蒸馏 |
| 3 | `gap-validator` | 找缺口 — 三源验证（期刊/学者/理论）确认 gap | ✅ v1.0 |
| 4 | `model-builder` | 建模 — 变量识别/假设生成/拆论文决策/贡献标注 | ✅ v1.0 |
| 5 | `contribution-shaper` | 打磨 — 贡献分层/变量升级/区分度检查/中介深挖 | ✅ v1.0 |

After the pipeline: `academic-writing-sop` for Deck construction and reverse-order writing, `literature-deck` for atom extraction and assembly.

### How to use

Each skill is independently usable — you can jump in at any step if you already have the inputs. For a new paper from scratch, run them in order.

## Research

| Skill | Description |
|-------|-------------|
| `literature-deck` | Academic literature deck system: atom extraction + tag-based paragraph assembly |

## Creative

| Skill | Description |
|-------|-------------|
| `collection-split` | Split a text collection into atomic scenes by POV × time × location |
| `novel-split` | Dual-atom novel analysis: Doyle (scene×topic) vs Christie (dialogue round) |
| `novel-tag` | 10/14-tag extension system for novel analysis atoms |
| `style-analyzer` | 文笔DNA卡片 — analyze writing style fingerprints |

## Productivity

| Skill | Description |
|-------|-------------|
| `task-ball-machine` | Draw random tasks from a configurable ball machine |

---

All skills are MIT licensed. Compatible with Hermes Agent.
