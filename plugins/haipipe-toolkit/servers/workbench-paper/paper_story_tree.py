"""A Story's §3 question blocks and its logic tree: each question's hypotheses and claims beside the work that tests them.
Moved from paper.py, which re-exports every name here so `from live.paper import story_tree` keeps working."""
import re
from pathlib import Path

from live.paper import (_FIELD, _REPORT_STATUS, _addresses, _col, _disc_link, _disc_lookup, _fmt_state, _plain, _row_ids,
                        _row_key, _unnamed_addrs, division_body, divisions, esc, outline_url, task_home)
from live.paper_run_view import run_result_url


_QHEAD = re.compile(r"^####\s+[\d.]+\s*·\s*Question\s+(\d+)(?:\s*·\s*(RQ\d+))?\s*$", re.I)
_GROUP = re.compile(r"^\*\*(tasks|hypotheses|potential claims|potential contributions|potential work)\*\*\s*:?\s*$", re.I)
_ITEM = re.compile(r"^-\s+(?:\*\*([A-Z]{1,2}\d+|\d+[a-z])\*\*\s*(?:·\s*)?)?(.*)$")
_CODE = re.compile(r"(?<![\w.])(\d+[a-z])(?!\w)")
_SUBFIELD = re.compile(r"\*\*(.+?)\*\*\s*:\s*(.*?)(?=\s*·\s*\*\*|$)")
_GROUPS = {"tasks": "tasks", "hypotheses": "hypotheses", "potential claims": "claims",
           "potential contributions": "contributions", "potential work": "work"}


def question_blocks(text):
    """§3 written as one block per question (JL 260929; hai-paper-story 0.12.0):
    `#### 3.N · Question N · RQn`, the question's `- **Field**: value` lines, then four
    groups, each a bold label and one `- ` line per item, coded by question (1a, 1b, 2a …;
    hai-paper-story 0.13.0), each a short name, a colon and one plain sentence:
      **Hypotheses**               - **1a** · Name: sentence · tested by E1, E2
      **Potential claims**         - **1a** · C1 · from 1a · Name: sentence   (indented `- **Role**: …`)
      **Potential contributions**  - rests on 1a, 1b · Name: sentence
      **Potential work**           - **T1** · for 1a, 1b   (optionally `· b04.j03.t01, …` to narrow)
    A question that sets the study's tasks rather than testing a guess may open with
      **Tasks**                    - Pretraining · Name: sentence   (the kind, then the task)
    A claim keeps its paper-wide id (C1) after its code. [] for a Story that still
    writes the RQ table."""
    n = next((n for n, title in divisions(text) if title.strip().lower().startswith("research question")), None)
    out, cur, group, last = [], None, None, None
    for line in (division_body(text, n) if n is not None else "").splitlines():
        s = line.strip()
        m = _QHEAD.match(s)
        if m:
            cur = {"n": int(m.group(1)), "id": m.group(2) or "RQ" + m.group(1), "fields": [], "tasks": [],
                   "hypotheses": [], "claims": [], "contributions": [], "work": []}
            out.append(cur)
            group = last = None
            continue
        if line.startswith("#"):
            cur = group = last = None
            continue
        if cur is None or not s:
            continue
        g = _GROUP.match(s)
        if g:
            group, last = _GROUPS[g.group(1).lower()], None
            continue
        if group is None:
            f = _FIELD.match(s)
            if f:
                cur["fields"].append((f.group(1).strip(), _plain(f.group(2))))
            continue
        if line[:1] == "-":
            m = _ITEM.match(s)
            last = {"id": m.group(1) or "", "fields": [],
                    "parts": [x.strip() for x in _plain(m.group(2)).split(" · ") if x.strip()] or [""]}
            cur[group].append(last)
        elif last is not None and s.startswith("- "):            # an indented `- **Role**: …` line
            last["fields"] += [(k.strip(), _plain(v)) for k, v in _SUBFIELD.findall(s[2:])]
        elif last is not None:                                    # a wrapped line continues the item
            last["parts"][-1] = (last["parts"][-1] + " " + _plain(s)).strip()
    return out


def _field(fields, *names):
    return next((v for k, v in fields if k.strip().lower() in names), "")


