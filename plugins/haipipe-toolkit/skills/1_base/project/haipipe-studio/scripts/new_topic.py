"""A studio topic: scaffold one, or save a session on it (haipipe-studio, b03 s21, 261007).

    python new_topic.py topic <level folder> --slug <topic> --title '<title>'
                              [--band concept|related|level|run|guide|procedure|server|slides] [--nn NN] [--feeds q01_x,q02_y]
                              [--builder] [--dry-run]
    python new_topic.py session <level folder> sNN --title '…' [--kind session|meeting] [--ask '…'] [--summary '…']
                                [--decided 'a; b'] [--started j02,t01] [--answered 'Q01: …'] [--next 'a; b']
                                [--read related/x.md] [--changed a,b]
                              [--date MMDD]

`topic` makes `sNN-<topic>/` directly in the level given, a Block, a Job or a Task, beside its jNN_/tNN_ folders (JL 261030:
"we don't have the studio/sNN, we just have sNN, along side with jNN, to make it visible directly"; an older `sNN-<topic>/`
still counts), at most LIMITS[level] per level ("we might have many sNN, but we need to control the numbers"), numbered once across the Block, with its face `sNN-<topic>.md` (Topic ·
For · Covers · Excluded · Feeds · Files · Decided · Open; one sNN, one idea, one delivery, JL 261030) and its mind map `sNN-<topic>.mindmap.md` (built from that face), numbered in its band: s01-s09 concepts · s11-s19 levels · s21-s29 runs and
skills · s31-s39 Guide · s41-s49 Task procedures · s51-s59 server · s61-s69 slide drafts · s10-s19 related work, on a paper Board only (haipipe-paper-related). Every topic also gets its quick drawing `sNN-<topic>.excalidraw` (quick_draw.py), a light scratch
opened from the ✎ on its line in the Block's map; `--builder` adds `build_sNN_<topic>.py`, a builder on excalidraw-studio's draw.py that draws
through canvas.write (a rebuild keeps the person's marks), and runs it once.

`session` saves one round of the topic (a working session or a meeting) inside it, `passes/pNN-<MMDD>/pass.md`:
Notes, Decided, Started, Answered, Next, Read, Changed.
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
LIMITS = {"Block": 9, "Job": 5, "Task": 3}    # sNN per level; more means the level is really two (JL 261030)
BANDS = {"concept": (1, 9), "related": (10, 19), "level": (11, 19), "run": (21, 29), "guide": (31, 39), "procedure": (41, 49), "server": (51, 59),
         "slides": (61, 69)}
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def topics(level: Path) -> dict[int, Path]:
    """{NN: folder} of the level's own studio topics: sNN-<topic>/ beside its Jobs or Tasks, or one in an older
    studio/ (sNN-<topic>/ or sNN_<topic>/)."""
    out = {}
    for holder in (level / "studio", level):
        for p in sorted(holder.iterdir()) if holder.is_dir() else []:
            m = re.match(r"^s(\d+)[-_]", p.name)
            if p.is_dir() and m and (holder != level or re.match(r"^s\d+-", p.name)):
                out.setdefault(int(m.group(1)), p)
    return out


def block_topics(level: Path) -> dict[int, Path]:
    """{NN: folder} across the whole Block: its own studio/, its Jobs' and its Tasks' (JL 261028: Studio lives at
    every level, with one sNN numbering per Block, so a number names one topic)."""
    block = block_owner(level)
    out = dict(topics(block))
    for job in sorted(block.glob("j[0-9]*_*")):
        for lvl in [job, *sorted(job.glob("t[0-9]*_*"))]:
            if lvl.is_dir():
                for nn, folder in topics(lvl).items():
                    out.setdefault(nn, folder)
    return out


def next_in_band(level: Path, band: str) -> int:
    lo, hi = BANDS[band]
    used = set(block_topics(level))
    for nn in range(lo, hi + 1):
        if nn not in used:
            return nn
    raise ValueError(f"the {band} band s{lo:02d}-s{hi:02d} is full in {level.name}")


def face_text(nn: int, title: str, feeds: list[str], at: str = "") -> str:
    name = f"s{nn:02d} · {title}"
    feed = " · ".join(feeds) if feeds else "<the Questions it feeds: qNN_<topic>>"
    return "\n".join([
        name, "=" * len(name), "",
        "**Stage:** explore", "",
        *([f"**At:** {at}", ""] if at else []),
        "**For:** <its one delivery: a deck, and the thing the deck is about (a draft, a figure, code or skills, a data"
        " table, a server package), and who it is for>", "",
        "**Delivery type:** <one word: skill · ui · code · draft · display · data; never deck, every sNN has one>", "",
        "**Covers:** <what this sNN decides, in a few parts>", "",
        "**Excluded:** <what it leaves to other sNN or Blocks, each named>", "",
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


def level_kind(level: Path) -> str:
    """Block, Job or Task, by the folder's name (bNN_, jNN_, tNN_); a standalone folder counts as a Block."""
    return {"j": "Job", "t": "Task"}.get(level.name[:1], "Block") if re.match(r"^[jt]\d+_", level.name) else "Block"


