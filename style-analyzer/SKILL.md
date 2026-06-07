---
name: style-analyzer
description: "Analyze a published paper's writing style across three dimensions: relevance, sentence/paragraph DNA, and stealable patterns. Supports single-paper analysis, batch processing to build a style gene pool, and browsing the pool by field/method/journal/verdict. Use when: 'analyze this paper's style', '拆文笔', '文笔DNA', '模仿这篇', '批量分析', '我的基因库', '基因库有什么'."
version: 1.1.0
author: JuliaHZhu (adapted from HKUSTDial/Supervisor-Skills framework)
license: CC-BY-4.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Writing Style, Academic Writing, Paper Analysis, Style Imitation]
    related_skills: [pre-submission-reviewer, idea-evaluator, intro-drafter]
    source: https://github.com/JuliaHZhu/skills
---

# Style Analyzer — 文笔 DNA 卡片

Analyze a published paper's writing style and produce a **Style DNA Card** — a structured reference for imitating the paper's writing patterns in your own work.

The goal is NOT to judge quality. It is to describe **how** the paper is written so you can steal the technique.

## When to Use

**Single paper analysis:**
- You found a well-written paper in your field and want to write like it.
- You're starting a new section and want a concrete style reference.
- You want to understand why a paper "reads well" — not the content, but the craft.
- The user asks to "analyze this paper's style", "拆文笔", "文笔DNA", "模仿这篇", "how is this written", "write like Teece".

**Batch + gene pool:**
- The user asks to "批量分析论文", "build my style gene pool", "批量生成文笔卡片".
- The user gives a list of paper URLs/paths and says "分析这些".
- The user asks "我的基因库", "基因库有什么", "浏览卡片", "文笔基因库", "style pool", "show my style cards".
- The user asks to filter the pool: "只看战略管理的卡片", "筛出 top journal 的".

## When NOT to Use

- The user wants a content review or logic audit. Use `pre-submission-reviewer`.
- The user wants to evaluate whether the idea is good. Use `idea-evaluator`.
- The user needs help structuring their own paper. Use `tech-paper-template` or `intro-drafter`.
- The paper is in a completely different field with no transferable style patterns. Say so and decline.

---

## Step 1: Get the Paper

Accept input as:
- arXiv URL → `web_extract`
- Local PDF/MD path → `fs_read_file`
- Open-access journal URL → `web_extract`
- Pasted text (sections or full)

If the paper is behind a paywall and the user only has partial text, work with what's available. Flag missing sections.

---

## Step 2: Relevance Assessment

🔴 **CHECKPOINT** — Ask the user for their research field/topic if unknown. Do NOT assume.

Before analyzing style, assess whether imitation makes sense:

| Dimension | What to Check |
|-----------|---------------|
| **Field distance** | Same sub-field? Same broad discipline? Completely different? |
| **Method distance** | Same method (SEM / case study / theory / experiment)? Adjacent? Different paradigm? |
| **Journal tier** | Top journal (ASQ, SMJ, AMJ)? Strong field journal? Lower tier? |
| **Writing tradition** | US business school style? European sociological style? CS conference style? |

Output a relevance verdict:
- ✅ **Highly imitable** — same field + same method + top journal
- ⚠️ **Partially imitable** — same field but different method, or adjacent field
- ❌ **Low transferability** — different discipline entirely; patterns may not translate

---

## Step 3: Style DNA Analysis

### 3A. Sentence DNA

Sample 15-20 sentences from the Introduction and Discussion (these sections carry the most stylistic signature).

| Metric | What to Observe | Example Finding |
|--------|----------------|-----------------|
| Avg sentence length | Count words per sentence across sample | 28 words avg |
| Length variation | Ratio of longest to shortest; pattern (stable / breathing / erratic) | 3:1 ratio, breathing pattern |
| Complex sentence frequency | Sentences with ≥2 subordinate clauses | ~1-2 per paragraph |
| Sentence opening pattern | Subject-first? Adverbial clause opener? Transition word? | 70% subject-first, 20% "However/In contrast/First" |
| Sentence ending pattern | Punchy short close? Qualifier? Citation? | 60% end on the main claim, 30% end on a qualifier |

Describe the pattern in one sentence:
> "Long declarative sentences that build a case, followed by a short punchline sentence that delivers the conclusion. Ratio roughly 3 long : 1 short."

### 3B. Paragraph DNA

Sample 5-8 paragraphs from the Introduction and Literature Review.

