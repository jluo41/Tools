#!/usr/bin/env python3
"""rename_tasks.py · name one paper version and its Tasks by series (haipipe-paper/ref/paper-ladder.md).

    python rename_tasks.py <board> --date MMDD --dry-run    print every rename and line edit; change nothing
    python rename_tasks.py <board> --date MMDD --apply      do them, then write <board>/.paper-tasks.yaml
    python rename_tasks.py <board> --rollback               reverse them from <board>/.paper-tasks.yaml

JL 261007: "no more S-xxx … just use MMDD". A version is named for the day it is sent, and its Tasks by series:

    jNN_v<N>_<desk>/                           -> jNN_v<MMDD>_<desk>/          the version, dated
    S-<desk>-Main-Abstract/                    -> t00_abstract/                Main, the abstract first
    S-<desk>-Main-<N>-<Title>/                 -> t0<N>_<title>/               Main, in reading order (t00-t19)
    S-<desk>-Appendix-<L>-<Title>/             -> t2<i>_<title>/               Appendix, A = t21 (t20-t29)
    RD<NN>-<desk>-<event>-<YYYYMMDD>/          -> reports/qNN_<event>-<MMDD>/  a comments batch: a report of type
                                                                               comments (page-type: comments)

JL 261007: "comments … are a special type of report … it should be in the reports/ but you can say its type is
the Comments". A batch is not a Task: it moves into the version's reports/, numbered after the reports already
there; t3N_ is for letters (t31 cover letter, t32 response). Its references are edited by stem; a relative link
written as a path (../RD01-…/) changes depth and is listed for a person to check.

A Page's stem is its folder name, so a rename renames the Page: its face <stem>.md and every source file named
for it (draft/<stem>-…, draft/records/<stem>-…). Then it edits, line by line, every source text file in the
Board that names an old stem or the old version (board.md, the Story Pages' rows, the faces, the plans, the
comments batch, paper-build.toml), and records each edit. Generated and history files are never edited:
results/, notebooks/, runs/, sent/, released/, board/, _archive/, draft/records/ and draft/previous/ keep their
words, and a Page's delivery/ is rebuilt under its new name by `page.py export` (its old-named files stay until
that lane rebuilds whole). Tracked paths move with `git mv`; nothing is committed.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

MAP = ".paper-tasks.yaml"
VERSION = re.compile(r"^(j\d{2})_v([^_]+)_(.+)$")
ABSTRACT = re.compile(r"^S-[A-Za-z0-9]+-Main-Abstract$")
MAIN = re.compile(r"^S-[A-Za-z0-9]+-Main-(\d+)-(.+)$")
APPENDIX = re.compile(r"^S-[A-Za-z0-9]+-Appendix-([A-Z])-(.+)$")
BATCH = re.compile(r"^(?:RD|CM)(\d+)-[A-Za-z0-9]+-(.+)-\d{4}(\d{4})$")
TEXT = {".md", ".toml", ".yaml", ".yml", ".txt", ".json", ".py", ".sh"}
SKIP = {"results", "notebooks", "runs", "sent", "released", "board", "_archive", ".git", "__pycache__",
        "node_modules", "delivery"}
SKIP_PAIRS = {("draft", "records"), ("draft", "previous")}
KEEP_IN_DELIVERY = {"paper-build.toml"}           # a source that lives in delivery/


def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def new_name(old):
    """The series name for an old Page folder, or None when it is not a Section or a batch."""
    if ABSTRACT.match(old):
        return "t00_abstract"
    m = MAIN.match(old)
    if m:
        return f"t{int(m.group(1)):02d}_{slug(m.group(2))}"
    m = APPENDIX.match(old)
    if m:
        return f"t{20 + ord(m.group(1)) - ord('A') + 1}_{slug(m.group(2))}"
    m = BATCH.match(old)
    if m:                                                  # a report; plan() numbers it after the version's reports
        return f"reports/qNN_{slug(m.group(2))}-{m.group(3)}"
    return None


def number_reports(v, pages):
    """Give each batch the next free qNN in the version's reports/."""
    taken = {int(m.group(1)) for d in (v / "reports").glob("q*_*") if (m := re.match(r"q(\d+)_", d.name))}
    out, n = [], max(taken, default=0)
    for old, new in pages:
        if new.startswith("reports/qNN_"):
            n += 1
            new = new.replace("qNN_", f"q{n:02d}_")
        out.append((old, new))
    return out


