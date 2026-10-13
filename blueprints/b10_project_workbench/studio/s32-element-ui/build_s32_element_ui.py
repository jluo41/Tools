"""s32 · Element UI: s32-element-ui.excalidraw, a gallery of every kind of workbench element as the base and
each theme draw it today, side by side, to pick one look per element (JL 261007: "collect all types of the UI
of different types of the element ... so we can unify them"; "for each type of the element, show the
different versions, like the gallery, and we will pick and select").

Reshot 261012 (JL: "please read s32, it is old enough, right? DO we want to update it again?"): every theme
draws on the shared frame now, so the versions are the base and each theme on the frame, one real Block or
Job of each, each from the host serving its own SPACE. Only what is still used is kept (s32-D24): no card for
an older theme page, no history/ (git keeps the 261010 shots and the 261011 builder, commit d09005f7).

Two steps:

    uv run --with playwright --with pillow python build_s32_element_ui.py --shoot [--host <SPACE>=<url> ...]
        opens each page in headless Chrome on the host serving its SPACE (HOSTS, or --host), screenshots each
        element into shots/<element>__<page>.png, and writes its computed style into shots/facts.json (font
        size, corner radius, padding, border and fill of its first button or cell). Rerun after a look changes.
    python build_s32_element_ui.py
        draws the gallery from shots/: one frame per element kind, one card per version (the theme, its
        folder, its picture, its style line), the base's own beside it as the proposal. Marks are kept on
        rebuild (canvas.write).
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
TOOLS = HERE.parents[3]                                   # the Tools repo
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE.parent / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers)
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas
import canvas  # noqa: E402

INK, GRAY, RED, TEAL = L.INK, L.GRAY, L.RED, L.TEAL
GREEN = "#2f9e44"
text, base = L.text, L.base


def q(path: str) -> str:
    return U.quote(path, safe="")


# the host serving each SPACE on this computer (override: --host <SPACE>=<url>); "Tools-SPACE" is this repo
HOSTS = {"Tools-SPACE": "http://127.0.0.1:5623", "WellDoc-SPACE": "http://127.0.0.1:5622",
         "DrFirst-SPACE": "http://127.0.0.1:5604", "Physician-SPACE": "http://127.0.0.1:5599"}
# (key, label, its SPACE, its folder there): the base and every theme on the frame, one real Block or Job each
FRAMES = [
    ("base", "base · b10_project_workbench", "Tools-SPACE", "blueprints/b10_project_workbench"),
    ("work", "work · b02_pretrain_corpus", "WellDoc-SPACE", "examples-2-lm/Proj11-CGM-Corpus/work/b02_pretrain_corpus"),
    ("cowork", "cowork · Samsung b12_epic_streaming", "WellDoc-SPACE",
     "examples-0-cowork/Project-Samsung/cowork/b12_epic_streaming"),
    ("paper", "paper · Paper-ScalingGlucose-NatSeries2026", "WellDoc-SPACE",
     "examples-2-nn/Proj11-CGM-FM/paper/Paper-ScalingGlucose-NatSeries2026"),
    ("insight", "insight · Insight-SMSR2v1, its Job j01", "DrFirst-SPACE",
     "examples-5-design/Project-Application-SMSDesign/insight/Insight-SMSR2v1/"
     "j01_prototype-p1-basic-questions_data-SMSR2v1"),
    ("design", "design · Design-SMSR2-Stage25-CarryOver-261008", "DrFirst-SPACE",
     "examples-5-design/Project-Application-SMSDesign/design/Design-SMSR2-Stage25-CarryOver-261008"),
    ("discovery", "discovery · b01_experimental_learning_evidence", "DrFirst-SPACE",
     "examples-4-learning/Project-ExpLearn-SMSDesign/discovery/b01_experimental_learning_evidence"),
    ("labeling", "labeling · b01_aci_bench", "Physician-SPACE",
     "examples-labeling/Project-Labeling-ClinicalDialogue/labeling/b01_aci_bench"),
]
PAGES = [(k, label) for k, label, *_ in FRAMES] + [("design-job", "design · a ladder Job (the tests' sample)")]
# (key, title, what it is, the frame's Space and mode, its selector on the frame).
# A selector "a|b" is the box around both; "a,b" the first that is on the page; "parent:x" is x's parent.
ELEMENTS = [
    ("top", "1 · Top of the page", "the level row (Studio | Block · Job · Task | Delivery), the title, the Spaces row "
     "and the view row", ("Audience Report", ""), "nav.levels|header.page-title|nav.spaces|nav.subs"),
    ("report", "2 · Report", "the Report Space: its groups and one card or row per Question",
     ("Audience Report", ""), ".space-main"),
    ("studio", "3 · Studio", "the Block's topics under their group bar, Related folded inside (s02, s04)",
     ("Audience Report", "studio"), ".space-main"),
    ("delivery", "4 · Delivery", "what the Block hands over: its parts by source, then its results (s03)",
     ("Delivery", ""), ".space-main"),
    ("description", "5 · Description", "the face: what this Block, Job or Task is", ("Description", ""), ".space-main"),
    ("work", "6 · Work", "the Jobs, Tasks and their Runs under this level", ("Work Details", ""), ".space-main"),
    ("runs", "7 · Disk · Runs panel", "the files behind the open Space, its run types and their runs, opened",
     ("Audience Report", ""), "section.runs-panel"),
    ("design", "8 · Design display", "a design Job's design items: its Report › Design display (b12)",
     None, ".space-main"),
]
DRAWN = [(k, t, w, (k,)) for k, t, w, *_ in ELEMENTS]


# the proposal per element: the base's own picture, the look every theme takes (the frame draws it), and why
PROPOSALS = {
    "top": ["built: the level row is the page index, Studio and Delivery at its two ends (s02-D18, s03-D04)",
            "the title larger, with a wide gap; the Spaces row Description · Report · Work · Runs; the view row",
            "a Job or Task in its dropdown by its folder name, as it is on disk (s32-D15)"],
    "report": ["built on the base: one card per Question under the Studio's group bar (s05-D05, D13)",
               "opened, two columns: Logic │ Report, the work a line inside the Report (s32-D23)",
               "proposed for every theme: its starting groups, a lens stays a row above (s05-D07, D09)",
               "insight: a Topic row across D · I · K · W, the levels stay its folds (JL 261012)"],
    "studio": ["one bar for Studio, Related and Report: Current · groups · Untagged · + Group (s02-D16, s05-D05)",
               "one closed row per topic, opened in place (s32-D06); its other drawings get no link on the row (s32-D17)"],
    "delivery": ["built: one card per result under the group bar, as the Studio's (s32-D18); its file kinds are "
                 "fixed groups, + Group adds your own (delivery/result_groups.md)",
                 "the source row (Block · jNN · tNN) stays above, the part picked (s03-D06)",
                 "built for every theme: paper's, cowork's, insight's and design's own parts stay below the cards "
                 "(s32-D22)",
                 "proposed: Sends from delivery.md above the cards; the state of each (s03-D07, D08)"],
    "description": ["each theme fills the face's fields; the box and the Runs panel are the base's"],
    "work": ["built: Job → Task → Run → what it found, one tree; each Run's headline and its result/ files (s32-D19)",
             "a Task a person works in carries its button: ✎ Write (a Page's Draft), 🏷 Label (labeling's rounds)",
             "built for paper, cowork and discovery too (s32-D22); a theme adds its words to a card (work_meta)",
             "design and insight keep their own Job cards and Task tree (b12's and b11's rulings)"],
    "runs": ["Disk, then Runs, in one panel with one fold; one row per run type, named by its Run",
             "a type's Runs as rows; a card opens only when its row is clicked"],
    "design": ["one row per design: the design │ its process (③) │ its review (④ ⑤); the dropped folded (b12)"],
}
# a short green note where a change was made (JL 261007), and a red one where something is still open
CHANGED = {"top": "built: Studio | Block · Job · Task | Delivery; folder names as on disk",
           "work": "built: Job → Task → Run → result, one tree, on base, work, cowork, paper, discovery (s32-D19, D22)",
           "studio": "built: one group bar; Related inside; no extra drawing links (s32-D17)",
           "delivery": "built: result cards under the group bar, on every theme (s32-D18, D22)",
           "runs": "kept: Disk in Runs, one fold", "design": "built: Job › Report › Design display (b12)"}
# the proposal's picture from a Block of the base's own look that has something to show, where b10 has none:
# (SPACE, folder, JS run before the shot)
PROPOSAL_FROM = {
    "delivery": ("Tools-SPACE", "blueprints/b12_theme_design", ""),
    "work": ("WellDoc-SPACE", "examples-2-lm/Proj11-CGM-Corpus/work/b02_pretrain_corpus",
             "const j = document.querySelector('.work-job'); if (j) { j.open = true;"
             " j.querySelectorAll('.work-task').forEach(t => t.open = true); }"),
}
# what a card shows when it is opened, drawn beside the proposal (JL 261012, on 2 · Report · proposed: "what we
# will have when we open it?"): (SPACE, folder, the card's selector, caption)
OPENED = {
    "report": ("Tools-SPACE", "blueprints/b10_project_workbench", "#question-Q05",
               "opened: Q05, the one with work on it. Two columns, Logic │ Report (s32-D23): the Question and where "
               "it comes from in the Studio; the report's answer, the work behind it, its drawing and its state"),
}
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


def space_python():
    """A Python with the workbench's own packages: the .venv of a SPACE beside this Tools repo."""
    for name in HOSTS:
        py = TOOLS.parent / name / ".venv" / "bin" / "python"
        if py.is_file():
            return py
    return Path(sys.executable)


