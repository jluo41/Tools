# Application Design Page: one audience × job × venue
state: 🟡 PARTIAL · contract 0.2.0 shipped · runtime projection pending
page-type: intervention
owner: JL

## Opening

What is the main compositional unit of an Application?

One user-facing Design Page serves one audience × behavior job × primary venue.
It consumes the Brief and exact Insight Design Handoffs through PageX, then owns principles, a message/unit map, repeated divisions, variants, rails, and visible projections. The machine key remains `intervention` for global uniqueness.

### Writing Style

Explain what each message or component does for the audience. Tie every substantive move to a handoff row and inherited boundary.

## Diagram

```text
Brief + Insight Design Handoffs
              │ PageX
              ▼
🎨 Design contract
   ├── principles
   ├── message/unit map
   ├── R1 message division
   ├── R2 message division
   └── Rn ... + variants + rails
              │
              ▼
visible SMS / email / dashboard / checklist / report projection
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

Pins audience, behavior job, primary venue, success/kill criteria, and Brief version.

#### 2 · Insight Use Map

Records Design Aim, Insight Page, exact handoff row, adopted/declined state, allowed use, and inherited boundary.

#### 3 · Principles and architecture

Turns accepted K/W into executable design moves and an organizing sequence or interaction architecture.

#### 4 · Message/unit map

Lists repeated units by job, content move, handoff refs, venue constraints, variant status, rails, and acceptance.

#### 5 · Repeated divisions

Each `R<n>` division contains the concrete unit, why it exists, what it may say, what it must not imply, variants, and projection state.

#### 6 · Acceptance and reopen

The Page closes when its required projections pass the venue and audience criteria. A changed handoff reopens only dependent divisions.

## Aims

### A1 · Contract
- A1.1 · One Page contains one coherent audience/job/venue design.
  **Done when:** no division silently serves another decision maker or channel.

#### A2 · Trace
- A2.1 · Every substantive design move reaches an accepted handoff.
  **Done when:** the Insight Use Map has no unsupported adopted row.

### P · Projection
- P1 · One runtime Design Page produces an accepted visible projection.
  **Done when:** output and trace pass CHECK.

## States

### A1 · Contract
- ✅ A1.1 · Fixed by Design Page Type 0.2.0.

#### A2 · Trace
- ✅ A2.1 · Fixed by the Insight Use Map contract.

### P · Projection
- ⬜ P1 · Runtime projection remains open.

## Files

### 📋 Contracts
- `../../../../application/page-types/haipipe-page-for-intervention/SKILL.md`
- `../../../../application/haipipe-application/fn/intervention.md`

## Law

Design consumes handoffs and owns composition. It never performs a substitute
Probe or copies raw evidence into its message logic.

## Log

260820 · Recast Intervention as many user-facing Design Pages with repeated message/unit divisions.
