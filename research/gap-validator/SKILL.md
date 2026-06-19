---
name: gap-validator
description: "Verify that a candidate research gap is real (nobody has done it) using three independent verification sources: journal tracing, scholar tracing, and theoretical grounding. No domain intuition required."
version: 1.0.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, gap-detection, literature-review, hypothesis-validation]
    category: research
    related_skills: [territory-mapper, idea-rebel, model-builder, academic-writing-sop, arxiv]
    requires_toolsets: [terminal, file, web]
---

# Gap Validator — 找缺口

锁不定 gap 不是你搜得不够——是**没有验证方法**。gap-validator 提供一套不需要领域直觉的三源验证：期刊追溯、学者追溯、理论论证。

**核心翻转**：不是"我觉得这没人做过" → 而是"我查了顶刊、追踪了学者、检验了理论，三个独立源都指向同一个结论。"

## When to Use

- territory-mapper 完成，有了概念地图和学者档案
- idea-rebel 生成了候选 idea 池（或你自己有了候选 gap）
- 想确认一个 gap 是"真的没人做过"而不是"我漏了"
- 写 Introduction 的"research gap"段需要证据，不只是说"few studies have..."

**Do not use**: 领域不熟且 territory-mapper 还没跑 — 没有概念地图和学者档案做验证锚点，三源验证无法执行。

## Pipeline Position

```
territory-mapper → idea-rebel → gap-validator → model-builder → contribution-shaper
     (Phase 1)      (Phase 2a)    (Phase 2b)       (Phase 3a)       (Phase 3b)
```

## Core Algorithm: Three-Source Verification

```
输入: 候选 gap（一句话 + 涉及的 construct）+ 概念地图 + 学者档案
输出: 验证报告（通过/不通过）+ 为什么 + 文献池（验证过程中发现的论文）

对于每个候选 gap：
  ├─ 验证源 1: 期刊追溯
  ├─ 验证源 2: 学者追溯
  └─ 验证源 3: 理论论证

三源全部通过 → gap 成立
任一源不通过 → gap 不成立（或需要缩小范围）
```

## Verification Source 1: Journal Tracing（期刊追溯）

**逻辑**：如果这个 gap 真的存在，领域顶刊近 5 年不应该有相关论文。

```
对于 gap 涉及的每个 construct 配对：
  ① 选领域 top 5 期刊（从 territory-mapper 的概念卡片中提取最常出现的期刊）
  ② 在每本期刊搜 construct A + construct B 的组合（标题/摘要/关键词）
  ③ 时间范围：近 5 年（不够可以扩展到 10 年）

  结果判定:
    找到 ≥ 1 篇直接相关的 → ❌ 期刊不通过 — gap 不成立
    找到 0 篇直接相关的 → ✅ 期刊通过
    找到 0 篇但找到 "related but different" 的 → ⚠️ 需分析差异
```

**搜索策略（实操）**：

```bash
# Scopus / Web of Science 标题+摘要搜索
TITLE-ABS-KEY("psychological safety" AND "AI") AND PUBYEAR > 2021 AND SRCTITLE("Academy of Management Journal")

# Google Scholar（无 API 时手动）
"psychological safety" "artificial intelligence" site:journals.aom.org
```

**期刊列表怎么定**：
- 从 territory-mapper 的概念卡片中提取"常用期刊"列
- 取出现频率最高的 5 本
- 如果 gap 涉及跨领域 construct（如 AI + org behavior），加 2-3 本另一领域的顶刊

**⚠️ 易犯错误**：
- 只搜一本期刊就说"没人做过" — 不够。至少要 3 本顶刊 + 2 本相关领域。
- 搜索词太窄 — 同义词/变体也要搜。比如 "AI" 也要搜 "artificial intelligence" "machine learning" "algorithm"。
- 只搜标题不搜摘要 — 会漏掉。标题可能不包含 construct 名但摘要有。

## Verification Source 2: Scholar Tracing（学者追溯）