def _part(parts, word):
    """The rest of the part that starts with `word` (`tested by`, `from`, `for`, …)."""
    return next((x[len(word):].strip() for x in parts if x.lower().startswith(word)), "")


_STAGES = ("data", "training", "evaluation", "results", "analysis", "figures")
_STAGE_ORDER = {k: i for i, k in enumerate(_STAGES + ("task", "discovery"))}


def _work_rows(s):
    """The §7 Task and §6 Discovery rows: id → its short name (a `name` cell) and the
    plain sentence under it (its `question` cell), or the question alone as its name when
    the row has no `name` cell; its stage (a §7 `stage` cell: data · training · evaluation ·
    results · analysis · figures), whether it serves `every question`, and the row ids it names."""
    work = {}
    for kind, rows, heads in (("task", s["tt"], s["tt_h"]), ("disc", s["dd"], s["dd_h"])):
        iq = next((i for i, h in enumerate(heads) if h.strip().lower() == "question"), 1)
        ist = next((i for i, h in enumerate(heads) if h.strip().lower() == "stage"), None)
        inm = next((i for i, h in enumerate(heads) if h.strip().lower() == "name"), None)
        for c in rows:
            stage = (c[ist].strip().lower() if ist is not None and ist < len(c) else "") or (
                "discovery" if kind == "disc" else "task")
            q = c[iq] if len(c) > iq else c[0]
            nm = c[inm].strip() if inm is not None and inm < len(c) else ""
            work[_row_key(c[0])] = {"id": _row_key(c[0]), "kind": kind, "cells": c, "stage": stage,
                                    "name": nm or q, "text": q if nm else "",
                                    "shared": any("every question" in x.lower() for x in c[1:]),
                                    "names": set(_row_ids(" ".join(c[1:])))}
    return work


