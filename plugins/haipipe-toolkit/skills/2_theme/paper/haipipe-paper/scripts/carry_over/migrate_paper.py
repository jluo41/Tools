#!/usr/bin/env python3
"""migrate_paper.py · move one paper Board onto the ladder (haipipe-paper/ref/paper-ladder.md).

    python migrate_paper.py <board> --dry-run     print every move and edit; change nothing
    python migrate_paper.py <board> --apply       do them, then write the run's moves map, <board>/.paper-moves[-N].yaml
    python migrate_paper.py <board> --rollback    reverse the newest moves map (roll back newest first)

Folders move, names stay (no Page stem changes, so every Run, receipt and Story row still finds its Page):

    A1-Story/ (or an earlier j00_story/)         -> studio/   then topics_paper.py: topics + Questions
    Ba-<desk>-Main/ · Bb-<desk>-Appendix/ ·      -> jNN_v<N>_<desk>/          one version Job per desk, in
      Bc-<desk>-Round/                                                        group-letter order; Rounds stay Tasks
    delivery/                                    -> j<NN>_v<N>_<desk>/delivery/   the desk paper-build.toml names

Then it edits, line by line, and records each edit: board.md's `## Pages` headings; paper-build.toml's
[pages] paths (and the folder names in its comments); each relative Markdown link whose source or target
moved, in a non-generated .md; .gitignore lines anchored on a moved path (a copy for the new path). It writes
each version's face, <job>/<job>.md (send · desk · venue · state · tells · an empty ## Questions register).

Uncommitted work never blocks the move: the pre-move `git status --porcelain` is kept in the moves map;
tracked paths move with `git mv` (their edits travel with them), untracked ones with a plain move. Nothing
is committed. Generated and history files are never edited: results/, notebooks/, delivery/, runs/,
draft/records/, draft/previous/, sent/, released/, board/, _archive/ (their links stay as written).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

MAP = ".paper-moves.yaml"
STORY_GROUP = re.compile(r"^A\d?-Story$|^A1-|^j00_story$")
STORY_HOME = "studio"          # the Story is the Board's, beside its drawings and reports (JL 261007), not a Job
DESK_GROUP = re.compile(r"^B([a-z])-(.+)-(Main|Appendix|Round)$")
HEADING = re.compile(r"^### +([^·]+?) +· +([\w.-]+)(.*)$")
LINK = re.compile(r"(\]\()([^)\s]+)(\))|^(\[[^\]]+\]:\s*)(\S+)", re.M)
SKIP = {"results", "notebooks", "delivery", "runs", "sent", "released", "board", "_archive", ".git",
        "__pycache__", "node_modules"}
SKIP_PAIRS = {("draft", "records"), ("draft", "previous")}
JUNK = {".DS_Store"}


# ── the plan ──────────────────────────────────────────────────────────────────────────────────────
def pages_groups(text):
    """[(line index, label, folder, rest)] for each `### <label> · <folder>` heading under `## Pages`."""
    out, inside = [], False
    for i, line in enumerate(text.splitlines()):
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith("pages")
            continue
        m = HEADING.match(line) if inside else None
        if m:
            out.append((i, m.group(1).strip(), m.group(2), m.group(3)))
    return out


def toml_desk(board):
    m = re.search(r'(?m)^desk\s*=\s*"([^"]+)"', read((tomls(board) or [board / "delivery" / "paper-build.toml"])[0]))
    return m.group(1).lower() if m else ""


def plan(board):
    """Every move, as (old, new) paths relative to the Board, and the group renames."""
    groups = sorted(p.name for p in board.iterdir() if p.is_dir())
    story = [g for g in groups if STORY_GROUP.match(g)]
    desks = []                                      # desks in the order of their first group letter
    for g in groups:
        m = DESK_GROUP.match(g)
        if m and m.group(2) not in desks:
            desks.append(m.group(2))
    taken = {int(p.name[1:3]) for p in board.iterdir() if p.is_dir() and re.match(r"^j\d{2}_", p.name)}
    renames, versions = {}, {}
    for g in story:
        renames[g] = STORY_HOME
    n = 0
    for desk in desks:
        n += 1
        while n in taken:
            n += 1
        versions[desk] = f"j{n:02d}_v{n}_{desk.lower()}"
        for g in groups:
            m = DESK_GROUP.match(g)
            if m and m.group(2) == desk:
                renames[g] = versions[desk]
    moves = []
    for old, new in renames.items():
        for child in sorted((board / old).iterdir()):
            if child.name in JUNK:
                continue
            moves.append((f"{old}/{child.name}", f"{new}/{child.name}"))
    if (board / "delivery").is_dir() and versions:
        want = toml_desk(board)
        home = next((v for d, v in versions.items() if d.lower() == want), next(iter(versions.values())))
        moves.append(("delivery", f"{home}/delivery"))
    if not moves:
        return {"renames": renames, "versions": versions, "moves": moves, "map": []}
    news = [n for _, n in moves]
    clash = sorted({n for n in news if news.count(n) > 1} | {n for n in news if (board / n).exists()})
    if clash:
        sys.exit("stop: these new paths would collide: " + ", ".join(clash))
    # what paths map through: each moved child, then a renamed group's own folder (longest prefix wins)
    return {"renames": renames, "versions": versions, "moves": moves, "map": moves + list(renames.items())}


def mapped(rel, moves):
    """A Board-relative path after the moves (the longest moved prefix wins)."""
    rel = Path(os.path.normpath(rel)).as_posix()
    for old, new in sorted(moves, key=lambda m: -len(m[0])):
        if rel == old or rel.startswith(old + "/"):
            return new + rel[len(old):]
    return rel


def read(p):
    try:
        return p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def skipped(rel):
    parts = Path(rel).parts[:-1]
    return bool(SKIP & set(parts)) or any(pair == parts[i:i + 2] for i in range(len(parts)) for pair in SKIP_PAIRS)


def heading_edits(board, P):
    """board.md: a renamed group's heading names its new folder; a desk's later groups become a bold label
    inside its version, so their Pages stay listed under it."""
    lines = read(board / "board.md").splitlines()
    edits, seen = [], set()
    for i, label, folder, rest in pages_groups("\n".join(lines)):
        new = P["renames"].get(folder)
        if not new:
            continue
        if new in seen:
            part = DESK_GROUP.match(folder).group(3) if DESK_GROUP.match(folder) else folder
            line = f"**{part}** (was `{folder}`)"
        elif new == STORY_HOME:
            seen.add(new)
            line = f"### Story · {new}{rest}"
        else:
            seen.add(new)
            line = f"### J{new[1:3]} · {new}{rest}"
        edits.append(("board.md", i + 1, lines[i], line))
    return edits


def tomls(board):
    """Each paper-build.toml: the Board's delivery/, or a version Job's (jNN_v…/delivery/)."""
    return [t for t in [board / "delivery" / "paper-build.toml"] + sorted(board.glob("j[0-9][0-9]_v*/delivery/paper-build.toml"))
            if t.is_file()]


def toml_edits(board, P):
    return [e for src in tomls(board) for e in _toml_edits(board, P, src)]


def _toml_edits(board, P, src):
    """One paper-build.toml, read where it is now and edited where it lands: its [pages] paths, and the old
    folder names in its comments."""
    new_rel = mapped(src.relative_to(board).as_posix(), P["map"])
    new_dir = (board / new_rel).parent
    edits, table = [], ""
    for i, line in enumerate(read(src).splitlines()):
        t = re.match(r"^\s*\[([^\]]+)\]", line)
        if t:
            table = t.group(1).strip()
            continue
        m = re.match(r'^(\s*\w+\s*=\s*")([^"]+)(".*)$', line)
        if table == "pages" and m:
            target = mapped(os.path.relpath((src.parent / m.group(2)).resolve(), board.resolve()), P["map"])
            value = Path(os.path.relpath(board / target, new_dir)).as_posix()
            if value != m.group(2):
                edits.append((new_rel, i + 1, line, m.group(1) + value + m.group(3)))
        elif line.lstrip().startswith("#"):
            new = line
            for old, ren in P["renames"].items():
                new = new.replace(old + "/", ren + "/")
            if new != line:
                edits.append((new_rel, i + 1, line, new))
    return edits


def link_edits(board, P):
    """Each relative Markdown link in a non-generated .md whose source or target moved:
    (new file, line, old line, new line), and the count of links already broken before the move."""
    edits, broken = [], 0
    root = board.resolve()
    for f in sorted(board.rglob("*.md")):
        rel = f.relative_to(board).as_posix()
        if skipped(rel):
            continue
        new_rel = mapped(rel, P["map"])
        text = read(f)
        changed = []
        for i, line in enumerate(text.splitlines()):
            def fix(m):
                nonlocal broken
                pre, link, post = (m.group(1), m.group(2), m.group(3)) if m.group(1) else (m.group(4), m.group(5), "")
                if re.match(r"^([a-z][\w+.-]*:|#|/|<)", link) or "{" in link:
                    return m.group(0)
                path, sep, frag = link.partition("#")
                if not path:
                    return m.group(0)
                target = (f.parent / path).resolve()
                if not target.exists():
                    broken += 1
                    return m.group(0)
                try:
                    t_rel = mapped(target.relative_to(root).as_posix(), P["map"])
                    new_target = board / t_rel
                except ValueError:                  # a link out of the Board keeps its target
                    new_target = target
                new_link = Path(os.path.relpath(new_target, (board / new_rel).parent)).as_posix()
                if path.endswith("/") and not new_link.endswith("/"):
                    new_link += "/"
                return m.group(0) if new_link == path else pre + new_link + sep + frag + post
            new_line = LINK.sub(fix, line)
            if new_line != line:
                changed.append((new_rel, i + 1, line, new_line))
        edits += changed
    return edits, broken


def gitignore_edits(board, P):
    """A .gitignore line anchored on a moved path gets a twin for the new path (the old one is kept)."""
    gi = board / ".gitignore"
    adds = []
    for line in read(gi).splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "!")) or "/" not in s.rstrip("/"):
            continue
        new = mapped(s.lstrip("/"), P["map"])
        if new != s.lstrip("/") and new not in read(gi):
            adds.append(new)
    return adds


def face_edits(board, P):
    """An existing version face's `tells:` path follows the Story it names."""
    edits = []
    for face in sorted(board.glob("j[0-9][0-9]_v*/j[0-9][0-9]_v*.md")):
        if face.stem != face.parent.name:
            continue
        rel = face.relative_to(board).as_posix()
        for i, line in enumerate(read(face).splitlines()):
            m = re.match(r"^(tells:\s*)(\S+)(.*)$", line)
            if m and mapped(m.group(2), P["map"]) != m.group(2):
                edits.append((mapped(rel, P["map"]), i + 1, line, m.group(1) + mapped(m.group(2), P["map"]) + m.group(3)))
    return edits


