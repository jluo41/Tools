"""The Block's six Spaces (s11): its Description views (Map, Goals, Methods, Inputs), its Jobs, Runs and Delivery
(split from design_views.py, which re-exports every name here)."""
from __future__ import annotations

from pathlib import Path

from live import design_reader as R
from live.frame import Space, delivery_view, esc, pop, rel, table, themes
from live.design_views_parts import GUIDE_METHOD, _kind, _rows, _st, _fold, _pairs, _open, _id, _mins, _job_link, _pred, _cost
from live.design_views_channel import as_read, as_it_reads
from live.design_views_disk import _disk
from live.design_views_report import _questions, _costs, _summary, _rounds, _predicted, _scorecard


# ── Block (s11) ──────────────────────────────────────────────────────────────────────────────
B_SKILLS = {"add-goal": ("haipipe-design-goal",), "setup-rules": ("haipipe-design-goal",), "add-inputs": ("haipipe-design-goal",),
            "add-job": ("haipipe-design",), "propose": ("haipipe-design-method",), "propose-questions": ("haipipe-report",),
            "report": ("haipipe-report", "haipipe-draft"), "add-observed": ("haipipe-design-method",),
            "score": ("haipipe-design-method",), "draw": ("haipipe-studio",), "release": ("haipipe-design-delivery",)}


def _bk(b: dict, root: Path, label: str, rtype: str, prompt: str) -> dict:
    return _kind(label, prompt, *B_SKILLS.get(rtype, ("haipipe-design",)), rows=_rows(b["runs"], root, rtype),
                 level="Block")


