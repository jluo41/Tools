"""A Block's s00, the background and index: what the Block stands on, and every studio topic and Job with its
progress, drawn as folder trees (JL 261012: "for every block, we also want to have the s00-background-and-index to
show the background information, and what are the sNN and jNN and what are the progress of them"; "我个人更 prefer
那种 tree 结构，就像 folder tree 那样"; "如果有 background，大概三个 frame 就差不多了").

    python block_index.py <block> ...                 print each index as a folder tree
    python block_index.py <block> ... --draw          draw studio/s00-background-and-index/ and its preview
    python block_index.py --all <root> [--draw]       every Block under <root>; archives, history and _-folders skipped

Three frames at most, read left to right (haipipe-studio, The look):

    Background   the face's `background:` yaml, one frame per entry, two at most: what the Block stands on, written
                 by a person. A Block without the face gets one, its background seeded from the Block's own face.
    Index        read from disk on every build, never typed: the Block's face (title, state, status), each studio
                 topic's face (its Stage, its decisions, its Open list) and its Run's passes, each Job's face (state,
                 waiting-on, since, next) with its Tasks and their states, the Questions in reports/,
                 related/related.md and the files in delivery/.

A face that says something old shows it old: the index does not correct it. It reads every file but the s00 face
(written once, when missing) and the s00 drawing, which it writes.
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import canvas  # noqa: E402
from topic_map import PAD, draw_frame, draw_map  # noqa: E402  (the drawing: trees, boxes and arrows)

S00 = "s00-background-and-index"
FIELD = re.compile(r"(?m)^([a-z][a-z0-9_-]*):[ \t]*(\S.*)$")
BLOCK = re.compile(r"^b\d\d_")
SKIP = {"history", "archive", "node_modules", "tests", "fixture", "fixtures"}   # never a Block's home; nor .x or _x
BG_MIN = 90                                            # words a background needs to be a frame of its own
STAGES = ("explore", "shaping", "agreed", "closed", "no stage")   # a topic's walk (servers/workbench/frame.py)
MOST_TASK_LINES = 40                                   # past this, a Job shows its Tasks' tally, not each Task
MOST_TASKS, MOST_ITEMS = 8, 6                          # a Job's Tasks, a related kind's or delivery's items
# excalidraw-studio's principles where they fit s00's own shape (JL 261012, through b31-s01): each frame's key point on
# the one slight colour (principle 5), and the frames as acts, a row each, named at the left, a named arrow for each
# step (principle 3). The frames themselves keep s00's shape: its trees, boxes, emoji, plan and proposals.
KEY = canvas.KEY                                       # the one slight colour, kept by canvas.write
SLIDE = 2560 * 1440 / 3                                # under this a frame reads as a slide (excalidraw-studio ①):
                                                       # a background that small is merged into the index, not padded
EXCALIDRAW_STUDIO = HERE.parents[2] / "excalidraw" / "excalidraw-studio" / "scripts"


EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u270D\u270F-\u27BF\u2B00-\u2BFF\u2300-\u23FF\uFE0F\u200D\u20E3]")
CJK = "\u2E80-\u9FFF\uAC00-\uD7AF\uF900-\uFAFF\uFF00-\uFFEF"   # a wide character: a line may break before it


def plain(s: str) -> str:
    """Markdown marks and emoji out (the drawing puts its own); every letter stays, Chinese included."""
    s = re.sub(r"\*\*|`|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or "", s)
    return re.sub(r"\s+", " ", EMOJI.sub("", s)).strip()


def first_sentence(s: str, cap: int = 150) -> str:
    s = plain(s)
    m = re.match(r"(.+?(?:[.;](?:\s|$)|[。；]))", s)
    s = m.group(1).strip() if m and len(m.group(1)) > 12 else s
    if len(s) <= cap:
        return s
    cut = s[:cap]
    return (cut.rsplit(" ", 1)[0] if " " in cut[-25:] else cut) + " …"


def section(text: str, name: str) -> str:
    """The body of a face section headed `name` and underlined with dashes."""
    m = re.search(rf"(?ms)^{re.escape(name)}\n-{{3,}}\n(.*?)(?=^\S[^\n]*\n[-=]{{3,}}\n|\Z)", text)
    return m.group(1) if m else ""


def open_items(text: str) -> list[str]:
    """The Open list's numbered items still open: an item saying it was answered or done is left out."""
    items = re.findall(r"(?ms)^\s*\d+\.\s+(.+?)(?=^\s*\d+\.\s|^\(write here|\Z)", section(text, "Open"))
    closed = re.compile(r"(?i)\b(answered|done|settled|decided|applied|resolved|closed)\b")
    return [plain(i) for i in items if not closed.search(i[:60]) and ": done" not in i]


def qnums(text: str) -> list[str]:
    """The Question numbers a line names: q05_skill_per_level, Q05 or QK10.E1's 10 are all "05"/"10"."""
    return sorted(set(re.findall(r"(?<![A-Za-z0-9])[qQ][A-Z]?(\d\d)(?!\d)", text)))


def face_of(folder: Path) -> Path | None:
    for name in (f"{folder.name}.md", "board.md"):
        if (folder / name).is_file():
            return folder / name
    return None


def read(path: Path | None) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path and path.is_file() else ""


def title_of(text: str, default: str) -> str:
    """A face's title: its `# ` line, or a line underlined with `=`; the part after its first ·."""
    lines = text.splitlines()[:40]
    for i, ln in enumerate(lines):
        if ln.startswith("# ") or (ln.strip() and i + 1 < len(lines) and re.fullmatch(r"={3,}", lines[i + 1].strip())):
            return plain(ln.lstrip("# ").split("·", 1)[-1])
    return default


def state_word(state: str) -> str:
    """A Task's state as one of five words, whatever its face spells: done · active · partly · open · dropped. Only
    the head counts, before its first · or ; ("🟡 PARTIAL · r03 done" is partly)."""
    s = re.split(r"[·;]", state.lower(), maxsplit=1)[0]
    if not s.strip():
        return "no state"
    if re.search(r"dropped|retired|superseded|cancel", s):
        return "dropped"
    if re.search(r"running|active|🔄|🔶", s):
        return "active"
    if re.search(r"done|validated|settled|kept|closed|sent|answered|agreed|✅|🟢", s):
        return "done"
    if re.search(r"open|planned|missing|expected|todo|⬜|🔴", s):
        return "open"
    if re.search(r"partial|ready|draft|shape|writing|🟡", s):
        return "partly"
    return "open"


def topic_row(block: Path, folder: Path) -> dict:
    text = read(folder / f"{folder.name}.md")
    nn = re.match(r"s\d+", folder.name).group(0)
    stage = re.search(r"\*\*Stage:\*\*\s*`?(\w+)", text)
    topic = re.search(r"(?s)\*\*Topic:\*\*\s*(.+?)(?:\n\s*\n|\Z)", text)
    feeds = re.search(r"(?s)\*\*Feeds:\*\*(.+?)(?:\n\s*\n|\Z)", text)
    tags = re.search(r"(?m)^\*\*(?:Tags|Type):\*\*[^\S\n]*(.*)$", text)
    passes = sorted(p.name for p in (block / "runs" / f"run-draw-{nn}" / "passes").glob("p*") if p.is_dir())
    last = re.search(r"-(\d\d)(\d\d)$", passes[-1]) if passes else None
    return {"nn": nn, "name": folder.name, "path": folder, "title": title_of(text, folder.name),
            "stage": stage.group(1).lower() if stage else "no stage",
            "topic": first_sentence(topic.group(1)) if topic else "", "open": open_items(text),
            "topic_long": first_sentence(topic.group(1), 600) if topic else "",   # for a wide index (`index: width`)
            "decided": len(re.findall(r"(?m)^s\d\d-D\d+", text)), "passes": len(passes),
            "feeds": qnums(feeds.group(1)) if feeds else [],
            "tags": [t.strip(" `") for t in re.split(r"[,·|]", tags.group(1)) if t.strip(" `")] if tags else [],
            "last": f"{last.group(1)}-{last.group(2)}" if last else ""}


def runs_count(folder: Path) -> int:
    rdir = folder / "runs"
    return sum(1 for p in rdir.iterdir() if not p.name.startswith((".", "_")) and p.name != "README.md") \
        if rdir.is_dir() else 0


