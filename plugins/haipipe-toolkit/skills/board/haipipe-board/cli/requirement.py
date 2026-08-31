#!/usr/bin/env python3
"""Write `outline/<stem>-requirement.md`: what this page must OBEY, resolved
from the VENUE division the page names, four short records a writer can hold
in one look (haipipe-plugin-outline §📏).

    python3 cli/requirement.py <page.md>            one page
    python3 cli/requirement.py --all <board-dir>    every section page

The law shipped in 0.17.1 and the generator did not, so the 🧭 tab never
showed a 📏 chip (JL 260831: "among them I didn't see the requirement").
The first generator also copied the narrative row and the board's writing
rules in; JL 260831: "requirement is very hard to read, make it concise and
readable, and maybe focus on the venue is sufficient". So: venue only.

  V1  Shape    the division's lead sentence, plus the ARC chain if the desk draws one
  V2  Size     the format values: words, citations, displays (one line each)
  V3  Refused  each named anti-pattern, one line each, the pack's own words
  V4  Moves    the slot names as a chain; the exemplar sentences fold underneath

The page's own reader question is on the 🧭 tab already; the narrative row
lives on the Narrative page; the board rules live in `ref/writing-rules.md`.

Never authored, never versioned: regenerate, do not edit. `check.py` reports
`requirement-missing`, `requirement-hand-edited` and `requirement-stale`.
"""
import argparse, datetime, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # haipipe-board/
SKILLS = HERE.parent.parent                             # skills/
BEGIN, END = "# --- requirement:begin (generated) ---", "# --- requirement:end ---"


def _fm(text, key):
    m = re.search(r"(?m)^%s:\s*(.+?)\s*$" % re.escape(key), text[:3000])
    return m.group(1).strip() if m else ""


