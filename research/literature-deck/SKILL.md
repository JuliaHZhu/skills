---
name: literature-deck
description: "Use when managing academic literature as atomic notes and assembling paragraph drafts from them. Research deck system: blueprint → atoms → framework → assembled drafts. Human-driven pipeline with AI retrieval and assembly."
version: 1.0.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Literature Review, Atomic Notes, Paper Assembly, Deck System, Academic Writing]
    related_skills: [arxiv, ocr-and-documents, web_extract, todo]
    requires_toolsets: [terminal, file, web]
---

# Literature Deck — Atomic Notes to Paragraph Drafts

A human-driven research pipeline that turns full-text papers into tagged atomic notes, then assembles them into paragraph drafts according to a writing framework. The human sets the research agenda and reviews output; the AI handles retrieval, assembly, and progress tracking.

Think of it as a **deck of cards**: each atom is a card with tags. The human deals the hand (framework); the AI draws the right cards (atoms) and lays them out (paragraphs).

## When to Use

- You have a collection of academic papers and want to extract reusable evidence fragments
- You are writing a research paper and need to assemble literature-backed paragraphs systematically
- You want to track coverage: which hypotheses have enough supporting atoms, which gaps remain
- You prefer a structured, tag-based retrieval system over free-text search

**Do not use for**: fully autonomous paper writing (human must define the framework and review every paragraph), non-academic content assembly, or projects without a clear hypothesis structure.

## Core Philosophy

1. **Human sets the blueprint.** The `project.yaml` defines variables, hypotheses, and theories. AI never invents hypotheses.
2. **Human writes the framework.** The `outline.md` defines sections and paragraph order. AI infers which tags each paragraph needs, but human confirms for critical sections.
3. **AI assembles, human reviews.** AI retrieves atoms by tag, composes paragraph drafts, and flags weak evidence. Human edits the draft.
4. **State lives in files, not context.** Progress is tracked in `deck-progress.json`. The pipeline survives session restarts.
5. **Never overwrite silently.** Every assembly creates a new timestamped file. Git is recommended but not enforced.

## Four-Step Pipeline

<!-- ascii-guard-ignore -->
```
┌────────────────────────────────────────────────────────────────┐
│  Step 1: Setup Blueprint                                       │
│  Human writes project.yaml (variables, hypotheses, theories)   │
│       │                                                        │
│       ▼                                                        │
│  Step 2: Extract Atoms                                         │
│  Human reads papers; AI assists extracting atomic notes        │
│  Each atom = one evidence fragment + YAML frontmatter + tags   │
│       │                                                        │
│       ▼                                                        │
│  Step 3: Define Framework                                      │
│  Human writes outline.md; AI parses → section-to-tags map      │
│       │                                                        │
│       ▼                                                        │
│  Step 4: Assemble Deck                                         │
│  AI retrieves atoms by section tags, writes paragraph drafts   │
│  Output: timestamped draft files per section                   │
└────────────────────────────────────────────────────────────────┘
```
<!-- ascii-guard-ignore-end -->

## Project Structure

```
my_research_deck/
├── project.yaml          # Blueprint: variables, hypotheses, theories (human-written, read-only)
├── tag-registry.md       # Tag definitions and coverage targets
├── outline.md            # Writing framework: sections and paragraph flow
├── deck-progress.json    # State: current phase, completed sections, atom counts
├── atoms/                # Atomic notes extracted from papers
│   └── atom-{AuthorYear}-{type}-{seq}.md
├── papers/               # Full-text papers (source material)
│   └── {AuthorYear}-full.md
└── drafts/               # Assembled paragraph outputs (timestamped)
    └── 20250604-143022-section-intro.md
```

## Step 1: Setup Blueprint

The human defines the research architecture in `project.yaml`:

```yaml
variables:
  var_a:
    name: "Variable A"
    definition: "..."
    scale_source: ""
hypotheses:
  - id: H1
    path: "var_a → var_b"
    variables: [var_a, var_b]
    atoms_needed: 3
theories:
  - id: KBV
    name: "Knowledge-Based View"
```

**Phase guard**: If `deck-progress.json` shows phase > 1, warn before editing `project.yaml` (blueprint changes invalidate downstream atoms).

## Step 2: Extract Atoms

An atom is a single evidence fragment:

```markdown
---
source: Author2024
type: arg
tags: [H1, define_var_a]
---
# Claim summary
> "Direct quote with page number" (p.12)
```

