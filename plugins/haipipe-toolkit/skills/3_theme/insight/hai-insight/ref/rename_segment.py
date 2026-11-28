"""rename_segment.py <insight Board> [--apply] · the word a person reads is "segment" (was "cut" and "partition").

A Board and its Question Book say "segment" in every sentence a person reads. One pass over both:

  prose     partition(s) · cut(s)                  ->  segment(s)
  run type  run-set-cuts-question-vN/ · set_cuts   ->  run-set-segments-question-vN/ · set_segments
  labels    Run a partition · Register a cut · Propose a cut · Set the cuts  ->  … a segment · Set the segments

Never rewritten, because a reader or a receipt holds the name: `partitions.md`, the keys `partition:` /
`partitions:` / `cut:`, `partition_power.csv`, the view key `by-cut`, `kind: cut`, `type: partition`, a word inside
a code span, a path or a quoted sentence, a `renamed-from:` line, a data: URI, a table (.csv), and "cut" as a verb
("is cut", "cut from", "cut off", "cut to"). A script (.py) gets its sentences only: strings and comments that hold a space.

Dry run by default: it prints each changed line, then a count. `--apply` writes. A question.md or a script the pass
rewrites makes its receipts older than their source: rerun those tickets after (insight_ladder.py update --rerun).
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import tokenize
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rename_code_data as RN  # noqa: E402  (front, the Question Book a Board names)

BINARY = RN.BINARY | {".csv", ".ico", ".woff", ".woff2", ".ttf"}
SKIP_DIRS = {"__pycache__", ".git", "node_modules", "chat"}

NAMES = [(re.compile(r"set-cuts"), "set-segments"), (re.compile(r"set_cuts"), "set_segments")]
LABELS = [(re.compile(r"Run a partition"), "Run a segment"), (re.compile(r"Register a cut"), "Register a segment"),
          (re.compile(r"Propose a cut"), "Propose a segment"), (re.compile(r"Set the cuts"), "Set the segments"),
          (re.compile(r"<(?:partition|cut)(s?)>"), r"<segment\1>"),
          (re.compile(r"\b(per|each|every)-(?:partition|cut)\b(?![-/.])"), r"\1-segment"),      # "a per-cut best"
          (re.compile(r"(?<![\w/`.-])(?:partition|cut)('{1,2})s\b"), r"segment\1s")]              # "every partition's best"; YAML 'partition''s'
KEEP = [re.compile(p) for p in (
    r"(?m)^\|[^\n]*\|[ \t]*$",                                   # a Markdown table row: a csv's cells, never reworded
    r"(?m)^[ \t-]*(?:x|y|hue|color|colour|facet|group|series|col|row|label|value):[ \t]*['\"]?(?:partition|cut)s?['\"]?[ \t]*$",
                                                                 # a figure spec's column name (figures:, x: partition)
    r"data:[\w/+.-]+;base64,[A-Za-z0-9+/=]+",r"(?m)^[ \t]*renamed-from:.*$", r'\d{6}[^"\n]{0,30}: "[^"\n]*"', r"“[^”\n]*”",
    r"partitions\.md", r"\bpartitions?(?=\s?[:=\]])", r"\bpartitions?\.\w+", r"[\"'`{\[./-]partitions?\b", r"\bpartitions?[\"'`}\]/(-]",
    r"the cell's partition", r"(?<!per )\b[Cc]ut at\b", r"\bcut no-", r"\bcut to\b", r"\b[Cc]ut a numeric\b",
    r"(?m)^[ \t-]*cuts?:", r"`cuts?:?`", r"\bkind: cut\b", r"\btype: partition\b", r"[\"']cuts?[\"']",
    r"[\w]-cuts?\b", r"\bcuts?-[\w]", r"[{\[]cuts?[}\]]", r"\bcut\(", r"\.cut\b",
    r"\b(?:is|are|was|were|been|be|being|to|not|when to|gets?|got) cut\b",
    r"\bcut (?:from|off|there|yet|down|out|into|short|away|a release|the release|a version)\b",
    r"\bcuts (?:the|a|off|out|down) \b", r"\b[Cc]ut and paste\b", r"\b(?:release|version)s? (?:is|are) cut\b",
)]
WORDS = [(re.compile(r"\bpartitions\b"), "segments"), (re.compile(r"\bpartition\b"), "segment"),
         (re.compile(r"\bPartitions\b"), "Segments"), (re.compile(r"\bPartition\b"), "Segment"),
         (re.compile(r"\bcuts\b"), "segments"), (re.compile(r"\bcut\b"), "segment"),
         (re.compile(r"\bCuts\b"), "Segments"), (re.compile(r"\bCut\b"), "Segment"),
         (re.compile(r"\ban segment"), "a segment")]
CODESPAN = re.compile(r"`[^`\s]+`")
OLD_WORD = re.compile(r"\b(?:[Cc]uts?|[Pp]artitions?)\b")


def prose(text: str, keeps=KEEP) -> str:
    """The words, with every kept name hidden first and put back after."""
    held = []

    def hide(m):
        held.append(m.group(0))
        return f"\0{len(held) - 1}\0"
    for pat in keeps:
        text = pat.sub(hide, text)
    for pat, rep in WORDS:
        text = pat.sub(rep, text)
    return re.sub(r"\0(\d+)\0", lambda m: held[int(m.group(1))], text)


def script(src: str) -> str:
    """A script's sentences only: a string or a comment that holds a space; never a name, a regex or bytes."""
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, SyntaxError, IndentationError):
        return src
    offs = [0]
    for line in src.splitlines(keepends=True):
        offs.append(offs[-1] + len(line))
    out, pos = [], 0
    for tk in toks:
        if tk.type not in (tokenize.STRING, tokenize.COMMENT, getattr(tokenize, "FSTRING_MIDDLE", -1)):
            continue
        a, b = offs[tk.start[0] - 1] + tk.start[1], offs[tk.end[0] - 1] + tk.end[1]
        seg = src[a:b]
        if not OLD_WORD.search(seg) or re.match(r"^[rRbB]+['\"]", seg) or " " not in seg.strip("\"'"):
            continue
        q = re.match(r'(?s)^([uUfF]*("""|\'\'\'|"|\'))(.*)(\2)$', seg)   # prose the inside: a closing quote is not a name
        out += [src[pos:a], q.group(1) + prose(q.group(3)) + q.group(4) if q else prose(seg)]
        pos = b
    out.append(src[pos:])
    return "".join(out)


