---
name: haipipe-paper-story
description: >-
  Paper journey phase P1 (Story) and the Page Type contract for the STORY
  PAGE, Story<NN>-<idea-slug>: one idea, one paper, one control center. It
  carries the paper's venue-free identity (the Seed: identity, pitch, stakes,
  boundaries), the Research Question table that drives the work, the
  Establishment Board that records what came back, and the handoff to its two
  child plans (roadmap = collect, narrative = show). Use when starting a paper,
  telling its one-minute story, reading where one idea stands, or retargeting
  to a new venue without rewriting the study. Trigger: story page, seed page,
  paper identity, research questions, pitch, establishment board, page-type
  story, page-type seed.
metadata:
  version: "0.8.0"
  last_updated: "2026-09-07"
  group-token: "Story<NN>"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Identity → Pitch → Research Questions → Stakes → Source Pages → Establishment Board → Boundaries → Narrative Handoff"
---

# /haipipe-paper-story · one idea, one page: what the paper is and what it asks

Load `haipipe-page` first and `haipipe-page-workflow` when running the Page.
Declare `page-type: story` (`page-type: seed` is the 0.7.x alias and still
resolves here). In a runtime paper board this page IS the Story page:
`A1-Story/Story<NN>-<idea-slug>/Story<NN>-<idea-slug>.md` (0.8.0, JL 260907:
one Story = one idea; the number is the idea counter, `Story01` is the first
idea that survived the pool).

## 🧭 What the Story page IS

```text
Story<NN>-<idea-slug>.md      the one address for one paper
├── the Seed                  §1 Identity · §2 Pitch · §4 Stakes · §7 Boundaries
│                             what the paper IS and is NOT · venue-free · 🔒 stable
├── the Research Questions    §3 · what we go out to explore · ⬜/🔨/✅ · drives the roadmap
├── the Establishment Board   §6 · what came back, one E-row per RQ · 🔥 volatile
├── Source Pages + Handoff    §5 · §8 · what it may read · the packet its narrative child opens
└── two child pages           Story<NN>-roadmap (plan to COLLECT) · Story<NN>-narrative-<desk> (plan to SHOW)
```

The Story page CONTROLS and never DOES: it holds no manuscript prose, no venue
word, no run. Its §3 table is the control view: the `collect` column is written
by the roadmap child and the `show` column by the narrative child, so reading
one page tells you what is asked, what is running, what came back, and where
each answer is shown. "Seed" survives as the name of the identity divisions
(§1, §2, §4, §7) and of the establish loop's scoreboard role; it is no longer
a page of its own. Its two children, `Story<NN>-roadmap/` and
`Story<NN>-narrative-<desk>/`, sit inside its folder. Older boards with a flat
`Story01-seed/` beside `Story02-roadmap/` are grandfathered:

## 🧭 Journey phase

