"""📃 Page · the one parse: a Page's divisions, Aims, States and Files, pinned by id or §N anchor.

Moved out of outline.py (the 600-line rule); outline re-exports every name here.
"""
import re


# Aim state emoji (haipipe-draft): current set + the older ones still parsed.
DONE = {"✅"}
STATE_EMOJI = ("✅", "⬜", "🔨", "🧠", "❄️", "🟡", "🟠", "⏸️")

_SEC_ALIAS = {"opening": "opening", "question": "opening",
              "content": "content",
              "aims": "aims", "items to finish": "aims",
              "states": "states", "where we are": "states",
              "files": "files"}

# A division heading, `### 3 · Title` or `### §3 · Title`. A DOTTED heading
# (`### §6.1 · Title`) is one paragraph inside division 6, so it registers 6
# with no title of its own: an S page whose Content is written entirely as
# 6.1, 6.2 still gets its division 6 card, and its A6 aims land in it.
# One division grammar, the same one check.py:1176 splits on: `### 3 · Title`,
# `### §6.1 Main Results` (a Section page numbers by the MANUSCRIPT, with a
# space and no ` · `), and a dotted subdivision. Requiring the ` · ` here made
# every Section page's divisions invisible, so each `§7` anchor in its plan
# read as "invented" (JL 260830, 5 of 7 plan-checker failures on MISQ).
_DIV_RE = re.compile(r"^###\s+§?(\d+)(\.\d+)*(?:\s*·\s*(.*)|\s+(?!·)(.*))?\s*$")
# An Aims/States group. The leading `(?:[^\w\s]|\s)*` is not decoration: pages
# write `### 🗣 Decision Now` with the emoji BEFORE the name, and without this
# the decision block goes unrecognized and its pending asks leak into States as
# if they were current facts about an aim.
_GROUP_RE = re.compile(r"^###\s+(?:[^\w\s]|\s)*([AC](\d+)|P|Decision Now)\b")
# An Aim id is `A3.1` (division 3) or `P1` (page-wide, no division).
_ID_RE = re.compile(r"\b(?:[AC](\d+)\.\d+|P\d+)\b")
# `§` was already in use on a board before this workbench, with two OTHER meanings,
# so an anchor is the narrowest of the three and the other two are stepped over:
#   `QB6 §7` · `[QB7 §3](…)`  a division of ANOTHER page — a page id precedes it
#   `§5.1` · `§4.3`           a SUB-division — a dot follows it
#   `§Required Inputs`        a named section — no digit at all
# Miss this and a page citing a sibling reports a bad anchor it never wrote.
_ANCHOR_RE = re.compile(r"§(\d+)(?!\.?\d)")
_XREF_TAIL = re.compile(r"(?:[A-Za-z][A-Za-z-]*\d+[a-z]?)[`\]\)]?\s*$")


# POSITION is what separates an anchor from prose, and it has to be, because
# on a paper-section page `§4` is ordinary prose meaning the manuscript's
# section 4 ("Every number §4 prints traces to one atom"). No regex can read
# that intent, so an anchor is recognized only where prose does not put one:
#   an Aim or State row  ->  the anchor LEADS the text, after the checkbox,
#                            the state emoji, a decorative emoji, or an id
#   a Files row          ->  the anchors TRAIL the row, at its very end
_LEAD_STRIP = re.compile(
    r"^\s*(?:-\s*)?(?:\[[ xX]\]\s*)?"          # the bullet and its checkbox
    r"(?:[^\w\s§]|\s)*"                         # emoji and punctuation
    r"(?:(?:[ACP]\d+(?:\.\d+)?)\s*·?\s*)?"      # an Aim id, if the row has one
)
_TRAIL_ANCHORS = re.compile(r"((?:\s*§\d+(?!\.?\d))+)\s*$")


_CAPTION_RE = re.compile(r"^\*\*(?P<name>[^*]+)\*\*:\s*(?P<what>.+?)\s*$")


def _is_job_line(line):
    """A division's JOB LINE: the one-liner under its face diagram saying what
    the part settles. The template writes it `📌 This part fixes …`; pages in
    the wild also write `📋 Establishes …` and `🧭 Establishes …`. What they
    share is the shape, an emoji then a sentence, so that is what is read."""
    s = line.strip()
    if not s or s[0] < "←":
        return None
    body = s.lstrip("".join(c for c in s if c >= "←")).strip()
    return body or None


