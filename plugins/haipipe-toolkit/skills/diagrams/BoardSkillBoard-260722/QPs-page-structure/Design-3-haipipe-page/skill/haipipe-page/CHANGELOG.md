haipipe-page · Changelog
========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.26.0 - 2026-08-15

**for-slide retired** (JL 260815, ruled on the design board's QPf3): a deck is
plugin material at `<page>/slide/<page>-deck.html`, authored by an agent
(`/_board/autodeck`) and regenerated on demand, never a Page Type.

- Type resolution drops the step-③ key `page-type: slide`.
- `page-types/haipipe-page-for-slide/` removed from the family; its specimen
  is archived on the design board (`_archive/QBt9-for-slide.md`).
- Sixteen variants ship. Re-run `Tools/install.sh --global` so the removed
  variant's symlink stops resolving.

## 0.24.0 - 2026-08-09

**Five paper variants admitted** (JL 260809), taking the roster to sixteen across
three skill sets.

- Four family DASHES, one per multi-unit paper family:
  `for-dash-section`, `-value`, `-display`, `-literature`.
- `for-narrative`, which absorbs seed, claims and pitch and adds the
  section-by-section outline the Section pages execute.
- Type resolution gains two step-③ keys. `page-type: narrative` behaves like
  `page-type: section`. `page-type: dash` is the first key that resolves to a
  FAMILY of contracts: the key says the page is a rollup and the
  `S-<Family>-Dash` filename says which of the four, so a key and a filename
  cooperate here instead of one beating the other.
- Two merges recorded on JL's ruling, both grounded in the real pages:
  **Value absorbs resource**, because `S-Work-R1-cms` already pointed at
  `tasks/A11_CMS-pipeline/` and sat at PROBE pending with no `route:` line;
  **Section includes Appendix**, because one stage row and one Page Type already
  governed both and only the reader-order key differed.

## 0.23.0 - 2026-08-09

- Page Type variants now ship under the `page-types/` folder of the SKILL SET
  THAT OWNS THEM (JL 260809). Every skill set carries its own `page-types/`, so
  the folder a variant sits in is what names its owner.
- Eleven variants across three skill sets, replacing the "ten, all here" roster:
  five in `board/page-types/` (for-stage, for-skill, for-meeting, for-slide,
  for-design), five in `paper/page-types/` (for-venue, for-section, for-display,
  for-literature, for-value), one in `subjective-label/skills/page-types/`
  (for-labeling).
- `for-stage` stays on the board side on purpose: a stage page is a BOARD
  mechanism (chain, managed contract span, human gate) that the paper and
  application families both instantiate, not a paper artifact.
- Supersedes "ships WHERE THE BOARD FAMILY MAINTAINS IT" (JL 260803), which held
  only while one family owned every variant.
- The base contract, the Type resolution table, and the phase grammar are
  unchanged. Only ownership and the roster moved.

## 0.22.0 - 2026-08-09

- Renamed from `haipipe-board-page` to `haipipe-page` (JL 260809), so the three
  altitudes read board, page, sentence, one word each.
- The 14 units built on this stem followed it: the 10 `page-types/` variants,
  the 4 `page-phases/` contracts, plus `haipipe-page-orchestrator-agent` and the
  externally maintained `haipipe-page-for-labeling`.
- No contract change. Every section rule, the Type resolution table, the phase
  grammar, and the RUN receipt are byte-identical apart from the name.
- `haipipe-board-routing` deliberately kept its prefix, on JL's call, so the
  family no longer names its members by one rule. The trade is recorded in the
  family `CHANGELOG.md`: this name now reads as a peer of `/haipipe-paper`
  rather than as a unit under the Board door.

## 0.21.0 - 2026-08-06

Resolution step ② re-keyed (JL's evidence-page ruling, 260806): the two
evidence types resolve by the HEAD `route: outward | inward` line, one line in
the metadata head right after `owner:`/`method:`, replacing the retired
`### Q-consumer register` marker + register route line. The variant table now
says "evidence page" for the pair; `haipipe-board/ref/topic-entry-contract.md`
declares the line.

## 0.20.1 - 2026-08-05

Resolve-order slot reworded for thin-paper phase 2: the last slot is
"family craft: the stage's declared craft files (and for probe, the family
door's probe tooling)". Family-specific stage data (the paper door's stages/
and craft files) stays in its own family; `haipipe-paper-stage` is retired.

## 0.20.0 - 2026-08-05

**One resolution table, every type machine-resolvable** (review fix). The stale
"Six Page Types" table, written when six types existed, is replaced by a single
resolution table covering ALL types, resolved in a fixed order: ① filename
prefix (`Skill-`/`Agent-` → for-skill, `Meeting-` → for-meeting, `QBv` →
for-venue), ② the register's REQUIRED `route: outward | inward` line
(for-literature / for-value, declared in `haipipe-board/ref/topic-entry-contract.md`),
③ the REQUIRED frontmatter `page-type: display | slide | design | section`,
④ the `S-<Family>-<unit>` stage filename, ⑤ the Q filename. Exactly one key
matches or the page is defective. A `page-type:` key beats the filename, which
settles the S-Display-4c stage/display double match and the QA4 Q-file slide
page.

- Four stale self-contradictions fixed: the six-type heading and table; "the
  three Page Type variants maintained here" (ten); the "five implemented types
  need only four prefixes" sentence (the glob decides membership only, the
  table decides type); the claim that Meeting "has no contract in any skill"
  (it has for-meeting).
