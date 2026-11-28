#!/usr/bin/env python3
"""must_check.py · the must-check gate (ref/must-check.md § The gate): the scripts first, then who reads.

    python3 must_check.py <section Task | version Job> [--json]

1. Auto checks, each finding mapped to its must-check id where one fits:
     page.py health --final (M-C07 and the row its check names), page.py structure (M-E01, M-A02 ⚠ lines),
     scope_guard.py (M-A08, M-A13, M-A18, M-D08, M-D11), each printed number a VALUE item covers (M-D18),
     each printed citation key in the Bib (M-B07), a review Run at the current Draft version (M-E04, M-D03),
     chain_check.py on the Board (M-B01), values_ledger.py check where the value Job keeps value maps (M-B01),
     caption_check.py on the display Job (M-D12, M-B09).
2. The dispatch list: the reading agents (hai-draft/agents/) to send, by name, each with its Draft version and why.
   This script never calls an agent.
3. For the person (D3, M-E06): what the loop cannot settle: open Section questions, missing facts, unverified
   citations, numbers no VALUE item covers, the person's own signs.

Exit 1 when any auto check fails. Read only: values_ledger's Run output goes to a temporary folder and is dropped.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scope_guard as sg  # noqa: E402

SKILLS = next(p for p in HERE.parents if p.name == "skills")
PAGE = SKILLS / "1_base/draft/hai-draft/cli/page.py"
EVID = SKILLS / "3_theme/paper/hai-paper-evidence/scripts"
# page.py health check name -> must-check id (M-C07 is the gate itself)
HEALTH_ID = {"paragraphs": "M-A02", "ids": "M-D01", "sync": "M-C02", "narrative": "M-D09", "budget": "M-D11",
             "content": "M-D15", "printed": "M-C07", "steps": "M-C21", "header": "M-C21", "bullets": "M-C21",
             "structure": "M-E01", "evidence": "M-B06", "threads": "M-E07", "delivery": "M-C25", "row": "M-C21",
             "cite": "M-D20"}
PERSON_WORDS = ("sign", "person", "accept")
NUM = re.compile(r"(?<![\w.,\-])[-+−]?\d[\d,]*(?:\.\d+)?%?(?![\w])")
NOT_NUM = re.compile(r"\\(?:ref|cite[pt]?|autoref|label)\*?\{[^}]*\}|\b(?:Extended Data |Supplementary )?"
                     r"(?:Fig\.|Figs\.|Figure|Table)\s*~?\d+[A-Za-z]?\b|\bC\d+(?:\.P\d+)?(?:\.[BbSs]\d+)?\b|\$[^$]*\$")
CITE = re.compile(r"\\cite[tp]?\*?(?:\[[^\]]*\])*\{([^}]*)\}")
QUESTION = re.compile(r"(?m)^### (Section question[^\n]*)\n(?:(?!### )[^\n]*\n)*?State:\s*(proposed[^\n]*)")
ITEM = re.compile(r"(?m)^###\s+(E\d+[a-z]?)-(VALUE|CITE|DISPLAY|TABLE)-(\S+)")
AGENTS = ("hai-draft-eval-structure-agent", "hai-draft-eval-paragraph-agent",
          "hai-draft-eval-sentence-agent", "hai-draft-ab-reader-agent", "hai-draft-evidence-value-agent",
          "hai-draft-evidence-cite-agent", "hai-draft-evidence-display-agent", "hai-draft-consistency-agent")


def run(*cmd) -> tuple[int, str]:
    p = subprocess.run([sys.executable, "-B", *map(str, cmd)], capture_output=True, text=True)
    return p.returncode, p.stdout + (p.stderr if p.returncode not in (0, 1) else "")


class Gate:
    def __init__(self):
        self.auto, self.dispatch, self.person, self.notes = [], [], [], []

    def fail(self, mid, where, what, level="FAIL"):
        self.auto.append({"id": mid, "where": where, "what": what, "level": level})

    def ask(self, kind, where, what):
        self.person.append({"kind": kind, "where": where, "what": what})


def field(body: str, name: str) -> str:
    m = re.search(r"(?mi)^-\s*\*\*" + re.escape(name) + r"\*\*\s*:\s*(.*?)\s*$", body)
    return m.group(1) if m else ""


def items(task: Path) -> list:
    """[{id, kind, targets, verified, expected}] from draft/<stem>-evidence-items.md."""
    text = sg._read(task / "draft" / f"{task.name}-evidence-items.md")
    heads = list(ITEM.finditer(text))
    out = []
    for i, m in enumerate(heads):
        body = text[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        out.append({"id": f"{m.group(1)}-{m.group(2)}-{m.group(3)}", "kind": m.group(2),
                    "targets": [t.strip() for t in re.split(r"[,;]", field(body, "Target")) if t.strip()],
                    "verified": field(body, "Verified"), "expected": field(body, "Expected")})
    return out


def covered(sents: list, its: list) -> set:
    """Addresses of the sentences a VALUE or CITE item targets (C1.P1.B2 by bullet position, C1.P1.s2 or bare s2): a
    number in a cited sentence is the cited paper's fact, not ours, as Draft Lab reads it."""
    by_b, per = {}, {}
    for addr, _ in sents:
        pid = addr.rsplit(".", 1)[0] if "." in addr else ""
        per[pid] = per.get(pid, 0) + 1
        by_b[f"{pid}.B{per[pid]}".lower()] = addr
        by_b[addr.lower()] = addr
        by_b.setdefault(addr.rsplit(".", 1)[-1].lower(), addr)
    return {by_b[t.lower()] for it in its if it["kind"] in ("VALUE", "CITE") for t in it["targets"] if t.lower() in by_b}


