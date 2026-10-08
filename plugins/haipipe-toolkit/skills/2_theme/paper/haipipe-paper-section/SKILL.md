---
name: haipipe-paper-section
description: >-
  The Paper Section PageType contract for one
  reader-ordered manuscript or appendix Section, the Abstract or a letter: a
  Page Task t0N_ · t2N_ · t3N_ in its version. It executes exactly one row of
  its version face's ## Narrative, resolves venue-and-kind structure, keeps its
  Requirement (venue and Page rules, the rubric, the SUB-* rows), and binds prose
  to typed Page-local Evidence Item Results. Use when adding, outlining,
  drafting, revising, checking, or retargeting one paper section.
metadata:
  version: "0.11.0"
  last_updated: "2026-10-07"
  page_ruling: none
  group-token: "t0N_<title> | t2N_<title> (legacy S-<desk>-Main-<Title> | S-<desk>-Appendix-<Title>)"
  outline:
    mode: resolved
    source: "2_theme/paper/venue/bank/1-QBv-desks/QBv*/QBv*.md"
    resolver: "cli/resolve-structure.py <QBv page> <section page> · prints structure-source (the bound QBv FILE) and structure-division (its `§<n> Sec-<n>-<Kind>` row)"
    marker: "section-page-template: 1"
    fallback: "paper/haipipe-paper-section/ref/generic-template.md"
    shape: "current Story Section Narrative row overlaid on the resolved venue Sec- division or the explicit generic fallback"
---

# /haipipe-paper-section · execute one Story Section Narrative row

> ⛔ **Generated files: never modify them directly; change the code that writes them (or its source), then rerun it** (hard rule, JL 260928; AGENTS.md rule 6). Here that means the Section's `delivery/latex/` and `delivery/word/` files: fix the Page, its Draft or the exporter, then rebuild.

For a Section Page update, load `haipipe-page`, `haipipe-page-workflow`, the
current Run Workflow/Spec owner, `haipipe-paper-workflow`, this PageType and
its relevant references in the shared set order. Read
`../haipipe-paper/ref/page-integration.md` when planning a Run or release.
Reading a proposed handoff alone allocates no Run.

Declare `page-type: section` and `section_kind: <kind>`.
Reading this contract for a prospective Story handoff does not start a Run.
Proposed bindings may remain unresolved until the relevant owner supplies them;
do not invent Page paths, accepted Results, or a release to complete a proposal.

## Paper ownership and entry

This skill owns the Paper Section Page and its `page-type: section` contract below. Enter through gate G3, one page per
row of its version face's `## Narrative` (an older Board's Story §8), each row released by a person independently
(the Release a Section card). A new Section is made by `haipipe-paper/scripts/paper_ladder.py task <version>
t0N_<title>` (the Add a Section card), with its reader-contract header and its own `studio/` and `reports/`.
Gate G4 marks the assembled build SUBMISSION-READY versus DRAFT; assemble
is a separately commissioned build, and runs anytime from `delivery/` on the Story's
compile-order block. `haipipe-paper-workflow` holds the full gate assertions; this block only
binds the Page owner. The page itself always runs through `/haipipe-page` and
`haipipe-page-workflow` (CONTEXT → OUTLINE ⇄ EVIDENCE → CONTENT → CHECK),
never a private lifecycle.

## 📄 Grain and authority

One Section Page owns one reader-ordered manuscript or appendix unit. Main and
appendix Sections use the same contract; numbering and venue treatment may
differ.

Authority order:

```text
Story Seed divisions (§1–§5: identity and evidence boundaries)
  → selected Venue rules
  → its row in the version face's ## Narrative (an older Board: the Story §8 row and Story version)
  → venue × section-kind structure/template
  → landed Page-local evidence
  → current prose
```

Prose never outranks a changed Section Narrative row or binding desk rule.

## 📏 Requirement (b16 s13, JL 261007)

Description › Requirement is its own tab: the rules the Section is written to and the rubric it is judged by, read
from three places and copied from none. Read [`ref/requirement.md`](ref/requirement.md).

## 🚪 Opening stays with the reader

