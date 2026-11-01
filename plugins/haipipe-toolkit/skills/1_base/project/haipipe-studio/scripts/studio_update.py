"""Bring existing sNN up to today's rules, and redraw each in five parts (JL 261030: "should we have something like
/haipipe-studio update"; "please go ahead to update the whole studios here, and also for their draw").

    python studio_update.py audit  <path>                    one line per sNN: what it misses today
    python studio_update.py update <path>                    the plan, nothing written (a dry run)
    python studio_update.py update <path> --apply            the mechanical steps, sNN by sNN
    python studio_update.py name   <sNN> --for "<...>" --type skill    an agent's proposal, written into the face
    python studio_update.py brief  <path>                    what an agent reads to name the sNN that lack them
    python studio_update.py name-batch <proposals.json>      many proposals: [{"topic", "for", "type"}]

<path> is any folder: a SPACE, a Project, a Block, one sNN. Three kinds of step:

    apply    Stage line (explore) · delivery/ with deck/ and a render.yaml · its mind map (haipipe-mindmap from-topic)
             · its drawing in five parts (five_parts.py), the old drawing kept whole as its Design
             · its Slide deck as a quick scratch (.ideas.md from the face, .slides.json, topic_slides.py), pictures
               only when a person asks
    person   the For: line and the Delivery type: word (the agent proposes them with `name`, a person agrees: the
             face's Open gets one point to agree them) · a level over its limit (9 at a Block, 5 at a Job, 3 at a Task)
    move     out of studio/ beside its Jobs: studio_move.py (JL 261031), which also rewrites the links; audit lists
             an sNN still in studio/, update never moves

The old drawing: <sNN>.excalidraw (or its first drawing) is copied once to result/first-drawing.excalidraw and drawn
whole as the Design part; a builder that wrote it moves to result/first-drawing-builder/, since rerunning it would draw
over the five parts. An sNN drawn by its own five_parts builder (b35's) is never redrawn here.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import five_parts as fp  # noqa: E402
from gallery_scan import SKIP, SNN, level_of  # noqa: E402

TYPES = ("skill", "ui", "code", "draft", "display", "data")
LIMITS = {"Block": 9, "Job": 5, "Task": 3}
ICON = {"skill": "book", "ui": "code", "code": "code", "draft": "doc", "display": "page", "data": "page"}
SOURCE = "haipipe-studio studio_update.py"                  # a drawing this script wrote, so a rerun refreshes it
MINDMAP = HERE.parents[1] / "haipipe-mindmap" / "scripts" / "mindmap.py"
TODAY = __import__("datetime").date.today().strftime("%y%m%d")   # from the clock, never written by hand
# the wrapper helpers an old builder imports to draw its own sNN's drawing (a Job view, a Section canvas, ...)
DRAWERS = ("section_canvas", "related_map", "model_option", "studio_job_layout")   # each draws HERE's own drawing


# ── finding and reading ──────────────────────────────────────────────────────────────────────────────────────────

def topics(root: Path) -> list[Path]:
    """Every sNN under root that has its face: beside a level's Jobs or Tasks, or in an older studio/."""
    root = root.resolve()
    if SNN.match(root.name) and (root / f"{root.name}.md").is_file():
        return [root]
    out = []
    for d, subs, files in os.walk(root, followlinks=False):
        p = Path(d)
        subs[:] = sorted(s for s in subs if s not in SKIP and not s.startswith(".") and not (p / s).is_symlink()
                         and not (s.endswith("-SPACE") and p != root))
        if SNN.match(p.name) and f"{p.name}.md" in files and p != root:
            out.append(p)
            subs[:] = []
    return out


def owner(topic: Path) -> Path:
    return topic.parent.parent if topic.parent.name == "studio" else topic.parent


def job_of(topic: Path) -> Path | None:
    """The Job whose work makes this sNN's delivery, for its Process part: the Job it sits in, or its Task's Job; a
    Block's sNN has none of its own (JL 261031: Process said "no Job yet" beside b63 j01's t01 and its Runs)."""
    o = owner(topic)
    if re.match(r"j\d+_", o.name):
        return o
    return o.parent if re.match(r"t\d+_", o.name) and re.match(r"j\d+_", o.parent.name) else None


def face(topic: Path) -> Path:
    return topic / f"{topic.name}.md"


