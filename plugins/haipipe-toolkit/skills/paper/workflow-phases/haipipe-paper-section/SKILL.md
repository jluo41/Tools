---
name: haipipe-paper-section
description: >-
  Paper journey phase P4 (Section) and the Page Type contract for one
  reader-ordered manuscript or appendix Section. It executes exactly one
  current Narrative row, resolves venue-and-kind structure, and binds prose to
  Page-local values, citations, probes, and displays. Use when outlining,
  drafting, revising, checking, or retargeting one paper section.
metadata:
  version: "0.6.0"
  last_updated: "2026-08-31"
  group-token: "S<D> | SA"
  outline:
    mode: resolved
    source: "paper/venue/bank/1-QBv-desks/QBv*/QBv*.md"
    resolver: "cli/resolve-structure.py <QBv page> <section page> · prints structure-source (the bound QBv FILE) and structure-division (its `§<n> Sec-<n>-<Kind>` row)"
    marker: "section-page-template: 1"
    fallback: "paper/workflow-phases/haipipe-paper-section/ref/generic-template.md"
    shape: "current Narrative row overlaid on the resolved venue Sec- division or the explicit generic fallback"
---

# /haipipe-paper-section · execute one Narrative row

Load `haipipe-page`, this Page Type, and `haipipe-page-workflow`. Declare
`page-type: section` and `section_kind: <kind>`.

## 🧭 Journey phase

This skill is journey phase P4 Section (realize) of the paper journey and owns
the `page-type: section` contract below. Enter through gate G5, one page per
Narrative map row. Gate G6 marks the assembled build SUBMISSION-READY versus
DRAFT; assemble itself is a verb, not a phase, and runs anytime from the desk
room. `haipipe-paper-workflow` holds the full gate assertions; this block only
places the phase. The page itself always runs through `/haipipe-page` and
`haipipe-page-workflow` (OUTLINE → … → CHECK), never a private lifecycle.

## 📄 Grain and authority

One Section Page owns one reader-ordered manuscript or appendix unit. Main and
appendix Sections use the same contract; numbering and venue treatment may
differ.

Authority order:

```text
Seed boundary
  → selected Venue rules
  → current Narrative row and version
  → venue × section-kind structure/template
  → landed Page-local evidence
  → current prose
```

Prose never outranks a changed Narrative row or binding desk rule.

## 🏠 Runtime home (0.4.0)

```text
0-paperboard/
├── Ba-<desk1>/            S<D><NN>-<kind>   the desk's main reading order
│                          SA<NN>-<slug>    its appendix sections
│                          RD<NN>-<event>    its rounds live here too (P6)
└── Bb-<desk2>/            a later desk, same shape
```

One B group per desk (journey 0.5.0): the desk's main units, appendix units,
and rounds share the group, so one folder tells one desk's whole downstream
story. Tokens carry the desk letter per the door's group grammar: `S<D>` for
main units, `SA` for appendix sections (Section-Appendix, JL 260831), `<D>` the desk's first distinctive
letter; split Ba1/Ba2 pair groups are grandfathered.

