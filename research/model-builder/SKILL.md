---
name: model-builder
description: "Transform a verified research gap into a testable theoretical model. Variable identification, hypothesis generation, paper splitting logic — with contribution markers on every path."
version: 1.0.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, model-design, hypothesis-generation, paper-planning]
    category: research
    related_skills: [gap-validator, contribution-shaper, academic-writing-sop]
    requires_toolsets: [terminal, file]
---

# Model Builder — 建模

把验证通过的 gap 变成可测试的模型。不是"画一个漂亮的路径图"——是**精确地识别出每个变量、每条路径、每个假设的逻辑支撑和贡献层级**。

**核心翻转**：不是"把所有相关 construct 堆进模型"，而是"只放进能讲清楚故事的变量，砍掉所有只是'可能有关系'的东西。"

## When to Use

- gap-validator 输出了 1-2 个三源通过的 gap
- 有了叙事框架（如 ABV、SCT）但不知道怎么转换成模型图
- 变量太多，不知道怎么精简
- 模型太大，不确定该不该拆成两篇

## Pipeline Position

```
territory-mapper → idea-rebel → gap-validator → model-builder → contribution-shaper
     (Phase 1)      (Phase 2a)    (Phase 2b)       (Phase 3a)       (Phase 3b)
```

## Step 1: Variable Identification

从验证通过的 gap 中提取变量，按角色分类：

```
从 gap 的 causal narrative 中提取:
  ┌─ 前因 (Independent)  : gap 的起点 — "什么推动了这件事"
  ├─ 中介 (Mediator)     : gap 的核心机制 — "为什么 A 会导致 C"
  ├─ 调节 (Moderator)    : gap 的情境条件 — "什么时候这个关系更强/更弱"
  ├─ 结果 (Dependent)    : gap 的终点 — "最终影响了什么"
  ├─ 控制 (Control)      : 已知的替代解释 — "排除这些后，贡献才纯"
  └─ 区分变量             : 与你核心贡献邻近但你必须区分的 construct
```

**变量命名规则**：
- 每个变量必须对应一个已有的 construct，不能自己捏
- 如果 gap 跨了管理学的子领域，选一个子领域的术语体系（不要混用）
- 量表来源必须在 Step 1 就标注，不要留到后面

**输出格式**：

```markdown
| 变量 | 角色 | Construct | 定义来源 | 量表来源 | 已有研究中常见角色 |
|------|------|-----------|---------|---------|-----------------|
| AI 学习支持 | IV | AI-mediated learning support | Smith 2023 | Smith 2023 (改编) | IV (training 文献) |
| 学习敏捷性 | Mediator | Learning agility | Bedford 2011 | Bedford 2011, 9-item | Mediator, DV |
| 双元创新 | DV | Organizational ambidexterity | Gibson & Birkinshaw 2004 | He & Wong 2004, 10-item | DV |
| 工作自主性 | Moderator | Job autonomy | Hackman & Oldham 1975 | Morgeson & Humphrey 2006, 9-item | Moderator |
| 组织规模 | Control | Firm size | - | 员工数的自然对数 | Control |
| 技术准备度 | Discriminant | Technology readiness | Parasuraman 2000 | Parasuraman 2000, 36-item | 与 AI 学习支持接近但不同 |
```

## Step 2: Variable Simplification Check

**模型不是越大越好**。对每个变量做必要性检查：

```
对每个非核心变量问：
  ├─ 删掉它会丢失什么故事？能合并到其他变量里吗？
  ├─ 它有自己的独立理论论证吗？还是只是"也许有关"？
  └─ 有可用量表吗？如果没有 → 不能进模型，除非你自创量表
```

**紧简规则**：

| 条件 | 动作 |
|------|------|
| 变量数 > 7 | ⚠️ 模型太大，必须拆或精简 |
| 中介链 > 2 层 | ⚠️ 论证链条太长，读者跟不上 |
| 调节变量 > 3 | ⚠️ 模型复杂度爆炸，选理论支撑最强的 1-2 个 |
| 任何变量无可用量表 | 🔴 不能进模型（或需自创量表 + 预测试） |

