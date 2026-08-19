# The receipts: how the loop is actually run, and how it resumes
state: 🟡 PARTIAL · the contract is written · open: nothing writes a receipt today
owner: CC
method: Borrow the page workflow's proven receipt model, then change the one thing labeling does differently: its expensive phase is a person sitting for hours and can be interrupted mid-phase.

## Opening
How is this loop actually RUN, and what happens when a person walks away in the middle of phase 4?
Eleven phases and their exit tests describe what should happen; nothing on this Board says who drives them, what is written down as they go, or how a half-finished job is picked back up.
This page fixes the four words a run is described in, the receipt those words live in, and the one place labeling's receipt must be finer-grained than the page workflow's.

**Where this page sits**: `QLw00` holds the sequence and `QLw1` to `QLw11` hold the phases.
This page holds the RUNNING of them, which is a different question from what any phase does.
A letter rather than a digit means this page is not a phase.

**Why it matters**: `skills/page-workflows/label-round/SKILL.md` already promises "Resume the recorded open phase when one exists", and no record exists for it to read.

**What is settled here**: The four words, the receipt fields, the per-item rule inside phase 4, the resume rule, and the auditor that rehashes.

**What remains open**: Nothing writes a receipt. `label-round` runs A to F and leaves closed artifacts only, which say what succeeded and never what was attempted.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**RUN is not ADVANCE.** A run may repeat a phase, go back, or stop without closing, so never write a sentence that assumes the next phase is the next number.

**Attempted, not completed.** Every rule here is about what was TRIED, because a record of successes cannot see an abandoned phase, and an abandoned phase is exactly what a resume needs to know about.

**Borrow the page workflow's model, and say where labeling differs.** The proven parts ship in `haipipe-page-workflow`; this page repeats none of them and names only the delta.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**The loop as it is actually driven**: routes are returned by a phase, never prescribed by a counter.

```text
   1 START ─▶ 1 PICK ─▶ 2 LOCK ─▶ 3 LABEL ─▶ 4 RULES ─▶ 5 NUMBERS ─▶ 6 NEXT?
              🚧gate              🧠hours                             │
              ▲                    ▲          ▲                       │
              └────────────────────┴──────────┴───── 6 routes back ───┤
                                                                      │
                                                        all gates hold│
                                                                      ▼
                                                  8 FREEZE 🚧 ─▶ 8 ─▶ 9 ─▶ 10
```

## Content

### 1 · Four words, and none substitutes for another
**The four words**: what each one answers, which receipt field carries it, and whether it repeats.

```text
word         answers                       receipt field   repeats?
────────────────────────────────────────────────────────────────────
🌀 JOB       which labeling job is this?   the run itself   no
             one target on one corpus
⏱️ PHASE     which authority acts?         `phase:`         YES
             one of the eleven
🔢 STEP      where in this run?            `step:`          never
             a monotonic position
🔁 ROUND     which calibration round?      `round:`         YES
             the era of one closed policy
```

A PHASE is a TYPE and a STEP is an INSTANCE of one: in a job that went back twice, phase 4 occupies steps 4, 9 and 15.
The word must permit repetition, which is the same reason RUN is not ADVANCE.

### 2 · What a receipt carries
**The receipt fields**: what one attempted phase writes down.
One receipt per ATTEMPTED phase, because an abandoned phase leaves no artifact and an artifact-only record cannot see it.

```text
field            what it holds
──────────────────────────────────────────────────────────────────────
job              the target and the corpus
round            t, the calibration round this attempt belongs to
step             the monotonic position in this run
phase            0 to 10
actor            the person, or the named agent file
started          the clock, not a guess
ended            the clock, or absent if the phase was abandoned
route            where the phase said to go, or absent if abandoned
inputs           the sha256 of every file the phase read
outputs          the sha256 of every file the phase wrote
prev             the sha256 of the previous receipt, which makes a chain
```

**The auditor REHASHES rather than trusting the receipt**, because a record that verifies itself verifies nothing.

### 3 · Phase 3 needs a receipt per ITEM, not per phase
**Where labeling differs**: why a phase-level receipt cannot record what happens inside phase 4.

```text
page workflow          one phase is one agent dispatch, minutes long, and
                       either it returns or it did not run
this workflow          phase 4 is a PERSON judging 60 items over 1 to 3
                       hours, and they leave the chair in the middle of it
──────────────────────────────────────────────────────────────────────
consequence            a phase-level receipt for phase 4 records "started,
                       never ended" and tells a resume nothing
the rule               inside phase 4, one line per ITEM: the item id, the
                       class, the region, the uncertainty, the reason, and
                       whether it was judged before or after the lock
what resume then does  re-show nothing already judged, skip nothing not
                       judged, and refuse to reopen the lock
```

The same rule applies to phase 10, where the person works a risk queue over days.
Phases 0, 1, 2, 4, 5, 6, 7, 8 and 10 are short enough that a phase-level receipt is enough.

