#!/usr/bin/env python3
"""🧭 The outline surface's standing check (QPf12), offline and read-only.

    python3 checks/outline.py [--boards DIR ...]

WHAT IT GUARDS. The 🧭 tab renders a page's aims and states grouped by Content
division, from the material alone. Two promises hold that up, and each has
already been broken once during the build:

  ① NO ROW IS EVER LOST. Every aim and every state must land on exactly one
    card. An `### A6` group on a page whose Content declares no division 6
    used to point at a card nobody drew, and the aim disappeared from BOTH
    lenses. Silent, and worse than a crash.

  ② NO ANCHOR IS EVER INVENTED. `§` was in use on these boards before this
    plugin, meaning a division of ANOTHER page (`QB6 §7`), a sub-division
    (`§5.1`), a named section (`§Required Inputs`), and, in ordinary prose on
    a paper-section page, the manuscript's own section ("Every number §4
    prints"). Shape-matching flagged four innocent pages; POSITION flags none.

So this walks every page of every board it is given, parses and renders each,
and fails on a crash, a lost row, or an anchor the page's writer did not write.
The unit table below pins the position rule itself, because a board can hold
none of a shape and still meet one tomorrow.

QPf12 · P2 is the aim this check closes.
"""
import argparse
import sys
import tempfile
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent      # the engine dir
sys.path.insert(0, str(HERE))
from live.outline import parse_outline, plan_card, render, _anchors   # noqa: E402

# (line, leading anchors, trailing anchors) · every row is a real shape seen on
# a real page, or the exact shape the contract promises to read.
CASES = [
    # the anchor, where an anchor belongs
    ("- [x] 📂 §1 The folder shows itself", [1], []),
    ("§1 Shipped 260724.", [1], []),
    ("- ✅ §2 the row is a door", [2], []),
    ("- A1.1 · §3 with an id first", [3], []),
    ("- [ ] §12 double digit", [12], []),
    # prose, where an anchor never belongs
    ("- Q-Sec4Results-1 · Every number §4 prints traces", [], []),
    ("- 260806 CC · a real §4, not an essay about §4s", [], []),
    ("The rule is documented in `conv.md` §3 with an explicit", [], []),
    ("- `QB6` §7 states", [], []),
    ("- §5.1 sub-division", [], []),
    ("- §Required Inputs says S-Work-C", [], []),
    ("- [x] plain aim, no anchor", [], []),
    # a Files row, whose anchors trail and may be several
    ("- `cli/build.py` §1 §2", [], [1, 2]),
    ("- `serve.py` §2", [], [2]),
    ("- `f.py` §12", [], [12]),
    ("- `unanchored.py`", [], []),
    ("- `reads · EVIDENCE` · [QB7 §3](QB-research/QB7-literature.md)", [], []),
    ("- The display page whose `§4 Placement` record names this", [], []),
]

# Page shapes that must not crash and must not swallow a row.
SHAPES = {
    "dotted-only S page":
        "## Content\n### §6.1 · First\n### §6.2 · Second\n"
        "## Aims\n### A6 · Six\n- A6.1 · an aim\n"
        "## States\n### A6 · Six\n- ✅ A6.1 · done\n",
    "no Content at all":
        "## Aims\n- [ ] just an aim\n## States\nsome state\n",
    "A-group naming an undeclared division":
        "## Content\n### 1 · One\n## Aims\n### A9 · Nine\n- A9.1 · orphan\n"
        "## States\n### A9 · Nine\n- ⬜ A9.1 · pending\n",
    "legacy section names":
        "## Question\nq\n## Items to Finish\n- [x] old-style aim\n"
        "## Where we are\ndone\n",
    "empty page": "",
    "Content only": "## Content\n### 1 · One\n### 2 · Two\n",
}


BRIEFS = {
    "the template's job line":
        "## Content\n### 1 · One\n```text\nfig\n```\n"
        "📌 This part fixes the mark itself.\nProse follows.\n",
    "a job line in another hand":
        "## Content\n### 1 · One\n📋 Establishes the reading protocol.\nProse.\n",
    "no job line, a caption instead":
        "## Content\n### 1 · One\n**The tab**: the first surface renders the folder.\n"
        "```text\nfig\n```\nProse follows.\n",
    "neither, so the first sentence":
        "## Content\n### 1 · One\nThe plainest sentence on the page.\n",
    "nothing to read, so no brief":
        "## Content\n### 1 · One\n**GROUP**\n- a bullet\n- another bullet\n",
}
BRIEF_WANT = ["This part fixes the mark itself.",
              "Establishes the reading protocol.",
              "the first surface renders the folder.",
              "The plainest sentence on the page.",
              None]


