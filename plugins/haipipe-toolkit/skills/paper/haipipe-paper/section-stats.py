#!/usr/bin/env python3
"""Measure an S page's prose FORM and print the structure block for `## Diagram`.

The shape is the one `S-Main-2` established by hand and JL ruled as the house
style on 2026-07-27: subsection, then one line per paragraph carrying that
paragraph's JOB and its counts, then a total with citation density.

    §2.1 Physician Prescribing Behavior and Personality Traits (2 P)
      P1. Prescribing varies + opioids consequential          6 sentences · ~155 words

    total: 8 P · 46 sentences · ~1,263 words · 38 unique \\citep keys (~0.8/sentence)

Why a script and not a hand-typed table: a form table is wrong the moment one
sentence changes, and a wrong one is worse than none, because it reads as
measured. So this is generated, dated, and regenerated rather than edited.

    python3 section-stats.py <S-page.md> [--date=YYMMDD] [--sentences]

`--sentences` adds a per-sentence word bar under each paragraph. It is off by
default because on a multi-paragraph section it buries the structure, and the
structure is what the block is for. On a one-paragraph section such as an
abstract it is the only informative view, so turn it on there.

Reads only `## Content` prose, by the paper dialect's own rules: `###` opens a
subsection, `####` opens a paragraph, the `(…)` line under a `####` is that
paragraph's job and not prose, a `>` line is an apparatus lane and not prose,
one sentence per source line. A `[Q-…]` bracket is apparatus too and is
stripped before counting, because a word budget is about what a reader reads.
"""
import pathlib
import json
import re
import statistics
import sys
from datetime import datetime
from pathlib import Path

QREF = re.compile(r"\[Q-[A-Za-z0-9]+-\d+\]")
CITE = re.compile(r"\\cite[tp]?\*?\{([^}]*)\}")
BEGIN, END = "# --- form:begin (generated) ---", "# --- form:end ---"
SKIP_H = ("stage record",)          # bookkeeping, not prose
CONTENT_STOPS = ("Aims", "Items to Finish", "States", "State", "Where we are", "Now", "Files")


def content_body(text):
    """Return Content only, accepting canonical Aims/States and legacy aliases."""
    if "## Content" not in text:
        return ""
    body = text.split("## Content", 1)[1]
    stop = re.search(
        rf"^## (?:{'|'.join(re.escape(name) for name in CONTENT_STOPS)})\s*$",
        body,
        re.M,
    )
    return body[:stop.start()] if stop else body


def words(line):
    return len(QREF.sub("", CITE.sub("", line)).split())


def parse(text):
    """-> [(subsection|None, [(pnum_and_job, [sentence, ...]), ...]), ...]"""
    if "## Content" not in text:
        return []
    body = content_body(text)
    subs, sub, para, job, sents = [], None, None, "", []

    def flush_para():
        if para is not None:
            subs[-1][1].append((para, job, sents[:]))

    for raw in body.split("\n"):
        s = raw.strip()
        if s.startswith("#### ") and re.match(r"P\d+\.", s[5:].strip()):
            flush_para()
            if not subs:
                subs.append((None, []))
            para, job, sents = s[5:].strip(), "", []
        elif s.startswith("#### "):        # a non-P heading: a table, a note
            flush_para()
            para, job, sents = None, "", []
        elif s.startswith("### "):
            flush_para()
            para, job, sents = None, "", []
            h = s[4:].strip()
            if h.lower() in SKIP_H:
                subs.append((h, []))          # kept so it can be dropped below
            else:
                subs.append((h, []))
        elif s.startswith("(") and para is not None and not job and not sents:
            job = s.strip("()").strip()
        elif not s or s.startswith((">", "```", "- ", "* ", "#", "|", "$")):
            continue
        elif para is not None:
            sents.append(s)
    flush_para()
    # drop empty subsections and bookkeeping ones
    return [(h, ps) for h, ps in subs
            if ps and (h is None or h.lower() not in SKIP_H)]


def bar(n, width=34):
    return "\u2588" * min(n, width)


