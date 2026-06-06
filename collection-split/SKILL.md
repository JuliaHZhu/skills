---
name: collection-split
description: "Use when splitting a short story collection into individual stories before atomic analysis. Handles Sherlock Holmes, short story anthologies, linked story cycles. Each story becomes its own atoms.md via novel-split."
version: 1.0.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Architecture, Novel Analysis, Short Stories, Collections, Story Splitting]
    related_skills: [novel-split, novel-tag]
    requires_toolsets: [file, terminal]
---

# Collection Split — Short Story Collections

A short story collection isn't a novel. Each story is an independent narrative unit with its own structure, pacing, and engine. Before running `novel-split`, you need to split the collection into individual stories.

## When to Use

- You have a short story collection (Sherlock Holmes, Dubliners, The Martian Chronicles, etc.)
- The text contains multiple independent narratives under one cover
- You want to analyze each story's structure separately, not treat the whole book as one continuous narrative

**Do not use for**: novels (use `novel-split` directly), essay collections (use paragraph-based splitting), or collections where stories share a continuous plot (treat as a novel).

## Storage

```
./analysis/<collection-name>/
├── index.md              ← story list with metadata
├── <story-slug-01>/
│   ├── source.md         ← story text
│   └── atoms.md          ← atoms (after novel-split)
├── <story-slug-02>/
│   ├── source.md
│   └── atoms.md
└── ...
```

`<collection-name>` = short English slug (e.g., `sherlock-adventures`).
`<story-slug>` = story title slug (e.g., `scandal-in-bohemia`).

## Phase 1: Split Collection into Stories

### Step 1: Identify story boundaries

Look for:
- Explicit story titles (e.g., "A Scandal in Bohemia", "The Red-Headed League")
- Numbered sections (I. / II. / III.)
- Clear narrative endings + new beginnings
- Table of contents (if available)

### Step 2: Extract each story

For each story identified:
1. Create `./analysis/<collection-name>/<story-slug>/source.md`
2. Write the full story text into it
3. Record in index.md

### Step 3: Write index.md

```markdown
# Collection: The Adventures of Sherlock Holmes
## Author: Arthur Conan Doyle
## Total stories: 12
## Analyzed: 0/12

| # | Story | Slug | Words | Status |
|---|-------|------|-------|--------|
| 1 | A Scandal in Bohemia | scandal-in-bohemia | 8,200 | pending |
| 2 | The Red-Headed League | red-headed-league | 9,400 | pending |
| 3 | A Case of Identity | case-of-identity | 7,100 | pending |
| ... | ... | ... | ... | ... |
```

## Phase 2: Atomic Split per Story

After collection is split, run `novel-split` on each story. The agent should:

1. Read index.md to see which stories are still `pending`
2. For each pending story: read `source.md` → follow novel-split rules → write `atoms.md`
3. Update index.md: `pending` → `atoms-ready`

Or batch: "split all pending stories" → process each one sequentially.

## Phase 3: Tag per Story (Optional)

After atoms are ready, run `novel-tag` on each story. The agent can:

- Tag one story: "tag scandal-in-bohemia"
- Tag all: "tag all atoms-ready stories"
- Update index.md: `atoms-ready` → `tagged`

## Cross-Story Analysis

Once multiple stories are analyzed, cross-story insights emerge:

```
✓ Collection stats: 12 stories, 104,000 words total
  Average story: 8,700 words / 58 atoms
  Clue density range: 8% (Bohemia) to 35% (Speckled Band)
  Twist frequency: 0.3/story (most stories don't have one)
  Resolution density: consistent 5-8% across all stories
```

This is where Architecture Bee earns its name — not just analyzing one story, but seeing patterns across the collection.

## Constraints

- Each story gets its own directory. Do not mix atoms across stories.
- Story slugs: lowercase, hyphens, no special chars. Derive from title.
- If a story is very short (<2,000 words), it might only have 10-15 atoms. That's fine.
- The index.md tracks progress. Update it after each operation.
- For very large collections (50+ stories): process in batches of 10, report progress.
