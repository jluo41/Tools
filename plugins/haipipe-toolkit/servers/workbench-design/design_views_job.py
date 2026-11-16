"""A Job's six Spaces (s12): its setup, Audience Report, Work Details, Runs and the Review and approve panel
(split from design_views.py, which re-exports every name here)."""
from __future__ import annotations

import re
from pathlib import Path

from live import design_reader as R
from live.frame import Space, delivery_view, esc, pop, rel, table, themes
from live.design_views_parts import GUIDE_METHOD, _kind, _rows, _st, _fold, _pairs, _open, _ideas_text, _id, _test, _qrow, _qhead, _mins, _live, _pred
from live.design_views_channel import as_read, as_it_reads
from live.design_views_disk import _disk


# ── Job (s12) ────────────────────────────────────────────────────────────────────────────────
J_SKILLS = {"setup-goal": ("haipipe-design-goal",), "setup-method": ("haipipe-design-method",), "setup-inputs": ("haipipe-design-goal",),
            "open-designs": ("haipipe-design",), "reason": ("haipipe-design-unit",), "generate": ("haipipe-design-unit",),
            "verify": ("haipipe-design-unit",), "revise": ("haipipe-design-unit",), "rank": ("haipipe-design-unit",),
            "freeze-predictions": ("haipipe-design-delivery",), "release": ("haipipe-design-delivery",),
            "close": ("haipipe-design-workflow",),
            "draw": ("haipipe-studio",)}


def _task_runs(j: dict) -> list:
    return [r for d in j["designs"] for r in d["runs"]]


