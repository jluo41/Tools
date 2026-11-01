# haipipe-paper-evidence · changelog

## 0.5.1 · 2026-11-01 · b16 review 261101: current paper names

- version Jobs are named `jNN_writing_v<MMDD>_<desk>` (from j11), no longer `jNN_v<MMDD>_<desk>` (ledger commands, ladder sketch, evidence_ledger.py help and docstring).
- evidence_ledger.py: a display drawn by a Run in the paper Board's own `j01_evidence_display` Job (`paper/Paper-<x>/j01_evidence_display/tNN_/runs/<run>/result`, s01-D13) is a proper source; work/ Runs still count, and a display with no Run is still flagged. Paper-Example-C j11: 10 ❗ to 5 (the five left are reviews not run yet).
- evidence_ledger.py: the display Job check accepts `j01_evidence_display` and still accepts the older `j21_paper_displays`; its warning names both.
- CHANGELOG 0.5.0: the all-displays PDF is `<Board>/delivery/<job>/<job>-all-displays.pdf`.
- Metadata last_updated set from the 0.5.0 entry (2026-11-01) before this bump.

## 0.5.0 · 2026-11-01 · All displays as one PDF

- JL 261101: "I also want a link for the display, so we can view all the displays as one pdf file". New
  `scripts/build_displays_pdf.py <display Job>` writes `<Board>/delivery/<job>/<job>-all-displays.pdf` (xelatex, one page per
  display, "Not drawn yet" where none is); the workbench's Evidence view, now Values, Citations, then Displays, links it.

## 0.4.0 · 2026-10-31 · The display Job moves to the paper Board; three evidence Jobs

- JL 261031: one paper Block links many discovery Blocks (external) and work Blocks (internal), deposits them into its evidence
  Jobs, and writes them into papers. The display Job is `j01_evidence_display` in the paper Board (was the work Block's
  `j21_paper_displays`), beside `j02_evidence_value` and `j03_evidence_cite`; a display Run draws from returned,
  aggregated Results only. The sketch, rule 3 and the colour scheme's path say so.

## [0.3.2] — 2026-10-26

Links, commands and companions repointed at the helper skills merged into `haipipe-ideation`, `haipipe-search`, `haipipe-evidence`, `inlab-human`, `haipipe-draft-review`, `haipipe-display` (now `_parts/<name>/PART.md`). (merge-parts 261026)

## [0.3.1] — 2026-10-26

Shorter description (1754 -> 503 characters): what it does, when to use it, its trigger words; aliases and old command names kept (diagnostics/descriptions/261026.yaml). (describe 261026)

## 0.3.0 · 2026-10-23 · The display Job is j21, and it opens with a display plan

- JL 261023: "for the paper, they will also have a work folder, one work folder to provide the content
  for the paper folder"; "one of the block's job will be the j21_paper_displays"; "this should be a plan, and should be
  proposed to the author to think about how to draw them". The display Job is `j21_paper_displays`
  (`j21_<venue>_displays` with several venues); its face opens with a display plan the authors agree before any
  Run draws; Sections write numbers only after the drawn displays pass review and are accepted.

## 0.2.0 · 2026-10-22 · every display passes the revise loop (JL 261022)

- Rule 3 grows (JL: "display should also have a loop, like the draft is a loop; a display matters as much as the main
  text"): every main-text and eAppendix display passes haipipe-display's `ref/display-revise-loop.md` before the
  version leaves DRAFT; one `colour-scheme.yaml` per paper, in the work Block's display Job; the set is reviewed together once; pass = overall
  >= 8/10 and no dimension under 7, at most 4 rounds; `accepted:` only after a pass. `/haipipe-paper-display` is an
  alias of this skill.
- `evidence_ledger.py` reads each display unit's README `question:` and its latest `review/rNN.md` scores: ❗ for a
  main-text display with no question or no passing review, ⚠️ for an eAppendix one, and the latest score in the
  display listing.
- A paper is a pair (JL 261022: "for the display, it should be in the b03?"; "for /haipipe-paper, we should have a
  paper block and a work block to provide the displays and E-work, right?"): the work Block's display Job
  `jNN_paper_displays` draws every picture (one Task per display, a Run's `result/`), the paper unit only frames
  it, VALUE cards read the same Block, and the version face names it in `work-block:`. The ledger flags ❗ display
  drawn inside the paper when a unit's `intake/manifest.yaml` names no work Run `result/`, one outside the
  `work-block:`, or one not on disk, and ⚠️ when the Run is not in a `*_displays` Job. Three new tests.

## 0.1.1 · 2026-10-20 · the ledger counts VALUE

- haipipe-evidence 0.6.0 renamed WORK to VALUE; `evidence_ledger.py` reads and prints VALUE, and its test writes `kind: value`.

## 0.1.0 · 2026-10-19 · What backs a paper, and one ledger per version

- New skill (JL 261019: "and also have a haipipe-paper-evidence? ... it is like we have the paper to combine the
  evidence and draft together to make a draft task, right?"; then "okay, please go ahead and do it"). A paper Section
  is a draft Task (b32_draft s03, s41-D06): `haipipe-paper-draft` keeps its `draft/`, this skill the paper's rules for
  its `evidence/` and `display/`, on top of the base `haipipe-evidence` and `haipipe-display`.
- The rules: citations from verified CITE Results, never `bank.bib`; one result, one number, one Run in every Section;
  displays numbered for the paper and within the venue's limit; claim words fit the design; every consequential
  sentence backed, framed as interpretation, or an open need. "Landing evidence in prose" moved here from
  haipipe-paper-section (now haipipe-paper-draft 0.13.0).
- `scripts/evidence_ledger.py <version Job>`: every Section of one version side by side, read from
  `evidence/cards.yaml` or an older Page's Evidence Items (haipipe-draft's `item_table`); flags one value read from
  two Runs, one label with different estimates compared in one unit (a copy with the same estimates is a ⚠️), one
  citation key with two entries, too many displays, a display shown twice, and cards that do not resolve; only the
  Sections in the version's compile order count. Changes no file of the paper; exit 1 on a ❗. 8 tests on a made-up
  version.
- Tested by a fresh agent on Paper-Example-Misq `j01_v0929_misq` (asked only to check the numbers
  before a send; it found haipipe-paper, then this skill). Its review made the ledger read the compile order, compare
  estimates in one unit, and check citation keys, and took a worked answer out of this SKILL.md so it no longer leads
  the reader. The ledger now finds what it found in the files it reads: Metformin's two estimates (3.75e-05 against
  −0.07 percentage points), `american20239` as 2024 and 2023, HighDose as a copy, 16 citations not verified. Numbers
  typed into table bodies (Table 4's 12.63 against Table D1's 12.90) and wording are not read yet.