def printed(text: str) -> list:
    """The numbers a sentence prints that need a VALUE item: as values_ledger.py counts them, an integer under 10 and a
    year are left out, and so are display calls, citations, ids and maths."""
    out = []
    for n in NUM.findall(NOT_NUM.sub(" ", text)):
        n = n.rstrip(",")
        bare = n.lstrip("+-−").rstrip("%").replace(",", "")
        if "." not in bare and (int(bare or 0) < 10 or 1900 <= int(bare) <= 2100):
            continue
        out.append(n)
    return out


def cite_states(board: Path) -> dict:
    """{key: status} from the citation Job's newest checks (cite_tasks.py citations.csv), t99 first."""
    out = {}
    for f in sorted(board.glob("j*/t99*/runs/*/result/citations.csv"), reverse=True) + sorted(
            board.glob("j*/t[0-8]*/runs/*/result/citations.csv"), reverse=True):
        with f.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                k, st = r.get("key", ""), r.get("status", "")
                if k and (k not in out or st == "verified"):
                    out[k] = st
    return out


def review_runs(board: Path, tnn: str, version: str) -> dict:
    """{step: run name} of the review Job's Runs for this Section at this Draft version."""
    steps = {"structure": "structure", "paragraph": "paragraph|logic", "sentence": "sentence", "ab": "readability|blind"}
    out = {}
    for run_dir in sorted(board.glob("j*_review_*/t*/runs/r*")):
        name, task = run_dir.name, run_dir.parent.parent.name
        named = [t for t in name.split("_")[1:] if re.fullmatch(r"t\d+", t)]
        if named and tnn not in named:
            continue                                  # another Section's Run; a Run naming none covers all
        for step, pat in steps.items():
            if re.search(pat, task) and (step == "ab" or name.endswith(f"_{version}")):
                out[step] = f"{task}/runs/{name}"
    return out