def job_row(folder: Path) -> dict:
    text = read(face_of(folder))
    f = {k: v.strip() for k, v in FIELD.findall(text[:1500])}
    timeline = folder / "Timeline.md"
    dates = re.findall(r"(?m)^(\d{4}-\d\d-\d\d)", read(timeline))
    tasks, answers = [], qnums(" ".join(re.findall(r"(?m)^answers:[ \t]*(.+)$", text)))
    for t in sorted(p for p in folder.glob("t[0-9][0-9]_*") if p.is_dir()):
        tt = read(face_of(t))
        answers += qnums(" ".join(re.findall(r"(?m)^answers:[ \t]*(.+)$", tt)))
        state = {k: v.strip() for k, v in FIELD.findall(tt[:1500])}.get("state", "")
        tasks.append({"nn": t.name.split("_", 1)[0], "title": title_of(tt, t.name.split("_", 1)[-1].replace("_", " ")),
                      "state": plain(state), "word": state_word(state), "runs": runs_count(t)})
    topics = sorted(p.name for p in (folder / "studio").glob("s[0-9][0-9]*") if p.is_dir())
    steps = re.findall(r"(?m)^\s*[-*] \[([ xX])\]", read(folder / "CHECKLIST.md"))
    return {"nn": folder.name.split("_", 1)[0], "path": folder, "title": title_of(text, folder.name),
            "close": plain(f.get("close", "")), "goal": plain(f.get("goal", "")),
            "output": plain(f.get("output", "") or f.get("delivers", "")),
            "steps": (sum(c.lower() == "x" for c in steps), len(steps)),
            "state": plain(f.get("state", "") or f.get("goal", "") and "goal: " + f["goal"] or "no state"),
            "waiting": plain(f.get("waiting-on", "")), "since": f.get("since", ""),
            "next": first_sentence(f.get("next", ""), 170), "tasks": tasks, "topics": topics,
            "answers": sorted(set(answers)),
            "runs": runs_count(folder) + sum(t["runs"] for t in tasks), "last": max(dates) if dates else ""}


def read_block(block: Path) -> dict:
    text = read(face_of(block))
    f = {k: v.strip() for k, v in FIELD.findall(text[:3000])}
    studio = block / "studio"
    topics = [topic_row(block, d) for d in sorted(studio.glob("s[0-9][0-9]*"))
              if d.is_dir() and d.name != S00] if studio.is_dir() else []
    jobs = [job_row(d) for d in sorted(block.glob("j[0-9][0-9]_*")) if d.is_dir()]
    questions = []
    for q in sorted(p for p in (block / "reports").glob("q[0-9][0-9]_*") if p.is_dir()):
        qt = read(q / f"{q.name}.md")
        st = re.search(r"(?m)^answer-status:\s*(\S+)", qt)
        questions.append({"nn": q.name, "num": q.name[1:3], "title": title_of(qt, ""),
                          "status": st.group(1).strip() if st else "open"})
    related = []
    rel = block / "related" / "related.md"
    if rel.is_file():
        rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in read(rel).splitlines()
                if ln.startswith("|") and not set(ln.replace("|", "").strip()) <= set("-: ")]
        head = [c.lower() for c in rows[0]] if rows else []
        for r in rows[1:]:
            d = dict(zip(head, r))
            related.append({"kind": d.get("kind", ""), "date": d.get("date", ""),
                            "item": plain(d.get("item", "")).split(":", 1)[0][:90]})
    deliv = block / "delivery"
    files = sorted(p.relative_to(deliv).as_posix() for p in deliv.rglob("*")
                   if p.is_file() and not p.name.startswith(".") and not p.name.endswith(".py")
                   and not {"history", "__pycache__"} & set(p.relative_to(deliv).parts)) if deliv.is_dir() else []
    order = [ln.strip() for ln in read(studio / "_groups.txt").splitlines() if ln.strip() and not ln.startswith("#")]
    return {"name": block.name, "title": title_of(text, block.name), "state": plain(f.get("state", "")), "groups": order,
            "owner": f.get("owner", ""), "spine": plain(f.get("spine", "")), "close": plain(f.get("close", "")),
            "status": plain(f.get("status", "")), "topics": topics, "jobs": jobs, "questions": questions,
            "related": related, "delivery": files}


# an emoji in front of each node, so the tree reads at a glance (JL 261012: "it is not that vivid, I think for the
# studio tree like things, you can also add the things like the emoji"); the same marks as a reply's sketch
MARK = {"done": "✅", "active": "🏃", "partly": "🔶", "open": "⬜", "dropped": "🗑", "no state": "▫️",
        "explore": "🌱", "shaping": "🔶", "agreed": "✅", "closed": "🔒", "no stage": "▫️",
        "answered": "✅", "partial": "🔶"}
THING = {"read": "📖", "studio": "🧠", "job": "🧱", "tasks": "📋", "reports": "📝", "related": "📥", "delivery": "📤",
         "next": "👉", "waiting": "⏳", "timeline": "🕒", "file": "📄"}


def mark(word: str) -> str:
    return MARK.get(word, "▫️")


def tally(words, order=("done", "active", "partly", "open", "dropped", "no state")) -> str:
    words = list(words)
    n = {w: words.count(w) for w in order}
    return " · ".join(f"{mark(w)} {n[w]} {w}" for w in order if n[w])


def capped(items: list, most: int) -> list:
    return items[:most] + ([f"… and {len(items) - most} more"] if len(items) > most else [])


def group_emoji(label: str) -> str:
    """The emoji the workbench's group bar shows for this group (servers/workbench/frame.py group_emoji)."""
    try:
        sys.path.insert(0, str(HERE.parents[4] / "servers" / "_host"))
        from host_paths import bootstrap
        bootstrap()
        from live import frame
        return frame.group_emoji(label)
    except Exception:  # the drawing still reads without the server's table
        return "▫️"


def topic_groups(b: dict) -> list:
    """(label, topics): the Studio's own groups, as the workbench's group bar shows them (JL 261012: "what is the
    rational you grouping these stadio items?"). A topic sits under its first tag, the groups in studio/_groups.txt
    order, then any other tag, then Untagged; its other tags ride on its line."""
    first = lambda t: t["tags"][0] if t["tags"] else "Untagged"
    order = list(b["groups"])
    for t in b["topics"]:
        if first(t) not in order:
            order.append(first(t))
    out = []
    for g in order:
        ts = [t for t in b["topics"] if first(t) == g]
        if ts:
            out.append((f"{group_emoji(g) if g != 'Untagged' else '▫️'} {g}", ts))   # no counts: they go stale
    return out


def also(t: dict) -> str:
    return " (+" + ", ".join(t["tags"][1:]) + ")" if len(t["tags"]) > 1 else ""