**Atom types**:
| Type | Purpose | Example |
|------|---------|---------|
| `def` | Variable definition | `define_var_a` |
| `theo` | Theory grounding | `theory_KBV` |
| `arg` | Empirical argument | `H1` |
| `bridge` | Connecting two concepts | `H1`, `H2` |
| `gap` | Research gap | `gap_search` |
| `scale` | Measurement scale | `scale_var_a` |

**Commands**:
```bash
# Interactive extraction from a paper
python scripts/deck-cli.py extract papers/Author2024-full.md

# Batch extraction (AI-assisted, human confirms each)
python scripts/deck-cli.py extract --batch papers/
```

**After extraction**: `deck-progress.json` auto-increments atom counts per tag.

## Step 3: Define Framework

Human writes `outline.md` in free Markdown:

```markdown
# Introduction
## Background
We need to establish why var_a matters in this field.

## Gap
Despite advances in X, the role of var_a remains unclear.

# Theory
## KBV Foundation
Organizations as knowledge repositories.
```

**Parse to structured map**:
```bash
python scripts/deck-cli.py outline parse outline.md
# Generates: outline-map.yaml (section → inferred_tags)
```

**Human confirmation rule**:
- Sections tagged `define_*` or `theory_*` → AI auto-infers, no confirmation needed
- Sections tagged `H*` (hypothesis arguments) → AI presents inferred tags, waits for human confirmation

## Step 4: Assemble Deck

### Paragraph Assembly Template

When composing a draft, follow this structure for each paragraph:

```markdown
<!-- Section: [section_name] -->
<!-- Tags: [tag1, tag2] -->
<!-- Atoms used: N -->

[Transition from previous paragraph, if not first]

[Claim / Topic sentence]: State the main point of this paragraph,
clearly linking to the section's purpose.

[Evidence synthesis]: Integrate atom quotes into a coherent argument.
- Use 2-4 atoms per paragraph when available
- Group by logical flow (chronological, theoretical, or contrasting)
- Connect atoms with transitions: "Similarly," "In contrast," "Building on this," "However"

[Inline citations]: (AuthorYear) after each claim backed by an atom.
Use author-year format; include page numbers when atoms provide them:
  "...found significant effects (Smith2024, p.12)."

[Interpretation / So what?]: 1-2 sentences explaining why this evidence
matters for the hypothesis or theory. Do not end on a quote.

<!-- If weak evidence: -->
> [WEAK_EVIDENCE: tag H2 needs 5 atoms, found 2]
```

**Synthesis rules**:
1. **Never drop a quote without context.** Each atom must be introduced ("According to X...") or woven into the narrative.
2. **Vary sentence structure.** Do not start every sentence with "Author (Year) found..."
3. **End with interpretation.** Every paragraph must close with the human's analytical voice, not a citation.
4. **Flag conflicts.** If two atoms contradict, note: `[CONFLICTING_EVIDENCE: AuthorA2024 vs AuthorB2025]`

### Per-section assembly
```bash
python scripts/deck-cli.py assemble --section "Background"
# Output: drafts/20250604-143022-section-Background.md
```

**What happens inside**:
1. Read `outline-map.yaml` for the section's target tags
2. Search `atoms/` for atoms matching those tags
3. If atoms_needed > atoms_found:
   - Assemble anyway
   - Flag paragraph with `[WEAK_EVIDENCE: needs 3, found 1]`
   - Append a `TODO_ATOMS` block listing missing tags
4. Compose paragraph draft using atom quotes + synthesis
5. Append inline citations (e.g., `(Author2024)`)
6. Save as timestamped file

**Full assembly**:
```bash
python scripts/deck-cli.py assemble --all
# Generates one file per section in drafts/
```

## Menu & Commands

### Interaction Protocol (Human-in-the-Loop)

The skill operates in **interactive mode by default**. Hermes must confirm with the human before executing irreversible or consequential actions:

| Action | Hermes Behavior |
|--------|----------------|
| **Phase 1 → 2** (first atom extraction) | "I see you have N papers in `papers/`. Shall I help you extract atoms from `[papername]`?" |
| **Phase 2 → 3** (outline parse) | "Outline parsed. I inferred these tags for each section: [list]. Please review `outline-map.yaml` and confirm before assembling." |
| **Assemble a section** | "For section `[name]`, I found N atoms matching tags [tags]. Shall I assemble the draft?" — wait for `yes` |
| **Re-assemble** (already assembled) | "This section was assembled on [date]. Create a new version instead of overwriting?" — default: yes |
| **Phase guard triggered** | Explain risk, offer alternatives, request explicit confirmation: "⚠️ You are in phase X. [Action] may invalidate Y. Proceed? (yes/no/save-backup)" |
| **Weak evidence detected** | "Only N/M atoms found for `[tag]`. I can write a flagged draft or wait for more atoms. Which do you prefer?" |

