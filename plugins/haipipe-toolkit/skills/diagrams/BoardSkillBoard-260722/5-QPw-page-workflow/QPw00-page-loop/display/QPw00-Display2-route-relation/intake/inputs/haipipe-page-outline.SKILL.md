---
name: haipipe-page-outline
description: >-
  The OUTLINE phase contract for any Board Page, and phase ① of the page workflow. OUTLINE agrees the SHAPE of a page before a word of it is written: the section list, the paragraph under each section, the bullets under each paragraph, and what each bullet still owes. Its deliverable is a versioned file at <page>/outline/<stem>-outline-v<N>.md, read on the 🧭 tab, and it exits only when a person ticks its approved: line. It writes no prose, lands no card, and dispatches no question. Load haipipe-page, the matching Page Type, this contract, then haipipe-plugin-outline for the file's own shape. Use when opening a new Page, when starting a new round after CHECK, when a plan must be agreed before expensive work, or when a page turned out to be built on a shape nobody approved. Trigger: page outline, OUTLINE phase, phase 1, plan the page, agree the shape, approve the outline, outline gate, v1 v2, supersedes, bullet, /haipipe-page-outline.
metadata:
  version: "0.6.0"
  last_updated: "2026-08-18"
  summary: "First contract, on JL's 260817 ruling that OUTLINE is a phase of the workflow rather than a step inside DRAFT. Takes the outline authority out of haipipe-page-draft."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-outline · agree the shape before writing a word of it

**LOAD `haipipe-page` FIRST**, then the Page Type, then this file, then `haipipe-plugin-outline` for the file's own shape. This contract owns the PHASE: its authority, its exit, and what it may not touch. The plugin owns the file and the tab, and this file never restates them.

## 🎯 The authority test

```text
owns       the SHAPE: which sections, which paragraphs, which bullets,
           and what each bullet still owes
may do     add · delete · move · rewrite, freely, while unapproved
exits      FOUR machine checks pass, THEN a person ticks `approved:`
           (the four are §🚦 below; the person judges DIRECTION, not arithmetic)
🚫 may not write prose · land a card · dispatch a question · invent a
           division the Page Type does not allow
```

## 📐 The Page Type's `outline:` block is READ, not assumed

**Every Page Type that exists already declares its mode.** All eleven do, in an
`outline:` block under `metadata:`. Until 260819 nothing in this phase read it,
so a plan's shape was whatever its author felt like:

```text
  mode: fixed      brief · dash · seed · venue · insight
                   the type LISTS the divisions. Fill them. Do not add, drop
                   or reorder.
  mode: grammar    intervention · narrative · task
                   a closed FIRST-WORD set plus an order rule. Choose how many
                   of each; write the free title after the fixed word.
  mode: resolved   artifact · stage · section
                   the outline lives OUTSIDE the type, at the path its `source:`
                   names. RESOLVE it first. A missing source is a HOLE, never
                   a licence to invent one.
```

**No `page-type:` key is the flexible DEFAULT** (`haipipe-page-draft` 0.7.3): the
plan then owes the base section order and nothing more. That is 247 of this
repo's 274 pages, so the common case is no check at all beyond the base.

**This is a machine-checkable exit, and it runs BEFORE the person is asked.** A
plan whose shape contradicts its declared type wastes the one gate that is
supposed to be cheap:

```text
  fixed     a division the type does not list, or a missing one   ❌ reject
  grammar   a first word outside the closed set, or an order the
            rule forbids                                          ❌ reject
  resolved  no `source:` resolved, or a shape copied from a
            sibling page instead                                  ❌ reject
```

`checks/outline.py` reports it as `plan-shape-off-type`. A rejection here is not a
finding against the person; it is the phase refusing to spend a human tick on a
shape a file already answered.

An operation does not identify OUTLINE. Adding a section to the PLAN is OUTLINE; adding a section to the PAGE is DRAFT. The two are different files.

## 🚧 Why this is a phase and not a step inside DRAFT

