---
page-type: ideation
id: SD00-ideation-cgm-cross-event-normalization
state: 🟡 INTAKE
owner: research team
method: consolidate the existing event-normalization work into a claim-level ICLR feasibility direction
---

# SD00 Ideation: Cross-event normalization for CGM prediction

## Opening

How can heterogeneous self-care events become trustworthy inputs to CGM prediction?
Food logs, exercise records, medication entries, and insulin records use different names, units, quantities, and denominators.
This page records the candidate direction, its decisive feasibility test, and the evidence gaps that must be resolved before a Seed is created.

**Where this page sits**: This is the P0 Ideation page at the head of the paper's venue-free story group.
The next authority page is `SD01-seed`, which is deliberately not created yet.

**Why it matters**: A CGM model can receive an event without receiving a quantity that is comparable across sources.
If the representation hides the quantity basis or its confidence, the model may learn to ignore events that are physiologically informative.

### Writing Style

Use evidence-qualified language.
Treat session-reported numbers as probes until a task-owned receipt records the exact data, split, model, metric, and code version.
Keep the Seed venue-free and move ICLR-specific framing to a later Narrative Page.

## Diagram

**Candidate research loop**: the proposed path from a raw event to the downstream CGM test.

```text
📝 raw event
    │
    ▼
🧭 noun-specific normalizer
    │
    ▼
📦 WHAT · HOW MUCH · BASIS · SOURCE · CONF
    │
    ▼
📏 IDENTITY / QUANTITY evaluation
    │
    ▼
📈 CGM prediction payoff
```

## Content

### 1 · Direction

**Direction shape**: four event families feed one common event packet.

```text
🍽 food  🏃 exercise  💊 medication  💉 insulin
                    │
                    ▼
              📦 common packet
```

The direction is to test whether a common, provenance-aware event representation can make heterogeneous diabetes self-care events usable in CGM prediction.
The four source sessions treated food, exercise, medication, and insulin as separate normalization families while preserving one shared event structure above them.
The current local artifacts already contain contracts, API examples, corpora, and benchmark runs for the four families.

Source intake comes from `Raw-FoodForm` session `beae21bc-6d8b-4b68-a516-34d761f44573` and `CGM-Raw-Page-Workflow` session `19088662-a806-4498-971f-9b5b9d15ab7e`.
No independent IDEA_REPORT, novelty QA, or task-owned pilot receipt exists yet.

### 2 · Ideas (ranked)

**Idea comparison**: one main method direction and one supporting evaluation direction.

```text
🧪 i1 method and payoff  ──▶  📈 CGM prediction
📏 i2 evaluation integrity ──▶  🔍 trustworthy benchmark
```

| id | idea | novelty | pilot | verdict | went to |
|---|---|---|---|---|---|
| i1 | Identity and quantity are separate axes for a common five-slot event contract, and quantity-aware normalization can improve CGM event use. | ⬜ open · claim-level search not run | 🟡 feasibility scan only · decisive pilot absent | ⚠️ PROCEED WITH CAUTION · human requested the ICLR build | none · Seed not minted |
| i2 | A leakage-aware, cross-event benchmark should expose when a lookup table and its gold labels share a source. | ⬜ open · claim-level search not run | 🟡 partial · food gate exists, cross-event gate absent | ⚠️ PROCEED WITH CAUTION · supporting direction | none · Seed not minted |
| i3 | Pitch the project as a larger NutritionBench-style resource benchmark. | LOW · method delta is unclear | none · not retained | 🚫 ABANDON · insufficient ICLR method story | none · no Seed |

Source intake for all three rows is the two named Claude Code sessions and the local DataBoard and EventNorm artifacts.

### 3 · Idea 1: Identity and quantity as separate axes

**Idea 1 shape**: representation, two-axis evaluation, and downstream test.

```text
📦 five slots  ──▶  📏 two axes  ──▶  📈 CGM payoff
```

**Method**:

Run the existing food, exercise, medication, and insulin normalizers through one evaluation protocol.
Expose `MatchedID` and `MatchedName` where the resolver already knows them.
Split each ruler into `IDENTITY` and `QUANTITY` outcomes.
Carry the five slots `WHAT`, `HOW MUCH`, `BASIS`, `SOURCE`, and `CONF` into a downstream CGM event channel.
Rerun the extra-large-meal experiment with quantity, basis, confidence, and coverage made explicit.