def render(path, date, per_sentence=False):
    text = Path(path).read_text(encoding="utf-8")
    subs = parse(text)
    if not subs:
        return f"{BEGIN}\n  no ## Content prose found in {Path(path).name}\n{END}"

    keys, every, npara = set(), [], 0
    for _, ps in subs:
        for _, _, ss in ps:
            npara += 1
            for s in ss:
                every.append(words(s))
                for m in CITE.finditer(s):
                    keys.update(k.strip() for k in m.group(1).split(",") if k.strip())

    L = [BEGIN,
         f"  FORM, MEASURED {date}. GENERATED; do not hand-edit.",
         f"  regenerate: section-stats.py .../{Path(path).name}"
         + (" --sentences" if per_sentence else ""),
         ""]
    med = statistics.median(every) if every else 0
    pn = 0
    for head, ps in subs:
        if head:
            L.append(f"{head} ({len(ps)} P)")
        for title, job, ss in ps:
            pn += 1
            ws = [words(s) for s in ss]
            # the paragraph's JOB is the point of this line, so it gets the room
            raw = job or title
            # cut at a WORD boundary: a job sliced mid-word reads as corruption
            what = raw if len(raw) <= 58 else raw[:58].rsplit(" ", 1)[0] + " …"
            L.append(f"  {title.split('.')[0]}. {what:<60}"
                     f"{len(ss)} sentences \u00b7 ~{sum(ws)} words")
            if per_sentence:
                for i, w in enumerate(ws, 1):
                    flag = " \u27f5 long" if med and w >= 1.5 * med else ""
                    L.append(f"       S{i:<3}{w:>3}w  {bar(w)}{flag}")
        L.append("")
    dens = f" (~{len(keys) / len(every):.1f}/sentence)" if every else ""
    L.append(f"total: {npara} P \u00b7 {len(every)} sentences \u00b7 ~{sum(every)} words"
             f" \u00b7 {len(keys)} unique \\citep keys{dens}")
    L.append("  words = PROSE only; \\citep{} commands are excluded, so this runs"
             " below a count that included them")
    if every:
        L.append(f"  sentence length: median {med:.0f}"
                 f" \u00b7 range {min(every)}-{max(every)}"
                 f" \u00b7 mean {statistics.mean(every):.1f}")
    L.append(END)
    return "\n".join(L)




# ---------------------------------------------------------------- dashboard --
# Transcribed ONCE from S-Venue-0-venue.md's Structural Blueprint, which is the
# venue stage's resolved contract. Kept here rather than re-parsed because that
# file states budgets in prose ("2,000-4,000 words (Research Article)") and a
# parser for it would be a second thing to keep true. If the venue is retargeted
# these change with it, and the dashboard says out loud that they are
# transcribed rather than measured.
FLOOR = {"0": (0, 0), "1": (2000, 4000), "2": (0, 0), "3": (2900, 6000),
         "4": (0, 0), "5": (0, 0), "6": (1500, 3000), "7": (2300, 5000),
         "8": (0, 0)}
CDENS = {"0": 0.0, "1": 0.50, "2": 0.80, "3": 0.72, "4": 0.34,
         "5": 0.34, "6": 0.30, "7": 0.21, "8": 0.0}
REFRX = re.compile(r"\\(?:auto|C|c)?ref\{((?:tab|fig):[^}]*)\}")
QIDRX = re.compile(r"\[(Q-[A-Za-z0-9]+-\d+)\]")


def prose_lines(text):
    body = content_body(text)
    return [l.strip() for l in body.split("\n")
            if l.strip() and not l.strip().startswith((">", "(", "#", "|", "`"))]