def job_spaces(jdir: Path, root: Path, sub: str, href) -> dict:
    j = R.job(jdir)
    b = R.board(R.block_of(jdir.parent) or jdir.parent, with_jobs=False)
    jid = j["id"]

    def k(label, rtype, prompt, rows=None):
        return _kind(label, prompt, *J_SKILLS.get(rtype, ("haipipe-design",)),
                     rows=rows if rows is not None else _rows(j["runs"], root, rtype), level="Job")

    desc = ("Goal", "Method", "Inputs")
    d_open = sub if sub in desc else "Goal"
    setup = {v: k(f"run-setup-{v.lower()}-{jid}", f"setup-{v.lower()}", f"Set up {{folder}}'s {v.lower()} "
                  f"(run-setup-{v.lower()}-{jid}): " + {"Goal": "pin a signed goal from the Block's goal list.",
                                                         "Method": "link the registered method's card into inputs/method.md.",
                                                         "Inputs": "build inputs/ (relative links into one inputs version) "
                                                                   "and freeze its manifest.yaml."}[v]) for v in desc}
    d_runs = (setup["Goal"], k(f"run-close-{jid}", "close", "Close {folder} once its designs are released; frozen.")) \
        if d_open == "Goal" else (setup[d_open],)
    d_html = _setup_strip(j) + {"Goal": _job_goal, "Method": lambda *a: _job_method(*a, href=href), "Inputs": _job_inputs}[d_open](j, b, root)
    reason = k("run-reason-t00", "reason", "Reason ideas for {folder} (② run-reason-t00): from inputs/ only, topic by topic, "
               "to N + 5 ideas, each naming its source.", rows=_rows(R.runs(j["t00"]), root) if j["t00"] else [])
    gen = k("run-generate-dNN", "generate", "Generate one design from its idea in a design Task of {folder} "
            "(③ run-generate-dNN), from inputs/ only.", rows=_rows(_task_runs(j), root, "generate"))
    ver = k("run-verify-dNN-v1", "verify", "Verify one design of {folder} (④ run-verify-dNN-v<k>) in a fresh context, "
            "by another agent: T0 rules · T1 every source in the manifest.", rows=_rows(_task_runs(j), root, "verify"))
    rev = k("run-revise-dNN", "revise", "Revise a design of {folder} that failed its review (run-revise-dNN), then "
            "verify again.", rows=_rows(_task_runs(j), root, "revise"))
    rank = k("run-rank-t99", "rank", "Review the whole of {folder} (⑤ run-rank-t99): rank the N + 5, keep the top N, "
             "each with its predicted outcome; another agent.", rows=_rows(R.runs(j["t99"]), root) if j["t99"] else [])
    approve = dict(k(f"run-release-{jid}", "release", f"Review and approve {{folder}}: read each kept design as it reads, "
                     f"its prediction and why, and its review; one sign freezes the predictions (run-freeze-predictions-{jid}) "
                     f"and releases the designs (run-release-{jid}).", rows=_rows(j["runs"], root, "freeze-predictions", "release")),
                   doing="review and approve: one sign freezes the predictions and releases the designs")
    opend = k(f"run-open-designs-{jid}", "open-designs", f"Open one design Task per idea in {{folder}} (run-open-designs-{jid}).")
    ar = ("Reason ideas", "Design display", "Review whole", "Predicted vs observed", "Performance")
    a_open = sub if sub in ar else "Reason ideas"
    a_html = {"Reason ideas": _reason_ideas, "Design display": _display, "Review whole": _review_whole,
              "Predicted vs observed": _job_observed, "Performance": _performance}[a_open](j, b, root, href)
    a_runs = {"Reason ideas": (reason,), "Design display": (gen, ver), "Review whole": (rank,),
              "Predicted vs observed": (approve,), "Performance": (approve,)}[a_open]
    wd = ("Reason ideas", "Conduct & review", "Review whole")     # one casing, as the Audience Report's (b03, 261008)
    w_open = sub if sub in wd else "Reason ideas"
    w_html = {"Reason ideas": _wd_reason, "Conduct & review": _wd_conduct, "Review whole": _wd_whole}[w_open](j, root, href)
    w_runs = {"Reason ideas": (reason, opend), "Conduct & review": (gen, ver, rev), "Review whole": (rank,)}[w_open]
    rv = ("Setup", "Reason ideas", "Conduct & review", "Review whole")
    r_open = sub if sub in rv else "Setup"
    r_runs = {"Setup": (setup["Goal"], setup["Method"], setup["Inputs"], opend), "Reason ideas": (reason,),
              "Conduct & review": (gen, ver, rev), "Review whole": (rank, approve)}[r_open]
    dv = ("designs.md", "designs.json")
    v_open = sub if sub in dv else "designs.md"
    return {
        "Description": Space(html=d_html, subspaces=desc, open=d_open, run_types=d_runs, page=True,
                             disk=_disk("Job", d_open, jdir)),
        "Idea Studio": Space(run_types=(k("Add a topic", "draw", "Add or redraw a studio topic of {folder} with "
                                          "/haipipe-studio: sNN-<topic>/ beside its Tasks (new_topic.py topic); save each "
                                          "working session as a round, sNN-<topic>/passes/pNN-<MMDD>/."),), page=True),
        "Audience Report": Space(html=a_html, subspaces=ar, open=a_open, run_types=a_runs, page=True,
                                 disk=_disk("Job", a_open, jdir)),
        "Work Details": Space(html=w_html, subspaces=wd, open=w_open, run_types=w_runs, page=True,
                              disk=_disk("Job", "WD " + w_open, jdir)),
        "Runs": Space(html=_job_runs(j, root, r_open), subspaces=rv, open=r_open, run_types=r_runs, page=True,
                      disk=_disk("Job", r_open if r_open == "Setup" else "Runs " + r_open, jdir)),
        "Delivery": Space(html=_approve_panel(j, jdir, root) + delivery_view(jdir, root, themes()["design"])
                          + _job_delivery(j, root, v_open),
                          subspaces=dv, open=v_open, run_types=(approve,), page=True,
                          disk=_disk("Job", v_open, jdir)),
    }


def _setup_strip(j: dict) -> str:
    order = {"setup-goal": 0, "setup-method": 1, "setup-inputs": 2}
    rs = sorted((r for r in j["runs"] if r["type"] in order), key=lambda r: order[r["type"]])
    return (f'<p class=mut>{" · ".join(_st("✓") + " <code>" + esc(r["run"]) + "</code>" for r in rs if r["status"] == "closed")}'
            f'</p>')


