---
name: haipipe-plugin-design
description: >-
  The design/ plugin of a Design page: one artifact UNIT per folder, display-shaped — README.md whose kind: routes to a venue pack the way a display unit's kind: routes to a renderer, spec.md compiled from the Brief and the venue rails, evidence.md binding only what the owning direction card granted, prospect.md holding the unit's ex-ante forecast of the artifact in use, and content/ holding the artifact itself (copy.txt, email.html, card.pen, whatever the kind needs). One released card begets one unit through one arm-agent; units are folder-isolated so agents cannot collide. Trigger: design unit, artifact unit, DU folder, unit spec, prospect, forecast, message artifact, design plugin, /haipipe-plugin-design.
metadata:
  version: "0.7.0"
  last_updated: "2026-08-28"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-design · one bet, realized as one folder

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only design's delta: the unit anatomy, the spec as compiled config, and the kind routing.

## 🎯 Why this exists

A display unit shows something already known; a design unit realizes a bet not yet judged by the world. Both need a folder, because an artifact is never one file for long: an SMS grows an email twin, an HTML preview, a .pen card, three variants. The folder is also the arm-agent's write boundary, which is what makes fan-out safe: one released card, one agent, one folder, no collisions — the display family proved this shape.

## 🗂 Storage · one unit, one folder

```text
<page>/design/
└── DU<NN>-<slug>/
    ├── README.md        identity · kind: routes to a venue pack · direction: cites the card back
    ├── spec.md          the COMPILED config the agent obeys and the judge checks against
    ├── evidence.md      the granted evidence rows, bound by path (pagex mechanics)
    ├── ideation.md      generate and brainstorm units · the diverge-then-converge record (§ideation)
    ├── prospect.md      the ex-ante forecast: the artifact reasoned forward into use
    └── content/         the artifact itself · format follows kind
```

README fields: `unit:` id, `kind:` (sms | email | push | reminder | ui-card | dashboard | checklist | report — the venue packs ARE the route table; a new object is a new pack, this plugin does not change), `serves:` the owning division, `direction:` the card id, `depth:` copied from the card, `state: draft | judged | accepted@v<N>`, and — written at the verdict, by the judge — `judged: <actor> <YYMMDD> · <n>/<m> acceptance items pass`.

**The verdict line (260827).** The JUDGE — a fresh context, never the arm that wrote the unit — checks the unit against its spec's acceptance list and the ⊆ chain, then writes the `judged:` line and flips `state: draft → judged` in the same edit. That line is the ex-post verdict's on-disk home: `haipipe-design-workflow`'s GD3 reads it, and no other actor may write it — the arm is forbidden (its own contract), the person writes only the division's `accepted:` row.

One further `state:` exists and only on a board that declares `mode: record` on board.md: `historical-record`, for a unit transcribed from an artifact made before this contract. Nothing judged it and no acceptance list existed to judge it against, so neither `judged` nor `accepted@v<N>` would be true. See `haipipe-plugin-direction` for the card side of record mode.

## 📋 spec.md · compiled, never invented

Three blocks, each naming its source, because a spec value with no source is a new requirement nobody approved:

```text
requirements   ← the Brief (outcome, guardrail, kill, promise)
rails          ← the venue pack (length caps, forbidden moves, tone, timing)
acceptance     ← the judge's list: rails pass · stance fidelity (the content visibly
                 does what the card's thesis says) · files complete
```

The judge AUDITS the acceptance list against these declared sources before applying it (ruled 260828, GD3): an invented item that NARROWS what passes is a finding; an invented item that WIDENS fails the unit, because passing under a test you wrote to fit yourself is not passing.

## 🔮 prospect.md · the forecast, reasoned forward (260827)

Reflect looks back at evidence; prospect (ex-ante, `haipipe-design-workflow` D3/GD4) reasons the artifact FORWARD into use. Four blocks: a walkthrough of the artifact as the recipient meets it, the mechanism the card's thesis relies on, a predicted effect with stated uncertainty, and the conditions under which the bet fails. It sharpens the card's expected effect into something scorable — it never replaces it, because the wager lives on the card.

Three guardrails, so the forecast cannot corrode the evidence chain:

```text
① grant-only      prospect may cite ONLY evidence inside the card's grant —
                  a simulation may not invent data
② forecast-typed  its output is a FORECAST, never a claim: no K/W prose, and it
                  never lands on any InsightBoard
③ scored, not cited   nothing cites a prospect as support; after deployment the
                  measured effect SCORES it, and the score conditions later bets
```

Scope: required before acceptance on units realized under `/haipipe-design-workflow` (its GD4); not retroactive — units accepted before 260827 and `state: historical-record` units on `mode: record` boards are exempt. The checker does not yet enforce it: a `unit-no-prospect` rule is OWED and must first be proven to FAIL on a board broken exactly that way.