**Where the words live (0.3.1)**: the tex a unit page tracks sits in its
telling's desk room, `<N>-<desk><year>/sections/`, and that room is
self-contained per the door's room law — the unit's `\includegraphics` paths
resolve inside the room's `displays/` (copies of accepted page-local display
units), and its citation keys resolve in the room's own `reference.bib`
(assembled from the consuming pages' `bibex/`). A unit whose tex reaches into
another room, a shared top-level folder, or a page's `display/` directly is a
defect: copy the artifact into the room and name the owning page as
provenance.

Older repos using `1-SC-main/`, `2-SA-appendix/`, the `SC`/`SA` tokens, or a
shared `0-sections/`/`0-display/` are grandfathered and migrate only on
explicit request.

## 📥 Required contract block

Record these fields in the Page before drafting:

```text
narrative-row       id + version
section_kind        abstract · introduction · literature-review · theory ·
                    methods · results · discussion · conclusion · appendix ·
                    venue-specific kind · UNDERSCORE, matching the header key
reader-question     the one question this Section answers
entry-state         what the reader already believes/knows
exit-state          what must be established on exit
claim-ids           exact Narrative claims landing here
venue-allocation    binding desk rules + observed pack guidance, distinguished
structure-source    the bound QBv page FILE, e.g. `paper/venue/bank/1-QBv-desks/
                    QBv1-misq/QBv1-misq.md`, or `ref/generic-template.md`; a
                    path, because `src/plan_shape.py` resolves it on disk
structure-division  the row inside it: `§8 Sec-4-Results` (EXACT), `§7
                    Sec-3-Methods · shared with SM05` (SHARED), or the reason
                    the fallback was taken (ABSENT BY DESIGN · MISSING)
evidence-allowlist  card, citation, value, and display ids
transition-in/out   required joins to neighboring Sections
```

If the Narrative row is missing or stale, stop section drafting and repair the
Narrative first.

## 🧱 Content outline

**Outline mode (also in this file's frontmatter, which the Skill tool strips):**
`mode: resolved` · source = the bound QBv desk division (`structure-source:` +
`structure-division:`, via `cli/resolve-structure.py`) · fallback =
`ref/generic-template.md` · one `## C<n>` per Content division of the page, so a
flat section is `C1` with one paragraph group per move · one bullet per
sentence slot.

Resolve paragraph or move divisions from the QBv Venue Page bound by the
governing Narrative's division 1. **Address the division by grep, never by a
remembered name or number** (0.5.0):

```bash
grep -n '^### [0-9]* · Sec-' <venue-bank>/QBv<n>-<desk>/QBv<n>-<desk>.md
```

The heading is `### <n> · Sec-<n>-<Kind>: <tagline>`, so the token is followed
by a colon and prose; match the token, never the whole line. Its NUMBER moves
between desks: MISQ's abstract is §4, Nature Communications' is §3, and PNAS §3
is Sec-0-Significance with the abstract at §4. Cite the whole address in
`structure-source`, both the number and the `Sec-` token, so a re-read can
prove it.

**`cli/resolve-structure.py` does this and prints the verdict**, so no page has
to trust a remembered mapping:

```bash
python3 <skill>/cli/resolve-structure.py <QBv page>.md <section page>.md
python3 <skill>/cli/resolve-structure.py <QBv page>.md --all <group>/   # a board
```

### The kind-to-token map · not derivable by casing

Two of the nine differ from their kind by more than capitalization, which is
why an agent must read this table and never transform the string itself:

```text
section_kind        Sec- token              note
────────────────────────────────────────────────────────────────────────────
abstract            Sec-0-Abstract
introduction        Sec-1-Introduction
literature-review   Sec-2-Related-Work      ⚠️ different word · absent at MISQ,
                                            present at QBv9/10/12
theory              Sec-2-Theory            shares the number 2 with
                                            Related-Work across desks
methods             Sec-3-Methods
results             Sec-4-Results
discussion          Sec-5-Discussion
conclusion          Sec-6-Conclusion
appendix            Sec-A-Appendix          ⚠️ letter, not a digit
```

Raw pack `style.md` files and stage-era playbook material stay informative: they
may feed a typed PACK OBSERVATION on the QBv page, but they may not become
`structure-source`.

### The kind-to-division map · four relations, not one

`section_kind` does not equal a `Sec-` token, and the mismatch has four
different remedies. Naming only one of them is what made every Section fall
silently to the fallback:

```text
relation            what it looks like                     what to do
──────────────────────────────────────────────────────────────────────────────
EXACT               one kind, one Sec- division            resolve · cite the
                    abstract → Sec-0-Abstract              address
SHARED              one division serves several Pages      resolve · SPLIT the
                    methods → Sec-3-Methods (2 Pages)      division's word and
                    appendix → Sec-A-Appendix (6 Pages)    move budget on the
                                                           Narrative row, never
                                                           give each Page the
                                                           whole budget
ABSENT BY DESIGN    the desk HAS no such unit and the      fallback · record the
                    paper keeps the section anyway         DEVIATION on the
                    literature-review at MISQ              Narrative · do NOT
                                                           raise a QBv gap
MISSING             the desk should have the division      fallback · raise the
                    but the page has not been written      gap on the QBv page
                    8 of 17 desks carry zero Sec- rows     · the desk owes it
```

**The ABSENT BY DESIGN row is the one 0.4.0 lacked.** MISQ publishes no
related-work unit, and a paper may still keep one as a deliberate deviation a
person ruled. Raising that as a gap tells the venue bank to invent a division
the desk does not have, which corrupts a consumer-neutral asset to suit one
paper. The deviation belongs on the Narrative, where the venue decision lives.

**Eight desks resolve to nothing today** (QBv5-jama, QBv7-jama-network-open,
QBv8-npj-digital-medicine, QBv9 partially, QBv11-nature-human-behaviour,
QBv14-diabetes-care, QBv15-grant, QBv16-patent, QBv17-wise carry zero `Sec-`
divisions). For those, `mode: resolved` is aspirational: every Section takes the
generic fallback and the gap is real. Say so in `structure-source` rather than
letting the page read as venue-resolved.

Each Content division states:

```text
reader move
claim ids advanced
evidence/citation/value/display bindings
expected prose or display placement
transition to the next move
known limitation or unresolved obligation
```

**The plan is a list of sentence slots (0.5.3, JL 260831).** One bullet is one
sentence slot, `S<n> · <what the sentence does>` in 4 to 11 plain words;
paragraphs group by move (`### C2.P1 · Problem and question · S1 to S3`); a
finding carries its claim id plus a word (`S6 · C1: +9.34 MME per visit,
comparison owed`); one `Cut:` bullet names what leaves the section and where it
goes; a Note is one line and never the drafted sentence, which lives on the
page. The approved specimen is `SM00-abstract-outline-v3.md` on the MISQ board,
quoted in `haipipe-plugin-outline` §✂️.

## 🃏 Landing evidence in prose

Literature, values, and displays are not separate Page Types. They land through
the Section's Page-local plugins:

```text
pagex/            Probe's accepted-Page lane: bounded source Page context
probe/<card>/     Probe's Task/Discovery QA lane: answer, proof, interpretation
bibex/            citation card and bibliography key used by the sentence
display/<unit>/   intake, recipe, artifacts, caption, bindings, acceptance
```

The value plugin is a storage-less surface over `probe/<card>/card.md` and the
Section prose. Cite one exact number as `PP<NN>.v<n>`; never create `value/` as
a second home.

Every consequential sentence must be one of:

- supported by one or more card/citation/value/display ids;
- explicitly framed as interpretation and bounded by its evidence;
- visibly marked as an open obligation that prevents closure.

One Section may cite many displays, including displays owned by another Page,
but it must record the source unit and accepted version. It may also own several
local displays.

## 🔁 Retargeting

On a venue change:

1. Bind the Section to the new Narrative row.
2. Re-resolve venue × kind structure and hard constraints.
3. Preserve evidence ids whose meaning and scope remain valid.
4. Reopen prose, citations, and displays whose role or placement changed.
5. Compile and CHECK the new built version.

## ✅ Closing checks

- Exactly one current Narrative row governs the Page.
- Reader entry and exit states match neighboring rows.
- Every claim and consequential sentence has inspectable support or an open
  obligation.
- Every citation key resolves; every value has provenance; every cited display
  names an accepted artifact version.
- Venue rules are distinguished from pack observations.
- The generated TeX/PDF/DOCX reflects the accepted Page version.
- CHECK, not prose completion, closes the Section.

## 📏 Measuring the form · `cli/section-stats.py`

A Section's word and paragraph budget comes from the resolved `Sec-` division's
Format values. `cli/section-stats.py` measures what the prose ACTUALLY is and
writes the dated `# --- form:begin (generated) ---` block the pages carry:

```bash
python3 <skill>/cli/section-stats.py <page>.md [--date=YYMMDD] [--sentences]
```

It reads only `## Content` prose under the paper dialect's rules: `###` opens a
subsection, `####` opens a paragraph, the `(…)` line under a `####` is that
paragraph's job and not prose, a `>` line is an apparatus lane, and a `[Q-…]`
bracket is stripped before counting. `--sentences` adds a per-sentence bar; keep
it off except on a one-paragraph unit such as an abstract.

**Never hand-edit a form block.** A form table is wrong the moment one sentence
changes, and a wrong one is worse than none because it reads as measured. The
board's `check.py` reports `generated-block-stale` when the block's date is
older than the page's newest Log row; regenerate, do not retype.

This variant owns `cli/resolve-structure.py`, `cli/section-stats.py` and
`ref/generic-template.md`, the
explicit fallback that keeps every Section kind executable while venue templates
are migrated one by one.