def _block(text, head_re, stop_re):
    """The text under the first heading matching head_re, up to stop_re."""
    m = re.search(head_re, text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    s = re.search(stop_re, rest, re.M)
    return rest[: s.start()] if s else rest


def _rec(rid, head, rows, detail=(), source=""):
    out = [f"### {rid} · {head}"]
    out += [f"- **{k}**: {v}" for k, v in rows if v]
    if source:
        out.append(f"- **Source**: {source}")
    out += [f"  {d}" for d in detail if d.strip()]
    return "\n".join(out)


def _clean(line):
    line = re.sub(r"\s*\[[^\]]*\]\s*$", "", line.strip())      # trailing [cite]
    return re.sub(r"^\(.*\)$", "", line).strip()


# ── V · the venue division, four records ─────────────────────────────────
def _cite(line, keep_refs=False):
    """drop the `[source lines]` brackets (all of them unless keep_refs) and a wrapping (aside)"""
    if keep_refs:
        return _clean(line)
    c = re.sub(r"\s*\[[^\]]*\]", "", line.strip())
    c = re.sub(r"\s+([.;,])", r"\1", c)
    return re.sub(r"^\(.*\)$", "", c).strip()


_FMT_LABEL = {"WORDS": "Words", "CITATION DENSITY": "Citations", "VALUE DENSITY": "Values", "DISPLAYS": "Displays"}


def _fence_lines(body):
    """the lines inside the FIRST ```text fence of a block"""
    out, fence = [], False
    for ln in body.splitlines():
        if ln.startswith("```"):
            if fence:
                break
            fence = True; continue
        if fence:
            out.append(ln)
    return out


def _arc(lead_fence):
    """`📐 ARC` chain: the lines under it until a blank, `→` stripped, joined"""
    chain, on = [], False
    for ln in lead_fence:
        if "ARC" in ln and not on:
            on = True
            continue
        if on:
            if not ln.strip():
                break
            c = _cite(ln.strip().lstrip("→").strip())
            if c and not c.startswith("["):
                chain.append(c)
    return " → ".join(chain)


def _format_rows(sub_body):
    """`📏 WORDS  value…` rows from the format fence; continuation lines join;
    citation lines drop; `not recorded` rows drop; a long value keeps its
    head up to the last ` · ` before ~140 chars and folds the rest"""
    rows, folds, cur = [], [], None
    for ln in _fence_lines(sub_body):
        # a row starts with the desk's emoji, then an ALL-CAPS label; a
        # continuation line has no emoji, so "CI and P together…" is not a row
        # (physician-space-21, JAMA SM03 V2, 260831)
        m = re.match(r"^\s*[^\w\s]+\s*((?:[A-Z]{2,}(?:\s(?=[A-Z]{2,}))?)+)\s+(.*)$", ln)
        if m:
            lab = m.group(1).strip()
            cur = [_FMT_LABEL.get(lab, lab.capitalize()), m.group(2).strip()]
            rows.append(cur)
        elif cur is not None and ln.strip():
            cur[1] += " " + ln.strip()
    out = []
    for lab, val in rows:
        val = re.sub(r"\s*\[[^\]]*\]", "", val).strip(" ·")
        if val.lower().startswith("not recorded"):
            continue
        full = val
        val = re.split(r",?\s+measured\b", val)[0].strip(" ·")
        if val != full:
            folds.append(f"{lab}, in full · {full}")
        elif len(val) > 140:
            cut = val.rfind(" · ", 0, 140)
            if cut > 40:
                folds.append(f"{lab}, in full · {full}")
                val = val[:cut]
        out.append((lab, val))
    return out, folds


def venue_records(page_text, board):
    src, div = _fm(page_text, "structure-source"), _fm(page_text, "structure-division")
    if not src:
        return []
    path = SKILLS / src if not (board / src).exists() else board / src
    if not path.exists():
        return [_rec("V1", "Venue desk not found", [("Rule", f"`{src}` does not exist; fix `structure-source:` on the page")])]
    t = path.read_text(encoding="utf-8", errors="replace")
    if not div or div.upper().startswith("ABSENT"):
        return [_rec("V1", "The venue publishes no unit for this section",
                     [("Rule", "the section exists by a person's ruling, recorded as a `D<nn>` thread; it is a deviation, not a requirement")],
                     source=f"`{src}` (no division)")]
    m = re.match(r"§(\d+)\s+(\S+)", div)
    if not m:
        return [_rec("V1", "structure-division: unreadable", [("Rule", f"`{div}` is not `§<n> Sec-<x>`")])]
    n, tok = m.groups()
    head_re = r"^### %s · %s:\s*(.*)$" % (n, re.escape(tok))
    body = _block(t, head_re, r"^### ")
    title = re.search(head_re, t, re.M).group(1).strip()
    where = f"`{Path(src).name}` §{n} {tok}"
    subs = {re.sub(r"[^a-z]", "", st.lower()): (sn, sb)
            for sn, st, sb in re.findall(r"(?ms)^#### %s\.(\d+) · ([^\n]+)\n(.*?)(?=^#### |\Z)" % n, body)}
    def pick(*keys):
        for k, v in subs.items():
            if any(x in k for x in keys):
                return v
        return None, ""
    recs = []
    # V1 · shape: the lead sentence and the arc chain
    lead = re.search(r"(?m)^\*\*(.+?)\*\*[:：]?\s*(.*)$", body)
    rows = [("Rule", (lead.group(1) + ": " + lead.group(2)).strip() if lead else title)]
    arc = _arc(_fence_lines(body.split("\n#### ", 1)[0]))
    if arc:
        rows.append(("Arc", arc))
    recs.append(_rec("V1", f"Shape · {title}", rows, source=where))
    # V2 · size: the format values, one line each
    sn, sb = pick("format")
    if sb:
        rows, folds = _format_rows(sb)
        recs.append(_rec("V2", "Size", rows, detail=folds, source=f"{where}.{sn}"))
    # V3 · refused: one line per anti-pattern, the pack's words
    sn, sb = pick("refuse")
    if sb:
        rows = []
        for ln in sb.splitlines():
            if ln.lstrip().startswith((">", "(", "```")):
                continue                                  # ✎ lanes and the aside
            c = _cite(ln)
            if c:
                rows.append(("Rule", c))
        recs.append(_rec("V3", "Refused", rows, source=f"{where}.{sn}"))
    # V4 · moves: the slot names as a chain, exemplars folded
    sn, sb = pick("moves", "slots")
    if sb:
        names, lines = [], []
        for ln in sb.splitlines():
            if ln.lstrip().startswith((">", "(", "```")):
                continue
            c = _cite(ln, keep_refs=True)
            if not c:
                continue
            lines.append(c)
            name = c.split(":", 1)[0].strip()
            if 0 < len(name.split()) <= 8:
                names.append(name[0].lower() + name[1:])
        chain = " → ".join(names[:4]) + (" → …" if len(names) > 4 else "")
        recs.append(_rec("V4", "Moves · " + chain, [("Rule", "fill each slot in this paper's words; never lift the exemplar's sentence")],
                         detail=lines, source=f"{where}.{sn}"))
    return recs


def build(page_md: Path, board: Path) -> str:
    text = page_md.read_text(encoding="utf-8", errors="replace")
    recs = venue_records(text, board)
    if not recs:
        return ""
    now = datetime.datetime.now().strftime("%y%m%d %H%M")
    head = [f"# {page_md.stem} · requirement", f"page: {page_md.stem}",
            f"kind: requirement · generated {now} by cli/requirement.py · venue only · never hand-edited", "",
            BEGIN, f"  REQUIREMENT, MEASURED {now}. GENERATED; do not hand-edit.",
            f"  regenerate: cli/requirement.py {page_md.name}", ""]
    return "\n".join(head + ["\n\n".join(recs)] + ["", END, ""])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", type=Path); ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.all:
        board = a.target
        pages = [p / f"{p.name}.md" for g in board.iterdir() if g.is_dir() and not g.name.startswith(("_", ".", "board"))
                 for p in g.iterdir() if p.is_dir() and (p / f"{p.name}.md").exists()]
        pages = [p for p in pages if re.search(r"(?m)^page-type:\s*section\b", p.read_text(errors="replace")[:600])]
    else:
        board, pages = a.target.parents[2], [a.target]
    n = 0
    for pg in sorted(pages):
        out = pg.parent / "outline" / f"{pg.stem}-requirement.md"
        made = build(pg, board)
        if not made:
            print(f"skip  {pg.name}: no `structure-source:` on the page, nothing to resolve"); continue
        out.parent.mkdir(exist_ok=True)
        out.write_text(made, encoding="utf-8"); n += 1
        print(f"wrote {out}")
    print(f"{n} file(s)")


if __name__ == "__main__":
    sys.exit(main())
