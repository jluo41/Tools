haipipe-board-page-for-stage · Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.5.0 - 2026-08-05

Thin-paper phase 2 (QC6 ruled A; JL "go" 260805): stage.md MAY declare `checker:`
(CHECK runs it before judging) and `craft:` (DRAFT/REVISE load these data files
last, in place of the old "family worker" skills). New paragraph added under the
stage.md resolver section. Stage roster repointed to
`paper/haipipe-paper/stages/index.yml`; the venue-free/aligned line is now drawn
by the paper door (`haipipe-paper`), and family artifact knowledge arrives
through declared craft files rather than worker skills.

## 0.4.3 - 2026-08-05

**The unit-page shape hands off to the more specific types** (review fix). An
`S-Main-<n>` or `S-Appendix-<letter>` section unit declares `page-type: section`
and loads `haipipe-board-page-for-section` on top of this file; an `S-Display`
unit page declares `page-type: display` and loads `haipipe-board-page-for-display`.
The stage filename still names family and unit; the `page-type:` key names the
governing contract, and the key beats the filename (base type resolution ③).

## 0.4.2 - 2026-08-05

**The resolver table caught up with the paper reorg it shipped a day behind.** The table stamped "where the keys ACTUALLY live" listed 7 dead dirs and 6 stale key pairs; regenerated from the shipped stage.md files: seed/venue/pitch are Open with capitalised control-page units, resource/claims/narrative are Work R/C/N. Three `5-section-edit/stage.md` citations repointed to `S06-main/section-edit/stage.md`; the `S-Venue-0` examples became `S-Open-Venue`; one em-dash pair became parentheses; the `S-Main-3` measurement sentence split in two.

## 0.4.1 - 2026-08-04

- Moved under `page-types/` with the other stable Page Type variants.
- States the orthogonal load order: base Page, Stage Page Type, current Page Phase, then the paper or application worker.
- Repoints its generic phase layer to `haipipe-board-page-draft`, `-probe`, `-revise`, and `-check` without imposing a fixed sequence.

## 0.4.0 - 2026-08-03

From the second fresh-agent test, which APPLIED this contract to `S-Main-3-theory` rather than only reading it, and took the page from 32 findings to 4. It listed ten defects; these are the ones this file owns.

- **🎯 The Aims and States scheme, which 0.3.0 was completely silent on and both testers named as the biggest hole.** The base keys an Aim id to a CONTENT PART, and a stage page's Content is a manuscript section numbered `§3.1`, so there is no part `3` for `A3.1` to hang from. Every stage page on the real board answered by using no ids at all: 21 un-ided Aims, zero `Done when`, no State row mirroring anything, and a render whose `met/total` counter therefore reports nothing. The scheme is now the q-consumer id `5-section-edit/stage.md` already declares, `Q-Sec<unit><Kind>-<n>`, with `P<n>` for cross-division targets — and a warning not to force the mirror in one pass on a live manuscript, because doing so would undo JL's 260727 ruling that a decision row carries the decision only.
- **📜 Stage Record placement contradicted itself.** `board-form.md` lifts it to the contract's OPENING lines; this file said author prose goes AFTER the end marker; the generated span sits directly under the heading, so both could not hold. Ruled: the SOURCE goes after the end marker, the RENDER may print it first, and a build's ordering is not an instruction to authors.
- **🔀 Two headings named Venue collide in one section.** `stage.py` generates a `### Venue` pointing at the PITCH page inside the managed span; the hand-written `### Venue contract` names the BLUEPRINT as binding. A reader hits the generated one first and gets the wrong page. Until the generator is renamed, the hand-written block says what it supersedes.
- **📋 The venue block example was thinner than the rules around it.** It showed BINDING and reference and omitted both `desk:` and the per-section override the surrounding prose demands, so the tester had to synthesize two rows. Now a complete worked block, including the finding that produced it: MISQ publishes NO per-section length rule for theory, so the blueprint binds alone and its budget is an allocation of the 55-page total rather than an addition.
- **🔢 Content numbering was unstated for this kind.** A stage page follows the MANUSCRIPT's `### §3.1` / `#### P<n>.`, not the base's `3 / 3.2 / 3.2.1`. Nothing checks it, so it held only by luck.

