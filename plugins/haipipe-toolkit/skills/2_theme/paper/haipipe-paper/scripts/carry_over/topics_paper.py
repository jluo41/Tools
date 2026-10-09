#!/usr/bin/env python3
"""topics_paper.py · a paper Board's Story and Ideation into studio topics and Questions (b16 Q04).

    python topics_paper.py <board> --dry-run     print every move, rewrite and new file; change nothing
    python topics_paper.py <board> --apply       do them; keep every changed file's old text for rollback
    python topics_paper.py <board> --rollback    undo the newest run of this script

A paper Board takes b03's shape (haipipe-paper/ref/paper-ladder.md): its thinking is studio topics, its
answers are Questions with reports, and each version tells the story in its own face. The Story and Ideation
Pages stop being Pages; their words move, nearly word for word:

    Story00-<direction>/                -> studio/s01-ideation/              the face keeps the whole page
    Story<L>-<desk>-<idea>/             -> studio/sNN-story-<desk>-<idea>/   the face keeps every division but:
      §3's "#### N · Question" blocks   -> reports/qNN_<name>/ (one each) + a row in board.md ## Questions
      §8 Section Narrative (the current telling only) -> its version's face, ## Narrative (the build reads it)
    a loose studio drawing + its make_*.py -> studio/sNN-<name>/
Then: board.md (story-current, ## Pages loses the Story group, ## Questions gains the rows); each version
paper-build.toml's [pages] order -> the version face; relative links in non-generated .md that point at a
moved file. A builder that finds the Board by counting parents gets one more level.

Every changed file's old text is kept in <board>/.paper-topics-N/<path>.orig with the run's record
(.paper-topics-N.yaml), so --rollback restores it exactly. Tracked paths move with `git mv`, untracked with a
plain move; nothing is committed. Generated and history files are never edited (results/, runs/, delivery/,
draft/records/, draft/previous/, sent/, released/, _archive/).
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("migrate_paper", HERE / "migrate_paper.py")
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

STORY = re.compile(r"^Story(?:[A-Z]|(?!00)\d{2})(?:-|$)")
IDEATION = re.compile(r"^Story00(?:-|$)")
# "#### 3.3 · Question 3 · RQ3": the number after "Question" is what makes it a question block, so a
# "#### 3.7 · Question logic" heading stays in the division as words (it was taken for an 8th question)
QBLOCK = re.compile(r"(?ms)^(####\s+[\d.]+\s*·\s*Question\s+\d+\b.*?)(?=^#{1,4} |\Z)")
QNUM = re.compile(r"·\s*Question\s+(\d+)\b")
DIV = re.compile(r"(?m)^### +(\d+) +· +(.*)$")


def read(p):
    return M.read(p)


def snake(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:48] or "question"


def field(block, name):
    m = re.search(r"(?m)^-\s+\*\*%s\*\*\s*:\s*(.*)$" % re.escape(name), block)
    return m.group(1).strip() if m else ""


def division(text, n):
    """(start, end) of `### n · …` inside ## Content, up to the next ### or ##; None when absent."""
    content = re.search(r"(?ms)^## Content[^\n]*\n(.*?)(?=^## |\Z)", text)
    if not content:
        return None
    for m in DIV.finditer(text, content.start(1), content.end(1)):
        if int(m.group(1)) == n:
            nxt = re.compile(r"(?m)^#{2,3} ").search(text, m.end())
            return m.start(), min(nxt.start() if nxt else len(text), content.end(1))
    return None


# ── the plan ──────────────────────────────────────────────────────────────────────────────────────
def pages_of(board):
    """The Story pages: (folder relative to the Board, stem) from studio/, j00_story/ or A1-Story/."""
    out = []
    for home in ("studio", "j00_story", "A1-Story"):
        d = board / home
        for f in sorted(d.iterdir()) if d.is_dir() else []:
            if f.is_dir() and (f / (f.name + ".md")).is_file() and (STORY.match(f.name) or IDEATION.match(f.name)):
                out.append((f"{home}/{f.name}", f.name))
    return out


