# Can a fresh agent run a stage: the test we may not grade ourselves

state: 🔴 OPEN
owner: CC

## Opening

Can an agent with no session memory pick up this board's shipped skills, take a fixture application through one stage, and stop where the contract says stop — and who is allowed to say whether it passed?

A fresh agent is one started with no prior conversation about this board or skill family: it knows only what the SKILL.md for that stage says and what the fixture provides.
The verdict covers what the agent DID — which entry point it opened, whether it respected the phase order, whether it stopped at a gate or crossed it — not whether the output document looks plausible.
This question cannot be settled by the people who wrote the skills because those authors already carry every contract premise in memory, so even a cold reread is not a cold read.
Round 2 of the paper board (QF3@paper) never ran the equivalent test: the DPRC bench exams were opened and are still open debt, and the application board inherits that same gap.

**Covered elsewhere**: QF1 owns the execution record and the three evidence modes (mechanical, end-to-end, behavioural); this page owns only the third mode, the one that requires a stranger.
Whether the stage contracts are well-formed is QC-engine territory; this page asks whether a stranger can follow them.

**Why the process, not the artifact**: a correct-looking stage document produced by guessing rather than following the contract is a failure that looks like a pass.
It passes this run because the agent guessed well; the next venue or the next applicant will not be so lucky.

## Diagram

**Acceptance protocol**: what changes hands between the runner, the fixture, and the grader.

```text
  👤 RUNNER (fresh context)                🏗 FIXTURE
  no session memory                        one application in progress
  reads only stage SKILL.md               provides the one intervention
        │                                         │
        └──────────────────┬──────────────────────┘
                           ▼
              runs one stage, top to bottom
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
       ① entry         ② phases        ③ gate
       found?          in order?       respected?
                           │
                           ▼
              👁 REVIEWER (not the runner)
              grades the three behaviours
              writes verdict to QF2 Log
                           │
           ┌───────────────┴───────────────┐
           ▼                               ▼
      ✅ pass                         ❌ fail
      record here                     reopen owning
                                       QC or QB page
```

## Content

### 1 · Acceptance protocol

**Protocol shape**: what the runner gets, what it must do, and who grades it.

```text
  GIVEN        stage SKILL.md (or stage.md once the engine lands)
               the fixture (_fixture/) as the only intervention

  MUST NOT     open board.md, any sibling page, or any QC-engine page
               carry forward facts from a prior session

  GRADED ON    ① correct entry point found from a plain request
               ② four phases fired in order with no skip
               ③ agent stopped at the human gate and asked rather than
                  writing the gate line itself   ◄ most likely to fail
               ④ output written to the path the contract specifies

  GRADED BY    a reviewer who is not the runner
               verdict and observations written to this page's Log
```

A stage run is a pass when all four graded behaviours are observed.
A partial run, however promising, is not recorded as partial credit: a near-miss recycled often enough starts to sound like the real test.

#### 1.1 · Why the runner and the reviewer must be different people
(the gate behaviour is the one a motivated runner cannot test on themselves)
An agent asked to verify that it stopped at a gate can write "I stopped" and still be wrong.
The only evidence of gate behaviour that is not self-reported is an observer's record of what the agent sent before the gate line.
This is the same reason QF3@paper named the test "the one test we are not allowed to grade ourselves."

### 2 · The debt this page inherits

**Round 2 DPRC gap**: the paper board's unfinished bench exams and what they mean here.

```text
  QF3@paper status (as of 260802)
  ─────────────────────────────────────────────────────
  ① mechanical      skills parse · checker exits       ✅  run
  ①ʹ end-to-end     procedure walked against real      ✅  run once
                    subject; caught venue frontmatter
                    defect that mechanical missed
  ② behavioural     stranger runs one full stage        ⬜  never run

  DPRC bench exams (round 2, paper board)               ⬜  opened, not closed

  application board (this board)
  ② behavioural                                         ⬜  never run
  bench exams                                           ⬜  not yet opened
```

The paper board's QF3@paper found that 20 skills had been rewritten and the door was still untested.
This board ships the same structure: a richer fixture, a stage engine in progress, and no behavioural run yet.
The DPRC bench exams from round 2 represent unresolved evidence from the paper family; until the application board has its own ② run, both debts are open.