def new_topic(level: Path, slug: str, title: str, band: str = "concept", nn: int | None = None,
              feeds: list[str] | None = None, builder: bool = False, dry_run: bool = False,
              over_limit: bool = False) -> Path:
    if not level.is_dir():
        raise ValueError(f"{level}: no such folder")
    # The topic sits in the level's own folder, beside its Jobs or Tasks (b35-s01: no studio/ folder, JL 261030); its
    # number is unique in the Block, its address b17.j01-s07 (s01-D02) read from where it sits.
    if not SLUG.match(slug):
        raise ValueError(f"slug {slug!r}: lower-case letters, digits and - only")
    if band not in BANDS:
        raise ValueError(f"band {band!r}: one of {' · '.join(BANDS)}")
    nn = nn if nn is not None else next_in_band(level, band)
    if nn in block_topics(level):
        raise ValueError(f"s{nn:02d} is taken: {block_topics(level)[nn].name}")
    kind = level_kind(level)
    count, limit = len(topics(level)) + 1, LIMITS.get(kind, LIMITS["Block"])
    if count > limit and not over_limit:
        raise ValueError(f"{level.name} would hold {count} sNN; a {kind} holds at most {limit}. Reuse one, put it on "
                         "the Job or Task that uses its delivery, or split the level (--over-limit to add it anyway)")
    folder = level / f"s{nn:02d}-{slug}"
    md = folder / f"{folder.name}.md"
    if dry_run:
        return md
    folder.mkdir(parents=True)
    (folder / "delivery" / "deck").mkdir(parents=True)   # its agreed version goes here, then renders out (JL 261030)
    feeds = [f.strip().removeprefix("reports/").strip("/") for f in feeds or []]   # `reports/q01_x` or `q01_x`
    md.write_text(face_text(nn, title, feeds).replace("<topic>", slug), encoding="utf-8")
    if builder:
        script = folder / f"build_s{nn:02d}_{slug.replace('-', '_')}.py"
        draw = HERE.parents[2] / "excalidraw" / "excalidraw-studio" / "scripts"   # excalidraw-studio's draw.py
        to_draw = os.path.relpath(draw, folder.resolve())       # both resolved: the builder resolves its own path
        script.write_text(BUILDER.format(nn=f"{nn:02d}", title=title, slug=slug, script=script.name,
                                         to_draw=Path(to_draw).as_posix()), encoding="utf-8")
        subprocess.run([sys.executable, str(script)], check=True, capture_output=True)
    mind_map(folder)
    if not builder:                  # every topic gets its quick drawing by default, the ✎ on its Block-map line (JL 261029)
        import quick_draw
        quick_draw.quick(folder)
    return md


