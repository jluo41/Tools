"""A studio topic: scaffold one, or save a session on it (haipipe-studio, b03 s21, 261007).

    python new_topic.py topic <level folder> --slug <topic> --title '<title>'
                              [--band concept|level|run|guide|server|slides] [--nn NN] [--feeds q01_x,q02_y]
                              [--builder] [--dry-run]
    python new_topic.py session <level folder> sNN --title '…' [--ask '…'] [--summary '…'] [--changed a,b]
                              [--date MMDD]

`topic` makes `studio/sNN-<topic>/` in a Block, Job or Task, with its face `sNN-<topic>.md` (Topic ·
Feeds · Files · Decided · Open), numbered in its band: s01-s09 concepts · s11-s19 levels · s21-s29 runs and
skills · s31-s39 Guide · s51-s59 server · s61-s69 slide drafts. `--builder` adds `build_sNN_<topic>.py`, a builder that draws
through canvas.write (a rebuild keeps the person's marks), and runs it once.

`session` saves one working session as a pass of the topic's soft Run `runs/run-draw-<sNN>/`
(haipipe-run's soft_run.py writes the card), which the Idea Studio lists under the topic.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN_SCRIPTS = HERE.parents[1] / "haipipe-run" / "scripts"
BANDS = {"concept": (1, 9), "level": (11, 19), "run": (21, 29), "guide": (31, 39), "server": (51, 59),
         "slides": (61, 69)}
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def topics(level: Path) -> dict[int, Path]:
    """{NN: folder} of the level's studio topics (sNN-<topic>/, or the older sNN_<topic>/)."""
    studio = level / "studio"
    out = {}
    for p in sorted(studio.iterdir()) if studio.is_dir() else []:
        m = re.match(r"^s(\d+)[-_]", p.name)
        if p.is_dir() and m:
            out[int(m.group(1))] = p
    return out


def next_in_band(level: Path, band: str) -> int:
    lo, hi = BANDS[band]
    used = set(topics(level))
    for nn in range(lo, hi + 1):
        if nn not in used:
            return nn
    raise ValueError(f"the {band} band s{lo:02d}-s{hi:02d} is full in {level.name}/studio/")


def face_text(nn: int, title: str, feeds: list[str]) -> str:
    name = f"s{nn:02d} · {title}"
    feed = " · ".join(feeds) if feeds else "<the Questions it feeds: qNN_<topic>>"
    return "\n".join([
        name, "=" * len(name), "",
        "**Topic:** <one paragraph: what this topic thinks through, and why now>", "",
        f"**Feeds:** `reports/` {feed}", "",
        "", "Files", "-----", "",
        "```text", f"s{nn:02d}-<topic>/", f"├── s{nn:02d}-<topic>.md        this face", "└── <drawings, builder>",
        "```", "",
        "", "Decided", "-------", "",
        f"(none yet: a decision is one line, s{nn:02d}-D01 · <what was decided> (<who> <date>))", "",
        "", "Open", "----", "",
        "1. <the first open point>", "",
        "(write here, or mark the drawing in red)", ""])


BUILDER = '''"""s{nn} · {title}: s{nn}-{slug}.excalidraw, drawn by this builder (haipipe-studio).

A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside the drawing).

    python {script}
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "{to_scripts}").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

INK, RED = canvas.INK, canvas.RED      # the studio look: black; red for an open question; green notes
els = []
# every change to this drawing: (date YYMMDD, what changed). Each gets a green note where it changed
# (canvas.change_note beside the changed thing) and a line in the title frame (JL 261007)
CHANGES = []


def el(kind, x, y, w, h, **extra):
    e = {{"id": f"e{{len(els)}}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
          "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
          "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
          "roundness": None, "seed": 1, "version": 1, "versionNonce": 1, "isDeleted": False,
          "boundElements": [], "updated": 1, "link": None, "locked": False}}
    e.update(extra)
    els.append(e)
    return e


def text(x, y, s, size=20, frame=None, color=INK):
    lines = s.split("\\n")
    return el("text", x, y, max(len(l) for l in lines) * size * 0.55, len(lines) * size * 1.25, text=s,
              originalText=s, fontSize=size, fontFamily=6, textAlign="left", verticalAlign="top",  # 6 Nunito, the studio font
              containerId=None, autoResize=True, lineHeight=1.25, frameId=frame, strokeColor=color)


def main():
    out = HERE / "s{nn}-{slug}.excalidraw"
    els.clear()
    f1 = el("frame", 0, 0, 1600, 900, name="1 · {title}")
    text(40, 40, "s{nn} · {title}", 36, f1["id"])
    text(40, 110, "<draw the topic here: a tree, lines and boxes, in black>", 22, f1["id"])
    text(40, 140, "? <an open question, in red>", 22, f1["id"], RED)
    for i, (date, what) in enumerate(CHANGES):          # the title frame's list of changes
        els.append(canvas.change_note(40, 190 + i * 26, what, date, f1["id"]))
    for e in canvas.off_palette(els):                    # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, els, "{script}")


if __name__ == "__main__":
    main()
'''


