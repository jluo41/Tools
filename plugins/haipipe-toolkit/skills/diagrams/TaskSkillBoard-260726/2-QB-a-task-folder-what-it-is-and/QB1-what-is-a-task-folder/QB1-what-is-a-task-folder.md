# What makes a directory a task-folder
state: 🟡 PARTIAL
owner: JL
method: test by structure, never by name, and say what the name convention is actually for

## Opening
Given a directory, how do you know whether it is a task-folder? Everything else in this layer depends on the answer: the router picks a scope from it, group iteration enumerates from it, and an audit walks from it. Get it wrong in the cheap way and 31% of the bank becomes invisible.

The cheap way is to match the name. `{NN}_{task_name}` is the documented convention and it holds for 235 of 342 real folders, which is exactly the ratio that makes a name filter feel safe. It is not: `B4_fit_scaling_law`, `C3-Visual-ForecastScaling`, `B6f_crosscompare` and `A4_data_population_comparison` are all real task-folders, and every one of them is skipped by a `{NN}_*` glob.

So the test has to be structural, and the interesting part is that the structural test is not merely safer, it is also the correct definition. A task-folder is a directory that holds runnable work. That is what the router needs to know, it is what the name was only ever a hint about, and it excludes `__pycache__`, `figures/`, `sbatch/` and `diagram/` for free.

**Covered elsewhere**: What a task-folder contains once identified is `QA6`'s neighbourhood and the `QC` group; the four phases it runs are `QB2` to `QB5`; the naming and indexing rules themselves are `hierarchy.md`'s and are not re-ruled here.

## Diagram
```
   THE TEST.   structure, never the name.

   a directory is a TASK-FOLDER if ANY of:
        a *.py at its root          ← the usual case
        workflow/                   ← it has been planned
        results/                    ← it has been run
        configs/                    ← it has been configured
        runs/                       ← it has a runner

   it is a TASK-GROUP if it holds task-folders and has NO *.py of its own.

   ── what the name filter costs ──────────────────────────────
      {NN}_ matches            235 of 342     69%
      real folders it skips    107            31%
        B4_fit_scaling_law · C3-Visual-ForecastScaling
        B6f_crosscompare   · A4_data_population_comparison

      and it fails SILENTLY, by finding fewer things. A group
      iteration that skips a third of its children reports success.

   ── what the structural test excludes, for free ────────────
      __pycache__/  figures/  sbatch/  diagram/  _archive/
      none of them hold work, so none of them need a rule.

   ── so what IS the name convention for? ─────────────────────
      SORTING, and nothing else. 2 digits, start at 01, no gaps at
      scaffold, forward-fill on deletion so existing references
      keep resolving. It orders `ls`; it does not define membership.
      Confusing those two is the whole bug.
```

## Content
### The test is a definition, not a heuristic
"A directory that holds runnable work" is what the router actually needs to decide, and the five
structural markers are five ways a directory can show that it does. That is why the structural
test is not a defensive workaround for a leaky name convention: it is the definition, and the name
was always a summary of it.

### The failure mode is the dangerous kind
A name filter does not crash. It returns a shorter list, and every downstream step reports success
over that shorter list. A group iteration that silently skips four of twelve children prints
`Overall: 8 ok, 0 failed`, which is indistinguishable from a correct run of an eight-child group.

`SKILL.md` carries this as a hard stop in two places, Step 2 and Step 3d, both with the ⛔ marker
and the 31% number. That is the right emphasis and it is worth noticing that it needed saying
twice, in a document that says most things once.

### Forward-fill, and why a gap is correct
The indexing rule that surprises people: when `02_foo` is deleted, `03_bar` is NOT renumbered.
References in papers, runs and notebooks point at task names, so renaming breaks them, and a gap
in the numbering costs nothing but tidiness.

That is the same instinct as the structural test, one level up. The number is for sorting. It is
not an identifier, and anything that treats a contiguous sequence as meaningful has made the name
load-bearing again.

## Aims
- [x] 🧪 The structural test is stated and used
      Five markers, in `SKILL.md` Step 2 and the Step 3d enumeration snippet, with the 31% figure attached to both.
- [ ] 🔍 Verify no code path still globs the name
      The rule is written twice in `SKILL.md`; whether every `fn/` file, every specialist and `ref/scan_status/scan_status.py` obey it has not been checked. One surviving glob reintroduces the whole failure.
- [ ] ⚖️ Rule the ambiguous case: a directory with only `diagram/`
      It holds no work by the test, so it is not a task-folder. It is also not a group, since it holds no children. Today it is simply invisible, which may be right and is not stated.
- [ ] 📏 Say out loud what the name convention IS for
      Sorting. The refs describe the convention in detail and never say that membership is not part of its job, which is exactly the gap the bug grows in.

## States
The rule is settled and stated; the enforcement is partial. `SKILL.md` carries the structural test
twice with its cost measured, and 107 task-folders are detected by it across 67 groups.

What has not been done is the sweep: no one has checked that every other file in the family, and
the status scanner in particular, uses structure rather than the name.

- 260726 CC · 🧪 Recorded the 31% as the load-bearing number
      It is what turns "prefer structure" from a style preference into a correctness rule, and it is the reason the ⛔ appears twice in one document.

## Files
- `SKILL.md`
  Step 2's cascade and Step 3d's enumeration snippet: both carry the test and the ⛔.
- `hierarchy.md`
  The naming and indexing rules, including forward-fill on deletion.
- `ref/scan_status/scan_status.py`
  The status scanner, which walks the bank and has not been checked against this rule.

## Law
A task-folder is detected by STRUCTURE and never by NAME. The test is: a `.py` at its root, or
`workflow/`, `results/`, `configs/` or `runs/`. A directory holding task-folders and no `.py` of
its own is a task-group.

The `{NN}_` convention is for SORTING. It is not a membership filter, and a glob on it silently
skips 31% of real task-folders while reporting success.

## Log
260726 · Created with the board.
