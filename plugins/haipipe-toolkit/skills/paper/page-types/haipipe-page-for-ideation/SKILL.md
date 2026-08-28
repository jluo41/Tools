---
name: haipipe-page-for-ideation
description: >-
  Paper Page Type for one research direction's ideas, before any paper's Seed
  exists: generate and rank ideas, novelty-check them, record pilots, then
  eliminate or send one to a Seed. Use when brainstorming a direction or
  checking whether an idea has been done. Trigger: ideation page, find ideas,
  brainstorm, novelty check, page-type ideation.
metadata:
  version: "0.5.4"
  last_updated: "2026-08-28"
  group-token: "SD"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "division 1 is Direction, division 2 is Ideas (ranked) with a source bullet naming each IDEA_REPORT it drew from; every later idea division is titled Idea <n>: <title>, in rank order, carrying the report's own fields (Method · Hypothesis · Minimum experiment · Expected outcome · Core Claims · Pilot result · Risk · Reviewer's likely objection · Recommendation); Eliminated Ideas and then Suggested Execution Order close the page (a retrofit page may nest its single idea under division 2)"
---

# /haipipe-page-for-ideation · one direction's ideas, in the reports' own words

Load `haipipe-page` first and `haipipe-page-workflow` when running the Page.
Declare `page-type: ideation`.

## 🌱 Grain and home

One Ideation Page holds ONE research direction and every candidate idea raised
under it. It is the story group's PAGE ZERO (0.4.0) — no separate group; it
sits in the same group as the Seed its best idea becomes, before it:

```text
Paper-<Slug>/0-paperboard/
└── A1-SD-story/                    the venue-free P0-P2 head (journey 0.6.0)
    ├── SD00-ideation/              one direction, its ideas, ranked
    ├── SD01-seed/                  what the winning idea became
    └── SD02-roadmap/               where the campaign goes next, and what
                                    it brought back
```

(The tellings live next door in `A2-NA-narrative/`, one page per desk.)

