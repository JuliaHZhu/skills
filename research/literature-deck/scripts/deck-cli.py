#!/usr/bin/env python3
"""
deck-cli.py — Literature Deck Engine
Atomic notes → paragraph drafts. Human-driven, AI-assisted.

Usage:
    python deck-cli.py init <project_name>
    python deck-cli.py extract <paper_path>
    python deck-cli.py outline parse <outline.md>
    python deck-cli.py assemble --section <name>
    python deck-cli.py assemble --all
    python deck-cli.py status
    python deck-cli.py coverage
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

DEFAULT_ATOM_TYPES = ["def", "theo", "arg", "bridge", "gap", "scale"]

# ---------------------------------------------------------------------------
# Progress (state) management
# ---------------------------------------------------------------------------

PROGRESS_FILE = "deck-progress.json"


def load_progress(project_dir: Path) -> dict:
    path = project_dir / PROGRESS_FILE
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_progress()


def save_progress(project_dir: Path, data: dict):
    path = project_dir / PROGRESS_FILE
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def default_progress() -> dict:
    return {
        "project": "",
        "current_phase": 1,
        "phases": {
            "1": {"status": "in_progress"},
            "2": {"status": "pending"},
            "3": {"status": "pending"},
            "4": {"status": "pending"},
        },
        "atoms_count": 0,
        "sections_parsed": [],
        "sections_assembled": [],
    }


def advance_phase(project_dir: Path, to_phase: int):
    prog = load_progress(project_dir)
    current = prog["current_phase"]
    if to_phase <= current:
        return
    for p in range(current + 1, to_phase + 1):
        prog["phases"][str(p)] = {"status": "in_progress"}
    for p in range(1, to_phase):
        prog["phases"][str(p)]["status"] = "completed"
    prog["current_phase"] = to_phase
    save_progress(project_dir, prog)


def require_phase(project_dir: Path, min_phase: int, action: str) -> bool:
    prog = load_progress(project_dir)
    current = prog["current_phase"]
    if current < min_phase:
        print(f"❌ Blocked: '{action}' requires phase {min_phase}, but current phase is {current}.")
        print(f"   Run the pipeline steps in order. See SKILL.md for details.")
        return False
    return True


# ---------------------------------------------------------------------------
# Init
# ---------------------------------------------------------------------------

def cmd_init(args):
    name = args.project_name
    root = Path(name)
    if root.exists() and not args.force:
        print(f"❌ Directory '{name}' already exists. Use --force to overwrite.")
        sys.exit(1)

    root.mkdir(parents=True, exist_ok=True)
    (root / "atoms").mkdir(exist_ok=True)
    (root / "papers").mkdir(exist_ok=True)
    (root / "drafts").mkdir(exist_ok=True)
    (root / "drafts" / ".tmp").mkdir(exist_ok=True)

    # project.yaml template
    project_yaml = root / "project.yaml"
    project_yaml.write_text(
        f"""project_id: {name}
version: '1.0'
phases:
  current: 1
  completed: []
variables:
  example_var:
    name: Example Variable
    definition: "..."
    scale_source: ""
hypotheses:
  - id: H1
    path: "example_var → outcome"
    variables: [example_var, outcome]
    atoms_needed: 3
theories:
  - id: THEORY_A
    name: "Theory A"
stats:
  total_atoms: 0
  coverage_complete: false
""",
        encoding="utf-8",
    )

    # tag-registry.md template
    tag_registry = root / "tag-registry.md"
    tag_registry.write_text(
        f"""# Tag Registry: {name}

| Tag | Description | Needed |
|-----|-------------|--------|
| H1 | Hypothesis 1 | 3 |
| define_example_var | Variable definition | 2 |
| theory_THEORY_A | Theory grounding | 2 |

## Coverage Summary

| Category | Total Tags | Total Needed |
|----------|-----------|--------------|
| Hypothesis | 1 | 3 |
| Variable Definition | 1 | 2 |
| Theory | 1 | 2 |
| **Total** | **3** | **7** |
""",
        encoding="utf-8",
    )

    # outline.md template
    outline_md = root / "outline.md"
    outline_md.write_text(
        f"""# Introduction
## Background
Set up the research context.

## Gap
Identify what is missing in the literature.

# Theory
## Theoretical Foundation
Ground the study in relevant theory.

