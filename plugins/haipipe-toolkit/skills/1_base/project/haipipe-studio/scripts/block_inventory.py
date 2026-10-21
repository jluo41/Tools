"""What a Block's Jobs and Tasks already do, read off their faces: the ground its studio topics and its Questions
are inferred from (b10 s10, JL 261012: "I don't ask the questions that is meaningless ... the questions that are
closely related to the jobs and tasks ... learn how to infer the relevant studios from the existing block job and
task").

    python block_inventory.py <block> [--json]

It reads, never writes:

    the Block      its face (board.md or <block>.md): board-kind, its ## sections, its ## Questions register
    each Job       its face: goal, close, answers:; its Tasks
    each Task      its face's first lines (key: value), state, its Opening's first line, every sub-question
                   heading it answers (### …?), the first bold answer under each, its Runs and their status

and reports what repeats, which is what a topic or a Question can stand on:

    kinds          a Task kind that recurs across Jobs (t21_profile_glucose and t12_profile_cgm are both profile)
    splits         a face field whose few values split the Tasks (raw-family: 7 values over 310 Tasks)
    sub-questions  a heading most Tasks of one kind answer, and how its answers spread across the Jobs
    stands out     an answer few Tasks of a kind give (a minority value, or an Opening that says "no …")

Candidates follow, each with its evidence: a topic per recurring kind and per split (haipipe-studio
ref/infer-topics.md), and a Question per sub-question whose answers differ across Jobs (haipipe-report
ref/infer-reports.md). A candidate names the Tasks that answer it; a person and the agent word it, and one
that no Task answers is not a candidate at all.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

FIELD = re.compile(r"(?m)^([a-z][a-z0-9_-]*):[ \t]*(\S.*)$")
HEAD = re.compile(r"(?m)^#{2,4}[ \t]+(?:\d+[ \t]*·[ \t]*)?(.+\?)[ \t]*$")
BOLD = re.compile(r"\*\*(.+?)\*\*")
STATUS = {"state", "status", "stage", "answer-status", "updated", "date"}   # where the work stands, not what it is about
WHO = {"owner", "session", "codex-session", "goal", "close", "emoji"}   # who does it and its own lines, never a split
                                       # (b04 trial 261021: owner: proposed a topic s01-owner)


def face(folder: Path) -> Path | None:
    for name in (f"{folder.name}.md", "board.md"):
        if (folder / name).is_file():
            return folder / name
    return None


def fields(text: str, head: int = 2000) -> dict:
    """The face's key: value lines near its top (state, task-type, raw-family, goal, close, answers, ...)."""
    return {k: v.strip() for k, v in FIELD.findall(text[:head])}


def opening(text: str) -> str:
    m = re.search(r"(?ms)^## (?:🚪 )?Opening[ \t]*\n(.*?)(?=^## |\Z)", text)
    lines = [ln.strip() for ln in (m.group(1) if m else "").splitlines()
             if ln.strip() and not ln.lstrip().startswith(("📓", "<!--", ">"))]
    return lines[0] if lines else ""


def answers(text: str) -> dict:
    """{sub-question heading: its short answer}: the first bold phrase under each heading that ends in '?'."""
    out = {}
    heads = list(HEAD.finditer(text))
    for i, m in enumerate(heads):
        body = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        bold = BOLD.search(body)
        out[m.group(1).strip()] = re.sub(r"`", "", bold.group(1)).strip()[:80] if bold else ""
    return out


def runs(folder: Path) -> list:
    out = []
    for card in sorted(folder.glob("runs/*/run.yaml")):
        m = re.search(r"(?m)^status:\s*(\S+)", card.read_text(encoding="utf-8", errors="ignore"))
        out.append((card.parent.name, m.group(1) if m else ""))
    return out


def kind_of(name: str, subject: str = "") -> str:
    """A Task's kind: its name less tNN_, cut to its first word (profile_glucose, profile_cgm -> profile). A first
    word that only repeats the Block's subject is skipped: in b10_aidatastore, t01_aidatastore_materialize is a
    materialize Task, not an "aidatastore" one."""
    words = re.sub(r"^t\d+_", "", name).split("_")
    if len(words) > 1 and subject and words[0].lower() == subject.lower():
        words = words[1:]
    return words[0]


def bucket(answer: str) -> str:
    """An answer cut to its gist when answers vary too much to compare: none (None, No …, Nothing, 0) or some."""
    if re.match(r"(?i)\s*(none\b|no\b|nothing\b|0\b|the files hold no)", answer):
        return "none"
    return "some" if answer and answer != "(no bold answer)" else answer