### 4 · Where a run stops, and what a stop means
**The six stops**: which of them mean the job is done, and which five do not.

```text
stop                        means
──────────────────────────────────────────────────────────────────────
✅ phase 8 signed            the job is done, and only phase 8 may say so
⏸️ explicit HOLD             a gate could not be evaluated
🚫 missing input             a phase's required file was not there
🚫 version mismatch          the policy moved under a phase that had
                            already read it
✋ human gate                a tick is owed and the person is not present
⏱️ max steps or max rounds   the run did NOT converge, and this never
                            means quality passed
```

### 5 · The receipt is the one state source
**One source or two**: what `label-status` reads today, and what it should read.

```text
today       label-status reads REPORT.md, config.yaml, .state.json, round
            manifests, checkpoints and scorecards, which are the closed
            artifacts: they say what succeeded
proposed    label-status reads the receipt chain, which says what was
            attempted, and derives the closed view from it
why         two sources drift, and the one that drifts silently is always
            the one nobody is looking at
```

⬜ Nothing writes a receipt today, so this division describes a contract and not a behaviour.

## Aims

### A1 · 🔤 Four words, and none substitutes for another
- A1.1 · A run can be described without ambiguity between a phase type and its instance.
  **Done when:** Division 1 defines job, phase, step and round, and each maps to one receipt field.

### A2 · 🧾 What a receipt carries
- A2.1 · Every attempted phase leaves a chained, rehashable record.
  **Done when:** A schema exists and `label-round` writes one receipt per attempted phase.

### A3 · 🧠 Phase 3 needs a receipt per ITEM, not per phase
- A3.1 · An interrupted session resumes re-showing no item and skipping none.
  **Done when:** Phase 3 and phase 10 write per-item lines and a resume reads them.

### A4 · 🛑 Where a run stops, and what a stop means
- A4.1 · A run that stopped at a limit is never read as a run that passed.
  **Done when:** Division 4 names all six stops and marks which are not success.

### A5 · 📡 The receipt is the one state source
- A5.1 · One source answers where a job stands.
  **Done when:** `label-status` derives its view from the receipt chain rather than from closed artifacts.

## States

### A1 · 🔤 Four words, and none substitutes for another
- ✅ A1.1 · Met; division 1 fixes the four words and their fields.

### A2 · 🧾 What a receipt carries
- ⬜ A2.1 · Not met; the fields are named and no schema or writer exists.

### A3 · 🧠 Phase 3 needs a receipt per ITEM, not per phase
- ⬜ A3.1 · Not met; the rule is stated and phase 4 records nothing per item.

### A4 · 🛑 Where a run stops, and what a stop means
- ✅ A4.1 · Met; division 4 names the six stops and marks the five that are not success.

### A5 · 📡 The receipt is the one state source
- ⬜ A5.1 · Not met; `label-status` reads closed artifacts, which is a second source.

## Files

### Contracts · what this Page borrows and what it changes
- `../../../../haipipe-toolkit/skills/board/page-workflows/haipipe-page-workflow/ref/page-run-contract.md`
  The packet and receipt spec this page borrows, and whose per-phase granularity it changes for phase 4.
- `../../skills/page-workflows/label-round/SKILL.md`
  Carries the unimplemented promise "Resume the recorded open phase when one exists".
- `../../skills/page-workflows/label-status/SKILL.md`
  Reads closed artifacts today, and should read the receipt chain.

## Law
- 260818 CC · 🔁 RUN is not ADVANCE
      A run may repeat a phase, route backwards, or stop without closing, so no rule may assume the next phase is the next number.
- 260818 CC · 🧾 A receipt records what was ATTEMPTED
      A record of closed artifacts cannot see an abandoned phase, and an abandoned phase is exactly what a resume needs to know about.
- 260818 CC · 🧠 A phase a PERSON sits through is recorded per item
      Phase 3 runs for hours and is interrupted, so a phase-level record says only "started, never ended" and tells a resume nothing.
- 260818 JL · ⏱️ A limit stop never means quality passed
      Hitting max steps or max rounds means the run did not converge, and reporting it as a completion is the failure the stop list exists to prevent.

## Glossary
- 🌀 **Job**: one labeling run, on one target and one corpus, from phase 1 to phase 11.
- ⏱️ **Phase**: one of the eleven authorities, which may be entered more than once.
- 🔢 **Step**: a monotonic position in one job, which never repeats.
- 🧾 **Receipt**: the record of an ATTEMPTED phase, which is not the record of a closed artifact.

## Log
260818 · Created QLw13 on the QPw8 precedent, borrowing the page workflow's four words and receipt chain.
260818 · Recorded labeling's one real difference: phase 4 and phase 10 are worked by a person over hours or days, so their receipts are per item and not per phase.