def index_tree(b: dict) -> list:
    """The index as tree nodes: how to read it, the studio topics by band, each Job with its Tasks, the Questions,
    related and delivery; each node led by its emoji."""
    def topic(t):                                       # what it is for, and where it leads
        kids = [first_sentence(t["topic"], 130)] if t["topic"] else []
        kids += ["→ " + " · ".join(f"Q{q}" for q in t["feeds"])] if t["feeds"] else []
        return {f"{mark(t['stage'])} {t['nn']} · {t['title']}": kids}

    def job(j):
        line = f"{mark(state_word(j['state']))} {first_sentence(j['state'], 120)}" + \
            (f" · {THING['waiting']} waiting on {j['waiting']}" if j["waiting"] else "") + \
            (f" · since {j['since']}" if j["since"] else "")
        kids = [line] + ([f"{THING['next']} next: {j['next']}"] if j["next"] else [])
        if j["tasks"]:
            rows = [f"{mark(t['word'])} {t['nn']} · {t['title']} · {t['state'] or 'no state'}" for t in j["tasks"]]
            count = f"{THING['tasks']} {len(j['tasks'])} Tasks: {tally(t['word'] for t in j['tasks'])} · {j['runs']} Runs"
            kids.append({count: capped(rows, MOST_TASKS)} if many_tasks <= MOST_TASK_LINES else count)
        if j["topics"]:
            kids.append(f"{THING['studio']} its own studio: " + ", ".join(j["topics"]))
        if j["last"]:
            kids.append(f"{THING['timeline']} Timeline, last {j['last']}")
        return {f"{THING['job']} {j['nn']} · {j['title']}": kids}

    many_tasks = sum(min(len(j["tasks"]), MOST_TASKS + 1) for j in b["jobs"])
    nodes = [{f"{THING['read']} How to read it": [
        f"{THING['studio']} studio/sNN · a topic we think on, one drawing each; its stage walks "
        "🌱 explore → 🔶 shaping → ✅ agreed → 🔒 closed",
        f"{THING['job']} jNN · a Job, one piece of work; its Tasks tNN are the steps (✅ done · 🏃 active · 🔶 partly · "
        "⬜ open), and a Task's Runs are what was executed",
        f"{THING['reports']} reports/qNN · the Block's Questions, each ⬜ open → 🔶 partial → ✅ answered",
        f"{THING['related']} related/ came in from outside; {THING['delivery']} delivery/ is what leaves the Block",
        "❓ red · still open (the first open point of a topic's face)"]}]
    for label, ts in topic_groups(b):
        nodes.append({f"{THING['studio']} studio/ {label}": [topic(t) for t in ts]})
    if not b["topics"]:
        nodes.append({f"{THING['studio']} studio/ · 0 topics": ["❓ no topic yet"]})
    nodes += [job(j) for j in b["jobs"]] or [{f"{THING['job']} Jobs · 0": ["no Job yet: work starts as a Job, jNN_<job>/"]}]
    qs = b["questions"]
    nodes.append({f"{THING['reports']} reports/ · {len(qs)} Questions" + (f": {tally_status(qs)}" if qs else ""):
                  [f"{mark(q['status'])} {q['nn']} · {q['status']}" + (f" · {q['title']}" if q["title"] else "")
                   for q in qs] or ["none yet: a Question opens when work needs one answer"]})
    kinds = {}
    for r in b["related"]:
        kinds.setdefault(r["kind"] or "item", []).append(f"{r['date']} · {r['item']}")
    nodes.append({f"{THING['related']} related/ · {len(b['related'])}":
                  [{f"{k} · {len(v)}": capped(v, MOST_ITEMS)} for k, v in kinds.items()] or ["nothing yet"]})
    nodes.append({f"{THING['delivery']} delivery/ · {len(b['delivery'])} files":
                  capped([f"{THING['file']} {f}" for f in b["delivery"]], MOST_ITEMS * 2) or ["nothing built yet"]})
    return nodes


def tally_status(qs) -> str:
    n = {}
    for q in qs:
        n[q["status"]] = n.get(q["status"], 0) + 1
    return " · ".join(f"{mark(k)} {v} {k}" for k, v in n.items())


def print_tree(nodes, depth=0):
    for n in nodes:
        label, kids = canvas._tree_node(n)
        print("    " * depth + ("├── " if depth else "") + label)
        print_tree(kids, depth + 1)


# ── the face, written once ─────────────────────────────────────────────────────────────────────────────────────
FACE = """s00 · Background and index
==========================

**Stage:** shaping
{tags}
**Topic:** what this Block stands on, for a reader new to it, and an index of its studio topics (sNN), Jobs (jNN)
and Questions (qNN) with how far each has come. The background is the yaml below, written by a person; the index
is read from disk on every build (JL {today}: "for every block, we also want to have the s00-background-and-index").

**Feeds:** none; it indexes the whole Block.


Files
-----

```text
s00-background-and-index/
├── s00-background-and-index.md          this face; its yaml is the Background frame
├── s00-background-and-index.excalidraw  the drawing: Background, then Index; a person's marks are kept
├── build_s00_background_and_index.py  rebuild using the current shared Tools generator
└── s00-background-and-index.png         its preview
```

Rebuild: `python <haipipe-studio>/scripts/block_index.py <this Block> --draw`, haipipe-studio being
`Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/`.


Background
----------

One frame per entry, two at most, each a folder tree: a string is a leaf, `{{label: [children]}}` a branch; an emoji
leads each node (🧭 📖 🎯 🧱 …), and a leaf that starts with "❓" is still open and draws red. Without an `intro`, the
first frame opens with the Block's spine.

```yaml
{yaml}```


Open
----

1. The background was seeded from the Block's face on {today}: a person rewrites it as the tree a newcomer needs.

(write here, or mark the drawing in red)
"""


def prose(text: str, most: int = 4) -> list[str]:
    """The first sentences of the face's prose: past its header fields, outside fences, tables and headings."""
    out, fence = [], False
    for ln in text.splitlines()[1:]:
        s = ln.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence or not s or s.startswith(("#", "|", "<", ">", "**")) or re.fullmatch(r"[-=]{3,}", s) \
                or FIELD.match(s) or re.match(r"^(Owner|Last updated)\b", s):
            continue
        out.append(re.sub(r"^[-*\d.]+\s+", "", s))
        if sum(len(re.findall(r"[.!?](?:\s|$)", x)) for x in out) >= most:
            break
    sentences = re.split(r"(?<=[.!?])\s+", plain(" ".join(out)))
    return [first_sentence(x, 220) for x in sentences if len(x) > 20][:most]


def seed_face(block: Path, b: dict) -> str:
    import yaml
    tree = []
    if b["close"]:
        tree.append({"🎯 Done when": [first_sentence(b["close"], 260)]})
    said = prose(read(face_of(block)))
    if said:
        tree.append({"📖 What it is about": said})
    tree.append("❓ Seeded from the Block's face: rewrite it as the tree a newcomer needs")
    data = {"background": [{"title": "🧭 What this Block stands on", "cols": 2, "tree": tree}]}
    siblings = " ".join(read(p) for p in (block / "studio").glob("s*/s*.md"))
    tags = "\n**Tags:** `Structure`\n" if re.search(r"(?m)^\*\*Tags:\*\*.*\bStructure\b", siblings) else ""
    return FACE.format(tags=tags, today=datetime.date.today().isoformat(),
                       yaml=yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110))


# ── drawing ────────────────────────────────────────────────────────────────────────────────────────────────────
def words(node) -> int:
    """The words in a background entry or a tree node, all the way down."""
    if isinstance(node, str):
        return len(node.split())
    if isinstance(node, dict):
        return sum(words(k) + words(v) for k, v in node.items() if k not in ("cols", "notes"))
    if isinstance(node, list):
        return sum(words(n) for n in node)
    return 0


def background_of(face: Path) -> list:
    import yaml
    m = re.search(r"```yaml\n(background:.*?)\n```", read(face), re.S)
    return (yaml.safe_load(m.group(1)) or {}).get("background") or [] if m else []


# ── the index: a mind map read left to right (JL 261012, on b32 EB1A's background index: "for the index, I love this
# type of things"; "This type of the tree"; "This is more like the mindmap, right?") ──────────────────────────────
#     🎯 Block ─thinks in─▶ 🧠 Studio ─▶ each topic: what it is about ──────▶ 📝 the Questions it feeds
#              └works in──▶ 🧱 Jobs   ─▶ each Job: state · steps · next ─▶ 🏁 what it must deliver
X_ROOT, W_ROOT = 40, 440                               # the Block, and its why and done-when under it
X_CAT, W_CAT = 660, 300                                # the two branches (room before them for "thinks in")
X_SPINE, X_ITEM, W_ITEM = 1120, 1160, 900              # each topic and Job, a box each; one column at most this wide
COLW, COL_GAP = 480, 80                                # a box when the items flow into columns, and the room between
INDEX_TALL = 2400                                      # the index may run taller than a screen (JL 261012: "you can
                                                       # make the frame to be larger"; "also too crowed, the content")
X_OUT_GAP, W_OUT = 140, 480                            # what each leads to, right of a single column
BOX_PAD, BOX_GAP = 18, 34
MM_W = 2560
_COLUMNS = ("X_CAT", "W_CAT", "X_SPINE", "X_ITEM", "W_ITEM", "X_OUT_GAP", "W_OUT", "W_ROOT", "MM_W", "WIDE")
WIDE = 1                                               # how much wider than usual a face asked its index to be


def widen(width) -> dict:
    """A face's `index: width:` (JL 261013 on b01_irb: "could you make the index's draw as wide as this", s03 beside
    it, 5,932 px): every column of the index scaled so its frame is that wide, the words' sizes kept, each box as wide
    as its column. Only a face that asks for it; returns the old values for `narrow`."""
    old = {k: globals()[k] for k in _COLUMNS}
    natural = X_ITEM + W_ITEM + X_OUT_GAP + W_OUT + 40
    if width and int(width) > natural:
        k = int(width) / natural
        globals().update({n: round(v * k) for n, v in old.items() if n != "WIDE"}, WIDE=k)
    return old


