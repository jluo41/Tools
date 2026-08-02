# Light or heavy: where an artifact is allowed to land
state: 🟡 PARTIAL
owner: JL
method: split by what a repository can carry, name the extensions, and keep a pointer where the thing itself may not go

## Opening
When a run produces a file, how does it decide whether that file goes in the repository or outside it? Two destinations exist: `results/<run>/` inside the task-folder, and `_WorkSpace/{N}-*Store/` outside the repository entirely. The rule is stated as light versus heavy, which sounds like a judgment call and is meant to be a list.

The cost of getting it wrong is asymmetric and that is why it is a hard error rather than a warning. A light file in `_WorkSpace/` is merely inconvenient: it is out of git and someone has to go find it. A heavy file in `results/` is committed, and a committed checkpoint is in the repository's history permanently, where it makes every later clone pay for it.

What keeps the rule usable is the pointer. A run that produces a model writes the model to `_WorkSpace/` and a `model_path.txt` to `results/`, so the repository still records that the run produced a model and where it went. Without that, the rule would be trading correctness for traceability, and it does not have to.

**Covered elsewhere**: What binds a run's outputs to its inputs is `QC1`; which notebook is the run record is `QC3`; the gate that would catch a violation is `QB5`; the `_WorkSpace/` store layout belongs to `/haipipe-data` and is not ruled here.

## Diagram
```
   TWO DESTINATIONS, decided by size and by repository policy

   📊 LIGHT   in-repo, results/<run>/
       metrics.json · eval logs · *.pdf *.png *.tex · *.csv
       report.md
       AND a POINTER to anything heavy the run produced

   💾 HEAVY   out-of-repo, _WorkSpace/{N}-*Store/
       *.pt *.ckpt *.safetensors        model weights
       *.npy *.pkl *.h5 *.bin           large arrays
       trained-instance folders · raw cohort tables

   ── the error is ASYMMETRIC, which is why one is HARD ──────
      light in _WorkSpace/    inconvenient. it is out of git and
                              somebody has to go find it.
      heavy in results/       PERMANENT. it is committed, it is in
                              history, and every later clone pays.

      so: heavy in results/ is a HARD ERROR, not a warning.

   ── the pointer keeps traceability ─────────────────────
      _WorkSpace/5-ModelInstanceStore/<instance>/     the model
      results/<run>/model_path.txt                    the pointer

      the repository still records that the run made a model and
      where it went. correctness without losing the trail.

   ── who would catch it, and does not ───────────────────
      the run script's EXIT footer PRINTS every file written, in
      both places, on success and on failure.  → QB4
      it prints. it does not judge.
      Gate 2 reads the results and could judge. it does not look.
                                                        → QB5
```

## Content
### The rule is a list, and lists are checkable
"Light versus heavy" reads as a judgment and the refs immediately turn it into extensions:
`.pt`, `.ckpt`, `.safetensors`, `.npy`, `.pkl`, `.bin`, `.h5`. That matters more than the phrasing,
because an extension list is a check a machine can run and a size heuristic is an argument.

Where it stays a judgment is the boundary case, and the honest answer is that the boundary case is
rare: a `.csv` is light and a `.h5` is heavy, and files that are genuinely ambiguous are unusual
enough to decide one at a time.

### The footer prints, and nothing judges
Every run already lists what it wrote, locally and in `_WorkSpace/`, on success and on failure.
So the information needed to catch a violation is produced by every run and read by nobody. The
gap between "printed in a log" and "checked" is the whole of this face's open work.

### The store layout is not ours
`_WorkSpace/{1-SourceStore, 2-RecStore, 3-CaseStore, 4-AIDataStore, 5-ModelInstanceStore,
6-EndpointStore}` belongs to the data and NN families. This layer decides only that heavy artifacts
go there, not what the numbered stores mean or how they are organized.

## Aims
- [ ] 🚨 Make the hard error actually hard
      An extension check over `results/` at Gate 2. The list exists, the gate exists, and they have never been connected.
- [ ] 📍 Require the pointer, not just permit it
      A run that writes to `_WorkSpace/` and leaves nothing in `results/` is traceable only through its log. The convention is described as a good practice and is not required.
- [ ] 📏 Rule the boundary case once
      A 200MB `.csv` passes the extension list and should not. Either add a size threshold on top of the list, or state that the list is the whole rule and accept the case.
- [ ] 🧹 Check the existing bank
      107 task-folders, none audited for this. A single committed checkpoint is already permanent, so the value here is knowing rather than fixing.

## States
The rule is documented in `hierarchy.md` and `authoring-conventions.md` §3 with an explicit
extension list, and `task-structure.md` calls a heavy artifact in `results/` a hard error caught by
inspection.

Nothing enforces it today. The run footer prints every file written in both destinations, which is
the raw material for a check nobody performs.

- 260726 CC · 📦 Wrote the asymmetry down
      The refs state the rule; they do not say why one direction is a hard error and the other is a nuisance. Permanence in git history is the reason, and it is the only argument that survives someone asking whether the rule could be relaxed.

## Files
- `authoring-conventions.md`
  §3, the heavy-artifact rule and the extension list.
- `hierarchy.md`
  The light/heavy split and the destination stores.
- `ref/run-sh-template.sh`
  The EXIT footer, which lists both destinations and judges neither.

## Log
260726 · Created with the board.
