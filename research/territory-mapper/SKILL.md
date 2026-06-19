---
name: territory-mapper
description: "Map an unfamiliar research domain by building concept cards and scholar profiles. Uses saturation detection instead of intuition. 触发词：铺地图、概念卡片、学者建档、领域不熟、帮我了解一下这个领域、saturation detection."
version: 1.0.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, literature-review, concept-mapping, scholar-profiling, territory-mapping]
    category: research
    related_skills: [idea-rebel, gap-validator, academic-writing-sop, arxiv]
    requires_toolsets: [terminal, file, web]
---

# Territory Mapper — 铺地图

进入一个不熟悉的领域时，不靠直觉判断"懂没懂"，而是靠信号衰减来判断"新信息何时枯竭"。

**核心翻转**：不是"我觉得够了"，而是"连续 N 篇论文没带来新概念 — 客观上够了。"

## When to Use

- 进入一个新研究领域，不知道有哪些 construct、谁在研究、发在哪
- 需要系统性地理解领域，但不清楚从哪里开始
- 想写一篇论文但不确定"变量池"够不够大
- 导师说"先去读文献"但不想无目标地读 100 篇

**Do not use**: 领域已经有了完整的概念地图（已有 survey/review paper 覆盖），或只想找 2-3 篇核心文献快速上手。

## Pipeline Position

```
territory-mapper → idea-rebel → gap-validator → model-builder → contribution-shaper → academic-writing-sop
     (Phase 1)      (Phase 2a)    (Phase 2b)       (Phase 3a)       (Phase 3b)         (已有)
```

独立可用，也做流水线第一步。输出直接喂给 idea-rebel 和 gap-validator。

## Core Algorithm: Saturation Detection

不靠直觉。靠可计算的信号衰减。

```
输入: 种子论文 3-5 篇（导师/同事推荐的核心文献）
输出: 概念卡片集 + 学者档案集 + 饱和报告

循环:
  读一篇论文 →
  ├─ 提取所有 construct/variable → 和已有概念卡片对比 → 新概念数
  ├─ 提取作者 + 高被引学者 → 和已有学者档案对比 → 新学者数
  ├─ 记录 construct 搭配（X—Y 关系）→ 新关系数
  └─ 检查退出条件
```

## Saturation Exit Conditions

| 维度 | 饱和信号 | 阈值 |
|------|---------|------|
| **概念** | 连续 N 篇新论文引入 0 个新 construct | N = 5 |
| **学者** | 新论文的作者/被引学者 100% 已在档案中 | 连续 5 篇 |
| **关系** | 论文中 construct 搭配重复率 | >80% |
| **期刊** | 追踪的种子期刊不再出现新变量 | 最新 3 期无新 |

**当 4 个维度中 3 个达到阈值 → 退出。**

## Concept Card Format

不是定义卡，是**用法卡**。关键信息：谁在用、在哪用、和什么搭配。

```markdown
---
source: Edmondson1999
type: concept-card
domain: organizational-behavior
saturation_status: active  # active | stable | saturated
---

## construct: psychological safety

### 定义
> "team psychological safety is a shared belief that the team is safe for
>  interpersonal risk taking" (Edmondson 1999, p.354)

### 用法矩阵
| 维度 | 内容 |
|------|------|
| 作为 IV 的前因 | leader behavior, team structure, organizational support |
| 作为 IV 的结果 | team learning, innovation, performance, voice |
| 作为 mediator | 常在 leader behavior → team learning 之间 |
| 常用期刊 | AMJ, ASQ, JAP, JOM, Organization Science |
| 核心学者 | Edmondson (Harvard), Newman (UQ), Frazier (Creighton) |
| 量表 | Edmondson 1999, 7-item Likert |
| 常搭配的 construct | team learning, voice behavior, error management, trust |

### 来源论文
- Edmondson 1999 ASQ (seminal, cited 12000+)
- Edmondson & Lei 2014 Annu. Rev. Psychol.
- Frazier et al. 2017 Personnel Psych. (meta)
- Newman et al. 2017 JOB (review)
```

## Scholar Profile Format

不是简历，是**研究地图**。关键信息：核心方向、方法偏好、合作圈、知识边界。

```markdown
---
source: multi
type: scholar-profile
---

## scholar: Amy Edmondson

### 核心方向
psychological safety → team learning → intelligent failure → extreme teaming

### 方法偏好
定量（survey + field study），有时定性（case study）

### 代表论文
- 1999 ASQ (seminal, psychological safety 的定义基础)
- 2014 Annu. Rev. Psychol. (review)
- 2018 book: The Fearless Organization
- 2023 book: Right Kind of Wrong (intelligent failure)

### 合作圈
Anita Woolley, Sara Singer, Michaela Kerrissey, Ingrid Nembhard

### 期刊层级
主要发 ASQ, AMJ, Organization Science, HBR

### 知识边界 — 她不做什么
- 不研究 strategic management
- 不碰 entrepreneurship
- 不研究 AI/technology adoption
- 极少涉及个体差异（personality/ability）

### 被引学者
抄 3-5 个她高频引用且与你领域相关的学者
- Richard Hackman (team effectiveness)
- Karl Weick (sensemaking)
- Edgar Schein (organizational culture)
```

**"知识边界"是这个档案最有价值的部分** — 它告诉 gap-hunter "这个学者不太可能在 X 方向做过研究"。

## 种子论文选取

从哪里开始铺地图？三条路，优先级递减：

| 优先级 | 来源 | 为什么 |
|--------|------|--------|
| 1 | 导师/同事直接推荐 | 最精准，领域核心 |
| 2 | 最近的 survey/review paper | 省力，已有结构化梳理 |
| 3 | 顶刊近 3 年与你关键词匹配的论文 | 时效性好 |