def _md_body(path: Path) -> str:
    """A Markdown file's text after its front matter and title."""
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if text.startswith("---"):
        text = text.split("\n---", 1)[-1].split("\n", 1)[-1]
    return "\n".join(l for l in text.splitlines() if not l.startswith("# ")).strip()


def _bullets(path: Path, heading: str) -> list:
    """The `- ` lines under `## <heading>` in a Markdown file."""
    if not path.is_file():
        return []
    m = re.search(rf"(?ms)^## {re.escape(heading)}[ \t]*\n(.*?)(?=^## |\Z)", path.read_text(encoding="utf-8", errors="ignore"))
    return [l[2:].strip() for l in (m.group(1) if m else "").splitlines() if l.startswith("- ")]


def _keyed(path: Path) -> dict:
    """`key: value` lines before a file's first `##` (a fence goal.md)."""
    if not path.is_file():
        return {}
    head = path.read_text(encoding="utf-8", errors="ignore").split("\n## ", 1)[0]
    return {k.strip(): v.strip() for k, v in re.findall(r"(?m)^([a-z][a-z -]*):\s*(.+)$", head)}


def _ul(items: list) -> str:
    return "<ul style='margin:0;padding-left:18px'>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def _job_goal(j: dict, b: dict, root: Path) -> str:
    """What the Job pins, read from its fence: inputs/goal.md (the goal as the design work sees it) and
    inputs/rules.md (the Block's signed shared rules), one flush row each."""
    g = next((x for x in b["goals"] if x.get("id") == j["goal"]), {})
    goal_md, rules_md = j["fence"] / "goal.md", j["fence"] / "rules.md"
    seen = _keyed(goal_md)
    own = [r for r in _bullets(goal_md, "Rules for this goal") if not r.startswith("(")]
    shared, leave = _bullets(rules_md, "Rules"), _bullets(rules_md, "Leave out")
    rk = _keyed(rules_md)
    files = [f["name"] for f in j["files"] if f["name"] not in ("goal.md", "method.md", "rules.md")]
    leave_goal = seen.get("leave out") or g.get("leave-out", "")
    return _pairs([
        ("aim", esc(f'{j["goal"]} · {seen.get("aim") or g.get("aim", "")}')),
        ("who", esc(seen.get("who") or g.get("who", "—"))),
        ("venue", esc(seen.get("venue") or g.get("venue", "—"))),
        ("N", esc(f'{seen.get("n") or j["n"]} designs, from N + 5 ideas')),
        ("rules", (_ul(own) if own else "")
         + (f'<p class=mut style="margin:0">shared rules {esc(rk.get("rules", ""))} · signed {esc(rk.get("signed", "—"))}</p>'
            + _ul(shared) if shared else '<span class=mut>no rules.md in the fence</span>')),
        ("leave out", (_ul([leave_goal]) if leave_goal else "") + (_ul(leave) if leave else "")),
        ("may draw on", " · ".join(_open(j["fence"] / f, root, f) for f in files) or "<span class=mut>the goal and rules only</span>"),
        ("signed", esc(g.get("signed") or "—") + " <span class=mut>in the Block's goal list</span>"),
        ("read from", _open(goal_md, root, "inputs/goal.md") + " · " + _open(rules_md, root, "inputs/rules.md"))])