**Rated by the tester as the contract's best moment**, recorded so it is not lost in a later trim: the two-source rule plus the DEFER TO DELIVER tier plus "the desk's total is the constraint the blueprint exists to divide" sent it to `QBv1-misq`, where it established that MISQ publishes no per-section length rule at all. It could not have written the override row without that chain.

## 0.3.0 - 2026-08-03

Every item came from ONE blind reader: given a single page path, no skill name, and told to work out what governs it. It found the contract in about four minutes, answered three of five questions cleanly, and broke the file in seven places. The three that were this contract's own fault are fixed here.

- **⚖️ THE SERIOUS ONE: the same number was "never enforced" and "BINDING".** Tier 🟡 says a word budget is measured after drafting and never enforced; five sections earlier the venue block stamps the blueprint `<- BINDING`, and `5-section-edit/stage.md` lists the word budget among what binds. The reader could not tell whether `S-Main-3`'s 1,770-word shortfall was a defect or a reported deviation, and that page has been stuck on the question for a week. Fixed by binding ROW BY ROW: the subsection count, the H-assignments and the owed displays bind because they are this paper's own architecture; the word floor, sentences per paragraph and citation density report because they are pack measurements that travelled into the blueprint by one copy step. A measurement does not become enforceable by being copied.
- **🧭 The resolver pointed at the wrong file.** 0.2.0 said "every stage row carries `board_family` and `board_unit`" under a table headed `stage row`. `stages/index.yml` carries `{key, order, dir, migrated, triggers}` and nothing else; the keys are in each `stages/<dir>/stage.md`. The blind reader grepped the index, got nothing, and lost a step. Second roster-shaped error in two releases, both from asserting a file's contents without opening it.
- **⚠️ The conformance-debt list is the CHEAP half, and now says so.** A session applied exactly the five listed renames to `S-Main-3` and stopped; the checker fell from 32 findings to 21 and every remaining structural violation was invisible to it: no Aim ids at all, 34 flat checkboxes, no `Done when`, no State row mirroring any Aim, `### Needs JL · tick these` in place of the reserved `### Decision Now`, two competing q-consumer id schemes. The render derives `met/total` from States, so the page passes the checker and reports nothing about itself.
- **🔀 New section for the four conflicts this contract cannot settle alone**, recorded rather than papered over: the base demanding an ASCII figure inside a journal theory section with no mechanism for a variant to suppress a base rule; `> CC:` being legacy to `check.py` and mandatory in `5-section-edit/stage.md`; `dead-file-path` not knowing a paper root exists; and nothing owning cross-page factual consistency, which is live on `S-Main-3` right now.

## 0.2.0 - 2026-08-03

Written from a review JL asked for hours after 0.1.0 shipped, plus his question of how the variant points at different kinds of stage. Both answers came from counting the real board rather than from re-reading the file.

