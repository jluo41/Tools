"""s32 · Paper element UI: s32-paper-element-ui.excalidraw, the gallery of every kind of element the paper theme
draws today, one card per version, so it can be unified with b03's picks (b03 s32-element-ui, JL 261007: "collect
all types of the UI of different types of the element ... so we can unify them").

Two steps, as b03's s32:

    uv run --with playwright --with pillow python build_s32_paper_element_ui.py --shoot [--base http://127.0.0.1:5851]
        walks the paper theme on the frame (/_board/workbench) at its Block, Job and Task levels, every Space and
        every view, plus its old pages (the old paper Board page, rendered by paper.py since its address forwards
        to the frame, and the item pages a paper row opens outside the frame); screenshots each element version
        into shots/<element>__<n>.png and writes where it was seen and its computed style into shots/facts.json.
    python build_s32_paper_element_ui.py
        draws the gallery from shots/: per element a frame of versions (old ones flagged OLD in red, a red
        dashed box) and beside it a "· proposed" frame (b03's picks), then the theme's own elements and the Pick
        frame. Marks are kept on rebuild (canvas.write).

The drawing helpers (picture, style line, the pick script, the canvas writer) are b03's, imported from its
s32 builder.
"""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.parse as U
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "shots"
TOOLS = HERE.parents[3]
SPACE = HERE.parents[4]
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
sys.path.insert(0, str(TOOLS / "blueprints/b03_project_workbench/studio/s32-element-ui"))
import build_s32_element_ui as B  # noqa: E402  (b03's gallery: picture, style_line, PICK_JS, its L and canvas)

L, canvas = B.L, B.canvas
INK, RED, GREEN = canvas.INK, canvas.RED, canvas.GREEN
text, base = L.text, L.base
MAX_H, CARD_W = 700, 720


def q(path: str) -> str:
    return U.quote(path, safe="")


def frame_url(folder: str, space: str = "", sub: str = "") -> str:
    query = {"path": folder}
    if space:
        query["space"] = space
    if sub:
        query["sub"] = sub
    return "/_board/workbench?" + U.urlencode(query)


# ── what is shot ────────────────────────────────────────────────────────────────────────────────
PAPER = "examples-4-learning/Project-ExpLearn-SMSDesign/paper/Paper-TestToLearn-MS2026"   # on the ladder
OLDER = "examples-4-learning/Project-ExpLearn-PatientSimulation/papers/Paper-LLMSocialOutcome-PNAS2026"  # A1-Story
SEC = "j01_v0429_mansci/t01_introduction/t01_introduction.md"    # a Section with delivery/, results/, runs/
SPACES = ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")
# the frame's paper pages: (key, label, folder). The first three give the per-level cards; all are walked
LEVELS = [("block", "Block · the paper Board", PAPER),
          ("job", "Job · a version (j01)", PAPER + "/j01_v0429_mansci"),
          ("task", "Task · a Section (j01 › t01_introduction)", PAPER + "/" + SEC.rsplit("/", 1)[0]),
          ("job2", "Job · the next version (j02)", PAPER + "/j02_v1007_mansci"),
          ("oblock", "Block · an older Board (A1-Story layout)", OLDER),
          ("ojob", "Job · the older Board's Story group (A1-Story)", OLDER + "/A1-Story")]
LEVEL_OF = {k: lbl.split(" · ")[0] for k, lbl, _ in LEVELS}
# the old pages: (key, label, url, why it is old). "render:board" is paper.py's old Board page, rendered here
# (its address /_board/paper-board forwards to the frame); "from:<url>|<css>" is the first such link on that page
OLD_PAGES = [
    ("old-board", "the old paper Board page (paper.py render_paper)", "render:board",
     "old page: /_board/paper-board forwards to the frame now; its look lives on inside the frame's pv() views"),
    ("old-draft", "a Section's Page workbench page (/_board/draft), opened by a Section row's ↗",
     f"/_board/draft?path={q(PAPER + '/board.md')}&file={q(SEC)}",
     "old item page: a Section row's ↗ leaves the frame; the Task tab embeds the same views"),
    ("old-runs", "a Section's Page Runs page (/_board/runs)",
     f"/_board/runs?path={q(PAPER + '/board.md')}&file={q(SEC)}",
     "old item page: the Task's Runs Space embeds it whole, in its own look"),
    ("old-run-result", "one run's results page (/_board/run-result), from a High-level logic row",
     "from:" + frame_url(PAPER, "Audience Report", "High-level logic + Low-level work") + "|a.bj-run",
     "old item page: a run's results open outside the frame, not in its pop-out"),
]
OLD_WHY = {k: why for k, _, _, why in OLD_PAGES}
OLD_LABEL = {k: lbl for k, lbl, _, _ in OLD_PAGES}
OLD_BOARD_SPACES = {"ideation": [""], "story": ["spine", "roadmap-draw", "logic-work", "related"],
                    "sections": ["main", "appendix"], "delivery": ["latex", "word", "cover", "rounds"]}

