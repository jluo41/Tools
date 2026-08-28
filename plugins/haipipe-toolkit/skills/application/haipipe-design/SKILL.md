---
name: haipipe-design
description: >-
  The design door of the Application family: one place assembling the laws for a DesignBoard that designs as BETS. A board declares reads: (which InsightBoards anything on it may cite); a Brief declares born-of: (the signed W handoff or the mandate it exists because of); a Design page proposes strategy cards in its direction/ plugin (stance toward evidence, thesis, expected effect), a person releases each card, one arm-agent realizes each released card as one artifact unit in the design/ plugin, a judge checks the unit against its compiled spec, and a person accepts each division. Ends at ACCEPTED, never ships. Use for creating or driving a DesignBoard, writing a brief, proposing or releasing direction cards, realizing units, message or email or UI design, reviewing and accepting. Trigger: design board, design door, direction card, release cards, design unit, message design, email design, ui design, born-of, reads whitelist, stance, /haipipe-design.
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "0.3.0"
  last_updated: "2026-08-24"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-design · design as bets, within a declared grant

`haipipe-application` remains the Application umbrella (two-board pairing, PageX crossing, ends-at-ACCEPTED); this door owns the DesignBoard's own laws and verbs. Physically it lives inside `skills/application/` because a DesignBoard cannot exist outside an Application; the slash name is first-class regardless.

**Who owns what**:

```text
haipipe-design               this door · the reads/born-of/stance laws · the verbs
haipipe-design-workflow      the lane's phase machine: D0-D4, gates GD0-GD5, rounds,
                             the commission entry
haipipe-plugin-direction     the strategy CARD: proposal, release gate, grant
haipipe-plugin-design        the artifact UNIT: spec, evidence, prospect, content,
                             kind routing, the judged: verdict line
haipipe-page-for-brief/-design/-principle   what each page IS
haipipe-page-workflow        the loop every page here runs, like every page anywhere
```

## The Reads Law · a four-level narrowing chain

Authority to cite evidence narrows at every level, and each level must sit inside the one above (⊆). Enforcement is two-sided: at dispatch the packet contains only granted evidence, so an agent cannot wander; at judge the three set-differences are checked.

```text
① board.md    reads: A01 · A02                 board whitelist · set once at scaffold
② BR00        born-of: A01·W01                 the Brief's birth · ⊆ ①
③ DR card     stance: follow A01·W01 · grant   the bet's evidence · ⊆ ①
④ DU unit     evidence.md rows                 what the artifact cites · ⊆ ③
```

A grant NAMES InsightBoard pages by path, and that is not a breach of the principle layer's monopoly: `haipipe-page-for-principle` owns the WARRANT, the reason a division may exist, while a grant is the evidence an arm-agent may quote while composing. Warranting and granting are different acts and the chain above governs only the second.

**A board with no `reads:` at all.** Declaring none is legal and means exactly what it says: nothing on this board may cite anything, so every card's grant is `none` and every unit's `evidence.md` records an absence. That is the correct shape for a board holding a PRE-CONTRACT artifact, one produced before this vocabulary existed, and such a board declares `mode: record` on `board.md`. Record mode relaxes the WORDS and nothing structural: a card may carry a historical `released:` rather than a person's tick, may have no stance, and a unit may sit at `state: historical-record`; files, depth, resolvable references and evidence-within-grant are still checked. Writing a `reads:` line for a source that carries no run identity would assert a grant chain that never existed, which is the one thing a record board must not do.

## Diverge, then bet, then vary · the creative half

The family as first built had only the convergent half: bets, grants, audits. A designer who may only cite is a designer who cannot surprise, so three layers now precede and follow the card, and the card keeps its old job in the middle:

```text
① DIVERGE   an ideation SLATE before any card: many candidate moves, generated
            cheaply and judged loosely — the paper family's Ideation, mirrored.
            Two modes, both legal, both honest about which they are:
              evidence-fed    a move suggested by a granted finding
              theory-fed      a move from a named theory or a declared intuition,
                              NO evidence behind it — legal because the card it
                              becomes will say so (stance: ignore / explore) and
                              carry a falsification line like any other bet
            The slate answers "what is the GOAL and what could serve it";
            wide is the point — most slate rows die unminted, and that is cheap
② BET       the card, unchanged: the few slate rows worth wagering become
            direction cards — propose wide, bet narrow, release fewer still
③ VARY      one thesis, MANY REALIZATIONS: the same nudge said differently is a
            different arm, because verbalization effects are real and the design
            space is mostly HERE. A unit's content/ may hold a VARIANT SET
            (v-a, v-b, …), same wager, different surface; the judge judges each
            against the rails; acceptance may accept a subset; and the
            difference between variants is itself a testable hypothesis the
            unit's prospect names — the EMIT edge's natural cargo
```