def render_demos() -> dict:
    """{name: file URL} of the sample pages no Project holds yet, rendered by a SPACE's own Python."""
    import subprocess
    out = SHOTS / "demo-design-job.html"
    done = subprocess.run([str(space_python()), "-c", DEMO_PY, str(SERVERS), str(out)], capture_output=True, text=True)
    if done.returncode or not out.exists():
        print("design-job sample:", (done.stderr or "").strip().splitlines()[-1:] or "failed")
        return {}
    return {"design-job": out.resolve().as_uri()}


def frame_url(folder: str, space: str, mode: str) -> str:
    return (f"/_board/workbench?path={q(folder)}&space={U.quote_plus(space)}"
            + ("&studio=1" if mode == "studio" else ""))


def snap(page, sel, out, facts, key, label, url):
    """Screenshot the first match of `sel` ("a,b": the first that is on the page) into `out`; record its style."""
    box = None
    for alt in sel.split(","):
        box = page.evaluate(PICK_JS, alt.strip())
        if box:
            break
    if not box:
        return False
    page.screenshot(path=str(out), full_page=True,
                    clip={"x": box["x"], "y": box["y"], "width": max(box["w"], 1), "height": min(max(box["h"], 1), MAX_H)})
    facts[out.stem] = {"page": label, "url": url, "selector": sel, "cut": box["h"] > MAX_H, **box["style"]}
    return True