# the elements. mode "level": one card per level (at the Space given) and per old page; "space": one card per
# level × Space; "distinct": every view of every page is walked and each look met is one card (its first
# place, and the count of places); "item": the listed places.
# frame: the selector on the frame (scoped to the Space body for "distinct"); old: {old page: selector}
ELEMENTS = [
    dict(key="tabs", title="1 · Top tabs", what="the rows you choose a level and a Space from", mode="level",
         space="Audience Report", frame="nav.levels|nav.spaces",
         old={"old-board": "div.spaces", "old-draft": "div.spaces"}),
    dict(key="views", title="2 · View row (third row)", what="the views of the open Space", mode="views",
         frame="nav.subs", old={"old-board": ".space-tabs|.space-views", "old-draft": ".draft-mode-switcher",
                                "old-runs": ".run-space-switcher"}),
    dict(key="report", title="3 · Audience Report: the Question rows", what="one question with its work and its report",
         mode="distinct", only=("Audience Report",),
         frame=[".q-row:not(.q-head-row)", "div.lw-row", "details.qc"],
         old={"old-board": ["div.lw-row", "details.qc"]}),
    dict(key="space", title="4 · The Space body", what="the open Space's box, its first screen (its first view)",
         mode="space", frame=".space-main", old={"old-board": ".space-main"}),
    dict(key="table", title="5 · Tables", what="rows of items in a table", mode="distinct",
         frame=["table"], old={"old-board": ["table"], "old-draft": ["table"], "old-run-result": ["table"]}),
    dict(key="cards", title="6 · Rows and cards", what="one item, closed or open", mode="distinct",
         frame=["details.topic", "div.topic", "div.sec-row", "details.item-card", "details.rp-card", "details.bj-tr",
                "details.lw-w", "div.item-row"],
         old={"old-board": ["details.item-card", "div.item-row", "details.rp-card", "details.bj-tr", "div.card"],
              "old-draft": ["div.card", "div.point-group", "div.sov-para"], "old-runs": ["div.run-card-summary"]}),
    dict(key="runs", title="7 · Disk · Runs panel", what="the files behind the open Space, its run types and their runs",
         mode="level", space="Audience Report", frame="section.runs-panel",
         old={"old-board": ".runs-panel", "old-draft": "section.runs-panel"}),
    dict(key="tags", title="8 · Tags and pills", what="a state, a kind or a count on an item", mode="distinct",
         frame=[".rp-tags", ".lw-tags", ".item-status", ".sec-state", ".sec-ver", "a.chip", "span.kind", ".st-ok",
                ".st-warn", "span.ok", "span.warn", ".idtag", ".bj-rs", ".item-kind", ".pill", ".tag"],
         old={"old-board": [".item-status", ".item-kind", ".idtag", "span.ok", "span.warn", ".pill", ".lw-tags"],
              "old-draft": [".pill", ".chip", ".tag", ".badge"], "old-runs": [".pill", ".run-card-action"]}),
    dict(key="header", title="9 · Page header", what="the title line at the top", mode="level", space="Audience Report",
         frame="header", old={"old-board": "h1|.wb-band", "old-draft": "h1|.wb-band", "old-run-result": "h1",
                              "old-runs": "h1,header"}),
    dict(key="item", title="10 · One item's display", what="one Section, one run: the item itself", mode="item"),
    dict(key="own", title="11 · The paper theme's own elements", what="what only the paper draws, each where it lives",
         mode="item"),
]
# 10 and 11: (label, url, selector, why old or "")
SPOT = lambda folder, space, sub="": frame_url(folder, space, sub)
ITEMS = {
    "item": [
        ("Task › Audience Report › Table: the Section's Page view, embedded in the frame",
         SPOT(LEVELS[2][2], "Audience Report", "Table"), ".space-main", ""),
        ("Task › Work Details › Draft-Revise: the Page's draft, embedded", SPOT(LEVELS[2][2], "Work Details", "Draft-Revise"),
         ".space-main", ""),
        ("Job › Work Details › Main: a Section's row, ↗ leaves the frame", SPOT(LEVELS[1][2], "Work Details", "Main"),
         ".space-main", ""),
        (OLD_LABEL["old-draft"], "old-draft", ".space-main,main,body", OLD_WHY["old-draft"]),
        (OLD_LABEL["old-runs"], "old-runs", ".wrap,main,body", OLD_WHY["old-runs"]),
        (OLD_LABEL["old-run-result"], "old-run-result", "main,body", OLD_WHY["old-run-result"]),
    ],
    "own": [
        ("Block › Description › Venue: the venues (none on disk yet)", SPOT(PAPER, "Description", "Venue"), ".space-main", ""),
        ("Block › Description › Related: paper cards", SPOT(PAPER, "Description", "Related"), ".space-main", ""),
        ("Block › Audience Report › Ideation", SPOT(PAPER, "Audience Report", "Ideation"), ".space-main", ""),
        ("Block › Audience Report › Narrative (was the Spine)", SPOT(PAPER, "Audience Report", "Narrative"), ".space-main", ""),
        ("Block › Audience Report › High-level logic + Low-level work",
         SPOT(PAPER, "Audience Report", "High-level logic + Low-level work"), ".space-main", ""),
        ("Block › Work Details › Main: the Sections list", SPOT(PAPER, "Work Details", "Main"), ".space-main", ""),
        ("Block › Delivery › LaTeX: the built paper", SPOT(PAPER, "Delivery", "LaTeX"), ".space-main", ""),
        ("Job › Audience Report › Draft-Main: the Narrative's rows", SPOT(LEVELS[1][2], "Audience Report", "Draft-Main"),
         ".space-main", ""),
        ("Job › Audience Report › Comments: Review Items", SPOT(LEVELS[3][2], "Audience Report", "Comments"), ".space-main", ""),
        ("Job › Audience Report › Cover letter", SPOT(LEVELS[3][2], "Audience Report", "Cover letter"), ".space-main", ""),
        ("Job › Delivery: the version's build", SPOT(LEVELS[1][2], "Delivery"), ".space-main", ""),
        ("Task › Description › Scope: ◆ the reader contract", SPOT(LEVELS[2][2], "Description", "Scope"), ".space-main", ""),
        ("Task › Description › Requirement: ◆ the SUB-* rows", SPOT(LEVELS[2][2], "Description", "Requirement"),
         ".space-main", ""),
        ("Task › Audience Report › Comments: ◆ Review Items on this Section", SPOT(LEVELS[2][2], "Audience Report", "Comments"),
         ".space-main", ""),
        ("Task › Delivery: ◆ Ready, then the delivery cards", SPOT(LEVELS[2][2], "Delivery"), ".space-main", ""),
        ("the old Board page › Story › Spine", "old-board#story/spine", ".panel[data-space=story] .space-main",
         OLD_WHY["old-board"]),
        ("the old Board page › Ideation", "old-board#ideation/", ".panel[data-space=ideation] .space-main", OLD_WHY["old-board"]),
    ],
}