def plan(board):
    text = read(board / "board.md")
    current = re.search(r"(?m)^story-current:\s*(\S+)", text)
    current = current.group(1) if current else ""
    pages = pages_of(board)
    if not pages:
        sys.exit("nothing to move: no Story or Ideation Page at this Board")
    if not current:            # no story-current: the telling a version's build reads, else the only telling
        tellings = [s for _, s in pages if not IDEATION.match(s)]
        built = [s for s in (order_story(t) for t in sorted(board.glob(TOMLS))) if s in tellings]
        current = built[0] if built else tellings[0] if len(tellings) == 1 else ""
    taken = {int(m.group(1)) for p in (board / "studio").glob("s[0-9][0-9]-*") for m in [re.match(r"s(\d{2})", p.name)]}
    n, topics = 0, {}
    for rel, stem in sorted(pages, key=lambda x: (not IDEATION.match(x[1]), x[1])):
        n += 1
        while n in taken:
            n += 1
        name = "ideation" if IDEATION.match(stem) else "story-" + stem.split("-", 1)[1] if "-" in stem else "story"
        topics[rel] = f"studio/s{n:02d}-{name}"
    loose = []
    for drawing in sorted((board / "studio").glob("*.excalidraw")):
        n += 1
        while n in taken:
            n += 1
        builder = next((b for b in sorted((board / "studio").glob("make_*.py")) if drawing.name in read(b)), None)
        loose.append((drawing, builder, f"studio/s{n:02d}-{snake(drawing.stem).replace('_', '-')}"))
    moves = []
    for rel, new in topics.items():
        stem = Path(rel).name
        moves.append((rel, new))
        moves.append((f"{new}/{stem}.md", f"{new}/{Path(new).name}.md"))      # after the folder: its face
        # the rest of what a tool finds by the stem (draft/, draft/records/, draft/previous/) follows it, as
        # rename_tasks.py does; generated folders are rebuilt under the new name instead
        for f in sorted((board / rel).rglob("*")):
            sub = f.relative_to(board / rel).as_posix()
            if f.is_file() and stem in f.name and sub != f"{stem}.md" \
                    and not sub.startswith(("delivery/", "results/", "runs/", "notebooks/")):
                moves.append((f"{new}/{sub}", f"{new}/{Path(sub).parent.as_posix()}/"
                              f"{f.name.replace(stem, Path(new).name)}".replace("/./", "/")))
    for drawing, builder, new in loose:
        for f in [drawing, drawing.with_suffix(".png"), builder]:
            if f is not None and f.is_file():
                moves.append((f"studio/{f.name}", f"{new}/{f.name}"))
    # how an old path maps (longest prefix wins): a Story's face, then its folder, then each loose file
    mapping = ([(f"{rel}/{Path(rel).name}.md", f"{new}/{Path(new).name}.md") for rel, new in topics.items()]
               + list(topics.items()) + [(o, n) for o, n in moves if o.startswith("studio/") and o.count("/") == 1])
    return {"current": current, "topics": topics, "loose": loose, "moves": moves, "map": mapping}


def questions(board, P):
    """[(qid, group, name, question, block, telling)]: each §3 question block, the current telling first."""
    ordered = sorted(P["topics"].items(), key=lambda kv: (Path(kv[0]).name != P["current"], kv[0]))
    have = sorted(int(m.group(1)) for p in (board / "reports").glob("q[0-9][0-9]_*") for m in [re.match(r"q(\d{2})", p.name)])
    used, out = set(have), []
    for rel, topic in ordered:
        stem = Path(rel).name
        if IDEATION.match(stem):
            continue
        text = read(board / rel / (stem + ".md"))
        span = division(text, 3)
        for m in QBLOCK.finditer(text[span[0]:span[1]] if span else ""):
            block = m.group(1).rstrip()
            # a question keeps the number its telling gave it (Question 3 -> Q03), so "Q3" in the Story's
            # tables and the meeting notes still names it; a number already taken gets the next free one
            own = QNUM.search(block.split("\n", 1)[0])
            k = int(own.group(1)) if own and int(own.group(1)) not in used else max(used, default=0) + 1
            used.add(k)
            out.append((f"Q{k:02d}", Path(topic).name.split("-", 2)[-1], field(block, "Name") or f"Question {k}",
                        field(block, "Question"), block, topic))
    return out