**Hypothesis**:

Clinical event normalization needs an explicit distinction between what an event refers to and how much of it occurred, and the distinction will improve the usefulness of event inputs for CGM prediction.

**Minimum experiment**:

Add the resolver identity fields, build the two-axis evaluation table, and rerun the existing extra-large-meal CGM comparison with an unchanged model and a changed event representation.
The run must report the exact cohort, split, model commit, event features, forecast horizon, metric, and uncertainty treatment.

**Expected outcome**:

The positive outcome is a measurable improvement in the event-conditioned CGM forecast on the pre-specified meal subset while the identity and quantity axes remain separately inspectable.
The negative outcome is also informative: if the corrected representation does not improve the forecast, the paper must narrow the mechanism claim and investigate temporal or individual-response bottlenecks.

**Core Claims**:

- C1: A common five-slot contract can describe identity, quantity, basis, source, and confidence across four diabetes self-care event families. Novelty: ⬜ open · closest prior `[UNVERIFIED]`. 📮 Claim-level novelty QA is required.
- C2: Identity and quantity should be evaluated as separate axes rather than collapsed into one normalization score. Novelty: ⬜ open · closest prior `[UNVERIFIED]`. 📮 Claim-level novelty QA is required.
- C3: Making quantity basis and confidence explicit can improve the use of events in CGM prediction. Novelty: ⬜ open · closest prior `[UNVERIFIED]`. 📮 Claim-level novelty QA is required.

**Pilot result**:

SKIPPED for the ideation gate.
The source sessions contain a feasibility scan and a proposed downstream comparison, but no independent task-owned receipt for the minimum experiment.

**Risk**:

The downstream payoff may not move after normalization.
The four event families have unequal gold coverage, and exercise currently has a small ruler.
The WellDoc-derived vocabulary may not be releasable.
Food and insulin contain possible circularity between the evaluation source and the lookup system.
The paper may require a stronger human-labeling story than the current artifacts provide.

**Reviewer's likely objection**:

The five-slot structure may be a descriptive restatement of good engineering rather than a method contribution.
The benchmark may be contaminated by shared lookup sources.
The downstream result may be a data-preprocessing effect or may fail to transfer beyond the selected CGM cohort.

**Recommendation**:

PROCEED WITH CAUTION.
The user has confirmed that this is the ICLR paper to build, but the paper should not advance to a Seed until the claim-level novelty search and decisive downstream pilot produce receipts.

### 4 · Idea 2: Leakage-aware cross-event evaluation

**Idea 2 shape**: source overlap is tested before scores are compared.

```text
📚 gold source  +  🔎 lookup source  ──▶  🚦 leakage gate  ──▶  📊 score
```

**Method**:

Apply the existing food leakage gate to medication and insulin, then compare external and same-source rulers under an explicit positive-control protocol.
Report identity and quantity separately and preserve refusal, coverage, and source metadata.

**Hypothesis**:

A single accuracy number can hide source overlap, so an evaluation protocol needs a contamination gate and an independent-reference status for each ruler.

**Minimum experiment**:

Produce one cross-event leakage table covering the four families, with the lookup source, gold source, overlap test, positive control, and post-gate score recorded for every ruler.

**Expected outcome**:

The evaluation will show which measurements are independent, which are circular, and which can support a public benchmark claim.

**Core Claims**:

- C4: Source overlap can materially inflate apparent normalization performance. Novelty: ⬜ open · closest prior `[UNVERIFIED]`. 📮 Claim-level novelty QA is required.
- C5: A contamination-aware ruler registry is necessary for a cross-event benchmark. Novelty: ⬜ open · closest prior `[UNVERIFIED]`. 📮 Claim-level novelty QA is required.

**Pilot result**:

SKIPPED for the cross-event gate.
The food line contains a positive-control analysis, but the corresponding medication and insulin receipts are not yet registered in this paper project.

**Risk**:

The integrity analysis may be a useful benchmark contribution but may not provide enough constructive method novelty for ICLR.

**Reviewer's likely objection**:

The paper could become a critique of benchmark construction without showing a new representation or a downstream benefit.

**Recommendation**:

PROCEED WITH CAUTION as a supporting direction under Idea 1.

### 5 · Eliminated Ideas

**Eliminated idea shape**: a resource-size claim without a method delta.