def _job_method(j: dict, b: dict, root: Path, href=None) -> str:
    """The pinned method, one flush row per step: what this version says, and what it did in this Job, so no step of the method
    is left out."""
    card = j["method_card"]
    steps = card.get("steps") or {}
    designs = j["designs"]
    kept = sum(r.get("kept") == "yes" for r in j["ranking"])
    revised = sum(1 for d in designs if len(d["drafts"]) > 1)
    task = lambda t, text: f'<a href="{esc(href("", "", t))}">{esc(text)}</a>' if (t and href) else esc(text)
    seen = [f["name"] for f in j["files"] if f["name"] not in ("goal.md", "method.md")]
    here = {"①": "sees " + (" · ".join(seen) or "—"),
            "②": (task(j["t00"], f'{len(j["topics"])} topics → {len(j["ideas"])} ideas') if j["reason"] else "not reasoned yet"),
            "③": f'{len(designs)} designs · {revised} revised' if designs else "no design yet",
            "④": "each design's verdict is on its row" if designs else "—",
            "⑤": (task(j["t99"], f'ranked {len(j["ranking"])} · kept {kept}') if j["ranking"] else "not ranked yet")}
    rows = [(f"<b>{esc(st)}</b>", esc(choice), here.get(st[:1], "")) for st, choice in steps.items()]
    rows += [("<b>runs it</b>", esc(card.get("runs-it", "—")), ""), ("<b>loops</b>", esc(card.get("loops", "—")), "")]
    reg = R.REGISTRY.get(j["method"], {})
    about = _md_body(reg["path"] / "method.md").split("\n\n")[0] if reg.get("path") else ""
    note = _md_body(j["fence"] / "method.md")
    head = (f'<p><b>{esc(j["method"])} · {esc(j["method_name"])} · {esc(j["version"])}</b> '
            f'<span class=mut>· type {pop(GUIDE_METHOD, j["type"] + " · a method card", j["type"] + " ↗")} · '
            f'pinned {_open(j["fence"] / "method.md", root, "inputs/method.md")} · {esc(j["sha"])}</span></p>'
            + (f'<p>{esc(about)}</p>' if about else ""))
    return (head + (table(("step", f'{j["version"]} says', f'in {j["name"]}'), rows) if steps
                    else '<p class=mut>No steps in inputs/method.md yet.</p>')
            + "".join(f'<p class=mut>{esc(p)}</p>' for p in note.split("\n\n") if p.strip()))


def _job_inputs(j: dict, b: dict, root: Path, fold: bool = True) -> str:
    man = j["manifest"]
    files = {f["name"].rstrip("/"): f for f in j["files"]}
    sha = {f.get("path"): f.get("sha256", "") for f in man.get("files", [])}
    rows = [("<span class=mut>the method (how)</span>", _id(j["method"], j["version"]),
             _file_cell(j, "method.md", files, sha, root))]
    for p in man.get("parts", []):
        rows.append((f"<span class=mut>{esc(p.get('part', ''))}</span>", esc(p.get("choice", "")),
                     _file_cell(j, p.get("file", ""), files, sha, root) if p.get("file") else "<span class=mut>—</span>"))
    return (f'<p><code>{esc(j["name"])}/inputs/</code> <span class=mut>· the fence: Generate and Verify see these and '
            f'nothing else</span></p>' + table(("① See input · part", f'{j["method"]}\'s choice', "in inputs/"), rows)
            + (_fold("manifest.yaml", f'every file above, its source and sha256 · frozen {esc(man.get("frozen", "—"))} = '
                                      f'{esc(man.get("inputs", j["inputs"]))}', mono=True) if fold else
               f'<p class=mut><code>manifest.yaml</code> · every file above, its source and sha256 · frozen '
               f'{esc(man.get("frozen", "—"))} = {esc(man.get("inputs", j["inputs"]))}</p>'))


def _file_cell(j: dict, name: str, files: dict, sha: dict, root: Path) -> str:
    f = files.get(name)
    if not f:
        return f'<code>{esc(name)}</code> <span class=st-warn>missing</span>'
    link = f' <span class=mut>→ {esc(f["link"])}</span>' if f["link"] else ""
    bad = " <span class=st-warn>broken link</span>" if f["broken"] else ""
    return _open(j["fence"] / name, root, name, name) + link + f' <span class=mut>{esc(sha.get(name, ""))}</span>' + bad


