---
name: idea-rebel
description: "Generate candidate research ideas by systematically applying thinking operators (reversal, boundary-shift, cross-domain grafting, etc.) to concept maps. 10 ideas, rough filter, feed to gap-validator."
version: 0.1.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, ideation, creativity, hypothesis-generation]
    category: research
    related_skills: [territory-mapper, gap-validator, model-builder]
    requires_toolsets: [terminal, file]
    status: skeleton
---

# Idea Rebel — 造反算法生成候选 idea

> ⚠️ **SKELETON — 待从 Daniel Dennett《Intuition Pumps and Other Tools for Thinking》蒸馏。**
>
> 计划：使用 cangjie book2skill 流程从《直觉泵》中提取思维工具，适配为学术 idea 生成算子。
>
> 临时算子列表（10 个，来自设计阶段）已在下文保留，待蒸馏后替换。

## When to Use

- territory-mapper 输出完成，概念地图就绪
- 需要从已知概念中生成新颖的研究问题
- 不怕 idea 不靠谱 — 10 个里 1 个能用就值

## Pipeline Position

```
territory-mapper → idea-rebel → gap-validator → model-builder → contribution-shaper
     (Phase 1)      (Phase 2a)    (Phase 2b)       (Phase 3a)       (Phase 3b)
```

## Temporary Operator Set（待蒸馏替换）

以下 10 个算子是设计阶段的占位符。蒸馏《直觉泵》后将根据 Dennett 的实际思维工具重新编织。

| # | 算子 | 操作 | 商科论文映射 |
|---|------|------|------------|
| 1 | 反转 | X→Y 倒过来 | team learning → psychological safety |
| 2 | 加边界 | X→Y 只在什么条件下成立 | AI learning → ambidexterity, only under high autonomy |
| 3 | 去边界 | 情境 A 成立的，搬到情境 B | psych safety 从知识团队 → 制造业产线 |
| 4 | 换层级 | 个体→团队→组织 | individual bricolage → team bricolage |
| 5 | 拆维度 | construct 拆子维度 | ambidexterity → exploration only vs exploitation only |
| 6 | 跨界嫁接 | 领域 A 的 construct × 领域 B 的理论 | entrepreneurial bricolage 解释 AI capability |
| 7 | 时间反转 | 横向变纵向 | 短期效果 vs 长期衰减 |
| 8 | 否定前提 | 推翻理论隐含假设 | SCT 假设人能准确评估 → 如果 AI 黑箱？ |
| 9 | 极端化 | 推到极限 | 极度资源匮乏 vs 丰裕下的 bricolage |
| 10 | 反向调节 | 已知正向调节 → 找什么条件下变负 | autonomy 什么情况下变成负担？ |

## 粗筛规则（保留，即使是占位符）

对每个生成的 idea：

| 判定 | 信号 | 动作 |
|------|------|------|
| 🔴 删 | 涉及无可用量表的 construct | 除非有能力自创 |
| 🔴 删 | 理论直接矛盾 | 不硬掰 |
| 🟡 存疑 | 有理论可能但未确认 | 标记，送理论查证 |
| 🟢 优先 | 有明确理论 + 可用量表 + 预估三源通过 | 先送 gap-validator |

## Idea Draft Format（保留）

```markdown
## idea-XX: {算子名} — {一句话}
- 算子: {算子名}
- 来源: 概念卡片 "{construct A}" + "{construct B}"
- 一句话: {核心主张}
- construct: {IV(s)}, {Mediator(s)}, {DV(s)}
- 量表: {量表来源 + 可用性评估}
- 理论: {可支撑的理论框架}
- 粗筛: 🔴/🟡/🟢 + 理由
```

## Output

```
候选 idea 池（10 个，每个一页 Markdown）
→ 粗筛后送 gap-validator 验证
```

## 蒸馏计划

- 来源: Daniel Dennett, *Intuition Pumps and Other Tools for Thinking* (2013)
- 工具: cangjie book2skill 流程
- 目标: 从书中 77 个 thinking tools 中提取适配学术 idea 生成的算子
- 预期: 替换临时算子列表，形成真正的造反算法

---

> 此 skill 处于 skeleton 状态。触发时提示用户使用 gap-validator 直接验证已知 gap，不尝试生成不靠谱的 idea。
