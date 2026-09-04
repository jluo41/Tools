# The refill sequence for male patients aged 18 to 34

state: 🟡 PARTIAL · R1 and R2 accepted · R3 open
page-type: design
owner: JL

## Opening

What does this audience receive, in what order, and who has signed off on each piece?

Three SMS messages over eight days, written for a segment the evidence says is measurably less responsive. Each message is a division carrying its own acceptance row, so R1 and R2 can be signed while R3 is still being written. Every substantive move traces back to one borrowed handoff, and the boundary on that handoff is what forbids the register most people reach for first.

### Writing Style

Write each move as because-do-within. A sentence naming a design choice without naming the handoff it rests on has no evidence behind it.

## Diagram

**The sequence**: three units, their triggers, and their acceptance state.

```text
day 0 ──────── day 3 ──────── day 8
  │              │              │
  ▼              ▼              ▼
 R1 opener      R2 nudge       R3 last call
 ✅ accepted    ✅ accepted    🔨 unaccepted
 both cite H1@v2               same handoff, not yet written
```

## Content

### 1 · Design contract

**One page, one grain**: audience, job and venue are fixed before any message.

```text
male 18-34  ×  refill on time  ×  SMS   ─▶  R1 · R2 · R3
```

Audience: male patients aged 18 to 34 in the reminder program. Behavior job: open the refill flow before the prescription lapses. Context: an unprompted SMS to a phone, read in seconds. Primary venue: SMS. Success condition: click-rate movement for this audience that holds across a full window, with no opt-out increase anywhere.

#### 2 · Insight Use Map

**Borrowed handoffs**: what each permits, and the boundary that came with it.

```text
Aim   handoff                     state     use                     boundary
──────────────────────────────────────────────────────────────────────────────
A2.1  I01 H1 @v2  (PageX)         adopted   design for a lower      no causal
                                            engagement ceiling      claim, ever
A2.2  I01 K2                      declined  age-band shape is       marked WEAK
                                            weak; not leaned on     on the source
```

Bound by path to `../../../SmsClickR4-InsightBoard/1-I-insights/I01-who-clicks/I01-who-clicks.md#8`, which is a relative hop across boards. No Task source is opened from this page and no probe card exists here.

#### 3 · Design principles

Because H1 says engagement is roughly half the population average, do plan a three-message sequence rather than a single send, within a cap of three so the sequence does not read as pressure. Because H1 forbids a causal claim, do write every message as an offer of a next step, within a rule that no message names a reason the recipient did not act. Because the venue is SMS read in seconds, do put the action in the first clause, within one screen of text.

#### 4 · Message map

**Units**: ordered by trigger, each with its job and what may vary.

```text
unit  trigger    job                  invariant              may vary
──────────────────────────────────────────────────────────────────────────
R1    day 0      make the action      the refill link        greeting form
                 visible
R2    day 3      lower the cost       the refill link        framing of effort
                 of acting
R3    day 8      final availability   the refill link        not yet decided
```

#### 5 · R1 · opener

Unit id R1. Recipient moment: the day the reminder window opens. Audience job: make the action visible in the first clause. Handoff refs: H1@v2. Design move: lead with the link and what it does, no preamble. Content: a one-line statement that the refill is ready, followed by the link. Variants: none declared. Safety rail: no motive language, per the H1 forbidden clause. Next trigger: R2 at day 3 if no click.

```text
accepted: JL · handoff I01@v2 · render v2
```

#### 6 · R2 · nudge

Unit id R2. Recipient moment: three days on, no click. Audience job: lower the perceived cost of acting. Handoff refs: H1@v2. Design move: name how short the task is, without referring to the earlier message going unanswered. Content: a one-line statement of the time it takes, followed by the link. Variants: two framings of effort, reviewed together under one invariant link. Safety rail: no reference to the recipient having ignored R1, which would assert a motive. Next trigger: R3 at day 8 if no click.

```text
accepted: JL · handoff I01@v2 · render v2
```

#### 7 · R3 · last call

Unit id R3. Recipient moment: day 8, window closing. Audience job: state that availability ends, factually. Handoff refs: H1@v2. Design move: not yet written. Content: open. Variants: not yet declared. Safety rail: urgency may describe the window and may not describe the recipient. Next trigger: none, sequence ends.

No acceptance row. That absence is the only way this page says R3 is unaccepted, and it is deliberate: R1 and R2 are signed and shippable while this division is still open.

#### 8 · Cross-unit rails

The link is identical in all three messages, so the sequence reads as one thread rather than three campaigns. Escalation is by availability only and never by tone. Prohibited across every unit: any claim about why the recipient did not act, which the H1 boundary forbids and which no row in I01 supports. Uncertainty language: none of the three may promise an outcome, because the evidence reaches the click and stops there.

## Aims

### A1 · Design contract
- ✅ A1.1 · Every load-bearing move reaches a settled handoff.
  **Done when:** the Insight Use Map has no adopted row without a source.
  **Now:** Both principles in division 3 cite H1@v2.
- ✅ A1.2 · Declined insights stay visible with a reason.
  **Done when:** K2 is recorded as declined and why.
  **Now:** K2 is declined in the Use Map with its WEAK marking as the reason.


#### P · Acceptance
- ✅ P1 · A unit can be accepted while a sibling is not.
  **Done when:** at least one division carries a row and one does not, legally.
  **Now:** R1 and R2 carry rows; R3 carries none and is open.


#### P2 · Cross-unit rails
- 🔨 P2.1 · The sequence coheres as one system, not three sends.
  **Done when:** the rails fix the link, the escalation, and the prohibited move.
  **Now:** Rails are written; the system cannot be judged whole until R3 exists.


## Discussion

## Files

### 📋 Contracts
- `../../../../../../application/page-types/haipipe-page-for-design/SKILL.md`
  The Page Type, including the per-division acceptance row.

### 🔗 Related Board Pages
- `reads · DRAFT` · [A00 §1](0-A-brief/A00-brief/A00-brief.md)
  The roster row that released this page.

## Law

Acceptance covers one division. A changed handoff clears only the rows that cite it, and an absent row is how a page says a unit is not accepted.

## Log

260820 · Accepted R1 and R2 against handoff v2; R3 left open on purpose so the fixture exercises mixed acceptance.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0