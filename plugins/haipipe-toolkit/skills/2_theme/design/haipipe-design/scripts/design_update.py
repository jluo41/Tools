"""Bring an older Design Board onto the current names (ref/design-ladder.md), with its Design Method Book.

    python design_ladder.py audit  <design/Design-<name> | design/>              what is old, read-only
    python design_ladder.py update <design/Design-<name> | design/> [--apply]    a dry run unless --apply

What it changes, in order:
    inputs/iN/                      -> inputs/inputs-vN/            (and runs/run-add-inputs-iN -> run-add-inputs-vN)
    jNN_<goal>_<method name>/       -> jNN_<goal>_M0x-<slug>-mK_inputs-vM/   from the face's `method:` and `inputs:` pins
    every file, folder and link that carries an old name, and the words in every text file
    design/DesignMethodBook-<Channel>/   made beside the Board, one method type per method the Jobs pin, each version
                                         the Jobs ran listed unsigned (`mK: ''`): a person signs it

It never rewrites a file whose hash a manifest records (an inputs version's files, a Job's fence), and it checks every
recorded hash again after it has run. It names what git shows as uncommitted in the Board first and changes nothing
else in the Project.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

import yaml

OLD_JOB = re.compile(r"^(j\d+)_([a-z0-9]+(?:-[a-z0-9]+)*)_([a-z0-9]+(?:-[a-z0-9]+)*)$")
NEW_JOB = re.compile(r"^j\d+_[a-z0-9-]+_M\d\d-[a-z0-9-]+-m\d+_inputs-v\d+$")
OLD_INPUTS = re.compile(r"^i(\d+)$")
PIN = re.compile(r"^(M\d\d)\s+(m\d+)$")


def _front(md: Path) -> dict:
    m = re.match(r"(?s)^---\n(.*?)\n---\n", md.read_text(encoding="utf-8", errors="ignore")) if md.is_file() else None
    data = yaml.safe_load(m.group(1)) if m else {}
    return data if isinstance(data, dict) else {}


def boards_of(folder: Path) -> list:
    """The Design Boards at or under a folder: board.md says `board-kind: design-board`."""
    folder = folder.resolve()
    cands = [folder] if (folder / "board.md").is_file() else sorted(p for p in folder.iterdir() if (p / "board.md").is_file())
    return [b for b in cands if re.search(r"(?m)^board-kind:\s*design-board\s*$", (b / "board.md").read_text(encoding="utf-8"))]


def _inputs_new(name: str) -> str:
    m = OLD_INPUTS.match(name.strip())
    return f"inputs-v{m.group(1)}" if m else name.strip()


def plan(board: Path, slug_of) -> dict:
    """What an update would rename and which method versions the Jobs pin. `slug_of(M01)` is the registry slug."""
    jobs, held, methods = [], [], {}
    for j in sorted(p for p in board.iterdir() if p.is_dir() and re.match(r"^j\d+_", p.name)):
        f = _front(j / f"{j.name}.md")
        pin = PIN.match(str(f.get("method", "")).strip())
        if not pin:
            continue
        mid, ver = pin.groups()
        methods.setdefault(mid, set()).add(ver)
        if NEW_JOB.match(j.name):
            continue
        old = OLD_JOB.match(j.name)
        if not old or old.group(3) != slug_of(mid):
            held.append((j.name, "its name is not jNN_<goal name>_<method name>; rename it by hand"))
            continue
        jobs.append((j.name, f"{old.group(1)}_{old.group(2)}_{mid}-{slug_of(mid)}-{ver}_{_inputs_new(str(f.get('inputs', '')))}"))
    idir = board / "inputs"
    inputs = [(p.name, _inputs_new(p.name)) for p in sorted(idir.iterdir()) if p.is_dir() and OLD_INPUTS.match(p.name)] if idir.is_dir() else []
    return {"jobs": jobs, "inputs": inputs, "held": held, "methods": methods}


def _rewrite(text: str, p: dict) -> str:
    for old, new in sorted(p["jobs"], key=lambda x: -len(x[0])):
        text = re.sub(rf"(?<![A-Za-z0-9_-]){re.escape(old)}(?![A-Za-z0-9_-])", new, text)
    for old, new in p["inputs"]:
        n = old[1:]
        text = text.replace(f"run-add-inputs-{old}", f"run-add-inputs-v{n}")
        text = re.sub(rf"(?<![A-Za-z0-9_.-]){old}(?![A-Za-z0-9_-])", new, text)
    return text


def _rename(name: str, p: dict) -> str:
    for old, new in sorted(p["jobs"], key=lambda x: -len(x[0])):
        if old in name:
            return name.replace(old, new)
    for old, new in p["inputs"]:
        if name == old:
            return new
        if name == f"run-add-inputs-{old}":
            return f"run-add-inputs-v{old[1:]}"
    return name


def hashed(board: Path) -> dict:
    """Every file whose hash a manifest records: {path: recorded sha}. These are never rewritten."""
    out = {}
    for man in board.rglob("manifest.yaml"):
        data = yaml.safe_load(man.read_text(encoding="utf-8", errors="ignore")) or {}
        for e in (data.get("files") or []) if isinstance(data, dict) else []:
            if isinstance(e, dict) and e.get("path") and e.get("sha256"):
                out[(man.parent / str(e["path"])).resolve()] = str(e["sha256"])
    return out


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12] if path.is_file() else "—"


def broken_hashes(board: Path) -> list:
    return [str(p) for p, want in hashed(board).items() if want not in ("—", "") and _sha(p) != want]


def _text_files(board: Path, keep: set):
    for f in board.rglob("*"):
        if f.is_symlink() or not f.is_file() or ".git" in f.parts or f.resolve() in keep or f.stat().st_size > 5_000_000:
            continue
        try:
            yield f, f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue


def changes(board: Path, p: dict) -> dict:
    """The paths, links and text files an update would touch (read-only)."""
    keep = set(hashed(board))
    paths = [f for f in board.rglob("*") if ".git" not in f.parts and _rename(f.name, p) != f.name]
    links = [f for f in board.rglob("*") if f.is_symlink() and _rewrite(str(f.readlink()), p) != str(f.readlink())]
    edits = [f for f, t in _text_files(board, keep) if _rewrite(t, p) != t]
    skipped = [f for f in keep if f.is_file() and not f.is_symlink()
               and _rewrite(f.read_text(encoding="utf-8", errors="ignore"), p) != f.read_text(encoding="utf-8", errors="ignore")]
    return {"paths": paths, "links": links, "edits": edits, "skipped": skipped}


def book_path(board: Path) -> Path:
    """The Board's Book: its `method-book:` line, else design/DesignMethodBook-<Channel> from its `channel:`."""
    text = (board / "board.md").read_text(encoding="utf-8")
    m = re.search(r"(?m)^method-book:\s*(\S+)", text)
    if m:
        return board.parent.parent / m.group(1)
    ch = re.search(r"(?m)^channel:\s*([A-Za-z0-9][A-Za-z0-9.-]*)\s*$", text)
    word = ch.group(1) if ch else "Method"
    return board.parent / f"DesignMethodBook-{word.upper() if len(word) <= 3 else word[:1].upper() + word[1:]}"