It was a step inside DRAFT until 260817, and the day it stopped being one is on the record. One phase owned both "agree the shape" and "write the page", so a single done-report covered both, and the plan ended up pasted into the page's own `## Content` where it immediately went stale (`QC1-visitlbp`, CMSRegBoard).

**The gate is the cheapest one on the board, which is the whole argument for it.**

```text
  change a section list   BEFORE the prose   one line
  change a section list   AFTER  the prose   the prose
```

A phase whose entire output fits on one screen, and which a person can reject in ten seconds, belongs in front of every expensive phase rather than folded into one.

## 🔁 The PREPARE loop, and why this phase repeats (260819)

Ruled by JL: "outline 之后就直接 probe 准备证据，基于证据我们再改 outline，直到
outline 自己是自洽的."

```text
  ┌── PREPARE · repeat until self-consistent ─────────────┐
  │   🧭 OUTLINE ──▶ 📮 PROBE ──▶ 🃏 EVIDENCE             │
  │       ▲                            │                  │
  │       └──── the answer changes the plan ───────────────┤
  └──────────────────────┬────────────────────────────────┘
                         ▼ 🚧 ONE gate: the plan AND its evidence
                     ✏️ DRAFT
```

**Evidence does not confirm a plan; it changes it.** That is the whole reason
this is a loop and not a line, and 260819 produced two worked cases on
`QPw00-page-loop`: a division the plan wanted turned out to score 0 of 4 on the
split tests and was folded away, and a count of 17 was recomputed as 13. Neither
was a defect. A plan written before its evidence is a guess.

## 🚦 Self-consistent means FOUR things, and each one is checkable

"Until the outline is self-consistent" has to be a test, or the loop cannot stop
and "it feels about right" becomes the gate. It is these four, in this order:

```text
  ① COVERAGE   the plan⇄disk join, BOTH directions. Forward: every mark is
               served by at least one card — the PROBE receipt already
               reports `coverage: n of n`. Reverse: every display unit on
               disk is cited by ≥1 bullet, or retired; an orphaned 🖼 is a
               COVERAGE failure, not a footnote (JL 260819, on seeing
               Display4 under "on disk, cited by no bullet": "you should
               try to make every display to be used")
  ② ADDRESS    every card's `serves:` names an address this plan really has
               ⚠️ three cards on QPw00 pointed at renumbered bullets on 260819
  ③ VALUE      every recomputable number matches the repo
               `checks/values.py`, and it caught 17-vs-13 on its first run
  ④ SHAPE      the plan's divisions match the Page Type's declared mode
               `plan-shape-off-type`; no `page-type:` key = base order only
```

**All four run BEFORE the person is asked.** That is what makes the human tick
worth something: a machine says the plan is consistent with what is on disk, and
the person answers the one question no file can, which is whether the plan is
aimed at the right thing.

