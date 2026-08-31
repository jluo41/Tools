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
import pathlib
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
 font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:17px;margin:0 0 2px}} .mut{{color:var(--mut);font-size:13px}}
.chips{{display:flex;gap:6px;margin:10px 0}}
.chip{{font:600 12px -apple-system,sans-serif;border:1px solid var(--line);
 border-radius:999px;padding:4px 12px;cursor:pointer;background:var(--card);
 color:var(--fg)}}
.chip.on{{border-color:var(--acc);color:var(--acc)}}
.ok{{color:var(--ok);font-weight:600}} .warn{{color:var(--warn);font-weight:600}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;
 padding:10px 14px;margin:0 0 10px}}
.card h2{{font-size:15px;margin:0 0 4px;display:flex;gap:8px;
 align-items:baseline}}
.card h2 .tally{{margin-left:auto;flex:none;font:600 11px ui-monospace,
 Menlo,monospace;color:var(--mut)}}
.card h2 .tally.all{{color:var(--ok)}}
.lead{{font-size:14.5px;margin:6px 0 0;color:var(--fg)}}
.tally{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;
 margin:10px 0 6px;font-size:12px}}
.tally b{{font-weight:600}}
.bar{{display:inline-block;width:84px;height:7px;border-radius:4px;
 background:var(--line);overflow:hidden}}
.bar i{{display:block;height:100%;background:var(--ok)}}
.left{{color:var(--fg)}} .wait{{color:var(--warn);font-weight:600}}
details{{margin:4px 0 0}}
summary{{cursor:pointer;font:600 12px -apple-system,sans-serif;
 color:var(--mut);text-transform:uppercase;letter-spacing:.03em;
 padding:3px 0;list-style:none}}
summary::-webkit-details-marker{{display:none}}
summary:before{{content:"▸ ";color:var(--mut)}}
details[open]>summary:before{{content:"▾ "}}
summary:hover{{color:var(--acc)}}
.brief{{color:var(--mut);font-size:13.5px;margin:0 0 8px;
 padding-bottom:8px;border-bottom:1px solid var(--line)}}
.sub{{font:600 12.5px -apple-system,sans-serif;color:var(--mut);
 text-transform:uppercase;margin:8px 0 2px}}
.row{{display:flex;gap:8px;padding:2px 0;font-size:14px;line-height:1.55;
 align-items:baseline}}
.row .t{{flex:none}} .row .x{{flex:1;min-width:0}}
.idtag{{flex:none;font:500 12px ui-monospace,Menlo,monospace;color:var(--mut)}}
/* A TAG, not a pill. As a rounded 14px pill on its own flex column it wrapped
   its own label onto two lines and pushed the sentence into half the pane
   (JL 260817, screenshot). Small, nowrap, inline at the end of the sentence. */
.evchip,.evtag{{display:inline;white-space:nowrap;
 font:12px/1.45 ui-monospace,Menlo,monospace;
 border:1px solid color-mix(in srgb,currentColor 26%,transparent);
 background:color-mix(in srgb,currentColor 8%,transparent);
 border-radius:4px;padding:0 4px;color:inherit;vertical-align:1px}}
.evchip{{cursor:pointer}}
.evtag{{border-style:dashed}}
/* A bullet with hidden detail is a details element: the row shows only the
   terse head + chips, and clicking unfolds the Answered:/Drawn: text (JL 260819:
   "点击之后能看到这个 bullet point 稍微详细一点、但又非常 concise 的解释…
   像 figure 之类的，其实完全可以放到 hidden text 里面"). Native, script-free,
   like the popovers. */
/* HARD RESET: the board shell injects this card into a page that styles its
   own drawers' summary/row classes (big, bold, accent-coloured — JL 260819
   screenshot: one folded bullet rendered like a section heading). Restate
   every typography and layout property so no host rule survives cascade. */
details.brow{{margin:0;padding:0;border:0;background:none}}
details.brow>summary{{list-style:none!important;cursor:pointer;display:flex;
 gap:8px;padding:2px 0;margin:0;border:0;background:none;font-size:14px;
 line-height:1.55;align-items:baseline;font-weight:400;color:var(--fg);
 text-transform:none;letter-spacing:normal;font-family:inherit}}
details.brow>summary .x{{flex:1;min-width:0;font-size:14px;font-weight:400;
 color:var(--fg);text-transform:none;letter-spacing:normal}}
details.brow>summary .addr{{font:500 11.5px ui-monospace,Menlo,monospace;
 color:var(--mut);flex:none;min-width:76px;text-align:left;
 text-transform:none}}
/* the paragraph row is a LEVEL, not another bullet (JL 260819: "hard to
   distinguish with the bullet point"): a thin rule above and a heavier,
   slightly spaced label make the structure visible at a skim. */
/* JL picked the ACCENT BAR (260819, from four previews): a short colored
   bar juts into the left gutter beside the paragraph label, dark text,
   and the bullets stay flush — the bar alone carries the hierarchy. */
.prow{{margin-top:10px;position:relative;margin-left:-9px;
 padding-left:9px}}
/* a short tick, not a full-height bar (JL 260819: "this one is too long"):
   0.85em tall, vertically centered on the label line. */
.prow::before{{content:"";position:absolute;left:0;top:50%;
 transform:translateY(-50%);width:3px;height:.85em;
 background:var(--acc);border-radius:2px}}
.prow .mut{{font-weight:650;font-size:13.5px;color:var(--fg);
 letter-spacing:.01em}}
/* the host shell draws its drawer triangle with ::before, which ::marker
   rules never touch — kill every pseudo that could carry a glyph */
details.brow>summary::before{{content:none!important;display:none!important}}
details.brow>summary::after{{content:none!important}}
details.brow>summary::-webkit-details-marker{{display:none!important}}
details.brow>summary::marker{{content:""!important;display:none!important}}
details.brow>summary:hover{{background:color-mix(in srgb,var(--fg) 5%,transparent)}}
.bdetail{{margin:1px 0 7px 3.6em;color:var(--mut);font-size:13px;
 line-height:1.5;max-width:62em}}
.evchip:hover,.evchip:focus-visible{{background:color-mix(in srgb,currentColor 18%,transparent);
 border-color:color-mix(in srgb,currentColor 45%,transparent)}}
.chipcard{{margin:auto;max-width:min(44em,calc(100vw - 2rem));padding:8px 11px;
 max-height:min(46vh,20em);overflow:auto;border:1px solid var(--line);
 border-left-width:3px;border-radius:8px;background:var(--card);color:var(--fg);
 font:14px/1.6 -apple-system,BlinkMacSystemFont,sans-serif;
 box-shadow:0 6px 20px rgba(0,0,0,.18)}}
@supports selector(:popover-open){{.chipcard:not(:popover-open){{display:none}}}}
.chipcard::backdrop{{background:rgba(0,0,0,.12)}}
.chipcard.ok{{border-left-color:var(--ok)}}
.chipcard.warn{{border-left-color:var(--warn)}}
.chipcard.mut{{border-left-color:var(--mut)}}
.cch{{display:flex;gap:7px;align-items:baseline;flex-wrap:wrap;
 padding-bottom:4px;margin-bottom:5px;border-bottom:1px solid var(--line)}}
.cch b{{font:600 12px ui-monospace,Menlo,monospace;word-break:break-all}}
.cck{{font:10px ui-monospace,Menlo,monospace;color:var(--mut);
 letter-spacing:.04em;text-transform:uppercase}}
.ccb p{{margin:0}}
/* THE FIGURE, in the panel the chip opens. A display unit whose mark opens a
   panel holding only its claim sends the reader out of the tab to see the one
   thing the mark is about (JL 260818). Bounded so the plan stays skimmable:
   the panel is evidence, never the page. */
.evfig{{display:block;width:100%;max-height:32vh;margin:0 0 7px;
 border:1px solid var(--line);border-radius:5px;background:#fff;
 object-fit:contain}}
object.evfig{{height:32vh}}
@supports (position-area:block-end){{
 .chipcard{{position:fixed;inset:auto;margin:0;
  position-area:block-end span-inline-end;
  position-try-fallbacks:flip-block,flip-inline}}}}
.ev>summary::-webkit-details-marker{{display:none}}
.ev>summary:hover{{text-decoration:underline dotted}}
.evbody{{margin:3px 0 5px 62px;padding:7px 10px;border-left:2px solid var(--line);color:var(--fg);font-size:13.5px;background:var(--card)}}
.sep{{opacity:.45;padding:0 2px}}
.addr{{font:500 11.5px ui-monospace,Menlo,monospace;color:var(--mut);flex:none;min-width:76px;text-align:left}} /* 76px fits C14.P2.B4; one shared column, so paragraph and bullet titles start at the same x (JL 260819: aligned) */
/* The SECTION address is LEFT aligned, and the bullet addresses stay right.
   A right-aligned gutter ends `C3` and `P1.B1` at the same x, so the two
   character section id sits FURTHER RIGHT than the five character bullet id
   beneath it and the hierarchy reads backwards (JL 260818, screenshot). */
