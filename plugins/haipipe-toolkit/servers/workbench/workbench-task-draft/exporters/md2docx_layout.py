"""Word namespaces, page measures, column widths, and which lanes and headings a manuscript keeps."""

import re

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
OFF = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
DRW = "http://schemas.openxmlformats.org/drawingml/2006"
LANES = ("Value:", "Note:", "Display:", "Citation:", "Check:")   # the fallback partition
EMU_IN = 914400
BODY_IN = 6.0               # usable text width
BODY_TW = 9360              # the same width in twentieths of a point, for tables


# Approximate advance widths in TWIPS for 10pt Times New Roman. Character COUNT
# was the first proxy and it is too coarse in the direction that matters: a
# results column is digits, which are half again as wide as lowercase, so
# "+12.90*** (3.68)" needs more room than the 16 characters of a row label
# suggest and was landing 0.02in inside its column.
_TW = {" ": 50, ".": 50, ",": 50, ";": 50, ":": 50, "(": 67, ")": 67,
       "*": 70, "-": 67, "–": 100, "+": 113, "=": 113, "%": 167}
_TW.update({c: 100 for c in "0123456789"})


def text_tw(s):
    return sum(_TW.get(c, 132 if c.isupper() else 89) for c in s)


def col_widths(rows, ncol, total=BODY_TW, pad=216):
    """Split `total` across `ncol` columns, `pad` covering two cell margins.

    Two numbers per column, and the distinction is the whole point:

        WANT   its widest whole cell, one line, no wrapping
        FLOOR  its widest UNBREAKABLE token

    A column may wrap between words: Table 4's middle column is a sentence of
    definition and is supposed to. A column may never break INSIDE a word, which
    is what "Accountabil / ity" and "1,234,5 / 67" were (JL 2026-07-28). So the
    floor is satisfied first and only the slack is shared out toward want.
    Word breaks after a hyphen and a slash, so those end a token here too."""
    want, floor = [1] * ncol, [1] * ncol
    for cells in rows:
        col = 0
        for text, _bold, span in cells:
            if span == 1 and col < ncol:               # a span tells us nothing
                want[col] = max(want[col], text_tw(text) + pad)  # about one column
                for tok in re.split(r"[\s/]|(?<=-)", text):
                    floor[col] = max(floor[col], text_tw(tok) + pad)
            col += span
    if sum(floor) >= total:          # cannot be honoured; scale it down evenly
        w = [max(1, int(x * total / sum(floor))) for x in floor]
    else:
        slack = total - sum(floor)
        head = [max(0, want[i] - floor[i]) for i in range(ncol)]
        w = [floor[i] + (int(slack * head[i] / sum(head)) if sum(head) else
                         slack // ncol) for i in range(ncol)]
    w[w.index(max(w))] += total - sum(w)               # rounding to the widest
    return w

# lanes that are EVIDENCE and become comments; see QC0 on typed lanes
# THE EVIDENCE LANES, and there are exactly three. This is not our list: it is
# the board's own, at haipipe-draft/src/body.py:288, "Typed evidence lanes
# (`> Citation:`, `> Value:`, `> Display:`)". Each one answers "what backs this
# sentence" and resolves against a file: the .bib, a run, a display unit.
EVIDENCE_LANES = ("Value", "Citation", "Display")
# NOT evidence, and they used to be exported as though they were (JL 260727:
# "for the sentences, we might have multiple comments, don't render them to the
# word, only the evidence card"). A `Note` is a PENDING candidate edit, so it is
# a review artifact about prose that has not been accepted. A `Check` is a gate
# REPORT about the section. Neither backs the sentence, and a coauthor reading
# the manuscript should not be handed our unresolved internal queue. They stay
# on the board, where they belong; they are counted on the way out, never
# silently dropped.
WORKING_LANES = ("Note", "Check", "Citation")
# `Citation` is in that list and it looks surprising, so: the CITATION COMMENT IS
# GENERATED, from `.board-refs.bbl`, and carries the reference plus the key. That
# is the evidence card. A hand-written `> Citation:` lane carries something else
# entirely: the `.bib` line number, where the key sits in the tex, a hit count, a
# de-duplication history. All true, all useful on the board, and none of it is
# what a coauthor checks. Merged in, one comment ran to 605 characters for a
# reference of 240 (JL 260727: "Too long, I think we only need: Citation: <the
# reference> key=<the key>"). So the generated half goes to Word and the
# hand-written half stays on the board.
# lanes that are people talking; dropped, same as the LaTeX column
DISCUSSION_LANES = ("JL", "CC", "USER", "Also")
# Content divisions that are the stage's own bookkeeping, not manuscript
# A MANUSCRIPT HEADING IS NUMBERED. That is MISQ's own contract: `1 MAJOR HEAD`,
# `1.1 First Subhead`, `1.1.1 Second Subhead`. So rather than grow a list of
# scaffolding names forever, the test is inverted: a `###` under ## Content is a
# manuscript heading only if it opens with a number, or is one of the few
# unnumbered divisions a manuscript really has. Everything else is working
# structure. Two had already slipped through a name-based list and printed as
# MAJOR HEADS in the export: "(Closing paragraph -- no subsection title)" in §2
# and "Display drafts (markdown-first; NOW FILED as DR requests …)" in §5
# (JL 260727).
# "Title": a Section page may hold the paper title as its own division so it can be reviewed and commented on; the
# build prints the title from paper-build.toml, so the exporters skip it (JL 261115, AITC LOI t01 C0 · Title).
SKIP_DIVISIONS = ("Stage Record", "Stage Contract", "Title")
UNNUMBERED_OK = ("Abstract", "References", "Acknowledgements", "Appendix")


def is_manuscript_heading(title):
    return bool(re.match(r"^\d+(?:\.\d+)*\s", title)) or \
        any(title.startswith(x) for x in UNNUMBERED_OK)

# A structured abstract prints its labels (JL 261021, the JAMA IM Abstract printed seven unlabeled
# paragraphs): on a Page whose head says `section_kind: abstract`, `### Key Points` is a division
# and a `#### <label>` from this list is the bold run-in label of the paragraph under it. Any other
# `####` stays a silent paragraph boundary, so a MISQ abstract's working labels never print.
SECTION_KIND = re.compile(r"(?m)^section_kind:\s*(\S+)\s*$")
ABSTRACT_DIVISIONS = ("Key Points",)
ABSTRACT_LABELS = ("Question", "Findings", "Meaning", "Importance", "Objective", "Objectives",
                   "Design, Setting, and Participants", "Exposure", "Exposures", "Intervention",
                   "Interventions", "Main Outcomes and Measures", "Main Outcome and Measures",
                   "Results", "Conclusions and Relevance", "Trial Registration",
                   # the Lancet journals' structured Summary (five paragraphs, the last one Funding)
                   "Background", "Methods", "Interpretation", "Funding")


def is_abstract_page(raw_page):
    m = SECTION_KIND.search(raw_page.split("\n## ", 1)[0])
    return bool(m) and m.group(1).lower() == "abstract"


def abstract_label(title):
    """`2.1 · Question`, `Question`, or the layout `page.py adopt` writes, `C1.P1 · Question · s1 to s2`
    -> `Question`; None when it is not a label."""
    name = re.sub(r"^\d+(?:\.\d+)*\s*(?:·\s*)?", "", title).strip()
    name = re.sub(r"^C\d+\.P\d+\s*·\s*", "", name)
    name = re.sub(r"\s*·\s*[Ss]\d+[a-z]*(?:\s+to\s+[Ss]\d+[a-z]*)?\s*$", "", name).strip()
    return next((x for x in ABSTRACT_LABELS if x.lower() == name.lower()), None)

NUMTOK = re.compile(r"[+-]?\d[\d,]*(?:\.\d+)?%?")
