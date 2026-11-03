"""A paper's display plan (s06-paper-displays) and the venue's display rules, read and checked together (JL 261101:
"in the /haipipe-paper-plan, we should also have the plan for the displays"; "the display like that should also
follow the venue, the venue we are using").

    python display_plan.py check <Board>            every display against the venue's rules; exit 1 on a ❗
                                                    (⚠️ worth a look and ⬜ not yet do not fail)
    python display_plan.py seed  <Board>            the j01 pool Tasks the plan names and the pool lacks (dry run)
    python display_plan.py seed  <Board> --apply    write them: tNN_display-<letter>-<slug>/tNN_….md

What it reads, each fact from its one owner:

    sNN-paper-displays/sNN-paper-displays.md   | Display | name | type | shows | answers | section | where | made by | state |
    venues/<venue>/call.md  ## Displays          | rule | value | source |   (rules: main limit, supplement limit,
                                               main labels, supplement labels, width, resolution, format, font,
                                               table style, caption)
    j01_evidence_display/tNN_*/tNN_*.md        label: Display A · name: … · type: figure|table
    its newest runs/*/result/                  float.tex (the caption's words), assets/figure.* (its size)

The paper number is never typed: main figures are Figure 1, 2 … and main tables Table 1, 2 … in the plan's row order,
and supplement rows take the venue's supplement labels (eFigure 1, eTable 1 at JAMA). A rule with no value is not
checked, and the check says so.
"""
from __future__ import annotations

import re
import struct
import sys
from pathlib import Path

RULES = ("main limit", "supplement limit", "main labels", "supplement labels", "width", "resolution", "format", "font",
         "table style", "caption")
TYPES = {"figure": "📈 Figure", "table": "📊 Table"}
# a Display cell that is already a printed label keeps it: Figure 2, Table B1, eTable 3, Supplementary Figure S1
PRINTED = re.compile(r"^(?:e|Supplementary\s+|Appendix\s+)?(?:Figure|Table|Fig\.)\s*[A-Z]?\d+[a-z]?$", re.I)


def table(lines: list[str], first: str) -> list[dict]:
    """The Markdown table whose header starts with `| first |` (any case), one dict per row, keys lower case."""
    for i, ln in enumerate(lines):
        if re.match(rf"\|\s*{re.escape(first)}\s*\|", ln, re.I):
            head = [h.strip().lower() for h in ln.strip().strip("|").split("|")]
            rows = []
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                rows.append(dict(zip(head, [c.strip() for c in row.strip().strip("|").split("|")])))
            return rows
    return []


def field(text: str, name: str) -> str:
    m = re.search(rf"(?mi)^\**{name}:?\**:?\s*(.+?)\s*$", text)
    return m.group(1).strip().strip("`") if m else ""


def plan_face(board: Path) -> Path | None:
    return next(iter(sorted([*board.glob("s??-paper-displays/s??-paper-displays.md"),
                             *board.glob("studio/s??-paper-displays/s??-paper-displays.md")])), None)


def venue_call(board: Path) -> Path | None:
    """The venue the plan follows: the s06 face's **Venue:** line, else board.md's `venue:`, else the only venue."""
    face = plan_face(board)
    names = [field(face.read_text(encoding="utf-8"), "Venue") if face else "",
             field((board / "board.md").read_text(encoding="utf-8"), "venue") if (board / "board.md").is_file() else ""]
    for n in names:
        n = re.sub(r"^venues/|/call\.md$", "", n.split()[0]) if n else ""
        if n and (board / "venues" / n / "call.md").is_file():
            return board / "venues" / n / "call.md"
    calls = sorted(board.glob("venues/*/call.md"))
    return calls[0] if len(calls) == 1 else None


def rules(board: Path) -> dict:
    """{rule: (value, source)} from the venue's call.md `| rule | value | source |` table."""
    call = venue_call(board)
    if call is None:
        return {}
    return {r.get("rule", "").lower(): (r.get("value", ""), r.get("source", ""))
            for r in table(call.read_text(encoding="utf-8").splitlines(), "rule")
            if r.get("value") and r["value"].strip().upper() != "UNKNOWN"}     # UNKNOWN is not recorded (JL 261102)