def line_of(text: str, name: str) -> str:
    m = re.search(rf"(?ms)^\*\*{name}:\*\*[^\S\n]*(.+?)(?:\n\s*\n|\Z)", text)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def dtype_of(text: str) -> str:
    m = re.search(r"(?mi)^\*\*Delivery type:\*\*[^\S\n]*`?([A-Za-z]+)", text)
    return m.group(1).lower() if m and m.group(1).lower() in TYPES else ""


def custom_built(topic: Path) -> bool:
    """Drawn by its own five_parts builder (b35's s01 to s05): this script leaves its drawing alone."""
    return any("five_parts" in b.read_text(encoding="utf-8", errors="ignore") for b in topic.glob("build_*.py"))


def five_part(drawing: Path) -> bool:
    if not drawing.is_file():
        return False
    try:
        doc = json.loads(drawing.read_text(encoding="utf-8"))
    except ValueError:
        return False
    return doc.get("source") == SOURCE                           # set last, so a draw cut short is drawn again


# ── what each sNN misses ─────────────────────────────────────────────────────────────────────────────────────────

def checks(topic: Path, counts: dict) -> list[tuple[str, str, str]]:
    """(kind, key, words): kind is apply, person or move."""
    text = face(topic).read_text(encoding="utf-8", errors="ignore")
    out = []
    if topic.parent.name == "studio":
        out.append(("move", "place", "in studio/, not beside its Jobs: studio_move.py"))
    if not re.search(r"(?m)^\*\*Stage:\*\*", text):
        out.append(("apply", "stage", "no **Stage:** line"))
    if not line_of(text, "For"):
        out.append(("person", "for", "no **For:** line"))
    if not dtype_of(text):
        out.append(("person", "type", "no **Delivery type:** word"))
    if not (topic / "delivery" / "deck").is_dir():
        out.append(("apply", "delivery", "no delivery/deck/"))
    if not (topic / "delivery" / "render.yaml").is_file():
        out.append(("apply", "render", "no delivery/render.yaml"))
    if not (topic / f"{topic.name}.mindmap.md").is_file():
        out.append(("apply", "mindmap", "no mind map"))
    if not custom_built(topic) and not five_part(topic / f"{topic.name}.excalidraw"):
        out.append(("apply", "draw", "drawing not in five parts"))
    elif not custom_built(topic) and old_builders(topic):
        out.append(("apply", "builder", "an old builder beside its five-part drawing"))
    if not (topic / f"{topic.name}.slides.html").is_file():
        out.append(("apply", "slides", "no Slide deck"))
    if dtype_of(text) == "data" and not any("data_table" in b.read_text(encoding="utf-8", errors="ignore")
                                            for b in list(topic.glob("build_*.py")) + list(topic.glob("sketch_*.py"))):
        out.append(("person", "data-built", "a data topic: its Design does not yet draw the data built step by step "
                                            "(excalidraw-studio § A data topic, JL 261031)"))
    lvl = level_of(owner(topic))
    n = counts.get(owner(topic), 0)
    if n > LIMITS.get(lvl, 99):
        out.append(("person", "limit", f"{owner(topic).name} holds {n} sNN, its limit is {LIMITS[lvl]}"))
    return out


def level_counts(found: list[Path]) -> dict:
    """How many sNN each level holds, counted over all of that level's sNN, not only the ones found."""
    owners = {owner(t) for t in found}
    return {o: sum(1 for p in [*o.iterdir(), *((o / "studio").iterdir() if (o / "studio").is_dir() else [])]
                   if p.is_dir() and SNN.match(p.name) and (p / f"{p.name}.md").is_file()) for o in owners}


# ── the apply steps ──────────────────────────────────────────────────────────────────────────────────────────────

def add_stage(topic: Path) -> None:
    f = face(topic)
    text = f.read_text(encoding="utf-8")
    m = re.search(r"(?m)^(?:=+|-+)\n|^# .+\n", text)              # after the title (setext or #)
    at = m.end() if m else 0
    f.write_text(text[:at] + "\n**Stage:** explore\n" + text[at:], encoding="utf-8")


