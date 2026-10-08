## 1.2.0 · 2026-10-07 · Its runner: review_items.py (b16 Q05)

- New `scripts/review_items.py <board> add | route | reply | rollback` (with `--dry-run`), the runner of the run cards Add comments, Route an item and Reply to an item. `add` was `version_paper.py comments`. `route` and `reply` edit one row of a report's `## Review Items` table; nothing is written into a Section's folder. Tested in the paper family's `tests/test_paper_ladder.py`, rollback included.
- "Add a review" is "Add comments": the workbench table's check reads "review" as a judging run.
- `review_items.py add` writes `responds-to:` on the version face (not `answers:`, which names Question ids, haipipe-report) and `answers: Q<NN>` + `answer-status: open` on the comments report, so `check_report.py` reads both levels clean.

## 1.1.0 · 2026-10-07 · A batch is a report of type comments

- A comments batch lives in its level's `reports/` as `qNN_<kind>-<MMDD>/`, numbered with the other reports, its face declaring `page-type: comments` and its row in `## Questions` with group `comments` (JL 261007: "comments … are a special type of report … it should be in the reports/ but you can say its type is the Comments"). A review batch sits in the version that answers it; a meeting or advisor batch in the Board's `reports/`. It is never a Task: `t3N_` is for letters (t31 cover letter, t32 response). Replaces the 1.0.0 placements (`comments/` on the Board, and a `t3N_` Task inside a version); today's desk shelves are still read.

## 1.0.0 · 2026-10-07 · Renamed from haipipe-paper-round: comments from anyone

- The skill is `haipipe-paper-comments` (was `haipipe-paper-round`; JL 261007: "we do not need to keep the round anymore … change it to the comments"). New Pages declare `page-type: comments` and take the token `CM<NN>`; existing `RD<NN>` Pages and `page-type: round` are read as review batches, unchanged. Entries below keep the old name.
- One batch takes any source: review · editor · coauthor · meeting · advisor · internal. A batch about a send sits on the desk's shelf (its `B<x>-<desk>-Round/` name kept until the ladder move); a batch about the Story sits in the Board's `comments/`.
- Points keep ids by source (`R<n>.<k>` · `E` · `A` · `M` · `V`); Review Items (0.10.0) are role 3; Proposed Questions are role 8: a point any reader would raise again becomes a proposed Board question in Related Questions, adopted by a person.
- Designed in Tools/designs/b16_theme_paper/studio/s22-paper-comments/.

## 0.10.0 · 2026-10-07 · Review Items

- A Round Page keeps a `## Review Items` table beside its concern table: `item | cites | lands on | work | reply | state` (JL 261007: "ok, good to go"). An item, `Review-<slug>`, is one concern answered once; it cites the concern ids it answers (`R1.1 · R1.3 · E1.2`), and each concern names its item in a new `review item` field. States are the concern states. The paper workbench reads the table: a version's Comments view, each Section's Reviews view.
- Proposed next, not applied: the skill becomes `haipipe-paper-comments` (any source: review, meeting, coauthor, advisor), drafted in Tools/designs/b16_theme_paper/studio/s22-paper-comments/.

## 0.9.0 · 2026-09-30 · The concern table

- "Feedback Coverage Ledger" is now **Feedback Concern Table**, and every "ledger" in this contract is the concern table (JL 260930, "go ahead and update them accordingly", on aligning the paper skills with the Paper Workbench; AGENTS rule 9 bans "ledger"). The shape is not matched exactly, so Round Pages that still title the division the old way pass; they take the new title on their next revision.
- Story parts are §N or their name, never C5-C8 (haipipe-paper-story 0.17.0).

## 0.8.1 · 2026-09-29 · outline/ to draft/ in current-layout prose (JL 260929)

- Paths that describe the current Page layout say `draft/`: the plan `draft/<stem>-draft-v<G>.<S>[.<E>].md`, records `draft/records/`, `draft/previous/`, `draft/skill/`, the Evidence Markdown `draft/<stem>-evidence-items.md`, `draft/evidence/bibex/` and `draft/evidence/materials/` (JL 260929: "it should be draft"). Mentions of legacy Pages, retired `outline/evidence/` lanes and the migration keep `outline/`, as do the OUTLINE stage, the Outline table and the `outline:` grammar key.

## 0.8.0 · 2026-09-29 · A submission Round carries the cover letter
- A submission Round's Content holds a `### Cover letter` division (words approved like any page); run-delivery-coverletter in haipipe-paper-assemble 0.9.0 builds it and `send` freezes it with the manuscript. First used by Paper-AgreeablePrescriptionDiscretion `RD02-MISQ-submission-20260929`.

## 0.7.4 · 2026-09-28 · No content hashes (JL 260928)

