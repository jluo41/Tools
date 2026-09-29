"""Three-section Draft Markdown: one skeleton, three sections (0.118).

    ## 1 · Structure · Bullet Point Table   Structure Overview, then per paragraph
                                            each Bullet's Point and plan lines
    ## 2 · Scratch · What to write here     per paragraph: rough notes
    ## 3 · Draft · Reading and Revise       per paragraph: the sentences

Every section repeats the same `### C<n>.P<m>` headings and `- B<k>` numbers,
so a Bullet's Point (section 1) and its sentence (section 3) share one address.
The Structure Overview declares each division as `- C<n> · <title>` and gives
each paragraph a three-line entry: its title, then its sentences and job, then
the question that leads to the next paragraph:

    - C1.P1 · Physician prescribing behavior
      → S1 to S6 · quality and spending · comparable decisions · opioid example
      → C1.P2: Could interpersonal dispositions help explain variation?

Readers keep one grammar: `to_canonical` folds the Draft section back into the
Draft-first plan every parser already reads. Writers edit that plan and hand it
to `from_canonical`, which writes sections 1 and 3 again and keeps the
Structure Overview, the Scratch notes and any trailing sections as they were.
"""
from __future__ import annotations

import re

SECTION = re.compile(r"^## (\d+) · (Structure|Scratch|Draft)\b")
SECTIONED = re.compile(r"(?m)^## \d+ · Structure\b")
PARAGRAPH = re.compile(r"^### (C\d+\.P\d+)\b")
DIVISION_HEAD = re.compile(r"^## (C\d+)\b\s*(?:·\s*(.*))?$")
DIVISION_LINE = re.compile(r"^- (C\d+) · (.+)$")
BULLET = re.compile(
    r"^(?P<prefix>- (?:\[[ xX]\]\s*)?(?:B|S)(?P<number>\d+)\s*·\s*)"
    r"(?P<tag>S\d+[a-z]?(?:\s*(?:-|–|to)\s*S\d+[a-z]?)?\s*·\s*)?(?P<text>.*)$"
)


def is_sectioned(text: str) -> bool:
    return bool(SECTIONED.search(text or ""))


def _sections(text: str):
    """-> (header lines, {kind: [heading, body lines]}, section order, tail lines)."""
    header, sections, order, tail = [], {}, [], []
    current = None
    for line in text.split("\n"):
        match = SECTION.match(line)
        if match and match.group(2).lower() not in sections:
            current = match.group(2).lower()
            sections[current] = [line, []]
            order.append(current)
            continue
        if line.startswith("## ") and current is not None:
            current = "tail"
        if current is None:
            header.append(line)
        elif current == "tail":
            tail.append(line)
        else:
            sections[current][1].append(line)
    return header, sections, order, tail


def _paragraphs(body: list[str]):
    """-> (lines before the first `### C.P`, [[heading, address, lines], ...])."""
    intro, blocks = [], []
    for line in body:
        match = PARAGRAPH.match(line)
        if match:
            blocks.append([line, match.group(1), []])
        elif blocks:
            blocks[-1][2].append(line)
        else:
            intro.append(line)
    return intro, blocks


def _bullets(lines: list[str]):
    """-> [(dash line, indented continuation lines)] in order."""
    out, i = [], 0
    while i < len(lines):
        if BULLET.match(lines[i]):
            j = i + 1
            while j < len(lines) and lines[j].startswith("  "):
                j += 1
            out.append((lines[i], lines[i + 1:j]))
            i = j
        else:
            i += 1
    return out


def _trim(lines: list[str]) -> list[str]:
    lines = list(lines)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def _title(heading: str) -> str:
    """`### C1.P2 · Agreeableness · S7 to S12` → `Agreeableness`."""
    parts = heading.split(" · ")
    return parts[1].strip() if len(parts) > 1 else ""


def division_titles(intro: list[str]) -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for line in intro if (m := DIVISION_LINE.match(line))}


