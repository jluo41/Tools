#!/usr/bin/env python3
"""latex_diff.py · the paper's change between two LaTeX builds, as one PDF (haipipe-paper-assemble 0.20.0).

A co-author reads what changed since the version they saw: deleted words struck through in red, added words
underlined in blue, in the venue's own LaTeX layout. Both sides are LaTeX rooms (a folder with master.tex,
sections/, appendices/, displays/, reference.bib), normally the build that was sent and the build that follows.

  .venv/bin/python <skill>/scripts/latex_diff.py --old <room or git:REV:path/to/room> --new <room> --out <diff.pdf>
      [--master master.tex] [--engine xelatex] [--notes notes.yaml]

--old git:<rev>:<room path> takes the room as it was at a commit (the round that was sent; delivery/ is tracked).
Each room is copied to a scratch folder with relative \\input/\\includegraphics paths made absolute and flattened by
latexdiff (--flatten). References are not diffed: BibTeX builds one list from both rounds' entries. Figures show their
new version only; equations are marked whole. It reads the two rooms and writes only --out (and its .tex beside
it); it never edits a room. Exit 1, with the log tail, when the diff does not compile.

--notes takes a YAML file `notes: [{at: <text>, note: <why>, who?: <name>, comment?: <their words>}]`: each note is printed in a widened right margin beside
the first place its `at` text occurs in the diff, numbered in reading order with the same number in the text, so a
co-author reads why a change was made next to the change. With `comment`, the note first quotes a reviewer's comment
(`who`) in orange, then the reply. A note whose `at` is not found is reported and skipped.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd, cwd, quiet=True):
    return subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE if quiet else None,
                          stderr=subprocess.STDOUT if quiet else None, text=True)


def materialize(spec: str, into: Path) -> Path:
    """A room as a folder: a path, or git:<rev>:<path> checked out from history."""
    if spec.startswith("git:"):
        _, rev, path = spec.split(":", 2)
        src = Path(path).resolve()
        top = Path(run(["git", "rev-parse", "--show-toplevel"], src if src.is_dir() else src.parent).stdout.strip())
        rel = src.relative_to(top)
        files = run(["git", "ls-tree", "-r", "--name-only", rev, "--", str(rel)], top).stdout.split()
        if not files:
            raise SystemExit(f"latex_diff: no files under {rel} at {rev}")
        for f in files:
            dest = into / Path(f).relative_to(rel)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(subprocess.run(["git", "show", f"{rev}:{f}"], cwd=top, capture_output=True).stdout)
        return src
    src = Path(spec).resolve()
    shutil.copytree(src, into, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("*.pdf", "*.aux", "*.log", "*.out", "*.blg", "*.toc"))
    return src


def absolutize(room: Path, origin: Path):
    """Relative inputs (../../.. into the Board) resolve from the room's real place, not the scratch copy."""
    pat = re.compile(r"(\\(?:input|include|includegraphics(?:\[[^\]]*\])?|graphicspath\{)\{)(\.\.?/[^}]*)\}")
    for f in room.rglob("*.tex"):
        x = f.read_text(errors="ignore")
        y = pat.sub(lambda m: m.group(1) + str((origin / m.group(2)).resolve()) + "}", x)
        if y != x:
            f.write_text(y)


def merge_bibs(old: Path, new: Path):
    """Every .bib entry the old room has and the new one lacks is appended to the new copy (scratch only)."""
    have = set()
    for b in new.glob("*.bib"):
        have |= set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", b.read_text(errors="ignore")))
    target = next(iter(sorted(new.glob("*.bib"))), new / "reference.bib")
    extra = []
    for b in old.glob("*.bib"):
        txt = b.read_text(errors="ignore")
        for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,", txt):
            if m.group(1) in have:
                continue
            depth, i = 1, txt.index("{", m.start()) + 1
            while i < len(txt) and depth:
                depth += {"{": 1, "}": -1}.get(txt[i], 0)
                i += 1
            extra.append(txt[m.start():i]); have.add(m.group(1))
    if extra:
        with open(target, "a") as f:
            f.write("\n\n% latex_diff: entries only the old round cites\n" + "\n\n".join(extra) + "\n")


def compile_room(room: Path, master: str, engine: str):
    stem = Path(master).stem
    run([engine, "-interaction=nonstopmode", master], room)
    run(["bibtex", stem], room)
    run([engine, "-interaction=nonstopmode", master], room)


NOTE_HEAD = (
    "% latex_diff --notes: a wider page with the notes in the right margin (the diff is for reading, never submitted)\n"
    "\\usepackage[paperwidth=11in,paperheight=11in,left=1in,right=3.4in,top=0.75in,bottom=1in,"
    "marginparwidth=2.8in,marginparsep=0.25in]{geometry}\n"
    "\\usepackage{xcolor}\n"
    "\\newcounter{diffnote}\\newcommand{\\diffnote}[1]{\\stepcounter{diffnote}"
    "\\textsuperscript{\\color{blue}\\textbf{\\arabic{diffnote}}}\\marginpar{\\raggedright\\linespread{1}\\footnotesize"
    "\\color{blue!70!black}\\textbf{\\arabic{diffnote}.} #1}}\n")


