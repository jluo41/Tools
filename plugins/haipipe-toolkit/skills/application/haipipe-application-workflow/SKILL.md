---
name: haipipe-application-workflow
description: >-
  The application-level phase machine: five phases named after their authority
  pages, in two lanes — Meta (scope) → Chain (climb) → Wisdom (hand off) on the
  InsightBoard, Brief (frame) → Design (compose) on the DesignBoard, joined only
  at the PageX crossing. One gate between each, every gate a checkable assertion
  over existing Pages. Meta, Chain and Wisdom form the climb loop: state the gap
  on a register, climb one rung, settle back onto the register, lap after lap,
  until the question is answered or refused. It owns transitions, gates and
  phase receipts only — content authority stays with the Page Type contracts,
  lifecycle authority with haipipe-page-workflow, design-side law with
  haipipe-design, and every verdict with an independent CHECK plus a human tick.
  "Journey phase" (P0-P4) and "Page phase" (OUTLINE…CHECK) are distinct words by
  law. Use when asking where an Application is, whether it may advance, what the
  next runnable page is, or where a run must stop. Trigger: application
  workflow, run the application, drive the boards, next page, application
  frontier, what is runnable, climb loop, compose loop, phase gate,
  /haipipe-application-workflow.
metadata:
  version: "0.4.0"
  last_updated: "2026-08-24"
  summary: "0.4.0 (JL 260824, restyled after haipipe-paper-workflow 0.5.0): phases are NAMED BY THEIR AUTHORITY PAGE with the old verb kept as a parenthesized alias — Meta (scope), Chain (climb), Wisdom (hand off), Brief (frame), Design (compose) — so no second vocabulary is maintained; ⑥ ACCEPT is retired AS A PHASE because its acceptance row lives on P4's own division and a phase with no authority page of its own is a gate wearing a phase's clothes; gates are now numbered G0-G5 as grep-able assertions; the FOURTH human gate (card release, added by haipipe-design and previously unlisted here) is named; receipts move onto the pages that grant them, the paper family's rule, and the unaudited _runs log is demoted to a trace; adds the terminology law, the group mapping, a gazette of retired names, and the never-scheduled rule. 0.3.0: the design lane's interior law moved to /haipipe-design. 0.2.0: mode: copilot pinned on every dispatch; phase-to-frontier mapping; signed defined. 0.1.0: six phases, two lanes, three gates."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-application-workflow · know the phase, test the gate, mint the next page

Load `haipipe-application` first; it says what an Application IS and this file is
its phase authority. It never edits a Page, never runs a Page's lifecycle (that
is `haipipe-page-workflow`), never states design-side rules (that is
`haipipe-design` since 0.3.0), and never judges content (that is CHECK plus the
human ticks).

## 🔤 Terminology law

A **journey phase** is one of the five positions below (P0–P4). A **Page phase**
is one step of `haipipe-page-workflow`'s OUTLINE…CHECK loop. A bare "phase" in
any Application document must be readable as exactly one of the two, or it is a
defect. Prefer "journey" when speaking of P0–P4; when a receipt could be read
either way, prefix the lane emoji, so `🔎P1` is the climb and a plain ② in a page
context is PROBE.

**The naming law (0.4.0)**: a journey phase is NAMED BY ITS AUTHORITY PAGE —
Meta, Chain, Wisdom, Brief, Design — so nobody maintains a second vocabulary.
Each keeps its old verb as a parenthesized ALIAS: Meta (scope), Chain (climb),
Wisdom (hand off), Brief (frame), Design (compose). The alias is legal in prose,
never in a folder or page id. A future phase inherits this law, and a candidate
phase that cannot name an authority page of its own is not a phase — that test
is what retired ACCEPT.

## 🧭 Why this is not the retired lifecycle lane

The deleted lane under `_old/` owned a dozen content contracts (seed,
descriptions, themes, claims, advice, pitch, narrative, display, section-edit)
plus a phase tree and a deliver tree. This file owns none of that: content lives
in the Page Type contracts, and this file only states WHICH page holds authority
in each phase and WHEN the next one may be minted. **Deleting this file would
lose no content rule** — that is the test it must keep passing.

## 🗺 The five phases, in two lanes

The lanes may start in either order, because Brief and Meta are both head pages
and `haipipe-application` rules their order free. A single line would be a lie;
the crossing is the only joint.

```text
phase                    authority page                what the phase produces
──────────────────────────────────────────────────────────────────────────────
🔎 InsightBoard lane
P0 Meta (scope)          meta + question registers     a question board: what
                         (0-MT-meta/MT00 · MT01-MT04)  data exists, what is asked
P1 Chain (climb)         the chain's FRONTIER rung     one rung closed, its
                         (a data/information/          answer bound to a QA file
                          knowledge page)
P2 Wisdom (hand off)     wisdom (the W page)           counsel + a SIGNED Design
                                                       Handoff
   ↺ P0↔P1↔P2 is the CLIMB LOOP · exits through the register at G3

🎨 DesignBoard lane
P3 Brief (frame)         brief (0-BR-brief/BR00)       audience, outcome, kill,
                                                       venue, needs raised OUT
P4 Design (compose)      design (2-DS-design/DS<NN>)   judged units and the
                         + its direction/ design/      divisions that cite them
                         render/ plugins
   P4.9 accept — a GATE, not a phase                   the person's per-division
                                                       row · then STOP

               🔎P2 ────────── PageX ────────── 🎨P4
        P4 has nothing LOCAL to bind until P2 has a signed handoff; a settled
        `scope: task` Page bound through PageX is the legal dataset-first
        alternative (door §Dataset-first), under which local P2 may stay empty
```