def faces(board, P):
    """Each version's face (D6): {path: text}, for a version that has none."""
    text = read(board / "board.md")
    current = re.search(r"(?m)^story-current:\s*(\S+)", text)
    story = STORY_HOME if STORY_HOME in P["renames"].values() else ""
    toml = read((tomls(board) or [board / "delivery" / "paper-build.toml"])[0])
    venue = (re.search(r'(?m)^venue_label\s*=\s*"([^"]+)"', toml) or re.search(r'(?m)^venue_profile\s*=\s*"([^"]+)"', toml))
    out = {}
    for desk, job in P["versions"].items():
        face = f"{job}/{job}.md"
        if (board / face).exists():
            continue
        batches = sorted(n.split("/")[-1] for o, n in P["moves"] if n.startswith(job + "/")
                         and re.match(r"^(RD|CM)\d", n.split("/")[-1]))
        state = f"under review · {batches[-1]}" if batches else "drafting"
        tells = f"{story}/{current.group(1)}" if story and current else "—"
        out[face] = (f"# {job} · version {int(job.split('_v')[1].split('_')[0])} of the paper\n\n"
                     f"send: {job}\ndesk: {desk}\nvenue: {(venue.group(1) if venue and venue.group(1) else desk)}\n"
                     f"state: {state}\ntells: {tells}\nfrom: none (the first send)\n\n"
                     "## Questions\n\n```yaml\nquestions: []\n```\n")
    return out


