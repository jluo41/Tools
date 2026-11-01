"""Move every sNN out of studio/ to beside its Jobs (JL 261031: "please update all the /studio folders to put them
under the block folder"; JL 261030: "we just have sNN, along side with jNN, to make it visible directly").

    python studio_move.py <path> [<path> ...]            the plan and every path it rewrites, nothing written
    python studio_move.py <path> [<path> ...] --apply    move, then rewrite

<path> is a SPACE, a Project or a Block. For each `<level>/studio/<sNN>-<topic>/`:

    move     to `<level>/sNN-<topic>/` (an `sNN_<topic>` takes the hyphen, its face and drawing too)
    links    a link `<prefix>studio/<sNN>-<topic>` becomes `<prefix>sNN-<topic>` only when its path, read from the
             file's folder or one above it, leads to a topic that moves (a held topic, another Block's studio/ and
             a template's `studio/sNN-<topic>` stay as written); inside the moved folder a
             relative path that climbed past studio/ climbs one level less (`../../j01_x` becomes `../j01_x`); a loose
             file left in studio/ reaches a moved topic through `../`
    builders a `.py` in the moved folder that climbs from its own file (`HERE.parents[5]`, `Path(__file__)...
             .parent.parent`) climbs one level less, so it still lands on the same folder
    studio/  left holding only `_groups.txt`, it goes: the order moves to `<level>/_studio_groups.txt`
             (frame.group_file reads it there); anything else loose keeps studio/ (a mind map, a question map, draw/)

Result, receipt and archive folders are never walked (result/, results/, passes/, _runs/, delivery/, _old/,
_legacy/, notebooks/: ladder.py's NO_RELINK; the one exception is a five-part topic's `result/first-drawing.excalidraw`,
the kept input its drawing is rebuilt from, whose links to moved topics follow them before the rebuild), and
generated files are never rewritten (AGENTS rule 6): `.html`, `.pptx`, `.png`, a file headed GENERATED FILE, and a
drawing an earlier script wrote (its `source`). Their generators are rerun after the move: the
five-part drawing (studio_update.draw), a report drawing (build_report_drawing.py), and each moved mind map's page
(mindmap.py render). /haipipe-project update runs this as its `studio` step.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
SNN = re.compile(r"^s\d{2}[-_]")
SKIP = {".git", "node_modules", "_WorkSpace", "__pycache__", ".venv", "venv", ".mypy_cache", ".pytest_cache",
        "result", "results", "passes", "_runs", "delivery", "_old", "_legacy", "notebooks"}   # + ladder.py NO_RELINK
TEXT = {".md", ".py", ".yaml", ".yml", ".json", ".txt", ".excalidraw", ".toml", ".sh", ".ps1", ".do", ".csv", ".tsv",
        ".js", ".css", ".ini", ".cfg", ".rst", ".bib"}
NEVER = {".html", ".htm", ".pptx", ".png", ".jpg", ".pdf", ".docx", ".svg"}
LOOSE_GOES = {"_groups.txt", ".DS_Store"}                   # studio/ holding only these goes with its topics
UP = re.compile(r"(?<![\w.~])\.\.(?:/\.\.)*(?=/|[\"'\s)\]>,`]|$)")
CHAIN = re.compile(r"(?P<base>Path\(__file__\)|\b[A-Za-z_]\w*\b)(?P<res>(?:\.resolve\(\))?)"
                   r"(?P<chain>(?:\.resolve\(\)|\.parent\b(?!s)|\.parents\[\d+\])+)")
ASSIGN = re.compile(r"^\s*(?P<name>[A-Za-z_]\w*)\s*=\s*(?P<expr>Path\(__file__\)(?:\.resolve\(\))?"
                    r"(?:\.resolve\(\)|\.parent\b(?!s)|\.parents\[\d+\])*)\s*(?:#.*)?$")
LINK = re.compile(r"(?<![\w.~-])(?P<pre>/?(?:[\w.~-]+/)*)studio/(?P<name>s\d\d[-_][A-Za-z0-9][\w-]*)"
                  r"(?=[/`'\"\s)\]>,:;#.]|$)")
ALIAS = re.compile(r"^\s*(?P<name>[A-Za-z_]\w*)\s*=\s*(?P<src>[A-Za-z_]\w*)\s*(?:#.*)?$")


def walk(root: Path):
    """(dir, subdirs, files) under root, never into a symlink, a skipped folder, a dot folder (a .worktrees/
    checkout, a .paper-sweep/ backup) or another SPACE."""
    for d, subs, files in os.walk(root):
        p = Path(d)
        subs[:] = sorted(s for s in subs if s not in SKIP and not s.startswith(".") and not s.endswith(".egg-info")
                         and not (p / s).is_symlink()
                         and not (s.endswith("-SPACE") and p != root))
        yield p, subs, files


def hyphen(name: str) -> str:
    return name[:3] + "-" + name[4:] if name[3] == "_" else name


def plan(roots: list[Path]) -> list[tuple[Path, Path]]:
    moves = []
    for root in roots:
        for p, subs, _ in walk(root):
            if p.name != "studio":
                continue
            for s in subs:
                if SNN.match(s):
                    moves.append((p / s, p.parent / hyphen(s)))
            subs[:] = [s for s in subs if not SNN.match(s)]
    return moves


def generated(f: Path, text: str) -> bool:
    if f.suffix in NEVER or "GENERATED FILE" in text[:400]:
        return True
    if f.suffix == ".excalidraw":
        try:
            src = str(json.loads(text).get("source") or "")
        except Exception:
            return False
        return src.startswith("haipipe") or "five_parts" in src or "studio_update" in src
    return False


class Mover:
    def __init__(self, moves: list[tuple[Path, Path]]):
        self.moves = moves
        self.old = {o: n for o, n in moves}
        self.names = {o.name: n.name for o, n in moves}
        self.studios = {o.parent for o, _ in moves}
        self.mismatch, self.stale = [], []

    def remap(self, path: str) -> str:
        """Where a path (lexical, absolute) lands after the moves."""
        p = Path(path)
        for o, n in self.old.items():
            if p == o or o in p.parents:
                return str(n / p.relative_to(o))
        return path

    # ── text ──────────────────────────────────────────────────────────────────────────────────────────────────
    def lands(self, f: Path, pre: str, name: str) -> Path | None:
        """The moving topic a link `<pre>studio/<name>` in file f leads to, read from f's folder or any folder above
        it (a page often writes its paths from its Block or its SPACE); None when it leads to no moving topic."""
        rel = pre.lstrip("/") + "studio/" + name
        for base in [f.parent, *f.parent.parents]:
            hit = Path(os.path.normpath(base / rel))
            if hit in self.old:
                return hit
        return None

    def names_out(self, text: str, f: Path) -> str:
        """`<pre>studio/<sNN>-<topic>` becomes `<pre>sNN-<topic>` when, and only when, it leads to a moving topic."""
        if not self.old:
            return text

        def fix(m):
            hit = self.lands(f, m.group("pre"), m.group("name"))
            return m.group("pre") + self.old[hit].name if hit else m.group(0)
        return LINK.sub(fix, text)

    def climb(self, text: str, old_file: Path, new_file: Path, topic_old: Path) -> str:
        """A relative path in a moved file that climbed past studio/ climbs one level less."""
        depth = len(old_file.parent.relative_to(topic_old).parts)       # 0: the file sits in the sNN itself

        def fix(m):
            n = m.group(0).count("..")
            if n <= depth + 1:
                return m.group(0)
            new = "/".join([".."] * (n - 1))
            before = os.path.normpath(old_file.parent / m.group(0))
            after = os.path.normpath(new_file.parent / new)
            if self.remap(before) != after:
                self.mismatch.append(f"{new_file}: {m.group(0)} -> {new}")
            return new
        return UP.sub(fix, text)

    def loose(self, text: str) -> str:
        """A file left in studio/ reaches a moved sibling through ../ now."""
        for o, n in self.names.items():
            text = re.sub(r"(?<![\w./-])" + re.escape(o) + r"(?=/|[\"')\]\s#]|$)", "../" + n, text)
        return text

    def builders(self, text: str, old_file: Path, topic_old: Path) -> str:
        """Path(__file__)-rooted climbs in a moved .py climb one level less when they reached past studio/."""
        level = {"__file__": len(old_file.relative_to(topic_old).parts)}  # steps from the file up to the sNN

        def steps(chain: str) -> int:
            return sum(1 for _ in re.finditer(r"\.parent\b(?!s)", chain)) + sum(
                int(k) + 1 for k in re.findall(r"\.parents\[(\d+)\]", chain))

        for line in text.splitlines():
            m = ASSIGN.match(line)
            if m:
                lvl = level["__file__"] - steps(m.group("expr"))
                if lvl >= 0:
                    level[m.group("name")] = lvl
            m = ALIAS.match(line)
            if m and m.group("src") in level and m.group("src") != "__file__":
                level[m.group("name")] = level[m.group("src")]

        def fix(m):
            base = "__file__" if m.group("base") == "Path(__file__)" else m.group("base")
            if base not in level:
                return m.group(0)
            chain = m.group("res") + m.group("chain")
            if level[base] - steps(chain) >= -1:                       # inside the sNN, or studio/ itself (now the level)
                return m.group(0)
            ks = list(re.finditer(r"\.parents\[(\d+)\]", chain))
            if ks and int(ks[-1].group(1)) >= 1:
                k = ks[-1]
                chain = chain[:k.start()] + f".parents[{int(k.group(1)) - 1}]" + chain[k.end():]
            elif ks:
                chain = chain[:ks[-1].start()] + ".parent" + chain[ks[-1].end():]
                chain = re.sub(r"\.parent\b(?!s)", "", chain, count=1) if chain.count(".parent") > 1 else chain
                chain = chain.replace(".parents[0]", ".parent")
            else:
                i = chain.rfind(".parent")
                chain = chain[:i] + chain[i + len(".parent"):]
            return m.group("base") + chain

        return CHAIN.sub(fix, text)


def text_files(roots: list[Path]):
    for root in roots:
        for p, _, files in walk(root):
            for f in files:
                q = p / f
                if q.suffix in TEXT and not q.is_symlink():
                    try:
                        if q.stat().st_size < 8_000_000:
                            yield q
                    except OSError:
                        pass


def rewrite(mv: Mover, f: Path, text: str, topic_old: Path | None, new_file: Path) -> str:
    out = mv.names_out(text, f)
    if topic_old:
        out = mv.climb(out, f, new_file, topic_old)
        if f.suffix == ".py":
            out = mv.builders(out, f, topic_old)
    elif f.parent in mv.studios:
        out = mv.loose(out)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--sweep", nargs="*", type=Path, default=[], help="more folders whose links to rewrite")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)
    roots = [p.resolve() for p in a.paths]
    moves = [(o, n) for o, n in plan(roots)]
    clash = [(o, n) for o, n in moves if n.exists()]
    moves = [(o, n) for o, n in moves if not n.exists()]
    mv = Mover(moves)
    print(f"{len(moves)} sNN to move, {len(clash)} held (a folder of that name is already beside the Jobs)")
    for o, n in clash:
        print(f"  ❗ held {o}")

    edits, regen = {}, set()
    for f in text_files(roots + [p.resolve() for p in a.sweep]):
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        topic_old = next((o for o in (f.parents[i] for i in range(min(6, len(f.parents)))) if o in mv.old), None)
        if not topic_old and f.parent not in mv.studios and "studio/" not in text:
            continue
        new_file = mv.old[topic_old] / f.relative_to(topic_old) if topic_old else f
        if generated(f, text):
            if mv.old and (mv.names_out(text, f) != text or topic_old and UP.search(text)):
                regen.add(topic_old or f)
            continue
        out = rewrite(mv, f, text, topic_old, new_file)
        if out != text:
            edits[f] = (new_file, topic_old)

    for f, (n, _) in sorted(edits.items()):
        print(f"  ✎ {n}")
    for m in mv.mismatch:
        print(f"  ❗ climb lands elsewhere: {m}")
    print(f"{len(edits)} files rewritten, {len(mv.mismatch)} climbs land elsewhere, {len(regen)} generated to rerun")
    if not a.apply:
        return 0

    for f, (n, topic_old) in edits.items():        # rewrite in place first, then move: the paths are the old ones
        text = f.read_text(encoding="utf-8")       # read again just before writing: another session may have edited it
        f.write_text(rewrite(mv, f, text, topic_old, n), encoding="utf-8")
    for o, n in moves:
        o.rename(n)
        if n.name != o.name:                       # sNN_x took the hyphen: its own files follow
            for q in sorted(n.iterdir()):
                if q.name.startswith(o.name):
                    q.rename(n / (n.name + q.name[len(o.name):]))
    for studio in sorted(mv.studios):
        left = {q.name for q in studio.iterdir()}
        if left <= LOOSE_GOES:
            groups = studio / "_groups.txt"
            if groups.is_file():
                target = studio.parent / "_studio_groups.txt"
                if target.is_file():
                    keep = target.read_text(encoding="utf-8").splitlines()
                    keep += [x for x in groups.read_text(encoding="utf-8").splitlines() if x not in keep]
                    target.write_text("\n".join(keep) + "\n", encoding="utf-8")
                    groups.unlink()
                else:
                    groups.rename(target)
            (studio / ".DS_Store").unlink(missing_ok=True)
            studio.rmdir()
    kept = sorted(s for s in mv.studios if s.is_dir())
    print(f"moved {len(moves)}; studio/ removed from {len(mv.studios) - len(kept)} levels, kept at {len(kept)} "
          "(it still holds loose items)")
    return rerun([mv.old.get(p, p) for p in sorted(regen)], [n for _, n in moves], mv)


def rerun(stale: list[Path], moved: list[Path], mv: Mover | None = None) -> int:
    """The generators whose output named a moved path: a five-part drawing (its kept first drawing, now its source,
    names its topics without studio/ first), a report drawing, and every moved topic's mind map page."""
    import subprocess
    import studio_update as su
    report = HERE.parents[1] / "haipipe-report" / "scripts" / "build_report_drawing.py"
    bad = 0
    for p in stale:
        try:
            if p.is_dir():
                kept = p / "result" / "first-drawing.excalidraw"
                if kept.is_file():
                    text = kept.read_text(encoding="utf-8")       # read as if it sat where it was written
                    kept.write_text(mv.names_out(text, kept) if mv else text, encoding="utf-8")
                su.draw(p)
            elif p.suffix == ".excalidraw" and "build_report_drawing" in p.read_text(encoding="utf-8"):
                subprocess.run([sys.executable, str(report), str(p.parent)], check=True, capture_output=True)
        except (Exception, SystemExit) as err:
            bad += 1
            print(f"  ❗ rerun {p}: {str(err)[-160:]}")
    maps = [m for t in moved for m in t.glob("*.mindmap.md")]
    for m in maps:
        out = subprocess.run([sys.executable, str(su.MINDMAP), "render", str(m)], capture_output=True)
        bad += bool(out.returncode)
    print(f"reran {len(stale)} generated drawings and {len(maps)} mind map pages, {bad} failed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