.addr.sec{{text-align:left;min-width:0;margin-right:8px}}
.bundles{{margin:7px 0 8px;padding:5px 8px;border:1px solid var(--line);
 border-radius:7px;background:color-mix(in srgb,var(--acc) 3%,var(--card))}}
.bundles>summary{{font-size:10px}}
.bundle-row{{display:flex;gap:7px;align-items:baseline;padding:2px 0;
 font-size:11px;line-height:1.35;border-top:1px solid var(--line)}}
.bundle-row:first-of-type{{border-top:0}}
.bundle-kind{{flex:none;font:500 10px ui-monospace,Menlo,monospace;
 color:var(--mut);text-transform:uppercase}}
.bundle-items{{flex:1;min-width:0;color:var(--fg);overflow-wrap:anywhere}}
.bundle-state{{flex:none;font:500 10px ui-monospace,Menlo,monospace}}
.now{{display:inline-block;font:600 10px -apple-system,sans-serif;
 text-transform:uppercase;letter-spacing:.04em;color:var(--acc);
 margin-right:6px;vertical-align:1px}}
.row .badge{{flex:none;font:500 11px ui-monospace,Menlo,monospace;
 color:var(--acc);border:1px solid var(--line);border-radius:6px;
 padding:0 6px;cursor:pointer;text-decoration:none}}
.st{{color:var(--mut);font-size:12px;margin:0 0 4px 2px;padding-left:10px;
 border-left:2px solid var(--line)}}
.err{{color:var(--warn);font-size:12px}}
/* the sibling-file records, one shape for every kind (0.18.0) */
.rmeta{{margin:0 0 6px;font:11.5px ui-monospace,Menlo,monospace}}
.rec{{padding:8px 0 6px;border-top:1px solid var(--line)}}
.rec:first-of-type{{border-top:0;padding-top:2px}}
.rh{{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}}
.rid{{flex:none;font:600 11px ui-monospace,Menlo,monospace;color:var(--acc);
 border:1px solid var(--line);border-radius:6px;padding:0 6px;white-space:nowrap}}
