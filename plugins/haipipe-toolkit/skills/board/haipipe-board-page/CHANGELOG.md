haipipe-board-page · Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.6.0 - 2026-08-01

## 0.8.0 — 260802

- TWO VERBS, and this skill is the door for both (JL 260802: "could we just
  rely on haipipe-board-page for this purpose? like haipipe-board-page create
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

- Usage stated at the top of the revise section: `/haipipe-board-page <page>`,
  and START FROM THE CHECKER FINDINGS rather than the top of the file, because
  each finding already names the rule it breaks and the part it is in.
- Four spots caught up with QB4: the Aim status vocabulary is `⬜ 🔨 🧠 ✅ ❄️`
  (shape, not hue) and is NOT the page `state:` set; an Aims or States group is
  `A<n>` carrying its Content part's number, name and emoji; Files groups are a
  menu of ACTIONS (Engines · Contracts · Checks · Input · Output); and an Aim id
  points at a Content PART.

- Makes `haipipe-board-page` the prose authority loaded by every one-page writer
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
  skills, like haipipe-board-page ... please creating them now") from the roster the
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