def block_spaces(block: Path, root: Path, sub: str, href) -> dict:
    b = R.board(block)
    first, _, rest = (sub or "").partition("/")
    desc = ("Map", "Goals", "Methods", "Inputs")
    d_open = first if first in desc else "Map"
    d_html = {"Map": lambda: _map(b, root, rest, href), "Goals": lambda: _goals(b, href),
              "Methods": lambda: _methods(b, href), "Inputs": lambda: _inputs(b, root, href)}[d_open]()
    d_runs = {"Map": (_bk(b, root, "run-add-job-<jNN>", "add-job", "Launch a Job in {folder}: a signed goal × a registered "
                          "method version × a frozen inputs version; makes the empty jNN_<goal>_<design-method>/ with its pins "
                          "(run-add-job-<jNN>). The Job's own setup Runs set it up."),),
              "Goals": (_bk(b, root, "run-add-goal-<goal>", "add-goal", "Add a goal to {folder}'s goal list (board.md ## Goals): "
                            "aim · who · venue · N · its own rules · leave out; a person signs (run-add-goal-<goal>)."),),
              "Methods": (_bk(b, root, "run-propose-method-<slug>", "propose", "Propose a change to a registered method from {folder}'s "
                              "Jobs (run-propose-method-<slug>); a new version is cut in the design skill's registry, not here."),),
              "Inputs": (_bk(b, root, "run-add-inputs-<vN>", "add-inputs", "Add an inputs version to {folder}: inputs/inputs-vN/ (rules · "
                             "theory · handoff links) and its frozen manifest.yaml (run-add-inputs-<vN>)."),)}[d_open]
    ar = ("Summary", "Rounds", "Questions", "Predicted vs observed", "Method scorecard", "Cost")
    a_open = first if first in ar else "Summary"
    a_html = {"Summary": _summary, "Rounds": _rounds, "Questions": _questions, "Cost": _costs,
              "Predicted vs observed": _predicted, "Method scorecard": _scorecard}[a_open](b, root, href)
    a_runs = {"Summary": (),                 # summary.py builds it with no Run folder: no Run type, no button
              "Rounds": (_bk(b, root, "run-add-inputs-<vN>", "add-inputs", "Add the next inputs version "
                                            "to {folder}: inputs/inputs-vN/ with the last round's Exp results and the insight "
                                            "Board's newer data version, frozen (run-add-inputs-<vN>)."),),
              "Questions": (_bk(b, root, "run-propose-questions", "propose-questions", "Propose {folder}'s report questions "
                                "from the Map, scores.csv and the method scorecard, into board.md ## Questions; another agent "
                                "agrees (run-propose-questions)."),
                            _bk(b, root, "run-report-<qNN>", "report", "Write a Block question's report in "
                                "{folder}/reports/qNN_<topic>/ from the Jobs it names (run-report-<qNN>).")),
              "Cost": (),
              "Predicted vs observed": (_bk(b, root, "run-add-observed-<eNN>", "add-observed", "Add what an Exp returned to "
                                            "{folder}/observed/eNN_<exp>/: per-arm totals, each arm naming jNN · dNN, its source "
                                            "and a frozen manifest; never rows (run-add-observed-<eNN>)."),
                                        _bk(b, root, "run-score-<eNN>", "score", "Score every arm's design of an Exp in "
                                            "{folder}: its frozen prediction against observed/ (direction · in range · error) → "
                                            "runs/run-score-<eNN>/scores.csv (run-score-<eNN>).")),
              "Method scorecard": ()}[a_open]
    goals = tuple(sorted({j["goal"] for j in b["jobs"]}))
    w_open = first if first in goals else "All"
    groups = {"Set up": ("add-goal", "setup-rules", "add-inputs"), "Launch a Job": ("add-job",),
              "Report": ("add-observed", "score", "propose-questions", "report")}
    r_views = ("All",) + tuple(groups)
    r_open = first if first in r_views else "All"
    return {
        "Description": Space(html=d_html, subspaces=desc, open=d_open, run_types=d_runs, page=True,
                             disk=_disk("Block", d_open, block)),
        "Idea Studio": Space(run_types=(_bk(b, root, "Add a topic", "draw", "Add or redraw a studio topic of {folder} with "
                                            "/haipipe-studio: sNN-<topic>/ beside its Jobs (new_topic.py topic); save each "
                                            "working session as a round, sNN-<topic>/passes/pNN-<MMDD>/."),), page=True),
        "Audience Report": Space(html=a_html, subspaces=ar, open=a_open, run_types=a_runs, page=True,
                                 disk=_disk("Block", a_open, block), note="" if a_runs else "No run writes this view: it reads the Jobs' receipts and scores."),
        "Work Details": Space(html=_jobs(b, root, href, w_open), subspaces=("All",) + goals, open=w_open,
                              disk=_disk("Block", "Work Details", block),
                              run_types=(_bk(b, root, "run-add-job-<jNN>", "add-job", "Launch a Job in {folder}: a signed "
                                             "goal × a registered method version × a frozen inputs version (run-add-job-<jNN>)."),),
                              page=True),
        "Runs": Space(html=_block_runs(b, root, groups, r_open), subspaces=r_views, open=r_open, page=True,
                      disk=_disk("Block", "Runs", block),
                      run_types=(_bk(b, root, "run-add-goal-<goal>", "add-goal", "Add a goal to {folder} (run-add-goal-<goal>)."),
                                 _bk(b, root, "run-add-job-<jNN>", "add-job", "Launch a Job in {folder} (run-add-job-<jNN>)."),
                                 _bk(b, root, "run-propose-questions", "propose-questions",
                                     "Propose {folder}'s report questions (run-propose-questions)."))),
        "Delivery": Space(html=delivery_view(block, root, themes()["design"])      # result cards (b10 s32-D18)
                          + "<h3>Released designs</h3>" + _block_delivery(b, href), page=True,
                          disk=_disk("Block", "Delivery", block),
                          run_types=(_kind("run-release-<jNN>", "Release a Job's kept designs into {folder}/delivery/ "
                                           "(the Job's run-release-jNN; a person signs).", "haipipe-design"),)),
    }


def _cells(b: dict) -> tuple:
    """The Map's columns: every registered method (s11), then any method a Job pins that the registry lacks."""
    methods = sorted(R.REGISTRY) if R.REGISTRY else []
    for j in b["jobs"]:
        if j["method"] not in methods:
            methods.append(j["method"])
    cell = {}
    for j in b["jobs"]:
        cell.setdefault((j["goal"], j["method"]), []).append(j)
    return methods, cell


