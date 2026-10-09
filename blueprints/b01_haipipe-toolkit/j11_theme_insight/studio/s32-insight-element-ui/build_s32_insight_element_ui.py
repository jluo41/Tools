"""b11 s32 · Insight element UI: s32-insight-element-ui.excalidraw, a gallery of every kind of element the
insight theme draws today, one card per version, each beside a "· proposed" frame with the unified look
(b03 s32's picks), so the insight theme can take one look per element. It follows b03's element gallery
(Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s32-element-ui/) and imports its helpers.

Two steps:

    uv run --with playwright --with pillow python build_s32_insight_element_ui.py --shoot [--base http://127.0.0.1:5851]
        opens every insight page in headless Chrome (a live host serving this SPACE): the frame
        (/_board/workbench) at its Block, Job and Task levels, every Space and every view, for a plan-C
        Board and for today's-layout Insight Block; and the old insight board and item pages. It
        screenshots each element into shots/<element>__<page>.png and writes each one's computed style
        into shots/facts.json. Rerun after a look changes.
    python build_s32_insight_element_ui.py
        draws the gallery from shots/ (needs Pillow): a title frame, then per element its gallery frame
        (one card per version, old pages flagged OLD in red) and its proposed frame (the picture, why,
        a green line for what changed, a red line for what is open). Marks are kept on rebuild (canvas.write).
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
DESIGNS = HERE.parents[3]
B03_S32 = DESIGNS / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio" / "s32-element-ui"
sys.path.insert(0, str(B03_S32))
import build_s32_element_ui as S  # noqa: E402  (b03's gallery: its pick script, style line, drawing kit)

L, canvas, SERVERS = S.L, S.canvas, S.SERVERS
INK, GRAY, RED, GREEN = L.INK, L.GRAY, L.RED, canvas.GREEN
text, base = L.text, L.base
DATE = "261008"


def q(path: str) -> str:
    return U.quote(path, safe="")


PROJ = "examples-5-design/Project-Application-SMSDesign"
BOARD = f"{PROJ}/insights/SMSR2v1-InsightBoard"                 # plan C: its Jobs pair a release and a data version
JOB = f"{BOARD}/j01_p1_SMSR2v1"
TASK = f"{JOB}/t05_I01_funnel-fundamentals"
B52 = f"{PROJ}/tasks/b52_sms_question_dikw"                     # today's layout: an Insight Block, `workbench: insight`
B52J = f"{B52}/j01_data"
B52T = f"{B52J}/t01_extract_shape_and_quality"
B03 = "Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench"


def wb(folder: str, space: str, sub: str = "") -> str:
    return (f"/_board/workbench?path={q(folder)}&space={U.quote_plus(space)}"
            + (f"&sub={U.quote_plus(sub)}" if sub else ""))


# every Space and view the insight theme draws, per level: (level key, its name, folder, [(Space, [views])]).
# A partition is the same view on another cut, so one partition (Full) stands for them, and Cross once.
LEVELS = [
    ("block", "Board (plan C)", BOARD, [
        ("Description", ["Map", "Prototype", "Dataset", "Partitions"]), ("Idea Studio", [""]),
        ("Audience Report", ["Full/Coverage", "Full/Tracks", "Full/Consistency", "Full/Findings", "Cross/Findings"]),
        ("Work Details", ["All", "p1"]), ("Runs", ["All", "soft", "from below"]), ("Delivery", ["Handoff"])]),
    ("job", "Job (one release × one data version)", JOB, [
        ("Description", ["Prototype", "Dataset"]), ("Idea Studio", [""]),
        ("Audience Report", ["Full/Current", "Full/vs previous", "Cross/Current"]),
        ("Work Details", ["All", "hard", "soft"]),
        ("Runs", ["All", "hard", "soft", "launch", "power", "compare", "propose", "close"]), ("Delivery", [""])]),
    ("task", "Task (one question)", TASK, [
        ("Description", ["Question", "Records"]), ("Idea Studio", [""]), ("Audience Report", ["Table", "Reading"]),
        ("Work Details", ["Partitions"]), ("Runs", ["All", "hard", "soft"]), ("Delivery", [""])]),
    ("b52", "Insight Block, today's layout (Block)", B52, [
        ("Description", ["Map", "Prototype", "Dataset", "Partitions"]), ("Idea Studio", [""]),
        ("Audience Report", ["Full/Coverage", "Full/Tracks", "Full/Consistency", "Full/Findings"]),
        ("Work Details", [""]), ("Runs", [""]), ("Delivery", [""])]),
    ("b52job", "Insight Block, today's layout (a Job: the base's own)", B52J,
     [(s, [""]) for s in ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")]),
    ("b52task", "Insight Block, today's layout (a Task: the base's own)", B52T,
     [(s, [""]) for s in ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")]),
]
SHORT = {"block": "Board", "job": "Job", "task": "Task", "b52": "b52 Block", "b52job": "b52 Job", "b52task": "b52 Task"}


def slug(s: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-") or "default"


# (key, label, url): the frame's pages, then the old ones
PAGES = [(f"{lv}.{slug(sp)}.{slug(v)}", f"{SHORT[lv]} › {sp}" + (f" › {v.replace('/', ' / ')}" if v else ""),
          wb(folder, sp, v)) for lv, _, folder, spaces in LEVELS for sp, views in spaces for v in views]
OLD_BOARD = f"/_board/insight-board?path={q(BOARD + '/board.md')}&file=board.md"
OLD_B52 = f"/_board/insight-board?path={q(B52 + '/board.md')}&file=board.md"
OLD_SPACES = [("scope", "Scope"), ("prototype", "Prototype"), ("insight", "Insight"), ("check", "Check"), ("delivery", "Delivery")]
PAGES += [(f"old.{k}", f"old Insight board page › {lab}", f"{OLD_BOARD}&space={k}") for k, lab in OLD_SPACES]
PAGES += [(f"old52.{k}", f"old Insight board page (b52) › {lab}", f"{OLD_B52}&space={k}") for k, lab in OLD_SPACES]
PAGES += [
    ("old.item", "old Insight page (one question page, MT01)", "/_board/insight?board=SMSR2v1-InsightBoard&page=MT01"),
    ("old.run", "old Insight run page (one run's results)",
     "/_board/insight-run?board=SMSR2v1-InsightBoard&task=b51_sms_dikw/j11_data_extract/t01_extract_shape"
     "&call=run_b51j11t01r01_full_extract_shape&page=D01-full-extract-shape"),
    ("b03.report", "the frame, vanilla (b03): the Question cell as the Insight row (b03 s32-D05)",
     wb(B03, "Audience Report")),
]
LABEL = {k: lab for k, lab, _ in PAGES}


def P(lv: str, sp: str, v: str = "") -> str:
    return f"{lv}.{slug(sp)}.{slug(v)}"


ALL_FRAME = [k for k, _, _ in PAGES if not k.startswith(("old", "b03"))]
OLD_PANES = [f"old.{k}" for k, _ in OLD_SPACES]
# (key, title, what, [(page, selector)]). "a|b" is the box around both; "parent:x" is x's parent; "nth:N:x" is
# the Nth visible x; "a,b" the first of them on the page.
ELEMENTS = [
    ("tabs", "1 · Top tabs", "the level row (Guide · Block · Job ▾ · Task ▾) and the six Spaces",
     [(P("block", "Description", "Map"), "nav.levels|nav.spaces"), (P("job", "Description", "Prototype"), "nav.levels|nav.spaces"),
      (P("task", "Description", "Question"), "nav.levels|nav.spaces"), (P("b52", "Description", "Map"), "nav.levels|nav.spaces"),
      ("old.insight", "nav.spaces")]),
    ("views", "2 · View row", "the views of the open Space; in Audience Report a second row under it (Reading or Period)",
     [(P("block", "Description", "Map"), "nav.subs"), (P("block", "Audience Report", "Full/Coverage"), "nav.subs|nth:1:nav.subs"),
      (P("job", "Audience Report", "Full/Current"), "nav.subs|nth:1:nav.subs"), (P("job", "Runs", "All"), "nav.subs"),
      (P("task", "Audience Report", "Table"), "nav.subs"), (P("b52", "Audience Report", "Full/Findings"), "nav.subs|nth:1:nav.subs"),
      ("old.insight", ".parts")]),
    ("report", "3 · Audience Report rows", "one question with its work and its report: Logic │ Work │ Report",
     [(P("block", "Audience Report", "Full/Coverage"), ".q-head-row|nth:0:.q-row:not(.q-head-row)"),
      (P("block", "Audience Report", "Full/Tracks"), ".q-head-row|nth:0:.q-row:not(.q-head-row)"),
      (P("block", "Audience Report", "Full/Consistency"), ".q-head-row|nth:0:.q-row:not(.q-head-row)"),
      (P("block", "Audience Report", "Full/Findings"), ".q-head-row|nth:0:.q-row:not(.q-head-row)"),
      (P("job", "Audience Report", "Full/Current"), ".q-head-row|nth:0:.q-row:not(.q-head-row)"),
      (P("job", "Audience Report", "Full/vs previous"), ".q-head-row|nth:0:.q-row:not(.q-head-row)"),
      (P("job", "Audience Report", "Cross/Current"), ".q-head-row|nth:0:.q-row:not(.q-head-row)"),
      (P("b52", "Audience Report", "Full/Findings"), ".q-head-row|nth:0:.q-row:not(.q-head-row)"),
      (P("b52job", "Audience Report"), ".q-head-row|nth:0:.q-row:not(.q-head-row)"),
      ("old.insight", ".hl-row.on,.hl-row")]),
    # the Space body, one frame per level: every Space and view
    *[(f"space-{lv}", f"4{'abcdef'[i]} · Space body · {name}", "the open Space's box, its first screen, every Space and view",
       [(k, ".space-main") for k in ALL_FRAME if k.startswith(lv + ".")]
       + ([(k, ".pane.on .shell") for k in OLD_PANES] if lv == "block" else [])
       + ([(f"old52.{k}", ".pane.on .shell") for k, _ in OLD_SPACES] if lv == "b52" else []))
      for i, (lv, name, _, _) in enumerate(LEVELS)],
    ("table", "5 · Tables", "rows of items: the frame's light table as each Space fills it",
     [(P("block", "Description", "Partitions"), "table.wf-table"), (P("block", "Work Details", "All"), "table.wf-table"),
      (P("block", "Runs", "All"), "table.wf-table"), (P("block", "Delivery", "Handoff"), "table.wf-table"),
      (P("job", "Description", "Dataset"), "table.wf-table"), (P("job", "Runs", "All"), "table.wf-table"),
      (P("task", "Audience Report", "Table"), "table.wf-table"), (P("task", "Runs", "All"), "table.wf-table"),
      (P("b52", "Runs"), "table.wf-table"), ("old.scope", ".pane.on table"), ("old.check", ".pane.on table")]),
    ("cards", "6 · Rows and cards", "one item, closed or open",
     [(P("block", "Audience Report", "Full/Coverage"), "details.topic"), (P("job", "Description", "Prototype"), "details.topic"),
      (P("job", "Work Details", "All"), "details.topic"), (P("b52", "Idea Studio"), ".space-main details"),
      (P("b52", "Work Details"), "details.topic"), ("old.prototype", ".pane.on details.lvl,.pane.on details"),
      ("old.insight", ".pane.on .card,.pane.on details")]),
    ("runs", "7 · Disk · Runs panel", "the files behind the open Space, its run types and their runs (Disk inside the panel)",
     [(P("block", "Audience Report", "Full/Coverage"), "section.runs-panel"), (P("block", "Description", "Map"), "section.runs-panel"),
      (P("job", "Runs", "All"), "section.runs-panel"), (P("task", "Description", "Question"), "section.runs-panel"),
      (P("b52", "Audience Report", "Full/Findings"), "section.runs-panel"), ("old.insight", ".pane.on .rp,.pane.on .runs-panel")]),
    ("tags", "8 · Tags and pills", "a state, a gate or a count on an item",
     [(P("b52", "Audience Report", "Full/Findings"), "parent:.q-row .chip"),
      (P("block", "Audience Report", "Full/Coverage"), "parent:.q-row .st-warn"),
      (P("job", "Work Details", "All"), "parent:table .st-warn"), ("old.insight", "parent:.pill"), ("old.check", "parent:.pane.on .pill")]),
    ("header", "9 · Page header", "the title line at the top",
     [(P("block", "Description", "Map"), "header"), (P("task", "Description", "Question"), "header"),
      (P("b52", "Description", "Map"), "header"), ("old.insight", "header"), ("old.item", "header"), ("old.run", "header,h1")]),
    ("item", "10 · One item's display", "one question, one run: the item itself",
     [(P("task", "Description", "Question"), ".space-main"), (P("task", "Audience Report", "Reading"), ".space-main"),
      (P("b52task", "Description"), ".space-main"), ("old.item", "main,body"), ("old.run", "main,body")]),
    ("own", "11 · Insight's own elements", "what only the insight theme draws: the two clocks' Map, the cuts and their power, "
     "the Reading and Period rows, the handoff, Check's gates",
     [(P("block", "Description", "Map"), ".space-main table"), (P("block", "Description", "Partitions"), ".space-main"),
      (P("job", "Description", "Dataset"), ".space-main"), (P("block", "Audience Report", "Full/Coverage"), "nth:1:nav.subs"),
      (P("job", "Audience Report", "Full/Current"), "nth:1:nav.subs"), (P("block", "Delivery", "Handoff"), ".space-main"),
      (P("task", "Work Details", "Partitions"), ".space-main"), ("old.check", ".pane.on .shell"), ("old.delivery", ".pane.on .shell")]),
]

# the proposed look per element: (page, selector) shot live from the frame, or "none:"; why; green: what changed
# (or is kept); red: what is open (b03's picks hold: tabs D · E, view row E, the Question cell as the Insight row,
# Disk inside the Runs panel, no tags)
PROPOSALS = {
    "tabs": ((P("block", "Description", "Map"), "nav.levels|nav.spaces"),
             ["the frame's tabs at every level: b03's pick D · E, 16px, 6px corners, grey border, the open one washed blue",
              "the insight theme gives the words only; the level row (Guide · Block · Job ▾ · Task ▾) is the frame's"],
             "took b03's D · E look at Block, Job and Task",
             "? the old Insight board page is still served with &file=board.md (it retires)"),
    "views": ((P("block", "Description", "Map"), "nav.subs"),
              ["one view row, b03's pick E: the tabs' shape, padding 5px 12px, the open one washed blue",
               "the insight theme's second row (Reading: · Period:) is drawn in the same look under the partitions"],
              "took b03's E look; no pills",
              "? Audience Report stacks two view rows (partition, then Reading or Period): one row, or the second as a filter?"),
    "report": (("b03.report", ".q-head-row|nth:0:.q-row:not(.q-head-row)"),
               ["one row per question: Question │ Work │ Report, at Board, Job and Task",
                "the Question cell as the Insight row (b03 s32-D05): Question N and its state dot, the short name, one "
                "sentence of what is asked, › More"],
               "picked: b03's Question cell (the Insight row)",
               "? the insight theme draws its own Logic cell (bold id + the whole question), not frame.question_cell"),
    "space-block": ((P("block", "Audience Report", "Full/Coverage"), ".split"),
                    ["one content box and one right column, Disk · Runs, at every level",
                     "the insight body kept for insight only (b03 s32-D07): partitions as views, levels folded, a row per question"],
                    "kept: the frame's box; insight's body for insight only", ""),
    "space-job": ((P("job", "Audience Report", "Full/Current"), ".split"),
                  ["the same box as the Board: the Job's questions by level, the partitions as views"],
                  "kept: the frame's box", ""),
    "space-task": ((P("task", "Audience Report", "Table"), ".split"),
                   ["the same box: one question, its partitions as rows, its Runs beside"],
                   "kept: the frame's box", ""),
    "space-b52": ((P("b52", "Audience Report", "Full/Findings"), ".split"),
                  ["today's-layout Block: the same box, the old page's content drawn in the frame's look"],
                  "kept: the frame's box",
                  "? carried over to plan C, its Block reads like the Board (b11 Q05)"),
    "space-b52job": ((P("b52job", "Audience Report"), ".split"),
                     ["a Job of today's layout is the base's own (vanilla)"],
                     "kept: the base's Job",
                     "? its Audience Report is vanilla, not the insight rows: the insight theme draws only its Block"),
    "space-b52task": ((P("b52task", "Description"), ".split"),
                      ["a Task of today's layout is the base's own (vanilla)"],
                      "kept: the base's Task",
                      "? the same: the base's own Task, no partitions"),
    "table": ((P("block", "Runs", "All"), "table.wf-table"),
              ["the frame's light table: small grey heads, rows ruled by one line, no boxed cells",
               "a state in a cell is a word (open · partial · answered), not a pill"],
              "kept: the frame's table", ""),
    "cards": ((P("job", "Work Details", "All"), "details.topic"),
              ["one closed row per item: ▸ name · its facts, opened in place (Idea Studio's topic rows)"],
              "kept: the frame's rows", ""),
    "runs": ((P("block", "Audience Report", "Full/Coverage"), "section.runs-panel"),
             ["Disk, then Runs, in one panel with one fold (b03 s32-D08)",
              "one row per run type, named by its Run (run-<type>-<target>); its Runs as rows"],
             "took: Disk inside the Runs panel", ""),
    "tags": (("none:", ""),
             ["none: no tags in any theme (b03 s32-D09)",
              "a state is a word (open · partial · answered) or the question's state dot; a gate is a word in the Work cell"],
             "changed: no tags at all (b03 s32-D09)",
             "? today's-layout Block (b52) still draws Check's gates as chips on each row (insight_theme.py)"),
    "header": ((P("block", "Description", "Map"), "header"),
               ["one line: the theme's icon · its name · the folder; the path on hover; no band"],
               "kept: one line, no band", ""),
    "item": ((P("task", "Description", "Question"), ".space-main"),
             ["one question opens in the frame as its Task (Description › Question); one run in the pop-out from its row",
              "no item page beside the frame: the question page and the run page retire"],
             "proposed: an item opens in the frame (its Task, or the pop-out)",
             "? the old question page (/_board/insight) and run page (/_board/insight-run) are still served"),
    "own": ((P("job", "Description", "Dataset"), ".space-main"),
            ["the theme's own content, drawn with the frame's parts only: the Map, the cuts and their power, the handoff "
             "are frame tables; the Reading and Period rows are view rows"],
            "kept: the content; the frame's tables and rows",
            "? Check's gates (old Check Space) have no place yet: chips on the row are dropped (no tags) (b11 Q03)"),
}

PICK_JS = S.PICK_JS.replace(
    "const one = s => { if (s.startsWith('parent:'))",
    "const one = s => { if (s.startsWith('nth:')) { const m = s.match(/^nth:(\\d+):(.*)$/);"
    " const vis = [...document.querySelectorAll(m[2])].filter(e => { const r = e.getBoundingClientRect();"
    " return r.width > 4 && r.height > 4; }); return vis[+m[1]] || null; }\n"
    "                     if (s.startsWith('parent:'))")


def shoot(base_url: str) -> None:
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(exist_ok=True)
    for old in SHOTS.glob("*.png"):
        old.unlink()
    facts = {}
    wanted = {}                                     # page -> [(shot name, selector)]
    for ekey, _, _, cards in ELEMENTS:
        for page_key, sel in cards:
            wanted.setdefault(page_key, []).append((f"{ekey}__{page_key}", sel))
    for ekey, ((page_key, sel), *_rest) in PROPOSALS.items():
        if page_key != "none:":
            wanted.setdefault(page_key, []).append((f"proposed__{ekey}", sel))
    urls = {k: u for k, _, u in PAGES}
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 1100}, device_scale_factor=1)
        for key, shots in wanted.items():
            resp = page.goto(base_url + urls[key])
            page.wait_for_timeout(900)
            page.evaluate("document.querySelectorAll('.runs-panel.folded,.rp.folded').forEach(p => p.classList.remove('folded'))")
            page.wait_for_timeout(200)
            if not resp or resp.status != 200:
                print(f"{key}: HTTP {resp.status if resp else '?'}, skipped")
                continue
            for name, sel in shots:
                box = None
                for alt in sel.split(","):              # "a,b": the first that is on the page
                    box = page.evaluate(PICK_JS, alt.strip())
                    if box:
                        break
                if not box:
                    print(f"{name}: {sel} not on the page")
                    continue
                clip = {"x": box["x"], "y": box["y"], "width": max(box["w"], 1), "height": min(max(box["h"], 1), S.MAX_H)}
                page.screenshot(path=str(SHOTS / f"{name}.png"), clip=clip, full_page=True)
                facts[name] = {"page": LABEL[key], "url": urls[key], "selector": sel, "cut": box["h"] > S.MAX_H, **box["style"]}
        browser.close()
    (SHOTS / "facts.json").write_text(json.dumps(facts, indent=1, ensure_ascii=False))
    print(f"{len(facts)} shots in {SHOTS.relative_to(HERE.parent)}")


# ── the drawing ────────────────────────────────────────────────────────────────────────────────
CARD_W = 720
FILES = {}
LAST_W = [0]


def picture(path: Path, x: float, y: float, frame_w: float, px: int = 1100) -> float:
    """b03's picture(), with the embedded image cut to `px` wide so the many Space bodies stay light."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > px:
        im = im.resize((px, round(im.height * px / im.width)))
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
    base("rectangle", x - 1, y - 1, w + 2, h + 2, INK, 1, rough=0)
    LAST_W[0] = w
    return h