def _brief(lines):
    """-> one line saying what a division is about, taken from the material.

    In priority order: the JOB LINE (what this part settles), then the face
    diagram's CAPTION (what the figure shows), then the first plain sentence.
    A division with none of the three simply has no brief; nothing is invented,
    which is the same rule the anchors follow."""
    job = caption = prose = None
    fence = False
    for line in lines:
        if line.strip().startswith("```"):
            fence = not fence
            continue
        if fence or not line.strip():
            continue
        s = line.strip()
        if s.startswith((">", "#", "-", "|")):
            continue
        m = _CAPTION_RE.match(s)
        if m:
            caption = caption or m.group("what")
            continue
        if s.startswith("**"):          # a group title, not a sentence
            continue
        j = _is_job_line(s)
        if j:
            job = job or j
            continue
        prose = prose or s
    return job or caption or prose


_ID_LEAD = re.compile(r"^\s*(?:[^\w\s]\s*)*(?:[ACP]\d+(?:\.\d+)?)\s*·\s*")


def _strip_id(text):
    """Drop a row's own id from what the reader sees. The card already prints
    the id once, as a tag, and an Aim and its State both opening `A1.1 ·` is
    the fastest way to make two different sentences look like one repeated."""
    return _ID_LEAD.sub("", text).strip()


def _strip_anchors(text):
    """The anchor is a MARK, not prose: the card already says which division
    it is, so `§1 Shipped 260724.` reads as `Shipped 260724.` once placed."""
    m = re.match(r"^((?:[^\w\s§]|\s)*(?:[ACP]\d+(?:\.\d+)?\s*·?\s*)?)"
                 r"§\d+\s*", text)
    if m:
        text = text[:m.end(1)] + text[m.end():]
    return _TRAIL_ANCHORS.sub("", text).rstrip()


def _anchors(line, trailing=False):
    """-> [int] the division numbers this line ANCHORS to.

    `trailing=True` reads a Files row, whose anchors sit at the end; otherwise
    one leading anchor is read from an Aim or State row. Prose mentions of a
    section, cross-page references, and sub-division references all sit in
    neither position and are stepped over."""
    if trailing:
        m = _TRAIL_ANCHORS.search(line)
        return [int(x) for x in re.findall(r"\d+", m.group(1))] if m else []
    head = line[_LEAD_STRIP.match(line).end():]
    m = _ANCHOR_RE.match(head)
    if not m or _XREF_TAIL.search(line[:len(line) - len(head)]):
        return []
    return [int(m.group(1))]
_CHECK_RE = re.compile(r"^-\s+\[( |x|X)\]\s*(.*)$")