TOMLS = "j[0-9][0-9]_v*/delivery/paper-build.toml"


def order_story(toml):
    """The Story Page a version's build reads its compile order from (`order = ".../<stem>/<stem>.md"`), or ''."""
    m = re.search(r'(?m)^order\s*=\s*"([^"]+)"', read(toml))
    p = Path(m.group(1)) if m else None
    return p.parent.name if p and p.stem == p.parent.name else ""


def versions_telling(board, stem):
    """Each version whose face `tells:` the stem; a face with no telling yet (`tells: —`, as migrate_paper.py
    writes when board.md has no story-current) tells the Story its build reads the order from."""
    out = []
    for face in sorted(board.glob("j[0-9][0-9]_v*/j[0-9][0-9]_v*.md")):
        tells = re.search(r"(?m)^tells:\s*(\S+)", read(face))
        toml = face.parent / "delivery" / "paper-build.toml"
        unset = not tells or not tells.group(1).strip("—-")
        if face.stem == face.parent.name and (
                (tells and Path(tells.group(1)).name == stem)
                or (unset and toml.is_file() and order_story(toml) == stem)):
            out.append(face.parent)
    return out


# ── the new texts ─────────────────────────────────────────────────────────────────────────────────
def fix_links(text, old_rel, new_rel, board, mapping):
    """Relative Markdown links and a face's `source:`/`tells:` paths, recomputed for the moves."""
    root = board.resolve()
    old_dir = (board / old_rel).parent

    def target(path):
        t = (old_dir / path).resolve()
        try:
            return board / M.mapped(t.relative_to(root).as_posix(), mapping)
        except ValueError:
            return t

    def fix(m):
        pre, link, post = (m.group(1), m.group(2), m.group(3)) if m.group(1) else (m.group(4), m.group(5), "")
        if re.match(r"^([a-z][\w+.-]*:|#|/|<)", link) or "{" in link:
            return m.group(0)
        path, sep, frag = link.partition("#")
        if not path or not (old_dir / path).exists():
            return m.group(0)
        new = Path(os.path.relpath(target(path), (board / new_rel).parent)).as_posix()
        return m.group(0) if new == path else pre + new + sep + frag + post

    out = M.LINK.sub(fix, text)

    def fix_path(m):                                 # source: ../X/X.md · ../Y.md  (relative, in a header)
        parts = []
        for tok in re.split(r"(\s+·\s+|\s+)", m.group(2)):
            path = tok.split("§")[0]
            if path.startswith("..") and (old_dir / path).exists():
                tok = tok.replace(path, Path(os.path.relpath(target(path), (board / new_rel).parent)).as_posix(), 1)
            parts.append(tok)
        return m.group(1) + "".join(parts)
    out = re.sub(r"(?m)^(source:\s*)(.*)$", fix_path, out)
    out = re.sub(r"(?m)^(tells:\s*)(\S+)", lambda m: m.group(1) + M.mapped(m.group(2), mapping), out)
    return out