def narrow(old: dict) -> None:
    globals().update(old)
# each level a clearly different size, largest first (JL 261012: "focus on the s00, make sure the font size to be
# differentiated"): the frame's title, the Block, a branch, an item, a heading or group, what it leads to, a detail
SIZE = {"title": 60, "root": 44, "cat": 38, "name": 30, "head": 26, "out": 22, "line": 20, "note": 20, "small": 20,
        "sub": 24}
_FONT_FILE, _fonts = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf", {}


def measure(s: str, size: int) -> float:
    """A line's width in px, as Excalidraw's Nunito draws it (Arial measured, a little wider)."""
    try:
        from PIL import ImageFont
        if size not in _fonts:
            _fonts[size] = ImageFont.truetype(_FONT_FILE, size)
        return _fonts[size].getlength(s) * 1.06
    except Exception:  # no font file: the estimate the tree uses
        return len(s) * size * 0.56


def wrap(s: str, size: int, width: float) -> list:
    """Lines no wider than `width`: break at a space, before any Chinese character, and inside a word too long for
    a line."""
    lines = []
    for para in str(s).split("\n"):
        line = ""
        for tok in re.findall(rf"[{CJK}]|[^\s{CJK}]+|\s+", para):
            if measure(line + tok, size) <= width or not line.strip():
                line += tok
            else:
                lines.append(line.rstrip())
                line = tok.lstrip()
            while measure(line, size) > width and len(line) > 1:      # one word wider than the line
                k = len(line) - 1
                while k > 1 and measure(line[:k], size) > width:
                    k -= 1
                lines.append(line[:k])
                line = line[k:]
        lines.append(line.rstrip())
    return lines


def _text(out, fid, x, y, s, size, width, color=None) -> dict:
    lines = wrap(s, size, width)
    body = "\n".join(lines)
    color = color or (canvas.RED if body.startswith(("?", "❓")) else canvas.GREEN if body.startswith("✎") else canvas.INK)
    e = canvas._tree_base("text", x, y, max(measure(ln, size) for ln in lines) + 4, len(lines) * size * 1.25, fid,
                          strokeColor=color, strokeWidth=1, text=body, originalText=body, fontSize=size,
                          fontFamily=canvas.FONT, textAlign="left", verticalAlign="top", containerId=None,
                          autoResize=True, lineHeight=1.25)
    out.append(e)
    return e


def _line(out, fid, pts, arrow=False, dashed=False, color=None) -> None:
    x0, y0 = pts[0]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    out.append(canvas._tree_base("arrow" if arrow else "line", x0, y0, max(1, max(xs) - min(xs)), max(1, max(ys) - min(ys)),
                                 fid, strokeColor=color or canvas.INK, strokeWidth=2,
                                 strokeStyle="dashed" if dashed else "solid",
                                 points=[[px - x0, py - y0] for px, py in pts], lastCommittedPoint=None,
                                 startBinding=None, endBinding=None, startArrowhead=None,
                                 endArrowhead="arrow" if arrow else None))


def plan_of(face: Path) -> dict:
    """The face's optional `index:` yaml, a person's words where a face says nothing: first (where to start),
    boundary, open (a list), tasks (expand Task names and states), jobs {jNN: {label, finish, action}},
    topics {sNN: note}, width (the index frame's width in px, its columns and words per box scaled to it; `widen`)."""
    import yaml
    m = re.search(r"```yaml\n(index:.*?)\n```", read(face), re.S)
    return (yaml.safe_load(m.group(1)) or {}).get("index") or {} if m else {}


def flat(node) -> list:
    """A background tree as lines: a branch with its leaves joined."""
    if isinstance(node, str):
        return [node]
    if isinstance(node, dict):
        return [f"{k}: " + "; ".join(x for v in vs for x in flat(v)) if isinstance(vs, list) else f"{k}: {vs}"
                for k, vs in node.items()]
    return []


def proposed(b: dict, face: Path) -> tuple[list, list]:
    """The face's proposed topics (`studio_proposals`) and Jobs (`job_proposals`) whose folder is not made yet (JL
    261012: "s00 should also work in a way for the proposing the sNN and jNN as well"). A topic is made once any
    sNN-* folder holds its number; a Job once its jNN_<slug>/ exists. A Job number another folder already holds is
    flagged, never drawn over."""
    made_t = {t["nn"] for t in b["topics"]}
    made_j = {j["path"].name: j for j in b["jobs"]}
    topics = [p for p in yaml_block(face, "studio_proposals") or [] if isinstance(p, dict) and p.get("id")
              and p["id"] not in made_t]
    jobs = []
    for p in yaml_block(face, "job_proposals") or []:
        if not isinstance(p, dict) or not p.get("id"):
            continue
        folder = f"{p['id']}_{p['slug']}" if p.get("slug") else p["id"]
        if folder in made_j:
            continue
        taken = next((n for n in made_j if n.split("_", 1)[0] == p["id"]), "")
        jobs.append(dict(p, folder=folder, taken=taken))
    return topics, jobs


