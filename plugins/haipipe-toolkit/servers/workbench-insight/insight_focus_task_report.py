"""A Task's Report on the focus page, one question read four ways: its Answer (figures, tiles, what it cites),
its Segments, Across segments, and its Plan; and the Task's question map."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from live import insight_plan_c as P
from live import insight_views as V
from live.frame import esc, rel
from live.ui_parts import _kv
from live.insight_view_parts import _pill, _section, _side_tabs
from live.insight_focus_parts import (
    is_job, _session, _pop, _big, _jlink, _pair, _written, _page_word, _cap1, draw_map, _in_job, _writing)


def _task_mindmap(tdir: Path, root: Path):
    """A Task's MindMap (round 2: "each Run leaf says what it found, not its name"): the answer; each segment and what its
    Run found (a cite-only question: each answer it cites); then what each check said."""
    def build():
        x = _task_x(tdir, root)
        t = x["t"]
        fm = t["face"]
        said = str(fm.get("answer") or "").strip()
        last = None if said else _last_answer(x)
        answer = said or (f'[last Job] {last[1]["face"]["answer"]}' if last else
                          f'Its page is {"being written" if _writing(t) else "still to write"}')
        branches = [("The answer", [answer])]
        if _cite_only(x):
            branches.append(("What it cites", [f'[{c["qid"]}] {_qlabel(x, c).split(" · ", 1)[-1]}: '
                                               f'{c["face"].get("answer") or "its page is still to write"}'
                                               for c, via in _plan_cites(x)]))
        else:
            from live import focus_page as FP
            takes = fm.get("takeaways") if isinstance(fm.get("takeaways"), dict) else {}
            leaves = []
            for h in sorted(t["hard"], key=lambda h: h["run"]):
                cut = str(h.get("partition") or h["run"].split("_", 1)[-1])
                st = str(h.get("status") or "planned").lower()
                found = (str(takes.get(cut) or "").strip() if st == "ok" else "") or (
                    FP.run_headline(Path(h["path"])) if st == "ok" else
                    str(h.get("reason") or "refused: too thin to answer") if st == "refused" else "⬜")
                leaves.append(f"[{cut}] {found or 'ran; its page says what it found'}")
            branches.append(("By segment", leaves))
        checks = []
        if str(fm.get("check") or "").startswith(("✅", "↩")):
            checks.append(f'[page check] {"passed " + str(fm["check"]).lstrip("✅ ") if str(fm["check"]).startswith("✅") else "returned: " + str(fm["check"]).lstrip("↩ ")}')
        verdict, line, _ = _aligned(t)
        if verdict:
            checks.append(f"[alignment] {verdict}" + (f": {line}" if line else ""))
        branches.append(("Its checks", checks))
        return draw_map(tdir, root, branches, "Nothing to map yet.")
    return build


# ── a Task's Report and Work (b11 j01 s57, s58): Answer · Changes · Method ────────────────────────────────────────────
# plain words; By segment is a section of Answer (its own button held one section), Changes is the Job's word
TASK_VIEWS = (("answer", "Answer"), ("across-jobs", "Changes"), ("plan", "Method"))


def is_task(folder: Path) -> bool:
    return bool(P.TASK_NAME.match(folder.name)) and is_job(folder.parent)


def _task_x(tdir: Path, root: Path) -> dict:
    jdir = tdir.parent
    b, j = P.board(jdir.parent), P.job(jdir)
    t = next((t for t in j["tasks"] if t["name"] == tdir.name), P.task(tdir))
    q = P.question_of(b["prototype"], j["release"], t["qid"])
    return {"b": b, "j": j, "t": t, "q": q, "root": root, "folder": rel(tdir, root), "session": _session(jdir),
            "jfolder": rel(jdir, root)}


def _state(t: dict) -> str:
    return str(t["face"].get("answer-status") or "").lower()


def _cited(x: dict) -> list:
    """The Tasks of its Job a page cites, `(K01 · t05)`, in order: what a question with no Run of its own rests on."""
    page = x["t"].get("page")
    text = Path(page).read_text(encoding="utf-8") if page and Path(page).is_file() else ""
    by = {t["name"].split("_", 1)[0]: t for t in x["j"]["tasks"]}
    return [by[n] for n in dict.fromkeys(m.group(2) for m in V.CITE.finditer(text)) if n in by]


def _blank(png: Path) -> bool:
    """A Run's figure whose table holds only zeros (every column complete, 0% missing): it says nothing a number
    does not, so the page says the number instead (round 1, D01: "a key-number tile, not the all-zero chart")."""
    m = re.match(r"^fig_(?:E\d+_)?(.+?)(?:_\d+)?$", png.stem)
    table = png.parent / f"{m.group(1)}.csv" if m else None
    if not table or not table.is_file():
        return False
    try:
        with table.open(encoding="utf-8", newline="") as fh:
            vals = [float(v) for row in csv.DictReader(fh) for v in row.values() if re.fullmatch(r"-?\d+(\.\d+)?", str(v or ""))]
    except (OSError, ValueError):
        return False
    return bool(vals) and all(v == 0 for v in vals)


def _figures(x: dict, run: dict | None = None, keep_blank: bool = False) -> list:
    """The page's figures, first one first: an Executive page's `figures:` (drawn into the Board's delivery), else the
    figures its ok Runs drew, the full segment's first (one Run's only, with `run`); an all-zero chart left out unless
    `keep_blank` (a Data page shows it under its tiles, round 2: "move the missing by column figure into The answer").
    [(png, caption)]."""
    t, j, b = x["t"], x["j"], x["b"]
    figs = [s for s in t["face"].get("figures") or [] if isinstance(s, dict)]
    if figs and run is None:
        part = b["path"] / "delivery" / j["name"]
        return [(V._fig_png(part, j, t["qid"], s.get("name")), str(s.get("title") or s.get("name") or ""))
                for s in figs if V._fig_png(part, j, t["qid"], s.get("name")).is_file()]
    ok = [run] if run is not None else sorted(
        (h for h in t["hard"] if str(h.get("status")) == "ok"),
        key=lambda h: (str(h.get("partition") or "") not in ("full", V.OVERALL), h["run"]))
    name = lambda p: FIG_NAME.sub("", p.stem).replace("_", " ")
    return [(p, f'{name(p)} · {h.get("partition") or h["run"]}')
            for h in ok if str(h.get("status")) == "ok" for p in sorted((Path(h["path"]) / "result").glob("fig_*.png"))
            if keep_blank or not _blank(p)]


FIG_NAME = re.compile(r"^fig_(?:E\d+_)?")
TILE_WORDS = {"n_rows": "rows", "n_cols": "columns", "n_days": "days", "first_day": "first day", "last_day": "last day"}


def _tiles(x: dict) -> str:
    """A Data page's key numbers as tiles (round 1, D01): its whole-extract Run's counts (a flat JSON it wrote) and the
    most any column is missing; '' when its Runs wrote none."""
    full = next((h for h in x["t"]["hard"] if str(h.get("status")) == "ok"
                 and (h.get("partition") or "") in ("full", V.OVERALL)), None)
    if x["t"]["qid"][:1] != "D" or full is None:
        return ""
    res = Path(full["path"]) / "result"
    nums = []
    for f in sorted(res.glob("*.json")):
        try:
            got = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(got, dict):
            nums += [(f"{v:,}" if isinstance(v, int) else str(v), TILE_WORDS.get(k, k.replace("n_", "").replace("_", " ")))
                     for k, v in got.items() if isinstance(v, (int, float, str)) and len(str(v)) <= 12]
    for f in sorted(res.glob("*.csv")):
        try:
            with f.open(encoding="utf-8", newline="") as fh:
                pct = [float(r["null_pct"]) for r in csv.DictReader(fh) if r.get("null_pct") not in (None, "")]
        except (OSError, ValueError, KeyError):
            continue
        if pct:
            nums.append((f"{max(pct):g}%", "missing, the most in any column"))
    return ('<div class=in-card>' + "".join(f'<div><b>{esc(a)}</b><span>{esc(k)}</span></div>' for a, k in nums) + '</div>') if nums else ""


def _sourced(x: dict) -> str:
    """The page's sourced facts: the bullets of its first section, each with its source (a `(K01 · t05)` opens that
    Task's page), as the face holds them (round 1: "the three sourced facts under the answer")."""
    from live.page_reader import markdown_html
    secs = V._sections(x["t"].get("page"))
    for _, md in secs:
        items = [ln for ln in md.splitlines() if ln.startswith("- ")]
        if items:
            html_ = V._cites(markdown_html("\n".join(items)), x["j"], x["root"])
            return html_.replace("<ul>", "<ul class=in-facts>", 1)
    return ""


