# haipipe-paper-evidence · changelog

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
- Tested by a fresh agent on Paper-AgreeablePrescriptionDiscretion `j01_v0929_misq` (asked only to check the numbers
  before a send; it found haipipe-paper, then this skill). Its review made the ledger read the compile order, compare
  estimates in one unit, and check citation keys, and took a worked answer out of this SKILL.md so it no longer leads
  the reader. The ledger now finds what it found in the files it reads: Metformin's two estimates (3.75e-05 against
  −0.07 percentage points), `american20239` as 2024 and 2023, HighDose as a copy, 16 citations not verified. Numbers
  typed into table bodies (Table 4's 12.63 against Table D1's 12.90) and wording are not read yet.
