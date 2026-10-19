"""One round of a Word file we share: numbered versions kept here, one copy in OneDrive, pictures of each version,
and the file read back when someone changed it (b32 s41-D21, D23; JL 261019: "the render haved changed a while, and
we need to read it again, and start another round of changing, and then send it back").

A lane folder (`delivery/word/` or `delivery/<jNN>/<tNN>/word/`) keeps every state of one file as `<name>-v<N>.docx`
with its PDF; a version is never written over. OneDrive keeps one copy under the plain name, the one people edit.
Each version's pages are rendered to `../render/<name>-v<N>/p-<N>.png`, the pictures a Section canvas puts on its
left ("the file today"). Was b21_event_cgm's `delivery/word_versions.py` (2026-10-14), made shared here.

    python word_round.py --word-dir <dir> --name <name> [--onedrive <file>] status
    python word_round.py ... pull              read back: OneDrive's file as the next version, rendered, its new comments
    python word_round.py ... adopt <glob>      number the build(s) a builder just wrote into the lane folder
    python word_round.py ... import <file>     save a dated copy as the next version, keeping its date
    python word_round.py ... render <N>        the pages of version N as pictures
    python word_round.py ... push <N>          put version N in OneDrive, only at a person's word

push refuses when OneDrive holds edits no version has (pull first), when N is not newer than what OneDrive holds, or
when N lacks a comment someone else wrote in OneDrive's copy; --force overrides, only at a person's word. push adds
a `draft` row to the Block's delivery/delivery.md and pull a `back` row; only a person writes `sent`.
Paths printed and written are relative to the SPACE (the folder holding env.sh).
"""
import argparse
import datetime
import filecmp
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DPI = 110                                       # a page picture: readable on a canvas, small on disk
READ_REVISE = Path(__file__).resolve().parents[3] / "excalidraw/excalidraw-draft/ref"


class Round:
    def __init__(self, word_dir, name, onedrive=None, me=("JL", "Junjie Luo"), reader=""):
        self.word = Path(word_dir).resolve()
        self.name, self.me, self.reader = name, set(me), reader
        self.onedrive = Path(onedrive).resolve() if onedrive else None
        self.space = next(p for p in self.word.parents if (p / "env.sh").is_file())
        self.render_dir = self.word.parent / "render"

    def rel(self, p):
        return Path(p).resolve().relative_to(self.space)

    def versions(self):
        """[(N, path)] of the numbered Word files, oldest first."""
        found = [(int(m[1]), p) for p in self.word.glob(f"{self.name}-v*.docx")
                 if (m := re.search(r"-v(\d+)\.docx$", p.name))]
        return sorted(found)

    def held(self, path):
        """The version whose bytes equal this file, or None."""
        return next((n for n, p in self.versions() if filecmp.cmp(p, path, shallow=False)), None)

    def delivery_md(self):
        """The Block's table of sends: the delivery.md in the nearest folder named delivery above the lane."""
        d = next((p for p in [self.word, *self.word.parents] if p.name == "delivery"), None)
        return d / "delivery.md" if d and (d / "delivery.md").is_file() else None

    def row(self, text, src, state):
        md = self.delivery_md()
        if md is None:
            print("no delivery/delivery.md above the lane: no row written")
            return
        line = f"| {datetime.date.today():%y%m%d} | {text} | `{src.relative_to(md.parent)}` and `.pdf` | {state} |\n"
        md.write_text(md.read_text(encoding="utf-8").rstrip("\n") + "\n" + line, encoding="utf-8")

    def print_pdf(self, docx):
        """Its PDF beside it, dated as the Word file is, so the Delivery view orders the version by the Word file."""
        sys.path.insert(0, str(READ_REVISE))
        from read_revise import office_pdf
        pdf = docx.with_suffix(".pdf")
        office_pdf(docx, pdf)
        st = docx.stat()
        os.utime(pdf, (st.st_atime, st.st_mtime))

    def add(self, src, move=False):
        """Save a Word file as the next version (moving a build, copying anything else), with its PDF."""
        if (n := self.held(src)) is not None:
            print(f"{src.name} is already v{n}")
            return n, False
        n = (self.versions()[-1][0] if self.versions() else 0) + 1
        dst = self.word / f"{self.name}-v{n}.docx"
        if move:
            shutil.move(src, dst)
            if src.with_suffix(".pdf").is_file():
                shutil.move(src.with_suffix(".pdf"), dst.with_suffix(".pdf"))
        else:
            shutil.copy2(src, dst)
        if not dst.with_suffix(".pdf").is_file():
            self.print_pdf(dst)
        print(f"v{n}: {self.rel(dst)} ({when(dst)}, from {src.name})")
        return n, True

    def render(self, n):
        """The pages of version n as pictures, one per page; returns them."""
        docx = dict(self.versions()).get(n)
        if docx is None:
            raise SystemExit(f"no v{n} in {self.rel(self.word)}")
        pdf = docx.with_suffix(".pdf")
        if not pdf.is_file():
            self.print_pdf(docx)
        out = self.render_dir / f"{self.name}-v{n}"
        out.mkdir(parents=True, exist_ok=True)
        for old in out.glob("p-*.png"):
            old.unlink()
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", str(pdf), str(out / "p")], check=True)
        pages = sorted(out.glob("p-*.png"))
        print(f"v{n}: {len(pages)} pages in {self.rel(out)}/")
        return pages

    def pull(self):
        """Read back: OneDrive's copy, if someone changed it, saved as the next version, rendered, its new comments."""
        if self.onedrive is None or not self.onedrive.is_file():
            raise SystemExit(f"no OneDrive copy at {self.onedrive}")
        before = self.versions()
        n, new = self.add(self.onedrive)
        if not new:
            print("nothing came back: OneDrive holds a version we have")
            return n
        self.render(n)
        prev = before[-1][1] if before else None
        fresh = sorted(c for c in comments(self.onedrive) - (comments(prev) if prev else set()) if c[0] not in self.me)
        print(f"{len(fresh)} new comments by others:" if fresh else "no new comments by others")
        for a, t in fresh:
            print(f"  {a}: {t[:90]}")
        who = ", ".join(sorted({a for a, _ in fresh})) or "someone"
        self.row(f"back from {who}: OneDrive `{self.onedrive.name}`, saved {when(self.onedrive)} as v{n}, "
                 f"{len(fresh)} new comments (`word_round.py pull`)", self.word / f"{self.name}-v{n}.docx", "back")
        return n

    def push(self, n, force=False):
        src = dict(self.versions()).get(n)
        if src is None:
            raise SystemExit(f"no v{n} in {self.rel(self.word)}")
        if self.onedrive is None:
            raise SystemExit("no OneDrive copy named (--onedrive)")
        if self.onedrive.is_file():
            now = self.held(self.onedrive)
            if now is None and not force:
                raise SystemExit("OneDrive holds edits no version has: pull first, then build on that version")
            if now is not None and n <= now and not force:
                raise SystemExit(f"OneDrive holds v{now}; v{n} is not newer")
            lost = sorted(c for c in comments(self.onedrive) - comments(src) if c[0] not in self.me)
            if lost and not force:
                raise SystemExit(f"v{n} lacks {len(lost)} comments others wrote in OneDrive's copy:\n" +
                                 "\n".join(f"  {a}: {t[:70]}" for a, t in lost))
        shutil.copyfile(src, self.onedrive)
        assert filecmp.cmp(src, self.onedrive, shallow=False)
        print(f"OneDrive: {self.rel(self.onedrive)} is now v{n}")
        self.row(f"{self.reader or 'the reader'}: OneDrive `{self.onedrive.name}`, v{n} placed "
                 f"{datetime.datetime.now():%H:%M} (`word_round.py push {n}`)", src, "draft")

    def status(self):
        for n, p in self.versions():
            pics = self.render_dir / f"{self.name}-v{n}"
            seen = f"{len(list(pics.glob('p-*.png')))} pages rendered" if pics.is_dir() else "not rendered"
            print(f"v{n}  {when(p)}  {p.stat().st_size:>9,} bytes  {seen}")
        if self.onedrive is None:
            return
        if not self.onedrive.is_file():
            print(f"OneDrive: no {self.onedrive.name}")
        elif (n := self.held(self.onedrive)) is not None:
            print(f"OneDrive: holds v{n} (saved there {when(self.onedrive)})")
        else:
            print(f"OneDrive: changed since the last version (saved there {when(self.onedrive)}); pull reads it back")


