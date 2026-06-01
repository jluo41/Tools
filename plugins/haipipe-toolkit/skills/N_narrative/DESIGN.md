N_narrative — The Story Layer (DESIGN)
========================================

Status: DESIGN draft (2026-05-30) — scope A only (narrative as a first-class
        "thing": folder + schema + one read/write skill). Scope B (gap-diff
        auto-driving the next probe) is deferred to a second pass.
Owner:  jluo41

Read ARCHITECTURE.md first. This doc designs the layer that ARCHITECTURE.md
calls layer 4 (Narrative) — the one drawn in the blueprint but absent from
code until now.


Why this layer exists
=====================

The KB (probes/ + tasks/ + insights/) is a pile of facts. By itself it is
"a heap of cards nobody sells". The Narrative is the **living story** that
selects a subset of those facts and argues "here is the angle, here is why
it matters, here is what I still need to make it sell".

ARCHITECTURE.md's one rule: **KB ⇄ Narrative is the only double arrow** —
the engine. N_narrative is the code home for the right-hand side of that
arrow.

```
   🧠 KB (facts)  ⇄[🔥 ignite]⇄  📖 N_narrative (story)
   probes/ tasks/                  narratives/<NN>_<slug>/
   insights (D/I/K/W)              story + claims + ignite-log + decision-tree
```


CRITICAL: two "narratives" — do not confuse them
=================================================

The word `narrative` is already used in code by
`F_paper/1-narrative/narrative-report`. They are NOT the same and do NOT
conflict — they are upstream vs downstream:

```
N_narrative/  (THIS layer, new)        F_paper/1-narrative/narrative-report (exists)
─────────────────────────────         ───────────────────────────────────────────
the living story, runs the whole time  a one-shot snapshot: the paper's design contract
⇄ double arrow with KB; holds ignite   one-way downstream: KB → it → paper
1 narrative : N papers                 "one narrative per paper"
lives in examples/<proj>/narratives/   emits NARRATIVE_REPORT.md beside the paper
the NOUN (the story itself)            the ACT of freezing a story into a paper contract
```

Relationship — strictly upstream → downstream, no overlap:

```
narratives/01_fairness/  ──(ignite says "sells")──►  narrative-report  ──►  NARRATIVE_REPORT.md ──► /haipipe-paper
   (living story, mutates)                            (snapshots it now)        (frozen, per venue)
```

So `narrative-report` is UNCHANGED. It becomes the bridge FROM this new
layer TO a paper. N_narrative owns the living story + ignite; rendering a
story into a paper contract stays with the existing narrative-report skill.


Where it sits in the letter sequence
====================================

```
A_discover → B_project → C_task → D_probe → E_insight → N_narrative → F_paper → G_application
                                  └────────── KB ──────────┘    ⇄         (publish)  (deliver)
```

N is placed AFTER E_insight (it reads the KB) and BEFORE F_paper /
G_application (they consume a settled story). The letter `N` is used (not
a position in A–G) to avoid renaming the existing A–G layers; mnemonic =
Narrative.


The unit: one narrative = one story line
========================================

```
examples/<PROJECT_ID>/narratives/
├── INDEX.md                      auto: list all narratives + ignite status
├── 01_<slug>/                    folder-per-narrative (2-digit, no gap on create)
│   ├── story.md                  the angle + why it sells (the NOUN)
│   ├── claims.md                 which K cards this story needs (BY REFERENCE)
│   ├── ignite-log.md             ③ per-round "am I ignited?" judgments
│   └── decision-tree.md          section paths A/B/C/D (turn-7 idea)
└── 02_<slug>/
    └── ...
```

