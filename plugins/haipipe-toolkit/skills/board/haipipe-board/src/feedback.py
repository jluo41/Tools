"""Feedback projection · read a Round page, land its routed rows on a target page.

ONE grammar for two readers (cli/feedback.py writes, cli/check.py checks), so
the two cannot drift the way pagestatus.py and check.py did (JL 260830).

A Round page carries two tables this reads and nothing else:
  §2A  | <PAGE> · <title> | <verdict> | <consensus> | <order> | <gate> |
  §2B  #### S<x> (<page ids>) · <title>
       - **<id> · <head>** (parent <R..>; <anchors>). **Feedback:** … **State:** <s>.

The register a page keeps is `outline/<stem>-feedback.md`, one file grouped by Round: rows DERIVED from the
Round (never paraphrased), one field the page authors, `landed:`.

A row carries the Round's WORDS, not only its head: the `**Feedback:**` and
`**Work:**` sentences of the §2B row, and the full concern of each parent R-row
from the §2 ledger. Head-and-ids-only rows (0.17.0) sent the writer back to the
Round for every row (JL 260831: "it lost a lot of informations"). The copy is
verbatim and regenerated whole, so it cannot drift from its source.
"""
import re
from pathlib import Path

PAGE_ID = re.compile(r"\b([A-Z]{2}\d{2})\b")
RANGE = re.compile(r"\b([A-Z]{2})(\d{2})[–-]([A-Z]{2})?(\d{2})\b")
HEAD = re.compile(r"(?m)^#### (S[A-Z0-9]+) \(([^)]*)\) · (.+)$")
ROW = re.compile(r"(?m)^- \*\*(S[A-Z0-9]+-PP\d+) · (.+?)\*\* \((.*?)\)\.(.*?)\*\*State:\*\* (\w+)")
A_ROW = re.compile(r"(?m)^\| ([A-Z]{2}\d{2}(?: \+ [A-Z]{2}\d{2})?|Appendices [A-Z]{2}\d{2}[–-][A-Z]{2}\d{2}) · ([^|]+)\| ([^|]+)\| ([^|]+)\| ([^|]+)\| ([^|]+)\|")
LEDGER = re.compile(r"(?m)^\| (R\d{2}) \| ([^|]*)\| ([^|]*)\| ([^|]*)\| (\w+) \|")
RID = r"(?:S[A-Z0-9]+-PP\d+|R\d{2})"
# Both register shapes: the 0.18.0 record (`### id · head` + `- **Landed**: x`)
# and the 0.17.0 row (`- id · head` + indented `landed: x`), so a register
# written under either law keeps its `landed:` on regeneration.
REG_ROW = re.compile(r"(?m)^(?:###|-) (" + RID + r") · .*?\n(?:(?:  |- \*\*).*\n)*?(?:  landed:|- \*\*Landed\*\*:)\s*(.*?)\s*$")


def expand_ids(text):
    """'SM04 + SM05' -> {SM04, SM05} · 'AM01–AM06' -> {AM01..AM06}"""
    ids = set(PAGE_ID.findall(text))
    for a, lo, b, hi in RANGE.findall(text):
        b = b or a
        if a == b:
            ids |= {f"{a}{n:02d}" for n in range(int(lo), int(hi) + 1)}
    return ids


def rounds(board):
    """Every Round page on the board, by path."""
    out = []
    for md in sorted(Path(board).glob("*/*/*.md")):
        if md.parent.name != md.stem or "_archive" in md.parts:
            continue
        head = md.read_text(encoding="utf-8", errors="replace")[:600]
        if re.search(r"(?m)^page-type:\s*round\b", head):
            out.append(md)
    return out


def parse_round(md):
    """-> {verdicts: {page: (verdict, consensus, gate, order)}, rows: {page: [row…]}, ledger}

    row = {id, head, parent, anchors, state, feedback, work, parents:[(rid, concern, pages)]}"""
    t = md.read_text(encoding="utf-8", errors="replace")
    verdicts = {}
    for pages, _title, verdict, consensus, order, gate in A_ROW.findall(t):
        for p in expand_ids(pages):
            verdicts[p] = (verdict.strip(), consensus.strip(), gate.strip(), order.strip())
    # §2 ledger: R-rows and the pages each routes to. A page named here but
    # holding no §2B block (the Narrative, typically) still owes a register,
    # keyed by the R id; and a Section whose parent R-row also routes to a
    # Narrative WAITS on that Narrative (the Round's own routing table:
    # claim role and paper order are ruled there first).
    ledger = {}
    for rid, anchors, concern, affected, state in LEDGER.findall(t):
        concern = concern.strip()
        # head = the first sentence, keeping a closing quote that follows the
        # period (`…online-review study.”` lost its quote to split(".") before)
        m = re.match(r"(.+?[.!?])([”’\"]?)(?:\s|$)", concern)
        ledger[rid] = dict(id=rid, head=(m.group(1) + m.group(2)) if m else concern,
                           parent="—", anchors=anchors.strip(), state=state.strip(),
                           feedback=concern, work=affected.strip(), parents=[],
                           pages=expand_ids(affected))
    rows = {}
    for m in HEAD.finditer(t):
        pages = expand_ids(m.group(2))
        end = t.find("\n#### ", m.end())
        block = t[m.end(): end if end > 0 else len(t)]
        for rid, head, paren, body, state in ROW.findall(block):
            parent = re.search(r"parent ([^;]+)", paren)
            anchors = paren.split(";", 1)[1].strip() if ";" in paren else ""
            fb = re.search(r"\*\*Feedback:\*\*\s*(.*?)\s*(?=\*\*Work:\*\*|$)", body, re.S)
            wk = re.search(r"\*\*Work:\*\*\s*(.*?)\s*$", body, re.S)
            pids = re.findall(r"R\d{2}", parent.group(1)) if parent else []
            row = dict(id=rid, head=head.strip(), parent=(parent.group(1).strip() if parent else ""),
                       anchors=anchors, state=state.strip(),
                       feedback=fb.group(1).strip() if fb else "", work=wk.group(1).strip() if wk else "",
                       parents=[(q, ledger[q]["feedback"], ledger[q]["pages"]) for q in pids if q in ledger])
            for p in pages:
                rows.setdefault(p, []).append(row)
    # decide the block-less pages ONCE; checking per row appended only the
    # first ledger row (NA01 got 1 of its 5, 260831)
    no_block = {p for r in ledger.values() for p in r["pages"] if p not in rows}
    for r in ledger.values():
        for p in r["pages"] & no_block:            # no §2B block: the ledger row IS the row
            rows.setdefault(p, []).append({k: v for k, v in r.items() if k != "pages"})
    return dict(verdicts=verdicts, rows=rows, ledger=ledger)


def register_path(page_md, round_md=None):
    """ONE file per page, `<stem>-feedback.md`, grouped by Round inside (JL
    260831: "or we just have feedback.md"). Fully DERIVED except `landed:`, so
    whole-file regeneration is safe and no generated-block fence is needed."""
    return page_md.parent / "outline" / f"{page_md.stem}-feedback.md"


def read_landed(reg):
    """The page's own pen: {row id: landed} from an existing register."""
    if not reg.exists():
        return {}
    return {rid: v for rid, v in REG_ROW.findall(reg.read_text(encoding="utf-8", errors="replace"))}


def register_ids(reg):
    if not reg.exists():
        return set()
    return set(re.findall(r"(?m)^(?:###|-) (" + RID + r") · ", reg.read_text(encoding="utf-8", errors="replace")))