def _cite_only(x: dict) -> bool:
    """A question with no Run of its own (Wisdom, Executive): it answers from the pages it cites."""
    return x["t"]["qid"][:1] not in V.RUN_LEVELS and not x["t"]["hard"]


def _plan_cites(x: dict) -> list:
    """[(Task, through)]: the questions this one's plan cites, in its Job, then what those rest on (through which);
    then any its written page cites beyond the plan (round 1, W01: "fill What it cites from the plan's needs")."""
    by = {t["qid"]: t for t in x["j"]["tasks"]}

    def cites_of(q):
        return [str(n["from"]).split(".")[0] for n in V._needs(q) if n.get("kind") in ("cite", "reuse")
                and isinstance(n.get("from"), str) and re.match(r"^[DIKWX]\d+", str(n["from"]))]
    out, seen = [], {x["t"]["qid"]}
    for c in cites_of(x["q"]):
        if c in by and c not in seen:
            out.append((by[c], ""))
            seen.add(c)
    for t, _ in list(out):
        for c in cites_of(P.question_of(x["b"]["prototype"], x["j"]["release"], t["qid"])):
            if c in by and c not in seen:
                out.append((by[c], t["qid"]))
                seen.add(c)
    for t in _cited(x):
        if t["qid"] not in seen:
            out.append((t, ""))
            seen.add(t["qid"])
    return out


