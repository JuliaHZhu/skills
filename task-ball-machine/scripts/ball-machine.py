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
            return {"ok": False, "error": f"{session} already has a task. Use edit or redraw first."}
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
            return {"ok": False, "error": f"{session} already has a task. Use edit or redraw first."}
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

    elif args.command == "new-cycle":
        r = engine.new_cycle(args.name, args.start, args.end)
        print(r["message"] if r["ok"] else f"❌ {r['error']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