def story_tree(s):
    """High-level logic joined to low-level work (JL 260929). §3 question blocks give each
    question its hypotheses (each names the §5 rows testing it), potential claims (each
    from a hypothesis), potential contributions (each resting on claims) and potential
    work (each §7/§6 row for the hypotheses it tests). A Story that still writes the RQ
    table gets one hypothesis per §5 row and its work read from either end of the §5↔§7
    links. §7 rows marked `every question` are the shared work; `up` maps each work row
    to every hypothesis, §5 row and question above it, which keys its Runs panel runs."""
    work = _work_rows(s)
    irq = _col(s["e_h"], ("rq", "question"), 1)
    ip = _col(s["e_h"], ("proposition", "claim"), 3)
    ist = _col(s["e_h"], ("support", "state", "status"), 2)
    tests = {}
    for c in s["e"]:
        if re.match(r"E-?\d+", c[0]):
            e, said = _row_key(c[0]), set(_row_ids(" ".join(c[1:])))
            tests[e] = {"id": e, "cells": c, "prop": c[ip] if len(c) > ip else "",
                        "state": c[ist] if len(c) > ist else "",
                        "rqs": [x for x in _row_ids(c[irq] if len(c) > irq else "") if x.startswith("RQ")],
                        "work": [w for w in work if w in said or e in work[w]["names"]]}
    qs = []
    for b in s.get("qb") or []:
        q = {"id": b["id"], "text": _field(b["fields"], "question") or b["id"], "fields": b["fields"],
             "tasks": [{"kind": x["parts"][0], "text": " · ".join(x["parts"][1:])} for x in b.get("tasks", [])],
             "hyps": [], "claims": [], "contribs": [], "items": [], "notes": {}}
        for h in b["hypotheses"]:
            if h["id"]:
                q["hyps"].append({"id": h["id"], "tests": [x for x in _row_ids(_part(h["parts"], "tested by")) if x in tests],
                                  "phrase": next((x for x in h["parts"] if not x.lower().startswith("tested by")), h["id"])})
            else:
                q["notes"]["hypotheses"] = " · ".join(h["parts"])
        for c in b["claims"]:
            if c["id"]:
                alias = next((x for x in c["parts"] if re.fullmatch(r"C\d+", x)), "")
                q["claims"].append({"id": c["id"], "alias": alias, "from": _CODE.findall(_part(c["parts"], "from ")),
                                    "fields": c["fields"],
                                    "text": " · ".join(x for x in c["parts"] if x != alias and not x.lower().startswith("from "))})
            else:
                q["notes"]["claims"] = " · ".join(c["parts"])
        for c in b["contributions"]:
            rests = _CODE.findall(_part(c["parts"], "rests on"))
            text = " · ".join(x for x in c["parts"] if not x.lower().startswith("rests on"))
            if rests:
                q["contribs"].append({"rests": rests, "text": text})
            else:
                q["notes"]["contributions"] = text
        for w in b["work"]:
            wid = _row_key(w["id"]) if w["id"] else ""
            if wid in work:
                q["items"].append({"w": wid, "for": _CODE.findall(_part(w["parts"], "for ")),
                                   "addrs": _addresses(" ".join(x for x in w["parts"] if not x.lower().startswith("for ")))})
        qs.append(q)
    if not s.get("qb"):                     # the RQ table: one hypothesis per §5 row naming the RQ
        for r in s["rq"]:
            rid, said = _row_key(r[0]), set(_row_ids(" ".join(r[1:])))
            hyps = [{"id": e, "phrase": x["prop"], "tests": [e]} for e, x in tests.items() if rid in x["rqs"]]
            items = []
            for w in work:
                fr = [h["id"] for h in hyps if w in tests[h["id"]]["work"]]
                if fr or w in said or rid in work[w]["names"]:
                    items.append({"w": w, "for": fr, "addrs": []})
            heads = s["rq_h"]
            qs.append({"id": rid, "text": r[1] if len(r) > 1 else rid, "hyps": hyps, "claims": [], "contribs": [],
                       "items": items, "notes": {},
                       "fields": [(heads[i] if i < len(heads) else "col %d" % (i + 1), r[i])
                                  for i in range(2, len(r)) if r[i] and r[i] not in ("—", "-")]})
    shared = [w for w in work if work[w]["shared"]]
    named = {i["w"] for q in qs for i in q["items"]}
    placed = {x for q in qs for h in q["hyps"] for x in h["tests"]}
    up = {w: [] for w in work}
    for q in qs:
        tests_of = {h["id"]: h["tests"] for h in q["hyps"]}
        for i in q["items"]:
            up[i["w"]] += i["for"] + [x for h in i["for"] for x in tests_of.get(h, [])] + [q["id"]]
    orphans = [x for x in tests.values() if x["id"] not in placed]
    for x in orphans:
        for w in x["work"]:
            up[w].append(x["id"])
    asked = {}
    for q in qs:
        for i in q["items"]:
            asked.setdefault(i["w"], []).append((_num(q["id"]), set(i["addrs"])))
    return {"questions": qs, "orphans": orphans, "tests": tests, "work": work, "shared": shared, "asked": asked,
            "up": {w: list(dict.fromkeys(ks)) for w, ks in up.items()},
            "loose": [w for w in work if w not in named and w not in shared]}


def _num(rid):
    m = re.search(r"\d+", rid or "")
    return m.group(0) if m else (rid or "")


def _mark(states):
    """One mark for a hypothesis from the states of the §5 rows that test it: ✅ when
    every row says established (a ✅ alone is not enough, since a Story may write
    `✅ stated · ⬜ unbacked`), ❌ when one is contradicted, 🔨 when one is provisional,
    ⬜ otherwise."""
    low = [(x or "").lower() for x in states]
    if low and all("established" in x for x in low):
        return "✅"
    if any("contradict" in x for x in low):
        return "❌"
    if any("🔨" in x or "provisional" in x for x in low):
        return "🔨"
    return "⬜"


def _nodes(tree, addrs):
    """Addresses (`b04j01t02`, `b04j01`, `b01`) → [(block, [(job, tasks)])] in folder
    order: a block or job address takes all of it, a task address takes that task."""
    out = []
    for blk in tree:
        jobs = []
        for j in blk["jobs"]:
            if any(j["addr"].startswith(a) for a in addrs):
                jobs.append((j, j["tasks"]))
            else:
                ts = [t for t in j["tasks"] if t["addr"] in addrs]
                if ts:
                    jobs.append((j, ts))
        if jobs:
            out.append((blk, jobs))
    return out