def to_canonical(text: str) -> str:
    """Fold a three-section Draft Markdown into the Draft-first plan."""
    if not is_sectioned(text):
        return text
    header, sections, _order, tail = _sections(text)
    s_intro, s_blocks = _paragraphs(sections["structure"][1])
    _d_intro, d_blocks = _paragraphs(sections.get("draft", ["", []])[1])
    titles = division_titles(s_intro)
    drafts = {}
    for _heading, address, lines in d_blocks:
        for line, more in _bullets(lines):
            drafts[(address, BULLET.match(line).group("number"))] = (line, more)
    out = _trim(header) + [""]
    division = None
    for heading, address, lines in s_blocks:
        this = address.split(".")[0]
        if this != division:
            division = this
            out += ["## %s · %s" % (this, titles[this]) if titles.get(this) else "## " + this, ""]
        out.append(heading)
        for line, more in _bullets(lines):
            head = BULLET.match(line)
            drafted = drafts.get((address, head.group("number")))
            if drafted:
                text_line = BULLET.match(drafted[0]).group("text")
                out.append(head.group("prefix") + (head.group("tag") or "") + text_line)
                out += drafted[1]
                out.append("  Point: " + head.group("text"))
                out += more
            else:
                out += [line] + more
        out.append("")
    out += tail
    return "\n".join(_trim(out)) + "\n"


def _canonical_blocks(canonical: str):
    """-> (header, [(division, title)], [(heading, address, bullets)], tail) from any plan shape."""
    from .plan_shape import split_bullet_block

    lines = canonical.split("\n")
    header, divisions, paragraphs, tail = [], [], [], []
    i, seen_division, paragraph_seen = 0, False, False
    while i < len(lines):
        line = lines[i]
        division = DIVISION_HEAD.match(line)
        if division:
            seen_division, paragraph_seen = True, False
            divisions.append((division.group(1), (division.group(2) or "").strip()))
            i += 1
            continue
        if line.startswith("## ") and seen_division:
            tail = lines[i:]
            break
        if not seen_division:
            header.append(line)
            i += 1
            continue
        paragraph = PARAGRAPH.match(line)
        if paragraph:
            paragraphs.append((line, paragraph.group(1), []))
            paragraph_seen = True
            i += 1
            continue
        if BULLET.match(line):
            if not paragraph_seen:
                # A Bullet straight under `## C<n>`, before any paragraph heading, sits in
                # paragraph P1 (plan_shape.iter_plan_bullets numbers it so).
                this = divisions[-1][0]
                paragraphs.append(("### %s.P1" % this, "%s.P1" % this, []))
                paragraph_seen = True
            j = i + 1
            while j < len(lines) and lines[j].startswith("  "):
                j += 1
            paragraphs[-1][2].append(split_bullet_block(line, lines[i + 1:j]))
            i = j
            continue
        i += 1
    return header, divisions, paragraphs, tail


def canonical_extras(canonical: str) -> tuple[dict, dict]:
    """Lines of a Draft-first plan that are neither a heading nor a Bullet block.

    -> ({division: lines}, {paragraph address: lines}). A note under a paragraph
    (`%% …`, `- Note: …`, a JL remark) belongs to that paragraph; a line before a
    division's first paragraph, or under a heading that is not `### C<n>.P<m>`
    (`### Cut · …`, `### Survey`), belongs to the division, heading included.
    The three-section layout has no place for them in sections 1 and 3, so the
    migration writer keeps them in section 2 (Scratch) under the same target.
    """
    lines = canonical.split("\n")
    by_division, by_paragraph = {}, {}
    division = paragraph = None
    in_block = False  # under a `###` heading that is not a paragraph (`### Cut · …`)
    i = 0
    while i < len(lines):
        line = lines[i]
        head = DIVISION_HEAD.match(line)
        if head:
            division, paragraph, in_block = head.group(1), None, False
            i += 1
            continue
        if division is None:
            i += 1
            continue
        if line.startswith("## "):
            break  # the tail is kept as it is
        match = PARAGRAPH.match(line)
        if match:
            paragraph, in_block = match.group(1), False
            i += 1
            continue
        if BULLET.match(line) and (paragraph or not in_block):
            # a Bullet straight under `## C<n>` is a Bullet of C<n>.P1, not a note
            i += 1
            while i < len(lines) and lines[i].startswith("  "):
                i += 1
            continue
        if line.startswith("### "):
            paragraph, in_block = None, True  # a block that is not a paragraph belongs to the division
        target = by_paragraph.setdefault(paragraph, []) if paragraph else by_division.setdefault(division, [])
        target.append(line)
        i += 1
    trim = lambda block: _trim(block[next((k for k, x in enumerate(block) if x.strip()), len(block)):])
    return ({k: trim(v) for k, v in by_division.items() if trim(v)},
            {k: trim(v) for k, v in by_paragraph.items() if trim(v)})


