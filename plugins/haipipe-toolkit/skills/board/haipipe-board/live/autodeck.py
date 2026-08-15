"""✨ Auto-deck: Claude authors a page's slide deck on demand.

JL 260815: "Could you add a new button to it so we can regenerate the slide?"
The button lives in the shell's Slides tab and the page's 🎞 panel; this is the
endpoint behind both, the slide plugin's twin of autodraw.
POST /_board/autodeck {file: <root-relative page .md>, prompt: <optional ask>}

THE DECK IS THE AI DECK (QPf3, JL 260815), so regeneration always overwrites:
there is no hand-drawn deck to protect the way autodraw protects a hand-drawn
scene. A person's lasting corrections belong on the PAGE, which is what every
regeneration reads; edits made directly to the deck file are one regeneration
away from gone, and that is the contract, not an accident.

THE HEAD IS OURS, THE SLIDES ARE CLAUDE'S. The asset links must climb from the
page's slide/ folder to the html-ppt skill, and a wrong hop renders the deck as
bare text (measured twice on 260815: the QA00 Tools/-rooted constant, then the
display/skills -> display move). So the exact <head>, with the prefix computed
HERE from real paths, is handed to the model as a block it must reproduce; the
model's editorial freedom starts at <body>.
"""
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

TIMEOUT = 600          # a deck is authored, not reflowed; minutes are normal
MAX_MD = 14000         # Opening + Diagram + Content + Aims on any page here

HEAD = """<!DOCTYPE html>
<html lang="en" data-theme="academic-report">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{a}/fonts.css">
<link rel="stylesheet" href="{a}/base.css">
<link rel="stylesheet" id="theme-link" href="{a}/themes/academic-report.css">
<link rel="stylesheet" href="{a}/academic-report-extras.css">
<link rel="stylesheet" href="{a}/animations/animations.css">
<script>document.documentElement.setAttribute('data-js','1')</script>
<style>
/* No-JS fallback, ONLY when scripts are blocked (the stamp above never ran):
   the URL fragment picks the slide and the stacked deck flattens to one
   visible slide. With the runtime alive this block is inert — is-active owns
   the stage, and a display:none here would freeze the deck on slide 1. */
html:not([data-js]) .slide {{ display: none; position: relative;
  opacity: 1; transform: none; pointer-events: auto; }}
html:not([data-js]) .slide:target {{ display: flex; }}
html:not([data-js]) .slide:first-of-type {{ display: flex; }}
html:not([data-js]) .slide:target ~ .slide:first-of-type {{ display: none; }}
</style>
</head>"""

PROMPT = """You are authoring a complete HTML slide deck for ONE page of a \
design board. Output ONLY the full HTML document, starting with <!DOCTYPE html> \
and ending with </html>. No prose before or after, no markdown fences.

PAGE ID: {pid}
{ask_line}

THE PAGE (markdown):
---
{md}
---

THE CONTRACT, exactly:
- Begin with THIS head, byte for byte (choose a short, specific <title>):
{head}
- Then <body><div class="deck"> holding 6 to 9 <section class="slide"> blocks,
  then </div>, then <script src="{a}/runtime.js"></script>, then </body></html>.
- Every section: id="sN", data-title="<short word>". Slide 1 is a COVER
  (p.kicker, h1.h1 with a <span class="gradient-text"> phrase, p.lede, and a
  deck-footer); the last slide is a CLOSER of the same shape. Middle slides:
  p.kicker, h2.h2 headline, then ONE of: a <div class="grid g2"> or "grid g3"
  of <div class="card"><h4>…</h4><p class="dim">…</p></div>, a <pre> figure,
  or a <ul> of short <li>. Optionally one <p class="dim mt-m"> afterthought.
- Cover and closer each carry:
  <div class="deck-footer"><span class="dim2">{pid} · AI-generated deck, \
{stamp}</span><span class="slide-number" data-current="N" data-total="TOTAL">\
</span></div> with the real N and TOTAL.
- EVERY slide ends with a <div class="notes">…</div>: 2-3 sentences of speaker
  guidance, said in a voice, not a caption.
- DISTILL, never copy: the page's paragraphs become three-word card titles and
  one-line card bodies; keep the page's own emoji and its exact numbers, ids
  and quoted rulings. Never invent a fact the page does not state.
- Escape < and > as &lt; &gt; inside visible text. Keep any ascii-figure <pre>
  under 70 columns, and align its columns on what RENDERS, never on the
  source: &lt; paints as ONE character. Inside a figure, avoid the problem
  instead of solving it: write ⟨page⟩ with ⟨ ⟩ (no entity, one column each),
  and keep emoji OUT of box interiors — set them before or after the border
  glyphs, because their width is not one column and every border after them
  drifts. A figure whose right borders do not line up is worse than no figure.
"""


def _fail(msg):
    return {"ok": False, "err": msg}


def autodeck(root, payload):
    root = Path(root).resolve()
    rel = (payload.get("file") or "").strip().lstrip("/")
    ask = (payload.get("prompt") or "").strip()
    if not rel:
        return _fail("no page named")
    md_path = (root / rel).resolve()
    if root not in md_path.parents:
        return _fail("page escapes the served root")
    if md_path.suffix != ".md" or md_path.parent.name != md_path.stem:
        return _fail("auto-deck only writes for a folded page "
                     "(<name>/<name>.md owns the slide/ plugin)")
    if not md_path.is_file():
        return _fail(f"{rel} does not exist")

    slide_dir = md_path.parent / "slide"
    out = slide_dir / f"{md_path.stem}-deck.html"

    # The skill beside THIS engine, the resolution deck.py settled on 260815:
    # live/ -> haipipe-board -> board -> skills, then the display plugin.
    skill = Path(__file__).resolve().parents[3] / "display" / "html-ppt"
    if not (skill / "assets").is_dir():
        return _fail(f"html-ppt assets not found at {skill}")
    assets = os.path.relpath(skill / "assets", slide_dir.resolve()).replace(os.sep, "/")

    md = md_path.read_text(encoding="utf-8")[:MAX_MD]
    pid = md_path.stem
    stamp = dt.datetime.now().strftime("%y%m%d")
    ask_line = f"THE ASK: {ask}" if ask else \
        "THE ASK: present this page's argument as a talk."
    prompt = PROMPT.format(pid=pid, ask_line=ask_line, md=md,
                           head=HEAD.format(title="{a short specific title}",
                                            a=assets),
                           a=assets, stamp=stamp)

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
    text = re.sub(r"^```(?:html)?\s*|\s*```$", "", text).strip()
    low = text.lower()
    if not low.startswith("<!doctype html"):
        return _fail("Claude did not return an HTML document")
    if not low.rstrip().endswith("</html>"):
        return _fail("the document is truncated (no closing </html>)")
    n = text.count('class="slide"')
    if n < 3:
        return _fail(f"only {n} slides came back — not written")
    for need in (f"{assets}/base.css", f"{assets}/runtime.js"):
        if need not in text:
            return _fail(f"the deck does not link {need} — its assets would 404")

    slide_dir.mkdir(exist_ok=True)
    when = dt.datetime.now().strftime("%y%m%d %H%M")
    text += f"\n<!-- autodeck: claude · {when} · ask: {ask or '(page)'} -->\n"
    tmp = out.with_suffix(".html.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(out)
    return {"ok": True, "slides": n, "deck": str(out.relative_to(root)),
            "url": "/" + out.relative_to(root).as_posix()}
