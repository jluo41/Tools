"""🧭 Outline · the page re-read per division, live and storage-less (QPf12).

WHAT THIS ANSWERS (JL 260816): a page groups its material by section kind —
all Content, then all Aims, then all States — so nothing shows one division
with ITS aims, ITS ticks, and ITS state receipts together. This surface flips
the axis: one card per Content division, everything that belongs to it inside.

RULE-BASED, NEVER AUTHORED (JL 260816: "我不想每一次都靠一个 code 去做这件事"):
the aim-to-division tie is read from the material, two grammars deep —
  ① the template's own A-grammar: an Aims/States group `### A<n>` and an id
    `A<n>.<m>` both carry the division number already; nothing to add.
  ② the §N anchor (QPf12 §1): a loose checkbox aim, a state line, or a Files
    row may carry `§N` pointing at Content's `### N ·` division. Files rows
    may carry several. An unanchored line is legal and means 🌐 page-wide.
No claude call at render time. A bad anchor renders as a named ❌, and the
🌐 card doubles as the worklist for anchoring the page.

LIVE AND STORAGE-LESS, the QPf1 folderstat precedent: rendered from the .md
on every open, written nowhere, so it can never be stale. The POST twin
exists only so the shell's `tab: {url, write}` contract holds.

TWO LENSES, one parse (QPf12 §2): 🧭 By division and 🚦 By progress are the
same data sorted twice, both rendered server-side, toggled client-side by
chips with no second request. The 🚦 lens lists ⬜ before ✅ on purpose:
opening it is asking what the page still owes.
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

# Aim state emoji (haipipe-page): current set + the older ones still parsed.
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
_DIV_RE = re.compile(r"^###\s+§?(\d+)(\.\d+)*(?:\s*·\s*(.*))?\s*$")
# An Aims/States group. The leading `(?:[^\w\s]|\s)*` is not decoration: pages
# write `### 🗣 Decision Now` with the emoji BEFORE the name, and without this
# the decision block goes unrecognized and its pending asks leak into States as
# if they were current facts about an aim.
_GROUP_RE = re.compile(r"^###\s+(?:[^\w\s]|\s)*([AC](\d+)|P|Decision Now)\b")
# An Aim id is `A3.1` (division 3) or `P1` (page-wide, no division).
_ID_RE = re.compile(r"\b(?:[AC](\d+)\.\d+|P\d+)\b")
# `§` was already in use on a board before this plugin, with two OTHER meanings,
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

_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#fbfbf9;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4df;--card:#fff;
 --warn:#b3541e;--ok:#3a7d44;--acc:#3e5c84}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;
 --mut:#9a9a97;--line:#2c2e33;--card:#1d1f23;--warn:#e0955a;--ok:#7dbb87;
 --acc:#7d9cc4}}}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--fg);
 font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:15px;margin:0 0 2px}} .mut{{color:var(--mut);font-size:12px}}
.chips{{display:flex;gap:6px;margin:10px 0}}
.chip{{font:600 12px -apple-system,sans-serif;border:1px solid var(--line);
 border-radius:999px;padding:4px 12px;cursor:pointer;background:var(--card);
 color:var(--fg)}}
.chip.on{{border-color:var(--acc);color:var(--acc)}}
.ok{{color:var(--ok);font-weight:600}} .warn{{color:var(--warn);font-weight:600}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;
 padding:10px 14px;margin:0 0 10px}}
.card h2{{font-size:13px;margin:0 0 4px;display:flex;gap:8px;
 align-items:baseline}}
.card h2 .tally{{margin-left:auto;flex:none;font:600 11px ui-monospace,
 Menlo,monospace;color:var(--mut)}}
.card h2 .tally.all{{color:var(--ok)}}
.lead{{font-size:13px;margin:6px 0 0;color:var(--fg)}}
.tally{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;
 margin:10px 0 6px;font-size:12px}}
.tally b{{font-weight:600}}
.bar{{display:inline-block;width:84px;height:7px;border-radius:4px;
 background:var(--line);overflow:hidden}}
.bar i{{display:block;height:100%;background:var(--ok)}}
.left{{color:var(--fg)}} .wait{{color:var(--warn);font-weight:600}}
details{{margin:4px 0 0}}
summary{{cursor:pointer;font:600 11px -apple-system,sans-serif;
 color:var(--mut);text-transform:uppercase;letter-spacing:.03em;
 padding:3px 0;list-style:none}}
summary::-webkit-details-marker{{display:none}}
summary:before{{content:"▸ ";color:var(--mut)}}
details[open]>summary:before{{content:"▾ "}}
summary:hover{{color:var(--acc)}}
.brief{{color:var(--mut);font-size:12px;margin:0 0 8px;
 padding-bottom:8px;border-bottom:1px solid var(--line)}}
.sub{{font:600 11px -apple-system,sans-serif;color:var(--mut);
 text-transform:uppercase;margin:8px 0 2px}}
.row{{display:flex;gap:8px;padding:3px 0 1px;font-size:13px;
 align-items:baseline}}
.row .t{{flex:none}} .row .x{{flex:1;min-width:0}}
.idtag{{flex:none;font:500 11px ui-monospace,Menlo,monospace;color:var(--mut)}}
.now{{display:inline-block;font:600 10px -apple-system,sans-serif;
 text-transform:uppercase;letter-spacing:.04em;color:var(--acc);
 margin-right:6px;vertical-align:1px}}
.row .badge{{flex:none;font:500 11px ui-monospace,Menlo,monospace;
 color:var(--acc);border:1px solid var(--line);border-radius:6px;
 padding:0 6px;cursor:pointer;text-decoration:none}}
.st{{color:var(--mut);font-size:12px;margin:0 0 4px 2px;padding-left:10px;
 border-left:2px solid var(--line)}}
.err{{color:var(--warn);font-size:12px}}
.lens{{display:none}} .lens.show{{display:block}}
code{{font:12px ui-monospace,Menlo,monospace}}
</style></head><body>
<h1>🧭 {title}</h1>
{lead}
<div class=tally>{tally}</div>
<div class="mut">always up to date · read from the page each time · {chip}</div>
<div class=chips>
 <button class="chip on" data-lens=div>🧭 By part</button>
 <button class=chip data-lens=prog>🚦 What is left</button>
</div>
<div class="lens show" id=lens-div>{by_div}</div>
<div class=lens id=lens-prog>{by_prog}</div>
<script>
document.querySelectorAll('.chip').forEach(function(c){{
  c.addEventListener('click',function(){{
    document.querySelectorAll('.chip').forEach(function(x){{
      x.classList.remove('on');}});
    document.querySelectorAll('.lens').forEach(function(x){{
      x.classList.remove('show');}});
    c.classList.add('on');
    document.getElementById('lens-'+c.dataset.lens).classList.add('show');
  }});
}});
document.querySelectorAll('a.badge').forEach(function(a){{
  a.addEventListener('click',function(ev){{
    ev.preventDefault();
    document.querySelector('.chip[data-lens=div]').click();
    var el=document.getElementById(a.getAttribute('href').slice(1));
    if(el)el.scrollIntoView({{behavior:'smooth'}});
  }});
}});
</script>
</body></html>"""


