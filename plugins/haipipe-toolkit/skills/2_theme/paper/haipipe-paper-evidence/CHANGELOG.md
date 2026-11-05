# haipipe-paper-evidence · changelog

## 0.13.0 · 2026-11-04 · a display's PDF ends with its earlier versions

- JL 261104: "add the previous old versions at the bottom of the pdfs". `preview_display.py` passes the Task's lower-numbered Runs to `build_preview.py`, one page each after the method. New rule: new data or a new look means a new Run, with a `change:` line on its card; never delete a display Run's `result/` to redraw it.

## 0.12.1 · 2026-11-04 · a pending value may wait for its Run

- Reported by Paper-PersonalityPDMPMandate: `pending:` crashed when the Run's result file did not exist yet. `catalog` now gives an empty, unlinked value; with no `pending`, a missing file stays an error.

## 0.12.0 · 2026-11-04 · the Values tabs are the paper Board standard

- JL 261104 ("you do it"; ScalingGlucose r04_collect_values_tables, s03-D09): `scripts/build_tables.py` moved here from that
  Board's t08, with no Run name written in it (the newest Run holding the file) and the column words in `tables.yaml`.
  SKILL.md "The Values tabs" has the rules and config; example: Paper-Example `t02_raw-value-tables`. The cell's Sections
  line now reads the Sections. Rerunning ScalingGlucose t08 gave the same tabs.

## 0.11.0 · 2026-11-04 · the venue's caption limit, from call.md

- JL 261104 on r03_collect_caption_style: "let's follow the venue". `caption_check.py` reads `at most N words` from the caption
  row of the Board's `venues/<venue>/call.md`, so paper_check's V10 uses it too; 75 stays the default when a venue says nothing.

## 0.10.0 · 2026-11-04 · the message is checked per display

- JL 261104: "把这个加 message 也写到对应的 skill 里好吧 当做一个 checklist". V6 only counted messages across the paper, and
  all eight ScalingGlucose previews still said "No message written yet". V6 now says when and how a message is written (with
  the display, in the same Run; plain words, the finding, no numbers), and `scripts/caption_check.py` names each display with
  no `## Message` or more than 3 sentences, and exits 1.

## 0.9.0 · 2026-11-03 · the checklist holds the caption rule

- JL 261103: "add the checklist or the rules, that for the Figure caption, do not add so much things, don't be too
  long." The 75-word rule sat only in haipipe-display's revise loop, unchecked, and ScalingGlucose's eight captions ran
  98 to 187 words. The display checklist gains V10 short caption, and `scripts/caption_check.py` counts each display
  Task's newest float.tex: title at most 15 words, legend at most 75 (a table's 120).

## 0.8.0 · 2026-11-03 · the display checklist

- JL 261103: "please update the /haipipe-paper-display's checklist"; "for the preview pdf, I think the first section
  should be: what we want to say with this display". SKILL.md gains The display checklist: planned (P9), drawn (V2),
  its message (V6), examples (V7), questions (V8), reviewed (V5), accepted (V9), the order a display is made and the
  order the Displays view shows (1 Plan, 2 Displays, 3 Examples, 4 Interaction). preview.pdf's page 2 opens with the
  message (haipipe-display 0.8.0).

## 0.7.1 · 2026-11-03 · the ledger leads with the value's name

- JL 261103, of the MISQ ledger: "I think the first column should be the name, right? do we have the name for each
  value?". Every value has one, its value map's `what:` (owed rows too). `values.html` now reads Value name (its ID
  under it) · Where · Printed · Value · Status · Source and key; the Source column keeps the Run chain and the key.
  Fixed column widths, so the table fits a workbench frame, and Where keeps its words whole. Checked in Chrome on
  Paper-Example's Evidence view.
- A /haipipe-ui walk at 390 px: the six columns piled up. On a phone each row is now a small card (the name, then
  Where · Printed · Value · Status on one line, then the Source); the status word never breaks.
