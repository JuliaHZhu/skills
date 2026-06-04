---
name: task-ball-machine
description: "Use when managing daily tasks via a randomized ball-drawing lottery system. Triggers: '抽彩球', '任务抽奖', 'ball machine', 'task lottery', '今天抽球', '开始新周期'. Tasks are pre-loaded into category boxes as balls; each day you draw one per time slot."
version: 1.0.0
author: JuliaHZhu
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Productivity, Task Lottery, Daily Planning, Decision Fatigue, Gamification]
    related_skills: [todo]
    requires_toolsets: [terminal, file]
---

# Task Ball Machine — Daily Task Lottery

A randomized daily task allocation system. You pre-fill category "boxes" with numbered balls, each representing a task. Each day, you draw one ball per time slot from a randomly chosen box. Over a cycle, all balls are consumed — ensuring every category gets its fair share of attention.

Think of it as a **carnival lottery booth** for your todo list. Instead of staring at a blank page wondering what to do, you pull a lever and the machine tells you. Not happy with the draw? Put it back and draw again — but each ball can only land in one slot per cycle.

## When to Use

- You have recurring tasks across multiple life/work categories and struggle with decision fatigue
- You want to ensure no category is neglected over a month/quarter
- You prefer a playful, low-cognitive-load approach to daily planning
- You want to track completion streaks and cycle progress

**Do not use for**: time-sensitive deadline management (the lottery does not know deadlines), collaborative project scheduling (everyone would need the same machine), or tasks requiring strict sequencing (lottery is random, not ordered).

## Core Philosophy

1. **Human loads the machine.** You define categories, tasks, and quotas in `config.json` and `balls.json`. AI never invents your life priorities.
2. **Machine does the drawing.** Random selection removes human bias toward "easy" or "urgent" categories.
3. **Human decides completion.** The machine tracks; you mark done, edit, or redraw.
4. **State lives in files, not context.** `state.json` tracks draws per day. Survives restarts.
5. **Cycles have boundaries.** One cycle = one full set of balls. When empty, the machine requires a refill (new cycle).

## Two-File Architecture

| File | Role | Mutability |
|------|------|-----------|
| `config.json` | Cycle metadata + box definitions (quotas, emojis) | Immutable during cycle |
| `balls.json` | The ball library — every ball with content and difficulty | Immutable during cycle |
| `state.json` | Runtime state — shuffled stacks, daily draws, used balls | Mutable |

This separation means: **you can reset a cycle without rewriting your task library**. Just reshuffle and go.

## Core Concepts

### The Box
A category of tasks. Example boxes: `Work`, `Study`, `Health`, `Social`, `Rest`. Each box has:
- A quota (how many balls total)
- An emoji for visual flair
- A stack of ball IDs (shuffled at cycle start)

### The Ball
A single task. Each ball has:
- `id`: unique identifier (`BALL-{BOX}-{seq}`)
- `content`: what to do
- `difficulty`: `hard` (3h), `medium` (2.5h), `easy` (2h) — guides time blocking

### The Session (Time Slot)
A part of the day. Default slots:
- `morning` → 上午场
- `afternoon` → 下午场
- `evening` → 晚间场
- `overtime` → 加班场

### The Cycle
A bounded period (e.g., "May 2026"). At cycle start, all balls are shuffled into their box stacks. As days pass, balls move from `stack` to `used`. When all stacks are empty, the cycle is complete.

## Daily Workflow

### Morning Setup (Input: user says "今天抽球" / "draw today")

1. **Show current board** → `status`
   - Input: `data_dir` path
   - Output: today's sessions + box inventory + cycle progress
2. **Draw remaining slots** → `draw <session>` or `quick-draw`
   - Input: which sessions are empty
   - Output: one ball per empty session, with box/content/difficulty
   - **Edge case**: If all boxes are empty → prompt user to start `new-cycle`
3. **Present preview** to user before any destructive draw (see Checkpoints)

