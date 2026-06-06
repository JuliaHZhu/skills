---
name: novel-tag
description: "Use when labeling novel atoms with engine tags. Deck-thinking: the full 10-tag taxonomy is pre-loaded; for each atom, pick 1-3 tags that best describe its narrative engine function. Tags: clue, misdirection, tension, revelation, motive, method, character, setting, twist, resolution."
version: 1.0.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Architecture, Novel Analysis, Structural Analysis, Narrative Engine, Tagging]
    related_skills: [novel-split]
    requires_toolsets: [file]
---

# Novel Engine Tagging

Label novel atoms with **engine tags** — not surface labels like "dialogue" or "description", but structural labels that reveal the narrative engine: what function does this atom serve in the story's machinery?

Uses **Deck thinking**: the full 10-tag taxonomy is your deck of cards. For each atom, you pick 1-3 cards that match. No more, no less.

## When to Use

- You have an `atoms.md` file from `novel-split` and want to add engine labels
- You want to answer questions like: "What's the clue-to-misdirection ratio in Chapter 3?" or "Where does the tension peak?"
- You're studying the structure of a mystery/thriller/suspense novel to understand its engine

**Do not use for**: academic papers, essays, or non-fiction (different tag taxonomy needed).

## The Tag Deck (10 Cards)

Read these carefully. This is your full deck. Every atom gets tagged from this set.

| Tag | Meaning | Judgment Rule |
|-----|---------|---------------|
| **clue** | Fragment pointing to truth | If deleted, the reader loses one reasoning path. Can be an object, a line of dialogue, or an environmental detail |
| **misdirection** | Deliberate red herring | If deleted, the reader would NOT be deceived. Looks like a clue but is a decoy |
| **tension** | Urgency/threat escalation | Time pressure (countdown), approaching threat, or rising stakes |
| **revelation** | Partial truth emerges | The reader's "aha" moment. Unlike a clue (fragment), a revelation is a piece snapping into place |
| **motive** | Why a character acts | Psychological reason for behavior. Can be dialogue, memory, or third-party account |
| **method** | How something was done | Hint about or demonstration of the *mechanism* of the crime/action. Separate from motive — one is *why*, the other is *how* |
| **character** | Character building / relationship development | Pure character work. Does NOT advance the main mystery |
| **setting** | Environment / atmosphere building | Pure spatial/mood description. Does NOT carry clue information |
| **twist** | Expectation overturned | Reader thought A, turns out B. Unlike revelation (adding a piece), twist is flipping the table |
| **resolution** | Loose end tied / callback paid off | Earlier foreshadowing cashes out here. The story's "clasp" closing |

## Tagging Workflow

### Step 1: Read the atoms

Open `./analysis/<work-name>/<segment-slug>/atoms.md` (or wherever novel-split wrote it). Look for atoms marked `[untagged]`.

### Step 2: Tag in batches

Process 200 atoms at a time. For each atom:

1. Read the original text
2. Consult the Tag Deck definitions above
3. Pick 1-3 tags that best describe the atom's engine function
4. Update: `[untagged] [180 chars] [dialogue]` → `[tension] [clue] [180 chars] [dialogue]`

### Step 3: Repeat until done

Continue until all atoms are tagged. Update the file header: `Tagged: Yes`.

## Tagging Examples

```
Original:
"How long you been waiting?"
"Three hours. He hasn't come out."
"Impossible. The back door?"
"Blocked off."
Old Zhang crushed his cigarette against the wall. Sparks jumped onto his hand. He didn't flinch.

→ [tension] [clue] [dialogue]
Why: "Three hours" creates time pressure (tension). "Back door blocked off" is an information fragment (clue).
Not character — this advances the mystery, not the character arc.
```

```
Original:
He remembered meeting her twenty years ago. Same winter, same alley.
She wore a red coat, a flame in the snow.

→ [character] [description-setting]
Why: Pure memory + relationship establishment. Does not advance the main plot.
Not clue — this is emotional background, not a reasoning path.
```

## Tagging Principles

- **Primary function first.** If 80% of the atom builds tension and 20% has character flavor → tag `[tension]` only, not `[character]`.
- **When in doubt, use `[other]`.** Better to leave it vague than force a wrong label.
- **1-3 tags. Most atoms get 1-2.** Don't pad.
- **Dialogue ≠ automatic `[character]`.** Dialogue can carry clue, misdirection, motive, tension, or revelation. The `[character]` tag is only for pure character-building moments.
- **Mutual exclusion awareness:**
  - `[clue]` vs `[misdirection]` — truth or decoy? Pick one.
  - `[revelation]` vs `[twist]` — adding a piece or flipping the table? Pick one.
  - `[motive]` vs `[method]` — why or how? Can coexist, but rarely do.

## After Tagging

When all atoms are tagged, report a quick preview:

```
✓ Tagged: <novel-name>
  847 atoms labeled

  Tag distribution (spot-check of first 100 atoms):
  clue 22% / tension 18% / dialogue 35% / character 15% / revelation 5% / other 5%

  Next: compute full statistics or generate a PM template.
```