The rendered Section Opening is exactly one paragraph: the question and the
minimum orientation needed to enter the manuscript unit. It has no reader
drawer. Page-owned prose rules live in
`draft/records/<stem>-requirement.md` as authored `W<n>` records with `Rule`,
`Applies`, and `Source`, after the generated venue `V<n>` block. The Outline
workbench exposes both through one `📏 Requirement` lens for CONTEXT, OUTLINE,
CONTENT, and CHECK. A Section Page carries no `### Writing Style` block.
Post-paragraph notes and `## Stage Contract` remain source-side and do not
render on the manuscript review surface. This keeps writer instructions out
of the paper reading path without deleting their authority.

## 🏠 Runtime home (0.4.0)

```text
Paper-<Slug>/
└── j01_v<MMDD>_<desk>/      one version: one send to one venue, named for the day it is sent (0.10.0)
    ├── t00_abstract/        the Abstract
    ├── t0N_<title>/         a Main Section, in reading order (t01-t19) · N = the H1's §N
    ├── t2N_<title>/         an Appendix Section, A = t21 (t20-t29) · its letter = the H1's Appendix L
    ├── t3N_<title>/         a letter (t30-t39): t31_cover-letter · t32_response; section_kind: letter
    └── reports/qNN_<kind>-<MMDD>/   a comments batch: a report of type comments, never a Task
```

Each Section Task holds, beside its face and the Page workflow's `draft/`, `runs/`, `results/` and `delivery/`, its
own `studio/sNN-<topic>/` (its drawings: the logic by hand, the Section map) and `reports/qNN_<topic>/` (the
discussion questions kept while it is changed, each a row in the face's `## Questions`, shown in Audience Report ›
Questions as Question │ Work │ Report). Both start empty (b16 s13, JL 261007).

A Section is a Task of its version, named by series (JL 261007: "no more S-xxx"): the number band says the
part (Main, Appendix, letters), the title is lowercase-kebab and says the page job, and the version folder
carries the desk. The older layout, `Ba-<desk>-Main/S-<desk>-Main-<N>-<Title>`, `Bb-<desk>-Appendix/
S-<desk>-Appendix-<L>-<Title>` and `Bc-<desk>-Round/RD<NN>-<event>`, stays readable;
`haipipe-paper/scripts/carry_over/rename_tasks.py` moves a version to the series names once, with a record. The version
face's compile-order block supplies manuscript order; `board.md` is the Page roster.
A Section is never renamed merely because another
section is inserted: the new one takes a free number in its band, and the version's compile order, not the
number, decides where it prints.

## ⚙️ Paper Section Run profile

Read [`../haipipe-paper/ref/run-naming.md`](../haipipe-paper/ref/run-naming.md)
and the shared Page Run names. New local Evidence uses full names such as
`run-citation-<slug>` or `run-value-<slug>`.
The Page owns the Evidence Item; the selected Task/Display worker does not
change that owner. Independent Supporting Runs keep their native Task or
Discovery identity and full path.

Human interaction uses a `run-structure-…` Run for SHAPE + SURVEY, then the
selected `run-section-…` or `run-paragraph-…` session. Feedback is a Step; same-target
reopening is a Version. Record the semantic `page:` and `paper_lane:` alongside
the native receipt. Older short names are retired; a reused Result keeps its
exact original path, and its owner and receipt are verified before reuse. Evidence acceptance never replaces human writing
acceptance. The Paper Workflow's `structure/write/evidence/deliver` Specs bind
these native Runs, without a wrapper Section Run.

**Where the words live (0.8.4 · JL 260907)**: on this page. The Section Page
compiles its own deliverable through the page-level delivery workbench,
`delivery/latex/<page>-master.tex` compiled to `<page>.pdf`, with its Bib at `selected-bibliography/<page>.bib`,
wrapping the body fragment `delivery/latex/<page>.tex` that the paper build
`\input`s; its `\includegraphics` paths resolve to its own accepted display units
(`results/<re-run>/payload/Display<n>-<slug>/assets/figure.pdf`; the stable Page id
owns the unit independently of printed section order; `S-Display-*`, `<PageID>-Display-*` and `Sec<N>-Display-*` are
retired, JL 260908) and its citation keys to
its own `selected-bibliography/<page>.bib`. The paper's `delivery/latex/` is regenerated FROM these
files by `haipipe-paper-assemble`, never the other way round: a correction goes
into this page and the paper folder is rebuilt whole. The old desk room
(`<N>-<desk><year>/sections/*.tex`) is not a current source of record.