def read_block(block: Path) -> dict:
    md = face(block)
    text = md.read_text(encoding="utf-8", errors="ignore") if md else ""
    reg = re.search(r"(?ms)^## Questions[ \t]*\n.*?```ya?ml\n(.*?)```", text)
    jobs = []
    subject = block.name.split("_", 1)[1] if "_" in block.name else ""     # b10_aidatastore -> aidatastore
    for jf in sorted(p for p in block.glob("j[0-9]*_*") if p.is_dir()):
        jmd = face(jf)
        jtext = jmd.read_text(encoding="utf-8", errors="ignore") if jmd else ""
        tasks = []
        for tf in sorted(p for p in jf.glob("t[0-9]*_*") if p.is_dir()):
            tmd = face(tf)
            ttext = tmd.read_text(encoding="utf-8", errors="ignore") if tmd else ""
            tasks.append({"name": tf.name, "kind": kind_of(tf.name, subject), "fields": fields(ttext), "opening": opening(ttext),
                          "answers": answers(ttext), "runs": runs(tf)})
        jobs.append({"name": jf.name, "fields": fields(jtext), "opening": opening(jtext), "tasks": tasks})
    return {"name": block.name, "face": md.name if md else None, "fields": fields(text),
            "sections": re.findall(r"(?m)^## (.+)$", text), "registered": len(re.findall(r"(?m)^\s*-\s+id:", reg.group(1)))
            if reg else 0, "jobs": jobs}


