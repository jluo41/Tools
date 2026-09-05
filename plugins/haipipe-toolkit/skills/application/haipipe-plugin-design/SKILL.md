---
name: haipipe-plugin-design
description: >-
  The ONE law of a Design page's design/ folder: the thread, card and unit
  together. card.md is the folder's FIRST file — the design card declaring a
  bet before any artifact exists (stance, thesis, expected effect with its
  falsification line), proposed by machine and RELEASED only by a person.
  The unit grows beside it after release: README.md whose kind: routes to a
  venue pack, spec.md compiled from the Brief and the venue rails,
  evidence.md binding only what the card granted, prospect.md holding the
  ex-ante forecast, ideation.md the diverge-then-converge record, and
  content/ holding the artifact itself. One released card begets one unit
  through one designer; units are folder-isolated so agents cannot collide.
  Absorbed haipipe-plugin-direction 260828 (JL: one folder should not live
  under two laws). Trigger: design unit, artifact unit, DU folder, unit
  spec, prospect, forecast, message artifact, design plugin, design card,
  card law, stance, release a card, kill a card, /haipipe-plugin-design.
metadata:
  version: "1.0.0"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-design · one bet, one folder: the card and its realization

This is a Design-family capability, not one of the generic Page plugins.
Load `haipipe-design` first; load `haipipe-plugin` only when reasoning about
the shared storage/surface/writer/boundary shape. This file owns the card
grammar and release gate, unit anatomy, compiled spec, and kind routing.

## 🎯 Why this exists

A designed message is a bet, and a bet placed after seeing the outcome is not a bet. The card exists so the stance, the move and the wager are written down and RELEASED by a person before any copy exists. Its two precedents are both in the family: probe cards (proposed, human-released, dispatched) give it its lifecycle; the retired stage ladder's failure (arms invented ad hoc, nobody could later say why 13) gives it its reason.

A design has two lives in ONE folder. The PROPOSAL is the folder at birth: card.md and nothing else, which is release-before-realize made checkable — a proposed card with sibling files is the checker's `unit-realized-before-release`, an ERROR, not a habit. The REALIZATION grows beside the card after a person releases it. Changing the wager terms means re-release, never editing them mid-realization.

The realization is folder-shaped for the display family's reason: an artifact is never one file for long (an SMS grows an email twin, an HTML preview, a .pen card, three variants), and the folder is the designer's write boundary, which is what makes fan-out safe — one released card, one agent, one folder, no collisions.

Until 260828 the card lived in its own `direction/` folder under its own plugin; JL ruled one thread is one folder and one folder should not live under two laws, so the card law moved here and `haipipe-plugin-direction` was deleted, git the only copy.

## 🗂 Storage · one thread, one folder

```text
<page>/design/
└── DU<NN>-<slug>/
    ├── card.md          the design card, the folder's FIRST file (§card owns its
    │                    grammar) · sole design material until release
    ├── workflow/        shared Folder control metadata; phase.yaml may exist
    │   └── phase.yaml   current kind + append-only D1/D2/D3 transitions
    ├── README.md        identity · kind: routes to a venue pack
    ├── spec.md          the COMPILED config the agent obeys and the judge checks against
    ├── evidence.md      the granted evidence rows, bound by path (pagex mechanics)
    ├── ideation.md      generate and brainstorm units · the diverge-then-converge record (§ideation)
    ├── prospect.md      the ex-ante forecast: the artifact reasoned forward into use
    └── content/         the artifact itself · format follows kind
```

README fields: `unit:` id, `kind:` (sms | email | push | reminder | ui-card | dashboard | checklist | report — the venue packs ARE the route table; a new object is a new pack, this plugin does not change), `serves:` the owning division, `depth:` copied from the card, `state: draft | judged` — no `direction:` field since 260828: the card is `./card.md` and a shared folder cannot dangle, and — written at the verdict, by the judge — `judged: <actor> <YYMMDD> · <n>/<m> acceptance items pass`. Acceptance exists only on the parent D4 division row; Folder/PageX surfaces may derive it but never copy it into README. Legacy `accepted@v<N>` remains readable during migration and is not written on new work.