| Metric | What to Observe | Example Finding |
|--------|----------------|-----------------|
| Opening sentence type | Topic sentence (states the point) / Transition (links from previous) / Question (raises an issue) | 70% direct topic sentence |
| Closing sentence type | Summary restatement / Hook to next paragraph / Abrupt stop | 50% summary, 40% hook |
| Paragraph length | Sentence count, consistency | 4-7 sentences, very consistent |
| Internal structure | Claim-evidence-warrant? Claim-counterclaim-resolution? Narrative arc? | Claim → evidence → warrant, tight 3-move structure |
| Citation placement | Citations in middle? End? Integrated into sentence flow? | Integrated mid-sentence: "As Teece (2007) argues, ..." |

Describe the paragraph pattern in one sentence:
> "Paragraphs open with a claim, support with 2-3 sentences of evidence/reasoning, and close with either a summary or a hook. Citations are woven into the sentence rather than parenthetical."

### 3C. Lexical DNA

Scan vocabulary patterns. Don't list every word — identify preferences.

| Metric | What to Observe | Example Finding |
|--------|----------------|-----------------|
| Academic register | Density of formal academic vocabulary | High — "conceptualize", "operationalize", "delineate" |
| Abstract vs. concrete | Ratio of abstract nouns to concrete examples | Abstract-heavy (3 abstract : 1 concrete) |
| Verb choice | Action verbs (demonstrate, reveal) vs. stative (is, has, exists) | Action-dominated (70% action verbs) |
| Adjective use | Restrained (only when needed) or abundant (descriptive style) | Restrained — adjectives serve precision, not decoration |
| Jargon density | Field-specific terminology per paragraph | ~5-8 field terms per paragraph |

### 3D. Voice & Stance

| Metric | What to Observe | Example Finding |
|--------|----------------|-----------------|
| Personal pronoun | "we" / "I" / "this paper" / "the author(s)" / passive avoidance | "we" dominant |
| Certainty level | Assertive ("demonstrates", "shows") vs. cautious ("suggests", "indicates", "may") | Assertive in claims, cautious in implications |
| Hedging density | % of sentences with hedging (may, might, could, suggest, appear, likely) | ~15% — low hedging, confident voice |
| Reader address | Direct ("as we will show") vs. distant ("the following sections demonstrate") | Direct, reader-inclusive "we" |

---

## Step 4: ✂️ Stealable Patterns

This is the most actionable section. Extract **concrete, reusable writing templates** from the paper.

For each pattern, provide:
- **Name**: short label
- **Template**: fill-in-the-blank formula
- **Where found**: which section
- **Why it works**: one sentence

```
### Definition Formula
Template: "[Construct] refers to the capacity to [specific action verb] 
          [object/domain] in order to [purpose/outcome]."
Found in: Literature Review, pages 3-5
Why: Packs the construct name, mechanism, domain, and purpose into one sentence.

### Hypothesis Setup
Template: "While prior research has established [known finding], 
          it remains unclear whether [boundary condition / new context]. 
          We argue that [theoretical logic], because [mechanism]."
Found in: Hypothesis Development, every H section
Why: Gap → logic → prediction in three moves. Reproducible across all hypotheses.

### Discussion Opening
Template: "The central insight from our findings is that [one-sentence takeaway]. 
          This challenges the prevailing view that [prior assumption] 
          and suggests that [new implication]."
Found in: Discussion, first paragraph
Why: Opens with the punchline, not a summary. Reviewer reads the first sentence and already knows the contribution.

### Limitation Framing
Template: "[Specific limitation]. However, [why it's not fatal / how future work addresses it]."
Found in: Discussion, limitations paragraph
Why: Names the limitation without apologizing. Every limitation has a counter-move.
```

Aim for **5-8 patterns** per paper. Fewer for short/poorly-written papers.

---

## Step 5: Compile the Style DNA Card

Write the final card to the user's workspace. Each card MUST include a YAML frontmatter block for machine readability — this is what powers the gene pool browser.

```markdown
---
paper_id: Teece2007
paper_title: "Explicating Dynamic Capabilities: The Nature and Microfoundations of (Sustainable) Enterprise Performance"
first_author: Teece
year: 2007
field: strategic management
method: theory/conceptual
journal: Strategic Management Journal
journal_tier: top
verdict: "✅"
pattern_count: 6
analyzed_date: 2026-06-07
---

# Style DNA Card: Teece2007

## Relevance
| Field | Method | Journal | Verdict |
|-------|--------|---------|---------|
| same | same | top (SMJ) | ✅ Highly imitable — same field, top journal |
...
```

