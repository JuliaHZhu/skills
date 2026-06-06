---
name: novel-tag
description: "Use when labeling novel atoms with engine tags. Two-layer system: (1) atom-layer 10 base tags — clue, misdirection, tension, revelation, motive, method, character, setting, twist, resolution. (2) relation-layer 4 tags — contradiction, omission, performance, interrogation — annotated in ## Relations section at end of atoms.md. Dialogue-heavy works (>50% dialogue) activate relation layer."
version: 1.2.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Architecture, Novel Analysis, Structural Analysis, Narrative Engine, Tagging, Detective Fiction, Dialogue Analysis]
    related_skills: [novel-split]
    requires_toolsets: [file]
---

# Novel Engine Tagging

Two-layer labeling system:

- **Atom layer**: 10 base tags per atom — what function does this atom serve?
- **Relation layer**: 4 extension tags — what pattern exists *between* atoms?

The 4 extension tags (contradiction, omission, performance, interrogation) describe **relationships**, not single-atom properties. They cannot be tagged atom-by-atom — they only become visible when you compare atoms.

## When to Use

- You have an `atoms.md` file from `novel-split` and want to add engine labels
- Dialogue-heavy works (>50% dialogue, e.g. Christie): the relation layer captures "dialogue as reasoning engine"

**Do not use for**: academic papers, essays, or non-fiction.

## Storage

```
./analysis/<work-name>/<segment-slug>/
├── source.md          ← original text (reference only, not modified)
└── atoms.md           ← INPUT: untagged atoms → OUTPUT: tagged atoms + ## Relations
```

- **Input**: `atoms.md` with `[untagged]` markers
- **Output**: same `atoms.md` — atom tags updated in-place, `## Relations` appended at end
- Updates file header: `Tagged: No` → `Tagged: Yes`

---

## Layer 1: Atom Tags (10 base — always active)

Every atom gets 1-3 tags from this set.

| Tag | Meaning | Judgment Rule |
|-----|---------|---------------|
| **clue** | Fragment pointing to truth | If deleted, the reader loses one reasoning path |
| **misdirection** | Deliberate red herring | If deleted, the reader would NOT be deceived |
| **tension** | Urgency/threat escalation | Time pressure, approaching threat, rising stakes |
| **revelation** | Partial truth emerges | Reader's "aha" moment. Clue is a fragment; revelation snaps it into place |
| **motive** | Why a character acts | Psychological reason for behavior |
| **method** | How something was done | Mechanism of crime/action. Separate from motive: why vs how |
| **character** | Character building / relationship | Pure character work. Does NOT advance the mystery |
| **setting** | Environment / atmosphere | Pure spatial/mood description. No clue information |
| **twist** | Expectation overturned | Reader thought A, turns out B. Revelation adds a piece; twist flips the table |
| **resolution** | Loose end tied / callback paid off | Earlier foreshadowing cashes out here |

### Atom Tagging Rules

- 1-3 tags per atom. Most get 1-2.
- Primary function first. If 80% tension + 20% character → tag `[tension]` only.
- When in doubt, use `[other]`.
- Mutual exclusion: `clue` vs `misdirection`, `revelation` vs `twist`, `character` vs `motive`.

### Atom Tagging Workflow

1. Read `atoms.md`, find `[untagged]` atoms, process 200 at a time
2. For each atom: read text → consult deck → pick 1-3 tags
3. Update: `[untagged] [180 chars] [dialogue]` → `[tension] [clue] [180 chars] [dialogue]`
4. Update header: `Tagged: Yes`

---

## Layer 2: Relations (4 tags — dialogue >50% only)

**Why not atom-level**: these describe patterns *between* atoms. A single atom cannot be "contradiction" — contradiction exists between atom #12 and atom #27. Interrogation is the Q&A rhythm across #15→#18→#22.

Append a `## Relations` section at the bottom of `atoms.md`:

```markdown
## Relations

### contradiction
- #012 ↔ #027: A says home at 8pm, B says A returned at 9pm — timeline conflict
- #045 ↔ #089: witness claims red car, suspect's neighbor says blue car

### omission
- #033 → #035: asked about the knife, responds with weather story — deliberate evasion
- (none found in this segment)

### performance
- #008–#015: Tommy poses as art collector, entire exchange is a performance
- #052–#058: suspect plays dumb when asked about bank records

### interrogation
- #018 → #022 → #025: three-round Q&A, each answer narrows the timeline
- (none found in this segment)
```

### Relation Tags

| Tag | What it captures | How to spot it |
|-----|-----------------|----------------|
| **contradiction** | Two atoms give conflicting information | Scan for pairs of atoms where facts don't align. Mark both atom IDs |
| **omission** | Character avoids answering a natural question | Look at atom N (question asked), atom N+1 (answer evaded). The gap between them is the omission |
| **performance** | A sequence of atoms where a character is acting | Scan for 3+ consecutive atoms where a character plays a role. Mark the range (#M–#N) |
| **interrogation** | Q&A pattern where the questioning itself drives revelation | Look for 3+ atoms forming a question→answer→follow-up chain |

### How to Spot Relations (after atom tagging is complete)

1. **contradiction**: re-read all clue-tagged atoms. Any pair that conflicts? Mark.
2. **omission**: scan dialogue-heavy chunks. Where does a question get a non-answer? Mark.
3. **performance**: scan for 3+ consecutive dialogue atoms where a character's stated identity doesn't match their behavior. Mark the range.
4. **interrogation**: scan for chains of 3+ dialogue atoms with escalating Q&A tension. Mark the chain.

### Relation Constraints

- Only annotate relations when dialogue >50%.
- `(none found in this segment)` is a valid entry — don't force it.
- Mark atom IDs, not just "chapter 3 has contradictions." Be specific.
- Performance ranges: mark the first and last atom of the performance sequence.

---

## Tagging Examples

### Atom layer (all works)

```
"How long you been waiting?"
"Three hours. He hasn't come out."
"Impossible. The back door?"
"Blocked off."

→ [tension] [clue] [dialogue]
```

### Atom + Relation layer (Christie style)

Atom tags:
```
#008 Tommy posed as an art collector, approaching the suspect with easy charm.
"Oh, I've been looking for a piece exactly like this. Wherever did you find it?"
The suspect warmed to the flattery and began describing the gallery—and the dealer.

→ [clue] [dialogue]
(atom-level only: clue. Performance and interrogation go in Relations, not here.)
```

Relations:
```markdown
## Relations

### performance
- #008–#015: Tommy as art collector — entire exchange is a fishing performance

### interrogation
- #018 → #022 → #025: three-round Q&A — each answer narrows the timeline
```

Critically: the atom itself is tagged `[clue]` (it contains a clue: the dealer's name). But the *fact that it's a performance* is annotated in Relations, not on the atom.

---

## After Tagging

```
✓ Tagged: scandal-in-bohemia
  124 atoms labeled — base 10 tags
  Mode: narrative-driven (dialogue 35%) — relation layer NOT activated

  Distribution: clue 22% / tension 18% / character 15% / revelation 8% / ...
```

```
✓ Tagged: the-tuesday-club
  203 atoms labeled — base 10 + relation layer
  Mode: dialogue-heavy (dialogue 68%) — relation layer active

  Atom distribution: clue 18% / tension 22% / character 12% / ...
  Relations: contradiction 3 / omission 2 / performance 1 / interrogation 4
```