def from_canonical(original: str, canonical: str) -> str:
    """Write an edited plan back into the three sections of `original`."""
    if not is_sectioned(original):
        return canonical
    _h, sections, order, _tail = _sections(original)
    s_intro, _ = _paragraphs(sections["structure"][1])
    d_intro, _ = _paragraphs(sections.get("draft", ["", []])[1])
    header, _divisions, paragraphs, tail = _canonical_blocks(canonical)
    structure, draft = [], []
    for heading, _address, bullets in paragraphs:
        structure += ["", heading]
        draft += ["", heading]
        for prefix, tag, point, plan_lines, text, reviews in bullets:
            structure.append(prefix + tag + point)
            structure += ["  " + x for x in plan_lines if x]
            structure += ["  " + x for x in (reviews or "").splitlines() if x.strip()]
            words = [x.strip() for x in (text or "").strip().splitlines()]
            if words:
                draft.append(prefix + tag + words[0])
                draft += ["  " + x if x else "  " for x in words[1:]]
    _notes, tail, _rewritten = legacy_scratch(tail)  # its notes went to section 2 (to_sectioned)
    # A renamed paragraph keeps one name everywhere: its overview line and its
    # Scratch heading follow the heading the edited plan now carries.
    new_heads = {address: heading for heading, address, _b in paragraphs}
    old_heads = {address: heading for heading, address, _l in _paragraphs(sections["structure"][1])[1]}
    for address, heading in new_heads.items():
        old, new = _title(old_heads.get(address, "")), _title(heading)
        if old and new and old != new:
            prefix = "- %s · " % address
            s_intro = [prefix + new + line[len(prefix) + len(old):]
                       if line.startswith(prefix + old) else line for line in s_intro]
    scratch = [new_heads.get(m.group(1), line) if (m := PARAGRAPH.match(line)) else line
               for line in sections.get("scratch", ["", []])[1]]
    built = {
        "structure": [sections["structure"][0]] + _trim(s_intro) + structure,
        "draft": [sections["draft"][0]] + _trim(d_intro) + draft if "draft" in sections else [],
        "scratch": [sections["scratch"][0]] + _trim(scratch) if "scratch" in sections else [],
    }
    out = _trim(header)
    for kind in order:
        out += [""] + _trim(built[kind])
    if tail:
        out += [""] + _trim(tail)
    return "\n".join(out) + "\n"


def overview_entries(divisions, paragraphs) -> list[str]:
    """Each division line, then its paragraphs as `- C.P · title` / `→ S.. to S..`.

    The job and the question to the next paragraph are the person's words, so
    a generated entry leaves them for the person to add after the span.
    """
    out = []
    for division, title in divisions:
        out.append("- %s · %s" % (division, title) if title else "- " + division)
        for heading, address, _b in paragraphs:
            if address.split(".")[0] != division:
                continue
            parts = heading[4:].split(" · ")
            out.append("- %s · %s" % (address, parts[1]) if len(parts) > 1 else "- " + address)
            span = next((x for x in parts[2:] if x.startswith("S")), "")
            if span:
                out.append("  → " + span)
    return out


def to_sectioned(canonical: str, *, scratch: dict | None = None,
                 overview: list[str] | None = None) -> str:
    """Lay a Draft-first plan out in three sections (the migration writer).

    `overview` defaults to `overview_entries`; `scratch` maps a paragraph
    address to note lines. Lines that are neither a heading nor a Bullet
    (`canonical_extras`) go to Scratch under their paragraph or division, so
    no word of the plan is lost.
    """
    header, divisions, paragraphs, tail = _canonical_blocks(canonical)
    if overview is None:
        overview = overview_entries(divisions, paragraphs)
    by_division, by_paragraph = canonical_extras(canonical)
    legacy, tail, _rewritten = legacy_scratch(tail)
    scratch = {k: list(v) for k, v in (scratch or {}).items()}
    for target, lines in legacy.items():
        scratch.setdefault(target, []).extend(lines)
    notes, placed = [], set()
    listed = [d for d, _t in divisions]
    for division in listed + sorted({a.split(".")[0] for _h, a, _b in paragraphs} - set(listed)):
        if by_division.get(division) or scratch.get(division):
            title = dict(divisions).get(division, "")
            notes += ["", "### %s · %s" % (division, title) if title else "### " + division]
            notes += scratch.get(division, []) + by_division.get(division, [])
            placed.add(division)
        for h, a, _b in paragraphs:
            if a.split(".")[0] == division:
                notes += ["", h] + scratch.get(a, []) + by_paragraph.get(a, [])
                placed.add(a)
    for target in sorted(set(scratch) - placed):  # a note whose target the plan no longer has
        notes += ["", "### " + target] + scratch[target]
    skeleton = "\n".join(
        ["## 1 · Structure · Bullet Point Table", "", "### Structure Overview", ""]
        + overview
        + ["", "## 2 · Scratch · What to write here", ""]
        + notes
        + ["", "## 3 · Draft · Reading and Revise", ""]
    )
    body = "\n".join(_trim(header)) + "\n\n" + skeleton + "\n"
    if tail:
        body += "\n" + "\n".join(tail)
    return from_canonical(body, canonical)