def when(path):
    return datetime.datetime.fromtimestamp(Path(path).stat().st_mtime).strftime("%Y-%m-%d %H:%M")


def comments(path):
    """{(author, text)} of the Word comments in a file."""
    with zipfile.ZipFile(path) as z:
        if "word/comments.xml" not in z.namelist():
            return set()
        root = ET.fromstring(z.read("word/comments.xml"))
    return {(c.get(W + "author") or "", " ".join("".join(t.text or "" for t in c.iter(W + "t")).split()))
            for c in root.iter(W + "comment")}


def main(argv=None, **fixed):
    """The command line; a Block's own script passes its lane, name and OneDrive copy as `fixed`."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    if not fixed:
        ap.add_argument("--word-dir", required=True, type=Path, help="the lane folder holding <name>-v<N>.docx")
        ap.add_argument("--name", required=True, help="the file's plain name, without -v<N>.docx")
        ap.add_argument("--onedrive", type=Path, help="the one shared copy people edit")
        ap.add_argument("--reader", default="", help="who the file goes to, for the delivery.md row")
    ap.add_argument("verb", nargs="?", default="status", choices=["status", "pull", "adopt", "import", "render", "push"])
    ap.add_argument("arg", nargs="?", help="adopt: a glob · import: a file · render, push: N")
    ap.add_argument("--force", action="store_true", help="with push: skip the checks (only at a person's word)")
    a = ap.parse_args(argv)
    r = Round(**fixed) if fixed else Round(a.word_dir, a.name, a.onedrive, reader=a.reader)
    if a.verb == "adopt":
        for p in sorted(r.word.glob(a.arg or "*.docx"), key=lambda p: p.stat().st_mtime):
            if not re.search(r"-v\d+\.docx$", p.name):
                r.add(p, move=True)
    elif a.verb == "import":
        r.add(Path(a.arg).resolve())
    elif a.verb == "pull":
        r.pull()
    elif a.verb == "render":
        r.render(int(a.arg) if a.arg else r.versions()[-1][0])
    elif a.verb == "push":
        r.push(int(a.arg), a.force)
    r.status()


if __name__ == "__main__":
    main()
