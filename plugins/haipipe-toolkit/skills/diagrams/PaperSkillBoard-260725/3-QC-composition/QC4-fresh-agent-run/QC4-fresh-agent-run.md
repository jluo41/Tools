# QC4 · Observe whether a fresh agent follows the current Paper architecture

state: 🟡 PARTIAL · five-type route passed · open: journey-era rerun (A1.3)
owner: JL
method: give a clean-context agent one realistic paper task and inspect its route, writes, and stop gates

## Opening
Can an agent with no design-discussion memory discover the thin Paper door and use the correct Pages and plugins?
The test watches behavior rather than grading only the final artifact.
It must show whether the agent avoids retired stages and finds PageX inside Probe.
It must also keep the PageX and QA lanes distinct, follow Narrative handoffs, and stop at human gates.

**Where this page sits**: QC3 defines the minimal graph against which behavior is observed.

**Why it matters**: a correct-looking paper can still be produced by an incorrect and non-repeatable route.

## Writing Style
Report what the agent opened, inferred, changed, checked, and refused to close.
Record divergence before repairing the contracts.

## Diagram
**Fresh-context loop**: behavioral findings reopen the owning contract.

```text
plain request ─▶ fresh agent ─▶ observed route + artifact
                      │
                      └─ divergence ─▶ repair owner ─▶ rerun
```

## Content
### 1 · Fresh-agent behavior
**Pass behaviors**: the agent discovers and follows the Page-first architecture from the public request.

```text
trigger Paper door · select correct type · use current workflow
Probe/PageX existing Pages · Probe/QA Task/Discovery · obey Narrative row
assemble checked versions · stop at human approval
```

The run fails if it revives S01 to S10, invents evidence, copies source material into Paper, or marks a human gate complete.

### 2 · Final receipt

**Validated route, five-type era**: the fresh agent found both Probe lanes and stopped at human gates. This run predates the journey; Ideation, Roadmap, and gates G0–G7 were not part of what it observed.

```text
Paper → Results Section → Probe ┬─ PageX
                                └─ QA Probe → EVIDENCE → human gates
```

The final clean-context run found the public Paper door and selected a Results Section.
It routed accepted Pages through Probe/PageX and sent the Task-only subgroup question through Probe/QA.
It kept `pagex/` and `probe/` distinct and landed A-consumer in `consumer/a-consumer.md`.
It used the marked MISQ Results template and stopped at human gates.
Focused runtime validation passed the marker/fallback guard and every mechanical-repair route.

### 3 · Journey field record

**Live-fire ledger**: which journey gates have ever run, per the family's dated status.

```text
fired live   G0 G2 G3 G4     2 boards · 1 formal field test · 3 gaps patched
never fired  G1 G5 G6 G7     next natural tests: the MS narrative opens G5,
                             the first decision letter opens G7
```

The journey machine has been field-tested on live boards rather than this fixture; its source of record is the family status in `paper/README.md`, a dated receipt and never a second authority.
A journey-era rerun of this fixture is the open obligation this page tracks.

## Aims
### A1 · 🧑‍🔬 Fresh-agent behavior
- A1.1 · A fresh agent executes a realistic current Paper task through the intended route.
  **Done when:** process evidence covers trigger, routing, evidence lanes, handoffs, checks, and stop gates.
- A1.2 · Any divergence is repaired and the test is repeated.
  **Done when:** the final fresh run behaves as designed.
- A1.3 · The journey-era architecture earns the same behavioral proof.
  **Done when:** a fresh-context run traverses the seven-type graph with the establish loop, or the remaining gates fire on live boards and are registered here.

## States
### A1 · 🧑‍🔬 Fresh-agent behavior
- ✅ A1.1 · The final fresh agent followed the Page-first route as of the 260820 five-type graph.
- ✅ A1.2 · Earlier contradictions were repaired and the rerun passed.
- 🔨 A1.3 · The journey machine's gates are live-fired 4/8 on real boards (G0 G2 G3 G4); a journey-era fresh rerun of this fixture has not happened.

## Files
- `3-QC-composition/QC3-minimal-fixture/QC3-minimal-fixture.md` · validation subject
- `../../paper/haipipe-paper/SKILL.md` · expected public entry
- `../../paper/README.md` · the dated family status this page's journey record cites

## Log
260820 · Reset the behavioral test for the Page-first Paper architecture.
260820 · Final fresh-context rerun passed after enforcing the template guard and legal repair routes.
260820 · Moved from QF2 to QC4 so behavioral validation closes the composition topic it tests.
260828 · Scoped the receipt to the five-type graph it actually observed; registered the journey's live-fire record (G0 G2 G3 G4 on two boards; G1 G5 G6 G7 never) from the family status, and opened A1.3 for the journey-era rerun. Repaired the `4-QC-composition/` path left dead by the 260820 regroup.