**The score comes home (260827).** After deployment, when the InsightBoard reads the actual effect back, whoever lands that read-back appends one dated line to this file: `scored: <YYMMDD> · predicted <x> · measured <y> · <hit|miss|partial>`. This is the same post-acceptance bookkeeping class as staleness clearing an `accepted:` row — legal maintenance, not new design work — and the next round's bets read the score history.

## ⚖️ Three laws

1. **The wager lives on the card.** Expected effect and falsification line are the direction card's fields; this folder cites the card and never restates them, so the bet's terms cannot drift in two places.
2. **Evidence within grant.** `evidence.md` binds only rows inside the owning card's `grant`, which sits inside the board's `reads:`. The chain narrows at every step and the judge checks the set-difference.
3. **A unit without a passing spec cannot be accepted.** `state:` moves draft → judged (the acceptance list passed) → accepted@v<N> (a person's row on the owning division names this unit and a render version). No person, no accepted.

## 🔎 What the checker enforces (260824)

`check.py · check_design_family` reads every `design/DU*/` and reports:

```text
unit-no-readme · unit-file-missing · unit-no-content   the folder contract
unit-depth-word / -no-why / -extra-why                 depth matches the files present
unit-state-word                                        draft · judged · accepted@v<N>
unit-no-direction · unit-direction-ghost               the unit names a card that exists
unit-dead-reference                                    ANY relative reference that
                                                       resolves to nothing            ← law 1
unit-evidence-outside-grant                            evidence beyond the card's grant ← law 2
```

`unit-dead-reference` exists because of a real failure: on 260824 a unit cited its owning card one directory level short, which left the wager unreachable from the artifact and so broke law 1 while every self-check reported clean. Each rule was proven to fail on a one-way-broken board before being trusted; see `tests/test_design_family.py`.

## ⚙️ Writer

One arm-agent per released card writes the whole folder and may touch nothing outside it: not the page prose, not a sibling unit, not the card beyond its `landed:` pointer. A person writes only the division's `accepted:` row. Re-opening a landed unit (venue change, evidence moved) clears the owning division's `accepted:` row and only that row.

## 📡 Surface

The owning division cites the unit by id and carries its stance and acceptance; `render/` projects `content/` into what the recipient sees, stamped with design, warrant and render versions as `haipipe-plugin-render` already rules.

## Variants · one wager, many realizations (260828)

A unit's `content/` may hold a VARIANT SET — `v-a`, `v-b`, … — the SAME wager said differently, because verbalization is most of the design space and the same nudge in different words is a different arm. Laws:

```text
one wager        every variant serves the owning card's single thesis and expected
                 effect; a variant needing its own thesis is a new card
each judged      the judge checks every variant against the compiled spec's rails,
                 not the set as a blob; a failing variant dies alone
subset accepted  the division's accepted: row names WHICH variants, by suffix;
                 accepting v-a and killing v-b is one row, two fates
the difference   what separates the variants is a stated, testable hypothesis in
                 prospect.md ("v-a's loss frame outperforms v-b's gain frame") —
                 the EMIT edge's natural cargo, and the reason to ship several
```

## Ideation · the open before the close (260828, generate units)

Design is not conclusion: it does not stand on the data and summarize, it opens from the data and then closes (JL 260828; the board page is QD5, which carries the fifteen verified anchors and the three qualifications). Every other surface in this folder is a CONVERGENCE surface — spec compiles, evidence binds, the judge checks — so without a lawful divergence surface the lane can only ever conclude, which two field rounds proved. `ideation.md` is that surface, and a generate unit without it is incomplete. Two movements, in order, both on disk:

```text
DIVERGE   quantity under deferred judgment: AT LEAST FIVE candidate copies
          spanning AT LEAST TWO distinct angles, of which GOAL-FIRST is
          always one — the goal-setting reinterpretation (QD5 §6) finds the
          active ingredient may be a specific, challenging goal rather than
          divergence as such, so a diverge with a vague goal is the known
          failure mode. The other angles are open: theory-riff (the same
          mechanism said differently: verbalization is most of the design
          space and the same nudge in different words is a different arm),
          intuition (labeled `intuition`, which is honesty, not a demotion),
          or any angle the arm can name. Five is a FLOOR and there is no
          ceiling: a cap would be a second judgment on generation, and the
          arm stops when its angles are covered (quality against quantity
          shows diminishing returns, not a wall).
          Candidates CITE NOTHING and CLAIM NOTHING: this surface is a
          sketchbook, and the grant-only law does not reach it — that law
          binds the citation surfaces (evidence.md, prospect.md), never
          invention. No rail-checking, no scoring, no self-censoring here:
          judging while diverging is the one forbidden move.
          Fixation guard: the arm diverges BEFORE re-reading fielded copy
          (QD4 §3's fixation anchor — examples anchor the mind on themselves),
          and a fielded template appearing as a "candidate" is the fixation
          this movement exists to break, not a candidate.
CONVERGE  the selection table: EVERY candidate dispositioned kept | discarded
          with one reason each; each FINALIST mapped to the card's warrant
          legs and passed through the rails only NOW; finalists land in
          content/ as the variant set (v-a, v-b, …); discards STAY in this
          file as the record that the space was opened.
          KEEP MORE THAN ONE unless the rails forbid it: generators are
          reliably poor at identifying their own best candidate (QD5 §6),
          so an arm that opens a space and then hands over ONE finalist has
          thrown away most of what the open bought. Narrowing to a single
          finalist is legal but owes a stated reason in this file, and the
          field, not the arm, is what picks between variants. A finalist born as
          `intuition` earns its justification HERE, at selection — the
          abductive order (QD4 §2: the leap first, the warrant after).
```

The two movements answer the two information regimes: with an insight row the diverge is seeded by who the audience is; with none (`warrant-insight: brief-only`, direction plugin law 4) the diverge is seeded by the Brief's goal alone and the missing insight is emitted as a need in the same round — designing without information and naming the information you lacked are one act.

## Pool · the unit a `brainstorm` card lands (260828)

A `brainstorm` card (direction plugin law 5) lands a POOL, not an arm, and the pool unit is deliberately the lightest unit in this plugin. Everything stripped from it was stripped for one reason: it belonged to designing an EXPERIMENT, and this unit designs a MESSAGE SET.

```text
<page>/design/
└── DU<NN>-<slug>/
    ├── README.md          unit · kind · serves · direction · pool: <n> · state: draft
    ├── ideation.md         the diverge-then-converge record, unchanged
    ├── content/pool.txt    N numbered messages, every one newly authored, each
    │                       carrying one `trying:` line naming what it reaches for
    └── inspiration.md      what was read, listed · NOT an evidence chain
```

What does NOT apply, stated as absences so no actor supplies them from habit:

```text
no evidence.md      inspiration is not warrant · no sentence in a pool owes a
                    citation, because no sentence in a pool is a claim
no prospect.md      a forecast is per-BET; a pool is not a bet · GD4 does not
                    reach a pool unit
no control cell     and no allocation, no power arithmetic, no predicted effect
no reuse            ZERO · a fielded template may not appear as an entry, a
                    variant, or a candidate · the fielded set is the AVOID list
```

What the judge checks, and it is only this: the count reaches `pool-target:`; every entry is newly authored, byte-diffed against the whole fielded set; the entries are MUTUALLY distinct, so a pool of near-duplicates fails as surely as a pool of quotations; every entry carries its `trying:` line; every entry passes the venue rails, because a message that cannot be sent is not a candidate.

**What happens next, and why it is not here.** Which entries get fielded, against which control, at what size, is the FIELDING decision, and it belongs downstream with the task layer that ships and measures. A pool that is never fielded is still a completed unit: it is the design space, written down. This separation is the whole point of the stance, and pulling comparator duties back into the pool is the failure it was written to prevent.

## Novelty · what a `generate` unit owes (260828)

A unit realizing a `generate` card (haipipe-plugin-direction law 4) inverts the family's non-novelty habit: where an explore unit's virtue is holding every byte it can, a generate unit's DUTY is to differ. Its `spec.md` carries one more block, and the judge fails the unit without it:

```text
novelty   ← the card's warrant pair, instantiated:
            surface     what in content/ differs from EVERY fielded template,
                        stated concretely (a byte-diff no reader has to run)
            mechanism   the theory mechanism that surface instantiates, named
                        as the card's stance: names it
            anchors     the warrant-theory QA file and warrant-insight row,
                        cited by path — the same two legs the card holds
```

Byte-identity of a generate unit's cell to any fielded template FAILS the unit outright: nominating existing copy is the bet-against lane's move, and two field rounds (260827 DU06, 260828 DU07-09) proved an arm under pressure will retreat there unless the retreat is illegal. The lawful poverty exit is EMIT, never quotation. Variants compose: a generate unit may ship `v-a`, `v-b` under the one wager, each variant satisfying the novelty block on its own bytes. Checker rules OWED, each prove-FAIL-first: `unit-generate-no-novelty`, `unit-generate-no-ideation` (missing file, under five candidates, one angle, or an undispositioned candidate), alongside the still-owed `unit-no-prospect`.
