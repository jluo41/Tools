# Agreeableness main association

view-id: QZ1-for-view
status: draft · awaiting validation and human acceptance

## QA inputs

- `input/probes/1-canonical-definition.md` (state: answered) — gives the minimal, specimen-scoped description of agreeableness (interpersonal warmth and cooperation) used in the View body below.
- `input/probes/2-observable-signal.md` (state: answered) — gives the observable project signal (review text records patient-facing behavior) and the bound source-Probe count (3) that Display 1 reports.
- `input/sources/references.bib` — one bibliography source (John & Srivastava, 1999) grounding the construct description.

## View body

### Construct description

For this specimen, agreeableness is represented as an interpersonal construct associated with warmth and cooperation \citep{john1999bigfive}.

> Card interpersonal warmth and cooperation: V1 · Value · Binding: `input/probes/1-canonical-definition.md` · State: current.

This description is intentionally narrow and supports only this example View grammar; it is not a complete literature review.

### Observable signal and evidence boundary

Review text directly records patient descriptions and evaluations of patient-facing behavior, so the score is treated as a patient-perceived signal rather than an error-free latent-trait measure.

> Card patient-perceived signal: V2 · Value · Binding: `input/probes/2-observable-signal.md` · State: current.

The current View binds 3 source Probe records into one evidence judgment.

> Card 3 source Probe records: V3 · Value · Binding: `input/probes/2-observable-signal.md` · State: current.

## Displays

QZ1-Display1 renders the four bound facts above as one summary table.

![QZ1-Display1 preview](output/QZ1-Display1-agreeableness-summary-table/preview.png)

> Card QZ1-Display1: Display · table · rendered · Binding: `output/QZ1-Display1-agreeableness-summary-table/output.md` · Uses: V1, V2, V3 · Preview: output/QZ1-Display1-agreeableness-summary-table/preview.png · PDF: output/QZ1-Display1-agreeableness-summary-table/preview.pdf · Acceptance: waiting.

## Consumers

QZ1-Display1 is handed to the **Main Results consumer** for a construct-interpretation placement.

> Card Results consumer: C1 · Consumer · Binding: `../../../../../QS-consumers/S-Main-4-results.md` · Uses: QZ1-Display1 · Placement: Results / construct interpretation · State: planned.

## Validation

- Input freshness: both Probes and the one bibliography source are copied verbatim from their answered originals; no value here was invented.
- Display artifact + acceptance: QZ1-Display1 is `rendered`, has both `preview.png` and `preview.pdf`, and remains `acceptance: waiting`.
- Consumer placement + handoff: C1 names a real target file, states its placement, and stays `planned` until both the View and QZ1-Display1 pass independent human acceptance.