def add_delivery(topic: Path) -> None:
    deck = topic / "delivery" / "deck"
    deck.mkdir(parents=True, exist_ok=True)
    if not any(deck.iterdir()):
        (deck / ".gitkeep").write_text("")
    card = topic / "delivery" / "render.yaml"
    if not card.is_file():
        card.write_text(f"# Where {topic.name.split('-')[0]}'s delivery goes (haipipe-studio scripts/render_delivery.py). "
                        "The deck stays in deck/.\n# No piece yet: add one once the delivery is agreed: a text piece "
                        "(from, to, block), a code piece (code, by) or a Theme piece (from, rendered_by).\npieces: []\n",
                        encoding="utf-8")


def add_mindmap(topic: Path) -> None:
    subprocess.run([sys.executable, str(MINDMAP), "from-topic", str(topic)], check=True, stdout=subprocess.DEVNULL)


def keep_old(topic: Path) -> Path | None:
    """Copy the old drawing once to result/first-drawing.excalidraw; move a builder that wrote it out of the way."""
    kept = topic / "result" / "first-drawing.excalidraw"
    if kept.is_file():
        return kept
    from_drawings = [d for d in sorted(topic.glob("*.excalidraw")) if not d.name.startswith("m")]
    own = topic / f"{topic.name}.excalidraw"
    old = own if own.is_file() else (from_drawings[0] if from_drawings else None)
    if old is None or five_part(old):
        return None
    kept.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(old, kept)
    park_builders(topic)
    return kept


def old_builders(topic: Path) -> list[Path]:
    """The scripts beside the face that drew the sNN's own drawing, <sNN>.excalidraw: one that names it, builds it from
    HERE.name, calls draw(HERE) (a Job-view wrapper) or imports a wrapper helper; never one built on five_parts, a deck's
    builder, or one that draws another file or writes a table or a .docx."""
    out = []
    for b in sorted(topic.glob("*.py")):
        src = b.read_text(encoding="utf-8", errors="ignore")
        if "five_parts" in src or "deck" in b.stem:              # its own five parts, or a slide deck's builder
            continue
        own = (f"{topic.name}.excalidraw" in src or "draw(HERE)" in src
               or bool(re.search(r"HERE\.name[^\n]{0,40}\.excalidraw", src))
               or bool(re.search(r"(?m)^\s*(?:from|import)\s+(" + "|".join(DRAWERS) + r")\b", src)))
        if own:                                                  # one drawing another file, a table or a .docx stays
            out.append(b)
    return out


def park_builders(topic: Path) -> None:
    """Move them to result/first-drawing-builder/: rerun, they would draw over the five parts."""
    for b in old_builders(topic):
        dest = topic / "result" / "first-drawing-builder" / b.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(b), str(dest))


def kept_design(topic: Path, kept: Path | None) -> list:
    """The old drawing, whole and at its own size, as the Design part; Process and Delivery move right past it."""
    if kept is None:
        return fp.text("kd_none", 690, 280, "no sketch yet: draw the first proposal here", 18, fp.ROOM)
    els = fp.kept_first(topic, 280, label=f"{topic.name.split('-')[0]}'s drawing before {TODAY}, kept whole (also in result/first-drawing.excalidraw)")
    return els                                                  # whole, at its size: shrunk, its words overlap


