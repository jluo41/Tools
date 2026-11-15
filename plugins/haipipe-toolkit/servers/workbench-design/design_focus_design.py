"""A design and a Job as every design focus view reads them: the design card, predicted vs observed, a Job's next
move, a design's drafts and state, the fence check, a review file's sections and the coverage (split out of
design_focus.py)."""
from __future__ import annotations

import re
from pathlib import Path

from live import design_canvas as C
from live import design_reader as R
from live import design_views as V
from live.frame import esc, pop, reader, table
from live.ui_parts import _kv
from live.design_focus_parts import _closed, _link, _plain

# ── a design, as the focus page shows it ───────────────────────────────────────────────────────────────────────
def _design_card(d: dict, j: dict, root: Path) -> str:
    """One design: as it reads on the left, on the right its idea, drafts, verify (④), prediction and rank (⑤), and
    each element with its source (the drawing's design card, b12 j01 B1 and B4)."""
    r = {x.get("design"): x for x in j["ranking"]}.get(d["id"], {})
    tests = d["verifies"][-1]["card"].get("tests", {}) if d["verifies"] else {}
    words = V._ideas_text(j).get(str(d["idea"]), "")
    elements = "".join(f'<li>{esc(e.get("words", ""))} <span class=mut>← {esc(e.get("from", ""))}</span></li>'
                       for e in d["elements"] if isinstance(e, dict))
    right = _kv([("idea", esc(f'{d["idea"]} · {words}' if words else d["idea"] or "—")),
                 ("drafts", esc(_chain_words(d))),
                 ("verify ④", (" · ".join(f"{V._test(t)} {esc(v)}" for t, v in tests.items()) or "not yet") + " · " + V._st(_design_state(d))),
                 ("predicted", V._pred(d["prediction"])),
                 ("rank ⑤", esc(f'#{r.get("rank")} · {"kept" if r.get("kept") == "yes" else "dropped"}') if r else "not ranked yet"),
                 ("elements", f"<ul style='margin:0;padding-left:18px'>{elements}</ul>" if elements else ""),
                 ("Task", _link(d["path"], root, d["name"]))])
    return f'<div class=dz-card><div>{V.as_it_reads(d["message"], d["path"], root)}</div><div>{right}</div></div>'


def _pvo(b: dict, jobs: list, root: Path) -> tuple:
    """Predicted vs observed, one row per tested design: as it reads, its frozen prediction, its Exp arm, and whether
    the direction and the range held; (html, tested)."""
    rows = []
    for j in jobs:
        for d in j["designs"]:
            a = R.arm_of(b, j["id"], d["id"])
            if not a:
                continue
            sc = b["scores"].get((j["id"], d["id"]), {})
            p = d["prediction"] if isinstance(d["prediction"], dict) else {}
            rows.append((_link(d["path"], root, f'{j["id"]} · {d["id"]} {d["short"]}') + V.as_it_reads(d["message"], d["path"], root, small=True),
                         V._pred(p, "cell") + f'<br><span class=mut>frozen {esc(p.get("frozen", "—"))}</span>',
                         esc(a.get("observed", "—")) + f'<br><span class=mut>arm {esc(a.get("arm", ""))} of {esc(a.get("exp", ""))}</span>',
                         V._st(sc.get("direction", "—")), V._st(sc.get("in_range", "—"))))
    return (table(("design", "predicted", "observed", "direction", "in range"), rows) if rows else ""), len(rows)


def _job_next(j: dict) -> tuple:
    """A Job's next move and its state word, in the method's order."""
    from live.design_ladder_act import ready
    if V._approved(j)[0]:                             # released: the close is yours to sign, then it is done
        return ("closed", "done") if _job_closed(j) else ("close the Job", "waiting for you")
    if j["ranking"] and ready(j["path"])[0]:          # a release ready for your sign comes first
        return "review and approve", "waiting for you"
    if str(j["state"]).lower() == "held":
        return "held: " + _plain(j["hold"]).split(".")[0][:80], "held"
    if not (j["goal"] and j["method"] and j["manifest"]):
        return "set up its pins", "next"
    if not (_closed(j["reason"]) and j["ideas"]):
        return "reason ideas (t00)", "running" if j["reason"] and str(j["reason"]["status"]) == "running" else "next"
    if not j["designs"]:
        return "check the fence, open the design Tasks", "next"
    undone = [d for d in j["designs"] if not d["verifies"] or d["verifies"][-1]["status"] != "passed"]
    if undone and d_state(undone[0]) != "dropped":
        return f'{len(undone)} designs to generate, verify or revise', "next"
    if not (_closed(j["rank"]) and j["ranking"]):
        return "review the whole (t99)", "next"
    if ready(j["path"])[0]:
        return "review and approve", "waiting for you"
    return "nothing ready to release", "open"