## Step 3: Model Diagram

用 ASCII 画模型图，标注每条路径的**贡献层级**：

```
        ┌─────────────────┐
        │  工作自主性       │  [standard: 常见调节变量]
        │  (Job Autonomy)  │
        └────────┬────────┘
                 │ H4a/b
                 ▼
┌──────────┐   H1   ┌──────────┐   H2   ┌──────────┐
│ AI学习支持 │ ────→ │ 学习敏捷性 │ ────→ │ 双元创新   │
│   (IV)   │       │(Mediator) │       │  (DV)    │
└──────────┘       └──────────┘       └──────────┘
     │                                      ▲
     └──────────── H3 (direct) ────────────┘

路径贡献层级:
  H1: 🟢 contribution — AI learning → learning agility 没人做过
  H2: 🟡 extension  — learning agility → ambidexterity 在 tech 行业做过，传统行业没做过
  H3: 🟢 contribution — AI learning → ambidexterity 的直接路径没人做过（通过中介间接已验证）
  H4a/b: 🟡 extension — autonomy 作为调节在 training 文献中常见但未用于 AI context
```

**贡献层级标注**：

| 标记 | 含义 | 论文里怎么写 |
|------|------|------------|
| 🟢 contribution | 没人做过，有理论支撑 | 核心贡献，Introduction 重点讲 |
| 🟡 extension | 有人做过但情境/方法不同 | Introduction 提"虽然 X 研究过，但..." |
| ⚪ standard | 常见关系，领域共识 | 不需要论证，引用即可 |

## Step 4: Hypothesis Generation

对每条路径生成假设。每条假设必须同时有：
- **一句话逻辑**（不是 "H1: A → B" 而是 "H1: A 通过 X 机制影响 B"）
- **理论支撑**（引用具体的理论 + 关键文献）
- **贡献层级**（🟢/🟡/⚪）

```markdown
## H1: AI 学习支持 → 学习敏捷性
- 一句话: AI 学习支持通过提供个性化、即时反馈的学习环境，增强员工的学习敏捷性
- 理论: SCT — 环境刺激（AI learning support）塑造个人认知能力（learning agility）
- 核心引用: Bandura 1986; Bedford 2011; Smith 2023
- 贡献层级: 🟢 contribution
- 量表: AI learning support (Smith 2023, 改编 12-item), learning agility (Bedford 2011, 9-item)

## H2: 学习敏捷性 → 双元创新
- 一句话: 学习敏捷性使员工能同时高效处理探索性和利用性任务，推动双元创新
- 理论: SCT — 个人认知能力（learning agility）驱动行为输出（ambidexterity）
- 核心引用: Bedford 2011; He & Wong 2004; Mom et al. 2009
- 贡献层级: 🟡 extension（tech 行业已验证，传统行业未验证）
- 量表: learning agility (Bedford 2011), ambidexterity (He & Wong 2004, 10-item)

## H3: AI 学习支持 → 双元创新 (直接)
- 一句话: AI 学习支持可能直接促进双元创新（超越通过学习敏捷性的间接路径）
- 理论: 技术赋能 — AI 降低信息获取成本，直接加速探索和利用
- 核心引用: Autor 2015; Smith 2023; Gibson & Birkinshaw 2004
- 贡献层级: 🟢 contribution（直接路径未经验证）
- 注意: H3 是探索性的 — 如果中介效应完全解释，H3 可能不显著。这对研究是好的（说明中介机制是核心），不是失败。

## H4a: 工作自主性调节 AI 学习支持 → 学习敏捷性
- 一句话: 工作自主性越高，AI 学习支持对学习敏捷性的影响越强
- 理论: JD-R — autonomy 作为 job resource 增强学习动机
- 核心引用: Bakker & Demerouti 2007; Morgeson & Humphrey 2006
- 贡献层级: 🟡 extension（调节逻辑在 training 文献中常见但未用于 AI）
```

## Step 5: Paper Splitting Decision