- pp-LBP-JAMA 261103: `build_displays_pdf.py` showed a Task's newest alternative, not the face's `printed:` version
  (JAMA t05 prints r07, the PDF showed r08). It now reads workbench-paper `board_evidence.display_pick`, the same rule
  the Evidence view uses, and prints page 1 of that version's preview.pdf, the display as the paper prints it.

## 0.7.0 · 2026-11-03 · the value Job and the citation Job, standard for every paper

- JL 261103 via the two paper sessions: the value and citation evidence pattern (the MISQ and JAMA papers wrote their
  own scripts) is part of this skill, and the two value ledgers are one engine ("how do you think you can unify them
  together"). New `scripts/values_ledger.py` (run · check · bind): a catalog from each value Task's
  `scripts/value_map.yaml` (ids `<RQ>-<tNN>-<nnn>`, `checks:` lineage from the work Run's values.csv `source`),
  bindings as VALUE card items seeded by the search into `evidence/proposals.md` and adopted once ticked, and the check
  (match, differs, missing, no anchor, owed, pending, stale, found) with the values never printed and, paper-wide, the
  numbers printed with no binding. values.html in the MISQ ledger look. The generic parts (status, rounding, lineage,
  proposals) are haipipe-evidence `cards.py` 0.9.0, imported, not written twice.
- New `gen_value_runs.py` (a j02's Run cards, tickets and `t99_paper_value_check` from its maps), `cite_tasks.py` (a
  j03's claim groups `scripts/claim_group.yaml`: gen, run, apply, inventory; the MISQ paper's script made generic) and
  `paper_text.py` (writing Job, printed Sections, both sentence shapes, display rows, workbench links).
- `evidence_ledger.py`: a printed value with no Run, from a screen read, or whose binding differs, is missing or is
  stale is a ❗; owed values count as open.
- The SKILL says the standard shape of j02 and j03 and the migration order: MISQ first (its bindings are the
  regression test), then JAMA (bindings seeded by the search). Neither paper is migrated here.
- Tools' Paper-Example gains a value map, a claim group, Section sentences and a drawn Display B, fed by the placeholder
  work Block `work/b90_example_paper_results`. `tests/test_values_ledger.py` covers every status on it;
  `test_evidence_ledger.py`'s old "names no work Run" wording follows 0.5.1's message.

## 0.6.3 · 2026-11-03 · a generated preview links its addresses

- A script that writes an HTML preview (values.html, citations.html) links each Run address and Section name through
  the shared `servers/workbench/address_links.py` (`page_linker`), never its own copy (JL 261103: "b52.j01.t01.r01
  <--- how could you make this to be clickable").

## 0.6.2 · 2026-11-01 · the venue's display limit, the display plan's numbers

- `evidence_ledger.py` takes the venue's main display limit from `venues/<venue>/call.md` `## Displays` when no
  `--max-displays` is given (JL 261101: "the display ... should also follow the venue").
- The pool is seeded from haipipe-paper-plan's `s06-paper-displays`; the Evidence tab reads `Display A → Figure 1`.

## 0.6.1 · 2026-11-01 · page 1 as the paper prints it; each display's name and type

- New `scripts/preview_display.py <unit>`: page 1 of a display's `preview.pdf` uses the paper's own built head
  (the unit's writing Job, else the newest built one, else the paper's default look), through haipipe-display's
  `build_preview.py --preamble-from`.
- A display face's `name:` and `type:` lines show in Report › Evidence › Displays as "📈 Figure · <name>"; a face
  without `name:` gives the title after "Display X," in its first line, else the folder's words.

## 0.6.0 · 2026-11-01 · each display version: one preview.pdf

- JL 261101: a display version's `preview.pdf` is page 1 the display with its caption, pages 2 on how it was made
  (`method.md`: Data, Sample, Method, Outcomes, Made by, Numbers), built by haipipe-display's `scripts/build_preview.py`.
  The workbench's Evidence view shows it, both pages, instead of the bare picture.
- Rule 2 names the Board's `j02_evidence_value` beside `j01_evidence_display` (the work Block's old Job names as history).

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
