---
name: haipipe-plugin-direction
description: >-
  The direction/ plugin of a Design page: one strategy CARD per file, each
  declaring a bet before any artifact exists — stance, thesis, and expected
  effect with its falsification line. Proposed by machine, RELEASED only by a
  person. Trigger: direction card, strategy card, stance, release a card, kill
  a direction, /haipipe-plugin-direction.
metadata:
  version: "0.6.0"
  last_updated: "2026-08-28"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-direction · declare the bet before the artifact

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only direction's delta: the card grammar, the release gate, and the grant chain.

## 🎯 Why this exists

A designed message is a bet, and a bet placed after seeing the outcome is not a bet. The card exists so the stance, the move and the wager are written down and RELEASED by a person before any copy exists. Its two precedents are both in the family: probe cards (proposed, human-released, dispatched) give it its lifecycle; the retired stage ladder's failure (arms invented ad hoc, nobody could later say why 13) gives it its reason.

A direction has two lives. The PROPOSAL lives here, because the artifact folder does not exist yet, a killed card needs a tombstone, and the release gate must be visible on disk. The REALIZATION lives in the `design/` unit that cites the card back; after landing, the card keeps only its terms and a pointer, and changing the terms means returning HERE for re-release, never editing them inside the unit.

## 🗂 Storage · one card, one file

```text
<page>/direction/
└── DR<NN>-<slug>.md      one strategy card
```

Card grammar, every field required unless marked:

```text
# DR<NN> · <name>
state: proposed | released | landed | killed
stance: follow <board·page id> | follow-all | ignore | bet-against <board·page id> | generate <mechanism> | brainstorm <audience>
depth: copy | copy+why | copy+why+expectation
thesis: <the design move, one or two sentences>
expected effect: <what it should achieve AND the falsification line>   (ignore cards: baseline, calibrates)
grant: <the exact evidence this card may hand its unit>                (ignore cards: none)
released: ⬜ | <person> <YYMMDD>
landed: — | <DU id>                                                    (killed cards: the reason, kept forever)
```

## ⚖️ Five laws

1. **Release is a person's act.** The machine proposes; only a person's decision flips `released:`. A card at `proposed` blocks its own fan-out and nothing else, so proposing is always safe. This is the standing stop-after-draft ruling wearing its design clothes. A person may release card by card, or by a RECORDED BLANKET over a named set: the person states in writing which cards are released, the run transcribes `released: <person> (blanket, <YYMMDD>)` onto each named card as a clerical record of that act, and the person's words are cited in the owning DS page's Log. A machine's inference that a person "would release" is never a release. **A release binds only cards that EXIST when the words are recorded** (260828): a blanket written before its cards were authored has the wager terms authored after the person agreed to them — the inversion a live run recorded as friction that day — so a commission may authorize PROPOSING, and the release follows as its own act once the written cards can be read.
2. **No expected effect, no release.** A card that cannot say what it is for and what would falsify it is not a bet; `ignore` cards state `baseline, calibrates` explicitly rather than leaving the field empty.
3. **The grant narrows, never widens.** `grant` must sit inside the owning board's `reads:`; the unit's `evidence.md` must sit inside the grant. A `bet-against` card's grant includes the claim it bets against, because refuting something you may not read is not a bet either.
4. **A `generate` card's license is a theory, not a gradient** (260828). The other stances position against evidence that exists; `generate` proposes an artifact no fielded data can yet score — the abductive move design exists for (QD4 §2's anchors, Dorst 2011 above all). Its warrant is therefore TWO legs, both inside the grant: **warrant-insight**, one named row on a board in `reads:` saying who this is for and what is true of them (an I-layer segment fact is admissible — a thin K/W lane must not block generation), and **warrant-theory**, one Discovery QA file stating the general mechanism the copy will instantiate. The `stance:` field names that mechanism (`generate self-referencing`, `generate framing-match`). `expected effect:` may state a direction ONLY as the theory's direction, written `theory-typed`, never as a data-derived prediction — which is why this law does not collide with a Wisdom page's prohibition on reading level gradients as wording licenses: the license never comes from the gradient. The rule that two rounds proved necessary: a card that cannot produce a warrant-theory leg is not a timid generate, it is a follow-family or bet-against card wearing the wrong word. **The insight leg alone may be POOR and the card still legal** (JL 260828: design must run in both information regimes): when the lane holds no insight row for this audience, the leg reads `warrant-insight: brief-only` and names the Brief's audience/goal row instead (board-local, always legal in a grant: a board may read itself, and `card-grant-outside-reads` must not fire on it) — and the same round EMITs the missing insight as a BR00 need, so designing without information and registering the information you lacked are one act, the co-evolution edge entered from the poor side. What never relaxes, in either regime: warrant-theory, the unit's novelty duty, the ideation record, and the rails.