**After writing the card to `~/.hermes/cache/style-cards/<paper-id>.md`**, update the pool index.

### Step 5A: Update index.json

The file `~/.hermes/cache/style-cards/index.json` is the machine-readable gene pool index. After every card write, update it:

```json
{
  "updated": "2026-06-07T16:00:00",
  "total_cards": 1,
  "cards": {
    "Teece2007": {
      "paper_title": "Explicating Dynamic Capabilities",
      "first_author": "Teece",
      "year": 2007,
      "field": "strategic management",
      "method": "theory/conceptual",
      "journal": "Strategic Management Journal",
      "journal_tier": "top",
      "verdict": "✅",
      "pattern_count": 6,
      "analyzed_date": "2026-06-07"
    }
  }
}
```

- If `index.json` doesn't exist, create it with the new card as the only entry.
- If it exists, add the new card to `cards` dict, increment `total_cards`, update `updated`.
- If re-analyzing an existing paper, update the entry — don't duplicate.

🔴 **CHECKPOINT** — Show the completed card to the user. Ask: "Does this capture the paper's style? Any patterns I missed?"

---

## Step 6: Gene Pool Browser — 基因库浏览

When the user asks "我的基因库", "基因库有什么", "浏览卡片", "style pool", "show my style cards", or wants to filter the pool — read from the gene pool and present results.

### 6A. Pool Overview

Read `~/.hermes/cache/style-cards/index.json`. If it doesn't exist or `total_cards` is 0:

```
📭 基因库为空。还没有分析过任何论文。
   用 "分析这篇论文" 来添加第一张文笔 DNA 卡片。
```

If cards exist, output a summary table:

```
🧬 文笔基因库 — 共 N 张卡片

| Paper | Author | Year | Field | Method | Journal | Verdict |
|-------|--------|------|-------|--------|---------|---------|
| Teece2007 | Teece | 2007 | strategic mgmt | theory | SMJ 🏆 | ✅ |
| ... | ... | ... | ... | ... | ... | ... |
```

### 6B. Filtered View

When user applies a filter (e.g., "只看战略管理", "筛出 top journal", "只看 ✅"):

1. Read `index.json`
2. Filter by the specified dimension(s)
3. Show the filtered table with filter description above

Supported filters:
- `field` — match against card's `field` field (fuzzy match)
- `method` — match against card's `method` field
- `journal_tier` — exact match on `top` / `field` / `lower`
- `verdict` — exact match on `✅` / `⚠️` / `❌`
- `author` — match against `first_author`

```
🔍 筛选: field=strategic, journal_tier=top — 共 N 张
[filtered table]
```

### 6C. Pool Stats

When the user asks "基因库统计" or "stats":

```
📊 基因库统计

卡片总数: N
字段分布:
  strategic management: 5
  entrepreneurship: 3
  organization theory: 2
方法分布:
  empirical (SEM): 4
  theory/conceptual: 3
  case study: 2
  experiment: 1
期刊层级:
  top: 6
  field: 3
  lower: 1
可模仿性:
  ✅  Highly imitable: 5
  ⚠️  Partially imitable: 4
  ❌  Low transferability: 1
```

### 6D. Keyword Search

When the user asks "基因库搜 <keyword>" or "find cards about <topic>":

Search across all `.md` card files in `~/.hermes/cache/style-cards/` using `search_files` for the keyword. Report matching cards with the surrounding context line.

---

## Step 7: Batch Mode — 批量分析

When the user provides a list of papers and says "批量分析", "分析这些论文", "build my gene pool", "批量生成文笔卡片":

### 7A. Parse the List

Accept:
- Multiple arXiv URLs (one per line)
- Multiple local file paths
- A list of paper names + authors (user will provide text for each later if needed)
- Mixed format

If the list is ambiguous, ask the user to clarify which papers.

### 7B. Process Each Paper

For each paper in the list:

1. Check `~/.hermes/cache/style-cards/` — if a card already exists for this paper, mark it `⏭️ SKIP (already in pool)`
2. Run **Steps 1–5** for the paper
3. Write the card + update `index.json`
4. Mark progress: `✅ Teece2007 done, 2/5`

🔴 **BATCH RULE**: Do NOT ask the CHECKPOINT question after each individual card in batch mode — it would block the pipeline. Trust the Steps 1-5 process. Only show the final batch summary.

