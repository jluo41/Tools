---
name: haipipe-paper-ideation
description: >-
  Paper journey phase P0 (Ideation) and the Page Type contract for one research
  direction's ideas, before any selected Story exists: generate, compare, and
  optionally order a dynamic candidate set, novelty-check claims, record
  pilots, compare journal fit, then eliminate, defer, or send selected
  idea-and-target pairs to distinct Stories. Use when brainstorming a direction,
  checking whether an idea has been done, or deciding where it fits. Trigger:
  ideation page, find ideas, brainstorm, novelty check, journal fit, page-type
  ideation.
metadata:
  version: "0.9.0"
  last_updated: "2026-09-08"
  group-token: "Story00"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "the Page Face is Opening → Outline → Content → Aims; Content division 1 is Direction, division 2 is Ideas (ranked) with a source bullet naming each ideation handoff or legacy IDEA_REPORT it drew from; for a dynamic set of K admitted ideas, divisions 3 through K+2 are Idea 1 through Idea K, each carrying Method · Hypothesis · Minimum experiment · Expected outcome · Core Claims / Novelty Check · Pilot result · Journal / Venue Fit · Risk · Reviewer's likely objection · Recommendation; division K+3 is Eliminated Ideas and K+4 is Suggested Execution Order (a retrofit page may nest its single idea under division 2)"
---

# /haipipe-paper-ideation · one direction's ideas, in the reports' own words

Load `haipipe-page` first and `haipipe-page-workflow` when running the Page.
Declare `page-type: ideation`.

## 🧭 Journey phase

This skill is journey phase P0 Ideation (ideate) of the paper journey and owns
the `page-type: ideation` contract below. The repo is minted WITH this page, so
there is no entry gate. Exit through gate G0 for each selected idea: per-claim
novelty bound to Supporting Run Results, a pilot result or explicit waiver, complete deep
venue fit, and a person's PROCEED or risk-accepted PROCEED WITH CAUTION tick
selecting the intended target/category
and sending that idea to its own Story. `haipipe-paper-workflow`
holds the full gate assertions; this block only places the phase. The page
itself always runs through `/haipipe-page` and `haipipe-page-workflow`
(OUTLINE → … → CHECK), never a private lifecycle.

## 🌱 Grain and home

One Ideation Page holds ONE research direction and a dynamic number of
candidate ideas raised under it. It is the story group's PAGE ZERO (0.4.0) —
no separate group; it sits in the same group as the Stories its selected ideas
become, before them:

```text
Paper-<Slug>/
└── A1-Story/                          the story group, at the paper root (0.8.0)
    ├── Story00-ideation/              THIS PAGE · one direction, its ideas, ranked
    └── Story-A/                       what the first selected idea became:
        ├── Story-A.md                 one idea · one prospective paper blueprint
        └── outline/                   its Page workflow records
    (a second surviving idea is Story-B/ · the letter identifies the Story)
```

