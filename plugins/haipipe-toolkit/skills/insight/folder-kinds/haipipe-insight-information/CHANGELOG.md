# haipipe-insight-information · version history


## 2.3.0 · 2026-10-01 · Evidence needs (JL 261001)

- The join is the evidence need: each question binds only its own grouping's files, with the fields its `pass:` names; a run on the topic that lacks them does not fit. GI3 uses `haipipe-insight-check`; the page cites `[QI<n>.E<k>]` and records `results-read:`.

## 2.2.0 · 2026-10-01 · Partition names, not letters (JL 261001)

- Page paths read `<n>-<partition>/I<NN>-<partition>-<slug>/`; cross contrasts named by `cross`; generic task example.

## 2.1.0 · 2026-10-01 · Page tickets (JL 261001)

- An Information answer is its page folder: `runs/` tickets call the task run with `RESULT_DIR` set to the page's `results/<ticket>/` (tables, `metrics.json`, `fig_*.png`); the page's `.md` is the report and embeds the figures. No `_results/` store or `reports/` folder.

## 2.0.0 · 2026-10-01 · Runs and reports (JL 261001)

- An Information answer is a task run in a `j2N_information_<topic>` Job (one run may answer every question its config lists) plus the report that says what the results show. Page Face, PARENTS rows and the Page evidence graph are gone; old boards keep their I pages, frozen.

## 1.3.1 — 2026-09-28 · No content hashes (JL 260928)

- D-row parents are pinned by path and version, never by content hash.

## 1.3.0 — 2026-09-20

- Move the resource owner to `insight/folder-kinds/` and remove Phase metadata.
- Bind actual work to native Run Specs, Tickets, Results and receipts; resource
  updates and GI checks create no synthetic Run.
- Preserve evidence, closure and person-signature boundaries. Migration rules:
  `../../haipipe-insight-workflow/ref/migration.md`.

## 1.1.0 · 2026-09-13

- Replace PageX parent binding with exact Page-version/hash `PARENTS` lineage;
  actual values remain governed by the Page evidence graph.
- Require Page CHECK/CLOSE before GI3 and retire active Probe selection.

## 1.0.2 · 2026-09-01

- Rename optional Execution to Runs and reserve Execute for workflow action.

## 1.0.1 · 2026-09-01

- Rename optional Code to Execution: exact Run/Result pairs define local
  computation; scripts/config are supporting material only when needed.

## 1.0.0 — 2026-08-31

- Renamed to `haipipe-insight-information` and migrated into workflow phase I3.
- Local derivation is now Task-Face work; the reader-facing pattern remains the Page Face.

Recovered from the SKILL.md frontmatter summary on 260827, when the family retired the `summary:` field: version history lives here and is never loaded at invocation.

- 0.2.0 (JL 260823): partition-major home path, and the X contrast page may derive from mirrored I rows (I-from-I across partition groups), the one legal same-rung citation. 0.1.0: derived from named D rows; a rate is Information, a proposition about it is Knowledge.

- 0.2.1 (260828, fieldtest round 3 Fr7): the mint-time Queue-row allocation is the register pen's act, performed by the lap — the old wording put a register write inside a chain-page instruction, against the door's three-pens law.

- 0.3.0 (260828, page-type normalization): gains `## Boundary`, which lifts the never-claim rule out of an outline bullet into the section every sibling contract already had and names this page as the home a COVARIATE routes to, the failure `ref/partition.md` calls misreading covariates as audiences; states the 🟡-final receipt duty this rung has owed since for-question 0.4.0 and the board checker has enforced since; and replaces the copied chain-law block with a CITATION of `haipipe-insight` §The Climb Law, keeping only the I-from-I exception this rung actually owns. Migration: owe-on-next-touch — the new closing check restates a rule already enforced by `partial-final-no-page-receipt`, so no settled page changes state.

- 0.2.2 (260828, round 4 Fr4): provenance in Content names the QA anchor by path, never a bare date code — the attribution rule and the provenance duty stop colliding when the path carries both.