# the proposed look per element (b03's picks hold: tabs D · E, view row E, the Question cell as the Insight row,
# Disk inside the Runs panel, no tags): (url, selector, why, changed (green), open (red))
JOB, TASK = LEVELS[1][2], LEVELS[2][2]
JOB2 = LEVELS[3][2]
PROPOSALS = {
    "tabs": (SPOT(JOB, "Audience Report"), "nav.levels|nav.spaces",
             ["b03's pick D · E (b03 s32-D01): one button shape for every top row, the open one washed blue",
              "the paper keeps its words only: Paper Board · Version ▾ · Section ▾, the six Spaces",
              "drawn by the base frame, so the paper has no tab code of its own"],
             "kept: the base's D · E tabs; the paper draws none of its own", ""),
    "views": (SPOT(JOB, "Audience Report"), "nav.subs",
              ["b03's pick E (b03 s32-D02): the tabs' shape, 5px 12px, the open one washed blue",
               "every paper view on this row, never a second row inside the body (the old page had tabs × views)"],
              "kept: the base's E view row at every level",
              "? Task › Runs keeps the Page Runs view's own lane row inside its body (s13 D8): a second row, its own look"),
    "report": (SPOT(JOB2, "Audience Report", "Questions"), ".q-head-row|.q-row:not(.q-head-row)",
               ["one row per question at every level: Question │ Work │ Report (b03 s04-D04)",
                "the Question cell as the Insight row (b03 s32-D05): a label and its state dot, the short name, "
                "one sentence, › More",
                "Ideation (ID…) and Narrative (N1–N4) take the base question_cell(); High-level logic keeps its lw "
                "rows (b03 ruling, 261008)"],
               "decided: Ideation and Narrative take question_cell(); lw rows kept (b03, 261008)",
               "? to build in paper_theme.py: Ideation and Narrative still draw the older cell; the Report cell "
               "carries tags"),
    "space": (SPOT(JOB2, "Audience Report", "Questions"), ".split",
              ["one content box and one right column, Disk · Runs, for every paper Space",
               "inside it the paper's views keep the old page's cards through pv() (JL: reuse the old cards)"],
              "kept: the base's box, the old cards inside it (pv(), JL)", ""),
    "table": (SPOT(PAPER, "Description", "Scope"), "table.wf-table",
              ["the base's light table: small grey heads, rows ruled by one line",
               "the built paper's checks and the reader contract are this table; an item with a body is a row (6)"],
              "decided: the Delivery grid tables take the base table() (b03, 261008)",
              "? to build in paper_theme.py: Delivery › LaTeX and Word still draw grid tables"),
    "cards": (SPOT(JOB2, "Work Details", "Main"), ".space-main",
              ["the paper reuses the old page's cards (JL 261007; b03 ruling 261008): the Sections list (sec-row), "
               "item cards (Draft-Main, Comments, Letters), paper cards (Related), through pv()",
               "the Idea Studio keeps the base's topic rows"],
              "kept: the old paper cards through pv() (JL; b03, 261008)", ""),
    "runs": (SPOT(PAPER, "Audience Report"), "section.runs-panel",
             ["Disk, then Runs, in one panel with one fold (b03 s32-D08)",
              "one row per run type, named by its Run (run-<type>-<target>), what it does under it"],
             "kept: Disk inside Runs, one fold, at every level",
             "fine for now: the Task's Runs Space embeds the Page Runs page until the base's Page views draw lanes"),
    "tags": ("none:", "",
             ["none: no tags in any theme (b03 s32-D09)",
              "a state is a word (open · partial · answered) or the question's state dot",
              "an id is plain text where it stands (t01, RQ1, Review-<slug>)"],
             "decided: no tags in the paper's views (b03 s32-D09; ruling 261008)",
             "? to build in paper_theme.py: {n} kinds drawn today (Report-cell tags, item status, section state "
             "and version, ok/warn, id tags, run counts)"),
    "header": (SPOT(JOB, "Audience Report"), "header",
               ["one line: 📄 Paper · the folder; the path on hover", "no band, no links row above the tabs"],
               "kept: one line, no band (the old page's band is gone)", ""),
    "item": (SPOT(TASK, "Audience Report", "Table"), ".space-main",
             ["an item opens in the frame: a Section is a Task, its views the Task's Spaces; a run in the pop-out",
              "no item page beside the frame: /_board/draft, /_board/runs and /_board/run-result stop being "
              "destinations; the Task embeds what it needs"],
             "decided: a Section's ↗ and a run row point at the frame (/_board/workbench?path=…&view=draft) (b03, 261008)",
             "? to build in paper_theme.py: they still point at /_board/draft and /_board/run-result"),
}