**Mechanical assembly milestone**: this Page can supply a fragment to a draft
build when three things exist: the current outline table is explicitly approved
(`draft/<page>-draft-v*.md`, ticked), every display unit has its
`preview.pdf`, and the page PDF compiles under `delivery/latex/`. A page
missing any of the three is not ready, and the paper build says so.
Those files do not make the Section DONE. Only current Page CHECK closure under
the Section contract and accepted evidence bindings closes it; paper-level G4
and the human submission decision remain separate. Follow
`haipipe-paper-assemble` for exact-version admission and manifest checks.

## 📥 Required contract block

Record these fields in the Page before drafting:

```text
story-row           <version> ## Narrative / <stem> (an older Board: Story<Letter>-<desk>-<idea-slug> §8 / <section-id>
                    + the Story version); resolve the actual row
section_kind        abstract · introduction · literature-review · theory ·
                    methods · results · discussion · conclusion · appendix ·
                    venue-specific kind · UNDERSCORE, matching the header key
reader-question     the one question this Section answers
entry-state         what the reader already believes/knows
exit-state          what must be established on exit
claim-ids           exact Story claim / E ids from the row
venue-allocation    binding desk rules + observed pack guidance, distinguished
structure-source    the bound QBv page FILE, e.g. `paper/venue/bank/1-QBv-desks/
                    QBv1-misq/QBv1-misq.md`, or `ref/generic-template.md`; a
                    path, because `src/plan_shape.py` resolves it on disk
structure-division  the row inside it: `§8 Sec-4-Results` (EXACT), `§7
                    Sec-3-Methods · shared with another named Section` (SHARED), or the reason
                    the fallback was taken (ABSENT BY DESIGN · MISSING)
evidence-allowlist  typed Evidence Item ids and accepted local Result ids
transition-in/out   required joins to neighboring Sections
```

If the Section Narrative row is missing or stale, CONTEXT records its exact
source and returns `HOLD` to `haipipe-paper-story`, the owner of the Story page
and its §8 narrative and detailed Section rows. If Venue
authority is missing or stale, it returns `HOLD` to
`haipipe-paper-venue`, the owning QBv bank Page Type; Venue is a shared reference library. After the exact owner repairs and versions the source, the
Section resumes at CONTEXT/PREPARE. Section work never repairs upstream
Story or Venue policy itself.

## 🧱 Content outline

