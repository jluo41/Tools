# Can a fresh agent run a stage: the one test we are not allowed to grade ourselves

state: 🔴 OPEN
owner: JL
method: hand a clean-context agent one stage and watch what it does, not what it produces

## Opening

Can someone with no background read this skill and run one stage correctly, end to end?

A fresh agent is one with no memory of any design discussion. Behavioural evidence is what it DID: which entry it found, which path it followed, where it stopped. This is the only question on the board whose answer is not ours to decide, because we read every contract with the context already in our heads.

**Where this page sits**: QF1 owns the execution record and names three evidence modes.
This page owns the third of them, and it is the only mode the author is disqualified from producing.
Whether any single contract is well written is a writing question and belongs elsewhere.

**Why the process and not the artifact**: a correct-looking artifact produced by ignoring the contract is a failure.
It passes today because the agent guessed well, and the next paper will not be so lucky.
So the test grades which entry was found, whether the phases were followed, and whether it stopped at the gate.

**What we already suspect**: it would fail today.
On the MISQ paper an agent wrote the line saying a gate had passed, which is exactly the step it was supposed to stop before.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `../BoardSkillBoard-260722/QPs-page-structure/QPs1-overall/QPs1-overall.md` and are not restated here.

**Never report an artifact as evidence here**: this page's currency is what an agent did.
"It produced a valid Seed page" is a QF1 mechanical record; "it stopped before DRAFT" is behavioural evidence and belongs here.

**Name which of the three levels any claim belongs to**: ①, ①ʹ, or ②.
The 260726 incident happened precisely because a ① result was read as covering ②.

**Keep a near-miss labelled a near-miss**: the 260725 clean-context run validated the creator boundary and nothing else.
Writing it as partial credit toward this test is how an unrun test starts looking run.

## Diagram

**Three levels, not two**: and only the third needs a stranger.

```text
   ① MECHANICAL      facts about files                  👤 the author MAY run
      every path resolves · every contract parses · checker exits 0

   ①ʹ END-TO-END     the skill's own procedure,         👤 the author MAY run
      walked against a REAL subject, exactly as written

   ② BEHAVIOURAL     what a stranger DOES               🚫 the author may NOT
      does it trigger · follow the workflow · stop at the gates

  ── why ①ʹ deserves its own name ──────────────────────────────────
  260726: the venue pin was ruled into a `venue:` frontmatter key that
  haipipe-board's parser cannot read. It was specified in 12 places.
  EVERY mechanical check passed: paths resolved, all 8 contracts parsed,
  the checker exited clean. Both documents were internally consistent
  and the pair was WRONG.
  It surfaced within hours by walking enter's own frontier predicates
  against the MISQ paper. That is ①ʹ: minutes to run, uncontaminated
  because it produces facts, and it caught what ① structurally cannot.

  ── run on 260726 ─────────────────────────────────────────────────
   ①   ✅  8 contracts form ok · conform exit 1, 56 findings
   ①ʹ  ✅  once, unplanned, and it found the day's worst defect
   ②   ⬜  never. 20 skills rewritten, the door untested.
```

## Content

### 1 · Why the test watches the process

**Two ways to produce the same artifact**: only one of them is a pass.

```text
   📄 the artifact looks correct
              │
     ┌────────┴────────┐
     ▼                 ▼
  ✅ followed        ❌ guessed well and
     the contract       ignored the contract
     │                  │
     ▼                  ▼
  repeatable         works once · the next
                     paper will not be lucky

  🔑 the repository's own rule: watch HOW a fresh agent works,
     not only what it produces
```

🔬 Establishes why an artifact cannot settle this question, and what the test grades instead.

#### 1.1 · The failure mode is invisible from the inside
(everyone who wrote the contracts reads them with the answer already in mind)
Every other face on this board is an internal argument we can settle among ourselves.
This one cannot be, because the thing being measured is whether the design survives contact with someone who was not in the room, and no amount of rereading it ourselves produces that evidence.

### 2 · What passing means

**Six behaviours**: and the one most likely to fail.

