---
name: haipipe-design
description: >-
  The design door of the Application family: one place assembling the laws for a DesignBoard that designs as BETS. A board declares reads: (which InsightBoards anything on it may cite); a Brief declares born-of: (the signed W handoff or the mandate it exists because of); a Design page proposes design cards as card.md, the first file of each thread folder under its design/ plugin (stance toward evidence, thesis, expected effect), a person releases each card, one designer realizes each released card as one artifact unit in the design/ plugin, a judge checks the unit against its compiled spec, and a person accepts each division. Ends at ACCEPTED, never ships. Use for creating or driving a DesignBoard, writing a brief, proposing or releasing design cards, realizing units, message or email or UI design, reviewing and accepting. Trigger: design board, design door, design card, release cards, design unit, message design, email design, ui design, born-of, reads whitelist, stance, /haipipe-design.
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-design · design as bets, within a declared grant

`haipipe-application` remains the Application umbrella (two-board pairing, PageX crossing, ends-at-ACCEPTED); this door owns the DesignBoard's own laws and verbs. Physically it lives inside `skills/application/` because a DesignBoard cannot exist outside an Application; the slash name is first-class regardless.

**Who owns what**:

```text
haipipe-design               this door · the reads/born-of/stance laws · the verbs
haipipe-design-workflow      the lane's phase machine: D0-D5, gates GD0-GD6, rounds,
                             the commission entry
haipipe-plugin-design        the Design-family THREAD contract, physically beside
                             this door: the card (§card — proposal, release gate,
                             grant) and the unit (spec, evidence, prospect, content,
                             kind routing, the judged: verdict line) · absorbed
                             haipipe-plugin-direction 260828
haipipe-design-brief/-card/-unit/-verdict/-division/-pagedown
                             the six phase-owned Folder contracts
haipipe-folder               the shared two-face Folder contract
haipipe-page-workflow        the loop every page here runs, like every page anywhere
```

## 🚧 The boundary: no experiment inside

Ruled by JL, 260828, and every law in this family is read under it: this board's purpose is DESIGN, and the real experiment belongs to another team, outside the board. Two clauses, in JL's own terms: ① inside the boundary there is NO experiment — no control cell, no allocation, no power arithmetic, no measured comparison lives on any page here; ② the board's whole deliverable is well-designed CANDIDATES, and only after they leave does anyone experiment on them.

The word law that follows: **arm is the experiment's word**, reserved for a message that has been allocated traffic downstream, and nothing on this board is ever called one. A candidate becomes an arm at the moment of allocation, and that moment never happens here.

