"""s32 · Element UI: s32-element-ui.excalidraw, a gallery of every kind of workbench element as each
workbench draws it today, side by side, to pick one look per element (JL 261007: "collect all types
of the UI of different types of the element ... so we can unify them"; "for each type of the
element, show the different versions, like the gallery, and we will pick and select. Like for the
audience report, we might have different versions as well").

Two steps:

    uv run --with playwright python build_s32_element_ui.py --shoot [--base http://127.0.0.1:5851]
        opens each workbench page in headless Chrome (a live host serving this SPACE), screenshots
        each element into shots/<element>__<page>.png, and writes its computed style into
        shots/facts.json (font size, corner radius, padding, border and fill of its first button
        or cell). Rerun after a look changes.
    python build_s32_element_ui.py
        draws the gallery from shots/: one frame per element kind, one card per version (the
        workbench, its page, its picture, its style line), then a Pick frame. Marks are kept
        on rebuild (canvas.write).

The pages are the frame (the new base) and every older page still served beside it. A version
an element has not on a page is left out; cowork has no Block on disk, so no card.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import sys
import urllib.parse as U
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "shots"
SERVERS = HERE.parents[3] / "plugins" / "haipipe-toolkit" / "servers"
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE.parent / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402

INK, GRAY, RED, TEAL = L.INK, L.GRAY, L.RED, L.TEAL
text, base = L.text, L.base


def q(path: str) -> str:
    return U.quote(path, safe="")


B03 = "Tools/designs/b03_project_workbench"
# (key, label: which workbench and how new, its URL). The frame first, then the older pages.
PAGES = [
    ("frame", "the frame (new base) · vanilla Block",
     f"/_board/workbench?path={q(B03)}&space=Audience+Report"),
    ("frame-studio", "the frame · Idea Studio",
     f"/_board/workbench?path={q(B03)}&space=Idea+Studio"),
    ("paper", "paper Board page (on the frame's look)",
     f"/_board/paper-board?path={q('examples-4-learning/Project-ExpLearn-SMSDesign/paper/Paper-TestToLearn-MS2026/board.md')}&file=board.md"),
    ("work", "work Block page (old task-board)",
     f"/_board/work-board?path={q(B03 + '/board.md')}"),
    ("insight", "Insight board page",
     f"/_board/insight-board?path={q('examples-5-design/Project-Application-SMSDesign/insights/SMSR2v1-InsightBoard/board.md')}&file=board.md"),
    ("design", "Design board page",
     f"/_board/design-board?path={q('examples-5-design/Project-Application-SMSDesign/designs/B01_DesignBoard-Stage25-CarryOver-261005/board.md')}&file=board.md"),
    ("discovery", "Discovery board page",
     f"/_board/discovery-board?path={q('examples-4-learning/Project-ExpLearn-SMSDesign/discoveries/b01_experimental_learning_evidence/board.md')}"),
    ("labeling", "Labeling board page",
     f"/_board/labeling-board?path={q('examples-6-labeling/Project-Labeling-SafeResponse/tasks/b61_response_safety/board.md')}&file=board.md"),
    # one item's own display (JL 261008: "I didn't see where to have display for the design items")
    ("frame-design", "the frame · an older Design Folder (its Task, Work Details › Designs)",
     f"/_board/workbench?path={q('examples-5-design/Project-Application-SMSDesign/designs/B01_DesignBoard-Stage25-CarryOver-261005/2-Design-M01-goal-only/Design-01-all-patients-prescription-review-sms')}&space=Work+Details"),
    ("design-item", "Design item page (one design)",
     f"/_board/design?path={q('/examples-5-design/Project-Application-SMSDesign/designs/B01_DesignBoard-Stage25-CarryOver-261005/board.md')}&file={q('2-Design-M01-goal-only/Design-01-all-patients-prescription-review-sms/Design-01-all-patients-prescription-review-sms.md')}&space=design"),
    # a design Job on the ladder: no Project holds one yet, so the design tests' sample Block (design_fixture.py)
    ("frame-design-job", "the frame · a design Job › Audience Report › Design display (the tests' sample Job)",
     "demo:design-job"),
    ("frame-authenui", "the frame · an older board in designs/_old/ (AuthenUI's login design, its Task)",
     f"/_board/workbench?path={q('examples-5-design/Project-Application-SMSDesign/designs/_old/B01_DesignBoard-AuthenUI-260917/2-Design/Design-01-all-patients-log-in-with-date-of-birth-ui-card')}&space=Work+Details"),
    ("design-ui-item", "Design item page, a UI design (AuthenUI, one login card)",
     f"/_board/design?path={q('/examples-5-design/Project-Application-SMSDesign/designs/_old/B01_DesignBoard-AuthenUI-260917/board.md')}&file={q('2-Design/Design-01-all-patients-log-in-with-date-of-birth-ui-card/Design-01-all-patients-log-in-with-date-of-birth-ui-card.md')}&space=design"),
    ("insight-item", "Insight page (one question page)", "/_board/insight?board=SMSR2v1-InsightBoard&page=MT01"),
    ("insight-run", "Insight run page (one run's results)",
     "/_board/insight-run?board=SMSR2v1-InsightBoard&task=b51_sms_dikw/j11_data_extract/t01_extract_shape"
     "&call=run_b51j11t01r01_full_extract_shape&page=D01-full-extract-shape"),
    ("labeling-item", "Labeling job page (one job)",       # its link exactly as the labeling board writes it
     "from:" + f"/_board/labeling-board?path={q('examples-6-labeling/Project-Labeling-SafeResponse/tasks/b61_response_safety/board.md')}"
     "&file=board.md|/_board/labeling?"),
    ("page", "Page workbench (one Page's Draft)",
     f"/_board/workbench?view=draft&path={q(B03 + '/reports/q03_block_questions/q03_block_questions.md')}"),
]
# (key, title, what it is, {page: selector}). A selector "a|b" is the box around both; "parent:x"
# is x's parent; the first visible match is taken.
ELEMENTS = [
    ("tabs", "1 · Top tabs", "the row you choose a Space (and a level) from",
     {"frame": "nav.levels|nav.spaces", "paper": "nav.levels|nav.spaces", "work": "nav.spaces",
      "insight": "nav.spaces", "design": "nav.spaces", "discovery": "nav.spaces", "labeling": "nav.spaces",
      "page": "div.spaces"}),
    ("views", "2 · View row (third row)", "the views or groups of the open Space",
     {"frame": "nav.subs", "paper": "nav.subs", "work": "parent:.wtab", "insight": ".parts",
      "discovery": "parent:.wtab", "page": ".draft-mode-switcher"}),
    ("report", "3 · Audience Report: the Question rows", "one Question with its work and its report",
     {"frame": ".q-row:not(.q-head-row)", "work": ".hl-row", "insight": ".hl-row.on",
      "discovery": "table"}),
    ("space", "4 · The Space body", "the open Space's box, its first screen",
     {"frame": ".space-main", "frame-studio": ".space-main", "paper": ".space-main", "work": ".pane.on",
      "insight": ".pane.on .shell", "design": ".space-main", "discovery": ".pane.on", "labeling": ".space-main",
      "page": ".space-main"}),
    ("table", "5 · Tables", "rows of items",
     {"paper": "table.wf-table", "design": "table.msgs", "discovery": "table", "insight": ".pane.on table"}),
    ("cards", "6 · Rows and cards", "one item, closed or open",
     {"frame-studio": ".space-main details,.space-main .topic", "labeling": ".card", "insight": "details.lvl",
      "work": "details.q-more", "design": ".pane.on .card,.pane.on details"}),
    ("runs", "7 · Disk · Runs panel", "the files behind the open Space, its run types and their runs (the Disk box is "
     "inside it now, one fold; JL 261007: \"this one can be removed, as the Disk and Runs are together\")",
     {"frame": "section.runs-panel", "paper": "section.runs-panel", "design": "section.runs-panel",
      "work": ".pane.on .runs-panel", "insight": ".pane.on .runs-panel", "discovery": ".pane.on .runs-panel",
      "page": ".runs-panel"}),
    ("tags", "8 · Tags and pills", "a state or a count on an item",
     {"discovery": ".pill", "labeling": ".pill", "insight": ".pill", "work": ".pill", "frame": ".tag,.chip,.pill"}),
    ("header", "9 · Page header", "the title line at the top",
     {"frame": "header", "work": "header", "insight": "header", "design": "header", "discovery": "header",
      "labeling": "h1", "paper": "header", "page": "header,h1"}),
    ("item", "10 · One item's display", "one design, one question page, one labeling job, one run: the item itself",
     {"frame-design": ".space-main", "design-item": ".space-main,main", "design-ui-item": ".space-main,main", "insight-item": "main,body",
      "insight-run": "main,body", "labeling-item": ".space-main,main,body"}),
    ("design", "11 · Design display", "a design Job's design items: the Job's Audience Report › Design display "
     "(JL 261008: \"we will in the Design-Job's Audience Report's Design Display show the Design Items\")",
     {"frame-design-job": ".space-main", "frame-design": ".space-main", "frame-authenui": ".space-main",
      "design-item": ".space-main,main", "design-ui-item": ".space-main,main"}),
]
# what is picked, per element (JL's marks on the gallery): the look only, never the content; each
# workbench keeps its own tabs and words and takes the picked style
PICKED = {"tabs": "D · E (Insight, Design): 16px, 6px corners, grey border, the open one washed blue; "
                  "the frame took it 261007",
          "tags": "none: no tags in any theme; 261008",
          "space": "Idea Studio: B kept as it is; Insight board: E kept for the insight theme only; 261007",
          "views": "E (the Page workbench's view buttons): 16px, 6px corners, padding 5px 12px, the open one washed "
                   "blue; not the small pills; the frame took it 261007"}
# the proposed unified look per element (JL 261007: "we want to unify things ... for each frame, add a new
# frame to the right of it and draw the proposed new one and explain why"): the frame is the base every
# theme draws on, so where it already draws an element in the picked look, its own version is the
# proposal; (url, selector) is shot live like the cards, a "mock:" is drawn in the frame's colours
FRAME_URL = f"/_board/workbench?path={q(B03)}"
PROPOSALS = {
    "tabs": (FRAME_URL + "&space=Audience+Report", "nav.levels|nav.spaces",
             ["picked D · E (s32-D01): one button shape for every top row, the open one washed blue",
              "the look only: the frame keeps its level row and its six Spaces, a theme its words",
              "optional Spaces drawn solid like the rest"]),
    "views": (f"/_board/workbench?path={q('examples-4-learning/Project-ExpLearn-SMSDesign/paper/Paper-TestToLearn-MS2026')}"
              "&space=Description", "nav.subs",
              ["picked E (s32-D02): the tabs' shape, padding 5px 12px, so the third row reads as one family",
               "not the small pills: they read as tags, not as views"]),
    "report": (FRAME_URL + "&space=Audience+Report", ".q-head-row|.q-row:not(.q-head-row)",
               ["one row per Question at every level and in every theme: Question │ Work │ Report (s04-D04)",
                "the Question cell as the Insight row (JL 261007): a label (Question 1) and its state dot, the "
                "Question's short name, one sentence of what is asked, › More; no 'builds on' line",
                "Insight's and work's rows already have the three columns; discovery's table becomes these rows",
                "the Report cell: title, answer line, the drawing's thumbnail, a tag"]),
    "space": (FRAME_URL + "&space=Audience+Report", ".split",
              ["one content box (1px border, 10px corners) and one right column, Disk · Runs",
               "every theme fills the box; none restyles it or draws its own page around it"]),
    "table": (FRAME_URL + "&space=Runs", "table.wf-table",
              ["the frame's light table: small grey heads, rows ruled by one line, no boxed cells",
               "an item with a body of its own is a row (6), not a table cell"]),
    "cards": (FRAME_URL + "&space=Idea+Studio", ".space-main details",
              ["one closed row per item: ▸ name · its facts · ↗, opened in place (Idea Studio's topic rows)",
               "the same as the Disk and Runs rows; a card only for the one item that is open"]),
    "runs": (FRAME_URL + "&space=Idea+Studio", "section.runs-panel",
             ["Disk, then Runs, in one panel with one fold; Disk: groups with a label and a count, one row per "
              "file or folder, 4 shown then +N more",
              "one row per run type, named by its Run (run-<type>-<target>), what it does under it",
              "a type's Runs as rows; a card opens only when its row is clicked"]),
    "tags": ("none:", "", ["none: no tags in any theme (JL 261008: \"we don't use any of them, just remove all\")",
                           "a state is a word (open · partial · answered) or the Question's state dot",
                           "an id is plain text where it stands (Q01, run-draw-s01)"]),
    "item": (f"/_board/workbench?path={q('examples-5-design/Project-Application-SMSDesign/designs/B01_DesignBoard-Stage25-CarryOver-261005/2-Design-M01-goal-only/Design-01-all-patients-prescription-review-sms')}&space=Work+Details", ".space-main",
             ["one item opens in the frame: as its own level's Spaces (a design is a Task: its Work Details "
              "holds the design, its rationale and its evaluation), or in the frame's pop-out from its row",
              "no item page of its own beside the frame: the design, insight, labeling and run pages retire",
              "the theme gives the item's words and fields; the frame gives the box, the rows and the Runs"]),
    "design": ("demo:design-job", ".space-main",
               ["a design Job's items live in its Audience Report › Design display: one row per design, the design "
                "as it reads │ its process (③: the idea, each element's source) │ its review (④ ⑤: verdict, rank)",
                "the first open, the rest one line each; the dropped ones folded, kept for the record",
                "an older board (Design-NN folders, designs/_old/) shows its old item view in place until it moves "
                "onto the ladder"]),
    "header": (FRAME_URL + "&space=Audience+Report", "header",
               ["one line: the theme's icon · its name · the folder; the path on hover",
                "no band, no dataset banner, no links row above the tabs"]),
}
# more pictures in a proposed frame, below its first: (url, selector, caption)
EXTRA_PROPOSALS = {
    "space": [(FRAME_URL + "&space=Idea+Studio", ".space-main",
               "Idea Studio: kept as it is, card B (JL 261007: \"for the idea studio, we will just keep this\"): "
               "one closed row per topic, its facts and the Questions it feeds, opened in place"),
              (f"/_board/insight-board?path={q('examples-5-design/Project-Application-SMSDesign/insights/SMSR2v1-InsightBoard/board.md')}"
               "&file=board.md", ".pane.on .shell",
               "Insight only, card E kept for the insight theme (JL 261007: \"this is for the Insight board only\"): "
               "its partitions as views, its levels folded, a Question │ Work │ Report row per question")],
}
# a short green note where a change was made (JL 261007: "my comments with the green short words in where
# the changes made"), drawn over each proposed picture
CHANGED = {"tabs": "changed: the D · E look (s32-D01)", "views": "changed: the E look, no pills (s32-D02)",
           "report": "changed: the Question cell as Insight's (s32-D05)",
           "space": "kept: the frame's body; Idea Studio as is (s32-D06)",
           "runs": "changed: Disk in Runs, one fold · rows · Run names",
           "tags": "changed: no tags at all (s32-D09)", "table": "kept: the frame's table",
           "cards": "kept: the frame's rows",
           "item": "proposed: an item opens in the frame (its level, or the pop-out)",
           "design": "built: Job › Audience Report › Design display; older boards in place (b12, 261008)",
           "item-open": "? labeling: its job page refuses a direct open (400), so it has no card yet", "header": "kept: one line, no band"}
MOCK_CSS = """body{margin:0;padding:16px;font:16px system-ui,sans-serif;background:#fff}
#m{display:inline-flex;gap:8px;padding:8px}
.tg{display:inline-block;border:1px solid;border-radius:999px;padding:1px 9px;font:12px system-ui,sans-serif}
.ok{color:#24733d;border-color:#24733d;background:#e5f1e7}.warn{color:#996b00;border-color:#996b00;background:#f8ebe1}
.mut{color:#6f6f6b;border-color:#ced4da;background:#fff}.bad{color:#c92a2a;border-color:#c92a2a;background:#f5e6e6}
.acc{color:#1864ab;border-color:#1864ab;background:#e7f5ff}"""
MAX_H = 700                     # a screenshot is cut at this height (the element's first screen)

PICK_JS = """(sel) => {
  const one = s => { if (s.startsWith('parent:')) { const c = document.querySelector(s.slice(7));
                       return c ? c.parentElement : null; }
                     for (const e of document.querySelectorAll(s)) { const r = e.getBoundingClientRect();
                       if (r.width > 4 && r.height > 4) return e; } return null; };
  const els = sel.split('|').map(one).filter(Boolean);
  if (!els.length) return null;
  // a row as wide as the page holds a few buttons at its left: take the box around what it holds
  const tight = e => { const r = e.getBoundingClientRect();
    const kids = [...e.children].map(c => c.getBoundingClientRect()).filter(k => k.width > 2 && k.height > 2);
    if (!kids.length) return r;
    const right = Math.max(...kids.map(k => k.right)) + 8;
    return right < r.left + 0.8 * r.width ? {left: r.left, top: r.top, right, bottom: r.bottom} : r; };
  const rs = els.map(tight);
  const x = Math.min(...rs.map(r => r.left)), y = Math.min(...rs.map(r => r.top));
  const w = Math.max(...rs.map(r => r.right)) - x, h = Math.max(...rs.map(r => r.bottom)) - y;
  const probe = els[0].querySelector('button, a, select, th, td, summary') || els[0];
  const cs = getComputedStyle(probe);
  const style = {font: cs.fontSize + ' ' + cs.fontWeight, radius: cs.borderTopLeftRadius,
                 padding: cs.paddingTop + ' ' + cs.paddingLeft, border: cs.borderTopColor,
                 fill: cs.backgroundColor, tag: probe.tagName.toLowerCase() + (probe.className ? '.' + String(probe.className).split(' ')[0] : '')};
  return {x: x + scrollX, y: y + scrollY, w, h, style};
}"""


DEMO_PY = r"""
import sys, tempfile
from pathlib import Path
T = Path(sys.argv[1])
sys.path.insert(0, str(T / "_host")); sys.path.insert(0, str(T / "workbench-design" / "tests"))
from host_paths import bootstrap; bootstrap()
from live import frame
from live.design_theme import THEME
import design_fixture as F
root = Path(tempfile.mkdtemp()).resolve()
job = F.make(root) / F.BLOCK / "j03_g01_m04"
Path(sys.argv[2]).write_text(frame.render(THEME, root, job, "Audience Report", "Design display"), encoding="utf-8")
"""


def render_demos() -> dict:
    """{name: file URL} of the sample pages no Project holds yet, rendered by the SPACE's own Python."""
    import subprocess
    space = HERE.parents[4]
    py = space / ".venv" / "bin" / "python"
    out = SHOTS / "demo-design-job.html"
    done = subprocess.run([str(py), "-c", DEMO_PY, str(SERVERS), str(out)], capture_output=True, text=True)
    if done.returncode or not out.exists():
        print("design-job sample:", (done.stderr or "").strip().splitlines()[-1:] or "failed")
        return {}
    return {"design-job": out.resolve().as_uri()}


def shoot(base_url: str) -> None:
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(exist_ok=True)
    for old in SHOTS.glob("*.png"):
        old.unlink()
    facts = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 1100}, device_scale_factor=1)
        demos = render_demos()
        for key, label, url in PAGES:
            if url.startswith("demo:"):
                if url[5:] not in demos:
                    print(f"{key}: no sample, skipped")
                    continue
                page.goto(demos[url[5:]])
                page.wait_for_timeout(500)
                for ekey, _, _, sels in ELEMENTS:
                    sel = sels.get(key)
                    box = page.evaluate(PICK_JS, sel) if sel else None
                    if box:
                        page.screenshot(path=str(SHOTS / f"{ekey}__{key}.png"), full_page=True,
                                        clip={"x": box["x"], "y": box["y"], "width": max(box["w"], 1),
                                              "height": min(max(box["h"], 1), MAX_H)})
                        facts[f"{ekey}__{key}"] = {"page": label, "url": url, "selector": sel,
                                                   "cut": box["h"] > MAX_H, **box["style"]}
                continue
            if url.startswith("from:"):                    # the first link of that kind on another page
                board, prefix = url[5:].split("|", 1)
                page.goto(base_url + board)
                page.wait_for_timeout(600)
                found = page.evaluate("p => { const a = [...document.querySelectorAll('a[href]')]"
                                      ".find(a => a.getAttribute('href').startsWith(p)); return a ? a.getAttribute('href') : ''; }",
                                      prefix)
                if not found:
                    print(f"{key}: no {prefix} link on its board, skipped")
                    continue
                url = found
            resp = page.goto(base_url + url)
            page.wait_for_timeout(900)
            # a Runs panel starts folded on some pages: open it, so every version shows its contents
            page.evaluate("document.querySelectorAll('.runs-panel.folded').forEach(p => p.classList.remove('folded'))")
            page.wait_for_timeout(200)
            if not resp or resp.status != 200:
                print(f"{key}: HTTP {resp.status if resp else '?'}, skipped")
                continue
            for ekey, _, _, sels in ELEMENTS:
                sel = sels.get(key)
                if not sel:
                    continue
                box = None
                for alt in sel.split(","):          # "a,b": the first that is on the page
                    box = page.evaluate(PICK_JS, alt.strip())
                    if box:
                        break
                if not box:
                    continue
                clip = {"x": box["x"], "y": box["y"], "width": max(box["w"], 1), "height": min(max(box["h"], 1), MAX_H)}
                out = SHOTS / f"{ekey}__{key}.png"
                page.screenshot(path=str(out), clip=clip, full_page=True)
                facts[f"{ekey}__{key}"] = {"page": label, "url": url, "selector": sel,
                                           "cut": box["h"] > MAX_H, **box["style"]}
        for key, (url, sel, _) in PROPOSALS.items():   # the proposed look per element
            if url.startswith("none:"):                   # proposed: nothing to show
                continue
            if url.startswith("demo:"):
                if url[5:] not in demos:
                    continue
                page.goto(demos[url[5:]])
                page.wait_for_timeout(500)
                box = page.evaluate(PICK_JS, sel)
                if box:
                    page.screenshot(path=str(SHOTS / f"proposed__{key}.png"), full_page=True,
                                    clip={"x": box["x"], "y": box["y"], "width": max(box["w"], 1),
                                          "height": min(max(box["h"], 1), MAX_H)})
                    facts[f"proposed__{key}"] = {"page": "proposed", "url": url, "selector": sel,
                                                 "cut": box["h"] > MAX_H, **box["style"]}
                continue
            if url.startswith("mock:"):
                page.set_content(f"<style>{MOCK_CSS}</style><div id=m>{url[5:]}</div>")
            else:
                page.goto(base_url + url)
                page.wait_for_timeout(900)
                page.evaluate("document.querySelectorAll('.runs-panel.folded').forEach(p => p.classList.remove('folded'))")
            page.wait_for_timeout(200)
            box = page.evaluate(PICK_JS, sel)
            if not box:
                print(f"proposal {key}: {sel} not found")
                continue
            page.screenshot(path=str(SHOTS / f"proposed__{key}.png"), full_page=True,
                            clip={"x": box["x"], "y": box["y"], "width": max(box["w"], 1), "height": min(max(box["h"], 1), MAX_H)})
            facts[f"proposed__{key}"] = {"page": "proposed", "url": url if not url.startswith("mock:") else "mock",
                                         "selector": sel, "cut": box["h"] > MAX_H, **box["style"]}
        for key, extras in EXTRA_PROPOSALS.items():     # the extra pictures of a proposed frame
            for n, (url, sel, _) in enumerate(extras, 1):
                page.goto(base_url + url)
                page.wait_for_timeout(900)
                box = page.evaluate(PICK_JS, sel)
                if box:
                    page.screenshot(path=str(SHOTS / f"proposed__{key}__{n}.png"), full_page=True,
                                    clip={"x": box["x"], "y": box["y"], "width": max(box["w"], 1),
                                          "height": min(max(box["h"], 1), MAX_H)})
        browser.close()
    (SHOTS / "facts.json").write_text(json.dumps(facts, indent=1, ensure_ascii=False))
    print(f"{len(facts)} shots in {SHOTS.relative_to(HERE.parent)}")


# ── the drawing ────────────────────────────────────────────────────────────────────────────────
CARD_W = 720                    # a card's picture width in the drawing (pictures are shown at most 1:1)
FILES = {}


def picture(path: Path, x: float, y: float, frame_w: float) -> float:
    """An image element for one screenshot at (x, y), at most `frame_w` wide; returns its height."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > 1400:
        im = im.resize((1400, round(im.height * 1400 / im.width)))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    raw = buf.getvalue()
    fid = hashlib.sha1(raw).hexdigest()[:20]
    FILES[fid] = {"mimeType": "image/png", "id": fid, "created": 1,
                  "dataURL": "data:image/png;base64," + base64.b64encode(raw).decode()}
    w = min(frame_w, im.width)
    h = im.height * w / im.width
    L.els.append({"id": f"img-{fid}-{round(x)}-{round(y)}", "type": "image", "x": x, "y": y, "width": w, "height": h, "angle": 0,
                  "strokeColor": "transparent", "backgroundColor": "transparent", "fillStyle": "solid",
                  "strokeWidth": 1, "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [],
                  "frameId": L.FRAME[0], "roundness": None, "seed": 1, "version": 1, "versionNonce": 1,
                  "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False,
                  "status": "saved", "fileId": fid, "scale": [1, 1]})
    base("rectangle", x - 1, y - 1, w + 2, h + 2, GRAY, 1, rough=0)
    LAST_W[0] = w
    return h


LAST_W = [0]


def style_line(f: dict) -> str:
    return (f"{f.get('tag', '')}: font {f.get('font', '')} · radius {f.get('radius', '')} · "
            f"padding {f.get('padding', '')}\nborder {f.get('border', '')} · fill {f.get('fill', '')}")


# which page each older card shows, by its theme: once a theme draws on the frame (its <theme>_theme.py),
# its old page is retiring (JL 261007: "some of them are old version and we will not use it ... flag them")
PAGE_THEME = {"paper": "paper", "work": "work", "insight": "insight", "design": "design",
              "discovery": "discovery", "labeling": "labeling", "design-item": "design", "design-ui-item": "design", "insight-item": "insight",
              "insight-run": "insight", "labeling-item": "labeling"}   # the frame's own pages are current


def old_reason(key: str) -> str:
    """Why a card's page is an old version, read off the code; "" for the frame (the current one)."""
    theme = PAGE_THEME.get(key)
    if theme and (SERVERS / f"workbench-{theme}" / f"{theme}_theme.py").is_file():
        return f"old page: the {theme} theme draws on the frame now; this page retires"
    if key == "page" and "VIEW_METHODS" in (SERVERS / "workbench" / "frame_view.py").read_text(encoding="utf-8"):
        return "old page: a Page's views are the frame's Task Spaces now; this page retires"
    return ""


def frame_element(ekey, title, what, x0, y0, facts) -> dict:
    fr = L.open_frame(title)
    text(x0, y0, title, 34)
    versions = [(k, label) for k, label, _ in PAGES if (SHOTS / f"{ekey}__{k}.png").exists()]
    olds = sum(bool(old_reason(k)) for k, _ in versions)
    text(x0, y0 + 50, f"{what} · {len(versions)} versions today, {olds} of them on old pages (flagged OLD: they retire; "
                      "a look from one may still be picked); mark the one to keep (or draw your own beside them)", 18, GRAY)
    x, y, row_h = x0, y0 + 120, 0
    for i, (k, label) in enumerate(versions):
        if i and i % 3 == 0:
            x, y, row_h = x0, y + row_h + 80, 0
        f = facts.get(f"{ekey}__{k}", {})
        why = old_reason(k)
        if why:                                  # an old page: flagged, greyed, a red dashed box around it
            text(x, y - 26, "OLD · " + why, 14, RED)
        text(x, y, f"{chr(65 + i)} · {label}", 20, GRAY if why else INK)
        h = picture(SHOTS / f"{ekey}__{k}.png", x, y + 40, CARD_W)
        if why:
            base("rectangle", x - 8, y + 32, LAST_W[0] + 16, h + 16, RED, 1.5, dashed=True, rough=0)
        text(x, y + 52 + h, style_line(f) + ("\n(cut at its first screen)" if f.get("cut") else ""), 14, GRAY, L.MONO)
        row_h = max(row_h, 52 + h + 60)
        x += CARD_W + 80
    if not versions:
        text(x0, y0 + 120, "no shots yet: run with --shoot", 18, RED)
    L.close_frame(fr)
    return fr


def frame_proposed(ekey, title, x0, y0, facts) -> dict:
    """The proposed look of one element, beside its gallery frame: the picture, its numbers, and why."""
    fr = L.open_frame(title + " · proposed")
    text(x0, y0, title + " · proposed", 34)
    _, sel, why = PROPOSALS[ekey]
    text(x0, y0 + 50, "one look for every theme, drawn by the base (servers/workbench); a theme gives the words only",
         18, GRAY)
    shot = SHOTS / f"proposed__{ekey}.png"
    y = y0 + 110
    if ekey in CHANGED:
        text(x0, y, CHANGED[ekey], 20, "#2f9e44")     # green: what changed here
        y += 40
    if ekey + "-open" in CHANGED:
        text(x0, y, CHANGED[ekey + "-open"], 18, RED)  # red: still open
        y += 40
    if shot.exists():
        h = picture(shot, x0, y, 1000)
        f = facts.get(f"proposed__{ekey}", {})
        text(x0, y + h + 12, style_line(f), 14, GRAY, L.MONO)
        y += h + 70
    elif PROPOSALS[ekey][0].startswith("none:"):
        text(x0, y, "(none)", 28, GRAY)
        y += 60
    else:
        text(x0, y, "no shot yet: run with --shoot", 18, RED)
        y += 40
    for n, (_, _, caption) in enumerate(EXTRA_PROPOSALS.get(ekey, []), 1):
        extra = SHOTS / f"proposed__{ekey}__{n}.png"
        if extra.exists():
            text(x0, y, caption, 17, "#2f9e44")       # a decided change: green
            h = picture(extra, x0, y + 34, 1000)
            y += h + 80
    text(x0, y + 10, "why", 22)
    for i, line in enumerate(why):
        text(x0 + 20, y + 50 + i * 30, "· " + line, 17)
    L.close_frame(fr)
    return fr


DESIGNS = HERE.parents[2]                        # Tools/designs: every theme Block's own s32 sits under it


def theme_tracks() -> list:
    """(Block, its s32 folder or None, its frame names, decided, open, its "Theme elements" lines) for every
    theme Block (b1N_theme_*), read off its s32 at build time (JL 261008: "for your own s32, you should
    track these theme based element UI as well")."""
    import re
    out = []
    for block in sorted(DESIGNS.glob("b1[0-9]_theme_*")):
        topic = next(iter(sorted((block / "studio").glob("s32-*"))), None)
        if topic is None:
            out.append((block.name, None, [], 0, 0, []))
            continue
        md = next(iter(sorted(topic.glob("s32-*.md"))), None)
        text_ = md.read_text(encoding="utf-8") if md else ""
        drawing = next(iter(sorted(topic.glob("s32-*.excalidraw"))), None)
        frames = []
        if drawing:
            try:
                frames = [e.get("name") for e in json.loads(drawing.read_text())["elements"]
                          if e.get("type") == "frame" and not e.get("isDeleted")]
            except (OSError, ValueError):
                frames = []
        m = re.search(r"(?ims)^(?:#+\s*)?Theme elements[^\n]*\n(?:[-=]{3,}\n)?(.*?)(?=^\S[^\n]*\n[-=]{3,}\n|^#+ |\Z)", text_)
        lines = [ln.rstrip() for ln in (m.group(1).splitlines() if m else []) if ln.strip()][:40]
        decided = len(re.findall(r"(?m)^s32-D\d+", text_))
        opened = len(re.findall(r"(?m)^\s*(?:\d+\.|-)\s", text_.split("\nOpen\n", 1)[1])) if "\nOpen\n" in text_ else 0
        out.append((block.name, topic, frames, decided, opened, lines))
    return out


def frame_themes(x0, y0) -> dict:
    """Every theme's own element UI, as its Block's s32 lists it: which theme has started, its frames, its
    decisions and open points, and its "Theme elements" list; rebuilt from their files on every build."""
    fr = L.open_frame("Theme elements")
    text(x0, y0, "Theme elements: what each theme uses, from its own s32", 34)
    text(x0, y0 + 50, "read from Tools/designs/b1N_theme_*/studio/s32-*/ on every build: its frames, decisions, open "
                      "points, and the list under its \"Theme elements\" heading", 18, GRAY)
    y = y0 + 120
    for block, topic, frames, decided, opened, lines in theme_tracks():
        if topic is None:
            text(x0, y, block, 22, GRAY)
            text(x0 + 520, y + 4, "not started: no studio/s32-* yet", 17, RED)
            y += 50
            continue
        text(x0, y, block, 22)
        text(x0 + 520, y + 4, f"{topic.name}/ · {len([f for f in frames if f])} frames · {decided} decided · "
                              f"{opened} open", 17, "#2f9e44" if decided else INK)
        y += 40
        if lines:
            text(x0 + 30, y, "\n".join(lines), 15, INK, L.MONO)
            y += 22 * len(lines) + 20
        else:
            text(x0 + 30, y, "? no \"Theme elements\" list yet in its notes", 16, RED)
            y += 40
        y += 20
    L.close_frame(fr)
    return fr


def frame_pick(x0, y0) -> dict:
    fr = L.open_frame("Pick")
    text(x0, y0, "Pick: one look per element", 34)
    text(x0, y0 + 50, "write the letter you keep beside each (or a new one); the base then draws it for every theme",
         18, GRAY)
    for i, (_, title, what, _) in enumerate(ELEMENTS):
        text(x0, y0 + 120 + i * 44, f"{title}  —  {what}", 20)
        key = ELEMENTS[i][0]
        if key in PICKED:
            text(x0 + 900, y0 + 120 + i * 44, "kept: " + PICKED[key], 20, "#2f9e44")   # a change: green
        else:
            text(x0 + 900, y0 + 120 + i * 44, "? keep: __", 20, RED)
    L.close_frame(fr)
    return fr


def draw(out: Path) -> None:
    facts = json.loads((SHOTS / "facts.json").read_text()) if (SHOTS / "facts.json").exists() else {}
    L.els.clear()
    L.FRAME[0] = None
    FILES.clear()
    width = 3 * CARD_W + 2 * 80 + 160
    y = 0
    frames = []
    for ekey, title, what, _ in ELEMENTS:
        fr = frame_element(ekey, title, what, 0, y, facts)
        frames.append(fr)
        pr = frame_proposed(ekey, title, fr["x"] + fr["width"] + 200, y, facts) if ekey in PROPOSALS else fr
        y = max(fr["y"] + fr["height"], pr["y"] + pr["height"]) + 200
    pk = frame_pick(width + 1500, -900)
    frame_themes(pk["x"] + pk["width"] + 300, -900)
    canvas.write(out, list(L.els), "build_s32_element_ui.py", files=FILES)


if __name__ == "__main__":
    if "--shoot" in sys.argv:
        url = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "http://127.0.0.1:5851"
        shoot(url.rstrip("/"))
    draw(Path(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].endswith(".excalidraw")
         else HERE / "s32-element-ui.excalidraw")
