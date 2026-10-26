"""The builders: a mind map read from disk, and the refresh that keeps what a person added.

    from_work(path)    a world, a Block or a Job: Block → Job → Task → Run, each with its run counts
    from_topic(topic)  a Studio topic's structured side (mNN): its face's labelled lines and sections as branches

A built node's id starts with @ and names where it came from (`@j01_x/t02_y`); its `#hash` is the hash of the words
its builder wrote, so a refresh can tell words a person changed (kept) from words the builder may update.
"""
from __future__ import annotations

import re
from pathlib import Path

import mmtree as MT

BLOCK = re.compile(r"^(b\d{2}_|Paper-)")
JOB, TASK = re.compile(r"^j\d{2,3}_"), re.compile(r"^t\d{2}_")
TOPIC = re.compile(r"^s(\d{2})[-_](.+)$")
STATUS = {"done": "✅", "passed": "✅", "ok": "✅", "complete": "✅", "completed": "✅", "failed": "❌", "fail": "❌",
          "error": "❌", "running": "🔶", "partial": "🔶", "blocked": "⛔"}


def built(key: str, text: str, children=()) -> MT.Node:
    return MT.Node("@" + key, text, list(children), hash=MT.words_hash(text))


def _dirs(folder: Path, pat) -> list:
    return sorted(p for p in folder.iterdir() if p.is_dir() and pat.match(p.name)) if folder.is_dir() else []


def _runs(task: Path) -> list:
    runs = task / "runs"
    return sorted(p for p in runs.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))) if runs.is_dir() else []


def _status(run: Path) -> str:
    card = run / "run.yaml"
    text = card.read_text(encoding="utf-8", errors="ignore") if card.is_file() else ""
    m = re.search(r"(?m)^status:\s*['\"]?([A-Za-z]+)", text)
    return (m.group(1).lower() if m else "") or ("done" if (run / "result").is_dir() else "")


def _n(k: int, word: str) -> str:
    return f"{k} {word}{'' if k == 1 else 's'}"


# ── from-work ──────────────────────────────────────────────────────────────────────────────────────────────
def from_work(path: Path) -> MT.MindMap:
    """A world (work/), a Block or a Job, down to its Runs (a world stops at Tasks, its Runs counted)."""
    path = Path(path).resolve()
    if JOB.match(path.name):
        kind = "job"
    elif BLOCK.match(path.name):
        kind = "block"
    else:
        kind = "world"

    def task_node(t: Path, key: str, leaves: bool) -> MT.Node:
        runs = _runs(t)
        done = sum(_status(r) in ("done", "passed", "ok", "complete", "completed") for r in runs)
        words = f"{t.name} · {_n(len(runs), 'run')}" + (f", {done} done" if done and done < len(runs) else
                                                        ", all done" if runs and done == len(runs) else "")
        kids = [built(f"{key}/{r.name}", f"{r.name} {STATUS.get(_status(r), '⬜')}") for r in runs] if leaves else []
        return built(key, words, kids)

    def job_node(j: Path, key: str, leaves: bool) -> MT.Node:
        tasks = _dirs(j, TASK)
        kids = [task_node(t, f"{key}/{t.name}", leaves) for t in tasks]
        runs = sum(len(_runs(t)) for t in tasks)
        return built(key, f"{j.name} · {_n(len(tasks), 'task')} · {_n(runs, 'run')}", kids)

    if kind == "job":
        tasks = _dirs(path, TASK)
        root = built(".", f"{path.name} · {_n(len(tasks), 'task')}", [task_node(t, t.name, True) for t in tasks])
    elif kind == "block":
        jobs = _dirs(path, JOB)
        root = built(".", f"{path.name} · {_n(len(jobs), 'job')}", [job_node(j, j.name, True) for j in jobs])
    else:
        blocks = _dirs(path, BLOCK)
        kids = [built(b.name, f"{b.name} · {_n(len(_dirs(b, JOB)), 'job')}",
                      [job_node(j, f"{b.name}/{j.name}", False) for j in _dirs(b, JOB)]) for b in blocks]
        root = built(".", f"{path.name} · {_n(len(blocks), 'block')}", kids)
    root.id = "root"
    return MT.MindMap({"mindmap": "1", "title": f"{path.name} · the work", "built": "from-work"}, root)


# ── from-topic ─────────────────────────────────────────────────────────────────────────────────────────────
LABEL = re.compile(r"^\*\*([A-Z][A-Za-z ]{1,24}):\*\*\s*(.*)$")
TO_ROOT = ("Stage", "Tags", "Label")                  # short facts: under the root, not branches


def short(s: str, words: int = 14) -> str:
    """A leaf's words: the first sentence, at most `words` words, so a node reads at a glance."""
    s = " ".join(str(s).split())
    s = re.split(r"(?<=[.;!?])\s+(?=[A-Z(`*])", s)[0].rstrip(".;")
    ws = s.split()
    return " ".join(ws[:words]) + (" …" if len(ws) > words else "")


def face_of(topic: Path) -> Path | None:
    md = topic / f"{topic.name}.md"
    return md if md.is_file() else None


