"""Adopt the Draft into the Page: `page.py adopt <page> [--dry-run]`.

The Draft Markdown (`draft/<stem>-draft-v<G>.<S>.md`, its `## 3 · Draft`) is the
working candidate; the Page Face's `## Content` is what prints. Nothing copies
one into the other on save: a person or the writing agent runs this at "apply".

What it does, per Page paragraph (a `###`/`####` heading block whose sentence
lines carry `<!-- realizes: C<n>.P<m>.B<k> -->`):

  1. the paragraph's sentences are rewritten in Draft order, each Draft on its
     own tagged line (a multi-line Draft or a `$$` display keeps its lines);
  2. a sentence already equal to its Draft keeps its Page lines untouched;
  3. every line under a sentence that is not its prose (`> Value:`,
     `> Citation:`, `> Display:`, a review mark, a comment) moves with it;
     under a sentence whose address was cut it is dropped and reported;
  4. headings, and lines above a paragraph's first sentence (a job line), stay
     where they are; untagged lines under a sentence stay with it and are named;
  5. the evidence lines under each sentence (`> Value:`, `> Citation:`,
     `> Display:`, `> Supporting Run:`) are rewritten from the Draft's Bullet
     fields and the Evidence Markdown (src/evidence_lines.py), right under the
     sentence; a `>` line that names no Evidence Item stays as written.

It refuses, and writes nothing, when the Draft's paragraphs and the Page's
paragraphs are not the same set: a Draft paragraph with no Page paragraph, a
tagged Page paragraph the Draft lacks, a heading block that mixes paragraphs,
or one paragraph under two headings (no guessing). Afterwards the Folder health
sync check passes: every Draft equals its Page sentence.
"""
from __future__ import annotations

import datetime
import difflib
import re
from pathlib import Path

from .evidence_lines import cite_keys_of, derive, owned
from .folder_health import REALIZES, _page_md, _page_sentences, check_sync
from .outline_version import latest_outline, plan_dir
from .plan_shape import iter_plan_bullets

HEADING = re.compile(r"^#{3,6} ")
DRAFT_SECTION = re.compile(r"(?m)^## \d+ · Draft\b")
DRAFT_PARAGRAPH = re.compile(r"^### (C\d+\.P\d+)\b")
DRAFT_BULLET = re.compile(r"^- (?:\[[ xX]\]\s*)?B(\d+)\s*·")
NOT_PROSE = ("#", ">", "<!--", "-", "|", "```", "*")   # what folder_health does not read as sentence text
# a Draft that is still a marker, not a sentence: `[open · E05 · …] …`, `[block E02 · unchanged] …`
MARKER = re.compile(r"^\[(?:open|block|pending|todo|tbd|placeholder)\b[^\]]*\]", re.I)


def _draft_order(plan_text: str, blocks: list) -> dict:
    """Paragraph → its Bullet addresses in Draft order. The plan's Bullet order is the
    frame; the Bullets `## 3 · Draft` lists fill their own places in the order it lists
    them, so a Section 3 that lists only some Bullets never moves the others."""
    listed: dict = {}
    match = DRAFT_SECTION.search(plan_text)
    if match:
        paragraph = None
        for line in plan_text[match.end():].splitlines():
            if line.startswith("## "):
                break
            head = DRAFT_PARAGRAPH.match(line)
            if head:
                paragraph = head.group(1)
                continue
            bullet = DRAFT_BULLET.match(line)
            if bullet and paragraph:
                listed.setdefault(paragraph, []).append("%s.B%s" % (paragraph, bullet.group(1)))
    plan: dict = {}
    for b in blocks:
        plan.setdefault(b["address"].rsplit(".", 1)[0], []).append(b["address"])
    order = {}
    for paragraph, addresses in plan.items():
        mine = [a for a in listed.get(paragraph, []) if a in addresses]
        slots = iter(mine)
        order[paragraph] = [next(slots) if a in mine else a for a in addresses]
    return order


