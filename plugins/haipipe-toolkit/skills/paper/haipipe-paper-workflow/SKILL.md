---
name: haipipe-paper-workflow
description: >-
  The paper-level phase machine: six phases (Ideation -> Seed -> Roadmap ->
  Narrative -> Section -> Round) with a checkable gate between each. Use when
  asking where a paper is, whether it may advance, or what to mint next.
  Trigger: paper journey, what phase are we in, phase gate,
  /haipipe-paper-workflow.
metadata:
  version: "0.6.2"
  last_updated: "2026-08-31"
---

# /haipipe-paper-workflow · know the phase, test the gate, mint the next page

Load `haipipe-paper` first; this file is its phase authority. It never edits a
Page, never runs a Page's lifecycle (that is `haipipe-page-workflow`), and
never judges content (that is CHECK plus the human ticks).

## 🔤 Terminology law

A **journey phase** is one of the six positions below (P0–P5). A **Page
phase** is one step of `haipipe-page-workflow`'s OUTLINE…CHECK loop. Every
`[phase]` argument in the door's verbs is a PAGE phase; a bare "phase" in any
Paper document must be readable as exactly one of the two, or it is a defect —
the same law the Round contract holds for "Paper Round" versus "workflow
round". Prefer "journey" when speaking of P0–P5.

**The naming law (0.5.0)**: a journey phase is NAMED BY ITS AUTHORITY PAGE
TYPE — Ideation, Seed, Roadmap, Narrative, Section, Round — so nobody
maintains a second vocabulary. Each phase keeps its old verb as a
parenthesized ALIAS — Ideation (ideate), Seed (establish), Roadmap (route),
Narrative (tell), Section (realize), Round (respond) — legal in prose, never
in a folder or page id. A future phase inherits this law: it takes its
authority page's name and may carry one verb alias.

## 🧭 Why this is not the retired stage lane

The deleted S01–S10 machinery owned ten content contracts, a resolver, and
per-stage tooling. This file owns none of that: content lives in the Page
Type contracts, and this file only states WHICH page holds authority in each
phase and WHEN the next one may be minted. Deleting this file would lose no
content rule — that is the test it must keep passing.

## 🗺 The six phases

Each phase's own law ships as one skill under `workflow-phases/`
(`haipipe-paper-ideation` … `haipipe-paper-round`); this file keeps only the
cross-phase journey: names, gates, groups, receipts.

```text
phase                     authority page                 what the phase produces
──────────────────────────────────────────────────────────────────────────────
P0 Ideation (ideate)      ideation   (A1-SD-story/SD00)  a winning idea sent to
                                                         its Seed · the repo is
                                                         minted WITH this page
P1 Seed (establish)       seed       (A1-SD-story/SD01)  a defensible identity
                                                         + E-board
P2 Roadmap (route)        roadmap    (A1-SD-story/SD02)  released blocks: where
                                                         to go, who runs it,
                                                         done-when · then the
                                                         landed QA receipts,
                                                         lap by lap, settled
                                                         back onto the Seed
   ↺ P1↔P2 is the ESTABLISH LOOP · exits only through the Seed at G4
P3 Narrative (tell)       narrative  (A2-NA, 1 per desk) a desk decision +
                                                         section map
P4 Section (realize)      section    (B group, per row)  signed-off units
   P4.9                   assemble — a VERB, not a phase the built deliverable ·
                                                         DRAFT until G6 holds
P5 Round (respond)        round      (in the desk's B)   routed concerns +
                                                         response

library                   venue      (QBv bank)          consulted at P3 §1 ·
                                                         never a phase
```

P0 and P5 are the cheap loop zones: ideas are disposable, rounds recur.
P1–P2 cycle as one loop; P3–P4 are the expensive one-way street the later
gates protect. A round may reopen P1, P3, or P4; a retarget mints a new P3
from the unchanged seed.

## 🔁 The establish loop (P1 → P2 → P1)

The Seed is the scoreboard; the Roadmap is the campaign plan AND the intake
desk, one page. One lap:

```text
Seed §6 states the gaps (⬜/🔨 E-rows)
   → Roadmap proposes BLOCK rows · a person releases them, block by block (G2)
   → the Roadmap dispatches through its probe lane · receipts land on its
     lap divisions (G3)
   → settle: the Seed's E-rows flip ✅ citing the landed QA files
   → gaps remain → next lap on the Roadmap · gaps closed or waived → face G4
```

Two pens, never crossed: the Roadmap plans and registers; the Seed alone
writes E-row flips. The join is one string on two pages: an E-row's cite =
the block row's receipt = the lap's QA path (the last two on the same page).
The loop's only exit is through the Seed at G4 — a Narrative reads the Seed's
§8 handoff and never reads the Roadmap directly, so two tellings can never
keep separate books.

## 🚪 The gates

Each gate is an assertion over pages that already exist. A gate that cannot be
tested by reading named files is misdesigned.