**Non-interactive mode** (for scripting): All commands accept `--yes` to skip confirmations. Hermes uses this internally when acting as a scripted agent.

### Interactive Menu (default on skill trigger)
When the skill is triggered without explicit command, Hermes presents:

```
Literature Deck — Main Menu
[1] Setup / Edit Blueprint (project.yaml)
[2] Extract Atoms from Papers
[3] Define / Parse Writing Framework
[4] Assemble Paragraph Drafts
[s] Status & Coverage Dashboard
[q] Quit
```

Hermes asks: "Which step are you on?" and navigates accordingly.

### Direct Commands (for power users)

All commands accept `--project-dir <path>` to operate on a specific deck. 
Interactive mode is default; use `--yes` to skip confirmations when scripting.

| Command | Purpose |
|---------|---------|
| `deck init <project_name>` | Create project skeleton with templates |
| `deck extract <paper>` | Scaffold atom extraction from one paper |
| `deck outline parse <outline.md>` | Parse framework to tag map |
| `deck assemble --section <name>` | Assemble one section (prompts for confirmation) |
| `deck assemble --all` | Assemble all sections |
| `deck status` | Show phase, coverage, gaps |
| `deck coverage` | Display hypothesis-path coverage matrix |

### Templates Directory

The `templates/` folder contains starter files copied by `deck init`:

| File | Purpose |
|------|---------|
| `templates/project.yaml` | Blueprint template with example variables, hypotheses, theories |
| `templates/outline.md` | Writing framework template with standard academic sections |
| `templates/tag-registry.md` | Tag registry starter with coverage summary table |

These are **starting points**, not enforced schemas. Humans edit them freely.

## State & Phase Guards

### deck-progress.json

```json
{
  "project": "my_research",
  "current_phase": 2,
  "phases": {
    "1": {"status": "completed", "atoms_count": 45},
    "2": {"status": "in_progress", "sections_parsed": ["Intro", "Theory"]},
    "3": {"status": "pending", "sections_assembled": []}
  },
  "last_updated": "2026-06-04T14:30:00Z"
}
```

### Guard Rules

| Action | Required Phase | Guard Behavior |
|--------|---------------|----------------|
| Edit `project.yaml` | Phase 1 only | Warn if phase > 1; suggest `deck init --force` |
| Extract atoms | Phase 1 or 2 | Allow; increment counts |
| Parse outline | Phase 2 | Block if phase < 2 |
| Assemble section | Phase 3 | Block if phase < 3; if already assembled, create timestamped new file |
| Re-assemble section | Any phase 3+ | Never overwrite; always create `drafts/*-v2-*` |

### File Safety

- **No silent overwrites.** Every `assemble` writes a new file with ISO timestamp.
- **Atomic writes.** Draft files are written to `drafts/.tmp/` then moved on success.
- **Optional git integration.** If `.git/` exists, `deck status` shows uncommitted drafts.

## Monitoring & Coverage Dashboard

### Coverage Matrix

```bash
python scripts/deck-cli.py coverage
```

Output:
```
Hypothesis Path          Needed  Found  Status
H1: var_a → var_b        3       3      ✅ Complete
H2: var_b → var_c        5       2      ⚠️  Gap (need 3 more)
H3: var_a × mod → var_c  5       1      🚨 Critical (need 4 more)
```

### Status Command

```bash
python scripts/deck-cli.py status
```

Shows:
- Current phase
- Total atoms extracted
- Sections assembled / pending
- Missing tags list (auto-generated from `atoms_needed - atoms_filled`)

## Weak Evidence Handling

When a section cannot find enough atoms:

1. **Draft is still written** — the pipeline does not block.
2. **Flag inserted**: `[WEAK_EVIDENCE: tag H2 needs 5 atoms, found 2]`
3. **TODO block appended**:
   ```markdown
   <!-- TODO_ATOMS -->
   - [ ] H2: Need 3 more atoms (found: Author2024, Author2025)
   - [ ] define_var_c: Missing entirely
   <!-- END_TODO_ATOMS -->
   ```
4. Human reviews TODO block and decides: extract more atoms, adjust framework, or accept weak evidence.

## Input / Output Contracts