def title(r: dict) -> str:
    """A planned display's title: its paper label, then its pool letter, "Table 1 (Display A)" (agreed 261101 with
    JL: "you can do it like Table 1 (Display XX)"); a row that is already its printed label (Table B1) is just that."""
    return r["as"] if r["as"] == r.get("display") else f"{r['as']} ({r.get('display', '')})"


def labels(R: dict, where: str) -> tuple[str, str]:
    """('Figure', 'Table') for the main paper; the venue's supplement labels, else 'Supplementary Figure' …"""
    default = ("Figure", "Table") if where == "main" else ("Supplementary Figure", "Supplementary Table")
    v = R.get(f"{where} labels", ("", ""))[0]
    parts = [re.sub(r"\s*(?:\d+|n|N|<n>|#)\s*$", "", p.strip()).strip() for p in re.split(r"[,/;·]", v) if p.strip()]
    fig = next((p for p in parts if "fig" in p.lower()), default[0])
    tab = next((p for p in parts if "tab" in p.lower()), default[1])
    return fig, tab


def rows(board: Path) -> list[dict]:
    """The plan's rows, each with `as` (its number in the paper, counted in row order), `type`, `where`."""
    face = plan_face(board)
    if face is None:
        return []
    R, seen, out = rules(board), {}, []
    for r in table(face.read_text(encoding="utf-8").splitlines(), "Display"):
        kind = "table" if "table" in r.get("type", "").lower() else "figure"
        where = "supplement" if re.match(r"\s*(supp|appendix|online|e\b)", r.get("where", ""), re.I) else "main"
        cell = r.get("display", "").strip()
        if PRINTED.match(cell):                   # already the printed label (MISQ's Table B1, lettered by appendix)
            out.append({**r, "type": kind, "where": where, "as": cell})
            continue
        base = labels(R, where)[0 if kind == "figure" else 1]
        seen[base] = seen.get(base, 0) + 1
        out.append({**r, "type": kind, "where": where, "as": f"{base} {seen[base]}"})
    return out


def keys(text: str) -> list[str]:
    """What a pool face answers to, in order: `display-plan:`, a `label:` that reads "Display X", `number:` (the
    printed label, Table 3), then any `label:` (a paper whose label: is its LaTeX label, tab:results, keeps it)."""
    lab = field(text, "label")
    got = [field(text, "display-plan"), lab if re.match(r"(?i)display\s+\w+$", lab) else "", field(text, "number"), lab]
    return list(dict.fromkeys(k for k in got if k))


def pool(board: Path) -> dict:
    """{key: Task folder} of the Board's j01 display pool, each Task under every key its face answers to."""
    job = next((j for j in sorted(board.glob("j[0-9]*_*")) if re.search(r"evidence_display|_displays", j.name)), None)
    out = {}
    for t in sorted(job.glob("t[0-9]*_*")) if job else []:
        f = t / f"{t.name}.md"
        for k in keys(f.read_text(encoding="utf-8", errors="ignore")) if f.is_file() else []:
            out.setdefault(k, t)
    return out


def newest(task: Path, name: str) -> Path | None:
    hits = sorted([*task.glob(f"runs/*/result/{name}"), *task.glob(f"display/*/{name}")], key=lambda p: p.stat().st_mtime)
    return hits[-1] if hits else None


def caption_words(float_tex: Path) -> int:
    s = float_tex.read_text(encoding="utf-8", errors="ignore")
    i = s.find(r"\caption{")
    if i < 0:
        return 0
    depth, j = 0, i + len(r"\caption")
    for k in range(j, len(s)):
        depth += {"{": 1, "}": -1}.get(s[k], 0)
        if depth == 0:
            body = re.sub(r"\\[a-zA-Z]+\*?|[{}]", " ", s[j + 1:k])
            return len(re.findall(r"[A-Za-z0-9<>][\w<>'’.-]*", body))
    return 0