CHANGES = [("261008", "the paper theme's element gallery, after b03's s32 (picks D · E, E, Insight row, Disk in Runs, "
                      "no tags)"),
           ("261008", "b03's rulings: old cards kept (pv), question_cell() for Ideation and Narrative, no tags, links "
                      "into the frame, delivery tables to table(), the planned views in order")]


# ── the shoot ───────────────────────────────────────────────────────────────────────────────────
COLLECT_JS = """([sels, scope, ctx]) => {
  const root = scope ? [...document.querySelectorAll(scope)].find(e => e.getBoundingClientRect().width > 4) : document;
  if (!root) return [];
  // inside a closed <details> (not its summary) an element is laid out but not painted
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
TAG_CTX = "summary,p,li,.sec-row,.lw-top,.st-bar,.item-summary,tr,.bj-t"

OLD_BOARD_PY = r"""
import sys
from pathlib import Path
T, root, board, out = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
sys.path.insert(0, str(T / "_host"))
from host_paths import bootstrap; bootstrap()
from live import paper as P
out.write_text(P.render_paper(root / board, root, board + "/board.md"), encoding="utf-8")
"""


def render_old_board() -> str:
    """The old paper Board page's HTML, rendered by the SPACE's own Python (paper.render_paper); "" if it fails."""
    out = SHOTS / "old-board.html"
    done = subprocess.run([str(SPACE / ".venv" / "bin" / "python"), "-c", OLD_BOARD_PY, str(SERVERS), str(SPACE),
                           PAPER, str(out)], capture_output=True, text=True)
    if done.returncode or not out.exists():
        print("old board:", (done.stderr or "").strip().splitlines()[-1:] or "failed")
        return ""
    return out.read_text(encoding="utf-8")


class Shooter:
    def __init__(self, page, base_url):
        self.page, self.base = page, base_url
        self.facts, self.n = {}, {}
        self.seen = {}                                   # (element, signature) -> fact key
        self.old_html = ""
        self.old_urls = {}

    def snap(self, box, path):
        """Screenshot a box given in page coordinates: scroll it to the top, then clip in the viewport (a
        full-page shot resizes the viewport, and the frame's 100vh boxes move under it)."""
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
        except Exception as exc:                          # off the page (a scrolled box): no card
            print(f"{ekey} at {place}: {str(exc).splitlines()[0]}")
            return None
        self.n[ekey] = n
        self.facts[name] = {"element": ekey, "place": place, "url": url, "selector": sel, "old": old,
                            "cut": box["h"] > MAX_H, "seen": [place], **box["style"]}
        return name

    def goto(self, url):
        """A frame URL, an old page key (old-board#space/tab), or a host URL; True when it is on screen."""
        if url.startswith("old-board"):
            if not self.old_html:
                return False
            self.page.goto(self.base + frame_url(PAPER))       # the host's origin, so its links resolve
            self.page.set_content(self.old_html, wait_until="load")
            self.page.wait_for_timeout(500)
            space, _, tab = url.partition("#")[2].partition("/")
            if space:
                self.page.evaluate("s => { const b = document.querySelector(`button.space[data-space='${s}']`); if (b) b.click(); }",
                                   space)
            if tab:
                self.page.evaluate("([s, t]) => { const b = document.querySelector(`.panel[data-space='${s}'] "
                                   ".space-tab[data-tab='${t}']`); if (b) b.click(); }", [space, tab])
            self.page.evaluate("document.querySelectorAll('.runs-panel.folded').forEach(p => p.classList.remove('folded'))")
            self.page.wait_for_timeout(300)
            return True
        if url in self.old_urls:
            url = self.old_urls[url]
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
                    for el in ELEMENTS:
                        mode = el["mode"]
                        if mode == "distinct" and (not el.get("only") or space in el["only"]):
                            self.distinct(el, el["frame"], ".space-main", place, url)
                        if not main or i:
                            continue
                        if mode == "level" and space == el["space"] or mode == "space" or mode == "views" and subs:
                            box = self.one(el["frame"])
                            if box:
                                lbl = (f"{LEVEL_OF[lkey]} › {space}" if mode != "level" else llabel)
                                self.shot(el["key"], box, lbl, url, el["frame"])
        for okey, _, url, why in OLD_PAGES:                 # the old pages
            if okey == "old-board":
                self.old_html = render_old_board()
                places = [f"old-board#{s}/{t}" for s, tabs in OLD_BOARD_SPACES.items() for t in tabs]
            else:
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
                places = [okey]
            for n, where in enumerate(places):
                if not self.goto(where):
                    print(f"{okey}: not on screen, skipped")
                    break
                space, _, tab = where.partition("#")[2].partition("/")
                first = not space or tab == OLD_BOARD_SPACES[space][0]     # a Space's first view
                place = OLD_LABEL[okey] + (f" › {space}" + (f" › {tab}" if tab else "") if space else "")
                src = self.old_urls.get(okey, "render:board")
                inside = lambda sel: "|".join(f".panel[data-space='{space}'] {s}" for s in sel.split("|")) if space else sel
                for el in ELEMENTS:
                    sel = el.get("old", {}).get(okey)
                    if not sel:
                        continue
                    if el["mode"] == "distinct":
                        self.distinct(el, sel, f".panel[data-space='{space}']" if space else None, place, src, why)
                    elif el["mode"] in ("space", "views"):
                        box = self.one(inside(sel)) if first else None
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
                self.page.wait_for_timeout(600)                   # an embedded view loads its iframe
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
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(exist_ok=True)
    for old in list(SHOTS.glob("*.png")) + list(SHOTS.glob("*.html")):
        old.unlink()
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 1100}, device_scale_factor=1)
        s = Shooter(page, base_url)
        s.walk()
        s.items()
        s.proposals()
        browser.close()
    (SHOTS / "old-board.html").unlink(missing_ok=True)            # rendered only to be shot
    (SHOTS / "facts.json").write_text(json.dumps(s.facts, indent=1, ensure_ascii=False))
    print(f"{len(s.facts)} shots in {SHOTS.relative_to(HERE.parent)}")