**The repo precedes the Seed** (0.2.0): minting a paper's Ideation Page is
what creates `Paper-<Slug>/` — as a git submodule immediately, per the
scaffold rule — with only `0-paperboard/A1-SD-story/SD00-ideation/` inside.
The direction's name may seed the repo slug; a direction that dies leaves the
repo standing as its own record. **A board holds exactly ONE ideation page**
(the journey fixes the story group's roles, one each): a direction that
genuinely forks is a new direction, so it mints its own `Paper-<Slug>/` with
its own `SD00-ideation`, and the two pages cross-reference through the
originating row's `went to`. Before 0.5.0 a fork could take "the next free SD
number"; that reading died when the journey fixed every SD number's role.

The page is EVERGREEN (♻️): it never closes while the direction is alive.
Ideas are cheap — generated in batches, ranked, eliminated without ceremony.
What is never cheap is the row: an eliminated idea's row stays forever,
because the record is what stops the same idea being re-thought in new words
six months later.

## 📐 Content outline · the source reports' structure

The divisions mirror IDEA_REPORT.md (idea-creator) section for section, with
the Novelty Check Report's Core Claims folded into each idea's division:

```text
### 1 · Direction                    🔒 the research direction · why now ·
                                        what makes an idea here worth a paper
### 2 · Ideas (ranked)               🔥 summary table, one row per live idea
                                        · one source bullet per IDEA_REPORT drawn from
### 3 · Idea 1: <title>              one division per idea, in rank order,
                                        the report's own fields (list below)
### 4 · Idea 2: <title>
### N-1 · Eliminated Ideas           ♻️ the report's table: | Idea | Reason eliminated |
                                        rows permanent
### N · Suggested Execution Order    ♻️ what to do first · who went to which Seed
```

A retrofit page whose single idea already became the paper may nest that idea
under division 2 (`#### 2.1 · Idea 1: <title>`); the field list still applies
inside it.

## 📊 Ideas (ranked) · division 2

The summary table, one row per live idea, every cell a state and never a
blank:

```text
id  idea (one line)                  novelty            pilot           verdict              went to
────────────────────────────────────────────────────────────────────────────────────────────────────
i1  <one sentence>                   HIGH · closest:    ✅ QA path      ✅ PROCEED           SD01 (here) ·
                                     <prior>                            (JL 260823)          or Paper-<Other>
i2  <one sentence>                   ⬜ unchecked        —               ⬜ open               —
```

Verdict vocabulary — the Novelty Report's own recommendation words, decided
by a person: `⬜ open`, `✅ PROCEED`, `⚠️ PROCEED WITH CAUTION` (the named
risk accepted in the tick), `🚫 ABANDON`. An abandoned or merged idea moves
its row to Eliminated Ideas with its reason; its division stays as history. A
`—` cell is legal only where the verdict makes the column moot; on a live row
every cell is a state or a bound path.

Each batch of ideas enters through a source bullet naming the IDEA_REPORT (or
ideas.md) and QA file it came from; ideas do not appear from nowhere.

## 🧾 Each idea's division · the report's fields

One division per idea, titled `Idea <n>: <title>`, carrying IDEA_REPORT.md's
own field names — no translation layer:

```text
Method                        what we actually do, 2-4 concrete steps, plain language
Hypothesis                    one sentence
Minimum experiment            the smallest run that would show signal
Expected outcome              what success/failure looks like
Core Claims                   one line per claim: claim — HIGH/MEDIUM/LOW — closest work
                              📮 → /haipipe-discovery-idea novelty_check QA, one question per claim
Pilot result                  POSITIVE/NEGATIVE/SKIPPED + the receipt
                              📮 → task-layer QA, or an explicit waiver
Risk                          what could sink it
Reviewer's likely objection   the strongest counterargument
Recommendation                the machine's PROCEED/CAUTION/ABANDON with reasons;
                              the table's verdict cell is the person's answer to it
```

A retrofit page fills only the fields its receipts support and marks the rest
`⬜`; inventing history is worse than a visible blank.

## 🔬 Core Claims, checked one by one

An idea is never novelty-checked as a blob. Its division states 3-5 Core
Claims that would need to be novel; each claim is checked separately and the
table's novelty cell records the WORST of them:

```text
claim → multi-source search (≥3 query shapes · recent-years window)
      → closest prior work + the delta, per claim
      → every cited prior work verified by id/DOI before it enters the page
```

"Applying X to Y" is not novel unless the application would reveal a
surprising finding; when the method is not novel but the finding would be, the
division says so explicitly. A prior-work citation that cannot be resolved is
written `[UNVERIFIED]`, never silently trusted. (Discipline adopted from the
ARIS `novelty-check` reference and from this workspace's own
fabricated-citation incidents.)

## 🃏 The page records; it never executes

The Ideation Page is a consumer. Searching, reading, and piloting are
Task/Discovery-layer work, and their receipts are QA files this page binds by
path:

```text
Core Claims lines   ← /haipipe-discovery-idea novelty_check QA (or Search/Review QA)
Ideas + divisions   ← /haipipe-discovery-idea generate → IDEA_REPORT/ideas.md + QA
Pilot result        ← task-layer QA file (small, budgeted, disposable run)
```

The standing executor for both idea lanes is the discovery layer's Idea type
(`/haipipe-discovery-idea`). The ARIS `idea-creator` and `novelty-check`
skills (Tools/references/aris) are the methodology this wiring absorbed —
claim-level checking, verified citations, budgeted pilots, ranked batches —
and remain references: their output enters this page only after it has become
a discovery- or task-layer QA file, never by direct write.

Two grain adapters, because the executor speaks per-idea and this page reads
per-claim: (1) claim-level novelty is achieved by DISPATCH GRAIN — each claim
is commissioned as its own question, so each gets its own QA file, matching
the discovery layer's one-question-one-file law; (2) the executor's
novelty_check vocabulary maps onto the page's reading as
`novel → HIGH · partial → MEDIUM · preempted → LOW · inconclusive → stays ⬜
(or [UNVERIFIED] when the prior work would not resolve)`, and the novelty
cell keeps recording the WORST claim.

A pilot is a feasibility receipt, not a result: budget it small, time-box it,
and record a failed pilot as honestly as a passed one. A cell asserting a
verdict with no QA path behind it is a defect.

## 🎓 Sending an idea to a Seed

An idea's row may name a Seed in `went to` only when all three hold:

- its Core Claims each carry a novelty reading from an independent context,
- its Pilot result binds a feasibility receipt (or records an explicit,
  reasoned waiver),
- a person has ticked PROCEED on that row, or PROCEED WITH CAUTION with its
  named risk accepted in the tick — the machine writes only the
  Recommendation field; the verdict is human, and eliminated ideas never
  leave.

It is a two-way act: `went to` names the Seed — normally `SD01` beside this
page, or the new repo when an idea leaves for a DIFFERENT paper — and that
Seed's §5 first row binds THIS page back through `pagex/`. A row naming a
Seed that does not bind back, or a Seed claiming an origin this page does not
show, is a defect on whichever side is missing.

## ✋ Human authority

A machine may generate ideas, run searches and pilots through the proper
layers, fill Core Claims lines, and write Recommendation fields. It may not
tick a verdict, eliminate an idea, or send one to a Seed. Killing an idea is
as human an act as committing to it.

Gate G0 (Ideation → Seed) is tested on the idea's summary row and ticked by
a person; its receipt Log row lives here, stating the gate, the assertion
results, and who ticked (the workflow's receipts law, restated so the pen
that writes this page knows the duty).

## ✅ Closing checks

- Division 1 names one direction and what would make an idea worth a paper.
- Every row in Ideas (ranked) has no blank cell; every verdict is from the
  fixed vocabulary; every batch names its source IDEA_REPORT, or the page
  states why none exists.
- Every idea division carries the report's fields, filled or honestly `⬜`.
- Every Core Claims line traces to a per-claim QA file; every cited prior
  work is verified or marked `[UNVERIFIED]`.
- Every Pilot result binds a QA path or an explicit waiver.
- Every verdict carries a person's tick and date.
- Every `went to` names a Seed that binds this page back.
- Eliminated Ideas holds every idea ever dropped, each with its reason;
  nothing raised has vanished.

This variant owns no scripts. The generic Page template and workflow own the
frame, plugins, receipts, and lifecycle.