**An answered ask is APPENDED, never re-asked and never re-bulleted** (JL
260819, on `📮 PP04 answered · 5 values`: "我们其实需要更新一下这个 bullet
points，把那 5 个 value 也列出来，这样的话就是有问有答"): when a bullet's card
lands its `## Values`, the SAME bullet gains the answer — prose quoting each
value id inline (`PP<NN>.v<n>` then the number and its meaning) — and the 📮
mark stays end-anchored. The ask and the answer live on one bullet; a new
bullet for the answer is wrong, and an asking bullet left answer-less after
its card landed is fold debt.

The same rule reaches 🖼 (JL, same night: "做完之后把这个图填上去…再 append 到
bullet points 上，说这个 Display 已经做好了，并描述它说明了什么"): a built
unit's citing bullet gains `Drawn: <what the figure shows>`, TRANSCRIBED from
the unit's own README claim, never composed fresh. Evidence must WORK on the
plan's face: a value says what its number means, a display says what its
picture shows.

⚠️ **A tick belongs to the version it ticked.** If evidence changes the plan after
`approved: ✅`, that is a `v<N+1>` and a new tick, not a quiet edit. On 260819 the
tick stayed on `v2` while `v2` was edited five more times, and all three stale
`serves:` addresses came from exactly that.

## 📦 The deliverable, and the one thing that ends the phase

```text
<page>/outline/<stem>-outline-v<N>.md      the plan · AUTHORED · versioned
        approved: ⬜  →  ✅                 🚧 a person, never a machine
```

The file's shape, its `C<n>.P<n>.B<n>` addressing, its five marks and its version rules are `haipipe-plugin-outline`'s, stated once there. What belongs HERE is what ends the phase: **a person reads the 🧭 tab and ticks `approved:`.** And the person's job there is to BREAK it, not bless it (JL 260819: "人看的时候不是去 approve，而是去 break——看看这个 outline 是不是你想要的，有些图是不是觉得不行"): hunt for the division that argues nothing, the figure that shows the wrong thing, the answer that dodges its ask. The tick means "I tried to break it and failed", which is the only meaning that survives a machine already having checked the arithmetic. No machine may write that tick, for the same reason no machine accepts a display render: what it judges is whether a plan is the right plan, and no check reaches that.

## 🔓 Before the tick it is a working document

```text
  ✍️ unapproved   discuss it · rewrite it · DELETE a bullet that is wrong
                  no version, no record, nobody agreed to it yet
  🔒 approved     frozen · correct as of that date
  ✍️ v2           the work moved on · `supersedes: v1` · v1 is KEPT
```

**`v2` does not mean `v1` was wrong** (JL 260817). It means `v1` was right then and the work has since moved, which is why the old version is kept rather than corrected. A plan deleted while unapproved needs no record at all.

## 🕳 What OUTLINE does with a hole

A bullet may name evidence it does not have. That is the phase working, not failing:

```text
  ✅ "- B2 · Does the estimate survive the placebo test?   📮 PP02"
  ✅ "- B3 · Five coefficients at each rung        🧮 PP02.v1"
     names what is owed. PROBE dispatches it, EVIDENCE lands it.

  🚫 "- B2 · The five coefficients are stable"
     asserts an answer nobody has. That is not a plan, it is a guess.
```

OUTLINE marks the hole and STOPS. It does not raise the card, it does not ask the bank, and it does not write the sentence. A plan that already knows every answer was written after the fact.

## 🔀 Exit and routing

```text
  any of the four ❌ ─▶ fix the plan HERE. The person is not asked yet.
  four pass, plan owes evidence ──▶ the 🧑 LOOK first, then ② PROBE and
                                    ③ EVIDENCE, and back here when it lands
  four pass, nothing owed, approved ✅ ──▶ ④ DRAFT
  not yet   ⬜  ────▶  stay in OUTLINE, or HOLD if the person is unavailable
  a Page Type refuses the shape ──▶ fix the plan, never the Page Type,
                                    unless the mismatch is a real finding
                                    against that type (record it as one)
```

OUTLINE never routes straight to EVIDENCE or REVISE: a shape nobody approved is not something to gather evidence for.

## 🧾 RUN receipt

The receipt records what a later reader cannot reconstruct: which version was produced, whether it was approved, and by whom.

```text
phase: OUTLINE
file: <page>/outline/<stem>-outline-v<N>.md
supersedes: v<N-1> | —
counts: sections · paragraphs · bullets · marks by kind
approved: ✅ <who> <date>  |  ⬜ waiting
next: DRAFT | HOLD
```

The counts go in because they are the honest size of the plan, and because a later phase's own exit test compares against them.

## 📂 Files

```
haipipe-page-outline/
├── SKILL.md            this phase contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-page`; the file and the 🧭 tab are `haipipe-plugin-outline`'s; the loop and the receipt are `haipipe-page-workflow`'s; the next phase is `haipipe-page-draft`, which no longer owns the outline.

**This phase in six fields** (❓ asks · 📥 reads · 📤 writes · 🚪 exits · ✋ tick · 🔀 routes):
`../haipipe-page-workflow/ref/phase-cards.md` §①. That file states every phase in the SAME fields, so one phase can be read next to another; this contract states the reasoning behind them.

**The Board page that argues this contract** is `QPw1-outline` on `BoardSkillBoard-260722`, created 260818 when JL ruled one page per workflow step. Its `## Law` rows and its `### Decision Now` carry what this contract leaves open.