# ── the drawing ─────────────────────────────────────────────────────────────────────────────────
def style_line(f: dict) -> str:
    return B.style_line(f)


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
    text(x, y + 48 + h, style_line(f) + ("\n(cut at its first screen)" if f.get("cut") else ""), 13, INK, L.MONO)
    return 48 + h + 50


def frame_element(el, x0, y0, facts, per_row=3) -> dict:
    fr = L.open_frame(el["title"])
    text(x0, y0, el["title"], 34)
    keys = sorted(k for k, f in facts.items() if f.get("element") == el["key"] and not k.startswith("proposed__"))
    olds = sum(bool(facts[k].get("old")) for k in keys)
    text(x0, y0 + 50, f"{el['what']} · {len(keys)} versions as the paper theme draws them today, {olds} on old pages "
                      "(flagged OLD: they retire; a look from one may still be picked)", 18)
    x, y, row_h = x0, y0 + 130, 0
    for i, k in enumerate(keys):
        if i and i % per_row == 0:
            x, y, row_h = x0, y + row_h + 70, 0
        letter = chr(65 + i) if i < 26 else "A" + chr(65 + i - 26)
        row_h = max(row_h, card(x, y, letter, facts[k], SHOTS / f"{k}.png"))
        x += CARD_W + 80
    if not keys:
        text(x0, y0 + 130, "? no shots yet: run with --shoot", 18, RED)
    L.close_frame(fr)
    return fr