def old_reason(key: str) -> str:
    """Why a card's page is an old version, read off the code; "" for the frame (the current one)."""
    if key.startswith("old") and (SERVERS / "workbench-insight" / "insight_theme.py").is_file():
        return "OLD · old page: the insight theme draws on the frame now; this page retires"
    return ""


def note(x, y, what):
    """A green change note where the drawing shows the change (canvas.change_note)."""
    L.els.append(canvas.change_note(x, y, what, DATE, L.FRAME[0], size=18))


def cards_of(ekey):
    cards = next(c for k, _, _, c in ELEMENTS if k == ekey)
    return [(k, sel) for k, sel in cards if (SHOTS / f"{ekey}__{k}.png").exists()]


def frame_element(ekey, title, what, x0, y0, facts) -> dict:
    fr = L.open_frame(title)
    text(x0, y0, title, 34)
    versions = cards_of(ekey)
    olds = sum(bool(old_reason(k)) for k, _ in versions)
    text(x0, y0 + 50, f"{what} · {len(versions)} versions today, {olds} on old pages (flagged OLD: they retire)", 18)
    x, y, row_h = x0, y0 + 120, 0
    for i, (k, _) in enumerate(versions):
        if i and i % 3 == 0:
            x, y, row_h = x0, y + row_h + 80, 0
        f = facts.get(f"{ekey}__{k}", {})
        why = old_reason(k)
        if why:
            text(x, y - 26, why, 14, RED)
        letter = chr(65 + i) if i < 26 else "A" + chr(65 + i - 26)
        text(x, y, f"{letter} · {LABEL[k]}", 20)
        h = picture(SHOTS / f"{ekey}__{k}.png", x, y + 40, CARD_W, 900 if ekey.startswith("space") else 1100)
        if why:
            base("rectangle", x - 8, y + 32, LAST_W[0] + 16, h + 16, RED, 1.5, dashed=True, rough=0)
        text(x, y + 52 + h, S.style_line(f) + ("\n(cut at its first screen)" if f.get("cut") else ""), 14, INK, L.MONO)
        row_h = max(row_h, 52 + h + 60)
        x += CARD_W + 80
    if not versions:
        text(x0, y0 + 120, "? no shots yet: run with --shoot", 18, RED)
    L.close_frame(fr)
    return fr