def new_topic(level: Path, slug: str, title: str, band: str = "concept", nn: int | None = None,
              feeds: list[str] | None = None, builder: bool = False, dry_run: bool = False) -> Path:
    if not level.is_dir():
        raise ValueError(f"{level}: no such folder")
    if not SLUG.match(slug):
        raise ValueError(f"slug {slug!r}: lower-case letters, digits and - only")
    if band not in BANDS:
        raise ValueError(f"band {band!r}: one of {' · '.join(BANDS)}")
    nn = nn if nn is not None else next_in_band(level, band)
    if nn in topics(level):
        raise ValueError(f"s{nn:02d} is taken: {topics(level)[nn].name}")
    folder = level / "studio" / f"s{nn:02d}-{slug}"
    md = folder / f"{folder.name}.md"
    if dry_run:
        return md
    folder.mkdir(parents=True)
    md.write_text(face_text(nn, title, feeds or []).replace("<topic>", slug), encoding="utf-8")
    if builder:
        script = folder / f"build_s{nn:02d}_{slug.replace('-', '_')}.py"
        to_scripts = os.path.relpath(HERE, folder.resolve())    # both resolved: the builder resolves its own path
        script.write_text(BUILDER.format(nn=f"{nn:02d}", title=title, slug=slug, script=script.name,
                                         to_scripts=Path(to_scripts).as_posix()), encoding="utf-8")
        subprocess.run([sys.executable, str(script)], check=True, capture_output=True)
    return md


def save_session(level: Path, snn: str, title: str, ask: str = "", summary: str = "", changed=None,
                 date: str = "") -> Path:
    """A pass of `runs/run-draw-<sNN>/`, the topic's soft Run, made on its first session."""
    m = re.fullmatch(r"s(\d+)", snn)
    if not m or int(m.group(1)) not in topics(level):
        raise ValueError(f"{snn}: no studio topic of that number in {level.name}/studio/")
    sys.path.insert(0, str(RUN_SCRIPTS))
    import soft_run
    run = level / "runs" / f"run-draw-{snn}"
    if not run.is_dir():
        topic = topics(level)[int(m.group(1))]
        face = topic / f"{topic.name}.md"
        fed = re.search(r"\*\*Feeds:\*\*(.+?)(?:\n\s*\n|\Z)", face.read_text(encoding="utf-8"), re.S) \
            if face.is_file() else None              # the Questions its face says it feeds
        feeds = [f"reports/{q}" for q in dict.fromkeys(re.findall(r"q\d\d_[A-Za-z0-9_]+", fed.group(1)))] if fed else []
        soft_run.new(level, "draw", snn, skill="haipipe-studio", feeds=feeds,
                     ask=f"work on the studio topic {topic.name}")
    return soft_run.add_pass(run, title, ask, summary, list(changed or []), date)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("topic")
    p.add_argument("level", type=Path)
    p.add_argument("--slug", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--band", default="concept", choices=sorted(BANDS))
    p.add_argument("--nn", type=int)
    p.add_argument("--feeds", default="")
    p.add_argument("--builder", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("session")
    p.add_argument("level", type=Path)
    p.add_argument("snn")
    p.add_argument("--title", required=True)
    for k in ("ask", "summary", "changed", "date"):
        p.add_argument(f"--{k}", default="")
    a = ap.parse_args()
    split = lambda v: [x.strip() for x in v.split(",") if x.strip()]
    try:
        if a.cmd == "topic":
            out = new_topic(a.level, a.slug, a.title, a.band, a.nn, split(a.feeds), a.builder, a.dry_run)
        else:
            out = save_session(a.level, a.snn, a.title, a.ask, a.summary, split(a.changed), a.date)
    except ValueError as err:
        print(f"refused: {err}", file=sys.stderr)
        return 2
    print(("would write " if getattr(a, "dry_run", False) else "") + str(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