LEGACY_RECORD = re.compile(r"^### (?P<run>rp-scratch-\d+_\S+) · (?P<scope>\w+) · (?P<target>C\d+(?:\.P\d+)?)\s*$")
LEGACY_FIELD = re.compile(r"^- (Scope|Target|Status|Started|Updated|Run|Notes|Summary):")


def legacy_scratch(tail: list[str]) -> tuple[dict, list[str], set]:
    """The 0.117 `## Scratch` registry in a plan's tail, for the three-section layout.

    -> ({target: section-2 lines}, the tail without the registry, the registry lines
    that were rewritten). Each record becomes the block `write_scratch` writes: the
    Run marker, the Notes words, and one `> Summary:` line. Its Scope, Target,
    Started, Updated and Run fields are not copied: the Scratch Run's ticket and
    Result under runs/ and results/ hold them.
    """
    start = next((k for k, line in enumerate(tail) if re.match(r"^## Scratch\s*$", line)), None)
    if start is None:
        return {}, tail, set()
    end = next((k for k in range(start + 1, len(tail)) if tail[k].startswith("## ")), len(tail))
    body, rest = tail[start + 1:end], tail[:start] + tail[end:]
    records, rewritten, record, field = [], {"## Scratch"}, None, None
    for line in body:
        head = LEGACY_RECORD.match(line)
        if head:
            record = dict(head.groupdict(), status="open", Notes=[], Summary=[])
            records.append(record)
            rewritten.add(line.strip())
            field = None
            continue
        if record is None:
            if line.strip():
                return {}, tail, set()  # words before the first record: not a registry
            continue
        name = LEGACY_FIELD.match(line)
        if name:
            rewritten.add(line.strip())
            if name.group(1) == "Status":
                record["status"] = line.split(":", 1)[1].strip() or "open"
            field = name.group(1) if name.group(1) in ("Notes", "Summary") else None
            continue
        if field and (line.startswith("  ") or not line.strip()):
            record[field].append(line[2:] if line.startswith("  ") else line)
            continue
        field = None
        record["Notes"].append(line)
    notes = {}
    for r in records:
        words = _trim(r["Notes"])
        words = words[next((k for k, x in enumerate(words) if x.strip()), len(words)):]
        summary = " ".join(" ".join(r["Summary"]).split())
        rewritten |= {x.strip() for x in r["Summary"] if x.strip()}
        block = ["<!-- %s · %s · %s -->" % (r["run"], r["scope"], r["status"])] + words
        notes.setdefault(r["target"], []).extend(block + (["> Summary: " + summary] if summary else []))
    return notes, rest, rewritten


# ── Scratch notes in section 2 ──────────────────────────────────────────────
# A note block sits under its target heading (`### C1.P2 …` or `### C1 …`).
# One hidden marker line names the Scratch Run that last saved it, so an
# autosave rewrites the same block; everything else in the block is the
# person's own words, plus an optional `> Summary:` line once it is finished.

SCRATCH_TARGET = re.compile(r"^### (C\d+(?:\.P\d+)?)(?=\s|$|·)")
SCRATCH_MARK = re.compile(
    r"^<!-- (?P<run>rp-scratch-\d+_[A-Za-z0-9._-]+|run-scratch-\d{4}-[a-z0-9-]+) · (?P<scope>\w+) · (?P<status>\w+) -->$"
)


def _assemble(header, sections, order, tail) -> str:
    out = list(header)
    for kind in order:
        out += [sections[kind][0]] + sections[kind][1]
    return "\n".join(out + tail)


