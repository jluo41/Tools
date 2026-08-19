# The agents: who runs each phase when no person is in the loop
state: 🟡 PARTIAL · nine agents, six reachable by name · open: three named only as role words
owner: CC
method: Name every hand by the ONE act it may never perform. Say which phases it acts in. A boundary is only real where it is written beside the phase that could cross it.

## Opening
Who actually performs each of the eleven phases, and what may each of them never do?
Nine agent files ship in `agents/`.
The boundary between them is the whole design: proposal, semantic ruling, canonical writing, and evaluation are separate authorities.
One hand holding two of them can turn its own output into gold.
This page is the ROSTER of those hands against the phases of `QLw00`.

**Where this page sits**: `QF3-agent-topology` fixes what authority each agent HOLDS across the method, and this page says which phase each one ACTS in and what it may never do there.
A letter rather than a digit means this page is not a phase: digits `QLw1` to `QLw11` are the eleven phases, and letters are the machinery that runs them.

**Why it matters**: A correct sequence still fails if the same hand predicts, reveals, adjudicates, rewrites gold, and approves its own checkpoint.

**What is settled here**: The nine hands, the act each may never perform, and the phases each appears in.

**What remains open**: `QF3`'s `## Files` names six of the nine. `classifier-agent`, `embedder-agent` and `prober-agent` appear only as role words in its `States A2.1`, so no scan can reach them from that page.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A hand is named by what it may NEVER do.** Writing `the sampler selects candidates` says nothing; writing `the sampler never assigns gold` says the design.

**Say the file name, never the role word.** Write `sampler-agent`, not `the candidate selector`, because a role word cannot be grepped and a reader cannot open it.

**This page never restates a procedure.** Each agent's own file is the authority on how it works, and a copy here goes out of date the night it is written.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
**The roster against the loop**: which hand acts in which phase, and where the person is the only hand.

```text
phase              hands that act                     🧠 person?
──────────────────────────────────────────────────────────────────
  1 START           sampler · moderator · embedder     RULES the meaning
  2 PICK            sampler · embedder · prober        APPROVES the batch
  3 LOCK            labeler-panel                      absent, on purpose
  4 LABEL           moderator · gallery-keeper         DECIDES every item
  5 RULES           moderator · gallery-keeper         ACCEPTS every rule
  6 NUMBERS         disagreement-analyzer              reads
 6 NEXT?           gallery-keeper                     SIGNS the route
  8 FREEZE          gallery-keeper records             SIGNS the freeze
  9 SCORE           validator · labeler-panel ·        absent, on purpose
                   classifier
 10 LABEL ALL       the chosen executor                ANSWERS the queue
11 SPOT CHECK      gallery-keeper                     JUDGES blind
```

## Content

### 1 · The nine hands, each by what it may never do
**The boundary is the identity**: every row ends at the line that hand cannot cross.

```text
moderator-agent            the only human-facing hand
   NEVER   discloses the sealed guesses before the first-pass lock,
           and never auto-confirms a semantic ruling
   phases  1 · 4 · 5

sampler-agent              composes the pool and the batch manifest
   NEVER   assigns gold
   phases  1 · 2

embedder-agent             vectors, neighbourhoods, distances
   NEVER   inherits a label from a nearest neighbour
   phases  1 · 2

prober-agent               suggests boundary contrasts and thin rules
   NEVER   chooses gold, replaces the random first batch, or finalizes
           the human batch
   phases  2

labeler-panel-agent        runs each weak executor independently
   NEVER   lets its own consensus become gold
   phases  3 · 9

disagreement-analyzer-agent compares sealed guesses with human records
   NEVER   decides a final class or resolves a case
   phases  6

gallery-keeper-agent       the SOLE writer of closed state and gold
   NEVER   writes a record the person did not confirm, and never
           closes a checkpoint whose seal or evidence is missing
   phases  4 · 5 · 7 · 8 · 11

validator-agent            the sealed Final Evaluator
   NEVER   modifies G*, T*, wrappers, candidates, or selection rules,
           and never approves a system it scored
   phases  9 · 11

classifier-agent           an optional small supervised model
   NEVER   creates gold, and never trains on model consensus
   phases  9 · 10
```