**The verdict line (260827).** The JUDGE — a fresh context, never the designer that wrote the unit — checks the unit against its spec's acceptance list and the ⊆ chain, then writes the `judged:` line and flips `state: draft → judged` in the same edit. That line is the ex-post verdict's on-disk home: `haipipe-design-workflow`'s GD3 reads it, and no other actor may write it — the designer is forbidden (its own contract), the person writes only the division's `accepted:` row.

One further `state:` exists and only on a board that declares `mode: record` on board.md: `historical-record`, for a unit transcribed from an artifact made before this contract. Nothing judged it and no acceptance list existed to judge it against, so `judged` would be false. Record mode relaxes the card vocabulary the same way (§card checker note): a historical `released:`, no stance, no grant — and nothing structural.

## 🃏 §card · the grammar and the release gate

One card, one file: `card.md`, first file of the thread folder. Every field required unless marked:

```text
# DU<NN> · <name>
state: proposed | released | landed | killed   (landed = the realization exists beside this file)
stance: follow <board·page id> | follow-all | ignore | bet-against <board·page id> | generate <mechanism> | brainstorm <audience>
depth: copy | copy+why | copy+why+expectation
thesis: <the design move, one or two sentences>
expected effect: <what it should achieve AND the falsification line>   (ignore cards: baseline, calibrates)
grant: <the exact evidence this card may hand its unit>                (ignore cards: none)
released: ⬜ | <person> <YYMMDD>
```

A killed thread keeps its folder forever: card.md plus optional `workflow/`
control history, the reason inside — the tombstone law, folder-shaped. No
realization material survives. `landed:` is gone from the grammar; the
checker's `card-landed-bare` tests the same law by asking a landed card for the
README beside it.

## ⚖️ Five card laws

1. **Release is a person's act.** The machine proposes; only a person's decision flips `released:`. A card at `proposed` blocks its own fan-out and nothing else, so proposing is always safe. This is the standing stop-after-draft ruling wearing its design clothes. A person may release card by card, or by a RECORDED BLANKET over a named set: the person states in writing which cards are released, the run transcribes `released: <person> (blanket, <YYMMDD>)` onto each named card as a clerical record of that act, and the person's words are cited in the owning DS Folder's `outline/<DS-stem>-log.md`. A machine's inference that a person "would release" is never a release. **A release binds only cards that EXIST when the words are recorded** (260828): a blanket written before its cards were authored has the wager terms authored after the person agreed to them — the inversion a live run recorded as friction that day — so a commission may authorize PROPOSING, and the release follows as its own act once the written cards can be read.
2. **No expected effect, no release.** A card that cannot say what it is for and what would falsify it is not a bet; `ignore` cards state `baseline, calibrates` explicitly rather than leaving the field empty.
3. **The grant narrows, never widens.** `grant` must sit inside the owning board's `reads:`; the unit's `evidence.md` must sit inside the grant. A `bet-against` card's grant includes the claim it bets against, because refuting something you may not read is not a bet either.
4. **A `generate` card's license is a theory, not a gradient** (260828). The other stances position against evidence that exists; `generate` proposes an artifact no fielded data can yet score — the abductive move design exists for (QD4 §2's anchors, Dorst 2011 above all). Its warrant is therefore TWO legs, both inside the grant: **warrant-insight**, one named row on a board in `reads:` saying who this is for and what is true of them (an I-layer segment fact is admissible — a thin K/W lane must not block generation), and **warrant-theory**, one Discovery QA file stating the general mechanism the copy will instantiate. The `stance:` field names that mechanism (`generate self-referencing`, `generate framing-match`). `expected effect:` may state a direction ONLY as the theory's direction, written `theory-typed`, never as a data-derived prediction — which is why this law does not collide with a Wisdom page's prohibition on reading level gradients as wording licenses: the license never comes from the gradient. The rule that two rounds proved necessary: a card that cannot produce a warrant-theory leg is not a timid generate, it is a follow-family or bet-against card wearing the wrong word. **The insight leg alone may be POOR and the card still legal** (JL 260828: design must run in both information regimes): when the lane holds no insight row for this audience, the leg reads `warrant-insight: brief-only` and names the Brief's audience/goal row instead (board-local, always legal in a grant: a board may read itself, and `card-grant-outside-reads` must not fire on it) — and the same round EMITs the missing insight as a BR00 need, so designing without information and registering the information you lacked are one act, the co-evolution edge entered from the poor side. What never relaxes, in either regime: warrant-theory, the unit's novelty duty, the ideation record, and the rails.