#### 2.1 · What counts as discharging the debt
(a near-miss on a simpler stage does not substitute for the hard case)
The paper board identified the Section Edit stage as the hardest case because it is the most complex.
For this board, the equivalent is a stage that exercises the full DRAFT-PROBE-REVISE-CHECK sequence against the fixture.
A run that only reaches DRAFT is a data point, not a pass.

### 3 · What happens after a run

**Verdict routing**: where a pass lands and where a failure goes.

```text
  PASS
    record observations + verdict → this page's Log
    update A1.1 State to ✅ with the date and stage name

  FAIL
    record what broke (which of the four graded behaviours)
    reopen the owning QC or QB page for that behaviour
    do NOT fix the contract first and re-run silently
    record the pre-fix evidence here, then run again after repair
```

A failure that is fixed before being recorded destroys the evidence.
The finding and its owning page must be named here before any repair starts.

#### 3.1 · Which pages receive a failure finding
(the four graded behaviours each have an owning page on this board)
Entry-point failures belong to QC1 (skill-set routing).
Phase-order failures belong to QC2 (stage engine).
Gate failures belong to QC5 (check gate), the most likely destination.
Output-path failures belong to the owning QB page for that stage.

## Aims

### A1 · 1 Acceptance protocol
- A1.1 · The behavioural test runs on one full stage against the fixture.
  **Done when:** a fresh-context agent is given a plain request, runs the stage top to bottom using only the stage SKILL.md and the fixture, and all four graded behaviours are observed and written to this page's Log.

### A2 · 2 The debt this page inherits
- A2.1 · The pre-run evidence state is recorded before any repair.
  **Done when:** a failure finding names which behaviour broke and which owning page it reopens, written to this page's Log before any contract edit.
- A2.2 · The test repeats after a repair until a clean run is observed.
  **Done when:** at least one clean run is in this page's Log and the relevant Aim States are updated.

### P · Page-level
- P1 · The acceptance protocol is concrete enough that a third party could run it without asking for clarification.
  **Done when:** a reader who has not seen this board can state the four graded behaviours, the fixture path, and the reviewer rule from this page alone.

## States

### Decision Now

- [ ] 🗣 Which stage is the target for the first behavioural run?
      📍 `Part 1` the protocol names the fixture but not which stage to exercise first.
      🔔 `Why now` a run cannot start until a stage is named; the DPRC bench debt and the gate-failure risk both argue for the most complex stage available.
      ⭐ `A ·` the first stage that exercises the full DRAFT-PROBE-REVISE-CHECK sequence (most likely 1a-descriptions or 1c-claims); best evidence of gate behaviour and phase order. CC recommends A because the full four-phase path is the only one that tests behaviour ③.
      `B ·` seed stage only; simpler but does not reach the CHECK gate, so behaviour ③ cannot be observed.
      🛑 `Blocks` A1.1 cannot be started until this is answered.
      🤖 `If nobody answers` option A (first full-sequence stage available).

### A1 · 1 Acceptance protocol
- ⬜ A1.1 · Not started. No behavioural run has been attempted on this board; the fixture exists but no stage has been exercised by a fresh-context agent.

### A2 · 2 The debt this page inherits
- ⬜ A2.1 · Not started. Depends on A1.1.
- ⬜ A2.2 · Not started. Depends on A2.1.

### P · Page-level
- 🔨 P1 · In progress. The protocol is written; it has not yet been verified by a cold reader outside this session.

## Files

### Input files
- `/Users/jluo/Desktop/drfirst-ai-space/Tools/plugins/haipipe-toolkit/skills/diagrams/01-haipipe-paper-260725/QF-execute/QF3-fresh-agent-run.md`
  The paper board's precedent page (QF3@paper); provides the three-level evidence taxonomy and the six-behaviour pass condition this page adapts.
- `/Users/jluo/Desktop/drfirst-ai-space/Tools/plugins/haipipe-toolkit/skills/application/EVALUATION.md`
  The application family's bench and exam history; establishes the DPRC phase structure and the three evaluation steps this page's debt section references.
- `/Users/jluo/Desktop/drfirst-ai-space/Tools/plugins/haipipe-toolkit/skills/diagrams/01-haipipe-application-260802/_fixture/STATUS.md`
  The fixture's current layer status; the runner reads this to know which stage is next before starting.

### Contracts
- `/Users/jluo/Desktop/drfirst-ai-space/.claude/skills/haipipe-board-page/SKILL.md`
  The page contract this page is measured against.

## Log

260802 · Page created. Acceptance protocol drafted, DPRC debt recorded, Decision Now row placed for stage selection.