P0–P2 cycle as one loop and are per-QUESTION, so two questions may sit in
different phases at once. P3–P4 are per-DESIGN-PAGE and are the expensive
one-way street the later gates protect. RUN is deliberately not ADVANCE: a
reopened source drops a chain back into P1 while another design sits at G5. **The
phase names name the FRONTIER, never a completed stage.**

## 🔁 The climb loop (P0 → P1 → P2 → P0)

The register is the scoreboard, the chain is the work, the handoff is the export.
One lap:

```text
a register cell states the gap (⬜/🔨 on MT01-MT04)
   → P1 opens the NEXT rung only · probes raised · ✋ a person releases each card
   → answers land · the rung closes CHECK
   → the rung was W? → P2 · ✋ a person signs the Design Handoff
   → settle: the register cell flips ✅, or 🚫 with a reason, citing the page that
     closed it
   → gaps remain → next lap at P1 · every cell settled → the lane is done
```

Three pens, never crossed: the **register** writes STATE and never a finding, the
**chain pages** write FINDINGS and never their own register cell, the **handoff**
exports and never re-derives. The join is one string in three places: the register
cell's cite = the closing page's id = the handoff's SERVES row. The loop's only
exit is through the register at G3, so a Design page reads a signed handoff and
never reads a D, I or K page's prose — two consumers can never keep separate
books.

## 🔁 The compose loop (inside P4, delegated)

`haipipe-design` owns this loop's law; this file owns only its gates.

```text
the Brief's roster names a DS page
   → cards proposed at `proposed` in direction/
   → ✋ a person releases each card, card by card — a machine proposes, never releases
   → one arm-agent per released card → one unit in design/ → judge against its spec
   → the division cites the unit id, its stance, and a render version
   → ✋ a person accepts the division                                          G5
```

Three pens again: the **card** holds the wager, the **unit** holds the artifact,
the **division** holds the acceptance. The unit never restates the wager, and no
machine writes `released:` or `accepted:`.

## 🚪 The gates

Each gate is an assertion over pages that already exist. **A gate that cannot be
tested by reading named files is misdesigned.**

```text
G0  Meta → Chain        MT00 is past 🔴 and its source resolves to a run · MT01-MT04
                        exist · every question carries a register row with a state cell

G1  Chain → Wisdom      this question's D/I/K rungs are CHECK-closed, each value bound
                        to a QA file by path · on a partition-major board the X group's
                        pooling verdict exists, because every W page cites it

G2  Wisdom → signed     ✋ the W page's Design Handoff division carries the person's
                        tick. SIGNED means exactly that tick, written by the person at
                        that page's CHECK; this workflow reads it and never writes it

G3  settle              the register cell flips ✅, or 🚫 with a reason, citing the page
                        that closed it · gaps remain → the next lap re-enters at P1

G4  Brief → Design      BR00 is past 🔴 · `born-of:` resolves · every need it raises
                        carries a register id · the board's `reads:` names every
                        InsightBoard anything on it may cite

G5  Design → accepted   ✋ every division carries an acceptance row naming a reviewer,
                        the unit id and a render version, and the render EXISTS and is
                        current · then STOP: ACCEPTED ends the Application
```

**The four human gates never have an auto mode**, because all four are a person's
by contract. Two sit between phases and two sit inside one:

```text
✋ probe release    INSIDE P1, per page: cards are PRESENTED after drafting and
                    dispatched only on explicit approval (JL ruling, standing)
✋ handoff          at G2: signed by a person, never ticked by a machine
✋ card release     INSIDE P4, per card: `state: proposed` → `released`, a person's
                    act (haipipe-plugin-direction law 1). Added by the design family
                    on 260824 and unlisted here until 0.4.0 — this file said "three
                    gates" while four were live
✋ acceptance       at G5: the exact visible version is explicitly accepted
```

Every dispatch therefore pins `mode: copilot`, because page-auto defers
`approved:`/`accepted:` onto the `--owed` ledger and would mechanically pass a
gate. A blocked gate is a clean stop: report the frontier, the waiting artifact,
and the person's owed decision, then end the run.

## 🗃 Group mapping