- **🧭 The stage resolver, which 0.1.0 simply did not have.** `stages/index.yml` says a stage's phases, artifact paths, sections, done-criteria and craft live in `stages/<dir>/stage.md` and load only for the stage picked, and every stage.md declares `board_family` + `board_unit`. That pair IS the join: read `S-<Family>-<unit>` off the filename, match the row, load that stage.md. The variant now resolves and points, and holds no per-stage rule at all, which is the same two-source discipline the venue variant uses on the pack.
- **🧩 Three page shapes sit under one stage row.** The stage page the row declares; a UNIT page, where `section-edit`'s board_family and board_unit are per-unit rather than per-stage; and a DASH page, which has no stage row, is regenerated every run, holds only what no single page in its family can hold, and must never be given a gate, `requires:` or `provides:`.
- **🚫 A family with no stage row is a real state.** Submission and Literature carry gated pages that no row declares, and Round carries a Q page instead of an S page. Such a page owns its contract on itself and says so; it is not filed under a neighbouring stage because the folder sits next to it.
- **🔴 The roster in 0.1.0 was WRONG, and this is the review's real finding.** It listed eight families from a partial `find` and never verified them: it missed Literature entirely and asserted a Round family of S pages that does not exist. Replaced with counts taken off `Paper-Personality2Opioid-MISQ2026` on 260803: 8 stage rows, 9 families, 48 S pages, and the three do not divide into each other. The same failure the venue contract warns about, a closed roster written without checking, committed in the file that inherits that warning.

## 0.1.0 - 2026-08-03

First release. JL asked for a variant that lets a page use the sixteen venue pages while writing, and named it STAGE rather than section on purpose: the paper lifecycle also carries seed, resource, claims, venue, pitch, narrative and display, and all of them are the same page kind. Written against the real S pages of `Paper-Personality2Opioid-MISQ2026`, not from the template.

- **🏛 ONE stage reads the venue page, and it is the venue stage.** The design that survived contact with the real board. An earlier sketch had every `S-Main-<n>` page binding directly to its `QBv` rows through the shared `Sec-<n>` index; the real pages already do something better, and the evidence was sitting in `S-Main-3-theory.md`'s own `### Venue contract` block: the BINDING source is this paper's blueprint in `S-Venue-0-venue.md`, and the pack's `style.md` is marked reference only. So the chain is catalog ▸ decision ▸ draft, and nine pages never re-derive one desk. The blueprint is also where a desk's TOTAL becomes this paper's per-section allocation, which is arithmetic no venue page can do because it does not know how long your Results are.
- **🚦 The four transfer tiers**, which is what a stage page actually needed and no contract stated: copy the shape, carry budgets as targets and never as gates, never copy an exemplar sentence, and defer the desk's binding rules to deliver EXCEPT the per-section ones, which bind the drafting page. ISR's 300-word abstract cap and its separate 500-word contribution statement are the worked example, both owned by `S-Main-0`.
- **⚖️ A per-section desk rule outranks the blueprint's budget**, because one is published and enforced and the other is this paper's plan. A blueprint allocating 200 words where the desk caps 150 is a planning error the stage page reports rather than obeys.
- **🧮 A stage page never adopts a per-section budget without knowing the whole.** Measured across the sixteen venue pages on 260803: at every desk publishing a total, the pack's per-section budgets sum to at or above it. Systematic, not unlucky — a pack measures published papers section by section, and a published page is not a submission budget.
- **⛓ The chain is the variant's spine**: `requires:` / `style-from:` / `provides:` / `contract-source-hash:`, the `haipipe:contract` managed span written only by `stage.py`, and the rule that author prose goes after the end marker where sync preserves it.
- **🔀 Venue-free against venue-aligned**, lifted from `haipipe-paper-lifecycle` and enforced on the page, because it is what tells a reader whether a retarget costs an afternoon or a month. A venue-aligned page whose `style-from:` does not resolve to a venue-pinned upstream page is misfiled.
- **🩺 `state:` is a gate position and a machine never flips it.** Sharpened by how the chain works: `stage.py` prints each upstream page's gate state into this page's Required Inputs, so a gate flipped early silently unblocks everything downstream.
- **⚠️ Conformance debt written down rather than hidden.** The real paper board runs its S pages on the retired vocabulary (`## Question`, `## Boundary`, `## Items to Finish`, `## Where we are`, a direct `### Stage Record`). The renderer aliases all of it, so the pages look correct and nobody sees the drift, which is exactly how the same debt survived on 45 of 55 design-board pages until `check.py` started reporting it.
