"""The design theme's ladder views: what each Space shows at the Block, a Job and a Task (b12 s11 · s12 · s13).

Drawn from the folders (design_reader.py) in the base's look only: .topic folds, .wf-table, the q-row
three-column cards, .st-ok / .st-warn, the frame's tab row (.row.subs .tab); no tags: an id is mono text, its words after
it (b03 s32-D09). A design is shown as it reads, the theme's own element (b12 s32): an SMS as one bubble on a phone, its
{LINK} where the platform puts it; a UI design as its rendered screen (its Task's screens/ PNG).
Every Space is laid out here (`page=True`), so its views and run types are exactly the design's. A Runs-panel
entry is named as its Run is, run-<type>-<target> (hard or soft, JL 261007), and carries its run card's skill, agent,
sign and prompt (haipipe-design-workflow/references/run-cards.md, `<Level> › <Space>`); a Run with no card keeps
the prompt written here. Read-only: a run type only copies its prompt.

What the design leaves open (b12 s11 · s12 · s13, red) is drawn as nothing or "—": tokens while a Run receipt has
no `usage:`. The method registry is read by design_reader (haipipe-design-method/methods/).
"""
from __future__ import annotations

import re
from pathlib import Path

from host_paths import skill_dir
from live import design_reader as R
from live.frame import Space, esc, pop, reader, rel, table

GUIDE_METHOD = "/_board/guide?family=design&view=method"
OK = ("passed", "closed", "released", "answered", "ok", "kept", "yes", "✓", "✅")
WARN = ("verify", "revise", "open", "failed", "waiting", "draft")


# ── the run cards (b12 s21, JL 261007: each Run's skill, agent, sign and prompt live on its card) ────────────
CARDS = skill_dir("haipipe-design-workflow") / "references" / "run-cards.md"
_CARD_LINE = re.compile(r"^🔘 BUTTON\s+(.+?) · (Block|Job|Task) › (.+?) · (\^run-\S+)(?: · views (.+))?$")
_ALIAS = {}                                     # older spellings of a Run, mapped to its card (none left, 261007)
_cache: dict = {}


def ladder_cards(path: Path = CARDS) -> list:
    """The ladder's run cards: [{label, level, space, pattern, views, skill, agent, signs, prompt}], in file order.
    The older board's cards (one-word Spaces) never match a `<Level> › <Space>` line, so they are left out."""
    try:
        stamp = path.stat().st_mtime
    except OSError:
        return []
    if _cache.get("stamp") == (path, stamp):
        return _cache["cards"]
    out, card = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = _CARD_LINE.match(line)
        if m:
            card = {"label": m.group(1), "level": m.group(2), "space": m.group(3), "pattern": m.group(4),
                    "views": (m.group(5) or "").split(), "skill": "", "agent": "", "signs": "", "prompt": ""}
            out.append(card)
        elif line.startswith("🔘 BUTTON") or line.startswith("## "):
            card = None
        elif card is not None:
            for mark, key in (("🧩 SKILL", "skill"), ("🤖 AGENT", "agent"), ("✍️ SIGNS", "signs"), ("💬 PROMPT", "prompt")):
                if line.startswith(mark):
                    card[key] = line[len(mark):].strip()
    _cache.update(stamp=(path, stamp), cards=out)
    return out


def card_for(label: str, level: str | None = None) -> dict | None:
    """The run card of a Runs-panel entry named as its Run (run-<type>-<target>), its own level's first."""
    name = re.sub(r"^(\?\s*)?t(?:00|NN|99|\d\d) › ", "", label.strip())
    name = _ALIAS.get(name, name).replace("run-freeze-prediction-", "run-freeze-predictions-")
    sample = re.sub(r"<[^>]+>", "x01", name)
    found = [c for c in ladder_cards() if re.match(c["pattern"], sample)]
    return next((c for c in found if c["level"] == level), found[0] if found else None)


# ── small parts in the base's look ───────────────────────────────────────────────────────────
def _kind(label: str, prompt: str, *skills: str, rows=(), level: str | None = None) -> dict:
    """A Runs-panel entry, named as its Run; its card (if any) gives the skill, the agent, the sign and the prompt."""
    card = card_for(label, level)
    if card:
        prompt = card["prompt"]
        if card["agent"] and card["agent"] != "none":
            prompt = f'Run with {card["agent"]}. {prompt}'
        if card["signs"] and card["signs"] != "none":
            prompt += f' I sign {card["signs"]}.'
        skills = (card["skill"],) if card["skill"] else skills
    return {"label": label, "prompt": prompt, "skills": list(skills), "rows": list(rows)}


def _rows(rs: list, root: Path, *types: str) -> list:
    return [{"run_id": r["run"], "status": r["status"], "target": r["target"], "result": rel(r["result"], root)}
            for r in rs if not types or r["type"] in types]


def _st(state) -> str:
    s = str(state if state not in (None, "") else "—")
    low = s.lower()
    cls = "st-ok" if any(low.startswith(o) for o in OK) else "st-warn" if any(low.startswith(w) for w in WARN) else "mut"
    return f"<span class={cls}>{esc(s)}</span>"


def _fold(title: str, meta: str, body: str = "", opened: bool = False, missing: bool = False, mono: bool = False) -> str:
    t = f"<code>{esc(title)}</code>" if mono else esc(title)
    inner = f'<div style="padding:8px 14px">{body}</div>' if body else ""
    return (f'<details class="topic{" missing" if missing else ""}"{" open" if opened else ""}><summary><b>{t}</b>'
            f'<span class=topic-meta>{meta}</span></summary>{inner}</details>')


def _pairs(rows) -> str:
    return table(("", ""), [(f"<span class=mut>{esc(k)}</span>", v) for k, v in rows])


def _open(path: Path, root: Path, label: str, text: str = "") -> str:
    return pop(reader(path, root), label, text or label) if path.exists() else esc(text or label)


def phone(message: str, small: bool = False) -> str:
    """An SMS as the reader sees it: one bubble on a phone, the {LINK} where the platform puts it."""
    body = esc(message or "—").replace("{LINK}", '<span style="color:var(--acc);text-decoration:underline">{LINK}</span>')
    w, f = ("190px", "12.5px") if small else ("280px", "14.5px")
    return (f'<div style="border:1px solid var(--line);border-radius:18px;padding:10px 10px 14px;margin:4px 0;'
            f'max-width:{w};background:var(--bg)"><div class=mut style="text-align:center;font-size:11px;margin-bottom:8px">'
            f'Text message</div><div style="background:var(--acc-soft);border-radius:16px 16px 16px 4px;padding:7px 10px;'
            f'font-size:{f};white-space:pre-wrap;word-break:break-word">{body}</div></div>')


def screen_of(task: Path | None, root: Path) -> Path | None:
    """A UI design's rendered screen: the first PNG in its Task's screens/ (render_screen.py writes it), or None."""
    shots = sorted((task / "screens").glob("*.png")) if task and (task / "screens").is_dir() else []
    return shots[0] if shots else None


def as_it_reads(message: str, task: Path | None, root: Path, small: bool = False) -> str:
    """A design as its reader sees it: a UI design's screen (its screens/ PNG), else the SMS on a phone (b03, 261008)."""
    png = screen_of(task, root)
    if png is None:
        return phone(message, small)
    w = "190px" if small else "280px"
    return (f'<a href="/{esc(rel(png, root))}" target=_blank rel=noopener>'
            f'<img loading=lazy alt="{esc(png.stem)}" src="/{esc(rel(png, root))}" style="max-width:{w};border:1px solid var(--line)"></a>')


