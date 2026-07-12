---
name: logline
description: "Evaluate or craft a story logline using a 7-element template that forces specificity. Use when critiquing narrative structure, developing a story premise, or checking whether a story has a real backbone beyond vague themes."
version: 1.0.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
triggers:
  - logline
  - 一句话梗概
  - 故事大纲
  - evaluate this story
  - 故事结构
  - 检查故事
metadata:
  hermes:
    tags: [Writing, Story Structure, Narrative Design, Critique, Screenwriting]
    related_skills: [collection-split]
    requires_toolsets: []
---

# Logline — 7-Element Story Spine

## Philosophy

> 如果你说一个故事是一个关于爱、成长和命运的故事。
> 等于没说。
> 因为这个世界上可能百分之八十的故事都可以说自己关于爱、成长和命运。

A logline that stays at the theme level ("a story about redemption", "a journey of self-discovery") says nothing — it's a bucket that catches 80% of all stories. **Specificity is the only signal.**

## The Template

一个【怎样的主角】，因为【什么意外事件】，被迫离开【怎样的原本生活】，试图达成【一个具体的可执行目标】；在经历【阻碍一】和【阻碍二】之后，她真正要面对的是【自己的致命缺陷/真正目标】。

In English:

A **[protagonist with a defining trait]** , after **[an inciting incident]** , must leave **[their old life/situation]** to achieve **[a concrete, executable goal]** ; through **[obstacle 1]** and **[obstacle 2]** , they ultimately face **[their fatal flaw / the real goal]** .

### The 7 Elements

| # | Element | Question | Anti-pattern |
|---|---------|----------|-------------|
| 1 | **Protagonist** | Who, specifically? | "A young woman" — no, *which* young woman? |
| 2 | **Inciting incident** | What specific event changes everything? | "Something happens" — no, *what* happens? |
| 3 | **Old life left behind** | What status quo is broken? | "Her normal life" — no, *whose* life, where, doing what? |
| 4 | **Concrete goal** | What can we *see* her achieve or fail at? | "Find herself" — invisible, unshootable, unverifiable |
| 5 | **Obstacle 1** | First major barrier (external or internal) | "Challenges arise" — name one |
| 6 | **Obstacle 2** | Second major barrier (escalation) | "Things get worse" — name the escalation |
| 7 | **Fatal flaw / real goal** | What's actually at stake beneath the surface? | "She learns a lesson" — again, invisible |

## How to Use

### Mode A: Critique

Feed the agent a story (summary, book report, script outline) and ask: "拆一下这个故事的 logline，看看骨架有没有问题。"

The agent:
1. Attempts to extract all 7 elements from the provided material
2. Marks each as ✅ (specific, verifiable) or ❌ (vague, generic, missing)
3. For ❌ elements, explains what's missing and what a stronger version would look like
4. 🔴 CHECKPOINT — 展示 7 元素分析表，让用户确认是否有遗漏或误判
5. Delivers a verdict: **有骨架** (spine exists) or **缺骨架** (no spine)
6. Optional — if the spine is solid, apply the Masterclass lens: is element 7 a test or a lesson? Does element 3 have moral weight? Do obstacles force value choices? Are specific details decorative or thematic?

### Mode B: Development

Feed the agent a premise or vague idea and ask: "帮我把这个写成 logline。"

The agent:
1. Extracts whatever specifics are present
2. For each missing/vague element, asks ONE focused question (not an interrogation — one at a time)
3. 🔴 CHECKPOINT — 每个问题问完后等待用户回答，不连续追问
4. Iterates until all 7 elements are concrete
5. 🔴 CHECKPOINT — 所有元素确认后，展示完整 logline 草案；用户确认后再输出最终版
6. Produces the final logline

### Mode C: Comparison

Compare two stories by their loglines to identify structural similarities or one's superior specificity.

Output structure:
1. Extract logline for Story A and Story B separately
2. 🔴 CHECKPOINT — 展示两边的 7 元素提取结果
3. Produce a side-by-side comparison table:

| # | Element | Story A | Story B | Winner |
|---|---------|---------|---------|--------|
| 1-7 | ... | ... | ... | A / B / Tie |

4. Deliver summary: which story has a stronger spine and why

## Examples