def receipts(board, P):
    """Run receipts under a moved folder that name an old folder: left as history, counted."""
    n = 0
    olds = tuple(g + "/" for g in P["renames"])
    for old, _ in P["moves"]:
        for f in list((board / old).rglob("runs/*.md")) + list((board / old).rglob("results/*/runtime.yaml")):
            if any(o in read(f) for o in olds):
                n += 1
    return n


def git(board, *args, check=True):
    return subprocess.run(["git", "-C", str(board), *args], capture_output=True, text=True, check=check)


def tracked(board, rel):
    r = git(board, "ls-files", "--", rel, check=False)
    return r.returncode == 0 and bool(r.stdout.strip())


def move(board, old, new):
    (board / new).parent.mkdir(parents=True, exist_ok=True)
    if tracked(board, old):
        git(board, "mv", old, new)
        return "git mv"
    shutil.move(str(board / old), str(board / new))
    return "mv"


def set_line(path, n, want_old, new):
    lines = path.read_text(encoding="utf-8").split("\n")
    if lines[n - 1] != want_old:
        return False
    lines[n - 1] = new
    path.write_text("\n".join(lines), encoding="utf-8")
    return True


def dump(obj):
    try:
        import yaml
        return yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, width=200)
    except ImportError:
        return json.dumps(obj, indent=1, ensure_ascii=False)