def frame_proposed(key, title, x0, y0, facts) -> dict:
    fr = L.open_frame(title + " · proposed")
    text(x0, y0, title + " · proposed", 34)
    url, _, why, changed, open_ = PROPOSALS[key]
    open_ = open_.replace("{n}", str(sum(1 for f in facts.values() if f.get("element") == key and not f.get("old")
                                         and f.get("place") != "proposed")))
    text(x0, y0 + 50, "one look for every theme, drawn by the base (servers/workbench); the paper gives the words only", 18)
    y = y0 + 110
    canvas_note(x0, y, changed)
    y += 40
    if open_:
        text(x0, y, open_, 18, RED)
        y += 40 * (1 + open_.count("\n"))
    shot = SHOTS / f"proposed__{key}.png"
    if shot.exists():
        h = B.picture(shot, x0, y, 1000)
        text(x0, y + h + 12, style_line(facts.get(f"proposed__{key}", {})), 13, INK, L.MONO)
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


def canvas_note(x, y, what, date="261008"):
    """A short green line: what changed here (or what is kept), ✎ <date> first."""
    e = canvas.change_note(x, y, what, date, L.FRAME[0], 20)
    L.els.append(e)


# the theme's elements: element · level · Space › view · base or own (and why) · drawn today? ("" yes, "? …" a gap)
THEME_ELEMENTS = [      # "" = drawn today; "? …" = a gap (red); other words: kept as drawn, and why
    ("Top tabs", "all", "the level row, the six Spaces", "base", ""),
    ("View row", "all", "every Space with views", "base", ""),
    ("Question rows", "Block", "Audience Report › Ideation (ID…: why this paper)", "base question_cell(), the paper's words",
     "? older cell (no label, no dot): take question_cell()"),
    ("Question rows", "Block", "Audience Report › Narrative (N1–N4: says · drawn · told · attracts)",
     "base question_cell(), the paper's words", "? older cell: take question_cell()"),
    ("Question rows", "Block", "Audience Report › High-level logic + Low-level work (RQ │ work │ report)",
     "own: the RQ's hypothesis and claim, the work tree under it", "kept: its lw rows (b03, 261008)"),
    ("Question rows", "Block", "Audience Report › Related Questions", "base", ""),
    ("Question rows", "Job", "Audience Report › Questions (J1–J5)", "base", ""),
    ("Old item cards", "Job", "Audience Report › Draft-Main · Draft-Appendix · Comments · Cover letter",
     "own: the old paper cards (pv())", "kept: JL reuses the old cards"),
    ("Question rows", "Task", "Audience Report › Questions · Comments", "base", ""),
    ("Space body", "all", "every Space", "base box, old cards inside (pv())", ""),
    ("Tables", "Block · Job · Task", "Description › Scope · Version · the reader contract", "base", ""),
    ("Tables", "Block", "Delivery › LaTeX · Word (checks, artifacts)", "base table()", "? grid tables: take table()"),
    ("Rows", "Block", "Work Details › Jobs (All · versions · grants · slides, s11)", "base",
     "? build 1: today Jobs · Main · Appendix · Evidence"),
    ("Old Section rows", "Block · Job", "Work Details › Main · Appendix: the Sections", "own: the old sec-row (pv())",
     "kept: JL reuses the old cards"),
    ("Old paper cards", "Block", "Description › Related: paper cards, each opening on its drawing",
     "own: the old rp-card (pv())", "kept (JL); no drawing on a card yet"),
    ("Rows", "Block", "Description › Venue: one row per venues/<venue>/", "base", "kept: no venues/ on disk, one line"),
    ("Rows", "Block · Job · Task", "Idea Studio: one topic per row", "base", ""),
    ("Disk · Runs panel", "Block · Job", "every Space", "base", ""),
    ("Disk · Runs panel", "Task", "Runs Space", "base", "for now: embeds the Page Runs page (until ?view=runs has lanes)"),
    ("Delivery cards", "Job", "Delivery (Manuscript · Letters · Checks · Sent, s12)", "base cards",
     "? build 2: today a folding list and a table"),
    ("Delivery cards", "Block", "Delivery (All · j01 · j02: each version's build, s11)", "base cards",
     "? build 3: today LaTeX · Word · Cover letter · Rounds"),
    ("Runs third row", "Block · Job", "Runs (venue · question · draw · version · from below, s11 · s12)", "base",
     "? build 4: no third row yet"),
    ("Delivery cards", "Task", "Delivery (◆ Ready, then Web · LaTeX · Word · Slides · Render, s13)", "base cards + "
     "own Ready", ""),
    ("Table · Reading", "Task", "Audience Report › Table · Reading", "the base's Page Task views",
     "embedded, in the Page's own look"),
    ("Draft-… · Evidence-…", "Task", "Work Details", "the base's Page Task views", "embedded, in the Page's own look"),
    ("Reader contract", "Task", "Description › Scope (◆)", "own lines in a base table", ""),
    ("SUB-* rows", "Task", "Description › Requirement (◆)", "own lines in a base row", ""),
    ("Tags", "all", "—", "none (b03 s32-D09)", "? {n} kinds drawn today: remove"),
    ("Page header", "all", "the title line", "base", ""),
    ("One item's display", "Task", "a Section opens as the Task tab", "base",
     "? a Section's ↗ and a run row: point at /_board/workbench?…&view=draft"),
]


