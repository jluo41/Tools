"""What each Space shows at an insight Job: its Question Book release, its data version, its Runs and what it
delivers."""

from __future__ import annotations

from pathlib import Path

from live import insight_plan_c as P
from live.frame import Space, delivery_view, esc, rel, table, themes
from live.insight_view_board import _version
from live.insight_view_overall import OVERALL, _executive, _overall
from live.insight_view_parts import (
    LEVELS, PERIODS, _kind, _next_line, _carded, _rows, _fold, _chip, _open, second_row, split, _where,
    _part_names, _part_key, _runs_table, _band)
from live.insight_view_work import (
    _cut_table, _job_current, _vs_previous, WORK_STEPS, STEP_KEY, _work_facts, _work_step, _work_view,
    _work_kinds)


# ── a Job ───────────────────────────────────────────────────────────────────────────────────────
def job_spaces(jdir: Path, root: Path, sub: str, href) -> dict:
    block = P.job_board(jdir)
    b = P.board(block)
    j = P.job(jdir)
    proto = b["prototype"]
    r = P.release(proto, j["release"])
    band = _band(j, b)
    desc = ("Question Book", "Dataset")
    d_open = sub if sub in desc else "Question Book"
    # no band beside the tab (s12, 261007): the Job's line opens Description › Question Book only
    d_html = (band + _job_prototype(j, r, root)) if d_open == "Question Book" else _job_dataset(j, b, r, root)
    parts = ((OVERALL,) if _executive(j) else ()) + _part_names(r["partitions"])
    a_part, a_period = split(sub, parts, PERIODS)
    prev = j["previous"][:3]
    a_html = _overall(j, b, r, root) if a_part == OVERALL else second_row(
        href, "Audience Report", a_part, PERIODS, a_period, "Period") + (
        _job_current(j, b, r, root, _part_key(a_part)) if a_period == "Current" else _vs_previous(j, root))
    me = j["name"][:3]
    propose = _kind("Propose questions", f"Propose questions from {me} (run-propose-{me}): file each new or changed "
                    "question, and each gap this Job could not answer, to the Question Book's proposals/<slug>.md (kind · "
                    f"DIKW level · from {me} · why). It writes nothing else.", rows=_rows(j["runs"], root, "propose"))
    a_runs = ((_kind("Write the overall report", "Write the Overall Report of {folder} (run-overall-<jNN>): each Executive "
                     "question's page from the answers below it, then its one page (ref/overall_report.py)."),
               _kind("Check a report", "Check an Executive question's page in {folder} (run-check-<tNN>).", run="run-check-<tNN>"))
              if a_part == OVERALL else
              (_kind("Compare with " + prev, f"Compare this Job with {prev} (run-compare-{prev}): it writes "
                     f"reports/vs-{prev}.md, after every check.", rows=_rows(j["runs"], root, "compare")), propose)
              if a_period == "vs previous" and prev else (propose,) if a_period == "vs previous" else
              (_kind("Pool or split", "Run the Cross test of a question in {folder} (rNN_cross): one test of the "
                     "difference."),) if _part_key(a_part) == "cross" else
              (_kind("Write a report", "Write a question's page in {folder}: a part per segment."),
               _kind("Check a report", "Check a question's page in {folder} (run-check-<tNN>).", run="run-check-<tNN>")))
    wf = _work_facts(j)
    w_open = _work_step(sub, j, wf)
    r_views = ("All", "hard", "soft", "launch", "power", "compare", "propose", "close")
    r_open = sub if sub in r_views else "All"
    hard = [x for t in j["tasks"] for x in t["hard"]]
    own = (_kind("Run the Job", "Run the Job {folder} (run-launch): start every Task's hard Runs, one per segment.",
                 rows=_rows(j["runs"], root, "launch")),
           _kind("Run a segment", "Run one question on one segment in {folder} (rNN_<segment>).",
                 rows=_rows(hard, root, "hard")))
    return _carded({
        "Description": Space(html=d_html, subspaces=desc, open=d_open, page=True,   # Dataset: no run, as s12 draws it
                             run_types=(_kind("Open the release ↗", f"Open the release {rel(r['job'], root) if r['job'] else j['release']}: "
                                              "read only here; it is changed in the Question Book Block."),) if d_open == "Question Book" else ()),
        "Audience Report": Space(html=a_html, subspaces=parts, open=a_part, run_types=a_runs),
        "Work Details": Space(html=_work_view(j, b, r, wf, w_open, jdir, root, href), subspaces=WORK_STEPS, open=w_open,
                              run_types=_work_kinds(j, wf, root)),
        "Runs": Space(html=_next_line(jdir) + _job_runs(j, root, r_open), subspaces=r_views, open=r_open,
                      run_types=own + ((_kind("Compare with " + prev, f"Compare this Job with {prev} (run-compare-{prev}).",
                                              rows=_rows(j["runs"], root, "compare")),) if prev else ())
                      + (propose, _kind("Close the Job", "Close the Job {folder} after its checks and the comparison (run-close): frozen.",
                               rows=_rows(j["runs"], root, "close")),)),
        "Idea Studio": Space(run_types=(_kind("Add a topic", "Add or redraw a studio topic of {folder} (no Run: a pass in sNN-<topic>/passes/pNN-<MMDD>/): sNN-<topic>/, a pass per session."),)),
        # page=True: the frame takes this Space's runs and third row as set, even none (frame.lays_out_page)
        "Delivery": Space(html=delivery_view(jdir, root, themes()["insight"]) + _job_delivery(j, b, root),
                          run_types=(), page=True,
                          note="Nothing to run here: the Board's Delivery holds the handoff; the Overall Report's one "
                               "page is printed by haipipe-insight ref/overall_report.py."),
    }, "Job", {"Audience Report": "overall-report" if a_part == OVERALL else "cross" if _part_key(a_part) == "cross" else a_period,
               "Work Details": STEP_KEY[w_open],
               "Runs": r_open},
        {"j<NN>": me, "j<prev>": prev or "j<prev>"},
        keep=lambda c: c["label"] != "Compare with the Job before" or bool(prev))