5. **A `brainstorm` card demands a POOL, and reuse is FORBIDDEN, not merely unrewarded** (JL 260828: "我们是完全摒弃任何现在的 message，我们是 propose new message"). This stance exists because the lane kept confusing two different jobs. Designing a MESSAGE SET and designing an EXPERIMENT are separate acts with separate outputs, and every duty that belongs to the second was being charged to the first, which is what pulled fielded copy back in as controls and comparators until nothing new got written. The brainstorm card commissions the first act only:

```text
stance: brainstorm <audience>          the audience the pool is for
pool-target: <n>                       how many NEW messages are wanted, default 10
inspiration: <free list of paths>      insight rows, QA files,
                                       anything the board may read · it says WHO
                                       these people are and what is known about
                                       them, and it licenses NOTHING and forbids
                                       NOTHING about wording
avoid: <path to the fielded set>       the NEGATIVE list · the only role fielded
                                       copy plays in this stance
expected effect: pool, predicts nothing   the law-2 form for this stance, as
                                       `ignore` cards write `baseline, calibrates`
grant: <inspiration ∪ avoid>           the SAME paths again, because the checker
                                       reads `grant:` on every card and a missing
                                       field is an error · on a brainstorm card
                                       grant means "may READ", never "must cite"
```

The three rules that follow, and card law 2 does not override them:

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

## ⚖️ Three unit laws

1. **The wager lives on the card.** Expected effect and falsification line are the design card's fields; the rest of the folder cites the card and never restates them, so the bet's terms cannot drift in two places.
2. **Evidence within grant.** `evidence.md` binds only rows inside the owning card's `grant`, which sits inside the board's `reads:`. The chain narrows at every step and the judge checks the set-difference.
3. **A unit without a passing spec cannot be accepted.** Unit `state:` moves
   draft → judged when the acceptance list passes. A person's row on the
   owning D4 division then names this unit and render version; README stays
   judged so there is one acceptance authority. No person, no accepted.

## 🔎 What the checker enforces (260824)

`check.py · check_design_family` walks every `design/DU*/` folder — the card and the unit in ONE pass, because they are one thread — and reports:

```text
card-field-missing / -empty   any of the eight card fields absent or blank
card-state-word               a `state:` off the four-word ladder
card-released-no-wager        released or landed with no expected effect   ← card law 2
card-released-unsigned        `state: released` with `released: ⬜`        ← card law 1
card-proposed-signed          a signature on a card still `proposed`
card-grant-path               a grant entry resolving to nothing
card-grant-outside-reads      a grant reaching outside the board's `reads:` ← card law 3
card-landed-bare              `state: landed` with no README beside the card
unit-no-card                  a thread folder with no card.md
unit-realized-before-release  a proposed card with realization material      ← card law 1
unit-tombstone-extra          a killed thread retaining realization material (WARN)
unit-no-readme · unit-file-missing · unit-no-content   the folder contract
unit-depth-word / -no-why / -extra-why                 depth matches the files present
unit-state-word                                        draft · judged (legacy accepted@v<N> readable)
unit-dead-reference           ANY relative reference that resolves to nothing ← unit law 1
unit-evidence-outside-grant   evidence beyond the card's grant               ← unit law 2
```

`card-landed-ghost`, `card-landed-empty`, `unit-no-direction` and `unit-direction-ghost` retired with the pointer fields (260828, the one-thread-one-folder merge). Each surviving rule was proven to FAIL on a board broken exactly that one way before it was trusted; the proofs are `tests/test_design_family.py`. `unit-dead-reference` exists because of a real failure: on 260824 a unit cited its owning card one directory level short, which left the wager unreachable from the artifact and so broke unit law 1 while every self-check reported clean.

A board may declare `mode: record` on board.md when it holds a PRE-CONTRACT artifact, which relaxes the vocabulary rules (a historical `released:`, no stance, no grant) and nothing structural.

Rules OWED and not yet in the checker, each to be proven to FAIL first: `card-generate-no-theory` (a `generate` card whose grant contains no Discovery QA path), `card-generate-no-insight` (one whose grant names no board row), `unit-generate-no-novelty`, `unit-generate-no-ideation` (missing file, under five candidates, one angle, or an undispositioned candidate), and `unit-no-prospect`. Until they land, the workflow's judge gates carry them by cold read.