### ❌ Bad (vague)
> 一个勇敢的女孩，在灾难发生后，踏上旅程寻找真相，最终发现了自己真正的力量。

**Why it fails**: Every element is a placeholder. "勇敢的女孩" = anyone. "灾难" = anything. "真相" = invisible. "真正的力量" = invisible. This catches 40% of YA novels.

### ✅ Good (specific)
> 一个靠偷窃为生的12岁聋哑女孩，在孤儿院被查封后，必须在三天内找到她失散的双胞胎妹妹——唯一的线索是妹妹耳后的一颗痣；她潜入三个不同的寄养家庭，每次都晚到一步；最后她发现妹妹一直在找她，而她自己才是被领养走的那个。

**Why it works**: Every element is concrete. Age. Disability. Skill. Three-day countdown. The goal (find sister) is verifiable — we will know if she succeeds. The obstacles are specific locations. The twist at element 7 is both specific and emotionally coherent with the setup.

## The Masterclass: From Spine to Theme

The 7-element template diagnoses whether a story has a backbone. But a backbone exists to carry weight. The masters — Dostoevsky, Dickens — show us that the same seven slots can be filled with details that are not just *specific*, but *thematically loaded*.

### Element 7 Is a Test, Not a Lesson

Dostoevsky's protagonists don't "learn a lesson." They live out an idea to its breaking point — and the story is the experiment.

| Character | Stated goal (element 4) | Real goal (element 7) | Why it works |
|-----------|------------------------|----------------------|--------------|
| Raskolnikov | Prove he's a "great man" above morality | Discover whether his conscience can be killed | The real goal is a *test* with two possible outcomes — he might succeed at the stated goal and fail at the real one, or vice versa |
| Prince Myshkin | Bring goodness to a corrupt world | Prove that pure goodness can *survive* in that world | The answer is devastating precisely because the question was genuine |

> **Rule**: Element 7 should be a test with two possible outcomes, not a lesson with one. "She learns to trust" is a lesson (and a weak element 7). "She must decide whether love is worth the risk of betrayal — knowing she might be wrong" is a test. A lesson tells you the answer; a test makes you watch the experiment.

### Element 3 Has Moral Weight

Dickens' characters don't just leave "their old life" — they leave a world the novel has already shown to be morally charged.

| Character | Old life (element 3) | Moral weight |
|-----------|---------------------|--------------|
| Oliver Twist | The workhouse | Not just a place — an institution the novel indicts as evil. Leaving it isn't just location change; it's rejecting a system that denies the poor their humanity. |
| Pip | Blacksmith's forge | Humble, honest, loved. The tragedy is he *wants* to leave it — his arc is realizing what he discarded. |

> **Rule**: Ask "what does leaving this life *cost* the protagonist, and what does that cost reveal about what the story values?" If the old life has no moral weight, element 3 is just scenery.

### Obstacles That Force a Choice (Elements 5-6)

A generic obstacle blocks. A thematic obstacle forces the protagonist to choose between two things the story has established as valuable.

| Generic obstacle | Thematic obstacle | What's at stake |
|---|---|---|
| "The villain captures her friend" | "She can save her friend by betraying the very principle she set out to prove" | Her stated goal vs. her moral identity |
| "He runs out of money" | "He inherits money from the person whose values he's spent the whole story rejecting" | Survival vs. integrity |
| "The bridge collapses" | "The bridge is the one thing he built with his father — destroy it to stop the enemy, or let the enemy cross" | Duty vs. memory |

Dostoevsky's obstacles are *moral*: Raskolnikov isn't blocked by police — he's blocked by his inability to live with what he did. Dickens' obstacles are *institutional*: the Circumlocution Office doesn't just delay — it incarnates the theme that bureaucracy destroys human life.

> **Rule**: Each obstacle should force a choice between two values the story has made the reader care about. If the choice is easy, the obstacle is weak.

### Thematic Specificity

The original template says specificity is the only signal. The refinement: *specificity must carry thematic weight.* Every concrete detail should be the tip of an iceberg.