def section(task: Path, board: Path, g: Gate, cites: dict):
    tag = task.name
    rc, out = run(PAGE, "health", "--final", "--json", task)
    try:
        rep = json.loads(out)[0]
    except (ValueError, IndexError):
        rep = {"findings": [{"level": "FAIL", "check": "health", "message": out.strip()[:200]}]}
    for f in rep["findings"]:
        if f["level"] in ("FAIL", "WARN"):
            mid = HEALTH_ID.get(f["check"], "M-C07")
            if f["level"] == "WARN" and any(w in f["message"] for w in PERSON_WORDS):
                g.ask("sign", tag, f"{mid} {f['message']}")
            else:
                g.fail(mid, tag, f"health {f['check']}: {f['message']}", f["level"])
    for rec in sorted((task / "draft" / "records").glob("*-revise.md")):      # M-D22: every problem has a card or a fix
        text = rec.read_text(encoding="utf-8", errors="replace")
        carded = {m.lower() for m in re.findall(r"(?m)^### (?:Edit|Review)\s*·\s*((?:C\d+\.P\d+\.)?[Ss]\d+[a-z]*)", text)}
        for m in re.finditer(r"(?m)^- ((?:C\d+\.P\d+\.)?[Ss]\d+[a-z]*) · (.*)$", text):
            sid, rest = m.group(1).lower(), m.group(2)
            scores = [int(n) for n in re.findall(r"\b(\d{1,2})/10\b", rest)]
            over = re.search(r"topics?\s+(\d+)\s*,\s*points?\s+(\d+)", rest, re.I)
            bad = (scores and min(scores) < 8) or re.search(r"\b(weak|broken)\b", rest.split(" · Fix:")[0]) \
                or (over and (int(over.group(1)) > 1 or int(over.group(2)) > 3))
            fix = rest.rsplit(" · Fix:", 1)[1].strip().lower() if " · Fix:" in rest else ""
            if bad and fix in ("", "none") and sid not in carded and sid.rsplit(".", 1)[-1] not in carded:
                g.fail("M-D22", f"{tag} {sid}", "a problem with no Fix and no Edit card")
    rc, out = run(PAGE, "structure", task)
    for line in ([f"page.py structure failed: {out.strip()[:160]}"] if rc else []) + [x for x in out.splitlines() if "⚠" in x]:
        g.fail("M-E01" if rc else "M-A02", tag, "structure " + " ".join(line.split()))
    rep = sg.guard(task)
    version = rep["version"]
    for h in rep["hits"]:
        (g.notes.append(f"{tag} {h['where']}: {h['what']}") if h["kind"] == "read"
         else g.fail(h["rule"], f"{tag} {h['where']}", h["what"]))
    sents = sg.sentences(sg._read(sg.newest_draft(task)))
    its = items(task)
    cov = covered(sents, its)
    loose = [(a, n) for a, n in ((a, printed(t)) for a, t in sents if a not in cov) if n]
    for a, n in loose:
        g.ask("number", f"{tag} {a}", f"M-D18 no VALUE item covers {', '.join(n[:4])}")
    keys = list(dict.fromkeys(k.strip() for _, t in sents for grp in CITE.findall(t) for k in grp.split(",")))
    for k in keys:
        st = cites.get(k, "")
        if k == "TOADD" or st == "missing-bib":
            g.fail("M-B07", tag, f"citation {k}: {'TOADD' if k == 'TOADD' else 'not in the Bib'}")
        elif st != "verified":
            g.ask("cite", tag, f"M-E09 {k}: {st or 'not in the citation check'}, a person verifies")
    for it in (i for i in its if i["kind"] != "CITE"):     # a CITE item's state is the citation's, listed above
        if it["verified"].startswith("⬜") or re.search(r"\bowe[sd]?\b|open need", it["expected"], re.I):
            g.ask("fact", tag, f"M-E09 {it['id']}: {it['verified'] or 'not verified'}")
    revise = sg._read(task / "draft" / "records" / f"{tag}-revise.md")
    for title, state in QUESTION.findall(revise):
        g.ask("claim", tag, f"M-E06 {title.strip()}: {state.strip()}")
    done = review_runs(board, tag.split("_")[0], version)
    for step in [s for s in ("paragraph", "sentence") if s not in done]:
        g.fail("M-E04", tag, f"no {step} review Run at Draft {version} (M-D03)")
    displays = any(re.search(r"\\ref\{(?:fig|tab):|\bFig(?:ure|\.)\s*\d", t) for _, t in sents)
    why = [("structure", "S1, S2 at " + version if "structure" not in done else None),
           ("paragraph", f"D1 at {version}" if "paragraph" not in done else None),
           ("sentence", f"D1 at {version}, with the scope guard's READ lines" if "sentence" not in done else None),
           ("ab", "D2, after hai-draft-writing-agent writes a rewrite for each item under 8"),
           ("value", f"{len(loose)} sentences print a number no VALUE item covers" if loose else None),
           ("cite", f"{sum(cites.get(k) != 'verified' for k in keys)} keys not verified"
            if any(cites.get(k) != "verified" for k in keys) else None),
           ("display", "the Section calls displays" if displays else None)]
    for (step, reason), agent in zip(why, AGENTS[:7]):
        if reason:
            g.dispatch.append({"agent": agent, "task": tag, "version": version, "why": reason})
        elif step in done:
            g.notes.append(f"{tag}: {agent} already ran at {version}: {done[step]}")


