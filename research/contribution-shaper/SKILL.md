---
name: contribution-shaper
description: "Identify and sharpen the core contribution of a research model. Layer contributions (theory vs context vs method), upgrade variable definitions, and check differentiation from the closest existing papers."
version: 1.0.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, contribution-analysis, model-refinement, paper-writing]
    category: research
    related_skills: [model-builder, academic-writing-sop]
    requires_toolsets: [terminal, file]
---

# Contribution Shaper — 打磨贡献

模型建好了，但真正的贡献在哪？哪些路径是"前人走过的"，哪些是"你开的路"？贡献不够 sharp 的模型，审稿人一句话就能打死："the contribution is unclear."

**核心翻转**：不是"我的模型有很多新关系" → 而是"我的模型有两个精准的贡献，其余是已知的逻辑必然。"

## When to Use

- model-builder 输出完成，模型图和假设表就绪
- 不确定核心贡献是什么——感觉"好像每个假设都挺新"
- 需要把一般变量升级为 sharp 变量（如 bricolage → knowledge-driven bricolage）
- 需要检查与最接近论文的区分度——"审稿人会拿哪几篇说事？"

## Pipeline Position

```
territory-mapper → idea-rebel → gap-validator → model-builder → contribution-shaper
     (Phase 1)      (Phase 2a)    (Phase 2b)       (Phase 3a)       (Phase 3b)
                                                                           ↓
                                                             academic-writing-sop (已有)
```

## Step 1: Contribution Layering

对模型中的每条路径，分层标注贡献层级。不止 🟢/🟡/⚪——要细化到**贡献类型**。

```markdown
对于每条假设路径：
  ├─ 这条路径在文献中有没有人走过？
  │    有  → 继续：在什么情境？用什么方法？得出了什么结论？
  │    部分 → 什么部分有人做、什么部分是新的？
  │    没有 → 继续：为什么没人做？（没有理论？没有数据？没有量表？）
  │
  └─ 判定贡献类型：
      layer-1 (理论贡献): 完全没人走过的路径，有理论支撑
      layer-2 (情境贡献): 有人做过但不在你的情境/行业/国家
      layer-3 (方法贡献): 新的测量方式、新的分析策略、新的数据来源
      layer-4 (复制): 标准关系，在你的情境中验证——最小的贡献但有时也必要（如跨文化验证）
```

**贡献分层表**：

```markdown
| 假设 | 路径 | 贡献层级 | 类型 | 最接近的已有研究 | 我们有什么不同 |
|------|------|---------|------|----------------|--------------|
| H1 | AI learning → learning agility | 🟢 | layer-1 theory | 无 — 首次连接 AI 与 learning agility | 全新的理论论证 |
| H2 | Learning agility → ambidexterity | 🟡 | layer-2 context | Mom 2009 (manufacturing) | 我们在 service industry |
| H3 | AI learning → ambidexterity (direct) | 🟢 | layer-1 theory | 无 | 探索直接路径超越中介 |
| H4a | Autonomy × AI → learning agility | 🟡 | layer-2 context | Bakker 2007 (general training) | 我们限定在 AI training context |
```

## Step 2: Variable Sharpening（变量升级）

有些变量太 generic — 审稿人会说"这不是 X 的 standard definition"。升级让变量更 sharp 同时保持可测量：

**升级判断三问**：

```
1. 这个 construct 在文献中有没有更窄但更精准的子类型？
   如: bricolage → resource bricolage vs knowledge bricolage vs network bricolage
2. 你的情境是否天然限定了 construct 的某个方面？
   如: "在 AI 辅助情境下的 learning agility" vs 通用 learning agility
3. 窄化后的 construct 有可用量表吗？如果没有 → 不能升级，回退到通用定义
```

**升级案例**：

