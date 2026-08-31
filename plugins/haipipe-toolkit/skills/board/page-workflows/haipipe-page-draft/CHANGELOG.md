## 0.10.0 — 2026-08-31

Rewritten as ONE pass: 453 → 185 lines, present tense. ① the conversion by
Page Type (Section: one slot → one sentence ending `<!-- realizes: C.P.B -->`;
other: one point → one or more sentences) · ② five rules every sentence
obeys (the number with its `> Value:` lane; no hole token in prose, three
cases: `state=provisional`, `{VAL:? …} [Q-…]`, or a clean sentence + comment
lane + probe card; evidence by id; the present tense; plain words) · ③ what
the pass writes on the page (Opening, Diagram, Content, the Aims rows and
their `Now:`; never Files, Log, States or Discussion) · ④ track the change
(the `~~old~~ → new` diff folded under one log record; a `✎` lane for a single
sentence) · 🔀 · 🧾 · ✅ exit sweep with `sentence-without-realizes` and
`number-without-lane`.
- Retired: `<HOLE: …>` in prose; `WRITES … Aims (transcribed from the plan) ·
  Files · Log`; the three-layer, the outline-moved-out and the no-card
  histories (this file states what the pass does now).

## 0.9.2 — 2026-08-31

- **No `## States`**: the section list, the Aims wall, the Log rule and the hole-address table now say the merged form (tick + `Done when:` + `Now:` on one Aim row; haipipe-page 0.41.0).

## 0.9.1 — 2026-08-21

- **§📏 A Log row is one line, not a paragraph** (JL: "make sure to make the
  logging content to be as concise as possible, current it is too long. not
  good."): 15-35 words, the headline fact and at most one load-bearing
  caveat; every number and sub-step the long form used to list is
  recoverable from the diff, a run receipt, or the Content it landed in.
  Applies going forward; an old Log row is not retroactively rewritten.

## 0.9.0 — 2026-08-20

- **§📖 Trust the plan's answers; recount only what is marked** (JL: "看看哪里
  可以去优化"): DRAFT quotes the outline's `Answered:`/`Drawn:` values as
  written and re-reads only cards whose line ends `· recount`, plus one
  spot-check; QPw00's first DRAFT re-read all 14 evidence folders to find 3
  drifts, all self-referential run counts.
- **§🕰 Content states the present; the Log holds the past** (JL: "我们这里
  不是做 log 的地方，content 永远只包含最新的东西"): no "Before <date> it
  was X" in Content; the current rule is written clean and `## Log` carries
  when and why it moved.

## 0.8.2 — 2026-08-19

- **The value mark is 🧮** (JL: "🧮 maybe this one?" — he never liked 🔢).
  🔢 stays accepted as the legacy alias, so pre-260819 plans remain legal.
  The abacus was the proof mark retired earlier on 260819 and is revived with
  its new meaning: a recomputable number, which is what `checks/values.py`
  does to every one of them.
- **Coherence sweep (260819)**: §🃏's dead stake argument deleted (Aims live in
  the plan, so PROBE precedes this phase); §🗂 and §🃏 renumbered DRAFT ④ ·
  PROBE ② and the footer points at phase-cards §④; §🧱's worked example writes
  the NUMBER on landed evidence, with the hole as the blocked exception; §📂's
  crossing begins at ② PROBE, not EVIDENCE; the metadata summary says the same.

## 0.8.1 — 2026-08-19

- **The receipt's `route` enum still listed EVIDENCE and COMPILE**, which the §🔀
  table already excluded. Corrected to `DRAFT | PROBE | REVISE | CHECK | HOLD`.
  Found by the display agent rebuilding `QPw00-Display2`.

## 0.8.0 — 2026-08-19

- **DRAFT enters on LANDED evidence.** JL 260819: "until outline is
  self-consistent and together with all the evidence cards, then we are good to go
  ahead to draft." OUTLINE ⇄ PROBE ⇄ EVIDENCE now loops before DRAFT starts.
- **A hole becomes the EXCEPTION.** DRAFT writes the number. A hole is what a
  genuinely blocked question leaves, and it must name the missing input; a hole
  with no named blocker means the PREPARE loop exited early, and the fix is a
  `v<N+1>` at OUTLINE.
- The conversion is unchanged and is still the whole phase: one POINT becomes one
  or more SENTENCES, citing evidence by id.

## 0.7.3 — 2026-08-19

- **No `page-type:` key is the DEFAULT, not a defect.** JL 260819, deciding
  against creating a `question` page type for it: "question itself just to be
  very flexible." Reading the absence as a defect made OUTLINE illegal on 247 of
  274 pages, this session's own QPw00 among them. A page with no type owes the
  base section order and nothing more.

## 0.7.2 — 2026-08-18

- Pointer added to `../haipipe-page-workflow/ref/phase-cards.md` §②, which
  states this phase and every sibling in the SAME six fields
  (`❓ ASKS · 📥 READS · 📤 WRITES · 🚪 EXITS · ✋ TICK · 🔀 ROUTES`). This
  contract still owns the reasoning; the card is the readable-across-phases
  summary, and the contract wins when they disagree.
- Board backlink retargeted: `QPw7`/`QPw8`/`QPw9` became `QPw00a`/`QPw00r`/
  `QPw00g` when JL ruled that pages which are not phases may not carry
  phase numbers.


## 0.7.1 — 2026-08-18

Added the Board page backlink: the page that argues this contract, created 260818 when JL ruled one page per workflow step.

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
