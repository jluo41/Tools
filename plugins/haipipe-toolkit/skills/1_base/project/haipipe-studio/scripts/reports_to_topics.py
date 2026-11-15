"""Fold a level's reports/ into its Studio topics (JL 261109: "we will no longer have the report folder").

    python reports_to_topics.py <path>            the plan, nothing written
    python reports_to_topics.py <path> --apply    do it

<path> is any folder: a SPACE, a Project, a Block. For every reports/ under it that sits beside a board.md or a
Job face, in a work/ or cowork/ world (a Paper, Insight, Design or Discovery Board's reports/ is its theme's own and
is listed, never moved):

    1 home     each Question's topic: the level's sNN whose **Feeds:** names it (Q01 or q01_<x>), a folder named
               sNN-q01-* first; an answered Question with none gets a new sNN-q01-<slug>/ (new_topic, view: findings)
    2 face     **Feeds:** as Q ids, a `Q01 · Answer` part (the page's Opening, its answer-status, a link to the page),
               view: findings when the face has none
    3 move     reports/ to _old/reports/; an answered page's folder into its topic as sNN-<topic>/qNN_<x>/ (its
               report drawing stays in _old: no report drawings); an empty page stays in _old, its Question in board.md
    4 links    every link into reports/ in the Project, rewritten: a page to its topic face (board.md when it has
               none), anything else to where it now lives; the register's report: for an empty, homeless one removed

Then studio_update.py audit lists what is left for a person (Why, redraws), and the topic faces render as they did.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import new_topic  # noqa: E402

THEME_OWN = {"paper", "insight", "design", "discovery", "labeling", "ideation"}
SKIP = {"_old", ".git", ".ladder-undo", "node_modules", ".venv", "delivery", "_WorkSpace", "fixture", "fixtures"}
EMPTY = "No answer has been recorded yet"
LINK = re.compile(r"(?<![\w-])((?:\.\./|\./)*[\w./-]*?reports/(q\d\d[\w-]*)(/[\w.-]+(?:/[\w.-]+)*)?)")


def owner_face(level: Path) -> Path | None:
    for f in (level / "board.md", level / f"{level.name}.md"):
        if f.is_file():
            return f
    return None


def project_of(p: Path) -> Path:
    for a in p.parents:
        if (a / "project.yaml").is_file() or (a / "project.md").is_file():
            return a
    return p.parent


def find_reports(root: Path):
    for d, subs, _ in os.walk(root):
        subs[:] = [s for s in subs if s not in SKIP and not s.startswith(".")]
        p = Path(d)
        if p.name == "reports" and owner_face(p.parent):
            rel = set(p.relative_to(project_of(p)).parts)
            yield p, not (rel & THEME_OWN) and bool(rel & {"work", "cowork"})
            subs[:] = []


def questions(face: Path) -> dict:
    t = face.read_text(encoding="utf-8")
    return {m.group(1): m.group(2).strip().strip("'\"") for m in re.finditer(r"(?m)^- id: (Q\d\d)\n\s+title: (.+)$", t)}


def topics(level: Path) -> list[Path]:
    return sorted(p for p in level.glob("s[0-9][0-9]-*/s[0-9][0-9]-*.md") if p.stem == p.parent.name)


def page_of(folder: Path) -> Path | None:
    p = folder / f"{folder.name}.md"
    return p if p.is_file() else next(iter(sorted(folder.glob("*.md"))), None)


def opening(text: str) -> str:
    m = re.search(r"(?ms)^## Opening\s*\n(.*?)(?:\n\s*\n|\Z)", text)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def feeds_of(face: Path) -> str:
    m = re.search(r"(?m)^\*\*Feeds:\*\*(.*)$", face.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def home_of(level: Path, qid: str) -> Path | None:
    n = qid[1:].lower()
    hits = [f for f in topics(level) if re.search(rf"\bQ{n}\b|\bq{n}_", feeds_of(f), re.I)]
    hits.sort(key=lambda f: (f"-q{n}-" not in f.parent.name, f.parent.name))
    return hits[0] if hits else None


def set_feeds(text: str, qs: list[str]) -> str:
    m = re.search(r"(?m)^\*\*Feeds:\*\*(.*)$", text)
    if m:
        new = re.sub(r"`reports/`\s*", "", m.group(1))
        new = re.sub(r"`?reports/[qQ](\d\d)[\w-]*/?`?", r"Q\1", new)
        new = re.sub(r"\b[qQ](\d\d)_[\w-]+", r"Q\1", new)
        new = re.sub(r"Q(\d\d)\s*,\s*(?=Q\d\d)", r"Q\1 · ", new)
        for q in qs:
            if not re.search(rf"\b{q}\b", new):
                new = f" {q} ·" + new
        return text[:m.start(1)] + " " + new.strip() + text[m.end(1):]
    m = re.search(r"(?ms)^\*\*Topic:\*\*.*?\n\s*\n", text)
    i = m.end() if m else len(text)
    return text[:i] + f"**Feeds:** {' · '.join(qs)}\n\n" + text[i:]


def set_view(text: str) -> str:
    if re.search(r"(?m)^view:", text):
        return text
    lines = text.split("\n")
    if len(lines) > 1 and lines[1] and set(lines[1]) == {"="}:
        lines.insert(2, "view: findings")
    return "\n".join(lines)


def answer_part(q, title, page_rel, ans, status) -> str:
    head = f"{q} · Answer"
    out = [head, "-" * len(head), "", f"**Question:** {title}", "", f"**Answer ({status}):** {ans or 'not written yet.'}", ""]
    if page_rel:
        out += [f"**Page:** [{Path(page_rel).name}]({page_rel}): the full answer, its evidence and limits "
                "(moved from reports/)", ""]
    return "\n".join(out) + "\n"


def insert_part(text: str, part: str) -> str:
    for h in ("Files\n-----", "Decided\n-------", "Open\n----"):
        i = text.find("\n" + h)
        if i >= 0:
            return text[:i + 1] + part + "\n" + text[i + 1:]
    return text.rstrip("\n") + "\n\n\n" + part


def plan_one(rep: Path, apply: bool, log: list) -> dict:
    level = rep.parent
    titles = questions(owner_face(level))
    moves, faces = {}, {}                                   # old folder -> new folder; face -> text
    for d in sorted(x for x in rep.iterdir() if x.is_dir() and re.match(r"q\d\d", x.name)):
        page = page_of(d)
        if not page:
            continue
        text = page.read_text(encoding="utf-8")
        m = re.search(r"(?m)^answers:\s*(Q\d\d)", text)
        qid = m.group(1) if m else "Q" + d.name[1:3]
        answered = EMPTY not in text and bool(opening(text))
        status = (re.search(r"(?m)^answer-status:\s*(\S+)", text) or [None, "open"])[1]
        home = home_of(level, qid)
        if not home and answered:
            slug = re.sub(r"[^a-z0-9]+", "-", d.name[4:].lower()).strip("-") or "answer"
            name = f"q{qid[1:]}-{slug}"
            if apply:
                for band in ("concept", "level", "guide", "procedure", "server", "run"):   # the first band with room
                    try:
                        home = new_topic.new_topic(level, name, titles.get(qid) or slug.replace("-", " "), band=band,
                                                   feeds=[qid], view="findings", over_limit=True)
                        break
                    except ValueError as err:
                        if "is full" not in str(err):
                            raise
                else:
                    raise SystemExit(f"{level.name}: every band is full; {qid} has no topic")
            else:
                home = level / f"sNN-{name}" / f"sNN-{name}.md"
            log.append(f"    new topic {home.parent.name} for {qid}")
        moves[d] = (home.parent / d.name) if (home and answered) else (level / "_old" / "reports" / d.name)
        log.append(f"  {qid} {d.name}: {'answered' if answered else 'empty'} -> "
                   f"{home.parent.name if home else 'no topic (its Question stays in the register)'}")
        if home and home.is_file():
            t = faces.get(home) or home.read_text(encoding="utf-8")
            t = set_view(set_feeds(t, [qid]))
            if f"{qid} · Answer" not in t:
                t = insert_part(t, answer_part(qid, titles.get(qid, ""), f"{d.name}/{page.name}" if answered else "",
                                               opening(text) if answered else "", status if answered else "open"))
            faces[home] = t
        moves[page] = home if home else owner_face(level)  # the page's links go to its topic face (or the register)
    for f in topics(level):                                 # other faces that only name reports/ in Feeds
        t = faces.get(f) or f.read_text(encoding="utf-8")
        if "reports/" in feeds_of(f):
            faces[f] = set_feeds(t, [])
    return {"level": level, "moves": moves, "faces": faces}


def relink_file(p: Path, plans: list) -> str | None:
    src = p.read_text(encoding="utf-8", errors="ignore")
    if "reports/q" not in src:
        return None

    def sub(m):
        raw = m.group(1)
        for base in (p.parent, *[pl["level"] for pl in plans]):
            tgt = (base / raw).resolve()
            for pl in plans:
                rep = (pl["level"] / "reports").resolve()
                if rep in tgt.parents:
                    rel = tgt.relative_to(rep)
                    folder = rep / rel.parts[0]
                    page = next((k for k in pl["moves"] if k.suffix == ".md" and k.resolve() == tgt), None)
                    if page is not None:
                        new = pl["moves"][page]
                    else:
                        dest = next((v for k, v in pl["moves"].items() if k.resolve() == folder), None)
                        if dest is None:
                            return raw
                        new = dest.joinpath(*rel.parts[1:])
                        if tgt.suffix in (".excalidraw", ".png"):   # a report drawing stays in _old
                            new = pl["level"] / "_old" / "reports" / rel
                    out = os.path.relpath(new, base).replace(os.sep, "/")
                    return out
        return raw
    new = LINK.sub(sub, src)
    if p.name in ("board.md",) or p.suffix == ".md":
        new = re.sub(r"(?m)^(\s+)report: board\.md\n", "", new)
    return new if new != src else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("path", type=Path)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)
    root = a.path.resolve()
    found = list(find_reports(root))
    for rep, ours in found:
        if not ours:
            print(f"⏸️ {rep.relative_to(root)}: a theme Board's own reports/, left for its theme")
    by_project: dict[Path, list] = {}
    for rep, ours in found:
        if ours:
            by_project.setdefault(project_of(rep), []).append(rep)
    for proj, reps in by_project.items():
        log: list[str] = []
        plans = []
        for rep in reps:
            log.append(f"{rep.relative_to(root)}")
            plans.append(plan_one(rep, a.apply, log))
        changed = []
        for p in proj.rglob("*"):
            if (p.is_file() and p.suffix in (".md", ".yaml", ".yml", ".toml", ".py")
                    and not (set(p.relative_to(proj).parts) & SKIP)
                    and not any((pl["level"] / "reports").resolve() in p.resolve().parents for pl in plans)):
                face_text = next((pl["faces"].get(p) for pl in plans if p in pl["faces"]), None)
                if face_text is not None:
                    tmp = p.read_text(encoding="utf-8")
                    p_text = face_text
                else:
                    p_text = None
                new = relink_file(p, plans) if p_text is None else None
                if p_text is not None:
                    newer = LINK.sub(lambda m: m.group(1), p_text)      # faces: links fixed after the write below
                    if a.apply:
                        p.write_text(newer, encoding="utf-8")
                        again = relink_file(p, plans)
                        if again:
                            p.write_text(again, encoding="utf-8")
                    if newer != tmp:
                        changed.append(p)
                elif new is not None:
                    changed.append(p)
                    if a.apply:
                        p.write_text(new, encoding="utf-8")
        log += [f"    edit {c.relative_to(root)}" for c in sorted(changed)]
        for pl in plans:
            rep = pl["level"] / "reports"
            if a.apply:
                old = pl["level"] / "_old" / "reports"
                old.parent.mkdir(exist_ok=True)
                if old.exists():
                    raise SystemExit(f"{old} exists; nothing moved for it")
                shutil.move(str(rep), str(old))
                for src, dest in pl["moves"].items():
                    if src.suffix or "_old" in dest.parts:
                        continue
                    moved = old / src.name
                    dest.mkdir(parents=True, exist_ok=True)
                    for item in list(moved.iterdir()):
                        if item.suffix not in (".excalidraw", ".png"):
                            shutil.move(str(item), str(dest / item.name))
                    for md in dest.rglob("*.md"):                  # its own report drawing stayed in _old
                        t = md.read_text(encoding="utf-8")
                        fixed = re.sub(r"\]\(([\w.-]+\.(?:excalidraw|png))\)", lambda m: "](" + os.path.relpath(
                            moved / m.group(1), md.parent).replace(os.sep, "/") + ")" if (moved / m.group(1)).exists()
                            and not (md.parent / m.group(1)).exists() else m.group(0), t)
                        if fixed != t:
                            md.write_text(fixed, encoding="utf-8")
            log.append(f"    {'moved' if a.apply else 'would move'} {rep.relative_to(root)} -> _old/reports/")
        print("\n".join(log))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