Hard rules (mirror E_insight's discipline):

- NO code, no notebooks, no plots in narratives/. Pure markdown.
- `claims.md` references K cards BY ID (e.g. `needs: [K01, K03, K05]`),
  never copies them. Same "reference, not nesting" rule as probe arms.
- A narrative NEVER writes to probes/ tasks/ insights/. It only reads the
  KB and records story + ignite state. (Triggering a probe is scope B,
  and even then goes THROUGH G_application's ask kind, not directly.)
- 1 narrative : N papers. A paper points home via `narrative: <id>` in its
  meta; the narrative does not know about papers.


File schemas (scope A)
======================

### story.md

```markdown
---
id:        N01
layer:     narrative
slug:      fairness_angle
status:    exploring | igniting | ready | shelved
created:   YYYY-MM-DD
updated:   YYYY-MM-DD
tags:      [fairness, conditioning]
papers:    []                      # paper ids that render this story (back-ref)
---

# N01: <one-line story title>

## Angle
<1-2 paragraphs: the lens. What is the surprising / important framing?>

## Why it matters
<who cares, and why now. The "eager to sell this" test.>

## Core claim (one sentence)
<the single sentence this story exists to defend>
```

`status` enum:
  exploring → still finding the angle; KB→N induction phase
  igniting  → angle found, accumulating claims, ignite judgments running
  ready     → ignited enough to sell → eligible for narrative-report → paper
  shelved   → dropped (record why in ignite-log)


### claims.md  (the N→KB interface — the gap lives here)

```markdown
# N01 — claims ledger

## Needed (what the story must defend)
| slot | claim (free text)                          | KB card | status   |
|------|--------------------------------------------|---------|----------|
| C1   | FiLM helps in-distribution                 | K03     | have     |
| C2   | benefit survives param-matching            | —       | GAP      |
| C3   | holds on test-od                           | K05?    | weak     |

## Gap summary
- C2: no K card. → next probe: param-matched re-test
- C3: K05 exists but confidence=low → strengthen or re-scope

## Claim Gap Contracts

### C2 — benefit survives param-matching
- needed_claim: Benefit survives parameter matching.
- why_needed: Without this, the story may be only a scale-confound story.
- evidence_standard: N>=3 paired seeds; same split; same schedule; same metric.
- candidate_probe: P.A03 param-matched re-test
- expected_return:
  - K: supported/refuted claim
  - W: next recommended move
```

`status` per slot: `have` (K card exists, confidence ok) / `weak` (exists
but low confidence) / `GAP` (no card). The GAP/weak rows ARE the
"which whip to crack next" list. The **Claim Gap Contract** is the precise
hinge from narrative-cycle to probe-cycle: a weak/GAP claim slot made
specific enough to become one probe's hypothesis, arms, evidence standard,
and expected K/W return. (Scope A: human reads this. Scope B: a skill diffs
`needs[]` against insights/K automatically and materializes the contract.)


### ignite-log.md  (③ the gate on the double arrow)

```markdown
# N01 — ignite log (append-only)

## 2026-05-30 — after probe 01 (FiLM in-dist confirmed)
- ignited? YES
- why: in-dist effect is clean (K03 high-conf); the "conditioning helps
  the hard sub-population" angle suddenly feels sellable
- next: crack probe for C2 (param-matched) to kill the scale confound

## 2026-06-02 — after probe 02 (param-matched null)
- ignited? NO
- why: param-matched result is null → the angle's spine (C2) is gone
- decision: re-scope to "in-dist-only" claim, OR shelve. Chose re-scope.
```

This is the heart of the whole system: each entry is one round-trip across
the KB⇄Narrative arrow. ignited→advance; not→re-scope or shelve. Honest
"NO" entries are what stop motivated reasoning (wanting to be ignited so
you can write the paper).


### decision-tree.md  (turn-7: section paths)

```markdown
# N01 — section decision tree

Each major section can go down one of several paths; the chosen spine is
what stitches them into one story.

## Intro
- [x] A. "fairness gap in CGM forecasting" (chosen)
- [ ] B. "personalization angle"
## Method
- [x] A. FiLM conditioning
- [ ] B. mixture-of-experts
## Results spine
- [x] in-dist win + honest od-limitation  ← the thread tying A/A together
```


The one skill (scope A)
=======================

```
N_narrative/
├── DESIGN.md                 (this file)
├── haipipe-narrative/        🧭 the layer skill
│   ├── SKILL.md
│   └── ref/narrative-schema.md   (the schemas above, canonical)
```

`/haipipe-narrative` verbs (scope A — read/write the story, no auto-drive):

```
/haipipe-narrative new <slug>           scaffold narratives/<NN>_<slug>/ (4 files)
/haipipe-narrative status [<id>]        dashboard: all narratives + ignite state
/haipipe-narrative claims <id>          show claims ledger + GAP/weak rows
                                        (reads insights/K to fill `have/weak/GAP`)
/haipipe-narrative ignite <id>          append an ignite-log entry (interactive:
                                        ignited? why? next?) + maybe flip status
/haipipe-narrative "<natural language>" infer + dispatch
```

Note on `claims`: even in scope A this verb READS insights/K to mark each
needed slot have/weak/GAP. It does NOT yet auto-fire a probe for the gaps
— it just surfaces them. Auto-firing (claims → /haipipe-probe design) is
scope B.


Interfaces to neighbours
========================

```
reads:   insights/K_knowledge/*.md   (to fill claims.md have/weak/GAP)
         insights/W_wisdom/*.md       (W cards of type next_probe = candidate gaps)
         probes/INDEX.md              (what's been probed already)

writes:  narratives/<NN>_<slug>/*     (only here)

feeds:   F_paper/1-narrative/narrative-report   (when status=ready, that skill
                                                 snapshots this story → NARRATIVE_REPORT.md)
         G_application ask kind        (scope B: gap rows → ask sub-questions)

NEVER:   writes to probes/ tasks/ insights/ ; triggers a probe directly
```


Scope boundary (what this DESIGN does NOT do)
=============================================

Deferred to scope B (a later pass), explicitly OUT of this design:

- Auto gap-diff: claims.md Claim Gap Contracts minus insights/K → auto-generate
  `/haipipe-probe design new ...` calls with an evidence standard.
- The G_application ask-kind wiring (load→gap→chain already has a stub;
  connecting narrative gaps to it is scope B).
- Multi-narrative strategic synthesis (one project, many stories competing
  for the same KB).
- ignite as an enforced GATE with a steelman reviewer (scope A records the
  judgment; it does not yet spawn an adversarial "argue it's NOT worth it"
  agent).

Scope A's goal is narrow and concrete: make the living story a
first-class, on-disk citizen with a stable schema, so scope B has
something solid to automate against.


Open questions (decide before scope B)
======================================

Q1. Does `claims.md` slot id (C1/C2…) need to be globally unique or just
    per-narrative? Proposed: per-narrative (C1 in N01 ≠ C1 in N02).

Q2. When a probe later produces the K card a gap wanted, who updates
    claims.md status from GAP→have? Scope A: human / `claims` verb re-scan.
    Scope B: E_insight filing a K card notifies narratives that reference it.

Q3. Should `status: ready` be gated (an ignite steelman must pass) or just
    user-set? Scope A: user-set. Scope B: gated.