def goto(page, url):
    """Open `url`; a host that restarts mid-shoot gets one more try after a pause, then the page is skipped (0)."""
    resp = None
    for wait in (0, 8000):
        page.wait_for_timeout(wait)
        try:
            resp = page.goto(url)
            break
        except Exception as e:                                  # refused while its host restarts
            print("  retry:", str(e).splitlines()[0][:100])
    if resp is None:
        return 0
    page.wait_for_timeout(900)
    # a Runs panel starts folded on some pages: open it, so every version shows its contents
    page.evaluate("document.querySelectorAll('.runs-panel.folded').forEach(p => p.classList.remove('folded'))")
    page.wait_for_timeout(200)
    return resp.status if resp else 0


def shoot(hosts: dict) -> None:
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(exist_ok=True)
    for old in SHOTS.glob("*.png"):
        old.unlink()
    facts = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 1100}, device_scale_factor=1)
        for key, label, space, folder in FRAMES:                       # the base and every theme on the frame
            host = hosts.get(space)
            if not host:
                print(f"{key}: no host for {space}, skipped")
                continue
            for ekey, _, _, where, sel in ELEMENTS:
                if where is None:
                    continue
                url = frame_url(folder, *where)
                status = goto(page, host + url)
                if status != 200:
                    print(f"{key} {ekey}: HTTP {status}, skipped")
                    continue
                if not snap(page, sel, SHOTS / f"{ekey}__{key}.png", facts, key, label, url):
                    print(f"{key} {ekey}: {sel} not on the page")
                elif ekey == "report":                                 # read live: the Report's group bar
                    facts[f"{ekey}__{key}"]["bar"] = page.evaluate("!!document.querySelector('[data-group-kind=reports]')")
        for ekey, (space, folder, js) in PROPOSAL_FROM.items():         # the proposals that need content
            where = next(e[3] for e in ELEMENTS if e[0] == ekey)
            url = frame_url(folder, *where)
            if hosts.get(space) and goto(page, hosts[space] + url) == 200:
                if js:
                    page.evaluate(js)
                    page.wait_for_timeout(300)
                snap(page, ".space-main", SHOTS / f"{ekey}__proposal.png", facts, "proposal", folder, url)
        for ekey, (space, folder, sel, _) in OPENED.items():           # a card opened, as a person opens it
            where = next(e[3] for e in ELEMENTS if e[0] == ekey)
            url = frame_url(folder, *where)
            if hosts.get(space) and goto(page, hosts[space] + url) == 200:
                page.evaluate("s => { const e = document.querySelector(s); const d = e && e.closest('details');"
                              " if (d) d.open = true; }", sel)
                page.wait_for_timeout(1200)
                card = page.evaluate("s => { const e = document.querySelector(s); const d = e && e.closest('details');"
                                     " if (d) d.setAttribute('data-shot', '1'); return !!d; }", sel)
                if card:
                    snap(page, "[data-shot]", SHOTS / f"{ekey}__opened.png", facts, "opened", folder, url)
        demos = render_demos()                                         # a design Job: the tests' sample Block
        if "design-job" in demos:
            page.goto(demos["design-job"])
            page.wait_for_timeout(500)
            snap(page, ".space-main", SHOTS / "design__design-job.png", facts, "design-job", "design-job", "demo")
        browser.close()
    (SHOTS / "facts.json").write_text(json.dumps(facts, indent=1, ensure_ascii=False))
    print(f"{len(facts)} shots in {SHOTS.relative_to(HERE.parent)}")