def scratch_notes(text: str) -> list[dict]:
    """-> one record per Scratch block that holds words or a Run marker."""
    _header, sections, _order, _tail = _sections(text)
    if "scratch" not in sections:
        return []
    blocks, current = [], None
    for line in sections["scratch"][1]:
        match = SCRATCH_TARGET.match(line)
        if match:
            current = {"target": match.group(1), "lines": []}
            blocks.append(current)
        elif current is not None:
            current["lines"].append(line)
    records = []
    for block in blocks:
        run = scope = status = summary = ""
        notes = []
        for line in block["lines"]:
            mark = SCRATCH_MARK.match(line.strip())
            if mark:
                run, scope, status = mark["run"], mark["scope"], mark["status"]
            elif line.startswith("> Summary:"):
                summary = line[len("> Summary:"):].strip()
            else:
                notes.append(line)
        words = "\n".join(_trim(notes)).strip()
        if words or run:
            target = block["target"]
            records.append({"run": run, "target": target, "notes": words, "summary": summary,
                            "scope": scope or ("paragraph" if ".P" in target else "section"),
                            "status": status or "open"})
    return records


def write_scratch(text: str, target: str, notes: str, *, run: str, scope: str,
                  status: str, summary: str = "", title: str = "") -> str:
    """Put one note block under `target` in section 2; the rest of the file is unchanged."""
    header, sections, order, tail = _sections(text)
    if "scratch" not in sections:
        sections["scratch"] = ["## 2 · Scratch · What to write here", [""]]
        order.insert(order.index("structure") + 1 if "structure" in order else 0, "scratch")
    body = sections["scratch"][1]
    block = ["<!-- %s · %s · %s -->" % (run, scope, status)] + notes.strip().splitlines()
    if summary:
        block.append("> Summary: " + " ".join(summary.split()))
    at = next((i for i, line in enumerate(body)
               if (m := SCRATCH_TARGET.match(line)) and m.group(1) == target), None)
    if at is None:
        heading = "### %s · %s" % (target, title) if title else "### " + target
        first = next((i for i, line in enumerate(body) if SCRATCH_TARGET.match(line)), None)
        if ".P" not in target and first is not None:
            body[first:first] = [heading] + block + [""]
        else:
            body[len(_trim(body)):] = ["", heading] + block + [""]
    else:
        end = next((i for i in range(at + 1, len(body)) if body[i].startswith("### ")), len(body))
        body[at + 1:end] = block + [""]
    return _assemble(header, sections, order, tail)


# ── Structure Overview entries ──────────────────────────────────────────────
# The overview block holds prose (kept as is) and entries: `- C<n> · title`,
# `- C<n>.P<m> · title`, and each entry's `→` lines. The workbench Structure
# card shows the entries and edits them as text.

OVERVIEW_ENTRY = re.compile(r"^- (C\d+(?:\.P\d+)?)\b")


def _overview_span(body: list[str]):
    """-> (start, end) of the lines under `### Structure Overview`, or None."""
    start = next((i for i, line in enumerate(body) if line.startswith("### Structure Overview")), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(body)) if body[i].startswith("### ")), len(body))
    return start + 1, end


def overview_lines(text: str) -> list[str]:
    """The overview's entry lines: each `- C…` line and the `→` lines under it."""
    _h, sections, _o, _t = _sections(text)
    body = sections.get("structure", ["", []])[1]
    span = _overview_span(body)
    out = []
    for line in body[span[0]:span[1]] if span else []:
        if OVERVIEW_ENTRY.match(line) or (out and line.strip().startswith("→")):
            out.append(line.rstrip())
    return out


def normalize_overview(text: str) -> list[str]:
    """Typed overview text → entry lines (`C1.P1 · x` gains its `- `; `→` lines indent)."""
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("→"):
            out.append("  " + line)
        elif re.match(r"^-?\s*C\d+", line):
            out.append("- " + line.lstrip("- ").strip())
        else:
            raise ValueError("an overview line starts with C<n>, C<n>.P<m> or →: %s" % line[:60])
    return out


def set_overview(text: str, entries: list[str]) -> str:
    """Replace the overview's entry lines; the prose around them stays."""
    header, sections, order, tail = _sections(text)
    body = sections["structure"][1]
    span = _overview_span(body)
    if span is None:
        body[0:0] = ["", "### Structure Overview", ""] + entries
        return _assemble(header, sections, order, tail)
    block = body[span[0]:span[1]]
    marks = [i for i, line in enumerate(block)
             if OVERVIEW_ENTRY.match(line) or line.strip().startswith("→")]
    if marks:
        block[marks[0]:marks[-1] + 1] = entries
    else:
        block[len(_trim(block)):] = ([""] if _trim(block) else []) + entries + [""]
    body[span[0]:span[1]] = block
    return _assemble(header, sections, order, tail)