**逻辑**：如果这个 gap 真的存在，研究这些 construct 的前沿学者不应该已经做过。

```
对于 gap 涉及的每个 construct：
  ① 从 territory-mapper 的学者档案中找出前 3-5 位学者
  ② 追溯每位学者的完整发表记录（Google Scholar profile + CV）
  ③ 检查：这些学者是否做过涉及 gap 中 construct 组合的研究？

  结果判定:
    任何一位学者做过直接相关的研究 → ❌ 学者不通过
    所有学者都没做过 → ✅ 学者通过
    学者做过 "相关但不完全一样" 的 → ⚠️ 分析差异，可能 gap 需要窄化
```

**学者追溯实操**：

```bash
# Google Scholar — 搜索学者名 + construct 名
"Michael Frese" "psychological safety"

# 如果学者 Google Scholar profile 有 "publications by year" 列表
# 扫描最近 5 年的论文标题，看是否涉及 gap 中的 construct 组合

# 检查学者的合作者 — 他们可能做了
"Michael Frese" "AI" "learning"
```

**为什么学者追溯有效**：
- 如果领域前 3 学者都没碰过这个 construct 组合 → 大概率真的是空白
- 如果前 3 学者有人碰过 → 你不会漏掉，因为他们的论文被引次数高，很容易发现

**⚠️ 易犯错误**：
- 只看学者的"代表作"不看全部 — 可能他们的非代表作里有。
- 只看一作 — 学者可能是合作者中的通讯作者。查完整 co-author 列表。
- 学者的档案中"知识边界"标注为"不研究 X" → 不能当作验证结论。必须实际搜索确认。

## Verification Source 3: Theoretical Grounding（理论论证）

**逻辑**：一个 gap 即使确实没人做过，也必须能用现有理论框架解释 — 否则可能是"没人做因为没意义"的假 gap。

```
对于通过期刊+学者验证的 gap：
  ① 列出 gap 涉及的 causal chain
  ② 找至少一个理论框架能解释这个 chain
  ③ 写出 2-3 句的理论论证草稿

  结果判定:
    至少一个理论框架能自然覆盖 → ✅ 理论通过
    理论框架能覆盖但需要额外假设 → ⚠️ 可以但论证成本高
    找不到任何理论支撑 → ❌ 理论不通过 — 可能是假 gap
```

**理论论证格式**：

```markdown
## gap: AI learning support → learning agility → ambidexterity
- 理论框架: Social Cognitive Theory (Bandura 1986)
- 论证:
  1. AI learning support = 环境刺激（SCT 的 "environment"）
  2. Learning agility = 个人认知能力（SCT 的 "person"）
  3. Ambidexterity = 行为输出（SCT 的 "behavior"）
  4. SCT 三元交互: E → P → B，AI 学习环境通过塑造学习敏捷性来驱动双元创新行为
- 已有文献怎么走的: SCT 在 training 领域很成熟，但从未用于 AI-mediated learning
- gap 成立: 理论框架清晰、有文献基础但未应用于此情境
```

**⚠️ 易犯错误**：
- 理论论证不是写 LR — 2-3 句就够。验证的是"能不能解释"，不是"怎么说服审稿人"。
- "找不到理论"≠ 假 gap — 可能是跨领域的新组合，理论还没跟上。这时候标注"理论待构建"，不直接判定为假 gap。
- 一个理论硬套不上就换 — 同一个 gap 试试 2-3 个理论框架。如果在已有理论中确实没有干净的解释 → 这本身是信号。

## Verification Report Format

每个候选 gap 的完整验证报告：