- The admissions paragraph is split into short sentences; "ride the stage
  shape" now reads "look like stage-page filenames".

## 0.19.0 - 2026-08-05

**for-design admitted** (JL, ruled A on the design board's QB6; his definition,
260805: "we want to design some messages, say message A, B, C for one group of
people; the Content divisions ARE the different messages"). One page per design
BRIEF, its Opening stating audience, goal, and constraints; one Content division
per CANDIDATE, each carrying the artifact itself, its rationale, and its fit to
the brief's criteria; Aims are the criteria. Closes on a SELECTION record naming
the winner, why, and each loser's disposition (dropped · kept for A/B test ·
merged). Sits upstream of for-display: design selects the candidate, display
accepts its render. A losing division is never silently deleted, because the
rationale for NOT choosing is part of the design record.

## 0.18.0 - 2026-08-05

**for-slide admitted** (JL, on the Page-for-Slide branch). One page per deck, one
division per slide, each carrying its outline plus the PNG export of the built
slide; the live html-ppt deck stays a linked artifact because the board strips JS.
The slide binding (division · source · render · acceptance) is its typed record.

## 0.17.0 - 2026-08-05

**Two more Page Types admitted** (JL, same day, thought against the paper skill board and the MISQ board together).

- `for-section`: loads `for-stage`, adds the section kind, the venue contract block (blueprint BINDING, style reference, override stated), and the landing surface for the three record types. Reverses the for-main rejection: Main is one family's region, section is a cross-family shape.
- `for-meeting`: the routing rule for spoken decisions; Meeting pages stop being contract-less.
- The types table's Meeting row now states the real closing rule.

## 0.16.0 - 2026-08-05

**Three Page Types admitted** (JL, QB6 Decision Now: D, plus display standing alone).

- `page-types/haipipe-page-for-literature` and `-for-value`: two types over ONE loaded topic core (`ref/topic-entry-contract.md`), each adding only its route's translation layer. They resolve by the register marker plus route direction, not by filename.
- `page-types/haipipe-page-for-display`: mirror-shaped, but its unit is produced by the project and closes on human acceptance of a specific render.
- The Six Page Types section now lists six variants and says why the last three were admitted.

## 0.15.1 - 2026-08-05

**Nine review findings applied** (fresh-context cold read, verdict REVISE; JL: "go ahead to update it").

- The Decision Now reservation now admits the unsettled S-page exception (`### Needs JL · tick these`) instead of stating the rule as settled while a variant contradicted it.
- The "A CHANGE IS FINISHED" paragraph split to one sentence per line; the QC1b consumer chain split at its double colon.
- The boundary figure names `cli/serve.py` and `cli/check.py` with their dir, as it already did for `src/`.

## 0.15.0 - 2026-08-04

