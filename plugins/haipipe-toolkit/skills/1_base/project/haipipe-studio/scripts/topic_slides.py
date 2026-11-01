"""A Studio topic's idea slides: its pictures gathered into a deck, `.slides.html` to look at, `.slides.pptx` to send.

    python topic_slides.py <studio/sNN-topic>

JL 261029: a Studio is never a report ("不要把 studio 写成一个中规中矩的 report"); its slides are open ideas, each one
finished picture that pulls a reader in within seconds. The pictures are made one per idea by image generation from
the topic's `sNN-<topic>.ideas.md` (the question, its options, the leaning, what is still open) and kept as source in
`slides/`. `sNN-<topic>.slides.json` names the deck's look once, `"style"` (a Studio's is `sketch-notes`, JL 261029:
"sketch note looks great"; any style of haipipe-display `_parts/slide/styles/`), then records each slide: id, idea,
content, image, notes. haipipe-display's `_parts/slide/scripts/slide_prompt.py --deck <topic> --slide NN` turns a
slide's content into its full prompt. This script only gathers the pictures: the HTML
deck shows one picture per slide, and the PowerPoint has each picture full-slide with its notes as speaker notes. Both
files are generated and git-ignored; a lasting change goes in the ideas file and a new picture.
"""
from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def esc(text: str) -> str:
    return html.escape(text or "", quote=True)


def record(topic: Path) -> list[dict]:
    """The slides the topic's record names, in order, each with its picture on disk."""
    spec = topic / f"{topic.name}.slides.json"
    if not spec.is_file():
        raise SystemExit(f"{topic.name} has no {spec.name}: make its idea pictures first")
    slides = json.loads(spec.read_text(encoding="utf-8"))["slides"]
    words = ideas(topic)
    for s in slides:                                     # a picture not drawn yet: its card of words, from the ideas file
        if s.get("image") and not (topic / s["image"]).is_file():
            s.pop("image")
        if not s.get("image") and not s.get("points"):
            s.update({k: v for k, v in words.get(s["idea"].strip(), {}).items() if not s.get(k)})
    return slides


def ideas(topic: Path) -> dict:
    """Each idea of `sNN-<topic>.ideas.md` by its heading: its points (the options), leaning and ask."""
    f = topic / f"{topic.name}.ideas.md"
    out = {}
    for chunk in re.split(r"(?m)^## ", f.read_text(encoding="utf-8"))[1:] if f.is_file() else []:
        head, _, body = chunk.partition("\n")
        out[head.strip()] = {"points": [x.strip() for x in re.findall(r"(?m)^\s*-\s+(.+)$", body)],
                             "leaning": (re.search(r"(?m)^leaning:\s*(.+)$", body) or [None, ""])[1],
                             "ask": (re.search(r"(?m)^ask:\s*(.+)$", body) or [None, ""])[1]}
    return out


def scratch(s: dict) -> str:
    """A slide with no picture yet, as a card of its words (JL 261029: "first try to make the quick scratch, and later
    we can draw the images"): its idea, its points, the leaning ★, what is still asked."""
    plain = lambda x: (x or "").replace("`", "")                 # a card shows words, not Markdown marks
    s = {**s, "idea": plain(s.get("idea")), "leaning": plain(s.get("leaning")), "ask": plain(s.get("ask")),
         "points": [plain(p) for p in s.get("points", [])]}
    points = "".join(f"<li>{esc(p)}</li>" for p in s.get("points", []))
    return (f'<div class="card"><h1>{esc(s["idea"])}</h1>' + (f"<ul>{points}</ul>" if points else "")
            + (f'<p class="lean">★ {esc(s["leaning"])}</p>' if s.get("leaning") else "")
            + (f'<p class="ask">? {esc(s["ask"])}</p>' if s.get("ask") else "")
            + '<p class="tag">scratch · its picture comes when asked</p></div>')


def deck(topic: Path, slides: list[dict]) -> str:
    pages = "".join(f'<section>' + (f'<img src="{esc(s["image"])}" alt="{esc(s["idea"])}">' if s.get("image") else scratch(s))
                    + f'<p class="notes">{esc(s.get("notes", ""))}</p></section>' for s in slides)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(topic.name)} · ideas</title>
