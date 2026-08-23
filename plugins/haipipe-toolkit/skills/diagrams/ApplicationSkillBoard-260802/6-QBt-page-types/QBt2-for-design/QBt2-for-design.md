# Application Design Page: one audience × job × venue
state: 🟡 PARTIAL · contract 0.3.0 shipped · runtime projection pending
page-type: design
owner: JL

## Opening

What is the main compositional unit of an Application?

One user-facing Design Page serves one audience × behavior job × primary venue.
It consumes the Brief and exact Insight Design Handoffs through PageX, then owns principles, a message/unit map, repeated divisions, variants, rails, and per-division acceptance. The machine key is `design`: JL retired the `intervention` key on 260820 because one concept wearing two words is what made readers ask whether Design and Artifact were the same thing.

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

Acceptance is a row on each `R<n>` division, not on the Page, which is what absorbed the retired `page-type: artifact`. One division may be accepted while a sibling is mid-revision. A changed handoff clears only the dependent divisions' rows.

#### 7 · Where the Page stops

The Page ends at ACCEPTED. Building it, shipping it, running the experiment, and collecting what came back are task-layer work, so no deploy record and no round folder appears here.

## Aims

### A1 · Contract
- A1.1 · One Page contains one coherent audience/job/venue design.
  **Done when:** no division silently serves another decision maker or channel.

#### A2 · Trace
- A2.1 · Every substantive design move reaches an accepted handoff.
  **Done when:** the Insight Use Map has no unsupported adopted row.

#### A3 · Acceptance grain
- A3.1 · One unit can be accepted while a sibling is not, without a second Page.
  **Done when:** acceptance lives on the division and clears per division.

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

#### A3 · Acceptance grain
- ✅ A3.1 · Absorbed the retired artifact type as a per-division `accepted:` row (0.3.0).

## Files

### 📋 Contracts
- `../../../../application/page-types/haipipe-page-for-design/SKILL.md`
- `../../../../application/haipipe-application/fn/design.md`

## Law

Design consumes handoffs and owns composition. It never performs a substitute
Probe or copies raw evidence into its message logic.

## Log

260820 · Recast Intervention as many user-facing Design Pages with repeated message/unit divisions.
260820 · Renamed the key `intervention` → `design`, absorbed the retired `page-type: artifact` as a per-division acceptance row, and cut the Page at ACCEPTED (JL).
