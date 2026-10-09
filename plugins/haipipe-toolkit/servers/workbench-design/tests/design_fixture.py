"""A placeholder design Project on b12's ladder, for the design theme's tests and screenshots (b12 s11 · s12 · s13).

The ladder (Tools/blueprints/b12_theme_design, goals/g01-design-workbench.md): a design Block `bNN_<app>/` holds its goal
list (board.md ## Goals), its inputs versions (inputs/iN/ + manifest.yaml), what an Exp returned
(observed/eNN_<exp>/), its soft Runs and its delivery/; a Job `jNN_<goal>_<design-method>/` pins one goal, one
registered method version and one inputs version (its face's goal: · method: · inputs:), fences its inputs in
inputs/, and holds t00 (② reason ideas), one Task per design (③ ④) and t99 (⑤ review whole). No real names and
no data values: every value is a placeholder. `make(root)` writes the Project under root and returns its folder.

    python design_fixture.py <out-dir>
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import yaml

PROJECT = "Project-DesignDemo"
BLOCK = "designs/b01_demo_app"
SMS = ["<opening>. <the reason>. <the ask>: {LINK}", "<opening>. <the reason as a question>? <the ask>: {LINK}",
       "<sender>. <the reason>. <the ask>: {LINK}", "<opening>. <the ask>: {LINK}",
       "<opening>, <the reason>. <the ask> today: {LINK}"]
GOALS = [{"id": "G01", "aim": "<the behaviour to change>", "who": "<audience>", "venue": "sms", "n": 10,
          "rules": ["<a rule for this goal only>"], "leave-out": "<what>", "signed": "✅ 261007"},
         {"id": "G02", "aim": "<another behaviour>", "who": "<audience>", "venue": "sms", "n": 10,
          "rules": [], "leave-out": "<what>", "signed": "✅ 261007"},
         {"id": "G03", "aim": "<a proposed behaviour>", "who": "<audience>", "venue": "sms", "n": 10,
          "rules": [], "leave-out": "", "signed": ""}]
QUESTIONS = [{"id": "Q01", "title": "Which method suits G01?", "evidence": ["j03", "j04"],
              "asks": "M04 m2 against M01 m1 on G01, the same inputs i2", "answer-status": "open",
              "report": "reports/q01_method-for-g01/"},
             {"id": "Q02", "title": "Did m2 beat m1?", "evidence": ["j02", "j03"], "answer-status": "answered",
              "report": "reports/q02_m2-against-m1/"},
             {"id": "Q03", "title": "Did our predictions hold?", "evidence": ["j03", "j04"], "answer-status": "open"}]
# (job, goal, method, version, inputs, state, moved, designs, dropped)
JOBS = [("j01_g01_m04", "G01", "M04", "m1", "i1", "closed", "start", 6, 0),
        ("j02_g01_m04", "G01", "M04", "m1", "i2", "closed", "inputs", 6, 0),
        ("j03_g01_m04", "G01", "M04", "m2", "i2", "released", "method", 15, 5),
        ("j04_g01_m01", "G01", "M01", "m1", "i2", "verify", "method", 4, 0),
        ("j05_g02_m01", "G02", "M01", "m1", "i2", "closed", "start", 3, 0)]
METHOD_STEPS = {   # each registered method's choice at the five steps (s03's design unit), placeholders
    "M04": {"① See input": "goal · rules · ours: the insight handoff", "② Reason ideas": "spread · distinct in principle",
            "③ Conduct process": "one design per idea, freestyle", "④ Review item": "T0 rules · T1 every source in the manifest",
            "⑤ Review whole": "rank the N + 5, keep the top N"},
    "M01": {"① See input": "goal only", "② Reason ideas": "more shots: N + 5 ideas", "③ Conduct process": "one design per idea",
            "④ Review item": "T0 rules", "⑤ Review whole": "rank, keep the top N"}}
STATES = ["passed", "passed", "passed", "passed", "revise", "passed", "passed", "verify", "passed", "passed"]


def _front(fields: dict, body: str = "") -> str:
    return "---\n" + yaml.safe_dump(fields, sort_keys=False, allow_unicode=True) + "---\n\n" + body


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12] if path.is_file() else "—"


HARD = ("reason", "generate", "verify", "rank")         # every Run is run-<type>-<target>; these four are hard


def _run(folder: Path, name: str, rtype: str, target: str, status: str = "closed", by: str = "designer agent",
         minutes: int = 4, extra: dict | None = None) -> Path:
    run = folder / "runs" / name
    card = {"type": rtype, "kind": "hard" if rtype in HARD else "soft", "target": target, "status": status,
            "by": by, "started_at": "2026-10-07T10:00:00", "finished_at": f"2026-10-07T10:{minutes:02d}:00"}
    _write(run / "run.yaml", yaml.safe_dump({**card, **(extra or {})}, sort_keys=False, allow_unicode=True))
    return run


def _block(block: Path) -> None:
    _write(block / "board.md",
           "# b01 · <app>\n\nboard-kind: design-board\nchannel: sms\n"
           "spine: One application, one channel: its goals, the inputs every Job reads, its Jobs and what they release.\n\n"
           "## Goals\n\n```yaml\n" + yaml.safe_dump({"goals": GOALS}, sort_keys=False, allow_unicode=True) + "```\n\n"
           "## Questions\n\n```yaml\n" + yaml.safe_dump({"questions": QUESTIONS}, sort_keys=False, allow_unicode=True) + "```\n")
    for v, handoff, new in (("i1", "W-02", "start"), ("i2", "W-03", "a new handoff (W-03); r2.3 added")):
        d = block / "inputs" / v
        _write(d / "rules.md", "# Shared rules\n\n- r2.1 <a rule>\n- r2.3 <a rule>\n")
        _write(d / f"handoff-{handoff}.md", f"# {handoff} · the insight handoff (placeholder)\n\n<the counsel, one line>\n")
        _write(d / "theory" / "papers.md", "# Theory\n\n- <a paper>\n")
        files = ["rules.md", f"handoff-{handoff}.md", "theory/papers.md"]
        _write(d / "manifest.yaml", yaml.safe_dump({
            "version": v, "frozen": "261007", "new": new, "rules": "r2" if v == "i2" else "r1",
            "parts": [{"part": "Goal · how much is set", "file": "rules.md", "says": "the shared rules"},
                      {"part": "Information · whose", "file": f"handoff-{handoff}.md", "says": "ours: the insight Block's signed handoff"},
                      {"part": "Information · form", "file": "theory/papers.md", "says": "a theory or rule"},
                      {"part": "Examples", "file": "", "says": "past released designs, from Delivery"}],
            "files": [{"path": f, "sha256": _sha(d / f)} for f in files]}, sort_keys=False, allow_unicode=True))
    e = block / "observed" / "e01_demo-exp"
    _write(e / "arms.csv", "arm,job,design,n,observed\nA,control,,<n>,<rate>\nB,j03,d04,<n>,+y [lo; hi]\n"
                           "C,j02,d06,<n>,+y [lo; hi]\nD,j04,d02,<n>,-y [lo; hi]\n")
    _write(e / "source.md", "# Source\n\nW-04 · the insight handoff of the Exp (per-arm totals only, placeholder).\n")
    _write(e / "manifest.yaml", yaml.safe_dump({"exp": "e01", "frozen": "261007",
                                                "files": [{"path": "arms.csv", "sha256": _sha(e / "arms.csv")}]}))
    for name, rtype, target in (("run-add-goal-g01", "add-goal", "G01"), ("run-add-goal-g02", "add-goal", "G02"),
                                ("run-setup-rules", "setup-rules", "rules r2"), ("run-add-inputs-i1", "add-inputs", "i1"),
                                ("run-add-inputs-i2", "add-inputs", "i2"), ("run-add-observed-e01", "add-observed", "e01"),
                                ("run-propose-questions", "propose-questions", "Q01 – Q03"),
                                ("run-report-q01", "report", "Q01")):
        _run(block, name, rtype, target, status="open" if name == "run-report-q01" else "closed")
    for job, goal, method, *_ in JOBS:
        _run(block, f"run-add-job-{job[:3]}", "add-job", f"{goal} × {method} → {job[:3]}")
    score = _run(block, "run-score-e01", "score", "e01")
    _write(score / "scores.csv", "job,design,predicted,observed,direction,in_range,error\n"
                                 "j03,d04,+x [lo; hi],+y [lo; hi],✓,✓,<e>\nj02,d06,+x [lo; hi],+y [lo; hi],✓,✗,<e>\n"
                                 "j04,d02,+x [lo; hi],-y [lo; hi],✗,✗,<e>\n")
    _write(block / "reports/q01_method-for-g01/q01_method-for-g01.md", "# Q01 · Which method suits G01?\n\n<the opening>\n")
    _write(block / "reports/q02_m2-against-m1/q02_m2-against-m1.md", "# Q02 · Did m2 beat m1?\n\n<the opening>\n")


def _design(job: Path, k: int, state: str, idea: str, released: bool, jid: str) -> None:
    slug = ["reason-first", "reason-question", "sender-first", "ask-only", "reason-then-ask"][(k - 1) % 5]
    t = job / f"t{k:02d}_d{k:02d}_{slug}"
    msg = SMS[(k - 1) % len(SMS)]
    _write(t / f"{t.name}.md", _front({"state": state, "name": slug, "idea": idea, "rank": k if state != "dropped" else ""},
                                      f"# d{k:02d} · {slug}\n\n## Design\n\n{msg}\n\n## Evaluation\n\n"
                                      f"T0 {'✓' if state != 'revise' else '✗ r2.3'} · T1 ✓\n"))
    _write(t / "elements.yaml", yaml.safe_dump([
        {"element": "opening", "words": "<opening>", "from": "W-03 row 2", "because": "<why>", "step": "③"},
        {"element": "reason", "words": "<the reason>", "from": "W-03 row 4", "because": "<why>", "step": "③"},
        {"element": "ask", "words": "<the ask>", "from": "rule r2.1", "because": "<why>", "step": "③",
         "changed": "draft 2" if k == 4 else ""}], sort_keys=False, allow_unicode=True))
    _write(t / "prediction.yaml", yaml.safe_dump({"predicted": "+x [lo; hi]", "against": "the control", "by": "the ④ ⑤ reviewer",
                                                  "frozen": "261007" if released else "draft"}, allow_unicode=True))
    d = f"d{k:02d}"
    _run(t, f"run-generate-{d}", "generate", d, minutes=3, extra={"draft": 1})
    _write(t / "runs" / f"run-generate-{d}" / "result" / "design.md", msg + "\n")
    if state == "verify":
        return
    passed = state not in ("revise",) and not (k == 4)
    _run(t, f"run-verify-{d}-v1", "verify", d, status="passed" if passed else "failed", by="another agent", minutes=2,
         extra={"tests": {"T0": "✓" if passed else "✗ r2.3", "T1": "✓"}})
    if k == 4:                                    # d04 passed on draft 2
        _run(t, f"run-revise-{d}", "revise", d, minutes=2, extra={"draft": 2})
        _write(t / "runs" / f"run-revise-{d}" / "result" / "design.md", msg + "\n")
        _run(t, f"run-verify-{d}-v2", "verify", d, status="passed", by="another agent", minutes=2,
             extra={"tests": {"T0": "✓", "T1": "✓"}})


def _job(block: Path, job: str, goal: str, method: str, version: str, inputs: str, state: str, moved: str,
         n_designs: int, dropped: int) -> None:
    j, jid = block / job, job[:3]
    kept = n_designs - dropped
    released = state == "released"
    _write(j / f"{job}.md", _front({"goal": goal, "method": f"{method} {version}", "method-sha": "<sha>", "inputs": inputs,
                                    "state": state, "moved": moved, "n": kept},
                                   f"# {jid} · {goal} by {method} {version} · inputs {inputs}\n"))
    fence = j / "inputs"
    _write(fence / "goal.md", f"# {goal}\n\n<the behaviour to change> · for <audience> · N = {kept}\n")
    _write(fence / "method.md", _front({"method": method, "version": version, "steps": METHOD_STEPS[method],
                                        "runs-it": "designer agent ①②③ · a reviewer agent ④⑤", "loops": "one pass"},
                                       f"# {method} · {version}\n"))
    _write(fence / "venue-sms.md", "# venue-sms\n\n<n> characters · one link\n")
    links = {"rules.md": f"../../inputs/{inputs}/rules.md"}
    if method == "M04":
        h = "W-02" if inputs == "i1" else "W-03"
        links[f"handoff-{h}.md"] = f"../../inputs/{inputs}/handoff-{h}.md"
    for name, target in links.items():
        if not (fence / name).exists():
            os.symlink(target, fence / name)
    parts = [{"part": "Goal · how much is set", "choice": "aim · N · leave out", "file": "goal.md"},
             {"part": "Goal · how much is set", "choice": "the shared rules", "file": "rules.md"},
             {"part": "Goal · for whom", "choice": "in goal.md: who", "file": ""},
             {"part": "Information · form", "choice": "the delivery setting", "file": "venue-sms.md"}]
    if method == "M04":
        parts.insert(3, {"part": "Information · whose", "choice": "ours: the insight Block's signed handoff",
                         "file": next(n for n in links if n.startswith("handoff"))})
    parts += [{"part": "Examples", "choice": "nothing", "file": ""}, {"part": "From the last unit", "choice": "nothing", "file": ""}]
    _write(fence / "manifest.yaml", yaml.safe_dump({
        "inputs": inputs, "frozen": "261007", "method": "method.md", "parts": parts,
        "files": [{"path": p.name, "source": os.readlink(p) if p.is_symlink() else "written", "sha256": _sha(p)}
                  for p in sorted(fence.iterdir()) if p.name != "manifest.yaml"]}, sort_keys=False, allow_unicode=True))
    for step in ("goal", "method", "inputs"):
        _run(j, f"run-setup-{step}-{jid}", f"setup-{step}", jid)
    _run(j, f"run-open-designs-{jid}", "open-designs", f"t01 – t{n_designs:02d}")
    # t00 · reason ideas
    t0 = j / "t00_reason-ideas"
    _write(t0 / "t00_reason-ideas.md", _front({"state": "closed", "step": "②"}, "# t00 · reason ideas\n"))
    r = _run(t0, "run-reason-t00", "reason", "t00", minutes=6)
    topics = [{"id": "T1", "title": "why click at all", "from": "W-03 row 2",
               "steps": [{"says": "<what the insight says>", "so": "give the reason before the ask"}], "ideas": ["I01", "I02"]},
              {"id": "T2", "title": "what to ask", "from": "rule r2.1",
               "steps": [{"says": "<the rule>", "so": "one ask, at the end"}], "ideas": ["I03", "I04"]},
              {"id": "T3", "title": "who it is from", "from": "own knowledge",
               "steps": [{"says": "<a known pattern>", "so": "name the sender first"}],
               "ideas": [f"I{k:02d}" for k in range(5, n_designs + 1)]}]
    _write(r / "result" / "chains.yaml", yaml.safe_dump({"topics": topics}, sort_keys=False, allow_unicode=True))
    _write(r / "result" / "ideas.yaml", yaml.safe_dump({"ideas": [
        {"id": f"I{k:02d}", "idea": f"<idea {k}>", "topic": "T1" if k < 3 else "T2" if k < 5 else "T3", "design": f"d{k:02d}"}
        for k in range(1, n_designs + 1)]}, sort_keys=False, allow_unicode=True))
    _write(r / "result" / "topics.md", "# Topics\n\n<the readable report, from chains.yaml>\n")
    # the designs
    for k in range(1, n_designs + 1):
        dstate = "dropped" if k > kept else (STATES[k - 1] if state in ("released", "verify") and k <= len(STATES) else "passed")
        if job.startswith("j04") and k > 2:
            dstate = "verify"
        _design(j, k, dstate, f"I{k:02d}", released and k <= kept, jid)
    # t99 · review whole
    t9 = j / "t99_review-whole"
    _write(t9 / "t99_review-whole.md", _front({"state": "closed" if state != "verify" else "waiting", "step": "⑤"},
                                              "# t99 · review whole\n"))
    if not job.startswith("j04"):
        r9 = _run(t9, "run-rank-t99", "rank", "t99", by="another agent", minutes=5)
        order = [4, 1] + [k for k in range(2, n_designs + 1) if k not in (4, 1)]
        _write(r9 / "result" / "ranking.csv", "rank,design,predicted,why,kept\n" + "".join(
            f"{i},d{k:02d},+x [lo; hi],<why>,{'yes' if i <= kept else 'no'}\n" for i, k in enumerate(order, 1)))
    if released:
        _run(j, f"run-freeze-predictions-{jid}", "freeze-predictions", jid, by="a person")
        _run(j, f"run-release-{jid}", "release", jid, by="a person")
        designs = [{"job": jid, "design": f"d{k:02d}", "words": SMS[(k - 1) % len(SMS)], "predicted": "+x [lo; hi]",
                    "released": "261007", "pins": {"goal": goal, "method": f"{method} {version}", "inputs": inputs}}
                   for k in (4, 1)]
        _write(j / "delivery" / "designs.json", json.dumps({"designs": designs}, indent=2, ensure_ascii=False))
        _write(j / "delivery" / "designs.md", "# Released designs\n\n" + "".join(
            f"## {d['design']}\n\n{d['words']}\n\n" for d in designs))


def make(root: Path) -> Path:
    project = Path(root) / PROJECT
    _write(project / "project.yaml", "name: DesignDemo\n")
    block = project / BLOCK
    _block(block)
    for spec in JOBS:
        _job(block, *spec)
    released = json.loads((block / "j03_g01_m04/delivery/designs.json").read_text())["designs"]
    released.append({"job": "j04", "design": "d02", "words": SMS[1], "predicted": "+x [lo; hi]", "released": "261007",
                     "pins": {"goal": "G01", "method": "M01 m1", "inputs": "i2"}})
    _write(block / "delivery" / "designs.json", json.dumps({"designs": released}, indent=2, ensure_ascii=False))
    _write(block / "delivery" / "designs.md", "# Released designs, every Job\n\n" + "".join(
        f"## {d['job']} · {d['design']}\n\n{d['words']}\n\n" for d in released))
    return project


if __name__ == "__main__":
    print(make(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