5. **A `brainstorm` card demands a POOL, and reuse is FORBIDDEN, not merely unrewarded** (JL 260828: "我们是完全摒弃任何现在的 message，我们是 propose new message"). This stance exists because the lane kept confusing two different jobs. Designing a MESSAGE SET and designing an EXPERIMENT are separate acts with separate outputs, and every duty that belongs to the second was being charged to the first, which is what pulled fielded copy back in as controls and comparators until nothing new got written. The brainstorm card commissions the first act only:

```text
stance: brainstorm <audience>          the audience the pool is for
pool-target: <n>                       how many NEW messages are wanted, default 10
inspiration: <free list of paths>      REPLACES grant: · insight rows, QA files,
                                       anything the board may read · it says WHO
                                       these people are and what is known about
                                       them, and it licenses NOTHING and forbids
                                       NOTHING about wording
avoid: <path to the fielded set>       the NEGATIVE list · the only role fielded
                                       copy plays in this stance
expected effect: pool, predicts nothing   the law-2 form for this stance, as
                                       `ignore` cards write `baseline, calibrates`
```

The three rules that follow, and law 2 does not override them:

```text
ZERO REUSE      every pool entry is newly authored. A fielded template may not
                appear as an entry, a variant, or even a candidate. The fielded
                set is read to AVOID it, never to source from it.
NO COMPARATOR   a pool carries no control cell, no allocation, no power
                arithmetic and no predicted effect. Which entries get fielded,
                against which control, at what size, is the FIELDING decision
                downstream, and charging it to the pool is the confusion this
                law exists to end.
INSPIRATION,    insights enter as background a person might have read anywhere,
NOT WARRANT     not as a chain each sentence must cite. Nothing in a pool is
                a claim, so nothing in it needs a warrant.
```

## 🔎 What the checker enforces (260824)

The three laws above stopped being prose on 260824. `check.py · check_design_family` reads every `direction/DR*.md` and reports:

```text
card-field-missing / -empty   any of the eight fields absent or blank
card-state-word               a `state:` off the four-word ladder
card-released-no-wager        released or landed with no expected effect   ← law 2
card-released-unsigned        `state: released` with `released: ⬜`        ← law 1
card-proposed-signed          a signature on a card still `proposed`
card-grant-path               a grant entry resolving to nothing
card-grant-outside-reads      a grant reaching outside the board's `reads:` ← law 3
card-landed-ghost / -empty    `landed:` naming no unit, or missing on a landed card
```

Each was proven to FAIL on a board broken exactly that one way before it was trusted; the proofs are `tests/test_design_family.py`. A board may declare `mode: record` on board.md when it holds a PRE-CONTRACT artifact, which relaxes the vocabulary rules (a historical `released:`, no stance, no grant) and nothing structural.

Two rules are OWED for law 4 and not yet in the checker, each to be proven to FAIL first: `card-generate-no-theory` (a `generate` card whose grant contains no Discovery QA path) and `card-generate-no-insight` (one whose grant names no board row). Until they land, GD2's judge carries the check by cold read.

## ⚙️ Writer

The page's producer (or the design door's `direction` verb) writes cards at `proposed`. A person edits `released:` and `state:` — directly, or through the recorded-blanket transcription law 1 defines, where the run's write is clerical and the decision remains the person's. The arm-agent that realizes a card writes ONLY the `landed:` pointer, nothing else on the card.

## 📡 Surface

The owning page's division table cites cards by id, and the page's state line counts them (`three cards proposed · none released`). A killed card stays in the folder as its own tombstone; deleting one deletes the record that the bet was considered.