def _ideas_text(j: dict) -> dict:
    return {str(i.get("id", "")): str(i.get("idea", "")) for i in j["ideas"]}


def _id(value: str, words: str = "") -> str:
    """An id as plain text: mono, its words after it (no chip; b03 s32-D09)."""
    return f"<code>{esc(value)}</code>" + (f" {esc(words)}" if words else "")


# the review's checks by their Guide names (guide/method.md: T0 Rules · T1 Fidelity · T2 Critique · T3 Pretest · T4 Exp);
# the T-number only on hover, since "T0" reads as a ticket (JL 261008: "we might want short full name")
TESTS = {"T0": "rules", "T1": "fidelity", "T2": "critique", "T3": "pretest", "T4": "Exp"}


def _test(t: str) -> str:
    return f'<span title="{esc(t)}">{esc(TESTS.get(str(t), str(t)))}</span>'


def _qrow(a: str, b: str, c: str) -> str:
    return f"<div class=q-row><div>{a}</div><div>{b}</div><div>{c}</div></div>"


def _qhead(a: str, b: str, c: str) -> str:
    return f"<div class='q-row q-head-row'><div>{esc(a)}</div><div>{esc(b)}</div><div>{esc(c)}</div></div>"


def _mins(v) -> str:
    return "—" if v is None else f"{v:.0f} min"


def _job_link(href, j: dict, label: str = "") -> str:
    return f'<a href="{esc(href("", "", j["path"]))}">{esc(label or j["name"])}</a>'


def _live(designs: list) -> list:
    return [d for d in designs if d["state"] != "dropped"]


def _passed(designs: list) -> list:
    return [d for d in designs if d["state"] in ("passed", "released")]


def _cost(j: dict) -> dict:
    """What a Job spent: every Run of the Job and its Tasks (generate, verify, revise, t00, t99)."""
    rs = list(j["runs"]) + [r for d in j["designs"] for r in d["runs"]]
    rs += [r for t in (j["t00"], j["t99"]) if t for r in R.runs(t)]
    live = _live(j["designs"])
    mins = [r["minutes"] for r in rs if r["minutes"] is not None]
    toks = [r["tokens"] for r in rs if r["tokens"] is not None]
    n = max(len(live), 1)
    passed = len(_passed(live))
    return {"minutes": sum(mins), "per_design": sum(mins) / n if mins else None,
            "tokens": f"{sum(toks) / n / 1000:.0f}k" if toks else "—",
            "rounds": sum(len(d["drafts"]) for d in live) / n, "first": sum(d["first_try"] for d in live),
            "n": len(live), "passed": passed, "per_passed": sum(mins) / passed if mins and passed else None}



# ── Disk: the files behind each view, under the open folder (the frame's Disk box, folded with the Runs; the "on
# disk" tree under each screen of s11 · s12 · s13). "{face}" is the open folder's face.
J = "j[0-9]*_*/"
DISK = {
    "Block": {
        "Map": (("board.md", "## Goals: the rows"), (J, "each Job: its face pins goal · method · inputs")),
        "Goals": (("board.md", "## Goals: one card per goal, signed once here"), (J + "inputs/goal.md", "a Job's copy (run-setup-goal-jNN)")),
        "Methods": ((J + "inputs/method.md", "each Job's pinned method (the registry is the skill's)"),),
        "Inputs": (("inputs/i*/", "the inputs versions"), ("inputs/i*/manifest.yaml", "each file's sha256, frozen"),
                   (J + "inputs/manifest.yaml", "each Job's fence")),
        "Questions": (("board.md", "## Questions: one row each"), ("reports/q*/q*.md", "Report: its title and opening"),
                      (J, "Task Work: the Jobs a question names")),
        "Cost": ((J + "runs/*/run.yaml", "started_at · finished_at · usage"), (J + "t*_*/runs/*/run.yaml", "each Task's Runs")),
        "Predicted vs observed": (("observed/e*/arms.csv", "observed: per-arm totals, each arm names jNN · dNN"),
                                  ("runs/run-score-*/scores.csv", "each arm's design scored"),
                                  (J + "t*_d*/prediction.yaml", "predicted: frozen at release")),
        "Method scorecard": (("runs/run-score-*/scores.csv", "summed per method version"), (J, "each Job's method pin")),
        "Work Details": ((J, "one card per Job"), (J + "t00_*/", "t00 · reason ideas"), (J + "t*_d*/", "one design each"),
                         (J + "t99_*/", "t99 · review whole")),
        "Runs": (("runs/*/", "the Block's Runs, every one soft"),),
        "Delivery": (("delivery/designs.json", "every released design, every Job"), ("delivery/designs.md", "for people"),
                     ("delivery/screens/", "a UI design's screens")),
    },
    "Job": {
        "Goal": (("{face}", "goal: the pin"), ("inputs/goal.md", "the goal as the design work sees it"),
                 ("runs/run-setup-goal-*/", "pins it (signed once, at the Block)")),
        "Method": (("inputs/method.md", "the pinned method: its five steps"), ("runs/run-setup-method-*/", "links it in")),
        "Inputs": (("inputs/", "the fence: the only folder the design work sees"), ("inputs/manifest.yaml", "each file's source and sha256"),
                   ("runs/run-setup-inputs-*/", "builds it")),
        "Reason ideas": (("t00_*/runs/r*_reason_*/result/chains.yaml", "each topic's chain"),
                         ("t00_*/runs/r*_reason_*/result/ideas.yaml", "the ideas")),
        "Design display": (("t*_d*/", "one card per design"), ("t*_d*/elements.yaml", "its process"), ("t*_d*/runs/*/", "generate · verify")),
        "Review whole": (("t99_*/runs/r*_rank_*/result/ranking.csv", "rank the N + 5, keep N"),),
        "Predicted vs observed": (("t*_d*/prediction.yaml", "frozen at release"), ("../observed/", "the Block's: what the Exp returned"),
                                  ("../runs/", "the Block's run-score-eNN")),
        "Performance": (("runs/*/run.yaml", "the Job's Runs: time"), ("t*_d*/runs/*/run.yaml", "each design's Runs"),
                        ("t*_d*/prediction.yaml", "predicted")),
        "WD Reason ideas": (("t00_*/", "step ②: the ideas"),),
        "WD Conduct & review": (("t*_d*/", "steps ③ ④: one design each"),),
        "WD Review whole": (("t99_*/", "step ⑤: the ranking"),),
        "Setup": (("runs/run-setup-*/", "goal · method · inputs"), ("runs/run-open-designs-*/", "opens one Task per idea")),
        "Runs Reason ideas": (("t00_*/runs/*/", "hard: reason"),),
        "Runs Conduct & review": (("t*_d*/runs/*/", "generate · verify · revise"),),
        "Runs Review whole": (("t99_*/runs/*/", "hard: rank"), ("runs/run-freeze-predictions-*/", "a person signs"),
                              ("runs/run-release-*/", "a person signs")),
        "designs.md": (("delivery/designs.md", "for people, written from designs.json"),),
        "designs.json": (("delivery/designs.json", "for machines: one entry per design, its pins"),),
    },
    "t00": {"Task": (("{face}", "state"), ("runs/r*_reason_*/", "the reasoning Run")),
            "Topics": (("runs/r*_reason_*/result/chains.yaml", "each topic's chain"),),
            "Ideas": (("runs/r*_reason_*/result/ideas.yaml", "the ideas, each with its design"),),
            "Chains": (("runs/r*_reason_*/result/chains.yaml", "a row per step"),),
            "Runs": (("runs/*/", "hard: reason"),),
            "Delivery": (("runs/r*_reason_*/result/ideas.yaml", "handed to the Job"),)},
    "design": {"Design": (("{face}", "## Design: the message"), ("elements.yaml", "its process"), ("prediction.yaml", "expected")),
               "Evaluation": (("runs/r*_verify_*/", "④ review, another agent"),),
               "Tests": (("runs/r*_verify_*/run.yaml", "each test's result"),),
               "Drafts": (("runs/r*_generate_*/result/design.md", "draft 1"), ("runs/run-revise-*/result/design.md", "later drafts")),
               "Performance": (("runs/*/run.yaml", "time"), ("prediction.yaml", "predicted"), ("../../observed/", "the Block's: the Exp")),
               "Elements": (("elements.yaml", "words · from · because · step"),),
               "Runs": (("runs/*/", "generate · verify · revise"),),
               "Delivery": (("../delivery/designs.json", "released with the Job"),)},
    "t99": {"Task": (("{face}", "state"), ("runs/r*_rank_*/", "the ranking Run")),
            "Ranking": (("runs/r*_rank_*/result/ranking.csv", "rank · design · predicted · why · kept"),),
            "Coverage": (("runs/r*_rank_*/result/ranking.csv", "the kept N"),),
            "Kept · Dropped": (("runs/r*_rank_*/result/ranking.csv", "kept or dropped"),),
            "Runs": (("runs/*/", "hard: rank"),),
            "Delivery": (("runs/r*_rank_*/result/ranking.csv", "handed to the Job's release"),)},
}