def frame_proposed(ekey, title, x0, y0, facts) -> dict:
    fr = L.open_frame(title + " · proposed")
    text(x0, y0, title + " · proposed", 34)
    (page_key, _), why, changed, open_ = PROPOSALS[ekey]
    text(x0, y0 + 50, "one look for every theme, drawn by the base (servers/workbench); the insight theme gives the words", 18)
    y = y0 + 110
    note(x0, y, changed)
    y += 40
    if open_:
        text(x0, y, open_, 18, RED)
        y += 40
    shot = SHOTS / f"proposed__{ekey}.png"
    if shot.exists():
        text(x0, y, f"from: {LABEL[page_key]}", 16)
        h = picture(shot, x0, y + 30, 1000)
        text(x0, y + 42 + h, S.style_line(facts.get(f"proposed__{ekey}", {})), 14, INK, L.MONO)
        y += h + 100
    elif page_key == "none:":
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


def frame_title(x0, y0, counts) -> dict:
    fr = L.open_frame("s32 · Insight element UI")
    text(x0, y0, "s32 · Insight element UI", 40)
    text(x0, y0 + 60, "every element the insight theme draws today, on the frame (/_board/workbench: Board, Job, Task; every Space "
                      "and view)\nand on its old board and item pages (OLD, red dashed: they retire), one card per version; beside "
                      "each, the proposed unified look\n(b03 s32's picks hold: tabs D · E, view row E, the Question cell as the "
                      "Insight row, Disk inside the Runs panel, no tags)", 20)
    text(x0, y0 + 170, "black: what is drawn today · red: open (? …), OLD pages · green: what changed (✎ …)", 18)
    y = y0 + 220
    for ekey, title, _, _ in ELEMENTS:
        changed, open_ = PROPOSALS[ekey][2], PROPOSALS[ekey][3]
        text(x0, y, f"{title} · {counts.get(ekey, 0)} versions", 18)
        note(x0 + 560, y, changed)
        if open_:
            text(x0 + 1360, y, open_, 16, RED)
        y += 36
    L.close_frame(fr)
    return fr


def draw(out: Path) -> None:
    facts = json.loads((SHOTS / "facts.json").read_text()) if (SHOTS / "facts.json").exists() else {}
    L.els.clear()
    L.FRAME[0] = None
    FILES.clear()
    counts = {ekey: len(cards_of(ekey)) for ekey, *_ in ELEMENTS}
    tf = frame_title(0, 0, counts)
    y = tf["y"] + tf["height"] + 200
    for ekey, title, what, _ in ELEMENTS:
        fr = frame_element(ekey, title, what, 0, y, facts)
        pr = frame_proposed(ekey, title, fr["x"] + fr["width"] + 200, y, facts)
        y = max(fr["y"] + fr["height"], pr["y"] + pr["height"]) + 200
    canvas.write(out, list(L.els), "build_s32_insight_element_ui.py", files=FILES)


if __name__ == "__main__":
    if "--shoot" in sys.argv:
        url = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "http://127.0.0.1:5851"
        shoot(url.rstrip("/"))
    draw(HERE / "s32-insight-element-ui.excalidraw")
