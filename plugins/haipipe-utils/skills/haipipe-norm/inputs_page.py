"""
Turn one noun's 0-inputs gallery into the tables its Task Page shows.

    from inputs_page import render
    summary = render(gallery=Path(".../_FoodInfo/0-inputs"),
                     expected=Path("scripts/expected.yaml"),
                     out_dir=Path(os.environ["RESULT_DIR"]))

WHAT THIS ADDS TO THE GALLERY
================================================================================
The gallery holds two facts per shape: `input.json` (what arrives) and
`door.json` (what the normalizer answered, captured at build time). It does NOT
hold a judgment. This module adds the third column -- what the answer SHOULD
be -- from `expected.yaml`, which is a human's file and the only hand-written
part of the tables.

So each table row is:

    the real input   ->   what it answers today   ->   what it should answer

and a verdict: `match`, `deviate`, or `ungraded`.

WHAT COMES OUT, AND WHY IT IS MARKDOWN
================================================================================
    <noun>-inputs.md    a count table, then one `#### <division>.<k>` paragraph
                        per shape with its four-column table
    <noun>-sources.md   who wrote these inputs: the cohort table

Both are fragments of the Task Page. The haipipe-page renderer turns the Page
into the Board page, so the Board is the website and this module draws no HTML
of its own (JL 260912: "not creating your own website"). The Page copies each
fragment between `<!-- haipipe:inputs:start run=... sha256=... -->` markers,
so a Page carrying an older copy than the Run is visible by its hash.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

MATCH, DEVIATE, UNGRADED = "match", "deviate", "ungraded"
VERDICT_CELL = {MATCH: "✅ match", DEVIATE: "❌ deviates", UNGRADED: "⬜ not graded"}

# The list-valued key that carries the specimens, per noun's input schema.
ITEM_KEYS = ("FoodName", "activities", "items")


# ---------------------------------------------------------------- reading


@dataclass
class Item:
    text: str
    today: dict[str, Any]
    verdict: str = UNGRADED
    expected: str = ""
    why: str = ""
    fix: str = ""


@dataclass
class Shape:
    slug: str
    title: str
    layer: str
    board: str
    note: str
    sampled: bool
    see: str
    unwraps: str
    items: list[Item] = field(default_factory=list)


def _note_fields(note: str) -> dict[str, str]:
    """The NOTE.md header is `key   value` lines under the `# title`."""
    out = {}
    for line in note.splitlines():
        m = re.match(r"^(shape|layer|board|door|unwraps)\s{2,}(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def _plain(md: str) -> str:
    """Bold markers out; a Page line carries its own emphasis."""
    return re.sub(r"\*\*(.+?)\*\*", r"\1", md)


def _read_shape(d: Path, spec: dict[str, Any]) -> Shape:
    note = (d / "NOTE.md").read_text()
    head = _note_fields(note)
    title = note.splitlines()[0].lstrip("# ").strip()

    body = [p.strip() for p in note.split("\n\n") if p.strip()]
    specimen = next((p for p in body if p.startswith("SPECIMEN")), "")
    prose = [p for p in body
             if not p.startswith(("#", "shape ", "SPECIMEN"))
             and "is the shape as it arrives" not in p
             and not p.startswith("unwraps")]

    raw_in = json.loads((d / "input.json").read_text())
    key = next((k for k in ITEM_KEYS if k in raw_in), None)
    if key is None:
        raise SystemExit(f"{d}/input.json has none of {ITEM_KEYS}")
    texts = [str(t) for t in raw_in[key]]
    today = json.loads((d / "door.json").read_text())
    if len(today) != len(texts):
        raise SystemExit(f"{d}: {len(texts)} inputs but {len(today)} answers")

    judged = (spec or {}).get("items") or []
    items = []
    for i, (text, rec) in enumerate(zip(texts, today)):
        j = judged[i] if i < len(judged) else {}
        items.append(Item(text=text, today=rec,
                          verdict=j.get("verdict", UNGRADED),
                          expected=j.get("expected", ""),
                          why=j.get("why", ""), fix=j.get("fix", "")))

    see = ""
    if (d / "SEE.md").exists():
        tail = (d / "SEE.md").read_text().strip().splitlines()
        see = tail[-1].strip() if tail else ""

    return Shape(slug=d.name, title=title,
                 layer=head.get("layer", "").split("(")[0].strip(),
                 board=_plain(head.get("board", "")),
                 note=" ".join(_plain(p) for p in prose[:2]),
                 sampled="CONSTRUCTED" not in specimen, see=see,
                 unwraps=_plain(head.get("unwraps", "")), items=items)


def _corpus_block(readme: Path) -> tuple[list[str], list[list[str]]]:
    """The prose and the pipe table under `## Where the inputs come from`."""
    if not readme.exists():
        return [], []
    m = re.search(r"^## Where the inputs come from\s*$(.*?)(?=^## |\Z)",
                  readme.read_text(), re.M | re.S)
    if not m:
        return [], []
    prose, rows = [], []
    for para in (p.strip() for p in m.group(1).split("\n\n")):
        if not para:
            continue
        if para.startswith("|"):
            for line in para.splitlines():
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in cells):
                    rows.append(cells)
        elif not para.startswith("GENERATED"):
            prose.append(para)
    return prose, rows


# ---------------------------------------------------------------- writing


def _cell(s: Any) -> str:
    """One pipe-table cell: a single line with no bare `|`, which the Board's
    table reader splits on (haipipe-page src/body.py table_flush)."""
    return str(s).replace("\r", "").replace("\n", " ⏎ ").replace("|", "¦").strip()


def _today(rec: dict[str, Any], fields: list[str]) -> str:
    conf = next((k for k in rec if k.endswith("Conf")), None)
    parts = []
    for k in (fields or list(rec)):
        if k not in rec:
            continue
        v = rec[k]
        shown = "null" if v is None else (str(v).lower() if isinstance(v, bool) else str(v))
        parts.append(f"**{shown}**" if k == conf else f"{k} `{shown}`")
    return " · ".join(parts)


def _sentences(text: str) -> list[str]:
    """One sentence per source line, which is how a Page is written."""
    text = " ".join(text.split())
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z`'\"(*])", text) if s]


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(header) + " |",
           "|" + "---|" * len(header)]
    out += ["| " + " | ".join(_cell(c) for c in r) + " |" for r in rows]
    return out


def _shape_md(sh: Shape, k: int, division: int, fields: list[str]) -> list[str]:
    job = [f"`{sh.slug}`", sh.layer or "contract", sh.board or "no row count",
           "sampled from the corpus" if sh.sampled else "written, not sampled"]
    lines = [f"#### {division}.{k} · {sh.title}", "(" + " · ".join(job) + ")"]
    lines += _sentences(sh.note)
    if sh.unwraps:
        lines += _sentences("Unwraps " + sh.unwraps)
    lines.append("")
    rows = [[str(n), f"`{_cell(it.text)}`", _today(it.today, fields),
             it.expected or "-", VERDICT_CELL.get(it.verdict, VERDICT_CELL[UNGRADED])]
            for n, it in enumerate(sh.items, 1)]
    lines += _table(["#", "Input", "Answers today", "Should answer", "Verdict"], rows)
    for n, it in enumerate(sh.items, 1):
        said = _sentences(it.why)
        if it.fix:
            said.append(f"Fix: {' '.join(it.fix.split())}")
        if said:
            lines.append("")
            said[0] = f"Specimen {n}: {said[0]}"
            lines += said
    if sh.see:
        lines += ["", f"Behaviour case: `{sh.see}`."]
    lines.append("")
    return lines


def render(gallery: Path, expected: Path, out_dir: Path,
           division: int = 4) -> dict[str, Any]:
    spec = yaml.safe_load(expected.read_text()) or {}
    noun = spec["noun"]
    fields = spec.get("today_fields") or []
    per_shape = spec.get("shapes") or {}

    shapes = [_read_shape(d, per_shape.get(d.name) or {})
              for d in sorted(p for p in gallery.iterdir() if p.is_dir())]
    items = [it for sh in shapes for it in sh.items]
    n_bad = sum(it.verdict == DEVIATE for it in items)
    n_ok = sum(it.verdict == MATCH for it in items)
    n_sampled = sum(sh.sampled for sh in shapes)

    inputs = _table(["Shapes", "Specimens", "✅ Match", "❌ Deviate",
                     "⬜ Not graded", "Sampled from the corpus"],
                    [[len(shapes), len(items), n_ok, n_bad,
                      len(items) - n_ok - n_bad, f"{n_sampled} of {len(shapes)}"]])
    inputs.append("")
    for k, sh in enumerate(shapes, 1):
        inputs += _shape_md(sh, k, division, fields)

    prose, rows = _corpus_block(gallery / "README.md")
    sources = []
    for para in prose:
        sources += _sentences(para) + [""]
    if rows:
        sources += _table(rows[0], rows[1:]) + [""]

    out_dir.mkdir(parents=True, exist_ok=True)
    written = {}
    for name, lines in ((f"{noun}-inputs.md", inputs), (f"{noun}-sources.md", sources)):
        text = "\n".join(lines).rstrip() + "\n"
        (out_dir / name).write_text(text)
        written[name] = hashlib.sha256(text.encode()).hexdigest()

    return {
        "noun": noun,
        "shapes": len(shapes),
        "specimens": len(items),
        "match": n_ok, "deviate": n_bad, "ungraded": len(items) - n_ok - n_bad,
        "sampled_shapes": n_sampled,
        "fragments": written,
        "deviations": [
            {"shape": sh.slug, "input": it.text[:90], "expected": it.expected}
            for sh in shapes for it in sh.items if it.verdict == DEVIATE
        ],
    }
