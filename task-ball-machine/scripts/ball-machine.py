#!/usr/bin/env python3
"""
Task Ball Machine CLI

Usage:
    python ball-machine.py --data-dir . init
    python ball-machine.py --data-dir . draw morning
    python ball-machine.py --data-dir . status
    python ball-machine.py --data-dir . stats
    python ball-machine.py --data-dir . new-cycle "July 2026" 2026-07-01 2026-07-31

All state lives in JSON files. No database, no context.
"""

import argparse
import json
import random
import sys
import time
from datetime import date, timedelta
from pathlib import Path


class Engine:
    SESSIONS = ["morning", "afternoon", "evening", "overtime"]
    DISPLAY = {
        "morning": "🌅 morning",
        "afternoon": "🌞 afternoon",
        "evening": "🌆 evening",
        "overtime": "🌙 overtime",
    }
    DIFFICULTY_EMOJI = {"hard": "🔴", "medium": "🟡", "easy": "🟢"}

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.state_path = self.data_dir / "state.json"
        self.balls_path = self.data_dir / "balls.json"
        self.config_path = self.data_dir / "config.json"
        self.state = self._load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def _load(self) -> dict:
        if not self.state_path.exists():
            return self._init()
        try:
            return json.loads(self.state_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            corrupted = self.state_path.parent / f"{self.state_path.stem}.json.corrupted.{int(time.time())}"
            try:
                self.state_path.rename(corrupted)
            except OSError:
                pass
            backup = self.state_path.with_suffix(".json.bak")
            if backup.exists():
                try:
                    data = json.loads(backup.read_text(encoding="utf-8"))
                    self.state_path.write_text(
                        json.dumps(data, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    return data
                except (json.JSONDecodeError, OSError):
                    pass
            return self._init()

    def _init(self) -> dict:
        cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
        balls = json.loads(self.balls_path.read_text(encoding="utf-8"))
        state = {
            "cycle": {
                "name": cfg["cycle_name"],
                "start": cfg["cycle_start"],
                "end": cfg["cycle_end"],
            },
            "boxes": {},
            "days": {},
        }
        for name, info in balls["boxes"].items():
            stack = [b["id"] for b in info["balls"]]
            random.shuffle(stack)
            state["boxes"][name] = {
                "emoji": info["emoji"],
                "stack": stack,
                "used": [],
            }
        return state

    def _save(self):
        data = json.dumps(self.state, ensure_ascii=False, indent=2)
        tmp = self.state_path.with_suffix(".json.tmp")
        try:
            tmp.write_text(data, encoding="utf-8")
            if self.state_path.exists():
                try:
                    bak = self.state_path.with_suffix(".json.bak")
                    bak.write_text(self.state_path.read_text(encoding="utf-8"), encoding="utf-8")
                except OSError:
                    pass
            tmp.rename(self.state_path)
        except OSError:
            try:
                self.state_path.write_text(data, encoding="utf-8")
            except OSError:
                pass

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _ball_lookup(self, box: str, ball_id: str) -> dict:
        balls = json.loads(self.balls_path.read_text(encoding="utf-8"))
        for b in balls["boxes"][box]["balls"]:
            if b["id"] == ball_id:
                return b
        return {"content": "Unknown task", "difficulty": "medium"}

    def _today(self) -> str:
        return str(date.today())

    def _day(self) -> dict:
        return self.state["days"].setdefault(self._today(), {})

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def draw(self, session: str, box: str = None) -> dict:
        day = self._day()
        if session in day:
            return {"ok": False, "error": f"{self.DISPLAY.get(session, session)} already drawn today"}

        candidates = []
        if box:
            if box not in self.state["boxes"]:
                return {"ok": False, "error": f"Box '{box}' does not exist"}
            candidates = [box]
        else:
            candidates = [n for n, b in self.state["boxes"].items() if b["stack"]]
            if not candidates:
                return {"ok": False, "error": "All boxes empty. Start a new cycle."}

        selected = random.choice(candidates)
        ball_id = self.state["boxes"][selected]["stack"].pop()
        self.state["boxes"][selected]["used"].append(ball_id)

        ball_info = self._ball_lookup(selected, ball_id)
        day[session] = {
            "box": selected,
            "content": ball_info["content"],
            "status": "planned",
            "ball_id": ball_id,
        }
        self._save()
        return {
            "ok": True,
            "message": f"✅ Drew {self.DISPLAY.get(session, session)}",
            "session": session,
            "block": {
                **day[session],
                "session": session,
                "difficulty": ball_info.get("difficulty", "medium"),
                "duration": {"hard": 3.0, "medium": 2.5, "easy": 2.0}.get(
                    ball_info.get("difficulty", "medium"), 2.5
                ),
            },
        }

    def quick_draw(self) -> dict:
        drawn = []
        for s in ["morning", "afternoon", "evening"]:
            if s not in self.state["days"].get(self._today(), {}):
                r = self.draw(s)
                if r["ok"]:
                    drawn.append(r)
        return {
            "ok": True,
            "message": f"✅ Quick draw complete: {len(drawn)} session(s)",
            "blocks": [d["block"] for d in drawn],
        }

    def complete(self, session: str) -> dict:
        day = self.state["days"].get(self._today(), {})
        if session not in day:
            return {"ok": False, "error": f"{session} not drawn yet"}
        day[session]["status"] = "completed"
        self._save()
        return {"ok": True, "message": f"✅ {self.DISPLAY.get(session, session)} completed"}

    def edit(self, session: str, content: str) -> dict:
        day = self.state["days"].get(self._today(), {})
        if session not in day:
            return {"ok": False, "error": f"{session} not drawn yet"}
        day[session]["content"] = content
        self._save()
        return {"ok": True, "message": f"✅ {self.DISPLAY.get(session, session)} updated"}

    def redraw(self, session: str) -> dict:
        day = self.state["days"].get(self._today(), {})
        if session not in day:
            return {"ok": False, "error": f"{session} not drawn yet"}

        old = day[session]
        box = old["box"]
        ball_id = old["ball_id"]
        self.state["boxes"][box]["stack"].append(ball_id)
        if ball_id in self.state["boxes"][box]["used"]:
            self.state["boxes"][box]["used"].remove(ball_id)
        del day[session]
        self._save()
        return self.draw(session)

    def fill(self, session: str, box: str, content: str) -> dict:
        if box not in self.state["boxes"]:
            return {"ok": False, "error": f"Box '{box}' does not exist"}
        box_data = self.state["boxes"][box]
        if not box_data["stack"]:
            return {"ok": False, "error": f"Box '{box}' empty. Switch box or start new cycle."}

        ball_id = box_data["stack"].pop()
        box_data["used"].append(ball_id)

        day = self._day()
        if session in day:
            return {"ok": False, "error": f"{session} already has a task. Use redraw or fill first."}
        day[session] = {
            "box": box,
            "content": content,
            "status": "completed",
            "ball_id": ball_id,
        }
        self._save()
        return {
            "ok": True,
            "message": f"✅ {self.DISPLAY.get(session, session)} logged (custom fill)",
            "block": day[session],
        }

    def log(self, session: str, content: str) -> dict:
        """Log something without consuming a ball."""
        day = self._day()
        if session in day:
            return {"ok": False, "error": f"{session} already has a task. Use redraw or fill first."}
        day[session] = {
            "box": "Free",
            "content": content,
            "status": "completed",
            "ball_id": "",
        }
        self._save()
        return {
            "ok": True,
            "message": f"✅ {self.DISPLAY.get(session, session)} logged (no ball consumed)",
            "block": day[session],
        }

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def status(self) -> dict:
        boxes = {}
        total_used = total_quota = 0
        for name, box in self.state["boxes"].items():
            used = len(box["used"])
            quota = used + len(box["stack"])
            total_used += used
            total_quota += quota
            boxes[name] = {
                "emoji": box["emoji"],
                "used": used,
                "total": quota,
                "remaining": len(box["stack"]),
            }

        today = self._today()
        day = self.state["days"].get(today, {})

        today_blocks = []
        for sess in self.SESSIONS:
            if sess in day:
                b = day[sess]
                today_blocks.append({
                    "session": sess,
                    "display": self.DISPLAY.get(sess, sess),
                    "box": b["box"],
                    "content": b["content"],
                    "status": b["status"],
                    "ball_id": b["ball_id"],
                })

        return {
            "today": today_blocks,
            "boxes": boxes,
            "cycle": self.state["cycle"],
            "cycle_progress": int(total_used / total_quota * 100) if total_quota else 0,
            "total_used": total_used,
            "total_quota": total_quota,
        }

    def today_summary(self) -> dict:
        today = self._today()
        day = self.state["days"].get(today, {})
        result = {}
        for sess in self.SESSIONS:
            if sess in day:
                result[sess] = day[sess]
            else:
                result[sess] = None
        return {"date": today, "sessions": result}

    def history(self, n_days: int = 7) -> list:
        result = []
        today = date.today()
        for i in range(n_days):
            d = str(today - timedelta(days=i))
            if d in self.state["days"]:
                result.append({"date": d, "sessions": self.state["days"][d]})
        return result

    def stats(self, n_days: int = 7) -> dict:
        box_stats = {}
        for name, box in self.state["boxes"].items():
            completed = 0
            for day in self.state["days"].values():
                for sess in day.values():
                    if sess and sess.get("box") == name and sess.get("status") == "completed":
                        completed += 1
            used = len(box["used"])
            total = used + len(box["stack"])
            box_stats[name] = {
                "emoji": box["emoji"],
                "used": used,
                "total": total,
                "completed": completed,
                "completion_rate": int(completed / used * 100) if used else 0,
            }

        daily_stats = []
        today = date.today()
        for i in range(n_days):
            d = str(today - timedelta(days=i))
            day_data = self.state["days"].get(d, {})
            drawn = len([s for s in day_data.values() if s])
            completed = len([s for s in day_data.values() if s and s.get("status") == "completed"])
            daily_stats.append({
                "date": d,
                "drawn": drawn,
                "completed": completed,
                "rate": int(completed / drawn * 100) if drawn else 0,
            })

        streak = 0
        for i in range(365):
            d = str(today - timedelta(days=i))
            day_data = self.state["days"].get(d, {})
            drawn = len([s for s in day_data.values() if s])
            completed = len([s for s in day_data.values() if s and s.get("status") == "completed"])
            if drawn > 0 and completed == drawn:
                streak += 1
            else:
                break

        cycle_start = self.state["cycle"]["start"]
        total_drawn = 0
        total_completed = 0
        for d, day in self.state["days"].items():
            if d < cycle_start:
                continue
            for sess in day.values():
                if sess:
                    total_drawn += 1
                    if sess.get("status") == "completed":
                        total_completed += 1

        return {
            "box_stats": box_stats,
            "daily_stats": daily_stats,
            "streak": streak,
            "cycle": self.state["cycle"],
            "total_drawn": total_drawn,
            "total_completed": total_completed,
            "overall_rate": int(total_completed / total_drawn * 100) if total_drawn else 0,
        }

    def new_cycle(self, name: str, start: str, end: str) -> dict:
        self.state["cycle"] = {"name": name, "start": start, "end": end}
        self.state["days"] = {}
        balls = json.loads(self.balls_path.read_text(encoding="utf-8"))
        for box_name, info in balls["boxes"].items():
            stack = [b["id"] for b in info["balls"]]
            random.shuffle(stack)
            self.state["boxes"][box_name] = {
                "emoji": info["emoji"],
                "stack": stack,
                "used": [],
            }
        self._save()
        return {"ok": True, "message": f"✅ New cycle '{name}' started"}

    def digest(self, weeks: int = 1, output_dir: str | None = None) -> dict:
        """Generate a Markdown weekly digest for LLM querying.

        The digest bridges structured JSON (machine state) and natural-language
        querying (agent reads markdown). It's read-only — no state changes.
        """
        from datetime import date as dt_date

        today = dt_date.today()
        iso = today.isocalendar()
        # target week: current week - weeks offset (weeks=1 means last week)
        target_year, target_week = iso.year, iso.week - (weeks - 1)
        while target_week < 1:
            target_year -= 1
            target_week += dt_date(target_year, 12, 28).isocalendar()[1]

        # Find date range for target week
        # ISO week: Monday=1, Sunday=7
        monday = dt_date.fromisocalendar(target_year, target_week, 1)
        days_in_week = []
        for i in range(7):
            d = monday + timedelta(days=i)
            if d > today:
                break
            days_in_week.append(str(d))

        if not days_in_week:
            return {"ok": False, "error": f"Week {target_year}-W{target_week:02d} has no past days"}

        # Load ball library for content/difficulty lookup
        try:
            balls_data = json.loads(self.balls_path.read_text(encoding="utf-8"))
        except Exception:
            balls_data = {"boxes": {}}

        ball_lib = {}
        for box_name, box_info in balls_data.get("boxes", {}).items():
            for b in box_info.get("balls", []):
                ball_lib[b["id"]] = {
                    "box": box_name,
                    "content": b["content"],
                    "difficulty": b.get("difficulty", "medium"),
                }

        # Collect week data
        daily = []
        week_completed = 0
        week_drawn = 0
        per_box = {}  # box -> {drawn, completed, hard/medium/easy}
        per_difficulty = {"hard": 0, "medium": 0, "easy": 0}

        for d in days_in_week:
            day_data = self.state["days"].get(d, {})
            sessions = []
            day_done = 0
            day_total = 0
            for sess in self.SESSIONS:
                s = day_data.get(sess)
                if s:
                    day_total += 1
                    info = ball_lib.get(s.get("ball_id", ""), {})
                    diff = info.get("difficulty", "medium")
                    status = s.get("status", "planned")
                    if status == "completed":
                        day_done += 1
                    sessions.append({
                        "session": sess,
                        "display": self.DISPLAY.get(sess, sess),
                        "box": s.get("box", "?"),
                        "content": s.get("content", "?"),
                        "status": status,
                        "difficulty": diff,
                        "ball_id": s.get("ball_id", ""),
                    })
                    # Per-box stats
                    box = s.get("box", "?")
                    if box not in per_box:
                        per_box[box] = {"drawn": 0, "completed": 0, "hard": 0, "medium": 0, "easy": 0}
                    per_box[box]["drawn"] += 1
                    per_box[box][diff] += 1
                    if status == "completed":
                        per_box[box]["completed"] += 1
                    per_difficulty[diff] += 1
                else:
                    sessions.append({
                        "session": sess,
                        "display": self.DISPLAY.get(sess, sess),
                        "box": None,
                        "content": None,
                        "status": "empty",
                    })
            daily.append({
                "date": d,
                "day_name": dt_date.fromisoformat(d).strftime("%A"),
                "sessions": sessions,
                "done": day_done,
                "total": day_total,
                "rate": int(day_done / day_total * 100) if day_total else 0,
            })
            week_completed += day_done
            week_drawn += day_total

        # Box inventory (current state, not just this week)
        box_inventory = {}
        for name, box in self.state["boxes"].items():
            used = len(box["used"])
            remaining = len(box["stack"])
            box_inventory[name] = {
                "emoji": box.get("emoji", ""),
                "used": used,
                "remaining": remaining,
                "total": used + remaining,
            }

        # Cycle info
        cycle = self.state["cycle"]

        # Build markdown
        lines = []
        lines.append(f"# 🎱 Ball Machine Digest — Week {target_year}-W{target_week:02d}")
        lines.append(f"")
        lines.append(f"**Cycle**: {cycle['name']} ({cycle['start']} → {cycle['end']})")
        lines.append(f"**Generated**: {today.isoformat()}")
        lines.append(f"**Week range**: {days_in_week[0]} → {days_in_week[-1]}")
        lines.append(f"**Week score**: {week_completed}/{week_drawn} ({int(week_completed/week_drawn*100) if week_drawn else 0}%)")
        lines.append(f"")

        # Daily log
        lines.append("## 📅 Daily Log")
        lines.append("")
        for day in daily:
            status_bar = f" {_bar(day['done'], day['total'], 14)}" if day["total"] else " — (no draws)"
            lines.append(f"### {day['date']} ({day['day_name']}){status_bar} {day['done']}/{day['total']}")
            lines.append("")
            for s in day["sessions"]:
                if s["status"] == "empty":
                    lines.append(f"| {s['display']} | — | — |")
                else:
                    status_icon = "✅" if s["status"] == "completed" else "📝"
                    diff_icon = self.DIFFICULTY_EMOJI.get(s["difficulty"], "")
                    lines.append(f"| {s['display']} | {s['box']} {diff_icon} | {status_icon} {s['content']} |")
            lines.append("")

        # Per-box breakdown
        lines.append("## 📦 Box Breakdown (This Week)")
        lines.append("")
        lines.append("| Box | Drawn | Completed | Rate | 🔴 Hard | 🟡 Medium | 🟢 Easy |")
        lines.append("|-----|-------|-----------|------|---------|-----------|---------|")
        for name in sorted(per_box.keys()):
            b = per_box[name]
            rate = int(b["completed"] / b["drawn"] * 100) if b["drawn"] else 0
            lines.append(f"| {name} | {b['drawn']} | {b['completed']} | {rate}% | {b['hard']} | {b['medium']} | {b['easy']} |")
        lines.append("")

        # Difficulty distribution
        total_diff = sum(per_difficulty.values())
        if total_diff:
            lines.append("## 🎯 Difficulty Mix")
            lines.append("")
            lines.append(f"- 🔴 Hard: {per_difficulty['hard']} ({int(per_difficulty['hard']/total_diff*100)}%)")
            lines.append(f"- 🟡 Medium: {per_difficulty['medium']} ({int(per_difficulty['medium']/total_diff*100)}%)")
            lines.append(f"- 🟢 Easy: {per_difficulty['easy']} ({int(per_difficulty['easy']/total_diff*100)}%)")
            lines.append("")

        # Box inventory (cycle-level)
        lines.append("## 📊 Cycle Inventory")
        lines.append("")
        for name, box in box_inventory.items():
            bar = _bar(box["used"], box["total"])
            pct = int(box["used"] / box["total"] * 100) if box["total"] else 0
            lines.append(f"- {box['emoji']} **{name}**: {bar} {box['used']}/{box['total']} ({pct}%) — {box['remaining']} remaining")
        lines.append("")

        # Ball library snapshot (for LLM cross-reference)
        lines.append("## 🎰 Ball Library (All Boxes)")
        lines.append("")
        for box_name in box_inventory:
            box_info = balls_data.get("boxes", {}).get(box_name, {})
            lines.append(f"### {box_info.get('emoji', '')} {box_name}")
            lines.append("")
            for b in box_info.get("balls", []):
                diff_icon = self.DIFFICULTY_EMOJI.get(b.get("difficulty", "medium"), "")
                lines.append(f"- {diff_icon} `{b['id']}` — {b['content']}")
            lines.append("")

        md_content = "\n".join(lines)

        # Write to file
        if output_dir:
            out_path = Path(output_dir)
        else:
            out_path = self.data_dir / "digests"
        out_path.mkdir(parents=True, exist_ok=True)
        filename = f"{target_year}-W{target_week:02d}.md"
        filepath = out_path / filename
        filepath.write_text(md_content, encoding="utf-8")

        return {
            "ok": True,
            "message": f"✅ Digest saved to {filepath}",
            "path": str(filepath),
            "week": f"{target_year}-W{target_week:02d}",
            "week_score": f"{week_completed}/{week_drawn} ({int(week_completed/week_drawn*100) if week_drawn else 0}%)",
            "days_covered": len(days_in_week),
        }

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate(self) -> dict:
        errors = []
        try:
            cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
        except Exception as e:
            return {"ok": False, "errors": [f"config.json unreadable: {e}"]}
        try:
            balls = json.loads(self.balls_path.read_text(encoding="utf-8"))
        except Exception as e:
            return {"ok": False, "errors": [f"balls.json unreadable: {e}"]}

        cfg_boxes = set(cfg.get("boxes", {}).keys())
        ball_boxes = set(balls.get("boxes", {}).keys())

        missing_in_balls = cfg_boxes - ball_boxes
        missing_in_cfg = ball_boxes - cfg_boxes
        if missing_in_balls:
            errors.append(f"Boxes in config but missing in balls: {missing_in_balls}")
        if missing_in_cfg:
            errors.append(f"Boxes in balls but missing in config: {missing_in_cfg}")

        for name in cfg_boxes & ball_boxes:
            quota = cfg["boxes"][name]["quota"]
            count = len(balls["boxes"][name]["balls"])
            if count != quota:
                errors.append(f"Box '{name}': quota={quota}, actual balls={count}")

        if errors:
            return {"ok": False, "errors": errors}
        return {"ok": True, "message": "✅ config.json and balls.json are consistent"}


# ------------------------------------------------------------------
# Admin Commands — operate on config.json / balls.json directly
# These do NOT require state.json. They are the ONLY write paths for
# box and ball definitions — humans never edit JSON by hand.
# ------------------------------------------------------------------

def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, data: dict):
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.rename(path)


def admin_list_boxes(data_dir: Path) -> dict:
    """List all boxes with their quota and ball count."""
    cfg = _load_json(data_dir / "config.json")
    balls = _load_json(data_dir / "balls.json")
    if not cfg:
        return {"ok": False, "error": "config.json not found or empty"}
    boxes = []
    for name, info in cfg.get("boxes", {}).items():
        quota = info.get("quota", 0)
        box_balls = balls.get("boxes", {}).get(name, {}).get("balls", [])
        boxes.append({
            "name": name,
            "emoji": info.get("emoji", ""),
            "quota": quota,
            "actual": len(box_balls),
        })
    has_state = (data_dir / "state.json").exists()
    return {"ok": True, "boxes": boxes, "state_exists": has_state}


def admin_list_balls(data_dir: Path, box: str) -> dict:
    """List all balls in a box."""
    balls = _load_json(data_dir / "balls.json")
    box_info = balls.get("boxes", {}).get(box)
    if not box_info:
        return {"ok": False, "error": f"Box '{box}' not found in balls.json"}
    return {"ok": True, "box": box, "emoji": box_info.get("emoji", ""), "balls": box_info.get("balls", [])}


def admin_add_box(data_dir: Path, name: str, emoji: str, quota: int) -> dict:
    """Add a new box to config.json and balls.json."""
    if quota < 1:
        return {"ok": False, "error": "Quota must be >= 1"}

    cfg = _load_json(data_dir / "config.json")
    if not cfg:
        # Bootstrap config.json
        cfg = {"cycle_name": "New Cycle", "cycle_start": str(date.today()),
               "cycle_end": str(date.today() + timedelta(days=30)),
               "duration_map": {"hard": 3.0, "medium": 2.5, "easy": 2.0}, "boxes": {}}
    cfg.setdefault("boxes", {})
    if name in cfg["boxes"]:
        return {"ok": False, "error": f"Box '{name}' already exists in config.json"}
    cfg["boxes"][name] = {"emoji": emoji, "quota": quota}
    _save_json(data_dir / "config.json", cfg)

    balls = _load_json(data_dir / "balls.json")
    balls.setdefault("boxes", {})
    if name not in balls["boxes"]:
        balls["boxes"][name] = {"emoji": emoji, "balls": []}
    _save_json(data_dir / "balls.json", balls)

    warn = ""
    if (data_dir / "state.json").exists():
        warn = " ⚠️ state.json exists — box won't appear until next new-cycle"
    return {"ok": True, "message": f"✅ Box '{name}' added ({emoji}, quota={quota}){warn}"}


def admin_add_ball(data_dir: Path, box: str, content: str, difficulty: str = "medium") -> dict:
    """Add a ball to a box in balls.json."""
    if difficulty not in ("hard", "medium", "easy"):
        return {"ok": False, "error": "Difficulty must be hard, medium, or easy"}

    balls = _load_json(data_dir / "balls.json")
    box_info = balls.get("boxes", {}).get(box)
    if not box_info:
        return {"ok": False, "error": f"Box '{box}' not found in balls.json"}

    cfg = _load_json(data_dir / "config.json")
    quota = cfg.get("boxes", {}).get(box, {}).get("quota", 0)
    current = len(box_info.get("balls", []))
    if quota and current >= quota:
        return {"ok": False, "error": f"Box '{box}' already has {current}/{quota} balls. Increase quota first (set-quota)."}

    existing_ids = [b["id"] for b in box_info.get("balls", [])]
    seq = 1
    while f"BALL-{box.upper()}-{seq:03d}" in existing_ids:
        seq += 1
    ball_id = f"BALL-{box.upper()}-{seq:03d}"

    new_ball = {"id": ball_id, "content": content, "difficulty": difficulty}
    box_info.setdefault("balls", []).append(new_ball)
    _save_json(data_dir / "balls.json", balls)

    warn = ""
    if (data_dir / "state.json").exists():
        warn = " ⚠️ state.json exists — new balls available after next new-cycle"
    return {"ok": True, "message": f"✅ Added {ball_id} to '{box}'{warn}", "ball": new_ball}


def admin_remove_ball(data_dir: Path, ball_id: str) -> dict:
    """Remove a ball from balls.json by ID."""
    balls = _load_json(data_dir / "balls.json")
    for box_name, box_info in balls.get("boxes", {}).items():
        for i, b in enumerate(box_info.get("balls", [])):
            if b["id"] == ball_id:
                removed = box_info["balls"].pop(i)
                _save_json(data_dir / "balls.json", balls)
                warn = ""
                if (data_dir / "state.json").exists():
                    warn = f" ⚠️ ball may already be used in current cycle — run validate and consider new-cycle"
                return {"ok": True, "message": f"✅ Removed {ball_id} from '{box_name}'{warn}", "ball": removed}
    return {"ok": False, "error": f"Ball '{ball_id}' not found in any box"}


def admin_edit_ball(data_dir: Path, ball_id: str, content: str) -> dict:
    """Edit a ball's content in balls.json."""
    balls = _load_json(data_dir / "balls.json")
    for box_name, box_info in balls.get("boxes", {}).items():
        for b in box_info.get("balls", []):
            if b["id"] == ball_id:
                old = b["content"]
                b["content"] = content
                _save_json(data_dir / "balls.json", balls)
                return {"ok": True, "message": f"✅ Edited {ball_id}", "old": old, "new": content}
    return {"ok": False, "error": f"Ball '{ball_id}' not found in any box"}


def admin_set_quota(data_dir: Path, box: str, quota: int) -> dict:
    """Change a box's quota in config.json."""
    if quota < 1:
        return {"ok": False, "error": "Quota must be >= 1"}

    cfg = _load_json(data_dir / "config.json")
    if box not in cfg.get("boxes", {}):
        return {"ok": False, "error": f"Box '{box}' not found in config.json"}

    old = cfg["boxes"][box]["quota"]
    cfg["boxes"][box]["quota"] = quota
    _save_json(data_dir / "config.json", cfg)

    balls = _load_json(data_dir / "balls.json")
    current = len(balls.get("boxes", {}).get(box, {}).get("balls", []))

    msgs = [f"✅ Quota for '{box}': {old} → {quota}"]
    if current > quota:
        msgs.append(f"⚠️ Box has {current} balls but quota is now {quota} — remove {current - quota} ball(s)")
    elif current < quota:
        msgs.append(f"📝 Box has {current}/{quota} balls — add {quota - current} more")
    else:
        msgs.append(f"✅ Box has exactly {quota} balls — quota matched")

    return {"ok": True, "message": "\n".join(msgs), "old": old, "new": quota, "current_balls": current}


# ------------------------------------------------------------------
# Pretty Printing
# ------------------------------------------------------------------
def _bar(used: int, total: int, width: int = 20) -> str:
    filled = int(used / total * width) if total else 0
    return "█" * filled + "░" * (width - filled)


def print_status(data: dict):
    today_str = date.today().strftime("%Y-%m-%d (%A)")
    print(f"📅 {today_str}")
    print("━" * 50)
    for sess in Engine.SESSIONS:
        found = [b for b in data["today"] if b["session"] == sess]
        if found:
            b = found[0]
            box_info = data["boxes"].get(b["box"], {})
            box_emoji = box_info.get("emoji", "")
            status_icon = "✅" if b["status"] == "completed" else "📝"
            print(f"{Engine.DISPLAY.get(sess, sess):<12} {box_emoji}  {b['content']:<30} {status_icon}")
        else:
            print(f"{Engine.DISPLAY.get(sess, sess):<12} (empty) {' ' * 31} —")
    print("━" * 50)
    print("📦 Box Inventory")
    for name, box in data["boxes"].items():
        bar = _bar(box["used"], box["total"])
        print(f"  {box['emoji']} {name:<10} {bar}  {box['used']}/{box['total']} used")
    print("━" * 50)
    prog = data["cycle_progress"]
    print(f"🎯 Cycle: {data['cycle']['name']} | {data['total_used']}/{data['total_quota']} balls used ({prog}%)")


def print_draw(result: dict):
    if not result["ok"]:
        print(f"❌ {result['error']}")
        return
    b = result["block"]
    diff_emoji = Engine.DIFFICULTY_EMOJI.get(b["difficulty"], "")
    print(f"\n{result['message']}")
    print(f"  📦 Box:  {b['box']}")
    print(f"  🎰 Ball: {b['ball_id']}")
    print(f"  📝 Task: {b['content']}")
    print(f"  {diff_emoji} Difficulty: {b['difficulty']} (~{b['duration']}h)")


def print_quick_draw(result: dict):
    if not result["ok"]:
        print(f"❌ {result['error']}")
        return
    print(f"\n{result['message']}")
    for b in result["blocks"]:
        diff_emoji = Engine.DIFFICULTY_EMOJI.get(b["difficulty"], "")
        print(f"  {b.get('session', 'unknown'):<12} {b['box']:<10} {diff_emoji} {b['content']}")


def print_stats(data: dict):
    print("\n📊 Stats Report")
    print("━" * 50)
    print("\nBox Completion Rates:")
    for name, box in data["box_stats"].items():
        print(f"  {box['emoji']} {name:<10} {box['completed']}/{box['used']} done  ({box['completion_rate']}%)")

    print("\nDaily Trend (last 7 days):")
    for day in reversed(data["daily_stats"]):
        bar = _bar(day["completed"], day["drawn"], width=10) if day["drawn"] else "░" * 10
        print(f"  {day['date']}  {bar}  {day['completed']}/{day['drawn']} ({day['rate']}%)")

    print(f"\n🔥 Current streak: {data['streak']} day(s)")
    print(f"🎯 Overall cycle rate: {data['total_completed']}/{data['total_drawn']} ({data['overall_rate']}%)")
    print(f"   Cycle: {data['cycle']['name']} ({data['cycle']['start']} → {data['cycle']['end']})")


def print_history(data: list):
    if not data:
        print("No history yet.")
        return
    for entry in data:
        print(f"\n📅 {entry['date']}")
        for sess in Engine.SESSIONS:
            s = entry["sessions"].get(sess)
            if s:
                status = "✅" if s["status"] == "completed" else "📝"
                print(f"  {Engine.DISPLAY.get(sess, sess):<12} {s['box']:<10} {status} {s['content']}")
            else:
                print(f"  {Engine.DISPLAY.get(sess, sess):<12} (empty)")


def print_validate(result: dict):
    if result["ok"]:
        print(result["message"])
    else:
        print("❌ Validation failed:")
        for err in result["errors"]:
            print(f"  • {err}")


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Task Ball Machine — Daily task lottery CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --data-dir ~/my-machine init
  %(prog)s --data-dir ~/my-machine draw morning
  %(prog)s --data-dir ~/my-machine quick-draw
  %(prog)s --data-dir ~/my-machine complete afternoon
  %(prog)s --data-dir ~/my-machine status
  %(prog)s --data-dir ~/my-machine stats
  %(prog)s --data-dir ~/my-machine new-cycle "July 2026" 2026-07-01 2026-07-31
        """.strip(),
    )
    parser.add_argument("--data-dir", default=".", help="Directory containing config.json, balls.json, state.json (default: .)")
    parser.add_argument("--force", action="store_true", help="Force overwrite state.json on init")

    sub = parser.add_subparsers(dest="command", help="Command")

    sub.add_parser("init", help="Create state.json from config.json + balls.json")
    sub.add_parser("validate", help="Check config/balls consistency")

    p_draw = sub.add_parser("draw", help="Draw a ball for a session")
    p_draw.add_argument("session", choices=["morning", "afternoon", "evening", "overtime"])
    p_draw.add_argument("--box", default=None, help="Force draw from a specific box")

    sub.add_parser("quick-draw", help="Draw for all empty morning/afternoon/evening slots")

    p_done = sub.add_parser("complete", help="Mark a session completed")
    p_done.add_argument("session", choices=["morning", "afternoon", "evening", "overtime"])

    p_redraw = sub.add_parser("redraw", help="Return ball and redraw a session")
    p_redraw.add_argument("session", choices=["morning", "afternoon", "evening", "overtime"])

    p_fill = sub.add_parser("fill", help="Custom content, consumes one ball from a box")
    p_fill.add_argument("session", choices=["morning", "afternoon", "evening", "overtime"])
    p_fill.add_argument("box", help="Box to consume ball from")
    p_fill.add_argument("content", nargs="+", help="Task description")

    p_log = sub.add_parser("log", help="Log something without consuming a ball")
    p_log.add_argument("session", choices=["morning", "afternoon", "evening", "overtime"])
    p_log.add_argument("content", nargs="+", help="Task description")

    sub.add_parser("status", help="Show today's board and box inventory")
    sub.add_parser("today", help="Show just today's sessions")

    p_hist = sub.add_parser("history", help="Show recent daily history")
    p_hist.add_argument("--days", type=int, default=7, help="Number of days (default: 7)")

    p_stats = sub.add_parser("stats", help="Show cycle stats and streak")
    p_stats.add_argument("--days", type=int, default=7, help="Daily trend window (default: 7)")

    p_digest = sub.add_parser("digest", help="Generate weekly Markdown digest for LLM querying")
    p_digest.add_argument("--weeks", type=int, default=1, help="Weeks ago (1=last week, default: 1)")
    p_digest.add_argument("--output", default=None, help="Output directory (default: data_dir/digests/)")

    # --- Admin commands (no state.json required) ---
    sub.add_parser("list-boxes", help="List all boxes with quota and ball count")

    p_list_balls = sub.add_parser("list-balls", help="List all balls in a box")
    p_list_balls.add_argument("box", help="Box name")

    p_add_box = sub.add_parser("add-box", help="Add a new box to config.json + balls.json")
    p_add_box.add_argument("name", help="Box name")
    p_add_box.add_argument("emoji", help="Box emoji (e.g. 💼 📚 🏃)")
    p_add_box.add_argument("quota", type=int, help="Number of balls for this box")

    p_add_ball = sub.add_parser("add-ball", help="Add a ball to a box")
    p_add_ball.add_argument("box", help="Target box name")
    p_add_ball.add_argument("content", nargs="+", help="Task description")
    p_add_ball.add_argument("--difficulty", default="medium", choices=["hard", "medium", "easy"])

    p_rm_ball = sub.add_parser("remove-ball", help="Remove a ball by ID")
    p_rm_ball.add_argument("ball_id", help="Ball ID (e.g. BALL-WORK-001)")

    p_edit_ball = sub.add_parser("edit-ball", help="Edit a ball's content")
    p_edit_ball.add_argument("ball_id", help="Ball ID to edit")
    p_edit_ball.add_argument("content", nargs="+", help="New task description")

    p_set_quota = sub.add_parser("set-quota", help="Change a box's quota")
    p_set_quota.add_argument("box", help="Box name")
    p_set_quota.add_argument("quota", type=int, help="New quota value")

    p_new = sub.add_parser("new-cycle", help="Start a new cycle (resets and reshuffles)")
    p_new.add_argument("name", help="Cycle name")
    p_new.add_argument("start", help="Start date (YYYY-MM-DD)")
    p_new.add_argument("end", help="End date (YYYY-MM-DD)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    data_dir = Path(args.data_dir)

    if args.command == "init":
        state_path = data_dir / "state.json"
        if state_path.exists() and not args.force:
            print("state.json already exists. Use --force to overwrite.")
            sys.exit(1)
        if state_path.exists():
            state_path.unlink()
        engine = Engine(data_dir)
        engine._save()
        print(f"✅ Initialized state.json in {data_dir}")
        sys.exit(0)

    # --- Admin commands (operate on config/balls, no state.json needed) ---
    if args.command == "list-boxes":
        r = admin_list_boxes(data_dir)
        if r["ok"]:
            print("\n📦 Boxes:")
            for b in r["boxes"]:
                match = "✅" if b["actual"] == b["quota"] else f"⚠️ {b['actual']}/{b['quota']}"
                print(f"  {b['emoji']} {b['name']:<12} quota={b['quota']}  balls={b['actual']}  {match}")
            if r.get("state_exists"):
                print("\n⚠️ state.json exists — changes won't affect current cycle")
        else:
            print(f"❌ {r['error']}")
        sys.exit(0)

    if args.command == "list-balls":
        r = admin_list_balls(data_dir, args.box)
        if r["ok"]:
            print(f"\n{r['emoji']} {r['box']} ({len(r['balls'])} balls):")
            for b in r["balls"]:
                diff_icon = Engine.DIFFICULTY_EMOJI.get(b.get("difficulty", "medium"), "")
                print(f"  {diff_icon} {b['id']} — {b['content']}")
        else:
            print(f"❌ {r['error']}")
        sys.exit(0)

    if args.command == "add-box":
        r = admin_add_box(data_dir, args.name, args.emoji, args.quota)
        print(r["message"] if r["ok"] else f"❌ {r['error']}")
        sys.exit(0)

    if args.command == "add-ball":
        r = admin_add_ball(data_dir, args.box, " ".join(args.content), args.difficulty)
        if r["ok"]:
            print(r["message"])
            print(f"   ID: {r['ball']['id']} | Difficulty: {r['ball']['difficulty']}")
        else:
            print(f"❌ {r['error']}")
        sys.exit(0)

    if args.command == "remove-ball":
        r = admin_remove_ball(data_dir, args.ball_id)
        print(r["message"] if r["ok"] else f"❌ {r['error']}")
        sys.exit(0)

    if args.command == "edit-ball":
        r = admin_edit_ball(data_dir, args.ball_id, " ".join(args.content))
        if r["ok"]:
            print(r["message"])
            print(f"   Old: {r['old']}")
            print(f"   New: {r['new']}")
        else:
            print(f"❌ {r['error']}")
        sys.exit(0)

    if args.command == "set-quota":
        r = admin_set_quota(data_dir, args.box, args.quota)
        print(r["message"] if r["ok"] else f"❌ {r['error']}")
        sys.exit(0)

    # For all other commands, require existing state
    engine = Engine(data_dir)

    if args.command == "validate":
        print_validate(engine.validate())

    elif args.command == "draw":
        print_draw(engine.draw(args.session, box=args.box))

    elif args.command == "quick-draw":
        print_quick_draw(engine.quick_draw())

    elif args.command == "complete":
        r = engine.complete(args.session)
        print(r["message"] if r["ok"] else f"❌ {r['error']}")

    elif args.command == "redraw":
        print_draw(engine.redraw(args.session))

    elif args.command == "fill":
        r = engine.fill(args.session, args.box, " ".join(args.content))
        print(r["message"] if r["ok"] else f"❌ {r['error']}")

    elif args.command == "log":
        r = engine.log(args.session, " ".join(args.content))
        print(r["message"] if r["ok"] else f"❌ {r['error']}")

    elif args.command == "status":
        print_status(engine.status())

    elif args.command == "today":
        data = engine.today_summary()
        print(f"📅 {data['date']}")
        for sess in Engine.SESSIONS:
            s = data["sessions"][sess]
            if s:
                status = "✅" if s["status"] == "completed" else "📝"
                print(f"  {Engine.DISPLAY.get(sess, sess):<12} {s['box']:<10} {status} {s['content']}")
            else:
                print(f"  {Engine.DISPLAY.get(sess, sess):<12} (empty)")

    elif args.command == "history":
        print_history(engine.history(args.days))

    elif args.command == "stats":
        print_stats(engine.stats(args.days))

    elif args.command == "digest":
        r = engine.digest(weeks=args.weeks, output_dir=args.output)
        if r["ok"]:
            print(r["message"])
            print(f"   Week: {r['week']} | Score: {r['week_score']} | Days: {r['days_covered']}")
        else:
            print(f"❌ {r['error']}")

    elif args.command == "new-cycle":
        r = engine.new_cycle(args.name, args.start, args.end)
        print(r["message"] if r["ok"] else f"❌ {r['error']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
