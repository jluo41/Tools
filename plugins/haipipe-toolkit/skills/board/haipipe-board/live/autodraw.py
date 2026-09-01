"""✨ Auto-draw: Claude authors a page's Excalidraw scene on demand.

JL 260815: "what I want is like a button, and it can generate what we want."
The button lives in the shell's Draw tab; this is the endpoint behind it.
POST /_board/autodraw {scene: <root-relative .excalidraw>, prompt: <optional ask>}

THE PEN IS CLAUDE, THE METADATA IS OURS. The model returns only an `elements`
array; everything the engine relies on (the haipipe key, the page address, the
autodraw stamp) is written here, so a creative answer can never corrupt the
scene's identity.

THE OWNERSHIP LAW (QPf2): a scene that has elements and no `autodraw` stamp was
drawn by a person, and auto-draw REFUSES to overwrite it. Regenerating over its
own previous output is fine — that is what the stamp is for.

Group scenes are composed, never authored, so `group.excalidraw` is refused:
draw the pages and the group view assembles itself.
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cli.draw import read_scene  # noqa: E402  (the same validator every writer uses)

TIMEOUT = 300          # claude -p can think for minutes on a dense page
MAX_MD = 12000         # enough for Opening + Diagram + Content on any page here

PROMPT = """You are generating the ELEMENTS of an Excalidraw scene for one page \
of a design board. Output ONLY a JSON object {{"elements": [...]}} — no prose, no \
markdown fences.

PAGE ID: {pid}
{ask_line}

THE PAGE (markdown):
---
{md}
---

Rules for the drawing:
- If the page has a `## Diagram` ascii figure and no other ask, draw THAT figure \
faithfully: same boxes, same arrows, same labels (emoji included).
{ascii_line}
- Layout left-to-right / top-down, total span roughly 900x600 starting near (0,{y0}).
- Every box is a rectangle with a BOUND text label; every arrow BINDS its two ends.
- Palette: stroke #1e1e1e; backgroundColor "transparent" on every shape \
(JL 260816: boxes stay unfilled); a shape that must stand out may use a colored \
STROKE from #e8590c #2f9e44 #1971c2 #9c36b5 instead of a fill; \
notes in #666666. fontFamily 8 on EVERY text element (Comic Shanns Mono, JL 260815). Keep it under 40 elements.

Element contract (follow exactly; ids are yours to invent, keep them short):
- rectangle: {{"id","type":"rectangle","x","y","width","height","angle":0,\
"strokeColor","backgroundColor","fillStyle":"solid","strokeWidth":2,\
"strokeStyle":"solid","roughness":1,"opacity":100,"groupIds":[],"frameId":null,\
"roundness":{{"type":3}},"seed":<int>,"version":1,"versionNonce":<int>,\
"isDeleted":false,"boundElements":[{{"id":"<textId>","type":"text"}}],\
"updated":1,"link":null,"locked":false}}
- bound label: {{"id","type":"text","x","y","width","height",...same base...,\
"roundness":null,"boundElements":[],"text","originalText","fontSize":16,\
"fontFamily":8,"textAlign":"center","verticalAlign":"middle",\
"containerId":"<rectId>","autoResize":true,"lineHeight":1.25}}
- arrow: {{"id","type":"arrow","x","y","width","height",...same base...,\
"roundness":{{"type":2}},"boundElements":[],"points":[[0,0],[dx,dy]],\
"lastCommittedPoint":null,"startBinding":{{"elementId":"<idA>","focus":0,\
"gap":8}},"endBinding":{{"elementId":"<idB>","focus":0,"gap":8}},\
"startArrowhead":null,"endArrowhead":"arrow","elbowed":false}}
  and BOTH bound elements list the arrow in their boundElements: \
{{"id":"<arrowId>","type":"arrow"}}.
- free note text: same as label but containerId null, textAlign "left".
"""


def _fail(msg):
    return {"ok": False, "err": msg}


def ascii_figure(md):
    """The page's `## Diagram` fenced figure, verbatim, or ''."""
    m = re.search(r"^## Diagram\b.*?^```[a-z]*\n(.*?)^```", md,
                  flags=re.S | re.M)
    return m.group(1).rstrip("\n") if m else ""


def ascii_element(fig):
    """The figure as ONE monospace text element at the top of the scene.

    Placed by the SERVER, never retyped by the model (JL 260816: "copy the
    diagram's ascii to the draw as well, and then draw its own version") —
    ascii art round-tripped through a generation comes back subtly bent,
    and Comic Shanns Mono renders the verbatim copy true. Returns
    (element, y_where_the_drawing_starts)."""
    lines = fig.split("\n")
    size = 14                                   # px; wide figures still fit
    w = int(max(len(x) for x in lines) * size * 0.6) + 8
    h = int(len(lines) * size * 1.25) + 8
    el = {"id": "ascii-figure", "type": "text", "x": 0, "y": 0,
          "width": w, "height": h, "angle": 0,
          "strokeColor": "#666666", "backgroundColor": "transparent",
          "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
          "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
          "roundness": None, "seed": 261608, "version": 1,
          "versionNonce": 261608, "isDeleted": False, "boundElements": [],
          "updated": 1, "link": None, "locked": False,
          "text": fig, "originalText": fig, "fontSize": size,
          "fontFamily": 8, "textAlign": "left", "verticalAlign": "top",
          "containerId": None, "autoResize": False, "lineHeight": 1.25}
    return el, h + 100


