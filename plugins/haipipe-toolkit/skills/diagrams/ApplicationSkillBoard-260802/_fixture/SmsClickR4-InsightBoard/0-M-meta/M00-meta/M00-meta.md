# What the refill-reminder data holds, before anything is asked of it

state: 🟡 PARTIAL · inventory complete · Roster has one open need
page-type: meta
owner: JL

## Opening

What data does this board actually read, at what grain, and how stale is it?

Three synthetic sources: a send log, a click log, and a patient dimension. One row means one invitation in the first two and one person in the third, so any per-person rate needs a join this page names rather than assumes. Everything here describes. Nothing here concludes, and no question originates on this page.

### Writing Style

Every row names its source and its as-of date. A sentence that compares two numbers has left this page and belongs in an Insight Page.

## Diagram

**Source map**: what joins to what, and on which key.

```text
📤 sms_send_log ──── invitation_id ────▶ 📥 sms_click_log
      │                                        (0 or 1 row per invitation)
      │ patient_id
      ▼
👤 patient_dim   one row per person
```

## Content

### 1 · Purpose and Scope

**Reading order**: what this page fixes, in the order a later page needs it.

```text
2 sources ─▶ 3 grain ─▶ 4 population ─▶ 5 freshness ─▶ 6 limits ─▶ 7 roster
   what        one row      who is in       how old       what is      who took
   exists      is what      and out         it is         unknown      each need
```

This board serves the YoungMaleRefill DesignBoard. The data on hand describes who received a refill reminder and who acted on it. It does not describe whether the refill happened, so any outcome beyond the click is out of scope for every page here.

#### 2 · Source Inventory

**Sources**: owner, run identity, and dated extract for each.

```text
source          owner   run identity              extract     rows
──────────────────────────────────────────────────────────────────────
sms_send_log    DataEng run_sms_send_2608a        260803      41,000
sms_click_log   DataEng run_sms_click_2608a       260803       2,300
patient_dim     DataEng run_patient_dim_2607c     260728      28,400
```

All three are fixture values and describe no real cohort.

#### 3 · Unit and Grain

One row is one invitation in `sms_send_log` and one click event in `sms_click_log`, joined on `invitation_id`. One row is one person in `patient_dim`, joined on `patient_id`. Sends outnumber people, so a person may appear several times and a per-person rate is not a per-invitation rate. Reading one as the other is the grain error this division exists to prevent.

#### 4 · Population and Time Window

Adults enrolled in the reminder program. Excluded: test accounts, records with a null `patient_id`, and anyone who opted out before the window opened, all excluded at extract time rather than in analysis. `sms_send_log` and `sms_click_log` cover the full eleven-month window. `patient_dim` is a snapshot, not a history, so anyone who changed cohort inside the window reads at their current value only.

#### 5 · Freshness and Staleness

**As-of dates**: when each source last landed, and what a refresh reopens.

```text
source          as-of    reopens on refresh
────────────────────────────────────────────────────────────
sms_send_log    260803   every D row citing a send count
sms_click_log   260803   every D row citing a click or rate
patient_dim     260728   every D row segmented by cohort
```

`patient_dim` is six days behind the other two. Any page joining across that gap says so in its own Source Map.

#### 6 · Known Limits

Click is the only observed response, so no page here can reach refill behavior. A click is device-attributed and not person-attributed, so a forwarded message reads as the original recipient. The snapshot in `patient_dim` erases cohort changes inside the window. Nothing is known about send-time variation, because the send hour is not recorded in this extract.

#### 7 · Insight Roster

**Roster**: one row per raised need, and which page took it.

```text
need  question, one line          target  Insight Page      state
─────────────────────────────────────────────────────────────────────────
N1    who clicks?                 K       I01-who-clicks    ✅ handoff v2
N2    does send timing matter?    K       ─                 ⬜ no page yet
```

N2 has no page and cannot get one from this data: division 6 records that send hour is absent from the extract. The row stays visible so the gap is not rediscovered.

## Aims

### A1 · Purpose and Scope
- ✅ A1.1 · Every source names an owner, a run identity, and a dated extract.
  **Done when:** no row in division 2 is missing one of the three.
  **Now:** Three sources, each with owner, run, and extract date.


#### P · Grain
- ✅ P1 · A reader cannot confuse a per-invitation rate with a per-person rate.
  **Done when:** division 3 states the join and the multiplicity.
  **Now:** The join and the sends-outnumber-people warning are stated.


#### P2 · Insight Roster
- 🧠 P2.1 · Every raised need is visible, answered or not.
  **Done when:** each need has a row and an honest state.
  **Now:** N2 is rostered and open. It is blocked on data that does not exist in this extract, not on effort.


## Discussion

## Files

### 📋 Contracts
- `../../../../../../application/page-types/haipipe-page-for-meta/SKILL.md`
  The Page Type this page instantiates.

### 🔗 Related Board Pages
- `reads · EVIDENCE` · [I01 §1](1-I-insights/I01-who-clicks/I01-who-clicks.md)
  The Source Map that consumes this inventory.

## Law

Meta describes and never concludes. A number here carries its source and its date; a number compared to another number has left this page.

## Log

260820 · Created as the InsightBoard head for the two-board fixture.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0