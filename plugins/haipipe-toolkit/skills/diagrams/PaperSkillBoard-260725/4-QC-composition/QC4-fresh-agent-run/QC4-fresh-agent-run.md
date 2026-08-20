# QC4 · Observe whether a fresh agent follows the current Paper architecture

state: ✅ SETTLED · final fresh-context route passed
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

**Validated route**: the fresh agent found both Probe lanes and stopped at human gates.

```text
Paper → Results Section → Probe ┬─ PageX
                                └─ QA Probe → EVIDENCE → human gates
```

The final clean-context run found the public Paper door and selected a Results Section.
It routed accepted Pages through Probe/PageX and sent the Task-only subgroup question through Probe/QA.
It kept `pagex/` and `probe/` distinct and landed A-consumer in `consumer/a-consumer.md`.
It used the marked MISQ Results template and stopped at human gates.
Focused runtime validation passed the marker/fallback guard and every mechanical-repair route.

## Aims
### A1 · 🧑‍🔬 Fresh-agent behavior
- A1.1 · A fresh agent executes a realistic current Paper task through the intended route.
  **Done when:** process evidence covers trigger, routing, evidence lanes, handoffs, checks, and stop gates.
- A1.2 · Any divergence is repaired and the test is repeated.
  **Done when:** the final fresh run behaves as designed.

## States
### A1 · 🧑‍🔬 Fresh-agent behavior
- ✅ A1.1 · The final fresh agent followed the current Page-first route.
- ✅ A1.2 · Earlier contradictions were repaired and the rerun passed.

## Files
- `4-QC-composition/QC3-minimal-fixture/QC3-minimal-fixture.md` · validation subject
- `../../paper/haipipe-paper/SKILL.md` · expected public entry

## Log
260820 · Reset the behavioral test for the Page-first Paper architecture.
260820 · Final fresh-context rerun passed after enforcing the template guard and legal repair routes.
260820 · Moved from QF2 to QC4 so behavioral validation closes the composition topic it tests.
