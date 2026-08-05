---
name: haipipe-board-page-for-design
description: >-
  The VARIANT contract for a DESIGN brief Page: one page per design BRIEF, such as one message drafted for one group of people, with the audience, the goal, and the constraints stated in its Opening and one Content division per CANDIDATE artifact, side by side. It loads haipipe-board-page for the base frame and adds only what a design page needs: each division carrying one candidate whole (the artifact itself, its rationale, its fit to the brief's criteria), Aims that ARE the brief's criteria, the SELECTION record that names the winner, why, and each loser's disposition, and the rule that a losing division is never silently deleted. It sits upstream of haipipe-board-page-for-display: design selects the candidate, display accepts its render. Use when writing or fixing a design page, when candidates live loose in a candidates/ folder or a chat thread, when a winner was picked but nothing records why, or when a rejected candidate vanished with its rationale. Trigger: design page, design brief, candidate, message A B C, candidates folder, selection record, A/B test, pick a variant, /haipipe-board-page-for-design.
metadata:
  version: "0.1.1"
  last_updated: "2026-08-05"
  summary: "First cut, on JL's A ruling: page = brief, division = candidate, closes on a SELECTION record; upstream of for-display, and a losing division keeps its disposition."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-design · candidates side by side, and the selection that closes them

**LOAD `haipipe-board-page` FIRST.** It owns the base frame. What this file guards is CHOOSING: several candidates answer one brief, and the record of why one won and the others lost must outlive the choice.

**The kind this variant covers**: one page per design BRIEF.

```
kind      subject                              closes when
──────────────────────────────────────────────────────────────────────
Design    ONE brief and its candidate          a SELECTION record names the
brief     artifacts, side by side              winner, why, and each loser's
                                               disposition
```

**The type key.** A design page declares `page-type: design` in its frontmatter, and the line is REQUIRED: no filename shape marks a brief, so the key is the only way a resolver, a checker, or a cold reader learns that the divisions are candidates. The `page-type:` key beats the filename (base, type resolution step ③).

**Where it stands beside the display type**: a design page sits UPSTREAM of `-for-display`. Design SELECTS the candidate; display ACCEPTS its render. The shape already exists unruled in two places: the application family designs channel messages per cohort, and the paper family's display units keep `candidates/` folders (display01b has one on disk). Nothing ruled how those candidates sit on a page or how one is chosen, and that gap is exactly what this contract closes (JL 260805, ruled A on the design board's QB6).

## 🧾 The page is the brief, the divisions are the candidates

JL's defining case is three messages, A, B and C, drafted for one group of people: "the Content divisions ARE the different messages" (JL 260805).

```
Opening      the BRIEF: who it is for · what it must do · what bounds it
Content      ### 1 · candidate A      the artifact itself
             ### 2 · candidate B      + the rationale for drafting it this way
             ### 3 · candidate C      + its fit to each of the brief's criteria
Aims         the brief's CRITERIA, one Aim per criterion
States       how each criterion stands across the candidates
```

The page IS the brief, because a candidate can only be judged against a stated brief. Each Content division carries ONE candidate whole: the artifact itself, never a pointer to a chat message that scrolls away. A division with the artifact but no rationale is half a candidate, because the selection has to weigh why each one was drafted the way it was. Aims are the brief's criteria, so States can say, per criterion, which candidates meet it and which fall short.

## 🏁 The SELECTION record closes the page

A design page closes on one typed record, and nothing else closes it:

```
SELECTION · <date> · <who ruled>
winner      candidate B          why it beat the others, in one or two lines
loser A     dropped              why it lost
loser C     kept for A/B test    what measurement would decide it
downstream  <path>               the display unit page the winner becomes or updates
```

The record names three things: which candidate won, WHY it won, and each loser's disposition. A disposition is one of three: `dropped`, `kept for A/B test`, or `merged` into the winner. Selection is a human judgment, like display acceptance: a machine may propose a winner as a Decision Now row and never record one as ruled. The handoff downstream is BY PATH: the record's `downstream` line names the display unit page the winning candidate becomes, or the existing one it updates, and `-for-display`'s acceptance ladder takes over from there.

## 🪦 A losing division is never silently deleted

The rationale for NOT choosing is part of the design record:

```
after SELECTION:
  winner's division  →  flows downstream · -for-display accepts its render
  loser's division   →  STAYS on the page, its disposition written at its head
🚫 deleting a losing candidate deletes the reason it lost
```

A loser keeps its division, with its disposition and the reason it lost written at the division's head. The next brief for the same audience starts by reading why the last losers lost, and that reading is impossible if selection swept them away. After selection only the disposition line changes; the artifact and its rationale stay as they were judged.

## 📂 Files

```
haipipe-board-page-for-design/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-board-page`; the downstream sibling is `haipipe-board-page-for-display`, which accepts the winner's render; the application family's channel messages and the paper family's display `candidates/` folders are the shapes this contract rules, which it names but never contains.