## ⚙️ Writer

The page's producer (or the design door's verb) births the thread folder with card.md at `proposed`. A person edits `released:` and `state:` — directly, or through the recorded-blanket transcription card law 1 defines, where the run's write is clerical and the decision remains the person's. One designer per released card then writes the whole folder and may touch nothing outside it: not the page prose, not a sibling unit, and on the card only the single flip `state: released → landed` when the realization is complete. The judge writes the README's `judged:` line; a person writes only the division's `accepted:` row. Re-opening a landed unit (venue change, evidence moved) clears the owning division's `accepted:` row and only that row.

## 📡 Surface

The owning page's division table cites cards and units by id; the page's state line counts them (`three cards proposed · none released`). A killed card stays in the folder as its own tombstone; deleting one deletes the record that the bet was considered. `delivery/render/` projects `content/` into what the recipient sees, stamped with design, warrant and render versions as `haipipe-plugin-delivery/ref/render.md` rules.

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
          or any angle the designer can name. Five is a FLOOR and there is no
          ceiling: a cap would be a second judgment on generation, and the
          arm stops when its angles are covered (quality against quantity
          shows diminishing returns, not a wall).
          Candidates CITE NOTHING and CLAIM NOTHING: this surface is a
          sketchbook, and the grant-only law does not reach it — that law
          binds the citation surfaces (evidence.md, prospect.md), never
          invention. No rail-checking, no scoring, no self-censoring here:
          judging while diverging is the one forbidden move.
          Fixation guard: the designer diverges BEFORE re-reading fielded copy
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
          so a designer that opens a space and then hands over ONE finalist has
          thrown away most of what the open bought. Narrowing to a single
          finalist is legal but owes a stated reason in this file, and the
          field, not the designer, is what picks between variants. A finalist born as
          `intuition` earns its justification HERE, at selection — the
          abductive order (QD4 §2: the leap first, the warrant after).
```

The two movements answer the two information regimes: with an insight row the diverge is seeded by who the audience is; with none (`warrant-insight: brief-only`, card law 4) the diverge is seeded by the Brief's goal alone and the missing insight is emitted as a need in the same round — designing without information and naming the information you lacked are one act.

## Pool · the unit a `brainstorm` card lands (260828)

A `brainstorm` card (§card law 5) lands a POOL: `pool-target:` messages that are CANDIDATE ARMS, every one a real message that could be fielded, none of them allocated yet. The distinction is allocation and nothing else (JL 260828 asked the right question, "它不应该就是 ARM 的一种吗", and the answer is yes): a candidate becomes a fielded arm the moment someone assigns traffic to it, that assignment is the task layer's act, and this board never performs it. The pool unit is therefore the lightest unit in this plugin, and everything stripped from it was stripped for one reason: it belonged to designing an EXPERIMENT, and this unit designs a MESSAGE SET.

```text
<page>/design/
└── DU<NN>-<slug>/
    ├── card.md            the brainstorm card, per §card law 5
    ├── README.md          unit · kind · serves · pool: <n> · state: draft
    ├── spec.md            compiled as ever: requirements ← Brief · rails ← venue
    │                       pack · acceptance ← the five pool checks below
    ├── evidence.md        one paragraph saying exactly this: nothing in a pool
    │                       is a claim, so nothing here binds evidence — see
    │                       inspiration.md · the ignore-card precedent, and what
    │                       keeps `unit-file-missing` honest
    ├── ideation.md         the diverge-then-converge record, unchanged
    ├── content/pool.txt    N numbered messages, every one newly authored, each
    │                       carrying one `trying:` line naming what it reaches for
    │                       and one `from:` line naming where the reach came from (§from)
    └── inspiration.md      what was read, listed · NOT an evidence chain
```

**§from · every entry says where its reach came from (JL 260828: "要不然谁能知道，对吧？谁能看得出来呀？").** One `from:` line per entry, beside `trying:`. It is an honesty label, not a warrant — the same class as the `intuition` label §ideation already mandates, extended to the finished entry — so it does not make the entry a claim and it does not repeal INSPIRATION-NOT-WARRANT. Three words, composable with `×`:

```text
from: insight · <row id>          the entry is seeded by a named row the unit's
                                  grant reaches (e.g. `insight · GI14-prior-exposure`)