# ── the drawing ────────────────────────────────────────────────────────────────────────────────
CARD_W, PIC_H, PER_ROW = 470, 380, 4   # a card's picture at most this wide and tall (never above 1:1), 4 a row,
                                       # so the 8 versions fill one screen-sized frame (canvas.FRAME_MAX)
FILES = {}


def picture(path: Path, x: float, y: float, frame_w: float, max_h: float = 10 ** 6) -> float:
    """An image element for one screenshot at (x, y), at most `frame_w` wide and `max_h` tall; returns its height."""
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
    w = min(frame_w, im.width, im.width * max_h / im.height)
    h = im.height * w / im.width
    L.els.append({"id": f"img-{fid}-{round(x)}-{round(y)}", "type": "image", "x": x, "y": y, "width": w, "height": h, "angle": 0,
                  "strokeColor": "transparent", "backgroundColor": "transparent", "fillStyle": "solid",
                  "strokeWidth": 1, "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [],
                  "frameId": L.FRAME[0], "roundness": None, "seed": 1, "version": 1, "versionNonce": 1,
                  "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False,
                  "status": "saved", "fileId": fid, "scale": [1, 1]})
    base("rectangle", x - 1, y - 1, w + 2, h + 2, GRAY, 1, rough=0)
    return h


def style_line(f: dict) -> str:
    """The first control's computed style, in short lines that fit under a card."""
    return (f"{f.get('tag', '')}\nfont {f.get('font', '')} · radius {f.get('radius', '')}\n"
            f"padding {f.get('padding', '')}\nborder {f.get('border', '')}\nfill {f.get('fill', '')}")


