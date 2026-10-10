# haipipe-insight-knowledge · version history


## 2.4.1 · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## 2.4.0 · 2026-10-01 · Work specs and the page flow (JL 261001)

- The page is a haipipe-page Page written through its flow (plan, Draft, adopt, health, page CHECK by another agent); each need is one Evidence Item carrying `**Need**:`, with no id in the prose. Binding follows each need's work spec exactly; configs list need ids ; a refusal needs a probe run.

## 2.3.0 · 2026-10-01 · Evidence needs (JL 261001)

- A claim computes whenever its question has a compute need (a gain with uncertainty, an adjusted contrast for a named rival, a held-out score, a size); a compute need answered by reasoning is a GAP, never a WEAK claim. Rivals the ask names are compute needs. GI4 uses `haipipe-insight-check`.
- Page shape follows `ref/report.md` § Shape (a Page Face: objective title, the Opening answers, one division per need), replacing the finding-as-headline rule.

## 2.2.0 · 2026-10-01 · Partition names, not letters (JL 261001)

- Page paths read `<n>-<partition>/K<NN>-<partition>-<slug>/` (no partition letters).

## 2.1.0 · 2026-10-01 · Page tickets (JL 261001)

- A Knowledge answer is its page's `.md` (no `reports/` folder); it cites Information pages and its own results. A page that computes calls the task through its own `runs/` ticket into its `results/<ticket>/`; one that reasons only from other pages has no `runs/`. No board `_results/` store.

## 2.0.0 · 2026-10-01 · Runs and reports (JL 261001)

- A Knowledge answer is a report citing named run results and Information reports. The strength rubric and the pooling-verdict rules are unchanged; GI4 passes on a fresh-context check of the report. New rival tests become `j3N_knowledge_<topic>` task runs.

## 1.4.1 — 2026-09-28 · No content hashes (JL 260928)

- I-row parents are pinned by path and version, never by content hash.

## 1.4.0 — 2026-09-20

- Define evidence-bound STRONG/MODERATE/WEAK criteria and required label
  rationale; distinguish unavailable parents from weak support.
- Add `UNDETERMINED` for complete but inconclusive pooling comparisons, and
  require threshold-pinned evidence and an explicit consequence route.
- Migration: existing K rows and POOL/SPLIT records remain historical and
  settled. Apply the rubric and third outcome on next adjudication; do not
  rewrite or force old verdicts.

## 1.3.0 — 2026-09-20

- Move the resource owner to `insight/folder-kinds/` and remove Phase metadata.
- Bind actual work to native Run Specs, Tickets, Results and receipts; resource
  updates and GI checks create no synthetic Run.
- Preserve evidence, closure and person-signature boundaries. Migration rules:
  `../../haipipe-insight-workflow/ref/migration.md`.

## 1.1.0 · 2026-09-13

- Replace PageX parent binding with exact Page-version/hash `PARENTS` lineage;
  new rival evidence uses decided Supporting/local Results.
- Require Page CHECK/CLOSE before GI4.

## 1.0.2 · 2026-09-01

- Rename the optional robustness presenter from Execution to Runs.

## 1.0.1 · 2026-09-01

- Rename the optional robustness capability from Code to Execution; require a
  declared Run/Result pair and treat scripts as optional support.

## 1.0.0 — 2026-08-31

- Renamed to `haipipe-insight-knowledge` and migrated into workflow phase I4.
- Claim adjudication is the Task Face; the bounded proposition is the Page Face.

Recovered from the SKILL.md frontmatter summary on 260827, when the family retired the `summary:` field: version history lives here and is never loaded at invocation.

- 0.2.0 (JL 260823): partition-major home path, and the pooling-verdict K page may cite the heterogeneity K row (K-from-K, one step) since its subject is a claim about claims. 0.1.0: a proposition with strength, rivals and boundary.

- 0.3.0 (260828, page-type normalization): gains `## Boundary`, which lifts the never-advise rule out of an outline bullet into the section every sibling contract already had and restates that a POOL/SPLIT verdict is a claim about exchangeability whose W-page obligations belong to `ref/partition.md`; states the 🟡-final receipt duty this level has owed since for-question 0.4.0 and the board checker has enforced since; and replaces the copied chain-law block with a CITATION of `haipipe-insight` §The Climb Law, keeping only the K-from-K exception this level actually owns. Migration: owe-on-next-touch — the new closing check restates a rule already enforced by `partial-final-no-page-receipt`, so no settled page changes state.

- 0.2.1 (260828, fieldtest round 3 Fr7): the mint-time Queue-row allocation is the register pen's act, performed by the lap — the old wording put a register write inside a chain-page instruction, against the door's three-pens law.
