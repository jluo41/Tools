# Who clicks a refill reminder, and how far that generalizes

state: ✅ SETTLED · handoff v2 · reopens if sms_click_log refreshes
page-type: insight
scope: application
application: fixture-refill-reminder
serves: N1
insight-target: knowledge
owner: JL

## Opening

Which recipients act on a refill reminder, and is the pattern strong enough to design against?

Younger male recipients click less than the rest of the population in this synthetic extract, and the gap is wide enough to survive the obvious rival explanations. It is not wide enough to explain why. This page settles the what, states the boundary the DesignBoard inherits, and refuses the causal reading that the data cannot carry.

### Writing Style

Never let a sentence cross a level. A rate belongs to Data, a contrast belongs to Information, a proposition with a strength belongs to Knowledge, and only Wisdom may mention an audience.

## Diagram

**The chain**: each level names its parent, so a reader can walk back from the handoff to a run.

```text
run_sms_click_2608a
        │
        ▼
D1 D2 D3 ──▶ I1 I2 ──▶ K1 (moderate) ──▶ W1 W2 ──▶ H1 Design Handoff
                        K2 (weak)                    boundary travels with it
```

## Content

### 1 · Application Need

**What this page owes**: one need in, one bounded handoff out.

```text
N1 raised on A00-brief ─▶ this page ─▶ H1 @v2 ─▶ D01 borrows it by path
```

The YoungMaleRefill DesignBoard cannot choose a message register without knowing whether its audience behaves differently from everyone else. Raised as N1 on the Brief. This page states no preferred answer: a null result would have been equally usable and would have released the same Aim.

#### 2 · Question and Scope

Among adults who received a refill reminder inside the covered window, does click rate differ by age band and sex? Unit is the invitation, not the person, per `M00-meta §3`. Excludes test accounts and pre-window opt-outs. Send timing is out of scope because the extract does not record it.

#### 3 · Source Map

`sms_send_log` and `sms_click_log` at `run_sms_click_2608a`, joined on `invitation_id`, then to `patient_dim` at `run_patient_dim_2607c`. The extract-date gap between the behavioral logs and the patient snapshot is inherited from `M00-meta §5` and is the reason K2 below is weak.

#### 4 · Data

**Observations**: fixture values, each carrying its run.

```text
id   observation                                          source
──────────────────────────────────────────────────────────────────────────
D1   41,000 invitations, 2,300 clicks overall             run_sms_click_2608a
D2   male 18-34: 9,100 invitations, 290 clicks            run_sms_click_2608a
D3   all others: 31,900 invitations, 2,010 clicks         run_sms_click_2608a
```

No rate is computed here and no comparison is drawn here.

#### 5 · Information

I1, from D1 D2 D3: the overall click rate is 5.6 percent; male 18-34 is 3.2 percent and everyone else is 6.3 percent, a gap of 3.1 points. I2, from D2 D3: the gap holds in every month of the window, with the monthly difference never falling below 2.4 points, so it is not one bad month.

#### 6 · Knowledge

K1, from I1 I2, strength MODERATE: younger male recipients click refill reminders at roughly half the rate of other recipients, and the pattern is stable across the window. Rivals considered and not eliminated: differential phone ownership, differential opt-out before the window, and the device attribution limit in `M00-meta §6`. Boundary: invitation-level, click-only, this program, this window.

K2, from I1, strength WEAK: the gap may narrow above age 34 rather than being male-specific, because the snapshot in `patient_dim` cannot place a person in the right band if they changed inside the window. Stated as weak on purpose; a Design Page may not lean on it.

#### 7 · Application Wisdom

W1, parent K1: the audience this board designs for is measurably less responsive, so a design that assumes population-average engagement will underperform for it. Plan for a lower ceiling rather than a different one.

W2, parent K1: the data says who, never why. Any message written as though the cause were known, for example one that implies forgetfulness or indifference, asserts something no row here supports and risks reading as blame.

#### 8 · Design Handoff

**H1**, version 2, releases N1.

```text
finding        male 18-34 click refill reminders at about half the rate of others
strength       MODERATE · stable across the window · rivals not eliminated
boundary       invitation-level · click-only · this program · the covered window
sources        run_sms_click_2608a · run_patient_dim_2607c · see M00 §5
consequence    design for a lower engagement ceiling for this audience
forbidden      do not assert a CAUSE · no message may imply forgetfulness,
               indifference, or any other motive · K2 is weak, do not lean on it
gaps           no refill outcome · no send-timing data · device-attributed clicks
staleness      reopens if sms_click_log or patient_dim refreshes
```

No message copy appears here. That is the Design Page's job.

## Aims

### A1 · Application Need
- A1.1 · No level cites a later level as evidence.
  **Done when:** every I, K, W and H row names its parent and no D row interprets.

#### P · Knowledge
- P1 · Rivals, weak propositions, and gaps stay visible.
  **Done when:** K carries its rivals and the handoff carries a forbidden clause.

#### P2 · Design Handoff
- P2.1 · A Design agent can use H1 without opening a source.
  **Done when:** finding, strength, boundary, consequence, and forbidden all read standalone.

## States

### A1 · Application Need
- ✅ A1.1 · D holds counts only; I derives the rates; K carries strength and rivals.

#### P · Knowledge
- ✅ P1 · K2 is marked WEAK and the handoff forbids leaning on it.

#### P2 · Design Handoff
- ✅ P2.1 · D01 §2 borrows H1 by path and cites no source of its own.

## Files

### 📋 Contracts
- `../../../../../../task/page-types/haipipe-page-for-insight/SKILL.md`
  The Page Type, `scope: application` column.

### 🔗 Related Board Pages
- `reads · EVIDENCE` · [M00 §1](0-M-meta/M00-meta/M00-meta.md)
  The freshness rows this page's Source Map inherits.

## Law

D, I and K are evidence-led and W may be contextual. The handoff may be narrower than W and never broader than K supports.

## Log

260820 · Settled at handoff v2 after the monthly stability check moved K1 from weak to moderate.