def read(p):
    try:
        return p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def skipped(rel):
    parts = Path(rel).parts
    if Path(rel).name in KEEP_IN_DELIVERY:
        parts = tuple(x for x in parts if x != "delivery")
    dirs = parts[:-1]
    return bool(SKIP & set(dirs)) or any(pair == dirs[i:i + 2] for i in range(len(dirs)) for pair in SKIP_PAIRS)


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


def plan(board, mmdd):
    """{'version': (old, new), 'pages': [(old, new)], 'files': [(old rel, new rel)], 'tokens': {old: new}}."""
    versions = [d for d in sorted(board.iterdir()) if d.is_dir() and VERSION.match(d.name)]
    if len(versions) != 1:
        sys.exit(f"stop: expected one jNN_v…_<desk>/ version at the Board, found {[v.name for v in versions]}")
    v = versions[0]
    n, _, desk = VERSION.match(v.name).groups()
    v_new = f"{n}_v{mmdd}_{desk}" if mmdd else v.name
    pages = number_reports(v, [(d.name, new_name(d.name)) for d in sorted(v.iterdir()) if d.is_dir() and new_name(d.name)])
    news = [b for _, b in pages]
    if len(set(news)) != len(news):
        sys.exit(f"stop: two Pages would take one name: {sorted(x for x in news if news.count(x) > 1)}")
    files = []
    for old, new in pages:
        for f in sorted((v / old).rglob("*")):
            rel_in = f.relative_to(v / old).as_posix()
            # names follow the stem everywhere a tool looks one up (the face, draft/, draft/records/, draft/previous/);
            # generated folders are rebuilt under the new name instead (delivery/, results/), and runs/ is named by Run
            if f.is_file() and old in f.name and not rel_in.startswith(("delivery/", "results/", "runs/", "notebooks/")):
                files.append((f"{v_new}/{new}/{rel_in}", f"{v_new}/{new}/{Path(rel_in).parent.as_posix()}/"
                              f"{f.name.replace(old, Path(new).name)}".replace("/./", "/")))
    tokens = {old: Path(new).name for old, new in pages}           # a Page is named by its stem, wherever it sits
    if v_new != v.name:
        tokens[v.name] = v_new
        if (v / f"{v.name}.md").is_file():                      # the version's face follows its folder
            files.insert(0, (f"{v_new}/{v.name}.md", f"{v_new}/{v_new}.md"))
    return {"version": (v.name, v_new), "pages": pages, "files": files, "tokens": tokens}


def line_edits(board, P):
    """Every source text line naming an old token: (file after the renames, line, old line, new line)."""
    pat = re.compile(r"(?<![\w-])(" + "|".join(re.escape(t) for t in sorted(P["tokens"], key=len, reverse=True))
                     + r")(?!\w|-(?![a-z]))")   # a stem alone, or a name made from it (<stem>-draft-v1.0.md)
    v_old, v_new = P["version"]
    pages = dict(P["pages"])
    renamed = {a: b for a, b in P["files"]}
    edits = []
    for f in sorted(board.rglob("*")):
        rel = f.relative_to(board).as_posix()
        if not f.is_file() or (f.suffix not in TEXT and f.name != ".gitignore") or skipped(rel) or rel.startswith(".paper-"):
            continue
        # where the file will be after the moves
        parts = rel.split("/")
        if parts[0] == v_old:
            parts[0] = v_new
            if len(parts) > 1 and parts[1] in pages:
                parts[1] = pages[parts[1]]
        after = "/".join(parts)
        after = renamed.get(after, after)
        for i, line in enumerate(read(f).splitlines()):
            new = pat.sub(lambda m: P["tokens"][m.group(1)], line)
            if new != line:
                edits.append((after, i + 1, line, new))
    return edits