def dashboard(main_dir, date):
    """One generated block: the facts no SINGLE section page can hold.

    board.md's test for a unit-0 page is that it "answers only what no single
    asset can". A word floor means nothing without the venue table, "9 of 10
    units placed" needs all nine pages at once, and a defect count is only
    trustworthy when it counts PROSE SENTENCES rather than the Items and Log
    entries that describe defects. That last one is why this exists: on
    2026-07-27 the board reported 81 defects and the real number was 15.
    """
    main = pathlib.Path(main_dir)
    # label -> unit, so "which units does the prose name" is a real lookup
    # rather than a string-prefix guess (the first version reported all ten
    # unplaced because it compared a label against a folder-name fragment).
    unit_of, units = {}, set()
    root = main.parent.parent
    # Display workspace is an optional runtime area; deliverable assets live in
    # the paper's unnumbered displays/ root. Follow both supported homes.
    homes = [main.parent / "S05-display" / "workspace", root / "displays"]
    for f in [x for h in homes for x in h.glob("*/float.tex")]:
        units.add(f.parent.name)
        for lab in re.findall(r"\\label\{([^}]*)\}", f.read_text()):
            unit_of[lab] = f.parent.name
    asked = set()
    for stage in ("S03-literature", "S04-value"):
        for topic in (main.parent / stage).glob("S-*.md"):
            asked.update(re.findall(r"Q-[A-Za-z][A-Za-z0-9-]*", topic.read_text()))

    L = [BEGIN,
         f"  SECTION DASHBOARD, MEASURED {date}. GENERATED; do not hand-edit.",
         "  regenerate: section-stats.py --dashboard <0-lifecycle/S06-main>",
         "  floors and citation targets are TRANSCRIBED from S-Open-Venue.md's",
         "  Structural Blueprint; everything else is measured from the pages.",
         "",
         "  §  page            P  sent  words  floor      !    cite  targ  disp  bad  state",
         "  " + "-" * 76]
    placed, tot_def, tot_w, owed, noq = set(), 0, 0, 0, 0
    detail, rows, found = [], [], []
    for p in sorted(main.glob("S-Main-[0-9]*.md")):
        n = p.name.split("-")[2]
        text = p.read_text()
        subs = parse(text)
        sents = [s for _, ps in subs for _, _, ss in ps for s in ss]
        npara = sum(len(ps) for _, ps in subs)
        w = sum(words(s) for s in sents)
        tot_w += w
        keys = set()
        for s in sents:
            for m in CITE.finditer(s):
                keys.update(k.strip() for k in m.group(1).split(","))
        dens = len(keys) / len(sents) if sents else 0
        pl = prose_lines(text)
        d_toadd = sum(1 for l in pl for m in CITE.findall(l) if "TOADD" in m)
        d_q = sum(1 for l in pl for q in QIDRX.findall(l) if asked and q not in asked)
        # WHAT the defect is, not just how many. A count tells you where to look
        # and nothing about what to do; these lines name the sentence.
        issues, para = [], ""
        for raw in content_body(text).split("\n"):
            s = raw.strip()
            if s.startswith("#### "):
                para = s[5:].split(".")[0]
            if not s or s.startswith((">", "(", "#", "|", "`")):
                continue
            for m in CITE.findall(s):
                if "TOADD" in m:
                    issues.append((para, "owed citation, .bib is human-only",
                                   s[:64] + ("…" if len(s) > 64 else "")))
            for q in QIDRX.findall(s):
                if asked and q not in asked:
                    issues.append((para, q + " has no probe entry",
                                   s[:64] + ("…" if len(s) > 64 else "")))
        for l in pl:
            for lab in REFRX.findall(l):
                if lab in unit_of:
                    placed.add(unit_of[lab])
        owed += d_toadd
        noq += d_q
        d = d_toadd + d_q
        tot_def += d
        lo, hi = FLOOR[n]
        # LOW is its OWN column. Appended to `floor` it overflowed the field
        # and shifted every column right on exactly the rows that matter
        # (JL 2026-07-27, reading the render).
        fl = "-" if not lo else "%d-%d" % (lo, hi)
        low = "LOW" if lo and w < lo else ""
        st = re.search(r"^state:\s*(\S+)", text, re.M)
        # The board turns a PAGE ID inside a figure into a link (`link_faces`,
        # JL 260730), and it does not know what `1-introduction` is. Printing
        # the id instead of the slug makes every row of this table clickable
        # with no new machinery: the reader sees a number they doubt and lands
        # on the page that produced it.
        page_id = "S-Main-%s" % n
        rows.append(dict(unit=n, page_id=page_id, file=p.name, paragraphs=npara,
                         sentences=len(sents), words=w, floor_low=lo, floor_high=hi,
                         under_floor=bool(low), cite_density=round(dens, 2),
                         cite_target=CDENS[n],
                         displays=len(REFRX.findall("\n".join(pl))), defects=d,
                         state=st.group(1) if st else "?"))
        L.append("  %s  %-14s %2d %5d %6d  %-9s %-4s %.2f  %.2f %4d %4d  %s" %
                 (n, page_id, npara, len(sents), w, fl, low, dens,
                  CDENS[n], len(REFRX.findall("\n".join(pl))), d,
                  st.group(1) if st else "?"))
        for one in issues:
            detail.append("  §%s %-4s %-38s %s" % (n, one[0], one[1], one[2]))
            found.append(dict(unit=n, page_id=page_id, paragraph=one[0],
                              what=one[1], sentence=one[2]))
    L += ["  " + "-" * 76,
          "  %d prose words across the section set" % tot_w,
          "  %d REAL defects in PROSE SENTENCES: %d owed citation(s), %d Q-id(s) that no"
          % (tot_def, owed, noq),
          "     probe entry declares. A marker inside an Aim record or a Log entry is a",
          "     defect being REPORTED, not committed, and is not counted here.",
          "  displays: %d of %d units are named by some section's prose"
          % (len(placed), len(units)),
          "  unplaced: %s" % (", ".join(sorted(units - placed)) or "none")]
    if detail:
        L += ["", "  THE %d ISSUES, BY SENTENCE" % tot_def,
              "  a defect here is a claim a reader cannot check, or a hole no",
              "  question owns. Each line is the sentence that carries it.",
              "  " + "-" * 76] + detail
    L.append(END)

    # THE MEASUREMENT IS DATA FIRST, TEXT SECOND (JL 260806).
    #
    # Until now the only place these numbers existed was the text block above,
    # which meant nothing could check them and nothing else could read them. A
    # number that lives only as prose drifts, and this page's own words are the
    # warning: four of nine hand-written totals had already drifted by
    # 2026-07-27, one of them by eleven sentences, and "a wrong measurement is
    # worse than none, because it reads as measured".
    #
    # So the profile is written beside the page as JSON and the table is one
    # rendering of it. `check.py` can then compare what a page SAYS against what
    # was MEASURED, another page can cite a figure by path instead of retyping
    # it, and an analysis in any language reads the profile rather than parsing
    # a fixed-width table.
    profile = dict(
        measured=date,
        generator="section-stats.py --dashboard",
        source=str(main),
        rows=rows,
        totals=dict(prose_words=tot_w, defects=tot_def, owed_citations=owed,
                    unowned_q_ids=noq,
                    displays_placed=len(placed), displays_total=len(units),
                    unplaced=sorted(units - placed)),
        issues=found,
    )
    (main / "profile.json").write_text(json.dumps(profile, indent=2) + "\n")
    return "\n".join(L)