def _disk(level: str, view: str, folder: Path) -> tuple:
    return tuple((p.replace("{face}", folder.name + ".md"), m) for p, m in DISK.get(level, {}).get(view, ()))


# ── Block (s11) ──────────────────────────────────────────────────────────────────────────────
B_SKILLS = {"add-goal": ("haipipe-design-goal",), "setup-rules": ("haipipe-design-goal",), "add-inputs": ("haipipe-design-goal",),
            "add-job": ("haipipe-design",), "propose": ("haipipe-design-method",), "propose-questions": ("haipipe-question",),
            "report": ("haipipe-question", "haipipe-page"), "add-observed": ("haipipe-design-method",),
            "score": ("haipipe-design-method",), "draw": ("workbench-studio",), "release": ("haipipe-design-delivery",)}


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
              "Inputs": (_bk(b, root, "run-add-inputs-<iN>", "add-inputs", "Add an inputs version to {folder}: inputs/iN/ (rules · "
                             "theory · handoff links) and its frozen manifest.yaml (run-add-inputs-<iN>)."),)}[d_open]
    ar = ("Questions", "Cost", "Predicted vs observed", "Method scorecard")
    a_open = first if first in ar else "Questions"
    a_html = {"Questions": _questions, "Cost": _costs, "Predicted vs observed": _predicted,
              "Method scorecard": _scorecard}[a_open](b, root, href)
    a_runs = {"Questions": (_bk(b, root, "run-propose-questions", "propose-questions", "Propose {folder}'s report questions "
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
        "Idea Studio": Space(run_types=(_bk(b, root, "run-draw-<sNN>", "draw", "Draw a studio topic of {folder}: "
                                            "studio/sNN-<topic>/ and its builder (run-draw-<sNN>)."),), page=True),
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
        "Delivery": Space(html=_block_delivery(b, href), page=True, disk=_disk("Block", "Delivery", block),
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
            row.append("<br>".join(f'{_job_link(href, j, j["id"])} <span class=mut>{esc(j["version"])}·{esc(j["inputs"])}</span> '
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
    return (f'<h2>{esc(a["id"])} → {esc(c["id"])} · two Jobs in one Map cell</h2>'
            + _pairs([("what moved", esc(" · ".join(moved) or "nothing") + f" <span class=mut>({esc(held)})</span>"),
                      ("passed", esc(f"{ca['passed']} → {cc['passed']} of {cc['n']}")),
                      ("first try", esc(f"{ca['first']} → {cc['first']}")),
                      ("time per passed", esc(f"{_mins(ca['per_passed'])} → {_mins(cc['per_passed'])}")),
                      ("tokens", "—"),
                      ("read from", "each Job's pins and its Performance")]))


def _goals(b: dict, href) -> str:
    out = []
    for g in b["goals"]:
        jobs = [j for j in b["jobs"] if j["goal"] == g.get("id")]
        meta = (f'for {esc(g.get("who", ""))} · {esc(g.get("venue", ""))} · N = {esc(g.get("n", ""))} · '
                + (f'Jobs {esc(" ".join(j["id"] for j in jobs))} · ' if jobs else "")
                + (_st(g["signed"]) if g.get("signed") else "<span class=st-warn>proposed · not signed</span>"))
        body = _pairs([("aim", esc(g.get("aim", ""))), ("who", esc(g.get("who", ""))), ("venue", esc(g.get("venue", ""))),
                       ("N", esc(f'{g.get("n", "")} designs a Job (N + 5 ideas)')),
                       ("rules", esc(" · ".join(g.get("rules") or []) or "the shared ones only (Inputs)")),
                       ("leave out", esc(g.get("leave-out", "") or "—")),
                       ("Jobs", " ".join(_job_link(href, j, j["id"]) for j in jobs) or "—"),
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
        rate = " · ".join(f'{v}: {len(_passed(sum((x["designs"] for x in js), [])))} passed' for v, js in versions.items())
        body = _pairs([("type", pop(GUIDE_METHOD, f"{mtype} · a method card", f"{mtype} ↗") + " <span class=mut>one of the 13 cards</span>"),
                       ("versions", " · ".join(f'{esc(v)} (' + " ".join(_job_link(href, x, x["id"]) for x in js) + ")"
                                               for v, js in versions.items())),
                       ("step ① sees", esc((jobs[-1]["method_card"].get("steps") or {}).get("① See input", "—"))),
                       ("runs it", esc(jobs[-1]["method_card"].get("runs-it", "—"))),
                       ("scorecard", esc(rate))])
        out.append(_fold(f"{mid} · {name}", f'type {esc(mtype)} · {esc(" · ".join(versions))} · Jobs '
                                            f'{esc(" ".join(j["id"] for j in jobs))}', body, opened=not out))
    return ('<p class=mut>Read only: the registered methods live in the design skill; a proposal from here goes there.</p>'
            + "".join(out))


def _inputs(b: dict, root: Path, href) -> str:
    """Each inputs version as one table: its files down, the Jobs that pin it across (by method), a ✓ where that
    Job's fence holds the file (JL 261008: "the input is associated with the method"). The version stays the
    Block's, frozen once; each method's step ① picks which of its parts it sees."""
    out = []
    for v in b["inputs"]:
        man = v["manifest"]
        sha = {f.get("path"): f.get("sha256", "") for f in man.get("files", [])}
        jobs = sorted((j for j in b["jobs"] if j["inputs"] == v["id"]), key=lambda j: (j["method"], j["id"]))
        head = "".join(f'<th>{_job_link(href, j, j["method"])} <span class=mut>{esc(j["id"])}</span><br>'
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
    return (''.join(out) or '<p class=mut>No inputs version yet: inputs/iN/.</p>') + (
        '<p class=mut>Each version is frozen once on the Block; a Job\'s fence (its inputs/) holds the files its '
        'method\'s step ① lets it see, and nothing else.</p>')


# a Block question as a row (JL 261007: "I want this style for the Question Work Report", the paper and insight rows):
# Question (pill, mark, its title, the question, More) │ Task Work (the Jobs it rests on, numbered) │ Report (pill, status,
# title, its opening)
_MARK = {"answered": "✅", "partial": "🟡", "open": "🟡"}
_WORD = {"answered": "Answered", "partial": "Partly answered", "open": "Not answered yet"}


def _pill(text: str) -> str:
    return f'<span class="item-kind">{esc(text)}</span>'


def _report_side(q: dict, b: dict, root: Path) -> str:
    rep = b["path"] / str(q.get("report", "")).rstrip("/") if q.get("report") else None
    page = next(iter(sorted(rep.glob("*.md"))), None) if rep and rep.is_dir() else None
    status = str(q.get("answer-status", "open"))
    if page is None:
        return f'<p>{_pill("Report")} <span class=mut>{esc(_WORD.get(status, status))}</span></p><p class=mut>No report yet</p>'
    text = page.read_text(encoding="utf-8", errors="ignore")
    head = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), page.stem)
    opening = next((p.strip() for p in text.split("\n\n")[1:] if p.strip() and not p.lstrip().startswith(("#", "---"))), "")
    return (f'<p>{_pill("Report")} <span class=mut>{esc(_WORD.get(status, status))}</span></p>'
            f'<p class=rp-title><b>{pop(reader(page, root), head, head + " ↗")}</b></p>'
            + (f'<p class=rp-text>{esc(opening)}</p>' if opening else "")
            + f'<p class=mut>report {esc(page.stem.split("_")[0])}</p>')


def _task_work(q: dict, b: dict, root: Path, href) -> str:
    jobs = {j["id"]: j for j in b["jobs"]}
    ev = [jobs[e] for e in q.get("evidence", []) if e in jobs]
    items = []
    for j in ev:
        live = _live(j["designs"])
        tested = [d["id"] for d in j["designs"] if (j["id"], d["id"]) in b["scores"]]
        gives = (f'{len(_passed(live))} of {len(live)} passed'
                 + (f' · {", ".join(tested)} tested' if tested else ""))
        outs = [x for x in ("ranking.csv" if j["ranking"] else "", "scores.csv" if tested else "") if x]
        items.append(f'<li><b>{_job_link(href, j, j["id"])}</b> · {esc(j["goal"])} × {esc(j["method"])} {esc(j["version"])} × '
                     f'{esc(j["inputs"])} · {esc(gives)}'
                     + (f' <span class=mut>→ {esc(" · ".join(outs))}</span>' if outs else "") + "</li>")
    tree = "".join(f'<div style="padding-left:22px"><code>{esc(j["id"])}</code> {esc(j["name"][4:])} '
                   f'<span class=mut>▸ {len(j["designs"])} designs · {_st(j["state"])}</span></div>' for j in ev)
    return (f'<p>{_pill("Task Work")} <span class=mut>{len(items)} Job{"" if len(items) == 1 else "s"}</span></p>'
            + (f'<ol>{"".join(items)}</ol>' if items else '<p class=mut>No Job named yet</p>')
            + (f'<div class=mut style="margin-top:8px"><code>{esc(b["path"].name.split("_")[0])}</code> '
               f'{esc(b["path"].name.split("_", 1)[-1])}{tree}</div>' if ev else ""))


def _questions(b: dict, root: Path, href) -> str:
    rows = [_qhead("Question", "Task Work", "Report")]
    for n, q in enumerate(b["questions"], 1):
        status = str(q.get("answer-status", "open"))
        more = [f'<li><b>asks</b> · {esc(q["asks"])}</li>'] if q.get("asks") else []
        more += [f'<li><b>evidence</b> · {esc(" · ".join(q.get("evidence", [])))}</li>',
                 '<li><b>asked by</b> · run-propose-questions, agreed by another agent</li>']
        left = (f'<p>{_pill(f"Question {n}")} {_MARK.get(status, "⬜")}</p><p><b>{esc(q.get("title", ""))}</b></p>'
                + (f'<p>{esc(q["asks"])}</p>' if q.get("asks") and q["asks"] != q.get("title") else "")
                +                 f'<details><summary class=mut>More</summary><ul>{"".join(more)}</ul></details>')
        rows.append(f'<div class=q-row id="question-{esc(q.get("id", ""))}"><div class=q-l>{left}</div>'
                    f'<div class=q-w>{_task_work(q, b, root, href)}</div><div class=q-r>{_report_side(q, b, root)}</div></div>')
    if len(rows) == 1:
        return '<p class=mut>No Block question yet: board.md ## Questions (run-propose-questions).</p>'
    return ('<p class=mut>A Block question needs evidence from two or more Jobs; one Job\'s is the Job\'s.</p>' + "".join(rows))


def _costs(b: dict, root: Path, href) -> str:
    out = []
    for j in sorted(b["jobs"], key=lambda x: x["state"] != "released"):
        c = _cost(j)
        body = _pairs([("tokens / design", f'{esc(c["tokens"])} <span class=mut>(usage: not in the Run receipt yet)</span>'),
                       ("time / design", esc(_mins(c["per_design"]))), ("rounds", esc(f'{c["rounds"]:.1f} drafts a design')),
                       ("first try", esc(f'{c["first"]} of {c["n"]} passed on draft 1')),
                       ("per passed", esc(_mins(c["per_passed"]))), ("read from", "each Run's started_at → finished_at")])
        out.append(_fold(j["id"], f'{esc(j["method"])} {esc(j["version"])} · {esc(j["inputs"])} · {esc(_mins(c["per_design"]))} '
                                  f'a design · {c["first"]} of {c["n"]} first try', body, opened=not out, mono=True))
    return "".join(out) or '<p class=mut>No Job yet.</p>'


def _predicted(b: dict, root: Path, href) -> str:
    jobs = {j["id"]: j for j in b["jobs"]}
    rows = [_qhead("Design", "Predicted · frozen at release", "Observed · the Exp, its arm")]
    tested = []
    for e in b["observed"]:
        for a in e["arms"]:
            j, did = jobs.get(a.get("job", "")), a.get("design", "")
            d = next((x for x in j["designs"] if x["id"] == did), None) if j else None
            if not d:
                continue
            tested.append(d["path"])
            p, s = d["prediction"], b["scores"].get((j["id"], did), {})
            rows.append(_qrow(f'<b>{_job_link(href, j, j["id"])} · <a href="{esc(href("", "", d["path"]))}">{esc(did)}</a></b>'
                              + phone(d["message"]),
                              f'{esc(p.get("predicted", "—"))} <span class=mut>against {esc(p.get("against", "the control"))}</span>'
                              f'<p class=mut>by {esc(p.get("by", "—"))} · frozen {esc(p.get("frozen", "—"))}</p>'
                              f'<p class=mut>{esc(j["method"])} {esc(j["version"])} · {esc(j["inputs"])}</p>',
                              f'{esc(a.get("observed", "—"))} <span class=mut>· arm {esc(a.get("arm", ""))} of {esc(e["id"])}</span>'
                              f'<p>direction {_st(s.get("direction", "—"))} · in range {_st(s.get("in_range", "—"))}</p>'
                              f'<p class=mut>{esc(s.get("run", ""))} · totals per arm, never rows</p>'))
    if len(rows) == 1:
        return '<p class=mut>No Exp result yet: observed/eNN_<exp>/ is filled by run-add-observed-<eNN>.</p>'
    return "".join(rows)


def _scorecard(b: dict, root: Path, href) -> str:
    groups = {}
    for j in b["jobs"]:
        groups.setdefault((j["method"], j["version"]), []).append(j)
    out = []
    for (m, v), js in groups.items():
        live = sum((_live(j["designs"]) for j in js), [])
        scores = [s for (jid, _), s in b["scores"].items() if jid in {j["id"] for j in js}]
        hit = sum(s.get("direction") == "✓" for s in scores)
        inr = sum(s.get("in_range") == "✓" for s in scores)
        rate = f'{100 * len(_passed(live)) // max(len(live), 1)}%'
        body = _pairs([("Jobs", " ".join(_job_link(href, j, j["id"]) for j in js)), ("pass rate", esc(rate)),
                       ("first try", esc(f'{sum(d["first_try"] for d in live)} of {len(live)}')),
                       ("tested", esc(f"{len(scores)} designs")), ("direction", esc(f"{hit} of {len(scores)}")),
                       ("in range", esc(f"{inr} of {len(scores)}")), ("tokens per passed", "—")])
        out.append(_fold(f"{m} {v}", f'{esc(" · ".join(j["id"] for j in js))} · pass {esc(rate)} · predictions '
                                     f'{inr} of {len(scores)} in range', body, opened=not out, mono=True))
    return ('<p class=mut>Summed from each Exp\'s scores.csv; with few arms tested, a match is only a hint.</p>'
            + ("".join(out) or '<p class=mut>No Job yet.</p>'))


def _preview(j: dict, href, root: Path) -> str:
    """An open Job card: a preview of its Tasks (t00 · each design as it reads · t99 · released)."""
    order = {"setup-goal": 0, "setup-method": 1, "setup-inputs": 2}
    setup = " · ".join(f'{_st("✓" if r["status"] == "closed" else r["status"])} <code>{esc(r["run"])}</code>'
                       for r in sorted((r for r in j["runs"] if r["type"] in order), key=lambda r: order[r["type"]]))
    tiles = []
    if j["t00"]:
        tiles.append((f'<a href="{esc(href("", "", j["t00"]))}">{_id("t00", "reason ideas")}</a>',
                      f'② {len(j["topics"])} topics → {len(j["ideas"])} ideas', _st("closed" if j["reason"] else "waiting")))
    if j["t99"]:
        kept = sum(r.get("kept") == "yes" for r in j["ranking"])
        tiles.append((f'<a href="{esc(href("", "", j["t99"]))}">{_id("t99", "review whole")}</a>',
                      f'⑤ ranked {len(j["ranking"])} · kept {kept}', _st("closed" if j["rank"] else "waiting")))
    if j["delivered"]:
        tiles.append(("released", " · ".join(esc(d.get("design", "")) for d in j["delivered"]) + " → Delivery", _st("released")))
    designs = [(f'<a href="{esc(href("", "", d["path"]))}">{_id(d["name"][:3] + " · " + d["id"])}</a>',
                as_it_reads(d["message"], d["path"], root, small=True), _st(d["state"])) for d in j["designs"][:6]]
    more = len(j["designs"]) - 6
    return ((f'<p class=mut>set up {setup}</p>' if setup else "") + table(("Task", "what it holds", "state"), tiles)
            + '<p class=mut style="margin-top:10px">③ ④ one design each, in order</p>'
            + table(("design", "as it reads", "state"), designs)
            + (f'<p class=mut>+ {more} more · {_job_link(href, j, "open the Job")}</p>' if more > 0 else ""))


def _jobs(b: dict, root: Path, href, only: str) -> str:
    out, opened = [], False
    for j in b["jobs"]:
        if only not in ("All", j["goal"]):
            continue
        live = _live(j["designs"])
        meta = (f'{esc(j["goal"])} · {esc(j["method"])} {esc(j["version"])} · {esc(j["inputs"])} · {esc(j["moved"])} moved · '
                f'{len(_passed(live))} of {len(live)} passed · {_st(j["state"])}')
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
        cells.append((_id(d.get("design", ""), pins.get("goal", "")), phone(d.get("words", "")),
                      f'{_job_link(href, j, j["id"]) if j else esc(d.get("job", ""))} · {esc(pins.get("method", ""))} · '
                      f'{esc(pins.get("inputs", ""))}',
                      f'{_st("released " + str(d.get("released", "")))} · predicted {esc(d.get("predicted", "—"))}'))
    return ((table(("design", "as it reads", "Job · method · inputs", "released · predicted"), cells) if cells
             else '<p class=mut>Nothing released yet: delivery/designs.json.</p>')
            + '<p class=mut>→ the Exp (outside the theme); its per-arm result returns into observed/.</p>')


# ── Job (s12) ────────────────────────────────────────────────────────────────────────────────
J_SKILLS = {"setup-goal": ("haipipe-design-goal",), "setup-method": ("haipipe-design-method",), "setup-inputs": ("haipipe-design-goal",),
            "open-designs": ("haipipe-design",), "reason": ("haipipe-design-unit",), "generate": ("haipipe-design-unit",),
            "verify": ("haipipe-design-unit",), "revise": ("haipipe-design-unit",), "rank": ("haipipe-design-unit",),
            "freeze-predictions": ("haipipe-design-delivery",), "release": ("haipipe-design-delivery",),
            "close": ("haipipe-design-workflow",),
            "draw": ("workbench-studio",)}


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
    freeze = k(f"run-freeze-predictions-{jid}", "freeze-predictions", "Freeze the kept designs' predictions of {folder} at "
               f"release (run-freeze-predictions-{jid}); a person signs.")
    release = k(f"run-release-{jid}", "release", f"Release {{folder}}'s kept designs (run-release-{jid}): designs.json · "
                "designs.md · screens/; a person signs.")
    opend = k(f"run-open-designs-{jid}", "open-designs", f"Open one design Task per idea in {{folder}} (run-open-designs-{jid}).")
    ar = ("Reason ideas", "Design display", "Review whole", "Predicted vs observed", "Performance")
    a_open = sub if sub in ar else "Reason ideas"
    a_html = {"Reason ideas": _reason_ideas, "Design display": _display, "Review whole": _review_whole,
              "Predicted vs observed": _job_observed, "Performance": _performance}[a_open](j, b, root, href)
    a_runs = {"Reason ideas": (reason,), "Design display": (gen, ver), "Review whole": (rank,),
              "Predicted vs observed": (freeze,), "Performance": (freeze,)}[a_open]
    wd = ("Reason ideas", "Conduct & review", "Review whole")     # one casing, as the Audience Report's (b03, 261008)
    w_open = sub if sub in wd else "Reason ideas"
    w_html = {"Reason ideas": _wd_reason, "Conduct & review": _wd_conduct, "Review whole": _wd_whole}[w_open](j, root, href)
    w_runs = {"Reason ideas": (reason, opend), "Conduct & review": (gen, ver, rev), "Review whole": (rank,)}[w_open]
    rv = ("Setup", "Reason ideas", "Conduct & review", "Review whole")
    r_open = sub if sub in rv else "Setup"
    r_runs = {"Setup": (setup["Goal"], setup["Method"], setup["Inputs"], opend), "Reason ideas": (reason,),
              "Conduct & review": (gen, ver, rev), "Review whole": (rank, freeze, release)}[r_open]
    dv = ("designs.md", "designs.json")
    v_open = sub if sub in dv else "designs.md"
    return {
        "Description": Space(html=d_html, subspaces=desc, open=d_open, run_types=d_runs, page=True,
                             disk=_disk("Job", d_open, jdir)),
        "Idea Studio": Space(run_types=(k(f"run-draw-s01", "draw", "Draw a studio topic of {folder}: studio/sNN-<topic>/ "
                                          "and its builder (run-draw-<sNN>)."),), page=True),
        "Audience Report": Space(html=a_html, subspaces=ar, open=a_open, run_types=a_runs, page=True,
                                 disk=_disk("Job", a_open, jdir)),
        "Work Details": Space(html=w_html, subspaces=wd, open=w_open, run_types=w_runs, page=True,
                              disk=_disk("Job", "WD " + w_open, jdir)),
        "Runs": Space(html=_job_runs(j, root, r_open), subspaces=rv, open=r_open, run_types=r_runs, page=True,
                      disk=_disk("Job", r_open if r_open == "Setup" else "Runs " + r_open, jdir)),
        "Delivery": Space(html=_job_delivery(j, root, v_open), subspaces=dv, open=v_open, run_types=(release,), page=True,
                          disk=_disk("Job", v_open, jdir)),
    }


def _setup_strip(j: dict) -> str:
    order = {"setup-goal": 0, "setup-method": 1, "setup-inputs": 2}
    rs = sorted((r for r in j["runs"] if r["type"] in order), key=lambda r: order[r["type"]])
    done = sum(r["status"] == "closed" for r in rs)
    return (f'<p class=mut>{" · ".join(_st("✓") + " <code>" + esc(r["run"]) + "</code>" for r in rs if r["status"] == "closed")}'
            f' → set up {_st(f"{done} of 3") if done == 3 else esc(f"{done} of 3")}</p>')


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
    inputs/rules.md (the Block's signed shared rules), one flush row each (JL 261008: "why the venue, and things
    are not ready and up to date?")."""
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
    """The pinned method, one flush row per step: what this version says, and what it did in this Job (JL 261008:
    "things here is not complete as well")."""
    card = j["method_card"]
    steps = card.get("steps") or {}
    designs = j["designs"]
    kept = sum(r.get("kept") == "yes" for r in j["ranking"])
    passed = sum(1 for d in designs if d["verifies"] and str(d["verifies"][-1]["card"].get("status", "")) == "passed")
    revised = sum(1 for d in designs if len(d["drafts"]) > 1)
    task = lambda t, text: f'<a href="{esc(href("", "", t))}">{esc(text)}</a>' if (t and href) else esc(text)
    seen = [f["name"] for f in j["files"] if f["name"] not in ("goal.md", "method.md")]
    here = {"①": "sees " + (" · ".join(seen) or "—"),
            "②": (task(j["t00"], f'{len(j["topics"])} topics → {len(j["ideas"])} ideas') if j["reason"] else "not reasoned yet"),
            "③": f'{len(designs)} designs · {revised} revised' if designs else "no design yet",
            "④": f'{passed} of {len(designs)} passed review' if designs else "—",
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
    return (head + (table(("step", f'{j["version"]} says', f'in {j["id"]}'), rows) if steps
                    else '<p class=mut>No steps in inputs/method.md yet.</p>')
            + "".join(f'<p class=mut>{esc(p)}</p>' for p in note.split("\n\n") if p.strip()))


def _job_inputs(j: dict, b: dict, root: Path) -> str:
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
            + _fold("manifest.yaml", f'every file above, its source and sha256 · frozen {esc(man.get("frozen", "—"))} = '
                                     f'{esc(man.get("inputs", j["inputs"]))}', mono=True))


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
        out.append(_fold(f'{t.get("id", "")} · {t.get("title", "")}',
                         f'from {esc(t.get("from", ""))} · {len(steps)} steps · → {len(t.get("ideas", []))} ideas',
                         f"<p>{chain}</p>", opened=not out))
    return (f'<p class=mut>inputs/ → reasoning, topic by topic → {len(j["ideas"])} ideas, frozen before any design is made '
            f'(t00 › chains.yaml).</p>' + ("".join(out) or '<p class=mut>t00 has not reasoned yet.</p>'))


def _display(j: dict, b: dict, root: Path, href) -> str:
    rank = {r.get("design"): r for r in j["ranking"]}
    rows = [_qhead("Design", "Process (③): its idea, each element's source", "Review (④) · expected outcome")]
    # every design a full card, in order (JL 261008: "why I only see a single one here?"); the dropped ones after them,
    # in one fold that opens to their full cards
    dropped = [d for d in j["designs"] if d["state"] == "dropped"]
    rows += [_card(d, j, href, root) for d in j["designs"] if d["state"] != "dropped"]
    if dropped:
        why = lambda d: f'rank #{rank[d["id"]].get("rank")}' if d["id"] in rank else "not ranked"
        rows.append(_fold(f"Dropped, kept for the record · {len(dropped)}",
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
                          # each element's source, folded until opened (JL 261008: "hidden by default ... we can open and check")
                          + (f'<details class=q-more><summary>› Elements and sources · {len(d["elements"])}</summary>'
                             + "".join(f'<p>{esc(e.get("words", ""))} <span class=mut>← {esc(e.get("from", ""))}</span></p>'
                                       for e in d["elements"]) + '</details>' if d["elements"] else ""),
                          f'<p>④ {" · ".join(f"{_test(t)} {esc(v)}" for t, v in tests.items()) or "—"} · {_st(d["state"])}</p>'
                          f'<p>expected {esc(d["prediction"].get("predicted", "—"))}</p>'
                          + (f'<p class=mut>⑤ rank #{esc(r.get("rank"))} · {"kept" if r.get("kept") == "yes" else "dropped"}</p>' if r else ""))


def _review_whole(j: dict, b: dict, root: Path, href) -> str:
    rows = [(esc(r.get("rank", "")), f'<code>{esc(r.get("design", ""))}</code>', esc(r.get("predicted", "")),
             esc(r.get("why", "")), _st("kept") if r.get("kept") == "yes" else "<span class=mut>dropped</span>") for r in j["ranking"]]
    kept = sum(r.get("kept") == "yes" for r in j["ranking"])
    return (table(("rank", "design", "predicted", "why", "kept"), rows)
            + _pairs([("ranked by", "predicted outcome, by the ④ ⑤ reviewer (another agent)"),
                      ("keeps", esc(f"the top N of N + 5 = {kept} of {len(j['ranking'])}"))])) if rows else \
        '<p class=mut>t99 has not ranked yet.</p>'


def _job_observed(j: dict, b: dict, root: Path, href) -> str:
    rows = [_qhead("Design", "Predicted · frozen at release", "Observed · the Block's observed/ and scores")]
    for d in j["designs"]:
        a = R.arm_of(b, j["id"], d["id"])
        if not a:
            continue
        s = b["scores"].get((j["id"], d["id"]), {})
        rows.append(_qrow(f'<b>{esc(d["id"])}</b>' + phone(d["message"]),
                          f'{esc(d["prediction"].get("predicted", "—"))}<p class=mut>frozen {esc(d["prediction"].get("frozen", "—"))}</p>',
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
                     esc(f'{len(d["message"])} ch'), esc(d["prediction"].get("predicted", "—")),
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
                      + [("design", phone(d["message"], small=True)), ("opens", f'<a href="{esc(href("", "", d["path"]))}">the Task</a>')])
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


def _job_delivery(j: dict, root: Path, view: str) -> str:
    path = j["delivery"] / view
    if not path.is_file():
        return f'<p class=mut>Nothing released yet: delivery/{esc(view)} is written by run-release-{esc(j["id"])}.</p>'
    text = path.read_text(encoding="utf-8", errors="ignore")
    if view == "designs.md":
        return (table(("design", "as it reads", "predicted"), [(_id(d.get("design", "")), phone(d.get("words", "")),
                                                                 esc(d.get("predicted", "—"))) for d in j["delivered"]])
                + f'<p class=mut>{_open(path, root, "designs.md", rel(path, root) + " ↗")}: for people, written from designs.json</p>')
    return f'<p class=mut>delivery/designs.json · what the experiment platform reads</p><pre>{esc(text)}</pre>'


# ── Task (s13) ───────────────────────────────────────────────────────────────────────────────
def task_spaces(tdir: Path, root: Path, sub: str, href) -> dict:
    j = R.job(tdir.parent)
    kind = R.kind_of(tdir)
    rs = R.runs(tdir)
    rows = lambda *t: _rows(rs, root, *t)
    draw = _kind("run-draw-s01", "Draw a studio topic about this Task: {folder}/studio/sNN-<topic>/ (run-draw-<sNN>).",
                 "workbench-studio")
    if kind == "t00":
        r = _kind("run-reason-t00", "Reason ideas for the Job (② run-reason-t00): inputs/ only, topic by topic, to N + 5 "
                  "ideas, each naming its source.", "haipipe-design-unit", rows=rows("reason"), level="Task")
        opend = _kind(f"run-open-designs-{j['id']}", "Open one design Task per idea (run-open-designs-jNN).", "haipipe-design",
                      rows=_rows(j["runs"], root, "open-designs"))
        ar = ("Topics", "Ideas")
        a_open = sub if sub in ar else "Topics"
        return {"Description": Space(html=_t00_task(j, root), subspaces=("Task",), open="Task", run_types=(r,), page=True,
                                     disk=_disk("t00", "Task", tdir)),
                "Audience Report": Space(html=(_reason_ideas(j, {}, root, href) if a_open == "Topics" else _t00_ideas(j, href)),
                                         subspaces=ar, open=a_open, run_types=(r,) if a_open == "Topics" else (opend,), page=True,
                                         disk=_disk("t00", a_open, tdir)),
                "Work Details": Space(html=_t00_chains(j), subspaces=("Chains",), open="Chains", run_types=(r,), page=True,
                                      disk=_disk("t00", "Chains", tdir)),
                "Idea Studio": Space(run_types=(draw,), page=True),
                "Runs": Space(html=_task_runs_table(rs, sub), subspaces=("All", "hard", "soft"),
                              open=sub if sub in ("hard", "soft") else "All", run_types=(r,), page=True,
                              disk=_disk("t00", "Runs", tdir)),
                "Delivery": Space(disk=_disk("t00", "Delivery", tdir), html='<p class=mut>Hands on ideas.yaml: run-open-designs opens one design Task per idea.</p>',
                                  page=True, note="Nothing to run here: t00 hands its ideas to the Job.")}
    if kind == "t99":
        r = _kind("run-rank-t99", "Review the whole (⑤ run-rank-t99): rank the N + 5, keep the top N, each with its predicted "
                  "outcome; another agent.", "haipipe-design-unit", rows=rows("rank"), level="Task")
        ar = ("Ranking", "Coverage")
        a_open = sub if sub in ar else "Ranking"
        return {"Description": Space(html=_t99_task(j), subspaces=("Task",), open="Task", run_types=(r,), page=True,
                                     disk=_disk("t99", "Task", tdir)),
                "Audience Report": Space(html=(_review_whole(j, {}, root, href) if a_open == "Ranking" else _coverage(j)),
                                         subspaces=ar, open=a_open, run_types=(r,), page=True, disk=_disk("t99", a_open, tdir)),
                "Work Details": Space(html=_kept(j, href), subspaces=("Kept · Dropped",), open="Kept · Dropped",
                                      run_types=(r,), page=True, disk=_disk("t99", "Kept · Dropped", tdir)),
                "Idea Studio": Space(run_types=(draw,), page=True),
                "Runs": Space(html=_task_runs_table(rs, sub), subspaces=("All", "hard", "soft"),
                              open=sub if sub in ("hard", "soft") else "All", run_types=(r,), page=True,
                              disk=_disk("t99", "Runs", tdir)),
                "Delivery": Space(disk=_disk("t99", "Delivery", tdir), html='<p class=mut>Hands on the kept N and their predictions: the Job\'s run-release '
                                       'writes its delivery/.</p>', page=True, note="Nothing to run here: the Job releases.")}
    d = R.design(tdir)
    did = d["id"]
    gen = _kind(f"run-generate-{did}", f"Generate {did} from its idea (③ run-generate-{did}): inputs/ only.",
                "haipipe-design-unit", rows=rows("generate"), level="Task")
    ver = _kind(f"run-verify-{did}", f"Verify {did} (④ run-verify-{did}-v<k>) in a fresh context, by another agent.",
                "haipipe-design-unit", rows=rows("verify"), level="Task")
    rev = _kind(f"run-revise-{did}", f"Revise {did} after a failed review (run-revise-{did}), then verify again.",
                "haipipe-design-unit", rows=rows("revise"), level="Task")
    frz = _kind(f"run-freeze-prediction-{did}", f"Freeze {did}'s prediction at release (the Job's run-freeze-predictions).",
                "haipipe-design", rows=_rows(j["runs"], root, "freeze-predictions"))
    desc = ("Design", "Evaluation")
    d_open = sub if sub in desc else "Design"
    ar = ("Tests", "Drafts", "Performance")
    a_open = sub if sub in ar else "Tests"
    b = R.board(R.block_of(tdir.parent.parent) or tdir.parent.parent, with_jobs=False)
    return {"Description": Space(html=_design(d, j, href, root) if d_open == "Design" else _evaluation(d), subspaces=desc, open=d_open,
                                 page=True, disk=_disk("design", d_open, tdir), note="Nothing to run here: the design is made in Runs."),
            "Audience Report": Space(html={"Tests": _tests, "Drafts": _drafts, "Performance": _task_perf}[a_open](d, j, b, root),
                                     subspaces=ar, open=a_open,
                                     run_types={"Tests": (ver,), "Drafts": (gen, rev), "Performance": (frz,)}[a_open], page=True,
                                     disk=_disk("design", a_open, tdir)),
            "Work Details": Space(html=_elements(d), subspaces=("Elements",), open="Elements", run_types=(rev,), page=True,
                                  disk=_disk("design", "Elements", tdir)),
            "Idea Studio": Space(run_types=(draw,), page=True),
            "Runs": Space(html=_task_runs_table(rs, sub), subspaces=("All", "hard", "soft"),
                          open=sub if sub in ("hard", "soft") else "All", run_types=(gen, ver, rev), page=True,
                          disk=_disk("design", "Runs", tdir)),
            "Delivery": Space(html=_task_delivery(d, j), page=True, disk=_disk("design", "Delivery", tdir), note="Released with the Job's run-release (a person).")}


def _t00_task(j: dict, root: Path) -> str:
    r = j["reason"]
    return _pairs([("step", "② Reason ideas: from inputs/ to N + 5 ideas, frozen before any design is made"),
                   ("reads", f'<code>{esc(j["name"])}/inputs/</code> only (the fence)'),
                   ("by", esc(f'the designer agent · {r["run"]} (hard)') if r else "—"),
                   ("returns", esc(f'{len(j["topics"])} topics → {len(j["ideas"])} ideas')),
                   ("state", _st(r["status"] if r else "waiting"))])


def _t00_ideas(j: dict, href) -> str:
    designs = {d["id"]: d for d in j["designs"]}
    rows = []
    for i in j["ideas"]:
        d = designs.get(i.get("design", ""))
        rows.append((f'<code>{esc(i.get("id", ""))}</code>', esc(i.get("idea", "")), esc(i.get("topic", "")),
                     (f'<a href="{esc(href("", "", d["path"]))}">{esc(d["id"])}</a> {_st(d["state"])}') if d else "—"))
    return table(("idea", "what", "topic", "its design"), rows)


def _t00_chains(j: dict) -> str:
    rows = [(esc(t.get("id", "")), esc(k + 1), esc(s.get("says", "")), esc(s.get("so", "")), esc(t.get("from", "")))
            for t in j["topics"] for k, s in enumerate(t.get("steps") or [])]
    return table(("topic", "step", "says", "so", "from (in the manifest)"), rows)


def _t99_task(j: dict) -> str:
    r = j["rank"]
    kept = sum(x.get("kept") == "yes" for x in j["ranking"])
    return _pairs([("step", "⑤ Review whole: rank the N + 5, keep the top N, each with its predicted outcome"),
                   ("by", esc(f'another agent · {r["run"]} (hard)') if r else "—"),
                   ("returns", esc(f'ranked {len(j["ranking"])} · kept {kept}')), ("state", _st(r["status"] if r else "waiting"))])


def _coverage(j: dict) -> str:
    kept = [d for d in j["designs"] if d["state"] != "dropped"]
    topics = {i.get("design"): i.get("topic") for i in j["ideas"]}
    covered = sorted({topics.get(d["id"], "") for d in kept} - {""})
    return _pairs([("topics covered by the kept", esc(" · ".join(covered) or "—")),
                   ("kept", esc(f"{len(kept)} designs")), ("no two alike", "read from the ranking's why")])


def _kept(j: dict, href) -> str:
    kept_, dropped_ = [], []
    for d in j["designs"]:
        dropped = d["state"] == "dropped"
        (dropped_ if dropped else kept_).append(_fold(f'{d["name"][:3]} · {d["id"]}',
                                                     ("dropped, folded" if dropped else "kept") + f' · {_st(d["state"])}', mono=True))
    return "".join(kept_) + (_fold(f"Dropped by t99, kept for the record · {len(dropped_)}", "", "".join(dropped_))
                             if dropped_ else "")


def _task_runs_table(rs: list, sub: str) -> str:
    view = sub if sub in ("hard", "soft") else "All"
    return table(("Run", "kind", "by", "state"), [(f'<code>runs/{esc(r["run"])}/</code>', esc(r["kind"]), esc(r["by"] or "—"),
                                                   _st(r["status"])) for r in rs if view in ("All", r["kind"])])


def _design(d: dict, j: dict, href, root: Path) -> str:
    """The Job's design card, opened (s12's Design display), then its state, its name and its Job."""
    r = {x.get("design"): x for x in j["ranking"]}.get(d["id"], {})
    kept = ("kept" if r.get("kept") == "yes" else "dropped") + f' (rank #{r.get("rank")} of {len(j["ranking"])})' if r else "not ranked yet"
    released = any(x.get("design") == d["id"] for x in j["delivered"])
    return (_qhead("Design", "Process (③): its idea, each element's source", "Review (④ ⑤) · expected outcome") + _card(d, j, href, root)
            + _pairs([("state", _st(d["state"]) + esc(f' · draft {len(d["drafts"])} · {kept} · '
                                                          + ("released" if released else "not released yet"))),
                      ("name", esc(f'{d["short"]} · born with its idea {d["idea"]} in t00')),
                      ("Job", esc(f'{j["id"]} · {j["goal"]} × design method {j["method"]}, version {j["version"]} × inputs {j["inputs"]}'))]))


def _evaluation(d: dict) -> str:
    tests = d["verifies"][-1]["card"].get("tests", {}) if d["verifies"] else {}
    return _pairs([("review (④)", " · ".join(f"{_test(t)} {_st(v)}" for t, v in tests.items()) or "—"),
                   ("by", esc(d["verifies"][-1]["by"]) if d["verifies"] else "—"),
                   ("as written", esc(d["evaluation"] or "—")), ("state", _st(d["state"]))])


def _tests(d: dict, j: dict, b: dict, root: Path) -> str:
    rows = [(f'<code>{esc(v["run"])}</code>', _test(t), _st(res), esc(v["by"])) for v in d["verifies"]
            for t, res in (v["card"].get("tests") or {}).items()]
    return table(("Run", "test", "result", "by"), rows) if rows else '<p class=mut>Not verified yet.</p>'


def _drafts(d: dict, j: dict, b: dict, root: Path) -> str:
    out = []
    for k, r in enumerate(d["drafts"], 1):
        text = ""
        f = r["path"] / "result" / "design.md"
        if f.is_file():
            text = f.read_text(encoding="utf-8", errors="ignore").strip()
        out.append((f"draft {k}", _id(r["run"]), as_it_reads(text, d["path"] if k == len(d["drafts"]) else None, root)))
    return table(("draft", "Run", "as it reads"), out) if out else '<p class=mut>No draft yet.</p>'


def _task_perf(d: dict, j: dict, b: dict, root: Path) -> str:
    a = R.arm_of(b, j["id"], d["id"])
    s = b["scores"].get((j["id"], d["id"]), {})
    mins = [r["minutes"] for r in d["runs"] if r["minutes"] is not None]
    return _pairs([("tokens", "— <span class=mut>(usage: not in the Run receipt yet)</span>"),
                   ("time", esc(_mins(sum(mins)) if mins else "—")), ("rounds", esc(len(d["drafts"]))),
                   ("predicted", esc(d["prediction"].get("predicted", "—"))), ("frozen", _st(d["prediction"].get("frozen", "—"))),
                   ("observed (Exp)", esc(f'{a.get("observed")} · arm {a.get("arm")} of {a.get("exp")}') if a else "<span class=mut>not tested</span>"),
                   ("matched", (f'direction {_st(s.get("direction"))} · in range {_st(s.get("in_range"))}') if s else "—")])


def _elements(d: dict) -> str:
    rows = [(esc(e.get("element", "")), esc(e.get("words", "")), esc(e.get("from", "")), esc(e.get("because", "")),
             esc(e.get("step", "")), esc(e.get("changed", "") or "—")) for e in d["elements"]]
    return table(("element", "words", "from", "because", "step", "changed"), rows) if rows else \
        '<p class=mut>No elements.yaml yet.</p>'


def _task_delivery(d: dict, j: dict) -> str:
    rel_ = next((x for x in j["delivered"] if x.get("design") == d["id"]), None)
    if rel_:
        return phone(rel_.get("words", "")) + f'<p class=mut>released {_st("✅ " + str(rel_.get("released", "")))} · predicted {esc(rel_.get("predicted", ""))}</p>'
    return '<p class=mut>Not released: released with the Job\'s run-release (a person); the prediction freezes then.</p>'