.rt{{flex:1;min-width:12em;font-size:14.5px;font-weight:600;line-height:1.4}}
.pill{{flex:none;font:600 10.5px -apple-system,sans-serif;text-transform:uppercase;
 letter-spacing:.04em;border-radius:999px;padding:1px 8px;border:1px solid currentColor;
 max-width:16em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.pill.ok{{color:var(--ok)}} .pill.warn{{color:var(--warn)}}
.pill.mut{{color:var(--mut)}} .pill.acc{{color:var(--acc)}}
.rrows{{margin-top:3px}}
.rr{{display:grid;grid-template-columns:5.4em 1fr;gap:6px;font-size:13.5px;
 line-height:1.5;padding:1px 0}}
.rr b{{font:600 11px -apple-system,sans-serif;color:var(--mut);text-transform:uppercase;
 letter-spacing:.04em;padding-top:3px}}
.rq{{margin:3px 0 0 5.8em;padding-left:9px;border-left:2px solid var(--line);
 color:var(--mut);font-size:12.5px;line-height:1.5}}
.rd{{margin:3px 0 0 5.8em}} .rd>summary{{font-size:11.5px;color:var(--mut);
 cursor:pointer;list-style:none}}
.rd>summary::-webkit-details-marker{{display:none}}
.rd>summary::before{{content:"▸ "}} .rd[open]>summary::before{{content:"▾ "}}
.rdb{{margin:3px 0 0;padding-left:9px;border-left:2px solid var(--line);color:var(--mut);
 font-size:13px;line-height:1.5;overflow-wrap:anywhere}}
.rec>.rdb{{margin-left:5.8em}}
.rgrp{{margin:12px 0 4px;font:600 12px -apple-system,sans-serif;color:var(--mut);
 text-transform:uppercase;letter-spacing:.05em}}
.rpre{{color:var(--mut);font-size:13px;margin:2px 0;line-height:1.5}}
.lens .card pre{{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}}
.lens{{display:none}} .lens.show{{display:block}}
code{{font:12px ui-monospace,Menlo,monospace}}
</style></head><body>
<h1>🧭 {title}</h1>
{lead}
<div class=tally>{tally}</div>
<div class="mut">always up to date · read from the page each time · {chip}</div>
<div class=chips>
 <button class="chip on" data-lens=div>🧭 By part</button>
 <button class=chip data-lens=prog>🚦 What is left</button>{extra_chips}
</div>
<div class="lens show" id=lens-div>{by_div}</div>
<div class=lens id=lens-prog>{by_prog}</div>{extra_lenses}
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
            # A plan's trailing section is written `## Aims · what must become
            # true, and how you would know` (haipipe-plugin-outline §📐), so
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
        # An empty cell is a STATUS, never a blank. "nothing lands here"
        # read as "this part is fine" when it actually means the page
        # carries no id that points here (JL 260817).
        parts.append('<div class=mut>no aim, state or file on this page names this part</div>')
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



# ---------------------------------------------------------------- the plan
# The OUTLINE phase's own file, `<page>/outline/<stem>-outline-v<N>.md`
# (haipipe-plugin-outline §🗂, JL 260817). It is AUTHORED, frozen once its
# `approved:` line is ticked, and progress is NEVER written back into it.
# So this card renders two things side by side: what the plan SAID, and what
# is on disk NOW. The gap between them is the whole point of the card.

# 🧮 = value since 260819 (JL; the glyph's proof meaning died that morning).
# 🔢 stays accepted as the pre-260819 legacy alias so old plans keep parsing.
# The ✅ "have it" mark was RETIRED 260819: it named nothing a machine could
# recheck, an unmarked bullet already means "plain point, nothing owed", and
# the glyph already works two other jobs (tick syntax, the CHECK phase). It
# confused JL three separate times, and a mark that needs explaining fails
# its only job. Zero plans carried it at retirement.
# 📮 probe and 🧮 value SEPARATED 260819 (JL: "I want to separate them"):
# 📮 = this point needs a QUESTION answered (the card, any answer shape);
# 🧮 = this point QUOTES one value, PP<NN>.v<n>, out of an answered card.
# 📮 doubles as phase ②'s glyph ON PURPOSE (same concept) and is END-ANCHORED
# in the hit scan, so prose ABOUT the phase can never grow a phantom chip
# (the ✅ lesson).
_MARK = {"🎯": "aim", "📚": "cite", "📮": "probe",
         "🧮": "value", "🔢": "value", "🖼": "display"}


def _latest_plan(page_src):
    """-> (Path, version) of the highest outline file, or (None, '')."""
    d = page_src.parent / "outline"
    if not d.is_dir():
        return None, ""
    best, bestkey = None, None
    for f in d.glob("*-outline-*.md"):
        tag = f.stem.split("-outline-")[-1]
        # v2 beats v1; v_0707 sorts by its own digits. A plain string sort
        # would put v10 before v2, so pull the digits out.
        digits = re.sub(r"\D", "", tag) or "0"
        key = (len(digits), digits, tag)
        if bestkey is None or key > bestkey:
            best, bestkey = f, key
    return best, (best.stem.split("-outline-")[-1] if best else "")


def _disk_state(page_src):
    """Read sibling plugin folders, including the bundle backlinks.

    The result is still a live projection: no status or bundle is written.
    ``serves`` belongs to Probe cards and ``display_serves`` belongs to Display
    units; keeping the maps separate prevents the two plugin state ladders from
    being mistaken for one another.
    """
    base = page_src.parent
    cards, units, serves, display_serves = {}, {}, {}, {}
    pd = base / "probe"
    if pd.is_dir():
        for d in sorted(pd.iterdir()):
            c = d / "card.md"
            if not c.is_file():
                continue
            t = c.read_text(errors="replace")
            st = (re.search(r"^state:\s*(\w+)", t, re.M) or [None, "?"])[1]
            # `proof/` is the name in haipipe-plugin-probe 0.4.0; `answer/`
            # was 0.3.0's and real cards on disk still use it. Read BOTH: a
            # renamed contract must not make an existing card read as empty.
            n = 0
            for name in ("proof", "answer"):
                dd = d / name
                if dd.is_dir():
                    n += len([f for f in dd.glob("*")
                              if f.is_file() and f.name != "manifest.yaml"])
            why_empty = bool(re.search(r"^why_empty:\s*\S+", t, re.M))
            sv = (re.search(r"^serves:\s*(.+)$", t, re.M) or [None, ""])[1]
            serves.setdefault(d.name.split("-")[0], []).extend(
                re.findall(r"C\d+\.P\d+\.B\d+", sv))
            q = (re.search(r"^question:\s*(.+)$", t, re.M) or [None, ""])[1]
            if not q:
                q = (re.search(r"^#\s*\S+\s*\n+(.+)$", t, re.M) or [None, ""])[1]
            # The `## Values` rows, keyed v1/v2/…, kept verbatim: the 🧮
            # chip's evidence card must show THE NUMBER and its proof
            # binding, not just the card's question (JL 260819: "why the
            # value '7' is not get the evidence card? is it the PP01.v1??").
            vals = {}
            vb = re.search(r"(?ms)^## Values\s*\n(.*?)(?=^## |\Z)", t)
            if vb:
                for row in re.finditer(r"(?m)^-\s*(v\d+)\s*·\s*(.+?)\s*$",
                                        vb.group(1)):
                    vals[row.group(1)] = row.group(2)
            cards[d.name.split("-")[0]] = (st, n, q.strip(), why_empty, vals)
    dd = base / "display"
    if dd.is_dir():
        for d in sorted(dd.iterdir()):
            m = re.search(r"-(Display\d+)-", d.name)
            if not d.is_dir() or not m:
                continue
            r = d / "README.md"
            txt = r.read_text(errors="replace") if r.is_file() else ""
            # ONE parser, shared with the checker. `src/page_evidence.py:60`
            # recorded this exact blind spot and named this file: both read
            # README rows, this one required a leading bullet, and every unit
            # writing a bare `claim: ...` came back with NO claim, NO kind and
            # NO acceptance. A tab and a checker disagreeing about what a ROW
            # is, is how a reader learns to trust neither.
            rows = {}
            for k, v in re.findall(
                    r"^\s*(?:[-*]\s*)?\*{0,2}([A-Za-z][\w -]{0,24}?)"
                    r"\*{0,2}\s*:\s*\*{0,2}\s*(.*?)\s*$", txt, re.M):
                rows.setdefault(k.strip().lower(), v.strip())
            acc = rows.get("accepted", "").startswith("✅")
            rendered = (d / "preview.pdf").is_file() and any(
                (d / "assets").glob("*")) if (d / "assets").is_dir() else False
            claim = re.sub(r"\s+", " ", rows.get("claim")
                           or rows.get("what it shows")
                           or rows.get("shows") or "")
            # A rendered PDF is not yet EVIDENCE. The current Display contract
            # also requires a frozen intake and an explicit renderer row; keep
            # those inputs in the live tuple so the bundle cannot call a bare
            # preview complete.
            intake_ready = (d / "intake").is_dir() and bool(
                rows.get("intake") or rows.get("evidence")
                or rows.get("source") or (d / "intake" / "inputs").is_dir())
            renderer = bool(rows.get("renderer"))
            # THE FIGURE ITSELF, not a description of it (JL 260818: "why
            # here the Displays are not embedded in the outline's content").
            # A 🖼 chip that opens a panel holding only the claim makes a
            # reader leave the tab to see the one thing the mark is about.
            # PNG first because a browser draws it inline with no plugin;
            # the PDF is the fallback and rides in an <object>.
            asset = None
            for cand in ("assets/figure.png", "assets/figure.svg",
                         "assets/figure.pdf", "preview.pdf"):
                if (d / cand).is_file():
                    asset = d / cand
                    break
            units[m.group(1)] = (rendered, acc, claim.strip(),
                                 intake_ready and renderer, renderer, asset)
            sv = (re.search(r"^serves:\s*(.+)$", txt, re.M) or [None, ""])[1]
            display_serves[m.group(1)] = re.findall(
                r"C\d+\.P\d+\.B\d+", sv
            )
    # The KEY alone says the citation resolves; the reader also wants to see
    # WHAT it is without leaving the tab (JL 260817: "我点它之后，它把这个内容
    # 就直接出现了"). So the entry's own fields come back with it.
    keys = {}
    bx = base / "bibex"
    if bx.is_dir():
        for f in bx.glob("*.bib"):
            for ent in re.split(r"\n(?=@)", f.read_text(errors="replace")):
                m = re.match(r"@\w+\{\s*([^,\s]+)", ent.strip())
                if not m:
                    continue
                def fld(name):
                    g = re.search(r"\b%s\s*=\s*[{\"]" % name, ent, re.I)
                    if not g:
                        return ""
                    i, depth, out = g.end(), 1, []
                    while i < len(ent) and depth:
                        ch = ent[i]
                        if ch == "{":
                            depth += 1
                        elif ch == "}":
                            depth -= 1
                            if not depth:
                                break
                        out.append(ch)
                        i += 1
                    # {CDC} protects capitalisation in BibTeX and is not
                    # part of the title. Stripping only the ENDS left a stray
                    # closing brace mid-string ("CDC} Guideline", 260817).
                    return re.sub(r"\s+", " ",
                                  re.sub(r"[{}]", "", "".join(out))).strip(' "')
                keys[m.group(1)] = {"title": fld("title"), "author": fld("author"),
                                    "year": fld("year"),
                                    "venue": fld("journal") or fld("booktitle") or fld("publisher"),
                                    "verified": bool(re.search(
                                        r"verified:\s*✅", ent, re.I))}
    return cards, units, keys, serves, display_serves


# THE PROBE STATE LADDER, and it is the plugin's, not this file's.
# `haipipe-plugin-probe` 0.7.0 retired the invented raised/working/bound ladder
# for haipipe-probe's own words. This file counted on `bound`, a word no card
# carries any more, so four cards on QC1-visitlbp read `⬜` and their bullets
# read `0 of 1 bound` while two of them were ANSWERED (found 260817 by asking
# whether the thing was ready to use). The old words stay readable because a
# renamed contract must not make an existing card read as empty.
LEGACY_STATE = {"raised": "planned", "working": "commissioned", "bound": "answered"}
# has the number LANDED? (a proof/ is expected with it)
LANDED = ("answered", "answered-local", "read")
# is a human DONE with it? the strip's one-line verdict
READ = ("read",)
STUCK = ("deferred", "failed", "concern")


def _pstate(st):
    """-> the protocol word, whatever vintage the card was written in."""
    st = (st or "").lower()
    return LEGACY_STATE.get(st, st)


def _short_authors(a):
    """`Dowell, Deborah and Haegerich, Tamara M. and Chou, Roger` -> `Dowell et al.`
    One surname is enough in a panel whose title bar already prints the key."""
    if not a:
        return ""
    people = [x.strip() for x in re.split(r"\s+and\s+", a) if x.strip()]
    first = people[0].split(",")[0].strip()
    return first if len(people) == 1 else first + " et al."


def _tex_dash(s):
    """BibTeX writes `---` for a dash. Printing the three hyphens raw is what
    the panel was doing. An EN dash, never an em dash (JL's standing rule)."""
    return re.sub(r"-{2,3}", "\u2013", s or "")


def _asset_url(units, ref, root):
    """-> a URL the browser can fetch for this unit's winning asset, or None.

    The tab is served from the SAME process that serves the tree, so a path
    made relative to `--root` is fetchable as-is. Outside the root there is no
    URL to give, and a broken <img> is worse than no image."""
    got = units.get(ref)
    asset = got[5] if got and len(got) > 5 else None
    if not asset or not root:
        return None
    try:
        return "/" + asset.resolve().relative_to(
            pathlib.Path(root).resolve()).as_posix()
    except ValueError:
        return None


def _aim_rows(page_text):
    """-> {aim id: (aim sentence, state emoji, state sentence)}.

    One id ties three places: the outline bullet says what a sentence will
    establish, `## Aims` says what must become true, `## States` says whether
    it has (haipipe-plugin-outline §📐). Only the first two were ever joined."""
    def _sec(name):
        m = re.search(r"(?m)^## %s\b[^\n]*$(.*?)(?=^## |\Z)" % name, page_text, re.S)
        return m.group(1) if m else ""
    want, got = {}, {}
    # Since haipipe-plugin-outline 0.16.0 the Aims live in the PLAN, and a plan
    # row is `- [ ] A1.1 · target` (a person's box) with its state on the
    # folded `**Now:** …` line, because `## States` is retired. Reading only
    # the bare `- A1.1 ·` form made a migrated page's 🧭 tab say "this page
    # lists no aims yet" while ten Aims sat in its plan (JL 260830, SM08).
    aims_txt = _sec("Aims")
    # The merged-States row is `- ⬜ A1.1 · …` (tick before the id, the set
    # src/common.py AIM_RE reads); without the tick group every 🎯 mark read
    # "not on the page yet" while the row sat on the page (MISQ-Board, 260831).
    for m in re.finditer(r"(?m)^-\s+(?:\[([ xX])\]\s+)?(?:(⬜|🔨|🧠|✅|❄️?|🟡|🟠|⏸️?)\s+)?(A\d+\.\d+|P\d+)\s*·\s*(.+?)\s*$",
                         aims_txt):
        box, tick, aid, sentence = m.group(1), m.group(2), m.group(3), m.group(4)
        want.setdefault(aid, sentence)
        tail = aims_txt[m.end():]
        nxt = re.search(r"(?m)^-\s+", tail)
        block = tail[:nxt.start()] if nxt else tail
        now = re.search(r"\*\*Now:\*\*\s*(.+)", block)
        if now:
            fact = now.group(1).strip()
            em = re.match(r"([⬜🔨🧠✅❄️🟡🟠⏸])\s*", fact)
            emoji = em.group(1) if em else (tick or ("✅" if (box or "").lower() == "x" else "⬜"))
            got.setdefault(aid, (emoji, fact[em.end():].strip() if em else fact))
        elif tick is not None:
            got.setdefault(aid, (tick, ""))
        elif box is not None:
            got.setdefault(aid, ("✅" if box.lower() == "x" else "⬜", ""))
    for m in re.finditer(r"(?m)^-\s+(\S+)\s+(A\d+\.\d+|P\d+)\s*·\s*(.+?)\s*$",
                         _sec("States")):
        got.setdefault(m.group(2), (m.group(1), m.group(3)))
    return {k: (want.get(k, ""), got.get(k, ("", ""))[0], got.get(k, ("", ""))[1])
            for k in set(want) | set(got)}


def _live(mark, ref, cards, units, keys=(), aims=None):
    """One bullet's LIVE half: what the folders say about what it owes."""
    if mark == "probe":
        if not ref:
            return "mut", "needs a probe · not raised yet", ""
        st, n, q, why_empty, _vals = cards.get(ref, (None, 0, "", False, {}))
        if st is None:
            return "warn", "🚨 no card", ""
        body, st = q, _pstate(st)
        if st in STUCK:
            return "warn", "🚨 " + st, body
        if st in LANDED and not n and not why_empty:
            # ANSWERED with an empty proof/ is the one shape that lies: the
            # card says the number came back and nothing on disk carries it.
            return "warn", "🚨 %s, proof/ empty" % st, body
        # "📮 PP01 answered 1" read as "the answer is 1" (JL 260819: "why
        # the answer is 1???") — the bare number was the proof/ FILE count.
        # Say what is counted, and prefer the count a reader wants: how
        # many values the card holds.
        nv = sum(1 for r in _vals.values() if "NOT HERE" not in r.upper())
        got = ("%d value%s" % (nv, "s" if nv != 1 else "")) if nv \
            else ("proof/ %d file%s" % (n, "s" if n != 1 else ""))
        # An answered ask's card SHOWS its values (JL 260819: "how could we
        # later convert this into the value evidence card?" — no conversion:
        # the card already holds them; quoting is 🧮's job, one id per use).
        if _vals:
            vrows = " · ".join(
                "%s.%s = %s (%s)" % (ref, k,
                                     (r.split("·")[1].strip() if "·" in r else r),
                                     r.split("·")[0].strip())
                for k, r in sorted(_vals.items()))
            body = "%s\n\nValues: %s" % (body, vrows)
        if st in READ:
            return "ok", "read · %s" % got, body
        if st in LANDED:
            return "ok", "%s · %s" % (st, got), body
        return "mut", st or "?", body
    if mark == "value":
        # 🧮 quotes ONE number: PP<NN>.v<n>. The card's lifecycle is 📮's
        # job; this chip answers only "is the quoted id real and landed".
        # checks/values.py owns re-computing the number itself.
        if not ref:
            return "mut", "owes its value id · PP<NN>.v<n>", ""
        card_id = ref.split(".")[0]
        st, n, q, why_empty, vals = cards.get(card_id,
                                              (None, 0, "", False, {}))
        if st is None:
            return "warn", "🚨 no card behind %s" % ref, ""
        body, st = q, _pstate(st)
        if "." not in ref:
            return "mut", "names the card, owes the .v id", body
        # The evidence behind a 🧮 chip is THE VALUES ROW — the number, its
        # meaning and its proof binding — with the card's question after it
        # for context. Showing only the question made the reader ask where
        # the 7 lives (JL 260819).
        row = vals.get(ref.split(".", 1)[1])
        if row is None:
            return ("warn", "🚨 %s names no row in %s's ## Values"
                    % (ref, card_id), body)
        parts = [p.strip() for p in row.split("·")]
        num = parts[1] if len(parts) > 1 else ""
        label = parts[0] if parts else row
        bind = " · ".join(parts[2:])
        body = "%s = %s · %s%s · state %s. The card asks: %s" % (
            ref, num or "?", label,
            (" · bound to " + bind) if bind else "", st, q)
        if num.upper() == "NOT HERE":
            return "warn", "🚨 allocated elsewhere · %s" % row, body
        if st in STUCK:
            return "warn", "🚨 " + st, body
        if st in READ or st in LANDED:
            return "ok", "= %s · %s" % (num, st), body
        return "mut", "%s · value not landed yet" % (st or "?"), body
    if mark == "display":
        if not ref:
            return "mut", "needs a figure · not built yet", ""
        got = units.get(ref)
        if got is None:
            return "warn", "🚨 no unit", ""
        rendered, acc, claim = got[:3]
        if not rendered:
            return "mut", "not rendered", claim
        return ("ok", "rendered ✓", claim) if acc \
            else ("mut", "rendered, unaccepted", claim)
    if mark == "cite":
        # A 📚 must name a REAL published work in this page's own bibex, not a
        # sibling board page. QB1/QB2/QB3 were board pages wearing the citation
        # mark, and the page's bibex held zero entries (JL 260817).
        if not ref:
            return "mut", "needs a bib key · not landed yet", ""
        if re.match(r"^QB?\d+$", ref):
            return "warn", "🚨 board page, not a citation", ""
        e = keys.get(ref)
        if not e:
            return "warn", "🚨 not in bibex/", ""
        # A CARD, not a bibliography entry. The full author list is what made
        # a 📚 card twice the height of a 🧮 one (JL 260817: "evidence card
        # 太大了"), and nobody reads six names in a popover: the citation KEY
        # already carries the first author, so the panel says "et al.".
        bits = [b for b in (_short_authors(e["author"]), e["year"]) if b]
        detail = _tex_dash(e["title"]) + ((" · " + " · ".join(bits)) if bits else "")
        if e["venue"]:
            detail += " · " + e["venue"]
        return "ok", "", detail

    if mark == "aim":
        # An empty cell is a STATUS, never a blank. A 🎯 bullet with no Aim id
        # is an intention nobody is tracking, and that must SHOW (JL 260817).
        # With an id the note stays EMPTY: the chip already prints the id, and
        # "→ %s" printed it a second time, so the chip read `🎯 A4.2 → A4.2`
        # (seen in the 260817 screenshot).
        #
        # 🎯 WAS THE ONE MARK THAT NEVER OPENED (JL 260818: "why the evidence
        # card here are not clickable?"). It returned an empty detail whether
        # the id resolved or not, so twenty tracked targets rendered as dead
        # grey tags. The material was on the page the whole time: the plugin's
        # own id grammar ties the bullet to `## Aims` and `## States` by that
        # id (§📐), and the panel is where the other three marks already show
        # the THING itself.
        if not ref:
            return "mut", "no Aim id", ""
        row = (aims or {}).get(ref)
        if row is None:
            # NOT an error. At OUTLINE time the plan names Aims that DRAFT has
            # not created yet, so an unresolved id is the normal forward case;
            # 🚨 here would fire on every well-formed new plan.
            return "mut", "not on the page yet", ""
        aim, emo, state = row
        detail = aim or "named in ## States, with no row in ## Aims"
        if state:
            detail += "  ·  " + (emo + " " if emo else "") + state
        return ("ok" if emo == "✅" else "mut"), "", detail

    return "mut", "", ""



def _count_landed(txt, cards, units, keys):
    """How many owed things EXIST. Not how many are finished."""
    n = 0
    for m in re.finditer(r"🧮[^\n]*?(?<![A-Za-z0-9-])(PP\d+)", txt):
        st = _pstate(cards.get(m.group(1), (None, 0, ""))[0])
        n += st in LANDED
    for m in re.finditer(r"🖼[^\n]*?(Display\d+)", txt):
        n += bool(units.get(m.group(1)))
    for m in re.finditer(r"📚[^\n]*?([A-Za-z][\w:-]*\d{4}[a-z]?)", txt):
        n += m.group(1) in keys
    return n


def _count_accepted(txt, cards, units):
    """How many carry a HUMAN yes: a display's `accepted: ✅` and, since the
    probe plugin's 0.7.0 ladder, a card's `state: read`. The two are the same
    act (a person looked at the thing itself and said yes), so counting only
    the display half under-reported every page that answers with numbers."""
    n = 0
    for m in re.finditer(r"🖼[^\n]*?(Display\d+)", txt):
        got = units.get(m.group(1))
        n += bool(got and got[1])
    for m in re.finditer(r"🧮[^\n]*?(?<![A-Za-z0-9-])(PP\d+)", txt):
        n += _pstate(cards.get(m.group(1), (None, 0, ""))[0]) in READ
    return n


def _bundle_state(kind, refs, address, by_bullet, display_by_bullet,
                  cards, units, keys, scaffolds=None):
    """Return the compact, derived status for one marked Outline Point.

    This deliberately returns data rather than HTML so the plan surface and a
    future API can share the same Evidence Bundle semantics. The bundle is
    keyed by the frozen Point address; plugin folders remain the authorities.
    """
    probes = sorted(set(by_bullet.get(address, [])))
    displays = sorted(set(display_by_bullet.get(address, [])))
    displays += [r for r in refs if r.startswith("Display") and r in units
                 and r not in displays]
    citations = [r for r in refs if r in keys]
    sentences = sorted(set((scaffolds or {}).get(address, [])))
    feedback = []
    for pid in probes:
        st = _pstate(cards.get(pid, ("", 0, ""))[0])
        if st in READ:
            feedback.append("%s: read" % pid)
        elif st in STUCK:
            feedback.append("%s: %s" % (pid, st))
    for did in displays:
        got = units.get(did, (False, False, "", False, ""))
        if got[1]:
            feedback.append("%s: accepted" % did)
    for cite in citations:
        feedback.append("%s: %s" % (
            cite, "verified" if keys.get(cite, {}).get("verified")
            else "unverified"))

    if kind in ("value", "probe"):
        landed = [p for p in probes
                  if _pstate(cards.get(p, ("", 0, "", False))[0]) in LANDED
                  and (cards.get(p, ("", 0, "", False))[1] > 0
                       or cards.get(p, ("", 0, "", False))[3])]
        status = "evidence-ready" if probes and len(landed) == len(probes) \
            else "needs-probe"
        return {"probes": probes, "displays": [], "citations": [],
                "sentences": sentences, "feedback": feedback, "status": status,
                "have": len(landed), "need": max(1, len(probes))}
    if kind == "display":
        rendered = [d for d in displays if units.get(d, (False, False, "", False, ""))[0]]
        intake = [d for d in displays if units.get(d, (False, False, "", False, ""))[3]]
        status = "evidence-ready" if displays and len(rendered) == len(displays) \
            and len(intake) == len(displays) \
            else "needs-intake"
        return {"probes": probes, "displays": displays, "citations": [],
                "sentences": sentences, "feedback": feedback,
                "status": status, "have": len(rendered),
                "need": max(1, len(displays))}
    if kind == "cite":
        status = "evidence-ready" if refs and len(citations) == len(refs) \
            else "needs-citation"
        return {"probes": probes, "displays": displays,
                "citations": citations, "sentences": sentences,
                "feedback": feedback, "status": status,
                "have": len(citations), "need": max(1, len(refs))}
    return {"probes": probes, "displays": displays,
            "citations": citations, "sentences": sentences,
            "feedback": feedback,
            "status": "evidence-ready",
            "have": 1, "need": 1}


def plan_card(page_src, root=None):
    """-> the html for the plan card, or '' when the page has no outline file."""
    f, ver = _latest_plan(page_src)
    if f is None:
        return ""
    txt = f.read_text(encoding="utf-8", errors="replace")
    approved = bool(re.search(r"^approved:\s*✅", txt, re.M))
    cards, units, keys, serves, display_serves = _disk_state(page_src)
    page_text = page_src.read_text(encoding="utf-8", errors="replace")
    # The page is the Aims' home (JL 260831, QPf12 row 2: "In the Page as well,
    # and should map to the content"); a plan that still carries Aim rows only
    # fills ids the page does not have.
    aims = {k: v for k, v in _aim_rows(txt).items() if v[0]}
    aims.update(_aim_rows(page_text))
    scaffolds = {}
    for m in re.finditer(r"(?m)^([^\n]*?)<!--\s*realizes:\s*"
                         r"(C\d+\.P\d+\.B\d+)\s*-->\s*$", page_text):
        sm = re.search(r"\b(C\d+\.P\d+\.S\d+)\b", m.group(1))
        if sm:
            scaffolds.setdefault(m.group(2), []).append(sm.group(1))

    # A card names the bullets it SERVES, so the plan never has to be edited
    # to carry an id that did not exist when it was frozen. Many-to-many: PP04
    # answers three bullets, and a bullet may need two cards.
    by_bullet = {}
    for pid, addrs in serves.items():
        for a in addrs:
            by_bullet.setdefault(a, []).append(pid)
    display_by_bullet = {}
    for did, addrs in display_serves.items():
        for a in addrs:
            display_by_bullet.setdefault(a, []).append(did)
    unserved = sorted(pid for pid, a in serves.items() if not a)


    # A bullet may WRAP, and its mark often sits on the continuation line.
    # Reading line-by-line called those bare, which is a false 🕳 on a bullet
    # the author did mark (found by driving it, 260817).
    lines, joined = txt.splitlines(), []
    i = 0
    while i < len(lines):
        cur = lines[i]
        if cur.startswith("- "):
            j = i + 1
            while (j < len(lines) and lines[j].startswith("  ")
                   and not lines[j].lstrip().startswith("- ")):
                cur += " " + lines[j].strip()
                j += 1
            i = j
        else:
            i += 1
        joined.append(cur)

    # One bullet = one planned SENTENCE ANCHOR. Its address is its position
    # (C3.P1.S2 = section 3, paragraph 1, sentence anchor 2), the same grammar
    # haipipe-sentence uses on the rendered page. DRAFT may expand that anchor
    # into several scaffolds (`realizes: C3.P1.B2`); the outline surface keeps
    # the stable Point join and does not pretend to own those later splits.
    rows, tally, cited, bundle_rows = [], {}, set(), []
    cn = pn = sn = nid = 0
    for line in joined:
        # A `## ` that is NOT `## C<n>` ENDS the plan's divisions. The plan's
        # own trailing sections (## Aims, ## Notes for DRAFT) were falling
        # through into the last paragraph, so its 26 `- A1.1 ·` rows rendered
        # as bullets B5..B30 of C15.P2 (JL 260819: "there are 32 points for one
        # paragraph"). Counting only `## C<n>` as a division was half the fix;
        # stopping at the first other `## ` is the other half.
        if line.startswith("## ") and not re.match(r"^## C\d+\b", line):
            break
        if re.match(r"^## C\d+\b", line):
            cn += 1; pn = 0
            rows.append('<div class=row style="margin-top:9px">'
                        '<span class="addr sec">C%d</span><b>%s</b></div>'
                        % (cn, _e(re.sub(r"^C\d+\s*·\s*", "", line[3:].strip()))))
            continue
        if line.startswith("### "):
            pn += 1; sn = 0
            # The paragraph row carries its OWN address in the same column the
            # bullets use (JL 260819, on reading a paragraph title as a broken
            # bullet: "how do you think we can add the Cx.Px to the paragraph
            # sentence as well"). The address was in the file all along; the
            # renderer used to strip it.
            rows.append('<div class="row prow"><span class=addr>C%d.P%d</span>'
                        '<span class=mut>%s</span></div>'
                        % (cn, max(pn, 1),
                           _e(re.sub(r"^C\d+\.P\d+\s*·\s*", "",
                                     line[4:].strip()))))
            continue
        if not line.startswith("- "):
            continue
        sn += 1
        body = re.sub(r"^[SB]\d+\s*·\s*", "", line[2:].strip())
        # The FULL address on every row. It was shortened to P<n>.B<n> once
        # (JL 260817: "为什么还要保留 C1") and JL reversed it on 260819
        # ("could you add back the C? like P2.B1 to C1.P2.B1, so we can know
        # the exact index"): a row is quoted OUT of the pane — in chat, in a
        # card's serves:, in a receipt — and there the C is the part that
        # says where it lives.
        # B, not S. At OUTLINE time a bullet is a POINT, and one point
        # becomes ONE OR MORE sentences when it is drafted (JL 260817:
        # "我们能一句话把一个 point 讲完吗?"). C3.P2 is shared with the
        # sentence address, so the link survives; only the last token
        # differs, and it differs because the units differ.
        full_addr = "C%d.P%d.B%d" % (cn, max(pn, 1), sn)
        addr = full_addr
        def _backlink(exclude=()):
            """The ↩ tag: cards that name THIS bullet in their `serves:`.
            It is skipped for a card the row already prints as a chip, because
            `🧮 PP01 answered 1` then `↩ PP01 ✓` is one fact twice on one line
            (JL 260817, screenshot). It is the ONLY thing that speaks when the
            plan's mark is bare, which is the normal case: the plan is frozen
            before the card exists, so the CARD names the bullet."""
            b = [x for x in by_bullet.get(full_addr, []) if x not in exclude]
            if not b:
                return ""
            # One chip PER card, each opening the card's own popover — the
            # same evidence-card treatment the forward chips got. A bare
            # <span> here meant the one chip that usually speaks for a bullet
            # was the one chip nobody could open (JL 260819: "why the probe
            # PP01 here we cannot click and see it?").
            out = []
            for x in b:
                st = _pstate(cards.get(x, ("?", 0, ""))[0])
                ok = st in LANDED
                cls = "ok" if ok else "mut"
                label = "↩ %s %s" % (_e(x), "✓" if ok else _e(st))
                _c, _n, detail = _live("probe", x, cards, units, keys, aims)
                if not detail:
                    out.append('<span class="evtag %s">%s</span>' % (cls, label))
                    continue
                pid = "bl-%s-%s" % (full_addr.replace(".", "-"), _e(x))
                out.append(
                    '<button class="evchip %s" popovertarget="%s">%s</button>'
                    '<div id="%s" popover class="chipcard %s">'
                    '<div class=cch><b>%s</b><span class=cck>🧮 probe card</span></div>'
                    '<div class=ccb><p>%s</p></div></div>'
                    % (cls, pid, label, pid, cls, _e(x), _e(detail)))
            return " ".join(out)

        # THE MARK IS THE LAST EMOJI ON THE LINE, inside the end-anchored
        # window. A first-hit substring scan read C1.P2.B1 — whose PROSE
        # mentions 📚 and 🧮 mid-sentence before ending `🖼 Display4` — as a
        # citation bullet, so Display4 landed on the orphan row of the very
        # plan that cites it (JL 260819: "Why you still didn't solve this
        # problem? you should cite it."). Same 64-char window as
        # plan_shape.check_coverage, one law in two readers.
        hit, hit_at = None, -1
        for emo, kind in _MARK.items():
            at = body.rfind(emo)
            if at > hit_at and at >= 0 and len(body) - at <= 64:
                hit, hit_at = (emo, kind), at
        def _bullet_row(head_raw, chips_html):
            """One bullet row; Answered:/Drawn:/Note: text folds behind a
            click (JL 260819), so the pane shows only the terse head."""
            m2 = re.search(r'\s(Answered:|Drawn:|Note:|More:|Routed:)\s', head_raw)
            if not m2:
                return ('<div class=row><span class=addr>%s</span>'
                        '<span class=x>%s %s</span></div>'
                        % (addr, _e(head_raw), chips_html))
            head, detail = head_raw[:m2.start()], head_raw[m2.start():].strip()
            # No marker of any kind (JL 260819: "without '>'"): the row reads
            # exactly like a plain one; hover + cursor are the affordance, and
            # a plain Note:'s label is stripped since it names nothing.
            detail = re.sub(r'^(Note|More):\s*', '', detail)
            return ('<details class=brow><summary class=row>'
                    '<span class=addr>%s</span><span class=x>%s %s</span>'
                    '</summary><div class=bdetail>%s</div></details>'
                    % (addr, _e(head.strip()), chips_html, _e(detail)))

        if hit is None:
            # A plain sentence is the NORMAL case, not a defect. Requiring a
            # tag on every line was wrong (JL 260817) and made the plan
            # unreadable: the plan is prose, the notes are the exception.
            tally["plain point"] = tally.get("plain point", 0) + 1
            rows.append(_bullet_row(body, _backlink()))
            continue
        emo, kind = hit
        tally[kind] = tally.get(kind, 0) + 1
        # Split at the WINNING occurrence, not the first: the prose before an
        # end mark may legally mention any glyph.
        raw_said = body[:hit_at].strip()
        after = body[hit_at + len(emo):]
        pat = {"probe": r"(?<![A-Za-z0-9-])(PP\d+)", "value": r"(?<![A-Za-z0-9-])(PP\d+(?:\.v\d+)?)",
               "display": r"(Display\d+)",
               # [A-Za-z]* after the year, not [a-z]?: author-year-WORD keys
               # (`luo2026eventglucose`) were truncated to `luo2026e`, and the
               # chip then reported not-in-bibex for a key nobody wrote.
               "cite": r"(QB\d+|[A-Za-z][\w:-]*\d{4}[A-Za-z]*)",
               "aim": r"(?<![A-Za-z0-9.\-])(A\d+\.\d+|P\d+)"}.get(kind)
        # ALL of them, not the first. "📚 Dowell2016 · Dowell2022" registered
        # only Dowell2016, so the second key appeared as an orphan on the very
        # reverse-join row built to catch orphans (found 260817 by driving it).
        refs = re.findall(pat, after) if pat else []
        # LEGACY TOLERANCE for multi-chip tails (`📚 Gray2021 · 🧮 proof`):
        # the ROW shows only the LAST mark, but the orphan join must credit
        # every kind named anywhere in the end window — Gray2021 printed as
        # an orphan of the very plan that cites it (260819 smoke, QC1).
        _tail = body[-64:]
        for _emo, _kind in _MARK.items():
            _at = _tail.rfind(_emo)
            _p = {"probe": r"(?<![A-Za-z0-9-])PP\d+", "value": r"(?<![A-Za-z0-9-])PP\d+(?:\.v\d+)?",
                  "display": r"Display\d+",
                  "cite": r"QB\d+|[A-Za-z][\w:-]*\d{4}[A-Za-z]*"}.get(_kind)
            if _at >= 0 and _p:
                cited.update(re.findall(_p, _tail[_at:]))
        # A BARE mark whose bullet already has a card is RAISED, and saying
        # "not raised yet" beside a ↩ chip that names the card is one fact
        # contradicted twice on one line (JL 260819: "why here you didn't
        # raise a probe here? I don't understand"). The plan is frozen before
        # the card exists, so bare is the NORMAL case and the backlink is the
        # only thing that knows: let it speak alone.
        # A BARE mark whose bullet already has a card is RAISED, so the chip
        # is suppressed and the ↩ backlink speaks alone. It must NOT skip the
        # Evidence Bundle row below: doing that dropped four rows from the
        # derived bundle, caught by checks/outline.py minutes after I wrote it.
        bare_served = not refs and bool(by_bullet.get(full_addr))
        chips = []
        for ref in (refs or [""]):
            if ref:
                cited.add(ref)
            cls, note, detail = _live(kind, ref, cards, units, keys, aims)
            label = " ".join(x for x in (emo, _e(ref), _e(note)) if x)
            if not detail:
                chips.append('<span class="evtag %s">%s</span>' % (cls, label))
                continue
            # THE EVIDENCE CARD, the board's own one (JL 260817: "我想让它有点
            # 像那个 evidence card 一样"). A chip in the line, a panel beside
            # it holding the THING itself — the reference as printed, the
            # card's own question, the unit's own claim — never a description
            # of it (haipipe-sentence §🃏). Native popover, no script: the
            # panel is real body text, so deleting every <script> leaves it.
            nid += 1
            pid = "ev%d" % nid
            media = ""
            if kind == "display":
                u = _asset_url(units, ref, root)
                if u:
                    media = ('<object class=evfig data="%s"></object>' % _e(u)
                             if u.endswith(".pdf")
                             else '<img class=evfig src="%s" alt="">' % _e(u))
            kindname = {"probe": "probe card", "value": "value",
                        "display": "display unit",
                        "cite": "citation", "aim": "aim"}.get(kind, kind)
            chips.append(
                '<button class="evchip %s" popovertarget="%s">%s</button>'
                '<div id="%s" popover class="chipcard %s">'
                '<div class=cch><b>%s</b><span class=cck>%s %s</span></div>'
                '<div class=ccb>%s<p>%s</p></div></div>'
                % (cls, pid, label, pid, cls, _e(ref or "—"), emo, kindname,
                   media, _e(detail)))
        if bare_served:
            chips = [_backlink()]
        else:
            bl = _backlink(exclude=refs)
            if bl:
                chips.append(bl)
        if kind in {"probe", "value", "display", "cite"}:
            bundle = _bundle_state("value" if kind == "probe" else kind,
                                   refs, full_addr, by_bullet,
                                   display_by_bullet, cards, units, keys,
                                   scaffolds)
            labels = []
            if bundle["sentences"]:
                labels.append("sentence " + ", ".join(bundle["sentences"]))
            if bundle["probes"]:
                labels.append("probe " + ", ".join(bundle["probes"]))
            if bundle["citations"]:
                labels.append("cite " + ", ".join(bundle["citations"]))
            if bundle["displays"]:
                labels.append("display " + ", ".join(bundle["displays"]))
            if bundle["feedback"]:
                labels.append("feedback " + ", ".join(bundle["feedback"]))
            if not labels:
                labels.append("no landed resource")
            state_cls = "ok" if bundle["status"] in {"evidence-ready", "accepted"} else "warn"
            bundle_rows.append(
                '<div class="bundle-row"><span class=addr>%s</span>'
                '<span class=bundle-kind>%s</span><span class=bundle-items>%s</span>'
                '<span class="bundle-state %s">%s</span></div>'
                % (full_addr, kind, _e(" · ".join(labels)), state_cls,
                   _e(bundle["status"]))
            )
        # The chips go INSIDE the sentence's own span, never beside it. As
        # siblings of `.row`'s flex they each became a COLUMN, stole width from
        # the text, and then wrapped their own label into a two-line pill: the
        # sentence got squeezed into half the pane and the plan stopped being
        # skimmable (JL 260817, with a screenshot: "你把这些 outline 都给挤得
        # 不知道去哪儿了"). Inline, they sit at the end of the last line.
        rows.append(_bullet_row(raw_said, " ".join(chips)))

    # ── the join runs BOTH ways ────────────────────────────────────────
    # Bullet → disk catches "we promised a display and built none". Disk →
    # bullet catches the opposite: evidence sitting on the page that no plan
    # line uses. The contract claimed both from the start and only the first
    # was built (found 260817 by checking the file against its own code).
    on_disk = [("🧮", k) for k in cards] + [("🖼", k) for k in units] \
        + [("📚", k) for k in keys]
    orphan = [(e, k) for e, k in on_disk
              if k not in cited and not serves.get(k)]
    if orphan:
        rows.append('<div class=row style="margin-top:11px"><b>🎈 on disk, '
                    'cited by no bullet</b></div>')
        for emo, k in sorted(orphan, key=lambda x: (x[0], x[1])):
            rows.append('<div class=row><span class=addr></span>'
                        '<span class=warn>%s %s</span>'
                        '<span class=mut> — evidence nobody is using, or a '
                        'citation that got lost</span></div>' % (emo, _e(k)))

    # Three counts, computed INDEPENDENTLY. A folder existing is not a landed
    # answer, and a landed answer is not an accepted one; collapsing them into
    # one number is how "declared" got read as "done".
    owed = sum(tally.get(k, 0) for k in ("probe", "value", "display", "cite"))
    landed = _count_landed(txt, cards, units, keys)
    accepted = _count_accepted(txt, cards, units)
    head = "%s plan %s" % ("🔒" if approved else "✍️", _e(ver))
    gate = ('<span class=ok>approved</span>' if approved
            else '<span class=wait>🚧 approved: ⬜ — waiting on a person</span>')
    # The counts run through _e(), so an `&nbsp;` written into the STRING is
    # escaped and printed as the five literal characters (seen in the 260817
    # screenshot: "0 accepted &nbsp; aim 9"). Separators belong in the markup.
    counts = "%d owed · %d landed · %d accepted" % (owed, landed, accepted)
    kinds = " · ".join("%s %d" % (k, v) for k, v in sorted(tally.items()))
    bundle = ""
    if bundle_rows:
        bundle = ('<details class=bundles><summary>🔗 Evidence Bundles · %d '
                  'Point%s</summary>%s</details>'
                  % (len(bundle_rows), "s"[:len(bundle_rows) != 1],
                     "".join(bundle_rows)))
    return ('<div class=card><h2>%s %s</h2>'
            '<div class=mut>%s<span class=sep>%s</span>%s<span class=sep>%s</span>'
            '%s</div>%s%s</div>'
            % (head, gate, _e(counts), "&nbsp;&middot;&nbsp;", _e(kinds),
               "&nbsp;&middot;&nbsp;", _e(f.name), bundle, "".join(rows)))



def _page_now(plan, plan_head, cards):
    """THE PAGE NOW, folded. It answers a different question from the plan and
    is worth keeping, but on a page whose aims carry no ids it is N empty cards
    in the reader's way (JL 260817: "第二部分还有必要要吗? 我感觉有点 confusing").
    So it collapses: one line when there is nothing in it, open on a click."""
    body = "".join(cards)
    empty = body.count("no aim, state or file on this page names this part")
    # `cards` ends with the 🌐 page-wide card, which is NOT a Content division:
    # it is the bucket for everything unanchored. Counting it said "15 Content
    # divisions" on a page with 14 (JL 260819), which is the one number in this
    # drawer's own title and the easiest to trust without checking.
    wide = 1 if any("🌐" in c for c in cards) else 0
    n = len(cards) - wide
    note = (" &middot; all %d empty: this page's aims carry no ids" % n
            if empty >= n else "")
    if wide:
        note += " &middot; plus the 🌐 page-wide card"
    fold = ('<details><summary style="cursor:pointer;color:var(--mut);'
            'font-size:12px;padding:8px 0">📄 THE PAGE NOW &mdash; %d Content '
            'division%s as written today%s</summary>%s</details>'
            % (n, "s"[:n != 1], note, body))
    return (plan_head + plan + fold) if plan else body


# ── the five sibling lenses (haipipe-plugin-outline 0.17.3) ────────────────
# ── the sibling files · ONE record shape, ONE renderer (0.18.0) ────────────
# JL 260831, reading the Discussion and Log lenses on SM00: "really hard to
# read", "the discussion is not for human", "the logging is very bad", then
# "the design of all of them are very bad … we should unify the format".
# Every sibling file is a list of RECORDS with one grammar
# (haipipe-plugin-outline §🧾 One record shape):
#
#   ### <ID> · <HEADLINE>        one line a stranger can read
#   - **<Label>**: <value>       a fixed label set per kind, one line each
#     indented lines             detail, folded under the record
#   > Comment WHO · text · date  signed lanes, kept forever
#
# and this ONE renderer draws every kind the same way: id badge, headline,
# label rows, a status pill, detail folded behind "more". The pre-0.18.0
# shapes (bare `YYMMDD ·` log rows, `- id · head` feedback rows with indented
# `key:` lines, `status:` metadata under a thread, the evidence table) are
# still READ, so an unmigrated page renders instead of breaking.
# 📎 Files is the seventh kind (JL 260831, QPf12-outline row 3: `## Files`
# leaves the page for `<stem>-files.md`, one `### F<n> · <what it is for>`
# per file with Path and Role).
_SIBLINGS = (("req", "📏 Requirement", "requirement"), ("disc", "💬 Discussion", "discussion"),
             ("fb", "🗣 Feedback", "feedback"), ("ev", "🧾 Evidence", "evidence"),
             ("files", "📎 Files", "files"), ("log", "📜 Log", "log"))

_HDR_RE = re.compile(r"^(page|kind|rounds|written|status|plan|ids|measured):\s")
_REC_RE = re.compile(r"^###\s+([^·]+?)\s*·\s*(.*)$")
_OLD_LOG_RE = re.compile(r"^(\d{6}(?:\s+\d{4})?)\s*·\s*(.*)$")
_OLD_FB_RE = re.compile(r"^- ((?:S[A-Z0-9]+-PP\d+|R\d{2}))\s*·\s*(.*)$")
_OLD_EV_RE = re.compile(r"^(C\d+\.P\d+\.B\d+)\s+(\S+)\s+(\S+)\s+(.*?)\s{2,}(\S+)\s*$")
_LABEL_RE = re.compile(r"^-\s+\*\*([^*]+?)\*\*\s*[:：]\s*(.*)$")
_KV_RE = re.compile(r"^\s*(status|serves|round|opened|settled|parent|anchors|state|landed|"
                    r"implements|owner|moved|question|ruling|rationale|consequences|refs|"
                    r"source|received)\s*:\s*(.*)$")
_QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
_PILL_LABELS = ("status", "state", "landed", "decide", "decides", "met")

def _inl(t):
    try:
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from src.body import inline as _inline
        return _inline(t)
    except Exception:
        return html.escape(t)

def _auto_head(text, limit=26):
    """An old one-paragraph row: its first sentence is the headline, the rest
    folds. Long rows were the whole complaint (JL 260831: a 150-word Log row
    rendered as one paragraph)."""
    words = text.split()
    if len(words) <= limit + 6:
        return text, ""
    m = re.match(r"(.{20,240}?[.!?])(?:\s+|$)(.*)", text, re.S)
    if m and len(m.group(1).split()) <= limit + 14:
        return m.group(1), m.group(2).strip()
    return " ".join(words[:limit]) + " …", text

def _records(text):
    """-> [("meta", line) | ("group", title) | ("text", line) | ("rec", rec)]
    rec = {id, head, rows:[[label, value]], quotes:[str], detail:[str]}"""
    items, rec, q, body, q_indent = [], None, None, False, 0
    def push():
        nonlocal rec
        if rec is not None:
            items.append(("rec", rec)); rec = None
    for raw in text.splitlines():
        ln = raw.rstrip()
        s = ln.strip()
        if not s:
            q = None; continue
        if ln.startswith("# ---") or s.startswith("EVIDENCE STATUS") or s.startswith("REQUIREMENT") \
                or s.startswith("regenerate:") or s.startswith("GENERATED"):
            continue
        if ln.startswith("# "):
            continue                      # the file's own title; the tab says it
        if not body and _HDR_RE.match(ln):
            items.append(("meta", s)); continue
        m = _REC_RE.match(ln)
        if m:
            push(); body = True; q = None
            rec = dict(id=m.group(1).strip(), head=m.group(2).strip(), rows=[], quotes=[], detail=[])
            continue
        if ln.startswith("## "):
            push(); body = True; items.append(("group", ln[3:].strip())); continue
        m = _OLD_LOG_RE.match(ln)
        if m and not ln.startswith(" "):
            push(); body = True
            head, rest = _auto_head(m.group(2).strip())
            rec = dict(id=m.group(1), head=head, rows=[], quotes=[], detail=[rest] if rest else [])
            continue
        m = _OLD_FB_RE.match(ln)
        if m:
            push(); body = True
            rec = dict(id=m.group(1), head=m.group(2).strip(), rows=[], quotes=[], detail=[]); continue
        m = _OLD_EV_RE.match(ln)
        if m:
            push(); body = True
            rec = dict(id=m.group(1), head="%s %s" % (m.group(2), m.group(3)),
                       rows=[["Has", m.group(4).strip()], ["Status", m.group(5)]], quotes=[], detail=[])
            push(); continue
        if rec is None:
            m = _KV_RE.match(ln)
            items.append(("text", "%s: %s" % (m.group(1), m.group(2)) if m else s)); continue
        m = _LABEL_RE.match(s)
        if m:
            rec["rows"].append([m.group(1).strip(), m.group(2).strip()]); q = None; continue
        m = _KV_RE.match(ln)
        if m and not s.startswith("- "):
            rec["rows"].append([m.group(1).capitalize(), m.group(2).strip()]); q = None; continue
        m = _QUOTE_RE.match(ln)
        if m:
            rec["quotes"].append(m.group(1)); q = rec["quotes"]
            q_indent = len(ln) - len(ln.lstrip()); continue
        # a lane continues only on a line indented DEEPER than the lane itself;
        # migrated records indent every line by two, and reading those as
        # continuation glued a whole ruling record into one quote (SM06 D01)
        if q is not None and (len(ln) - len(ln.lstrip())) > q_indent:
            q[-1] += " " + s; continue
        q = None
        rec["detail"].append(s[2:] if s.startswith("- ") else s)
    push()
    return items

def _pill(rec):
    """The one row that says where the record stands, as a pill."""
    for lab, val in rec["rows"]:
        L = lab.lower()
        if L not in _PILL_LABELS:
            continue
        v = val.strip(); low = v.lower()
        if L in ("decide", "decides"):
            # the pill names WHO rules; the row stays, it carries serves/opened
            return (None, "acc", v.split(" · ")[0].strip() or "open")
        if L == "landed":
            return (lab, "warn", "not landed") if v in ("", "—", "-") else (lab, "ok", v)
        if any(k in low for k in ("✅", "settled", "landed", "accepted", "evidence-ready", "decided", "gated")) \
                or low in ("met", "yes"):
            return (lab, "ok", v)
        if any(k in low for k in ("open", "needs", "🔴", "🟡", "hold", "unmet", "⬜")) or v in ("", "—", "-"):
            return (lab, "warn", v or "open")
        return (lab, "mut", v)
    return None

def _rec_html(rec, kind):
    pill = _pill(rec)
    h = ['<div class="rec %s"><div class=rh><span class=rid>%s</span><span class=rt>%s</span>'
         % (kind, _e(rec["id"]), _inl(rec["head"]))]
    if pill:
        h.append('<span class="pill %s">%s</span>' % (pill[1], _e(pill[2])))
    h.append("</div>")
    rows = [(l, v) for l, v in rec["rows"] if not (pill and l == pill[0])]
    if rows:
        h.append("<div class=rrows>" + "".join(
            '<div class=rr><b>%s</b><span>%s</span></div>' % (_e(l), _inl(v)) for l, v in rows) + "</div>")
    qs = rec["quotes"]
    inline_q = qs if (len(qs) <= 2 and sum(len(x) for x in qs) <= 300) else []
    for qq in inline_q:
        h.append('<div class=rq>%s</div>' % _inl(qq))
    d = [x for x in rec["detail"] if x]
    folded_q = [] if inline_q else qs
    n = len(d) + len(folded_q)
    if n:
        body = "".join('<div class=rq>%s</div>' % _inl(x) for x in folded_q) + \
               "".join('<div>%s</div>' % _inl(x) for x in d)
        if n > 2 or sum(len(x) for x in d + folded_q) > 240:
            h.append('<details class=rd><summary>more · %d line%s</summary><div class=rdb>%s</div></details>'
                     % (n, "s"[:n != 1], body))
        else:
            h.append('<div class=rdb>%s</div>' % body)
    h.append("</div>")
    return "".join(h)

def _records_html(items, kind):
    out, meta = [], []
    for k, v in items:
        if k == "meta":
            if not v.startswith(("page:", "kind:")):
                meta.append(_e(v))
        elif k == "group":
            out.append('<div class=rgrp>%s</div>' % _inl(v))
        elif k == "text":
            out.append('<div class=rpre>%s</div>' % _inl(v))
        else:
            out.append(_rec_html(v, kind))
    head = ('<div class="mut rmeta">%s</div>' % " · ".join(meta)) if meta else ""
    return head + ("".join(out) or '<div class=mut>nothing here yet</div>')

def _lenses(page_src):
    """-> (chips html, lenses html) for the sibling files that exist."""
    if page_src is None:
        return "", ""
    chips, lenses = [], []
    for key, label, suffix in _SIBLINGS:
        f = page_src.parent / "outline" / ("%s-%s.md" % (page_src.stem, suffix))
        if not f.is_file():
            continue
        items = _records(f.read_text(encoding="utf-8", errors="replace"))
        n = sum(1 for k, _ in items if k == "rec")
        chips.append('\n <button class=chip data-lens=%s title="outline/%s">%s%s</button>'
                     % (key, f.name, label, (" · %d" % n) if n else ""))
        lenses.append('\n<div class=lens id=lens-%s><div class=card>%s</div></div>'
                      % (key, _records_html(items, key)))
    return "".join(chips), "".join(lenses)

def render(title, o, page_src=None, root=None):
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
    # TWO HALVES, and they are not the same thing (JL 260817 asked what the
    # second one was for). The PLAN is what we said we would write; the PAGE
    # is what is written now. Reading them unlabelled beside each other, with
    # two different section lists, is what made the tab confusing.
    plan = plan_card(page_src, root) if page_src is not None else ""
    plan_head = ('<div class=lead>🧭 THE PLAN &mdash; what this page said it '
                 'would cover. Authored, frozen when approved.</div>')
    by_div = _page_now(plan, plan_head, cards) if o["divs"] else (plan +
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
    extra_chips, extra_lenses = _lenses(page_src)
    return _PAGE.format(title=_e(title), lead=lead, tally=_tally(o),
                        chip=chip, by_div=by_div, by_prog="".join(prog),
                        extra_chips=extra_chips, extra_lenses=extra_lenses)


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
        # haipipe-plugin-outline 0.16.0: the Aims live in the PLAN and the page
        # keeps no copy, so a migrated page parsed alone reads "lists no aims
        # yet" while its plan holds them (JL 260830, SM08). Page first, plan
        # second, the same order check.py's page_aims_text uses.
        if not o.get("aims"):
            plan, _v = _latest_plan(page_src)
            if plan is not None:
                po = parse_outline(plan.read_text(encoding="utf-8", errors="replace"))
                if po.get("aims"):
                    o["aims"] = po["aims"]
        page = render(page_src.stem, o, page_src, self.root)
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