def load(text):
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        return json.loads(text)


# ── the three modes ───────────────────────────────────────────────────────────────────────────────
def maps(board):
    """This Board's moves maps, oldest first: .paper-moves.yaml, then .paper-moves-2.yaml, …"""
    found = [board / MAP] if (board / MAP).is_file() else []
    more = [f for f in board.glob(".paper-moves-*.yaml") if re.fullmatch(r"\.paper-moves-\d+\.yaml", f.name)]
    return found + sorted(more, key=lambda f: int(re.findall(r"\d+", f.name)[-1]))     # a rolled-back record is not one


def next_map(board):
    have = maps(board)
    return board / (MAP if not have else f".paper-moves-{len(have) + 1}.yaml")


def build(board):
    P = plan(board)
    if not P["moves"]:
        sys.exit("nothing to move: no A1-Story/, j00_story/ or B<x>-<desk>-<part>/ group at this Board")
    links, broken = link_edits(board, P)
    edits = heading_edits(board, P) + toml_edits(board, P) + face_edits(board, P) + links
    return P, edits, broken, gitignore_edits(board, P), faces(board, P), receipts(board, P)


def dry_run(board):
    P, edits, broken, ignores, made, rec = build(board)
    print(f"Board: {board.name}")
    print("\nmoves")
    for old, new in P["moves"]:
        print(f"  {old:70} -> {new}  ({'git mv' if tracked(board, old) else 'mv'})")
    for title, keep in (("board.md ## Pages headings", lambda e: e[0] == "board.md"),
                        ("paper-build.toml", lambda e: e[0].endswith("paper-build.toml")),
                        ("links", lambda e: e[0] != "board.md" and not e[0].endswith("paper-build.toml"))):
        rows = [e for e in edits if keep(e)]
        print(f"\n{title}: {len(rows)} line(s)")
        for f, n, old, new in rows:
            print(f"  {f}:{n}\n    - {old.strip()[:160]}\n    + {new.strip()[:160]}")
    print(f"\nlinks broken before the move (left as they are): {broken}")
    print(f"\n.gitignore lines added: {ignores or 'none'}")
    for face, text in made.items():
        print(f"\nversion face {face}:\n" + "\n".join("  " + l for l in text.splitlines()))
    print(f"\nRun receipts that name an old folder, left as history: {rec}")
    print(f"\n{len(P['moves'])} moves · {len(edits)} line edits · {len(made)} face(s) · nothing changed (dry run)")


