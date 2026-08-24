---
name: haipipe-page-for-explore
description: >-
  The Paper Page Type for one research DIRECTION's exploration ledger: the
  nursery where candidate ideas are generated, novelty-checked claim by claim,
  feasibility-piloted, and killed or graduated, before the paper's Seed exists.
  One page per direction at the head of the paper's own board
  (paperboard/A0-EX-explore/), minted with the repo; ideas are cheap and
  disposable, the ledger is not. Use when brainstorming a direction, checking
  whether an idea has been done, recording a pilot, killing an idea, or
  graduating one into a new paper's Seed. Trigger: explore page, idea ledger,
  find ideas, brainstorm, novelty check, has this been done, kill this idea,
  graduate to seed, page-type explore, /haipipe-page-for-explore.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-23"
  summary: "0.2.0 moves the nursery home (JL 260823): the explore page lives at the head of the paper's OWN board, paperboard/A0-EX-explore/, before the seed — the repo is minted with the explore page, the same locality law that puts an InsightBoard inside its application; the standing IdeaBoard is retired. 0.1.0 created the P0 nursery page: idea ledger with claim-level novelty and pilot receipts; graduation gate to a Seed; ABANDONED rows never deleted; methodology informed by the ARIS idea-discovery reference (Tools/references/aris)."
  group-token: "EX"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "division 1 is Direction, division 2 is Idea Ledger; every later division's first word is an idea id i<n>, in id order; Graduations is last"
---

# /haipipe-page-for-explore · run the nursery one direction at a time

Load `haipipe-page` first and `haipipe-page-workflow` when running the Page.
Declare `page-type: explore`.

## 🌱 Grain and home

One Explore Page holds ONE research direction and every candidate idea raised
under it. It lives at the HEAD of the paper's own board, before the Seed —
the same locality law that puts an InsightBoard inside its application:

```text
Paper-<Slug>/paperboard/
├── A0-EX-explore/
│   └── EX01-<direction-slug>/     one direction, many ideas, one ledger
└── A1-SD-story/                    the Seed this nursery graduates into
```

**The repo precedes the Seed** (0.2.0): minting a paper's first Explore Page
is what creates `Paper-<Slug>/` — as a git submodule immediately, per the
scaffold rule — with only `paperboard/A0-EX-explore/` inside. The slug may
start as the direction's name; a direction that dies leaves the repo standing
as its own graveyard. A second EX page on one board is legal only when the
direction genuinely forks and the fork stays this paper's.

The page is EVERGREEN (♻️): it never closes while the direction is alive.
Ideas on it are cheap — generated in batches, ranked, killed without ceremony.
What is never cheap is the ledger row: a killed idea's row stays forever,
because the graveyard is what stops the same idea being re-thought in new
words six months later.

## 📐 Content outline

```text
### 1 · Direction            🔒 what question space, why now, what would make
                                any idea here worth a paper
### 2 · Idea Ledger          🔥 the whole nursery in one screen · one row per idea
#### 3 · i1 · <slug>         one division per candidate, in id order
#### 4 · i2 · <slug>
### N · Graduations          ♻️ who left, when, to which Seed
```

## 📊 The Idea Ledger · division 2

One row per candidate, every column a state and never a blank:

```text
id  idea (one line)         claims  novelty            pilot        verdict         graduated-to
────────────────────────────────────────────────────────────────────────────────────────────────
i1  <one sentence>          3       HIGH · closest:    ✅ QA path   ✅ PROCEED      SD00 (here) ·
                                    <prior> · delta:                 (JL 260823)    or Paper-<Other>
i2  <one sentence>          4       LOW · <prior>      —            🚫 ABANDONED    —
i3  <one sentence>          —       ⬜ unchecked        —            ⬜ open         —
```

Verdict vocabulary: `⬜ open`, `✅ PROCEED`, `⚠️ CAUTION` (proceed with named
risk), `🚫 ABANDONED` (reason in the division), `🔀 MERGED → i<m>`. ABANDONED
and MERGED rows are never deleted. A `—` cell is legal only where the verdict
makes the column moot (an ABANDONED row's pilot, an open row's graduated-to);
on a live row every cell is a state or a bound path.

## 🔬 Claim-level novelty, not paper-level

An idea is never novelty-checked as a blob. Its division first states 3-5 core
claims that would need to be novel; each claim is checked separately and the
ledger's novelty cell summarizes the worst of them:

```text
claim → multi-source search (≥3 query shapes · recent-years window)
      → closest prior work + the delta, per claim
      → every cited prior work verified by id/DOI before it enters the page
```

"Applying X to Y" is not novel unless the application would reveal a surprising
finding; when the method is not novel but the finding would be, the division
says so explicitly. A prior-work citation that cannot be resolved is written
`[UNVERIFIED]`, never silently trusted. (Discipline adopted from the ARIS
`novelty-check` reference and from this workspace's own fabricated-citation
incidents.)

## 🃏 The ledger records; it never executes

The Explore Page is a consumer. Searching, reading, and piloting are
Task/Discovery-layer work, and their receipts are QA files this page binds by
path:

```text
novelty cell     ← discovery-layer Search/Review QA files
ideation batch   ← discovery-layer Idea QA files
pilot cell       ← task-layer QA file (small, budgeted, disposable run)
```

A pilot is a feasibility receipt, not a result: budget it small, time-box it,
and record a failed pilot as honestly as a passed one. A cell asserting a
verdict with no QA path behind it is a defect.

## 🎓 The graduation gate

One row may graduate to a Seed only when all three hold:

- its novelty cell carries a per-claim verdict from an independent context,
- its pilot cell binds a feasibility receipt (or records an explicit,
  reasoned waiver),
- a person has ticked PROCEED on that row, or CAUTION with its named risk
  accepted in the tick — the machine reports PROCEED/CAUTION/ABANDON as a
  recommendation; the verdict is human, and ABANDONED or MERGED rows never
  graduate.

Graduation is a two-way act: the ledger's `graduated-to` names the Seed —
normally `SD00` on this same board, or the new repo when an idea leaves for a
DIFFERENT paper — and that Seed's §5 binds THIS page through `pagex/` as its
birth certificate. An Explore Page with a graduated row and no back-binding
Seed, or a Seed claiming an origin this ledger does not show, is a defect on
whichever side is missing.

## ✋ Human authority

A machine may generate ideas, run searches and pilots through the proper
layers, fill novelty cells, and recommend verdicts. It may not tick PROCEED,
ABANDON a row, or graduate one. Killing an idea is as human an act as
committing to it.

## ✅ Closing checks

- Division 1 names one direction and what would make an idea worth a paper.
- Every ledger row has no blank cell; every verdict is from the fixed
  vocabulary.
- Every novelty cell traces to per-claim QA files; every cited prior work is
  verified or marked `[UNVERIFIED]`.
- Every pilot cell binds a QA path or an explicit waiver.
- Every PROCEED/ABANDONED verdict carries a person's tick and date.
- Every graduated row names its Seed, and that Seed binds this page back.
- ABANDONED and MERGED rows are all present; nothing raised has vanished.

This variant owns no scripts. The generic Page template and workflow own the
frame, plugins, receipts, and lifecycle.
