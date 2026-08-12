# Value evidence inside a View: project results become bounded Cards
state: 🟡 PARTIAL
owner: JL
method: compare several project-produced evidence forms and identify only the fields that the shared Evidence Card cannot infer

## Opening
What must a Value Evidence Card show when a View relies on project-produced data, analysis, or measured artifacts?
Value is broad here: it includes estimates, distributions, diagnostics, model outputs, and other results created inside the project.
The Card must expose enough provenance to judge the finding without turning into a duplicate QA answer.
This page decides the Value-specific additions inside the shared View contract after QBt1 is accepted.

**Where this page sits**: QA2 owns the common Card payload, and QBt1 supplies EC3 as the first project-value example.

**Ownership rule**: Value is an internal evidence profile of View, not an independent Page Type, skill door, or workflow line.

## Diagram

**The Value binding**: a project result reaches a View only through a Probe answer and a bounded interpretation.

```text
🧪 Task run ──▶ 🏦 QA-bank ──▶ 🔎 Probe
                                      │
                                      ▼
                          👀 VIEW · Value profile
                          finding · provenance · scope
                                      │
                                      ▼
                        View interpretation + applicable boundaries
```

## Content

### 1 · Value-specific fields
**The proposed additions**: the Card names the producing context needed to interpret a project result.

```text
run          producing task and version
population   sample or corpus
quantity     estimand, metric, or measured object
unit         scale and transformation
specification model or procedure
uncertainty  interval, variation, or diagnostic
stale when   upstream changes that invalidate the Card
```

These fields refine the common kind, finding, bearing, boundary, binding, freshness, and used-by fields in QA2.
A Card may omit a Value-specific field only when the field genuinely does not apply, never because the source failed to report it.

## Aims

### A1 · Value-specific fields
- A1.1 · Define the minimum provenance needed for a project-produced result.
  **Done when:** A cold reader can identify producing run, population, quantity, scale, specification, uncertainty, and staleness trigger.
- A1.2 · Test the fields on more than one Value form.
  **Done when:** An estimate and a non-regression artifact both fit without inventing empty slots.

## States

### A1 · Value-specific fields
- 🔨 A1.1 · QBt1 now resolves its checked value through Probe, QA-bank answer, and run folder; population, specification, uncertainty, and staleness still need a richer empirical specimen.
- ⬜ A1.2 · A second Value form is not yet instantiated.

## Files

- `QBt1-for-view.md`
  The base specimen and its first Value Card.

## Log

- 260810 · [RULING-JL] Kept Value as an internal View evidence profile and removed the need for a separate `for-value` Page Type or workflow line.
- 260810 · [DRAFT-CC] Opened as a profile rather than a Page Type so mixed-evidence Views remain legal.