def _qlabel(x: dict, t: dict) -> str:
    """A question by its id and its words, `I01 · outcome by arm`, never its id alone (round 1)."""
    q = V._spec(P.question_of(x["b"]["prototype"], x["j"]["release"], t["qid"]))
    return f'{t["qid"]} · {q.get("name") or t["name"].split("_", 2)[-1].replace("-", " ")}'


def _answer_pop(t: dict, root: Path, words: str) -> str:
    return _pop("/_board/insight-run?answer=" + rel(Path(t["path"]), root), f'{t["name"]} · the page', esc(words) + " ↗")


def _aligned(t: dict) -> tuple:
    """(verdict, its one line, its pass) of the Task's alignment check, from its newest pass; ('', '', None) without."""
    run = next((r for r in t["soft"] if "alignment" in r["run"]), None)
    passes = sorted((Path(run["path"]) / "passes").glob("*/pass.md")) if run else []
    if not passes:
        return "", "", None
    text = passes[-1].read_text(encoding="utf-8", errors="ignore")
    verdict = text.lstrip().split("\n", 1)[0].lstrip("# ").strip()
    m = re.search(r"(?ms)^## Summary\s*\n(.*?)(?=^## |\Z)", text)
    line = re.split(r"(?<=[.!?])\s+", " ".join((m.group(1) if m else "").split()), maxsplit=1)[0]
    return verdict, line, passes[-1]


def _answer_word(t: dict) -> str:
    """The Answer bar's state, each check named (round 1: "page checked · aligned", never a bare "checked")."""
    words = ["being written" if _writing(t) and not _written(t) else _page_word(t)]
    if str(t["face"].get("check") or "").startswith("✅"):
        words.append("page checked")
    verdict = _aligned(t)[0]
    if verdict:
        words.append(verdict)
    return " · ".join(words)


def _last_answer(x: dict) -> tuple | None:
    """(Job, Task) of the newest Job before this one whose page answers the same question: what stands while this
    Job's page is written (round 2, W01: "the last Job's counsel in the headline slot, marked last Job")."""
    jobs = x["b"]["jobs"]
    me = next((i for i, j in enumerate(jobs) if j["name"] == x["j"]["name"]), len(jobs))
    for j in reversed(jobs[:me]):
        t = next((t for t in j["tasks"] if t["qid"] == x["t"]["qid"]), None)
        if t and _written(t):
            return j, t
    return None


