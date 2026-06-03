scope: expmt
============

Project-level comparison-centric probe log. Aggregates the BEST runs
across all task-groups in a project into a single readable file that answers:

> "Of all the architectures / data / training tricks I've tried this project,
> which won on which split, by how much, and how confident am I?"

This scope migrates the prior `haipipe-project-expmtlog` skill into the
umbrella. Behavior preserved; the rest of this file is the canonical spec.


Commands
--------

```
/log expmt <project-path>                refresh the comparison table
/log expmt <project-path> --add <NAME>   add a specific run by name
/log expmt <project-path> --diff         show what would change vs current
```


Files this scope reads/writes
------------------------------

```
Reads:   <project>/tasks/*/configs/*.yaml                  (_meta)
         <project>/tasks/*/results/*/runtime.yaml          (facts)
         <project>/tasks/*/results/*/{metrics,summary,aggregated}.json
         <project>/tasks/*/grouplog.md                     (for context)
         <project>/diagram/probe-log.txt              (existing, preserved)

Writes:  <project>/diagram/probe-log.txt              (atomic overwrite)
```

The log is plain `.txt` (NOT .md) — keeps it canvas-friendly via
`diagram-ascii-canvas` and diff-clean in git.


File structure (top → bottom)
------------------------------

```
🧪 <ProjectName> — Full Probe Log
═══════════════════════════════════════

(intro: dataset, metric, period covered)


─§ Headline scoreboard ────────────────────────
   one-line summary table — best in each split per category


─§ <Task-group 1>  e.g. A01 — Baselines ──────
  one ─§ ID block per important probe, see entry template below


─§ <Task-group 2>  e.g. A02 — LHM family ─────
  ...


─§ Caveats and confounds (honest list) ───────
   bullet list of comparisons that are NOT apples-to-apples,
   reproducibility concerns, parser bugs, single-seed noise, etc.


─§ Where artifacts live ──────────────────────
   pointer to per-run JSON / forecast.json / checkpoint paths
```


Per-probe entry template
------------------------------

```
ID   <task-group>/<NAME> — <one-line description from _meta.purpose>
─────────────────────────────────────────────────
Data           <aidata version> · <split sizes> · <filter>
Architecture   <hidden / layers / heads / params>
Training       <epochs / LR / batch / optimizer / seed(s)>
Loss           <objective + any auxiliary terms>
Recipe notes   <framework / pretrain origin / warm-start ckpt>
Results        val / test-id / test-od  (or whatever splits exist)
                metric_1   X.XX  /  X.XX  /  X.XX
                metric_2   X.XX  /  X.XX  /  X.XX
                (include 1-3 diagnostic numbers per split)
Saved          <checkpoint path / forecast.json path>
Time           <wall-clock / hardware>
Notes          <anything weird, follow-ups, bugs encountered>
```

Keep each entry under ~25 lines. Link to deeper notes if needed.


Workflow
--------

```
Step 1: Locate or initialize.
  LOG=<project>/diagram/probe-log.txt
  mkdir -p $(dirname $LOG)
  [ ! -f $LOG ] && initialize from skeleton

Step 2: Decide which runs to include.
  Default: every run whose runtime.yaml has status=ok AND has a
           non-empty headline.
  --add <NAME>: just this one.

Step 3: For each candidate run, fill the entry template by
  reading:
    - configs/<NAME>.yaml (_meta + params)
    - results/<NAME>/runtime.yaml (timing, headline)
    - results/<NAME>/{metrics.json, summary.json, aggregated.json}
      (preference order; aggregated.json preferred when present, for
      multi-seed mean ± std)

Step 4: Run the caveats checklist (see below). Each YES becomes a
        bullet in the Caveats section.

Step 5: Re-derive the headline scoreboard. Mark with 🏆 the row
        that beats every other on a given split.

Step 6: Write atomically (tmp + mv). Do NOT silently rewrite older
        entries; if a number is now wrong (e.g., parser bug fix),
        strike-through with inline note and add the corrected entry.
```


Caveats checklist (mandatory pass per entry)
---------------------------------------------

Mentally check each before saving. Each YES becomes a bullet.

```
⚠️ Single seed?                            → flag noise floor uncertainty
⚠️ Compared against different framework?    → flag apples-to-oranges
⚠️ Different hyperparameter tuning?         → flag confound
⚠️ Different params count by >2x?           → flag scale confound
⚠️ Data parser bug history?                 → flag the fix
⚠️ Outlier seed?                            → note + show outlier-excluded analysis
⚠️ Loss differs from comparison group?      → flag objective confound
⚠️ Filter / split definition changed?       → flag dataset confound
```

"No confounds identified" must be stated explicitly if no caveats apply.


Multi-seed extension
---------------------

When the same probe was repeated with multiple seeds:

```
Results (mean ± std, N=<#seeds>):
   val      X.XX ± Y.YY
   test-id  X.XX ± Y.YY
   test-od  X.XX ± Y.YY
Paired-t vs baseline (seed-matched):
   val      Δ = -X.XX  p = 0.0XX  ✅ p<0.05
   test-id  Δ = -X.XX  p = 0.0XX
   test-od  Δ = -X.XX  p = 0.XXX  🟡 not significant
Sign test (more robust):    N/N seeds show negative Δ ← p = 2^(-N)
```

If an outlier seed dominates the t-test, report BOTH raw and
outlier-excluded analyses, with the diagnosis of why the outlier happened.


Anti-patterns
-------------

- ❌ Logging only the best metric without paired baseline Δ.
- ❌ Re-running the same probe with a new name to "fix" a result.
  If a number changes, add a corrected entry; don't overwrite history.
- ❌ Burying caveats in prose — they belong in the numbered Caveats section.
- ❌ Letting the log grow past ~500 lines. When it does, fold sub-tasks
  into their own per-task probe-log.txt and link.
- ❌ Using `.md` extension — table alignment breaks in some renderers.
  Stay with `.txt`.


Comparison-centric philosophy
-----------------------------

Most probe-tracking tools default to "one row per run." This skill
flips that: the **default view is the comparison table**, individual runs
are entries that feed into it.

When adding an probe, always ask:

1. What baseline does this beat? (Quote a number, not a vibe.)
2. What's the Δ on the headline metric across all splits?
3. Is the comparison apples-to-apples? If not, **flag the confound now**.
4. Is the result statistically meaningful, or single-seed?


Honest-caveats discipline
-------------------------

This is the differentiator vs MLflow / W&B. Those log what happened; this
scope insists on logging what's **uncertain** about what happened. Adding
caveats is **mandatory**, not optional.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "Refreshed probe-log.txt: <N> entries, <M> caveats"
artifacts: [path to probe-log.txt]
next:      suggested: /diagram-ascii-canvas to render headline scoreboard
```


See also
--------

- `diagram-ascii-canvas` — render the probe log into a visual canvas
- `analyze-results` — deeper post-hoc statistical analysis after logging
- `monitor-probe` — track RUNNING probes before they finalize