def mind_map(topic: Path) -> Path:
    """The topic's other side, its mind map `sNN-<topic>.mindmap.md`, started beside the face just written (the mind map
    skill, haipipe-mindmap): every sNN has both, its drawing and its map, linked by number (JL 261026)."""
    scripts = HERE.parents[1] / "haipipe-mindmap" / "scripts"
    sys.path.insert(0, str(scripts))
    import mindmap
    return mindmap.skeleton(topic)                    # its root and Files; written later, from the page and drawing


def save_session(level: Path, snn: str, title: str, ask: str = "", summary: str = "", changed=None,
                 date: str = "", kind: str = "session", decided=None, started=None, read=None, answered=None,
                 next_=None) -> Path:
    """One round of the topic: a working session or a meeting, kept inside the topic as `passes/pNN-<MMDD>/pass.md`
    (JL 261029: a Studio is the discussion; its rounds live with it). It says what was discussed (Notes), what was
    decided, what it sent to Work (Started) and to Report (Answered), what goes back to the Studio (Next), and what it
    read from related/. A topic with idea pictures gets its deck regathered after it (topic_slides.py)."""
    m = re.fullmatch(r"s(\d+)", snn)
    if not m or (int(m.group(1)) not in topics(level) and int(m.group(1)) not in block_topics(level)):
        raise ValueError(f"{snn}: no studio topic of that number in {block_owner(level).name} or its Jobs and Tasks")
    topic = topics(level).get(int(m.group(1))) or block_topics(level)[int(m.group(1))]   # the level's own first
    passes = topic / "passes"
    date = date or __import__("datetime").date.today().strftime("%m%d")
    n = 1 + max([int(x.name[1:3]) for x in passes.glob("p[0-9][0-9]-*")] or [0])
    out = passes / f"p{n:02d}-{date}"
    out.mkdir(parents=True)
    lines = lambda xs: "\n".join(f"- {x}" for x in xs) if xs else "<nothing>"
    (out / "pass.md").write_text(
        f"# {title}\n\nkind: {kind}\n\n## Notes\n\n{(ask + chr(10) + chr(10) + summary).strip() or '<nothing>'}\n\n"
        f"## Decided\n\n{lines(list(decided or []))}\n\n## Started\n\n{lines(list(started or []))}\n\n"
        f"## Answered\n\n{lines(list(answered or []))}\n\n## Next\n\n{lines(list(next_ or []))}\n\n"
        f"## Read\n\n{lines(list(read or []))}\n\n## Changed\n\n{lines(list(changed or []))}\n", encoding="utf-8")
    sys.path.insert(0, str(HERE))
    import topic_slides
    try:
        if (topic / f"{topic.name}.slides.json").is_file():   # a topic with idea pictures gets its deck regathered
            topic_slides.write(topic)
    except SystemExit as err:                            # no html-ppt above this folder: the round stands without slides
        print(f"slides not rebuilt: {err}", file=sys.stderr)
    return out


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
    p.add_argument("--over-limit", action="store_true")
    p = sub.add_parser("session")
    p.add_argument("level", type=Path)
    p.add_argument("snn")
    p.add_argument("--title", required=True)
    p.add_argument("--kind", default="session", choices=["session", "meeting"])
    for k in ("ask", "summary", "changed", "date", "decided", "started", "read", "answered", "next"):
        p.add_argument(f"--{k}", default="")
    a = ap.parse_args()
    split = lambda v: [x.strip() for x in v.split(",") if x.strip()]
    try:
        if a.cmd == "topic":
            out = new_topic(a.level, a.slug, a.title, a.band, a.nn, split(a.feeds), a.builder, a.dry_run, a.over_limit)
        else:
            out = save_session(a.level, a.snn, a.title, a.ask, a.summary, split(a.changed), a.date, a.kind,
                               [x.strip() for x in a.decided.split(";") if x.strip()], split(a.started), split(a.read),
                               [x.strip() for x in a.answered.split(";") if x.strip()],
                               [x.strip() for x in a.next.split(";") if x.strip()])
    except ValueError as err:
        print(f"refused: {err}", file=sys.stderr)
        return 2
    print(("would write " if getattr(a, "dry_run", False) else "") + str(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
