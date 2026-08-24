---
name: haipipe-design
description: >-
  The design door of the Application family: one place assembling the laws for a DesignBoard that designs as BETS. A board declares reads: (which InsightBoards anything on it may cite); a Brief declares born-of: (the signed W handoff or the mandate it exists because of); a Design page proposes strategy cards in its direction/ plugin (stance toward evidence, thesis, expected effect), a person releases each card, one arm-agent realizes each released card as one artifact unit in the design/ plugin, a judge checks the unit against its compiled spec, and a person accepts each division. Ends at ACCEPTED, never ships. Use for creating or driving a DesignBoard, writing a brief, proposing or releasing direction cards, realizing units, message or email or UI design, reviewing and accepting. Trigger: design board, design door, direction card, release cards, design unit, message design, email design, ui design, born-of, reads whitelist, stance, /haipipe-design.
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "0.2.0"
  last_updated: "2026-08-24"
  summary: "0.2.0 (JL 260824): the Reads Law now says a grant NAMES InsightBoard pages without breaching the principle layer's warrant monopoly, and covers a board that declares no reads: at all — `mode: record`, for pre-contract artifacts. 0.1.0: the door, two plugins, one agent, three declarations."
---

# /haipipe-design · design as bets, within a declared grant

`haipipe-application` remains the Application umbrella (two-board pairing, PageX crossing, ends-at-ACCEPTED); this door owns the DesignBoard's own laws and verbs. Physically it lives inside `skills/application/` because a DesignBoard cannot exist outside an Application; the slash name is first-class regardless.

**Who owns what**:

```text
haipipe-design               this door · the reads/born-of/stance laws · the verbs
haipipe-plugin-direction     the strategy CARD: proposal, release gate, grant
haipipe-plugin-design        the artifact UNIT: spec, evidence, content, kind routing
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

## The two births of a Brief

```text
mandate-first    a person names the program; needs are raised 🔴 and land on the
                 InsightBoards' registers unanswered
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
direction | cards   propose cards at `proposed` on one DS page · NEVER release them
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

No design-specific phase machine exists; the mapping is three lines and the page family owns the rest:

```text
READ + FRAME     BR00 through its own page RUN (born-of resolves at its EVIDENCE)
DIRECT           the DS page's card proposals + the person's release — plugin state, not a phase
COMPOSE + ACCEPT the DS page's RUN: units land at EVIDENCE, divisions cite them at DRAFT,
                 acceptance rows are the human gate CHECK already owns
```

## Ends at ACCEPTED

A landed, accepted unit is a design decision, not a shipment. Building, sending, and measuring are task-layer work; reading the actual effect back against each card's expected effect is an InsightBoard's, and a `bet-against` card that wins is new evidence flowing there, citing itself.