### During the Day (Input: user completes or wants to change a task)

4. **Mark done** → `complete <session>`
   - Input: session name
   - Output: confirmation + updated status
5. **Edit task** → `edit <session> <new_content>`
   - Input: session + new description
   - Output: confirmation + diff preview
6. **Redraw** → `redraw <session>` (with user confirmation)
   - Input: session name
   - Output: old ball returned to stack + new draw result
7. **Custom fill** → `fill <session> <box> <content>` (with preview)
   - Input: session + box + custom task text
   - Output: ball consumed + custom task logged as completed
8. **Free log** → `log <session> <content>`
   - Input: session + free text
   - Output: no ball consumed, task logged

### Evening Review (Input: user says "今天怎么样" / "review")

9. **Show today's summary** → `today`
   - Output: all 4 sessions with status icons
10. **Show cycle stats** → `stats`
    - Output: box completion rates + 7-day trend + streak + overall rate
11. **Show history** → `history [days]`
    - Output: recent days with session details

### Cycle Transition (Input: user says "开始新周期" / "new cycle")

12. **Archive & reset** → `new-cycle <name> <start> <end>` (with confirmation)
    - Input: new cycle name + date range
    - Output: old cycle archived, all balls reshuffled, days cleared

## Project Structure

```
task-ball-machine/
│─── config.json          # Cycle + box definitions (human-edited)
│─── balls.json           # Ball library (human-edited)
│─── state.json           # Runtime state (machine-managed)
└─── scripts/
    └─── ball-machine.py  # CLI engine
```

## Setup: Loading the Machine

### 1. Write config.json

```json
{
  "cycle_name": "June 2026",
  "cycle_start": "2026-06-01",
  "cycle_end": "2026-06-30",
  "duration_map": {
    "hard": 3.0,
    "medium": 2.5,
    "easy": 2.0
  },
  "boxes": {
    "Work":   { "emoji": "💼", "quota": 21 },
    "Study":  { "emoji": "📚", "quota": 21 },
    "Health": { "emoji": "🏃", "quota": 15 },
    "Rest":   { "emoji": "🧘", "quota": 14 }
  }
}
```

### 2. Write balls.json

```json
{
  "boxes": {
    "Work": {
      "emoji": "💼",
      "balls": [
        {"id": "BALL-WORK-001", "content": "Deep work: core project", "difficulty": "hard"},
        {"id": "BALL-WORK-002", "content": "Email and admin", "difficulty": "easy"},
        ... (quota total balls)
      ]
    },
    "Study": {
      "emoji": "📚",
      "balls": [
        {"id": "BALL-STU-001", "content": "Read one paper", "difficulty": "medium"},
        ...
      ]
    }
  }
}
```

Each box must have exactly `quota` balls. The CLI provides a `validate` command to check.

### 3. Initialize State

```bash
python scripts/ball-machine.py --data-dir . init
# Reads config.json + balls.json → creates state.json with shuffled stacks
```

## Commands

### Interactive Menu (default on skill trigger)

When the skill is triggered without explicit command, Hermes presents:

```
🎱 Task Ball Machine — Main Menu
[1] Draw for a session        (morning / afternoon / evening / overtime)
[2] Quick draw all remaining  (fill all empty slots for today)
[3] Mark session completed
[4] Redraw a session          (return ball, draw again)
[5] Custom fill               (use a ball but write your own content)
[6] Free log                  (record something without consuming a ball)
[s] Status & today's board
[p] Progress & stats
[n] New cycle
[q] Quit
```

### Direct Commands Reference