def _sections(text):
    """-> {canonical section name: [lines]} for the sections outline reads."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*?)\s*$", line)
        if m:
            # A plan's trailing section is written `## Aims · what must become
            # true, and how you would know` (workbench-task-draft §📐), so
            # the name is the part before the first ` · `; keying on the whole
            # line found no Aims in any plan (JL 260830, SM08).
            head = m.group(1).strip().split(" · ", 1)[0].strip().lower()
            cur = _SEC_ALIAS.get(head)
            if cur:
                out.setdefault(cur, [])
            continue
        if cur:
            out[cur].append(line)
    return out


def parse_outline(text):
    """The one parse both lenses and the check read from.

    -> {divs: [{n, title}], aims: [...], states: [...], files: [...],
        bad: [str], loose: int}
    An aim: {text, div (int|None), done (bool|None), id}. A state:
    {text, div, emoji}. A file: {text, divs}. div None = 🌐 page-wide.
    """
    secs = _sections(text)
    divs, seen, body = [], {}, {}
    cur = None
    for line in secs.get("content", []):
        m = _DIV_RE.match(line)
        if m:
            n, dotted = int(m.group(1)), m.group(2)
            title = (m.group(3) or m.group(4) or "").strip()
            if n not in seen:
                seen[n] = {"n": n, "title": "" if dotted else title}
                divs.append(seen[n])
                body[n] = []
            elif not dotted and not seen[n]["title"]:
                seen[n]["title"] = title   # an undotted heading names it later
            cur = n
            continue
        if cur is not None:
            body[cur].append(line)
    for d in divs:
        d["brief"] = _brief(body.get(d["n"], []))
    known = {d["n"] for d in divs}

    # WHAT IS THIS PAGE FOR. The outline used to open straight into division 1,
    # so a reader arriving cold met a list of aims with nothing to hang them on
    # (JL 260816: "我读完之后 no idea，不知道在干嘛"). The page already answers
    # it in its own first line: the Opening's lead question.
    lead = next((l.strip() for l in secs.get("opening", []) if l.strip()), "")
    bad = []

    def _pin(line, group_div):
        """One line -> its division, by id ①, anchor ②, then group ①."""
        m = _ID_RE.search(line)
        if m:
            # `A3.1` names its division; `P1` says page-wide and means it.
            return int(m.group(1)) if m.group(1) else None
        ns = _anchors(line)
        if ns:
            if ns[0] not in known:
                bad.append("§%d: no such division" % ns[0])
                return None
            return ns[0]
        return group_div

    aims, group_div = [], None
    for line in secs.get("aims", []):
        g = _GROUP_RE.match(line)
        if g:
            group_div = int(g.group(2)) if g.group(2) else None
            continue
        if not line.startswith("- "):
            continue
        m = _ID_RE.search(line)
        c = _CHECK_RE.match(line.strip())
        aims.append({"text": _strip_anchors(
                         (c.group(2) if c else line[2:]).strip()),
                     "done": (c.group(1).lower() == "x") if c else None,
                     "div": _pin(line, group_div),
                     "id": m.group(0) if m else None})

    states, decisions, group_div, decision = [], [], None, False
    for line in secs.get("states", []):
        g = _GROUP_RE.match(line)
        if g:
            decision = g.group(1) == "Decision Now"
            group_div = int(g.group(2)) if g.group(2) else None
            continue
        if decision:
            # A Decision Now row is an ask a person still owes, not a fact
            # about an aim, so it is neither a state nor dropped: the card
            # says the page is waiting on someone.
            c = _CHECK_RE.match(line.strip())
            if c:
                decisions.append({"text": _strip_id(c.group(2).strip()),
                                  "answered": c.group(1).lower() == "x"})
            continue
        if not line.strip() or line.startswith((" ", "\t", ">")):
            continue
        body = line[2:].strip() if line.startswith("- ") else line.strip()
        emoji = next((e for e in STATE_EMOJI if body.startswith(e)), None)
        states.append({"text": _strip_anchors(body), "emoji": emoji,
                       "div": _pin(line, group_div)})

    # the canonical mirror: an id-carrying aim with no checkbox takes its
    # done-ness from its ✅ state row, so A-grammar pages need no [x]
    done_ids = {m.group(0) for s in states if s["emoji"] in DONE
                for m in [_ID_RE.search(s["text"])] if m}
    for a in aims:
        if a["done"] is None and a["id"]:
            a["done"] = a["id"] in done_ids

    # A Files ENTRY is the `- ` row plus the indented description under it, so
    # the anchors may trail either line: the row is usually a bare path and the
    # sentence saying what the file is for is the natural place to mark it.
    files, entry = [], None

    def _close(e):
        if not e:
            return
        for n in e["divs"]:
            if n not in known:
                bad.append("§%d: no such division" % n)
        e["divs"] = [n for n in e["divs"] if n in known]
        files.append(e)

    for line in secs.get("files", []):
        if line.startswith("- "):
            _close(entry)
            entry = {"text": _strip_anchors(line[2:].strip()),
                     "divs": _anchors(line, trailing=True)}
        elif entry is not None and line.startswith((" ", "\t")):
            entry["divs"] += _anchors(line, trailing=True)
        elif not line.strip():
            continue
        else:
            _close(entry)
            entry = None
    _close(entry)

    # THE SAFETY NET, and the one invariant this surface must never break: every
    # aim and every state appears on exactly one card. An `### A6` group on a
    # page whose Content declares no division 6 would otherwise point at a card
    # that is never drawn, and the aim would vanish from BOTH lenses. So a
    # division named by the material but missing from Content gets its own card,
    # marked as undeclared rather than silently dropped.
    for n in sorted({r["div"] for r in aims + states if r["div"] is not None}
                    - known):
        divs.append({"n": n, "title": "", "undeclared": True})
    divs.sort(key=lambda d: d["n"])

    loose = sum(1 for a in aims if a["div"] is None) + \
        sum(1 for s in states if s["div"] is None)
    return {"divs": divs, "aims": aims, "states": states, "files": files,
            "decisions": decisions, "lead": lead, "bad": bad, "loose": loose}