```markdown
## 案例：bricolage → knowledge-driven bricolage

原 construct: bricolage（"make do with resources at hand" — Baker & Nelson 2005）
问题: 太通用。在你的模型中，员工不是用所有随手资源，而是用知识（learnings, insights, mental models）

升级后: knowledge-driven bricolage
- 定义: "the process of recombining existing knowledge resources to address novel problems" 
- 区别于 resource bricolage: 操作的不是物质资源，而是知识资源
- 区别于 improvisation: bricolage 是资源重组，improvisation 是时间压力下的即时行动
- 量表: 改编 Baker & Nelson 2005 的 bricolage 量表，将 "resources" 替换为 "knowledge resources"
  - 原题："We use any existing resource that seems useful"
  - 改编："We recombine existing knowledge from different domains to address new challenges"
- 理论依据: KBV — knowledge as the primary resource for recombination
- 贡献: bricolage 文献中知识维度的缺失 → 填补

## 案例（反例 — 不能升级的情况）

原 construct: 数字化转型（太 generic）
想升级为: AI 赋能的数字化转型
问题: 没有成熟量表。自创量表成本太高（预测试 + EFA + CFA 至少 300 样本）。
决策: 保留 "数字化转型" 的通用定义和成熟量表，在理论论证中强调 AI 维度作为边界条件，而非独立变量。
```

**升级评估表**：

```markdown
| 变量 | 是否可升级 | 升级方向 | 量表可用？ | 决策 |
|------|----------|---------|----------|------|
| bricolage | ✅ | knowledge-driven bricolage | 可改编 Baker & Nelson 2005 | 升级 |
| AI learning support | ✅ | AI-mediated interactive learning | Smith 2023 有改编量表 | 升级 |
| 双元创新 | ❌ | - | He & Wong 2004 已够 sharp | 保持 |
| 工作自主性 | ❌ | - | 标准定义已够 | 保持 |
```

## Step 3: Differentiation Check（区分度检查）

找出文献池中与你模型最接近的 3 篇论文，系统性地比较。这直接决定 Introduction 的"how we differ"段。

**最接近论文识别**：
- 从 gap-validator 的文献池中找 construct 组合最匹配的
- 如果文献池不够大，用 Google Scholar 搜核心 construct 组合 + "vs" / "and"

**区分度矩阵**：

```markdown
| 维度 | 我们的 Paper | Smith 2024 | Lee 2023 | Chen 2022 |
|------|------------|-----------|---------|----------|
| IV | AI learning support | AI training | Digital platform | E-learning system |
| Mediator | Learning agility | (无中介) | Self-efficacy | Motivation |
| DV | Ambidexterity | Task performance | Innovation | Learning outcomes |
| 调节 | Job autonomy | (无调节) | Tech readiness | (无调节) |
| 理论 | SCT | HRM | TAM | Self-determination |
| 情境 | 传统制造 | Tech startups | 金融 | 教育 |
| 方法 | PLS-SEM, survey | Field experiment | Survey | Lab experiment |

区分度总结:
  vs Smith 2024: 他们有 AI 但只有任务绩效，我们引入双元能力和 SCT 机制 — 区分度足够
  vs Lee 2023: 他们研究数字平台但不涉及 AI-specific 学习 — 窄领域中不同
  vs Chen 2022: 教育情境不重叠 — 区分度足够但情境差异不能作为唯一区分点
```

**区分度标准**：

| 区分度 | 信号 | 风险 |
|--------|------|------|
| 足够 | 至少 2 个核心维度不同（IV/Mediator/DV/理论/情境） | 低 |
| 勉强 | 只有情境不同 | 审稿人: "为什么不直接在已有模型上做 cross-context 研究？" |
| 不够 | 相同点多于不同点 | 必须重新设计，和已有论文撞了 |

## Step 4: Mediation Mechanism Deepening

如果模型中有中介变量，必须问：**这个中介的内在机制是什么？**

不只要说 "A 通过 M 影响 C" — 要说 **"A 通过 M 的哪个具体机制影响 C"**。

```
对每个中介路径问:
  ├─ M 的哪个维度在起作用？
  │   如 learning agility → 是 "people agility" 还是 "results agility"？
  ├─ 这个机制有没有被其他研究提过但没有实证？
  │   如果有 → 你在填补 gap 的同时也在验证已有理论推测 → 贡献更强
  └─ 有没有对立的机制？
      A 会不会通过降低 X（而非增加 M）来影响 C？→ research question，不是 confounding
```