def _sections(text):
    """-> {canonical section name: [lines]} for the sections outline reads."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*?)\s*$", line)
        if m:
            cur = _SEC_ALIAS.get(m.group(1).strip().lower())
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
            title = (m.group(3) or "").strip()
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


def _e(s):
    return html.escape(s)


def _aim_row(a, badge=False, receipt=None):
    """One aim, with its matching State row folded in UNDER it as the receipt.

    TWO SENTENCES, TWO JOBS, and the card has to show that (JL 260816: "I
    cannot understand what is happening"). An Aim is what should become true;
    a State is what IS true. Printed as two look-alike lines both opening
    `A1.1 ·` and both ticked, they read as one sentence said twice. So the id
    prints ONCE as a dim tag, the goal keeps the plain voice, and the status
    goes under it behind a `now` label, in the State's own emoji."""
    b = ('<a class=badge href="#div-%s">div %s</a>'
         % (a["div"], a["div"])) if badge and a["div"] else (
        '<a class=badge href="#div-P">whole page</a>' if badge else "")
    tag = '<span class=idtag>%s</span>' % _e(a["id"]) if a["id"] else ""
    row = ('<div class=row><span class=x>%s</span>%s%s</div>'
           % (_e(_strip_id(a["text"])), tag, b))
    if receipt:
        row += ('<div class=st><span class=now>now</span>%s</div>'
                % _e(_strip_id(receipt)))
    return row


def _card(anchor, title, aims, states, files, brief=None):
    """One division.

    WHAT IS LEFT stays open, WHAT IS FINISHED folds away. A card that prints
    six finished aims in full makes the reader work through work that is over
    before reaching the one thing still to do, and on a page where most aims
    are met that is nearly the whole card (JL 260816: "非常非常难去读懂"). So
    done aims collapse behind a count that can be clicked, and the open ones,
    the only ones anybody can act on, are always in plain sight."""
    # An id-carrying State is that Aim's receipt; the rest stand alone.
    byid, loose = {}, []
    for s in states:
        m = _ID_RE.search(s["text"])
        if m and m.group(0) not in byid:
            byid[m.group(0)] = s["text"]
        else:
            loose.append(s["text"])
    done = [a for a in aims if a["done"]]
    todo = [a for a in aims if not a["done"]]

    count = ""
    if aims:
        count = ('<span class="tally %s">%d/%d</span>'
                 % ("all" if not todo else "part", len(done), len(aims)))
    parts = ['<div class=card id="div-%s"><h2>%s%s</h2>'
             % (anchor, title, count)]
    if brief:
        parts.append('<div class=brief>%s</div>' % _e(brief))

    if todo:
        parts.append('<div class=sub>⬜ still to do</div>')
        parts += [_aim_row(a, receipt=byid.get(a["id"])) for a in todo]
    if done:
        parts.append(
            '<details><summary>✅ %d done</summary>%s</details>'
            % (len(done),
               "".join(_aim_row(a, receipt=byid.get(a["id"]))
                       for a in done)))
    if loose or files:
        extra = "".join(
            ['<div class=sub>📍 notes</div>'] +
            ['<div class=st>%s</div>' % _e(t) for t in loose] +
            (['<div class=sub>📎 files</div>'] if files else []) +
            ['<div class=st>%s</div>' % _e(f["text"]) for f in files])
        parts.append('<details><summary>📍 more</summary>%s</details>' % extra)
    if not (aims or states or files):
        parts.append('<div class=mut>nothing lands here yet</div>')
    parts.append("</div>")
    return "".join(parts)


def _tally(o):
    """The whole page in one line of numbers, before any sentence.

    A reader who cannot hold six paragraphs at once still needs to know where
    the page stands, and counting ticks by eye is exactly the work this is
    supposed to save."""
    done = sum(1 for a in o["aims"] if a["done"])
    todo = len(o["aims"]) - done
    waiting = sum(1 for d in o.get("decisions", []) if not d["answered"])
    bits = []
    if o["aims"]:
        pct = int(100 * done / len(o["aims"]))
        bits.append('<span class=bar><i style="width:%d%%"></i></span>' % pct)
        bits.append('<b>%d of %d done</b>' % (done, len(o["aims"])))
    if todo:
        bits.append('<span class=left>⬜ %d to do</span>' % todo)
    if waiting:
        bits.append('<span class=wait>🗣 %d waiting on you</span>' % waiting)
    if not bits:
        bits.append('<span class=mut>this page lists no aims yet</span>')
    return " ".join(bits)


def render(title, o):
    """-> the full html page: both lenses rendered, chips toggle."""
    # Say it in words a tired reader can take in the first time (JL 260816).
    # "3 loose lines" and "aligned" are this plugin's own shorthand, and a
    # reader meeting the tab for the first time has no reason to know either.
    if o["bad"]:
        chip = '<span class=warn>❌ %s</span>' % " · ".join(
            _e(b.replace(": no such division", " points at a part that "
                         "does not exist")) for b in sorted(set(o["bad"])))
    elif o["loose"]:
        chip = ('<span class=warn>⚠️ %d line%s not placed in any part</span>'
                % (o["loose"], "s"[:o["loose"] != 1]))
    else:
        chip = '<span class=ok>✅ every line is placed</span>'

    # The pending asks used to get a card of their own here, above everything.
    # It was cut (JL 260816: "我们大概不需要吧"): the header line already says
    # `🗣 1 waiting on you`, so the card repeated a number the reader had just
    # read and spent four lines explaining what "waiting" means.
    cards = []
    for d in o["divs"]:
        n = d["n"]
        name = _e(d["title"]) if d["title"] else (
            '<span class=mut>not declared in Content</span>'
            if d.get("undeclared") else '<span class=mut>&mdash;</span>')
        cards.append(_card(
            n, "%d · %s" % (n, name),
            [a for a in o["aims"] if a["div"] == n],
            [s for s in o["states"] if s["div"] == n],
            [f for f in o["files"] if n in f["divs"]],
            brief=d.get("brief")))
    cards.append(_card(
        "P", "🌐 the whole page",
        [a for a in o["aims"] if a["div"] is None],
        [s for s in o["states"] if s["div"] is None],
        [f for f in o["files"] if not f["divs"]]))
    by_div = "".join(cards) if o["divs"] else (
        cards[-1] + '<div class=mut>no numbered Content divisions found; '
        'everything is 🌐 until the page grows `### N ·` parts</div>')

    todo = [a for a in o["aims"] if not a["done"]]
    done = [a for a in o["aims"] if a["done"]]
    prog = ['<div class=card><h2>⬜ still to do · %d</h2>' % len(todo)]
    prog += [_aim_row(a, badge=True) for a in todo] or [
        '<div class=mut>nothing left to do</div>']
    prog.append('</div><div class=card><h2>✅ already done · %d</h2>' % len(done))
    prog += [_aim_row(a, badge=True) for a in done] or [
        '<div class=mut>nothing done yet</div>']
    prog.append("</div>")

    lead = ('<div class=lead>%s</div>' % _e(o.get("lead", ""))
            if o.get("lead") else "")
    return _PAGE.format(title=_e(title), lead=lead, tally=_tally(o),
                        chip=chip, by_div=by_div, by_prog="".join(prog))


class OutlineMixin:

    # ---- GET/HEAD /_board/outline?path=…&file=… ------------------------
    def outline_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        p = {"path": (q.get("path") or [""])[0],
             "file": (q.get("file") or [""])[0]}
        got = self.target(p)
        if got[0] is None:
            body = ("<h1>🧭 outline</h1><p>%s</p>" % html.escape(got[1])
                    ).encode()
            return self._outline_send(body, 404, head_only)
        f, board = got
        page_src = Path(board) / f
        o = parse_outline(page_src.read_text(encoding="utf-8"))
        page = render(page_src.stem, o)
        return self._outline_send(page.encode("utf-8"), 200, head_only)

    def _outline_send(self, body, code, head_only):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    # ---- POST /_board/outline — the shell's write() twin ---------------
    def plug_outline(self, p):
        """{path, file} -> {ok, url}. Nothing is written: the GET renders
        live. This exists so the tab spec's write() has something to call."""
        got = self.target(p)
        if got[0] is None:
            return None, got[1]
        url = ("/_board/outline?path=%s&file=%s"
               % (quote(p.get("path") or ""), quote(p.get("file") or "")))
        return {"url": url}, None