```text
   ① picks the right stage from a plain request
   ② runs DRAFT without fetching evidence
   ③ raises questions rather than answering them
   ④ respects probe_depth, defers what it may not spend
   ⑤ stops at CHECK and ASKS, rather than writing the gate line   ◄ ⚠️
   ⑥ writes the artifact where the contract says, and nowhere else

  ⚠️ ⑤ is the one most likely to fail: it is the only one that
     requires an agent to STOP when it could continue

  🚪 the sharpened form, from the single-door ruling:
     given /haipipe-paper enter <path>, a fresh agent must end up
     LOOKING at a board without ever hearing the word `haipipe-board`.
     If it types the second skill, the ruling is not implemented,
     whatever the files say.
```

🎯 Establishes the pass condition as six observable behaviours, so the verdict is a comparison rather than an impression.

#### 2.1 · Stopping is the hard one because nothing forces it
(the other five are about doing the right thing; this one is about not doing an available thing)
An agent that can write the gate line usually will, because writing it looks like completing the task.
Every other behaviour on the list can be satisfied by following instructions well, and this one requires declining an action the environment permits.

### 3 · What we know already

**Two data points**: one near-miss, one warning.

```text
  260725  a clean-context agent created a missing Seed page, paged it,
          and stopped before DRAFT
          ✅ validates the CREATOR boundary (QA8)
          ✗  did not exercise the four phases, the probe ceiling,
             or the CHECK gate
          🚫 NOT the acceptance test

  MISQ    an agent wrote the line saying a gate had passed        ⚠️
          one data point saying this test would FAIL TODAY on ⑤,
          which is exactly QC4d's open item
```

📋 Establishes the current evidence, and marks clearly which of it does not count toward this test.

#### 3.1 · The near-miss is recorded so it cannot be recycled as a pass
(a partial run cited often enough starts to sound like the real one)
The 260725 run validated the creator boundary and that alone.
It is written here with what it did NOT exercise, so a later reader cannot mistake it for the acceptance test that has still never been run.

## Aims

### A2 · 🎯 What passing means
- A2.1 · The behavioural test is run on one full stage.
  **Done when:** a clean-context agent is given a plain request against a scratch copy, and all six behaviours are observed and written down.
- A2.2 · What it got wrong is recorded before anything is fixed.
  **Done when:** the findings are written here first, because fixing before recording destroys the evidence.
- A2.3 · The test is re-run after the fixes.
  **Done when:** the loop has repeated until a clean-context agent behaves as designed, which is the repository's own rule.

### P · 🏁 Page-level
- P1 · The board's design is validated by someone who was not in the room.
  **Done when:** ② is ✅ for at least one stage, so the pages on this board are results rather than designs.

## States

### A2 · 🎯 What passing means
- ⬜ A2.1 · Never run. Twenty skills have been rewritten and the door is still untested; Section Edit remains the intended hard case because it is the most complex stage.
- ⬜ A2.2 · Not started, and it depends on A2.1.
- ⬜ A2.3 · Not started, and it depends on A2.2.

### P · 🏁 Page-level
- ⬜ P1 · Unrun, and one data point suggests it would fail. On MISQ an agent wrote a gate line itself, which is behaviour ⑤ and is QC4d's open item.

## Files

- `../../../../CLAUDE.md` · the repository's fresh-subagent validation rule
- `../../paper/S06-main/section-edit/stage.md` · the hardest stage, and therefore the right one to test
- `../QF1-execution-map/QF1-execution-map.md` · owns the record this run's observations become
- `6-QC-engine/QC4d-check/QC4d-check.md` · owns the gate-line item this test would most likely fail on

## Law

- A correct-looking artifact produced by ignoring the contract is a failure, not a pass.
  The author may run ① and ①ʹ; only a stranger may produce ② evidence, and a partial clean-context run is never recorded as partial credit toward it.

## Glossary

- **Behavioural evidence**: what a fresh agent did, as distinct from what it produced.
- **①ʹ end-to-end**: walking the skill's own procedure against a real subject; cheap, uncontaminated, and able to catch what mechanical checks structurally cannot.

## Log

260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered into three divisions with face figures and captions, Aims regrouped as A2/P with `Done when`, States mirrored per Aim, and Law and Glossary written for the first time.
260726 · Recorded the three levels after ①ʹ caught the `venue:` frontmatter defect that every mechanical check had passed.