if __name__ == "__main__":
    argv = sys.argv[1:]
    args = [a for a in argv if not a.startswith("--")]
    # Default to the REAL clock, not to "unknown date". The standing rule is
    # never to invent a date, and reading one is the opposite of inventing it.
    # A block whose whole job is to say when it was measured, printing "unknown
    # date", is the stale-aggregate failure this script exists to prevent.
    date = next((a.split("=", 1)[1] for a in argv if a.startswith("--date=")),
                datetime.now().strftime("%y%m%d"))
    if not args:
        sys.exit(__doc__)
    if "--dashboard" in argv:
        block = dashboard(args[0], date)
        page = next(Path(args[0]).glob("S-*-Dash.md"), None)
        if page is None or "--print" in argv:
            print(block)
        else:
            # REPLACE THE BLOCK, do not print it for a person to paste.
            # The page has always said "produced by this script and replaced
            # whole on every run"; until 260806 the script printed to stdout and
            # a human pasted, which is how the block on disk came to be ten days
            # stale and to carry a regenerate command naming a folder that had
            # been renamed. A generated block that a person has to move by hand
            # is a hand-maintained block wearing a machine's label.
            text = page.read_text(encoding="utf-8")
            if BEGIN in text and END in text:
                head, rest = text.split(BEGIN, 1)
                new = head + block + rest.split(END, 1)[1]
            else:
                sys.exit(f"{page.name} carries no {BEGIN} … {END} pair to replace. "
                         f"Paste the block once by hand, then this runs itself.")
            page.write_text(new, encoding="utf-8")
            print(f"{page.name}: block replaced · profile.json written")
    else:
        print(render(args[0], date, per_sentence="--sentences" in argv))
