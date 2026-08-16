# Two notebooks, and which one is the record
state: 🟡 PARTIAL
owner: JL
method: the .py is the source, both notebooks are build artifacts, and only one of them holds what happened

## Opening
A task-folder holds two kinds of `.ipynb`. Which is the record of what happened, and which is disposable? One sits at the task root beside the `.py`; the other sits in `notebooks/`, one per run. They have the same extension, they open in the same editor, and they mean entirely different things.

Getting it backwards is easy and costs the run record. The template at the root is regenerated from the `.py` on every single run, so anything typed into it is destroyed by the next execution. The one in `notebooks/` is papermill's output: it carries the injected parameters, the stdout, the errors and the figures, and it IS what happened. Editing the first loses work silently; trusting the first as evidence means reading a file with no execution state at all.

Underneath both is one rule that removes most of the confusion: the `.py` is the source of truth and both notebooks are build artifacts. The template exists so an author can READ the cell flow during review, not so anyone can edit it.

**Covered elsewhere**: The token that pairs `notebooks/<run>.ipynb` with its runner is `QC1`; what else a run writes is `QC2`; who starts the run is `QB4`.

## Diagram
```
   TWO NOTEBOOKS, TWO ROLES.   the .py is the source of both.

   🐍 {task}/{NN}_{task_name}.py          ← THE SOURCE. edit only this.
        │
        ├──▶ {task}/{NN}_{task_name}.ipynb        TEMPLATE, at the task ROOT
        │      no execution state
        │      REGENERATED ON EVERY RUN           ← anything typed here dies
        │      exists so an author can READ the cell flow
        │
        └──▶ {task}/notebooks/<run>.ipynb         EXECUTION, one per run
               papermill output
               injected parameters · stdout · errors · figures
               👑 THIS IS THE RUN RECORD

   ── the authoring loop ─────────────────────────────
      author edits .py ──▶ convert ──▶ reads the template .ipynb
           ↑                                    │
           └────────── identifies what to change ┘

      the template is for READING. the loop always returns to the .py.

   ── why the log is not a log, in papermill mode ────────
      Template A (nbconvert)  exec > >(tee log)   → results/<run>/0-*.log
      Template B (papermill)  NO tee              → the NOTEBOOK is the log

      and task-structure.md forbids MIXING them in one task, because
      a mixed task has half its story in a log and half in a notebook.

   ── the retention knob ─────────────────────────────
      _meta.notebook: full | thin | off
      default policy gitignores notebooks/ and _WorkSpace/.

      ⚠️ so the RUN RECORD is, by default, not committed.
         that is a defensible size decision and it means the record
         of what happened lives only on the machine that ran it.  → Items
```

## Content
### One source, two artifacts
The rule that makes the rest follow: edit the `.py`, never either notebook. The template is
regenerated on every run; the execution record is written by papermill and is not a thing anyone
should be typing into either.

That also explains why the template lives at the task root rather than in `notebooks/`. It sits
next to its `.py` so opening the folder shows source and template side by side, and so that
`notebooks/` contains only records.

### The record is not committed by default
Worth stating plainly because it is the surprising consequence. `notebooks/` is gitignored under
the default policy, so the canonical record of what happened during a run exists on the machine
that ran it and nowhere else. The retention knob (`full`, `thin`, `off`) controls how much is kept
locally, not whether it is shared.

For a run whose numbers end up in a paper, that is the difference between a reproducible claim and
a remembered one. Whether that is acceptable is a real question and it has not been asked.

### The two templates and the ban on mixing
Template A tees a log because there is no notebook to hold it. Template B does not, because the
notebook holds it. Mixing them in one task produces a folder where some runs are logged and others
are recorded, and no single place tells you which.

## Aims
- [ ] 💾 Rule what happens to the record of a run that matters
      `notebooks/` is gitignored by default, so a published number's execution record is local-only. Either that is accepted and said out loud, or runs that feed a claim need a retention exception.
- [ ] 🚫 Check that no task mixes Template A and Template B
      The ban is stated in `task-structure.md`. Across 107 folders it has never been verified, and a mixed folder is the one where the record question above becomes unanswerable.
- [ ] 📌 State the edit rule where an editor would see it
      The template is regenerated on every run. Nothing in the template says so, so the first person to edit one loses their work and learns the rule the expensive way.

## States
Both notebooks are produced correctly by the run script, and the conceptual split is documented in
`hierarchy.md` and `task-structure.md`.

The open items are all about what survives: the record is gitignored by default, the no-mixing rule
is unverified across the bank, and nothing warns an editor that the template is disposable.

- 260726 CC · 👑 Named the execution notebook as the record
      Both refs describe the two roles. Stating which one is evidence is what makes the gitignore default a question rather than a detail.

## Files
- `hierarchy.md`
  "Two notebooks, two roles", and the authoring loop.
- `task-structure.md`
  The `notebooks/` rules, the two build modes, and the ban on mixing templates.
- `authoring-conventions.md`
  §7, the retention knob and the commit/gitignore policy.

## Log
260726 · Created with the board.