# A card has to keep an Aim and its State legible as two different sentences,
# and a Decision Now block is neither of them (JL 260816: "I cannot understand
# what is happening"). Both broke once: the id printed twice made one sentence
# look like two, and `### 🗣 Decision Now` went unrecognized so its pending asks
# were counted as facts about an aim.
READABLE = """## Content
### 1 · The contract
📌 what a person writes and keeps.
## Aims
### A1 · The contract
- A1.1 · The row grammar survives a refresh untouched.
## States
### 🗣 Decision Now
- [ ] 🗣 Does a seed ever go deeper than the named page?
- [x] 🗣 An answered ask, which no longer waits.
### A1 · The contract
- ✅ A1.1 · A re-mint left the store byte-identical.
"""


def lost_rows(o):
    """-> the aims and states that no card would draw. Must always be empty."""
    cards = {d["n"] for d in o["divs"]} | {None}
    return [r for r in o["aims"] + o["states"] if r["div"] not in cards]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boards", nargs="*", default=None,
                    help="board folders to sweep; default: every board under "
                         "the toolkit and its sibling plugins")
    args = ap.parse_args()
    fails = []

    print("① the position rule")
    for line, lead, trail in CASES:
        got = (_anchors(line), _anchors(line, trailing=True))
        if got != (lead, trail):
            fails.append(f"anchor {line!r} -> {got}, want {(lead, trail)}")
    print(f"   {len(CASES)} shapes · "
          f"{'ok' if not fails else str(len(fails)) + ' FAILED'}")

    print("② page shapes that must not swallow a row")
    for name, text in SHAPES.items():
        try:
            o = parse_outline(text)
            render("x", o)
            if lost_rows(o):
                fails.append(f"shape {name!r} lost {len(lost_rows(o))} rows")
        except Exception:
            fails.append(f"shape {name!r} CRASH "
                         f"{traceback.format_exc().splitlines()[-1]}")
    print(f"   {len(SHAPES)} shapes · ok")

    print("③ the division brief, read and never invented")
    for (name, text), want in zip(BRIEFS.items(), BRIEF_WANT):
        got = parse_outline(text)["divs"][0].get("brief")
        if got != want:
            fails.append(f"brief {name!r} -> {got!r}, want {want!r}")
    print(f"   {len(BRIEFS)} shapes · ok")

    print("④ an aim, its state, and an ask stay three different things")
    o = parse_outline(READABLE)
    html = render("x", o)
    if len(o["states"]) != 1:
        fails.append(f"a Decision Now ask leaked into States: {o['states']}")
    if [d["answered"] for d in o["decisions"]] != [False, True]:
        fails.append(f"decisions misread: {o['decisions']}")
    # Both lenses are rendered server-side, so an aim legitimately appears
    # twice in the file; what must never double is the id WITHIN one lens,
    # which is what made an Aim and its State read as one sentence twice.
    div_lens = html.split("id=lens-prog")[0]
    if div_lens.count("A1.1") != 1:
        fails.append(f"the id A1.1 printed {div_lens.count('A1.1')} times "
                     f"in the division lens, want 1")
    if "class=now" not in html:
        fails.append("the state lost its `now` label under its aim")
    if "🗣 1 waiting on you" not in html:
        fails.append("the unanswered ask is not counted in the header")
    print("   1 page · ok")

    print("⑤ a Point exposes a derived Evidence Bundle")
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        page = root / "QF1-page.md"
        page.write_text(
            "# QF1\n\nC1.P1.S1 · The headline effect is <VALUE HOLE>. "
            "<!-- realizes: C1.P1.B1 -->\n",
            encoding="utf-8",
        )
        outline = page.parent / "outline"
        outline.mkdir()
        (outline / "QF1-page-outline-v1.md").write_text(
            "# QF1 · outline v1\noutline-version: v1\n"
            "approved: ✅\n\n## C1 · Result\n\n"
            "### C1.P1 · Headline\n- B1 · the headline effect 🔢\n"
            "- B2 · the headline display 🖼 Display2\n",
            encoding="utf-8",
        )
        probe = page.parent / "probe" / "PP01-headline-effect"
        probe.mkdir(parents=True)
        (probe / "card.md").write_text(
            "# PP01-headline-effect\nstate: read\n"
            "read: ✅\nserves: C1.P1.B1\n"
            "question: what is the headline effect?\n",
            encoding="utf-8",
        )
        display = page.parent / "display" / "QF1-page-Display2-headline"
        (display / "assets").mkdir(parents=True)
        (display / "intake").mkdir()
        (display / "intake" / "manifest.yaml").write_text(
            "card: PP01-headline-effect\n", encoding="utf-8"
        )
        (display / "assets" / "plot.pdf").write_bytes(b"pdf")
        (display / "preview.pdf").write_bytes(b"pdf")
        (display / "README.md").write_text(
            "claim the headline display\nrenderer: haipipe-display-figure\n"
            "intake: frozen · intake/manifest.yaml\n"
            "serves: C1.P1.B2\naccepted: ✅\n",
            encoding="utf-8",
        )
        bundle_html = plan_card(page)
        for wanted in ("Evidence Bundles", "C1.P1.B1", "C1.P1.S1", "needs-probe",
                       "feedback PP01: read", "feedback Display2: accepted"):
            if wanted not in bundle_html:
                fails.append(f"derived bundle omitted {wanted!r}")
    print("   1 Point · ok")

    # A reader who cannot hold six paragraphs at once, in a language that is
    # not their first, has to get the answer before the detail (JL 260816: "我
    # 读完之后 no idea，不知道在干嘛"). Three things carry that, and each is a
    # thing the page already says, so none can be lost to a later edit.
    print("⑥ the answer arrives before the detail")
    o = parse_outline("## Opening\nWhat is this page for, in one question?\n"
                      "## Content\n### 1 · One\n📌 the brief.\n"
                      "## Aims\n### A1 · One\n- A1.1 · a done aim\n"
                      "- A1.2 · an open aim\n"
                      "## States\n### A1 · One\n- ✅ A1.1 · met\n"
                      "- ⬜ A1.2 · not started\n")
    html = render("x", o)
    if o["lead"] != "What is this page for, in one question?":
        fails.append(f"the page's own purpose is missing: {o['lead']!r}")
    for want, why in [
            ("What is this page for", "the purpose line"),
            ("1 of 2 done", "the tally"),
            ("⬜ 1 to do", "what is left"),
            ("still to do", "the open aims, always in sight"),
            ("<details>", "the done aims, folded away")]:
        if want not in html:
            fails.append(f"{why} is gone from the page header ({want!r})")
    if html.index("still to do") > html.index("<details>"):
        fails.append("finished work is printed before the work still to do")
    print("   1 page · ok")

    print("⑦ every page of every board")
    roots = ([Path(b) for b in args.boards] if args.boards else
             sorted({p.parent for p in
                     (HERE / "../../../..").resolve().rglob("board.md")
                     if "_archive" not in p.parts}))
    total = 0
    for root in roots:
        pages = [p for p in root.rglob("*.md")
                 if p.name != "board.md"
                 and not any(s.startswith(("_", ".")) for s in
                             p.relative_to(root).parts)]
        for p in pages:
            try:
                o = parse_outline(p.read_text(encoding="utf-8",
                                              errors="replace"))
                render(p.stem, o)
                total += 1
                if o["bad"]:
                    fails.append(f"{p.name} invented an anchor: {o['bad']}")
                if lost_rows(o):
                    fails.append(f"{p.name} lost {len(lost_rows(o))} rows")
            except Exception:
                fails.append(f"{p.name} CRASH "
                             f"{traceback.format_exc().splitlines()[-1]}")
        print(f"   {root.name:<34} {len(pages):>4} pages")
    print(f"   {total} pages across {len(roots)} boards")

    print()
    if fails:
        print(f"❌ {len(fails)} FAILURES")
        for f in fails[:20]:
            print("   ", f)
        return 1
    print("✅ outline: position rule, page shapes, and every board page pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
