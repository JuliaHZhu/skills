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
4. Delivers a verdict: **有骨架** (spine exists) or **缺骨架** (no spine)

### Mode B: Development

Feed the agent a premise or vague idea and ask: "帮我把这个写成 logline。"

The agent:
1. Extracts whatever specifics are present
2. For each missing/vague element, asks ONE focused question (not an interrogation — one at a time)
3. Iterates until all 7 elements are concrete
4. Produces the final logline

### Mode C: Comparison

Compare two stories by their loglines to identify structural similarities or one's superior specificity.

## Examples

### ❌ Bad (vague)
> 一个勇敢的女孩，在灾难发生后，踏上旅程寻找真相，最终发现了自己真正的力量。

**Why it fails**: Every element is a placeholder. "勇敢的女孩" = anyone. "灾难" = anything. "真相" = invisible. "真正的力量" = invisible. This catches 40% of YA novels.

### ✅ Good (specific)
> 一个靠偷窃为生的12岁聋哑女孩，在孤儿院被查封后，必须在三天内找到她失散的双胞胎妹妹——唯一的线索是妹妹耳后的一颗痣；她潜入三个不同的寄养家庭，每次都晚到一步；最后她发现妹妹一直在找她，而她自己才是被领养走的那个。

**Why it works**: Every element is concrete. Age. Disability. Skill. Three-day countdown. The goal (find sister) is verifiable — we will know if she succeeds. The obstacles are specific locations. The twist at element 7 is both specific and emotionally coherent with the setup.

## Pitfalls

1. **Theme ≠ logline.** "关于爱与牺牲" is a theme, not a logline. A logline describes *what happens*, not *what it means*.
2. **The goal must be visible.** "Find happiness", "discover herself", "learn to trust" — if you can't film it, it's not a logline.
3. **"被迫离开" matters.** Without a clear BEFORE → AFTER contrast at element 3, there's no stakes. The audience needs to feel what was lost.
4. **Element 7 is the hardest — and the most important.** If the "real goal" is the same as the stated goal, the story is flat. There must be a shift from what the protagonist *thinks* she wants to what she *actually* needs.
5. **If you can't write it down in 3-5 sentences, the story probably has structural problems.** This is not a writing exercise — it's a diagnostic tool.

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
