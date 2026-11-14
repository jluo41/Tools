"""📃 Page · the By-division and By-progress lenses: one card per division, its aims with their State receipts, and the page tally.

Moved out of outline.py (the 600-line rule); outline re-exports every name here.
"""
from live.outline_parse import _ID_RE, _strip_id
from live.outline_plan_html import _e


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
            '<details><summary>✅ done</summary>%s</details>'
            % (               "".join(_aim_row(a, receipt=byid.get(a["id"]))
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
        # the bar shows the share; the words say the state, never "N of M" (JL 261113)
        bits.append('<b>%s</b>' % ("done" if not todo else "in progress" if done else "not started"))
    if waiting:
        bits.append('<span class=wait>🗣 %d waiting on you</span>' % waiting)
    if not bits:
        bits.append('<span class=mut>this page lists no aims yet</span>')
    return " ".join(bits)