def board_checks(board: Path, g: Gate, scope: str = ""):
    rc, out = run(EVID / "chain_check.py", board, "--json")
    try:
        for f in json.loads(out)["failures"]:
            head = f["where"].split("/")[0]
            if scope and "_writing_" in head and f"/{scope}/" not in f["where"] + "/":
                continue                              # another Section's binding: its own gate names it
            g.fail("M-B01", f["where"], f"chain rule {f['rule']}: {f['what']}")
    except (ValueError, KeyError):
        g.fail("M-B01", board.name, "chain_check.py did not run: " + out.strip()[:160])
    j02 = next(iter(sorted(board.glob("j*_evidence_value"))), None)
    if j02 and list(j02.glob("t*/scripts/value_map.yaml")):
        with tempfile.TemporaryDirectory() as tmp:
            import yaml
            run(EVID / "values_ledger.py", "check", j02, tmp)
            text = sg._read(Path(tmp) / "values.yaml")
            doc = yaml.safe_load(text[text.find("\n") + 1:]) or {}
        for r in doc.get("rows", []):
            if r.get("status") in ("differs", "missing", "stale") and (not scope or scope in str(r.get("where"))):
                g.fail("M-B01", str(r.get("where")), f"value {r.get('key')}: {r.get('status')}")
    j01 = next(iter(sorted(board.glob("j*_evidence_display"))), None)
    if j01:
        rc, out = run(EVID / "caption_check.py", j01)
        for line in out.splitlines():
            if line.startswith("❗"):
                g.fail("M-D12" if "numbering" in line else "M-B09",
                       j01.name, line.lstrip("❗ ").strip())


def sections_of(job: Path) -> list:
    face = sg._read(job / f"{job.name}.md")
    block = re.search(r"compile-order:start -->(.*?)<!--", face, re.S)
    names = re.findall(r"(?m)^-\s*(t\d+\S*)", block.group(1)) if block else []
    names = names or sorted(p.name for p in job.glob("t[0-9]*") if (p / "draft").is_dir())
    return [job / n for n in names if (job / n / "draft").is_dir()]


def gate(target: Path) -> dict:
    target = Path(target).resolve()
    board = sg.board_of(target)
    if board is None:
        raise SystemExit(f"no paper Board (board.md) above {target}")
    g = Gate()
    cites = cite_states(board)
    if re.match(r"t\d+", target.name) and (target / "draft").is_dir():
        mode, tasks = "section", [target]
    else:
        mode, tasks = "version", sections_of(target)
        rc, out = run(PAGE, "health", "--final", "--json", target)
        try:
            for f in json.loads(out)[0]["findings"]:
                if f["level"] in ("FAIL", "WARN"):
                    g.fail(HEALTH_ID.get(f["check"], "M-C07"), target.name, f"{f['check']}: {f['message']}", f["level"])
        except (ValueError, IndexError, KeyError):
            g.fail("M-C07", target.name, "page.py health did not run: " + out.strip()[:160])
    for task in tasks:
        section(task, board, g, cites)
    board_checks(board, g, target.name if mode == "section" else "")
    versions = {t.name: sg.draft_version(sg.newest_draft(t)) for t in tasks}
    job = target if mode == "version" else target.parent
    g.dispatch.append({"agent": AGENTS[7], "task": job.name, "version": ", ".join(f"{k} {v}" for k, v in versions.items()),
                       "why": "one report for the version: terms, wording of one claim, counts"})
    fails = [a for a in g.auto if a["level"] == "FAIL"]
    return {"target": target.name, "mode": mode, "board": board.name, "versions": versions, "auto": g.auto,
            "failed": len(fails), "dispatch": g.dispatch, "person": g.person, "notes": g.notes}


def render(rep: dict) -> str:
    vs = " · ".join(f"{k} {v}" for k, v in rep["versions"].items())
    lines = [f"must_check {rep['target']} ({rep['mode']}) · {vs}", "", "## Auto checks"]
    lines += [f"{'❌' if a['level'] == 'FAIL' else '⚠️'} {a['id']} {a['where']}: {a['what']}" for a in rep["auto"]]
    lines += ["✅ every auto check passes"] if not rep["failed"] else []
    lines += ["", "## Dispatch (fresh context each; none reads text it wrote)"]
    lines += [f"- {d['agent']} · {d['task']} · Draft {d['version']} · {d['why']}" for d in rep["dispatch"]]
    lines += ["", "## For the person (what the loop cannot settle)"]
    heads = {"claim": "open claims and story questions", "fact": "evidence a person checks",
             "cite": "citations a person verifies", "number": "numbers no VALUE item covers", "sign": "the person's signs"}
    for kind, head in heads.items():
        rows = [p for p in rep["person"] if p["kind"] == kind]
        lines += [f"{head}:"] if rows else []
        lines += [f"- {p['where']}: {p['what']}" for p in rows[:12]]
        lines += [f"- and {len(rows) - 12} more (--json lists all)"] if len(rows) > 12 else []
    lines += ["- nothing"] if not rep["person"] else []
    if rep["notes"]:
        lines += ["", "## Notes"] + [f"- {n}" for n in rep["notes"]]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("target", type=Path, help="a paper Section Task (tNN_<section>) or a version Job (jNN_writing_*)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    rep = gate(a.target)
    print(json.dumps(rep, indent=1, ensure_ascii=False) if a.json else render(rep))
    return 1 if rep["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