| Command | Args | Purpose |
|---------|------|---------|
| `init` | `[--force]` | Create state.json from config + balls. `--force` overwrites existing state. |
| `validate` | — | Check config/balls consistency |
| `draw` | `<session> [--box <box>]` | Draw one ball. `--box` forces a specific category. |
| `quick-draw` | — | Draw for all empty morning/afternoon/evening slots |
| `complete` | `<session>` | Mark a session completed |
| `redraw` | `<session>` | Return ball to stack and redraw |
| `edit` | `<session> <content...>` | Change task text for an already-drawn session |
| `fill` | `<session> <box> <content...>` | Custom task, consumes one ball from `<box>` |
| `log` | `<session> <content...>` | Free record, no ball consumed |
| `status` | — | Today's board + box inventory |
| `today` | — | Just today's sessions |
| `stats` | `[--days N]` | Cycle stats, streak, daily rates. Default: last 7 days |
| `history` | `[--days N]` | Recent daily history. Default: last 7 days |
| `new-cycle` | `<name> <start> <end>` | Reset for a new cycle. Dates: `YYYY-MM-DD` |

**Args legend:** `<required>` `[optional]` `...` = space-separated remainder

## State Format

### state.json

```json
{
  "cycle": {"name": "June 2026", "start": "2026-06-01", "end": "2026-06-30"},
  "boxes": {
    "Work": {
      "emoji": "💼",
      "stack": ["BALL-WORK-003", "BALL-WORK-007", ...],
      "used": ["BALL-WORK-001", ...]
    }
  },
  "days": {
    "2026-06-04": {
      "morning": {
        "box": "Work",
        "content": "Deep work: core project",
        "status": "completed",
        "ball_id": "BALL-WORK-001"
      },
      "afternoon": {
        "box": "Study",
        "content": "Read one paper",
        "status": "planned",
        "ball_id": "BALL-STU-003"
      },
      "evening": null,
      "overtime": null
    }
  }
}
```

**Resilience**: If `state.json` is corrupted on load, the engine:
1. Archives the corrupted file with a timestamp suffix
2. Attempts to recover from `state.json.bak`
3. Falls back to `init` if both fail

All writes are atomic (write to `.tmp`, then rename).

## Phase Guards & Checkpoints

### Automatic Blocks

| Action | Guard |
|--------|-------|
| `draw` | Block if session already drawn today |
| `complete` | Block if session not yet drawn |
| `redraw` | Block if session not yet drawn; returns old ball to stack |
| `new-cycle` | Archives old state, re-shuffles all balls, resets days |
| `init` | Warn if state.json already exists; use `--force` to overwrite |

### Human-in-the-Loop Checkpoints

Before executing any **destructive** action, Hermes MUST ask for confirmation using `clarify`:

| Action | Confirmation Prompt |
|--------|---------------------|
| `init --force` | "`state.json` already exists. Overwriting will erase today's draws and cycle progress. Confirm?" |
| `new-cycle` | "Starting a new cycle will archive all current progress and reshuffle balls. Confirm?" |
| `redraw` | "The old ball returns to the stack and may be drawn again. Confirm redraw?" |

Before executing any **creative** action that modifies user-facing content, Hermes MUST present a preview:

| Action | Preview Requirement |
|--------|---------------------|
| `fill` | Show the custom content and which box's ball will be consumed |
| `edit` | Show old → new content diff before saving |

### Daily Workflow Checkpoints

```
1. User says "draw" or "today" → Hermes runs `status` first to show current board
2. User says "new cycle" → Hermes shows current cycle summary, then asks confirm
3. User says "init" on existing dir → Hermes shows `validate` output, then asks confirm
```

## Monitoring

### Status Dashboard

```bash
python scripts/ball-machine.py status
```

Output:
```
📅 2026-06-04 (Wednesday)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌅 morning     💼  Deep work: core project          ✅ completed
🌞 afternoon   📚  Read one paper                   📝 planned
🌆 evening     (empty)                             —
🌙 overtime    (empty)                             —
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Box Inventory
💼 Work    ████████████░░░░░░░░  12/21 used
📚 Study   ██████░░░░░░░░░░░░░░   6/21 used
🏃 Health  ████████░░░░░░░░░░░░   8/15 used
🧘 Rest    ██████░░░░░░░░░░░░░░   6/14 used
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Cycle: June 2026 | 32/71 balls used (45%)
```

