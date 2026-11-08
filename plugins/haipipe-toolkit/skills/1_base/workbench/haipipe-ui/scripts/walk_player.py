"""A walk as a short video you can pause (JL 261105: "make it to be a very quick video and we can pause in the middle").

Turns a Chrome walk's GIF (gif_creator's export, one frame per action) into one self-contained HTML player: play and
pause, one frame back or on, a scrubber, the speed, and under each frame what was done there. The frames sit inside the
file (JPEG, at most 1200 px wide), so the player opens anywhere, from a theme Block's `walks/` folder in its Report or
on its own. Standard library and Pillow only.

    python walk_player.py <walk.gif | frames folder> <out.html> --title "<page>" [--frames 1-3,5] [--caption "…" ...] [--seconds 2]

A frames folder (walk_shoot.py's) brings its captions.txt, one line per frame, unless --caption is given.

`--frames` keeps those frames (from 0, in order); `--caption` is given once per kept frame. A walk saved into Tools
comes from a Tools placeholder page only (haipipe-ui Walk, step 9).
"""
from __future__ import annotations

import argparse
import base64
import html
import io
import json
from pathlib import Path

from PIL import Image, ImageSequence

PAGE = """<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#fff;--fg:#1e1e1e;--muted:#6c6c6c;--line:#e3e3e3;--accent:#1864ab}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;--muted:#9a9a97;--line:#2c2e33;--accent:#74a7e0}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
.wp{{max-width:1200px;margin:0 auto;padding:10px}}
.wp-h{{display:flex;align-items:baseline;gap:10px;margin:0 0 8px}}.wp-h b{{font-size:15px}}.wp-h span{{color:var(--muted);font-size:12px}}
.wp-img{{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#fff}}.wp-img img{{display:block;width:100%;height:auto}}
.wp-cap{{min-height:2.9em;margin:8px 2px 6px;font-size:14px}}
.wp-bar{{display:flex;align-items:center;gap:6px;flex-wrap:wrap}}
.wp-bar button,.wp-bar select{{font:inherit;font-size:13px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);padding:3px 9px;cursor:pointer}}
.wp-bar button.on{{border-color:var(--accent);color:var(--accent)}}
.wp-bar input[type=range]{{flex:1 1 160px;accent-color:var(--accent)}}.wp-n{{font-size:12px;color:var(--muted);min-width:4.5em;text-align:right}}
</style></head><body><div class=wp>
<div class=wp-h><b>{title}</b><span>space plays or pauses · ← → one step</span></div>
<div class=wp-img><img id=wpi alt=""></div>
<div class=wp-cap id=wpc></div>
<div class=wp-bar><button id=wpb title="one step back">◀</button><button id=wpp class=on>⏸ Pause</button>
<button id=wpf title="one step on">▶</button><input id=wps type=range min=0 value=0>
<select id=wpv title="speed"><option value=0.5>0.5×</option><option value=1 selected>1×</option><option value=2>2×</option></select>
<span class=wp-n id=wpn></span></div></div>
<script>(function(){{var F={frames},C={captions},S={seconds};
var i=0,play=true,t=null,img=document.getElementById('wpi'),cap=document.getElementById('wpc'),sc=document.getElementById('wps'),
n=document.getElementById('wpn'),pp=document.getElementById('wpp'),sp=document.getElementById('wpv');sc.max=F.length-1;
function show(k){{i=(k+F.length)%F.length;img.src=F[i];cap.textContent=C[i]||'';sc.value=i;n.textContent=(i+1)+' of '+F.length;}}
function tick(){{clearTimeout(t);if(play)t=setTimeout(function(){{show(i+1);tick();}},S*1000/parseFloat(sp.value));}}
function toggle(){{play=!play;pp.textContent=play?'⏸ Pause':'▶ Play';pp.classList.toggle('on',play);tick();}}
pp.onclick=toggle;document.getElementById('wpb').onclick=function(){{if(play)toggle();show(i-1);}};
document.getElementById('wpf').onclick=function(){{if(play)toggle();show(i+1);}};
sc.oninput=function(){{if(play)toggle();show(+sc.value);}};sp.onchange=tick;
document.addEventListener('keydown',function(e){{if(e.key===' '){{e.preventDefault();toggle();}}
else if(e.key==='ArrowLeft'){{if(play)toggle();show(i-1);}}else if(e.key==='ArrowRight'){{if(play)toggle();show(i+1);}}}});
show(0);tick();}})();</script></body></html>
"""


def pick(spec: str, n: int) -> list:
    """`1-3,5` -> [1, 2, 3, 5]; empty: every frame."""
    if not spec:
        return list(range(n))
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return [k for k in out if 0 <= k < n]


def frames(gif: Path, keep: str, width: int = 1200) -> list:
    """The frames of a GIF, or of a folder of NN.jpg / NN.png (walk_shoot.py's output), in name order."""
    if Path(gif).is_dir():
        shots = [Image.open(p).convert("RGB") for p in sorted(Path(gif).glob("*")) if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
    else:
        shots = [f.copy().convert("RGB") for f in ImageSequence.Iterator(Image.open(gif))]
    out = []
    for k in pick(keep, len(shots)):
        im = shots[k]
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=74, optimize=True)
        out.append("data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode())
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("gif", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--title", default="The walk")
    ap.add_argument("--frames", default="")
    ap.add_argument("--caption", action="append", default=[])
    ap.add_argument("--seconds", type=float, default=2.2)
    a = ap.parse_args()
    shots = frames(a.gif, a.frames)
    given = a.caption
    if not given and a.gif.is_dir() and (a.gif / "captions.txt").is_file():   # walk_shoot.py's one line per frame
        lines = (a.gif / "captions.txt").read_text(encoding="utf-8").splitlines()
        given = [lines[k] for k in pick(a.frames, len(lines))] if a.frames else lines
    caps = given + [""] * (len(shots) - len(given))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(PAGE.format(title=html.escape(a.title), frames=json.dumps(shots), captions=json.dumps(caps[:len(shots)],
                     ensure_ascii=False), seconds=a.seconds), encoding="utf-8")
    print(f"{a.out}: {len(shots)} frames, {a.out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
