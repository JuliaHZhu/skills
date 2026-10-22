---
name: double-helix
description: "把对话反转录成双螺旋知识卡。流程：对话→核心问题→精华/反转/创新点/反逻辑→二分「经典理论」vs「个人独特答案」→落经典理论卡/个人问题答案卡。触发词：记卡、记一下、知识卡、双螺旋、反转录、对话蒸馏、沉淀这段、这条理论是谁提出的。"
version: 0.1.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [knowledge-management, conversation-distillation, theory-cards, metacognition, note-taking]
    category: knowledge-management
    related_skills: [personal-wiki, llm-wiki]
    requires_toolsets: [file]
---

# 双螺旋 Double Helix — 对话反转录成知识卡

把一段高密度对话「反转录」成可遗传的知识卡。

**两条链**：经典理论链（成熟理论，别人的）× 个人答案链（你的独特洞见）。**核心问题是碱基配对的中轴**。

## 核心流程

```
对话
  → 核心问题（这段对话在回答什么）
    → 精华 / 反转 / 创新点 / 反逻辑（洞察时刻）
      → 二分：经典理论 ｜ 个人独特答案
        → 经典理论卡 ｜ 个人问题答案卡
```

## 纯度机制（最重要）

**agent 不自动扫描沉淀。** 只有你主动说「记卡 / 记一下 / 沉淀这段」才启动。

agent 的活被限定为机械的：
1. 提取候选洞察（精华/反转/创新点/反逻辑），列成待拍板清单
2. 预分类建议（这条像经典理论还是你的独特答案）
3. 查重（`search_files` 扫 cards/，避免重复卡）
4. 落卡 + 打时间戳

**「什么算精华、归经典还是归个人」——判断权在你，agent 只给建议。**

## 两类卡

模板见 `templates/classic-card.md` 和 `templates/personal-card.md`。

- **经典理论卡**：成熟理论，有提出者。解决「记不住是谁提出的」。
- **个人问题答案卡**：你对核心问题的独特答案。核心资产，`对照经典` 字段标出与哪个经典沾边/区别。

## 时间戳

- `source`: 会话发生时间（回看时知道语境）
- `created` / `updated`: 卡片沉淀 / 扩充时间

## 扩充 vs 新建

加新卡前先查重。若已有同「核心问题 + 同主题」的卡 → **扩充**（追加 source、更新 updated、补新角度），而非新建重复卡。

## 目录结构

```
double-helix/
  SKILL.md
  cards/
    classic/       # 经典理论卡
    personal/      # 个人问题答案卡
  conversations/   # 会话摘录（策展，非全文）
  templates/       # 两类卡模板
```

## 会话摘录

全文已在 session DB。`conversations/` 只存「策展摘录 + 会话时间戳 + 一句话主题」，留指针不复制，避免两处漂移。

## 使用步骤

1. 你指向某段对话，说「记卡」
2. agent 提取候选洞察 + 预分类，列成待拍板清单
3. 你拍板（哪些要存、归经典还是个人）
4. agent 落卡 + 打时间戳 + 查重

## Pitfalls

- 不要自动扫描沉淀——等你说「记卡」。
- 不要替用户判断「什么值得沉淀」——那是纯度的来源。
- 经典归经典，个人归个人，别焊在一张卡里。
- 会话只存摘录 + 指针，不存全文。
- 卡片控制在 30 行内，是「用法卡」不是 essay。