def book_missing(board: Path, p: dict, slug_of) -> list:
    """The (method type folder name, version) pairs the Jobs pin that the Book does not hold yet."""
    bk, out = book_path(board), []
    for mid in sorted(p["methods"]):
        kind = next(iter(sorted(bk.glob(f"j*_{mid}-{slug_of(mid)}"))), None) if bk.is_dir() else None
        have = (_front(kind / f"{kind.name}.md").get("versions") or {}) if kind else {}
        out += [(mid, v) for v in sorted(p["methods"][mid]) if v not in have]
    return out


def unsigned(board: Path) -> list:
    bk = book_path(board)
    out = []
    for kind in sorted(bk.glob("j*_M*")) if bk.is_dir() else []:
        f = _front(kind / f"{kind.name}.md")
        out += [f'{f.get("method")} {v}' for v, s in (f.get("versions") or {}).items() if not str(s or "").strip()]
    return out


def dirty(board: Path) -> list | None:
    """What git shows as uncommitted in the Board (someone's work in progress); None outside a repository."""
    r = subprocess.run(["git", "status", "--short", "--", "."], cwd=board, capture_output=True, text=True)
    return [l for l in r.stdout.splitlines() if l.strip()] if r.returncode == 0 else None


def audit(folder: Path, slug_of) -> list:
    rows = []
    for b in boards_of(folder):
        p = plan(b, slug_of)
        c = changes(b, p)
        rows += [(b, "names", len(p["jobs"]) + len(p["inputs"]), "update --apply (Jobs M0x-<slug>-mK_inputs-vM, inputs/inputs-vN)"),
                 (b, "by hand", len(p["held"]), "; ".join(f"{n}: {why}" for n, why in p["held"])),
                 (b, "words", len(c["edits"]) + len(c["links"]), "update --apply (the old names in text files and links)"),
                 (b, "book", len(book_missing(b, p, slug_of)), f"update --apply ({book_path(b).name}: a method type per method the Jobs pin)"),
                 (b, "signs", len(unsigned(b)), "a person signs each version on its method type's face (versions:)"),
                 (b, "hashes", len(broken_hashes(b)), "a recorded hash no longer matches its file: read it before anything else")]
    for b, check, n, step in rows:
        print(f"{'✅' if n == 0 else '❗'} {b.name:<44} {check:<8} {n:>4}" + ("" if n == 0 else f"   ▶ {step}"))
    return rows