# Hypotheses
## H1 Argument
Present evidence for H1.
""",
        encoding="utf-8",
    )

    # deck-progress.json
    prog = default_progress()
    prog["project"] = name
    save_progress(root, prog)

    print(f"✅ Initialized project '{name}' at ./{name}/")
    print(f"   Next: Edit project.yaml, then place papers in papers/")


# ---------------------------------------------------------------------------
# Extract atoms
# ---------------------------------------------------------------------------

def cmd_extract(args):
    project_dir = Path(args.project_dir or ".")
    paper_path = Path(args.paper)

    if not paper_path.exists():
        print(f"❌ Paper not found: {paper_path}")
        sys.exit(1)

    # For now, this is a scaffolding command.
    # Full AI-assisted extraction happens via Hermes skill interaction.
    print(f"📖 Paper loaded: {paper_path.name}")
    print(f"   To extract atoms, create files in {project_dir / 'atoms'}/")
    print(f"   Template:")
    print(f"""
---
source: {paper_path.stem.replace('-full','')}
type: arg
tags: [H1]
---
# Claim summary
> "Direct quote" (p.12)
""")

    # Update atom count from existing atoms
    atoms_dir = project_dir / "atoms"
    count = len(list(atoms_dir.glob("*.md"))) if atoms_dir.exists() else 0
    prog = load_progress(project_dir)
    prog["atoms_count"] = count
    save_progress(project_dir, prog)
    print(f"   Current atom count: {count}")


# ---------------------------------------------------------------------------
# Outline parse
# ---------------------------------------------------------------------------

def parse_outline(outline_path: Path) -> dict:
    """Parse a Markdown outline into a structured section-to-tags map.

    Returns:
        {
          "sections": [
            {"title": "Background", "level": 2, "inferred_tags": [...]},
            ...
          ]
        }
    """
    content = outline_path.read_text(encoding="utf-8")
    sections = []
    for line in content.splitlines():
        m = re.match(r"^(#{2,4})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            inferred = infer_tags_for_section(title)
            sections.append({"title": title, "level": level, "inferred_tags": inferred})
    return {"sections": sections}


def infer_tags_for_section(title: str) -> List[str]:
    """Infer likely tags from a section title. Simple heuristic."""
    tags = []
    lower = title.lower()
    # Hypothesis tags
    for h in re.findall(r"\b(H\d+[a-z]?)\b", title):
        tags.append(h)
    # Definition tags
    if any(w in lower for w in ["definition", "concept", "construct", "measurement"]):
        tags.append("define_*")
    # Theory tags
    if "theory" in lower or "theoretical" in lower:
        tags.append("theory_*")
    # Gap tags
    if "gap" in lower or "missing" in lower or "limitation" in lower:
        tags.append("gap_*")
    return tags if tags else ["*"]


def cmd_outline_parse(args):
    project_dir = Path(args.project_dir or ".")
    outline_path = Path(args.outline)

    if not outline_path.exists():
        print(f"❌ Outline not found: {outline_path}")
        sys.exit(1)

    result = parse_outline(outline_path)
    map_path = project_dir / "outline-map.yaml"

    # Write as a simple YAML-like text
    lines = ["# Auto-generated from outline.md", "sections:"]
    for sec in result["sections"]:
        lines.append(f'  - title: "{sec["title"]}"')
        lines.append(f'    level: {sec["level"]}')
        tags = ", ".join(sec["inferred_tags"])
        lines.append(f'    inferred_tags: [{tags}]')
        lines.append(f'    confirmed_tags: []  # human fills this')

    map_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Advance phase
    advance_phase(project_dir, 3)
    prog = load_progress(project_dir)
    prog["sections_parsed"] = [s["title"] for s in result["sections"]]
    save_progress(project_dir, prog)

    print(f"✅ Parsed {len(result['sections'])} sections.")
    print(f"   Saved to: {map_path}")
    print(f"   Please review and edit 'confirmed_tags' before assembling.")


# ---------------------------------------------------------------------------
# Assemble
# ---------------------------------------------------------------------------

def find_atoms_by_tags(project_dir: Path, tags: List[str]) -> List[Path]:
    atoms_dir = project_dir / "atoms"
    if not atoms_dir.exists():
        return []

    matched = []
    for atom_path in sorted(atoms_dir.glob("*.md")):
        content = atom_path.read_text(encoding="utf-8")
        # Look for tags in YAML frontmatter
        if re.search(r"^tags:\s*\[([^\]]*)\]", content, re.MULTILINE):
            # Simple substring match for tags
            for tag in tags:
                pattern = tag.replace("*", r"\w+")
                if re.search(rf"\b{pattern}\b", content):
                    matched.append(atom_path)
                    break
    return matched


def read_atom_content(atom_path: Path) -> dict:
    content = atom_path.read_text(encoding="utf-8")
    # Extract source from frontmatter
    source_match = re.search(r"^source:\s*(.+)$", content, re.MULTILINE)
    source = source_match.group(1).strip() if source_match else atom_path.stem

    # Extract body (after first --- end)
    parts = content.split("---")
    body = parts[-1].strip() if len(parts) >= 3 else content.strip()

    return {"source": source, "body": body, "path": str(atom_path)}


def cmd_assemble(args):
    project_dir = Path(args.project_dir or ".")

    if not require_phase(project_dir, 3, "assemble"):
        sys.exit(1)

    map_path = project_dir / "outline-map.yaml"
    if not map_path.exists():
        print(f"❌ outline-map.yaml not found. Run 'deck outline parse' first.")
        sys.exit(1)

    # Parse outline-map.yaml (simple line-based parser)
    map_text = map_path.read_text(encoding="utf-8")
    sections: list[dict] = []
    current: dict = {}
    for line in map_text.splitlines():
        if line.startswith("  - title:"):
            current = {"title": line.split(":", 1)[1].strip().strip('"')}
        elif line.startswith("    level:"):
            current["level"] = int(line.split(":", 1)[1].strip())
        elif line.startswith("    inferred_tags:"):
            tags_str = line.split(":", 1)[1].split("#")[0].strip()
            current["inferred_tags"] = [t.strip().strip('"') for t in tags_str.strip("[]").split(",") if t.strip()]
        elif line.startswith("    confirmed_tags:"):
            tags_str = line.split(":", 1)[1].split("#")[0].strip()
            current["confirmed_tags"] = [t.strip().strip('"') for t in tags_str.strip("[]").split(",") if t.strip()]
            # Use confirmed_tags if non-empty, else fall back to inferred_tags
            tags = current.get("confirmed_tags", []) or current.get("inferred_tags", [])
            current["tags"] = tags
            sections.append(current)
            current = {}

    targets = []
    if args.section:
        targets = [s for s in sections if s.get("title") == args.section]
        if not targets:
            print(f"❌ Section '{args.section}' not found in outline-map.yaml.")
            print(f"   Available: {', '.join(s['title'] for s in sections)}")
            sys.exit(1)
    elif args.all:
        targets = sections
    else:
        print("❌ Use --section <name> or --all")
        sys.exit(1)

    drafts_dir = project_dir / "drafts"
    drafts_dir.mkdir(exist_ok=True)

    for sec in targets:
        title = sec["title"]
        tags = sec.get("tags", [])
        print(f"\n🔍 Assembling: {title} (tags: {tags})")

        atoms = find_atoms_by_tags(project_dir, tags)
        print(f"   Found {len(atoms)} matching atoms.")

        # Build draft
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        draft_path = drafts_dir / f"{ts}-section-{title.replace(' ', '_')}.md"

        lines = [f"# {title}", ""]

        needed = 3  # default; could read from project.yaml per-hypothesis
        weak = len(atoms) < needed

        if weak:
            lines.append(f"> [WEAK_EVIDENCE: needs ~{needed} atoms, found {len(atoms)}]\n")

        for atom_path in atoms:
            atom = read_atom_content(atom_path)
            lines.append(f"## Evidence from {atom['source']}")
            lines.append(atom["body"])
            lines.append(f"\n(Citation: {atom['source']})")
            lines.append("")

        if weak:
            lines.append("<!-- TODO_ATOMS -->")
            lines.append(f"- [ ] {title}: Need {needed - len(atoms)} more atoms for tags {tags}")
            lines.append("<!-- END_TODO_ATOMS -->")
            lines.append("")

        # Atomic write
        tmp_path = project_dir / "drafts" / ".tmp" / f"{ts}.tmp"
        tmp_path.parent.mkdir(exist_ok=True)
        tmp_path.write_text("\n".join(lines), encoding="utf-8")
        tmp_path.rename(draft_path)

        print(f"   ✅ Draft saved: {draft_path}")

    # Update progress
    prog = load_progress(project_dir)
    assembled: list = prog.get("sections_assembled", [])
    assembled_titles = [sec["title"] for sec in targets]
    for t in assembled_titles:
        if t not in assembled:
            assembled.append(t)
    prog["sections_assembled"] = assembled
    save_progress(project_dir, prog)

    advance_phase(project_dir, 4)
    print(f"\n✅ Assembly complete. Drafts in: {drafts_dir}/")


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def cmd_status(args):
    project_dir = Path(args.project_dir or ".")
    prog = load_progress(project_dir)

    print("📊 Literature Deck Status")
    print(f"   Project:     {prog.get('project', 'N/A')}")
    print(f"   Phase:       {prog['current_phase']}")
    print(f"   Atoms:       {prog.get('atoms_count', 0)}")
    print(f"   Sections:    {len(prog.get('sections_parsed', []))} parsed, {len(prog.get('sections_assembled', []))} assembled")
    print(f"   Last update: {prog.get('last_updated', 'N/A')}")

    # Check for missing tags by scanning project.yaml
    project_yaml = project_dir / "project.yaml"
    if project_yaml.exists():
        text = project_yaml.read_text(encoding="utf-8")
        needed = {}
        for m in re.finditer(r"atoms_needed:\s*(\d+)", text):
            needed["hypothesis"] = needed.get("hypothesis", 0) + int(m.group(1))
        print(f"   Total atoms needed (from hypotheses): {needed.get('hypothesis', 'N/A')}")


# ---------------------------------------------------------------------------
# Coverage
# ---------------------------------------------------------------------------

def cmd_coverage(args):
    project_dir = Path(args.project_dir or ".")
    prog = load_progress(project_dir)

    project_yaml = project_dir / "project.yaml"
    if not project_yaml.exists():
        print("❌ project.yaml not found.")
        sys.exit(1)

    text = project_yaml.read_text(encoding="utf-8")

    # Simple YAML block extraction for hypotheses
    print("📊 Coverage Matrix")
    print(f"{'Hypothesis':<20} {'Needed':>8} {'Found':>8} {'Status':>12}")
    print("-" * 52)

    # Find hypothesis blocks
    in_hyp = False
    current = {}
    for line in text.splitlines():
        if line.strip().startswith("- id:"):
            in_hyp = True
            current["id"] = line.split(":", 1)[1].strip()
        elif in_hyp and "atoms_needed:" in line:
            current["needed"] = int(line.split(":", 1)[1].strip())
            # Count atoms for this hypothesis by scanning atoms/
            atoms_dir = project_dir / "atoms"
            found = 0
            if atoms_dir.exists():
                for atom in atoms_dir.glob("*.md"):
                    content = atom.read_text(encoding="utf-8")
                    if current["id"] in content:
                        found += 1
            current["found"] = found
            status = "✅" if found >= current["needed"] else ("⚠️" if found >= current["needed"] / 2 else "🚨")
            print(f"{current['id']:<20} {current['needed']:>8} {found:>8} {status:>12}")
            current = {}
            in_hyp = False


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="deck-cli",
        description="Literature Deck Engine — atomic notes to paragraph drafts",
    )
    parser.add_argument(
        "--project-dir", "-p", default=".", help="Project directory (default: current)"
    )
    sub = parser.add_subparsers(dest="command")

    # init
    p_init = sub.add_parser("init", help="Initialize a new deck project")
    p_init.add_argument("project_name", help="Project directory name")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing directory")

    # extract
    p_extract = sub.add_parser("extract", help="Scaffold atom extraction from a paper")
    p_extract.add_argument("paper", help="Path to paper Markdown file")

    # outline parse
    p_outline = sub.add_parser("outline", help="Outline operations")
    p_outline_sub = p_outline.add_subparsers(dest="outline_cmd")
    p_parse = p_outline_sub.add_parser("parse", help="Parse outline.md to outline-map.yaml")
    p_parse.add_argument("outline", help="Path to outline Markdown file")

    # assemble
    p_assemble = sub.add_parser("assemble", help="Assemble paragraph drafts")
    g = p_assemble.add_mutually_exclusive_group(required=True)
    g.add_argument("--section", help="Assemble a specific section")
    g.add_argument("--all", action="store_true", help="Assemble all sections")

    # status
    sub.add_parser("status", help="Show project status")

    # coverage
    sub.add_parser("coverage", help="Show hypothesis coverage matrix")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "init":
        cmd_init(args)
    elif args.command == "extract":
        cmd_extract(args)
    elif args.command == "outline":
        if args.outline_cmd == "parse":
            cmd_outline_parse(args)
        else:
            p_outline.print_help()
    elif args.command == "assemble":
        cmd_assemble(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "coverage":
        cmd_coverage(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