The asymmetry with the insight side is deliberate and healthy: insight narrows toward one signed handoff, design widens from it. A design run producing one artifact per released card was insight discipline applied to the wrong lane.

## The two births of a Brief

```text
mandate-first    a person names the program; needs are raised and land on the
                 InsightBoards' registers as open, unanswered cells
evidence-first   one or more SIGNED W handoffs propose it; born-of: names them, and
                 BR00's opportunity, audience, outcome and kill are DRAFTED from the
                 handoff's finding, context, strength/boundary and forbidden clauses;
                 needs whose chains already settled are born ✅
```

Either way `born-of:` is written and resolvable, and a subgroup-audience Design page additionally requires the insight side's SPLIT verdict, exactly as `ref/partition.md` rules for child boards.

## The board, concretely

```text
B<NN>_DesignBoard-<Topic>/
├── board.md                 spine · close · reads:
├── 0-BR-brief/BR00-brief/   born-of: · opportunity · audience set · outcome+kill ·
│                            venue scope · promise · needs (OUT to insight registers) · roster
├── (1 vacant)               the principle group's reserved slot; principles exist only
│                            promoted (haipipe-page-for-principle: reuse across pages,
│                            or two boards in conflict)
└── 2-DS-design/DS<NN>-<audience>-<job>-<venue>/
    ├── DS<NN>-….md          one division per landed unit: cites DU id · stance · accepted:
    ├── direction/           the cards        (haipipe-plugin-direction)
    ├── design/              the units        (haipipe-plugin-design)
    └── outline/ · pagex/ · render/           ordinary page plugins, unchanged jobs
```

## Verbs

```text
enter | status      resolve the board · derive frontier from disk · count cards by state
brief               create/resume BR00 · either birth · needs rows carry register ids
design              create/resume one DS page (audience × job × venue, per the roster)
diverge | ideate    build or extend the DS page's ideation SLATE: goal, then many
                    candidate moves, evidence-fed and theory-fed both · judged
                    loosely, most die unminted
direction | cards   mint the few slate rows worth wagering as cards at `proposed`
                    on one DS page · NEVER release them
release | kill      RECORD a person's decision on named cards · never decide it
realize | compose   for each released, unlanded card: dispatch one arm-agent
                    (agents/haipipe-design-arm-agent) · packet carries only the grant ·
                    inline fallback runs the same contract serially when agents are unavailable
judge               check each landed unit against its spec's acceptance list + the ⊆ chain
render              project content/ through the page's render/ plugin
accept              record the person's per-division accepted: row · the last act
workflow | run      drive the loop: propose → ✋release → realize → judge → ✋accept · STOP
```

The two ✋ gates never have an auto mode: releasing a card and accepting a division are a person's, and every page dispatched into `haipipe-page-workflow` pins `mode: copilot` for the same reason the application workflow does.

## The journey, mapped onto existing machinery

The lane has its own phase machine since 260827, `haipipe-design-workflow`: five phases named by the lane's artifact classes — D0 Brief, D1 Direction, D2 Unit, D3 Verdict, D4 Division — with gates GD0-GD5, the THREAD (a card until it lands, the division row after) as frontier unit, rounds that always complete, the two-faced verdict (reflect ex-post · prospect ex-ante) and the EMIT edge through BR00's needs. The division of labor with this door:

```text
this door        the LAW: reads/born-of/stance, the grant chain, the two ✋ · and
                 the VERBS, which are HOW one thread moves
design-workflow  the PHASES: where a thread is, which gate it faces, rounds,
                 receipts, stop rules · and the one-sentence commission entry
page-workflow    OUTLINE…CHECK inside every single page RUN (BR00, the DS page)
```

## Ends at ACCEPTED

A landed, accepted unit is a design decision, not a shipment. Building, sending, and measuring are task-layer work; reading the actual effect back against each card's expected effect is an InsightBoard's, and a `bet-against` card that wins is new evidence flowing there, citing itself.