from: knowledge · <mechanism>     general behavioral or craft knowledge the designer
                                  brought, named in plain words (e.g. `knowledge ·
                                  verification framing`)
from: intuition                   the designer's own sense, no external seed —
                                  legal, and ALWAYS carrying the unit's information
                                  regime, because the two intuitions are different
                                  things (JL 260828: "啥都没有的时候你有一种
                                  intuition，看了一部分东西之后再有 intuition，
                                  效果可能完全不一样"):
                                    intuition · brief-only   arose with no insight
                                                             rows in hand
                                    intuition · informed     arose after reading the
                                                             rows inspiration.md lists
```

The line is derivable, not invented: converge's finalist-to-ancestor map already records each finalist's angle (`goal-first` and `theory-riff` ancestors are `knowledge`, labeled-`intuition` ancestors are `intuition`, a candidate ideation explains via a named row is `insight`), and the unit's regime is a card-level fact. An entry may compose (`insight · GI14 × intuition · informed`). The open research question this line makes answerable — what informed intuition produces that blind intuition cannot, for the same audience — has its first natural experiment in DU16 (brief-only) against DU17/DU18 (informed), same people, on this board.

What does NOT apply, stated as absences so no actor supplies them from habit:

```text
no warrant duty     inspiration is not warrant · no sentence in a pool owes a
                    citation, because no sentence in a pool is a claim — the
                    evidence.md on disk exists to SAY so, not to bind rows
no prospect.md      a forecast is per-BET; a pool is not a bet · GD4 does not
                    reach a pool unit
no control cell     and no allocation, no power arithmetic, no predicted effect
no reuse            ZERO · a fielded template may not appear as an entry, a
                    variant, or a candidate · the fielded set is the AVOID list
```

What the judge checks, and it is only this: the count reaches `pool-target:`; every entry is newly authored, byte-diffed against the whole fielded set; the entries are MUTUALLY distinct, so a pool of near-duplicates fails as surely as a pool of quotations; every entry carries its `trying:` line; every entry carries its `from:` line, and a `from: insight` names a row the grant actually reaches while an `intuition` carries its regime word; every entry passes the venue rails, because a message that cannot be sent is not a candidate. Six checks (the `from:` line joined 260828; pools judged before it carry the lines by backfill from their own ideation records, a maintenance act, and are not re-judged for it).

**What happens next, and why it is not here.** Which entries get fielded, against which control, at what size, is the FIELDING decision, and it belongs downstream with the task layer that ships and measures. A pool that is never fielded is still a completed unit: it is the design space, written down. This separation is the whole point of the stance, and pulling comparator duties back into the pool is the failure it was written to prevent.

**One word this family uses badly, recorded so it stops causing confusion.** `haipipe-designer-agent` is named for the thing it writes toward, not the thing it is: it is a WRITER of units, never an arm. A pool entry, a variant and a fielded arm are the same species of object at three moments of one life — written, chosen, allocated — and only the third is an experiment's arm. When this plugin says a pool holds candidates rather than arms, it means unallocated, never a different kind of thing.

## Novelty · what a `generate` unit owes (260828)

A unit realizing a `generate` card (§card law 4) inverts the family's non-novelty habit: where an explore unit's virtue is holding every byte it can, a generate unit's DUTY is to differ. Its `spec.md` carries one more block, and the judge fails the unit without it:

```text
novelty   ← the card's warrant pair, instantiated:
            surface     what in content/ differs from EVERY fielded template,
                        stated concretely (a byte-diff no reader has to run)
            mechanism   the theory mechanism that surface instantiates, named
                        as the card's stance: names it
            anchors     the warrant-theory QA file and warrant-insight row,
                        cited by path — the same two legs the card holds
```

Byte-identity of a generate unit's cell to any fielded template FAILS the unit outright: nominating existing copy is the bet-against lane's move, and two field rounds (260827 DU06, 260828 DU07-09) proved a designer under pressure will retreat there unless the retreat is illegal. The lawful poverty exit is EMIT, never quotation. Variants compose: a generate unit may ship `v-a`, `v-b` under the one wager, each variant satisfying the novelty block on its own bytes.
