#!/usr/bin/env python3
"""/wb update <block>: bring one Block, old or new and of any theme, up to today's rules (b10 s10, JL 261012:
"I want it work like /wb update-to-date path to the block").

    wb.py update <block> [--apply] [--json] [--no-open]

Seven steps, each done by the skill that owns that part; a dry run writes nothing:

    1 shape      haipipe-project ladder.py audit                 names, faces, folders, Run cards
    2 today      ladder.py audit --today                         studio topics, Questions register, reports/
    3 plan       what moves, what is made, what is proposed      printed
    4 apply      --apply: the moves (ladder.py update --today --apply), then a pass of
                 <block>/runs/run-update-<bNN>/ holding proposals.md, the list a person ticks
    5 topics     haipipe-studio block_inventory.py               the topics the Block's own work stands on
    6 Questions  the same reading (haipipe-report ref/infer-reports.md): Block and Job Questions
                 where the Jobs' answers differ; each one's group is its topic's
    7 open       the workbench link at the Block's Studio; opened after --apply

Nothing proposed in steps 5 and 6 is made here (s10-D03): the agent words each line per
haipipe-studio ref/infer-topics.md and haipipe-report ref/infer-reports.md, a person ticks
proposals.md, and only the ticked lines become studio/sNN-*/ folders (new_topic.py) and
register rows (haipipe-question).
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import io
import json
import re
import sys
import webbrowser
from pathlib import Path

import wb

PROJECT = wb.SKILLS / "1_base" / "project"
for _d in ("haipipe-project", "haipipe-studio", "haipipe-run"):
    sys.path.insert(0, str(PROJECT / _d / "scripts"))
import block_inventory as inv  # noqa: E402
import ladder  # noqa: E402
import soft_run  # noqa: E402

BAND = range(1, 10)                     # s01-s09: concept topics (haipipe-studio numbering)


def short(block: Path) -> str:
    """b00_rawdata -> b00; a Block not named bNN_ keeps its own lower-case name."""
    m = re.match(r"^(b\d{2})_", block.name)
    return m.group(1) if m else re.sub(r"[^a-z0-9_.-]", "-", block.name.lower())


# ── steps 1 to 3 ──────────────────────────────────────────────────────────────────────────────────

def shape(block: Path, root: Path) -> dict:
    nodes = ladder.audit_path(block, root)
    counts: dict = {}
    failed = []
    for n in ladder.walk(nodes):
        counts.setdefault(n.level, {"ok": 0, "debt": 0, "failed": 0})[n.status] += 1
        failed += [f"{n.path.relative_to(block).as_posix() or '.'}: {m}" for s, m in n.findings if s == "failed"]
    debt = [m for n in nodes for s, m in n.findings if s == "debt"]
    return {"counts": counts, "failed": failed, "block_debt": debt}


def plan(block: Path, root: Path) -> dict:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        ladder.update(block, root, apply=False, today=True)
    lines = [ln.rstrip() for ln in out.getvalue().splitlines() if ln.strip()]
    at = wb.rel(block, root) + "/"
    moves = [ln.strip()[3:].replace(at, "") for ln in lines if ln.strip().startswith("mv ")]
    counts = next((ln for ln in reversed(lines) if "planned" in ln), "")
    return {"moves": moves, "ladder": counts}


# ── steps 5 and 6 ─────────────────────────────────────────────────────────────────────────────────

def topic_proposals(block: Path, s: dict) -> list[dict]:
    """A topic per recurring Task kind (largest first), then one per field that splits the Tasks."""
    studio = block / "studio"
    taken = {int(m.group(1)) for d in studio.iterdir() for m in [re.match(r"^s(\d{2})[-_]", d.name)] if m} \
        if studio.is_dir() else set()
    faces = [f for d in studio.iterdir() if d.is_dir() and re.match(r"^s\d{2}[-_]", d.name) and not d.name.startswith("s00")
             for f in [d / f"{d.name}.md"] if f.is_file()] if studio.is_dir() else []
    have = " ".join([d.name for d in studio.iterdir()] if studio.is_dir() else []) + " " + \
        " ".join(f.read_text(encoding="utf-8", errors="ignore") for f in faces).lower()   # names and faces
    free = iter(n for n in BAND if n not in taken)
    out = []
    kinds = sorted(s["recurring"], key=lambda k: -s["kinds"][k]["tasks"])
    for k in kinds:
        if re.search(rf"(?<![a-z]){re.escape(k)}(?![a-z])", have):
            continue
        asks = [q["heading"] for q in s["subquestions"].values() if q["kind"] == k]
        out.append({"slug": f"{k}-tasks", "title": f"How the {k} Tasks are done", "kind": k,
                    "from": f"{s['kinds'][k]['tasks']} Tasks in {s['kinds'][k]['jobs']} Jobs", "asks": asks})
    for key, vals in s["splits"].items():
        noun = key.replace("_", "-").split("-")[-1]
        if re.search(rf"(?<![a-z]){re.escape(noun[:max(4, len(noun) - 2)])}", have):   # raw-family: s02-raw-families
            continue
        out.append({"slug": key.replace("_", "-"), "title": f"The {key} split", "kind": "",
                    "from": " · ".join(f"{v} {n}" for v, n in vals.items()), "asks": []})
    for t in out:
        n = next(free, None)
        t["snn"] = f"s{n:02d}" if n else "s??"
        # a first guess the agent rewords (haipipe-studio ref/infer-topics.md § Groups): the kind, or the split's noun
        t["group"] = (t["kind"] or t["slug"].split("-")[-1]).replace("_", " ").capitalize()
    return out


def question_proposals(b: dict, s: dict, c: dict, topics: list[dict]) -> dict:
    group = {t["kind"]: t["group"] for t in topics if t["kind"]}
    start = b["registered"] + 1
    block_qs = []
    for i, q in enumerate(c["block_questions"]):
        few = {a: js for a, js in q["differ"].items()}
        block_qs.append({"id": f"Q{start + i:02d}", "question": q["question"], "kind": q["kind"],
                         "group": group.get(q["kind"], q["kind"].capitalize()),
                         "answered_by": f"{q['answered_by']} {q['kind']} Tasks",
                         "spread": q["spread"],
                         "differ": {a: [j.split("_")[0] for j in js] for a, js in few.items()}})
    job_qs = [{"question": q["question"], "answered_by": q["answered_by"]} for q in c["job_questions"]]
    return {"block": block_qs, "job": job_qs}


# ── step 4: the tick list ─────────────────────────────────────────────────────────────────────────

def proposals_md(block: Path, r: dict) -> str:
    lines = [f"# /wb update {block.name} · proposals to tick", "",
             "Tick `[x]` what to keep; only ticked lines are made (b10 s10-D03). Reword a line before ticking:",
             "the agent words each one from the Tasks named (haipipe-studio ref/infer-topics.md,",
             "haipipe-report ref/infer-reports.md).", "", "## Moves done by --apply", ""]
    lines += [f"- {m}" for m in r["plan"]["moves"]] or ["- none"]
    lines += ["", "## Topics (haipipe-studio new_topic.py topic)", ""]
    for t in r["topics"]:
        asks = f" · asks: {' · '.join(t['asks'][:5])}" if t["asks"] else ""
        lines.append(f"- [ ] {t['snn']}-{t['slug']} · {t['title']} · group {t['group']} · {t['from']}{asks}")
    order = list(dict.fromkeys(t["group"] for t in r["topics"]))
    lines += ["", "## Group order (studio/_groups.txt; the Report's bar follows it)", "",
              "- [ ] " + " · ".join(order) if order else "- none"]
    lines += ["", "## Block Questions (haipipe-question)", ""]
    for q in r["questions"]["block"]:
        spread = " · ".join(f"{a} {n}" for a, n in q["spread"].items())
        differ = "; ".join(f"{a}: {', '.join(js)}" for a, js in q["differ"].items() if len(js) <= 6)
        lines.append(f"- [ ] {q['id']} · {q['group']} · {q['question']} · {q['answered_by']}: {spread}"
                     + (f" · differ {differ}" if differ else ""))
    lines += ["", "## Job Questions (each Job's register; its report is that Task's face)", ""]
    lines += [f"- [ ] {q['question']} · {q['answered_by']}" for q in r["questions"]["job"]]
    lines += ["", "## Task Questions", "", "Each Task's own sub-questions; its report is its face (b10 s05-D10).", ""]
    return "\n".join(lines)


def write_pass(block: Path, r: dict) -> Path:
    name = f"run-update-{short(block)}"
    run = block / "runs" / name
    if not run.is_dir():
        soft_run.new(block, "update", short(block), skill="workbench", agent="",
                     ask=f"/wb update {block.name}: bring it to today's rules, propose its topics and Questions",
                     close="a person ticked proposals.md and the ticked lines are made",
                     writes=["studio/", "reports/", "board.md"])
    moved = [m.split(" → ")[0] for m in r["plan"]["moves"]]
    folder = soft_run.add_pass(run, f"/wb update {block.name}", ask="bring the Block to today's rules (b10 s10)",
                               summary=f"{len(moved)} move(s); {len(r['topics'])} topic(s), "
                                       f"{len(r['questions']['block'])} Block Question(s) and "
                                       f"{len(r['questions']['job'])} Job Question(s) proposed in proposals.md",
                               changed=moved, status="waiting")
    (folder / "proposals.md").write_text(proposals_md(block, r), encoding="utf-8")
    return folder


# ── main ──────────────────────────────────────────────────────────────────────────────────────────

def update(block: Path, root: Path, apply: bool) -> dict:
    r: dict = {"block": wb.rel(block, root), "apply": apply, "date": dt.date.today().isoformat()}
    r["shape"] = shape(block, root)
    r["today"] = [m for _, m in ladder.today_findings(block)]
    r["plan"] = plan(block, root)
    b = inv.read_block(block)
    s = inv.summarize(b)
    c = inv.candidates(b, s)
    r["inventory"] = {"jobs": len(b["jobs"]), "tasks": s["tasks"], "registered": b["registered"],
                      "kinds": s["kinds"], "splits": s["splits"]}
    r["topics"] = topic_proposals(block, s)
    r["questions"] = question_proposals(b, s, c, r["topics"])
    # a rerun proposes only what no earlier pass named, kept or dropped (its tick lists hold both)
    earlier = " ".join(f.read_text(encoding="utf-8", errors="ignore") for f in
                       sorted((block / "runs" / f"run-update-{short(block)}" / "passes").glob("*/proposals.md")))
    if earlier:
        seen = lambda words: words.lower() in earlier.lower()
        before = len(r["topics"]) + len(r["questions"]["block"]) + len(r["questions"]["job"])
        r["topics"] = [t for t in r["topics"] if not seen(t["slug"])]
        r["questions"]["block"] = [q for q in r["questions"]["block"] if not seen(q["question"])]
        r["questions"]["job"] = [q for q in r["questions"]["job"] if not seen(q["question"])]
        r["earlier"] = before - len(r["topics"]) - len(r["questions"]["block"]) - len(r["questions"]["job"])
    if apply:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            ladder.update(block, root, apply=True, today=True)
        r["pass"] = wb.rel(write_pass(block, r), root)
    place = wb.target(block, root, studio=True)
    found = wb.servers(root)
    r["link"] = (found[0].public if found else "") + place["url"]
    r["theme"] = place["theme"]
    return r


def render(r: dict) -> str:
    sh, counts = r["shape"], r["shape"]["counts"]
    lines = [f"/wb update {r['block']}" + ("   (applied)" if r["apply"] else "   (dry run: nothing written; --apply)"),
             "",
             "1 shape      " + " · ".join(f"{lvl} {sum(c.values())} (debt {c['debt']}, failed {c['failed']})"
                                        for lvl, c in counts.items())]
    lines += [f"             ✗ {f}" for f in sh["failed"][:8]]
    lines += ["2 today      " + ("ok" if not r["today"] else f"{len(r['today'])} finding(s)")]
    lines += [f"             · {m.removeprefix('today: ')}" for m in r["today"]]
    planned = r["plan"]["ladder"] or "nothing to move"
    lines += ["3 plan       " + (planned.replace("planned (dry run; --apply to do it)", "applied in step 4")
                                 if r["apply"] else planned)]
    lines += [f"             mv {m}" for m in r["plan"]["moves"][:12]]
    lines += ["4 apply      " + (f"done; tick {r['pass']}/proposals.md" if r.get("pass") else "not run (--apply)")]
    lines += [f"5 topics     {len(r['topics'])} proposed from {r['inventory']['tasks']} Tasks in "
              f"{r['inventory']['jobs']} Jobs"]
    lines += [f"             {t['snn']}-{t['slug']:<22} {t['from'][:70]}" for t in r["topics"]]
    lines += [f"6 Questions  {len(r['questions']['block'])} Block · {len(r['questions']['job'])} Job"
              f" (already registered: {r['inventory']['registered']})"
              + (f"; {r['earlier']} candidate(s) skipped, named in an earlier pass" if r.get("earlier") else "")]
    for q in r["questions"]["block"]:
        spread = " · ".join(f"{a} {n}" for a, n in q["spread"].items())
        lines.append(f"             {q['id']} {q['group']:<8} {q['question'][:56]:<56} {spread[:40]}")
    for q in r["questions"]["job"]:
        lines.append(f"             Job      {q['question'][:56]:<56} {q['answered_by']}")
    lines += [f"7 open       {r['link']}" + (f"   theme {r['theme']}" if r["theme"] else "")]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="wb.py update", description=__doc__.split("\n\n")[0])
    ap.add_argument("block")
    ap.add_argument("--root")
    ap.add_argument("--apply", action="store_true", help="make the moves and write the pass to tick")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else wb.space_root(Path.cwd().resolve())
    if root is None:
        raise SystemExit("wb update: no SPACE root above this folder; pass --root")
    block = wb.resolve_path(a.block, root)
    if block is None or not ladder.NAMES["block"].match(block.name):
        raise SystemExit(f"wb update: {a.block} is not a Block folder (bNN_<topic>/) inside {root.name}")
    r = update(block, root, a.apply)
    print(json.dumps(r, ensure_ascii=False, indent=1) if a.json else render(r))
    if a.apply and not a.no_open and r["link"].startswith("http"):
        webbrowser.open(r["link"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