def update(folder: Path, apply: bool, ladder) -> None:
    """`ladder` is design_ladder (its book and method writers, its registry slugs)."""
    slug_of = lambda mid: ladder.method_card(mid)[0]
    for b in boards_of(folder):
        p = plan(b, slug_of)
        c = changes(b, p)
        wip = dirty(b)
        print(f"{b.name}")
        for old, new in p["inputs"] + p["jobs"]:
            print(f"  {old}  ->  {new}")
        for n, why in p["held"]:
            print(f"  ❗ {n}: {why}")
        need = book_missing(b, p, slug_of)
        print(f"  {len(c['paths'])} names · {len(c['edits'])} text files · {len(c['links'])} links · "
              f"{book_path(b).name}: {', '.join(f'{m} {v}' for m, v in need) or 'nothing to add'}")
        for f in c["skipped"]:
            print(f"  kept as it is (its hash is recorded): {f.relative_to(b)}")
        if wip is None or any(l.startswith("??") and l.rstrip("/").endswith((b.name, ".")) for l in wip):
            print("  ❗ this Board is not in git: an update cannot be undone there; copy the Board first")
        elif wip:
            print(f"  ❗ git shows {len(wip)} uncommitted paths here; they are renamed and reworded with the rest")
        if broken_hashes(b):
            sys.exit(f"  ❗ a recorded hash does not match its file before any change: {broken_hashes(b)[0]}; nothing done")
        if not apply:
            print("  dry run: rerun with --apply")
            continue
        keep = set(hashed(b))
        for f, t in list(_text_files(b, keep)):
            new = _rewrite(t, p)
            if new != t:
                f.write_text(new, encoding="utf-8")
        for l in [f for f in b.rglob("*") if f.is_symlink()]:
            tgt = _rewrite(str(l.readlink()), p)
            if tgt != str(l.readlink()):
                l.unlink()
                l.symlink_to(tgt)
        for f in sorted((f for f in b.rglob("*") if ".git" not in f.parts and _rename(f.name, p) != f.name),
                        key=lambda x: -len(x.parts)):
            dst = f.with_name(_rename(f.name, p))
            if dst.exists():
                sys.exit(f"  ❗ {dst} exists; stopped before renaming {f.name}")
            f.rename(dst)
        made, bk = [], book_path(b)
        if not (bk / "board.md").is_file():
            ladder.book(bk, f"{b.parent.name}/{b.name}", made)
        else:
            ladder.serve(bk, b)
        for n, mid in enumerate(sorted(p["methods"]), 1):
            kind = next(iter(sorted(bk.glob(f"j*_{mid}-{slug_of(mid)}"))), None)
            if kind is None:
                top = max([int(d.name[1:3]) for d in bk.glob("j[0-9][0-9]_*")] or [0])
                kind = bk / f"j{top + 1:02d}_{mid}-{slug_of(mid)}"
            for v in sorted(p["methods"][mid]):
                if v not in (_front(kind / f"{kind.name}.md").get("versions") or {}):
                    ladder.method(kind, v, made)
        bad = broken_hashes(b)
        dead = [str(l.relative_to(b)) for l in b.rglob("*") if l.is_symlink() and not l.exists()]
        print(f"  applied · {sum(bk in Path(m).parents for m in made)} Book files written · recorded hashes: {'all match' if not bad else bad} · "
              f"links: {'all resolve' if not dead else dead}")
        print(f"  next: a person signs {', '.join(unsigned(b)) or 'nothing'} in {bk.name}")