**示例 — 两个中介机制的深度分析**：

```markdown
## 中介 1: BSS → 认知定势打断 → Ambidexterity
- 机制: BSS (behavioral strategy style) 通过打破决策惯性来促进双元
- 为什么: 高管的行为战略风格创造了一种"松动"——既有惯例被频繁挑战
- 操作化: "认知定势打断" = 管理者能够 (a) 识别自己的思维惯性 (b) 主动寻求反向证据
- 最接近的研究: Hodgkinson 2009 (cognitive inertia) — 提了理论但没有实证
- 贡献: 首次实证检验 "BSS → cognitive frame-breaking → ambidexterity" 路径

## 中介 2: 被动快速试错 → Bricolage
- 机制: 在缺乏资源的压力下，组织通过低成本快速试错来找到可行方案
- 为什么: 不是主动实验（那需要资源），而是被动应对（constraint-driven experimentation）
- 操作化: 被动快速试错 = (a) trial frequency (b) trial cost (c) learning from failed trials
- 最接近的研究: Ries 2011 Lean Startup — 但那是创业情境，不是成熟组织
- 贡献: 将 Lean Startup 逻辑移植到成熟组织的资源重组情境，通过 bricolage 理论桥接
```

## Output

```markdown
~/workspace/wiki/research/{domain-name}/
├── contribution/
│   ├── contribution-layers.md       # 每条路径的贡献分层
│   ├── variable-upgrade-report.md   # 变量升级/不升级的决策 + 依据
│   ├── differentiation-matrix.md   # 与最接近论文的区分度矩阵
│   └── mediation-deepening.md       # 中介机制深度分析
```

## Input / Output Contract

| 输入 | 格式 | 来源 |
|------|------|------|
| 模型图 + 假设表 | Markdown | model-builder |
| 文献池（验证过程中搜到的论文） | Markdown 目录 | gap-validator |
| 概念地图 | 概念卡片 | territory-mapper |

| 输出 | 格式 | 给谁的输入 |
|------|------|----------|
| 贡献分层报告 | Markdown | academic-writing-sop（Introduction 段） |
| 变量升级报告 | Markdown | academic-writing-sop（Method 段 — 量表改编） |
| 区分度矩阵 | Markdown | academic-writing-sop（Introduction 段 — "how we differ"） |
| 中介机制分析 | Markdown | academic-writing-sop（Hypothesis 段 — 机制论证） |

## Pitfalls

- **不要把所有路径都标成 contribution。** 如果 5 条假设全是 🟢，说明 gap-validator 没做对——至少 H2（mediator→DV）大概率在已有文献中出现过。
- **不要为了升级而升级。** 升级必须有理论依据 + 可用量表。两者缺一的，保持标准定义。
- **区分度检查不要只看标题。** 必须读摘要——标题相似但实际变量不同的情况很常见。反之标题不同但路径一样的情况也很多。
- **中介机制分析不要停留在"A 通过 M 影响 C"。** 必须说明 M 的哪个具体维度/机制在起作用。这是把"descriptive mediation"变成"explanatory mediation"的关键。
- **区分度矩阵中不要把"情境不同"当作唯一区分点。** 必须有理论或 construct 层面的差异——否则审稿人会说"这是 cross-context replication，不是新贡献"。
- **不要跳过最接近论文的作者追溯。** Lee 2023 的作者可能正在写一个直接相关的 working paper——查他们的 recent presentations、SSRN preprint、conference submissions。

## Composability

- **With `model-builder`**: 直接吞模型图和假设表
- **With `academic-writing-sop`**: 
  - 贡献分层 → SOP-2 Introduction（"我们的三个贡献是..."）
  - 区分度矩阵 → SOP-2 Introduction（"与 Smith 2024 不同，我们..."）
  - 变量升级报告 → SOP-2 Method（量表改编理由）
  - 中介机制分析 → SOP-2 Hypothesis（每个 H 的机制论证）
- **With `gap-validator`**: 使用 gap-validator 的文献池做区分度检查