**模型是否太大需要拆？使用拆论文决策矩阵**：

```
判断流程:
  变量总数 > 7？
    ├─ 否 → 一篇搞定
    └─ 是 →
        变量能否自然分成两个独立的故事？
          ├─ 能 → 拆成 Paper A + Paper B
          │      每篇 ≤ 5 个核心变量 + ≤ 4 个假设
          │      两篇共享 Intro 的领域背景，各自有独立的理论叙事
          │      两篇的 construct 不重叠（或只在控制变量层面重叠）
          └─ 不能 → 不拆，但精简：合并相关变量、砍掉调节中理论最弱的

如果拆：
  Paper A 的叙事：{一篇的一句话}
  Paper B 的叙事：{另一篇的一句话}
  两篇的关系：{互补？递进？平行？}
```

**拆论文示例**：

```markdown
原模型: 5 前因 → BSS → Ambidexterity → Resilience → Bricolage → Competitive Advantage
变量数: 10 → 太大

拆分:
  Paper A: 5 前因 → BSS → Ambidexterity（"什么影响了 BSS 和双元能力"）
  Paper B: Ambidexterity → Resilience → Bricolage → Competitive Advantage（"双元能力如何转化为韧性、bricolage 和竞争优势"）

  关系: 递进 — Paper A 讲"怎么产生"，Paper B 讲"产生后怎么用"
  共享变量: Ambidexterity（Paper A 的 DV，Paper B 的 IV）
```

## Output

```
~/workspace/wiki/research/{domain-name}/
├── models/
│   ├── paper-A/
│   │   ├── model.md              # 模型图 + 变量表 + 贡献层级标注
│   │   ├── hypotheses.md         # 每个假设的一句话逻辑 + 理论支撑
│   │   └── scale-map.md          # 每个变量的量表来源 + 改编策略
│   └── paper-B/                  # (如果拆分)
│       └── ...
└── model-overview.md              # 所有模型的汇总 + 拆论文决策
```

## Input / Output Contract

| 输入 | 格式 | 来源 |
|------|------|------|
| 验证通过的 gap（1-2 个） | Markdown 报告 | gap-validator |
| ABV/理论叙事框架 | 文本 | gap-validator 的输出 |
| 领域概念地图 | 概念卡片 + 学者档案 | territory-mapper |

| 输出 | 格式 | 给谁的输入 |
|------|------|----------|
| 模型图 + 变量表 + 假设表 | Markdown | contribution-shaper, academic-writing-sop |
| 量表映射表 | Markdown | academic-writing-sop（Method 部分） |
| 拆论文决策 | Markdown | contribution-shaper |

## Pitfalls

- **不要在变量未标注量表的情况下建模。** 量表不可得 = 变量不可用。不要"先建模型后找量表"——这会导致 Method 部分卡死。
- **不要把所有"可能有关系"的变量全放进来。** 每个变量必须有独立的理论论证——不是"文献中它出现了"就够了。
- **不要跳过拆论文决策。** 模型 > 7 个变量时，拆不拆必须明确决定。不要抱着"先写写看"的态度——写到 Hypothesis 段一半发现模型太大，回退成本高。
- **中介链不要太长。** A→B→C 两层是上限。A→B→C→D 三层中介链，要么合并 B 和 C、要么拆成不同模型。
- **贡献层级不要主观判断。** 基于 gap-validator 的验证结论来标——通过三源验证的标 🟢，期刊不通过但窄化后通过的标 🟡。
- **调节变量宁缺毋滥。** 审稿人最常挑战的就是"这个调节变量真的有理论依据吗？"选 1 个理论支撑最强的就够了。

## Composability

- **With `gap-validator`**: 直接吞验证通过的 gap + 文献池
- **With `contribution-shaper`**: 模型输出直接送贡献打磨
- **With `academic-writing-sop`**: 模型图 + 假设表 → SOP-1 Deck 构筑的 blueprint；量表映射表 → SOP-2 Method 部分
- **With `territory-mapper`**: 变量选择时参考概念卡片确认哪个 construct 有成熟量表