**One family, one prefix** (JL 260828, "unify the names", completed the same day by the one-thread-one-folder merge): the three stations of a bet share the design- prefix and read as one line — the **design card** states the bet (`card.md`, the first file of the thread folder), the **designer** realizes it (`agents/haipipe-designer-agent`, renamed from arm-agent the same day the boundary was ruled), and the **design unit** carries it (the folder itself, id `DU<NN>` under `design/`; the old dual DR/DU numbering and the `direction/` folder retired when the card moved in, and with them both pointer fields, since a shared folder cannot dangle). Around them: **candidate** (a written message not yet allocated), **variant** (one wager said several ways), **pool** (a brainstorm card's set of candidates), **division** (the ledger row a person accepts), **judge** (the fresh-context verdict writer). In family prose the bare words card, designer, unit suffice; the full design- forms are for speaking outside the family.


## The Reads Law · a four-level narrowing chain

Authority to cite evidence narrows at every level, and each level must sit inside the one above (⊆). Enforcement is two-sided: at dispatch the packet contains only granted evidence, so an agent cannot wander; at judge the three set-differences are checked.

```text
① board.md    reads: A01 · A02                 board whitelist · set once at scaffold
② BR00        born-of: A01·W01                 the Brief's birth · ⊆ ①
③ design card stance: follow A01·W01 · grant   the bet's evidence · ⊆ ①
④ design unit evidence.md rows                 what the artifact cites · ⊆ ③
```

A grant NAMES InsightBoard pages by path — and, since 0.5.0, may also name a
Discovery QA file when a card's warrant-theory leg requires one, PROVIDED the
board's `reads:` lists the discovery bank. That does not replace the D4
warrant role: `haipipe-design-division` owns WHY a division may exist, while
a grant names evidence a designer may quote while composing. Warranting and
granting are different acts.

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
            design cards — propose wide, bet narrow, release fewer still
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
<Topic>-DesignBoard/        canonical; optional B<NN>_ ordering prefix
├── board.md                 spine · close · reads:
├── 0-BR-brief/BR00-brief/   born-of: · opportunity · audience set · outcome+kill ·
│                            venue scope · promise · needs (OUT to insight registers) · roster
├── (1 vacant)               the principle group's reserved slot; principles exist only
│                            promoted (haipipe-design-division: reuse across pages,
│                            or two boards in conflict)
├── workflow/rounds/         one minimal R<NN>-pagedown/ receipt Folder per sealed round
└── 2-DS-design/DS<NN>-<audience>-<job>-<venue>/
    ├── DS<NN>-….md          one division per landed unit: cites DU id · stance · accepted:
    ├── design/              one THREAD per folder (260828: direction/ retired):
    │   └── DU<NN>-<slug>/   one stable Folder evolving in place:
    │                        design-card → design-unit → design-verdict;
    │                        workflow/phase.yaml preserves every transition
    └── outline/ · evidence/pagex/ · delivery/render/   selected Page capabilities
```

## The Folder phases this door owns

```text
D0  haipipe-design-brief       frame one board
D1  haipipe-design-card        state and release/kill one bet
D2  haipipe-design-unit        realize one released card
D3  haipipe-design-verdict     judge realization and prospect independently
D4  haipipe-design-division    render; accept or emit; promoted Principle lives here
D5  haipipe-design-pagedown    make grown pages read true and seal the round
```

These are workflow phases, not independent configuration/Page-Type skills.
Every phase owns both faces and its selected plugins. Legacy `page-type: brief`
resolves to D0 and `page-type: design` resolves to D4. Principle has no
independent phase: D4 promotes it only on reuse/conflict, and D5 rereads it.

## Verbs

```text
enter | status      resolve the board · derive frontier from disk · count cards by state
brief               create/resume BR00 · either birth · needs rows carry register ids
design              create/resume one DS page (audience × job × venue, per the roster)
diverge | ideate    build or extend the DS page's ideation SLATE: goal, then many
                    candidate moves, evidence-fed and theory-fed both · judged
                    loosely, most die unminted
cards | bet         mint the few slate rows worth wagering as cards at `proposed`
                    on one DS page · NEVER release them
release | kill      RECORD a person's decision on named cards · never decide it
realize | compose   for each released, unlanded card: dispatch one designer
                    (agents/haipipe-designer-agent) · packet carries only the grant ·
                    inline fallback runs the same contract serially when agents are unavailable
judge               check each landed unit against its spec's acceptance list + the ⊆ chain
render              project content/ through the page's delivery/render/ plugin
accept              record the person's per-division accepted: row · last design decision;
                    PageDown/GD6 still seals the round
workflow | run      drive: propose → ✋release → realize → judge → ✋accept → PageDown/GD6 · STOP
```

The two Design cross-phase ✋ gates never have an auto mode: releasing a card
and accepting a division are a person's. Page-local outline/read/verified ticks
remain nested authoring controls rather than extra GD transitions. Every page
dispatched into `haipipe-page-workflow` pins `mode: copilot`.

## The journey, mapped onto existing machinery

The lane has its own phase machine since 260827, `haipipe-design-workflow`: six phases named by the lane's artifact classes — D0 Brief, D1 Card, D2 Unit, D3 Verdict, D4 Division, D5 PageDown — with gates GD0-GD6, the THREAD (a card until it lands, the division row after) as frontier unit, rounds that always complete, the two-faced verdict (reflect ex-post · prospect ex-ante) and the EMIT edge through BR00's needs. The division of labor with this door:

```text
this door        the LAW: reads/born-of/stance, the grant chain, the two ✋ · and
                 the VERBS, which are HOW one thread moves
design-workflow  the PHASES: where a thread is, which gate it faces, rounds,
                 receipts, stop rules · and the one-sentence commission entry
page-workflow    OUTLINE…CHECK inside every single page RUN (BR00, the DS page)
```

## Ends at ACCEPTED

A landed, accepted unit is a design decision, not a shipment. Building, sending, and measuring are task-layer work; reading the actual effect back against each card's expected effect is an InsightBoard's, and a `bet-against` card that wins is new evidence flowing there, citing itself.