def summarize(b: dict) -> dict:
    tasks = [(j["name"], t) for j in b["jobs"] for t in j["tasks"]]
    kinds = collections.defaultdict(list)
    for jn, t in tasks:
        kinds[t["kind"]].append((jn, t))
    recurring = {k: v for k, v in kinds.items() if len({jn for jn, _ in v}) >= 2}
    # a field whose few values split the Tasks: on most of them, more than one value, fewer than the Jobs
    keys = collections.Counter(k for _, t in tasks for k in t["fields"])
    splits = {}
    for key, n in keys.items():
        values = collections.Counter(t["fields"][key] for _, t in tasks if key in t["fields"])
        per_job = {jn: {t["fields"][key] for j2, t in tasks if j2 == jn and key in t["fields"]} for jn, _ in tasks}
        restates_job = all(len(v) <= 1 for v in per_job.values()) and len(values) > len(b["jobs"]) / 2
        if key in STATUS or key in WHO:
            continue
        if (n >= len(tasks) / 2 and 2 <= len(values) < max(3, len(b["jobs"])) and not restates_job
                and max(len(v) for v in values) <= 60):          # a free-text field is no split
            splits[key] = dict(values.most_common())
    subq = {}
    for k, members in recurring.items():
        asked = collections.Counter(h for _, t in members for h in t["answers"])
        for h, n in asked.items():
            if n < max(2, len(members) / 2):
                continue
            spread = collections.defaultdict(list)
            for jn, t in members:
                if h in t["answers"]:
                    spread[t["answers"][h] or "(no bold answer)"].append(f"{jn}/{t['name']}")
            if len(spread) > 6:                                  # too many to compare: none against some
                gist = collections.defaultdict(list)
                for a, w in spread.items():
                    gist[bucket(a)] += w
                cut = {a: w for a, w in gist.items()}
            else:
                cut = dict(spread)
            subq[f"{k} · {h}"] = {"kind": k, "heading": h, "asked": n, "values": len(spread), "cut": len(cut),
                                  "spread": {a: w for a, w in sorted(spread.items(), key=lambda kv: -len(kv[1]))},
                                  "gist": {a: w for a, w in sorted(cut.items(), key=lambda kv: -len(kv[1]))}}
    stands = []
    for k, members in recurring.items():                   # what Openings say is missing: "no event time", …
        nos = collections.defaultdict(list)
        for jn, t in members:
            for phrase in re.findall(r"(?i)(?:^|[;:,.]\s*)(no [a-z][a-z ]{2,30}?)\s*(?=[.;,]|$)", t["opening"]):
                nos[phrase.lower()].append(jn)
        for phrase, js in sorted(nos.items(), key=lambda kv: -len(kv[1])):
            stands.append(f"{k} Openings · {phrase}: {len(js)} Tasks in " + ", ".join(sorted(set(js))))
    for key, q in subq.items():
        if 2 <= len(q["gist"]) <= 6:
            for answer, where in q["gist"].items():
                if len(where) <= max(1, q["asked"] // 4):
                    stands.append(f"{q['heading']} → {answer}: {len(where)} in "
                                  + ", ".join(sorted({w.split('/')[0] for w in where})))
    return {"tasks": len(tasks), "kinds": {k: {"tasks": len(v), "jobs": len({jn for jn, _ in v})} for k, v in
                                           sorted(kinds.items(), key=lambda kv: -len(kv[1]))},
            "recurring": sorted(recurring), "splits": splits, "subquestions": subq, "stands_out": stands}


def candidates(b: dict, s: dict) -> dict:
    """Topics and Questions a Block's own work can stand on, each with what answers it."""
    topics = [{"topic": f"how the {k} Tasks are done", "from": f"{s['kinds'][k]['tasks']} Tasks in {s['kinds'][k]['jobs']} Jobs",
               "asks": [q["heading"] for q in s["subquestions"].values() if q["kind"] == k][:6]}
              for k in s["recurring"]]
    topics += [{"topic": f"the {key} split", "from": " · ".join(f"{v} {n}" for v, n in vals.items()), "asks": []}
               for key, vals in s["splits"].items()]
    block_qs, job_qs = [], []
    for q in s["subquestions"].values():
        if 2 <= len(q["gist"]) <= 6:        # answers that differ across the work: a Block Question
            block_qs.append({"question": q["heading"], "kind": q["kind"], "answered_by": q["asked"],
                             "spread": {a: len(w) for a, w in q["gist"].items()},
                             "differ": {a: sorted({x.split("/")[0] for x in w}) for a, w in q["gist"].items()
                                        if len(w) <= q["asked"] // 2}})
        per_job = s["kinds"][q["kind"]]["tasks"] == s["kinds"][q["kind"]]["jobs"]
        settled = q["values"] == 1 and "(no bold answer)" not in q["spread"]
        if per_job and not settled:          # one Task of this kind per Job, not settled the same everywhere
            job_qs.append({"question": q["heading"], "answered_by": f"each Job's {q['kind']} Task"})
    return {"topics": topics, "block_questions": block_qs, "job_questions": job_qs,
            "task_questions": "each Task's own sub-questions; its report is its face (b10 s05-D10)"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("block", type=Path)
    ap.add_argument("--json", action="store_true", help="the whole reading as JSON")
    a = ap.parse_args(argv)
    if not a.block.is_dir():
        ap.error(f"{a.block} is not a folder")
    b = read_block(a.block)
    s = summarize(b)
    c = candidates(b, s)
    if a.json:
        print(json.dumps({"block": {k: v for k, v in b.items() if k != "jobs"}, "summary": s, "candidates": c},
                         indent=1, ensure_ascii=False))
        return 0
    print(f"{b['name']}  face {b['face']}  {b['fields'].get('board-kind', '')}  · {len(b['jobs'])} Jobs · {s['tasks']} Tasks"
          f" · {b['registered']} registered Questions · {len(b['sections'])} face sections")
    print("\nkinds      " + " · ".join(f"{k} {v['tasks']} ({v['jobs']} Jobs)" for k, v in s["kinds"].items()))
    for key, vals in s["splits"].items():
        print(f"split      {key}: " + " · ".join(f"{v} {n}" for v, n in vals.items()))
    print("\nsub-questions (asked by most Tasks of a kind):")
    for q in s["subquestions"].values():
        top = " · ".join(f"{a[:40]} {len(w)}" for a, w in list(q["gist"].items())[:4])
        print(f"  {q['kind']:<10} {q['heading'][:60]:<60} {q['asked']:>4} asked · {q['values']} answers: {top}")
    if s["stands_out"]:
        print("\nstands out:")
        for line in s["stands_out"][:20]:
            print("  " + line)
    print("\ncandidate topics:")
    for t in c["topics"]:
        print(f"  {t['topic']}  ({t['from']})" + (f"  asks: {' · '.join(t['asks'][:3])}" if t["asks"] else ""))
    print("candidate Block Questions (answers differ across Jobs):")
    for q in c["block_questions"]:
        print(f"  {q['question']}  ({q['answered_by']} {q['kind']} Tasks: "
              + " · ".join(f"{a} {n}" for a, n in q["spread"].items()) + ")"
              + ("  differ: " + "; ".join(f"{a}: {len(js)} Jobs" + (f" ({', '.join(js)})" if len(js) <= 4 else "")
                                           for a, js in q["differ"].items()) if q["differ"] else ""))
    print("candidate Job Questions:")
    for q in c["job_questions"]:
        print(f"  {q['question']}  ({q['answered_by']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
