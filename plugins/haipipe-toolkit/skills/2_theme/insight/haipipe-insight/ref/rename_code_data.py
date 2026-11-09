"""rename_code_data.py <insight Board> [--also <path> ...] [--apply] · carry a Board and its Prototype onto code-v/data-v.

JL 261109: a release is `code-vN` (was `pN`, shown as AP<N>), a data version is `data-vM` (was `vM`, shown as F<M>),
and the Prototype sits beside the Board it serves, `<Project>/insight/Prototype-<Topic>/` (was
`<Project>/work/Prototype-bNN-<Topic>/`). One pass, for a Board and its Prototype together:

  folders   work/Prototype-bNN-<T>/                       ->  insight/Prototype-<T>/
            jNN_pN_<slug>/                                ->  jNN_code-vN_<slug>/
            jNN_prototype-pN-<slug>_data-<D>vM/           ->  jNN_code-vN-<slug>_data-vM/
            data/vM/ · run-<type>-pN/ · …                 ->  data/data-vM/ · run-<type>-code-vN/ · …
  ids       release: pN · data: vM · AP<N> · F<M>         ->  release: code-vN · data: data-vM · code-vN · data-vM

Every text file under the Board and the Prototype is rewritten, names and bare ids; an `--also` path (a design Block,
a doc that names the example) gets the whole names only. Never rewritten: the Board's own folder name, each data
version's `folder:`/`extract:` path (data outside the Board), a register board's `*-InsightBoard` name, a data: URI (its `p1 × v2` prose may be about another layout). Dry run by default: it prints each folder it would rename and each changed line, then a count.
`--apply` writes. Generated files are rewritten for their paths; rerun the Board's tickets after (run_job.py) so the
receipts and hashes are their generators' again, and re-pin each Job's `hash:` (insight_ladder.py).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

BINARY = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".parquet", ".pyc", ".zip", ".xlsx", ".docx", ".pptx", ".webp"}


def front(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        k, _, v = line.partition(":")
        if v and not line.startswith((" ", "-")):
            out[k.strip()] = v.strip().strip("'\"")
    return out


def rules(dataset: str, old_proto: str, new_proto: str) -> tuple:
    """(names, ids): the whole names, rewritten everywhere; then the bare ids, only inside the Board and the Prototype."""
    old_name, new_name = old_proto.rsplit("/", 1)[-1], new_proto.rsplit("/", 1)[-1]
    d = re.escape(dataset)
    names = [
        (re.compile(rf"(?<![\w])j(\d+)_prototype-p(\d+)(-[a-z0-9-]+)?_data-{d}v(\d+)(?![0-9])"), r"j\1_code-v\2\3_data-v\4"),
        (re.compile(r"(?<![\w])j(\d+)_p(\d+)_([A-Z][A-Za-z0-9]*?|<[dD]>)v(\d+)(?![0-9])"), r"j\1_code-v\2_data-v\4"),
        (re.compile(r"(?<![\w])j(\d+)_p(\d+)(?![0-9])"), r"j\1_code-v\2"),
        (re.compile(re.escape(old_proto) + r"(?![\w-])"), new_proto),
        (re.compile(re.escape(old_name) + r"(?![\w])"), new_name),
        (re.compile(rf"(?<![A-Za-z0-9_])(?:data-)?{d}v(\d+)(?![0-9])"), r"data-v\1"),   # not inside a file name
    ]
    ids = [
        (re.compile(r"Analysis plan AP(\d+) \(release p\d+\) on data freeze F(\d+) \(data version v\d+\)"),
         r"code-v\1 on data-v\2"),
        (re.compile(r"(?<![\w-])AP(\d+)\b"), r"code-v\1"),
        (re.compile(r"(?<![\w-])F(\d+)\b"), r"data-v\1"),
        (re.compile(r"\banalysis plan (\d+)\b"), r"code-v\1"),
        (re.compile(r"\bdata freeze (\d+)\b"), r"data-v\1"),
        (re.compile(r"(?<![\w])(?<!code-)(?<!data-)(?<!draft-)v([1-9]\d*)(?![\w.])"), r"data-v\1"),
        (re.compile(r"(?<![\w])p([1-9]\d*)(?![\w.])"), r"code-v\1"),
    ]
    return names, ids


DATA_URI = re.compile(r"data:[\w/+.-]+;base64,[A-Za-z0-9+/=]+")
CODE = {".py", ".r", ".sh", ".js", ".sql", ".do", ".ipynb", ".css"}   # code: names only, its p1/v2 are variables
HISTORY = re.compile(r"^[ \t]*renamed-from:.*$", re.M)          # an old name kept on purpose, so old links open
REGISTER = re.compile(r"[\w.-]*-InsightBoard\b")       # an older register board's name: another folder, kept
TIDY = [(re.compile(r"\bdata (?:version )?(data-v\d+)"), r"\1")]   # "data version v1" -> "data-v1"


def kept(board: Path) -> list:
    """What names another thing and is never rewritten: the Board's own folder name, and each data version's
    `folder:` / `extract:` (a path outside the Board, e.g. .../20250616_SMSR2v1/), with its last parts."""
    out = {board.name}
    for row in yaml.safe_load(re.match(r"---\n(.*?)\n---", (board / "board.md").read_text(encoding="utf-8"),
                                        re.S).group(1)).get("versions") or []:
        for key in ("folder", "extract"):
            v = str(row.get(key) or "").strip().rstrip("/")
            if v:
                out.add(v)
                out.update(part for part in v.split("/")[-2:] if not re.fullmatch(r"v\d+", part))
    return sorted(out, key=len, reverse=True)


def rewrite(text: str, rs: list, keep: list = ()) -> str:
    """The rules applied in order; an embedded data: URI (a picture inside a page), a register board's name and
    every `keep` string (kept()) are never touched."""
    pats = [DATA_URI, HISTORY, REGISTER] + [re.compile(r"(?<![\w-])" + re.escape(k) + r"(?![\w])") for k in keep]
    blobs = []

    def hide(m):
        blobs.append(m.group(0))
        return f"\0{len(blobs) - 1}\0"
    for pat in pats:
        text = pat.sub(hide, text)
    for pat, rep in [*rs, *TIDY]:
        text = pat.sub(rep, text)
    return re.sub(r"\0(\d+)\0", lambda m: blobs[int(m.group(1))], text)


def text_files(top: Path):
    for p in sorted(top.rglob("*")):
        if p.is_file() and p.suffix.lower() not in BINARY and "__pycache__" not in p.parts and ".git" not in p.parts:
            try:
                yield p, p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue


def plan(board: Path, also: list) -> tuple:
    face = front(board / "board.md")
    dataset, old_rel = face.get("dataset", ""), face.get("prototype", "")
    if not dataset or not old_rel:
        sys.exit(f"{board}: board.md names no dataset: or prototype:")
    project = board.parent.parent
    proto = project / old_rel
    new_rel = "insight/" + re.sub(r"^Prototype-b\d+-", "Prototype-", proto.name) if old_rel.startswith("work/") else old_rel
    names, ids = rules(dataset, old_rel, new_rel)
    keep = kept(board)
    tops = [t for t in [board, proto, *also] if t.exists()]
    edits = []
    for top in tops:
        inside = top in (board, proto)
        files = [(top, top.read_text(encoding="utf-8"))] if top.is_file() else text_files(top)
        for p, old in files:
            new = rewrite(old, names + ids if inside and p.suffix.lower() not in CODE else names, keep)
            if new != old:
                edits.append((p, old, new))
    renames = []
    for top in tops:
        rs = names + ids if top in (board, proto) else names
        if top.is_dir():
            for p in sorted(top.rglob("*"), key=lambda q: -len(q.parts)):   # deepest first
                n = rewrite(p.name, rs, keep)
                if n != p.name:
                    renames.append((p, p.with_name(n)))
        elif rewrite(top.name, rs, keep) != top.name:
            renames.append((top, top.with_name(rewrite(top.name, rs, keep))))
    move = (proto, project / new_rel) if new_rel != old_rel else None
    return edits, renames, move


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("board", type=Path)
    ap.add_argument("--also", type=Path, nargs="*", default=[])
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    board = a.board.resolve()
    edits, renames, move = plan(board, [p.resolve() for p in a.also])
    for p, old, new in edits:
        print(f"== {p}")
        for o, n in zip(old.splitlines(), new.splitlines()):
            if o != n:
                print(f"-  {o.strip()[:200]}\n+  {n.strip()[:200]}")
    for src, dst in renames:
        print(f"mv {src}  ->  {dst.name}")
    if move:
        print(f"mv {move[0]}  ->  {move[1]}")
    print(f"\n{len(edits)} files rewritten · {len(renames)} names · {'1 Prototype moved' if move else 'Prototype stays'}"
          + ("" if a.apply else " · dry run, nothing written"))
    if not a.apply:
        return 0
    for p, _, new in edits:
        p.write_text(new, encoding="utf-8")
    for src, dst in renames:
        src.rename(dst)
    if move:
        move[1].parent.mkdir(parents=True, exist_ok=True)
        if move[1].exists():
            sys.exit(f"{move[1]} exists; nothing moved")
        move[0].rename(move[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
