# Three Display groups: specimen-first plan

status: PROPOSAL ONLY
scope: Value Display · Literature Display · Paper Display
rule: do not revise the live contracts until the three specimens are accepted

## 1 · The design question

The three groups are not three mutually exclusive kinds of picture.
Value and Literature classify a display by where its evidence came from.
Paper classifies a selected display by where it is going.
Treating all three as peer folders creates the duplicate-table problem.

```text
                              origin                              destination
                  ┌──────────────────────────┐              ┌──────────────────┐
task / analysis ─▶│ Value Display            │──┐           │                  │
published record ▶│ Literature Display       │──┼─ Narrative ─▶ Paper Display │──▶ Main / Appendix
                  └──────────────────────────┘  │  selects   │ wrapper          │
                                               └─ parks     └──────────────────┘
```

The proposed interpretation is therefore:

| Group | The decision it makes | What it owns | What it must not own |
|---|---|---|---|
| Value Display | Can we see and interrogate a result this project produced? | working visual, value binding, provenance, limits | final paper number, final caption, placement |
| Literature Display | Can we see and interrogate the shape of published knowledge? | matrix/map, citation bindings, search scope, positioning limit | unsupported novelty verdict, final placement |
| Paper Display | Must the target reader see this display to accept a named claim? | adoption mode, claim job, caption, acceptance, placement | a second copy of the source data or visual |

## 2 · Stable identity and the no-duplication rule

Every display receives one stable id when it first becomes inspectable.
Paper selection does not automatically create a second visual.

```text
direct-adopt   DV-01 ───────────────▶ DP-01 wrapper adopts DV-01 unchanged
transform      DL-02 ──reason───────▶ DP-02 derives a new reader-facing visual
no-paper-use   DV-03 ───────────────▶ parked; remains useful for analysis
```

`direct-adopt` is preferred when the existing visual already has one takeaway, readable labels,
and a defensible evidence binding.
`transform` is required when the paper needs consolidation, a different comparison, redaction,
or a reader-facing form that changes what is shown.
The transformed unit must declare `derived_from` and why direct adoption failed.

## 3 · Four independent state lanes

A single state word cannot describe evidence, visual quality, narrative selection, and paper
placement at once.
The specimen uses four independent lanes:

| Lane | States |
|---|---|
| evidence | open · bound/supported · weakened · withdrawn |
| visual | sketch · inspectable · candidate · superseded |
| narrative | unassigned · claim-linked · selected · parked |
| paper | not-requested · requested · rendered · accepted · placed |

A regression table may therefore be `evidence: bound`, `visual: candidate`,
`narrative: unassigned`, and `paper: not-requested` at the same time.

## 4 · Shared specimen anatomy

The three pages share only identity and traceability.
Their Content differs because each one makes a different decision.

```text
Value Display       Question → Visual → Reading → Provenance → Paper eligibility
Literature Display  Stake → Visual → Coverage → Citation binding → Paper eligibility
Paper Display       Claim job → Adoption → Reader render → Caption → Acceptance → Placement
```

The visual appears once.
A Paper Display wrapper points to the adopted asset when `adoption: direct`.
It contains a new visual only when `adoption: transform`, and then records the derivation.

## 5 · Specimen set

- `01-value-display.md` shows a regression table that is paper-eligible by direct adoption.
- `02-literature-display.md` shows a positioning matrix that is useful but needs transformation
  before a target reader should see it.
- `03-paper-display.md` shows the formal wrapper that adopts the Value table without copying it.

All values and study labels are illustrative.
The specimens test structure, not a substantive result.

## 6 · Implementation sequence after the specimens are accepted

### Phase A · Rule the model

1. Confirm that Value/Literature are origin workspaces and Paper is a destination wrapper.
2. Confirm the two promotion modes: `direct-adopt` and `transform`.
3. Confirm that one probe may truthfully end with `not-displayable`.

### Phase B · Revise the contracts

1. Replace the one-dimensional companion `state` with the four state lanes.
2. Give Value and Literature distinct display anatomies rather than one generic card.
3. Make Paper Display require `adopts` or `derived_from` for promoted material.
4. Keep direct-born Paper displays legal for conceptual frameworks, workflows, and editorial
   diagrams that have no single Value or Literature parent.

### Phase C · Revise the checker

1. Verify every candidate has an evidence parent.
2. Verify every direct Paper adoption resolves to exactly one candidate and copies no source data.
3. Verify every transformation names its parent and reason.
4. Verify every accepted Paper display has a human acceptance record and every placed display has
   a citing sentence.

### Phase D · Pilot on real work

Use three units from one paper:

1. one regression table suitable for direct adoption;
2. one robustness or heterogeneity display that belongs in the Appendix;
3. one literature matrix that remains internal or is transformed into a conceptual figure.

The pilot passes when all three can be found, compared, selected, and placed without retyping a
number or maintaining two independent visual authorities.

### Phase E · Forward test

Ask a fresh agent to classify and route unseen Value, Literature, and Paper display requests.
Revise the contracts if the agent duplicates an artifact, assigns a final caption too early, or
cannot explain why a display is direct-adopted, transformed, or parked.

## 7 · Decisions the specimens put in front of the owner

1. Is Paper Display a thin wrapper over selected displays, as proposed, or a separate artifact
   store that copies selected visuals?
2. Must every completed probe create a candidate record, including `not-displayable`, or only
   probes whose answers have visual potential?
3. Should ids preserve origin (`DV`, `DL`, `DP`) or use one global sequence (`D-01`, `D-02`)?

Recommendation: thin Paper wrapper, explicit record for every completed probe, and origin-preserving
ids during the pilot.