- A Round records each `sent/` and `released/` snapshot by path and its `build-manifest.json` `built` time, not a manifest hash; CHECK verifies snapshot builds, and received feedback is inventoried with received dates.

## 0.7.3 · 2026-09-20

- Define Round-local blocking/material/editorial severity anchors and preserve source severity separately.
- Describe shared Page lifecycle labels as controller Steps, not extra Runs.

## 0.7.2 · 2026-09-20

- Separate RD Round Pages, controller rounds and writing Versions. Define commissioned response Runs, pending answer identity, owner-routed repairs, matching human release approval and final freeze/CHECK ordering; concern-table triage creates no evidence Run.

## 0.7.1 · 2026-09-13

- Clarify that the Round's Outline is a generated Page projection and must not
  be authored as a second `## Outline` section.

## 0.7.0 · 2026-09-08

- Round is explicitly a Page-level feedback control surface, not a Run or an
  Evidence/Execution owner; new evidence routes to Story §5/§6/§7 and the
  external Discovery/Task/Run owners.
- `RD<NN>` remains the paper-wide unique Round token. The new Page
  stem is `RD<NN>-<desk>-<event>-<YYYYMMDD>`, aligned with the desk's Main and
  Appendix naming style; `R` and `RR` are not aliases.
- The Page surface is fixed as `Opening → Outline → Content → Aims`, with the
  seven Round roles inside Content. `Discussion`, `Files`, `States`, and `Log`
  are outline records, not on-page sections.
- An external response package has one immutable `response/` home beside the
  manuscript snapshots; internal Rounds record `no external response required`
  and omit that directory.
- “Routed exactly once” now means one atomic concern row and one route decision;
  one decision may name a primary Page plus linked Story updates. `applied` is
  non-terminal until the response is `answered`, and G5 records approver
  identity and timestamp.
- `sent/` and `released/` freeze the complete declared delivery output set,
  including supplements, manifest, and display register; they are immutable.

## 0.6.1 · 2026-09-08

- Keep `RD<NN>` as the Round Page token. The earlier Round-local
  `pr-…` suggestion is superseded by 0.7.0: Round does not mint Runs.

## 0.6.0 · 260907

- Journey position P5 → P4, close gate G7 → G5 (haipipe-paper-workflow 1.0.0).
- Routes point at the Story: new evidence → the Story's §6 Evidence Board and a
  §6.4 work row; contribution/order → a Story §8 Section Control row; the
  identity block's `narrative` field becomes `story` (old name read as alias).
  Written by Claude Peer.

## 0.5.0 · 260907
- A Round begins with a delivery and ends with one (JL 260907): `sent/` (the
  PDF+DOCX that drew the comments), `feedback/` (what came back; was `files/`),
  `released/` (the PDF+DOCX with every concern answered). Roles 1 and 7 name
  them with manifest hashes. Path at the paper root, no `0-paperboard/`.

## 0.4.1 · 260831
- Runtime home is the desk's -Round group (JL 260831); combined B<x>-<desk> and lone C1-RD-round grandfathered.

## 0.4.0 — 2026-08-31

- **Renamed and moved** (JL 260831: "replace page-types to be workflow-phases"):
  `paper/page-types/haipipe-page-for-round/` is now `paper/workflow-phases/haipipe-paper-round/`.
  The skill is one paper JOURNEY PHASE and still owns its `page-type:` key;
  a new `## 🧭 Journey phase` block places the phase and its gates, and the
  description carries the P-number. Contract body unchanged.

## 0.3.0 — 2026-08-24

- **Rounds live in their desk's B group** (JL 260824, journey 0.5.0 P5-P6
  mapping): `B<x>-<desk>/RD<NN>-<event>/` beside that desk's section pages;
  the lone C1-RD-round group is grandfathered; a foreign-desk round mints its
  desk's B group even when the group holds only RD pages.

## 0.2.0 — 2026-08-23

- **A Round parents to a NAMED Narrative — or to the Seed when the telling has
  no page on this board**: the new `foreign-desk` round-kind covers a review
  arriving from a desk this paper never told (the ICIS case), with the desk
  named in intake.
- **The routing table gains the Seed** as the destination for a concern that
  demands evidence the paper does not yet hold (new analysis class, ablation,
  downstream outcome).
- **Letters live inside the Round page's folder**, never at repo root; the
  runtime group is `paperboard/C1-RD-round/RD<NN>-<desk>-<event>/`.
- Frontmatter gains version, summary, and `group-token: RD`.

## 0.1.0 — baseline

- The pre-260823 contract, written before this file carried versioned
  metadata; that history lives in git. (This CHANGELOG was created in the
  260823 family review, which found the 0.2.0 bump had no log.)