This skill is journey phase P1 Story (establish; "Seed" was the 0.5–0.7 phase name) of the paper journey and owns
the `page-type: story` contract below (`seed` accepted as alias). Enter through gate G0. Two exits: G1
opens the Roadmap (the establish loop P1↔P2), and G4 (the loop's ONLY exit)
opens the first Narrative. The Seed alone writes E-row flips; the Roadmap only
proposes settles. `haipipe-paper-workflow` holds the full gate assertions; this
block only places the phase. The page itself always runs through
`/haipipe-page` and `haipipe-page-workflow` (OUTLINE → … → CHECK), never a
private lifecycle.

```text
A1-Story/
├── Story00-ideation/                 the pool the idea came from
└── Story<NN>-<idea-slug>/            THIS PAGE · what the paper IS · venue-free
    ├── Story<NN>-roadmap/            child · plan to COLLECT · fills the RQ
    │                                 table's "collect" column · proposes settles
    └── Story<NN>-narrative-<desk>/   child · plan to SHOW · one per desk · fills
                                      the RQ table's "show" column
```

The group law: the Story page and its roadmap child are venue-free; no
manuscript prose and no venue word lives in them. A venue enters the Story only
through a narrative child. In the establish loop this page is the SCOREBOARD:
the Roadmap plans and registers, and the Seed ALONE writes RQ states and E-row
flips, each flip citing the landed QA path the Roadmap's lap carries.

## 🌱 Grain and boundary

There is exactly one Seed per paper. It survives retargeting unchanged.

```text
Seed       what the work is; venue-free
Venue      what one external desk requires
Narrative  how this work is told to that desk
Section    how one Narrative row becomes manuscript content
```

Seed must not name a selected venue, editor, target audience, venue-specific
pitch, section order, or submission rule. If changing the target desk requires
changing Seed, the boundary has leaked.

## 📐 Fixed Content outline

Use these eight divisions in order. A title may add a paper-specific phrase
after the fixed role. Each division carries a LIFETIME, and the lifetimes are
the retargeting law made checkable: a diff outside the 🐢/🔥/♻️ divisions is
identity drift and must be explained.

```text
### 1 · Identity              🔒 STABLE
working title · one-sentence identity · unit of analysis · scope

### 2 · Pitch                 🎤 BLUF · re-opens when a cited row flips
the one-minute story: hook → what we did → what we found → who should care

### 3 · Research Questions    🔒 question text STABLE · 🔥 state column VOLATILE
one row per question the paper goes out to explore: RQ<n> · the question ·
⬜ open / 🔨 exploring / ✅ answered · collect (roadmap block) · show
(narrative section) · answer form stated once above the table

### 4 · Stakes                🔒 STABLE
real-world problem · intellectual problem · why this study is worth finishing

### 5 · Source Pages          🐢 SLOW · the PageX seedbed
one row per asset: page/file id · what it may be read for

### 6 · Establishment Board   🔥 VOLATILE · the only frequently-moving division
one row per proposition: E<n> · ✅ established / 🔨 provisional / ⬜ absent
· cites a §5 asset by id

### 7 · Boundaries            🔒 STABLE
hard limits · non-claims · what the paper will NOT assert

### 8 · Narrative Handoff     ♻️ DERIVED · assembled from 1–7, licenses nothing new
the smallest typed packet from which any venue-specific Narrative can begin
```

## ❓ The Research Question table · division 3 (0.7.0 · JL 260907)

A Research Question is a QUESTION the paper goes out to explore. It is not a
hypothesis: a hypothesis asserts an answer, an RQ sends the roadmap out to get
one. The table is the Story's control center, and it is why the Story page is
the paper's one address: read it and you know what is being asked, what is
running, what came back, and where each answer is shown.

```text
id    the question we go explore                     state        collect          show
RQ1   Does X predict Y beyond Z?                     ✅ answered   B1 · done        S-<desk>-Main-Results
RQ2   Does the effect survive the stricter FE?       🔨 exploring  B2 · running     S-<desk>-Appendix-Robustness
RQ3   Does it hold in a pooled interaction test?     ⬜ open       B3 · not started (not allocated)
```

The state is about the QUESTION, never about how strong the answer turned out:
⬜ open means named and nobody is on it, and a ⬜ row is an instruction to the
roadmap child; 🔨 exploring means a block is running; ✅ answered means a result
is back, and an ✅ row is an obligation for the narrative child. Whether the
answer supports or refutes belongs to the Establishment Board, one E-row per
RQ, so every RQ has exactly one E-row and the two ids appear side by side.
The `collect` column is written by the roadmap child (its block id and state);
the `show` column is written by the narrative child (the Section page that
carries the answer). The Seed alone flips the state. The question text is
STABLE: rewording a question is identity drift and must be explained on the
Log; adding a question is a new row, never a rewrite.

## 🎤 The Pitch · division 2

BLUF, bottom line up front: the reader gets the story before the machinery.
The pitch is spoken prose, roughly 150 words, in four moves: the tension
(from Stakes), the study in a clause (from Identity), the headline finding
(from ✅ Establishment rows), and who should care (from Stakes). It is the
GENERAL listener's telling; each Narrative writes its own desk-shaped opening,
and a pitch that changes when the target desk changes belongs there, not here.

**The placeholder discipline is what makes day-1 BLUF honest.** Every sentence
that sells a finding either cites an `✅ E<n>` row or carries an explicit
placeholder naming the row it waits on:

```text
day 1   "...and found ⟦FOUND · pending E1⟧. If it holds, ..."
mid     E1 flips ✅  ──▶  the slot fills with the number, citing E1
done    zero placeholders · every sold sentence cites an ✅ row
```

A pitch selling a 🔨 or ⬜ row as fact is a defect. A visible placeholder is
honest, and a Seed whose pitch still holds placeholders is a paper that has
not yet found its bottom line. The pitch compiles to a standalone `pitch.tex`
through the page's `latex/` plugin when a shareable copy is needed.

## 📊 The Establishment Board · division 6

One row per proposition the paper could defend: a one-sentence claim, its
status, the §5 asset it rests on, and the §3 Research Question it answers
(0.7.0: one E-row per RQ, the RQ id is a column, so the forward question and
the backward record read as one line). The board is FLAT and UNRANKED — no row
is crowned the headline here, because ranking answers "important to whom?"
and that names a desk. Each Narrative selects and orders from this board for
its own target; the pitch's lead is the one exception, and it is the general
listener's, not a desk's.

```text
E1  ✅ established   <one-sentence proposition>        cites S2 (W01 handoff)
E2  🔨 provisional   <proposition · missing obligation> cites S4 (QA file)
E3  ⬜ absent        <proposition nobody can yet assert> —
```

A row may be WEAK and still belong; what it may not do is appear in the pitch
or the handoff with a status it does not have. Evidence changing flips rows
here and nowhere else: this division is why the rest of the Seed can be
stable.

**Every ✅ and 🔨 row also carries its novelty reading** (0.4.0): the closest
prior work, the delta against it, and a HIGH/MEDIUM/LOW call — judged at the
CLAIM level, never for the paper as a blob, and traced to discovery-layer QA
files whose cited papers are id-verified. The H/M/L call reads the discovery
layer's own verdicts through the fixed adapter (novel → HIGH · partial →
MEDIUM · preempted → LOW · inconclusive → stays ⬜; ideation 0.4.1's table,
restated here because the settle pen is this page's). A row selling HIGH
novelty on an
unresolved citation is a defect; `[UNVERIFIED]` is honest, silence is not.
The board's novelty column is what makes "is this idea any good?" a readable
property instead of an opinion: idea quality = how many rows can flip ✅ and
what their deltas are worth.

## 🔗 Source Pages and PageX · division 5

Division 5 is the paper's READ SCOPE: which existing pages, task outputs and
discovery QA files this paper may draw from, one row per asset with what it
may be read for. It exists because at paper start assets outnumber
propositions — material not yet formed into any E-row needs a home, and the
PageX scan needs prose to seed from.

```text
outline bullet (source: page) ──▶ pagex/ binds the file ──▶ §5 rows it ──▶ §6 cites it
```

Probe's `pagex/` lane binds exactly what §5 rows, by path and bounded scope,
during OUTLINE. An asset in `pagex/` with no §5 row, or a §6 citation naming
an asset §5 does not row, is a defect.

**The birth certificate** (0.4.0): when this paper came from an Ideation
Page, §5's first row binds that page through `pagex/` — normally `Story00-ideation`
beside this page in the story group, cross-repo only when the idea
left ANOTHER paper's ideation page — and that page's `went to` cell
points back here. A Seed claiming no origin when an ideation page names it, or naming
an origin whose page does not show the exit, is a defect on whichever
side is missing. A retrofit Seed (paper predates the ideation page) states that in
its Log instead.

## 🃏 Evidence rule

Seed is not evidence-free. If it states a factual proposition — sample
coverage, the existence of a gap, or a headline association — it must bind
that statement to Page-local evidence.

- Probe routes existing accepted Board Pages through its `pagex/` lane.
- Probe routes unresolved Task/Discovery questions into QA cards in `probe/`.
- Citations live in `bibex/`.
- A display is allowed when it materially clarifies identity, scope, or
  establishment; it lives in `display/` and has its own acceptance state.

Do not copy raw evidence into the handoff. Hand off ids, status,
interpretation, and boundaries.

## 📤 The Narrative Handoff · division 8

Derived last, assembled from everything above, and the only division a
Narrative may bind:

```text
identity          one sentence
primary RQ        one answerable sentence
stakes            practical + intellectual
established       E<n> ids with ✅ status and source ids
provisional       E<n> ids with 🔨 status and missing obligations
hard boundaries   what the paper will not claim
open tensions     what Narrative must order rather than silently settle
```

Gates G1 (Seed → Roadmap) and G4 (Seed → Narrative) both read this page;
each gate's receipt Log row lives here, stating the gate, the assertion
results, and who ticked.

## ✅ Closing checks

- One identity and one primary RQ are visible.
- Every pitch sentence selling a finding cites an ✅ E-row or carries an
  explicit `⟦pending E<n>⟧` placeholder naming a real row.
- Every E-row is marked established, provisional, or absent, and cites a §5
  asset by id (⬜ rows may cite nothing).
- Every ✅/🔨 E-row carries a claim-level novelty reading with a verified
  closest-prior citation or an explicit `[UNVERIFIED]` mark.
- The Ideation origin is bound in §5 and reciprocated by that page, or the
  Log states the Seed is a retrofit.
- Every §5 asset is bound in `pagex/`, and `pagex/` holds nothing §5 does
  not row.
- The Establishment Board is unranked: no headline marker, no importance
  order.
- The handoff can seed more than one venue-specific Narrative.
- No venue, editor promise, venue-specific audience, or manuscript prose
  leaked into the Page.
- The current outline is approved and CHECK closes the built Seed version.

This variant owns no scripts. The generic Page template and workflow own the
frame, plugins, receipts, and lifecycle.