def rewrites(board, P, Q):
    """{new path: (old path, new text)} for every file whose text changes, and {new path: text} created."""
    mapping = P["map"]
    change, create = {}, {}
    cur_topic = next((t for r, t in P["topics"].items() if Path(r).name == P["current"]), "")

    # each topic's face
    for rel, topic in P["topics"].items():
        stem, name = Path(rel).name, Path(topic).name
        old = f"{rel}/{stem}.md"
        text = read(board / old)
        text = re.sub(r"(?m)\A# +%s\b" % re.escape(stem), "# " + name, text, count=1)
        # a telling feeds its own Questions; Ideation feeds the current telling's (the idea it admitted)
        mine = " ".join(rpath(q) for q in Q if q[5] == (cur_topic if IDEATION.match(stem) else topic))
        head = text.split("\n## ", 1)
        if mine and not re.search(r"(?m)^\*\*Feeds:\*\*", head[0]):     # b03's topic contract: report folders
            head[0] = head[0].rstrip("\n") + f"\n**Feeds:** {mine}\n"
            text = "\n## ".join(head) if len(head) > 1 else head[0]
        span = division(text, 3)
        if span and any(q[5] == topic for q in Q):     # the question blocks leave; the division keeps its words
            body = QBLOCK.sub("", text[span[0]:span[1]]).rstrip() + "\n\n"
            body += "Each question is a Board Question with its report: " + ", ".join(
                f"{q[0]} [{q[2]}](../../reports/{rpath(q)}/{rpath(q)}.md)" for q in Q if q[5] == topic) + ".\n\n"
            text = text[:span[0]] + body + text[span[1]:]
        if stem == P["current"] and versions_telling(board, stem):   # §8 leaves only when a version takes it
            span = division(text, 8)
            if span:
                text = text[:span[0]] + text[span[1]:]
        new = f"{topic}/{name}.md"
        change[new] = (old, fix_links(text, old, new, board, mapping))

    # each report, and its page.toml
    for q in Q:
        r = rpath(q)
        create[f"reports/{r}/{r}.md"] = (
            f"# {q[2]}\nstate: ⬜ OPEN · moved from {Path(q[5]).name} §3 (b16 Q04); not answered yet\n"
            f"answers: {q[0]}\nanswer-status: open\n\n## Opening\n\n{q[3] or q[2]}\n\n"
            f"**Where this Page sits:** [{q[0]} · {q[2]}](../../board.md) · its telling: "
            f"[{Path(q[5]).name}](../../{q[5]}/{Path(q[5]).name}.md).\n\n## Content\n\n### 1 · The question\n\n"
            f"{q[4]}\n\n### 2 · Answer\n\nNot answered yet. The evidence and work it needs are in its telling's "
            "Evidence Basis, Discovery and Task Roadmaps.\n")
        create[f"reports/{r}/page.toml"] = f'version = 1\nsource = "{r}.md"\ntitle = "{q[2]}"\n'

    # board.md: story-current, ## Pages without the Story group, ## Questions with the rows
    text = read(board / "board.md")
    if cur_topic:
        if re.search(r"(?m)^story-current:", text):
            text = re.sub(r"(?m)^(story-current:\s*)\S+", lambda m: m.group(1) + Path(cur_topic).name, text)
        else:                  # the paper workbench reads the current telling from this line
            text = re.sub(r"(?m)^(dialect:.*\n)", lambda m: m.group(1) + f"story-current: {Path(cur_topic).name}\n",
                          text, count=1)
    text = re.sub(r"(?ms)^### +[^\n]*·\s*(?:%s)\b[^\n]*\n.*?(?=^### |^## |\Z)" % "|".join(
        re.escape(h) for h in {"studio", "j00_story", "A1-Story"}), "", text)
    rows = "".join(f"- id: {q[0]}\n  title: {yaml_s(q[2])}\n  question: {yaml_s(q[3] or q[2])}\n  group: {q[1]}\n"
                   f"  report: reports/{rpath(q)}/{rpath(q)}.md\n" for q in Q)
    if rows:
        if re.search(r"(?m)^## Questions", text):
            text = re.sub(r"(?ms)(^## Questions.*?```ya?ml\n.*?)(```)", lambda m: m.group(1) + rows + m.group(2), text, count=1)
        else:
            block = f"## Questions\n\n```yaml\nquestions:\n{rows}```\n\n"
            text = re.sub(r"(?m)^## Links", block + "## Links", text, count=1) if "\n## Links" in text else text + "\n" + block
    change["board.md"] = ("board.md", fix_links(text, "board.md", "board.md", board, mapping))

    # the current telling's §8 -> each version that tells it; its build reads the order there
    cur_page = next((r for r in P["topics"] if Path(r).name == P["current"]), None)
    if cur_page:
        story = read(board / cur_page / (P["current"] + ".md"))
        span = division(story, 8)
        narrative = DIV.sub("", story[span[0]:span[1]], count=1).strip() if span else ""
        for v in versions_telling(board, P["current"]):
            face = f"{v.name}/{v.name}.md"
            vt = change.get(face, (face, read(board / face)))[1]
            vt = re.sub(r"(?m)^(tells:\s*)[—-]\s*$", lambda m: m.group(1) + cur_page, vt, count=1)
            if narrative and not re.search(r"(?m)^## Narrative", vt):
                cut = re.search(r"(?m)^## (Questions|Log)", vt)
                add = f"## Narrative\n\nMoved from {Path(cur_topic).name} §8 (b16 Q04): how this version tells the story, in reading order.\n\n{narrative}\n\n"
                vt = vt[:cut.start()] + add + vt[cut.start():] if cut else vt.rstrip("\n") + "\n\n" + add
            change[face] = (face, fix_links(vt, face, face, board, mapping))
            # each Section's story-row follows its row: `<Story> §8.3 / <stem>` -> `<version> ## Narrative / <stem>`
            # (paper_ladder.py task's shape), the Story version it was bound to kept under the topic's name
            for sf in sorted(v.glob("*/*.md")):
                srel = sf.relative_to(board).as_posix()
                if sf.stem != sf.parent.name or srel in change:
                    continue
                st = read(sf)
                nt = re.sub(r"(?m)^(story-row:\s*)%s\s*§8[\d.]*\s*/" % re.escape(P["current"]),
                            lambda m: f"{m.group(1)}{v.name} ## Narrative /", st)
                nt = re.sub(r"(?m)^(story-row:.*?)\b%s\b" % re.escape(P["current"]),
                            lambda m: m.group(1) + Path(cur_topic).name, nt)
                if nt != st:
                    change[srel] = (srel, fix_links(nt, srel, srel, board, mapping))
            toml = v / "delivery" / "paper-build.toml"
            if toml.is_file():
                tt = re.sub(r'(?m)^(order\s*=\s*")[^"]*(")', lambda m: m.group(1) + f"../{v.name}.md" + m.group(2), read(toml))
                tt = tt.replace(cur_page + "/", cur_topic + "/")
                change[toml.relative_to(board).as_posix()] = (toml.relative_to(board).as_posix(), tt)

    # every other non-generated .md with a link that moves
    for f in sorted(board.rglob("*.md")):
        rel = f.relative_to(board).as_posix()
        new = M.mapped(rel, mapping)
        if M.skipped(rel) or new in change or rel.startswith("."):
            continue
        t = read(f)
        nt = fix_links(t, rel, new, board, mapping)
        if nt != t:
            change[new] = (rel, nt)

    # a builder that finds the Board by counting parents: one level deeper now
    for drawing, builder, topic in P["loose"]:
        if builder is not None:
            t = read(builder)
            nt = re.sub(r"HERE\.parents\[(\d+)\]", lambda m: f"HERE.parents[{int(m.group(1)) + 1}]", t)
            if nt != t:
                change[f"{topic}/{builder.name}"] = (f"studio/{builder.name}", nt)
    return change, create