def set_line(path, n, want_old, new):
    lines = path.read_text(encoding="utf-8").split("\n")
    if n > len(lines) or lines[n - 1] != want_old:
        return False
    lines[n - 1] = new
    path.write_text("\n".join(lines), encoding="utf-8")
    return True


def dump(obj):
    import yaml
    return yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, width=220)


def dry_run(board, mmdd):
    P = plan(board, mmdd)
    edits = line_edits(board, P)
    print(f"Board: {board.name}\n\nversion\n  {P['version'][0]} -> {P['version'][1]}\n\nPages")
    for a, b in P["pages"]:
        print(f"  {a:55} -> {b}")
    print(f"\nfiles named for their Page: {len(P['files'])}")
    for a, b in P["files"]:
        print(f"  {a.split('/', 2)[-1]:70} -> {b.split('/')[-1]}")
    by_file = {}
    for f, *_ in edits:
        by_file[f] = by_file.get(f, 0) + 1
    print(f"\nline edits: {len(edits)} in {len(by_file)} file(s)")
    for f, n in sorted(by_file.items()):
        print(f"  {n:4}  {f}")
    print(f"\n1 version · {len(P['pages'])} Pages · {len(P['files'])} files · {len(edits)} line edits · "
          "nothing changed (dry run)")


def apply(board, mmdd):
    if (board / MAP).exists():
        sys.exit(f"stop: {MAP} exists, this version was renamed already (--rollback first)")
    P = plan(board, mmdd)
    edits = line_edits(board, P)
    status = git(board, "status", "--porcelain", check=False).stdout.splitlines()
    done = []
    v_old, v_new = P["version"]
    if v_new != v_old:
        done.append({"old": v_old, "new": v_new, "how": move(board, v_old, v_new)})
    for old, new in P["pages"]:
        done.append({"old": f"{v_new}/{old}", "new": f"{v_new}/{new}",
                     "how": move(board, f"{v_new}/{old}", f"{v_new}/{new}")})
    for old_rel, new_rel in P["files"]:
        done.append({"old": old_rel, "new": new_rel, "how": move(board, old_rel, new_rel)})
    applied = []
    for f, n, old, new in edits:
        if set_line(board / f, n, old, new):
            applied.append({"file": f, "line": n, "old": old, "new": new})
        else:
            print(f"  ! {f}:{n} changed under the run; left as it is")
    record = {"renamed": date.today().isoformat(), "tool": "haipipe-paper/scripts/carry_over/rename_tasks.py",
              "note": "roll this back before rolling back .paper-moves.yaml (migrate_paper.py), which names the old folders",
              "tokens": P["tokens"], "moves": done, "edits": applied, "git_status_before": status}
    (board / MAP).write_text(dump(record), encoding="utf-8")
    print(f"{len(done)} renames · {len(applied)} line edits · record {MAP}; nothing committed")


def rollback(board):
    import yaml
    path = board / MAP
    if not path.is_file():
        sys.exit(f"stop: no {MAP} at this Board")
    rec = yaml.safe_load(read(path))
    for e in reversed(rec.get("edits") or []):
        if not set_line(board / e["file"], e["line"], e["new"], e["old"]):
            print(f"  ! {e['file']}:{e['line']} changed since the rename; left as it is")
    for m in reversed(rec.get("moves") or []):
        move(board, m["new"], m["old"])
    path.rename(board / f".paper-tasks.rolled-back-{date.today().isoformat()}.yaml")
    print(f"rolled back {len(rec.get('moves') or [])} renames and {len(rec.get('edits') or [])} line edits")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("board", type=Path)
    ap.add_argument("--date", help="MMDD: the day the version is sent (the version folder takes v<MMDD>)")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--rollback", action="store_true")
    a = ap.parse_args(argv)
    board = a.board.resolve()
    if not (board / "board.md").is_file():
        sys.exit(f"stop: {board.name} has no board.md")
    if a.date and not re.fullmatch(r"\d{4}", a.date):
        sys.exit("stop: --date takes MMDD, four digits")
    if a.rollback:
        rollback(board)
    elif a.apply:
        apply(board, a.date)
    else:
        dry_run(board, a.date)


if __name__ == "__main__":
    main()