def mind_map(b: dict, block: Path, plan: dict, folded: list, detail: int = 2, cols: int = 1,
             props: tuple = ((), ())) -> list:
    """The index frame's elements: the Block, two branches, and each topic and Job in a box of its own saying what it
    is for and where it leads (JL 261012: "I want to focus on eahc item ... the studio item and job item should have
    the box as well"; no counts, they go stale). One column: what each leads to sits right of its box, joined by an
    arrow. `cols` 2 or 3: the boxes flow into columns and carry it on their last line. `detail` 2, 1, 0: shorter
    purposes, no next step. `props`, from `proposed()`: the topics and Jobs proposed but not made; they are drawn in
    their own frame (`proposals_frame`), so the index holds what is on disk and names them in one red line."""
    fid, out = "frame-s00-index", []
    f = canvas.reads_down(canvas._tree_base("frame", 0, 0, MM_W, 100, None, id=fid,
                                            name=f"s00 · {b['name']} · the index", customData={"map": True}))
    out.append(f)
    top = 24 + SIZE["title"] * 1.25 + 60
    pj, pt, unsaid = plan.get("jobs") or {}, plan.get("topics") or {}, []
    fed = {}
    for t in b["topics"]:
        for q in t["feeds"]:
            fed.setdefault(q, []).append(t["nn"])
    answered = {q for j in b["jobs"] for q in j["answers"]}
    qtitle = {q["num"]: q["title"] for q in b["questions"]}
    inside = cols > 1
    cap = round((130, 95, 70)[2 - detail] * WIDE)       # a wider index says more of each purpose

    def topic_item(t):
        purpose = pt.get(t["nn"]) or (t.get("topic_long") if WIDE > 1 else t["topic"])
        feeds = t["feeds"]
        leads = None
        if feeds:
            leads = (f"📝 Q{feeds[0]} · {qtitle.get(feeds[0], '')}".rstrip(" ·") if len(feeds) == 1
                     else "📝 " + " · ".join(f"Q{q}" for q in feeds))
        lines = [(first_sentence(purpose, cap), "line")] if purpose else []
        if inside and leads:
            lines.append(("→ " + leads, "small"))
        return {"name": f"{mark(t['stage'])} {t['nn']} · {t['title']}", "lines": lines,
                "out": None if inside else leads, "dashed": False}

    def job_item(j):
        p = pj.get(j["nn"]) or {}
        done = sum(t["word"] == "done" for t in j["tasks"])
        steps = (f"steps {j['steps'][0]}/{j['steps'][1]}" if j["steps"][1] else
                 "" if plan.get("tasks") else
                 f"Tasks {done}/{len(j['tasks'])} done" if j["tasks"] else "no Task yet")
        state = f"{mark(state_word(j['state']))} {first_sentence(j['state'], 40)}" + \
            (f" · {steps}" if steps else "") + \
            (f" · waiting: {first_sentence(j['waiting'], 30)}" if j["waiting"] else "")
        nxt = p.get("action") or j["next"]
        finish = p.get("finish") or j["output"] or next((x for x in (j["close"], j["goal"]) if x and x.lower() != "open"), "")
        answers = " → " + " ".join(f"Q{q}" for q in j["answers"]) if j["answers"] else ""
        leads = ("🏁 " + first_sentence(finish, 110 if not inside else 80) + answers) if finish else \
            ("📝" + answers if answers else None)
        if not finish:
            unsaid.append(j["nn"])
        lines = [(state, "line")]
        if plan.get("tasks"):
            for t in j["tasks"]:
                lines += [(f"↳ {mark(t['word'])} {t['nn']} · {t['title']}", "line"),
                          (f"state: {t['state'] or 'not recorded'}", "small")]
            if not j["tasks"]:
                lines.append(("no Task yet", "small"))
        if detail == 2 and nxt:
            lines.append((f"{THING['next']} next: {first_sentence(nxt, cap)}", "line"))
        if inside and leads:
            lines.append(("→ " + leads, "small"))
        hold = bool(re.search(r"hold|⏸|paused|blocked|dropped|retired", j["state"].lower()))
        return {"name": f"{THING['job']} {j['nn']} · {p.get('label') or j['title']}", "lines": lines,
                "out": None if inside else leads, "dashed": hold}

    ptopics, pjobs = props
    pnote = lambda ids: ("label", f"❓ proposed, not made yet: {' · '.join(ids)} (see 💡 what we propose next)")
    srows = []
    groups = topic_groups(b)
    for label, ts in groups:
        if len(groups) > 1:
            srows.append(("label", label))
        srows += [("item", topic_item(t)) for t in ts]
    if not srows and not ptopics:
        srows = [("label", "❓ no topic yet: a topic is where the Block thinks before it works")]
    srows += [pnote([p["id"] for p in ptopics])] if ptopics else []
    jrows = [("item", job_item(j)) for j in b["jobs"]] or \
        [("label", "no Job yet: work starts as a Job, jNN_<job>/, built from an agreed topic")]
    jrows += [pnote([p["folder"] for p in pjobs])] if pjobs else []

    def inner(it, w):
        tw = w - 2 * BOX_PAD
        return [(it["name"], "name")] + list(it["lines"]), tw

    if inside:
        bw = COLW
    else:
        widest = max([measure(x, SIZE[k]) for _, it in srows + jrows if _ == "item" for x, k in inner(it, 0)[0]] + [0])
        bw = W_ITEM if plan.get("width") else min(W_ITEM, max(460, widest + 2 * BOX_PAD + 10))
    x_out = X_ITEM + bw + X_OUT_GAP

    def height(kind, r):
        if kind == "label":
            return len(wrap(r, SIZE["head"], bw)) * SIZE["head"] * 1.25 + 16
        rows, tw = inner(r, bw)
        return sum(len(wrap(x, SIZE[k], tw)) * SIZE[k] * 1.25 + 6 for x, k in rows) + 2 * BOX_PAD

    def section(rows, y0):
        """Lay rows into `cols` columns of about equal height; draw each box, the spines and the ticks into them, and
        (one column) the arrow to what each leads to. Returns (the middles of column 0's names, every middle, bottom)."""
        hs = [height(k, r) + (BOX_GAP if k == "item" else 0) for k, r in rows]
        target, cut, acc, group = sum(hs) / cols, [[]], 0, None
        for (k, r), h in zip(rows, hs):
            if cut[-1] and acc + h / 2 > target * len(cut) and len(cut) < cols:
                carry = [cut[-1].pop()] if cut[-1][-1][0] == "label" else []   # a label goes with its first box
                cut.append(carry)
                if k == "item" and group and not carry:  # a group cut in two names itself again
                    cont = f"{group} · continued"
                    cut[-1].append(("label", cont, height("label", cont)))
            if k == "label":
                group = r
            cut[-1].append((k, r, h))
            acc += h
        mids0, bottom = [], y0
        spines = []
        for c, col in enumerate(cut):
            x, y, mids = X_ITEM + c * (bw + COL_GAP), y0 + (24 if cols > 1 else 0), []
            for k, r, h in col:
                if k == "label":
                    _text(out, fid, x, y, r, SIZE["head"], bw)
                    y += h
                    continue
                bh = h - BOX_GAP
                out.append(canvas._tree_base("rectangle", x, y, bw, bh, fid, strokeWidth=2, roundness={"type": 3}))
                yy = y + BOX_PAD
                for i, (txt, kind) in enumerate(inner(r, bw)[0]):
                    e = _text(out, fid, x + BOX_PAD, yy, txt, SIZE[kind], bw - 2 * BOX_PAD)
                    yy += e["height"] + 6
                mid = y + BOX_PAD + SIZE["name"] * 0.65
                mids.append(mid)
                if r.get("out"):
                    _line(out, fid, [(x + bw + 6, mid), (x_out - 16, mid)], arrow=True, dashed=r["dashed"])
                    o = _text(out, fid, x_out, y + BOX_PAD - 2, r["out"], SIZE["out"], W_OUT)
                    y = max(y, o["y"] + o["height"] - bh)
                y += h
            spines.append((x - 40, mids))
            mids0 = mids0 or mids
            bottom = max(bottom, y)
        for c, (sx, mids) in enumerate(spines):
            if not mids:
                continue
            if c:                                       # a later column hangs from a bus over the first
                _line(out, fid, [(spines[0][0], y0), (sx, y0), (sx, max(mids))])
            for m in mids:
                _line(out, fid, [(sx, m), (sx + 32, m)], arrow=True)
        if cols > 1 and spines[0][1]:
            _line(out, fid, [(spines[0][0], y0), (spines[0][0], max(spines[0][1]))])
        return mids0, [m for _, ms in spines for m in ms], bottom

    if not inside:
        _text(out, fid, x_out, top - 34, "📝 the Questions each topic feeds", SIZE["small"], W_OUT)
    smids, sall, sbottom = section(srows, top)
    unfed = [q for q in b["questions"] if q["num"] not in fed and q["num"] not in answered]
    if unfed:
        e = _text(out, fid, x_out if not inside else X_ITEM, sbottom,
                  "❓ no topic or Job feeds " + " · ".join(f"Q{q['num']}" for q in unfed), SIZE["small"], W_OUT)
        sbottom = max(sbottom, e["y"] + e["height"] + 20)
    jtop = sbottom + 60
    if b["jobs"] and not inside:
        _text(out, fid, x_out, jtop - 34, "🏁 what each Job must deliver", SIZE["small"], W_OUT)
    jmids, jall, jbottom = section(jrows, jtop)
    if unsaid:                                          # one red note, not a red line per Job
        e = _text(out, fid, x_out if not inside else X_ITEM, jtop if (len(unsaid) == len(b["jobs"]) and not inside)
                  else jbottom, f"❓ no close: line yet, so what it must deliver is unknown: {' · '.join(unsaid)} "
                  "(write it in each Job's face, or in this face's index: jobs)", SIZE["small"], W_OUT)
        jbottom = max(jbottom, e["y"] + e["height"] + 20)
    widths = [x_out + W_OUT + 40] if not inside else [X_ITEM + cols * bw + (cols - 1) * COL_GAP + 40]

    def branch(mids, label, sub, notes, y_min):
        """A branch box level with its items (its name big, what it is small), joined to the first spine, its notes
        under it."""
        mid = max((min(mids) + max(mids)) / 2 if mids else y_min + 40, y_min + 40)
        h = len(wrap(label, SIZE["cat"], W_CAT - 36)) * SIZE["cat"] * 1.25 + \
            len(wrap(sub, SIZE["sub"], W_CAT - 36)) * SIZE["sub"] * 1.25 + 36
        y = mid - h / 2
        out.append(canvas._tree_base("rectangle", X_CAT, y, W_CAT, h, fid, strokeWidth=3, roundness={"type": 3}))
        e = _text(out, fid, X_CAT + 18, y + 14, label, SIZE["cat"], W_CAT - 36)
        _text(out, fid, X_CAT + 18, e["y"] + e["height"] + 4, sub, SIZE["sub"], W_CAT - 36)
        if mids:
            _line(out, fid, [(X_CAT + W_CAT, mid), (X_SPINE, mid)])
            _line(out, fid, [(X_SPINE, min(mids + [mid])), (X_SPINE, max(mids + [mid]))])
        yy = y + h + 16
        for n in notes:
            e = _text(out, fid, X_CAT, yy, n, SIZE["note"], X_SPINE - X_CAT - 40)
            yy += e["height"] + 10
        return mid, yy

    smid, snotes = branch(smids, f"{THING['studio']} Studio", "where we think", [], top)
    live = [j for j in b["jobs"] if j["next"] and "reference" not in j["state"].lower()]   # never a people list
    start = plan.get("first") or next((f"{j['nn']} · {j['next']}" for want in ("active", "partly", "open")
                                      for j in live if state_word(j["state"]) == want), "")
    jnotes = ([f"👉 start here: {first_sentence(start, 140)}"] if start else []) + \
        ([f"🧭 boundary: {plan['boundary']}"] if plan.get("boundary") else []) + \
        ["❓ " + str(q).removeprefix("? ").removeprefix("❓ ") for q in (plan.get("open") or [])[:2]]
    jmid, jnbottom = branch(jmids, f"{THING['job']} Jobs", "where we work", jnotes, max(jtop, snotes + 30))
    # ── the root: the Block, why it exists and when it is done
    rmid = (smid + jmid) / 2
    head = b["title"] if b["title"] and b["title"] != b["name"] else b["name"]      # the words big, the folder small
    rh = len(wrap(head, SIZE["root"], W_ROOT - 36)) * SIZE["root"] * 1.25 + \
        len(wrap(b["name"], SIZE["sub"], W_ROOT - 36)) * SIZE["sub"] * 1.25 + 40
    rnotes = [f"🚦 {first_sentence(b['state'], 60)}"] if b["state"] else []
    rnotes += [f"🎯 why it exists\n{first_sentence(b['spine'], 220)}"] if b["spine"] else ["❓ why it exists: no spine: line"]
    rnotes += [f"🏁 done when\n{first_sentence(b['close'], 180)}"] if b["close"] else []
    rnotes += [f"📍 now\n{first_sentence(b['status'], 180)}"] if b["status"] else []
    rnotes += [ln for n in folded for ln in flat(n) if "Done when" not in ln][:3]
    def note_h(n):
        top_line, _, rest = n.partition("\n")
        return (len(wrap(top_line, SIZE["head"], W_ROOT + 20)) * SIZE["head"] * 1.25 +
                (len(wrap(rest, SIZE["note"], W_ROOT + 20)) * SIZE["note"] * 1.25 + 4 if rest else 0) + 16)
    nh = sum(note_h(n) for n in rnotes)
    items_bottom = max(jbottom, jnbottom, snotes)
    ry = max(top, min(rmid - rh / 2, items_bottom - rh - 18 - nh))   # the root and its notes end with the branches
    out.append(canvas._tree_base("rectangle", X_ROOT, ry, W_ROOT, rh, fid, strokeWidth=3, roundness={"type": 3},
                                 backgroundColor=KEY))     # the index's key point: the Block itself
    e = _text(out, fid, X_ROOT + 18, ry + 14, head, SIZE["root"], W_ROOT - 36)
    _text(out, fid, X_ROOT + 18, e["y"] + e["height"] + 4, b["name"], SIZE["sub"], W_ROOT - 36)
    rmid = ry + rh / 2
    for cmid, label in ((smid, "thinks in"), (jmid, "works in")):
        xb = X_ROOT + W_ROOT + 30
        _line(out, fid, [(X_ROOT + W_ROOT, rmid), (xb, rmid), (xb, cmid), (X_CAT - 10, cmid)], arrow=True)
        ly = (rmid + cmid) / 2 - 12 if abs(cmid - rmid) > 60 else cmid - 34    # beside the branch, never on it
        _text(out, fid, xb + 8, ly, label, SIZE["sub"], X_CAT - xb - 14)
    yy = ry + rh + 18
    for n in rnotes:                                    # a heading (🎯 why it exists) big, its words under it
        top_line, _, rest = n.partition("\n")
        e = _text(out, fid, X_ROOT, yy, top_line, SIZE["head"], W_ROOT + 20)
        yy += e["height"] + 4
        if rest:
            e = _text(out, fid, X_ROOT, yy, rest, SIZE["note"], W_ROOT + 20)
            yy += e["height"] + 4
        yy += 12
    bottom = max(yy, items_bottom) + 20
    mm_w = max(widths + [1800])
    _text(out, fid, X_ROOT, 24, f"🗂 {b['name']} · {b['title']} · the index", SIZE["title"], mm_w - 2 * X_ROOT)
    _text(out, fid, X_ITEM, bottom, "read from each topic's face, each Job's face, Tasks and CHECKLIST, and the Questions' report pages; "
          "drawn by haipipe-studio block_index.py", SIZE["small"], mm_w - X_ITEM - 40)
    out.append(canvas.change_note(X_ROOT, bottom,
                                  "Job → Task names and recorded states expanded" if plan.get("tasks") else
                                  "the index is a mind map, each topic and Job its own box (JL)",
                                  "261012", fid, size=20))
    f["width"], f["height"] = mm_w, bottom + 60
    return out