**Outline mode (also in this file's frontmatter, which the Skill tool strips):**
`mode: resolved` · source = the bound QBv desk division (`structure-source:` +
`structure-division:`, via `cli/resolve-structure.py`) · fallback =
`ref/generic-template.md` · one `## C<n>` per Content division of the page, so a
flat section is `C1` with one paragraph group per move · one bullet per
sentence slot.

Resolve paragraph or move divisions from the QBv Venue Page named by the
governing Story §8 row's `target` column. **Address the division by grep, never by a
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
                                                           Story §8 row, never
                                                           give each Page the
                                                           whole budget
ABSENT BY DESIGN    the desk HAS no such unit and the      fallback · record the
                    paper keeps the section anyway         DEVIATION on the
                    literature-review at MISQ              Story §8 row · do NOT
                                                           raise a QBv gap
MISSING             the desk should have the division      fallback · raise the
                    but the page has not been written      gap on the QBv page
                    8 of 17 desks carry zero Sec- rows     · the desk owes it
```

**The ABSENT BY DESIGN row is the one 0.4.0 lacked.** MISQ publishes no
related-work unit, and a paper may still keep one as a deliberate deviation a
person ruled. Raising that as a gap tells the venue bank to invent a division
the desk does not have, which corrupts a consumer-neutral asset to suit one
paper. The deviation belongs on the Story's §8 row, where the target decision lives.

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
known limitation or unresolved need
```

**The plan is a list of sentence slots (0.5.3, JL 260831).** One bullet is one
sentence slot, `S<n> · <what the sentence does>` in 4 to 11 plain words;
paragraphs group by move (`### C2.P1 · Problem and question · S1 to S3`); a
finding carries its claim id plus a word (`S6 · C1: <the number and its unit>,
comparison owed`); one `Cut:` bullet names what leaves the section and where it
goes; a Note is one line and never the drafted sentence, which lives on the
page. The approved specimen is quoted in `workbench-page` §✂️.

## 🏷 Reader-facing subsection titles

During SHAPE and CONTENT revision, name each subsection for the substantive
subject or relationship its paragraphs develop. A reader scanning the titles
should recognize the actors, constructs, decisions, or contexts being studied
without knowing the planning vocabulary.

- Prefer concrete, concise noun phrases with parallel grammatical form across
  peer subsections. Preserve defined construct names and the venue's casing;
  do not shorten a title by changing the construct or making a stronger claim.
- Distinguish a reader-facing title from a paragraph job. `Resolve the rivalry`
  describes the writer's task; `Patient-Request Pressure and Physician
  Accommodation` names the subject. `Boundary tests and integrated model`
  is too generic when the actual subject is prescribing across clinical contexts.
  These examples illustrate the distinction, not a required outline or phrase list.
- Check title-to-body fit: the title covers the whole subsection, distinguishes
  it from its neighbors, and promises no unmeasured mediation, demonstrated
  causality, or material absent from its paragraphs. `Boundary`, `model`, and
  `competing predictions` are legitimate terms when they identify the actual
  subject; they are not banned words.
- Read the ordered titles alone, then inspect the corresponding paragraphs.
  Revise a vague title; do not reorganize an approved argument merely to fit
  a more attractive label. A genuine scope/order/claim change returns to SHAPE.
- For an authorized title-only clarification, synchronize the current Outline
  division, Page Content heading, and matching Aim heading; regenerate the
  Board and declared delivery and inspect both. Preserve historical plans and
  completed Run inputs. Apply the plan grammar's version rule: a mechanical
  relabeling with unchanged scope, order, Bullets, and evidence need not consume
  a version; record the rationale instead of disguising a Shape change as wording.

## 🃏 Landing evidence in prose

Literature, values, citations, and displays are typed Evidence Items, not
separate Page Types or workbenches. The Section uses the same Outline workbench as the
other Page Runs:

```text
Context Workspace    Story Section Narrative row, Venue, requirements, and bounded related links
Bullet Workspace     sentence slots and their Evidence Item ids
Evidence Workspace   Supporting Runs → Local Input → Local Run → typed Result
```

Cross-Folder material enters through an Execution or Discovery Supporting Run
Result. LAND freezes those Results into one Local Input and produces one local
`VALUE`, `CITE`, or `DISPLAY` Result for the focal item. EMBED binds that local
Result to its Bullet before CONTENT writes prose. There is no active PageX,
legacy evidence, bibex, value, or display workbench in this contract; old lanes are
migration-only input.

Every consequential sentence must be one of:

- supported by one or more typed Evidence Item and accepted local Result ids;
- explicitly framed as interpretation and bounded by its evidence;
- visibly marked as an open need that prevents closure.

One Section may cite many displays. A display owned elsewhere must arrive
through a named Supporting Run Result; the Section's local DISPLAY Result
records that source and accepted version. A Section may also create several
local display items, one typed contract and local Run per item.

## 🔁 Retargeting

On a venue change:

1. Bind the Section to the new Story Section Narrative row.
2. Re-resolve venue × kind structure and hard constraints.
3. Preserve Evidence Item/Result ids whose meaning and scope remain valid.
4. Return changed item meaning to OUTLINE/SHAPE, changed Run design to
   OUTLINE/SURVEY, and stale Results to EVIDENCE/LAND.
5. Run CONTENT/WRITE and CHECK the new built version.

## ✅ Closing checks

- Exactly one current Story Section Narrative row governs the Page.
- Reader entry and exit states match neighboring rows.
- Every claim and consequential sentence has inspectable support or an open
  need.
- Every citation key resolves; every value has provenance; every cited display
  names an accepted artifact version.
- Venue rules are distinguished from pack observations.
- The generated TeX/PDF/DOCX reflects the accepted Page version.
- CHECK, not prose completion, closes the Section.

`page_ruling: none` is explicit for the per-Section Page. CHECK may close one
unit when its Section contract and artifact-specific gates pass. Paper gate G4
is separate and non-circular: it waits until every mapped Section is closed,
then governs whether the assembled paper is SUBMISSION-READY and receives the
paper-level human decision.

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
