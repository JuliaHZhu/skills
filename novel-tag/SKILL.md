---
name: novel-tag
description: "Use when labeling novel atoms with engine tags. Deck-thinking: 14-tag taxonomy pre-loaded (10 base + 4 dialogue-heavy extension). Base: clue, misdirection, tension, revelation, motive, method, character, setting, twist, resolution. Extension (dialogue>50% only): contradiction, omission, performance, interrogation."
version: 1.1.0
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

Label novel atoms with **engine tags** — not surface labels like "dialogue" or "description", but structural labels that reveal the narrative engine: what function does this atom serve in the story's machinery?

Uses **Deck thinking**: the full 14-tag taxonomy is your deck of cards. For each atom, pick 1-3 cards that match. No more, no less.

## When to Use

- You have an `atoms.md` file from `novel-split` and want to add engine labels
- You want to answer questions like: "What's the clue-to-misdirection ratio in Chapter 3?" or "Where does the tension peak?"
- You're studying the structure of a mystery/thriller/suspense novel to understand its engine
- **Dialogue-heavy works** (>50% dialogue, e.g. Christie): the extension tags capture "dialogue as reasoning engine"

**Do not use for**: academic papers, essays, or non-fiction (different tag taxonomy needed).

## Storage

novel-tag reads and writes in the same directory:

```
./analysis/<work-name>/<segment-slug>/
├── source.md          ← original text (reference only, not modified)
└── atoms.md           ← INPUT: untagged atoms → OUTPUT: tagged atoms (in-place update)
```

- **Input**: `atoms.md` with `[untagged]` markers
- **Output**: same `atoms.md` with `[untagged]` replaced by engine tags
- The skill updates the file header: `Tagged: No` → `Tagged: Yes`
- Source text (`source.md`) is never modified — reference only

## The Tag Deck

### Base 10 — Universal Detective Fiction Tags

Designed for narrative-driven works (Doyle / Watson-narrator style). Applicable to all detective fiction.

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

### Extension +4 — Dialogue-Heavy Tags

**Use only when dialogue >50% of total atoms** (e.g. Christie, Sayers, Marsh). These capture "dialogue as reasoning engine" — the mechanism where conversation IS the investigation.

| Tag | Meaning | Judgment Rule | vs. Base Tag |
|-----|---------|---------------|--------------|
| **contradiction** | Two accounts/perspectives conflict | If deleted, the reader loses a logical inconsistency. A says X at 8pm, B says X at 9pm — not about who's lying, but that the information *itself* conflicts | vs `misdirection`: misdirection is *deliberate* deception; contradiction may be accidental, but the *conflict itself* is the signal |
| **omission** | What's NOT said — avoidance, silence, evasion | Character naturally *could* mention something but doesn't. The gap itself carries information | vs `misdirection`: misdirection is actively saying something false; omission is *passively* not saying something true |
| **performance** | Acting / pretending / fishing in dialogue | Character plays a role that isn't themselves (playing dumb, fake familiarity, feigned weakness, probing questions) | vs `character`: character is real personality building; performance is a character *acting* — a mask, not the face |
| **interrogation** | Dialogue as questioning game — back-and-forth inquiry IS the reasoning process | The structure of Q&A itself drives the investigation. Who asks, who answers, who evades — the *process* reveals more than individual answers | vs `clue`: clue is an information fragment (result); interrogation is the *method and process* of obtaining information |

## Usage Rules

1. **Base 10 always available.** Every work gets these.
2. **Extension +4 only when dialogue >50%.** Don't use `contradiction` / `omission` / `performance` / `interrogation` on narrative-heavy works.
3. **1-3 tags per atom.** Most get 1-2. Don't pad.
4. **Primary function first.** If 80% is interrogation and 20% reveals a clue → tag `[interrogation]`, not `[clue]`.
5. **When in doubt, use `[other]`.** Better vague than wrong.

### Mutual Exclusion Notes

| Pair | Rule |
|------|------|
| `clue` vs `misdirection` | Truth or decoy? Pick one |
| `revelation` vs `twist` | Adding a piece or flipping the table? Pick one |
| `contradiction` vs `misdirection` | Info conflict or deliberate deception? Usually pick one, can coexist if both clearly present |
| `omission` vs `misdirection` | Passive silence or active lie? Can coexist |
| `performance` vs `character` | Acting or real? Pick one |
| `interrogation` vs `clue` | Process or result? Can coexist — interrogation is *how*, clue is *what* |

## Tagging Workflow

### Step 1: Determine mode

Check the atoms.md header or spot-check dialogue ratio. If dialogue >50%, activate the extension +4 tags.

### Step 2: Read the atoms

Open `./analysis/<work-name>/<segment-slug>/atoms.md`. Look for atoms marked `[untagged]`.

### Step 3: Tag in batches

Process 200 atoms at a time. For each atom:

1. Read the original text
2. Consult the Tag Deck (base 10, + extension 4 if applicable)
3. Pick 1-3 tags that best describe the atom's engine function
4. Update: `[untagged] [180 chars] [dialogue]` → `[tension] [clue] [180 chars] [dialogue]`

### Step 4: Repeat until done

Continue until all atoms are tagged. Update the file header: `Tagged: Yes`.

## Tagging Examples

### Doyle / Watson style (base 10)

```
"How long you been waiting?"
"Three hours. He hasn't come out."
"Impossible. The back door?"
"Blocked off."
Old Zhang crushed his cigarette against the wall. Sparks jumped onto his hand. He didn't flinch.

→ [tension] [clue] [dialogue]
Why: "Three hours" creates time pressure (tension). "Back door blocked off" is an information fragment (clue).
Not character — this advances the mystery, not the character arc.
```

### Christie style (base 10 + extension 4)

```
Tommy posed as an art collector, approaching the suspect with easy charm.
"Oh, I've been looking for a piece exactly like this. Wherever did you find it?"
The suspect warmed to the flattery and began describing the gallery—and the dealer.

→ [performance] [interrogation] [clue]
performance: acting as a collector
interrogation: fishing for information through feigned interest
clue: the dealer's name is extracted
```

```
"I was at home all evening."
"But your landlady says you didn't return until nine."

→ [contradiction] [tension]
contradiction: the two accounts don't match
tension: the confrontation is escalating
```

```
Asked directly about the missing knife, the suspect launched into a long story about the weather, the traffic, and what he had for lunch—never once touching the question.

→ [omission] [tension]
omission: deliberate avoidance of the topic
tension: the evasion creates pressure
```

## After Tagging

When all atoms are tagged, report a quick preview:

```
✓ Tagged: <novel-name>
  847 atoms labeled
  Mode: dialogue-heavy (dialogue 62%) — extension tags active

  Base distribution: clue 18% / tension 22% / character 12% / ...
  Extension distribution: interrogation 15% / performance 8% / contradiction 5% / omission 3%

  Next: compute full statistics or generate a PM template.
```