- Adds `### 🔗 Related Board Pages` as the fixed, typed Files group for bounded
  cross-Page context rather than configuration inheritance or dependency
  inference.
- Defines relation + Page Phase + Page id + scope + Board-relative path rows.
  Scope is either one whole Page or one direct Content division; a division
  brings its Page identity, Opening, and matching Aims/States group.
- Requires agents and Page RUN to resolve the current phase through
  `cli/pagecontext.py`, one hop only. Broken paths, mismatched Page ids, missing
  scopes, and malformed rows stop as mechanical findings instead of silently
  dropping context.
- Emits Page identity and Opening once when one phase selects several scopes on
  the same target, after the first fresh-context trial exposed the repetition.

## 0.14.0 - 2026-08-04

- Adds the concrete `RUN` verb for one bounded, non-linear Page lifecycle. It is
  not named `ADVANCE` because phases may repeat, branch, HOLD, or begin a new
  DRAFT round.
- Adds `ref/page-run-contract.md`, the common raw-material packet, phase receipt,
  version identity, role-separation, durable audit bundle, legal-route, stop,
  and fault-test contract shared by all four Page Phases.
- Requires the producer, mechanical builder, and judge to have distinct actor
  identities and verifies that each version is exactly its two declared
  lowercase SHA-256 digests.
- Makes the CLI independently rehash the current source and rendered Page, so
  agreement among receipt fields cannot substitute for artifact identity.
- Audits the preserved packet against the run and enforces receipt-to-receipt
  version continuity, start-phase identity, gate identity, and declared bounds.
- Wires RUN to the Board-owned Workflow and deterministic lifecycle auditor.

## 0.13.0 - 2026-08-04

- Adopts QB9's lifecycle vocabulary without adding an `ADVANCE` verb: one persistent Page combines a stable Page Type with a current DRAFT, PROBE, REVISE, or CHECK phase.
- Adds the load order `base → matching Page Type → current Page Phase → family worker` and routes phases by authority rather than add, delete, move, or rewrite operations.
- Moves the three `for-*` variants under `page-types/` and names the four direct phase contracts under `page-phases/`.
- Defines returning to DRAFT after purpose or Aims change as a new round on the same Page.
- Changes the section write table from generic machine permissions to phase authority, including the correction that changing Aim intent is DRAFT rather than REVISE.

## 0.12.0 - 2026-08-03

**Board bucket review, 260803** (JL: "go ahead to solve yourself, dont ask me"). Ledger: `skills/_console/260803-board-bucket-review.md`.

- **"The seven sections" is gone.** It was an invented count, cited as settled by four files, and it disagreed with its own authority and with the template: `ref/board-form.md` §4 fixes the ON-STAGE order at FIVE, and `ref/page-template.md` carries 13 `##` headings. Every statement now points at the authority instead of restating a number.
- The kind table went from three kinds to **six**, with the note that `src/common.py` globs four prefixes because a `Skill-` page rides the `S` glob.
- Both variants are named, with which page kind each governs, so a `QBv` author is routed. Only `haipipe-page-for-skill` was named before.
- The variant location rule is MAINTAINER-based, matching the door.
- The Opening budget says target ~450, hard ceiling 520, which is what `check.py` enforces. It had said "under ~450", a limit nothing checked.

## 0.11.1 - 2026-08-02

- Routes the two skill and agent page kinds away from this skill's own `create a new page` steps. They are GENERATED by `haipipe-board/cli/skillpage.py new`, which writes the page from its own stub and registers it in `board.md` itself; copying `ref/page-template.md` and registering by hand produces a page with no managed spans that the checker reports as broken forever.
- Found by a blind door test that followed this contract literally and hit the contradiction: two create procedures existed and nothing said which applied.

## 0.11.0 - 2026-08-02

- Names `haipipe-page-for-skill` as the variant for the Skill and Agent mirror
  kinds, and says to load it before writing or fixing any `Skill-<n>` or `Agent-<n>`
  page. It is the one variant that ships BESIDE this skill rather than under a
  consumer family, because for those two kinds the consumer IS the board family.