def _map(b: dict, root: Path, rest: str, href) -> str:
    if "~" in rest:
        return _compare(b, rest, href)
    methods, cell = _cells(b)
    goals = [g.get("id") for g in b["goals"] if g.get("signed")] or sorted({j["goal"] for j in b["jobs"]})
    rows, pairs = [], []
    for g in goals:
        row = [f"<b>{esc(g)}</b>"]
        for m in methods:
            chain = cell.get((g, m), [])
            row.append("<br>".join(f'{_job_link(href, j)} <span class=mut>{esc(j["version"])}·{esc(j["inputs"])}</span> '
                                   f'{_st(j["state"])}' for j in chain) or '<span class=mut>· Add a Job</span>')
            pairs += [(a, c) for a, c in zip(chain, chain[1:])]
        rows.append(row)
    heads = ["goal \\ method"] + [f"{m} · {R.METHODS.get(m, ('', ''))[0]}" for m in methods]
    compare = " · ".join(pop(href("Description", f"Map/{a['name']}~{c['name']}"), f"{a['id']} → {c['id']}",
                             f"{a['id']} → {c['id']} ↗") for a, c in pairs)
    return ('<p class=mut>Goals down × registered methods across; each cell is its chain of Jobs, each one clock '
            '(method or inputs) moved from the one above. Two Jobs in one row, different columns, compare methods.</p>'
            + table(heads, rows)
            + (f'<p>Two Jobs in a cell: {compare}</p>' if pairs else ""))


def _compare(b: dict, rest: str, href) -> str:
    a_name, _, c_name = rest.partition("~")
    jobs = {j["name"]: j for j in b["jobs"]}
    a, c = jobs.get(a_name), jobs.get(c_name)
    if not (a and c):
        return '<p class=mut>Pick two Jobs of one Map cell.</p>'
    moved = []
    if (a["method"], a["version"]) != (c["method"], c["version"]):
        moved.append(f"the method, {a['version']} → {c['version']}")
    if a["inputs"] != c["inputs"]:
        moved.append(f"the inputs, {a['inputs']} → {c['inputs']}")
    ca, cc = _cost(a), _cost(c)
    held = "inputs held" if a["inputs"] == c["inputs"] else "method held" if a["version"] == c["version"] else "both moved"
    return (f'<h2>{esc(a["name"])} → {esc(c["name"])} · two Jobs in one Map cell</h2>'
            + _pairs([("what moved", esc(" · ".join(moved) or "nothing") + f" <span class=mut>({esc(held)})</span>"),
                      ("first try", esc(f"{ca['first']} → {cc['first']}")),
                      ("time per passed", esc(f"{_mins(ca['per_passed'])} → {_mins(cc['per_passed'])}")),
                      ("tokens", "—"),
                      ("read from", "each Job's pins and its Performance")]))


def _goals(b: dict, href) -> str:
    out = []
    for g in b["goals"]:
        jobs = [j for j in b["jobs"] if j["goal"] == g.get("id")]
        meta = (f'for {esc(g.get("who", ""))} · {esc(g.get("venue", ""))} · N = {esc(g.get("n", ""))} · '
                + (f'Jobs {esc(" · ".join(j["name"] for j in jobs))} · ' if jobs else "")
                + (_st(g["signed"]) if g.get("signed") else "<span class=st-warn>proposed · not signed</span>"))
        body = _pairs([("aim", esc(g.get("aim", ""))), ("who", esc(g.get("who", ""))), ("venue", esc(g.get("venue", ""))),
                       ("N", esc(f'{g.get("n", "")} designs a Job (N + 5 ideas)')),
                       ("rules", esc(" · ".join(g.get("rules") or []) or "the shared ones only (Inputs)")),
                       ("leave out", esc(g.get("leave-out", "") or "—")),
                       ("Jobs", " · ".join(_job_link(href, j) for j in jobs) or "—"),
                       ("signed", esc(g.get("signed") or "not yet") + " <span class=mut>· once, here; a Job only pins it</span>")])
        out.append(_fold(f'{g.get("id", "")} {g.get("aim", "")}', meta, body, opened=not out, missing=not g.get("signed")))
    return "".join(out) or '<p class=mut>No goal list yet: board.md ## Goals.</p>'