def _runs_fold(d, t):
    """R: a task's runs as (`3 runs · no receipts`, one line per run ticket, or per
    `results/<run>/` folder when a Task has results and no tickets), or the "no runs yet"
    mark. A line opens that run's results in the pop-out (JL 260930: "a popout window to
    show the results")."""
    ticks = [stem for stem, _ in (t.get("ticket_list") or [])]
    home = Path(t["dir"])
    if not ticks and (home / "results").is_dir():
        ticks = sorted(x.name for x in (home / "results").iterdir() if x.is_dir() and not x.name.startswith("."))
    if not ticks and (home / "runs").is_dir():                 # one folder per Run: runs/<run>/result/
        ticks = sorted(x.name for x in (home / "runs").iterdir() if (x / "result").is_dir())
    n = len(ticks) or t.get("n_results", 0)
    if not n:
        return '<span class="mut bj-rn">no runs yet</span>'
    opens = d.get("root") is not None and ((home / "results").is_dir() or (home / "runs").is_dir())
    line = lambda stem: '<span class="idtag">%s</span> <span class="mut">%s</span>' % (
        esc(stem), esc((t.get("receipt_map") or {}).get(stem) or "no receipt"))
    lines = "".join(('<a class="bj-run" href="%s" target="_blank" data-pop="%s">%s</a>'
                     % (esc(run_result_url(d["root"], home, stem)), esc(stem), line(stem))) if opens else
                    '<div class="bj-run">%s</div>' % line(stem) for stem in ticks)
    return esc("%d run%s · %s" % (n, "" if n == 1 else "s", _fmt_state(t.get("receipts") or {}))), lines


def _bjtr(d, nodes, disc=False):
    """B → J → T → R, one line per level, no boxes (JL 260929)."""
    out = []
    for blk, jobs in nodes:
        out.append('<div class="bj-b"><span class="idtag">%s</span> <b>%s</b></div>' % (esc(blk["addr"]), esc(blk["name"][4:])))
        for j, ts in jobs:
            out.append('<div class="bj-j"><span class="idtag">%s</span> %s</div>' % (esc(j["name"][:3]), esc(j["name"][4:])))
            for t in ts:
                if disc:                         # a Discovery task also says what it found
                    name = _disc_link(d, blk, j, t, t["name"][4:]) + (
                        ' <span class="mut">%s</span>' % esc(t["outcome"] + ((" · " + t["confidence"]) if t.get("confidence") else ""))
                        if t.get("outcome") else "")
                else:
                    # plain text: the link only opened the raw Task Markdown (JL 260930: "I don't
                    # think this is useful, could you remove this link?"); its runs open results
                    name = esc(t["name"][4:])
                head, fold = '<span class="idtag">%s</span> %s' % (esc(t["name"][:3]), name), _runs_fold(d, t)
                # the runs open below the task, one level in, as t sits under j (JL 260930:
                # "make the run below the t02 … follow the same indentation as b and j and t")
                out.append(('<details class="bj-tr"><summary class="bj-t">%s <span class="bj-rs">%s</span></summary>'
                            '<div class="bj-runs">%s</div></details>' % (head, fold[0], fold[1])) if isinstance(fold, tuple)
                           else '<div class="bj-t">%s %s</div>' % (head, fold))
            if not ts:
                out.append('<div class="bj-t mut">no task yet</div>')
    return "".join(out)


def _home_label(home):
    return ((home["dir"].name + "/") if home.get("dir") is not None else "")