<!-- GENERATED FILE: haipipe-studio scripts/topic_slides.py, from {esc(topic.name)}.slides.json; never edit by hand. -->
<style>
html,body{{margin:0;height:100%;background:#fff;font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#1c1c1c}}
section{{display:none;height:100vh;flex-direction:column;align-items:center;justify-content:center}}section.on{{display:flex}}
img{{max-width:100vw;max-height:calc(100vh - 44px);object-fit:contain}}
.notes{{display:none;max-width:900px;margin:6px 16px;color:#6f6f6b}}body.n .notes{{display:block}}
.bar{{position:fixed;bottom:10px;right:16px;font-size:13px;color:#6f6f6b}}.bar a{{color:#1864ab;margin-left:12px}}
.card{{width:min(980px,88vw);aspect-ratio:16/9;box-sizing:border-box;padding:56px 64px;border:2px solid #343a40;border-radius:18px;
 background:#fffdf6;box-shadow:6px 6px 0 #e9ecef;display:flex;flex-direction:column;justify-content:center}}
.card h1{{font-size:clamp(24px,3.4vw,40px);line-height:1.2;margin:0 0 22px;color:#1e3a5f}}
.card ul{{margin:0 0 14px;padding-left:26px;font-size:clamp(16px,1.9vw,23px)}}.card li{{margin:6px 0}}
.card .lean{{font-size:clamp(15px,1.7vw,20px);color:#2b8a3e;margin:6px 0}}.card .ask{{font-size:clamp(15px,1.7vw,20px);color:#c92a2a;margin:6px 0}}
.card .tag{{margin:18px 0 0;font-size:12px;color:#adb5bd}}
</style></head>
<body>
{pages}
<div class="bar"><span id="at"></span><a href="#" id="nt">notes</a><a href="{esc(topic.name)}.slides.pptx" download>PowerPoint file</a></div>
<script>
var s=document.querySelectorAll('section'),i=Math.max(0,parseInt(location.hash.slice(1)||'1')-1);
function show(k){{i=Math.min(Math.max(k,0),s.length-1);s.forEach(function(e,j){{e.classList.toggle('on',j===i)}});
 document.getElementById('at').textContent=(i+1)+' / '+s.length+' · ← →';history.replaceState(null,'','#'+(i+1));}}
document.addEventListener('keydown',function(e){{if(e.key==='ArrowRight'||e.key===' ')show(i+1);if(e.key==='ArrowLeft')show(i-1);}});
document.addEventListener('click',function(e){{if(e.target.closest('.bar'))return;show(e.clientX>innerWidth/2?i+1:i-1);}});
document.getElementById('nt').onclick=function(e){{e.preventDefault();document.body.classList.toggle('n');}};
show(i);
</script>
</body></html>
'''


def write_pptx(topic: Path, out: Path) -> Path:
    """Each picture full-slide on a 16:9 page, its notes as the speaker notes."""
    from pptx import Presentation
    from pptx.util import Emu, Inches
    slides = record(topic)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    for s in slides:
        page = prs.slides.add_slide(prs.slide_layouts[6])
        if not s.get("image"):                              # a scratch: its words in one text box
            box = page.shapes.add_textbox(Inches(0.8), Inches(0.7), prs.slide_width - Inches(1.6), prs.slide_height - Inches(1.4))
            tf = box.text_frame
            tf.word_wrap = True
            tf.text = s["idea"]
            for line in [f"• {p}" for p in s.get("points", [])] + ([f"★ {s['leaning']}"] if s.get("leaning") else []) \
                    + ([f"? {s['ask']}"] if s.get("ask") else []):
                tf.add_paragraph().text = line
            page.notes_slide.notes_text_frame.text = s.get("notes", "")
            continue
        pic = page.shapes.add_picture(str(topic / s["image"]), 0, 0, width=prs.slide_width)
        if pic.height > prs.slide_height:                  # a taller picture fits by height, centred
            ratio = prs.slide_height / pic.height
            pic.height, pic.width = prs.slide_height, int(pic.width * ratio)
            pic.left = Emu((prs.slide_width - pic.width) // 2)
        else:
            pic.top = Emu((prs.slide_height - pic.height) // 2)
        pic.name = s["idea"]
        page.notes_slide.notes_text_frame.text = s.get("notes", "")
    prs.save(out)
    return out


def write(topic: Path) -> Path:
    """Both files, the HTML deck and the PowerPoint; returns the HTML deck."""
    topic = Path(os.path.abspath(topic))                  # "." names its folder; never resolved through a symlink
    topic = topic if topic.is_dir() else topic.parent
    out = topic / f"{topic.name}.slides.html"
    out.write_text(deck(topic, record(topic)), encoding="utf-8")
    pptx = topic / f"{topic.name}.slides.pptx"
    try:
        import pptx as _  # noqa: F401
        write_pptx(topic, pptx)
    except ImportError:                                   # this Python lacks python-pptx: uv brings it for one call
        subprocess.run(["uv", "run", "-q", "--with", "python-pptx", "python", __file__, "--pptx", str(topic)], check=False)
    return out


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--pptx":
        t = Path(os.path.abspath(sys.argv[2]))
        print(write_pptx(t, t / f"{t.name}.slides.pptx"))
    elif len(sys.argv) == 2:
        print(write(Path(sys.argv[1])))
    else:
        sys.exit(__doc__.split("\n\n")[1])