def rpath(q):
    return f"q{q[0][1:]}_{snake(q[2])}"


def yaml_s(s):
    return "'" + (s or "").replace("'", "''") + "'"


# ── the three modes ───────────────────────────────────────────────────────────────────────────────
def runs(board):
    found = [f for f in board.glob(".paper-topics-*.yaml") if re.fullmatch(r"\.paper-topics-\d+\.yaml", f.name)]
    return sorted(found, key=lambda f: int(re.findall(r"\d+", f.name)[-1]))         # a rolled-back record is not one


def build(board):
    P = plan(board)
    Q = questions(board, P)
    change, create = rewrites(board, P, Q)
    return P, Q, change, create


def dry_run(board):
    P, Q, change, create = build(board)
    print(f"Board: {board.name}\n\nmoves")
    for o, n in P["moves"]:
        print(f"  {o:64} -> {n}  ({'git mv' if M.tracked(board, o) else 'mv'})")
    print("\nQuestions")
    for q in Q:
        print(f"  {q[0]}  group {q[1]:32} {q[2]}")
    print("\nfiles rewritten")
    for new, (old, text) in change.items():
        before = read(board / old)
        print(f"  {new}  ({len(before.splitlines())} → {len(text.splitlines())} lines)")
    print("\nfiles created")
    for new in create:
        print(f"  {new}")
    print(f"\n{len(P['moves'])} moves · {len(change)} files rewritten · {len(create)} created · nothing changed (dry run)")


