"""b17 s32 · Work element UI: s32-work-element-ui.excalidraw, the work theme's element gallery (b03's
s32-element-ui, cut to one theme): every kind of element the work theme draws, as it draws it today on the
frame (/_board/workbench at its Block, Job and Task levels, every Space and view) and on its old pages (the
old work Block page, its Run page, a Task's Page workbench page; flagged OLD), then as planned (b03's s11 work
Block screens and this Block's s01 Job and Task rows), and beside each element a "· proposed" frame: the
unified look (b03's picks hold), why, a green line for what changed and a red line for what is open.

Two steps, as b03's s32:

    uv run --no-project --with playwright --with pillow python build_s32_work_element_ui.py --shoot [--base http://127.0.0.1:5851]
        (--no-project: inside the SPACE, uv would otherwise build the SPACE's own environment)
        walks the work theme on the frame at a work Block, one of its Jobs and one of its Tasks (plus a Task with
        draft/ and workflow/), every Space and every view, then the old pages; screenshots each element version
        into shots/<element>__NN.png, writes where it was seen and its computed style into shots/facts.json, and
        every Runs-panel button met (its words, where) into facts.json's "_buttons".
    python build_s32_work_element_ui.py
        draws the gallery from shots/: per element a frame of versions (old ones flagged OLD in red, a red dashed
        box), the planned screen under them, and beside it a "· proposed" frame; then the theme's own elements,
        the Theme elements list, the buttons with no Run name, and Pick. Marks are kept on rebuild (canvas.write).

The picture helpers (picture, style_line, PICK_JS) are b03's, imported from its s32 builder; the planned screens
are drawn by b03's _build/screens.py (the s11 work Block screens, WORK_BLOCK) and from this Block's s01 rows.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import urllib.parse as U
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "shots"
TOOLS = HERE.parents[3]
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
B03S = TOOLS / "designs" / "b03_project_workbench" / "studio"
sys.path.insert(0, str(B03S / "s32-element-ui"))
import build_s32_element_ui as B  # noqa: E402  (b03's gallery: picture, style_line, PICK_JS; it loads L and canvas)
import screens as SC  # noqa: E402  (b03 _build/: the workbench screens, drawn large)
import run_names as RN  # noqa: E402  (b03 _build/: each button's Run name, read off the server code)
import level_views as LV  # noqa: E402  (b03 s01: the Task tab's planned screens per variant)

L, canvas = B.L, B.canvas
INK, RED, GREEN, MONO = canvas.INK, canvas.RED, canvas.GREEN, L.MONO
text, base = L.text, L.base
MAX_H, CARD_W = B.MAX_H, B.CARD_W
DATE = "261008"


def frame_url(folder: str, space: str = "", sub: str = "") -> str:
    query = {"path": folder}
    if space:
        query["space"] = space
    if sub:
        query["sub"] = sub
    return "/_board/workbench?" + U.urlencode(query)


# ── what is shot ────────────────────────────────────────────────────────────────────────────────
# a work Block with Questions, report Pages, three Jobs, each a Task with scripts/, runs/, notebooks/ and
# CODE_REVIEW.md; and a Task of another Block that also holds draft/ and workflow/
BLOCK = "examples-3-model/Project-Algorithm-Design/tasks/b18_smart_dynamic_regime"
JOB = BLOCK + "/j02_smart_design"
TASK = JOB + "/t01_design_size"
OTASK = "examples-1-data/Project-Data-DrFirst-Raw2AIData/tasks/b00_A_sms_rawdata/j51_smsr1all_v250218_raw/t01_load_cohort_parquet"
SPACES = ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")
LEVELS = [("block", "Block · a work Block (b18)", BLOCK),
          ("job", "Job · j02", JOB),
          ("task", "Task · j02 › t01", TASK),
          ("otask", "Task · one with draft/ and workflow/ (b00 › j51 › t01)", OTASK)]
LEVEL_OF = {k: lbl.split(" · ")[0] for k, lbl, _ in LEVELS}
TASK_MD = TASK + "/" + TASK.rsplit("/", 1)[1] + ".md"
OLD_BOARD = "/_board/work-board?" + U.urlencode({"path": BLOCK + "/board.md"})
# the old pages: (key, label, url, why it is old). "from:<url>|<css>" is the first such link on that page
OLD_PAGES = [
    ("old-board", "the old work Block page (/_board/work-board)", OLD_BOARD,
     "old page: the work theme draws on the frame now (work_theme.py); this page retires"),
    ("old-run", "one Run on the old work Block page (?task=…&run=…), from a Run id on a Question row",
     "from:" + OLD_BOARD + "|a.bj-run.idtag",
     "old item page: a Run's result opens outside the frame, not in its pop-out"),
    ("old-draft", "a Task's Page workbench page (/_board/draft), the old page's Task Page link",
     "/_board/draft?" + U.urlencode({"path": TASK_MD, "file": TASK_MD[len(BLOCK) + 1:]}),
     "old page: a Task's Page views are the frame's Task Spaces now; this page retires"),
]
OLD_WHY = {k: why for k, _, _, why in OLD_PAGES}
OLD_LABEL = {k: lbl for k, lbl, _, _ in OLD_PAGES}
# the old work Block page: its Spaces and the views (.wtab) of each
OLD_BOARD_SPACES = {"scope": ["Block", "Questions", "Resources", "RoadMap Draw"], "task": ["Questions"],
                    "check": ["Runs", "Tasks", "Reports"], "delivery": ["Reports"]}
OLD_DRAFT_SPACES = ["draft", "evidence", "delivery"]

# the elements. mode "level": one card per level (at the Space given) and per old page; "space": one card per
# level × Space; "views": one card per Space that has views; "distinct": every view of every page is walked and
# each look met is one card (its first place, and the count of places); "item": the listed places (ITEMS)
ELEMENTS = [
    dict(key="tabs", title="1 · Top tabs", what="the rows you choose a level and a Space from", mode="level",
         space="Description", frame="nav.levels|nav.spaces", old={"old-board": "nav.spaces", "old-draft": "div.spaces"}),
    dict(key="views", title="2 · View row (third row)", what="the views of the open Space", mode="views",
         frame="nav.subs", old={"old-board": ".pane.on .wtabs", "old-draft": ".draft-mode-switcher,.space-tabs"}),
    dict(key="report", title="3 · Audience Report: the Question rows", what="one Question with its work and its report",
         mode="distinct", only=("Audience Report",), frame=[".q-row:not(.q-head-row)", ".space-main > p"],
         old={"old-board": ["div.hl-row"]}),
    dict(key="space", title="4 · The Space body", what="the open Space's box, its first screen (its first view)",
         mode="space", frame=".space-main", old={"old-board": ".pane.on .space-main", "old-draft": ".space-main"}),
    dict(key="table", title="5 · Tables", what="rows of items in a table", mode="distinct",
         frame=["table"], old={"old-board": ["table"], "old-draft": ["table"]}),
    dict(key="cards", title="6 · Rows and cards", what="one item, closed or open", mode="distinct",
         frame=["details.topic", "div.topic", "details.q-more", "article.card", "div.card"],
         old={"old-board": ["details.bj-tr", "article.card", "details.draw", "details.wk", "details.q-more"],
              "old-draft": ["div.card", "details.rd-card"]}),
    dict(key="runs", title="7 · Disk · Runs panel", what="the files behind the open Space, its run types and their Runs",
         mode="level", space="Audience Report", frame="section.runs-panel",
         old={"old-board": ".pane.on section.runs-panel", "old-draft": "section.runs-panel"}),
    dict(key="tags", title="8 · Tags and pills", what="a state, a kind, an id or a count on an item", mode="distinct",
         frame=[".rp-tags", ".pill", ".chip", ".tag", "span.kind", ".idtag", ".st-ok", ".st-warn"],
         old={"old-board": [".idtag", ".pill", "span.kind", ".rp-tags", ".rp-label"],
              "old-draft": [".pill", ".chip", ".tag", ".badge", ".space-count"]}),
    dict(key="header", title="9 · Page header", what="the title line at the top", mode="level", space="Audience Report",
         frame="header", old={"old-board": "header", "old-draft": "h1|.wb-band", "old-run": "h1,h2,body"}),
    dict(key="item", title="10 · One item's display", what="one Task, one Run, one report: the item itself", mode="item"),
    dict(key="own", title="11 · The work theme's own elements", what="what only the work theme draws, each where it lives",
         mode="item"),
]
SPOT = frame_url
ITEMS = {      # 10 and 11: (label, url, selector, why old or "")
    "item": [
        ("Task › Description › Scope: a Task opens as the Task tab", SPOT(TASK, "Description"), ".space-main", ""),
        ("Task › Runs › All: its hard Runs, a row each (no pop-out)", SPOT(TASK, "Runs"), ".space-main", ""),
        ("Block › Audience Report: a report's ↗ opens the Page reader in the pop-out",
         "/_board/page?path=" + U.quote("/" + BLOCK + "/reports/q03_plan_menu_size/q03_plan_menu_size.md", safe=""),
         "main,body", ""),
        (OLD_LABEL["old-run"], "old-run", "main,body", OLD_WHY["old-run"]),
        (OLD_LABEL["old-draft"], "old-draft", ".space-main,main,body", OLD_WHY["old-draft"]),
    ],
    "own": [
        ("Block › Work Details: the Jobs (Job · title · Tasks)", SPOT(BLOCK, "Work Details"), ".space-main", ""),
        ("Job › Work Details: the Tasks (Task · title · Runs)", SPOT(JOB, "Work Details"), ".space-main", ""),
        ("Job › Description: a Job with no face file", SPOT(JOB, "Description"), ".space-main", ""),
        ("Task › Description › Plan: the face's Plan section", SPOT(TASK, "Description", "Plan"), ".space-main", ""),
        ("Task › Audience Report › Report: the report is its face", SPOT(TASK, "Audience Report", "Report"), ".space-main", ""),
        ("Task › Audience Report › Draft: the Page's Draft view, embedded (not draft/)", SPOT(OTASK, "Audience Report", "Draft"), ".space-main", ""),
        ("Task › Work Details › Code: scripts/ · workflow/ · tests/", SPOT(OTASK, "Work Details", "Code"), ".space-main", ""),
        ("Task › Work Details › Review: CODE_REVIEW.md", SPOT(TASK, "Work Details", "Review"), ".space-main", ""),
        ("Task › Work Details › Notebooks (generated)", SPOT(TASK, "Work Details", "Notebooks"), ".space-main", ""),
        ("Task › Work Details › Evidence: a Page view, embedded", SPOT(TASK, "Work Details", "Evidence"), ".space-main", ""),
        ("Task › Runs › Page Runs: a Page view, embedded", SPOT(TASK, "Runs", "Page Runs"), ".space-main", ""),
        ("Task › Delivery › Lanes: a Page view, embedded", SPOT(TASK, "Delivery", "Lanes"), ".space-main", ""),
        ("the old work Block page › Task › Questions: Question │ Work │ Report with the Job → Task → Run tree",
         "old-board#task/Questions", ".pane.on .space-main", OLD_WHY["old-board"]),
        ("the old work Block page › Check › Tasks: Plan · Build · Run · Report per Task",
         "old-board#check/Tasks", ".pane.on .space-main", OLD_WHY["old-board"]),
        ("the old work Block page › Check › Runs: every Run of the Block", "old-board#check/Runs", ".pane.on .space-main",
         OLD_WHY["old-board"]),
    ],
}

# the proposed look per element (b03's picks hold: tabs D · E, view row E, the Question cell as the Insight row,
# Disk inside the Runs panel, no tags, every soft Run button named run-<type>-<target>): (url, selector, why,
# changed (green), open (red))
PROPOSALS = {
    "tabs": (SPOT(TASK, "Description"), "nav.levels|nav.spaces",
             ["b03's pick D · E (b03 s32-D01): one button shape for every top row, the open one washed blue",
              "the work theme gives its words only: Work Block · Job ▾ · Task ▾, the six Spaces",
              "drawn by the base frame, so the work theme has no tab code of its own"],
             "kept: the base's D · E tabs at every level",
             "? the Job ▾ and Task ▾ selects list folder names, not grouped by the Job series (j0N · j1N · j5N, s01 Open 7)"),
    "views": (SPOT(TASK, "Work Details"), "nav.subs",
              ["b03's pick E (b03 s32-D02): the tabs' shape, 5px 12px, the open one washed blue",
               "a work Task's views: Scope · Plan | Report · Draft | Code · Review · Notebooks | All · run · build · "
               "report (s13 1, 1d)"],
              "changed: the work theme's own Draft wins over the Page's Draft view (base fix, b03)",
              "? the Page views (Folder · Evidence · Value · Page Runs · Lanes) are still added to every work Task's row"),
    "report": (SPOT(BLOCK, "Audience Report"), ".q-head-row|.q-row:not(.q-head-row)",
               ["one row per Question at every level: Question │ Work │ Report (b03 s04-D04)",
                "the Question cell as the Insight row (b03 s32-D05): label and state dot, the short name, one "
                "sentence, › More",
                "the Work column names the j · t · r each Question reads (Q03)"],
               "kept: the Insight row at Block level (b03 s32-D05)",
               "? a Task's Audience Report › Report is one line (its face), not the row (s13 1b); "
               "the Report cell carries tags"),
    "space": (SPOT(BLOCK, "Audience Report"), ".split",
              ["one content box and one right column, Disk · Runs, for every work Space",
               "the work theme fills the box; it draws no page of its own"],
              "kept: the base's body at Block, Job and Task",
              "? Task › Work Details › Evidence, Runs › Page Runs and Delivery › Lanes embed the old Page workbench "
              "in an iframe, in its own look"),
    "table": (SPOT(JOB, "Work Details"), "table.wf-table",
              ["the base's light table: small grey heads, rows ruled by one line",
               "a Job's Tasks as rows, each with its Plan · Build · Run · Report state (s01 GRID)"],
              "kept: the base table (Jobs, Tasks, Code, Notebooks, Runs)",
              "? a Task row has title and Runs count only, no Plan · Build · Run · Report state; a Block's Jobs "
              "have no series row (j0N · j1N · j5N)"),
    "cards": (SPOT(BLOCK, "Idea Studio"), ".space-main details",
              ["one closed row per item: ▸ name · its facts, opened in place (b03 s32-D06)",
               "the same row for a topic, a Job, a Task, a Run"],
              "kept: the base's topic rows (b03 s32-D06)",
              "? the old page's Job → Task → Run tree (bj-tr) has no home on the frame yet (Work Details › Jobs ▾)"),
    "runs": (SPOT(TASK, "Runs"), "section.runs-panel",
             ["Disk, then Runs, in one panel with one fold (b03 s32-D08)",
              "one row per run type, named by its Run: run-plan-t01, run-build-t01, rNN_<slug> (hard)"],
             "changed: the work Run names carry the Task's tag, run-plan-t01 · run-build-t01 (base fix, b03)",
             "? Block and Job Runs offer only run-<type>-<target>"),
    "tags": ("none:", "",
             ["none: no tags in any theme (b03 s32-D09)",
              "a state is a word (open · ok · failed) or the Question's state dot",
              "an id is plain text where it stands (j02 · t01 · r06_<slug>)"],
             "decided: no tags in the work views (b03 s32-D09)",
             "? to build: {n} kinds drawn today (Report-cell tags, …)"),
    "header": (SPOT(TASK, "Description"), "header",
               ["one line: 📋 Work · the folder; the path on hover", "no band, no links row above the tabs"],
               "kept: one line, no band",
               ""),
    "item": (SPOT(TASK, "Description"), ".space-main",
             ["an item opens in the frame: a Task is the Task tab; a Run (hard rNN_) opens in the pop-out: its card, "
              "ticket, config, result/ and passes (s01 GRID, Run row)",
              "no item page beside the frame: the old Run page and /_board/draft stop being destinations"],
             "proposed: a Task is the Task tab; a Run in the pop-out",
             "? a hard Run's row in Task › Runs opens nothing yet; its result is only on the old page"),
}

CHANGES = ["new topic: the work theme's element gallery, after b03's s32 and b12 · b16's (b03's picks hold)",
           "live from the frame at a work Block, a Job and a Task, every Space and view; the old pages flagged OLD",
           "the planned screen under each element: b03 s11's work Block, this Block's s01 Job and Task rows",
           "the Theme elements list and the buttons with no Run name (asked by b03)",
           "b03 fixed two gaps in the base: a theme's own Draft wins over the Page's; the Run names carry the tag (frames 2, 7)"]


# ── the shoot ───────────────────────────────────────────────────────────────────────────────────
COLLECT_JS = """([sels, scope, ctx]) => {
  const root = scope ? [...document.querySelectorAll(scope)].find(e => e.getBoundingClientRect().width > 4) : document;
  if (!root) return [];
  const folded = e => { for (let d = e.parentElement; d; d = d.parentElement) {
      if (d.tagName === 'DETAILS' && !d.open && !e.closest('summary')?.parentElement?.isSameNode(d)) return true; }
    return false; };
  const out = [], seen = new Set();
  for (const sel of sels) for (const e of root.querySelectorAll(sel)) {
    const r = e.getBoundingClientRect();
    if (r.width < 4 || r.height < 4 || e.closest('dialog') || folded(e)) continue;
    if (e.closest('.runs-panel') && !sel.includes('runs')) continue;          // the panel is its own element
    const ce = getComputedStyle(e);
    const cls = e.tagName.toLowerCase() + '.' + (String(e.className).trim().split(/\\s+/)[0] || '');
    const sig = cls + '|' + ce.fontSize + '|' + ce.borderTopLeftRadius + '|' + ce.paddingTop + ' ' + ce.paddingLeft
                + '|' + ce.borderTopWidth + ' ' + ce.borderTopStyle;
    if (seen.has(sig)) continue;
    seen.add(sig);
    let b = e.getBoundingClientRect();
    if (ctx) { const c = e.closest(ctx); if (c && c.getBoundingClientRect().height < 90) b = c.getBoundingClientRect(); }
    const pad = ctx ? 4 : 0;
    const probe = e.querySelector('button, a, select, th, td, summary') || e, cs = getComputedStyle(probe);
    out.push({sig, x: b.left + scrollX - pad, y: b.top + scrollY - pad, w: b.width + 2 * pad, h: b.height + 2 * pad,
              style: {font: cs.fontSize + ' ' + cs.fontWeight, radius: cs.borderTopLeftRadius,
                      padding: cs.paddingTop + ' ' + cs.paddingLeft, border: cs.borderTopColor, fill: cs.backgroundColor,
                      tag: cls}});
  }
  return out;
}"""
TAG_CTX = "summary,p,li,tr,.q-top,.bj-t,.hl-l,.st-bar"
# every Runs-panel button on the page: its words (the frame's data-label, else its text)
BUTTONS_JS = """() => [...document.querySelectorAll('section.runs-panel .run-type:not(.run-new), .runs-panel .run-type:not(.run-new)')]
  .filter(b => b.getBoundingClientRect().width > 0 || b.closest('.pane'))
  .map(b => (b.dataset.label || b.textContent.replace(/\\s*\\d+\\s*$/, '')).trim())"""


class Shooter:
    def __init__(self, page, base_url):
        self.page, self.base = page, base_url
        self.facts, self.n, self.seen, self.old_urls = {}, {}, {}, {}
        self.buttons = {}                                # button words -> [places]

    def snap(self, box, path):
        """Scroll the box to the top, then clip in the viewport (the frame's 100vh boxes move in a full-page shot)."""
        top = self.page.evaluate("y => { window.scrollTo(0, Math.max(0, y - 8)); return window.scrollY; }", box["y"])
        self.page.wait_for_timeout(120)
        clip = {"x": max(box["x"], 0), "y": max(box["y"] - top, 0), "width": max(min(box["w"], 1490 - max(box["x"], 0)), 1),
                "height": min(max(box["h"], 1), MAX_H)}
        self.page.screenshot(path=str(path), clip=clip)

    def shot(self, ekey, box, place, url, sel, old=""):
        n = self.n.get(ekey, 0) + 1
        name = f"{ekey}__{n:02d}"
        try:
            self.snap(box, SHOTS / f"{name}.png")
        except Exception as exc:                          # off the page: no card
            print(f"{ekey} at {place}: {str(exc).splitlines()[0]}")
            return None
        self.n[ekey] = n
        self.facts[name] = {"element": ekey, "place": place, "url": url, "selector": sel, "old": old,
                            "cut": box["h"] > MAX_H, "seen": [place], **box["style"]}
        return name

    def note_buttons(self, place):
        for words in self.page.evaluate(BUTTONS_JS):
            self.buttons.setdefault(words, [])
            if place not in self.buttons[words]:
                self.buttons[words].append(place)

    def goto(self, url):
        """A frame URL, an old page key (old-board#space/tab, old-draft#space), or a host URL; True when shown."""
        key, _, rest = url.partition("#")
        if key in ("old-board", "old-draft"):
            resp = self.page.goto(self.base + self.old_urls.get(key, dict((k, u) for k, _, u, _ in OLD_PAGES)[key]))
            self.page.wait_for_timeout(1200)
            space, _, tab = rest.partition("/")
            if key == "old-board" and space:
                self.page.evaluate("s => { const b = document.querySelector(`button.space[data-space='${s}']`); if (b) b.click(); }",
                                   space)
                self.page.wait_for_timeout(300)
                if tab:
                    self.page.evaluate("t => { const p = document.querySelector('.pane.on'); if (!p) return;"
                                       " const b = [...p.querySelectorAll('button.wtab')].find(b => b.textContent.trim() === t);"
                                       " if (b) b.click(); }", tab)
            elif key == "old-draft" and space:
                self.page.evaluate("s => { const b = [...document.querySelectorAll('button.space')]"
                                   ".find(b => b.textContent.trim().toLowerCase() === s); if (b) b.click(); }", space)
            self.page.evaluate("document.querySelectorAll('.runs-panel.folded').forEach(p => p.classList.remove('folded'))")
            self.page.wait_for_timeout(400)
            return bool(resp and resp.status == 200)
        url = self.old_urls.get(url, url)
        resp = self.page.goto(self.base + url)
        self.page.wait_for_timeout(700)
        self.page.evaluate("document.querySelectorAll('.runs-panel.folded').forEach(p => p.classList.remove('folded'))")
        self.page.wait_for_timeout(150)
        return bool(resp and resp.status == 200)

    def one(self, sel):
        for alt in sel.split(","):
            box = self.page.evaluate(B.PICK_JS, alt.strip())
            if box:
                return box
        return None

    def distinct(self, el, sels, scope, place, url, old=""):
        ctx = TAG_CTX if el["key"] == "tags" else None
        for box in self.page.evaluate(COLLECT_JS, [sels, scope, ctx]):
            k = (el["key"], box["sig"], bool(old))
            if k in self.seen:
                if place not in self.facts[self.seen[k]]["seen"]:
                    self.facts[self.seen[k]]["seen"].append(place)
                continue
            name = self.shot(el["key"], box, place, url, box["sig"], old)
            if name:
                self.seen[k] = name

    def walk(self):
        """Every frame page (level × Space × view), then every old page, each element taken as its mode says."""
        for lkey, llabel, folder in LEVELS:
            main = lkey in ("block", "job", "task")
            for space in SPACES:
                if not self.goto(frame_url(folder, space)):
                    print(f"{lkey} {space}: not 200")
                    continue
                subs = self.page.evaluate("[...document.querySelectorAll('nav.subs a')].map(a => a.textContent)")
                for i, sub in enumerate(subs or [""]):
                    if i and not self.goto(frame_url(folder, space, sub)):
                        continue
                    url = frame_url(folder, space, sub)
                    place = f"{LEVEL_OF[lkey]} › {space}" + (f" › {sub}" if sub else "") + ("" if main else f" ({llabel})")
                    self.note_buttons(f"the frame · {LEVEL_OF[lkey]} › {space}")
                    for el in ELEMENTS:
                        mode = el["mode"]
                        if mode == "distinct" and (not el.get("only") or space in el["only"]):
                            self.distinct(el, el["frame"], ".space-main", place, url)
                        if not main or i:
                            continue
                        if mode == "level" and space == el["space"] or mode == "space" or mode == "views" and subs:
                            box = self.one(el["frame"])
                            if box:
                                lbl = llabel if mode == "level" else f"{LEVEL_OF[lkey]} › {space}"
                                self.shot(el["key"], box, lbl, url, el["frame"])
        for okey, _, url, why in OLD_PAGES:                 # the old pages
            if url.startswith("from:"):
                src, css = url[5:].split("|", 1)
                self.goto(src)
                found = self.page.evaluate("c => { const a = document.querySelector(c); return a ? a.getAttribute('href') : ''; }", css)
                if not found:
                    print(f"{okey}: no {css} link, skipped")
                    continue
                self.old_urls[okey] = found
            else:
                self.old_urls[okey] = url
            places = ([f"old-board#{s}/{t}" for s, tabs in OLD_BOARD_SPACES.items() for t in tabs] if okey == "old-board"
                      else [f"old-draft#{s}" for s in OLD_DRAFT_SPACES] if okey == "old-draft" else [okey])
            for n, where in enumerate(places):
                if not self.goto(where):
                    print(f"{okey}: not on screen, skipped")
                    break
                space, _, tab = where.partition("#")[2].partition("/")
                first = okey != "old-board" or not space or tab == OLD_BOARD_SPACES[space][0]
                place = OLD_LABEL[okey] + (f" › {space}" + (f" › {tab}" if tab else "") if space else "")
                self.note_buttons(OLD_LABEL[okey].split(" (")[0])
                src = self.old_urls.get(okey, url)
                for el in ELEMENTS:
                    sel = el.get("old", {}).get(okey)
                    if not sel:
                        continue
                    if el["mode"] == "distinct":
                        self.distinct(el, sel, ".pane.on" if okey == "old-board" else None, place, src, why)
                    elif el["mode"] in ("space", "views"):
                        box = self.one(sel) if first else None
                        if box:
                            self.shot(el["key"], box, OLD_LABEL[okey] + (f" › {space}" if space else ""), src, sel, why)
                    elif n == 0:
                        box = self.one(sel)
                        if box:
                            self.shot(el["key"], box, OLD_LABEL[okey], src, sel, why)

    def items(self):
        for ekey, rows in ITEMS.items():
            for label, url, sel, why in rows:
                if not self.goto(url):
                    print(f"{ekey}: {label}: not on screen")
                    continue
                self.page.wait_for_timeout(700)                   # an embedded view loads its iframe
                box = self.one(sel)
                if box:
                    self.shot(ekey, box, label, self.old_urls.get(url.split("#")[0], url), sel, why)

    def proposals(self):
        for key, (url, sel, *_rest) in PROPOSALS.items():
            if url.startswith("none:"):
                continue
            self.goto(url)
            self.page.wait_for_timeout(500)
            box = self.page.evaluate(B.PICK_JS, sel)
            if not box:
                print(f"proposal {key}: {sel} not found")
                continue
            self.snap(box, SHOTS / f"proposed__{key}.png")
            self.facts[f"proposed__{key}"] = {"element": key, "place": "proposed", "url": url, "selector": sel,
                                              "old": "", "cut": box["h"] > MAX_H, "seen": [], **box["style"]}


def shoot(base_url: str) -> None:
    """Shoot into .shots-new/, then swap it in for shots/, so a rebuild meanwhile (make.sh) reads the last set."""
    import shutil
    from playwright.sync_api import sync_playwright
    global SHOTS
    final, SHOTS = SHOTS, HERE / ".shots-new"
    shutil.rmtree(SHOTS, ignore_errors=True)
    SHOTS.mkdir()
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 1100}, device_scale_factor=1)
        s = Shooter(page, base_url)
        s.walk()
        s.items()
        s.proposals()
        browser.close()
    s.facts["_buttons"] = s.buttons
    (SHOTS / "facts.json").write_text(json.dumps(s.facts, indent=1, ensure_ascii=False))
    shutil.rmtree(final, ignore_errors=True)
    SHOTS.rename(final)
    SHOTS = final
    print(f"{len(s.facts) - 1} shots in {SHOTS.relative_to(HERE.parent)}; {len(s.buttons)} buttons met")