def rewrite(text: str, suffix: str) -> str:
    for pat, rep in NAMES + LABELS:
        text = pat.sub(rep, text)
    return script(text) if suffix == ".py" else prose(text, [CODESPAN] + KEEP)


def tops_of(board: Path) -> list[Path]:
    """The Board and the Question Book its board.md names (when it is there)."""
    rel = RN.front(board / "board.md").get("prototype", "")
    proto = board.parent.parent / rel if rel else None
    return [t for t in (board, proto) if t and t.is_dir()]


def plan(board: Path) -> tuple:
    """(edits, renames): each text file whose words change (path, old, new), each name that holds the old run type."""
    edits, renames = [], []
    for top in tops_of(board):
        for p in sorted(top.rglob("*")):
            if SKIP_DIRS & set(p.relative_to(top).parts):
                continue
            if p.is_file() and p.suffix.lower() not in BINARY:
                try:
                    old = p.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                new = rewrite(old, p.suffix.lower())
                if new != old:
                    edits.append((p, old, new))
        for p in sorted(top.rglob("*"), key=lambda q: -len(q.parts)):          # deepest first
            name = p.name
            for pat, rep in NAMES:
                name = pat.sub(rep, name)
            if name != p.name and not (SKIP_DIRS & set(p.relative_to(top).parts)):
                renames.append((p, p.with_name(name)))
    return edits, renames


def apply(edits: list, renames: list) -> None:
    for p, _, new in edits:
        p.write_text(new, encoding="utf-8")
    for src, dst in renames:
        src.rename(dst)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("board", type=Path)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    edits, renames = plan(a.board.resolve())
    for p, old, new in edits:
        print(f"== {p}")
        for o, n in zip(old.splitlines(), new.splitlines()):
            if o != n:
                print(f"  - {o.strip()[:200]}\n  + {n.strip()[:200]}")
    for src, dst in renames:
        print(f"mv {src}  ->  {dst.name}")
    if a.apply:
        apply(edits, renames)
    print(f"\n{len(edits)} files {'rewritten' if a.apply else 'would change'} · {len(renames)} names"
          + ("" if a.apply else " · dry run, rerun with --apply"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