def _t_answer(x: dict) -> str:
    """Answer: the answer as the view's headline (the bar stays closed, round 1: settled), then the answer's bar: what
    its one segment adds, its lead picture (a Data page its key numbers, then its figure under them), its sourced facts,
    its page; then how sure it is and what it rests on, each question by its words. A page still to write heads the
    view with the last Job's answer, marked "last Job" (round 2, W01), never with a status line."""
    t, root = x["t"], x["root"]
    fm = t["face"]
    said = str(fm.get("answer") or "").strip()
    last = None if said else _last_answer(x)
    now = "being written" if _writing(t) else "still to write"
    if said:
        head = _big(said)
    elif last:
        head = (_big(str(last[1]["face"]["answer"]))
                + f'<p class=in-sub>{_pill("last Job")} {_jlink(last[0], root)}\'s answer; this Job\'s page is {now}.</p>')
    else:
        head = _big(f"Its page is {now}")
    takes = fm.get("takeaways") if isinstance(fm.get("takeaways"), dict) else {}
    under = (f'<p class=in-sub>{esc(next(iter(takes.values())))}</p>'     # the cross takeaway under the verdict (K01)
             if len(takes) == 1 and str(next(iter(takes.values()))).strip() != said else "")
    tiles = _tiles(x)
    figs = _figures(x, keep_blank=bool(tiles))          # a Data page: its figure under its tiles (round 2, D01)
    lead = figs[0] if figs else None
    first = "" if not lead else (
        f'<figure class=in-fig><a href="/{esc(rel(lead[0], root))}" target=_blank rel=noopener data-pop="{esc(lead[1])}">'
        f'<img src="/{esc(rel(lead[0], root))}" alt="{esc(lead[1])}" loading=lazy></a>'
        f'<figcaption>{esc(lead[1])}</figcaption></figure>')
    thumbs = "".join(f'<a class=ov-thumb data-pop="{esc(c)}" href="/{esc(rel(p, root))}" target=_blank rel=noopener>'
                     f'<img src="/{esc(rel(p, root))}" alt="" loading=lazy><span>{esc(c)}</span></a>' for p, c in figs[1:])
    cites = _plan_cites(x) if _cite_only(x) else []
    if said:
        body = (under + tiles + first + (V.OV_CSS + f'<div class=ov-thumbs>{thumbs}</div>' if thumbs else "")
                + _sourced(x) + f'<p>{V._page_link(t, root)}</p>')
    elif last:                                      # what it rests on is How sure's and By segment's (round 2, W01)
        body = (f'<p class=in-sub>This Job\'s page is {now}; until then {_jlink(last[0], root)}\'s answer stands: '
                f'{_answer_pop(last[1], root, "its page")}</p>')
    else:
        body = (f'<p class=in-sub>Its page is {now}, from the answers it cites.</p>' if cites
                else '<p class=in-sub>Its Runs come first; then its page.</p>')
    big = _section("⚓ The answer", body, _answer_word(t))
    ok = [h for h in t["hard"] if str(h.get("status")) == "ok"]
    plan = [c for c, via in (_plan_cites(x) if not cites else cites) if not via]
    rests = ", ".join([V._run_link(h, root, f'the {h.get("partition") or h["run"]} segment') for h in ok]
                      + [_answer_pop(c, root, _qlabel(x, c)) for c in plan]) or "its Runs, once they run"
    sure = str(fm.get("how-sure") or "").strip() or ("once its page is written" if not said else "not said on its page")
    return head + big + _t_cuts(x) + _section("🎯 How sure", _kv([("how sure", esc(sure)), ("rests on", rests)]),
                                              "✅" if str(fm.get("check") or "").startswith("✅") else "⬜")


def _power(h: dict) -> str:
    """A segment's power, in words: its card's `power:` and, when its Run wrote partition_power.csv, the smallest gap it
    can see (the minimum detectable effect, in points)."""
    said = str(h.get("power") or "")
    f = Path(h.get("path") or "") / "result" / "partition_power.csv"
    mde = ""
    if f.is_file():
        try:
            with f.open(encoding="utf-8", newline="") as fh:
                row = next(csv.DictReader(fh), {})
            mde = f'can see a gap of {float(row["mde"]):.0f} points or more' if row.get("mde") else ""
        except (OSError, ValueError, KeyError):
            mde = ""
    return " · ".join(w for w in ("enough" if said == "ok" else said, mde) if w) or "—"


CUT_WORD = {"ok": "answered", "refused": "refused", "failed": "failed", "planned": "planned", "running": "running"}