def _methods(b: dict, href) -> str:
    used = {}
    for j in b["jobs"]:
        used.setdefault(j["method"], []).append(j)
    out = []
    for mid in list(used) + [m for m in R.METHODS if m not in used]:
        name, mtype = R.METHODS.get(mid, ("", "—"))
        jobs = used.get(mid, [])
        if not jobs:
            out.append(_fold(f"{mid} · {name}", f"type {esc(mtype)} · no Job here yet"))
            continue
        versions = {}
        for j in jobs:
            versions.setdefault(j["version"], []).append(j)
        body = _pairs([("type", pop(GUIDE_METHOD, f"{mtype} · a method card", f"{mtype} ↗") + " <span class=mut>one of the 13 cards</span>"),
                       ("versions", " · ".join(f'{esc(v)} (' + " · ".join(_job_link(href, x) for x in js) + ")"
                                               for v, js in versions.items())),
                       ("step ① sees", esc((jobs[-1]["method_card"].get("steps") or {}).get("① See input", "—"))),
                       ("runs it", esc(jobs[-1]["method_card"].get("runs-it", "—")))])
        out.append(_fold(f"{mid} · {name}", f'type {esc(mtype)} · {esc(" · ".join(versions))} · Jobs '
                                            f'{esc(" · ".join(j["name"] for j in jobs))}', body, opened=not out))
    return ('<p class=mut>Read only: the registered methods live in the design skill; a proposal from here goes there.</p>'
            + "".join(out))


def _inputs(b: dict, root: Path, href) -> str:
    """Each inputs version as one table: its files down, the Jobs that pin it across (by method), a ✓ where that
    Job's fence holds the file. The version stays the
    Block's, frozen once; each method's step ① picks which of its parts it sees."""
    out = []
    for v in b["inputs"]:
        man = v["manifest"]
        sha = {f.get("path"): f.get("sha256", "") for f in man.get("files", [])}
        jobs = sorted((j for j in b["jobs"] if j["inputs"] == v["id"]), key=lambda j: (j["method"], j["id"]))
        head = "".join(f'<th>{_job_link(href, j, j["method"])} <span class=mut>{esc(j["name"])}</span><br>'
                       f'<span class=mut>{esc(j["method_name"])}</span></th>' for j in jobs)
        rows = []
        for p in man.get("parts", []):
            f = p.get("file", "")
            cells = "".join(f'<td style="text-align:center">{"✓" if f and (j["fence"] / f).exists() else ""}</td>'
                            for j in jobs)
            rows.append(f'<tr><td><span title="sha256 {esc(sha.get(f, ""))}">'
                        f'{_open(v["path"] / f, root, f) if f else "—"}</span></td>{cells}'
                        f'<td class=mut>{esc(p.get("part", ""))} · {esc(p.get("says", ""))}</td></tr>')
        seen = "".join(f'<td style="text-align:center" class=mut>'
                       f'{sum(bool(p.get("file")) and (j["fence"] / p["file"]).exists() for p in man.get("parts", []))}</td>'
                       for j in jobs)
        rows.append(f'<tr><td class=mut>files it sees</td>{seen}<td></td></tr>')
        out.append(f'<p><code>{esc(v["id"])}</code> · frozen {esc(man.get("frozen", "—"))} · rules {esc(man.get("rules", "—"))}'
                   f' · <span class=mut>{esc(man.get("new", ""))}</span></p>'
                   f'<table class=wf-table><thead><tr><th>file</th>{head}<th>what it is</th></tr></thead>'
                   f'<tbody>{"".join(rows)}</tbody></table>')
    return (''.join(out) or '<p class=mut>No inputs version yet: inputs/inputs-vN/.</p>') + (
        '<p class=mut>Each version is frozen once on the Block; a Job\'s fence (its inputs/) holds the files its '
        'method\'s step ① lets it see, and nothing else.</p>')


def _run_state(r: dict | None) -> str:
    """A t00 or t99 tile's state: its Run's own status (running, closed …), "waiting" before the Run exists; a Run that
    exists is not yet closed (j02 of the design example: its reason Run still running, 261108)."""
    return str(r["status"]) if r else "waiting"