# Between two words of `at`, the diff may hold latexdiff markup: a deleted run (skipped whole), an added run's opening,
# a block's begin or end, or a closing brace. So `at` can be any text of the new room, even across a change.
_GAP = r"(?:\s+|\\DIF(?:add|del)(?:begin|end)(?:FL)?\b|\\DIFdel(?:FL)?\{[^{}]*\}|\\DIFadd(?:FL)?\{|\})+"


def locate(tex: str, at: str, start: int) -> int:
    """Where `at` begins in the diff after `start`: the text as written, else its words with latexdiff markup between."""
    i = tex.find(at, start)
    if i >= 0 or not at.split():
        return i
    m = re.compile(_GAP.join(re.escape(w) for w in at.split())).search(tex, start)
    return m.start() if m else -1


def add_notes(tex: str, path: Path) -> str:
    """Each note beside the first occurrence of its `at` text, moved before the latexdiff block that holds it: a margin
    note inside latexdiff's underline box does not compile."""
    import yaml
    notes = (yaml.safe_load(path.read_text()) or {}).get("notes") or []
    body = tex.index("\\begin{document}")
    for n in notes:
        at = locate(tex, n["at"], body)
        if at < 0:
            print(f"latex_diff: note not placed, text not found: {n['at'][:60]!r}", file=sys.stderr)
            continue
        line = tex.rfind("\n", 0, at)
        block = max(tex.rfind("\\DIFaddbegin", 0, at), tex.rfind("\\DIFdelbegin", 0, at))
        closed = max(tex.rfind("\\DIFaddend", 0, at), tex.rfind("\\DIFdelend", 0, at))
        at = block if block > line and block > closed else at      # only out of a block the text is still inside
        if re.match(r"\s*\\(?:sub)*section\*?\{|\s*\\caption\{", tex[line + 1:at]):   # never inside a heading or caption
            at = tex.find("\n", at) + 1
        tex_of = lambda s: re.sub(r'"([^"]*)"', r"``\1''", re.sub(r"([%&#_$])", r"\\\1", s))   # TeX quotes
        text = tex_of(n["note"])
        if n.get("comment"):        # a reviewer's comment, quoted in their words, then the reply
            text = ("{\\color{orange!80!black}\\textbf{" + tex_of(n.get("who") or "Comment") + ":} ``" + tex_of(n["comment"])
                    + "''}\\\\[2pt]$\\to$ " + text)
        tex = tex[:at] + "\\diffnote{" + text + "}" + tex[at:]
    return tex.replace("\\begin{document}", NOTE_HEAD + "\\begin{document}", 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--master", default="master.tex")
    ap.add_argument("--engine", default="xelatex")
    ap.add_argument("--notes", type=Path, help="YAML notes: [{at, note}] printed in the margin beside each change")
    a = ap.parse_args()
    for tool in ("latexdiff", a.engine, "bibtex"):
        if not shutil.which(tool):
            raise SystemExit(f"latex_diff: {tool} not found (install TeX Live / MacTeX)")
    with tempfile.TemporaryDirectory(prefix="latexdiff-") as tmp:
        old, new = Path(tmp) / "old", Path(tmp) / "new"
        old.mkdir(); new.mkdir()
        absolutize(old, materialize(a.old, old))
        absolutize(new, materialize(a.new, new))
        # References are not diffed (latexdiff breaks apacite's .bbl); the diff cites both rounds' keys and BibTeX
        # builds one reference list from both rounds' entries, so a citation in deleted text still resolves.
        for room in (old, new):
            for b in room.glob("*.bbl"):
                b.unlink()
        merge_bibs(old, new)
        diff = new / "diff.tex"
        r = subprocess.run(["latexdiff", "--flatten", "--type=UNDERLINE", "--graphics-markup=none",
                            "--math-markup=whole",
                            str(old / a.master), str(new / a.master)], capture_output=True, text=True)
        if r.returncode or not r.stdout.strip():
            raise SystemExit(f"latexdiff failed: {r.stderr[-2000:]}")
        diff.write_text(add_notes(r.stdout, a.notes) if a.notes else r.stdout)
        run([a.engine, "-interaction=nonstopmode", "diff.tex"], new)
        run(["bibtex", "diff"], new)
        for _ in range(2):
            run([a.engine, "-interaction=nonstopmode", "diff.tex"], new)
        pdf = new / "diff.pdf"
        if not pdf.exists():
            log = (new / "diff.log").read_text(errors="ignore") if (new / "diff.log").exists() else ""
            print(log[-3000:], file=sys.stderr)
            raise SystemExit("latex_diff: the diff did not compile")
        errors = [l for l in (new / "diff.log").read_text(errors="ignore").splitlines() if l.startswith("!")]
        a.out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pdf, a.out)
        shutil.copy2(diff, a.out.with_suffix(".tex"))
        pages = run(["pdfinfo", str(a.out.resolve())], a.out.parent).stdout
        pages = re.search(r"Pages:\s+(\d+)", pages or "")
        print(f"latex_diff: {a.out} ({pages.group(1) if pages else '?'} pages, {len(errors)} LaTeX errors)")
        if errors:
            print("\n".join(sorted(set(errors))[:10]), file=sys.stderr)


if __name__ == "__main__":
    main()
