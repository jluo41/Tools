# Lesson 19: Reuse prior-run artifacts on identical sources — but say so

## The Problem
A "new" figure (`Figure1-v0701-v4.png`) was actually byte-identical (same MD5) to a previously
processed one (`Figure1-v0701-v3.png`) — only the filename and folder differed. The run correctly
reused the prior run's 37 regenerated + sliced icons, skipping ~10 codex image-gen calls.

## The Symptom
The user watched the run and saw no `redraw_icon/` grids, no generation logs, no
`figures/ai_generated/` — and concluded the pipeline was broken ("为啥没看到 redraw 的带 3x3 的
icon 呢"). The reuse was invisible: nothing announced that Step 2 had been satisfied from a
previous run.

## The Solution
Before regenerating, checksum the source and search for prior `*_regenerated/` runs of the same
figure (renamed copies count — compare checksums, not filenames). On an identical match, reuse
the sliced icons and announce it explicitly: "Step 2 skipped — reusing N icons from <path>,
source checksums match." On a changed source, regenerate (at least the affected parts).

## Why It Works
Image-gen is the most expensive, slowest step; identical input ⇒ identical valid output, so reuse
is pure savings. But an invisible skip is indistinguishable from a silent failure — the
announcement is what converts "broken?" into "smart". Checksums, not filenames: version-suffixed
copies of the same file are common.

## When to Apply
Any run where the source figure may have been processed before — check `_workspace/`, earlier
version folders, and sibling project dirs before every Step 2.

## Caveats
Reuse only on byte-identical sources (or after verifying the changed regions don't touch the
icons). Icons the prior run got wrong still need fresh regeneration — reuse the good ones, redo
the bad. The fresh-eyes review (Step 6) still runs on everything, reused or not.