| Random specificity | Thematic specificity | The iceberg beneath |
|---|---|---|
| "She's a 12-year-old pickpocket" | "She steals because the orphanage taught her that love must be earned with money" | The story is about transactional love and its cost |
| "He's a 35-year-old programmer" | "He codes because algorithms feel safer than people — and he's about to be proven wrong" | The story is about the limits of rational control |
| "She's deaf" | "She's deaf in a family that communicates only through shouting matches" | The deafness isn't decoration — it's the physical form of her core isolation |

When auditing a logline, ask: *could I replace this specific detail with a random one and the story would still work?* If yes, the detail is decorative. If the story would collapse without it, the detail is thematic.

## Pitfalls

1. **Theme ≠ logline.** "关于爱与牺牲" is a theme, not a logline. A logline describes *what happens*, not *what it means*.
2. **The goal must be visible.** "Find happiness", "discover herself", "learn to trust" — if you can't film it, it's not a logline.
3. **"被迫离开" matters.** Without a clear BEFORE → AFTER contrast at element 3, there's no stakes. The audience needs to feel what was lost.
4. **Element 7 is the hardest — and the most important.** If the "real goal" is the same as the stated goal, the story is flat. There must be a shift from what the protagonist *thinks* she wants to what she *actually* needs.
5. **If you can't write it down in 3-5 sentences, the story probably has structural problems.** This is not a writing exercise — it's a diagnostic tool.

## Guardrails

What this skill must NOT do:

| # | 禁止行为 | 原因 | 正确做法 |
|---|---------|------|---------|
| 1 | **替用户编造缺失元素** | 骨架是用户的，不是 agent 的 | 只提问、不替答；用户说"不知道"就标记 ❌ |
| 2 | **评价故事好坏** | 技能只诊断骨架完整度，不评判审美价值 | 只说"有骨架/缺骨架"，不说"好故事/烂故事" |
| 3 | **输入太短时强行凑 7 元素** | 一句话梗概不可能拆出 7 个元素 | 明确告诉用户"信息不足，至少需要一段情节描述" |
| 4 | **Mode C 自由发挥比较结论** | 没有模板的比较容易变成读后感 | 必须用结构化对比表，两列对齐逐元素比 |
| 5 | **问连环炮式问题** | Mode B 一次一个问题，不是审讯 | 每轮只问一个，等用户回答再继续 |
| 6 | **用英文输出中文用户的结果** | 用户用中文提问就用中文回答 | 检测输入语言，保持输出语言一致 |

## Failure Recovery

When things go wrong, here's what to do:

| 症状 | 一线修复 | 仍失败则 |
|------|---------|---------|
| 用户输入只有一句话，无法提取 7 元素 | 回应用户："信息不足——你至少需要一段情节描述（3-5句话），告诉我主角是谁、发生了什么、她想要什么。" | 让用户选：给更多信息 / 只分析已有元素并标记其余为 ❌ / 切换为 Mode B 逐元素挖掘 |
| 用户输入是非叙事文本（论文、散文、对话） | 回应："这是 [文本类型]，logline 分析需要的是故事/情节描述。如果你有这个想法的故事版本，请发给我。" | 不强行分析 |
| Mode B 用户连续三轮回答"不知道" | 标记该元素为 ❌，跳下一个元素 | 三轮后主动问："要不要先跳过这个，回头再补？" |
| 两个故事差异太大（Mode C 无法逐元素比较） | 分两列展示各自的 7 元素填充情况，不强行判 Winner | 总结各自的骨架强弱，不做逐元素对决 |
| 用户用非中英文提问 | 尝试理解并用相同语言回应 | 无法识别语言时用英文回应并说明 |

## Output Format

```markdown
## Logline Analysis: [Story Title]

| # | Element | Status | Content |
|---|---------|--------|---------|
| 1 | Protagonist | ✅/❌ | ... |
| 2 | Inciting incident | ✅/❌ | ... |
| 3 | Old life | ✅/❌ | ... |
| 4 | Concrete goal | ✅/❌ | ... |
| 5 | Obstacle 1 | ✅/❌ | ... |
| 6 | Obstacle 2 | ✅/❌ | ... |
| 7 | Fatal flaw / real goal | ✅/❌ | ... |

### Verdict: 有骨架 / 缺骨架

### Compiled Logline
[the assembled logline in Chinese]

### Gaps
[list each ❌ element with specific suggestions]
```