def _sections(lines: list) -> tuple:
    """The face as (title, [(heading or None, [paragraph or item, ...])]); code blocks left out."""
    title, i = "", 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines):
        if lines[i].startswith("# "):
            title, i = lines[i][2:].strip(), i + 1
        elif i + 1 < len(lines) and re.match(r"^=+\s*$", lines[i + 1]):
            title, i = lines[i].strip(), i + 2
    out, head, cur, para, code = [], None, [], [], False

    def flush():
        if para:
            cur.append(" ".join(para))
            para.clear()
    while i < len(lines):
        ln = lines[i]
        if ln.lstrip().startswith("```"):
            flush()
            code = not code
        elif code:
            pass
        elif i + 1 < len(lines) and ln.strip() and re.match(r"^-{3,}\s*$", lines[i + 1]):
            flush()
            out.append((head, cur))
            head, cur, i = ln.strip(), [], i + 1
        elif ln.startswith("## "):
            flush()
            out.append((head, cur))
            head, cur = ln[3:].strip(), []
        elif MT.BULLET.match(ln):
            flush()
            cur.append(MT.BULLET.match(ln).group(2))
        elif not ln.strip():
            flush()
        else:
            para.append(ln.strip())
        i += 1
    flush()
    out.append((head, cur))
    return title, out


def from_topic(topic: Path) -> MT.MindMap:
    topic = Path(topic).resolve()
    face = face_of(topic)
    if face is None:
        raise FileNotFoundError(f"{topic.name}/ has no face {topic.name}.md")
    title, parts = _sections(face.read_text(encoding="utf-8").splitlines())
    title = title or topic.name
    branches, note = [], []
    for head, items in parts:
        if head is None:                                 # before the first section: the labelled lines
            for it in items:
                m = LABEL.match(it)
                if not m:
                    continue
                if m.group(1) in TO_ROOT:
                    note.append(f"**{m.group(1)}:** {m.group(2)}")
                    continue
                leaves = [s for s in re.split(r"(?<=[.;])\s+(?=[A-Z(`*])", m.group(2)) if s.strip()]
                branches.append((m.group(1), leaves))
            continue
        if head.lower() == "files":                      # the topic's real files, read from disk
            items = [p.name + ("/" if p.is_dir() else "") for p in sorted(topic.iterdir())
                     if not p.name.startswith((".", "_")) and not re.match(r"m\d{2}[-_]", p.name)]   # not its own mNN
        items = [it for it in items if not it.startswith("(write here")]
        branches.append((head, items))
    kids = []
    for k, (head, items) in enumerate(branches):
        key = re.sub(r"[^a-z0-9]+", "-", head.lower()).strip("-") or f"b{k}"
        leaves = [built(f"{key}/{j}", short(it)) for j, it in enumerate(items)]
        kids.append(built(key, head, leaves))
    root = built(".", short(title, 14), kids)
    root.id, root.note = "root", note
    return MT.MindMap({"mindmap": "1", "title": f"{title} · structured", "built": "from-topic"}, root)


def mnn_name(topic: Path) -> str:
    """s01-work-ladder → m01-work-ladder.mindmap.md: the structured side keeps its topic's number."""
    m = TOPIC.match(Path(topic).name)
    if not m:
        raise ValueError(f"{Path(topic).name}: a Studio topic is named sNN-<topic>")
    return f"m{m.group(1)}-{m.group(2)}{MT.SUFFIX}"


def words(mm: MT.MindMap) -> int:
    return sum(len(MT.display(n.text).split()) for n, *_ in MT.walk(mm.root))


# ── refresh: the builder's new tree over the file a person worked on ───────────────────────────────────────
def _has_person(n: MT.Node) -> bool:
    return any(not c.built or c.edited or _has_person(c) for c in n.children)


def refresh(old: MT.MindMap, new: MT.MindMap) -> dict:
    """Merge a new build into the file, in place: unedited built words take the new words; a node or words a person
    added stay; a built node gone from disk goes, unless a person changed it or hangs something under it."""
    done = {"updated": 0, "added": 0, "dropped": 0}

    def merge(o: MT.Node, n: MT.Node):
        if o.built or o.id == "root":
            if (not o.hash or o.hash == MT.words_hash(o.text)) and o.text != n.text:
                o.text = n.text
                done["updated"] += 1
            if not o.hash or o.hash == MT.words_hash(o.text):
                o.hash = n.hash
        new_by = {c.id: c for c in n.children}
        out = []
        for c in o.children:
            if not c.built:
                out.append(c)
            elif c.id in new_by:
                merge(c, new_by[c.id])
                out.append(c)
            elif c.edited or _has_person(c):
                out.append(c)
            else:
                done["dropped"] += 1
        have = {c.id for c in out}
        for k, nc in enumerate(n.children):
            if nc.id in have:
                continue
            prev = next((n.children[j].id for j in range(k - 1, -1, -1) if n.children[j].id in have), None)
            at = next((i + 1 for i, c in enumerate(out) if c.id == prev), 0)
            out.insert(at, nc)
            have.add(nc.id)
            done["added"] += 1
        o.children = out

    merge(old.root, new.root)
    for k, v in new.meta.items():
        old.meta.setdefault(k, v)
    return done