### Input

| File | Format | Who Writes | Mutability |
|------|--------|-----------|------------|
| `project.yaml` | YAML | Human | Immutable after phase 1 |
| `tag-registry.md` | Markdown | Human | Mutable (tags grow) |
| `outline.md` | Markdown | Human | Mutable before phase 3 |
| `atoms/*.md` | Markdown | Human + AI | Append-only |
| `papers/*.md` | Markdown | Human | Immutable |

### Output

| File | Format | Content |
|------|--------|---------|
| `deck-progress.json` | JSON | Phase state, counts |
| `outline-map.yaml` | YAML | Section → tags mapping |
| `drafts/*-section-*.md` | Markdown | Paragraph drafts with citations |
| `drafts/*-full-draft.md` | Markdown | Concatenated all sections |

## Composability

- **With `arxiv`**: Fetch papers before extracting atoms.
- **With `ocr-and-documents`**: Convert PDFs to Markdown before placing in `papers/`.
- **With `todo`**: Track `TODO_ATOMS` items as session tasks.
- **With `web_extract`**: Fetch online papers for atom extraction.

## Error Recovery & Edge Cases

### Atoms Directory Empty
If `atoms/` has no `.md` files:
- Hermes: "No atoms found in `atoms/`. You need to extract atoms from papers first (Step 2)."
- Do not proceed to assembly. Offer to help with extraction.

### outline-map.yaml Parse Failure
If `outline-map.yaml` is malformed or missing:
- Hermes: "Cannot read outline map. Please run `deck outline parse outline.md` first."
- If parse produces zero sections, warn: "Outline parsed but found 0 sections. Check that `outline.md` uses `##` or `###` headings."

### Missing Tags in Atoms
If a section requires tag `X` but no atom has it:
- During assembly: proceed with `[WEAK_EVIDENCE: tag X, found 0]`
- Append to `deck-progress.json` under `missing_tags` for tracking
- Hermes offers: "Tag X has zero atoms. Continue with weak evidence, or pause to extract more?"

### File Permission / IO Errors
If `deck-cli.py` cannot write to `drafts/`:
- Error: "Permission denied writing to drafts/. Check directory permissions or run from a writable location."
- Never crash silently. Always report the exact path that failed.

### Corrupted deck-progress.json
If `deck-progress.json` is unreadable:
- Hermes: "Progress file appears corrupted. I can recreate it, but phase history will be lost. Back up first?"
- Default: create backup `deck-progress.json.bak`, then reinitialize with `current_phase: 1`

### Blueprint Mismatch
If `project.yaml` is edited after atoms exist (detected by atom timestamps newer than `project.yaml` mtime):
- Warning: "Atoms were extracted after the last blueprint edit. If you changed hypotheses, existing atom tags may be stale."
- Recommend: `deck coverage` to check tag consistency, then selective re-tagging.

## Common Pitfalls

1. **Editing `project.yaml` after phase 1.** Changing hypotheses invalidates atoms tagged with old hypothesis IDs. The guard warns, but does not prevent. Use `deck init --force` if you really need to restart.

2. **Forgetting to parse the outline.** `outline.md` is human-readable; `outline-map.yaml` is machine-readable. Always run `deck outline parse` after editing the outline.

3. **Assuming AI knows which atoms are "best."** The deck system retrieves by tag match, not quality ranking. Human must review atom selection in the draft.

4. **Missing `deck-progress.json` in git.** If you delete or lose this file, the phase guards break. Treat it as source code.

5. **Overwriting drafts manually.** Never edit files in `drafts/` directly. If you need a revision, re-run `assemble` and edit the new file. Or, move the draft out of `drafts/` before editing.

6. **Chinese or non-English triggers in `tag-registry.md`.** Tag names must be ASCII-compatible (`H1`, `define_var`, `theory_KBV`) for global portability. Human-facing notes in atoms can be any language.

## Verification Checklist

- [ ] `project.yaml` exists and has at least one hypothesis with `atoms_needed`
- [ ] `tag-registry.md` lists all tags referenced in `project.yaml`
- [ ] `deck-progress.json` exists and `current_phase` is accurate
- [ ] `atoms/` directory has atoms with proper YAML frontmatter (`source`, `type`, `tags`)
- [ ] `outline.md` parsed successfully (`outline-map.yaml` generated)
- [ ] At least one draft generated in `drafts/`
- [ ] No `[WEAK_EVIDENCE]` flags in critical hypothesis sections (or human has reviewed them)