def autodraw(root, payload):
    root = Path(root).resolve()
    rel = (payload.get("scene") or "").strip().lstrip("/")
    ask = (payload.get("prompt") or "").strip()
    if not rel:
        return _fail("no scene named")
    f = (root / rel).resolve()
    if root not in f.parents:
        return _fail("scene escapes the served root")
    if f.suffix != ".excalidraw" or f.parent.name != "draw":
        return _fail("auto-draw only writes <owner>/draw/*.excalidraw")
    if f.name == "group.excalidraw":
        return _fail("the group view is COMPOSED, never authored — "
                     "draw the pages and it assembles itself")
    # Labeling HOLD owns every model run/write door, not only the GUI SDK
    # composer. Bind the scene back to its exact Board Page and derive the
    # guard from canonical receipts before Claude starts or a tmp file exists.
    from .labeling import labeling_hold_for_scene
    held, reason = labeling_hold_for_scene(root, rel)
    if held:
        return _fail(reason + " · Draw generation is read-only at this gate")

    scene = None
    if f.is_file():
        try:
            scene = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            return _fail(f"existing scene is unreadable: {e}")
        if scene.get("elements") and not scene.get("haipipe", {}).get("autodraw"):
            return _fail("this scene is hand-drawn — auto-draw refuses to "
                         "overwrite a person's work")

    page_dir = f.parent.parent
    md_path = page_dir / f"{page_dir.name}.md"
    md = md_path.read_text(encoding="utf-8")[:MAX_MD] if md_path.is_file() else ""
    pid = f.stem
    ask_line = f"THE ASK: {ask}" if ask else \
        "THE ASK: draw this page's ## Diagram figure (or, if none, its core idea)."
    fig = ascii_figure(md)
    fig_el, y0 = (None, 0)
    ascii_line = "- (this page carries no ascii figure)"
    if fig:
        fig_el, y0 = ascii_element(fig)
        ascii_line = (f"- The ascii original is ALREADY placed on the canvas "
                      f"above y={y0}; do not retype it. Draw your version "
                      f"BELOW it, starting at y={y0}.")
    prompt = PROMPT.format(pid=pid, ask_line=ask_line, ascii_line=ascii_line,
                           y0=y0, md=md or "(no markdown found)")

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    try:
        run = subprocess.run(["claude", "-p", prompt, "--output-format", "text"],
                             capture_output=True, text=True, timeout=TIMEOUT,
                             cwd=root, env=env)
    except FileNotFoundError:
        return _fail("the `claude` CLI is not on this machine's PATH")
    except subprocess.TimeoutExpired:
        return _fail(f"Claude took longer than {TIMEOUT}s — try again")
    if run.returncode != 0:
        return _fail(f"claude -p failed: {(run.stderr or run.stdout)[:300]}")

    text = run.stdout.strip()
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        return _fail("Claude returned no JSON")
    try:
        out = json.loads(m.group(0))
    except Exception as e:
        return _fail(f"Claude's JSON does not parse: {e}")
    elements = out.get("elements")
    if not isinstance(elements, list) or not elements:
        return _fail("Claude returned no elements")
    for el in elements:
        if not (isinstance(el, dict) and el.get("id") and el.get("type")
                and isinstance(el.get("x"), (int, float))
                and isinstance(el.get("y"), (int, float))):
            return _fail("an element is missing id/type/x/y — not written")

    base = scene or {"type": "excalidraw", "version": 2,
                     "source": "haipipe-board/autodraw",
                     "appState": {"gridSize": None,
                                  "viewBackgroundColor": "#ffffff"},
                     "files": {}}
    hp = base.setdefault("haipipe", {})
    hp.setdefault("schema", "haipipe-linked-drawing/v1")
    hp.setdefault("kind", "page")
    hp.setdefault("page", {"id": pid,
                           "markdown": str(md_path.relative_to(root))
                           if md_path.is_file() else ""})
    hp["autodraw"] = {"by": "claude", "at": dt.datetime.now().strftime("%y%m%d %H%M"),
                      "prompt": ask or "## Diagram"}
    if fig_el:
        elements = [e for e in elements if e.get("id") != "ascii-figure"]
        elements.insert(0, fig_el)
    base["elements"] = elements

    tmp = f.with_suffix(".excalidraw.tmp")
    tmp.write_text(json.dumps(base, indent=1), encoding="utf-8")
    try:
        read_scene(tmp)                       # the house validator gets a veto
    except Exception as e:
        tmp.unlink(missing_ok=True)
        return _fail(f"generated scene failed validation: {e}")
    tmp.replace(f)
    return {"ok": True, "elements": len(elements), "scene": rel}