def _item_folders(d, T, it):
    """One work item's B → J → T → R: the folders the question block names for it (a
    shared row narrowed to what this question needs), else its row's own addresses.
    Returns (html, size): size is the closed line's count, `4 tasks · 14 runs`."""
    c = T["work"][it["w"]]
    if c["kind"] == "task":
        addrs = it["addrs"] or [x["address"].replace(".", "") for x in task_home(d, c["cells"])["all"]]
        nodes, home = _nodes(d["blocks"]["tree"], set(addrs)), d["blocks"]
    else:
        addrs = it["addrs"] or [x for x in _addresses(" ".join(c["cells"])) if _disc_lookup(d, x)]
        nodes, home = _nodes(d["disc"]["tree"], set(addrs)), d["disc"]
    if nodes:
        tasks = [t for _, jobs in nodes for _, ts in jobs for t in ts]
        runs = sum(len(t.get("ticket_list") or []) or t.get("n_results", 0) for t in tasks)
        size = "%d task%s · %d run%s" % (len(tasks), "" if len(tasks) == 1 else "s", runs, "" if runs == 1 else "s")
        return ('<div class="bj-home mut">%s</div>%s' % (esc(_home_label(home)), _bjtr(d, nodes, disc=c["kind"] == "disc")), size)
    away = re.search(r"\b(examples-[\w.-]+/[\w.@-]+)", " ".join(c["cells"]))
    if away and c["kind"] == "task":                 # built in another project, outside the Task home
        return ('<div class="bj-none mut">built outside %s: <code>%s</code></div>'
                % (esc(_home_label(home) or "this project"), esc(away.group(1))), "built outside " + (_home_label(home) or "this project"))
    return ('<div class="bj-none mut">%sno folder yet</div>' % (esc(_home_label(home) + " · ") if _home_label(home) else ""),
            "no folder yet")


def _and(labels):
    """["Hypothesis 1", "Hypothesis 2"] → "Hypotheses 1 and 2"; one label stays as it is."""
    if len(labels) < 2:
        return "".join(labels)
    kinds = {x.split()[0] for x in labels}
    if len(kinds) == 1:
        nums = [x.split()[-1] for x in labels]
        word = {"Hypothesis": "Hypotheses", "Claim": "Claims"}.get(kinds.pop(), "")
        return "%s %s and %s" % (word, ", ".join(nums[:-1]), nums[-1])
    return ", ".join(labels[:-1]) + " and " + labels[-1]


def _lw_row(key, left, right, cls="lw-g", report=None):
    """One row of the split: logic left, work right, and with `report` a third column, the
    question's Report (JL 261003: "following the question --> Work and report")."""
    third = '<div class="lw-p">%s</div>' % report if report is not None else ""
    return ('<div class="lw-row %s%s"%s><div class="lw-l">%s</div><div class="lw-r">%s</div>%s</div>'
            % (cls, " lw-3" if report is not None else "", (' data-key="%s"' % esc(key)) if key else "",
               left, right, third))


def _report_cell(d, q):
    """The Report column of one question: its state, its answer in a line, Open ↗."""
    r = (d.get("reports") or {}).get(_num(q["id"]))
    if not r:
        return '<div class="lw-say">No report yet.</div>'
    word, cls = _REPORT_STATUS.get(r["status"], (r["status"].capitalize() or "Open", "mut"))
    answer = r["answer"] if len(r["answer"]) <= 260 else r["answer"][:257].rsplit(" ", 1)[0] + "…"
    return ('<div class="lw-c"><div class="lw-top"><span class="item-kind">Report</span>'
            '<span class="lw-rstate %s">%s</span></div><div class="lw-body">%s</div>'
            '<div class="lw-say">%s · <a href="%s">Open ↗</a></div></div>'
            % (cls, esc(word), esc(answer) or "No answer recorded yet.", esc(r["stem"]),
               esc(outline_url(d["path"], r["rel"]))))


def _label(kind, rid):
    """`Hypothesis 1a` for a §3 code; `Hypothesis 1` for an older id such as E1."""
    return "%s %s" % (kind, rid if re.fullmatch(r"\d+[a-z]", rid or "") else _num(rid))


def _nx(text):
    """`Short name: one sentence` → the name in bold, then the sentence (JL 260929: "both
    the hypotheses and claims to be short-phrase-name: explanation")."""
    m = re.match(r"^([^:]{2,80}):\s+(.+)$", text or "")
    if not m:
        return esc(text)
    return '<b class="lw-name">%s</b>: %s' % (esc(m.group(1)), esc(m.group(2)))