def frame_theme_elements(x0, y0, facts) -> dict:
    fr = L.open_frame("11 · The paper theme's own elements · proposed")
    text(x0, y0, "11 · Theme elements · proposed", 34)
    text(x0, y0 + 50, "every element the paper uses, planned in s11 · s12 · s13: same as the base, or its own and why; "
                      "red: what today's frame does not draw yet", 18)
    canvas_note(x0, y0 + 100, "decided (b03, 261008): old cards kept; question views take question_cell(); build order 1–4 in the list")
    heads = ("element", "level", "Space › view", "base or own", "drawn today")
    xs = [0, 230, 420, 1420, 1900]
    y = y0 + 160
    for hx, h in zip(xs, heads):
        text(x0 + hx, y, h, 18)
    y += 36
    L.path([(x0, y - 4), (x0 + 2500, y - 4)], arrow=False, color=INK)
    for row in THEME_ELEMENTS:
        for hx, cell in zip(xs, row):
            cell = cell.replace("{n}", str(sum(1 for f in facts.values() if f.get("element") == "tags" and not f.get("old"))))
            text(x0 + hx, y, cell or "✓", 15, RED if cell.startswith("?") else INK)
        y += 30
    L.close_frame(fr)
    return fr


PICKED = {"tabs": "D · E (b03 s32-D01), from the base", "views": "E (b03 s32-D02), from the base",
          "report": "the Insight row (b03 s32-D05)", "runs": "Disk inside Runs (b03 s32-D08)",
          "tags": "none (b03 s32-D09)"}


