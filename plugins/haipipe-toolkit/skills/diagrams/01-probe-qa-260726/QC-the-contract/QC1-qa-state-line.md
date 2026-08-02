# The QA file: one mutable field, one writer

state: 🟡 PARTIAL
owner: JL
method: a ticket that becomes a receipt, with exactly one field allowed to change

## Opening
The bank's answer is a file; what may change in it afterwards, and who may change it?
Exactly one mutable field, the `state:` line, and exactly one writer for its whole life, the executor.
Everything else follows: a claim that expires at 24 hours, a noclobber race guard, and supersession that writes a new file rather than rewriting a body.

Everything else on the page follows from those two constraints.
The executor writes twice, the claim when it starts and the completion at its Report, so a claim is visible on disk before any work happens and nobody duplicates it.
A claim must expire, or a crashed run would block a question forever, so `QA_WORKING_TTL_HOURS = 24` makes a stale `working` file restartable.
The race guard is `set -C` and nothing more: two runs may both pick `QA/3-`, the claim is created under noclobber, and the loser re-scans and defers.
An answer that later changes is never rewritten; a new file is written and the old one gains `superseded-by:`, so the record of what was believed when stays intact.

**Covered elsewhere**: The executor-side flow that writes these files, the `qa` verb, is `haipipe-task/`'s `fn/qa.md` and its discovery twin. The entry states on the consumer side are `QC3`.

## Diagram
```
   state: working                      state: answered
   started: 2026-07-14T09:12    ──▶    ## Answer  …            ──▶  state: superseded-by:
   by: <executor>                      ## Caveats                    QA/7-<slug>.md
                                       ## Not-done                   (body never rewritten)

   ONE writer: the executor, for the whole life of the file.
   ONE mutable field: state:.
   A `working` file older than QA_WORKING_TTL_HOURS = 24 is STALE and restartable.
   The race guard is `set -C` and nothing more; the loser re-scans and defers.
```

## Aims
- [x] 🎫 One mutable field, one writer, two writes
- [x] ⏰ A claim expires at 24 hours and becomes restartable
- [x] 🔒 The race guard is noclobber, and the loser defers
- [x] 📚 Supersession writes a new file and never rewrites a body
- [ ] 🧠 JL confirms 24 hours is the right TTL
      It is a constant chosen once and never tested against a real long-running task.
      A build-lane answer legitimately takes days, which is why `commissioned` exists, but the interaction between the two has not been walked through.

## States
Ruled and enforced: four of the checker's FAIL conditions are about this file alone.
The one soft spot is the TTL constant, which was picked rather than derived.

## Files
- `SKILL.md`
  The QA contract, the TTL constant, and the noclobber idiom.
- `haipipe-task/`
  The executor-side `qa` verb that actually writes these files.