**种子论文数：3-5 篇。** 少于 3 不足以启动饱和检测，多于 5 容易过早饱和（种子太窄）。

🔴 **CHECKPOINT: 种子论文选定后，展示列表给用户确认，再开始建第一张概念卡片。不要自己替用户决定种子论文。**

## 扩展策略：引文滚雪球

读种子论文时，从引用中选下一批论文：

```
种子 A 的后引 → 4 篇 "种子 A 引用的人"
种子 A 的前引 → 3 篇 "引用了种子 A 的人"（Google Scholar cited-by）
种子 B 的后引 → ...
```

**扩展原则**：
- 优先选与种子论文共享 ≥ 2 个 construct 的论文（保持领域聚焦）
- 优先选顶刊（ABS 4*/4、FT50、UTD24）
- 优先选不同学术圈的（避免只追踪一个 school of thought）

## Saturation Tracking

每读一篇论文后，更新一个简单的追踪表：

```markdown
| # | 论文 | 新概念 | 累计概念 | 新学者 | 累计学者 | 新关系 | 是否饱和？ |
|---|------|--------|---------|--------|---------|--------|----------|
| 1 | Edmondson1999 | 3 | 3 | 5 | 5 | 2 | - |
| 2 | Newman2017 | 2 | 5 | 3 | 8 | 3 | - |
| ... | ... | ... | ... | ... | ... | ... | - |
| 15 | Smith2022 | 0 | 11 | 0 | 22 | 0 | ⚠️ 概念+学者 0 |
| 16 | Jones2023 | 0 | 11 | 0 | 22 | 0 | ⚠️ |
| 17 | Brown2023 | 0 | 11 | 1 | 23 | 0 | ⚠️ (学者未饱和) |
| 18 | Lee2024 | 0 | 11 | 0 | 23 | 0 | ⚠️ |
| 19 | Park2025 | 0 | 11 | 0 | 23 | 0 | ✅ 概念饱和 |
```

🔴 **CHECKPOINT: 3/4 维度达阈值时，暂停并展示饱和报告给用户确认——是否退出 mapping 还是继续扩展搜索范围？不替用户做"已经够了"的判断。**

## 失败恢复

| 场景 | 症状 | 恢复动作 |
|------|------|---------|
| **种子论文不足** | 可获得的种子 < 3 篇 | ① 从已有 1-2 篇的后引/前引扩展；② 用关键词在顶刊搜近 3 年综述；③ 仍不足 → 向用户请求推荐或降低种子数阈值到 2 篇 |
| **滚雪球越滚越远** | 连续 3 篇新论文与种子共享 construct < 2 个 | 回退到上一步的论文池，换一条引文路径；如果所有路径都偏 → 可能是领域本身较窄，提前检查饱和信号 |
| **饱和迟迟不出现** | >30 篇论文后仍未达 3/4 阈值 | ① 检查种子是否太窄（只覆盖一个学派）；② 扩展种子期刊范围（加 2-3 本相关领域期刊）；③ 可能领域本身概念空间大——此时饱和信号不适用，改按"新概念增长率 < 10%"判断 |
| **概念之间关系稀疏** | 累计概念 > 15 但关系 < 5 | 领域可能还没形成稳定的 construct 搭配——概念卡片有效但关系维度的饱和信号不可靠。此时退出条件改为 2/3（概念+学者）而非 3/4 |

## Output

```
~/workspace/wiki/research/{domain-name}/
├── saturation-report.md       # 饱和追踪表 + 退出判断
├── concept-cards/             # 每张概念卡片一个 .md
│   ├── psychological-safety.md
│   ├── team-learning.md
│   └── ...
├── scholar-profiles/          # 每位学者一个 .md
│   ├── amy-edmondson.md
│   ├── michael-frese.md
│   └── ...
└── index.md                   # 概念索引 + 学者索引 + 关系矩阵
```

## Input / Output Contract

| 输入 | 谁给 | 格式 |
|------|------|------|
| 领域名 + 关键词 | 你 | 文本 |
| 种子论文 3-5 篇 | 你 / 导师 | PDF 或 DOI |

| 输出 | 格式 | 给谁的输入 |
|------|------|----------|
| 概念卡片集 | Markdown | idea-rebel, gap-validator |
| 学者档案集 | Markdown | gap-validator |
| 饱和报告 | Markdown | 你审阅 |

## Pitfalls

- **不要一次读完所有种子论文再开始做卡。** 读完第一篇就做第一张卡——边读边建，饱和检测才能生效。
- **概念卡片不是给每个 construct 写一篇 essay。** 一页纸，控制在 30 行以内。重点是用法矩阵，不是文献综述。
- **不要追求 88 位学者全部建档后再继续。** 学者饱和信号出来（新论文不再引入新学者）就停止，不是"把领域所有人建完"。
- **知识边界不是随便猜。** 基于学者的 publication list 和研究轨迹下判断，不凭空说"他不研究 X"。
- **饱和不等于"我已经读了领域所有论文"。** 饱和 = "继续读大概率不会改变我对领域结构的理解"，这是退出信号，不是完成信号。
- **种子论文不要全是同一个导师或合作圈的。** 会漏掉其他学术流派。
- **引文滚雪球时容易越滚越远。** 每次扩展检查：这篇论文是否与种子共享 ≥ 2 个 construct？不满足就跳过。

## Composability

- **With `arxiv`**: fetch seed papers before mapping
- **With `academic-writing-sop`**: concept cards evolve into Deck atoms when gap is validated
- **With `gap-validator`**: scholar profiles feed directly into scholar-trace verification
- **With `idea-rebel`**: concept cards are the operating surface for rebel operators
