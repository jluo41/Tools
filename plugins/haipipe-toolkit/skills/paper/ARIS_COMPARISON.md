# HAI-Pipe Paper vs ARIS

ARIS is an autonomous research workflow (idea > experiment > review > paper > rebuttal). HAI-Pipe paper is a manuscript-state system (pitch > narrative > minimap > draft > edit > review, with loopback to the earliest broken layer). They are compatible but organize work differently.

## Core difference

| | ARIS | HAI-Pipe paper |
|---|---|---|
| Optimizes for | Autonomous forward motion | Story reliability + state correction |
| Main unit | Workflow stage | Paper folder state |
| Evidence lives in | Workflow logs, research wiki | Project-level probes/tasks/discoveries; claim gaps buffer in `1-probe-plans/`, batch-dispatch to probe |
| Review means | Fix weaknesses, rerun | Diagnose earliest broken layer, loop back |
| Story state | Implicit in NARRATIVE_REPORT | First-class `0-lifecycle/1-pitch/` with provenance |

## Workflow mapping

```text
ARIS                          HAI-Pipe paper
W1   Idea Discovery      ->   Outside paper > seed/pitch
W1.5 Experiment Bridge    ->   Outside paper > probes/tasks > narrative
W2   Auto Review Loop     ->   Review gate (routes to pitch/narrative/plan/edit)
W3   Paper Writing        ->   pitch > narrative > minimap > write/edit (the whole convergence loop)
W4   Rebuttal             ->   respond/revise
W5   Resubmit             ->   submit + architecture-level transformation
W6   Conference Talk      ->   present (reads pitch first)
```

## File-state mapping

| ARIS artifact | HAI-Pipe equivalent | Note |
|---|---|---|
| `IDEA_REPORT.md` | seed, upstream discoveries, pitch seed | Candidate pools stay upstream |
| `EXPERIMENT_PLAN/LOG.md` | probes/tasks feeding narrative | Paper cites evidence summaries, not run logs |
| `NARRATIVE_REPORT.md` | `0-lifecycle/3-narrative/3-narrative.tex` | Strong overlap; HAI-Pipe adds pitch upstream |
| `PAPER_PLAN.md` | `0-lifecycle/5-minimap/5-minimap.tex` | In HAI-Pipe, downstream of pitch + narrative |
| `figures/`, `latex_includes.tex` | `0-displays/displayNN-*/` | Display units with claim, caption, preview |
| `AUTO_REVIEW.md` / `REVIEW_STATE.json` | review reports, `1-rounds/` | HAI-Pipe routes findings by layer |
| `research-wiki/` | project KB / discoveries / insights | HAI-Pipe path: discovery > insight > narrative > pitch |

## Review routing (the key difference)

| Finding | ARIS | HAI-Pipe |
|---|---|---|
| Unclear intro | Rewrite intro | Check pitch first; if pitch unclear, fix pitch then intro |
| Claim too strong | Soften text | Update claims/narrative, then edit |
| Need more ablation | Run experiment | Buffer probe plan > dispatch > verdict backfills |
| Lacks contribution focus | Rewrite abstract | Reopen pitch and narrative |

## Integration model

Use ARIS as upstream engine + audit discipline. Use HAI-Pipe as the paper state model.

```text
ARIS-like research work (idea, experiment, review, wiki)
        |
        v
HAI-Pipe paper folder
  0-lifecycle/{0-seed..5-minimap}/
  0-sections/*.tex
  0-displays/displayNN-*/
  1-probe-plans/PPNN_*.md       <- buffered evidence needs, batch-dispatched to probe
  1-rounds/vYYMMDD/
```

When upstream evidence arrives, update paper in this order: (1) does the pitch change? (2) do claims change? (3) does narrative change? (4) do displays change? (5) does minimap change? Then edit the TeX.

## What to borrow from ARIS

1. Reviewer independence (read artifacts cold)
2. Assurance levels (draft mode vs submission mode)
3. Verdict schemas (PASS/WARN/FAIL)
4. Resumable long runs
5. Edit whitelists for constrained phases

## What not to copy

1. Paper folder as project-wide research cockpit (keep upstream work upstream)
2. Collapsing pitch into narrative (pitch is a distinct one-minute artifact)
3. PAPER_PLAN as the first planning file (pitch and narrative come first)
4. Routing all review findings into editing (some need upstream evidence work)
