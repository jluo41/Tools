# The workflow: five phases named by their authority page, and six gates

state: ✅ SETTLED · 0.5.0 delegates the climb loop's law to /haipipe-insight 260827 · ACCEPT retired as a phase
owner: JL

## Opening

Which page runs next, and where must a run stop for a person?

Five journey phases in two lanes, each NAMED BY THE PAGE THAT HOLDS AUTHORITY in it, and six gates that are assertions over pages already on disk. The InsightBoard lane climbs Meta, Chain, Wisdom; the DesignBoard lane frames and composes; they touch only at the PageX crossing. Phase is read from disk on every invocation and never stored.

### Writing Style

A phase name must tell a reader which page to open. If it does not, it is a verb pretending to be a place.

## Diagram

```text
🔎 InsightBoard lane                     🎨 DesignBoard lane
P0 Meta (scope)    MT00 + MT01-04        P3 Brief (frame)   BR00
   │ G0                                     │ G4
P1 Chain (climb)   the frontier rung      P4 Design (compose) DS<NN> + 3 plugins
   │ G1  ✋ probe release inside            │  ✋ card release inside
P2 Wisdom (hand off) the W page           ══ G5 ✋ accept ══▶ STOP
   │ ✋ G2 signed
   └─ G3 settle ──▶ ↺ back to P1          P4.9 accept is a GATE, not a phase
                    │
                    └──── PageX ─────────────▶ P4 has nothing local to bind
                                               until P2 has a signed handoff
```

## Content

### 1 · The naming law

**What changed**: phases were verbs, and a verb does not name a place.

```text
before (0.3.0)        after (0.4.0)             authority page
──────────────────────────────────────────────────────────────────────
① SCOPE               P0 Meta (scope)           meta + question registers
② CLIMB               P1 Chain (climb)          the chain's frontier rung
③ HANDOFF             P2 Wisdom (hand off)      the W page
④ FRAME               P3 Brief (frame)          brief
⑤ COMPOSE             P4 Design (compose)       design + direction/ design/ render/
⑥ ACCEPT              RETIRED as a phase        it had none of its own
```

A journey phase is named by its authority page and keeps its old verb as a parenthesized alias, so nobody maintains a second vocabulary. The law was adopted from `haipipe-paper-workflow` 0.5.0, which had already solved it.

#### 2 · Why ACCEPT stopped being a phase

The naming law is also a test. ACCEPT's acceptance row lives on the Design page's own division, so it never had an authority page distinct from P4's, and a position that cannot name one is a gate wearing a phase's clothes. It is now G5, and six phases became five. The paper family made the same call for `assemble`, which it records as a VERB and not a phase.

#### 3 · Two loops, each with three pens that never cross

```text
CLIMB LOOP  P0 → P1 → P2 → P0, law delegated to /haipipe-insight
  register writes STATE, never a finding
  chain pages write FINDINGS, never their own register cell
  handoff EXPORTS, never re-derives
  the join: register cell's cite = closing page's id = handoff's SERVES row

COMPOSE LOOP  inside P4, law delegated to /haipipe-design
  card holds the WAGER · unit holds the ARTIFACT · division holds the ACCEPTANCE
```

The climb loop's only exit is through the register at G3, so a Design page reads a signed handoff and never a D, I or K page's prose. Two consumers can then never keep separate books.

#### 4 · Gates are assertions, not intentions

```text
G0  MT00 past 🔴 and its source resolves to a run · four registers exist ·
    every question carries a state cell
G1  this question's D/I/K rungs are CHECK-closed, values bound to QA files ·
    partition-major boards additionally need the X group's pooling verdict
G2  ✋ the W page's Design Handoff carries the person's tick
G3  the register cell flips ✅ or 🚫-with-reason, citing the page that closed it
G4  BR00 past 🔴 · `born-of:` resolves · needs carry register ids · `reads:` set
G5  ✋ every division carries an acceptance row and its render EXISTS and is current
```

A gate that cannot be tested by reading named files is misdesigned. That single sentence is what keeps this file from becoming the retired stage engine `QC2` documents.

#### 5 · Four human gates, not three

```text
✋ probe release   INSIDE P1, per page      cards presented, dispatched on approval
✋ handoff         at G2                    signed, never ticked by a machine
✋ card release    INSIDE P4, per card      added by the design family 260824
✋ acceptance      at G5                    the exact visible version
```

The card-release gate was live for a day before this file named it, while the file still said "three gates". Every dispatch therefore pins `mode: copilot`, because page-auto defers `approved:`/`accepted:` onto the owed ledger and would mechanically pass a gate.

#### 6 · Receipts live on the pages

A phase transition leaves one dated Log row on the page that GRANTED it. No separate store is authoritative, which replaced an unaudited `_runs/application/log.md` the previous version had itself marked as having no auditor. A trace that disagrees with the pages loses.

## Aims

### A1 · The naming law
- ✅ A1.1 · Every phase name identifies a page a reader can open.
  **Done when:** each of the five names a page type or role, and none is a bare verb.
  **Now:** Five phases, five authority pages; ACCEPT failed the test and became G5.


#### A4 · Gates
- ✅ A4.1 · Every gate is testable by reading named files.
  **Done when:** no gate's assertion requires interpreting prose.
  **Now:** G0 through G5 each name the files they read.


#### A6 · Receipts
- ✅ A6.1 · The record cannot drift from the artifact.
  **Done when:** the pages are authoritative and any trace is explicitly subordinate.
  **Now:** Receipts moved onto the granting pages on 260824; the run log is a trace.


## Discussion

## Files

### 📋 Contracts
- `../../../../application/haipipe-application-workflow/SKILL.md`
  The phase machine this page documents.
- `../../../../application/haipipe-application/SKILL.md`
  The door whose `frontier:` scalar must never disagree with the phase reading.
- `../../../../application/haipipe-insight/SKILL.md`
  The insight door the climb loop's law is delegated to since 0.5.0.
- `../../../../application/haipipe-insight-workflow/SKILL.md`
  The insight lane's interior phase machine since 0.6.0: I0-I5, gates GI0-GI6, the cell frontier.
- `../../../../application/haipipe-design-workflow/SKILL.md`
  The design lane's interior phase machine since 0.7.0: D0-D4, gates GD0-GD5, the division frontier, rounds, reflect/prospect, the EMIT edge.
- `../../../../paper/haipipe-paper-workflow/SKILL.md`
  The sibling machine the naming law, the gazette and the receipt rule were taken from.

## Law

A journey phase is named by its authority page. A position that cannot name one is a gate, not a phase.

## Log

260824 · Restyled on `haipipe-paper-workflow` 0.5.0: phases named by authority page with verb aliases, gates numbered G0-G5, a gazette of retired names, the never-scheduled rule, and receipts moved onto the granting pages.

260824 · ACCEPT retired as a phase and the fourth human gate named. The file had said "three gates" since the design family added card release the same day.

260827 · The climb loop's law delegated to the new insight door `/haipipe-insight` (workflow 0.5.0), exactly as 0.3.0 delegated the compose loop to `/haipipe-design`; the workflow keeps the lap, the order and gates G0-G3. Each lane now has its own law door, two ✋ gates per door.

260827 · The design lane's interior machine landed, `/haipipe-design-workflow` (app workflow 0.7.0): D0-D4 named by the lane's artifact classes (a stated extension of the naming law from page to artifact), the division as frontier unit, rounds that always complete, the two-faced verdict — reflect (ex-post) · prospect (ex-ante) — and the EMIT edge into the insight registers. Both lanes now carry door + machine, fully symmetric.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0