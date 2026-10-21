"""Is a Job drawing true to its disk? (asked 261019: "How do you evaluate the sNN jNN with /excalidraw-job, do we have
the evaluation?"). check.py judges how a drawing reads; this judges what it claims. A reviewer then reads it as a
newcomer (haipipe-studio ref/reader-review.md).

    python job_check.py <topic folder>

1. Every Task folder and every Run folder of the Job is named on the canvas by its folder name, exactly (JL 261019:
   "we don't need to create the new named"; shared tickets excepted).
2. Every Run card carries a state mark (✅ ❌ 🔶 ⬜ ◌), and a proposed Run is drawn dashed.
3. A failed Run says why (its receipt's `failure:` or the face's sentence).
4. Every percentage the face's words claim (reading, findings, how sure) is found in a result file of the Job, or
   of a Job the face names in `cites:` (paths from the Block), rounded to its shown digits, or as the difference of
   two values in one file (a gain in points).
Exit 1 when any ❌.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import job_drawing as jd  # noqa: E402
import job_ladder as jl  # noqa: E402

jr = jd.jr
PCT = re.compile(r"(?<![\w.])(\d{1,3}(?:\.\d)?)\s?%")
MARKS = "✅❌🔶⬜◌"


def leaves(x, out: list) -> list:
    """Every number inside a JSON or YAML value."""
    if isinstance(x, dict):
        for v in x.values():
            leaves(v, out)
    elif isinstance(x, list):
        for v in x[:200]:
            leaves(v, out)
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        out.append(float(x))
    return out


def result_numbers(job: Path, cites: list[Path] = ()) -> list[set[float]]:
    """Per result file of the Job (and of the Jobs its face `cites:`), the percentages it can support: values,
    values x 100, and differences of two."""
    sets = []
    files = list(job.glob("t*/runs/*/result/*")) + [f for c in cites for f in c.glob("**/runs/*/result/*")]
    for f in files:
        if f.suffix == ".md" and f.is_file():                              # a paper's facts.md and abstract.md: the
            nums = [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", f.read_text()[:200000])]
            sets.append({round(v, 1) for v in nums} | {round(v * 100, 1) for v in nums if abs(v) <= 1.0})
            continue                                                       #   numbers a Discovery Result states
        if f.suffix not in (".json", ".yaml", ".yml", ".csv") or not f.is_file():   # a CSV table too (J22's funnel)
            continue
        try:
            data = json.loads(f.read_text()) if f.suffix == ".json" else jr.load(f)
        except Exception:
            continue
        vals = leaves(data, [])[:400]
        s = set()
        for v in vals:
            s.add(round(v, 1))
            if abs(v) <= 1.0:
                s.add(round(v * 100, 1))
        fr = [v for v in vals if 0 <= v <= 1][:120]
        for i, a in enumerate(fr):
            for b in fr[i + 1:]:
                s.add(round(abs(a - b) * 100, 1))
        sets.append(s)
    return sets


def canvas_texts(topic: Path) -> tuple[str, list[dict]]:
    ex = next(topic.glob("*.excalidraw"))
    els = json.loads(ex.read_text()).get("elements", [])
    text = "\n".join(str(e.get("text") or "") for e in els if e.get("type") == "text" and not e.get("isDeleted"))
    return text, els


def check(topic: Path) -> list[tuple[str, str]]:
    cfg = jd.face_cfg(topic / f"{topic.name}.md")                    # the face's job: yaml, as draw() reads it
    block = topic.parent.parent
    job = block / cfg.get("name", "")
    out: list[tuple[str, str]] = []
    if not job.is_dir():
        return [("❌", f"the face names no Job folder: {cfg.get('name')!r}")]
    text, els = canvas_texts(topic)

    # 1. every Task and Run named
    rows = jr.job_rows(block, job, {})
    for row in rows:
        if row["task"].name not in text:
            out.append(("❌", f"{row['task'].name}: its folder name is not on the canvas"))
        for r in row["runs"]:
            if r["name"] not in text:
                out.append(("❌", f"{row['task'].name}/{r['name']}: no card names it by its folder name"))
    if not any(k == "❌" for k, _ in out):
        n = sum(len(r["runs"]) for r in rows)
        out.append(("✅", f"{len(rows)} Tasks and {n} Runs, each named on the canvas by its folder name"))

    # 2. states and dashed proposals; 3. failures say why
    bad_state, bad_dash, bad_why = [], [], []
    for row in rows:
        for r in row["runs"]:
            kind = jl.card_state(r)
            line = next((ln for ln in text.splitlines() if r["name"][:3] in ln and any(m in ln for m in MARKS)), "")
            if not line:
                bad_state.append(r["name"])
            if kind == "proposed" and not any(e.get("type") == "rectangle" and e.get("strokeStyle") == "dashed"
                                              for e in els):
                bad_dash.append(r["name"])
            if kind == "failed" and not jl.run_why(r, kind) and not jl.run_says(cfg, row["task"].name, r["name"]):
                bad_why.append(r["name"])
    out.append(("❌" if bad_state else "✅", "every Run card carries a state mark" if not bad_state else
                f"no state mark on: {', '.join(bad_state)}"))
    if bad_dash:
        out.append(("❌", f"proposed but not dashed: {', '.join(bad_dash)}"))
    out.append(("❌" if bad_why else "✅", "every failed Run says why" if not bad_why else
                f"failed with no cause on disk or in the face: {', '.join(bad_why)}"))

    # 4. percentages claimed in words are on disk
    words = [str(cfg.get("reading") or ""), str(cfg.get("sure") or "")]
    words += [str((v or {}).get("found") or "") for v in (cfg.get("tasks") or {}).values()]
    claimed = sorted({float(x) for w in words for x in PCT.findall(w)})
    cites = [(block / c).resolve() for c in (cfg.get("cites") or [])]   # numbers quoted from another Job
    sets = result_numbers(job, [c for c in cites if c.is_dir()])
    missing = [c for c in claimed if not any(c in s or round(c) in s for s in sets)]
    if claimed:
        out.append(("❌" if missing else "✅", f"{len(claimed) - len(missing)} of {len(claimed)} percentages in the "
                    "words are in a result file" + (f"; not found: {', '.join(f'{m:g} %' for m in missing)}"
                                                     if missing else "")))
    return out


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        print("usage: job_check.py <topic folder>   (a Studio topic: its face and its .excalidraw)")
        return 0 if len(sys.argv) == 2 else 2
    topic = Path(sys.argv[1]).resolve()
    res = check(topic)
    for k, s in res:
        print(f"{k} {s}")
    return 1 if any(k == "❌" for k, _ in res) else 0


if __name__ == "__main__":
    sys.exit(main())
