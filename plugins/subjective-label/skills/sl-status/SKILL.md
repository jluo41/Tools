---
name: sl-status
description: "Read-only dashboard for a human-grounded subjective-labeling project. Shows lifecycle phase, open round, D_t/G_t, Session progress, audit and challenge evidence, seven-region coverage, stopping gates, sealed-test validity, executor scorecards, production provenance, implementation holds, and next valid action. Use for /sl-status or progress checks."
---

# Show subjective-label project status

Read state without modifying artifacts, opening seals, rerunning models, or advancing a
phase.

## Read first

Read `../../ref/ref-output-style.md`, `../../ref/ref-assets.md`, and
`../../ref/ref-stages.md`.

Resolve the project directory and inspect, when present:

- `REPORT.md`, `config.yaml`, and `.state.json`;
- latest closed policy manifest and guideline components;
- cumulative human gold;
- open and recent round manifests, Session progress, checkpoints, policy diffs, audit
  and challenge metrics, coverage, and risk ledger;
- sealed-test status and access log metadata without reading protected ids or labels;
- evaluation registry, validity, and scorecards;
- production manifest, terminal dispositions, risk queue, and final audit;
- migration receipts and implementation holds.

## Output

Lead with:

```text
project {id} · state {state} · round {round/phase}
policy {G_t/G*} · human gold {n} · unresolved {n}
quality {gate} · stability {gate/streak} · coverage {gate} · risk {gate}
sealed test {reserved/frozen/released/valid/invalid}
next {single valid action}
```

Then show only relevant detail:

- H/L/N and seven-region coverage;
- audit and challenge metrics in separate rows;
- consensus-audit shared errors;
- last material guideline diff and backward-impact result;
- executor qualification and scorecard summary after evaluation;
- terminal/provenance shares and final-audit findings during completion;
- explicit `HOLD` entries with missing capability and preserved state.

Distinguish `not started`, `pending human`, `HOLD`, `failed`, `invalid`, and `complete`.
Never infer success from missing files, model consensus, a legacy kappa field, or a
rendered report that conflicts with canonical records.

Recommend exactly one next valid command or human decision based on the state machine.
