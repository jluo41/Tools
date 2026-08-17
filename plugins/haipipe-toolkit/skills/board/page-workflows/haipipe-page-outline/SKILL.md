---
name: haipipe-page-outline
description: >-
  The OUTLINE phase contract for any Board Page, and phase ① of the page workflow. OUTLINE agrees the SHAPE of a page before a word of it is written: the section list, the paragraph under each section, the bullets under each paragraph, and what each bullet still owes. Its deliverable is a versioned file at <page>/outline/<stem>-outline-v<N>.md, read on the 🧭 tab, and it exits only when a person ticks its approved: line. It writes no prose, lands no card, and dispatches no question. Load haipipe-page, the matching Page Type, this contract, then haipipe-plugin-outline for the file's own shape. Use when opening a new Page, when starting a new round after CHECK, when a plan must be agreed before expensive work, or when a page turned out to be built on a shape nobody approved. Trigger: page outline, OUTLINE phase, phase 1, plan the page, agree the shape, approve the outline, outline gate, v1 v2, supersedes, bullet, /haipipe-page-outline.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-17"
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
exits      ONLY when a person ticks `approved:` on the 🧭 tab
🚫 may not write prose · land a card · dispatch a question · invent a
           division the Page Type does not allow
```

An operation does not identify OUTLINE. Adding a section to the PLAN is OUTLINE; adding a section to the PAGE is DRAFT. The two are different files.

## 🚧 Why this is a phase and not a step inside DRAFT

It was a step inside DRAFT until 260817, and the day it stopped being one is on the record. One phase owned both "agree the shape" and "write the page", so a single done-report covered both, and the plan ended up pasted into the page's own `## Content` where it immediately went stale (`QC1-visitlbp`, CMSRegBoard).

**The gate is the cheapest one on the board, which is the whole argument for it.**

```text
  change a section list   BEFORE the prose   one line
  change a section list   AFTER  the prose   the prose
```

A phase whose entire output fits on one screen, and which a person can reject in ten seconds, belongs in front of every expensive phase rather than folded into one.

## 📦 The deliverable, and the one thing that ends the phase

```text
<page>/outline/<stem>-outline-v<N>.md      the plan · AUTHORED · versioned
        approved: ⬜  →  ✅                 🚧 a person, never a machine
```

The file's shape, its `C<n>.P<n>.B<n>` addressing, its six marks and its version rules are `haipipe-plugin-outline`'s, stated once there. What belongs HERE is what ends the phase: **a person reads the 🧭 tab and ticks `approved:`.** No machine may write that tick, for the same reason no machine accepts a display render: what it judges is whether a plan is the right plan, and no check reaches that.

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
  ✅ "- B2 · the five coefficients at each rung        🔢 PP02"
     names what is owed. PROBE dispatches it, EVIDENCE lands it.

  🚫 "- B2 · the five coefficients are stable"
     asserts an answer nobody has. That is not a plan, it is a guess.
```

OUTLINE marks the hole and STOPS. It does not raise the card, it does not ask the bank, and it does not write the sentence. A plan that already knows every answer was written after the fact.

## 🔀 Exit and routing

```text
  approved ✅  ────▶  ② DRAFT        purpose · Aims · the page's own promise
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