```text
P0        0-MT-meta/            MT00-meta · MT01-MT04 question registers
P1        rung-major:           1-D-data/ · 2-I-information/ · 3-K-knowledge/
          partition-major:      <N>-<L>-<partition>/ with the partition letter
                                prefixed to every page id, plus 9-X-cross/
P2        the W page of whichever layout above (4-W-wisdom/ or <N>-<L>-*/…W…)
P3        0-BR-brief/BR00-brief/
P4        2-DS-design/DS<NN>-<audience>-<job>-<venue>/ and its plugins
          1-P-principle/ stays VACANT unless a principle is promoted
                                (haipipe-page-for-principle: reuse across two or
                                 more Design pages, or two boards in conflict)
```

`ref/partition.md` rules the partition grammar; this file rules only the ORDER,
below.

## 🪜 Partition-major climb order

On a partition-major InsightBoard, P1 has a fixed order, because the cross group
consumes the mirrored ladders and every W page cites the verdict:

```text
F's D/I/K first ─▶ each partition's D/I/K mirror, in parallel ─▶ X group
                                                                  │ XI → XK → verdict
                                                                  ▼
                                                 every W page last, template
                                                 included, all citing the verdict
```

A rung-major board has no constraint beyond each chain's own D→I→K→W order.

## 📜 Gazette of retired names (0.4.0)

Documents dated before 260824 use the old vocabulary; read them against this
table and do not rewrite frozen files:

```text
old phase (0.3.0)     new phase (alias)          gate now
─────────────────────────────────────────────────────────────────────────
① SCOPE               P0 Meta (scope)            G0
② CLIMB               P1 Chain (climb)           G1
③ HANDOFF             P2 Wisdom (hand off)       G2 · G3
④ FRAME               P3 Brief (frame)           G4
⑤ COMPOSE             P4 Design (compose)        G5
⑥ ACCEPT              RETIRED as a phase         G5 — its acceptance row lives on
                                                 P4's own division, so it had no
                                                 authority page of its own
```

## 🔗 Mapping to the door's Status vocabulary

The door's `frontier:` is one scalar; this table is what "never disagree" means:

```text
this skill        door frontier reads
──────────────────────────────────────────────────────────────
P0 Meta           meta
P1 Chain          insight:<id>       the frontier chain page
P2 Wisdom         insight:<id>       that id is a W page; the door has no handoff
                                     token, so P2 is the climb's last stop
P3 Brief          brief
P4 Design         design:<id>, then review
G5 passed         accepted
lanes diverged    the scalar reads the insight lane until G3 closes, then design
```

The door's second axis, `maturity:`, stays solely the Status verb's output; this
skill neither reads nor writes it.

## 🚚 Dispatch: one page at a time

This skill selects a page and hands it to `haipipe-page-workflow` with its Page
Type contract; it never runs a phase of a page itself.

```text
select   the frontier phase's first page whose inputs exist and whose gate is open
load     haipipe-page + the matching haipipe-page-for-<type> contract
run      haipipe-page-workflow over that ONE page · the packet ALWAYS sets
         mode: copilot (see the gates, above)
fold     move the register cell or the acceptance row ONLY on CLOSE; every other
         terminal (HOLD, missing input, version mismatch, human gate, a step or
         round limit) is a named non-settlement and the cell does not move
repeat   until the frontier phase closes or a gate blocks
```

A page whose inputs do not exist is not runnable, and naming WHY is this skill's
answer, never scaffolding the missing input silently.

## 🧾 Phase receipts

A phase transition leaves exactly one receipt: a dated Log row on the page that
GRANTED it — the register page for G0 and G3, the chain's closing rung for G1,
the W page for G2, the Brief for G4, the Design page's division for G5 — stating
the gate, the assertion results, and who ticked. **No separate receipt store is
authoritative; the pages are the record** (adopted from the paper family on
260824, replacing an unaudited log). `<application-root>/_runs/application/log.md`
may still receive one line per run as a convenience trace, and a trace that
disagrees with the pages loses.

## ⏱ Advancement is never scheduled

A gate test may be run any time; a gate may only be DECLARED passed by the human
tick or CHECK verdict it names. Nothing here may be wired to a timer, a
heartbeat, or a loop that advances phases on wall-clock time — a recurring job
may report "G5 still fails: two divisions unaccepted", never "gate passed".

## 🔀 Resolving "what phase are we in"

Phase is read, not stored: it is the highest gate whose assertion currently
holds, per lane and per question. Inside the climb loop the reading is the lap —
a question with probes still out sits at P1; one whose last rung settled and left
the register open sits at P0. Two questions may sit in different phases, and the
two lanes may sit in different phases, which is why the answer is a pair and
never one number.

## 🛑 Stop rules

- STOP at G5: ACCEPTED ends the Application. Building, shipping, running the
  experiment and reading the result back are task-layer and InsightBoard work,
  and this workflow never dispatches them.
- STOP at any gate: report and end, never wait in a loop.
- STOP on contradiction: a frontier that derives to two phases at once (a
  register says answered, the page says 🔴) is reported as a defect, never
  repaired silently.

## ↩ Return

The frontier phase per lane, the pages dispatched this run with their CHECK
outcomes, the gate now blocking with the person's owed decision, and the next
runnable page once that gate clears.
