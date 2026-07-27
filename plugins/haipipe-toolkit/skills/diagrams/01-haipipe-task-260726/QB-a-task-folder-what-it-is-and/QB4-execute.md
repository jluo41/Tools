# EXECUTE: why the agent does not press the button
state: 🟡 PARTIAL
owner: JL
method: keep the run a human act by default, and make the record of it automatic

## Question
Who starts a run, and why is the default not the agent? EXECUTE is the only phase with no creator and no reviewer. It is one line, `bash runs/<run>.sh`, and by default a human types it. Every other phase in this lifecycle is agent work with a review loop, so the asymmetry needs a reason or it is just friction.

The reason is cost and irreversibility, and those are the two properties nothing else in the lifecycle has. A plan can be rewritten, code can be revised, a report can be corrected. A run spends GPU hours, writes into `_WorkSpace/`, and on a shared cluster takes a slot from someone else. It is the one phase where being wrong costs something that cannot be undone by editing a file.

What that argument does not settle is `autoExecute`, which exists and defaults to false. If the reasoning above is right, the flag is a deliberate override of a safety property and should be recorded when used. If it is wrong, the default is wrong. Nothing states which.

## Boundary
- ✅ Covered here
  Who runs, why the default is a human, what the run records automatically, and what `autoExecute` means.
- ↪ Covered elsewhere
  What a run script contains is `QC1`; where its outputs land is `QC2`; the notebook it produces is `QC3`; the audit of its results is `QB5`.

## Diagram
```
   EXECUTE                   the ONE phase with no creator, no reviewer

    a HUMAN types            bash runs/<run>.sh
         │                        │
         │                        ├─ pre-flight: the CODE_REVIEW gate   → QB3
         │                        ├─ snapshot runtime.yaml
         │                        ├─ convert .py → template .ipynb
         │                        ├─ papermill → notebooks/<run>.ipynb  → QC3
         │                        └─ EXIT trap: print every file produced
         ▼
    results/<run>/           light artifacts        → QC2
    _WorkSpace/{N}-*Store/   heavy artifacts        → QC2

   ── why a human, by default ────────────────────────────
      a run is the ONLY phase that is
        EXPENSIVE      GPU hours, cluster slots someone else wanted
        IRREVERSIBLE   it writes outside the repo, into _WorkSpace/
      every other phase is a file that can be rewritten for free.

   ── what makes the human's job small ───────────────────
      the run script is ATOMIC and self-contained: one config,
      one model, no CLI arguments, no loops. The human types one
      line and cannot get it subtly wrong, which is what makes
      "a human presses it" cheap enough to keep.

   ── the EXIT trap, which runs on failure too ───────────
      every run prints what it produced, locally and in _WorkSpace,
      on success AND on crash. A run that fails still says what it
      wrote, which is exactly when you most need to know.

   ── autoExecute: false ─────────────────────────────
      the flag exists. If the argument above is right, using it
      overrides a safety property and should leave a record.
      It leaves none.                                  → Items
```

## Content
### The atomic run script is what makes the human affordable
"A human presses the button" is only reasonable if the button is one button. The `runs/` rules
make it so: each script runs exactly one config and one model, hardcodes its parameters, takes no
CLI arguments and contains no loops. Anything that needs to coordinate several runs is `sbatch/`,
one level out.

So the human's decision is binary, which is the only kind of decision worth interrupting someone
for.

### The record is automatic, and that is the trade
The phase asks a human for the one thing only a human should decide and then takes everything else
off them. `runtime.yaml` is snapshotted, the notebook captures stdout, stderr, injected parameters
and figures, and the EXIT trap lists every file produced whether the run succeeded or crashed.

The crash case is the one worth keeping: a failed run still reports what it wrote, which is when a
half-written `_WorkSpace/` entry is most likely and least visible.

### The two templates, and the rule against mixing
Template A tees a log; Template B is papermill and does not, because the recorded notebook IS the
log. `ref/task-structure.md` states that the two must never be mixed within one task, and the
reason is that mixing them produces a run whose log and whose notebook each contain half the
story.

## Items to Finish
- [x] 👤 The human default is implemented
      `autoExecute: false` in the lifecycle workflow; the run is one atomic script with no arguments.
- [x] 🧾 The record is automatic on success and on failure
      `runtime.yaml` snapshot, papermill notebook, and an EXIT-trap footer listing local and `_WorkSpace` writes.
- [ ] ⚖️ Rule what `autoExecute: true` means
      If the human default is a safety property, overriding it should be recorded in `runtime.yaml` alongside the review skip. Today the flag exists and leaves no trace.
- [ ] 🚦 Rule when an agent MAY run without asking
      A no-op rerun, a cached-result check and a five-second script are not the case this rule was written for. Either state the exemptions or accept that the rule is routinely and correctly ignored.

## Where we are
Implemented and in daily use across the bank. The human default holds, the automatic record works
including on failure, and the two open items are both about the override rather than the rule.

- 260726 CC · 📝 Wrote down the reason for the asymmetry
      EXECUTE is the only phase with no review loop, and the reason (expensive plus irreversible) was implied by the design and stated nowhere. A rule whose reason is unwritten is a rule that gets optimized away.

## Files
- `ref/run-sh-template.sh`
  The canonical papermill runner: pre-flight gate, `runtime.yaml` snapshot, convert, papermill.
- `fn/run.md`
  The `run` verb and its logging conventions.
- `task-structure.md`
  The `runs/` rules, and the ban on mixing Template A with Template B.

## Log
260726 · Created with the board.