```markdown
## gap-03: AI learning support → learning agility → ambidexterity

### 一句话
AI 驱动的学习支持工具通过增强员工学习敏捷性，促进双元创新行为。

### 涉及 construct
- IV: AI learning support
- Mediator: learning agility
- DV: ambidexterity

### 三源验证

| 验证源 | 方法 | 结果 | 判定 |
|--------|------|------|------|
| 期刊 | AMJ/ASQ/JAP/JOM/MISQ 搜索 | 0 篇直接相关，2 篇 "AI + training" 但不涉及 learning agility | ✅ 通过 |
| 学者 | 追溯 Bedford(learning agility) + Edmondson(team learning) + Frese(error management) | 三位学者均未将 AI 引入其研究 | ✅ 通过 |
| 理论 | SCT: E→P→B | 三元交互清晰覆盖 | ✅ 通过 |

### 结论
✅ **gap 成立。** 三源全部通过。

### 验证过程中发现的邻近论文
- Johnson 2024 JAP: AI training effectiveness — 涉及 AI + training，但不研究 learning agility
- Lee 2023 MISQ: AI-assisted decision making — 涉及 AI + human capability，不研究 ambidexterity
- → 这些论文可以作为 Introduction 的 "related but different" 引用

### 下一步
送 model-builder 建模，建议优先用 SCT 作理论框架。
```

## Exit Conditions

```
停止验证的条件（满足任一即退出）:
  1. 有 1-2 个 gap 三源全部通过 → 送 model-builder（够了，不用把 idea 池全部验完）
  2. 连续验证 3 个候选 gap 全部三源不通过 → 回 territory-mapper 或 idea-rebel（领域可能已饱和）
  3. idea 池中已验证完 5 个 → 如果没有通过的就回头重生成（不用全验 10 个）
```

## Output

```
~/workspace/wiki/research/{domain-name}/
├── gap-validation/              # 验证报告
│   ├── gap-01-report.md         # 每个候选 gap 的完整验证
│   ├── gap-02-report.md
│   └── ...
├── literature-pool/             # 验证过程中发现的论文（无论通过与否）
│   ├── johnson2024-ai-training.md
│   └── ...
└── verified-gaps.md             # 通过的 gap 汇总 + 推荐优先级
```

## Input / Output Contract

| 输入 | 格式 | 来源 |
|------|------|------|
| 候选 gap（1 句话 + construct 列表） | Markdown / 文本 | idea-rebel 输出 or 你自己 |
| 概念地图（概念卡片 + 学者档案） | Markdown 目录 | territory-mapper 输出 |
| 领域 top 期刊列表 | 文本 | territory-mapper 输出 |

| 输出 | 格式 | 给谁的输入 |
|------|------|----------|
| 验证报告 | Markdown | model-builder |
| 文献池（验证过程中搜到的论文） | Markdown | model-builder, academic-writing-sop |

## Pitfalls

- **不要跳过期刊追溯直接靠感觉。** "我觉得顶刊肯定没有"是最常见的错误 — 很多 gap 其实去年刚有人做。
- **不要因为一个期刊通过了就停止。** 三源都必须独立验证。一源通过不代表 gap 成立。
- **学者追溯不是查一次就够。** 搜索学者名 + construct A 可能不精准。换 construct B + 学者名再搜一遍。
- **理论验证不是"写一个不矛盾的解释"。** 是找一个**已有的、公认的**理论框架。不能自己发明一个理论凑 gap。
- **发现 1 篇 "related but different" 不要直接判不通过。** 分析差异——如果差异够大（不同情境、不同机制、不同 granularity），gap 可能窄化后仍然成立。
- **不要验证第一个通过的就停下来不追其他的。** 至少验证 2-3 个 gap，从中选理论支撑最强的。
- **期刊搜索的 year constraint 不要设太窄。** 至少近 5 年。如果 gap 涉及的是热门话题（如 AI），缩短到 3 年也够。

## Composability

- **With `territory-mapper`**: 使用其概念卡片和学者档案作为验证锚点
- **With `idea-rebel`**: 直接吞 idea-rebel 的输出（候选 idea 池）
- **With `model-builder`**: 验证通过的 gap 直接送建模
- **With `academic-writing-sop`**: 验证过程中发现的论文形成文献池，直接入 Deck
- **With `arxiv`**: 搜索最新 preprint 确保 gap 在 preprint 层面也是空的
