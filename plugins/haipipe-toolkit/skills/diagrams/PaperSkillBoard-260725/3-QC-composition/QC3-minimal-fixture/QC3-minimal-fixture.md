# QC3 · Specify the minimal fixture that can test the Page graph

state: ✅ SETTLED · spec at the seven-type graph · open: establish-loop fixture material
owner: JL
method: define the smallest observable graph for downstream integration and fresh-agent tests

## Opening
What is the smallest realistic paper graph that can expose a missing ownership boundary or broken handoff?
The fixture covers every live Page Type once and both Probe lanes.
One page of each of the seven types, one released block with one lap, two Sections, and one status rollup are enough.
The two lanes stay observable as a PageX read and a Task/Discovery QA question.

The full inventory: one Ideation, one Seed, one Roadmap with one released block and one lap, one Venue read from the bank, one Narrative, two Sections, one Round, one `/haipipe-paper status` rollup.
The on-disk `_fixture/` still holds the earlier five-type material.
The establish-loop edges (G0, G2, G3, G4) are specified here but their fixture material is not yet built.

**Where this page sits**: QC4 asks a fresh agent to run the architecture against this shape.

**Why it matters**: static consistency cannot prove that a new agent will find the intended route and stop correctly.

## Writing Style
Record observable inputs, outputs, versions, and stop gates.
Do not count a plausible artifact as proof that the route was followed.

## Diagram
**Minimal validation fixture**: every active type and evidence route appears once.

```text
Probe: PageX source + QA source
          │
Ideation ─▶ Seed ⇄ Roadmap (1 block · 1 lap)
              │ G4
Venue (bank) ─▶ Narrative ─┬─▶ Section A
                           └─▶ Section B
                                  │
                          assemble + Round
                                  │
                          /haipipe-paper status
```

## Content
### 1 · Minimal fixture
**Observable receipt**: each edge names the source version, target version, and acceptance or open state.

```text
7 Page Types · 2 evidence routes · 1 establish loop (block + lap + settle)
2 Section handoffs · 1 assembly · 1 routed revision · 1 status rollup
```

This Page specifies the validation scenario and receipt fields; it does not claim that the whole seven-type integration run has executed.
QC4 records the fresh-agent route test.
A downstream integration run passes only when edits land on owning Pages and the rebuilt artifact contains the checked versions.

## Aims
### A1 · 🧪 Minimal fixture
- A1.1 · One bounded fixture specifies every live Paper Page Type and critical handoff.
  **Done when:** the inputs, expected edges, receipts, and stop gates are explicit enough for a clean-context run.

## States
### A1 · 🧪 Minimal fixture
- ✅ A1.1 · The test shape, evidence lanes, handoffs, and expected receipt are explicit.

## Files
- `_fixture/` · Board-local validation material (260820 five-type era)
- `3-QC-composition/QC4-fresh-agent-run/QC4-fresh-agent-run.md` · behavioral test

## Log
260820 · Separated the current Page-graph test specification from the frozen legacy resolver fixture.
260820 · Moved from QF1 to QC3 so validation closes the composition topic it tests.
260820 · Dash dropped from the fixture's Page Type count (six → five); the status rollup stays as a non-Page edge in the diagram.
260828 · Spec raised to the seven-type journey graph (Ideation, establish loop, bank Venue, assemble verb); the on-disk `_fixture/` material still covers the five-type era, and building the loop's fixture edges is the registered open obligation. Repaired the `4-QC-composition/` path left dead by the 260820 regroup.