def _preview(j: dict, href, root: Path) -> str:
    """An open Job card: a preview of its Tasks (t00 · each design as it reads · t99 · released)."""
    order = {"setup-goal": 0, "setup-method": 1, "setup-inputs": 2}
    setup = " · ".join(f'{_st("✓" if r["status"] == "closed" else r["status"])} <code>{esc(r["run"])}</code>'
                       for r in sorted((r for r in j["runs"] if r["type"] in order), key=lambda r: order[r["type"]]))
    tiles = []
    if j["t00"]:
        tiles.append((f'<a href="{esc(href("", "", j["t00"]))}">{_id("t00", "reason ideas")}</a>',
                      f'② {len(j["topics"])} topics → {len(j["ideas"])} ideas', _st(_run_state(j["reason"]))))
    if j["t99"]:
        kept = sum(r.get("kept") == "yes" for r in j["ranking"])
        tiles.append((f'<a href="{esc(href("", "", j["t99"]))}">{_id("t99", "review whole")}</a>',
                      f'⑤ ranked {len(j["ranking"])} · kept {kept}', _st(_run_state(j["rank"]))))
    if j["delivered"]:
        tiles.append(("released", " · ".join(esc(d.get("design", "")) for d in j["delivered"]) + " → Delivery", _st("released")))
    designs = [(f'<a href="{esc(href("", "", d["path"]))}">{_id(d["name"][:3] + " · " + d["id"])}</a>',
                as_it_reads(d["message"], d["path"], root, small=True), _st(d["state"])) for d in j["designs"][:6]]
    more = len(j["designs"]) - 6
    return ((f'<p class=mut>set up {setup}</p>' if setup else "") + table(("Task", "what it holds", "state"), tiles)
            + '<p class=mut style="margin-top:10px">③ ④ one design each, in order</p>'
            + (table(("design", "as it reads", "state"), designs) if designs else
               f'<p class=mut>Its design Tasks open after t00\'s ideas pass the fence check '
               f'(run-open-designs-{esc(j["id"])}).</p>')
            + (f'<p class=mut>+ {more} more · {_job_link(href, j, "open the Job")}</p>' if more > 0 else ""))


def _jobs(b: dict, root: Path, href, only: str) -> str:
    out, opened = [], False
    for j in b["jobs"]:
        if only not in ("All", j["goal"]):
            continue
        meta = (f'{esc(j["goal"])} · {esc(j["method"])} {esc(j["version"])} · {esc(j["inputs"])} · {esc(j["moved"])} moved · '
                f'{_st(j["state"])}')
        first = not opened and j["state"] == "released"
        opened = opened or first
        out.append(_fold(j["name"], meta, _preview(j, href, root), opened=first, mono=True))
    return (''.join(out) or '<p class=mut>No Job yet.</p>') + (
        '<p class=mut>A card opens in place to its Tasks; a row opens that Task, a Job\'s name its own tab.</p>')


def _block_runs(b: dict, root: Path, groups: dict, view: str) -> str:
    out = ['<p class=mut>Every Block Run is soft: it writes the Block\'s own files; hard Runs sit in a Job\'s Tasks.</p>']
    for g, types in groups.items():
        if view not in ("All", g):
            continue
        rs = [r for r in b["runs"] if r["type"] in types]
        out.append(f"<h2>{esc(g)}</h2>" + ("".join(
            _fold(r["run"], f'{esc(r["kind"])} · {esc(r["target"])} · {_st(r["status"])}',
                  _pairs([("by", esc(r["by"] or "—")), ("time", esc(_mins(r["minutes"]))),
                          ("result", f"<code>{esc(rel(r['result'], root))}</code>")]), mono=True) for r in rs)
            or '<p class=mut>None yet.</p>'))
    return "".join(out)


def _block_delivery(b: dict, href) -> str:
    jobs = {j["id"]: j for j in b["jobs"]}
    cells = []
    for d in b["delivered"]:
        j = jobs.get(d.get("job", ""))
        pins = d.get("pins", {})
        cells.append((_id(d.get("design", ""), pins.get("goal", "")), as_read(d.get("words", ""), R.venue_of(j["path"]) if j else ""),
                      f'{_job_link(href, j) if j else esc(d.get("job", ""))} · {esc(pins.get("method", ""))} · '
                      f'{esc(pins.get("inputs", ""))}',
                      f'{_st("released " + str(d.get("released", "")))} · predicted {_pred(d, "cell")}'))
    return ((table(("design", "as it reads", "Job · method · inputs", "released · predicted"), cells) if cells
             else '<p class=mut>Nothing released yet: delivery/designs.json.</p>')
            + '<p class=mut>→ the Exp (outside the theme); its per-arm result returns into observed/.</p>')
