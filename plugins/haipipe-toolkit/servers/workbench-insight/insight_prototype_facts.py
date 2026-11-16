"""What a Question Book holds on disk, in the words its page uses: a question's state, a release's state, the
tally, the proposals, and the stylesheet its parts share."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import insight_plan_c as P
from live import insight_views as V
from live.frame import rel


ORDER = "DIKWX"                                   # the ladder, the Executive answers last: the order the work is done in
READ_ORDER = "XDIKW"                              # the order a reader meets them: Executive first, as the map and the phone tabs
LEVEL = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom", "X": "Executive"}
RUN_WORDS = {"plan-evidence": "Plan the evidence", "review-plan": "Review the plan", "write-script": "Write the script",
             "review-script": "Review the script", "review-questions": "Review the questions", "set-segments": "Set the segments",
             "sign-release": "Sign the release", "ask": "Ask the question", "triage-proposals": "Triage the proposals"}
CSS = """<style>
.pq{list-style:none;margin:0;padding:0}.pq li{padding:8px 2px;border-bottom:1px solid var(--line);font-size:14px;line-height:1.45}
.pq li:last-child{border-bottom:0}.pq .h{display:flex;flex-wrap:wrap;align-items:baseline;gap:2px 10px}
.pq .h b{font-weight:600}.pq .h .pb-pill{margin-left:auto}.pq .ask{margin:3px 0 0}
.pq .by{margin:3px 0 0;font-size:12.5px;color:var(--muted)}.pq .by a{margin-right:10px}
.pr-files{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:13.5px;margin:6px 0 0}
@media(max-width:600px){.pq .h .pb-pill{margin-left:0}}
</style>"""


# ── what is on disk ─────────────────────────────────────────────────────────────────────────────────────────────
def block_of(folder: Path, level: str) -> Path:
    return {"Block": folder, "Job": folder.parent, "Task": folder.parent.parent}.get(level, folder)


def _proto(folder: Path, level: str) -> dict:
    return P.prototype_at(block_of(Path(folder), level))


def _verdict(run: dict) -> str:
    """A soft Run's newest verdict, its pass's first heading (`# agreed`, `# returned`, `# release signed ✅ 261106`)."""
    passes = sorted((Path(run["path"]) / "passes").glob("*/pass.md")) if run.get("path") else []
    head = passes[-1].read_text(encoding="utf-8", errors="ignore").lstrip().split("\n", 1)[0] if passes else ""
    return head.lstrip("# ").strip()


def _newest_pass(run: dict) -> Path | None:
    passes = sorted((Path(run["path"]) / "passes").glob("*/pass.md")) if run.get("path") else []
    return passes[-1] if passes else None


def _soft(task: Path) -> dict:
    """{type: card} of a folder's soft Runs, by the type in their name (run-review-plan-d01 -> review-plan)."""
    out = {}
    for r in P.runs(task):
        if "_collect_" in r["run"]:                       # a 🙋 form is the page's Interaction, never a step of it
            continue
        m = re.match(r"^run-(.+?)-[a-z]?\d+$", r["run"]) or re.match(r"^run-(.+?)-[a-z0-9]+$", r["run"])
        out[str(r.get("type") or (m.group(1) if m else r["run"]))] = r
    return out


def _computes(q: dict) -> bool:
    return any(isinstance(n, dict) and n.get("kind") == "compute" for n in (q.get("needs") or {}).values())


def _scripts(q: dict) -> list:
    return sorted(p for p in (Path(q["task"]) / "scripts").glob("*.py")) if q.get("task") else []


def _done(run: dict | None) -> bool:
    return bool(run) and V._closed(run)


def q_state(q: dict) -> tuple:
    """(agreed word, script word) of a question, from question.md and its Runs: agreed · returned · to agree; script
    reviewed · script written · script to write; a question with no compute need cites the answers below it."""
    runs = _soft(Path(q["task"])) if q.get("task") else {}
    if str(q.get("agreed") or "").startswith("✅"):
        agreed = "agreed"
    elif _verdict(runs.get("review-plan", {})).startswith("returned"):
        agreed = "returned"
    else:
        agreed = "to agree"
    if not _computes(q):
        script = "cites the answers below"
    elif _done(runs.get("review-script")):
        script = "script reviewed"
    elif _done(runs.get("write-script")) or _scripts(q):
        script = "script written"
    else:
        script = "script to write"
    return agreed, script


def q_word(q: dict) -> str:
    return " · ".join(q_state(q))


def _ready(q: dict) -> bool:
    a, s = q_state(q)
    return a == "agreed" and s in ("script reviewed", "cites the answers below")


def _closed_r(r: dict) -> bool:
    """A release that takes no more change: release.yaml's face says closed, or carries a person's sign."""
    return str(r["face"].get("state")) == "closed" or str(r["face"].get("signed") or "").startswith("✅")


def r_word(r: dict) -> str:
    """A release's mark, never a state word: ✅ once a person signed it, ⬜ until then. What waits on the person (a
    proposal to triage, the sign itself) is the section's 🙋 line (insight_prototype_status._release_waits)."""
    return "✅" if str(r["face"].get("signed") or "").startswith("✅") else "⬜"


def tally_word(r: dict) -> str:
    """A Status bar's word, never a count ("draft · partly agreed"): a closed release its sign; a draft how far its
    questions are agreed and scripted."""
    if _closed_r(r):
        return r_word(r)
    qs = list(r["questions"].values())
    return f"draft · {V.far(sum(_ready(q) for q in qs), len(qs), 'agreed')}" if qs else "draft · no question yet"


def _release_of(proto: dict, folder: Path) -> dict | None:
    return next((x for x in proto["releases"] if x.get("job") == folder or Path(x.get("job") or "").name == folder.name), None)


def _label(r: dict) -> str:
    return r.get("label") or r["name"]


def _proposals(proto: dict, r: dict | None = None) -> list:
    """Every proposal (a Block), or a release's: those it took in, and the open ones while it is a draft."""
    ps = proto["proposals"]
    if r is None:
        return ps
    draft = not _closed_r(r)
    return [p for p in ps if str(p.get("taken-in") or "") == r["name"]
            or (draft and str(p.get("state") or "open").lower() in ("open", "proposed", ""))]


def _p_word(p: dict) -> str:
    st = str(p.get("state") or "open").lower()
    taken = str(p.get("taken-in") or "")
    return f"taken in {P.plan_code(taken)}" if st == "taken" and taken else st


def _focus(path: Path, root: Path) -> str:
    return f"/_board/workbench?path={quote(rel(path, root))}&layout=focus"


KIND_WORD = {"cut": "segment"}        # a proposal's `kind: cut` is the file's word; a person reads "segment"