def _reason_ideas(j: dict, b: dict, root: Path, href) -> str:
    out, words = [], _ideas_text(j)
    for t in j["topics"]:
        steps = t.get("steps") or []
        chain = (_id(t.get("from", "")) + " → "
                 + " → ".join(f'{esc(s.get("says", ""))} <span class=mut>so</span> {esc(s.get("so", ""))}' for s in steps)
                 + " → " + " · ".join(_id(i, words.get(str(i), "")) for i in t.get("ideas", [])))
        out.append(_fold(f'{t.get("title", "") or t.get("id", "")}',
                         f'&nbsp;· {len(steps)} steps → {len(t.get("ideas", []))} idea{"" if len(t.get("ideas", [])) == 1 else "s"} · from {esc(str(t.get("from", "")).split(" · ")[0])}',
                         f"<p>{chain}</p>", opened=not out))
    return ("".join(out) or '<p class=mut>Nothing reasoned yet.</p>')


def _display(j: dict, b: dict, root: Path, href) -> str:
    rank = {r.get("design"): r for r in j["ranking"]}
    rows = [_qhead("Design", "Process (③): its idea, each element's source", "Review (④) · expected outcome")]
    # every design a full card, in order; the dropped ones after them,
    # in one fold that opens to their full cards
    dropped = [d for d in j["designs"] if d["state"] == "dropped"]
    rows += [_card(d, j, href, root) for d in j["designs"] if d["state"] != "dropped"]
    if dropped:
        why = lambda d: f'rank #{rank[d["id"]].get("rank")}' if d["id"] in rank else "not ranked"
        rows.append(_fold("Dropped, kept for the record",
                          esc(" · ".join(f'{d["id"]} ({why(d)})' for d in dropped)),
                          "".join(_card(d, j, href, root) for d in dropped)))
    return "".join(rows)


def _card(d: dict, j: dict, href, root: Path) -> str:
    """One design, as the Job shows it: the design as it reads │ its process (③) │ its review (④ ⑤)."""
    r = {x.get("design"): x for x in j["ranking"]}.get(d["id"], {})
    tests = d["verifies"][-1]["card"].get("tests", {}) if d["verifies"] else {}
    return _qrow(f'<b><a href="{esc(href("", "", d["path"]))}">{esc(d["id"])} · {esc(d["short"])}</a></b>'
                 + as_it_reads(d["message"], d["path"], root),
                          f'<p class=mut>from idea {esc(d["idea"])} · ③ {esc(d["drafts"][0]["run"]) if d["drafts"] else "—"} · '
                          f'{len(d["drafts"])} draft(s)</p>'
                          # each element's source, folded until opened
                          + (f'<details class=q-more><summary>› Elements and sources</summary>'
                             + "".join(f'<p>{esc(e.get("words", ""))} <span class=mut>← {esc(e.get("from", ""))}</span></p>'
                                       for e in d["elements"]) + '</details>' if d["elements"] else ""),
                          f'<p>④ {" · ".join(f"{_test(t)} {esc(v)}" for t, v in tests.items()) or "—"} · {_st(d["state"])}</p>'
                          f'<p>expected {_pred(d["prediction"], "fold")}</p>'
                          + (f'<p class=mut>⑤ rank #{esc(r.get("rank"))} · {"kept" if r.get("kept") == "yes" else "dropped"}</p>' if r else ""))


def _review_whole(j: dict, b: dict, root: Path, href) -> str:
    rows = [(esc(r.get("rank", "")), f'<code>{esc(r.get("design", ""))}</code>', esc(r.get("predicted", "")),
             esc(r.get("why", "")), _st("kept") if r.get("kept") == "yes" else "<span class=mut>dropped</span>") for r in j["ranking"]]
    return (table(("rank", "design", "predicted", "why", "kept"), rows)
            + _pairs([("ranked by", "predicted outcome, by the ④ ⑤ reviewer (another agent)"),
                      ("keeps", esc("the top N of N + 5"))])) if rows else \
        '<p class=mut>t99 has not ranked yet.</p>'


