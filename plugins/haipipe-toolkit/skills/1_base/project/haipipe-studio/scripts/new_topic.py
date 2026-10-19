"""A studio topic: scaffold one, or save a session on it (haipipe-studio, b03 s21, 261007).

    python new_topic.py topic <level folder> --slug <topic> --title '<title>'
                              [--band concept|related|level|run|guide|procedure|server|slides] [--nn NN] [--feeds q01_x,q02_y]
                              [--builder] [--dry-run]
    python new_topic.py session <level folder> sNN --title '…' [--ask '…'] [--summary '…'] [--changed a,b]
                              [--date MMDD]

`topic` makes `studio/sNN-<topic>/` in the owning Block (also from a Job/Task input), with its face `sNN-<topic>.md` (Topic ·
Feeds · Files · Decided · Open), numbered in its band: s01-s09 concepts · s11-s19 levels · s21-s29 runs and
skills · s31-s39 Guide · s41-s49 Task procedures · s51-s59 server · s61-s69 slide drafts · s10-s19 related work, on a paper Board only (haipipe-paper-related). `--builder` adds `build_sNN_<topic>.py`, a builder on excalidraw-studio's draw.py that draws
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
# the close rule of a topic's soft Run, written into its ticket when the first session makes it; without one
# the ticket said `close: <what settles it>` and the Run had no end (b10 s06-D06, 261011)
DRAW_CLOSE = "a person moves the topic's Stage to agreed, or names what is still wrong in red on the drawing"
RECOMMENDED_TOPICS = 10
BANDS = {"concept": (1, 9), "related": (10, 19), "level": (11, 19), "run": (21, 29), "guide": (31, 39), "procedure": (41, 49), "server": (51, 59),
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
        "**Stage:** explore", "",
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


BUILDER = '''"""s{nn} · {title}: s{nn}-{slug}.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py (frames, a map, the key point,
the density badge, acts). The topic, its face and sessions: /haipipe-studio. A rebuild keeps whatever a person drew
on the canvas (canvas.write, a seed snapshot beside the drawing). Check it: excalidraw-studio's scripts/check.py.

    python {script}
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "{to_draw}").resolve()))
from draw import Drawing, canvas  # noqa: E402  (excalidraw-studio's helpers; canvas.write keeps a person's marks)

# every change to this drawing: (date YYMMDD, what changed). Each gets a green note where it changed
# (canvas.change_note beside the changed thing) and a line in the title frame (JL 261007)
CHANGES = []


def main():
    out = HERE / "s{nn}-{slug}.excalidraw"
    d = Drawing()
    f1 = d.frame("① {title}")                                    # one idea, one screen-sized frame
    d.heading("s{nn} · {title}", "<one line: what this frame says>")
    d.key(40, 196, 1400, 140)                                     # the frame's key point, the one slight colour
    d.para(64, 220, "<the key point, in one line>", 1350, 30)
    d.flow([{{"title": "<step 1>", "lines": ["<a fact read from disk>"]}},     # inside: a workflow map, or d.mind_map
            {{"title": "<step 2>", "lines": ["<a fact>"]}},
            {{"title": "? <an open question, in red>", "lines": []}}], 40, 400, 2480, labels=["<leads to>", "<then>"])
    for i, (date, what) in enumerate(CHANGES):                    # the title frame's list of changes
        e = canvas.change_note(1480, 220 + i * 26, what, date, f1["id"])
        e["id"] = f"c{{i}}"
        d.els.append(e)
    d.badge(f1)                                                   # its density, measured
    d.acts([{{"name": "Act 1 · <what the topic is about>", "frames": [f1["id"]]}}])
    d.write(out, "{script}")


if __name__ == "__main__":
    main()
'''


def block_owner(level: Path) -> Path:
    """The shared Studio owner, retaining standalone folders without a Block."""
    return next((candidate for candidate in (level, *level.parents)
                 if (candidate / "board.md").is_file() or re.match(r"^b\d+[_-]", candidate.name)), level)


def new_topic(level: Path, slug: str, title: str, band: str = "concept", nn: int | None = None,
              feeds: list[str] | None = None, builder: bool = False, dry_run: bool = False) -> Path:
    if not level.is_dir():
        raise ValueError(f"{level}: no such folder")
    # A Job or Task uses the same Block Studio; old local sessions remain readable.
    level = block_owner(level)
    if not SLUG.match(slug):
        raise ValueError(f"slug {slug!r}: lower-case letters, digits and - only")
    if band not in BANDS:
        raise ValueError(f"band {band!r}: one of {' · '.join(BANDS)}")
    nn = nn if nn is not None else next_in_band(level, band)
    if nn in topics(level):
        raise ValueError(f"s{nn:02d} is taken: {topics(level)[nn].name}")
    folder = level / "studio" / f"s{nn:02d}-{slug}"
    md = folder / f"{folder.name}.md"
    count = len(topics(level)) + 1
    if count > RECOMMENDED_TOPICS:
        print(f"Recommendation: {level.name} would have {count} studio topics; "
              f"aim for at most {RECOMMENDED_TOPICS}. Reuse a related topic or split "
              "an independent area into a peer Block.", file=sys.stderr)
    if dry_run:
        return md
    folder.mkdir(parents=True)
    feeds = [f.strip().removeprefix("reports/").strip("/") for f in feeds or []]   # `reports/q01_x` or `q01_x`
    md.write_text(face_text(nn, title, feeds).replace("<topic>", slug), encoding="utf-8")
    if builder:
        script = folder / f"build_s{nn:02d}_{slug.replace('-', '_')}.py"
        draw = HERE.parents[2] / "excalidraw" / "excalidraw-studio" / "scripts"   # excalidraw-studio's draw.py
        to_draw = os.path.relpath(draw, folder.resolve())       # both resolved: the builder resolves its own path
        script.write_text(BUILDER.format(nn=f"{nn:02d}", title=title, slug=slug, script=script.name,
                                         to_draw=Path(to_draw).as_posix()), encoding="utf-8")
        subprocess.run([sys.executable, str(script)], check=True, capture_output=True)
    return md


def save_session(level: Path, snn: str, title: str, ask: str = "", summary: str = "", changed=None,
                 date: str = "") -> Path:
    """A pass of `runs/run-draw-<sNN>/`, the topic's soft Run, made on its first session."""
    m = re.fullmatch(r"s(\d+)", snn)
    if m and int(m.group(1)) not in topics(level):
        level = block_owner(level)
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
                     ask=f"work on the studio topic {topic.name}", close=DRAW_CLOSE)
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