# ── the Studio plan: the topics a Block needs, as its story (b32 EB1A's s00, the model JL picked on 261012: "could you
# not try to replicate this one? and update the /haipipe-studio and other excalidraw skills for this?") ────────────
def yaml_block(face: Path, key: str):
    import yaml
    m = re.search(rf"```yaml\n({key}:.*?)\n```", read(face), re.S)
    return (yaml.safe_load(m.group(1)) or {}).get(key) if m else None


def plan_frame(face: Path, b: dict) -> dict | None:
    """The Studio plan as a map frame for topic_map.draw_map: one box per step of the Block's story (`studio_plan:
    steps`, each naming its topic ids and the arrow to the next), else one box per Studio group; in each box every
    topic, made or proposed, with its question, the Jobs it rests on and what it should produce. None when the face
    has no `studio_plan` (a Block's session writes it, and `studio_proposals`: it knows the work)."""
    plan, props = yaml_block(face, "studio_plan") or {}, yaml_block(face, "studio_proposals") or []
    if not plan:                                        # the plan is drawn when the face writes one
        return None
    made = {t["nn"]: t for t in b["topics"]}
    by_id = {p["id"]: p for p in props}

    def node(nn):
        p, t = by_id.get(nn), made.get(nn)
        if not p:                                       # a topic that exists and was never proposed
            return {f"{mark(t['stage'])} {nn} · {t['title']}": [first_sentence(t["topic"], 110)] if t["topic"] else []}
        status = p.get("status", "proposed")
        head = f"{mark(t['stage']) if t else '⬜'} {nn} · {p.get('title', '')}" + \
            ("" if t else f" [{status}]")
        kids = [first_sentence(p.get("map_question") or p.get("question", ""), 140)]
        kids += [f"rests on: {', '.join(p.get('jobs') or [])}" + (f" · order {p['priority']}" if p.get("priority") else "")]
        kids += [f"→ {first_sentence(p.get('map_output') or p.get('output', ''), 140)}"]
        if status == "conditional" and p.get("condition"):
            kids += [f"❓ only if: {first_sentence(p['condition'], 120)}"]
        return {head: [k for k in kids if k.strip(" →")]}

    first_tag = {t["nn"]: (t["tags"][0] if t["tags"] else "Untagged") for t in b["topics"]}
    steps = plan.get("steps")
    if not steps:                                       # no story written: one box per group, in order
        groups = []
        for nn in sorted(set(by_id) | set(made), key=lambda n: (by_id.get(n, {}).get("priority", 99), n)):
            g = by_id.get(nn, {}).get("group") or first_tag.get(nn, "Untagged")
            if g not in [x["title"] for x in groups]:
                groups.append({"title": g, "ids": []})
            next(x for x in groups if x["title"] == g)["ids"].append(nn)
        steps = groups
    boxes, arrows = [], []
    for i, st in enumerate(steps):
        row, col = divmod(i, 4)                         # a snake: the next row runs back, so each arrow stays short
        boxes.append({"id": f"step{i}", "at": [col if row % 2 == 0 else 3 - col, row], "title": st.get("title", f"step {i + 1}"),
                      "why": st.get("why", ""), "tree": [node(nn) for nn in st.get("ids") or []], "most": 2})
        if i and steps[i - 1].get("next"):
            arrows.append((f"step{i - 1}", f"step{i}", steps[i - 1]["next"], False))
    return {"title": plan.get("title") or "🧠 the Studio plan · the topics this Block needs",
            "intro": plan.get("intro") or f"{len(made)} made · {sum(n not in made for n in by_id)} proposed",
            "boxes": boxes, "arrows": arrows}


S00_RUNNER = '''"""Rebuild this S00 with the current shared haipipe-studio generator."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "{scripts}").resolve()))
import block_index  # noqa: E402

if __name__ == "__main__":
    block_index.draw(HERE.parent.parent)
'''