def png_size(p: Path) -> tuple[int, int] | None:
    with p.open("rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24]) if head[:8] == b"\x89PNG\r\n\x1a\n" else None


def number(text: str) -> float | None:
    m = re.findall(r"\d+(?:\.\d+)?", text or "")
    return max(float(x) for x in m) if m else None


def sketch(text: str, label: str) -> str:
    """The ```text sketch under `#### <label>` on the plan's face, or ''."""
    m = re.search(rf"(?ms)^####\s*{re.escape(label)}\s*\n+```text\n(.*?)```", text) if label else None
    return m.group(1).rstrip() if m else ""


def run_of(board: Path, cell: str) -> tuple[str, Path | None]:
    """A `made by` cell's Run address and its folder: `j01.t01.r01` inside the Board, `b03.j03.t02.r05` in the
    Project's work/; ('', None) when the cell names no address (a Run still to make, in words)."""
    m = re.search(r"\b(?:(b\d+)\.)?(j\d+)\.(t\d+)(?:\.(r\d+))?\b", cell or "")
    if not m:
        return "", None
    b, j, t, r = m.groups()
    bases = [board] if not b else [p / "work" for p in board.parents if (p / "work").is_dir()][:1]
    for base in bases:
        hits = sorted(base.glob(f"{b}_*/{j}_*/{t}_*" if b else f"{j}_*/{t}_*"))
        if hits:
            if not r:
                return m.group(0), hits[0]
            run = sorted([*hits[0].glob(f"runs/{r}_*"), *hits[0].glob(f"runs/{r}")])
            return m.group(0), run[0] if run else None
    return m.group(0), None


def check(board: Path) -> list[tuple[str, str]]:
    """(mark, line): ✅ holds, ❗ breaks a venue rule or the plan, ⚠️ worth a look, ⬜ not checked yet."""
    out, R, P, have = [], rules(board), rows(board), pool(board)
    if plan_face(board) is None:
        return [("⬜", "no display plan yet: make s06-paper-displays (haipipe-paper-plan)")]
    call = venue_call(board)
    if call is None:
        out.append(("⚠️", "no venue named: write **Venue:** <name> on the s06 face (venues/<name>/call.md)"))
    elif not R:
        out.append(("⚠️", f"{call.parent.name}: call.md has no `| rule | value | source |` Displays table; nothing is checked"))
    for where in ("main", "supplement"):
        cap = number(R.get(f"{where} limit", ("", ""))[0])
        n = sum(1 for r in P if r["where"] == where)
        if cap is not None:
            out.append(("✅" if n <= cap else "❗", f"{n} of at most {cap:g} {where} displays"))
    caption_cap = number(R.get("caption", ("", ""))[0])
    width_in, dpi = number(R.get("width", ("", ""))[0]), number(R.get("resolution", ("", ""))[0])
    formats = [f.lower() for f in re.findall(r"[A-Za-z]{2,5}", R.get("format", ("", ""))[0])]
    text = plan_face(board).read_text(encoding="utf-8", errors="ignore")
    for r in P:
        name = title(r)
        made = r.get("made by", "")
        if not re.search(r"\w", re.sub(r"[—–-]", "", made)):
            out.append(("❗", f"{name}: no Run named to make it (made by)"))
        else:
            addr, found = run_of(board, made)
            if addr and found is None:
                out.append(("❗", f"{name}: made by {addr}, which is not on disk"))
            elif not addr:
                out.append(("⬜", f"{name}: its Run is not made yet ({made.strip('<>')})"))
        if not sketch(text, r.get("display", "")):
            out.append(("⬜", f"{name}: no sketch yet (#### {r.get('display', '')} under ### Sketches)"))
        task = have.get(r.get("display", ""))
        if task is None:
            out.append(("⬜", f"{name}: not in the pool yet (display_plan.py seed)"))
            continue
        face = (task / f"{task.name}.md").read_text(encoding="utf-8", errors="ignore")
        if field(face, "type") and field(face, "type").lower() != r["type"]:
            out.append(("⚠️", f"{name}: the plan says {r['type']}, its face says {field(face, 'type')}"))
        _, run = run_of(board, made)
        stem = (re.match(r"\S+\s*·\s*(\S+)", field(face, "printed") or "") or [None, ""])[1]   # a Run that draws several
        name_ft = f"{stem}-float.tex" if stem else "float.tex"                                      # tables names each by its stem
        ft = (run / "result" / name_ft) if run is not None and (run / "result" / name_ft).is_file() \
            else newest(task, name_ft)            # the version the row names, else the newest
        if ft is None:
            out.append(("⬜", f"{name}: not drawn yet"))
            continue
        if caption_cap is not None:
            w = caption_words(ft)
            out.append(("✅" if w <= caption_cap else "❗", f"{name}: caption {w} of at most {caption_cap:g} words"))
        art = next((a for a in sorted(ft.parent.glob("assets/figure.*"))), None) if r["type"] == "figure" else None
        if art is not None and formats and art.suffix.lstrip(".").lower() not in formats:
            out.append(("❗", f"{name}: {art.name} is not one of the venue's formats ({', '.join(formats)})"))
        size = png_size(art) if art is not None and art.suffix.lower() == ".png" else None
        if size and width_in and dpi:
            need = int(width_in * dpi)
            out.append(("✅" if size[0] >= need else "❗",
                        f"{name}: {size[0]} px wide; the venue's {width_in:g} in at {dpi:g} dpi needs {need}"))
    planned = {r.get("display", "") for r in P}
    hit = {t for k, t in have.items() if k in planned}
    loose = list(dict.fromkeys(t for t in have.values() if t not in hit))
    out += [("⚠️", f"{t.name}: in the pool but not in the plan; name it in a plan row (its label: or number:, or add "
                   f"display-plan: Display <letter> to its face) or drop it") for t in loose]
    told = {k for k in RULES if k in R}
    if R and told != set(RULES):
        out.append(("⬜", "venue rules not recorded: " + ", ".join(k for k in RULES if k not in told)))
    return out


def seed(board: Path, apply: bool = False) -> list[Path]:
    """The pool Tasks the plan names and the pool lacks, next tNN each: tNN_display-<letter>-<slug>/tNN_….md."""
    job = next((j for j in sorted(board.glob("j[0-9]*_*")) if re.search(r"evidence_display|_displays", j.name)), None)
    if job is None:
        raise SystemExit("no display Job (jNN_evidence_display): make it first (paper_ladder.py evidence)")
    have, made = pool(board), []
    used = [int(t.name[1:3]) for t in job.glob("t[0-9][0-9]_*") if t.name[1:3].isdigit()]
    nn = max(used or [0])                         # one letter sequence (JL 261101: "display A, B, C, D, and within it,
                                                  # we can see different versions"); main or supplement is the plan's call
    small = {"a", "an", "the", "of", "in", "on", "by", "and", "or", "for", "to", "who", "is", "are", "with", "at"}
    for r in rows(board):
        lab = r.get("display", "")
        if not lab or lab in have:
            continue
        nn += 1
        letter = re.sub(r"(?i)^display\s*", "", lab).lower() or str(nn)
        slug = "-".join([w for w in re.findall(r"[a-z0-9]+", r.get("name", "").lower()) if w not in small][:3]) or r["type"]
        name = f"t{nn:02d}_display-{letter}-{slug}"
        face = job / name / f"{name}.md"
        made.append(face)
        if apply:
            face.parent.mkdir(parents=True)
            face.write_text(f"# {name}\n\nlabel: {lab}\nname: {r.get('name', '')}\ntype: {r['type']}\n"
                            f"answers: {r.get('answers', '')}\nmade by: {r.get('made by', '')}\nstatus: not drawn\n",
                            encoding="utf-8")
    return made


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[0] not in ("check", "seed"):
        sys.exit(__doc__)
    board = Path(argv[1]).resolve()
    if argv[0] == "seed":
        made = seed(board, "--apply" in argv)
        print("\n".join(f"{'wrote' if '--apply' in argv else 'would write'} {p.relative_to(board)}" for p in made)
              or "the pool already holds every planned display")
        return 0
    lines = check(board)
    for r in rows(board):
        print(f"  {title(r):28} {TYPES[r['type']]} · {r.get('name', '')}")
    print("\n".join(f"{m} {t}" for m, t in lines))
    return 1 if any(m == "❗" for m, _ in lines) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