def apply(board):
    P, edits, broken, ignores, made, rec = build(board)
    status = git(board, "status", "--porcelain", check=False).stdout.splitlines()
    done = []
    for old, new in P["moves"]:
        done.append({"old": old, "new": new, "how": move(board, old, new)})
    removed = []
    for old in P["renames"]:
        d = board / old
        for j in JUNK:
            (d / j).unlink(missing_ok=True)
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()
            removed.append(old)
    applied = []
    for f, n, old, new in edits:
        if set_line(board / f, n, old, new):
            applied.append({"file": f, "line": n, "old": old, "new": new})
        else:
            print(f"  ! {f}:{n} changed under the run; left as it is")
    if ignores:
        gi = board / ".gitignore"
        gi.write_text(read(gi).rstrip("\n") + "\n# moved onto the ladder (migrate_paper.py)\n"
                      + "\n".join(ignores) + "\n", encoding="utf-8")
    written = {}
    for face, text in made.items():
        (board / face).write_text(text, encoding="utf-8")
        written[face] = hashlib.sha256(text.encode()).hexdigest()
    record = {"migrated": date.today().isoformat(), "tool": "haipipe-paper/scripts/carry_over/migrate_paper.py",
              "renames": P["renames"], "moves": done, "removed_dirs": removed, "edits": applied,
              "gitignore_added": ignores, "faces": written, "links_broken_before": broken,
              "receipts_left_as_history": rec, "git_status_before": status}
    out = next_map(board)
    record["roll_back_first"] = "any record newer than this one (a later moves map, or another tool's)"
    out.write_text(dump(record), encoding="utf-8")
    print(f"{len(done)} moves · {len(applied)} line edits · {len(written)} face(s) · {len(ignores)} .gitignore "
          f"line(s) · moves map {out.name}; nothing committed")


def rollback(board):
    if not maps(board):
        sys.exit(f"stop: no {MAP} at this Board")
    path = maps(board)[-1]                          # the newest run first
    rec = load(read(path))
    for e in reversed(rec.get("edits") or []):
        if not set_line(board / e["file"], e["line"], e["new"], e["old"]):
            print(f"  ! {e['file']}:{e['line']} changed since the move; left as it is")
    for face, digest in (rec.get("faces") or {}).items():
        f = board / face
        if f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest() == digest:
            f.unlink()
        elif f.is_file():
            print(f"  ! {face} was edited since the move; kept")
    if rec.get("gitignore_added"):
        gi = board / ".gitignore"
        drop = set(rec["gitignore_added"]) | {"# moved onto the ladder (migrate_paper.py)"}
        gi.write_text("\n".join(l for l in read(gi).splitlines() if l not in drop) + "\n", encoding="utf-8")
    for d in rec.get("removed_dirs") or []:
        (board / d).mkdir(exist_ok=True)
    for m in reversed(rec.get("moves") or []):
        move(board, m["new"], m["old"])
    for new in sorted(set((rec.get("renames") or {}).values())):
        d = board / new
        if d.is_dir() and not any(p for p in d.iterdir() if p.name not in JUNK):
            shutil.rmtree(d)
    path.rename(board / f"{path.stem}.rolled-back-{date.today().isoformat()}.yaml")
    print(f"rolled back {len(rec.get('moves') or [])} moves and {len(rec.get('edits') or [])} line edits")


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