def _t_cuts(x: dict) -> str:
    """By segment: a side tab per segment (round 1, I01: "side tabs, one per segment, a planned segment says planned"), each its
    takeaway, its figure, its Run and its power; a question with no Run of its own (Wisdom, Executive) keeps the view's
    name and shows what it cites instead, each answer with its page."""
    t, root = x["t"], x["root"]
    fm = t["face"]
    if _cite_only(x):
        cites = _plan_cites(x)
        return _section("🔗 What it cites", _cite_chain(x, cites) if cites else
                        "<p class=in-sub>Its method names the answers it will cite.</p>", _gather_word(x) if cites else "cites none yet")
    takes = fm.get("takeaways") if isinstance(fm.get("takeaways"), dict) else {}
    hard = sorted(t["hard"], key=lambda h: h["run"])
    items, panels = [], []
    for h in hard:
        cut = str(h.get("partition") or h["run"].split("_", 1)[-1])
        st = str(h.get("status") or "planned").lower()
        take = str(takes.get(cut) or "").strip()
        figs = _figures(x, h) if st == "ok" else []
        pics = "".join(f'<figure class=in-tab-fig><a href="/{esc(rel(p, root))}" data-pop="{esc(c)}" target=_blank rel=noopener>'
                       f'<img src="/{esc(rel(p, root))}" alt="{esc(c)}" loading=lazy></a></figure>' for p, c in figs[:2])
        n = h.get("n")
        facts = [("Run", _pop(V.run_url(h["path"], root), h["run"], esc(f'{h["run"]} {V.MARK.get(st, "·")}'))),
                 ("power", esc(_power(h)) if st == "ok" else "—"), ("rows", esc(f"{n:,}" if isinstance(n, int) and n else "—"))]
        if st == "planned":
            take = take or "Its Run is planned: launch it in Work › Answer."
        elif st == "refused":
            take = take or str(h.get("reason") or "Refused: too thin to answer.")
        items.append((cut, CUT_WORD.get(st, st)))
        panels.append((f'<p class=in-sub>{esc(take)}</p>' if take else "") + pics + _kv(facts))
    ran = sum(str(h.get("status")) in V.FINAL for h in hard)
    if not hard:
        return _section("🔲 By segment", "<p class=in-sub>Its Runs are opened with its Job.</p>", "to launch")
    return _section("🔲 By segment", _side_tabs("cut", items, panels), V.far(ran, len(hard), "ran", "not run yet"))


def _cite_word(c: dict) -> str:
    """One cited question's state, one word from one source (round 2, X01: "four state words for one step"): cited once
    its page in this Job is written, else what it waits on."""
    return "cited" if _written(c) else f"waits on {c['qid']}'s page"


def _gather_word(x: dict) -> str:
    """Gathering what a page cites, in that same word: cited when every question it cites directly is, else the first
    it waits on (the chain row, Work · By segment and What it cites all read this)."""
    direct = [c for c, via in _plan_cites(x) if not via]
    return next((_cite_word(c) for c in direct if not _written(c)), "cited") if direct else "cites none yet"


CHAIN_CSS = """<style>.in-chain{display:flex;flex-direction:column;gap:10px;margin:2px 0 6px}
.in-chain .row{display:flex;flex-wrap:wrap;align-items:stretch;gap:6px 8px}
.in-chain .node{flex:1 1 220px;max-width:380px;border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:var(--paper);
 font-size:13.5px;line-height:1.45}.in-chain .node b{display:block;font-size:14px;margin:0 0 2px}
.in-chain .node .pb-pill{margin-top:4px}.in-chain .to{align-self:center;color:var(--muted);font-size:18px}
.in-chain .to .dn{display:none}
@media(max-width:600px){.in-chain .row{flex-direction:column}.in-chain .node{max-width:none;flex:none}
 .in-chain .to .rt{display:none}.in-chain .to .dn{display:inline}.in-chain .to{align-self:flex-start;padding-left:14px}}</style>"""


def _cite_chain(x: dict, cites: list) -> str:
    """What a page cites drawn as a chain (round 2, W01: "K01 → I01"): a row per question it cites, then the questions
    that one rests on, each a card with its answer and its state word."""
    root = x["root"]

    def node(c, word):
        return (f'<div class=node><b>{_answer_pop(c, root, _qlabel(x, c))}</b>'
                f'{esc(str(c["face"].get("answer") or "its page is still to write"))}<br>{_pill(word)}</div>')
    arrow = '<span class=to title="rests on"><span class=rt>→</span><span class=dn>↓</span></span>'
    rows = []
    for c, via in cites:
        if via:
            continue
        under = [d for d, v in cites if v == c["qid"]]
        rows.append('<div class=row>' + node(c, _cite_word(c))
                    + "".join(arrow + node(d, f"under {c['qid']}") for d in under) + '</div>')
    return CHAIN_CSS + f'<div class=in-chain>{"".join(rows)}</div>'