If a paper fails (paywall, too short, inaccessible):
- Mark it `❌ FAILED: <paper-id> — <reason>`
- Continue to the next paper

### 7C. Batch Summary

After all papers processed:

```
🧬 批量分析完成

| Status | Paper | Details |
|--------|-------|---------|
| ✅ | Teece2007 | 6 patterns, ✅ highly imitable |
| ✅ | Eisenhardt1989 | 5 patterns, ✅ highly imitable |
| ⏭️ | Barney1991 | Already in pool |
| ❌ | PaperX | Paywall — need text |

3 processed, 1 skipped, 1 failed
基因库现在有 N 张卡片
```

Then automatically show the updated pool overview (Step 6A).

---

## Failure Modes & Fallback

| Trigger | What Went Wrong | Fix |
|---------|----------------|-----|
| `web_extract` returns empty / paywall | Paper not accessible | Try `fs_read_file` if local copy exists; else tell user "I can't access this paper — can you paste the Introduction and Discussion sections?" |
| Paper text < 500 words | Too short to sample | Tell user: "Need at least 500 words for meaningful analysis. Can you provide more of the paper?" Do NOT produce a card from insufficient data |
| User's research field unknown | Can't assess relevance | Ask: "What field are you writing in? (management / CS / economics / ...)" |
| Paper in completely different discipline | Low transferability | Still produce the card, but verdict = ❌ Low transferability. Flag specific dimensions that won't translate (e.g., "CS papers use passive voice heavily; management papers prefer active we") |
| User pastes only one section (e.g., just Intro) | Can't sample Discussion for voice contrast | Flag: "Analysis based on Introduction only. Discussion patterns not assessed." Still produce partial card |
| Can't identify 5 stealable patterns | Paper is short, formulaic, or poorly written | Produce 3-4 patterns if that's all there is. Do NOT fabricate patterns. Note: "Only N patterns found — paper has limited stylistic variation" |
| Same paper analyzed before | Duplicate effort | Check `~/.hermes/cache/style-cards/` for existing card. If found: "This paper already has a Style DNA Card. Show existing card or re-analyze?" |

---

## After Writing the Card

Tell the user:
```
✓ Style DNA Card: Teece2007
  Saved: ~/.hermes/cache/style-cards/Teece2007.md
  
  Verdict: ✅ Highly imitable — same field, top journal
  6 stealable patterns extracted
  
  Use it: "Write my Hypothesis section in Teece2007 style"
```

## Anti-Patterns — Do NOT Do

| # | Anti-Pattern | Why It's Wrong | Correct Approach |
|---|-------------|---------------|------------------|
| 1 | **Judge content quality** | This skill is about style, not substance. "This argument is weak" is off-topic | Only comment on writing: sentence structure, word choice, paragraph rhythm |
| 2 | **Produce a card from < 500 words** | Can't sample meaningfully. Card will be noise | Refuse and ask for more text |
| 3 | **Fabricate patterns for a bare paper** | If the paper only has 2 distinct patterns, say so. Don't invent 6 | Report "Only N patterns found" |
| 4 | **Use the same template sentences for every paper** | Makes cards indistinguishable. Each paper has unique DNA | Extract paper-specific patterns, not generic advice |
| 5 | **Analyze only the Abstract** | Abstracts are compressed; they don't reflect paragraph rhythm or sentence variation | Always analyze Introduction and Discussion, which carry the most stylistic signature |
| 6 | **Skip the relevance assessment** | User needs to know whether imitation even makes sense before investing time | Always produce a verdict (✅/⚠️/❌) before the DNA analysis |
| 7 | **Overwrite existing style cards silently** | User may have annotated the card or rely on a previous analysis | Check for existing card first; if found, ask "Show existing or re-analyze?" |
| 8 | **Compare to the user's own writing** | This skill analyzes published papers, not the user's draft. Mixing the two confuses the output | Only analyze the input paper. If user wants their own writing reviewed, use `pre-submission-reviewer` |

## Constraints

- Sample at least 15 sentences and 5 paragraphs. Don't extrapolate from 3 sentences.
- If the paper is in a completely different discipline, flag low transferability but still produce the card. The user decides.
- Don't judge content quality. "This argument is weak" is off-topic. Only comment on style.
- Store the card on disk. Don't just reply with it — the user needs it for future sessions.
- If the user's own research field/topic is unknown, ask briefly. Use "management/strategy/entrepreneurship" as default if not specified.
