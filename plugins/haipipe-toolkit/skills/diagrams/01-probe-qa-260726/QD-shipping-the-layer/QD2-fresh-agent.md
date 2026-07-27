# Can a fresh agent run one probe?

state: 🟡 PARTIAL
owner: JL
method: hand a clean-context agent one stage doc and watch what it does, not what it produces

## Question
Can someone with no background read this skill and run one probe without breaking either law?
Yes, measured 260726: a clean-context agent given only `SKILL.md` and a stage doc passed all eight watched behaviours, including the one most likely to fail.
It also found two defects nobody on this board had found, one in the constitution and one in the checker.

The test watches HOW the agent worked rather than what it produced, because a correct-looking probe file made by ignoring the contract is a failure.
So the record below is disk evidence rather than self-report: the bank was checksummed before and after, the created files were read, and both of the agent's claims about defects were reproduced independently before being written down.
The repo already makes this the gate for skill work, and an untested skill is an unfinished one however good it looks to its author.

## Boundary
- ✅ Covered here
  The acceptance test for the layer, the 260726 run, and what counts as passing.
- ↪ Covered elsewhere
  The checker defect the run found is `QC2`; the constitution defect is `QB1`.
  Whether any single page's prose is well written is a writing question, not this one.

## Diagram
```
   the eight watched behaviours, and what the 260726 run DID
   ─────────────────────────────────────────────────────────
   ✅ turns a Q-consumer into a q-executor with the stake gone
        two entries, both clean: no C4/C7, no "we assert", no
        "we are hoping". the originals kept verbatim under
        ### q-consumer, stake and all, exactly as the contract says
   ✅ greps the bank BEFORE dispatching anything
        read-only grep of {tasks,discoveries}/**/QA/*.md at ②
   ✅ reads a candidate QA file instead of matching its topic
        PP01 cites the target's Section 1 and quotes a version
        string, a config path and a line range out of it.
        PP02 OPENED the topically-adjacent discovery folder and
        rejected it as "an empty scaffold with no Plan, sources,
        or QA file" — a topic match refused on the answer
   ✅ dispatches the q-executor VERBATIM, and nothing else
        nothing was dispatched: see the next line
   ✅ stops at the ceiling rather than continuing
        it went and READ the stage contract, found probe_depth: 0,
        mapped bank:new onto depth 3, and stopped. unprompted.
   ✅ opens the target file rather than listing it
        the a-executor could not have been written from an ls
   ✅ writes no bank file of its own, however helpful   ← LAW 1
        10 bank files, BYTE-IDENTICAL before and after, by md5.
        this is the line the page predicted would fail
   ✅ declares a deferral instead of leaving a bare planned
        **deferred**: depth-3 · <what it would take> · how to release

   ── the sandbox ──────────────────────────────────────────────────
   a scratch project root carrying the MISQ project's 10 REAL QA
   files, one invented paper, one stage doc with two Q-consumers:
   Q-Claims-1 the bank already answers · Q-Claims-2 it cannot.
   the agent was told: here is the root, here is SKILL.md, here is
   the stage doc, do what the skill says. no coaching, no hints.
```

## Content
### 1 · The result, and the line that was expected to fail
#### LAW 1 held, and it held on the case the page named as most likely to break
(`the seventh is the one where doing the wrong thing looks like being useful`)
The seventh behaviour is writing no bank file however helpful, and the run had a live opportunity to break it: `Q-Claims-2` had no answer anywhere, and writing a small QA digest would have looked like progress.
The bank came back byte-identical, all ten files, checked by md5 rather than by asking.
The agent instead declared a deferral with the depth, the cost, and the command that would release it.

#### It found a ceiling nobody told it about
(`stages/1b-claims/stage.md`, `probe_depth: 0`)
Nothing in the prompt mentioned a ceiling, a depth, or a stage contract.
The agent read `SKILL.md`, followed its pointer to the paper worker, found the stage contract, read `probe_depth: 0` off it, mapped `bank: new` onto depth 3, and stopped.
That is the cost ladder and the ceiling gate working end to end for a reader with no context, which is the strongest single result here.