def spec_of(topic: Path) -> dict:
    """The five parts' facts, read from the face: its title, why (its Topic), what it hands over (For, type)."""
    text = face(topic).read_text(encoding="utf-8", errors="ignore")
    nn = topic.name.split("-")[0]
    first = text.strip().splitlines()[0] if text.strip() else topic.name
    title = re.sub(r"^#+\s*|^s\d+\s*[·:-]\s*", "", first).strip() or topic.name
    plain = lambda s: re.sub(r"[`*_]|\[([^\]]+)\]\([^)]*\)", lambda m: m.group(1) or "", s)
    said = plain(line_of(text, "Topic") or line_of(text, "Covers") or title)
    bits = [b.strip() for b in re.split(r"(?<=[.;:])\s+|\s+\(", said) if len(b.strip()) > 3][:3]
    notes = ["\n".join(fp.textwrap.wrap(fp.textwrap.shorten(b, 64, placeholder="…"), 22)[:3]) for b in bits]
    q = re.search(r"(JL \d{6})[^\n“\"]{0,40}[“\"]([^”\"\n]{6,90})[”\"]", text)
    for_line = plain(line_of(text, "For"))
    dtype = dtype_of(text)
    parts = [(ICON.get(dtype, "doc"), fp.textwrap.shorten(for_line, 46, placeholder="…") if for_line else "not named yet",
              "its For: line" if for_line else "the agent proposes **For:**, a person agrees", bool(for_line))]
    held = sorted(p.name for p in (topic / "delivery").iterdir() if p.name not in ("deck", "render.yaml") and
                  not p.name.startswith(".")) if (topic / "delivery").is_dir() else []
    parts += [("page", f"delivery/{n}", "agreed, in delivery/", True) for n in held[:4]]
    try:
        import yaml
        pieces = (yaml.safe_load((topic / "delivery" / "render.yaml").read_text()) or {}).get("pieces") or []
    except (OSError, ValueError, AttributeError):
        pieces = []
    target = next((Path(p["to"]).name for p in pieces if isinstance(p, dict) and "to" in p), "") or "not set yet"
    return {"title": title,
            "why": {"question": f"why do we need {nn}?", "notes": notes or ["(its Topic, not written yet)"],
                    "quote": f"{q.group(1)}: “{q.group(2)}”" if q else ""},
            "what": {"head": f"② what {nn} hands over", "icon": ICON.get(dtype, "doc"),
                     "name": fp.textwrap.shorten(for_line, 34, placeholder="…") if for_line else "not named yet",
                     "type": dtype or "type?", "deck_why": "stays in its delivery/deck/", "parts": parts},
            "job": job_of(topic), "target": target,
            "missing": [] if for_line else [("For: line", "names the one thing it hands over")]}


