---
name: collection-split
description: "Use when splitting a larger work into natural segments before atomic analysis. Two modes: (1) short story collections → individual stories, (2) detective/mystery novels → investigation phases (案发→初查→线索→误导→突破→对峙→收束). Each segment becomes its own directory with source.md and atoms.md."
version: 1.1.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Architecture, Novel Analysis, Detective Fiction, Short Stories, Story Splitting, Narrative Structure]
    related_skills: [novel-split, novel-tag]
    requires_toolsets: [file, terminal]
---

# Segment Split — Collections & Detective Novels

Split a larger work into natural narrative segments. Two modes:

**Mode A — Short story collections**: each story = one segment
**Mode B — Detective/mystery novels**: each investigation phase = one segment

Before running `novel-split` atom-by-atom, you need these segments — they're the right granularity for structural analysis.

## When to Use

- Short story collections (Sherlock Holmes, Dubliners, etc.)
- Detective/mystery novels (Holmes novels, Christie, Chandler, etc.)
- Linked story cycles (The Martian Chronicles, Winesburg, Ohio)
- Any work where the natural narrative unit is larger than a chapter but smaller than the whole book

**Do not use for**: standalone novels without clear phase structure (use `novel-split` directly), essay collections, or non-fiction.

## Storage

```
./analysis/<work-name>/
├── index.md              ← segment list
├── <segment-slug>/
│   ├── source.md         ← segment text
│   └── atoms.md          ← after novel-split
├── <segment-slug>/
│   ├── source.md
│   └── atoms.md
└── ...
```

## Mode A: Collection → Stories

Split a collection into individual stories by identifying story titles, numbered sections, or clear narrative endings followed by new beginnings.

### index.md format

```markdown
# Collection: The Adventures of Sherlock Holmes
## Mode: collection
## Author: Arthur Conan Doyle
## Segments: 12
## Analyzed: 0/12

| # | Title | Slug | Words | Status |
|---|-------|------|-------|--------|
| 1 | A Scandal in Bohemia | scandal-in-bohemia | 8,200 | pending |
| 2 | The Red-Headed League | red-headed-league | 9,400 | pending |
| ... | ... | ... | ... | ... |
```

## Mode B: Detective Novel → Investigation Phases

For detective/mystery novels, split by **case progression**, not by chapter. A 200-page novel might have 6-8 segments, each spanning multiple chapters.

### Standard phase template

| # | Phase | Slug | What happens | Typical signals |
|---|-------|------|-------------|-----------------|
| 1 | 案发 | crime | Crime discovered, initial scene, victim found | Body discovered, crime reported |
| 2 | 初查 | initial-investigation | Detective arrives, basic facts gathered, key players introduced | Interviews begin, scene examined |
| 3 | 线索 | clue-gathering | Evidence collected, witnesses interviewed, theories form | Detective visits locations, gathers items |
| 4 | 误导 | red-herring | False lead emerges, wrong suspect, tension from wrong direction | Suspicion falls on innocent party |
| 5 | 突破 | breakthrough | Key insight, turning point, puzzle pieces click | Detective has "aha" moment |
| 6 | 对峙 | confrontation | Facing the culprit, climax, stakes at maximum | Detective confronts suspect |
| 7 | 收束 | resolution | Explanation of the crime, tying loose ends | Detective explains the case |

**Not every novel has all 7 phases.** Some merge phases, some skip them, some loop back. Adapt to the actual text — the template is a guide, not a straitjacket.

If a phase is very long (e.g., clue-gathering spans 80 pages), split it further: `clue-gathering-1`, `clue-gathering-2`.

### Phase-specific index.md

```markdown
# Novel: The Hound of the Baskervilles
## Mode: detective-novel
## Author: Arthur Conan Doyle
## Total words: 59,000
## Segments: 6

| # | Phase | Slug | Words | Chapters | Status |
|---|-------|------|-------|----------|--------|
| 1 | 案发 | crime | 6,200 | Ch.1-2 | pending |
| 2 | 初查 | initial-investigation | 11,000 | Ch.3-5 | pending |
| 3 | 线索 | clue-gathering | 18,000 | Ch.6-9 | pending |
| 4 | 突破 | breakthrough | 8,500 | Ch.10-12 | pending |
| 5 | 对峙 | confrontation | 9,300 | Ch.13-14 | pending |
| 6 | 收束 | resolution | 6,000 | Ch.15 | pending |
```

## After Splitting

Each segment gets `novel-split` (atomize) then `novel-tag` (label). Update index.md status: `pending` → `atoms-ready` → `tagged`.

## Cross-Segment Analysis

Once tagged, compare segments:

**Collection mode:**
```
Clue density range: 8% (Bohemia) → 35% (Speckled Band)
Twist frequency: 0.3/story
```

**Detective novel mode:**
```
Clue density by phase:
  案发: 12%  初查: 22%  线索: 38%  突破: 15%  对峙: 5%  收束: 8%
  
Tension peaks at: 对峙 (68% of atoms tagged [tension])
Misdirection concentrated in: 线索 phase (all 4 misdirection atoms)
```

## Constraints

- Each segment gets its own directory. No mixing.
- Slugs: lowercase, hyphens. Derive from phase or story title.
- For detective novels: adapt the 7-phase template to the actual text. Don't force a phase that isn't there.
- For very short segments (<2,000 words, <15 atoms): merge into adjacent segment if it makes narrative sense.
- index.md tracks everything. Update after each operation.