# ── the planned screens: b03 s11's work Block (WORK_BLOCK), this Block's s01 Job and Task rows ──────
def _s11():
    spec = importlib.util.spec_from_file_location("b03_s11_builder", B03S / "s11-block-variants" / "build_s11_block_variants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


TD = LV.TASK_DEFAULT
PLAN = {
    "block": {d["space"]: d for d in _s11().WORK_BLOCK},
    "job": {      # this Block's s01 GRID, its Job row: the Job takes the Block's six Spaces
        "Description": dict(space="Description", third=["Scope", "Shared code"], kind="lines",
                            content=["jNN_<job>.md   the Job's face", "goal: the one line this Job delivers",
                                     "state: half · next: <step>", "task_groups: t0N · t1N",
                                     "shared: src/ · sbatch/ · CODE_REVIEW.md"],
                            runs=["Update the Job", "Review the shared code"]),
        "Work Details": dict(space="Work Details", third=["All", "t0N", "t1N"], kind="table",
                             heads=["Task", "Plan · Build · Run · Report", "state"], cols=(0, 420, 820),
                             content=[("t01_<task>", "done · done · done · half", "waits on its report"),
                                      ("t02_<task>", "done · half · — · —", "building"),
                                      ("t03_<task>", "— · — · — · —", "new")],
                             runs=["Add a Task", "Plan its Tasks"]),
        "Runs": dict(space="Runs", third=["All", "plan", "launch", "from below"], kind="table",
                     heads=["Run", "type · writes", "state"], cols=(0, 420, 820),
                     content=[("run-plan-<jNN>", "plan · tNN_ faces", "closed · p01"),
                              ("run-launch-<jNN>", "launch · sbatch/", "open"),
                              ("t01 › r03_<slug>", "from below", "ok")],
                     runs=["Plan its Tasks", "Launch all", "Review the shared code"]),
    },
    "task": {     # b03 s13's work Task (level_views: TASK_DEFAULT, REPORT_GROUPS, WORK_GROUPS, RUN_GROUPS)
        "Description": dict(space="Description", third=["Scope", "Plan"], kind="lines", content=TD["Description"][0],
                            runs=TD["Description"][1]),
        "Audience Report": dict(space="Audience Report", third=LV.REPORT_GROUPS["work Task"], kind="table",
                                heads=["Question", "Work", "Report"], cols=(0, 420, 760), content=TD["Report"][0],
                                runs=TD["Report"][1]),
        "Work Details": dict(space="Work Details", third=LV.WORK_GROUPS["work Task"], kind="lines",
                             content=TD["Code"][0], runs=TD["Code"][1]),
        "Runs": dict(space="Runs", third=LV.RUN_GROUPS["work Task"], kind="lines", content=TD["Runs"][0],
                     runs=TD["Runs"][1]),
        "Delivery": dict(space="Delivery", third=None, kind="lines",
                         content=[ln for group, cards in LV.DELIVERY_CARDS["work Task"]
                                  for ln in [group] + [f"  ▢ {n}   {s}" for n, s in cards]],
                         runs=TD["Delivery"][1]),
    },
}
TABS = {"block": 1, "job": 2, "task": 3}
RUN_POPOUT = ("r03_<slug>  ·  a hard Run (from Task › Runs)",          # s01 GRID, the Run row
              ["run.yaml · rNN_<slug>.sh (the ticket) · config.yaml", "passes: p01 1005 ok · p02 1006 ok",
               "[ result/: metrics · tables · figures · heavy.yaml ]", "  Rerun (a new pass) · Open the Result"])
PLANNED = {      # element -> [(level, Space)] or the Run pop-out
    "tabs": [("task", "Description")], "views": [("task", "Work Details")], "report": [("block", "Audience Report")],
    "space": [("job", "Work Details")], "table": [("block", "Work Details")], "cards": [("block", "Idea Studio")],
    "runs": [("task", "Runs")], "item": [("popout", "")], "own": [("task", "Delivery"), ("job", "Runs")],
}
PLAN_FROM = {"block": "b03 s11 · work Block", "job": "b17 s01 · the Job row", "task": "b03 s13 · work Task"}


def planned_screen(level, space, x, y) -> float:
    """One planned screen at (x, y), as b03's screens.py draws it; its height."""
    if level == "popout":
        h = 72 + sum(168 if r.startswith("[") else 28 for r in RUN_POPOUT[1]) + 20
        SC.window(x, y, SC.PW, h, RUN_POPOUT[0], RUN_POPOUT[1])
        return h
    sp = PLAN[level][space]
    SC.chrome(x, y, SC.TABS, TABS[level], space, sp.get("third"))
    top = y + (190 if sp.get("third") else 140)
    if sp["kind"] == "table":
        SC.table(x + 24, top, sp["heads"], sp["content"], sp.get("cols", (0, 380, 700)))
    elif sp["kind"] == "rows":
        SC.closed_rows(x + 24, top, sp["content"], sp.get("opened"))
    else:
        SC.lines(x + 24, top, sp["content"])
    SC.runs_panel(x, y, sp["runs"], sp.get("recent", ""), sp.get("disk", ()))
    return SC.SH


# ── the drawing ─────────────────────────────────────────────────────────────────────────────────
def change(x, y, what, size=20):
    """A short green line where a change was made (or what is kept), ✎ <date> first."""
    L.els.append(canvas.change_note(x, y, what, DATE, L.FRAME[0], size))


def card(x, y, letter, f, path, width=CARD_W) -> float:
    """One version: its place, its picture, its style line; an old one flagged OLD, red dashed. Its height."""
    old = f.get("old", "")
    if old:
        text(x, y - 26, "OLD · " + old, 14, RED)
    seen = f.get("seen", [])
    more = f"  (+{len(seen) - 1} more places)" if len(seen) > 1 else ""
    text(x, y, f"{letter} · {f.get('place', '')}{more}", 18)
    h = B.picture(path, x, y + 36, width)
    if old:
        base("rectangle", x - 8, y + 28, B.LAST_W[0] + 16, h + 16, RED, 1.5, dashed=True, rough=0)
    text(x, y + 48 + h, B.style_line(f) + ("\n(cut at its first screen)" if f.get("cut") else ""), 13, INK, MONO)
    return 48 + h + 50


def versions(facts, key):
    return sorted(k for k, f in facts.items() if not k.startswith(("proposed__", "_")) and f.get("element") == key)


def frame_element(el, x0, y0, facts, per_row=3) -> dict:
    fr = L.open_frame(el["title"])
    text(x0, y0, el["title"], 34)
    keys = versions(facts, el["key"])
    olds = sum(bool(facts[k].get("old")) for k in keys)
    text(x0, y0 + 50, f"{el['what']} · {len(keys)} versions as the work theme draws them today, {olds} on old pages "
                      "(flagged OLD: they retire; a look from one may still be picked); then as planned", 18)
    x, y, row_h = x0, y0 + 130, 0
    for i, k in enumerate(keys):
        if i and i % per_row == 0:
            x, y, row_h = x0, y + row_h + 70, 0
        letter = chr(65 + i) if i < 26 else "A" + chr(65 + i - 26)
        row_h = max(row_h, card(x, y, letter, facts[k], SHOTS / f"{k}.png"))
        x += CARD_W + 140
    if not keys:
        text(x0, y0 + 130, "? no shots yet: run with --shoot", 18, RED)
    y += row_h + 40
    plans = PLANNED.get(el["key"], [])
    if plans:
        text(x0, y + 20, "as planned · the screen b03's s11 · s13 and this Block's s01 draw (lines only, not served yet; "
                         "a red button has no Run name yet)", 22)
        px = x0
        for k, (level, space) in enumerate(plans):
            where = "the Run pop-out · b17 s01, the Run row" if level == "popout" else f"{PLAN_FROM[level]} › {space}"
            text(px, y + 70, f"P{k + 1} · {where}", 20)
            planned_screen(level, space, px, y + 110)
            px += SC.SW + 120
    L.close_frame(fr)
    return fr


def tag_count(facts) -> int:
    return sum(1 for k in versions(facts, "tags") if not facts[k].get("old"))


def frame_proposed(key, title, x0, y0, facts) -> dict:
    fr = L.open_frame(title + " · proposed")
    text(x0, y0, title + " · proposed", 34)
    url, _, why, changed, open_ = PROPOSALS[key]
    open_ = open_.replace("{n}", str(tag_count(facts)))
    text(x0, y0 + 50, "one look for every theme, drawn by the base (servers/workbench); the work theme gives the words only", 18)
    y = y0 + 110
    change(x0, y, changed)
    y += 40
    if open_:
        text(x0, y, open_, 18, RED)
        y += 40
    shot = SHOTS / f"proposed__{key}.png"
    if shot.exists():
        h = B.picture(shot, x0, y, 1000)
        text(x0, y + h + 12, B.style_line(facts.get(f"proposed__{key}", {})), 13, INK, MONO)
        y += h + 70
    elif url.startswith("none:"):
        text(x0, y, "(none)", 28)
        y += 60
    else:
        text(x0, y, "? no shot yet: run with --shoot", 18, RED)
        y += 40
    text(x0, y + 10, "why", 22)
    for i, line in enumerate(why):
        text(x0 + 20, y + 50 + i * 30, "· " + line, 17)
    L.close_frame(fr)
    return fr


# the theme's elements: (element, level, Space › view, base or its own and why, drawn today ("" = yes) or GAP)
THEME_ELEMENTS = [
    ("Top tabs", "all", "the level row, the six Spaces", "base", ""),
    ("Job ▾ · Task ▾ select", "Job · Task", "the level row", "base; the options grouped by Job series (j0N · j1N · j5N)",
     "GAP: folder names, not grouped"),
    ("View row", "all", "every Space with views", "base", ""),
    ("View row", "Task", "Scope · Plan | Report · Draft | Code · Review · Notebooks | runs by type",
     "base, the work theme's words (s13 1, 1d)", "GAP: the Page views (Folder · Evidence · Value · Page Runs · Lanes) "
     "added to every work Task's row"),
    ("Question rows", "Block", "Audience Report: one row per Question", "base (the Insight row, b03 s32-D05)", ""),
    ("Question rows", "Job", "Audience Report: the Block's Questions this Job's Tasks feed", "base, a filter (s01 Open 2)",
     "GAP: empty: a Job has no reports/ and no filter"),
    ("Question rows", "Task", "Audience Report › Report: Question │ Work │ Report (s13 1b)", "base row",
     "GAP: one line, 'the report is its face'"),
    ("Draft list", "Task", "Audience Report › Draft: draft/", "own: the Task's draft notes", "GAP: lists draft/*.md "
     "only; a draft/ holding records/ reads 'Nothing here yet'"),
    ("Space body", "all", "every Space", "base", "GAP: Evidence · Page Runs · Lanes embed the old Page workbench"),
    ("Tables", "Block", "Work Details: the Jobs", "base", "GAP: no Job series third row, no state (s01)"),
    ("Tables", "Job", "Work Details: the Tasks with Plan · Build · Run · Report", "base", "GAP: title and Runs count only"),
    ("Tables", "Task", "Work Details › Code · Notebooks (file · bytes)", "base", ""),
    ("Plan", "Task", "Description › Plan: the face's ## Plan", "own: the plan as written", ""),
    ("Review", "Task", "Work Details › Review: CODE_REVIEW.md", "own: one link to the review", ""),
    ("Rows", "all", "Idea Studio: one topic per row", "base (b03 s32-D06)", ""),
    ("Job → Task → Run tree", "Block", "Work Details › Jobs ▾ Tasks (was the old page's Question rows)",
     "base rows, opened in place", "GAP: no tree on the frame; the Work column lists ids"),
    ("Disk · Runs panel", "all", "every Space", "base", ""),
    ("Runs table", "Block · Job", "Runs: its own soft Runs, ☐ from below its Tasks' hard Runs", "base",
     "GAP: no 'from below'; only run-<type>-<target>"),
    ("Runs table", "Task", "Runs › All · run · build · report (hard rNN_, soft run-)", "base, third row by type",
     "GAP: the types read off disk (All · run); a row opens nothing"),
    ("Run pop-out", "Run", "a hard Run: card · ticket · config · result/ · passes", "base pop-out (s01 Run row)",
     "GAP: none; the result is on the old page only"),
    ("Delivery cards", "Task", "Delivery: Reports · Exports, no third row (s13 1b)", "base cards",
     "GAP: Files table + the old Page's Lanes"),
    ("Delivery", "Block · Job", "Delivery: optional, its own and from below", "base", "GAP: no 'from below'"),
    ("Job face", "Job", "Description: jNN_<job>.md (goal · state · task_groups)", "base",
     "GAP: no face on disk: 'No face file', no button"),
    ("Tags", "all", "—", "none (b03 s32-D09)", "GAP: {n} kinds drawn today"),
    ("Page header", "all", "the title line", "base", ""),
    ("One item's display", "Task · Run", "a Task is the Task tab; a Run opens in the pop-out", "base",
     "GAP: a Run's row opens nothing; old Run page and /_board/draft still answer"),
]
# every button of the work theme with no Run name yet, and the Run it should make (run-<type>-<target>)
PROPOSED_RUNS = {
    "Ask a Question": "run-ask-<qNN>", "Review the questions": "run-review-questions-<bNN>",
    "Add a resource": "run-add-resource-<slug>", "Save resource": "run-add-resource-<slug>",
    "Draw the question map": "run-draw-<sNN>", "Draw": "run-draw-<sNN>", "Edit drawing": "run-draw-<sNN>",
    "+ Add drawing": "run-draw-<sNN>", "Plan a Task": "run-plan-<tNN>", "Review the plan": "run-review-plan-<tNN>",
    "Build the Task": "run-build-<tNN>", "Review the Task code": "run-review-code-<tNN>", "Run a Task": "rNN_<slug> (hard)",
    "Report the Run": "run-write-<tNN>", "Plan the report": "run-plan-report-<qNN>", "Write the report": "run-report-<qNN>",
    "Check a Task": "run-check-<tNN>", "Check a report": "run-check-<qNN>", "Build the report": "run-delivery-<qNN>",
    "Rerun": "a new pass of rNN_<slug>", "run-<type>-<target>": "its types: Block run-report-<qNN> …; Job run-launch-<jNN>",
    "Context": "run-context-<slug>", "Structure revise": "run-structure-<slug>", "Evidence embed": "run-evidence-<slug>",
    "Bind / update citation": "run-citation-<slug>", "Build": "run-delivery-<target>",
    "Update the Job": "run-face-<jNN>", "Review the shared code": "run-review-code-<jNN>",
    "Launch all": "run-launch-<jNN>", "Plan its Tasks": "run-plan-<jNN>",
}


def unnamed(facts) -> list:
    """(words, where it was met, proposed Run) for every button met with no Run name of its own; the generic
    run-<type>-<target> counts as none; plus the planned screens' buttons that have none yet."""
    met = dict(facts.get("_buttons", {}))
    met.setdefault("Rerun", ["the old work Block page (a Run card)"])   # inside each run card, not a run type
    for level, spaces in PLAN.items():
        for sp in spaces.values():
            for words in sp["runs"]:
                if not RN.named(words):
                    met.setdefault(words, []).append(f"planned · {PLAN_FROM[level]} › {sp['space']}")
    out = []
    for words, places in sorted(met.items()):
        if words.startswith(("run-", "rNN_")) and words != "run-<type>-<target>":
            continue
        out.append((words, places, PROPOSED_RUNS.get(words, "? " + (RN.name_of(words) if RN.named(words) else "to name"))))
    return out


def frame_theme_elements(x0, y0, facts) -> dict:
    fr = L.open_frame("11 · The work theme's own elements · proposed")
    text(x0, y0, "11 · Theme elements · proposed", 34)
    text(x0, y0 + 50, "every element the work theme uses, planned in b03 s11 · s13 and this Block's s01: the base's, or its "
                      "own and why; red: what today's frame does not draw yet", 18)
    change(x0, y0 + 100, "the list b03's s32 reads (its Theme elements frame); same lines in the face")
    heads = ("element", "level", "Space › view", "base or own", "drawn today")
    xs = [0, 330, 520, 1380, 2120]
    y = y0 + 160
    for hx, h in zip(xs, heads):
        text(x0 + hx, y, h, 18)
    y += 36
    L.path([(x0, y - 4), (x0 + 3000, y - 4)], arrow=False, color=INK)
    for row in THEME_ELEMENTS:
        for hx, cell in zip(xs, row):
            cell = cell.replace("{n}", str(tag_count(facts)))
            text(x0 + hx, y, cell or "✓ drawn", 15, RED if cell.startswith("GAP") else INK)
        y += 30
    L.close_frame(fr)
    return fr


def frame_buttons(x0, y0, facts) -> dict:
    fr = L.open_frame("Buttons with no Run name")
    rows = unnamed(facts)
    text(x0, y0, f"Buttons with no Run name yet: {len(rows)}", 34)
    text(x0, y0 + 50, "every Runs-panel button met on the work pages (and on the planned screens) that names no "
                      "run-<type>-<target>; red: the proposed name, open until b03 and the work skills agree", 18)
    y = y0 + 120
    for hx, h in zip((0, 420, 1300), ("button", "where", "proposed Run")):
        text(x0 + hx, y, h, 18)
    y += 36
    L.path([(x0, y - 4), (x0 + 2200, y - 4)], arrow=False, color=INK)
    for words, places, run in rows:
        where = " · ".join(sorted(set(places)))
        text(x0, y, words, 15)
        text(x0 + 420, y, L.short(where, 100), 14)
        text(x0 + 1300, y, run, 15, RED, MONO)
        y += 30
    y += 30
    if PLACEHOLDER_RUNS:
        text(x0, y, "named, but with a placeholder or another theme's target", 22)
        y += 40
    for words, where, run in PLACEHOLDER_RUNS:
        text(x0, y, L.short(words, 38), 15, INK, MONO)
        text(x0 + 420, y, where, 14)
        text(x0 + 1300, y, "? " + run, 15, RED)
        y += 30
    y += 20
    for what in FIXED_RUNS:
        change(x0, y, "fixed in the base (b03): " + what, 16)
        y += 30
    L.close_frame(fr)
    return fr


# buttons that carry a Run name, but a placeholder the base would fill, or another theme's target
PLACEHOLDER_RUNS = []
# fixed in the base by b03 (261008), drawn green under the list
FIXED_RUNS = ["the work Run names carry the Task's tag: run-plan-t01 · run-build-t01 · run-review-code-t01 · run-check-t01",
              "a Task's Write the report is run-write-t01 (was run-report-<qNN>)",
              "planned Release is run-release-<target>, no longer the design theme's run-release-j<NN>"]


PICKED = {"tabs": "D · E (b03 s32-D01), from the base", "views": "E (b03 s32-D02), from the base",
          "report": "the Insight row (b03 s32-D05)", "runs": "Disk inside Runs (b03 s32-D08)",
          "tags": "none (b03 s32-D09)"}


def frame_pick(x0, y0) -> dict:
    fr = L.open_frame("Pick")
    text(x0, y0, "Pick: one look per work element", 34)
    text(x0, y0 + 50, "b03's picks hold for the work theme; write the letter you keep for the rest (or draw a new one)", 18)
    for i, el in enumerate(ELEMENTS):
        text(x0, y0 + 120 + i * 44, f"{el['title']}  —  {el['what']}", 20)
        if el["key"] in PICKED:
            text(x0 + 1100, y0 + 120 + i * 44, "kept: " + PICKED[el["key"]], 20, GREEN)
        else:
            text(x0 + 1100, y0 + 120 + i * 44, "? keep: __", 20, RED)
    L.close_frame(fr)
    return fr


def frame_title(x0, y0, facts) -> dict:
    fr = L.open_frame("s32 · Work element UI")
    text(x0, y0, "s32 · Work element UI", 44)
    keys = [k for k in facts if not k.startswith(("proposed__", "_"))]
    olds = sum(1 for k in keys if facts[k].get("old"))
    text(x0, y0 + 70, f"every element the work theme draws today ({len(keys)} versions, {olds} on old pages), one frame each "
                      "with the planned screen under it and its proposed look beside it", 20)
    text(x0, y0 + 104, "after b03 s32-element-ui (and b12 · b16's); live from the frame at Block · Job · Task, every Space "
                       "and view; OLD = an old page, red dashed", 20)
    for i, what in enumerate(CHANGES):
        change(x0, y0 + 160 + i * 34, what)
    L.close_frame(fr)
    return fr


def draw(out: Path) -> None:
    facts = json.loads((SHOTS / "facts.json").read_text()) if (SHOTS / "facts.json").exists() else {}
    L.els.clear()
    L.FRAME[0] = None
    B.FILES.clear()
    title = frame_title(0, -900, facts)
    pk = frame_pick(title["x"] + title["width"] + 200, -900)
    bt = frame_buttons(pk["x"] + pk["width"] + 200, -900, facts)
    y = max(f["y"] + f["height"] for f in (title, pk, bt)) + 300
    for el in ELEMENTS:
        per_row = 4 if el["key"] in ("space", "tags", "views", "cards", "table") else 3
        fr = frame_element(el, 0, y, facts, per_row)
        right = fr["x"] + fr["width"] + 200
        if el["key"] in PROPOSALS:
            pr = frame_proposed(el["key"], el["title"], right, y, facts)
        else:
            pr = frame_theme_elements(right, y, facts)
        y = max(fr["y"] + fr["height"], pr["y"] + pr["height"]) + 200
    canvas.write(out, list(L.els), Path(__file__).name, files=B.FILES)


if __name__ == "__main__":
    if "--shoot" in sys.argv:
        url = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "http://127.0.0.1:5851"
        shoot(url.rstrip("/"))
    draw(Path(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].endswith(".excalidraw")
         else HERE / "s32-work-element-ui.excalidraw")