def apply(board):
    P, Q, change, create = build(board)
    k = 1 + max([int(re.match(r"\.paper-topics-(\d+)", f.name).group(1)) for f in board.glob(".paper-topics-*")] or [0])
    keep = board / f".paper-topics-{k}"
    keep.mkdir()
    status = M.git(board, "status", "--porcelain", check=False).stdout.splitlines()
    for new, (old, _) in change.items():          # the old text, kept by its new path (.orig: no reader scans it)
        dst = keep / (new + ".orig")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(board / old, dst)
    done = []
    for o, n in P["moves"]:
        if (board / o).exists():
            done.append({"old": o, "new": n, "how": M.move(board, o, n)})
    for new, (_, text) in change.items():
        (board / new).write_text(text, encoding="utf-8")
    for new, text in create.items():
        (board / new).parent.mkdir(parents=True, exist_ok=True)
        (board / new).write_text(text, encoding="utf-8")
    record = {"run": date.today().isoformat(), "tool": "haipipe-paper/scripts/carry_over/topics_paper.py", "moves": done,
              "rewritten": sorted(change), "created": sorted(create), "kept": keep.name,
              "questions": [{"id": q[0], "group": q[1], "title": q[2]} for q in Q], "git_status_before": status,
              "roll_back_first": "any record newer than this one"}
    (board / f".paper-topics-{k}.yaml").write_text(M.dump(record), encoding="utf-8")
    print(f"{len(done)} moves · {len(change)} files rewritten · {len(create)} created · record .paper-topics-{k}.yaml; "
          "nothing committed")


def rollback(board):
    if not runs(board):
        sys.exit("stop: no .paper-topics-N.yaml at this Board")
    path = runs(board)[-1]
    rec = M.load(read(path))
    keep = board / rec["kept"]
    for new in rec.get("created") or []:
        f = board / new
        if f.is_file():
            f.unlink()
        for d in [f.parent] + list(f.parent.parents):
            if d == board or not d.is_dir() or any(d.iterdir()):
                break
            d.rmdir()
    for new in rec.get("rewritten") or []:
        shutil.copy2(keep / (new + ".orig"), board / new)
    for m in reversed(rec.get("moves") or []):
        M.move(board, m["new"], m["old"])
    for d in sorted({Path(m["new"]).parts[0] + "/" + Path(m["new"]).parts[1] for m in rec.get("moves") or []
                     if len(Path(m["new"]).parts) > 2}, reverse=True):
        if (board / d).is_dir() and not any((board / d).iterdir()):
            (board / d).rmdir()
    shutil.rmtree(keep)
    path.rename(board / f"{path.stem}.rolled-back-{date.today().isoformat()}.yaml")
    print(f"rolled back {len(rec.get('moves') or [])} moves, {len(rec.get('rewritten') or [])} rewrites, "
          f"{len(rec.get('created') or [])} created files")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("board", type=Path)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--rollback", action="store_true")
    a = ap.parse_args(argv)
    board = a.board.resolve()
    if not (board / "board.md").is_file():
        sys.exit(f"stop: {board.name} has no board.md")
    (rollback if a.rollback else apply if a.apply else dry_run)(board)


if __name__ == "__main__":
    main()