def draw(topic: Path) -> Path:
    kept = keep_old(topic)
    els = kept_design(topic, kept)
    wide = max((e["x"] + e["width"] for e in els), default=1300)
    shift = max(1050, int((wide - 690) * fp.GROW + 690 + fp.MOVE - 2210 + 180))   # Process sits past the Design
    out = fp.build(topic, spec_of(topic), lambda: els, shift)
    doc = json.loads(out.read_text(encoding="utf-8"))
    doc["source"] = SOURCE
    if kept:                                                     # its pictures come along with it
        doc["files"] = json.loads(kept.read_text(encoding="utf-8")).get("files") or {}
    out.write_text(json.dumps(doc, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def _phrase(text: str, words: int = 14) -> str:
    """A face's line as a slide's phrase: no markup, no (JL ...) quote, cut at a clause."""
    text = re.sub(r"\s*\((?:JL|User) \d{6}[^)]*\)", "", re.sub(r"[`*]|\[([^\]]+)\]\([^)]*\)", lambda m: m.group(1) or "", text))
    return fp.textwrap.shorten(re.split(r"(?<=[.;])\s", text.strip())[0].rstrip(".;"), words * 7, placeholder="…")


def ideas_from_face(topic: Path) -> str:
    """The sNN's ideas, one per slide, from its face (JL 261031: "could you make the slides for other studio?"): its
    question, what it hands over, what is decided, what is still open; the same shape a person's .ideas.md has."""
    text = face(topic).read_text(encoding="utf-8", errors="ignore")
    nn = topic.name.split("-")[0]
    first = text.strip().splitlines()[0] if text.strip() else topic.name
    title = re.sub(r"^#+\s*|^s\d+\s*[·:-]\s*", "", first).strip() or topic.name
    said = line_of(text, "Topic") or line_of(text, "Covers")
    bits = [_phrase(b) for b in re.split(r"(?<=[.;])\s+", re.sub(r"\s*\((?:JL|User) \d{6}[^)]*\)", "", said))
            if len(b) > 12 and not re.match(r"\s*(?:JL|User) \d{6}", b)][:3]       # a person's quote is not a point
    blocks = [(title, bits, "", "")]
    gives = line_of(text, "For")
    if gives:
        blocks.append(("What it hands over", [_phrase(gives, 18)] + ([f"a {dtype_of(text)}"] if dtype_of(text) else []), "", ""))
    decided = [_phrase(d) for d in re.findall(rf"(?m)^{nn}-D\d+\s*·\s*(.+)$", text)][:4]
    if decided:
        blocks.append(("What is decided", decided, "", ""))
    opened = re.search(r"(?ms)^Open\n-+\n(.*?)(?=^\S[^\n]*\n[-=]{3,}\n|\Z)", text)
    asks = [_phrase(a) for a in re.findall(r"(?m)^\d+\.\s+(.+)$", opened.group(1))][:4] if opened else []
    if asks:
        blocks.append(("Still open", asks[1:], "", asks[0]))
    out = [f"# {nn} · {title}: ideas", "", "The open ideas of this topic, one per slide: written from its face as a quick scratch "
           f"({TODAY}); a person edits them here, and its pictures come when asked.", ""]
    for head, points, lean, ask in blocks:
        out += [f"## {head}"] + [f"- {x}" for x in points] + ([f"leaning: {lean}"] if lean else []) + ([f"ask: {ask}"] if ask else []) + [""]
    return "\n".join(out)


def slides_from_ideas(ideas: str) -> list[dict]:
    slides = []
    for k, chunk in enumerate(re.split(r"(?m)^## ", ideas)[1:], 1):
        lines = chunk.splitlines()
        body = "\n".join(lines[1:])
        slides.append({"id": f"{k:02d}", "idea": lines[0].strip(),
                       "points": [x.strip() for x in re.findall(r"(?m)^\s*-\s+(.+)$", body)],
                       "leaning": (re.search(r"(?m)^leaning:\s*(.+)$", body) or [None, ""])[1],
                       "ask": (re.search(r"(?m)^ask:\s*(.+)$", body) or [None, ""])[1],
                       "notes": "a scratch: its words from the sNN's ideas file; its picture comes when asked"})
    return slides


def add_slides(topic: Path) -> None:
    """Its Slide deck as a quick scratch: .ideas.md from the face if it has none, .slides.json from that if it has none,
    then the deck (topic_slides.py: a card per slide without a picture). A deck with pictures is never touched."""
    ideas = topic / f"{topic.name}.ideas.md"
    if not ideas.is_file():
        ideas.write_text(ideas_from_face(topic), encoding="utf-8")
    spec = topic / f"{topic.name}.slides.json"
    if not spec.is_file():
        spec.write_text(json.dumps({"topic": topic.name, "style": "sketch-notes", "source": ideas.name,
                                    "slides": slides_from_ideas(ideas.read_text(encoding="utf-8"))}, indent=1,
                                   ensure_ascii=False) + "\n", encoding="utf-8")
    import topic_slides
    topic_slides.write(topic)


STEPS = {"stage": add_stage, "delivery": add_delivery, "render": add_delivery, "mindmap": add_mindmap, "draw": draw,
         "builder": park_builders, "slides": add_slides}
ORDER = ["stage", "delivery", "render", "mindmap", "draw", "builder", "slides"]


# ── naming: an agent's proposal, written into the face ──────────────────────────────────────────────────────────

def name(topic: Path, for_line: str, dtype: str) -> None:
    if dtype not in TYPES:
        sys.exit(f"--type must be one of {', '.join(TYPES)} (never deck: every sNN has one)")
    f = face(topic)
    text = f.read_text(encoding="utf-8")
    nn = topic.name.split("-")[0]
    if not line_of(text, "For") and for_line:
        m = re.search(r"(?m)^\*\*Stage:\*\*.*\n", text) or re.search(r"(?m)^(?:=+|-+)\n|^# .+\n", text)
        at = m.end() if m else 0
        text = text[:at] + f"\n**For:** {for_line}\n" + text[at:]
    if not dtype_of(text):
        m = re.search(r"(?ms)^\*\*For:\*\*.*?\n(?=\s*\n|\Z)", text)
        at = m.end() if m else 0
        text = text[:at] + f"\n**Delivery type:** {dtype}\n" + text[at:]
    ask = f"Agree its **For:** line and **Delivery type:** ({dtype}), proposed by the agent {TODAY}?"
    if ask not in text:
        opened = re.search(r"(?m)^Open\n-+\n|^#+ Open\b.*\n", text)
        if opened:
            rest = text[opened.end():]
            nums = [int(n) for n in re.findall(r"(?m)^(\d+)\.\s", rest.split("\n\n\n")[0])]
            text = text[:opened.end()] + (_append_open(rest, max(nums) + 1, ask) if nums else f"\n1. {ask}\n" + rest)
        else:
            text = text.rstrip("\n") + f"\n\n\nOpen\n----\n\n1. {ask}\n"
    f.write_text(text, encoding="utf-8")
    if five_part(topic / f"{topic.name}.excalidraw") and not custom_built(topic):
        draw(topic)                                              # its Idea part now shows what it hands over
    print(f"{nn}: For and Delivery type ({dtype}) written; an Open point asks a person to agree them")


def brief(root: Path) -> None:
    """What an agent needs to name each sNN that has no For: or no Delivery type: its title, Topic, Covers and what
    its delivery/ and folder hold, a few lines each."""
    for t in topics(root):
        text = face(t).read_text(encoding="utf-8", errors="ignore")
        if line_of(text, "For") and dtype_of(text):
            continue
        first = text.strip().splitlines()[0] if text.strip() else t.name
        held = sorted(q.name for q in t.iterdir() if not q.name.startswith(".") and q.name != face(t).name)[:12]
        print(f"## {t}\ntitle: {first}")
        for key in ("For", "Covers", "Topic"):
            v = line_of(text, key)
            if v:
                print(f"{key}: {fp.textwrap.shorten(v, 420, placeholder='...')}")
        print(f"holds: {', '.join(held)}\n")


def name_batch(path: Path) -> None:
    """Many proposals at once: a JSON list of {"topic": <sNN folder>, "for": "<For line>", "type": "<type>"}."""
    for row in json.loads(path.read_text(encoding="utf-8")):
        try:
            name(Path(row["topic"]).resolve(), row.get("for", "").strip(), row["type"].strip().lower())
        except (SystemExit, Exception) as err:                   # one bad row never stops the rest
            print(f"\u2757 {row.get('topic')}: {err}")


def _append_open(rest: str, n: int, ask: str) -> str:
    """Put the new point after the last numbered point of the Open part."""
    lines = rest.split("\n")
    last = max((i for i, ln in enumerate(lines) if re.match(r"^\d+\.\s", ln)), default=-1)
    stop = next((i for i in range(last + 1, len(lines)) if lines[i].strip() == "" or re.match(r"^\d+\.\s", lines[i])), len(lines))
    lines.insert(stop, f"{n}. {ask}")
    return "\n".join(lines)


# ── the commands ─────────────────────────────────────────────────────────────────────────────────────────────────

def report(root: Path, apply: bool, plan: bool) -> int:
    found = topics(root)
    counts = level_counts(found)
    tally = collections.Counter()
    for t in found:
        rel = os.path.relpath(t, root) if t != root else t.name
        miss = checks(t, counts)
        tally.update(key for _, key, _ in miss)
        if not miss:
            print(f"✅ {rel}")
            continue
        mark = {"apply": "⬜", "person": "\U0001f64b", "move": "⬜"}
        print(f"{rel}  " + " · ".join(f"{mark[k]} {w}" for k, _, w in miss))
        if plan or apply:
            todo = [key for kind, key, _ in miss if kind == "apply"]
            for key in [k for k in ORDER if k in todo]:
                if key == "render" and "delivery" in todo:
                    continue
                if apply:
                    try:
                        STEPS[key](t)
                        print(f"    ✅ {key}")
                    except (Exception, SystemExit) as err:         # one sNN's trouble never stops the rest
                        print(f"    ❗ {key}: {type(err).__name__}: {err}")
                else:
                    print(f"    would {key}")
    print(f"\n{len(found)} sNN; missing before this run: " + ", ".join(f"{k} {v}" for k, v in tally.most_common()) if tally else
          f"\n{len(found)} sNN, all meet today's rules")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("audit"); a.add_argument("path", type=Path)
    u = sub.add_parser("update"); u.add_argument("path", type=Path); u.add_argument("--apply", action="store_true")
    n = sub.add_parser("name"); n.add_argument("topic", type=Path); n.add_argument("--for", dest="for_line", default="")
    n.add_argument("--type", dest="dtype", required=True)
    b = sub.add_parser("brief"); b.add_argument("path", type=Path)
    nb = sub.add_parser("name-batch"); nb.add_argument("json", type=Path)
    args = ap.parse_args(argv)
    if args.cmd == "brief":
        brief(args.path)
        return 0
    if args.cmd == "name-batch":
        name_batch(args.json)
        return 0
    if args.cmd == "name":
        name(args.topic.resolve(), args.for_line.strip(), args.dtype.strip().lower())
        return 0
    return report(args.path, args.cmd == "update" and args.apply, args.cmd == "update")


if __name__ == "__main__":
    raise SystemExit(main())
