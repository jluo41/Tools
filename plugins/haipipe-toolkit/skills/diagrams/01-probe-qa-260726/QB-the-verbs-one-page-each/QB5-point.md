# ④ POINT · what makes a target honest?

state: 🟡 PARTIAL
owner: JL
method: a path to a FILE, opened and read rather than listed, with the entry's state derived from what the file says

## Opening
An answer exists somewhere; what does the entry write down, and what stops that pointer from lying?
A path to the answering QA FILE, never to its folder, and the file must be OPENED and its state line read before the entry believes anything.
An `ls` is not enough, which is the whole ruling: a target that exists and a target that answers are different facts.

This step has never had a page and it carries more of the checker than any other.
Five of the FAIL codes are about targets, and two of the three failure kinds found on real data were target-state disagreements.
The reason is structural: `target` is the only field that points across the wall, so it is the only field whose truth depends on a file the consumer does not own and cannot fix.

**Covered elsewhere**: The QA state line being pointed at is `QC1`; the derived entry states and how `status` computes them are `QC3`. The rule that decides whether ③ ran before this step is `QB4`; harvesting what the target says is `QB6`.

## Diagram
```
   ── target points at a FILE ──────────────────────────────────────
   target: tasks/A03_welldoc/01_column_scan/QA/1-cycle-indicator.md
                                              ▲
                       point at the FILE, never at the folder

   NEW <path>    the file does not exist yet, the folder is decided
   NEW ?         even the folder is undecided
   <a real path> then OPEN IT. an `ls` is NOT enough.

   ── the read, and what it decides ────────────────────────────────
   the QA file's `- state:` line says      the entry becomes
     answered                                answered  → ⑤ may harvest
     working  + started:                     commissioned, in flight
     superseded-by: QA/<m>-…                 follow the chain; do NOT harvest
     (no state line)                         MALFORMED, the executor must fix
     the file is gone                        failed

   state is DERIVED, never asserted. the entry does not get to say
   what it is; the disk says, and the entry is read off it.

   ── the five checker codes that live at this step ────────────────
   empty-target                 no target at a state that requires one
   unresolved-target            still NEW at a state past planned
   workspace-target             points under _WorkSpace/, which is
                                gitignored: name the TASK instead
   read-target-no-state         the target carries no `- state:` line
   commissioned-target-no-state the same, at the other entry state
   ── plus the two that fire when the read is SKIPPED ──────────────
   answered-not-read            the answer landed, nobody harvested
   commissioned-target-answered the answer landed, entry still waiting
     together: ALL 7 real failures on the MISQ paper (the other 5
     were the checker false-failing correct work — QC2)
```

## Content
### 1 · Why the file, and not the folder
A folder can exist, be full of results, and answer nothing readable.
The layer binds by path precisely so that a consumer can hand an agent a pointer, and a pointer to a folder is an instruction to go and judge, which is the one thing the probe is forbidden to do.
Pointing at the file also makes the state question answerable: a file has a state line, a folder does not.

### 2 · Why `an ls is not enough` had to be written down
#### The two failures it prevents are the two that actually happened
(`answered-not-read` 5 times and `commissioned-target-answered` twice, and after the 260726 correction they are the ONLY real failures on the only real consumer)
Both are the same mistake seen from two entry states: the target's file says `answered` and the entry does not know it.
Neither is a checker bug and neither is a missing answer; in every case the work was done and the pointer was never re-read.
That is why the read is stated as an obligation of this step rather than as a nicety of the next one.

#### `NEW ?` is the honest form of not knowing
An entry that has not decided where the answer will live writes `NEW ?` rather than guessing a folder.
Guessing produces a `workspace-target` or an `unresolved-target` that looks decided, and a plausible wrong path is harder to notice than an admitted unknown.

### 3 · The one thing this step may write, and nothing else
The agent that performs ③ and ④ is permitted to write the `target` field and never the stake, and its state is derived rather than set.
So the write is a single field, and everything else about the entry is either frozen from ① or computed from disk.

## Aims
- [x] 📍 `target` is a path to the answering FILE, never to a folder
- [x] 👁 The target must be OPENED and its state line read; an `ls` is not enough
- [x] 🧮 The entry's state is derived from that read, never asserted
- [ ] 🔁 The 7 target-state failures on MISQ are fixed or triaged
      5 `answered-not-read` and 2 `commissioned-target-answered`, all of them a landed answer whose entry never re-read the target.
      Once the five false `deferred-undeclared` are struck, every real failure the layer has on real data belongs to this step.
      Held jointly with `QC2`, which owns the whole failure list.
- [ ] 🧪 A stale target is detected before a gate, not at one
      Every one of the 7 was found by running the checker at CHECK, which is the last possible moment.
      This closes when a re-point runs during PROBE, or a ruling says the gate is the right place to catch it.
- [ ] 🧠 JL rules what a consumer does with a `superseded-by:` target
      The model says follow the chain to the live answer and says nothing about whether the entry re-points itself, or whether the old answer stays valid for a consumer that already harvested it.
      A paper that cited the superseded answer has a real problem and no stated procedure.

## States
Newly separated on 260726, and it was the step most worth separating: it had no page, it owns five of the checker's codes, and after the `QD2` run struck five false failures, **every one of the 7 real failures on the MISQ paper is its**.

The rules themselves are sound and stated. What is missing is any moment before the gate at which a stale pointer is noticed, and any procedure for the case where a harvested answer is later superseded.

## Files
- `SKILL.md`
  The target field, the three unresolved forms, and the derived states.
- `haipipe-paper-probe/`
  Where the read obligation is spelled out per step.