def _hyp_line(key, pill, text, mark="", strong=True):
    """One pickable item on the left: the pill and its mark on one line, the short name
    and sentence starting on the next (JL 260929: "make the text start from the next line
    after the label")."""
    return ('<div class="lw-h"%s><div class="lw-top"><span class="item-kind">%s</span><span class="lw-mark">%s</span></div>'
            '<div class="lw-body">%s</div></div>'
            % ((' data-key="%s"' % esc(key)) if key else "", esc(pill), mark, _nx(text) if strong else esc(text)))


def _also(others):
    if not others:
        return ""
    nums = [str(n) for n in others]
    words = ("Question " + nums[0]) if len(nums) == 1 else "Questions %s and %s" % (", ".join(nums[:-1]), nums[-1])
    return '<span class="lw-also">also for %s</span>' % esc(words)


def _work_item(d, T, it, labels, also=()):
    """One piece of work, named as the question it answers (JL 260929), folded like the
    foundation work (JL 260929: "results 也是可以 click 的，也是可以 collapse 的"). Closed, it
    still shows its stage and short name on one line, the plain sentence below, as a question
    does (JL 260930: "the Label, + Short names, and a new line to explain what it is"), then
    the hypotheses it tests, the other questions that use it and its size; open, its
    B → J → T → R. Opening it selects it for the Runs panel."""
    c = T["work"][it["w"]]
    folders, size = _item_folders(d, T, it)
    fr = [labels.get(h, _label("Hypothesis", h)) for h in it["for"]]
    tags = "".join(x for x in (('<span class="lw-for">for %s</span>' % esc(_and(fr))) if fr else "",
                               _also(also), '<span class="lw-size">%s</span>' % esc(size)) if x)
    from live.work_items import work_item
    return work_item(c["stage"].capitalize(), c["name"], c.get("text", ""), tags, folders,
                     key=it["w"], for_keys=" ".join(it["for"]))


def _in_order(T, items):
    """Work in the order it runs: data, training, evaluation, results, analysis, figures,
    then Discovery (JL 260929: "the work should follow the logics")."""
    return [x for _, x in sorted(enumerate(items), key=lambda p: (_STAGE_ORDER.get(T["work"][p[1]["w"]]["stage"], 6), p[0]))]