def ensure_builder(block: Path, topic: Path) -> Path:
    """Register the shared generator as this topic's builder, so Workbench opens it view only.

    Prefer the SPACE's Tools symlink; keep a relative fallback for Tools' own blueprints.
    An existing local builder belongs to its author and is never replaced.
    """
    runner = topic / "build_s00_background_and_index.py"
    if runner.exists():
        return runner
    scripts = HERE
    for parent in (block, *block.parents):
        candidate = parent / "Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"
        if candidate.is_dir() and candidate.resolve() == HERE:
            scripts = candidate
            break
    relative = Path(os.path.relpath(scripts, topic)).as_posix()
    runner.write_text(S00_RUNNER.format(scripts=relative), encoding="utf-8")
    return runner


# ── ④ what we propose next: one row per proposal, read left to right like the index (JL 261012: "we also need to
# propose the new studio and new jobs in a new frame"; "each studio should be a row")
#     ❓ the gap it closes ─▶ 🧠 the topic that thinks it through ─▶ 🧱 the Job that does it ─▶ 🏁 what it delivers
P_COLS, P_GAP = (440, 620, 620, 440), 110             # the four columns, and the room for an arrow between two


def proposal_rows(b: dict, face: Path) -> list:
    """The rows of ④: each proposed topic with the first proposed Job resting on it, then each Job left over, beside
    the made topic it rests on when there is one. A row keeps every `why` it holds: a topic's and its Job's."""
    ptopics, pjobs = proposed(b, face)
    made = {t["nn"]: t for t in b["topics"]}
    rows, used = [], set()
    for p in ptopics:
        j = next((j for j in pjobs if p["id"] in (j.get("topics") or []) and j["folder"] not in used), None)
        used |= {j["folder"]} if j else set()
        whys = [(p["id"], p.get("why"))] + ([(j["id"], j["why"])] if j and j.get("why") else [])
        rows.append({"whys": whys, "topic": p, "job": j, "out": (j or {}).get("finish") or p.get("output")})
    for j in pjobs:
        if j["folder"] not in used:
            on = next((t for t in j.get("topics") or [] if t in made), None)
            rows.append({"whys": [(j["id"], j.get("why"))], "topic": made.get(on), "job": j, "out": j.get("finish")})
    return rows


def proposals_frame(b: dict, face: Path) -> list:
    """④'s elements: a heading per column, then one row per proposal, its boxes red and dashed until a person agrees
    and its folder is made; a made topic a proposed Job rests on is a plain black box. [] when nothing is proposed:
    the Block's session writes `studio_proposals` and `job_proposals` (each with a `why`); the drawing never invents
    one."""
    rows = proposal_rows(b, face)
    if not rows:
        return []
    fid, out = "frame-s00-proposals", []
    xs = [X_ROOT]
    for w in P_COLS[:-1]:
        xs.append(xs[-1] + w + P_GAP)
    width = xs[-1] + P_COLS[-1] + X_ROOT
    f = canvas.reads_down(canvas._tree_base("frame", 0, 0, width, 100, None, id=fid, customData={"map": True},
                                            name=f"s00 · 💡 {b['name']} · what we propose next"))
    out.append(f)
    e = _text(out, fid, X_ROOT, 24, f"💡 {b['name']} · what we propose next", SIZE["title"], width - 2 * X_ROOT)
    e = _text(out, fid, X_ROOT, e["y"] + e["height"] + 8, "Not made yet. A person agrees each one; then its folder is "
              "made and it moves into the index.", SIZE["sub"], width - 2 * X_ROOT)
    out.insert(len(out) - 1, key_box(e, fid))
    y = e["y"] + e["height"] + 40
    for x, w, head in zip(xs, P_COLS, ("❓ the gap it closes", "🧠 the topic", "🧱 the Job", "🏁 what it delivers")):
        _text(out, fid, x, y, head, SIZE["head"], w, canvas.INK)
    y += SIZE["head"] * 1.25 + 30

    def cell(t, job):
        """A box's name and lines: a proposal's status, question, what it rests on and when it holds; a made topic."""
        if t.get("nn"):
            return f"{mark(t['stage'])} {t['nn']} · {t['title']}", [("made: the Job rests on it", "line")], False
        status = t.get("status", "proposed")
        lines = [] if job else [(first_sentence(t["question"], 150), "line")] if t.get("question") else []
        rests = t.get("topics" if job else "jobs") or []
        lines += [(f"{'rests on' if job else 'draws on'}: {' · '.join(rests)}", "line")] if rests else []
        if status == "conditional" and t.get("condition"):
            lines.append((f"❓ only if: {first_sentence(t['condition'], 130)}", "line"))
        if job and t.get("taken"):
            lines.append((f"❓ {t['id']} is already {t['taken']}: give it a free number", "line"))
        return f"⬜ {t['folder'] if job else t['id']} · {t.get('title', '')} [{status}]", lines, True

    def box(x, y, w, name, lines, red):
        tw, yy, parts = w - 2 * BOX_PAD, y + BOX_PAD, []
        for s, kind in [(name, "name")] + lines:
            e = _text(parts, fid, x + BOX_PAD, yy, s, SIZE[kind], tw, canvas.RED if red and kind == "name" else None)
            yy = e["y"] + e["height"] + 6
        rect = canvas._tree_base("rectangle", x, y, w, yy - y + BOX_PAD - 6, fid, strokeWidth=2, roundness={"type": 3},
                                 strokeColor=canvas.RED if red else canvas.INK, strokeStyle="dashed" if red else "solid")
        out.extend([rect] + parts)
        return rect

    for r in rows:
        mid = y + BOX_PAD + SIZE["name"] * 0.65
        gy, right = y + BOX_PAD - 2, xs[0]
        for nn, why in r["whys"]:                       # the gap each one closes; named when a row holds two
            why = (why or "why not written yet").removeprefix("❓ ").removeprefix("? ")
            e = _text(out, fid, xs[0], gy, f"❓ {nn}: {why}" if len(r["whys"]) > 1 else f"❓ {why}", SIZE["out"],
                      P_COLS[0])
            gy, right = e["y"] + e["height"] + 10, max(right, e["x"] + e["width"])
        bottom = gy
        for x, w, t, job in ((xs[1], P_COLS[1], r["topic"], False), (xs[2], P_COLS[2], r["job"], True)):
            if not t:
                continue
            name, lines, red = cell(t, job)
            if not job and r["job"] and red and t.get("output"):
                lines.append((f"→ {first_sentence(t['output'], 130)}", "line"))
            rect = box(x, y, w, name, lines, red)
            _line(out, fid, [(right + 10, mid), (x - 10, mid)], arrow=True, dashed=True)
            right, bottom = x + w, max(bottom, rect["y"] + rect["height"])
        if r["out"]:
            e = _text(out, fid, xs[3], y + BOX_PAD - 2, f"🏁 {first_sentence(r['out'], 160)}", SIZE["out"], P_COLS[3])
            _line(out, fid, [(right + 10, mid), (xs[3] - 10, mid)], arrow=True, dashed=True)
            bottom = max(bottom, e["y"] + e["height"])
        y = bottom + BOX_GAP + 10
    f["height"] = y + 30
    return out


def key_box(e: dict, fid: str, pad: float = 10) -> dict:
    """A frame's key point: the slight colour behind one text, as excalidraw-studio's Drawing.key draws it."""
    return canvas._tree_base("rectangle", e["x"] - pad - 8, e["y"] - pad, e["width"] + 2 * pad + 16,
                             e["height"] + 2 * pad, fid, strokeWidth=3, roundness={"type": 3}, backgroundColor=KEY)