def _job_prototype(j: dict, r: dict, root: Path) -> str:
    rows = {}
    for t in j["tasks"]:
        q = r["questions"].get(t["qid"], {})
        rows.setdefault(t["qid"][:1], []).append(
            (f'<b>{esc(t["qid"])}</b>', _open(q.get("file"), root, t["qid"], q.get("question") or "<question>"),
             esc(q.get("change") or "—"), " ".join(_chip(f"{k}: {v}") for k, v in (q.get("method") or {}).items())))
    body = "".join(_fold(f"{lv} · {name}", f"{len(rows[lv])}", table(("#", "question", "in this release", "methods"), rows[lv]),
                         opened=True) for lv, name, _ in LEVELS if rows.get(lv))
    defs = [(f'<b>{esc(p.get("name", ""))}</b>', f'<code>{esc(_where(p))}</code>',
             esc(p.get("why", ""))) for p in r["partitions"]]
    power = (r["thresholds"].get("power") or {})
    compare = r["thresholds"].get("compare")
    code = [d for d in ("src", "configs") if r["job"] and (r["job"] / d).is_dir()]
    return (f'<p class=mut>{esc(r.get("label") or r["name"])}: {esc(rel(r["job"], root)) if r["job"] else "—"} (read only).</p>' + body
            + _fold("the segments, as defined in the release", f"{len(defs)}", table(("partition", "where", "why"), defs))
            + f'<p class=mut>Power floor: {esc(power.get("smallest_effect_pp", "—"))} pp · compare rule: '
              f'{esc(compare) if compare else "not set (still open)"} · shared code: {esc(", ".join(code) or "none")}</p>')


def _job_dataset(j: dict, b: dict, r: dict, root: Path | None = None) -> str:
    v = next((v for v in b["versions"] if v.get("version") == j["data"]), {"version": j["data"]})
    return ((_version(v, root) if root else "")
            + "<p class=mut>Each segment on this version, checked before any outcome (run-power):</p>" + _cut_table(j))


def _job_runs(j: dict, root: Path, view: str) -> str:
    own = [r for r in j["runs"] if view in ("All", "soft") or r.get("type") == view]
    below = [r for t in j["tasks"] for r in t["hard"] + t["soft"] if view in ("All",) or r.get("kind") == view]
    order = ("Add a Job (Board) → run-launch → run-power → per Task: rNN_&lt;segment&gt; → rNN_cross → run-write → "
             "run-check → run-compare-&lt;prev&gt; (after the checks) → run-propose-&lt;job&gt; (reads the compare) → "
             "run-close (frozen)")
    out = [f"<p class=mut>{order}</p>"]
    if own:
        out.append(_fold("the Job's own · soft", f"{len(own)}", _runs_table(own, root), opened=True))
    if below and view in ("All", "hard", "soft"):
        out.append(_fold("its Tasks'", f"{len(below)}", _runs_table(below, root), opened=view != "All"))
    return "".join(out)


def _job_delivery(j: dict, b: dict, root: Path | None = None) -> str:
    """The Job's part of the Board's delivery/ (its Overall Report on one page), then where its counsel goes."""
    part = b["path"] / "delivery" / j["name"]
    files = sorted(f for f in part.iterdir() if f.is_file()) if part.is_dir() else []
    links = "".join(f'<li><a href="/{esc(rel(f, root))}" target=_blank rel=noopener>{esc(f.name)} ↗</a></li>'
                    for f in files) if root else ""
    out = (f'<p><b>Overall Report</b>: its {len(_executive(j))} Executive answers on one page.</p>'
           f'<ul class=files>{links}</ul>' if files else
           '<p class=mut>No one-page Overall Report yet: ref/overall_report.py prints it from the Executive answers.</p>'
           if _executive(j) else "")
    latest = b["jobs"][-1]["name"] if b["jobs"] else ""
    if any(t["qid"][:1] == "W" for t in j["tasks"]) and j["name"] == latest:
        return out + "<p>This is the latest Job: its Wisdom counsel goes to Board › Delivery › Handoff, naming this Job.</p>"
    return out or "<p class=mut>None of its own: a Job's answers are read by the Board.</p>"