- Records why that variant had to exist rather than a tighter rule here. This skill
  already carries the noun-substitution test, so the rule was on the books when five
  skill and agent pages came out of one template on 260802. The cause is upstream of the test:
  this skill's Opening shape ends in `what this page decides`, and a mirror page
  decides nothing, so a writer obliged to ask a question can only manufacture a
  rhetorical one. The empty slot was the defect, not the writers.

## 0.10.0 - 2026-08-02

- `working on an existing page` gains steps 7 and 8: ONE page is the deliverable,
  a write outside it is allowed only when the page cannot be made correct without
  it and must be named in the report, and a sibling page's CONTENT is never
  rewritten. Step 5 sends an agent to other files on purpose; nothing bounded it.
- The verb now states the measurement that produced the rule. Three fresh agents
  were each given one sentence and nothing else on 260802. All three found this
  skill unaided (at tool calls #5, #6, #5) and drove their page to zero findings,
  including the one whose wording matches no trigger in the description. They then
  disagreed completely about reach: 1 file versus 15, the wide one touching four
  shipped `SKILL.md`, four `CHANGELOG.md`, six sibling pages and `board.md`.
  Neither was wrong on the merits, which is exactly why the bound had to be written
  rather than left to judgment.

## 0.9.0 - 2026-08-02

- A machine now CLOSES a `### Decision Now` row once the person has answered it,
  recording which option, who ruled, when, and the words they used (JL 260802:
  "I think you should close it automatically, please go ahead and do it").
  It still may not close a row nobody answered, and may not flip a page-level
  human gate; a machine's own recommendation is never an answer. Before this a
  row answered in chat and acted on within the hour still rendered as pending,
  so the page reported work as waiting that had already shipped.

## 0.8.1 - 2026-08-02

- Repointed every design-board citation after `QC1b`'s 260802 Content rebuild: the door test
  moved from `QC6 §7` to `QC1b §1`, the anchored-write rule from `QC6 §9` to `QC1b §4`, and the
  human-decision rule from `QC6 §10` to `QC1b §5`.
- Corrected the named next step. The rule strings it must replace are not in `cli/serve.py` and
  there are not one of them: they moved to `live/chat.py` in the `QC2c` live-layer split, and
  there are four (`CHAT_RULES`, `FULL_RULES`, `BOARD_CHAT_RULES`, `BOARD_FULL_RULES`).

## 0.8.0 — 260802

- TWO VERBS, and this skill is the door for both (JL 260802: "could we just
  rely on haipipe-page for this purpose? like haipipe-page create
  a new xxx on the topic of xxx, or working on the xxx"): `create a new page
  on <topic>` scaffolds from the template and registers it in the roster;
  `working on <page>` brings an existing page up to the contract, starting
  from the checker's findings rather than the top of the file.
- The boundary was restated rather than broken. "Never renders, serves or
  checks" meant this skill does not CONTAIN that code; it does call it. A
  reader asking for one page should not have to know which script does what.
- The engine commands both verbs run are listed once, so nobody memorises
  them, with the note that `watch.py` covers `.md` only.

## 0.7.0 — 260802

- Usage stated at the top of the revise section: `/haipipe-page <page>`,
  and START FROM THE CHECKER FINDINGS rather than the top of the file, because
  each finding already names the rule it breaks and the part it is in.
- Four spots caught up with QB4: the Aim status vocabulary is `⬜ 🔨 🧠 ✅ ❄️`
  (shape, not hue) and is NOT the page `state:` set; an Aims or States group is
  `A<n>` carrying its Content part's number, name and emoji; Files groups are a
  menu of ACTIONS (Engines · Contracts · Checks · Input · Output); and an Aim id
  points at a Content PART.

- Makes `haipipe-page` the prose authority loaded by every one-page writer
  instead of copying an Opening checklist into assignment prompts.
- Keeps the physical Opening shape but removes the fixed sentence count and
  rhetorical slot order; difficulty, failure, downstream effect, and success
  are review probes rather than one sentence each.
- Requires an existing page to be read completely before its Opening changes,
  adds the noun-substitution self-check, and keeps independent approval with a
  fresh reviewer.
- Adds a batch readability unit so individually clear pages still fail when
  they repeat the same sentence stems or form-letter argument across a Board.

## 0.5.1 - 2026-08-01

- Clarified the base/variant boundary: a consumer variant defines Content and
  may fill typed records through declared Aims, States, and Stage Contract
  extension points, but it never redefines the shared frame sections.

## 0.5.0 - 2026-08-01

- Keeps requirements in the page spec instead of copying them into a separate
  evaluation skill.
- Resolves base, variant, page-local, Stage Contract, division, and paragraph-job
  requirements before judging.
- Defines four axes (mechanics, function, evidence, readability), four verdicts,
  and one evidence-bearing report row per section or Content unit.
- Assigns execution to the existing `check.py`, `✅ Quality Check`, and fresh
  Board reviewer surfaces.

## 0.4.1 - 2026-08-01

- Canonicalized the paired section labels as `Aims / States`: both are plural
  collections, while one Aim still maps to one current State record.
- Kept singular `State` as a legacy input alias alongside `Where we are` and
  `Now`.

## 0.4.0 - 2026-08-01

- The page contract now separates durable intent from present fact. `## Aims` holds stable Content-linked targets (`A3.1`, with `P1` for page-level targets), a testable `Done when`, and an optional temporary `Plan`. `## State` mirrors every Aim exactly once with ⬜, 🟡, 🟠, ✅, or ⏸️. State transitions go to Log; Decision Now remains the human-only checkbox edge. A Content division may have zero, one, or many Aims, while every Aim must have one current State row.
- The fixed sequence is `Opening → Diagram → Content → Aims → State → Files`. The contract no longer teaches the retired generated Structure row or checkbox-based page completion. Historical `Items to Finish`, `Done when`, `Where we are`, and `Now` remain parser aliases, not canonical authoring guidance.

## 0.3.0 - 2026-08-01

- The five-row section contract (JL 260801, ruled as option A on the design board's
  QB4 Decision Now): every section answers ONE reader question, and the same five
  rows define each section's contract — conveys · holds · source · rules · omit.
  The seven-sections table gains the reader-question ladder plus the
  misplaced-sentence rule (substance in Opening → Content, contract material in
  Content → Stage Contract, settled flags → Where we are, open work → Items to
  Finish). Long form stays on the board's QB4a-QB4g faces; the compact form now
  lives here and in `ref/q-template.md`'s How-to-use comment, where a writer
  actually meets it.

## 0.2.0 - 2026-07-31

- Decision Now: the one RESERVED subsection name inside `## Where we are` (JL, same
  day: "don't make the decision here ... Always go to the corresponding Q's Where we
  are's subsection of Decision Now"). It lists the decisions a machine proposes and
  the human must make, one `- [ ]` row each with the ask, the options, and a
  recommendation; the human answers by ticking; an answered row moves into the
  page's dated record. The 260729 contextual-naming rule stands for every other
  subsection; this is its single exception.
- The tick rule now names the landing spot: a machine PROPOSES a tick as a Decision
  Now row, never in chat alone.
- The board pages `QB4e` (the Where-we-are face) and `QC6` on the design board carry
  the first two live subsections.

## 0.1.0 - 2026-07-31

- First cut, created on JL's order ("make the haipipe-board thinner, and have other
  skills, like haipipe-page ... please creating them now") from the roster the
  design board had already settled: QC6 §8's shape is one door, two SPECS, two VERBS,
  and this is the page SPEC the routing and digest verbs LOAD.
- Contract-first: no code moved. It owns what a page IS (the three kinds over one
  base, the seven sections in their fixed order, the write anchors), and it cites
  `haipipe-board/ref/q-template.md` as the authority rather than forking it.
- Carries the two machine-write rules with their provenance: writes land at a
  SECTION BOUNDARY, never a byte offset (QC6 §9, after a concurrent session spliced
  a heading into the middle of another page's Question sentence on 260730), and a
  transcript-reading verb may propose a tick but never tick or flip `state:`
  (QC6 §10, because reporting a claim is not verifying it).
- Names its own next step from QC6 §7: `serve.py`'s `CHAT_RULES` becomes a consumer
  of this contract instead of a hand-rolled copy, which has already rotted once
  (QB5d caught it describing a page shape that no longer existed).