```text
G0  Ideation → Seed        precondition, tested on the idea's summary row
                           alone: per-claim novelty bound to QA files · a
                           pilot result or explicit waiver · a person's
                           PROCEED tick (or PROCEED WITH CAUTION with its risk
                           accepted in the tick) · receipt, recorded after the
                           act: SD01-seed exists in this board's A1-SD-story,
                           its §5 first row binds SD00-ideation back, and the
                           idea's `went to` cell names it (an idea that went
                           to a DIFFERENT paper adds: that new repo exists as
                           a submodule)

G1  Seed → Roadmap         the Seed skeleton stands: its outline is
                           human-ticked and §6 states every proposition as an
                           ⬜/🔨/✅ row, so the gap list is readable

G2  Roadmap plan →         every 🔨/⬜ E-row names a ▶️ released block row
    dispatch               that serves it, or carries an explicit waiver on
                           the Seed's Log · release is a person's act, block
                           by block — a machine proposes and never releases

G3  lap → Seed             the lap's done-when tests hold · every dispatched
                           card binds a landed QA path · the settle is written
                           on the Seed: each flipped E-row cites the QA file
                           its block row landed · gaps remain → the next lap
                           on the Roadmap

G4  Seed → Narrative       the Seed's current outline is human-ticked · every
                           ✅/🔨 E-row cites a §5 asset and carries its novelty
                           reading · the pitch sells nothing beyond ✅ rows
                           (placeholders visible otherwise)

G5  Narrative → Section    the Narrative's §1 binds one bank page · every claim
                           row names an E-row parent · every section-map row
                           names its unit page and budget

G6  Section → assemble     every map row's unit page is CHECK-closed
                           (✅ SETTLED) · `/haipipe-paper-assemble` itself
                           RUNS ANYTIME from the active desk-room source — a
                           build made while G6 fails is watermarked DRAFT in
                           its receipt, one made while it holds is
                           SUBMISSION-READY · the gate informs, the person
                           decides, and the upload is a human act either way

G7  Round (per round)      every received concern appears exactly once in the
                           ledger and routes exactly once — to the Seed when it
                           demands evidence the paper does not hold, to the
                           Narrative for a retelling, to a Section for a rework
                           — and a person approves the response receipt
```

Gate numbers are stable across 0.6.0: G2 and G3 both read the Roadmap now
(its plan face and its lap face), and no other gate moved.

## 🗃 Group mapping (JL 260828)

```text
P0–P2   A1-SD-story/         SD00-ideation · SD01-seed · SD02-roadmap —
                             the venue-free head, one each
P3      A2-NA-narrative/     NA<NN>-narrative-<desk>, one page per desk,
                             numbered in arrival order
P4–P5   B<x>-<desk>/         one group per desk: its section pages (S<D> main,
                             SA appendix) AND its rounds (RD token) live together
```

A foreign-desk round (feedback from a desk this board never told) mints that
desk's B group even when the group holds only RD pages. Boards laid out under
the pre-0.5.0 grammar (narratives inside the SD story group, a lone
C1-RD-round group), and boards holding a separate `SD03-collection` page from
the 0.5.0 era, are grandfathered and migrate only on explicit request.

## 📜 Gazette of retired names

Documents dated before the version shown use the old vocabulary; read them
against this table and do not rewrite frozen files:

```text
old phase name        new phase (alias)          old gate         new gate
──────────────────────────────────────────────────────────────────────────
— 0.6.0 (260828): the Collection page folded into the Roadmap ——————————
P3 Collection         P2 Roadmap (route) ·       G3 (unchanged    G3
   (collect)          its lap divisions          number)
P4 Narrative (tell)   P3 Narrative (tell)        G5               G5
P5 Section (realize)  P4 Section (realize)       G6               G6
P6 Round (respond)    P5 Round (respond)         G7               G7
— 0.5.0 (260824) ————————————————————————————————————————————————————————
P0 Ideate / Explore   P0 Ideation (ideate)       G0               G0
P1 Establish          P1 Seed (establish)        G1 (est→tell)    G4
P2 Tell               P4 Narrative (tell)        G2               G5
P3 Realize            P5 Section (realize)       G3               G6
P4 Respond            P6 Round (respond)         G4               G7
(none)                P2 Roadmap (route)         (none)           G1 · G2
(none)                P3 Collection (collect)    (none)           G3
```

## 🧾 Phase receipts

A phase transition leaves exactly one receipt: a dated Log row on the page
that granted it (the Ideation Page for G0, the Seed for G1 and G4, the
Roadmap for G2 and G3, the Narrative for G5 and G6, the Round for G7),
stating the gate, the assertion results, and who ticked. No separate receipt
store exists; the pages are the record.

## ⏱ Advancement is never scheduled

A gate test may be run any time; a gate may only be DECLARED passed by the
human tick or CHECK verdict it names. Nothing in this file may be wired to a
timer, a heartbeat, or a loop that advances phases on wall-clock time — a
recurring job may report "gate G6 still fails: SM04 not settled", never "gate
passed". (Adopted from the ARIS external-cadence rule: a heartbeat may say
keep going, never good enough.)

## 🔀 Resolving "what phase are we in"

Phase is read, not stored: it is the highest gate whose assertion currently
holds, per telling. Inside the establish loop the reading is the lap: a paper
with released blocks still running sits at P2 with cards out; one whose last
lap settled and left gaps sits at P2 planning the next release. Two tellings
of one paper may sit in different phases — the MS telling in P5 while a WISE
telling is in P4 — because P3 onward is per-narrative. P0–P2 are per-paper
and shared.