### 2 · Three of the nine cannot be reached from QF3
**The roster and the topology disagree**: `QF3`'s `## Files` lists six agent files, and nine ship.

```text
in QF3 ## Files      moderator · sampler · labeler-panel ·
                     disagreement-analyzer · gallery-keeper · validator
NOT in ## Files      classifier · embedder · prober
                     they appear in QF3's States A2.1 as the role words
                     "classifier, embedder, and optional prober"
consequence          a name scan over QF3 seeds six rows and misses three,
                     so the two pages will drift and neither will notice
```

⬜ Repairing `QF3` is not this page's work, and this page is where the gap is recorded until someone does it.

### 3 · The two phases where the person is absent ON PURPOSE
**Absence is content**: in two phases the person's only correct action is to do nothing.

```text
  3 LOCK    the guesses must be produced without the person seeing them,
           or the comparison in phase 6 measures anchoring
  9 SCORE   the protocol was fixed before any score was seen, and a
           person who can intervene can select the answer they wanted
```

Everywhere else the person acts, and in five phases they write a tick no agent may write, which is `QLw14`.

## Aims

### A1 · 🤖 The nine hands, each by what it may never do
- A1.1 · Every agent that ships is named here with the one act it may never perform and the phases it acts in.
  **Done when:** Division 1 carries all nine with a NEVER line and a phase list.

### A2 · 🔗 Three of the nine cannot be reached from QF3
- A2.1 · The roster and the topology name the same nine files.
  **Done when:** `QF3`'s `## Files` lists all nine agent files, so a name scan from either page reaches the same set.

### A3 · 🙈 The two phases where the person is absent ON PURPOSE
- A3.1 · A reader can tell an absent person from a forgotten one.
  **Done when:** Division 3 names both phases and the failure each absence prevents.

## States

### A1 · 🤖 The nine hands, each by what it may never do
- ✅ A1.1 · Met; division 1 carries all nine.

### A2 · 🔗 Three of the nine cannot be reached from QF3
- ⬜ A2.1 · Not met; `QF3` names six in `## Files` and three only as role words in `States A2.1`.

### A3 · 🙈 The two phases where the person is absent ON PURPOSE
- ✅ A3.1 · Met; division 3 names phase 3 and phase 9 and the failure each prevents.

## Files

### Contracts · what this Page rosters
- `../../agents/moderator-agent.md`
  The only human-facing hand.
- `../../agents/sampler-agent.md`
  Pool and batch composition, with no gold authority.
- `../../agents/embedder-agent.md`
  Vectors and neighbourhoods, which never inherit a label.
- `../../agents/prober-agent.md`
  Optional contrasts, which never finalize a batch.
- `../../agents/labeler-panel-agent.md`
  The weak-executor committee, whose consensus is never gold.
- `../../agents/disagreement-analyzer-agent.md`
  The comparison auditor, which decides nothing.
- `../../agents/gallery-keeper-agent.md`
  The single writer of closed state and cumulative gold.
- `../../agents/validator-agent.md`
  The sealed Final Evaluator, read-only over G* and T*.
- `../../agents/classifier-agent.md`
  An optional candidate, trained on human-confirmed gold only.

## Law
- 260806 JL · 🔐 Human decision, model evidence, policy proposal, canonical write, and evaluation are separate authorities
      No agent may turn its own prediction or proposal into human gold or approve a changed system on the same final test.
- 260818 CC · 🔤 A letter is machinery, a digit is a phase
      `QLw1` to `QLw11` are the eleven phases and `QLw12` to `QLw14` are what runs them, so a reader never has to work out whether page 8 is a step or a service.

## Glossary
- 🤖 **Hand**: one agent file that acts in at least one phase, named on this page by the act it may never perform.
- 🙈 **Absent on purpose**: a phase where the person's only correct action is to do nothing, and the absence is what makes a later number mean something.

## Log
260818 · Created QLw12 to hold the roster against the phases, on the QPw7 precedent, and to record that QF3 names six of nine agent files.