def _content_span(lines: list) -> tuple[int, int] | None:
    start = next((i for i, line in enumerate(lines) if re.match(r"^## Content\s*$", line)), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start + 1, end


def _heading_blocks(lines: list) -> list:
    """Content lines → [{head, lines}] split at every `###`-or-deeper heading."""
    blocks = [{"head": None, "lines": []}]
    for line in lines:
        if HEADING.match(line):
            blocks.append({"head": line, "lines": []})
        else:
            blocks[-1]["lines"].append(line)
    return blocks


def _units(lines: list) -> tuple[list, list]:
    """A paragraph's lines → (lead, units). A unit is one tagged sentence: its
    prose lines (the tagged line, contiguous prose, a `$$` block resumed after a
    blank line: what folder_health reads as its text) and the lines under it."""
    lead, units = [], []
    current = held = None
    blanks: list = []
    in_math = False
    for line in lines:
        stripped = line.strip()
        if in_math:
            current["prose"].append(line)
            in_math = stripped != "$$"
            continue
        match = REALIZES.match(line)
        if match:
            (units[-1]["under"] if units else lead).extend(blanks)
            blanks = []
            current, held = {"address": match.group(2), "prose": [line], "under": []}, None
            units.append(current)
            continue
        if stripped == "$$" and (current or held):
            current, held, in_math = current or held, None, True
            current["prose"].extend(blanks + [line])
            blanks = []
            continue
        if current and stripped and not line.lstrip().startswith(NOT_PROSE):
            current["prose"].append(line)
            continue
        if not stripped:
            held, current = current or held, None
            blanks.append(line)
            continue
        (units[-1]["under"] if units else lead).extend(blanks + [line])
        blanks = []
        current = held = None
    (units[-1]["under"] if units else lead).extend(blanks)
    return lead, units


def _text(lines: list) -> str:
    return _page_sentences("\n".join(lines)).get(REALIZES.match(lines[0]).group(2), "")


def _draft_lines(address: str, draft: str) -> list:
    """A Draft as Page lines: the first line carries the tag; a multi-line Draft or
    a `$$` display keeps its lines, the way the Page already writes them."""
    lines = draft.strip().splitlines()
    return ["%s <!-- realizes: %s -->" % (lines[0].rstrip(), address)] + [l.rstrip() for l in lines[1:]]


def _trailing_blanks(lines: list) -> tuple[list, list]:
    n = len(lines)
    while n and not lines[n - 1].strip():
        n -= 1
    return lines[:n], lines[n:]


def adopt(target, *, plan: Path | None = None) -> dict:
    """Compute the adopted Page. Returns {page, plan, refused, text, changes, dropped, notes}."""
    page = _page_md(Path(target))
    folder, stem = page.parent, page.stem
    plan = Path(plan) if plan else latest_outline(plan_dir(folder), stem)
    report = {"page": str(page), "plan": plan.name if plan else None, "refused": [], "text": None,
              "changes": [], "dropped": [], "notes": []}
    if plan is None or not plan.is_file():
        report["refused"].append("no current Draft Markdown in %s/" % plan_dir(folder).name)
        return report
    plan_text = plan.read_text(encoding="utf-8")
    blocks = iter_plan_bullets(plan_text)
    drafts = {b["address"]: b["draft"] for b in blocks}
    order = _draft_order(plan_text, blocks)
    wanted = {p for p, addrs in order.items() if any(drafts.get(a) for a in addrs)}
    text = page.read_text(encoding="utf-8")
    lines = text.split("\n")
    span = _content_span(lines)
    if span is None:
        report["refused"].append("the Page has no `## Content` section")
        return report
    evidence = derive(page, blocks)
    blocks_ = _heading_blocks(lines[span[0]:span[1]])
    on_page: dict = {}
    for i, block in enumerate(blocks_):
        lead, units = _units(block["lines"])
        block["lead"], block["units"] = lead, units
        paragraphs = {u["address"].rsplit(".", 1)[0] for u in units}
        where = (block["head"] or "(before the first heading)").strip()
        if len(paragraphs) > 1:
            report["refused"].append("%s mixes paragraphs %s" % (where, ", ".join(sorted(paragraphs))))
        elif paragraphs:
            paragraph = paragraphs.pop()
            if paragraph in on_page:
                report["refused"].append("%s appears under two headings" % paragraph)
            on_page[paragraph] = i
            block["paragraph"] = paragraph
    missing = sorted(wanted - set(on_page), key=_address_key)
    extra = sorted(set(on_page) - set(order), key=_address_key)
    if missing:
        report["refused"].append("Draft paragraph(s) with no Page paragraph: %s" % ", ".join(missing))
    if extra:
        report["refused"].append("Page paragraph(s) the Draft lacks: %s" % ", ".join(extra))
    if report["refused"]:
        return report
    out = lines[:span[0]]
    for block in blocks_:
        if block["head"] is not None:
            out.append(block["head"])
        paragraph = block.get("paragraph")
        if not paragraph:
            out.extend(block["lines"])
            continue
        out += _adopt_paragraph(block, paragraph, order.get(paragraph, []), drafts, report, evidence)
    if report["refused"]:
        return report
    out += lines[span[1]:]
    report["text"] = "\n".join(out)
    findings: list = []
    check_sync(report["text"], blocks, plan_text, findings)
    report["sync"] = [(f.level, f.message) for f in findings]
    return report


def _group(units: list) -> list:
    """Units → one per address, at its first place. One address tagged on several
    lines is one sentence (folder_health joins them); its lines keep their order."""
    out, by = [], {}
    for unit in units:
        lines = unit["prose"] + unit["under"]
        if unit["address"] in by:
            by[unit["address"]]["lines"] += lines
            by[unit["address"]]["under"] += unit["under"]
            continue
        by[unit["address"]] = {"address": unit["address"], "lines": lines, "under": list(unit["under"]),
                               "prose": len(unit["prose"])}
        out.append(by[unit["address"]])
    for g in out:
        g["lines"], g["gap"] = _trailing_blanks(g["lines"])
        g["under"] = _trailing_blanks(g["under"])[0]
    return out


def _with_evidence(lines: list, prose: int, address: str, evidence: dict | None, changes: list) -> list:
    """A sentence's lines with its derived evidence lines right under its prose; the
    lines it owned before are replaced, every other line keeps its place."""
    if evidence is None or address not in evidence:
        return lines
    want = evidence[address]
    keys = cite_keys_of(want)
    kept = [l for l in lines if not owned(l, keys)]
    new = kept[:prose] + want + kept[prose:]
    if new != lines:
        had = {l.strip() for l in lines if owned(l, keys)}
        plus = sum(1 for w in want if w not in had)
        minus = len(had - set(want))
        changes.append("evidence lines %s: %s" % (address, "+%d −%d" % (plus, minus) if plus or minus else "reordered"))
    return new


def _adopt_paragraph(block: dict, paragraph: str, order: list, drafts: dict, report: dict,
                     evidence: dict | None = None) -> list:
    """One Page paragraph in Draft order; its original lines when nothing changes."""
    groups = _group(block["units"])
    by = {g["address"]: g for g in groups}
    pieces, sequence, changes, evidence_changes = [], [], [], []
    for address in order:
        g, draft = by.pop(address, None), drafts.get(address, "")
        marker = MARKER.match(draft.strip()) if draft else None
        if marker:
            report["notes"].append("%s Draft is still a marker (%s); left off the Page"
                                   % (address, marker.group(0)[:40]))
            draft = ""
        if not draft:
            if g:
                if not marker:
                    report["notes"].append("%s has no Draft; its Page sentence is kept" % address)
                pieces.append(_with_evidence(g["lines"], g["prose"], address, evidence, evidence_changes))
                sequence.append(address)
            continue
        sequence.append(address)
        page_text = _page_sentences("\n".join(g["lines"])).get(address, "") if g else ""
        if g and " ".join(page_text.split()) == " ".join(draft.split()):
            pieces.append(_with_evidence(g["lines"], g["prose"], address, evidence, evidence_changes))
            continue
        changes.append(("rewritten" if g else "added") + " " + address)
        sentence = _draft_lines(address, draft)
        pieces.append(_with_evidence(sentence + (g["under"] if g else []), len(sentence), address,
                                     evidence, evidence_changes))
    cut = list(by.values())                       # sentences whose address the Draft no longer has
    old = [g["address"] for g in groups]
    if not changes and not evidence_changes and not cut and sequence == old:
        return block["lines"]
    # untagged material under a sentence (a fenced block, a list, a link, loose prose) moves or
    # goes with it: only rewrites in place are safe there, anything else is left to a person
    loose = [l.strip() for g in groups for l in g["under"] if l.strip() and not l.lstrip().startswith((">", "<!--"))]
    moved = [a for a in sequence if a in old] != [a for a in old if a in sequence]
    added = [c.split()[-1] for c in changes if c.startswith("added")]
    if loose and (added or cut or moved):
        report["refused"].append(
            "%s holds %d untagged line(s) under its sentences (e.g. %s); %s would move or drop them: "
            "place %s by hand, then adopt" % (paragraph, len(loose), loose[0][:50],
                                             "adding " + ", ".join(added) if added else ("cutting a sentence" if cut else "reordering"),
                                             "the Draft sentence(s)" if added else "the change"))
        return block["lines"]
    report["changes"] += changes + ["removed " + g["address"] for g in cut] + evidence_changes
    report["dropped"] += ["%s · %s" % (g["address"], l.strip()) for g in cut for l in g["under"] if l.strip()]
    blank = len(groups) > 1 and all(g["gap"] for g in groups[:-1])    # sentences set one per paragraph
    body = []
    for i, piece in enumerate(pieces):
        body += piece + ([""] if blank and i < len(pieces) - 1 else [])
    return block["lead"] + body + groups[-1]["gap"]


def _address_key(address: str) -> tuple:
    return tuple(int(n) for n in re.findall(r"\d+", address))


def content_line(text: str, plan_name: str, now: datetime.datetime | None = None) -> str:
    """Set the Page header's `content:` line: which Draft is in `## Content`, and when.

    Code keeps this record (JL 260928: agents keep text, code keeps records); no agent
    types a version or a date into `state:`. The line is replaced in place, or put
    right after `state:` (else after the title) on its first adoption."""
    m = re.search(r"-(draft|outline)-v([0-9][0-9.]*)\.md$", plan_name or "")
    source = "%s v%s" % (m.group(1), m.group(2)) if m else (plan_name or "Draft")
    line = "content: %s · adopted %s" % (source, (now or datetime.datetime.now()).strftime("%y%m%d %H%M"))
    lines = text.split("\n")
    head_end = next((i for i, l in enumerate(lines) if l.startswith("## ")), len(lines))
    at = next((i for i in range(head_end) if lines[i].startswith("content:")), None)
    if at is not None:
        lines[at] = line
    else:
        after = next((i for i in range(head_end) if lines[i].startswith("state:")),
                     next((i for i in range(head_end) if lines[i].startswith("# ")), -1))
        lines.insert(after + 1, line)
    return "\n".join(lines)


def run(target, *, plan: Path | None = None, dry_run: bool = False) -> dict:
    """Adopt and, unless `dry_run`, write the Page. Adds a unified `diff`."""
    report = adopt(target, plan=plan)
    if report["refused"]:
        return report
    if report["changes"]:
        report["text"] = content_line(report["text"], report["plan"])
    page = Path(report["page"])
    before = page.read_text(encoding="utf-8")
    report["diff"] = "".join(difflib.unified_diff(
        before.splitlines(True), report["text"].splitlines(True), page.name, page.name + " (adopted)"))
    if report["diff"] and not dry_run:
        page.write_text(report["text"], encoding="utf-8")
    report["written"] = bool(report["diff"]) and not dry_run
    return report


def render(report: dict) -> str:
    name = Path(report["page"]).stem
    if report["refused"]:
        return "\n".join(["❌ %s · refused, nothing written (plan %s)" % (name, report["plan"])]
                         + ["   - %s" % r for r in report["refused"]])
    changes = report["changes"]
    head = ("✅ %s · already equals its Draft (%s)" % (name, report["plan"]) if not changes else
            "%s %s · %d change(s) from %s" % ("✏️" if report["written"] else "🔎", name, len(changes), report["plan"]))
    out = [head] + ["   - %s" % c for c in changes]
    out += ["   dropped with its cut sentence: %s" % d for d in report["dropped"]]
    out += ["   note: %s" % n for n in report["notes"]]
    out += ["   sync after adopt: %s %s" % (level, message) for level, message in report.get("sync", [])]
    if changes and not report["written"]:
        out.append(report["diff"].rstrip("\n"))
    return "\n".join(out)