```text
📚 more data alone  ──▶  ❓ unclear method contribution
```

| idea | reason eliminated |
|---|---|
| Larger NutritionBench-style resource benchmark | The project currently lacks the complete LLM baseline matrix and the larger-resource framing does not by itself provide the desired method contribution. |

### 6 · Suggested Execution Order

**Execution shape**: repair identity, run payoff, then close the evidence gaps.

```text
🔧 resolver  ──▶  🧪 payoff  ──▶  🔍 novelty  ──▶  🌱 Seed decision
```

1. Create the food resolver identity fields and verify that the matched identifier is the actual lookup result, not an input echo.
2. Create the minimum downstream task for the extra-large-meal CGM payoff experiment.
3. Build the cross-event `IDENTITY` / `QUANTITY` table and migrate the leakage gate to medication and insulin.
4. Run the independent novelty search for C1 through C5, one claim per QA question.
5. Run LLM baselines on the public rulers only after the evaluation protocol and contamination status are fixed.
6. Decide whether the evidence licenses `SD01-seed` and, later, an ICLR Narrative.

## Aims

### A1 · 🧭 Direction

- A1.1 · Make the decisive pilot executable.
  Done when: a task-owned QA receipt records matched identity fields and the extra-large-meal rerun inputs and outputs.
- A1.2 · Preserve the five-slot representation while testing the downstream payoff.
  Done when: quantity, basis, confidence, and coverage are explicit model inputs and the exact run is reproducible.

### A2 · 🔥 Ideas (ranked)

- A2.1 · Establish claim-level novelty for the identity/quantity and leakage directions.
  Done when: C1 through C5 each have a discovery QA path or an explicit `[UNVERIFIED]` limitation.

### A3 · 🧪 Idea 1: Identity and quantity as separate axes

- A3.1 · Keep session-reported probes separate from established paper claims.
  Done when: every number that enters a Seed or Narrative resolves to a local task or discovery receipt.

## States

### S · 🧭 Current state

- 🟡 A1.1 · matched identity fields are not yet exposed in a task-owned receipt.
- 🟡 A1.2 · the extra-large-meal payoff rerun is not yet recorded.
- 🟡 A2.1 · claim-level novelty searches are not yet registered.
- 🟡 A3.1 · session-reported probes remain outside established paper claims.
- Journey position: P0 Ideation.
- Human scope decision: the current user request confirms that this is the ICLR paper to build.
- Scientific verdict: open; the decisive downstream pilot has not been run in this paper project.
- Novelty verdict: open; claim-level searches have not been registered.
- Seed: not minted.

### Decision Now

- [ ] 🗣 After the novelty and pilot receipts land, decide whether to mint `SD01-seed`.
  A · Mint a provisional Seed if the identity/quantity direction has a defensible novelty delta and a bounded pilot.
  B · Keep the project in Ideation if the downstream result or novelty evidence does not support the method claim.
  → Recommendation: wait for the two receipts, then choose explicitly.

## Files

- `README.md` - project intake and source summary.
- `../../board.md` - paper board and current journey state.
- `_WorkSpace/0-RawDataStore/0-EventNorm/` - local event-normalization contracts, examples, corpora, and benchmark runs.
- `examples/ProjA-CGM-Raw2AIData/diagram/01-DataBoard-260818/` - local DataBoard and analysis pages.
- Remote source: `/home/jluo41/.claude/projects/-home-jluo41-WellDoc-SPACE/beae21bc-6d8b-4b68-a516-34d761f44573.jsonl`.
- Remote source: `/home/jluo41/.claude/projects/-home-jluo41-WellDoc-SPACE/19088662-a806-4498-971f-9b5b9d15ab7e.jsonl`.
- Future executor, not yet created: `examples/ProjC-Model-LHM/tasks/B93_event_arch/`.

No `pagex/`, `probe/`, `bibex/`, or `display/` folder is created yet.
The source sessions are intake material, not accepted Page evidence.

## Log

- 2026-08-23 - `Raw-FoodForm` session asked whether the research paper was doable and developed the identity/quantity story for ICLR.
- 2026-08-23 - The same session mapped the common five-slot output and proposed the downstream CGM payoff test.
- 2026-08-24 - The user confirmed that this is the ICLR paper to build.
- 2026-08-24 - This P0 Ideation page was created under the current `haipipe-paper` scaffold.