ACROSS_CSS = """<style>.in-across .st-m{display:none}
@media(max-width:600px){.in-across .st-m{display:block;margin:3px 0 0}.in-across td.st{display:none!important}}</style>"""


def _t_across(x: dict) -> str:
    """This question in each Job: the Job, its answer, its status; under 600 px the status sits under the Job's name
    (round 2: "Across Jobs status cut off at 390 px")."""
    b, t, root = x["b"], x["t"], x["root"]
    rows = []
    for j in b["jobs"]:
        word, tt = _in_job(j, t["qid"])
        if word == "not asked":
            continue
        st = V._st(word)
        rows.append(f'<tr><td>{_jlink(j, root, _pair(j))}<span class=st-m>{st}</span></td>'
                    f'<td>{esc(str((tt or {}).get("face", {}).get("answer") or "—"))}</td><td class=st>{st}</td></tr>')
    grid = (ACROSS_CSS + '<table class="wf-table in-ct in-across"><thead><tr><th>Job</th><th>answer</th><th>status</th></tr>'
            f'</thead><tbody>{"".join(rows)}</tbody></table>')
    return _section("🔁 Changes", grid if rows else "<p class=mut>Only this Job asks it so far.</p>",
                    f"in {len(rows)} Jobs" if len(rows) > 1 else "this Job only")


def _delivers(spec: dict) -> str:
    """What the question delivers and the test each part must meet, read from its question file alone
    (haipipe-insight ref/deliverables.py): a row per live need, then the Task page. "" for an older question file."""
    if not spec.get("id") or not isinstance(spec.get("needs"), dict):
        return ""
    try:
        from live.instance_reader import _tools
        _tools()
        import deliverables as DL
        d = DL.deliverables(spec)
    except Exception:  # noqa: BLE001 · the list is an extra: the section still shows the needs
        return ""
    rows = []
    for r in d["needs"]:
        if r["kind"] == "compute":
            figs = {f["table"]: f["kind"] for f in r["figures"]}
            gives = "<br>".join(esc(t) + (f' <span class=mut>+ {esc(figs[t])} figure</span>' if t in figs else "")
                                for t in r["tables"])
        else:
            gives = f'<span class=mut>{"from " + esc(r["source"]) if r["kind"] == "cite" else "a reading on the page"}</span>'
        rows.append(f'<tr><td><b>{esc(r["id"])}</b> {esc(r["what"])}</td><td>{gives}</td><td>{esc(r["test"])}</td></tr>')
    rows.append(f'<tr><td><b>Answer</b></td><td>{"<br>".join(esc(a) for a in d["answer"])}</td><td>{esc(d["may_say"])}</td></tr>')
    return ('<table class="wf-table in-ct"><thead><tr><th>Need</th><th>Delivers</th><th>Counts when</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


def _t_plan(x: dict) -> str:
    q, t, root = x["q"], x["t"], x["root"]
    may = next((m for lv, _, m in V.LEVELS if lv == t["qid"][:1]), "")
    spec = V._spec(q)
    needs = V._needs(q)
    need = "<br>".join(esc(str(n.get("need") or n.get("ask") or n.get("what") or n.get("kind") or ""))
                       + (f' <span class=mut>{esc(V._goes(n))}</span>' if V._goes(n) else "") for n in needs) or "—"
    steps = " · ".join(dict.fromkeys(V.STEP.get(str(n.get("kind")), _cap1(str(n.get("kind") or "step"))) for n in needs))
    q = dict(q, question=q.get("question") or spec.get("ask") or spec.get("question") or "")
    table = _delivers(spec)
    return _section("📋 Needs", _kv([("question", esc(q.get("question") or "—")), ("need", "" if table else need),
                                     ("steps", esc(steps or "—")), ("may say", "" if table else esc(may.replace("may say: ", ""))),
                                     ("agreed", esc(str(q.get("agreed") or "not yet")))]) + table
                    + (f'<p>{_pop(V.open_url(Path(q["file"]), root), t["qid"], "the question file ↗")}</p>' if q.get("file") else ""),
                    "agreed" if q.get("agreed") else "to agree")


TASK_PARTS = {"answer": _t_answer, "across-jobs": _t_across, "plan": _t_plan}