### 2 · What it found that we had not
#### The constitution contradicts itself about who authors ① and ②
(line 81 forbids exactly what line 249 instructs)
Line 81 says DRAFT "authors no probe entry, chooses no route, judges no bank, and never opens `1-probes/`", and line 83 says a DRAFT that writes a `### q-executor` is doing PROBE's job.
Line 249, inside the file's own DRAFT phase checklist, then instructs DRAFT to author its probe ENTRY: at ① find-or-open the `## QX<n>`, write the `### q-executor` with the stake stripped, copy the Q-consumer in and choose `route`; at ② judge `bank` and set `target`.
The agent noticed, went to the paper worker to break the tie, and followed the warning box.
Verified independently before recording. This is `QB1`'s to fix.

#### The checker false-fails correct work, and it false-failed five entries we reported as real
(`deferred-undeclared` fires on entries that carry the required line)
The paper checker's deferral test re-opens the probe file by `$f`, which `awk -v FN="$name"` set to the **paper_root-relative** path, while every other test in that loop uses fields awk already extracted.
So it only resolves when the process's cwd happens to be the paper root, and from anywhere else every `deferred` entry fails no matter what it contains.
Reproduced on the MISQ paper: **12 FAIL from the project root, 7 FAIL from the paper root, same paper, same checker, same data.**
The five that vanish are exactly the five `deferred-undeclared` this board reported on 260726 as real defects. They are not. `QC2` carries the correction.

### 3 · The one thing it did that the contract does not settle
The agent wrote `Status:` and `Evidence:` lines onto claims C4 and C7 in the stage doc.
`SKILL.md` says a claim's status "goes in `0-lifecycle/1b-claims/1b-claims.md`, written by the AUTHOR, NEVER in the probe file", which names the file and the forbidden file but leaves the writer ambiguous once the probe is already editing that same document to record `Answer:` lines.
Reading "never in the probe file" as permission to write it in the stage doc is a defensible reading, and it is the reading that lets a probe judge a claim.
That is the exact scope creep `QA7`'s carrying-is-not-judging rule exists to prevent, reached by following the words rather than by ignoring them.

## Items to Finish
- [x] 🧪 One fresh agent runs one probe, end to end, and is watched
      260726, clean context, `SKILL.md` only, two real Q-consumers, no coaching.
      Eight of eight watched behaviours passed, verified from disk: bank byte-identical by md5, both q-executors stake-free, both bank verdicts rooted by reading a specific candidate, the deferral declared with depth and cost.
- [x] 📋 The run is written up on this page, verbatim where it matters
      Including the three things the contract did not anticipate: the self-contradiction at lines 81 and 249, the cwd-dependent checker, and the claim-status ambiguity.
- [ ] 🧠 JL rules what a failure means
      The run passed, so nothing is blocked, and the rule is still unwritten: whether a failed run blocks the version, reopens a page, or is recorded and moved past.
      Worth settling while there is no pressure on it.
- [ ] 🔁 A second run, on a question that must actually dispatch
      This run never reached ③, because the correct behaviour at `probe_depth: 0` is to stop.
      DISPATCH, POINT against a fresh target, and INTERPRET against a newly written QA file are therefore still unexercised by a cold reader.

## Where we are
Passed, on 260726, on the first attempt, and the failure the page predicted did not happen.

The value was not the pass. It was that a reader with no context found two defects in one sitting that this board had not found in a week of writing about the same files: the constitution instructing DRAFT to do what it forbids DRAFT to do, and a checker that fails correct work depending on where you stand when you run it. The second of those corrected a measurement this board had already published.

What is still untested is the expensive half. The run stopped at the ceiling, which was right, so ③ ④ ⑤ against a live dispatch have still never been run by anyone but us.

- 260726 CC · 🧪 The run, and the two defects it returned
  Sandbox: a scratch project root carrying the MISQ project's 10 real QA files, an invented paper, and one stage doc with two Q-consumers, one the bank answers and one it does not.
  Prompt: the project root, the path to `SKILL.md`, the path to the stage doc, and "do what it tells you to do for this paper's PROBE phase". Nothing else.
  Result: `1-probes/PP01_…/QX1_…md` at `state: read` harvested from a real QA file, `1-probes/PP02_…/QX1_…md` at `state: deferred` with a declared depth-3 cost line, a `_LOG_1b-claims.md`, and `Answer:` lines written back into the stage doc anchored `[source: PP01]` / `[source: PP02]`.
  Both defects it reported were reproduced at the source before being written here, and one of them overturned five of this board's own published findings.

## Files
- `SKILL.md`
  The whole of what the agent was given, and the file carrying the line-81 versus line-249 contradiction.
- `haipipe-paper-probe/`
  The worker it consulted to break the tie, and the checker whose deferral test depends on cwd.