def _q_block(d, T, q):
    """One question block (JL 260929: the question is the main block): the question across
    the top; left, its tasks (only a question that sets them), its hypotheses, potential claims and potential contributions, coded 1a,
    1b …, each a short name and a sentence; right, its potential work: first the foundation
    every question stands on (§7 rows marked `every question`, folded, marked shared), then
    this question's own work in run order, each named as a question, with its folders."""
    labels = {h["id"]: _label("Hypothesis", h["id"]) for h in q["hyps"]}
    # no group labels (JL 260930: "Hypotheses <--- could we just remove this … of no
    # information", and the same for Foundation work and This question's work): every
    # item's pill names its kind, so each group is only a gap; an empty group says so
    # under its kind's pill. Tasks keeps its label: its pills name only the task.
    none = lambda kind, key: ('<div class="lw-c"><div class="lw-top"><span class="item-kind">%s</span></div>'
                              '<div class="lw-say">%s</div></div>' % (esc(kind), esc(q["notes"].get(key) or "none yet")))
    group = lambda items: '<div class="lw-g">%s</div>' % "".join(items)
    # a question that sets the tasks (JL 260930: "what is the pretraining task, and also the
    # downstream task") lists them first, and shows only the groups it fills
    tasks = q.get("tasks") or []          # the RQ table has none
    # the question's tasks, without a "Tasks" band over them (JL 261007: "what is this 'Task' could we remove this?")
    groups = [[_hyp_line("", x["kind"], x["text"]) for x in tasks] if tasks else []]
    # a ✅ needs the question's Report to say answered (JL 261003); before that the prose
    # states it but nothing has shown it: 📝
    answered = ((d.get("reports") or {}).get(_num(q["id"])) or {}).get("status") == "answered"
    shown = lambda m: "📝" if m == "✅" and not answered else m
    groups.append([_hyp_line(h["id"], labels[h["id"]], h["phrase"], shown(_mark([T["tests"][x]["state"] for x in h["tests"]])))
                   for h in q["hyps"]] or ([] if tasks else [none("Hypothesis", "hypotheses")]))
    groups.append(['<div class="lw-c"><div class="lw-top"><span class="item-kind">%s</span></div><div class="lw-body">%s</div>'
                   '<div class="lw-say">from %s</div></div>' % (esc(_label("Claim", c["id"])), _nx(c["text"]),
                                                                  esc(_and([labels.get(h, _label("Hypothesis", h)) for h in c["from"]])))
                   for c in q["claims"]] or ([] if tasks else [none("Claim", "claims")]))
    # a contribution is labelled like a claim (JL 260930: "we can have the contribution label
    # as well"), coded by question in its order: Contribution 1a, 1b
    groups.append(['<div class="lw-c"><div class="lw-top"><span class="item-kind">%s</span></div><div class="lw-body">%s</div>'
                   '<div class="lw-say">rests on %s</div></div>'
                   % (esc(_label("Contribution", _num(q["id"]) + "abcdefghijklmnopqrstuvwxyz"[i % 26])), _nx(c["text"]),
                      esc(_and([_label("Claim", x) for x in c["rests"]]))) for i, c in enumerate(q["contribs"])] or (
                       [] if tasks else [none("Contribution", "contributions")]))
    left = [group(g) for g in groups if g]
    listed = {i["w"]: i for i in q["items"]}
    found = _in_order(T, [listed.get(w) or {"w": w, "for": [], "addrs": []} for w in T["shared"]])
    own = _in_order(T, [i for i in q["items"] if i["w"] not in T["shared"]])
    right = [group([_work_item(d, T, it, labels) for it in found])] if found else []
    # "also for" only where another question uses the same folders: a row narrowed to other
    # folders there (each question's own figures) is not shared work
    also = lambda it: [n for n, a in T["asked"].get(it["w"], [])
                       if n != _num(q["id"]) and (not a or not it["addrs"] or a & set(it["addrs"]))]
    right.append(group([_work_item(d, T, it, labels, also=also(it)) for it in own] or ['<div class="lw-say">no work named yet</div>']))
    # closed by default (JL 260930): the questions alone read as the paper's outline
    # the label sits on its own line with the question's short name, the question below it
    # (JL 260930: "Question: short name, then the sentence"), as hypotheses and claims do
    name = _field(q["fields"], "name")
    return ('<details class="qc lw-q" data-key="%s"><summary><span class="bjt-chev">›</span><div class="lw-qhead">'
            '<div class="lw-qtop"><span class="item-kind">Question %s</span>%s</div>'
            '<div class="lw-qtext">%s</div></div></summary>%s</details>'
            % (esc(q["id"]), esc(_num(q["id"])), ('<span class="lw-qname">%s</span>' % esc(name)) if name else "",
               esc(q["text"]), _lw_row("", "".join(left), "".join(right), report=_report_cell(d, q))))


def _rest_block(d, T):
    """What no question holds: §5 rows no hypothesis names, §7/§6 rows no question names,
    and claimed folders no row names."""
    left = [_hyp_line(x["id"], x["id"], x["prop"], _mark([x["state"]]), strong=False) for x in T["orphans"]]
    right = [_work_item(d, T, it, {}) for it in _in_order(T, [{"w": w, "for": [], "addrs": []} for w in T["loose"]])]
    ta, da = _unnamed_addrs(d)
    tn, dn = _nodes(d["blocks"]["tree"], set(ta)), _nodes(d["disc"]["tree"], set(da))
    if tn or dn:
        right.append('<div class="lw-w"><div class="lw-wline"><span class="lw-wq mut">Folders no row names</span></div>%s%s</div>'
                     % (('<div class="bj-home mut">%s</div>%s' % (esc(_home_label(d["blocks"])), _bjtr(d, tn))) if tn else "",
                        ('<div class="bj-home mut">%s</div>%s' % (esc(_home_label(d["disc"])), _bjtr(d, dn, disc=True))) if dn else ""))
    if not left and not right:
        return ""
    return ('<details class="qc lw-q lw-rest"><summary><span class="bjt-chev">›</span>'
            '<span class="lw-qtext">Not under a question</span></summary>%s</details>'
            % _lw_row("", "".join(left) or '<div class="lw-say">every §5 row has a hypothesis</div>', "".join(right),
                      report=""))
