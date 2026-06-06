---
name: novel-split
description: "Use when analyzing novel structure: split novel text into atomic units by scene × topic. Each atom = one identifiable information unit (motive reveal, method hint, tension spike, etc.). Long dialogue at climax is split by topic, not by speaker."
version: 1.0.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Architecture, Novel Analysis, Atomic Notes, Writing Structure]
    related_skills: [novel-tag]
    requires_toolsets: [file, terminal]
---

# Novel Atomic Split

Split novel text into atomic units. One atom = one scene × one topic. This is the foundation for structural analysis — the atoms feed into `novel-tag` for engine labeling.

## When to Use

- You have a novel chapter (or full novel) and want to understand its structural composition
- You want to see what percentage of a chapter is dialogue vs. description vs. action — **and more importantly, what function each atom serves in the narrative engine**
- You plan to run `novel-tag` afterward to label atoms with engine tags (clue, misdirection, tension, etc.)
- You want to break down a long dialogue (e.g., final confrontation) into thematic units rather than treating it as one blob

**Do not use for**: academic papers (use paragraph-based splitting), non-fiction essays, or short story collections — use `collection-split` first to separate individual stories, then `novel-split` on each.

## Core Philosophy

1. **Scene is the primary boundary.** Location change, POV switch, or time jump = new atom. Always.
2. **Within a scene, topic is the boundary.** A long dialogue isn't one atom — it's multiple atoms divided by what information is being revealed.
3. **Dialogue is split by what's being said, not who's speaking.** "The protagonist reveals the motive" = one atom. "Then reveals the method" = another atom.
4. **Description is split by what's being described.** Environment vs. character appearance vs. atmosphere are separate atoms.
5. **Surface type is annotated at split time.** Each atom gets a surface marker (`[dialogue]`, `[description]`, `[action]`, `[inner]`, `[mixed]`) plus optional topic hints.

## Storage

novel-split works on **whatever directory it's pointed at**. Read `source.md` in the current analysis directory, write `atoms.md` in the same directory.

**Standalone novel** (no collection-split):
```
./analysis/<novel-name>/
├── source.md      ← put raw text here
└── atoms.md       ← output
```

**As part of pipeline** (after collection-split):
```
./analysis/<work-name>/
├── source.md              ← collection raw text
├── index.md
├── <segment-slug>/
│   ├── source.md          ← collection-split wrote this
│   └── atoms.md           ← novel-split writes this ← HERE
└── ...
```

`<novel-name>` or `<segment-slug>` = short English slug (e.g., `three-body-ch3`, `scandal-in-bohemia`).

## Split Rules

### Level 1: Scene Boundary (always split)

Any of these triggers a new atom:
- Location/scene change
- POV switch (character A → character B)
- Time jump ("Three days later...")
- Chapter/section break

### Level 2: Topic Boundary (split within same scene)

**Dialogue:**
- Same scene, continuous conversation → split by thematic content
- Protagonist reveals motive → 1 atom
- Protagonist then reveals method → 1 atom (separate)
- Two characters bantering/chatting (single function) → 1 atom
- Rule: one atom = one identifiable information unit

**Description:**
- Split by what's being described
- Environment description → 1 atom
- Character appearance → 1 atom
- Atmosphere/mood → 1 atom

**Action:**
- One continuous action sequence → 1 atom
- Action type shift (chase → standoff → escape) = each gets its own atom

**Inner Monologue:**
- One continuous thought stream → 1 atom
- Topic shift in thoughts → new atom

### Surface Markers (annotate at split time)

| Marker | Meaning |
|--------|---------|
| `[dialogue]` | Character dialogue (including speech tags) |
| `[description]` | Environment/appearance/sensory detail |
| `[action]` | Physical movement/event progression |
| `[inner]` | Inner monologue/stream of consciousness |
| `[mixed]` | Dialogue with heavy description/action mixed in |

Optional topic hints (add when confident):
- `[dialogue-motive]` / `[dialogue-method]` / `[dialogue-relationship]`
- `[description-setting]` / `[description-character]` / `[description-mood]`
- `[action-chase]` / `[action-confrontation]`

## Output Format

Save to `./analysis/<novel-name>/atoms.md`:

```markdown
# Atoms: <novel-name>
## Type: Novel
## Total atoms: <N>
## Tagged: No

## Chapter 1: <name>

#001 [untagged] [180 chars] [description-setting]
The alley smelled of coal smoke. Streetlights made the snow glow yellow.
Old Zhang huddled in his army coat, eyes fixed on the apartment door across the way.

#002 [untagged] [340 chars] [dialogue]
"How long you been waiting?"
"Three hours. He hasn't come out."
"Impossible. The back door?"
"Blocked off."
Old Zhang crushed his cigarette against the wall. Sparks jumped onto his hand. He didn't flinch.
"You're sure he went in at seven?"
"I watched him go in."

#003 [untagged] [120 chars] [action]
Old Zhang stood up suddenly. His coat fell to the ground.
He didn't pick it up. He walked straight toward the apartment door.
```

## Constraints

- Do NOT ask questions. Genre is fixed to novel.
- Write atoms.md immediately after splitting — do not accumulate in memory.
- For texts over 2,000 atoms: split in batches, append to file.
- Preserve original text verbatim. Do not edit or summarize.
- Surface markers are auxiliary — real labeling happens in `novel-tag`.
- Atom IDs are zero-padded (`#001`, `#002`, ...) for sortability.
