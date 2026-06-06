---
name: novel-tag
description: "Use when labeling novel atoms with engine tags. Two modes: Doyle mode (dialogue≤50%) = 10 base tags at atom level. Christie mode (dialogue>50%) = all 14 tags at atom level — dialogue-round atoms naturally contain contradiction/performance/interrogation/omission within a single atom."
version: 1.3.0
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

Two modes, auto-selected by dialogue ratio (from novel-split report):

- **Doyle mode** (dialogue ≤50%): 10 base tags. Small observation-point atoms.
- **Christie mode** (dialogue >50%): all 14 tags. Large dialogue-round atoms — contradiction, performance, interrogation, and omission are visible *within* a single atom.

No separate Relations layer needed. In Christie mode, the atom IS the exchange unit.

## When to Use

- You have an `atoms.md` from `novel-split` and want to add engine labels
- The split report tells you which mode to use

## Storage

```
./analysis/<work-name>/<segment-slug>/
├── source.md          ← original text (reference only)
└── atoms.md           ← INPUT: untagged → OUTPUT: tagged (in-place)
```

- **Input**: `atoms.md` with `[untagged]` markers
- **Output**: same file, tags updated in-place
- Header updated: `Tagged: No` → `Tagged: Yes`

---

## Doyle Mode — 10 Tags (dialogue ≤50%)

Watson is *watching*. Atoms are small observation points. Each atom carries 1-3 tags.

| Tag | Meaning | Judgment Rule |
|-----|---------|---------------|
| **clue** | Fragment pointing to truth | If deleted, reader loses a reasoning path |
| **misdirection** | Deliberate red herring | If deleted, reader would NOT be deceived |
| **tension** | Urgency/threat escalation | Time pressure, approaching threat, rising stakes |
| **revelation** | Partial truth emerges | Reader's "aha" moment |
| **motive** | Why a character acts | Psychological reason for behavior |
| **method** | How something was done | Mechanism of crime/action |
| **character** | Character building / relationship | Pure character work, doesn't advance mystery |
| **setting** | Environment / atmosphere | Pure spatial/mood, no clue information |
| **twist** | Expectation overturned | Reader thought A, turns out B |
| **resolution** | Loose end tied / callback paid off | Earlier foreshadowing cashes out |

Rules: 1-3 tags per atom. Primary function first. Mutual exclusion: `clue` vs `misdirection`, `revelation` vs `twist`.

---

## Christie Mode — 14 Tags (dialogue >50%)

Atoms are **dialogue rounds**. A single atom captures: question → answer → evasion → contradiction → follow-up. The full exchange dynamic is visible within the atom.

### Base 10 (same as Doyle)

All 10 base tags apply. Tag as usual.

### Extension +4 (visible within dialogue-round atoms)

| Tag | Meaning | How it's visible in a dialogue-round atom |
|-----|---------|------------------------------------------|
| **contradiction** | Two accounts/perspectives conflict | Atom contains both: A says X, B says Y that contradicts X. The conflict is inside the atom |
| **omission** | What's NOT said — avoidance, silence | Atom contains a question AND an answer that isn't an answer. The gap is in the atom |
| **performance** | Character playing a role | Atom captures the full act: the setup, the fake persona, the fishing. Performance spans the atom |
| **interrogation** | Q&A itself is the reasoning engine | Atom IS the Q&A cycle. Who asks, who answers, who evades — all in one atom |

### Christie Tagging Rules

- 1-3 tags per atom, same as Doyle
- `contradiction`: use when the atom contains conflicting claims. Don't also tag `misdirection` unless the conflict is *deliberately* deceptive
- `performance`: use when the atom's dialogue is a character acting. Don't also tag `character` — character is real; performance is mask
- `interrogation`: use when the atom's Q&A structure itself drives the investigation. Can coexist with `clue` (process + result)
- `omission`: use when a question gets a non-answer within the atom. Don't tag `misdirection` unless the evasion is deliberately deceptive

### Christie Examples

```
Tommy posed as an art collector, approaching the suspect with easy charm.
"Oh, I've been looking for a piece exactly like this. Wherever did you find it?"
The suspect warmed to the flattery and began describing the gallery—and the dealer.
Tommy nodded along, already memorizing the name.

→ [performance] [interrogation] [clue]
performance: the whole atom is Tommy acting as a collector
interrogation: the Q&A structure — ask → flatter → extract
clue: dealer's name extracted
```

```
"I was at home all evening."
"But your landlady says you didn't return until nine."
"I don't know what she's talking about. She must have confused the days."
The inspector wrote something down without looking up.

→ [contradiction] [tension]
contradiction: "home all evening" vs "returned at nine" — both in the atom
tension: the inspector's silent note-taking ratchets pressure
Not misdirection — not clear yet if it's a lie or a mistake
```

```
"Where were you on Tuesday?"
"What a lovely painting behind you. Is that a Turner?"
"I asked about Tuesday."
"I've always loved art. My mother was a painter, you know..."
The detective waited.

→ [omission] [performance]
omission: three answers, none answers the question
performance: playing the art enthusiast to deflect
```

---

## After Tagging

```
✓ Doyle mode: scandal-in-bohemia
  124 atoms / 10 tags active
  clue 22% / tension 18% / character 15% / ...
```

```
✓ Christie mode: the-tuesday-club
  203 atoms / 14 tags active (dialogue 68%)
  clue 18% / tension 22% / interrogation 12% / performance 8% / contradiction 5% / omission 3% / ...
```