### Stats Report

```bash
python scripts/ball-machine.py stats
```

Shows:
- Per-box completion rate
- Daily completion trend (last 7 days)
- Current streak (consecutive fully-completed days)
- Overall cycle completion rate

## Composability

- **With `todo`**: Ball-machine sessions can be synced to the Hermes todo list for cross-system tracking.
- **With cron jobs**: Schedule a morning notification: "🌅 Time to draw your morning ball!"
- **With calendar**: Export `state.json` days to `.ics` or read calendar to block slots.

## Common Pitfalls

1. **Quota mismatch.** If `config.json` says quota=21 but `balls.json` only has 20 balls for that box, the cycle will end early for that box. Always run `validate` after editing.

2. **Editing balls mid-cycle.** Changing `balls.json` after `init` has no effect until `new-cycle`. The engine reads balls only at cycle start. If you need emergency changes, use `new-cycle` (resets everything).

3. **Forgetting to mark complete.** Uncompleted sessions at end of day hurt your streak. The machine tracks `planned` vs `completed`; only `completed` counts.

4. **Redrawing too much.** The `redraw` command returns the old ball to the stack — so you might draw it again tomorrow. Use sparingly; it is meant for "this task became impossible today," not "I don't feel like it."

5. **Losing state.json.** The backup mechanism handles corruption, but not deletion. Git-commit your machine directory, or at least back up `state.json`.

6. **`init --force` must delete `state.json` before Engine instantiation.** The `Engine` class auto-loads `state.json` on construction if it exists. A naive `init --force` that passes `--force` but does not `unlink()` the old file first will simply reload the old state and save it back unchanged.

7. **`fill` and `log` must guard against session collisions.** Both commands write into `day[session]` unconditionally. If the session already has a ball drawn, the old entry is silently overwritten. Always check `if session in day: return error` before writing.

8. **Variable shadowing in `new_cycle`.** The method parameter `name` (cycle name) can shadow the loop variable if you iterate `for name, info in boxes.items()`. Rename the loop variable to `box_name` to avoid accidentally writing cycle metadata into box keys.

## Quick Start

Copy the built-in templates to your working directory and edit them:

```bash
# Find where the skill templates live (Hermes skill directory)
SKILL_DIR="$(dirname $(python -c 'import ball_machine; print(ball_machine.__file__)'))"
# Or simply copy from the skill path:
cp ~/.hermes/skills/productivity/task-ball-machine/templates/config.json .
cp ~/.hermes/skills/productivity/task-ball-machine/templates/balls.json .
# Edit config.json and balls.json, then:
python scripts/ball-machine.py init
```

> Templates live at `~/.hermes/skills/productivity/task-ball-machine/templates/`.

## Input / Output Contracts

### Input

| File | Format | Who Writes | When |
|------|--------|-----------|------|
| `config.json` | JSON | Human | Once per cycle setup |
| `balls.json` | JSON | Human | Once per cycle setup |
| CLI args | Strings | Human | Daily interaction |

### Output

| File | Format | Content |
|------|--------|---------|
| `state.json` | JSON | Shuffled stacks, daily draws, used balls |
| `state.json.bak` | JSON | Automatic backup before each write |
| `stdout` | Text | Human-readable status, draw results, errors |

## Verification Checklist

- [ ] `config.json` has matching `cycle_start` / `cycle_end` dates
- [ ] Every box in `config.json` has a matching entry in `balls.json`
- [ ] Every box has exactly `quota` balls in `balls.json`
- [ ] `state.json` exists and has shuffled `stack` arrays
- [ ] At least one draw has been performed
- [ ] `stats` shows a reasonable completion rate (not 0%, not impossible 100%)
- [ ] Backup file `state.json.bak` exists (proves atomic writes are working)
