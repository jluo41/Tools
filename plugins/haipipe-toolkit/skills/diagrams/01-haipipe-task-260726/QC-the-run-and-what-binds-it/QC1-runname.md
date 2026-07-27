# RUNNAME: four sister files, one token
state: 🟡 PARTIAL
owner: JL
method: one token names one execution in four folders, and every tool depends on the pairing rather than on a lookup

## Question
What holds one execution together, when its parts live in four different folders? A run is not a folder. It is a NAME, and that name appears as the filename in `configs/`, in `runs/`, as the directory in `results/` and as the notebook in `notebooks/`. Nothing links them but the shared token, and every tool in the layer relies on that.

This is the layer's most load-bearing convention and its least defended one. `run-sh-template.sh` hard-codes `CONFIG="configs/${RUN_NAME}.yaml"`, so a config whose name drifts from its runner does not produce a warning, it produces a run against the wrong parameters, or no run at all. There is no registry, no manifest and no index: the pairing IS the data structure.

What makes it worth a page rather than a line in a ref file is that the convention is invisible at the moment it is broken. Renaming one of the four is a normal, tidy-looking edit, and the failure surfaces later as a result directory that does not match anything.

## Boundary
- ✅ Covered here
  What the four sisters are, what binds them, what breaks when one drifts, and what the token may contain.
- ↪ Covered elsewhere
  Where each sister's contents go is `QC2`; which notebook is the record is `QC3`; who starts the run is `QB4`; the `<NAME>` token's own grammar is `authoring-conventions.md` §1 and is not restated here.

## Diagram
```
   RUNNAME = run_5m_ep0.1        ONE token, FOUR folders, no index

     configs/run_5m_ep0.1.yaml       📥 inputs      config + args
     runs/run_5m_ep0.1.sh            ▶️ entry       bash: convert + papermill
     results/run_5m_ep0.1/           📊 outputs     light artifacts   → QC2
     notebooks/run_5m_ep0.1.ipynb    📓 record      papermill output  → QC3

   one entity in four projections. change the name and you change all four.

   ── why it is fragile ──────────────────────────────────
      run-sh-template.sh hard-codes
          CONFIG="configs/${RUN_NAME}.yaml"
          RUN_NAME="$(basename "$0" .sh)"

      so the runner DERIVES its config from its own filename.
      rename runs/run_5m.sh → runs/run_5m_v2.sh and it silently
      looks for configs/run_5m_v2.yaml, which does not exist.

      there is no registry. no manifest. no index.
      THE PAIRING IS THE DATA STRUCTURE.

   ── the three identity axes ────────────────────────────
      Project   examples/Proj{...}/                    a folder
      Task      tasks/{G}{NN}_{name}/{NN}_{task}/      a folder
      Run       <run_name>                             A NAME
                                                       ← the odd one out

      two of the three are places you can cd into. the third exists
      only as a string repeated in four filenames.

   ── what a rename actually costs ───────────────────────
      it is a normal, tidy-looking edit
      it fails LATER, not at the edit
      it fails as "results/ has a directory matching nothing"
      nothing warns, because nothing is watching the set
```

## Content
### The pairing is the data structure, and that is a real design choice
There is an alternative and it was not taken: a manifest listing every run with its config, its
script and its outputs. The convention is cheaper, needs no maintenance, and cannot itself go
stale, because it stores nothing. What it gives up is any ability to detect its own violation.

That trade is defensible for a repository of scripts and it stops being defensible the moment
something automated walks the set, which is what `scan-status` and any board over a task-folder
would both do.

### What the token is allowed to be
`run_`-prefixed snake_case, unique within the task-folder. The grammar lives in
`authoring-conventions.md` §1 and the useful part to know here is that uniqueness is scoped to the
folder, not the group or the project, so two sibling folders may both hold `run_baseline` and
mean different things.

### The one check that would close it
Listing the four sisters and reporting any token that does not appear in all four is a few lines,
and it is exactly what `audit` should be doing. `fn/audit.md` exists and audits structure against
the four-sister contract; whether it verifies the token set or only that the folders exist has not
been checked.

## Items to Finish
- [ ] 🔍 Verify whether `audit` checks the token SET or only the folders
      The whole convention's enforcement rests on this and nobody has looked. If it only checks that `configs/` exists, the four-sister contract is documentation.
- [ ] 🧮 Report orphans in both directions
      A config with no runner, and a `results/` directory matching no run script. The second is the common one, since results outlive the scripts that made them.
- [ ] 📐 State that uniqueness is folder-scoped
      Two siblings may both have `run_baseline`. Anything that aggregates across a group, including a board over one, has to key by folder and run, not by run.
- [ ] 🧪 Rename one sister and confirm it fails loudly
      The acceptance test. Today the expected result is a silent failure, which is what this face is about.

## Where we are
The convention is documented in three places, `hierarchy.md`, `task-structure.md` and
`authoring-conventions.md`, and implemented in `run-sh-template.sh`, which derives the config path
from the script's own filename.

Enforcement is unverified. `fn/audit.md` audits against the four-sister contract, and whether that
includes the token set is the open question above.

- 260726 CC · 🧷 Named the pairing as the data structure
      The refs describe the four sisters as a convention. Calling it the data structure is what makes the fragility legible: there is no second place where the relationship is written, so an inconsistency is not a mismatch with a record, it is simply the truth changing.

## Files
- `ref/run-sh-template.sh`
  Derives `RUN_NAME` from its own filename and `CONFIG` from `RUN_NAME`.
- `authoring-conventions.md`
  §1, the four sister files and the `<NAME>` token grammar.
- `fn/audit.md`
  The structural audit against the four-sister contract.

## Log
260726 · Created with the board.