def frame_pick(x0, y0) -> dict:
    fr = L.open_frame("Pick")
    text(x0, y0, "Pick: one look per paper element", 34)
    text(x0, y0 + 50, "b03's picks hold for the paper; write the letter you keep for the rest (or draw a new one)", 18)
    for i, el in enumerate(ELEMENTS):
        text(x0, y0 + 120 + i * 44, f"{el['title']}  —  {el['what']}", 20)
        if el["key"] in PICKED:
            text(x0 + 1000, y0 + 120 + i * 44, "kept: " + PICKED[el["key"]], 20, GREEN)
        else:
            text(x0 + 1000, y0 + 120 + i * 44, "? keep: __", 20, RED)
    L.close_frame(fr)
    return fr


def frame_title(x0, y0, facts) -> dict:
    fr = L.open_frame("s32 · Paper element UI")
    text(x0, y0, "s32 · Paper element UI", 44)
    n = sum(1 for k in facts if not k.startswith("proposed__"))
    olds = sum(1 for k, f in facts.items() if f.get("old"))
    text(x0, y0 + 70, f"every element the paper theme draws today ({n} versions, {olds} on old pages), "
                      "one frame each with its proposed look beside it", 20)
    text(x0, y0 + 104, "after b03 s32-element-ui; live from the frame at Block · Job · Task, every Space and view", 20)
    for i, (date, what) in enumerate(CHANGES):
        canvas_note(x0, y0 + 160 + i * 34, what, date)
    L.close_frame(fr)
    return fr


def draw(out: Path) -> None:
    facts = json.loads((SHOTS / "facts.json").read_text()) if (SHOTS / "facts.json").exists() else {}
    L.els.clear()
    L.FRAME[0] = None
    B.FILES.clear()
    frame_title(0, -700, facts)
    y = 0
    for el in ELEMENTS:
        per_row = 4 if el["key"] in ("space", "tags", "views") else 3
        fr = frame_element(el, 0, y, facts, per_row)
        right = fr["x"] + fr["width"] + 200
        if el["key"] in PROPOSALS:
            pr = frame_proposed(el["key"], el["title"], right, y, facts)
        elif el["key"] == "own":
            pr = frame_theme_elements(right, y, facts)
        else:
            pr = fr
        y = max(fr["y"] + fr["height"], pr["y"] + pr["height"]) + 200
    frame_pick(4 * CARD_W + 2000, -900)
    canvas.write(out, list(L.els), "build_s32_paper_element_ui.py", files=B.FILES)


if __name__ == "__main__":
    if "--shoot" in sys.argv:
        url = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "http://127.0.0.1:5851"
        shoot(url.rstrip("/"))
    draw(HERE / "s32-paper-element-ui.excalidraw")
