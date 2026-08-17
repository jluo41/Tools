
## 0.7.0 — 2026-08-17

Defines the Point-to-sentence handoff: DRAFT instantiates each approved Point
as visible sentence scaffolds with holes, while PROBE owns cards and REVISE
realizes the final prose.

## 0.6.0 — 2026-08-17

**DRAFT creates NO card**, reversing the 260816 ruling that it may create one in
OWED state. JL asked the question directly on 260817: "具体的 proof 应该由谁来做？
我还没想好这部分是在 draft 阶段来做，还是在 outline 阶段来做？" §🃏 no longer
describes proposing; it records why the move left and where it went.

- The outline's MARK is the proposal, and `haipipe-page-probe` turns it into a
  folder. A card that only repeats the mark is a second copy of the plan, which
  is `haipipe-page-workflow` §🪞's duplication rule.
- The deciding reason is the STAKE: a card's `consumer/` side carries what the
  page loses if the answer never comes, that is an Aim, and Aims are written
  HERE. A card raised before this phase ends cannot carry its own stake.
- §🕳 renamed from "Raise the question, then stop" to "Name the hole and the Aim
  it costs, then stop", because DRAFT no longer raises a Q-consumer: it writes
  the visible hole and the Aim, and PROBE copies that pairing into `consumer/`.
- §🔀 routes an unsupported claim to PROBE, not straight to EVIDENCE.

## 0.5.0 — 2026-08-16

Every Page Type now DECLARES how it supplies its outline, and DRAFT reads that
declaration before proposing anything (JL 260816: "for the page-types, we should
have this outline to be ready first, and then people can fill it").

- Three modes, declared in each type's own `outline:` frontmatter block:
  FIXED (7 types) lists the divisions outright; GRAMMAR (for-task) fixes a
  closed first-word set with an order and repeat rule and lets DRAFT choose the
  count and the free title; RESOLVED (for-section, for-stage) names the source
  the outline comes from at runtime.
- GRAMMAR is the mode for a type that must be ready before anyone knows the
  content: the skeleton is fillable on day one and the free title still carries
  the subject's own families.
- The 🧭 outline tab is named as the surface where the result is read and
  approved (`page-plugins/haipipe-plugin-outline`).

## 0.4.0 — 2026-08-16

DRAFT is the PLANNING phase and the OUTLINE is its deliverable (JL 260816).

- Added the three-layer ownership map for content shape: the FRAME is
  `haipipe-page`/QPs1's (section order, and it deliberately leaves Content free),
  the DIVISION SHAPE is the matching Page Type's, and THIS page's outline is
  DRAFT's. DRAFT instantiates the type's shape; inventing one it already declares
  is the defect. Raised by JL: "there are structure for the page format, right?
  but there is not structure for the content".
- Named the CONTAINER-shape trap: `page-type: view` fixes four divisions
  (QA inputs · View body · Displays · Consumers), so a seven-result-family
  regression report written to it prints machinery as its top-level sections and
  buries the result families under `View body`. Readable as a View, unreadable as
  a report.
- Added the OUTLINE section: the numbered `### <n> ·` list with an ESTABLISHES
  column and an EVIDENCE-OWED column using the three kinds 📚 citation · 🔢 value
  · 🖼 display. A blank evidence column is a division nobody can finish.
- Four outline rules: group by the subject's own families never by work order;
  a division names what the READER LEARNS never where material came from;
  one estimand per division; show the outline before writing the prose.
- DRAFT may now PROPOSE the evidence card itself, in OWED state (JL 260816:
  "the evidence card should be proposed by either draft or by the evidence").
  This is the existing `\cite{TOADD} [Q-<Stage>-<n>]` move generalized from
  citations to all three kinds: a probe card carrying its stake, a display unit
  README carrying `claim:` + `caption-job:` and no `intake/`. PROPOSE vs FILL is
  the boundary; only EVIDENCE fills. A proposal says what it will hold, so a
  claim-less folder is litter and `display-declared-no-claim` reports it.
- Phase token DRAFT -> EVIDENCE throughout.

haipipe-page-draft · Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.3.2 - 2026-08-05

Load-order slot reworded for thin-paper phase 2: "family worker" is now
"family craft: the stage's declared craft files". The dissolved paper workers/
leaves live on as stage data files declared in each stage.md `craft:` list.

## 0.3.1 - 2026-08-05

- Opening now states DRAFT's own risk (a hidden hole reaches print) instead of the three-line ownership couplet shared verbatim with REVISE and CHECK, the 260802 form-letter failure repeating one level down.
- Q-consumer and stake get a defining line at first use; this file is loadable standalone.

## 0.3.0 - 2026-08-04

- Adds the shared RUN receipt boundary: DRAFT names the promise authority it
  exercised, its changed artifacts and visible evidence, and one legal route.
- Keeps round ownership in the controller so a DRAFT entered after reopening
  does not increment the round twice or approve its own result.

## 0.2.0 - 2026-08-04

- Renamed from `haipipe-board-page-for-stage-draft` and moved under `page-phases/`.
- DRAFT now applies to any Page Type and is defined by authority over purpose, Aims, and promised shape rather than first creation or a specific editing operation.
- Returning from REVISE or CHECK to DRAFT explicitly starts a new round on the same Page.
- DRAFT raises the stake-bearing Q-consumer and leaves Q-executor, routing, evidence collection, and interpretation to PROBE.

## 0.1.0 - 2026-08-04

**Created** (JL: "ok, I agree, please go ahead and make them.").

Split out of the family workers so the four-phase loop has ONE rulebook instead of
one per family. Measured 260804: the paper and application families each shipped
their own draft/probe/revise/check hubs (1,263 lines against 531), and NONE of the
eight loaded `haipipe-page` at all, so each had copied the page grammar from
memory. `haipipe-paper-draft` still named `## Items to Finish` five times, a
section renamed that morning.

- Host-agnostic on purpose: names no venue, no markup, no checker. A family worker
  adds its artifact knowledge and obeys this file.
- Settles `QC6 A4.1`: paper and application share a CONTRACT, not folder names.