def _job_observed(j: dict, b: dict, root: Path, href) -> str:
    rows = [_qhead("Design", "Predicted · frozen at release", "Observed · the Block's observed/ and scores")]
    for d in j["designs"]:
        a = R.arm_of(b, j["id"], d["id"])
        if not a:
            continue
        s = b["scores"].get((j["id"], d["id"]), {})
        rows.append(_qrow(f'<b>{esc(d["id"])}</b>' + as_it_reads(d["message"], d["path"], root),
                          f'{_pred(d["prediction"])}<p class=mut>frozen {esc(d["prediction"].get("frozen", "—"))}</p>',
                          f'{esc(a.get("observed", "—"))} <span class=mut>· arm {esc(a.get("arm", ""))} of {esc(a.get("exp", ""))}</span>'
                          f'<p>direction {_st(s.get("direction", "—"))} · in range {_st(s.get("in_range", "—"))}</p>'))
    if len(rows) == 1:
        return '<p class=mut>None of this Job\'s designs is in an Exp yet (the Block\'s observed/).</p>'
    return "".join(rows)


def _performance(j: dict, b: dict, root: Path, href) -> str:
    rows = []
    for d in _live(j["designs"]):
        mins = [r["minutes"] for r in d["runs"] if r["minutes"] is not None]
        rows.append((f'<code>{esc(d["id"])}</code>', "—", esc(_mins(sum(mins)) if mins else "—"), esc(len(d["drafts"])),
                     esc(f'{len(d["message"])} ch'), _pred(d["prediction"], "cell"),
                     _st(d["prediction"].get("frozen", "—"))))
    return (table(("design", "tokens", "time", "rounds", "length", "predicted", "frozen"), rows)
            + '<p class=mut>tokens: — until usage: is in the Run receipt; a prediction is frozen at release.</p>')


def _wd_reason(j: dict, root: Path, href) -> str:
    if not j["t00"]:
        return '<p class=mut>No t00 yet.</p>'
    r = j["reason"]
    return _fold("t00 · reason ideas", f'② {len(j["topics"])} topics → {len(j["ideas"])} ideas · {_st(r["status"] if r else "waiting")}',
                 _pairs([("its Run", esc(f'{r["run"]} · hard · {r["status"]} · {r["by"]}') if r else "—"),
                         ("result", "chains.yaml · ideas.yaml · topics.md"),
                         ("opens", f'<a href="{esc(href("", "", j["t00"]))}">the Task</a>')]), opened=True, mono=True)


def _wd_conduct(j: dict, root: Path, href) -> str:
    out = []
    for d in j["designs"]:
        line = f'{esc(d["idea"])} · {_st(d["state"])} · {len(d["drafts"])} draft(s)'
        if d["state"] == "dropped":
            out.append(_fold(f'{d["name"][:3]} · {d["id"]}', "dropped by t99 · " + line, mono=True))
            continue
        body = _pairs([(r["run"], esc(f'{r["status"]} · {r["by"]}')) for r in d["runs"]]
                      + [("design", as_read(d["message"], R.venue_of(d["path"]), small=True)), ("opens", f'<a href="{esc(href("", "", d["path"]))}">the Task</a>')])
        out.append(_fold(f'{d["name"][:3]} · {d["id"]}', line, body, opened=not out, mono=True))
    return '<p class=mut>One Task per design, in order; one Task, two Runs: generate · verify.</p>' + "".join(out)


def _wd_whole(j: dict, root: Path, href) -> str:
    if not j["t99"]:
        return '<p class=mut>No t99 yet.</p>'
    r = j["rank"]
    kept = sum(x.get("kept") == "yes" for x in j["ranking"])
    return _fold("t99 · review whole", f'⑤ ranked {len(j["ranking"])} · kept {kept} · {_st(r["status"] if r else "waiting")}',
                 _pairs([("its Run", esc(f'{r["run"]} · hard · {r["status"]} · {r["by"]}') if r else "—"),
                         ("result", "ranking.csv: rank · design · predicted · why · kept"),
                         ("opens", f'<a href="{esc(href("", "", j["t99"]))}">the Task</a>')]), opened=True, mono=True)