def frame_element(ekey, title, what, x0, y0, facts, parts=None) -> dict:
    parts = parts or (ekey,)
    fr = L.open_frame(title)
    text(x0, y0, title, 34)
    versions = [(k, label) for k, label in PAGES if any((SHOTS / f"{p}__{k}.png").exists() for p in parts)]
    text(x0, y0 + 50, f"{what}\n{len(versions)} versions today: the base and each theme on the frame"
                      "; mark the one to keep, or draw your own beside them", 20)
    if ekey == "report":                         # which themes' Reports have the group bar, read on the shoot
        has = [k for k, _ in versions if facts.get(f"report__{k}", {}).get("bar")]
        lacks = [k for k, _ in versions if k not in has]
        CHANGED["report"] = (f"? the group bar on {len(has)} of {len(has) + len(lacks)}: " + ", ".join(has)
                             + "; not yet: " + ", ".join(lacks) + " (s05)") if lacks else "built: the group bar on every theme"
    if ekey in CHANGED:
        open_ = CHANGED[ekey].startswith("?")
        text(x0, y0 + 108, ("" if open_ else "✎ 261012 ") + CHANGED[ekey], 20, RED if open_ else GREEN)
    x, y, row_h = x0, y0 + 240, 0
    for i, (k, label) in enumerate(versions):
        if i and i % PER_ROW == 0:
            x, y, row_h = x0, y + row_h + 20, 0
        text(x, y - 26, f"{chr(65 + i)} · " + label.replace(" · ", "\n", 1), 22, INK)   # the theme, then its folder
        h, keys = 0, [p for p in parts if (SHOTS / f"{p}__{k}.png").exists()]
        for n, part in enumerate(keys):
            h += picture(SHOTS / f"{part}__{k}.png", x, y + 40 + h, CARD_W, PIC_H) + (12 if n < len(keys) - 1 else 0)
        f = facts.get(f"{keys[0]}__{k}", {})
        text(x, y + 52 + h, style_line(f) + ("\n(cut at its first screen)" if f.get("cut") else ""), 20, INK, L.MONO)
        row_h = max(row_h, 52 + h + (170 if f.get('cut') else 140))
        x += CARD_W + 60
    if not versions:
        text(x0, y0 + 150, "? no shots yet: run with --shoot", 22, RED)
    L.close_frame(fr)
    return fr


def frame_proposed(ekey, title, x0, y0, facts) -> dict:
    """The proposed look of one element, beside its gallery: the base's own picture (the frame draws it for every
    theme), its numbers, and why."""
    fr = L.open_frame(title + " · proposed")
    text(x0, y0, title + " · proposed", 34)
    text(x0, y0 + 50, "one look for every theme, drawn by the base (servers/workbench/frame.py); a theme gives "
                      "the words only", 20)
    shot = next((SHOTS / f"{ekey}__{k}.png" for k in ("proposal", "base", "design-job")
                 if (SHOTS / f"{ekey}__{k}.png").exists()), None)
    y = y0 + 110
    if shot:
        h = picture(shot, x0, y, 1000)
        text(x0, y + h + 12, style_line(facts.get(shot.stem, {})), 20, INK, L.MONO)
        y += h + 160
    else:
        text(x0, y, "? no shot yet: run with --shoot", 22, RED)
        y += 50
    opened = SHOTS / f"{ekey}__opened.png"
    if ekey in OPENED and opened.exists():                       # beside it: one card opened
        e, _ = canvas.tree_text(x0 + 1060, y0 + 110, OPENED[ekey][3], 20, 1150, fr["id"], GREEN)
        L.els.append(e)
        picture(opened, x0 + 1060, y0 + 110 + e["height"] + 14, 1150)
    text(x0, y + 10, "why", 24)
    for i, line in enumerate(PROPOSALS[ekey]):
        text(x0 + 20, y + 52 + i * 32, "· " + line, 20, RED if line.startswith(("proposed", "?")) else INK)
    L.close_frame(fr)
    return fr


def draw(out: Path) -> None:
    facts = json.loads((SHOTS / "facts.json").read_text()) if (SHOTS / "facts.json").exists() else {}
    L.els.clear()
    L.FRAME[0] = None
    FILES.clear()
    y = 0
    frames = []
    for ekey, title, what, parts in DRAWN:
        fr = frame_element(ekey, title, what, 0, y, facts, parts)
        frames.append(fr)
        pr = frame_proposed(ekey, title, fr["x"] + fr["width"] + 200, y, facts) if ekey in PROPOSALS else fr
        y = max(fr["y"] + fr["height"], pr["y"] + pr["height"]) + 200
    canvas.write(out, list(L.els), "build_s32_element_ui.py", files=FILES)


if __name__ == "__main__":
    if "--shoot" in sys.argv:
        hosts = dict(HOSTS)
        for i, arg in enumerate(sys.argv):                     # --host <SPACE>=<url>
            if arg == "--host" and i + 1 < len(sys.argv) and "=" in sys.argv[i + 1]:
                name, url = sys.argv[i + 1].split("=", 1)
                hosts[name] = url
        shoot({k: v.rstrip("/") for k, v in hosts.items()})
    draw(next((Path(a) for a in sys.argv[1:] if a.endswith(".excalidraw")), HERE / "s32-element-ui.excalidraw"))