**The repo precedes the Story** (0.2.0): minting a paper's Ideation Page is
what creates `Paper-<Slug>/` — as a git submodule immediately, per the
scaffold rule — with only `board.md` and `A1-Story/Story00-ideation/` inside.
The direction's name may seed the repo slug; a direction that dies leaves the
repo standing as its own record. **A board holds exactly ONE ideation page**
(the journey fixes the story group's roles, one each): a direction that
genuinely forks is a new direction, so it mints its own `Paper-<Slug>/` with
its own `Story00-ideation`, and the two pages cross-reference through the
originating row's `went to`. Two ideas from the SAME direction that both
survive are `Story-A` and `Story-B` in this board (0.9.0, JL 260907: the Story
letter identifies the selected Story); the `went to` cell names the Story page
by id. Before 0.5.0 a fork could take "the next free SD number"; that reading
died when the journey fixed the roles, and 0.8.0 gives the number back its
counting job at the idea level.

Historical `SD00-ideation` / `SD01-seed` instances remain readable and are not
renamed or moved merely to satisfy this contract. When such a Page is next
revised, record its canonical `Story00-ideation` / `Story-<letter>` role and
preserve two-way links. A filesystem rename is a separate, explicitly scoped
migration, never an implicit Page or G0 action.

The page is EVERGREEN (♻️): it never closes while the direction is alive.
Ideas are cheap — generated in batches, compared, optionally ordered, and
eliminated without ceremony. There is no fixed count and no required global
winner. `Ideas (ranked)` records the current comparison/attention order; it is
not a best-to-worst truth and never substitutes for a human verdict.
What is never cheap is the row: an eliminated idea's row stays forever,
because the record is what stops the same idea being re-thought in new words
six months later.

## 🪟 Page face

The reader-facing Page keeps the base four-part shell. `Outline` and `Content`
are the two primary working surfaces, but `Opening` is required and `Aims`
remains a brief completion contract:

```text
## Opening   the direction question and why this decision needs a visible record
## Outline   the compact C/P/B · Feedback · Evidence · Supporting/Local Run projection
## Content   the full Direction, candidate Ideas, novelty, pilots, and routing below
## Aims      short direction-level and Page-level done-when statements
```

Do not promote Data, Preliminary Results, Novelty Check, Feedback, Display,
States, Files, Log, or Discussion into additional top-level Page sections.
Data and preliminary results live in each Idea's Method/Minimum experiment and
Pilot result; Novelty Check lives under Core Claims; Journal / Venue Fit lives
inside each Idea division; Feedback/Display/receipts remain in their owning
Page workflow records.

Page review and Paper selection are separate human decisions. The Page
workflow's `approved:` accepts the C/P/B Shape and its `accepted:` CHECK ruling
accepts one readable Page version. Neither selects an Idea. G0's dated
`PROCEED` or `PROCEED WITH CAUTION` verdict selects one Idea and authorizes its
`went to` Story edge; it does not close this evergreen Ideation Page. Never
infer either decision from the other.

## 📐 Content outline · the source reports' structure

The divisions mirror IDEA_REPORT.md (idea-creator) section for section, with
the Novelty Check Report's Core Claims and HAI Idea × Venue Fit projection
folded into each idea's division. Let
`K >= 1` be the number of admitted Idea Cards, including cards later
eliminated whose divisions remain as history. The number is dynamic:

```text
### 1 · Direction                    🔒 the research direction · why now ·
                                        what makes an idea here worth a paper
### 2 · Ideas (ranked)               🔥 summary table, one row per live idea
                                        · one source bullet per ideation handoff
### 3 … K+2 · Idea <n>: <title>      one division per admitted idea, in current
                                        comparison order,
                                        the report's own fields (list below)
### K+3 · Eliminated Ideas           ♻️ the report's table: | Idea | Reason eliminated |
                                        rows permanent
### K+4 · Suggested Execution Order  ♻️ what to do first · who went to which Story
```

A retrofit page whose single idea already became the paper may nest that idea
under division 2 (`#### 2.1 · Idea 1: <title>`); the field list still applies
inside it.

Admission is the stable boundary. An idea becomes admitted when the semantic
layer assigns it a zero-padded `iNN` card (`i01`, `i02`, ...); from then on it
keeps one division forever.
A duplicate phrase, overbroad claim, or framing rejected before `iNN`
assignment may appear only in Eliminated Ideas with its source and reason and
does not owe a fabricated Idea division. The Page must state which kind each
eliminated row is.

## 📊 Ideas (ranked) · division 2

The summary table, one row per live idea, every cell a state and never a
blank:

```text
id  idea                 novelty       pilot        venue fit       verdict       target       went to
─────────────────────────────────────────────────────────────────────────────────────────────────────
i01 <one sentence>       HIGH           ✅ Result     STRONG · vfit   ✅ PROCEED    JAMA · Art.  Story-A
i02 <one sentence>       ⬜ unchecked   —            ⬜ pending      ⬜ open       —            —
```

Verdict vocabulary — the Novelty Report's own recommendation words, decided
by a person: `⬜ open`, `✅ PROCEED`, `⚠️ PROCEED WITH CAUTION` (the named
risk accepted in the tick), `🚫 ABANDON`. An abandoned or merged idea moves
its row to Eliminated Ideas with its reason; its division stays as history. A
`—` cell is legal only where the verdict makes the column moot; on a live row
every cell is a state or a bound path.

Each batch of ideas enters through a source bullet naming the IDEA_REPORT (or
ideas.md) and its Run/Result receipt; ideas do not appear from nowhere.

The row order supports comparison and attention only. The first row is not
automatically selected, and the page may end with no selected idea, one
selected idea, or several selected ideas. Human verdict and `went to`, not
position, record selection; several selected rows route to distinct Stories.
For every admitted row, `venue fit` is a state backed by its Idea × Venue Fit
Card. A selected row also names the person's target and article/category;
machine recommendations stay inside the idea division.

## 🧾 Each idea's division · the report's fields

One division per idea, titled `Idea <n>: <title>`, carrying IDEA_REPORT.md's
field names plus the explicit HAI Journal / Venue Fit field:

```text
Method                        what we actually do, 2-4 concrete steps, plain language
Hypothesis                    one sentence
Minimum experiment            the smallest run that would show signal
Expected outcome              what success/failure looks like
Core Claims / Novelty Check   one line per claim plus its exact search question,
                              closest verified work, remaining delta, limitation,
                              and novel/partial/preempted/inconclusive/unverified status
                              📮 → /haipipe-ideation pressure-test + Discovery Search Run/Result
Pilot result                  POSITIVE/NEGATIVE/SKIPPED + the receipt
                              📮 → task-layer Run/Result, or an explicit waiver
Journal / Venue Fit           broad screen for every admitted idea; deep fit
                              for live finalists; candidate targets, article
                              type, desk risks, missing evidence, reroute,
                              current Venue contract, and machine recommendation
                              📮 → /haipipe-ideation venue-fit
Risk                          what could sink it
Reviewer's likely objection   the strongest counterargument
Recommendation                the machine's PROCEED/CAUTION/ABANDON with reasons;
                              the table's verdict cell is the person's answer to it
```

A retrofit page fills only the fields its receipts support and marks the rest
`⬜`; inventing history is worse than a visible blank.

For retrofit novelty, split a flat Core Claims block only where the inherited
text already states distinct claims. Reuse an archived Result only when its exact
question tests the matching claim; otherwise print `unverified` and route a
new Discovery check. Do not convert one old blob-level novelty verdict into
several claim-level passes.

## 🔬 Core Claims, checked one by one

An idea is never novelty-checked as a blob. Its division states 3-5 Core
Claims that would need to be novel; each claim is checked separately and the
table's novelty cell records the WORST of them:

```text
claim → multi-source search (≥3 query shapes · recent-years window)
      → closest prior work + the delta, per claim
      → every cited prior work verified by id/DOI before it enters the page
```

The visible claim table preserves the semantic executor's fields:

```text
claim · search question · closest verified work · remaining delta · limitation · status · Result path
```

"Applying X to Y" is not novel unless the application would reveal a
surprising finding; when the method is not novel but the finding would be, the
division says so explicitly. A prior-work citation that cannot be resolved is
written `[UNVERIFIED]`, never silently trusted. (Discipline adopted from the
ARIS `novelty-check` reference and from this workspace's own
fabricated-citation incidents.)

## 🃏 The page records; it never executes

The Ideation Page is a consumer. Searching, reading, and piloting are
Task/Discovery-layer work, and their receipts are Run/Result records this page binds by
path:

```text
Core Claims lines   ← /haipipe-ideation pressure-test + Discovery Search Run/Result
Ideas + divisions   ← /haipipe-ideation synthesize → Idea Cards + handoff
Pilot result        ← task-layer Run/Result (small, budgeted, disposable run)
Journal/Venue Fit   ← /haipipe-ideation venue-fit → Fit Card + Venue contract
```

The standing semantic executor for both idea lanes is `/haipipe-ideation`.
External prior-work retrieval routes through `/haipipe-discovery-search`, and
feasibility routes through the Task owner. The historical ARIS `idea-creator`
and `novelty-check` skills (Tools/references/aris) remain methodology
references: their output enters this page only after it has become an ideation
card or a discovery-/task-layer Run/Result, never by direct write.

Two grain adapters, because the executor speaks per-idea and this page reads
per-claim: (1) claim-level novelty is achieved by DISPATCH GRAIN — each claim
is commissioned as its own bounded question, so each gets its own Run/Result, matching
the discovery layer's one-question-one-file law; (2) the executor's
novelty_check vocabulary maps onto the page's reading as
`novel → HIGH · partial → MEDIUM · preempted → LOW · inconclusive → stays ⬜
(or [UNVERIFIED] when the prior work would not resolve)`, and the novelty
cell keeps recording the WORST claim.

A pilot is a feasibility receipt, not a result: budget it small, time-box it,
and record a failed pilot as honestly as a passed one. A cell asserting a
verdict with no Result path behind it is a defect.

Existing regressions may be read as a retrospective pilot only through a
Task-owned Run/Result receipt that names the bounded minimum experiment, exact output
paths and execution provenance, acceptance reading, and positive/negative
result. An inherited `SKIPPED` line or manuscript claim does not satisfy G0;
it needs that retrospective receipt, a new pilot, or an explicit human waiver.

## 🎓 Sending selected ideas to Stories

An idea's row may name a Story in `went to` only when all four hold:

- its Core Claims each carry a novelty reading from an independent context,
- its Pilot result binds a feasibility receipt (or records an explicit,
  reasoned waiver),
- its Venue Fit Card has a retained broad screen, complete deep fit against a
  current Venue contract, and the row names the person's intended
  target/category,
- a person has ticked PROCEED on that row, or PROCEED WITH CAUTION with its
  named risk accepted in the tick — the machine writes only the
  Recommendation field; the verdict is human, and eliminated ideas never
  leave.

It is a two-way act: `went to` names the Story — normally `Story-A`, `Story-B`,
and so on beside this page, or the new repo when an idea leaves for a DIFFERENT
paper — and that Story's C5 Source Pages and provenance subsection binds THIS page and its
ideation handoff back. A row naming a Story that does not bind back, or a
Story claiming an origin this page does not show, is a defect on whichever
side is missing.

Selection is per idea, not per comparison table. A person may select none,
one, or several candidates; every selected candidate receives one distinct
Story and passes G0 independently. The page never needs to declare one global
best idea.

## ✋ Human authority

A machine may generate ideas, run searches and pilots through the proper
layers, fill Core Claims lines, build Venue Fit Cards, and recommend target
options. It may not tick a verdict, select a target/category, eliminate or
defer an idea, or send a selected idea to a Story. Killing, deferring,
targeting, and committing are all human acts.

Gate G0 (Ideation → Story; historical Seed wording remains readable) is tested
on each selected idea's summary row and ticked by
a person; its workflow receipt belongs to this Page's process records and
states the gate, assertion results, and who ticked. It is not a top-level
`## Log` section on the reader-facing Page.

G0 is not the Page CHECK gate. A current Page version may be accepted while no
Idea is selected, and a previously selected Story may remain valid while a
later Page version adds, defers, or eliminates other candidates.

## ✅ Closing checks

- Division 1 names one direction and what would make an idea worth a paper.
- The Page Face contains Opening, Outline, Content, and Aims; Outline and
  Content are the primary working surfaces.
- Page Shape approval, Page CHECK acceptance, and per-Idea G0 selection remain
  three distinct human receipts; none is inferred from another.
- The number of Idea divisions is dynamic; every admitted Idea Card has one
  retained division, filled or honestly `⬜`.
- Every Eliminated Ideas row states whether it is an admitted `iNN` card or a
  rejected pre-admission framing; only admitted cards owe retained divisions.
- Every row in Ideas (ranked) has no blank cell; every verdict is from the
  fixed vocabulary; every batch names its source IDEA_REPORT, or the page
  states why none exists.
- Comparison order is not treated as selection; only the human verdict and
  `went to` authorize a Story.
- Every idea division carries the report's fields, filled or honestly `⬜`.
- Every Core Claims / Novelty Check line traces to a per-claim Run/Result; every
  cited prior work is verified or marked `[UNVERIFIED]`.
- Every Pilot result binds a Result path or an explicit waiver.
- Every admitted Idea has a broad Venue screen; every selected Idea has a
  complete deep fit, current Venue contract, and human-selected target/category.
- Every non-open human verdict carries a person's tick and date.
- Every `went to` names a distinct Story that binds this page back.
- Historical SD-named instances preserve their paths unless an explicit
  migration is authorized; canonical roles and two-way bindings remain clear.
- Eliminated Ideas holds every idea ever dropped, each with its reason;
  nothing raised has vanished.

This variant owns no scripts. The generic Page template and workflow own the
frame, plugins, receipts, and lifecycle.
