# The refill nudge for younger male patients: what this board is building

state: ✅ SETTLED · audience, outcome and venue fixed · N2 still open
page-type: brief
owner: JL

## Opening

What is this board building, for whom, and what must be understood before it can be designed?

A short SMS sequence that moves younger male patients to refill on time. The audience is chosen because it is the least responsive segment, not the largest. This page fixes the audience, the outcome, the kill criteria, and the channel, then raises the two things design cannot proceed without. It answers neither of them.

### Writing Style

State what is fixed and what is open, and never let a raised need carry a hoped-for answer. A need written as a hypothesis has already decided.

## Diagram

**What this board authorizes**: two needs raised, one Design Page released.

```text
📌 A00-brief
   ├── N1 who clicks?            ──▶ ✅ answered · SmsClickR4 I01 handoff v2
   ├── N2 does timing matter?    ──▶ ⬜ open · no data in the extract
   └── roster: D01 young male × refill on time × SMS
```

## Content

### 1 · Opportunity

**Fixed against raised**: which rows this page settles, and which it only opens.

```text
FIXED here          2 audience · 3 outcome · 4 venue · 5 promise · 8 roster
RAISED here         6 needs · answered on the InsightBoard, never on this page
```

Refill reminders already reach every enrolled patient, so the channel costs nothing new. One segment responds at roughly half the rate of the rest, which means the same send is buying less for those recipients than for anyone else. Closing part of that gap needs a design change, not a delivery change.

#### 2 · Audience Set and Behavior

Male patients aged 18 to 34 enrolled in the reminder program. Current action: they receive the reminder and mostly do not click. Desired change: they open the refill flow before the prescription lapses. This board does not design for the other segments, which are covered adequately by the existing generic message.

#### 3 · Outcome and Kill Criteria

Success is a click-rate improvement for this audience that holds across a full window. Guardrail: no increase in opt-outs for any segment. Kill: if two consecutive windows show no movement, the message register is not the lever and this board closes rather than iterating on wording.

#### 4 · Venue Scope

SMS only. Email and push are out of scope for this board because the program has no verified addresses for most of this audience.

#### 5 · Promise

A short sequence that reads as useful rather than corrective. The ceiling is modest and named on purpose: the evidence supports designing for lower engagement, not for parity with other segments.

#### 6 · Insight Needs Raised

**Needs**: each with a target level and the Aim it blocks.

```text
id  question                    target  blocks   state
──────────────────────────────────────────────────────────────
N1  who clicks?                 K       A6.1     ✅ answered
N2  does send timing matter?    K       A6.2     ⬜ open
```

N1 carries no preferred result: a null would have released A6.1 just as well. N2 is open and, per `M00-meta §6`, unanswerable from the current extract, so A6.2 stays held rather than being designed around.

#### 7 · Core PageX Inputs

None yet. No accepted Page applies across this whole board; the one binding that exists is Design-specific and lives on D01.

#### 8 · Design Roster and Handoff

**Roster**: one row per audience, behavior job, and primary venue.

```text
page  audience         behavior job        venue   state
─────────────────────────────────────────────────────────────
D01   male 18-34       refill on time      SMS     🔨 in design
```

One row only. A second audience would be a second Design Page, not a second division on D01.

## Aims

### A1 · Opportunity
- A1.1 · Audience, outcome, kill criteria and venue are all observable.
  **Done when:** each has a division and none is stated as an intention.

#### P · Insight Needs Raised
- P1 · The responsiveness premise is settled before design leans on it.
  **Done when:** N1 has a settled handoff.
- P2 · The timing premise is settled or explicitly held.
  **Done when:** N2 is answered, or recorded as unanswerable with a reason.

## States

### A1 · Opportunity
- ✅ A1.1 · Divisions 2 through 4 fix all four.

#### P · Insight Needs Raised
- ✅ P1 · Met by `SmsClickR4-InsightBoard` I01 handoff v2.
- ❄️ P2 · Held on purpose. The send hour is absent from the extract, so this is blocked on data collection, not on analysis.

## Files

### 📋 Contracts
- `../../../../../../application/page-types/haipipe-page-for-brief/SKILL.md`
  The Page Type this page instantiates.

### 🔗 Related Board Pages
- `reads · DRAFT` · [D01 §1](1-D-design/D01-young-male-refill/D01-young-male-refill.md)
  The Design contract this Brief releases.

## Law

A Brief raises needs and never answers them. A need written with its answer implied is a decision wearing a question mark.

## Log

260820 · Fixed the audience and venue, raised N1 and N2, released D01.
