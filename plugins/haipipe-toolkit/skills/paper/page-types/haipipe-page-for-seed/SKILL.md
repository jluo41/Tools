---
name: haipipe-page-for-seed
description: >-
  The Paper Page Type for one venue-free Seed per paper. It establishes the
  stable research identity, the BLUF pitch with placeholder discipline, the
  research question, stakes, read scope, the Establishment Board of defensible
  propositions, boundaries, and a bounded handoff to venue-specific
  Narratives. Use when starting a paper, repairing its identity, telling the
  one-minute story, checking what the evidence licenses, separating the paper
  from venue framing, or retargeting without rewriting what the study is.
  Trigger: seed page, paper identity, pitch, one-minute story, establishment
  board, what can we claim, page-type seed, /haipipe-page-for-seed.
metadata:
  version: "0.5.1"
  last_updated: "2026-08-27"
  summary: "0.5.1 (JL 260827): gate-receipt duty sunk from the workflow's receipts law into this contract — G1's and G4's receipt Log rows live on this page. 0.5.0 (JL 260824): journey 0.5.0 story order — the story group becomes the venue-free P0-P3 head (SD00-ideation, SD01-seed, SD02-roadmap, SD03-collection) and Narratives move out to A2-NA-narrative; the Seed is the establish loop's scoreboard: Roadmap plans against its §6 gaps, Collection proposes settles, and this page alone writes E-row flips, each citing the landed QA path. 0.4.4 (JL 260824): ideation 0.5.0 vocabulary — the origin page's cell is `went to` (was graduated-to), 'ledger/nursery/graduation' wording dropped from the birth-certificate clause and checks. 0.4.3 (JL 260824): ideation joins the story group as page zero — the seed is SD01-seed, its birth certificate binds SD00-ideation beside it. 0.4.2 (JL 260824): explore renamed IDEATION — §5's first row points at this board's ideation page. 0.4.1 (JL 260823): the birth certificate binds same-board by default; cross-repo only when the idea came from another paper's nursery. 0.4.0 (JL 260823): every ✅/🔨 E-row carries a novelty reading (closest prior · delta · H/M/L, claim-level per the ARIS lesson); §5's first row binds the Explore Page that graduated this paper as its birth certificate; runtime home renamed to paperboard/A1-SD-story (old boards grandfathered). 0.3.0 re-cut the shape (JL 260821): BLUF pitch at division 2, Establishment split from Boundaries, Source Pages named the PageX seedbed."
  group-token: "SD"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Identity → Pitch → Research Question → Stakes → Source Pages → Establishment Board → Boundaries → Narrative Handoff"
---

# /haipipe-page-for-seed · establish what the paper is

Load `haipipe-page` first and `haipipe-page-workflow` when running the Page.
Declare `page-type: seed`. In a runtime paper board this page lives at
`0-paperboard/A1-SD-story/SD01-seed/`, second page of the venue-free story
group it shares with its Ideation origin and the establish loop's two working
pages (journey 0.5.0, JL 260824; older boards with narratives inside this
group are grandfathered):

```text
0-paperboard/A1-SD-story/
├── SD00-ideation/                the ideas this paper came from
├── SD01-seed/                    what the paper IS · venue-free · exactly one
├── SD02-roadmap/                 where to go next · plans against §6's gaps
└── SD03-collection/              what came back · proposes the settles
```

The group law: the story group is the paper's venue-free head (P0–P3); no
manuscript prose and no venue word lives here — the tellings start next door
in `A2-NA-narrative/`. In the establish loop this page is the SCOREBOARD:
the Roadmap plans, the Collection registers, and the Seed ALONE writes E-row
flips, each flip citing the landed QA path the other two pages carry.

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

### 3 · Research Question     🔒 STABLE
primary RQ · answer form · secondary RQs only when indispensable

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
status, and the §5 asset it rests on. The board is FLAT and UNRANKED — no row
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
files whose cited papers are id-verified. A row selling HIGH novelty on an
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
Page, §5's first row binds that page through `pagex/` — normally `SD00-ideation`
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