def _job_closed(j: dict) -> bool:
    """Closed: its face says so, or its run-close Run has closed (a person signed it)."""
    return str(j["state"]).lower() == "closed" or any(r["type"] == "close" and _closed(r) for r in j["runs"])


def d_state(d: dict) -> str:
    return str(d.get("state") or "")


def _goal_name(b: dict, gid: str) -> str:
    g = next((g for g in b["goals"] if g.get("id") == gid), None)
    return C.goal_words(g) if g else (gid or "no goal yet")


def _chain_words(d: dict) -> str:
    """A design's drafts in the order they ran: generate ✅ · verify v1 ✗ · revise ✅ · verify v2 ✅ (each verify
    reads the draft before it; the folders sort by name, so the order is rebuilt from the loop)."""
    mark = lambda r: " ✅" if _closed(r) else " ⏳"
    out = []
    for i, draft in enumerate(d["drafts"]):
        out.append(draft["type"] + mark(draft))
        if i < len(d["verifies"]):
            v = d["verifies"][i]
            out.append(f'verify v{i + 1} ' + ("✅" if v["status"] == "passed" else "✗" if v["status"] == "failed" else "⏳"))
    return " · ".join(out) or "not generated yet"


def _design_state(d: dict) -> str:
    if d_state(d) in ("kept", "released", "dropped"):
        return d_state(d)
    last = d["verifies"][-1] if d["verifies"] else None
    if last and last["status"] == "failed":
        return "revise next"
    if last and last["status"] == "passed":
        return "passed"
    return "verify next" if d["drafts"] else "generate next"


def _section_of(path: Path, heading: str) -> str:
    """The text under a `Heading\\n-----` (or `## Heading`) in a review file, up to the next heading."""
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(rf"(?ms)^(?:##\s+)?{re.escape(heading)}\s*\n(?:-+\s*\n)?(.*?)(?=^\S[^\n]*\n-{{3,}}\s*$|^##\s|\Z)", text)
    return m.group(1).strip() if m else ""


def _md_lines(text: str) -> str:
    """A short Markdown body as paragraphs and bullets, its **bold** and `code` kept as plain words."""
    out, items = [], []
    clean = lambda s: esc(re.sub(r"\*\*|`", "", s))
    for line in text.splitlines():
        if line.startswith("- "):
            items.append(f"<li>{clean(line[2:])}</li>")
            continue
        if items:
            out.append("<ul style='margin:4px 0;padding-left:18px'>" + "".join(items) + "</ul>")
            items = []
        if line.strip():
            out.append(f"<p style='margin:4px 0'>{clean(line)}</p>")
    if items:
        out.append("<ul style='margin:4px 0;padding-left:18px'>" + "".join(items) + "</ul>")
    return "".join(out)


def _fence_verdict(jdir: Path) -> tuple | None:
    """(verdict, steps checked, steps outside) of the newest fence check of run-open-designs-jNN, or None."""
    run = jdir / "runs" / f"run-open-designs-{jdir.name.split('_')[0]}"
    checks = sorted((run / "passes").glob("*/fence-check.md")) if (run / "passes").is_dir() else []
    if not checks:
        return None
    text = checks[-1].read_text(encoding="utf-8", errors="ignore")
    inside = len(re.findall(r"(?m)^- .*:\s*inside\b", text))
    outside = len(re.findall(r"(?m)^- .*:\s*outside\b", text))
    return ("fail" if outside else "pass"), inside + outside, outside


def _coverage_md(j: dict) -> Path | None:
    p = j["rank"]["path"] / "result" / "coverage.md" if j["rank"] else None
    return p if p and p.is_file() else None


def _coverage(j: dict, root: Path) -> str:
    md = _coverage_md(j)
    said = _section_of(md, "Does the kept design cover the goal") if md else ""
    return V._coverage(j) + (_md_lines(said) + f'<p class=mut>{pop(reader(md, root), "coverage.md", "coverage.md ↗")}</p>'
                             if said else "")