def _job_runs(j: dict, root: Path, view: str) -> str:
    if view == "Setup":
        rs = [(r, "") for r in j["runs"] if r["type"] in ("setup-goal", "setup-method", "setup-inputs", "open-designs")]
    elif view == "Reason ideas":
        rs = [(r, "t00_reason-ideas/") for r in (R.runs(j["t00"]) if j["t00"] else [])]
    elif view == "Review whole":
        rs = [(r, "t99_review-whole/") for r in (R.runs(j["t99"]) if j["t99"] else [])]
        rs += [(r, "") for r in j["runs"] if r["type"] in ("freeze-predictions", "release")]
    else:                                        # Conduct & review: one row per design Task, its Runs folded under it
        return "".join(_fold(d["name"], f'{len(d["runs"])} Runs · {_st(d["state"])}',
                             table(("Run", "kind", "by", "state"),
                                   [(f'<code>runs/{esc(r["run"])}/</code>', esc(r["kind"]), esc(r["by"] or "—"), _st(r["status"]))
                                    for r in d["runs"]]), mono=True) for d in j["designs"]) or '<p class=mut>No design Task yet.</p>'
    return table(("Run", "kind", "by", "state"),
                 [(f'<code>{esc(pre)}runs/{esc(r["run"])}/</code>', esc(r["kind"]), esc(r["by"] or "—"), _st(r["status"]))
                  for r, pre in rs])


def _approve_panel(j: dict, jdir: Path, root: Path, head: bool = True) -> str:
    """🙋 Review and approve, by a person on the screen: each kept design as it reads with its prediction and why, as release.py's own dry run would
    release it today, then one tick and one sign (POST /_board/design-ladder-act, design_ladder_act.py). A refusal says
    why, in release.py's words; a released Job says who signed and when, from its run-release card."""
    import json
    from live.design_ladder_act import ready
    done = next((r for r in j["runs"] if r["type"] == "release" and r["status"] == "closed"), None)
    designs, why = ready(jdir)
    head = '<h3 style="margin:0 0 6px">🙋 Review and approve</h3>' if head else ""     # the focus page's Process names it
    if done and not designs:
        return (head + f'<p><span class="st st-ok">✓ released</span> {esc(str(done["card"].get("signed") or ""))}</p>')
    if not designs:
        if str(j.get("state")) == "held" and j.get("hold"):      # a held Job says why it is held, not what is missing
            first = re.split(r"(?<=\.)\s", re.sub(r"^held:\s*", "", str(j["hold"]).strip(), flags=re.I), maxsplit=1)[0]
            why = "held: " + first.rstrip(".")
        return head + f'<p><button type=button class=work-act disabled>Approve the release</button> <span class=mut>not ready: {esc(why)}</span></p>'
    venue = R.venue_of(jdir)
    rows = [(_id(d["design"], d.get("name", "")), as_read(d["words"], venue, small=True), _pred(d, "cell")) for d in designs]
    body = esc(json.dumps({"action": "approve", "job": rel(jdir, root)}))
    return (head + table(("design", "as it reads", "predicted"), rows)
            + f'<p class=sign-row><label><input type=checkbox name=attest> I read each kept design as it reads, its '
              f'prediction and why</label> <button type=button class=work-act data-post="/_board/design-ladder-act" '
              f'data-body="{body}" data-fields="attest">Approve the release</button> <span class=mut>one sign: '
              f'freezes the {len(designs)} predictions and releases the designs</span></p>')


def _job_delivery(j: dict, root: Path, view: str) -> str:
    path = j["delivery"] / view
    if not path.is_file():
        return f'<p class=mut>Nothing released yet: delivery/{esc(view)} is written by run-release-{esc(j["id"])}.</p>'
    text = path.read_text(encoding="utf-8", errors="ignore")
    if view == "designs.md":
        return (table(("design", "as it reads", "predicted"), [(_id(d.get("design", "")), as_read(d.get("words", ""), R.venue_of(j["path"])),
                                                                 _pred(d, "cell")) for d in j["delivered"]])
                + f'<p class=mut>{_open(path, root, "designs.md", rel(path, root) + " ↗")}: for people, written from designs.json</p>')
    return f'<p class=mut>delivery/designs.json · what the experiment platform reads</p><pre>{esc(text)}</pre>'
