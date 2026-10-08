Scorecard: an Exp's per-arm totals, the scores, and the sum per method version
===============================================================================

(JL 261007, b12 s11: "what the Exp returns lands once, in the Block".) The Exp spans Jobs, so it is never copied
per Job. The files, all at the Block:

```text
observed/eNN_<exp>/            run-add-observed-e<NN> (soft)
├── arms.csv                   arm · job · design · n · observed      per-arm totals only, never rows
├── source.md                  where they came from: an insight Block's signed handoff, or a vendor's per-arm report
└── manifest.yaml              exp · frozen · files (path · sha256)
runs/run-score-eNN/            run-score-e<NN> (soft, the reviewer agent; keeps scores.csv in its own folder)
├── run.yaml
└── scores.csv                 job · design · predicted · observed · direction · in_range · error
```

`arms.csv`: one row per arm. `job` and `design` name the design the arm sent (`j03`, `d04`); the control arm, or an
arm with no design of ours, leaves them empty or says `control`. `observed` is the arm's effect against the control
as `<point> [<lo>; <hi>]`, or its rate.

`scores.csv`, one row per arm with a design, scored against that design's `prediction.yaml` (`predicted`, frozen at
the release by `run-freeze-predictions-j<NN>`):

```text
direction   ✓ the observed sign is the predicted sign · ✗ it is not · ? either is not stated
in_range    ✓ the observed point is inside the predicted [lo; hi] · ✗ outside · ? a bound or the point is missing
error       observed point − predicted point, signed, 2 decimals · ? when either is not a number
```

A prediction still `frozen: draft` is not scored: only a released design was sent. Scoring again (a corrected
`arms.csv`) moves the old `scores.csv` into the Run's `passes/` first; the script never overwrites.

**The scorecard** sums `scores.csv` per method version, reading each Job face's `method:`: designs scored (a row
whose prediction or observed value scores `?` is listed but not counted), right direction, in the predicted range. The Block's Audience Report › Method scorecard shows it; a version that loses is a
trigger for `run-propose-method-<slug>` (SKILL.md, How a method evolves).