def key_intro(els: list, start: int, n: int) -> None:
    """The key point of a frame topic_map just drew from els[start]: the frame, its title, then its `n` intro lines,
    in that order (topic_map's draw_map and draw_frame); the slight colour goes behind those lines, or behind the
    title when the frame has no intro (n 0), since then the title is what the frame says."""
    fid = els[start]["id"]
    lines = [e for e in els[start + 2:start + 2 + n] if e.get("frameId") == fid and e["type"] == "text"] or \
        [e for e in els[start + 1:start + 2] if e.get("frameId") == fid and e["type"] == "text"]
    if not lines:
        return
    if not n:                                            # behind the title: it goes before the title
        els.insert(start + 1, key_box(lines[0], fid))
        return
    x0, y0 = min(e["x"] for e in lines), min(e["y"] for e in lines)
    x1, y1 = max(e["x"] + e["width"] for e in lines), max(e["y"] + e["height"] for e in lines)
    els.insert(start + 2, key_box({"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0}, fid))


def merge_into_index(els: list, fid: str, drop: set) -> list:
    """A small tree background (under SLIDE) merged into the top of the index frame, under its title: excalidraw-studio's
    "a thin frame is merged, not padded" (JL 261012, the s00 redraw). It keeps its heading, tree and green notes; its
    key box goes (the index keeps one key point, the Block), and so do the elements in `drop` (an opening line that
    only repeats the spine, which the Block's box already says)."""
    frames = {e["id"]: e for e in els if e["type"] == "frame"}
    small, index = frames[fid], frames["frame-s00-index"]
    title_bottom = max((e["y"] + e["height"] for e in els
                        if e.get("frameId") == index["id"] and e["type"] == "text" and e["y"] == 24),
                       default=24 + SIZE["title"] * 1.25)
    under = title_bottom + 30                         # leave room for every wrapped title line
    shift = small["height"] + 30 + max(0, title_bottom - (24 + SIZE["title"] * 1.25))
    for e in els:
        if e.get("frameId") == index["id"] and not (e["type"] == "text" and e["y"] == 24):
            e["y"] += shift
    out = [e for e in els if e is not small and not (e.get("frameId") == fid and
                                                     (e.get("backgroundColor") == KEY or e["id"] in drop))]
    for e in out:
        if e.get("frameId") == fid:
            e["frameId"] = index["id"]
            e["y"] += under - 20
    index["height"] += shift
    return out


def acts(els: list) -> list:
    """s00's frames as two acts (excalidraw-studio principle 3): the story and what the Block stands on, then what is
    made and what we propose next; a named arrow for each step. Uses excalidraw-studio's Drawing.acts."""
    sys.path.insert(0, str(EXCALIDRAW_STUDIO))
    from draw import Drawing
    frames = {e["id"]: e for e in els if e["type"] == "frame"}
    plan = [f for f in frames if f == "frame-s00-plan"]
    grounds = [f for f in frames if f.startswith("frame-s00-background")]
    made = [f for f in frames if f in ("frame-s00-index", "frame-s00-proposals")]
    rows, between = [], []
    if plan or grounds:
        rows.append({"name": "The story, and what the Block stands on", "frames": plan + grounds,
                     "arrow": (["stands on"] if plan and grounds else []) + ["and on"] * (len(grounds) - 1)})
    rows.append({"name": "What is made" + (", and what we propose next" if len(made) > 1 else ""), "frames": made,
                 "arrow": ["still needs"] * (len(made) - 1)})
    for n, row in enumerate(rows, 1):
        row["name"] = f"Act {n} · {row['name']}"
    if len(rows) == 2:
        between.append((rows[0]["frames"][0], "frame-s00-index", "is made so far as"))
    d = Drawing()
    d.els = els
    d.acts(rows, between=between)
    return d.els


def draw(block: Path) -> Path:
    topic = block / "studio" / S00
    topic.mkdir(parents=True, exist_ok=True)
    ensure_builder(block, topic)
    face = topic / f"{S00}.md"
    b = read_block(block)
    if not face.is_file():
        topic.mkdir(parents=True, exist_ok=True)
        face.write_text(seed_face(block, b), encoding="utf-8")
    story = plan_frame(face, b)
    els, frames = [], background_of(face)[:1 if story else 2]   # plan, background, index, then what we propose
    if story:
        draw_map(els, "frame-s00-plan", f"s00 · {story['title']}", story["title"], [story["intro"]], story["boxes"],
                 story["arrows"])
        canvas.reads_down(els[0])                       # s00's frames may run taller (JL 261012: "make the frame larger")
        key_intro(els, 0, 1)
    for fr in frames:
        fr.setdefault("intro", b["spine"] if fr is frames[0] else "")
    thin = len(frames) == 1 and not frames[0].get("boxes") and words(frames[0]) < BG_MIN
    folded = list(frames.pop().get("tree") or []) if thin else []      # a thin background goes into the Block's box
    small = []                                          # (fid, its spine line): backgrounds too small for a frame
    for i, fr in enumerate(frames, 1):
        fid, name, title = f"frame-s00-background-{i}", f"s00 · {fr.get('title', f'background {i}')}", \
            fr.get("title", f"Background {i}")
        start = len(els)
        if fr.get("boxes"):
            draw_map(els, fid, name, title, [fr["intro"]] if fr["intro"] else [], fr["boxes"],
                     [(a["from"], a["to"], a.get("label", ""), a.get("dashed", False)) for a in fr.get("arrows") or []],
                     fr.get("notes") or ())
        else:
            draw_frame(els, fid, name, title, [fr["intro"]] if fr["intro"] else [], fr.get("tree") or [],
                       int(fr.get("cols", 2)), fr.get("notes") or ())
        key_intro(els, start, 1 if fr["intro"] else 0)
        frame = els[start]
        if not fr.get("boxes") and frame["width"] * frame["height"] < SLIDE:     # a slide: merged into the index
            # its opening line sits after the title and the key box key_intro put before it
            small.append((fid, {e["id"] for e in els[start + 3:start + 4] if e["type"] == "text"
                                and fr["intro"] and fr["intro"] == b["spine"]}))
    plan = plan_of(face)
    # one row per topic and per Job, in one column, the frame as tall as that needs (JL 261012, on b10's index: "This
    # one can be larger, of height. Currently it is too compact. each studio should be a row.")
    old = widen(plan.get("width"))
    try:
        els += mind_map(b, block, plan, folded, 2, 1, proposed(b, face))
    finally:
        narrow(old)
    els += proposals_frame(b, face)                     # ④ what we propose next, after what is there
    for fid, drop in reversed(small):                   # the last first: each merge goes on top, so they keep order
        els = merge_into_index(els, fid, drop)
    els = acts(els)                                     # two rows, each an act, a named arrow for each step
    out = topic / f"{S00}.excalidraw"
    # palette off: the key point's slight colour is excalidraw-studio's principle 5, as its Drawing.write keeps it
    canvas.write(out, els, f"haipipe-studio scripts/block_index.py {block.name}", palette=False)
    from render_png import render
    render(out, out.with_suffix(".png"))
    return out


def blocks(root: Path) -> list[Path]:
    """Every Block under `root`: a bNN_ folder with a face, outside any archive, history or _-folder. A link is not
    followed, so a SPACE's Tools/ is its own root."""
    out = []
    for dirpath, dirnames, _ in os.walk(root):
        p = Path(dirpath)
        dirnames[:] = sorted(d for d in dirnames if not d.startswith((".", "_")) and d not in SKIP
                             and "archive" not in d.lower())
        if BLOCK.match(p.name) and face_of(p):
            out.append(p)
            dirnames[:] = []                          # a Block's Jobs and Tasks are not Blocks
    return out


def other_s00(block: Path) -> list[str]:
    """Another s00 topic beside the background and index: two s00s would share a number."""
    return sorted(p.name for p in (block / "studio").glob("s00-*") if p.is_dir() and p.name != S00)


def shown(p: Path) -> str:
    """A path as printed: relative to its SPACE root (the nearest folder with env.sh, else its repository: Tools has no
    env.sh), never /Users/... (AGENTS.md rule 12; b31-s01, 261012)."""
    p = p.resolve()
    root = next((d for d in p.parents if (d / "env.sh").is_file()), None) or \
        next((d for d in p.parents if (d / ".git").exists()), None)
    return p.relative_to(root).as_posix() if root else p.name


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("block", type=Path, nargs="*")
    ap.add_argument("--all", type=Path, metavar="ROOT", help="every Block under ROOT")
    ap.add_argument("--draw", action="store_true", help=f"draw studio/{S00}/ and its preview")
    a = ap.parse_args(argv)
    todo = [p.resolve() for p in a.block] + (blocks(a.all.resolve()) if a.all else [])
    if not todo:
        ap.error("name a Block, or --all <root>")
    for block in todo:
        if other_s00(block):
            print(f"{shown(block)}: skipped; it already has {', '.join(other_s00(block))}: renumber it, then rerun")
            continue
        if a.draw:
            print(shown(draw(block)))
        else:
            b = read_block(block)
            print(f"{b['name']} · {b['title']}")
            print_tree(index_tree(b), 1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
